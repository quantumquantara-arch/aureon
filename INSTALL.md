# Installing AUREON

## Requirements
- Python 3.10+
- Git
- (Optional) Ollama for local LLM inference

## Quick Install

```bash
git clone https://github.com/quantumquantara-arch/aureon.git
cd aureon
pip install -r requirements.txt
```

## Run the Brain (local, no LLM)
```bash
python anatomy/aureon_brain.py
```

## Run AGI Verification
```bash
python verification/run_agi_verifier.py
```

## Run with Ollama (full local inference)
```bash
ollama pull mistral
python anatomy/aureon_brain.py --model ollama/mistral
```

## Verify DGK-IES Ethics Layer
```bash
python DGK-IES/src/reference_engine.py --verify
```
