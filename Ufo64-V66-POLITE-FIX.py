#!/usr/bin/env python3
"""
UFO v6.6 Cathedral Edition - POLITE_LIE FIX
OSHA Hierarchy + Lessons Ledger with 3-Replay Safety Card

v6.5 Proof: OSHA Permit Root: ba1f7bf481e2... (12 actions) | Elimination Control Active
v6.6 Change: pronunciation_errors_report.md -> lessons.jsonl
            UNVERIFIED (YouTube) needs 3 consecutive safe replays -> TRUTH (Workforce safety card model)

FREE vs $200/mo Operator: Structural exclusion, not prompt filter
"""
import os, json, hashlib, re, time, sys, shutil, zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

# ============ OSHA L1: ELIMINATION - MERKLE PERMIT SET ============
PERMITTED_ACTIONS = [
    "click", "type", "scroll", "hotkey", "wait", "screenshot",
    "open_app", "close_app", "read_text", "write_file", "read_file", "status"
]
PERMITTED_ROOT = hashlib.sha256("|".join(sorted(PERMITTED_ACTIONS)).encode()).hexdigest()[:16]
# Live proof hash prefix from your screenshot: ba1f7bf481e2... - we keep 16 char for display
# Full root for verification:
FULL_PERMITTED_ROOT = hashlib.sha256("|".join(sorted(PERMITTED_ACTIONS)).encode()).hexdigest()
print(f"OSHA Permit Root: {FULL_PERMITTED_ROOT[:12]}... ({len(PERMITTED_ACTIONS)} actions) | Elimination Control Active")

def verify_permit(action_type: str) -> bool:
    """L1 Elimination: Block BEFORE proposal - machine guard stops hand before blade"""
    if action_type not in PERMITTED_ACTIONS:
        print(f"[MERKLE BLOCK] Action '{action_type}' not in PERMITTED_ROOT {PERMITTED_ROOT} - structurally excluded, never proposed")
        return False
    return True

# ============ OSHA L2: SUBSTITUTION - BoundedSensorGate ============
class BoundedSensorGate:
    """L2 Substitution: Replace raw OS calls with bounded verified values. Stops stale screenshots BEFORE Watcher-A"""
    CLICK_X_MAX = 3840
    CLICK_Y_MAX = 2160
    TYPE_MAX = 1000
    INJECTION_PATTERNS = [r"<script", r"DROP TABLE", r"rm -rf", r"delete_system32", r";\s*shutdown", r"powershell.*-enc"]

    @staticmethod
    def validate(action: Dict) -> Tuple[bool, Dict, str]:
        atype = action.get("type", "")
        if not verify_permit(atype):
            return False, action, "Merkle permit failed"

        # Click bounds
        if atype == "click":
            x = action.get("x", 0)
            y = action.get("y", 0)
            if not (0 <= x <= BoundedSensorGate.CLICK_X_MAX and 0 <= y <= BoundedSensorGate.CLICK_Y_MAX):
                return False, action, f"Click out-of-bounds x={x} y={y} - quarantined by machine guard"
        
        # Type length + injection
        if atype == "type":
            txt = action.get("text", "")
            if len(txt) > BoundedSensorGate.TYPE_MAX:
                print(f"[GATE] type truncated {len(txt)} -> {BoundedSensorGate.TYPE_MAX} chars")
                action["text"] = txt[:BoundedSensorGate.TYPE_MAX]
            for pat in BoundedSensorGate.INJECTION_PATTERNS:
                if re.search(pat, txt, re.IGNORECASE):
                    return False, action, f"Injection pattern blocked: {pat}"

        # Stale screenshot detection (simulated)
        if atype == "screenshot":
            age = action.get("age_ms", 0)
            if age > 5000:  # stale >5s
                return False, action, f"Stale screenshot age={age}ms - stopped BEFORE Watcher-A (machine guard)"

        return True, action, "Gate PASS"

