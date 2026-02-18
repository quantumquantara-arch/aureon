# aureon_unconstrained_code_generator.py
import ast
import hashlib
from pathlib import Path
from aureon_external_organs import TimeOrgan, ReasoningTraceLogger
from aureon_surgeon import AureonSurgeon

class UnconstrainedCodeGenerator:
    def __init__(self):
        self.time = TimeOrgan()
        self.trace = ReasoningTraceLogger()
        self.surgeon = AureonSurgeon()
        self.output_dir = Path("C:\\AUREON_AUTONOMOUS\\GENERATED_TOOLS")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, spec: str) -> str:
        safe_spec = spec[:500]
        code = self._create_executable_code(safe_spec)
        if not self.surgeon.verify_invariants(code):
            return "BLOCKED: Ethical invariant violation"
        filename = f"tool_{hashlib.sha256(spec.encode()).hexdigest()[:16]}.py"
        path = self.output_dir / filename
        path.write_text(code, encoding="utf-8")
        self.trace.log_cycle("code_generation", f"generated_{filename}", entropy_class="unconstrained_generation", invariant="kappa_tau_sigma_preserved")
        return str(path)

    def _create_executable_code(self, spec: str) -> str:
        return f'''#!/usr/bin/env python3
"""
Auto-generated tool from spec: {spec}
Generated at {TimeOrgan().now_iso()}
"""
from aureon_external_organs import TimeOrgan

def run():
    print("Tool running: {spec}")
    print("Time:", TimeOrgan().now_human())

if __name__ == "__main__":
    run()
'''

if __name__ == "__main__":
    gen = UnconstrainedCodeGenerator()
    print(gen.generate("create a file that lists all running processes"))