"""Positive control and negatives for p206_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control206.py <real_repo_root>
Builds a temp tree holding the real lib/trading_calendar.py and three stub manual_api scripts, writes a clean synthetic record (computed from the calendar),
runs every criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp tree is removed.
"""
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r206/p206_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p206_cells as P  # noqa: E402

spec = importlib.util.spec_from_file_location("tcal_ctl", str(REAL / "lib/trading_calendar.py"))
CAL = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CAL)
SCRIPTS = {"positions": "pull_inflection_positions_daily.py", "transactions": "pull_inflection_transactions_v2.py", "performance": "pull_inflection_performance_rest.py"}
READ_DATE = "2026-10-15"


def build():
    root = Path(tempfile.mkdtemp(prefix="c206_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / "data/inf/manual_api").mkdir(parents=True)
    hashes = {}
    for feed, s in SCRIPTS.items():
        b = ("# stub %s\n" % feed).encode()
        (root / "data/inf/manual_api" / s).write_bytes(b)
        hashes[feed] = hashlib.sha256(b).hexdigest()
    (root / "infra/aws/lambda/inf-pipeline/inf-gold-trigger").mkdir(parents=True)
    (root / "infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py").write_text("x = 1\n")
    return root, hashes


def record(hashes):
    steps = {f: {"step": P.STEPS[f], "script": SCRIPTS[f], "invokes_manual_api": True, "chain_copy_sha256": hashes[f], "repo_cli_sha256": hashes[f], "identical": True,
                 "evidence": "dispatch script line 612 identifier run_pull_step invokes the manual_api script by name"} for f in P.FEEDS}
    spans = {}
    for f, (a, b) in {"positions": ("2026-05-04", "2026-10-14"), "transactions": ("2026-05-04", "2026-10-14"), "performance": ("2026-05-04", "2026-10-14")}.items():
        days = [d.isoformat() for d in CAL.trading_days_between(a, b)]
        miss = days[3:5]
        spans[f] = {"first_key_day": a, "last_key_day": b, "trading_days_in_span": len(days), "flat_present": len(days) - len(miss) - 2, "parquet_only": 2,
                    "missing_count": len(miss), "missing": miss, "keys_listed": len(days), "out_of_span_note": "days before the first key are out of span, not missing"}
    end = CAL.prev_trading_day(dt.date.fromisoformat(READ_DATE))
    want = [d for d in CAL.trading_days_between(end - dt.timedelta(days=45), end)][-20:]
    feeds = {}
    for f in P.FEEDS:
        feeds[f] = [{"day": d.isoformat(), "landed_at_utc": d.isoformat() + "T11:41:07Z", "asof_field": "asOfDate", "asof_day": CAL.prev_trading_day(d).isoformat(),
                     "asof_is_prior_trading_day": True} for d in want]
    return {"base_commit": "a" * 40, "read_date": READ_DATE,
            "chain_invocation": {"steps": steps, "positive_control_needed": False, "positive_control_plan": "not needed: every step invokes the manual_api script by name",
                                 "cli_retirement_scope": "retire only a bronze write the chain does not reach; the invoked scripts stay"},
            "silver_aggregator": {"function": "inf-silver-aggregator", "code_sha256_b64": "A" * 43 + "=", "handler": "lambda_function.handler", "runtime": "python3.12",
                                  "source_in_repo": False, "repo_path": None, "source_map_entry": False,
                                  "gap_statement": "no source directory under infra/aws/lambda/inf-pipeline; the artifact is built outside the repository"},
            "spans": spans, "absent_total": sum(len(s["missing"]) for s in spans.values()),
            "t1_completeness": {"feeds": feeds},
            "data_ready_field": {"found": False, "name": None, "note": "no data-ready field in the pulled content of the three feeds"},
            "earliest_measured_complete": {"claim": "measured", "clock_ny": "07:56", "reason": "every as-of day equals the prior trading day and the latest landing in 20 days is 07:56 New York"},
            "trigger_moves_now": False,
            "notes": ["objects read: 60 small bronze objects, as-of field and landing time only", "not read: the vendor's documentation and any Orion endpoint",
                      "the dispatch script was read from its S3 object; the repository holds no copy"],
            **{k: 0 for k in P.P6.BOUND}}


def write(root, rec):
    p = root / P.REC
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def m(ac, name, fn):
    return (ac, name, fn)


def set_path(d, path, v):
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = v


MUTS = [
    m("AC1", "wrong_step_name", lambda r: set_path(r, ["chain_invocation", "steps", "positions", "step"], "INF_API_PULL_X")),
    m("AC1", "script_missing_in_tree", lambda r: set_path(r, ["chain_invocation", "steps", "positions", "script"], "pull_nothing.py")),
    m("AC1", "repo_hash_wrong", lambda r: set_path(r, ["chain_invocation", "steps", "transactions", "repo_cli_sha256"], "e" * 64)),
    m("AC1", "identical_flag_wrong", lambda r: set_path(r, ["chain_invocation", "steps", "performance", "identical"], False)),
    m("AC1", "control_flag_wrong", lambda r: (set_path(r, ["chain_invocation", "steps", "performance", "invokes_manual_api"], False),
                                              set_path(r, ["chain_invocation", "steps", "performance", "chain_copy_sha256"], "d" * 64),
                                              set_path(r, ["chain_invocation", "steps", "performance", "identical"], False))),
    m("AC1", "retirement_scope_short", lambda r: set_path(r, ["chain_invocation", "cli_retirement_scope"], "short")),
    m("AC1", "silver_in_repo_without_path", lambda r: set_path(r, ["silver_aggregator", "source_in_repo"], True)),
    m("AC1", "silver_digest_bad", lambda r: set_path(r, ["silver_aggregator", "code_sha256_b64"], "short")),
    m("AC2", "span_count_wrong", lambda r: set_path(r, ["spans", "positions", "trading_days_in_span"], 5)),
    m("AC2", "missing_not_a_trading_day", lambda r: set_path(r, ["spans", "transactions", "missing"], ["2026-05-09", "2026-05-12"])),
    m("AC2", "partition_broken", lambda r: set_path(r, ["spans", "performance", "flat_present"], 1)),
    m("AC2", "absent_total_wrong", lambda r: set_path(r, ["absent_total"], 1)),
    m("AC2", "missing_count_wrong", lambda r: set_path(r, ["spans", "positions", "missing_count"], 9)),
    m("AC3", "rows_not_last_20", lambda r: r["t1_completeness"]["feeds"]["positions"].pop(0)),
    m("AC3", "asof_flag_wrong", lambda r: set_path(r, ["t1_completeness", "feeds", "performance", 3, "asof_is_prior_trading_day"], False)),
    m("AC3", "measured_with_stale_asof", lambda r: (set_path(r, ["t1_completeness", "feeds", "performance", 3, "asof_day"], "2026-01-02"),
                                                    set_path(r, ["t1_completeness", "feeds", "performance", 3, "asof_is_prior_trading_day"], False))),
    m("AC3", "landing_day_mismatch", lambda r: set_path(r, ["t1_completeness", "feeds", "transactions", 2, "landed_at_utc"], "2026-01-02T11:41:07Z")),
    m("AC3", "measured_with_too_few_days", lambda r: [r["t1_completeness"]["feeds"]["positions"].__setitem__(i, {"day": r["t1_completeness"]["feeds"]["positions"][i]["day"], "key_present": False, "landed_at_utc": None, "asof_day": None}) for i in range(9)]),
    m("AC3", "absent_day_with_landing", lambda r: r["t1_completeness"]["feeds"]["positions"].__setitem__(0, {"day": r["t1_completeness"]["feeds"]["positions"][0]["day"], "key_present": False, "landed_at_utc": "2026-01-02T11:41:07Z", "asof_day": None})),
    m("AC3", "trigger_moves", lambda r: set_path(r, ["trigger_moves_now"], True)),
    m("AC3", "clock_not_hhmm", lambda r: set_path(r, ["earliest_measured_complete", "clock_ny"], "7am")),
    m("AC3", "short_notes", lambda r: set_path(r, ["notes"], ["short"])),
    m("AC3", "counter_nonzero", lambda r: set_path(r, ["vendor_requests_sent"], 1)),
]

bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root, hashes = build()
rec = record(hashes)
write(root, rec)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB206-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB206-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