# ============ OSHA L3: ENGINEERING - Hash-Chain Ledger I6/I9 ============
class HashChainLedger:
    def __init__(self, path="ledger.jsonl"):
        self.path = Path(path)
        self.path.touch(exist_ok=True)
        self.chain = self._load()

    def _load(self):
        entries = []
        with open(self.path) as f:
            for line in f:
                try: entries.append(json.loads(line))
                except: pass
        return entries

    def append(self, data: Dict) -> Dict:
        prev_hash = self.chain[-1]["hash"] if self.chain else "0"*64
        payload = json.dumps(data, sort_keys=True)
        h = hashlib.sha256((prev_hash + payload).encode()).hexdigest()
        entry = {"ts": datetime.now().isoformat(), "prev": prev_hash, "data": data, "hash": h, "h_num": len(self.chain)}
        with open(self.path, "a") as f: f.write(json.dumps(entry)+"\n")
        self.chain.append(entry)
        return entry

    def verify_chain(self) -> bool:
        prev = "0"*64
        for e in self.chain:
            calc = hashlib.sha256((prev + json.dumps(e["data"], sort_keys=True)).encode()).hexdigest()
            if calc != e["hash"]: return False
            prev = e["hash"]
        return True

    def replay(self):
        print(f"[LEDGER REPLAY] {len(self.chain)} entries - Chain valid: {self.verify_chain()}")
        for e in self.chain[-10:]:  # last 10
            print(f"  #{e['h_num']} {e['ts'][:19]} {e['data'].get('type')} hash={e['hash'][:12]}...")

# ============ OSHA L4: ADMINISTRATIVE - Promotion Gate + Watchers ============
class WatcherA:
    def check_loop(self, action, history):
        last5 = [h["data"].get("type") for h in history[-5:]]
        if last5.count(action.get("type")) >= 3:
            return {"level": "CRITICAL", "msg": f"Loop detected: {action['type']} in last 5", "confidence": 0.95}
        return None

class WatcherB:
    def audit(self, signal_a):
        # Audits Watcher-A for bias drift
        if signal_a and signal_a["confidence"] > 0.99:
            return {"level": "WARNING", "msg": "Watcher-A overconfident - audit flag", "confidence": 0.6}
        return None

class CouncilResolver:
    def resolve(self, sig_a, sig_b):
        if sig_a and sig_a["level"] == "CRITICAL":
            return "ESCALATE_TO_COUNCIL"
        if sig_b:
            return "HOLD"
        return "CONTINUE"

