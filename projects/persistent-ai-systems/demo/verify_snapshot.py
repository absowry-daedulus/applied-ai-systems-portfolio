from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
manifest = json.loads((base / "manifest.example.json").read_text())
state = json.loads((base / "state.example.json").read_text())
errors = []

for name, expected in manifest["files"].items():
    actual = hashlib.sha256((base / name).read_bytes()).hexdigest()
    if actual != expected:
        errors.append(f"hash mismatch: {name}")

events = [json.loads(line) for line in (base / "event_log.example.jsonl").read_text().splitlines() if line.strip()]
ids = [event["event_id"] for event in events]

if len(ids) != len(set(ids)):
    errors.append("duplicate event ids")
if state["last_event_id"] != ids[-1]:
    errors.append("state does not match event-ledger tail")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
else:
    print("PASS: snapshot hashes and continuity pointers agree")
