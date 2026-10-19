"""Control for pn6_cells.py (cell IB-pn-6): builds a temp root, a synthetic good record (all three PASS), then one negative per rule
(each fails only its own arm). Usage: python control_pn6.py <repo_root>."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pn6_cells as P  # noqa: E402

GOOD = {
    "reads": {"read_at_utc": "2026-10-19T15:00:00Z", "first_run_day": "2026-10-16", "earliest_start_date": "2019-01-02",
              "day_count_n": 2844, "n_within_limit": True, "household_count": 294, "accounts_in_universe": 863,
              "accounts_with_null_start_date": 68,
              "bronze_object": {"keys": 1, "versions": 1, "bytes": 123456}, "silver_object": {"keys": 1, "versions": 1, "bytes": 98765}},
    "aws_writes_made": 0, "orion_requests": 0,
}
NEGATIVES = [
    ("N not the days between", ("reads", "day_count_n"), 2799, "IBN6-AC1"),
    ("earliest after the first run", ("reads", "earliest_start_date"), "2026-10-17", "IBN6-AC1"),
    ("limit flag wrong", ("reads", "n_within_limit"), False, "IBN6-AC1"),
    ("households over the bound", ("reads", "household_count"), 295, "IBN6-AC1"),
    ("null count over accounts", ("reads", "accounts_with_null_start_date"), 900, "IBN6-AC1"),
    ("bronze bytes zero", ("reads", "bronze_object", "bytes"), 0, "IBN6-AC2"),
    ("silver two versions", ("reads", "silver_object", "versions"), 2, "IBN6-AC2"),
    ("a write made", ("aws_writes_made",), 1, "IBN6-AC3"),
    ("an Orion request made", ("orion_requests",), 1, "IBN6-AC3"),
]


def run(root, cid):
    out = subprocess.run([sys.executable, str(HERE / "pn6_cells.py"), str(root), cid], capture_output=True, text=True, timeout=60)
    return out.returncode, (out.stdout.strip().splitlines() or ["-"])[-1]


def main():
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rec = root / P.RECORD
        rec.parent.mkdir(parents=True, exist_ok=True)
        base = {c: run(root, c)[0] for c in P.CHECKS}
        print("NO RECORD (the base):", base, "(all must be 1)")
        bad += sum(1 for v in base.values() if v != 1)
        rec.write_text(json.dumps(GOOD), encoding="utf-8")
        pos = {c: run(root, c) for c in P.CHECKS}
        print("POSITIVE:", {c: v[1] for c, v in pos.items()})
        bad += sum(1 for v in pos.values() if v[0] != 0)
        for label, path, value, own in NEGATIVES:
            doc = copy.deepcopy(GOOD)
            node = doc
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            rec.write_text(json.dumps(doc), encoding="utf-8")
            res = {c: run(root, c)[0] for c in P.CHECKS}
            ok = res[own] == 1 and all(v == 0 for c, v in res.items() if c != own)
            print("%-28s fails %s only: %s" % (label, own, "OK" if ok else "UNEXPECTED %s" % res))
            bad += not ok
        doc = copy.deepcopy(GOOD)
        doc["reads"]["household_id"] = 5001
        rec.write_text(json.dumps(doc), encoding="utf-8")
        res = {c: run(root, c)[0] for c in P.CHECKS}
        ok = res["IBN6-AC3"] == 1 and res["IBN6-AC1"] == 0 and res["IBN6-AC2"] == 0
        print("%-28s fails IBN6-AC3 only: %s" % ("an identifier member added", "OK" if ok else "UNEXPECTED %s" % res))
        bad += not ok
    print("unexpected:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