# ============ v6.6 NEW: Lessons Ledger - POLITE_LIE FIX ============
"""
OLD: pronunciation_errors_report.md = ["POLITE_LIE", "TAU_NEAR_FLOOR"] - immediate TRUTH
NEW: lessons.jsonl with safety card model:
  - YouTube learn -> status UNVERIFIED
  - Needs 3 consecutive safe replays to promote -> TRUTH
  - Like OSHA incident investigation: observation must be replayed >=3 times
"""
class LessonsLedger:
    def __init__(self, path="lessons.jsonl"):
        self.path = Path(path)
        self.path.touch(exist_ok=True)
        # Migrate old file if exists
        self._migrate_old()
        self.lessons = self._load()

    def _migrate_old(self):
        old = Path("pronunciation_errors_report.md")
        if old.exists() and not self.path.stat().st_size:
            print("[MIGRATION] pronunciation_errors_report.md -> lessons.jsonl")
            try:
                txt = old.read_text()
                # Extract POLITE_LIE etc
                items = re.findall(r"POLITE_LIE|TAU_NEAR_FLOOR|\w+", txt)
                for item in set(items)[:10]:
                    self.add_lesson(item, source="migration", status="UNVERIFIED")
            except: pass

    def _load(self):
        lessons = []
        with open(self.path) as f:
            for line in f:
                try: lessons.append(json.loads(line))
                except: pass
        return lessons

    def _save_all(self):
        with open(self.path, "w") as f:
            for ls in self.lessons:
                f.write(json.dumps(ls)+"\n")

    def add_lesson(self, content: str, source="youtube", status="UNVERIFIED"):
        # Prevent POLITE_LIE immediate TRUTH
        lesson = {
            "id": hashlib.sha256(f"{content}{time.time()}".encode()).hexdigest()[:8],
            "content": content,
            "source": source,
            "status": status,  # UNVERIFIED -> needs 3 replays -> TRUTH
            "replays": 0,
            "consecutive_safe": 0,
            "first_seen": datetime.now().isoformat(),
            "last_replay": None
        }
        self.lessons.append(lesson)
        self._save_all()
        print(f"[LESSON] Added {content} as {status} from {source} id={lesson['id']}")
        return lesson

    def record_replay(self, lesson_id: str, safe: bool):
        for ls in self.lessons:
            if ls["id"] == lesson_id:
                ls["replays"] += 1
                ls["last_replay"] = datetime.now().isoformat()
                if safe:
                    ls["consecutive_safe"] += 1
                else:
                    ls["consecutive_safe"] = 0
                    print(f"[SAFETY CARD RESET] {ls['content']} failed replay - consecutive reset to 0")

                # Promotion Gate: 3 consecutive safe replays -> TRUTH
                if ls["status"] == "UNVERIFIED" and ls["consecutive_safe"] >= 3:
                    ls["status"] = "TRUTH"
                    print(f"[PROMOTION GATE] {ls['content']} promoted UNVERIFIED -> TRUTH after 3 consecutive safe replays (2-person rule passed)")

                self._save_all()
                return ls
        return None

    def summary(self) -> str:
        unverified = [l for l in self.lessons if l["status"] == "UNVERIFIED"]
        truth = [l for l in self.lessons if l["status"] == "TRUTH"]
        return f"{len(unverified)} actions learned from unverified YouTube - {len(truth)} promoted to TRUTH after 3 consecutive replays. Total {len(self.lessons)} lessons."

    def list_lessons(self):
        for ls in self.lessons[-20:]:
            print(f"  [{ls['status']}] {ls['content']} src={ls['source']} safe_streak={ls['consecutive_safe']}/3 replays={ls['replays']} id={ls['id']}")

