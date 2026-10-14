"""Self-test of r3_checks.py: one GOOD fixture per grader (must pass) and mutants (must fail). ASCII only.
Prints `R3 SELFTEST: OK <n> arms` on success.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "r3_checks.py")
CALLS = ["aws s3api get-object --bucket opal-data-bd --key silver/transactions/2026-10-09.parquet"]
SHA = "a" * 64

GOOD = {
    "ruleprobe2": {"claim": "measured", "calls": CALLS, "amendment": "R1.2", "deterministic": True, "reinvestment_in": True,
                   "transfer_in_out": True, "types_seen": {"Buy": 1},
                   "par_quoted": {"class_field": "asset_class", "assets_scaled": 3, "withheld_disagreement": 1,
                                  "unit_scale_rows_unchanged": 3, "per_unit_left": 2, "withheld_ratios": [0.5]},
                   "assets": [{"asset_name": "A", "date": "2026-10-09", "price": 1.5, "kind": "trade", "distinct_trade_ids": ["t"]}]},
    "replay2": {"claim": "measured", "calls": CALLS, "amendment": "R1.2", "window": "w", "served_rows": 10, "served_write": False,
                "deterministic": True, "list_file": "L.csv", "list_sha256": SHA, "par_quoted_rows": 2, "par_rows_unchanged": 2,
                "transfer_in_carry_forwards": 3, "carry_forwards_with_date": 4,
                "classes": {"UNCHANGED": 5, "CHANGED": 1, "NOW_CARRY_FORWARD": 4, "NOT_RECOMPUTABLE": 0},
                "interpolated": {"rows": 10, "with_trade_price": 4, "with_last_traded_date": 5, "unresolved": 1},
                "lookback_keying": {"mode": "limited", "statement": "reads t and t+1"}},
    "packet2": {"claim": "measured", "calls": CALLS, "amendment": "R1.2", "snapshot_date": "2026-10-09", "price_changes": 3,
                "assets_changed": 2, "lots_touched": 9, "dollar_effect_latest_snapshot": 12.5, "movers_file": "M.csv",
                "before_after_file": "B.csv", "served_write": False, "par_rows_in_movers": 0, "plain_page": "PACKET2.md",
                "interpolated_fate": {"rows": 10, "trade_price": 4, "last_traded_date": 5, "unresolved": 1},
                "readers": [{"reader": "a", "class": "internal"}, {"reader": "b", "class": "client-facing"},
                            {"reader": "c", "class": "unknown"}, {"reader": "d", "class": "internal"}]},
    "cap": {"claim": "measured", "calls": CALLS, "days_checked": 10, "days_at_500000": 2,
            "rows_per_day": {"d%d" % i: (500000 if i < 2 else 100000 + i) for i in range(10)},
            "paging_config": "limit=500000 at runner.py:10", "verdict": "CAP", "evidence": "x",
            "second_window": {"dates": ["d1"], "rows": [1]}},
    "lotproof2": {"claim": "measured", "legacy_bytes_equal": True, "lot_rows": 5, "rows_folded": 0,
                  "colliding_groups_differing": 0, "keyed_on_lot": True, "key_basis": "relationship_id",
                  "lot_key": ["relationship_id", "account_id", "asset_id", "open_date", "unit_cost"], "address": "s3://b/k",
                  "address_from_builder": True, "new_columns_in_legacy": []},
    "sentinel": {"claim": "measured", "calls": CALLS, "rerun": False, "deployed_fix": {"deployed": True, "evidence": "e"},
                 "runs_checked": 14, "honest_lines": 14, "dishonest_lines": 0, "window_rule": "runner.py:99 asOfDate",
                 "cause": "EXPORT_WINDOW_RULE",
                 "monday_tuesday": [{"date": "2026-10-12", "weekday": "Mon", "first_export_bytes": 4357, "sentinel_exists": False,
                                     "evidence": "e"}]},
    "offcanon": {"claim": "measured", "calls": CALLS, "lots_total": 10, "extract_sha256": SHA,
                 "classes": {"EQUALS_OLDER_CANONICAL_VERSION": 3, "EQUALS_DAILY_FILE_ROW": 2, "EQUALS_NAMED_OTHER_SOURCE": 1,
                             "UNEXPLAINED": 4},
                 "named_sources": ["gold B_01 injection"],
                 "exemplars": {"EQUALS_OLDER_CANONICAL_VERSION": "x", "EQUALS_DAILY_FILE_ROW": "y",
                               "EQUALS_NAMED_OTHER_SOURCE": "z", "UNEXPLAINED": "w"}},
}


def _r13(kind, **extra):
    rec = copy.deepcopy(GOOD[kind])
    rec["amendment"] = "R1.3"
    rec["served_units"] = {"assets": 10, "per100": 3, "per_unit": 6, "unreadable": 1}
    rec.update(extra)
    return rec


GOOD["ruleprobe3"] = _r13("ruleprobe2", unit_changed_assets=0)
GOOD["replay3"] = _r13("replay2", unit_changed_rows=0, unit_map_file="U.csv", unit_withheld_rows=1)
GOOD["packet3"] = _r13("packet2", held_unit_rows=0)

GOOD["lotproof3"] = {"claim": "measured", "legacy_bytes_equal": True, "lot_rows": 5, "keyed_on_lot": True, "key_basis": "relationship_id",
                     "lot_key": ["relationship_id", "account_id", "asset_id", "open_date", "unit_cost", "units"], "units_in_key": True,
                     "folded_without_units": 192, "recount_without_units": 192, "zero_fold": "deferred_to_first_real_export",
                     "address": "s3://b/k", "address_from_builder": True, "new_columns_in_legacy": []}


def mutant(kind, why, edit):
    rec = copy.deepcopy(GOOD[kind])
    edit(rec)
    return (kind, why, rec)


MUTANTS = [
    mutant("lotproof3", "units not in key", lambda r: r.update(units_in_key=False)),
    mutant("lotproof3", "key lacks units", lambda r: r.update(lot_key=["relationship_id", "account_id", "asset_id", "open_date", "unit_cost"])),
    mutant("lotproof3", "fold differs from the recount", lambda r: r.update(recount_without_units=191)),
    mutant("lotproof3", "zero claimed", lambda r: r.update(zero_fold="zero")),
    mutant("lotproof3", "legacy changed", lambda r: r.update(legacy_bytes_equal=False)),
    mutant("lotproof3", "units leaked into legacy", lambda r: r.update(new_columns_in_legacy=["units"])),
    mutant("ruleprobe3", "amendment R1.2 offered", lambda r: r.update(amendment="R1.2")),
    mutant("ruleprobe3", "a unit changed", lambda r: r.update(unit_changed_assets=1)),
    mutant("ruleprobe3", "unit classes do not sum", lambda r: r["served_units"].update(per100=4)),
    mutant("ruleprobe3", "no unit map", lambda r: r.pop("served_units")),
    mutant("replay3", "a row changed unit", lambda r: r.update(unit_changed_rows=2)),
    mutant("replay3", "no unit map file", lambda r: r.pop("unit_map_file")),
    mutant("packet3", "a row still held", lambda r: r.update(held_unit_rows=1)),
    mutant("packet3", "amendment R1.2 offered", lambda r: r.update(amendment="R1.2")),
    mutant("ruleprobe2", "wrong amendment", lambda r: r.update(amendment="R1")),
    mutant("ruleprobe2", "transfer in kept", lambda r: r.update(transfer_in_out=False)),
    mutant("ruleprobe2", "reinvestment out", lambda r: r.update(reinvestment_in=False)),
    mutant("ruleprobe2", "no par block", lambda r: r.pop("par_quoted")),
    mutant("ruleprobe2", "no per-unit count", lambda r: r["par_quoted"].pop("per_unit_left")),
    mutant("ruleprobe2", "no withheld ratios", lambda r: r["par_quoted"].pop("withheld_ratios")),
    mutant("replay2", "served write", lambda r: r.update(served_write=True)),
    mutant("replay2", "par not unchanged", lambda r: r.update(par_rows_unchanged=1)),
    mutant("replay2", "sum mismatch", lambda r: r["classes"].update(UNCHANGED=6)),
    mutant("replay2", "carry without date", lambda r: r.update(carry_forwards_with_date=3)),
    mutant("replay2", "interpolated sum", lambda r: r["interpolated"].update(unresolved=2)),
    mutant("replay2", "lookback mode off set", lambda r: r["lookback_keying"].update(mode="whatever")),
    mutant("packet2", "par rows in movers", lambda r: r.update(par_rows_in_movers=2)),
    mutant("packet2", "three readers", lambda r: r.update(readers=r["readers"][:3])),
    mutant("packet2", "interpolated sum", lambda r: r["interpolated_fate"].update(unresolved=3)),
    mutant("packet2", "served write", lambda r: r.update(served_write=True)),
    mutant("cap", "count mismatch", lambda r: r.update(days_at_500000=5)),
    mutant("cap", "verdict off set", lambda r: r.update(verdict="MAYBE")),
    mutant("cap", "nine days", lambda r: r.update(days_checked=9, rows_per_day={"d%d" % i: 1 for i in range(9)}, days_at_500000=0)),
    mutant("lotproof2", "rows folded", lambda r: r.update(rows_folded=3)),
    mutant("lotproof2", "still differing", lambda r: r.update(colliding_groups_differing=1)),
    mutant("lotproof2", "key lacks relationship", lambda r: r.update(lot_key=["account_id", "asset_id", "open_date", "unit_cost"])),
    mutant("lotproof2", "legacy changed", lambda r: r.update(legacy_bytes_equal=False)),
    mutant("sentinel", "rerun", lambda r: r.update(rerun=True)),
    mutant("sentinel", "thirteen runs", lambda r: r.update(runs_checked=13)),
    mutant("sentinel", "cause off set", lambda r: r.update(cause="BAD LUCK")),
    mutant("sentinel", "write verb", lambda r: r["calls"].append("aws lambda invoke --function-name f")),
    mutant("offcanon", "sum mismatch", lambda r: r["classes"].update(UNEXPLAINED=5)),
    mutant("offcanon", "class without exemplar", lambda r: r["exemplars"].pop("UNEXPLAINED")),
    mutant("offcanon", "bad sha", lambda r: r.update(extract_sha256="zz")),
]


def run(kind, rec):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(rec, fh)
        r = subprocess.run([sys.executable, CHK, kind, "--file", p], capture_output=True, text=True)
        return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""


def main():
    arms = 0
    for kind, rec in GOOD.items():
        rc, line = run(kind, rec)
        if rc != 0 or "record ok" not in line:
            print("R3 SELFTEST: FAIL good arm %s -> %s" % (kind, line))
            return 1
        arms += 1
    for kind, why, rec in MUTANTS:
        rc, line = run(kind, rec)
        if rc == 0 or "record FAIL" not in line:
            print("R3 SELFTEST: FAIL mutant arm %s/%s was admitted -> %s" % (kind, why, line))
            return 1
        arms += 1
    print("R3 SELFTEST: OK %d arms" % arms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
