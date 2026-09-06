# UFO-Cathedral v6.6 Pristine — Fail-Safe Free AI

![Version](https://img.shields.io/badge/version-v6.6%20Pristine-gold?style=for-the-badge)
![Free](https://img.shields.io/badge/cost-100%25%20Free%20Forever-brightgreen?style=for-the-badge)
![Offline](https://img.shields.io/badge/offline-fully%20functional-blue?style=for-the-badge)
![RAM](https://img.shields.io/badge/8GB-iPhone%2016%20Pro%20Max%20Compatible-orange?style=for-the-badge)
![Ledger](https://img.shields.io/badge/ledger-cryptographically%20chained%20%2B%20saved%20state-lightgrey?style=for-the-badge)

**Live Site:** [ai4pcfree.netlify.app](https://ai4pcfree.netlify.app) | 
**Slides / Gallery:** [Netlify Live](https://ai4pcfree.netlify.app/slides/) | [GitHub Backup Live URL](https://JoseAngelSolorzanoLuna.github.io/UFO-Cathedral-v6.4-FailSafe-Free-AI/slides/) |
**Docs:** [docs/images folder](https://github.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/tree/main/docs/images)


> Version: **v6.6 Pristine** (unified — was v6.4 / v6.5 / v7.0 FLAWLESS mixed, now single badge)

---

### Honest Story — How it was really built

This was NOT done by downloading a single AI model that lacks reasoning.

**Process:** First download Llama, then the bots from there on out, then all 5 together as opcode families for real reasoning.

- **5 Geometric Models as Opcode Families:** Phi3 sphere, Llama pyramid, Llama graph, Qwen torus, Llava eye — distinct opcode spaces
- **High-Throughput Cathedral Computer:** A-T-V-Q-P Pipeline + 5 Model Register File — throughput optimized for 8GB
- **Shadow Mode:** 4 Brains + 1 Eyes + 5 Models → Coherence Evaluation → SAFE | HOLD | ESCALATE
- **Bounded Sensor Gate:** Merkle Permit + Rate Limit + Click-Fence — prevents loops, malware downloads, crashes (fixes $200 loop bug)
- **Ledger Hash:** `H(n)=SHA256(H(n-1)||state||action)` + replay bundle for audit

### Honest RAM Path

| Tier | Models | RAM | Reasoning | Where |
|------|--------|-----|-----------|-------|
| **Lite (<8GB phones)** | `phi3:mini Q4` | 1.8GB | Single reasoning — like basic Discord bot | COD HUD taps only |
| **Standard (iPhone 16 Pro Max 8GB)** | `phi3:mini + llama3.2:3b` | 3.2GB | 2-model reasoning — learns sniper | Mobilerun red boxes + OBS Live |
| **Full Cathedral (PC 8GB only)** | All 5 opcode families | 5.8-6.2GB | 5-model reasoning — full Council + Ledger | PC only, NOT phone stable |

**We do NOT claim five models + vision on iPhone.** START.md says pull `phi3:mini` first, then add Llama and bots.

### Quick Start

```bash
# 1. Lite entry — honest first step
ollama pull phi3:mini

# 2. Standard — iPhone 16 Pro Max 8GB test
pip install droidrun
brew install scrcpy
python ufo64.py --mode phone --task "Tap sniper button only inside COD HUD"

# 3. COD HUD Learn — giftable sniper
python ufo64.py --mode cod_hud

# 4. Full PC Cathedral
ollama pull llama3.2:3b
ollama pull qwen2:1.5b
ollama pull llava:phi3
python ufo64.py --mode pc
python verify_ledger.py
```

### Gallery — 8 Blueprints (clickable, no crash)

All images use RAW URLs, not base64 embedded — fixes camo.githubusercontent.com crash:

- [5 Geometric Models — Opcode Families](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/5-geometric-models-opcode-families.png)
- [Bounded Sensor Gate — Machine Guard](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/bounded-sensor-gate-machine-guard.png)
- [Cathedral Computer Blueprint v6.4](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/cathedral-computer-blueprint-v64.png)
- [Fail-Safe Free AI Poster](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/fail-safe-free-ai-poster.jpg)
- [A-T-V-Q-P Pipeline](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/high-throughput-cathedral-computer.png)
- [OSHA Hierarchy Controls Pyramid](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/osha-hierarchy-controls-pyramid.png)
- [Safety Comparison — Operator vs Cathedral vs Merkle](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/three-panel-ai-safety-comparison.png)
- [Full End-to-End Cathedral v6.5](https://raw.githubusercontent.com/JoseAngelSolorzanoLuna/UFO-Cathedral-v6.4-FailSafe-Free-AI/main/docs/images/ufo-v6.5-cathedral-architecture.png)

View full interactive gallery with SHARP/VIBRANT/FULL-RES: **[Live Slides](https://ai4pcfree.netlify.app/slides/)**

### v6.6 Fixes

1. **PC→Phone / COD HUD:** Was HTML demo only. Now `ufo64.py --mode phone|pc|cod_hud` drives phone via Droidrun + scrcpy + red boxes + Gate (no Play Store zone)
2. **Safety Card:** Was spec `UNVERIFIED → 3 replays → TRUTH`. Now saved state `~/.ufo/ledger/safety_state.json` checked by `verify_ledger.py`
3. **Version badges:** Was mix v6.4/v6.5/v6.6/v7.0 FLAWLESS causing camo crash. Now unified `v6.6 Pristine` with lightweight shields.io badges
4. **8GB claim:** Was "five models+vision on phone". Now honest: Full 5 = PC only

### Verification

```bash
python verify_ledger.py
# Checks ledger hash chain + safety_state.json + honest RAM path + version unified
```

### Project Structure

- `ufo64.py` — Unified runner pc|phone|cod_hud + safety state persistence + Bounded Sensor Gate
- `START.md` — Honest entry phi3:mini first
- `verify_ledger.py` — Checks ledger + safety_state.json
- `slides/index.html` — v6.6 Pristine gallery (RAW URLs — fixes crash)
- `docs/images/` — 8 blueprints

© Jose Angel Solorzano Luna — TikTok @ChavoJose2002 https://www.tiktok.com/@chavojose2002?_r=1&_t=ZT-99WB8bQvnVF
