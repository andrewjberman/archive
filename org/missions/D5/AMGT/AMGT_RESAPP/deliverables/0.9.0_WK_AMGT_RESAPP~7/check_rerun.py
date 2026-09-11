"""
check_rerun.py -- AC2's own invocation. Reads the before/after ledger snapshots
run_exercise.py wrote beside this script and prints ONE line: which class(es)
moved, how many stayed byte-for-byte unchanged, and the exercised class's
outcome -- read from the artifact, never from the exercise script's own log.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_ledger():
    mod_path = (
        Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent.parent
        / "lib"
        / "research"
        / "ledger"
        / "ledger.py"
    )
    spec = importlib.util.spec_from_file_location("ledger", mod_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load ledger from {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _entries_by_class(doc: dict, classes) -> dict[str, list]:
    out: dict[str, list] = {cls: [] for cls in classes}
    for entry in doc.get("entries", []):
        out.setdefault(entry["input_class"], []).append(entry)
    return out


def main() -> int:
    here = Path(__file__).resolve().parent
    before = json.loads((here / "ledger_before.json").read_text(encoding="utf-8"))
    after = json.loads((here / "ledger_after.json").read_text(encoding="utf-8"))
    security_key = after.get("security_key") or before.get("security_key")

    ledger = _load_ledger()
    classes = list(ledger.CLASSES)

    before_by_class = _entries_by_class(before, classes)
    after_by_class = _entries_by_class(after, classes)

    moved = [cls for cls in classes if before_by_class[cls] != after_by_class[cls]]
    unchanged = [cls for cls in classes if before_by_class[cls] == after_by_class[cls]]

    latest_market_data = None
    for entry in after_by_class.get("market_data", []):
        if latest_market_data is None or entry["stamp"] > latest_market_data["stamp"]:
            latest_market_data = entry
    outcome = latest_market_data["outcome"] if latest_market_data else "UNKNOWN"

    moved_str = ", ".join(moved) if moved else "none"
    print(
        f"RERUN market_data on {security_key}: classes moved {len(moved)} ({moved_str}), "
        f"classes unchanged {len(unchanged)}, outcome {outcome}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
