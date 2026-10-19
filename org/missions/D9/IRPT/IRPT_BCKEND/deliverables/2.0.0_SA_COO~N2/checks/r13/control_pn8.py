"""Control for pn8_cells.py (cell IB-pn-8): builds a temp root from the real ADDENDUM 5, both halves, the script and the pn7 check, a synthetic pn7
record that passes IBN7-AC3, and a synthetic backfill record (all three PASS on both host shapes), then one negative per rule (each fails only its
own arm). Usage: python control_pn8.py <repo_root>."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "r12"))
import control_pn7 as C7  # noqa: E402
import pn7_cells as P7  # noqa: E402
import pn8_cells as P  # noqa: E402

GOOD = {
    "gates": {"addendum_blob": P.ADD5_BLOB, "both_halves_signed": True, "live_script_sha256": P.SCRIPT_SHA,
              "live_hash_read_immediately_before_run": True, "household_count": 294, "earliest_start_date_read": True,
              "partition_count_stated": 2326, "stated_before_first_call": True, "other_act_open_on_chain": False,
              "host": {"kind": "ib2_host", "every_check_allowed_as_is": True, "grants_added": 0}},
    "run": {"started_at_utc": "2026-10-21T15:00:00Z", "calls_made": 294, "call_phase_seconds": 560, "days_written": 2326,
            "days_skipped_existing": 0, "zero_returns": 0, "keys_outside_feed_prefixes": 0, "stored_value": "daily_factor",
            "calc_gross_of_fees_false_on_every_request": True, "run_objects_written": 1, "envelopes_v2_without_responses": True,
            "peak_memory_mb": 2200.5, "host_memory_limit_mb": 8000, "write_phase_seconds": 3000, "persistent_429": False,
            "overwrote_existing_day": False},
    "check": {"days_read_back": 2326, "accounts": [{"window_days": 200, "error_bp": 0.1}, {"window_days": 237, "error_bp": 0.5},
                                                   {"window_days": 100, "error_bp": 0.0}, {"window_days": 30, "error_bp": 0.2},
                                                   {"window_days": 150, "error_bp": 0.3}],
              "window_named_readable": False},
}
NEGATIVES = [
    ("halves flag", ("gates", "both_halves_signed"), False, "IBN8-AC1"),
    ("live hash differs", ("gates", "live_script_sha256"), "0" * 64, "IBN8-AC1"),
    ("hash not read just before", ("gates", "live_hash_read_immediately_before_run"), False, "IBN8-AC1"),
    ("household count over bound", ("gates", "household_count"), 295, "IBN8-AC1"),
    ("partition count other than 2326", ("gates", "partition_count_stated"), 2000, "IBN8-AC1"),
    ("partition count stated after", ("gates", "stated_before_first_call"), False, "IBN8-AC1"),
    ("another act open", ("gates", "other_act_open_on_chain"), True, "IBN8-AC1"),
    ("started inside the band", ("run", "started_at_utc"), "2026-10-21T12:00:00Z", "IBN8-AC1"),
    ("started on the transaction day", ("run", "started_at_utc"), "2026-10-20T16:00:00Z", "IBN8-AC1"),
    ("ib2 host with a grant added", ("gates", "host", "grants_added"), 1, "IBN8-AC1"),
    ("calls over bound", ("run", "calls_made"), 295, "IBN8-AC2"),
    ("call phase over 20 minutes", ("run", "call_phase_seconds"), 1300, "IBN8-AC2"),
    ("days do not sum to the count", ("run", "days_written"), 2000, "IBN8-AC2"),
    ("a zero written", ("run", "zero_returns"), 1, "IBN8-AC2"),
    ("a key outside the prefixes", ("run", "keys_outside_feed_prefixes"), 1, "IBN8-AC2"),
    ("summary stored", ("run", "stored_value"), "return_value", "IBN8-AC2"),
    ("two run objects", ("run", "run_objects_written"), 2, "IBN8-AC2"),
    ("envelopes carry responses", ("run", "envelopes_v2_without_responses"), False, "IBN8-AC2"),
    ("peak memory over the limit", ("run", "peak_memory_mb"), 9000, "IBN8-AC2"),
    ("an existing day overwritten", ("run", "overwrote_existing_day"), True, "IBN8-AC2"),
    ("fewer than 5 accounts", ("check", "accounts"), GOOD["check"]["accounts"][:4], "IBN8-AC3"),
    ("a window over 237 days", ("check", "accounts", 0, "window_days"), 300, "IBN8-AC3"),
    ("an error over 0.5 bp", ("check", "accounts", 1, "error_bp"), 0.6, "IBN8-AC3"),
    ("window named readable", ("check", "window_named_readable"), True, "IBN8-AC3"),
    ("days not all read back", ("check", "days_read_back"), 2000, "IBN8-AC3"),
]


def run(root, cid):
    out = subprocess.run([sys.executable, str(HERE / "pn8_cells.py"), str(root), cid], capture_output=True, text=True, timeout=90)
    return out.returncode, (out.stdout.strip().splitlines() or ["-"])[-1]


def main(repo):
    repo = Path(repo).resolve()
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in (P.ADD5, P.ADD5_COO, P.ADD5_CTO, P.SCRIPT, P7.WRITER_ORDER, P.PN7_CHECK):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(repo / rel, root / rel)
        (root / P7.RECORD).parent.mkdir(parents=True, exist_ok=True)
        (root / P7.RECORD).write_text(json.dumps(C7.GOOD), encoding="utf-8")
        rec = root / P.RECORD
        rec.parent.mkdir(parents=True, exist_ok=True)
        rc = {c: run(root, c)[0] for c in P.CHECKS}
        print("NO RECORD (the base):", rc, "(all must be 1)")
        bad += sum(1 for v in rc.values() if v != 1)
        for label, host in (("ib2_host", GOOD["gates"]["host"]),
                            ("runner, no shutdown sent", {"kind": "runner", "started_once": True, "shutdown_command_sent": False,
                                                          "idle_hours_recorded": True})):
            doc = copy.deepcopy(GOOD)
            doc["gates"]["host"] = host
            rec.write_text(json.dumps(doc), encoding="utf-8")
            pos = {c: run(root, c) for c in P.CHECKS}
            print("POSITIVE (%s):" % label, {c: v[1] for c, v in pos.items()})
            bad += sum(1 for v in pos.values() if v[0] != 0)
        doc = copy.deepcopy(GOOD)
        doc["gates"]["host"] = {"kind": "runner", "started_once": True, "shutdown_command_sent": True, "idle_hours_recorded": True}
        rec.write_text(json.dumps(doc), encoding="utf-8")
        res = {c: run(root, c)[0] for c in P.CHECKS}
        ok = res["IBN8-AC1"] == 1 and sum(res.values()) == 1
        print("%-34s fails IBN8-AC1 only: %s" % ("runner shutdown command sent", "OK" if ok else "UNEXPECTED %s" % res))
        bad += 0 if ok else 1
        for name, path, value, cid in NEGATIVES:
            mutated = copy.deepcopy(GOOD)
            node = mutated
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            if name == "days do not sum to the count":
                mutated["check"]["days_read_back"] = value
            if name == "partition count other than 2326":
                mutated["run"]["days_written"] = value
                mutated["check"]["days_read_back"] = value
            rec.write_text(json.dumps(mutated), encoding="utf-8")
            res = {c: run(root, c)[0] for c in P.CHECKS}
            ok = res[cid] == 1 and sum(res.values()) == 1
            print("%-34s fails %s only: %s" % (name, cid, "OK" if ok else "UNEXPECTED %s" % res))
            bad += 0 if ok else 1
        rec.write_text(json.dumps(GOOD), encoding="utf-8")
        bad7 = copy.deepcopy(C7.GOOD)
        bad7["first_run"]["tolerated_failure"] = True
        (root / P7.RECORD).write_text(json.dumps(bad7), encoding="utf-8")
        res = {c: run(root, c)[0] for c in P.CHECKS}
        ok = res["IBN8-AC1"] == 1 and res["IBN8-AC2"] == 0 and res["IBN8-AC3"] == 0
        print("%-34s fails IBN8-AC1 only: %s" % ("new writer's first run not passed", "OK" if ok else "UNEXPECTED %s" % res))
        bad += 0 if ok else 1
    print("unexpected: %d" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
