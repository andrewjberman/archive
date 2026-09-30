"""RIV-m-1 AC1 -- the home-producer verdict is recorded for IDVZ and PFOE, every field present, and each verdict follows
from its own numbers by the cell's rule (meets_grain iff daily coverage >= 95% of trading days AND share counts on 100% of
rows AND first_date <= history_reference_date; READ iff meets_grain). IDVZ's reference is the census's first Bloomberg
report date (2024-12-27); PFOE's, where no census measured it, is last_date minus two years."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REC = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/m1_home_producer.json"
FIELDS = ["daily_days", "days_in_window", "share_count_rows", "total_rows", "first_date", "last_date",
          "history_reference_date", "history_reference_source", "meets_grain", "verdict", "evidence_keys"]
REF = {"IDVZ": "2024-12-27"}


def run(v):
    root = c.setup_path()
    rec = json.loads((root / REC).read_text(encoding="utf-8"))
    from lib.trading_calendar import trading_days_between

    v.check(isinstance(rec.get("runs_listed"), int) and rec["runs_listed"] > 0,
            f"runs_listed is a positive count over every page (got {rec.get('runs_listed')})")
    for fund in ("IDVZ", "PFOE"):
        f = rec.get("funds", {}).get(fund)
        v.check(isinstance(f, dict), f"{fund} measured")
        if not isinstance(f, dict):
            continue
        missing = [k for k in FIELDS if k not in f]
        v.check(not missing, f"{fund} carries every field (missing {missing})")
        if missing:
            continue
        span = len(trading_days_between(f["first_date"], f["last_date"])) if f["first_date"] else 0
        v.check(f["days_in_window"] == span, f"{fund} days_in_window {f['days_in_window']} == trading days "
                                             f"{f['first_date']}..{f['last_date']} ({span})")
        rule = (f["days_in_window"] > 0 and f["daily_days"] / f["days_in_window"] >= 0.95
                and f["total_rows"] > 0 and f["share_count_rows"] == f["total_rows"]
                and bool(f["first_date"]) and f["first_date"] <= f["history_reference_date"])
        if fund in REF:
            v.check(f["history_reference_date"] == REF[fund], f"{fund} history_reference_date {f['history_reference_date']} == census {REF[fund]}")
        else:
            import datetime
            two = (datetime.date.fromisoformat(f["last_date"]) - datetime.timedelta(days=730)).isoformat() if f["last_date"] else None
            v.check(two is not None and abs((datetime.date.fromisoformat(f["history_reference_date"]) - datetime.date.fromisoformat(two)).days) <= 3,
                    f"{fund} history_reference_date {f['history_reference_date']} == last_date - 2y ({two})")
        v.check(f["meets_grain"] == rule, f"{fund} meets_grain {f['meets_grain']} follows from its numbers ({rule})")
        want = "READ" if f["meets_grain"] else "JOIN_BLOOMBERG"
        v.check(f["verdict"] == want, f"{fund} verdict {f['verdict']} == {want}")
        v.check(bool(f["evidence_keys"]), f"{fund} names its evidence keys ({len(f['evidence_keys'])})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
