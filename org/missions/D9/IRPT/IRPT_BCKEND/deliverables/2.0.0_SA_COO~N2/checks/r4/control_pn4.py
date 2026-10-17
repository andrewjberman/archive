"""Control for pn4_cells.py: a positive arm per host kind (a synthetic good record, all three PASS) and one negative per rule (each
fails only its own arm). Builds its own temp root from the real addendum 4, its halves and the IB-pn-3 order; synthetic record;
removed at the end. Usage: python control_pn4.py <repo_root>; prints a summary and exits 1 on any unexpected result."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pn4_cells as P  # noqa: E402

GOOD = {
    "gates": {"addendum_blob": P.ADDENDUM_BLOB, "both_halves_signed": True,
              "dispatch_object": {"live_sha256": "a" * 64, "repository_sha256": "a" * 64, "equal": True},
              "other_open_ledger_on_chain": False,
              "runner_role": {"secret_read_allowed": True, "feed_prefix_write_allowed": True},
              "household_count": 294, "request_bound": 294,
              "sidecar": {"live_sha256": "e" * 64, "equals_generated_address": True}, "calendar_object_present": True},
    "ledger_entry": "org/critical_paths/change_management/x.json",
    "apply": {"applied_at_utc": "2026-10-17T15:00:00Z",
              "replaced_script": {"sha256": P.REPLACED_OK[0], "saved_copy_sha256": P.REPLACED_OK[0]},
              "script": {"uploaded_sha256": P.SCRIPT_SHA},
              "import_smoke": {"ran_on_runner": False, "fallback_host": True, "python_version": "3.9.25",
                               "part_i_import_and_prefixes": True, "part_ii_session_token_client_under_scrubbed_env": True,
                               "part_iii_plan_only_run": True, "built_from_live_prefixes": True, "exit_code": 0,
                               "orion_requests": 0},
              "dispatch_edit": {"saved_copy_sha256": "c" * 64, "rows_added": 1, "chain_entries_added": 2,
                                "chains_carrying_perf": 2, "other_lines_changed": 0},
              "rollback_performed": False},
    "first_run": {"read_from_step_log": True, "exit_code": 0, "tolerated_failure": False, "skipped_days": 0,
                  "requests_made": 294, "calc_gross_of_fees_false_on_every_request": True,
                  "keys_outside_inflection_scope": 0, "coverage": {"denominator": 800, "returned": 700, "absent": 100},
                  "zero_returns": 0, "stored_value": "daily_factor"},
}
NEGATIVES = [
    ("dispatch differs", ("gates", "dispatch_object", "equal"), False, "IBN4-AC1"),
    ("another ledger open", ("gates", "other_open_ledger_on_chain"), True, "IBN4-AC1"),
    ("bound not household count", ("gates", "request_bound"), 293, "IBN4-AC1"),
    ("halves flag", ("gates", "both_halves_signed"), False, "IBN4-AC1"),
    ("sidecar differs from address()", ("gates", "sidecar", "equals_generated_address"), False, "IBN4-AC1"),
    ("calendar object absent", ("gates", "calendar_object_present"), False, "IBN4-AC1"),
    ("applied inside the weekday band", ("apply", "applied_at_utc"), "2026-10-19T12:00:00Z", "IBN4-AC1"),
    ("applied on the transaction day", ("apply", "applied_at_utc"), "2026-10-20T16:00:00Z", "IBN4-AC1"),
    ("wrong upload hash", ("apply", "script", "uploaded_sha256"), "d" * 64, "IBN4-AC2"),
    ("replaced object unexpected", ("apply", "replaced_script", "sha256"), "f" * 64, "IBN4-AC2"),
    ("smoke part ii missing", ("apply", "import_smoke", "part_ii_session_token_client_under_scrubbed_env"), False, "IBN4-AC2"),
    ("smoke part iii missing", ("apply", "import_smoke", "part_iii_plan_only_run"), False, "IBN4-AC2"),
    ("smoke made an Orion request", ("apply", "import_smoke", "orion_requests"), 1, "IBN4-AC2"),
    ("smoke exit nonzero", ("apply", "import_smoke", "exit_code"), 1, "IBN4-AC2"),
    ("smoke not on live prefixes", ("apply", "import_smoke", "built_from_live_prefixes"), False, "IBN4-AC2"),
    ("two rows added", ("apply", "dispatch_edit", "rows_added"), 2, "IBN4-AC2"),
    ("other dispatch lines changed", ("apply", "dispatch_edit", "other_lines_changed"), 1, "IBN4-AC2"),
    ("rollback performed", ("apply", "rollback_performed"), True, "IBN4-AC2"),
    ("tolerated failure", ("first_run", "tolerated_failure"), True, "IBN4-AC3"),
    ("read from the chain exit", ("first_run", "read_from_step_log"), False, "IBN4-AC3"),
    ("skipped day", ("first_run", "skipped_days"), 1, "IBN4-AC3"),
    ("coverage does not sum", ("first_run", "coverage", "absent"), 1, "IBN4-AC3"),
    ("a zero written", ("first_run", "zero_returns"), 1, "IBN4-AC3"),
    ("requests over the bound", ("first_run", "requests_made"), 295, "IBN4-AC3"),
    ("a key outside scope", ("first_run", "keys_outside_inflection_scope"), 1, "IBN4-AC3"),
    ("summary stored", ("first_run", "stored_value"), "return_value", "IBN4-AC3"),
]


def run(root, cid):
    out = subprocess.run([sys.executable, str(HERE / "pn4_cells.py"), str(root), cid], capture_output=True, text=True, timeout=60)
    return out.returncode, (out.stdout.strip().splitlines() or ["-"])[-1]


def main(repo):
    repo = Path(repo).resolve()
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in (P.ADDENDUM, P.COO_HALF, P.CTO_HALF, P.BUILDER_ORDER):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(repo / rel, root / rel)
        rec = root / P.RECORD
        rec.parent.mkdir(parents=True, exist_ok=True)
        rc = {c: run(root, c)[0] for c in P.CHECKS}
        print("NO RECORD (the base):", rc, "(all must be 1)")
        bad += sum(1 for v in rc.values() if v != 1)
        for label, data in (("ib2 host fallback", GOOD), ("runner", None)):
            rec_data = copy.deepcopy(GOOD)
            if data is None:
                rec_data["apply"]["import_smoke"].update({"ran_on_runner": True, "fallback_host": False})
            rec.write_text(json.dumps(rec_data), encoding="utf-8")
            pos = {c: run(root, c) for c in P.CHECKS}
            print("POSITIVE (%s):" % label, {c: v[1] for c, v in pos.items()})
            bad += sum(1 for v in pos.values() if v[0] != 0)
        for name, path, value, cid in NEGATIVES:
            mutated = copy.deepcopy(GOOD)
            node = mutated
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            if name == "bound not household count":
                mutated["first_run"]["requests_made"] = value  # keep the run within the new bound so only AC1 sees the defect
            rec.write_text(json.dumps(mutated), encoding="utf-8")
            results = {c: run(root, c)[0] for c in P.CHECKS}
            ok = results[cid] == 1 and sum(results.values()) == 1
            print("%-34s fails %s only: %s" % (name, cid, "OK" if ok else "UNEXPECTED %s" % results))
            bad += 0 if ok else 1
    print("unexpected: %d" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
