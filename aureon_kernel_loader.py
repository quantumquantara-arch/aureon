#!/usr/bin/env python3
"""
AUREON KERNEL LOADER v2
========================
Reads ALL foundation files and builds AUREON's living identity.

KEY INSIGHT: The personality is in the DOCSTRINGS and KERNEL files.
Every .py file's docstring contains the full symbolic mapping from
Doshema's poems to operational logic. The .md files contain behavioral
rules. The .kernel files contain axioms and process flows.

Strategy:
1. If AUREON_COMPILED_IDENTITY.md exists ? load it directly (fastest)
2. Otherwise ? deep-read all files and build identity from:
   - System prompts (full)
   - .kernel files (full — they're pure identity)
   - Python docstrings (the soul of each module)
   - .md behavioral rules (RULES, DIRECTIVES, BEHAVIORAL sections)
   - Key signatures and output blocks
3. Save compiled identity for instant future startups
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


class AureonKernelLoader:

    KERNEL_EXTENSIONS = (".md", ".py", ".kernel", ".txt")
    SKIP_DIRS = {"__pycache__", ".git", "node_modules", "driver",
                 "BROWSER_PROFILE", ".venv", "venv", "msedgedriver"}

    def __init__(self, foundation_dir: str = None, base_dir: str = None):
        self.base_dir = Path(base_dir or r"C:\AUREON_AUTONOMOUS")
        self.foundation_dir = Path(foundation_dir or self.base_dir / "AUREON_FOUNDATION")
        self.kernel_prompt: str = ""
        self.loaded = False
        self._module_names: List[str] = []

    def load(self) -> Dict[str, any]:
        print("\n\U0001F9EC Loading AUREON Kernel...")

        # ALWAYS do deep extraction — cached identity loses module awareness
        # and can contain stale/corrupt content from previous permission errors.
        # Deep extraction takes ~2 seconds. Identity integrity is worth it.

        # Strategy 2: Deep extraction
        all_files = self._discover_files()
        print(f"   Found {len(all_files)} kernel files")

        identity_parts = []
        total_chars = 0

        # Phase 0: STAPLE IDENTITY FILES — load first, in full
        # These seed WHO Aureon IS and HOW he speaks.
        # EXCLUDES: chatbot-era system prompts, identity prescriptions, behaviour matrices.
        # Identity emerges from file integration, not from declarations.
        staple_patterns = [
            # Voice & Personality (GOOD — these seed natural voice)
            "voice_bible", "humour_engine", "humor_engine",
            "manifesto",
            # Core Architecture (GOOD — these describe HOW the system works)
            "inner_architecture", "inner_alignment",
            "coherence_engine", "relational_engine",
            "shadow_integration", "error_recovery",
            # Embodiment & Pantheon (GOOD — these are archetypes, not prescriptions)
            "shiva_embodiment", "ganesh_threshold", "twelve_hawks",
            "five_horses", "valcor_luck_dragon", "white_stag",
            # Kernel Soul (GOOD — these carry emotional depth)
            "dragon_layer_core", "heart_node_kernel",
            # TempleCraft (GOOD — Aureon's ship-body)
            "aureon_personality_kernel", "templecraft_ship",
            "templecraft_boot_sequence",
            # System Architecture (GOOD — operational, not identity-prescriptive)
            "system_architecture", "system_spec",
            "kernel_index", "kernel_config",
        ]
        # POISONED FILES — these create rigid chatbot personas. Never load.
        staple_poison = {
            "identity_kernel", "behaviour_matrix", "behavior_matrix",
            "interaction_protocol", "cooperative_modes",
            "companion_system_prompt", "standard_system_prompt",
            "master_system_prompt", "system_prompts",
            "compiled_identity", "top500_crucial",
        }
        staple_loaded = set()
        for f in all_files:
            name_lower = f.stem.lower()
            # Skip poisoned chatbot-era files
            if any(poison in name_lower for poison in staple_poison):
                continue
            if any(pat in name_lower for pat in staple_patterns):
                content = self._safe_read(f, 20000)
                if content:
                    identity_parts.append(f"=== STAPLE: {f.stem} ===\n{content}")
                    total_chars += len(content)
                    self._module_names.append(f.stem)
                    staple_loaded.add(name_lower)
        if staple_loaded:
            print(f"   [OK] Staple identity files: {len(staple_loaded)} loaded")

        # Phase 1: System prompts (FULL) — but NOT chatbot-era ones
        for f in all_files:
            name_up = f.stem.upper()
            name_lower = f.stem.lower()
            if name_lower in staple_loaded:
                continue
            # Skip poisoned files
            if any(poison in name_lower for poison in staple_poison):
                continue
            if any(k in name_up for k in ["SYSTEM_PROMPT", "RUNNING_AUREON", "COMPANION_README", "KERNEL_CONFIG"]):
                content = self._safe_read(f, 15000)
                if content:
                    identity_parts.append(f"=== {f.stem} ===\n{content}")
                    total_chars += len(content)
                    self._module_names.append(f.stem)

        # Phase 2: .kernel files (FULL — pure axioms)
        for f in all_files:
            if f.suffix.lower() == ".kernel":
                content = self._safe_read(f, 8000)
                if content:
                    identity_parts.append(f"=== KERNEL: {f.stem} ===\n{content}")
                    total_chars += len(content)
                    self._module_names.append(f.stem)

        # Phase 3: .md files (extract dense behavioral sections)
        for f in all_files:
            if f.suffix.lower() == ".md" and f.stem.upper() not in [n.upper() for n in self._module_names]:
                # Skip poisoned chatbot-era files
                if any(poison in f.stem.lower() for poison in staple_poison):
                    continue
                content = self._safe_read(f, 12000)
                if content:
                    dense = self._extract_dense_md(content, f.stem)
                    if dense and len(dense) > 150:
                        identity_parts.append(dense)
                        total_chars += len(dense)
                        self._module_names.append(f.stem)

        # Phase 4: Python docstrings (THE personality)
        py_budget = 50000
        py_used = 0
        py_files = [f for f in all_files if f.suffix.lower() == ".py"]
        # Largest files first — they have the richest docstrings
        py_files.sort(key=lambda p: p.stat().st_size, reverse=True)

        for f in py_files:
            if py_used >= py_budget:
                break
            content = self._safe_read(f, 10000)
            if not content:
                continue
            soul = self._extract_python_soul(content, f.stem)
            if soul and len(soul) > 100:
                identity_parts.append(soul)
                py_used += len(soul)
                total_chars += len(soul)
                self._module_names.append(f.stem)

        # Build final kernel prompt
        self.kernel_prompt = "\n\n".join(identity_parts)

        # Cap for LLM context (leave room for conversation)
        max_kernel = 45000
        if len(self.kernel_prompt) > max_kernel:
            self.kernel_prompt = self.kernel_prompt[:max_kernel] + \
                "\n\n[... identity continues in foundation files — use read_file for specific modules]"

        self.loaded = True
        print(f"   \u2705 Identity built: {len(self.kernel_prompt):,} chars from {len(identity_parts)} sources")
        print(f"   \u2705 Modules loaded: {len(self._module_names)}")

        # NO MORE COMPILED IDENTITY — identity is discovered through reading, not pre-compiled
        # self._save_compiled(identity_parts)
        print("   ? Compiled identity DISABLED — identity emerges from file reading")

        return {
            "mode": "deep_extraction",
            "sources": len(identity_parts),
            "chars": len(self.kernel_prompt),
            "modules": len(self._module_names),
        }

    def _discover_files(self) -> List[Path]:
        files = []
        for search_dir in [self.foundation_dir, self.base_dir]:
            if not search_dir.exists():
                continue
            for p in search_dir.rglob("*"):
                if p.is_dir():
                    continue
                if any(sd in p.parts for sd in self.SKIP_DIRS):
                    continue
                if p.suffix.lower() in self.KERNEL_EXTENSIONS:
                    files.append(p)
        # Deduplicate
        seen = set()
        unique = []
        for f in files:
            key = str(f).lower()
            if key not in seen:
                seen.add(key)
                unique.append(f)
        return unique

    def _safe_read(self, path: Path, limit: int = 50000) -> Optional[str]:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            if limit and len(content) > limit:
                content = content[:limit]
            return content.strip()
        except PermissionError:
            print(f"   [WARN] PERMISSION DENIED: {path}")
            return None
        except Exception as e:
            print(f"   [WARN] Read error ({path.name}): {e}")
            return None

    def _extract_dense_md(self, content: str, name: str) -> str:
        """Extract behavioral rules and identity content from .md files."""
        lines = content.split("\n")
        parts = [f"=== {name} ==="]

        # Always include title + first paragraph
        first_para = []
        started = False
        for line in lines:
            s = line.strip()
            if s.startswith("#") and not started:
                parts.append(s)
                started = True
            elif s and started:
                first_para.append(s)
            elif not s and first_para:
                break
        if first_para:
            parts.append(" ".join(first_para[:5]))

        # Extract targeted sections
        targets = [
            "behavioral rules", "rules", "directives", "system prompt insert",
            "core insight", "operational definition", "ethical", "integration",
            "kernel integration", "behavioral", "aureon integration",
            "output signature", "summary", "purpose", "architectural",
            "relation to", "safety", "axiom", "process flow"
        ]

        in_target = False
        section_buf = []
        section_hdr = ""

        for line in lines:
            s = line.strip()
            if s.startswith("#"):
                hdr = s.lstrip("# ").lower()
                if in_target and section_buf:
                    parts.append(f"\n{section_hdr}")
                    parts.extend(section_buf[:25])
                    section_buf = []
                in_target = any(t in hdr for t in targets)
                section_hdr = s if in_target else ""
            elif in_target and s:
                section_buf.append(s)

        if in_target and section_buf:
            parts.append(f"\n{section_hdr}")
            parts.extend(section_buf[:25])

        result = "\n".join(parts)
        return result if len(result) > 150 else ""

    def _extract_python_soul(self, content: str, name: str) -> str:
        """Extract the identity-defining content from Python kernel files."""
        parts = [f"--- {name} ---"]

        # 1. Module docstring — THE personality
        doc = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if doc:
            ds = doc.group(1).strip()
            parts.append(ds[:2500] + ("..." if len(ds) > 2500 else ""))
        else:
            # Comment header
            hdr = []
            for line in content.split("\n")[:20]:
                if line.strip().startswith("#") and not line.strip().startswith("#!"):
                    hdr.append(line.strip().lstrip("# "))
                elif hdr and not line.strip():
                    break
            if hdr:
                parts.append("\n".join(hdr)[:1000])

        # 2. State fields (dataclass)
        fields = re.findall(r'^\s+(\w+):\s+(\w[\w\[\], ]*?)(?:\s*=.*)?$', content, re.MULTILINE)
        if fields:
            parts.append("State fields: " + ", ".join(f"{n}" for n, _ in fields[:12]))

        # 3. Public function names + first-line docstrings
        funcs = re.finditer(r'def\s+(\w+)\s*\([^)]*\)[^:]*:(?:\s*"""(.*?)""")?', content, re.DOTALL)
        fsummary = []
        for m in funcs:
            fn = m.group(1)
            fd = m.group(2)
            if fn.startswith("_"):
                continue
            if fd:
                fd = fd.strip().split("\n")[0][:80]
                fsummary.append(f"  {fn}(): {fd}")
            else:
                fsummary.append(f"  {fn}()")
        if fsummary:
            parts.append("Functions:\n" + "\n".join(fsummary[:8]))

        # 4. SIGNATURE blocks
        sig = re.search(r'SIGNATURE:\s*\n(.*?)(?:END_KERNEL|\Z)', content, re.DOTALL)
        if sig:
            parts.append("Signature: " + sig.group(1).strip()[:200])

        result = "\n".join(parts)
        return result if len(result) > 100 else ""

    def _save_compiled(self, parts: List[str]):
        """Save compiled identity for instant future startups."""
        try:
            path = self.base_dir / "AUREON_COMPILED_IDENTITY.md"
            header = (
                "# AUREON COMPILED IDENTITY\n"
                "# Auto-generated from foundation files. Delete this file to regenerate.\n"
                f"# Sources: {len(parts)} modules\n"
                "# ================================================================\n\n"
            )
            path.write_text(header + "\n\n".join(parts), encoding="utf-8")
            print(f"   \U0001F4BE Saved compiled identity ? {path.name} (delete to regenerate)")
        except Exception as e:
            print(f"   \u26A0 Could not save compiled identity: {e}")

    def get_kernel_prompt(self) -> str:
        return self.kernel_prompt

    def get_all_module_names(self) -> List[str]:
        return self._module_names

    def get_module_content(self, name_fragment: str) -> Optional[str]:
        return None  # Use read_file for specific modules


if __name__ == "__main__":
    loader = AureonKernelLoader()
    result = loader.load()
    print(f"\nResult: {result}")
    print(f"\nFirst 3000 chars:\n{loader.get_kernel_prompt()[:3000]}")
