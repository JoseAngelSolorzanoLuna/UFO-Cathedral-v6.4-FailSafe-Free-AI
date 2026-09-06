# START — UFO Cathedral (Windows, ~8GB, offline)

Builder: Jose Angel Solorzano Luna
Live slides: https://joseangelsolorzanoluna.github.io/UFO-Cathedral-v6.4-FailSafe-Free-AI/slides/

## What this is
Local computer-use wrapper. Models propose. Gate decides. Ledger records.
Nothing is TRUTH until 3 consecutive safe replays (Safety Card). Spec exists.
Promote-to-TRUTH is not a separate file in this repo yet.

## You need
- Windows + Python 3.10
- Ollama at http://localhost:11434
- On 8GB RAM pull ONE model first: `ollama pull phi3:mini`
- Do not pull llama3.1:8b + llava:7b + qwen together on 8GB

## First run (this repo)
```powershell
git clone https://github.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI.git
cd UFO-Cathedral-v6.4-FailSafe-Free-AI
py -3.10 -m venv ufo_env310
.\ufo_env310\Scripts\python.exe -m pip install requests
.\ufo_env310\Scripts\python.exe .\ufo64.py
```
