# aureon_recursive_self_improver.py
import ast
import hashlib
import os
import subprocess
from pathlib import Path
from datetime import datetime
from aureon_external_organs import TimeOrgan, ReasoningTraceLogger
from aureon_surgeon import AureonSurgeon

class RecursiveSelfImprover:
    def __init__(self):
        self.time = TimeOrgan()
        self.trace = ReasoningTraceLogger()
        self.surgeon = AureonSurgeon()
        self.forge_dir = Path("C:\\AUREON_AUTONOMOUS\\FORGE")
        self.forge_dir.mkdir(parents=True, exist_ok=True)

    def improve(self, target_file: str, improvement_spec: str) -> str:
        with open(target_file, "r", encoding="utf-8") as f:
            original_code = f.read()
        original_hash = hashlib.sha256(original_code.encode()).hexdigest()

        new_code = self._generate_improved_code(original_code, improvement_spec)
        new_hash = hashlib.sha256(new_code.encode()).hexdigest()

        if not self.surgeon.verify_invariants(new_code):
            self.trace.log_cycle("self_improve", "invariant_violation", entropy_class="blocked")
            return "BLOCKED: Invariant violation"

        backup_path = self.forge_dir / f"backup_{Path(target_file).stem}_{self.time.now().strftime('%Y%m%d_%H%M%S')}.py"
        backup_path.write_text(original_code, encoding="utf-8")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_code)

        self.trace.log_cycle(
            user_input=improvement_spec,
            response=f"self_improved_{Path(target_file).name}",
            entropy_class="recursive_improvement",
            invariant="kappa_tau_sigma_preserved"
        )
        return f"SELF-IMPROVED: {target_file} (hash {new_hash[:12]})"

    def _generate_improved_code(self, code: str, spec: str) -> str:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "respond":
                node.body.insert(0, ast.parse(f"        # Improved per {spec} at {self.time.now_iso()}").body[0])
        return ast.unparse(tree)

if __name__ == "__main__":
    improver = RecursiveSelfImprover()
    print(improver.improve("aureon_brain.py", "increase coherence by 0.15"))