"""RIV-gd-1 AC1 (round-8 analysis item 7, row Z-S29): classify the G5 history drift -- a READ, no replay. Measured by the D12 Step B
mirror dry run: rebuilding G5 with current code changes the other funds' served trades on most of 189 report dates (confidence
176 dates, action 99, est_price/est_notional 99, discretionary_shares 43, income_funded 10, row count 3; columns est_price_source
and key_resolution new on 183; revision references 186).

Interface (prescribed): `data/etfs/scripts/rivalfunds/tools/g5_drift.py` compares, per report date 2026-01-02..2026-10-02, the live
newest G5 object (s3, READ-ONLY) with a G5 built by the current code from the live newest G1 into a LOCAL sink, for every fund
except IDVZ and PFOE, and writes `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~6/g5_drift.json`:
{"dates": <int>, "rows_compared": <int>, "rows_differing": <int>, "classes": [{"name", "columns": [...], "n_dates", "n_rows",
"cause": {"commit", "cell"}, "reader_visible": true|false}], "unclassified_rows": <int>} plus a one-page G5_DRIFT.md beside it.
No S3 write, no G5 replay.
  - (a) the JSON exists and parses, dates == 189 and unclassified_rows == 0;
  - (b) every class names a cause commit that exists in this repository and a cell id, and the classes' n_rows cover
    rows_differing (sum >= rows_differing, a row may sit in two classes);
  - (c) control: the measured column set {confidence, action, est_price, discretionary_shares, income_funded} each appears in at
    least one class's columns.
FAIL at base: (a) FAILS (no report), so (b) and (c) FAIL with it."""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

MEASURED = {"confidence", "action", "est_price", "discretionary_shares", "income_funded"}


def run(v):
    p = c.ROOT / "org" / "missions" / "D5" / "ETFS" / "ETFS_RIVALS" / "deliverables" / "0.9.0_WK_ETFS_RIVALS~6" / "g5_drift.json"
    doc = None
    if p.exists():
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            doc = None
    print("report:", p, "exists" if p.exists() else "ABSENT")
    v.check(isinstance(doc, dict) and doc.get("dates") == 189 and doc.get("unclassified_rows") == 0,
            "(a) the drift report exists, covers 189 dates and leaves 0 rows unclassified")
    classes = (doc or {}).get("classes") or []

    def commit_ok(h):
        if not h:
            return False
        r = subprocess.run(["git", "-C", str(c.ROOT), "cat-file", "-e", f"{h}^{{commit}}"], capture_output=True)
        return r.returncode == 0

    named = [k for k in classes if commit_ok((k.get("cause") or {}).get("commit")) and (k.get("cause") or {}).get("cell")]
    total = sum(int(k.get("n_rows") or 0) for k in classes)
    print("classes:", len(classes), "| with a real cause commit + cell:", len(named), "| n_rows sum", total,
          "| rows_differing", (doc or {}).get("rows_differing"))
    v.check(bool(classes) and len(named) == len(classes) and total >= int((doc or {}).get("rows_differing") or 1),
            "(b) every class names a real cause commit and a cell, and the classes cover every differing row")
    cols = {col for k in classes for col in (k.get("columns") or [])}
    v.check(MEASURED <= cols, "(c) control: each measured drifting column sits in a class")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
