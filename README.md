# UFO-Cathedral v6.6 Pristine — Fail-Safe Free AI

**Version: v6.6 Pristine (unified — was v6.4 / v6.5 / v7.0 FLAWLESS mixed, now single badge: v6.6 Pristine — 8GB / iPhone 16 Pro Max Compatible)**

**Live Site:** https://ai4pcfree.netlify.app | **Slides:** https://ai4pcfree.netlify.app/slides/ | **Cost:** 100% Free Forever | **Offline:** Fully Functional | **Ledger:** Cryptographically Chained + Saved State

---

### Honest Story — How it was really built

This was NOT done by downloading a single AI model that lacks reasoning.

**Process:** First download Llama, then the bots from there on out, then all 5 together as opcode families for real reasoning.

- **5 Geometric Models as Opcode Families:** Phi3 sphere, Llama pyramid, Llama graph, Qwen torus, Llava eye — distinct opcode spaces
- **High-Throughput Cathedral Computer:** A-T-V-Q-P Pipeline + 5 Model Register File — throughput optimized for 8GB
- **Shadow Mode:** 4 Brains + 1 Eyes + 5 Models → Coherence Evaluation → SAFE | HOLD | ESCALATE
- **Bounded Sensor Gate:** Merkle Permit + Rate Limit + Click-Fence — prevents loops, malware downloads, crashes (fixes $200 loop bug)
- **Ledger Hash:** `H(n)=SHA256(H(n-1)||state||action)` + replay bundle for audit

### Honest RAM Path (fixes old "five models + vision on iPhone" claim)

| Tier | Models | RAM | Reasoning | Where | Works |
|------|--------|-----|-----------|-------|-------|
| **Lite (<8GB phones)** | `phi3:mini Q4` | 1.8GB | Single reasoning — like basic Discord bot | COD HUD taps only | Low-end phones |
| **Standard (iPhone 16 Pro Max 8GB — my device)** | `phi3:mini + llama3.2:3b` | 3.2GB | 2-model reasoning — learns sniper | Mobilerun red boxes + OBS Live | iPhone 16 Pro Max 8GB |
| **Full Cathedral (PC 8GB only)** | All 5 opcode families | 5.8-6.2GB | 5-model reasoning — full Council + Ledger | PC 8GB only, NOT phone stable | PC 8GB+ |

**We do NOT claim five models + vision on iPhone.** START.md now says pull `phi3:mini` first as entry, then add Llama and bots to get all 5 together.

### Quick Start — v6.6 Pristine

```bash
# 1. Lite entry — honest first step (<8GB)
ollama pull phi3:mini

# 2. Standard — iPhone 16 Pro Max 8GB test (your device)
pip install droidrun
brew install scrcpy
python ufo64.py --mode phone --task "Tap sniper button only inside COD HUD"

# 3. COD HUD Learn — giftable sniper for TikTok Live 1v1
python ufo64.py --mode cod_hud
# exports my_sniper_v1.jsonl + obs_cathedral_cod.json

# 4. Full PC Cathedral — all 5 together for reasoning
ollama pull llama3.2:3b
ollama pull qwen2:1.5b
ollama pull llava:phi3
python ufo64.py --mode pc
python verify_ledger.py
```

### v6.6 Fixes — What Changed from v6.4 / v7.0

1. **PC→Phone / COD HUD:** Was HTML demo only, `ufo64.py` shelled `python -m ufo` on Windows, did not drive phone. Now `ufo64.py --mode phone|pc|cod_hud` drives phone via Droidrun/Mobilerun + scrcpy fallback + pre-mapped red boxes + Bounded Sensor Gate (no Play Store zone).
2. **Safety Card:** Was spec in README `UNVERIFIED → 3 replays → TRUTH`. Now saved state in `~/.ufo/ledger/safety_state.json` `{state,replays,threshold,next,version}` checked by `verify_ledger.py`.
3. **Version badges:** Was mix v6.4 / v6.5 / v6.6 / v7.0 FLAWLESS (yellow badge `20 DISSECTED V7.0 FLAWLESS` caused camo.githubusercontent.com crash). Now unified `v6.6 Pristine — 8GB / iPhone 16 Pro Max Compatible` everywhere.
4. **8GB claim:** Was "five models + vision on 8GB phone". Now honest: Full 5 models = PC only, Standard = 2 models on iPhone.

### Mobile Driver + COD HUD (Now in Python too)

- **Panic Stop:** ESC 3x or shake iPhone → instant HOLD, ledger saved
- **Undo / Rollback:** `python rollback.py --last 1` + visual diff before/after red outline
- **Health Dashboard:** RAM / Battery / Gate / Shadow gauges, auto-unloads if RAM>90% so 16 Pro Max never crashes
- **OBS Preset:** `obs_cathedral_cod.json` one-click import scrcpy + agent view + ledger overlay for TikTok Live

### OmniGood Guardrails — Civilized + Safe

- No spam/flooding — rate + embedding drift, only last 8 messages, no crash
- No bashing/heated arguments — formal civilized, respectful back
- No racism/degrading / excessive cursing — auto ask to stay respectful
- +18 fictional storybook euphoric writing allowed, but NOT rape / non-consensual / wax without permission — therapist analogy: "communication is key, ask permission"
- Dangerous Admin Step warning + alternative + obfuscated backup email to SolorzanoLunaJose@gmail.com (cipher 1↔9,2↔8,3↔7,4↔6,5↔5, e.g., 123456789→987654321, only robot can decode)

### Verification

```bash
python verify_ledger.py
# Checks: ledger hash chain + safety_state.json + honest RAM path + version unified
```

### Project Structure

- `ufo64.py` — Unified runner pc|phone|cod_hud + safety state persistence + Bounded Sensor Gate
- `START.md` — Honest entry path phi3:mini first
- `verify_ledger.py` — Checks ledger + safety_state.json
- `slides/index.html` — v6.6 Pristine gallery (RAW URLs, not base64 embedded — fixes camo crash)
- `docs/images/` — 8 blueprints: 5 Geometric Models, Bounded Sensor Gate, Cathedral Blueprint v6.4, Fail-Safe Poster, A-T-V-Q-P Pipeline, OSHA Pyramid, Safety Comparison, Full End-to-End v6.5

### Why Stick With This vs Operator / Astra / Basic Discord Bot?

- 100% Free Offline — no $200 loop bug — Gate blocks runaway taps
- Formal validation layering — OSHA 5 controls mapped to AI safety
- Ledger Hash + Safety State saved — replay bundle + PDF audit + portable USB mode
- Community Blueprint Hub — zip 8 images + hash proves prior art vs Z1T

**Previous badges deleted:** `v7.0 FLAWLESS` removed until phone driver + safety state + 5-model proof passes on iPhone.

---

© Jose Angel Solorzano Luna — Millville, NJ — Built on iPhone 16 Pro Max 8GB
