"""RIV-rp-2 AC1 (round-9 analysis ruling 4 as re-ruled by CTO~Z msg 29806, option A): replay ONLY the 4 code-defect classes that do
not depend on G3 arrival, G3-pinned, with a census in which nothing else moves. Measured by RIV-gd-1
(deliverables/0.9.0_WK_ETFS_RIVALS~6/g5_drift.json, merged 9de2a6a666): key_resolution_out_of_confidence 1,040 rows (RIV-h-6),
full_exit_priced 266 (RIV-x-1), own_prior_pairing 7 (RIV-t-5), implausible_window_refused 10 (RIV-h-5) -- 1,323 rows; the two RIV-e-2
classes (20 rows) and the data-arrival class (9,467 rows) keep their vintage (ruling 3).

Interface (prescribed): `data/etfs/scripts/rivalfunds/tools/g5_code_replay.py` with `plan` (the (report date, fund) set the 4 classes
touch, from the drift tool's comparison) and `dry` (each planned date's G5 rebuilt into a LOCAL sink at current code with the G3
objects pinned to the live object's recorded revisions and `rebuild_funds` = that date's planned funds, then a census against the
live newest object). It writes `deliverables/0.9.0_WK_ETFS_RIVALS~3/g5_replay_dry.json`: {"classes": [...], "dates": <int>,
"rows_moved": <int>, "rows_moved_by_class": {...}, "rows_moved_outside_classes": <int>, "columns_moved_outside_classes": [...],
"g3_label_columns_moved": <int>}. No S3 write: the served replay is the issuer's act under its own pair.
  - (a) the report exists; its classes are exactly the 4 named; rows_moved_by_class equals gd-1's n_rows per class;
  - (b) rows_moved_outside_classes == 0 and g3_label_columns_moved == 0;
  - (c) control: neither RIV-e-2 class nor g3_latest_pull_supersession appears in the report's classes.
FAIL at base: (a) FAILS (no report), so (b) FAILS with it; (c) PASSES vacuously only with a report -- it FAILS at base too."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

FOUR = {"key_resolution_out_of_confidence": 1040, "full_exit_priced": 266, "own_prior_pairing": 7, "implausible_window_refused": 10}
KEEP = {"g3_currency_in_income_conversion", "g3_minor_unit_dividend_currency", "g3_latest_pull_supersession"}


def run(v):
    p = c.ROOT / "org" / "missions" / "D5" / "ETFS" / "ETFS_RIVALS" / "deliverables" / "0.9.0_WK_ETFS_RIVALS~3" / "g5_replay_dry.json"
    doc = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    print("report:", p, "exists" if doc else "ABSENT")
    classes = set((doc or {}).get("classes") or [])
    by = (doc or {}).get("rows_moved_by_class") or {}
    print("classes", sorted(classes), "| by class", by, "| outside", (doc or {}).get("rows_moved_outside_classes"),
          "| g3 label moves", (doc or {}).get("g3_label_columns_moved"))
    v.check(bool(doc) and classes == set(FOUR) and all(int(by.get(k, -1)) == n for k, n in FOUR.items()),
            "(a) the replay report names exactly the 4 code classes, each moving gd-1's row count")
    v.check(bool(doc) and doc.get("rows_moved_outside_classes") == 0 and doc.get("g3_label_columns_moved") == 0,
            "(b) nothing outside the 4 classes moves, and no G3 label column moves")
    v.check(bool(doc) and not (classes & KEEP), "(c) control: the RIV-e-2 and data-arrival classes are not replayed")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
