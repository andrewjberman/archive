"""Control for pn7_cells.py (cell IB-pn-7): builds a temp root from the real addendum, both halves, the writer order and the script, a synthetic
good record (all three PASS), then one negative per rule (each fails only its own arm). Usage: python control_pn7.py <repo_root>."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pn7_cells as P  # noqa: E402

GOOD = {
    "gates": {"addendum_blob": P.ADDENDUM_BLOB, "both_halves_signed": True, "other_act_open_on_chain": False,
              "dispatch_object": {"feed_row_present": True, "live_sha256": "a" * 64},
              "runner_role": {"secret_read_allowed": True, "feed_prefix_write_allowed": True},
              "household_count": 294, "request_bound": 294,
              "sidecar": {"live_sha256": "e" * 64, "equals_generated_address": True}, "calendar_object_present": True,
              "notification_filter_matches_feed_keys": False},
    "ledger_entry": "org/critical_paths/change_management/x.json",
    "apply": {"applied_at_utc": "2026-10-19T15:00:00Z",
              "replaced_script": {"sha256": P.REPLACED_EXPECT, "saved_copy_sha256": P.REPLACED_EXPECT},
              "script": {"uploaded_sha256": P.SCRIPT_SHA},
              "import_smoke": {"ran_on_runner": False, "fallback_host": True, "python_version": "3.9.25",
                               "part_i_import_and_prefixes": True, "part_ii_session_token_client_under_scrubbed_env": True,
                               "part_iii_plan_only_run": True, "built_from_live_prefixes": True, "exit_code": 0, "orion_requests": 0},
              "run_object_address": {"source": "sidecar", "partition_equals_builder": True, "object_name_equals_builder": True,
                                     "bucket_and_prefix_equal_builder": True},
              "dispatch_unchanged": {"sha256_before": "a" * 64, "sha256_after": "a" * 64},
              "rollback_performed": False},
    "first_run": {"read_from_step_log": True, "exit_code": 0, "tolerated_failure": False, "days_complete": 3, "skipped_days": 0,
                  "requests_made": 294, "calc_gross_of_fees_false_on_every_request": True, "keys_outside_inflection_scope": 0,
                  "coverage": {"denominator": 863, "returned": 795, "absent": 68}, "zero_returns": 0, "stored_value": "daily_factor",
                  "run_object": {"keys": 1, "versions": 1, "bytes": 100000, "sha256": "b" * 64, "partition_is_run_pull_date": True},
                  "envelopes": {"count": 3, "schema_v2": True, "responses_member_absent": True, "raw_object_names_the_run_object": True,
                                "raw_object_sha256_equals_stored": True},
                  "silver": {"count": 3, "columns_equal_first_run": True}, "new_keys_total": 7},
}
NEGATIVES = [
    ("halves flag", ("gates", "both_halves_signed"), False, "IBN7-AC1"),
    ("another act open", ("gates", "other_act_open_on_chain"), True, "IBN7-AC1"),
    ("feed row missing", ("gates", "dispatch_object", "feed_row_present"), False, "IBN7-AC1"),
    ("bound not household count", ("gates", "request_bound"), 293, "IBN7-AC1"),
    ("sidecar differs", ("gates", "sidecar", "equals_generated_address"), False, "IBN7-AC1"),
    ("calendar absent", ("gates", "calendar_object_present"), False, "IBN7-AC1"),
    ("filter matches a feed key", ("gates", "notification_filter_matches_feed_keys"), True, "IBN7-AC1"),
    ("applied inside the band", ("apply", "applied_at_utc"), "2026-10-19T12:00:00Z", "IBN7-AC1"),
    ("applied on the transaction day", ("apply", "applied_at_utc"), "2026-10-20T16:00:00Z", "IBN7-AC1"),
    ("wrong upload hash", ("apply", "script", "uploaded_sha256"), "d" * 64, "IBN7-AC2"),
    ("replaced object unexpected", ("apply", "replaced_script", "sha256"), "f" * 64, "IBN7-AC2"),
    ("smoke part ii missing", ("apply", "import_smoke", "part_ii_session_token_client_under_scrubbed_env"), False, "IBN7-AC2"),
    ("smoke part iii missing", ("apply", "import_smoke", "part_iii_plan_only_run"), False, "IBN7-AC2"),
    ("smoke made an Orion request", ("apply", "import_smoke", "orion_requests"), 1, "IBN7-AC2"),
    ("run address partition differs", ("apply", "run_object_address", "partition_equals_builder"), False, "IBN7-AC2"),
    ("run address source unnamed", ("apply", "run_object_address", "source"), "typed", "IBN7-AC2"),
    ("dispatch changed", ("apply", "dispatch_unchanged", "sha256_after"), "c" * 64, "IBN7-AC2"),
    ("rollback performed", ("apply", "rollback_performed"), True, "IBN7-AC2"),
    ("tolerated failure", ("first_run", "tolerated_failure"), True, "IBN7-AC3"),
    ("read from the chain exit", ("first_run", "read_from_step_log"), False, "IBN7-AC3"),
    ("skipped day", ("first_run", "skipped_days"), 1, "IBN7-AC3"),
    ("coverage does not sum", ("first_run", "coverage", "absent"), 1, "IBN7-AC3"),
    ("a zero written", ("first_run", "zero_returns"), 1, "IBN7-AC3"),
    ("two run objects", ("first_run", "run_object", "keys"), 2, "IBN7-AC3"),
    ("envelope still has responses", ("first_run", "envelopes", "responses_member_absent"), False, "IBN7-AC3"),
    ("envelope names another object", ("first_run", "envelopes", "raw_object_sha256_equals_stored"), False, "IBN7-AC3"),
    ("envelope schema not v2", ("first_run", "envelopes", "schema_v2"), False, "IBN7-AC3"),
    ("silver columns changed", ("first_run", "silver", "columns_equal_first_run"), False, "IBN7-AC3"),
    ("new keys miscounted", ("first_run", "new_keys_total"), 6, "IBN7-AC3"),
    ("a key outside scope", ("first_run", "keys_outside_inflection_scope"), 1, "IBN7-AC3"),
]


def run(root, cid):
    out = subprocess.run([sys.executable, str(HERE / "pn7_cells.py"), str(root), cid], capture_output=True, text=True, timeout=60)
    return out.returncode, (out.stdout.strip().splitlines() or ["-"])[-1]


def main(repo):
    repo = Path(repo).resolve()
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in (P.ADDENDUM, P.COO_HALF, P.CTO_HALF, P.WRITER_ORDER, P.SCRIPT):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(repo / rel, root / rel)
        rec = root / P.RECORD
        rec.parent.mkdir(parents=True, exist_ok=True)
        rc = {c: run(root, c)[0] for c in P.CHECKS}
        print("NO RECORD (the base):", rc, "(all must be 1)")
        bad += sum(1 for v in rc.values() if v != 1)
        rec.write_text(json.dumps(GOOD), encoding="utf-8")
        pos = {c: run(root, c) for c in P.CHECKS}
        print("POSITIVE:", {c: v[1] for c, v in pos.items()})
        bad += sum(1 for v in pos.values() if v[0] != 0)
        for name, path, value, cid in NEGATIVES:
            mutated = copy.deepcopy(GOOD)
            node = mutated
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            if name == "bound not household count":
                mutated["first_run"]["requests_made"] = value
            rec.write_text(json.dumps(mutated), encoding="utf-8")
            results = {c: run(root, c)[0] for c in P.CHECKS}
            ok = results[cid] == 1 and sum(results.values()) == 1
            print("%-34s fails %s only: %s" % (name, cid, "OK" if ok else "UNEXPECTED %s" % results))
            bad += 0 if ok else 1
        rec.write_text(json.dumps(GOOD), encoding="utf-8")
        (root / P.SCRIPT).write_text("# a different script\n", encoding="utf-8")
        results = {c: run(root, c)[0] for c in P.CHECKS}
        ok = results["IBN7-AC1"] == 1 and results["IBN7-AC2"] == 0 and results["IBN7-AC3"] == 0
        print("%-34s fails IBN7-AC1 only: %s" % ("repository script differs", "OK" if ok else "UNEXPECTED %s" % results))
        bad += 0 if ok else 1
    print("unexpected: %d" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
