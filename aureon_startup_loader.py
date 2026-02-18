"""
AUREON STARTUP LOADER
Imports and activates ALL Python modules in C:\\AUREON_AUTONOMOUS at boot time.
These are Aureon's body parts - ears, eyes, heart, nerves, spine, etc.
They must ALL be live and integrated before communication begins.

Usage: Called from aureon_web_interface.py AFTER brain init, BEFORE chat starts.
    from aureon_startup_loader import activate_all_modules
    modules = activate_all_modules(brain)
"""

import sys
import os
import importlib
import importlib.util
import traceback
from pathlib import Path
from typing import Dict, Any, Optional


# Modules that should NOT be auto-imported (they are loaded separately or cause conflicts)
SKIP_MODULES = {
    "aureon_brain",           # Already loaded as the brain
    "aureon_web_interface",   # The web server itself
    "aureon_hands",           # Already loaded by brain
    "aureon_autonomous",      # Entry point, not a module
    "setup",                  # Package setup files
    "conftest",               # Test config
    "__init__",               # Package inits
}

# Modules that should be connected to the brain as named subsystems
BRAIN_SUBSYSTEMS = {
    "aureon_ears":          "ears",
    "aureon_eyes":          "eyes",
    "aureon_heart":         "heart",
    "aureon_body":          "body",
    "aureon_nerves":        "nerves",
    "aureon_spine":         "spine",
    "aureon_vision":        "vision",
    "aureon_soul":          "soul",
    "aureon_voice":         "voice",
    "aureon_memory":        "memory",
    "aureon_dreamer":       "dreamer",
    "aureon_rl_core":       "rl_core",
    "aureon_agency_safety_shell": "safety_shell",
    "aureon_hallucination_firewall": "hallucination_firewall",
    "aureon_temporal_coherence": "temporal_coherence",
    "aureon_external_organs": "external_organs",
    "aureon_kernel_loader":  "kernel_loader",
    "coherence_arbiter":     "coherence_arbiter",
    "paradox_integration_layer": "paradox_integrator",
    "pi_density_operators":  "pi_density",
    "llm_life_support_stabilizer": "life_support",
    "router":                "router",
    "solid_state_ignorance": "ignorance_kernel",
}


def import_module_from_file(filepath):
    """Import a Python module from its file path."""
    path = Path(filepath)
    module_name = path.stem
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"   [WARN] {module_name}: {type(e).__name__}: {str(e)[:100]}")
        return None


def find_main_class(module):
    """Find the primary class in a module (usually named Aureon* or matches module name)."""
    module_name = module.__name__
    
    # Look for class matching module name (e.g., aureon_ears -> AureonEars)
    expected_class = ''.join(word.capitalize() for word in module_name.split('_'))
    
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type):
            if name == expected_class:
                return obj
            if name.replace('_', '').lower() == module_name.replace('_', '').lower():
                return obj
    
    # Fallback: return first class defined in THIS module (not imported)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and not name.startswith('_') and not issubclass(obj, Exception):
            if obj.__module__ == module.__name__:
                return obj
    
    return None


def activate_all_modules(brain, base_dir=None):
    """
    Import and activate ALL Python modules in AUREON_AUTONOMOUS.
    Connects subsystems to the brain. Returns status dict.
    """
    if base_dir is None:
        base_dir = str(getattr(brain, 'base_dir', r'C:\AUREON_AUTONOMOUS'))
    
    base_path = Path(base_dir)
    if not base_path.exists():
        return {"ok": False, "error": f"Directory not found: {base_dir}"}
    
    # Add base_dir to Python path so modules can import each other
    base_str = str(base_path)
    if base_str not in sys.path:
        sys.path.insert(0, base_str)
    
    foundation_path = base_path / "AUREON_FOUNDATION"
    if foundation_path.exists() and str(foundation_path) not in sys.path:
        sys.path.insert(0, str(foundation_path))
    
    results = {
        "ok": True,
        "imported": [],
        "connected": [],
        "failed": [],
        "skipped": [],
    }
    
    print("\n   === AUREON MODULE ACTIVATION ===")
    
    # PHASE 1: Import all .py files from base directory
    py_files = sorted(base_path.glob("*.py"))
    print(f"   Found {len(py_files)} Python modules in {base_dir}")
    
    modules = {}
    
    for py_file in py_files:
        name = py_file.stem
        if name in SKIP_MODULES or name.startswith("__"):
            results["skipped"].append(name)
            continue
        
        module = import_module_from_file(str(py_file))
        if module:
            modules[name] = module
            results["imported"].append(name)
        else:
            results["failed"].append(name)
    
    print(f"   [OK] Imported: {len(results['imported'])} modules")
    if results["failed"]:
        print(f"   [WARN] Failed: {len(results['failed'])} ({', '.join(results['failed'][:10])})")
    
    # PHASE 2: Connect subsystems to brain
    for module_name, attr_name in BRAIN_SUBSYSTEMS.items():
        if module_name not in modules:
            continue
        
        module = modules[module_name]
        
        # Skip if brain already has this subsystem
        existing = getattr(brain, attr_name, None)
        if existing is not None:
            continue
        
        main_class = find_main_class(module)
        if main_class:
            try:
                instance = None
                try:
                    instance = main_class()
                except TypeError:
                    try:
                        instance = main_class(brain=brain)
                    except TypeError:
                        try:
                            instance = main_class(hands=brain.hands)
                        except TypeError:
                            pass
                
                if instance:
                    setattr(brain, attr_name, instance)
                    results["connected"].append(attr_name)
            except Exception as e:
                print(f"   [WARN] {attr_name}: {e}")
        else:
            # No class but module is imported - store as module reference
            setattr(brain, f"_{attr_name}_module", module)
    
    print(f"   [OK] Connected to brain: {len(results['connected'])} subsystems")
    if results["connected"]:
        print(f"   Subsystems: {', '.join(results['connected'])}")
    
    # PHASE 3: Import .py from AUREON_FOUNDATION subdirectories
    foundation_count = 0
    if foundation_path.exists():
        for py_file in sorted(foundation_path.rglob("*.py")):
            name = py_file.stem
            if name in SKIP_MODULES or name.startswith("__") or name in modules:
                continue
            module = import_module_from_file(str(py_file))
            if module:
                modules[name] = module
                foundation_count += 1
    
    if foundation_count:
        print(f"   [OK] Foundation modules: {foundation_count}")
    
    # Store on brain
    brain._loaded_modules = modules
    brain._module_count = len(modules)
    
    total = len(results["imported"]) + foundation_count
    print(f"\n   === ACTIVATION COMPLETE: {total} modules live ===\n")
    
    return results


if __name__ == "__main__":
    print("AUREON STARTUP LOADER - Dry run")
    base = Path(r"C:\AUREON_AUTONOMOUS")
    if base.exists():
        py_files = sorted(base.glob("*.py"))
        print(f"Found {len(py_files)} Python modules:")
        for f in py_files:
            skip = " (SKIP)" if f.stem in SKIP_MODULES else ""
            sub = BRAIN_SUBSYSTEMS.get(f.stem, "")
            if sub:
                sub = f" -> brain.{sub}"
            print(f"  {f.name}{skip}{sub}")