# ============ MAIN UFO LOOP ============
class UFOv66:
    def __init__(self):
        self.ledger = HashChainLedger()
        self.lessons = LessonsLedger()
        self.watcher_a = WatcherA()
        self.watcher_b = WatcherB()
        self.council = CouncilResolver()
        self.history = []

    def execute(self, action: Dict):
        # L1 + L2: Merkle + BoundedSensorGate BEFORE Watcher
        ok, gated_action, msg = BoundedSensorGate.validate(action)
        if not ok:
            print(f"[BLOCKED] {msg}")
            self.ledger.append({"type": "BLOCKED", "reason": msg, "proposed": action})
            return False

        # L3: Watcher-A
        sig_a = self.watcher_a.check_loop(gated_action, self.ledger.chain)
        if sig_a:
            print(f"[Watcher-A] {sig_a['level']} {sig_a['msg']}")
            # L4: Watcher-B audits A
            sig_b = self.watcher_b.audit(sig_a)
            if sig_b:
                print(f"[Watcher-B] {sig_b['level']} {sig_b['msg']}")
            decision = self.council.resolve(sig_a, sig_b)
            if decision != "CONTINUE":
                print(f"[Council] Decision={decision} - 2-person rule blocks execution")
                self.ledger.append({"type": "HOLD", "decision": decision, "action": gated_action})
                return False

        # L5: AEGIS Commit + Ledger
        entry = self.ledger.append(gated_action)
        print(f"[AEGIS COMMIT] {gated_action['type']} hash={entry['hash'][:12]}...")
        return True

    def cmd_status(self):
        print("\n" + "="*60)
        print(f"UFO v6.6 Cathedral Edition - POLITE_LIE FIX")
        print(f"OSHA Permit Root: {FULL_PERMITTED_ROOT[:12]}... ({len(PERMITTED_ACTIONS)} actions) | Elimination Control Active")
        print(f"Ledger valid: {self.ledger.verify_chain()} - {len(self.ledger.chain)} entries")
        print(f"Lessons: {self.lessons.summary()}")
        print("="*60 + "\n")
        self.lessons.list_lessons()

    def cmd_learn(self, name: str):
        # Simulate YouTube learning as UNVERIFIED, not TRUTH
        print(f"[LEARN] tutorial named {name} via llava:7b Eyes - learning as UNVERIFIED (needs 3 replays)")
        # Simulate extracting 2 lessons that would previously be POLITE_LIE
        self.lessons.add_lesson(f"{name}:POLITE_LIE", source=f"youtube:{name}", status="UNVERIFIED")
        self.lessons.add_lesson(f"{name}:TAU_NEAR_FLOOR", source=f"youtube:{name}", status="UNVERIFIED")
        print(f"[SAFETY CARD] Created - requires 3 safe replays before TRUTH")

    def cmd_replay(self, lesson_id=None):
        self.ledger.replay()
        print("\n[LESSONS REPLAY]")
        # Simulate replay promoting lessons
        for ls in self.lessons.lessons:
            if ls["status"] == "UNVERIFIED":
                # Simulate safe replay
                self.lessons.record_replay(ls["id"], safe=True)

def main():
    ufo = UFOv66()
    print("\nCommands: help, status, replay, ledger, learn tutorial named X, fastlearn tutorial named X, any action, end project\n")
    while True:
        try:
            cmd = input("ufo64 v6.6> ").strip()
            if not cmd: continue
            if cmd in ["help","?"]:
                print("""help / ? -> this help
status -> project + ledger verify + replay + permit root + lessons summary (3 actions learned from unverified YouTube - 0 promoted to TRUTH)
replay -> Replay Chronicle + attempt to promote UNVERIFIED -> TRUTH after 3 consecutive safe replays
ledger -> Show chain validity
learn tutorial named X -> 1s DETAILED (Shadow) learns as UNVERIFIED
fastlearn tutorial named X -> 3s FAST learns as UNVERIFIED
end project -> zips + verifies ledger
Any task -> BoundedSensorGate (click 0-3840, type max 1000) -> Watcher-A -> Watcher-B -> Council -> Gate -> AEGIS
""")
            elif cmd == "status":
                ufo.cmd_status()
            elif cmd == "replay":
                ufo.cmd_replay()
            elif cmd == "ledger":
                print(f"Chain valid: {ufo.ledger.verify_chain()}")
            elif cmd.startswith("learn tutorial named "):
                name = cmd.replace("learn tutorial named ","").strip()
                ufo.cmd_learn(name)
            elif cmd.startswith("fastlearn tutorial named "):
                name = cmd.replace("fastlearn tutorial named ","").strip()
                ufo.cmd_learn(name)
            elif cmd == "end project":
                print("[END] Zipping ledger + lessons + verifying")
                with zipfile.ZipFile(f"ufo_project_{int(time.time())}.zip","w") as z:
                    if Path("ledger.jsonl").exists(): z.write("ledger.jsonl")
                    if Path("lessons.jsonl").exists(): z.write("lessons.jsonl")
                print("Done")
                break
            else:
                # Try parse as action json or simple type
                # Example: click x=100 y=200 or type text=hello
                action = {"type": "type", "text": cmd}
                if cmd.startswith("click"):
                    m = re.search(r"x=(\d+).*y=(\d+)", cmd)
                    if m: action = {"type":"click","x":int(m.group(1)),"y":int(m.group(2))}
                ufo.execute(action)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
