import re
from pathlib import Path

brain_file = Path(r"C:\AUREON_AUTONOMOUS\aureon_brain.py")

if not brain_file.exists():
    print("[FAIL] Brain file not found! Check path.")
    exit(1)

# Backup
backup = brain_file.with_suffix('.py.backup_ensemble')
brain_file.rename(backup)
print(f"[OK] Backed up to: {backup}")

# Read content
content = backup.read_text(encoding='utf-8')

# Add ensemble models list to class
models_code = '''    ensemble_models = [
        "deepseek-r1:7b",
        "deepseek-r1:14b",
        "dolphin-mistral:8x7b",
        "wizard-vicuna-uncensored:13b",
        "qwen2.5-coder:7b"
    ]'''

init_pattern = r'(    def __init__\()'
content = re.sub(init_pattern, models_code + r'\n\1', content)

# Modify analysis to query all models and combine (simple concat for now; can improve)
content = content.replace(
    'return self.say_guard(self._ollama_chat(messages, temperature=0.3))',
    '''responses = []
for model in self.ensemble_models:
    try:
        resp = self._ollama_chat(messages, temperature=0.3, model=model)
        responses.append(resp)
    except Exception:
        pass  # Skip failed model
if responses:
    return self.say_guard(' \\n'.join([f"[{m}]: {r}" for m, r in zip(self.ensemble_models, responses)]))  # Label and join
else:
    return "All models failed - check Ollama."'''
)

# Write patched version
brain_file.write_text(content, encoding='utf-8')
print("[OK] Patched for ensemble brain! Restart AUREON.")