#!/usr/bin/env python3
"""
AUREON SYSTEM LOADER - COMPLETE VERSION
Loads ALL systems from repos, skips agent output spam
"""

import sys
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Any
import json

BASE_DIR = Path('C:\\AUREON_AUTONOMOUS')
REPOS_DIR = BASE_DIR / 'github_repos'

class AureonSystemLoader:
    """Dynamically load all systems from repos"""
    
    def __init__(self):
        self.loaded_modules = {}
        self.loaded_classes = {}
        self.loaded_functions = {}
        self.active_systems = {}
        self.kernel_configs = {}
        
        print("=" * 80)
        print("? AUREON SYSTEM LOADER")
        print("=" * 80 + "\n")
    
    def discover_and_load_all(self):
        """Load everything"""
        print("[PKG] LOADING PYTHON MODULES\n")
        self._load_all_python_modules()
        
        print("\n? LOADING CONFIGS\n")
        self._load_kernel_configs()
        
        print("\n? INITIALIZING SYSTEMS\n")
        self._initialize_systems()
        
        self._print_summary()
    
    def _load_all_python_modules(self):
        """Load all .py files from repos"""
        if not REPOS_DIR.exists():
            print(f"[WARN]?  No repos: {REPOS_DIR}")
            return
        
        python_files = list(REPOS_DIR.rglob("*.py"))
        print(f"Found {len(python_files)} Python files\n")
        
        for py_file in python_files:
            if '__pycache__' in str(py_file) or 'test_' in str(py_file):
                continue
            
            self._load_python_file(py_file)
    
    def _load_python_file(self, filepath: Path):
        """Load single Python file"""
        try:
            relative = filepath.relative_to(REPOS_DIR)
            module_name = str(relative).replace('\\', '.').replace('/', '.').replace('.py', '')
            
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                self.loaded_modules[module_name] = module
                
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if obj.__module__ == module_name:
                        full_name = f"{module_name}.{name}"
                        self.loaded_classes[full_name] = obj
                        print(f"  [OK] Class: {full_name}")
                
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if obj.__module__ == module_name:
                        full_name = f"{module_name}.{name}"
                        self.loaded_functions[full_name] = obj
        except:
            pass
    
    def _load_kernel_configs(self):
        """Load configs, skip agent output spam"""
        json_files = list(REPOS_DIR.rglob("*.json"))
        
        skipped = 0
        for jf in json_files:
            if '__pycache__' in str(jf):
                continue
            
            # SKIP AGENT OUTPUT SPAM
            if 'agent_' in jf.stem and '_output' in jf.stem:
                skipped += 1
                continue
            
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.kernel_configs[jf.stem] = config
                    print(f"  [OK] Config: {jf.stem}")
            except:
                pass
        
        if skipped > 0:
            print(f"\n??  Skipped {skipped} agent output files\n")
        
        # Load MD kernels
        md_files = list(REPOS_DIR.rglob("*KERNEL*.md"))
        md_files.extend(list(REPOS_DIR.rglob("*ENGINE*.md")))
        
        for md in md_files:
            try:
                with open(md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.kernel_configs[md.stem] = {'type': 'markdown', 'content': content}
                    print(f"  [OK] Kernel: {md.stem}")
            except:
                pass
    
    def _initialize_systems(self):
        """Initialize systems"""
        system_patterns = [
            'Engine', 'Firewall', 'System', 'Manager', 'Controller',
            'Handler', 'Processor', 'Analyzer', 'Generator', 'Validator'
        ]
        
        for class_name, class_obj in self.loaded_classes.items():
            if any(pattern in class_name for pattern in system_patterns):
                try:
                    instance = class_obj()
                    self.active_systems[class_name] = instance
                    print(f"  ? Initialized: {class_name}")
                except TypeError:
                    try:
                        instance = class_obj({})
                        self.active_systems[class_name] = instance
                        print(f"  ? Initialized: {class_name} (with config)")
                    except:
                        print(f"  [WARN]?  Could not init: {class_name}")
                except Exception as e:
                    print(f"  [WARN]?  Failed: {class_name}")
    
    def _print_summary(self):
        """Print summary"""
        print("\n" + "=" * 80)
        print("[CHART] SYSTEM LOADER SUMMARY")
        print("=" * 80 + "\n")
        print(f"Modules: {len(self.loaded_modules)}")
        print(f"Classes: {len(self.loaded_classes)}")
        print(f"Functions: {len(self.loaded_functions)}")
        print(f"Configs: {len(self.kernel_configs)}")
        print(f"Active systems: {len(self.active_systems)}")
        print()
    
    def get_system(self, name: str) -> Any:
        """Get system by name"""
        for sys_name, sys_obj in self.active_systems.items():
            if name.lower() in sys_name.lower():
                return sys_obj
        return None
    
    def get_all_systems(self) -> Dict[str, Any]:
        """Get all systems"""
        return self.active_systems

_SYSTEM_LOADER = None

def get_system_loader():
    """Get or create loader"""
    global _SYSTEM_LOADER
    if _SYSTEM_LOADER is None:
        _SYSTEM_LOADER = AureonSystemLoader()
        _SYSTEM_LOADER.discover_and_load_all()
    return _SYSTEM_LOADER

def get_system(name: str) -> Any:
    """Get system by name"""
    return get_system_loader().get_system(name)

def get_all_systems() -> Dict[str, Any]:
    """Get all systems"""
    return get_system_loader().get_all_systems()
