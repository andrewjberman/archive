"""Self-test of r2_checks.py: one GOOD fixture per grader (must pass) and mutants (must fail). ASCII only.
Prints `R2 SELFTEST: OK <n> arms` on success.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "r2_checks.py")
CALLS = ["aws s3api get-object --bucket opal-data-bd --key silver/transactions/2026-10-09.parquet"]

GOOD = {
    "ruleprobe": {"claim": "measured", "calls": CALLS, "deterministic": True,
                  "variants": {"A_trades_only": {}, "B_plus_reinvestment": {}},
                  "excluded_by_type": {"Dividend": 816, "Cash Deposit": 346},
                  "assets": [{"asset_name": "A", "date": "2026-10-09", "price": 1.5, "distinct_trade_ids": ["t1"]}]},
    "replay": {"claim": "measured", "calls": CALLS, "window": "2026-09-16..2026-10-13", "served_rows": 10,
               "classes": {"UNCHANGED": 6, "CHANGED": 2, "NOW_CARRY_FORWARD": 1, "NOT_RECOMPUTABLE": 1},
               "served_write": False, "deterministic": True, "list_file": "BEFORE_AFTER.csv",
               "variants": {"A_trades_only": {}, "B_plus_reinvestment": {}}, "no_trade_policy": "carry with date"},
    "census": {"claim": "measured", "calls": CALLS, "objects_total": 10, "objects_read": 10, "lots_total": 20,
               "classes": {"PRICED_FROM_CANONICAL": 15, "PRICED_OFF_NO_CANONICAL": 2, "NOT_UNTICKERED": 3},
               "listed_untickered": {"count": 1, "assets": ["X"]}, "extract_file": "E.csv", "extract_sha256": "a" * 64,
               "by_entity_class": {"normal": 9, "catch_all": 1}},
    "trace2": {"asset_name": "A", "date": "2026-10-09", "served_price": 1.5, "followed_source": "canonical",
               "followed_price": 1.5, "follows_served": True, "trade_ids": ["t1"], "match": True,
               "daily_row": {"price": 1.4}, "canonical_row": {"price": 1.5}},
    "cause": {"claim": "measured", "calls": CALLS, "rerun": False,
              "dates": [{"date": "2026-09-21", "class": "NO_RUN", "evidence": "x"}],
              "behind_objects": {"producer": "script:x", "derivation": "data_as_of = max(trade date)"}},
    "lotproof": {"claim": "measured", "legacy_bytes_equal": True, "lot_rows": 5, "keyed_on_lot": True,
                 "lot_key": ["account_id", "asset_id", "open_date", "unit_cost"], "address": "s3://b/k",
                 "address_from_builder": True, "new_columns_in_legacy": []},
    "packet": {"claim": "measured", "price_changes": 3, "assets_changed": 2, "dollar_effect_latest_snapshot": 12.5,
               "snapshot_date": "2026-10-09", "before_after_file": "B.csv", "served_write": False,
               "readers": [{"reader": "a", "class": "internal"}, {"reader": "b", "class": "client-facing"},
                           {"reader": "c", "class": "unknown"}, {"reader": "d", "class": "internal"}]},
    "thread2": {"claim": "measured", "served_object_key": "k", "as_of_date": "2026-10-09", "account_ref": "0123456789ab",
                "asset_name": "A", "ticker": None, "served_price": 1.5, "rule_id": "R1", "trade_ids": ["t1", "t2"],
                "distinct_trade_ids": 2, "recomputed_price": 1.5, "recompute_equals_served": True,
                "unlisted_sources_checked": ["a", "b", "c"], "tie_order_applied": "none needed",
                "client_entity_class": "normal", "one_served_price": True},
}


def mutant(kind, why, edit):
    rec = copy.deepcopy(GOOD[kind])
    edit(rec)
    return (kind, why, rec)


MUTANTS = [
    mutant("ruleprobe", "not deterministic", lambda r: r.update(deterministic=False)),
    mutant("ruleprobe", "one variant only", lambda r: r.update(variants={"A_trades_only": {}})),
    mutant("replay", "served write", lambda r: r.update(served_write=True)),
    mutant("replay", "sum mismatch", lambda r: r["classes"].update(UNCHANGED=7)),
    mutant("replay", "write verb", lambda r: r["calls"].append("aws s3api put-object --bucket b --key k")),
    mutant("census", "objects_read over total", lambda r: r.update(objects_read=11)),
    mutant("census", "sum mismatch", lambda r: r["classes"].update(NOT_UNTICKERED=4)),
    mutant("census", "bad sha", lambda r: r.update(extract_sha256="zz")),
    mutant("trace2", "follows daily not served", lambda r: r.update(follows_served=False)),
    mutant("trace2", "bad source", lambda r: r.update(followed_source="other")),
    mutant("cause", "rerun", lambda r: r.update(rerun=True)),
    mutant("cause", "class off set", lambda r: r["dates"][0].update({"class": "MAYBE"})),
    mutant("cause", "no evidence", lambda r: r["dates"][0].update({"evidence": ""})),
    mutant("lotproof", "legacy changed", lambda r: r.update(legacy_bytes_equal=False)),
    mutant("lotproof", "key not lot", lambda r: r.update(lot_key=["account_id", "asset_name"])),
    mutant("lotproof", "address typed", lambda r: r.update(address_from_builder=False)),
    mutant("lotproof", "columns leaked", lambda r: r.update(new_columns_in_legacy=["units"])),
    mutant("packet", "served write", lambda r: r.update(served_write=True)),
    mutant("packet", "three readers", lambda r: r.update(readers=r["readers"][:3])),
    mutant("thread2", "raw account id", lambda r: r.update(account_id="1")),
    mutant("thread2", "tickered", lambda r: r.update(ticker="XOM")),
    mutant("thread2", "wrong rule", lambda r: r.update(rule_id="T1")),
    mutant("thread2", "distinct disagrees", lambda r: r.update(distinct_trade_ids=5)),
    mutant("thread2", "two sources", lambda r: r.update(unlisted_sources_checked=["a", "b"])),
    mutant("thread2", "catch-all entity", lambda r: r.update(client_entity_class="catch_all")),
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
            print("R2 SELFTEST: FAIL good arm %s -> %s" % (kind, line))
            return 1
        arms += 1
    for kind, why, rec in MUTANTS:
        rc, line = run(kind, rec)
        if rc == 0 or "record FAIL" not in line:
            print("R2 SELFTEST: FAIL mutant arm %s/%s was admitted -> %s" % (kind, why, line))
            return 1
        arms += 1
    print("R2 SELFTEST: OK %d arms" % arms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
