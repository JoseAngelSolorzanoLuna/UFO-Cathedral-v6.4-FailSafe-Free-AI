
# ARCHITECTURE — CATHEDRAL Execution Substrate (UFO v6.4)

## Layer Stack (Merged from Sentinel Substrate + UFO)

| Layer | Name | Role |
|-------|------|------|
| L0 | World Input | Users, videos, screen, files |
| L1 | Model / Tool Ports | 5 local Ollama models — proposal only |
| L2 | VECTOR Sensor Fabric | Read-only sensing |
| L3 | Watcher-A | Internal consistency auditor |
| L4 | Watcher-B | Adversarial auditor (audits Watcher-A) |
| L5 | Council Resolver | Merge watchers → one SignalNode (I4) |
| L6 | World Model | Untrusted simulation (SMART) |
| L7 | Concept Formation Engine | Falsifiable abstractions |
| L8 | Transfer Engine | Cross-domain transfer tests |
| L9 | Planner | Monte Carlo candidate edge generator |
| L10 | CGIR | Causal Graph Intermediate Representation |
| L11 | Gate | Pure deterministic decision function — ONLY authority |
| L12 | AEGIS / CESK | Execution kernel — only mutator |
| L13 | Ledger / Chronicle | Immutable truth layer — hash-chained (I6) |
| L14 | Replay / Gnosis | Replay validation and RCA (I9) |
| L15 | Hardware RoT | Signing, attestation (future) |

## Data Flow
```
[L0 World Input]
       ↓
[L1 5 Models] → proposals only
       ↓
[L2 VECTOR] ─read-only─→ observations
       ↓
[L3 Watcher-A] + [L4 Watcher-B] → audit signals
       ↓
[L5 Council Resolver] → exactly one SignalNode
       ↓
[L9 Planner] → ranked CGIR edge candidates (auto-chunk if >4k)
       ↓
[L10 CGIR] → StateNode + EventEdge + SignalNode
       ↓
[L11 Gate] → ALLOW | MODIFY | THROTTLE | FALLBACK | HARD_FAIL
       ↓
[L12 AEGIS/CESK] → LOAD → PROPOSE → CHECK → COMMIT → PROVE
       ↓
[L13 Ledger/Chronicle] → immutable record hash(prev+data)
       ↓
[L14 Replay/Gnosis] → validation and RCA
```

## CGIR Node Types (from friend's work, applied to UFO)
- **StateNode** — snapshot of PC: windows open, files, tutorials
- **EventEdge** — transition with invariant mask and signal binding
- **SignalNode** — severity/confidence from Council
- **TimedEdge** — latency constraints
- **InvariantBinding** — bound invariant rule
- **HardwareBinding** — (future) RoT latch

## Gate Decision Priority (deterministic)
1. Ledger violation → HARD_FAIL
2. Critical SignalNode → HARD_FAIL
3. Temporal / hardware violation → THROTTLE
4. Contract violation (rm -rf) → HARD_FAIL
5. VECTOR risk score → MODIFY / FALLBACK
6. Planner proposal quality → ALLOW

## Three Strata
### PROPOSAL STRATUM (Untrusted)
World Model, Concept Engine, Transfer Engine, Planner, Shadow branches, 5 models

### EPISTEMIC STRATUM (Sensing, Audit, Resolution)
VECTOR, Watcher-A, Watcher-B, Council, Signal Algebra

### EXECUTION STRATUM (Formal Execution)
CGIR, Gate, AEGIS, Ledger, Replay, Hardware RoT

## Shadow / Ghost Mode
For every real execution, N shadow branches run in parallel:
- Compare: coherence, causal lift, risk, latency, cost, contract compliance, failure rate
- Promotion: Shadow → Replay → Value Contract → Gate Promotion
- Live self-modification NEVER allowed.

## Invariants (from Sentinel, enforced in v6.4)
- I4: Exactly one SignalNode per cycle
- I6: Ledger is canonical history (no mod/del)
- I9: All committed executions must be replayable
- Fail-closed: ambiguous → HARD_FAIL, not continue
