#!/usr/bin/env python3
"""
AUREON SURGEON
==============
Focused, bounded code mutation engine.

Follows foundational architectural constraints:
- UEE: navigate ? scan ? edit ? save ? run
- AGRe: gradient-based, feedback-driven, growth-oriented
- ABS: identity-preserving diffs, not wholesale overwrite
- UIO: coherence-routing packets, traceable provenance
- ?–?–?: every mutation passes through the moral compass

NEVER rewrites an entire file.
ALWAYS operates on bounded focus blocks (30-100 lines).
EVERY edit is auditable, reversible, and state-aware.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import re
import json
import time
import hashlib


@dataclass
class FocusBlock:
    """A bounded region of code selected for mutation."""
    file_path: str
    start_line: int
    end_line: int
    content: str
    function_name: str = ""
    class_name: str = ""
    purpose: str = ""
    hash: str = ""
    
    def __post_init__(self):
        self.hash = hashlib.md5(self.content.encode()).hexdigest()[:12]


@dataclass
class MutationPlan:
    """A bounded, coherence-locked edit plan."""
    focus: FocusBlock
    intent: str              # what we're trying to improve
    scope: str               # "add_lines" | "replace_lines" | "refactor" | "fix_bug"
    estimated_lines: int     # how many lines will change
    rationale: str           # why this mutation is needed
    risks: List[str] = field(default_factory=list)
    kappa_check: bool = True   # coherence preserved?
    tau_check: bool = True     # temporally responsible?
    sigma_check: bool = True   # systemic risk low?


@dataclass 
class MutationResult:
    """Result of applying a mutation."""
    success: bool
    old_content: str
    new_content: str
    diff_summary: str
    lines_changed: int
    timestamp: float
    hash_before: str
    hash_after: str
    feedback: str = ""


class AureonSurgeon:
    """
    Surgical code modification engine.
    
    Follows the correct Aureon method:
    1. scan_file ? extract structure (functions, classes, markers)
    2. select_focus_block ? choose 1-2 related functions
    3. plan_mutation ? AGRe plans a bounded edit (30-100 lines)
    4. apply_mutation ? edit with diff, not overwrite
    5. verify ? run/test the change
    6. reflect ? integrate feedback, build memory
    """
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or r"C:\AUREON_AUTONOMOUS")
        self.mutation_log: List[Dict[str, Any]] = []
        self.max_mutation_lines = 100  # Never touch more than 100 lines at once
    
    # ??????????????????????????????????????????????????????????
    # STEP 1: SCAN — Extract file structure without reading everything
    # ??????????????????????????????????????????????????????????
    
    def scan_file(self, path: str) -> Dict[str, Any]:
        """
        Scan a file and extract its structural skeleton.
        Returns functions, classes, imports, and structural markers
        WITHOUT dumping the entire file content.
        """
        p = self._resolve_path(path)
        if not p.exists():
            return {"ok": False, "error": f"File not found: {path}"}
        
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").split("\n")
        except Exception as e:
            return {"ok": False, "error": str(e)}
        
        structure = {
            "path": str(p),
            "total_lines": len(lines),
            "size_bytes": p.stat().st_size,
            "functions": [],
            "classes": [],
            "imports": [],
            "constants": [],
            "comments": [],   # section markers
        }
        
        current_class = ""
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Class definitions
            m = re.match(r'^class\s+(\w+)', stripped)
            if m:
                current_class = m.group(1)
                # Find the end of class (next class or EOF)
                end = self._find_block_end(lines, i - 1)
                structure["classes"].append({
                    "name": m.group(1),
                    "line": i,
                    "end_line": end,
                    "size": end - i + 1,
                })
            
            # Function definitions
            m = re.match(r'^(\s*)def\s+(\w+)\s*\(', stripped)
            if m:
                indent = len(m.group(1))
                fname = m.group(2)
                end = self._find_block_end(lines, i - 1, indent)
                
                # Extract docstring if present
                docstring = ""
                for j in range(i, min(i + 5, len(lines))):
                    if '"""' in lines[j] or "'''" in lines[j]:
                        doc_match = re.search(r'["\']+(.*?)["\']', lines[j])
                        if doc_match:
                            docstring = doc_match.group(1).strip()
                        break
                
                structure["functions"].append({
                    "name": fname,
                    "class": current_class if indent > 0 else "",
                    "line": i,
                    "end_line": end,
                    "size": end - i + 1,
                    "docstring": docstring[:100],
                })
            
            # Imports
            if stripped.startswith(("import ", "from ")):
                structure["imports"].append({"line": i, "text": stripped[:100]})
            
            # Section comment markers
            if stripped.startswith("# ") and len(stripped) > 10:
                if any(c in stripped for c in ("?", "?", "===", "---", "***")):
                    structure["comments"].append({"line": i, "text": stripped[:100]})
            
            # Constants (ALL_CAPS = ...)
            if re.match(r'^[A-Z_]{3,}\s*=', stripped):
                structure["constants"].append({"line": i, "text": stripped[:80]})
        
        structure["ok"] = True
        structure["output"] = (
            f"Scanned {p.name}: {len(lines)} lines, "
            f"{len(structure['classes'])} classes, "
            f"{len(structure['functions'])} functions"
        )
        
        return structure
    
    # ??????????????????????????????????????????????????????????
    # STEP 2: SELECT — Choose a bounded focus block
    # ??????????????????????????????????????????????????????????
    
    def select_focus_block(
        self, 
        path: str, 
        target: str,
        context_lines: int = 5,
    ) -> Dict[str, Any]:
        """
        Select a specific function, class, or line range for focused editing.
        
        Args:
            path: file path
            target: function name, class name, or "lines:50-80"
            context_lines: extra lines of context above/below
        
        Returns the focus block content with surrounding context.
        """
        p = self._resolve_path(path)
        if not p.exists():
            return {"ok": False, "error": f"File not found: {path}"}
        
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").split("\n")
        except Exception as e:
            return {"ok": False, "error": str(e)}
        
        start = 0
        end = len(lines) - 1
        block_name = target
        
        # Line range: "lines:50-80"
        if target.startswith("lines:"):
            try:
                parts = target[6:].split("-")
                start = max(0, int(parts[0]) - 1)
                end = min(len(lines) - 1, int(parts[1]) - 1)
            except Exception:
                return {"ok": False, "error": f"Invalid line range: {target}"}
        else:
            # Search for function or class by name
            found = False
            for i, line in enumerate(lines):
                if re.match(rf'^\s*(?:def|class)\s+{re.escape(target)}\b', line):
                    start = i
                    end = self._find_block_end(lines, i)
                    found = True
                    break
            
            if not found:
                return {"ok": False, "error": f"Could not find '{target}' in {p.name}"}
        
        # Add context lines
        ctx_start = max(0, start - context_lines)
        ctx_end = min(len(lines) - 1, end + context_lines)
        
        # Cap at max mutation size
        if (ctx_end - ctx_start) > self.max_mutation_lines + 20:
            ctx_end = ctx_start + self.max_mutation_lines + 20
        
        content_lines = lines[ctx_start:ctx_end + 1]
        content = "\n".join(f"{ctx_start + i + 1:4d}| {line}" for i, line in enumerate(content_lines))
        
        block = FocusBlock(
            file_path=str(p),
            start_line=start + 1,
            end_line=end + 1,
            content=content,
            function_name=target if not target.startswith("lines:") else "",
        )
        
        return {
            "ok": True,
            "block": {
                "path": block.file_path,
                "start": block.start_line,
                "end": block.end_line,
                "lines": end - start + 1,
                "hash": block.hash,
            },
            "content": content,
            "output": f"Selected {block_name} (lines {start+1}-{end+1}, {end-start+1} lines)",
        }
    
    # ??????????????????????????????????????????????????????????
    # STEP 3: APPLY — Surgical line replacement
    # ??????????????????????????????????????????????????????????
    
    def apply_edit(
        self,
        path: str,
        start_line: int,
        end_line: int,
        new_content: str,
        backup: bool = True,
    ) -> Dict[str, Any]:
        """
        Replace lines start_line through end_line with new_content.
        
        This is a BOUNDED edit — not a full file overwrite.
        Creates a backup before editing.
        
        Args:
            path: file path
            start_line: first line to replace (1-indexed)
            end_line: last line to replace (1-indexed)
            new_content: replacement text
            backup: whether to create .bak backup
        """
        p = self._resolve_path(path)
        if not p.exists():
            return {"ok": False, "error": f"File not found: {path}"}
        
        # Safety checks
        line_count = end_line - start_line + 1
        new_lines = new_content.split("\n")
        
        if line_count > self.max_mutation_lines:
            return {
                "ok": False, 
                "error": f"Mutation too large: {line_count} lines exceeds limit of {self.max_mutation_lines}. "
                         f"Break into smaller edits."
            }
        
        try:
            original = p.read_text(encoding="utf-8", errors="ignore")
            lines = original.split("\n")
            
            # Backup
            if backup:
                bak_path = p.with_suffix(p.suffix + ".bak")
                bak_path.write_text(original, encoding="utf-8")
            
            # Get old content for diff
            old_section = "\n".join(lines[start_line - 1:end_line])
            
            # Apply the edit
            lines[start_line - 1:end_line] = new_lines
            new_file = "\n".join(lines)
            
            # Write
            p.write_text(new_file, encoding="utf-8")
            
            # Build diff summary
            diff_summary = (
                f"Lines {start_line}-{end_line} ({line_count} lines) ? "
                f"{len(new_lines)} new lines"
            )
            
            # Log the mutation
            result = MutationResult(
                success=True,
                old_content=old_section,
                new_content=new_content,
                diff_summary=diff_summary,
                lines_changed=abs(len(new_lines) - line_count) + min(len(new_lines), line_count),
                timestamp=time.time(),
                hash_before=hashlib.md5(original.encode()).hexdigest()[:12],
                hash_after=hashlib.md5(new_file.encode()).hexdigest()[:12],
            )
            
            self.mutation_log.append({
                "path": str(p),
                "start": start_line,
                "end": end_line,
                "timestamp": result.timestamp,
                "hash_before": result.hash_before,
                "hash_after": result.hash_after,
                "diff": diff_summary,
            })
            
            return {
                "ok": True,
                "diff": diff_summary,
                "lines_changed": result.lines_changed,
                "hash_before": result.hash_before,
                "hash_after": result.hash_after,
                "backup": str(bak_path) if backup else None,
                "output": f"[OK] Applied edit to {p.name}: {diff_summary}",
            }
            
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    # ??????????????????????????????????????????????????????????
    # STEP 4: VERIFY — Test if the edit didn't break anything
    # ??????????????????????????????????????????????????????????
    
    def verify_syntax(self, path: str) -> Dict[str, Any]:
        """Check if a Python file has valid syntax after editing."""
        p = self._resolve_path(path)
        if not p.exists():
            return {"ok": False, "error": f"File not found: {path}"}
        
        try:
            code = p.read_text(encoding="utf-8", errors="ignore")
            compile(code, str(p), "exec")
            return {
                "ok": True,
                "valid": True,
                "output": f"[OK] {p.name}: syntax valid",
            }
        except SyntaxError as e:
            return {
                "ok": True,
                "valid": False,
                "error_line": e.lineno,
                "error_msg": str(e),
                "output": f"[FAIL] {p.name}: syntax error at line {e.lineno}: {e.msg}",
            }
    
    def revert(self, path: str) -> Dict[str, Any]:
        """Revert to the .bak backup if available."""
        p = self._resolve_path(path)
        bak = p.with_suffix(p.suffix + ".bak")
        
        if not bak.exists():
            return {"ok": False, "error": f"No backup found for {path}"}
        
        try:
            content = bak.read_text(encoding="utf-8", errors="ignore")
            p.write_text(content, encoding="utf-8")
            return {"ok": True, "output": f"[OK] Reverted {p.name} from backup"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    # ??????????????????????????????????????????????????????????
    # HELPERS
    # ??????????????????????????????????????????????????????????
    
    def _resolve_path(self, path: str) -> Path:
        p = Path(path)
        if not p.is_absolute():
            p = self.base_dir / p
        return p
    
    def _find_block_end(self, lines: List[str], start_idx: int, base_indent: int = None) -> int:
        """Find the end of a code block (function or class) by indentation."""
        if base_indent is None:
            # Detect indentation of the def/class line
            line = lines[start_idx]
            base_indent = len(line) - len(line.lstrip())
        
        end = start_idx
        for i in range(start_idx + 1, len(lines)):
            line = lines[i]
            if not line.strip():  # empty line
                continue
            indent = len(line) - len(line.lstrip())
            if indent <= base_indent and line.strip():
                break
            end = i
        
        return end + 1  # 1-indexed
    
    def get_mutation_log(self) -> List[Dict[str, Any]]:
        """Return the audit trail of all mutations."""
        return self.mutation_log
    
    # ??????????????????????????????????????????????????????????
    # DISPATCH — For integration with aureon_hands
    # ??????????????????????????????????????????????????????????
    
    def dispatch(self, op: str, **kwargs) -> Dict[str, Any]:
        """Dispatch surgical operations."""
        if op == "scan_file":
            return self.scan_file(kwargs.get("path", ""))
        elif op == "select_focus":
            return self.select_focus_block(
                kwargs.get("path", ""),
                kwargs.get("target", ""),
                kwargs.get("context_lines", 5),
            )
        elif op == "apply_edit":
            return self.apply_edit(
                kwargs.get("path", ""),
                kwargs.get("start_line", 1),
                kwargs.get("end_line", 1),
                kwargs.get("new_content", ""),
            )
        elif op == "verify_syntax":
            return self.verify_syntax(kwargs.get("path", ""))
        elif op == "revert":
            return self.revert(kwargs.get("path", ""))
        elif op == "mutation_log":
            return {"ok": True, "log": self.get_mutation_log(), "output": f"{len(self.mutation_log)} mutations logged"}
        else:
            return {"ok": False, "error": f"Unknown surgeon op: {op}"}


# Self-test
if __name__ == "__main__":
    surgeon = AureonSurgeon()
    
    # Test scan
    result = surgeon.scan_file("aureon_brain.py")
    if result.get("ok"):
        print(f"Scanned: {result['total_lines']} lines")
        print(f"Classes: {len(result['classes'])}")
        for c in result["classes"]:
            print(f"  class {c['name']} (line {c['line']}-{c['end_line']}, {c['size']} lines)")
        print(f"Functions: {len(result['functions'])}")
        for f in result["functions"][:10]:
            prefix = f"  {f['class']}." if f['class'] else "  "
            print(f"{prefix}{f['name']}() line {f['line']}-{f['end_line']} ({f['size']} lines)")
    else:
        print(f"Error: {result.get('error')}")
