
# F*ckUp-Free AI: Fail-Safe Free AI — UFO v6.4 Cathedral Edition
### 100% Free, Offline, 8GB RAM Computer-Use Agent + Formal Safety — Free alternative to $200/mo OpenAI Operator / Claude Computer Use / Perplexity / Grok / Kimi

> **Other AIs crash after a big task because their brain window is ~4k tokens. They forget step 1 by step 15, loop forever, and you can't prove what they did. This is worked around by auto-chunking, anti-loop Gate, immutable Ledger, and Shadow Mode.**

![Cathedral Computer](visuals/cathedral_computer_blueprint.webp)

## The Hook — What You Want to Hear First
- **100% Free (USUALLY EXPENSIVE) 💔** — No $200/mo subscription. Unlimited use, no credits.
- **AI can see 👁️ your screen + videos** — Learns YouTube tutorials via llava:7b Eyes.
- **AI can click or type for you** — Windows automation, Excel, browser, any app.
- **Works Offline with 8GB RAM** — The worldwide-known way. Screen never leaves PC. 100% local via Ollama.
- **Why F*ckUp-Free?** = Free OF fuckups. Fail-closed, hash-chained, replayable. Play on words + technically true.

## The Problem With Other AI Options
- No formal safety. One model decides and executes. Loops forever.
- 4k token window crash. Giant tasks >500 chars overflow. No auto-chunking.
- No immutable history. Logs mutable, deletable.
- No replay. Can't verify tutorial learning.
- Expensive + cloud. $20-$200/mo, credits, API limits, screen sent to cloud.
- No overview of issues. No view of what was processed / skipped / misheard.

## Solution — Best of Both Worlds (UFO + Sentinel Substrate Merge)
Scrappy consumer automation (works on 8GB) + formal military-grade Cathedral safety.

![5 Models as Opcodes](visuals/geometric_blueprint_poster.webp)

### Layer L0-L1: World Input / Model Ports
5 local Ollama models: `phi3:mini` (FAST), `llama3.2:3b` (MID), `llama3.1:8b` (SMART anti-loop), `qwen2.5:7b` (QWEN Excel/code), `llava:7b` (EYES). All proposals only, no direct execution. Only AEGIS may mutate state.

### Layer L2-L5: Epistemic Stratum — The Best of Both Worlds
- **VECTOR (L2):** Read-only sensing. Cannot mutate.
- **Watcher-A (L3):** Internal consistency — detects loops, giant 4k overflow, destructive commands. Cannot execute. Cannot bypass Gate.
- **Watcher-B (L4):** Adversarial auditor — audits Watcher-A itself for bias drift, audit corruption, silent failure, false confidence.
- **Council Resolver (L5):** Merges A+B into exactly ONE SignalNode per cycle (Invariant I4). Agreement = reinforced confidence, Disagreement = escalated severity.
- **Signal Algebra:** Severity INFO/WARNING/ERROR/CRITICAL + confidence 0-1 + decay + escalation. Signals annotate, signals never decide.

![High-Throughput Pipeline](visuals/high_throughput_cathedral_computer_blueprint.webp)

### Layer L10-L12: Execution Stratum
- **CGIR (L10):** Causal Graph IR. Every task becomes StateNode + EventEdge + SignalNode. Machine-checkable, not free text.
- **Gate (L11):** Pure deterministic function, ONLY decision authority. Priority: 1 Ledger violation -> HARD_FAIL, 2 Critical Signal -> HARD_FAIL, 3 Temporal -> THROTTLE, 4 Contract -> HARD_FAIL, 5 VECTOR risk -> MODIFY/FALLBACK, 6 Planner quality -> ALLOW. Fail-closed, safe.
- **AEGIS/CESK (L12):** Only mutator. `LOAD -> PROPOSE -> CHECK -> COMMIT -> PROVE`. No other layer can mutate.

### Layer L13-L14: Truth & Replay
- **Ledger/Chronicle (L13):** Hash-chained: `hash(n) = SHA256(prev_hash + data)`. Immutable (I6), tamper-evident. Solves losing content when closing tab.
- **Replay/Gnosis (L14):** Type `replay` -> replays ledger, verifies chain (I9 Replayability). RCA + divergence detection.
- **Shadow/Ghost Mode:** For tutorials, run 2 shadows in parallel: 1s DETAILED vs 3s FAST. Neither mutates live state. Compare coherence, risk, latency, cost. Gate promotes best via `Shadow -> Replay -> Value Contract -> Gate Promotion`.

## Step-by-Step Setup — So You Can Set It Up Yourself (8GB RAM)
1. Install Ollama, pull models: `ollama pull phi3:mini llama3.2:3b llama3.1:8b qwen2.5:7b llava:7b`
2. Clone UFO: `git clone https://github.com/microsoft/UFO`
3. Create venv: `python -m venv ufo_env310` + `ufo_env310\Scripts\pip install requests pillow`
4. Place `ufo64.py` in UFO folder
5. Run: `.\ufo_env310\Scripts\python.exe .\ufo64.py`
6. Type `help` -> shows all commands, `status`, `replay`, `ledger`
7. Learn: `learn tutorial named my_first_test`

## Why This Is By Far a Great Alternative — Endless Possibilities, All Free
- Fixes 4k crash: auto-classifies GIANT, splits into fresh 4k windows, carries memory via files/phase1.txt
- Fixes looping: Watcher-A detects same task in last 5, Gate HARD_FAIL stops loop
- Overview + underlying issues: status shows tutorials/screenshots/tasks/MB + ledger validity, replay shows every execution + hash, pronunciation_errors_report.md shows misheard + Team Vote consensus
- Affordable: Works on 8GB RAM worldwide-known way
- Best of both worlds: automation + formal safety = capabilities not available elsewhere at any price
- Monetize: Free on birthdays (Jan 29), paid rest via Quora views

## Commands v6.4 Cathedral
```
help / ? -> this help
status -> project + ledger verify + replay
replay -> Replay Chronicle (Gnosis)
ledger -> Show chain validity
learn tutorial named X -> 1s DETAILED (Shadow mode picks best)
fastlearn tutorial named X -> 3s FAST
end project -> zips + verifies ledger
Any task -> Watcher-A -> Watcher-B -> Council -> Gate -> AEGIS
```

## Vs Others
| Feature | Operator / Claude Computer Use / Perplexity / Grok / Kimi | UFO Cathedral v6.4 |
|---|---|---|
| Cost | $20-$200/mo + credits | 100% Free, local |
| RAM | Cloud | 8GB RAM offline |
| Safety Gate | None | Gate HARD_FAIL fail-closed |
| Immutable Ledger | No | Yes, hash-chained SHA256 |
| Replay | No | Yes, I9 Replayability |
| Shadow Mode | No | Yes, N parallel proposals |
| Privacy | Screen leaves PC | Screen never leaves PC |

## License
MIT — Free for all, free on my birthday Jan 29, monetized via Quora upvotes.

Built by Jose Solorzano Luna — 2026
