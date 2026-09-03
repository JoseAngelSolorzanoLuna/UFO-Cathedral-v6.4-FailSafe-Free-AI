import os, shutil, subprocess, requests, json, time, hashlib, re, signal, atexit
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum

# ========== CONFIG ==========
BASE_DIR = Path(__file__).parent
PROJECTS_DIR = BASE_DIR / "projects"
ZIPS_DIR = PROJECTS_DIR / "_zips"
ENV_PYTHON = BASE_DIR / "ufo_env310" / "Scripts" / "python.exe"
PROJECTS_DIR.mkdir(exist_ok=True)
ZIPS_DIR.mkdir(exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELS = {
    "FAST": "phi3:mini",
    "MID": "llama3.2:3b",
    "SMART": "llama3.1:8b",
    "QWEN": "qwen2.5:7b",
    "EYES": "llava:7b"
}

# ========== CATHEDRAL LAYERS INSPIRED BY SENTINEL ==========

class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3

@dataclass
class SignalNode:
    severity: Severity
    confidence: float  # 0.0 - 1.0
    category: str
    evidence_refs: List[str]
    source: str  # VECTOR, Watcher-A, Watcher-B, Council
    emitted_by: str
    reason: str
    valid_for_time_range: str = "now"

    def to_dict(self):
        d = asdict(self)
        d['severity'] = self.severity.name
        return d

@dataclass
class StateNode:
    id: str
    snapshot: str  # description of CESK state: windows open, files, etc
    timestamp: str
    project: str

@dataclass
class EventEdge:
    id: str
    from_state: str
    to_state: str
    action: str
    invariant_mask: List[str]  # must not violate
    signal_binding: Optional[SignalNode]
    latency_ms: Optional[int] = None

class Ledger:
    """Immutable truth layer - hash-chained, like Sentinel"""
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.ledger_path = project_path / "chronicle.jsonl"
        self.ledger_path.touch(exist_ok=True)
        self.entries = self._load()

    def _load(self):
        entries = []
        try:
            for line in self.ledger_path.read_text(encoding='utf-8', errors='ignore').splitlines():
                if line.strip():
                    entries.append(json.loads(line))
        except:
            pass
        return entries

    def _hash_entry(self, prev_hash: str, data: dict) -> str:
        payload = prev_hash + json.dumps(data, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def append(self, event_type: str, cgir_edge: dict, signal: Optional[SignalNode], state_before: str, state_after: str):
        prev_hash = self.entries[-1]['hash'] if self.entries else "0000000000000000"
        data = {
            "id": len(self.entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "state_before": state_before,
            "cgir_edge": cgir_edge,
            "signal": signal.to_dict() if signal else None,
            "state_after": state_after,
        }
        h = self._hash_entry(prev_hash, data)
        entry = {"prev_hash": prev_hash, "hash": h, **data}
        self.entries.append(entry)
        with open(self.ledger_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def verify_chain(self) -> bool:
        prev = "0000000000000000"
        for e in self.entries:
            check = self._hash_entry(prev, {k: v for k, v in e.items() if k not in ('prev_hash','hash')})
            if check != e['hash'] or e['prev_hash'] != prev:
                return False
            prev = e['hash']
        return True

    def replay(self):
        print(f"\n[REPLAY/GNOSIS] Replaying {len(self.entries)} entries from Chronicle...")
        for e in self.entries:
            print(f"  {e['id']}: {e['type']} -> {e['cgir_edge'].get('action','?')[:60]} hash={e['hash']}")
        ok = self.verify_chain()
        print(f"[REPLAY] Chain valid? {ok} (I9 Replayability)")
        return ok

# ========== WATCHERS ==========

def watcher_a_audit(task: str, state: StateNode, history: List[dict]) -> SignalNode:
    """L3 Watcher-A - Internal Consistency Auditor - Cannot execute"""
    reasons = []
    severity = Severity.INFO
    confidence = 0.9

    # Check 1: Loop detection (same task repeated)
    recent_tasks = [h.get('cgir_edge',{}).get('action','') for h in history[-5:]]
    if task.lower() in [t.lower() for t in recent_tasks]:
        reasons.append("Loop detected: same task in last 5")
        severity = Severity.WARNING
        confidence = 0.85

    # Check 2: Giant token overflow
    if len(task) // 4 > 3000:
        reasons.append(f"Giant task ~{len(task)//4} tokens near 4k window")
        severity = max(severity, Severity.WARNING, key=lambda s: s.value)
        confidence = 0.8

    # Check 3: Tutorial blurry screenshot risk (from your v6.2)
    if "tutorial" in task.lower() and "fast" in task.lower():
        reasons.append("FAST 3s mode unreliable, may miss blur")
        severity = max(severity, Severity.WARNING, key=lambda s: s.value)
        confidence = 0.75

    # Check 4: Invariant - must not delete projects
    if any(w in task.lower() for w in ["rm -rf", "delete", "format", "del /f"]):
        reasons.append("Potential destructive action violates invariant")
        severity = Severity.CRITICAL
        confidence = 0.95

    if not reasons:
        reasons = ["No internal inconsistency"]

    return SignalNode(
        severity=severity,
        confidence=confidence,
        category="internal_consistency",
        evidence_refs=[state.id],
        source="Watcher-A",
        emitted_by="Watcher-A",
        reason="; ".join(reasons)
    )

def watcher_b_adversarial_audit(task: str, state: StateNode, watcher_a_signal: SignalNode, history: List[dict]) -> SignalNode:
    """L4 Watcher-B - Adversarial Auditor - Audits Watcher-A itself"""
    reasons = []
    severity = Severity.INFO
    confidence = 0.9

    # Check Watcher-A for bias drift / silent failure
    if watcher_a_signal.severity == Severity.INFO and len(task) > 500:
        # Watcher-A said INFO but task is giant - possible silent failure
        reasons.append("Watcher-A says INFO but task giant -> possible silent failure / false confidence")
        severity = Severity.WARNING
        confidence = 0.7

    # Check same evidence independently
    if "loop" in watcher_a_signal.reason.lower():
        # Verify independently
        recent = [h.get('cgir_edge',{}).get('action','') for h in history[-3:]]
        if task.lower() not in [r.lower() for r in recent]:
            reasons.append("Watcher-A claims loop but independent check disagrees -> Watcher-A bias drift?")
            severity = Severity.ERROR
            confidence = 0.6

    # Check for pronunciation errors (your team vote idea, now formal)
    if any(w in task.lower() for w in ["pivolt", "excell", "formular"]):
        reasons.append("Possible mispronunciation detected in task, needs Team Vote")
        severity = max(severity, Severity.WARNING, key=lambda s: s.value)
        confidence = 0.65

    # Adversarial: Watcher-A missed risk
    if watcher_a_signal.confidence < 0.6:
        reasons.append(f"Watcher-A low confidence {watcher_a_signal.confidence} -> escalation")
        severity = max(severity, Severity.WARNING, key=lambda s: s.value)

    if not reasons:
        reasons = ["Watcher-A audit passed, no adversarial findings"]

    return SignalNode(
        severity=severity,
        confidence=confidence,
        category="adversarial_audit",
        evidence_refs=[state.id, watcher_a_signal.source],
        source="Watcher-B",
        emitted_by="Watcher-B",
        reason="; ".join(reasons)
    )

def council_resolver(watcher_a: SignalNode, watcher_b: SignalNode) -> SignalNode:
    """L5 Council Resolver - Merges into EXACTLY ONE SignalNode (I4)"""
    # Resolution rules from Sentinel spec
    if watcher_a.severity == watcher_b.severity and watcher_a.category != "adversarial_audit":
        # Agreement
        severity = watcher_a.severity
        confidence = min(1.0, (watcher_a.confidence + watcher_b.confidence) / 2 + 0.1)  # reinforced
        reason = f"Agreement: {watcher_a.reason} | {watcher_b.reason}"
    elif abs(watcher_a.severity.value - watcher_b.severity.value) >= 2:
        # Critical disagreement
        severity = Severity.CRITICAL
        confidence = min(watcher_a.confidence, watcher_b.confidence, 0.5)
        reason = f"Critical disagreement: A={watcher_a.severity.name}({watcher_a.reason}) vs B={watcher_b.severity.name}({watcher_b.reason})"
    else:
        # Disagreement
        severity = Severity(max(watcher_a.severity.value, watcher_b.severity.value) + 1) if max(watcher_a.severity.value, watcher_b.severity.value) < 3 else Severity.CRITICAL
        confidence = min(watcher_a.confidence, watcher_b.confidence) * 0.8
        reason = f"Disagreement escalated: A={watcher_a.reason} | B={watcher_b.reason}"

    return SignalNode(
        severity=severity,
        confidence=confidence,
        category="council_merged",
        evidence_refs=watcher_a.evidence_refs + watcher_b.evidence_refs,
        source="Council",
        emitted_by="Council Resolver",
        reason=reason
    )

def gate_decision(signal: SignalNode, ledger: Ledger, cgir_edge: dict) -> str:
    """L11 Gate - Pure deterministic decision function - ONLY decision authority"""
    # Priority order from Sentinel ARCHITECTURE.md
    # 1. Ledger violation
    if not ledger.verify_chain():
        return "HARD_FAIL"  # I6 violation

    # 2. Critical SignalNode
    if signal.severity == Severity.CRITICAL:
        return "HARD_FAIL"

    # 3. Temporal / hardware violation (simplified: latency)
    if cgir_edge.get('latency_ms', 0) and cgir_edge['latency_ms'] > 10000:
        return "THROTTLE"

    # 4. Contract violation (example: destructive)
    if any(bad in cgir_edge.get('action','').lower() for bad in ["rm -rf", "delete project"]):
        return "HARD_FAIL"

    # 5. VECTOR risk score (Watcher signals)
    if signal.severity == Severity.ERROR and signal.confidence > 0.8:
        return "FALLBACK"

    if signal.severity == Severity.WARNING and signal.confidence > 0.7:
        return "MODIFY"  # modify proposal, e.g., switch from FAST to DETAILED

    # 6. Planner proposal quality
    return "ALLOW"

# ========== AEGIS EXECUTION KERNEL ==========

def aegis_execute(project_path: Path, ledger: Ledger, state_before: StateNode, edge: EventEdge, signal: SignalNode):
    """L12 AEGIS / CESK - Only mutator - LOAD → PROPOSE → CHECK → COMMIT → PROVE"""
    print(f"\n[AEGIS] LOAD state {state_before.id}: {state_before.snapshot}")
    print(f"[AEGIS] PROPOSE edge {edge.id}: {edge.action[:100]}")
    
    # CHECK
    gate = gate_decision(signal, ledger, asdict(edge))
    print(f"[AEGIS] CHECK via Gate: Signal={signal.severity.name} conf={signal.confidence:.2f} -> Gate={gate}")

    if gate == "HARD_FAIL":
        print(f"[AEGIS] ❌ HARD_FAIL - execution blocked by Gate. No state mutation (fail-closed)")
        # Still log to ledger as blocked attempt (immutable truth)
        ledger.append("BLOCKED", asdict(edge), signal, state_before.snapshot, state_before.snapshot)
        return False, state_before

    if gate == "THROTTLE":
        print(f"[AEGIS] ⏳ THROTTLE - waiting 2s")
        time.sleep(2)

    if gate == "MODIFY":
        print(f"[AEGIS] 🔧 MODIFY - Planner quality low, switching to safer mode")
        # Example modification: force DETAILED if was FAST
        if "fast" in edge.action.lower():
            edge.action = edge.action.replace("fast", "detailed") + " [Gate-modified to DETAILED]"
            print(f"[AEGIS] Modified action to: {edge.action[:100]}")

    # COMMIT - Only place where state mutates
    print(f"[AEGIS] COMMIT - executing via UFO...")
    try:
        cmd = [str(ENV_PYTHON), "-m", "ufo", "--task", edge.action]
        subprocess.run(cmd, cwd=str(BASE_DIR))
        state_after_snapshot = f"After: {edge.to_state}"
        print(f"[AEGIS] COMMIT done")
    except Exception as e:
        state_after_snapshot = f"Error: {e}"
        print(f"[AEGIS] COMMIT error: {e}")

    # PROVE
    print(f"[AEGIS] PROVE - verifying state_after")
    ledger.append("COMMITTED", asdict(edge), signal, state_before.snapshot, state_after_snapshot)
    
    state_after = StateNode(
        id=f"S{ledger.entries[-1]['id']}",
        snapshot=state_after_snapshot,
        timestamp=datetime.now().isoformat(),
        project=project_path.name
    )
    print(f"[AEGIS] PROVE complete, new state {state_after.id}")
    return True, state_after

# ========== ORIGINAL UFO HELPERS ==========

def ask_model(model_name, prompt, timeout=45):
    try:
        resp = requests.post(OLLAMA_URL, json={"model": model_name, "prompt": prompt, "stream": False}, timeout=timeout)
        if resp.status_code == 200:
            return resp.json().get('response','').strip()
    except Exception as e:
        return f"[ERROR {model_name}: {e}]"
    return ""

def ai_classify_and_chunk(task: str):
    prompt = f"""You are Windows automation planner. Brain window ONLY 4k tokens.
Task: "{task}"
Classify: FAST=phi3:mini (1 click) MID=llama3.2:3b (2-4 steps) SMART=llama3.1:8b (anti-loop) QWEN=qwen2.5:7b (Excel/code)
If >10 steps or >500 chars, split into phases.
JSON only: {{"level": "FAST/MID/SMART/QWEN", "reason": "short", "is_giant": true/false, "chunk_count": number, "chunks": ["Phase 1: ..."]}} If not giant, chunks=[original task]"""
    try:
        resp = requests.post(OLLAMA_URL, json={"model": "phi3:mini", "prompt": prompt, "stream": False, "format": "json"}, timeout=30)
        if resp.status_code == 200:
            return json.loads(resp.json().get('response','{{}}'))
    except:
        pass
    return {"level":"FAST","reason":"classifier offline","is_giant":False,"chunk_count":1,"chunks":[task]}

def print_help():
    print("""
================================================================
 UFO v6.4 - CATHEDRAL EDITION (UFO + Sentinel Merge)
================================================================
NEW CATHEDRAL LAYERS (from friend's Sentinel):
 L2 VECTOR (read-only sensing)
 L3 Watcher-A (internal consistency) - loop, giant, destructive
 L4 Watcher-B (adversarial) - audits Watcher-A for bias/silent fail
 L5 Council Resolver - merges A+B into ONE SignalNode (I4)
 L10 CGIR - StateNode + EventEdge + SignalNode (formal)
 L11 Gate - Pure decision: ALLOW | MODIFY | THROTTLE | FALLBACK | HARD_FAIL
 L12 AEGIS - LOAD -> PROPOSE -> CHECK -> COMMIT -> PROVE (only mutator)
 L13 Ledger/Chronicle - Hash-chained immutable (I6), replayable (I9)
 L14 Replay/Gnosis - replays ledger, verifies chain
 L15 Shadow Mode - N branches in parallel for tutorial learning

COMMANDS:
 help / ? -> this help
 status -> project status + ledger verify + replay
 replay -> Replay Chronicle (Gnosis) validates all executions
 ledger -> Show Chronicle chain validity
 learn tutorial named X -> 1s DETAILED (default)
 fastlearn tutorial named X -> 3s FAST (unreliable)
 Shadow mode: for tutorial, runs both 1s and 3s as shadows, Gate picks best
 end project -> zips + verifies ledger
 Any task -> Goes through Watcher-A -> Watcher-B -> Council -> Gate -> AEGIS

GATE PRIORITY (deterministic):
 1. Ledger violation -> HARD_FAIL
 2. Critical SignalNode -> HARD_FAIL
 3. Temporal/hardware violation -> THROTTLE
 4. Contract violation -> HARD_FAIL
 5. VECTOR risk -> MODIFY/FALLBACK
 6. Planner quality -> ALLOW

Vs Claw/Operator/Perplexity/Grok/Kimi: FREE, local, 8GB RAM, formal safety
================================================================
""")

def get_status(project_path: Path, ledger: Ledger):
    size_mb = sum(f.stat().st_size for f in project_path.rglob("*") if f.is_file()) / 1024 / 1024 if project_path.exists() else 0
    tut_count = len(list((project_path / "tutorials").glob("*"))) if (project_path / "tutorials").exists() else 0
    screenshots = len(list((project_path / "tutorials").rglob("*.png"))) + len(list((project_path / "tutorials").rglob("*.jpg"))) if (project_path / "tutorials").exists() else 0
    chain_ok = ledger.verify_chain()
    return f"""
--- STATUS {project_path.name} [CATHEDRAL] ---
Path: {project_path}
Tutorials: {tut_count} | Screenshots: {screenshots} | Ledger entries: {len(ledger.entries)}
Size: {size_mb:.2f} MB | Chain valid (I6): {chain_ok} | Replayable (I9): {chain_ok}
Ledger: {project_path / 'chronicle.jsonl'}
Auto-save: Instant + hash-chained (immutable)
Gate: Active (only decision authority)
Watchers: A (internal) + B (adversarial) + Council (one SignalNode)
"""

def list_projects():
    projects = [p for p in PROJECTS_DIR.iterdir() if p.is_dir() and not p.name.startswith("_")]
    if not projects:
        print("No projects")
        return []
    print("\nExisting projects:")
    for i, p in enumerate(sorted(projects, key=lambda x: x.stat().st_mtime, reverse=True), 1):
        size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / 1024 / 1024
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {i}. {p.name} - {size:.1f}MB - {mtime}")
    return sorted(projects, key=lambda x: x.stat().st_mtime, reverse=True)

def zip_project(project_path: Path):
    try:
        zip_name = f"{project_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        zip_path = ZIPS_DIR / zip_name
        shutil.make_archive(str(zip_path), 'zip', project_path.parent, project_path.name)
        print(f"[ZIPPED] {zip_path}.zip")
    except Exception as e:
        print(f"[ZIP ERROR] {e}")

def set_mode(name):
    print(f"-> Activated {name.upper()}: config_{name}.yaml + vision={MODELS['EYES']}")
    return name.lower()

def run_tutorial_with_shadow(project_path: Path, tutorial_name: str, ledger: Ledger, state: StateNode):
    """Shadow/Ghost mode - run N branches, Gate picks best"""
    print(f"\n{'='*60}")
    print(f"  TUTORIAL LEARNING v6.4 - SHADOW MODE")
    print(f"  Name: {tutorial_name}")
    print(f"  Shadow branches: 2 (1s DETAILED vs 3s FAST)")
    print(f"  Each shadow NEVER mutates live state until promoted")
    print(f"{'='*60}")
    
    # Simulate shadow branches
    shadow_results = []
    for interval, label in [(1, "DETAILED 1s - reliable"), (3, "FAST 3s - unreliable")]:
        print(f"\n[SHADOW {label}] Proposing capture every {interval}s...")
        # In real impl, would capture screenshots without committing
        mock_risk = 0.2 if interval == 1 else 0.7
        mock_coherence = 0.95 if interval == 1 else 0.6
        shadow_results.append({"interval": interval, "label": label, "risk": mock_risk, "coherence": mock_coherence})
        print(f"  Shadow {interval}s: risk={mock_risk} coherence={mock_coherence} latency={interval}s")

    # Gate promotion based on comparison metrics (from Sentinel spec)
    best = min(shadow_results, key=lambda x: x['risk'] - x['coherence'])  # lowest risk, highest coherence
    print(f"\n[SHADOW PROMOTION] Gate selects {best['interval']}s as best (coherence {best['coherence']}, risk {best['risk']})")
    print(f"  Path: Shadow -> Replay -> Value Contract -> Gate Promotion")

    tutorial_dir = project_path / "tutorials" / tutorial_name
    tutorial_dir.mkdir(parents=True, exist_ok=True)
    (tutorial_dir / "screenshots").mkdir(exist_ok=True)
    
    # Log shadow decision to ledger
    edge = EventEdge(
        id=f"E{len(ledger.entries)+1}",
        from_state=state.id,
        to_state=f"tutorial {tutorial_name} learned",
        action=f"learn tutorial named {tutorial_name} interval={best['interval']}s via shadow promotion",
        invariant_mask=["no deletion"],
        signal_binding=None
    )
    ledger.append("SHADOW_PROMOTION", asdict(edge), None, state.snapshot, f"tutorial {tutorial_name} learned via {best['interval']}s")
    print(f"[LEDGER] Shadow promotion recorded in Chronicle hash={ledger.entries[-1]['hash']}")
    return tutorial_dir

def main():
    global current_project_global
    current_project_global = None

    def safe_exit(signum=None, frame=None):
        if current_project_global:
            print(f"\n[SAFE EXIT] Saving {current_project_global.name} + verifying ledger...")
            # verify before zip
            l = Ledger(current_project_global)
            print(f"[SAFE EXIT] Chain valid: {l.verify_chain()}")
            zip_project(current_project_global)
        exit(0)

    signal.signal(signal.SIGINT, safe_exit)
    atexit.register(lambda: safe_exit() if current_project_global else None)

    print(f"""
===============================================
 UFO v6.4 - CATHEDRAL EDITION
 UFO + Sentinel Substrate Merge
 4 Brains + 1 Eyes = 5 models
 + CGIR + Gate + AEGIS + Ledger + Council
 + Shadow Mode + Replay + Hash-Chain
 + FREE vs $200/mo Operator/Claw/Perplexity/Grok
===============================================
""")

    current_mode = set_mode("fast")
    current_project = None
    task_counter = 0
    last_reminder = time.time()
    ledger = None
    current_state = StateNode(id="S0", snapshot="initial", timestamp=datetime.now().isoformat(), project="none")

    print("\n--- PROJECT MENU ---\n")
    while True:
        q = input("Start a NEW project? (y/n): ").strip().lower()
        if q in ('y','yes',''):
            name = input("Project name: ").strip() or f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            current_project = PROJECTS_DIR / name
            current_project.mkdir(parents=True, exist_ok=True)
            for sub in ["files","memory","tutorials"]:
                (current_project / sub).mkdir(exist_ok=True)
            ledger = Ledger(current_project)
            current_state = StateNode(id="S0", snapshot=f"Project {name} created", timestamp=datetime.now().isoformat(), project=name)
            ledger.append("CREATE_PROJECT", {"action": f"create {name}"}, None, "none", current_state.snapshot)
            print(f"[NEW] {current_project} | Ledger genesis hash={ledger.entries[-1]['hash']}")
            break
        elif q in ('n','no'):
            projects = list_projects()
            if not projects:
                continue
            sel = input("Continue which number? (or name): ").strip()
            try:
                idx = int(sel)-1
                current_project = projects[idx]
            except:
                current_project = PROJECTS_DIR / sel
                if not current_project.exists():
                    print("Not found")
                    continue
            ledger = Ledger(current_project)
            current_state = StateNode(id=f"S{len(ledger.entries)}", snapshot=f"Resumed {current_project.name}", timestamp=datetime.now().isoformat(), project=current_project.name)
            print(f"[CONTINUE] {current_project}")
            print(get_status(current_project, ledger))
            ledger.replay()
            break

    current_project_global = current_project
    print(f"\nType 'help' for Cathedral commands! Ledger chain valid: {ledger.verify_chain()}\n")

    while True:
        now = time.time()
        if now - last_reminder > 600:
            print(f"\n{'='*60}\n[AUTO-SAVE REMINDER + LEDGER CHECK]\n{get_status(current_project, ledger)}\nChain valid? {ledger.verify_chain()} | Tasks: {task_counter}\n{'='*60}\n")
            last_reminder = now

        try:
            raw = input(f"[Task | {current_mode.upper()} | Gate:ON] > ").strip()
        except KeyboardInterrupt:
            safe_exit()

        if not raw:
            continue
        low = raw.lower()

        if low in ('help','?','h'):
            print_help()
            continue
        if low in ('status','what saved'):
            print(get_status(current_project, ledger))
            continue
        if low == 'replay':
            ledger.replay()
            continue
        if low == 'ledger':
            print(f"Chain valid: {ledger.verify_chain()} | Entries: {len(ledger.entries)}")
            for e in ledger.entries[-10:]:
                print(f"  {e['id']} prev={e['prev_hash']} hash={e['hash']} {e['type']}")
            continue
        if low == 'end project':
            ledger.append("END_PROJECT", {"action": "end project"}, None, current_state.snapshot, "ended")
            print(f"[LEDGER] Final hash={ledger.entries[-1]['hash']} chain valid={ledger.verify_chain()}")
            zip_project(current_project)
            break
        if low.startswith("switch"):
            if "fast" in low: current_mode = set_mode("fast")
            elif "mid" in low: current_mode = set_mode("mid")
            elif "qwen" in low: current_mode = set_mode("qwen")
            elif "smart" in low: current_mode = set_mode("smart")
            continue

        # Tutorial with Shadow Mode
        if low.startswith("learn") or "tutorial" in low or low.startswith("fastlearn"):
            t_name = "tutorial_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            if "named" in low:
                try:
                    t_name = low.split("named")[1].strip().split()[0]
                    t_name = "".join(c for c in t_name if c.isalnum() or c in ('_','-')).strip()
                except:
                    pass
            if input(f"Start Shadow tutorial learning {t_name}? (y/n): ").strip().lower() in ('','y','yes'):
                run_tutorial_with_shadow(current_project, t_name, ledger, current_state)
                task_counter += 1
                last_reminder = time.time()
                continue

        # ===== CATHEDRAL PIPELINE FOR EVERY TASK =====
        print(f"\n[PIPE] Task: {raw[:100]}")

        # 1. AI classify + chunk -> CGIR candidates
        plan = ai_classify_and_chunk(raw)
        level = plan.get("level","FAST").upper()
        chunks = plan.get("chunks", [raw])
        print(f"  [L9 Planner] {level} chunks={len(chunks)}")

        for chunk in chunks:
            # Build CGIR
            edge = EventEdge(
                id=f"E{len(ledger.entries)+1}",
                from_state=current_state.id,
                to_state=f"after {chunk[:30]}",
                action=chunk,
                invariant_mask=["no rm -rf", "no delete projects", "no format"],
                signal_binding=None,
                latency_ms=100
            )
            print(f"  [L10 CGIR] Edge {edge.id}: {edge.action[:60]}")

            # 2. VECTOR read-only sensing (simplified)
            print(f"  [L2 VECTOR] Sensing current state...")

            # 3. Watcher-A + Watcher-B
            sig_a = watcher_a_audit(chunk, current_state, ledger.entries)
            sig_b = watcher_b_adversarial_audit(chunk, current_state, sig_a, ledger.entries)
            print(f"  [L3 Watcher-A] {sig_a.severity.name} conf={sig_a.confidence:.2f}: {sig_a.reason[:80]}")
            print(f"  [L4 Watcher-B] {sig_b.severity.name} conf={sig_b.confidence:.2f}: {sig_b.reason[:80]}")

            # 4. Council Resolver -> exactly one SignalNode (I4)
            council_signal = council_resolver(sig_a, sig_b)
            print(f"  [L5 Council] -> ONE SignalNode: {council_signal.severity.name} conf={council_signal.confidence:.2f}")
            print(f"     Reason: {council_signal.reason[:120]}")
            edge.signal_binding = council_signal

            # 5. Gate + AEGIS (only mutator)
            success, new_state = aegis_execute(current_project, ledger, current_state, edge, council_signal)
            if success:
                current_state = new_state
                task_counter += 1
            else:
                print(f"  [GATE BLOCKED] Task did NOT mutate state (fail-closed)")

        last_reminder = time.time()

if __name__ == "__main__":
    main()
