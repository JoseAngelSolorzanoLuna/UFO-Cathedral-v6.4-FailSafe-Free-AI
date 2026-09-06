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

# ========== SAFETY CARD: persistent state for replay promotion ==========

@dataclass
class SafetyCard:
    name: str
    source: str = "learn"
    status: str = "UNVERIFIED"
    safe_streak: int = 0
    needed: int = 3

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d: dict):
        return SafetyCard(
            name=d.get('name'),
            source=d.get('source','learn'),
            status=d.get('status','UNVERIFIED'),
            safe_streak=int(d.get('safe_streak',0)),
            needed=int(d.get('needed',3))
        )


def cards_path(project_path: Path) -> Path:
    return project_path / "safety_cards.json"


def load_cards(project_path: Path) -> dict:
    p = cards_path(project_path)
    cards = {}
    if p.exists():
        try:
            raw = json.loads(p.read_text(encoding='utf-8'))
            for name, d in raw.items():
                cards[name] = SafetyCard.from_dict(d)
        except Exception:
            pass
    return cards


def save_cards(project_path: Path, cards: dict) -> None:
    p = cards_path(project_path)
    out = {name: card.to_dict() for name, card in cards.items()}
    p.write_text(json.dumps(out, indent=2), encoding='utf-8')


def new_card(name: str, source: str = "learn") -> SafetyCard:
    return SafetyCard(name=name, source=source, status="UNVERIFIED", safe_streak=0, needed=3)


def last_event_safe(ledger) -> bool:
    # True unless last entry type is BLOCKED or ledger missing/empty
    if ledger is None or not getattr(ledger, 'entries', None):
        return False
    last_type = ledger.entries[-1].get('type')
    return last_type not in ("BLOCKED",)


def try_promote(card: SafetyCard, ledger) -> SafetyCard:
    # If last ledger event is unsafe, reset streak and remain UNVERIFIED
    if not last_event_safe(ledger):
        card.safe_streak = 0
        card.status = "UNVERIFIED"
        print(f"[STREAK RESET] {card.name} unsafe ledger event → UNVERIFIED 0/{card.needed}")
        return card

    # Otherwise increment streak
    card.safe_streak += 1
    if card.safe_streak >= card.needed and card.status != "TRUTH":
        card.status = "TRUTH"
        print(f"[PROMOTION GATE] {card.name} promoted UNVERIFIED -> TRUTH after {card.needed} consecutive safe replays")
    else:
        print(f"[REPLAY {card.safe_streak}] {card.name} safe_streak={card.safe_streak}/{card.needed}")
    return card

# ========== LEDGER ==========

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
# (remaining code unchanged...)

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

# ... rest of file unchanged until main (we kept existing functions) ...

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

# (other helper functions like list_projects, zip_project, set_mode, run_tutorial_with_shadow remain unchanged)

# For brevity we will reuse the remainder of the original file content as-is, but we must inject wiring into main for safety cards.

# ========== MAIN (with Safety Card wiring) ==========

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

    # Safety Card runtime state
    cards = {}
    last_learned = None

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

            # Load safety cards for this project
            cards = load_cards(current_project)
            last_learned = None
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

            # Load safety cards for resumed project
            cards = load_cards(current_project)
            last_learned = None
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
            # print safety cards
            if cards:
                for c in cards.values():
                    if c.status == 'UNVERIFIED':
                        print(f"[UNVERIFIED] {c.name} safe_streak={c.safe_streak}/{c.needed}")
                    else:
                        print(f"[TRUTH] {c.name}")
            else:
                print("No Safety Cards yet. learn a tutorial first.")
            continue
        if low == 'replay':
            ledger.replay()
            if not cards:
                print("No Safety Cards yet. learn a tutorial first.")
            else:
                # choose targets: prefer last learned, else all UNVERIFIED
                targets = []
                if last_learned and last_learned in cards:
                    targets = [last_learned]
                else:
                    targets = [name for name, c in cards.items() if c.status == 'UNVERIFIED']
                if not targets:
                    print("No UNVERIFIED Safety Cards to promote.")
                for t in targets:
                    card = cards[t]
                    try_promote(card, ledger)
                save_cards(current_project, cards)
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
                # add safety card for this tutorial
                cards[t_name] = new_card(t_name, source="tutorial")
                save_cards(current_project, cards)
                last_learned = t_name
                print(f"[UNVERIFIED] {t_name} → needs 3 consecutive safe replays")
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
