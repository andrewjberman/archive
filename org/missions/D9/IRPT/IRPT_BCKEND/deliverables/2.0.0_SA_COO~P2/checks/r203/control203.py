"""Positive control and negatives for p203_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control203.py <real_repo_root>
Builds temp git roots with a stub file for the file sites and synthetic records and packets, runs every criterion expecting PASS, then applies each
mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r203/p203_cells.py"
for sub in ("r196", "r200", "r203"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p203_cells as P  # noqa: E402

P6 = P.P6
PO = P.PO


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt if isinstance(txt, str) else json.dumps(txt), encoding="utf-8")


PERF = ["2026-05-%02d" % d for d in range(4, 24)] + ["2026-07-01", "2026-09-28"]
H = "ab" * 32
H2 = "cd" * 32
ORION = {
    "base_commit": "a" * 40,
    "pair_b": {"files": [{"path": "cli/chain.py", "line": 4, "identifier": "chain_trigger"}],
               "retiming": "the existing inf-gold-trigger Lambda's schedule moves into the 06:00 America/New_York fold; it keeps starting the runner and sending the chain",
               "new_function": False, "port": False, "silver_steps_chained": True,
               "t1_completeness": {"claim": "inferred", "statement": "Orion's T-1 is complete by 06:00 New York on the days measured; the earliest measured-complete time is 05:40",
                                   "evidence": ["the newest bronze object of each feed lands before 05:40 on the measured days", "no feed rewrote a T-1 object after 06:00 in the window"]},
               "cli_retirement": "each manual CLI's bronze writes are removed and it exits with a message naming the gold chain; the scripts stay for the chain's copy",
               "schedule_builder_output": "any new schedule name is the output of lib/opal_naming.py name(); the existing trigger keeps its name",
               "trading_day_frontier": "the chain pulls the previous trading day by lib/trading_calendar.py"},
    "pair_a": {"feeds": {
        "positions": {"days": list(PO.DAYS), "keys": [PO.KEYPFX + d + ".jsonl.gz" for d in PO.DAYS], "requests": 2240, "chain_step": "INF_API_PULL_POSITIONS_DAILY"},
        "transactions": {"days": list(PO.TXN_DAYS), "keys": ["s3://opal-data-inf/bronze/transactions/" + d + ".jsonl.gz" for d in PO.TXN_DAYS], "requests": 6041, "chain_step": "INF_API_PULL_TXN"},
        "performance": {"days": PERF, "keys": ["s3://opal-data-inf/bronze/performance/" + d + ".jsonl.gz" for d in PERF], "requests": 7040, "chain_step": "INF_API_PULL_PERF"}},
        "absent_beforehand_read_at_act": True, "through_chain_steps": True,
        "read_back": "list each written key and compare its size and ETag with the response held in scratch",
        "rollback_per_key": "delete each created key by the version id its put returned (Andrew's act) after a HEAD showed it absent",
        "absent_at_source_policy": "where the vendor returns nothing for a day the day is recorded ABSENT-AT-SOURCE with the response status and we never write an empty key"},
    "blast_radius": {"writes": ["flat keys for the absent trading days of three feeds"], "reads": ["the vendor"], "new_iam": False, "served_values_changed": False, "other_dates_touched": False},
    "build_slices": [{"cell": "retime the trigger", "risk": "LOCAL", "files": ["infra/x.tf"]}],
    "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
PKT = "# never-widen packet v2\n" + "pair (a), pair (b); blast radius; rollback; stop rule; re-timing of inf-gold-trigger; no shadow pipeline; this packet supersedes IB-pr-556; COO half UNSIGNED. CTO half UNSIGNED.\n" + ("padding line\n" * 600)
REC2 = {
    "base_commit": "b" * 40, "function": "irpt-ycharts-generate", "live_codesha256": P.LIVE_DIGEST,
    "candidate": {"codesha256": "Z" * 43 + "=", "moved_count": 3, "total_members": 104, "moved_members": ["a/submission.py", "a/acceptance.py", "a/contracts/AnalysisSubmissionRequest.schema.json"]},
    "r29c_members_preserved": True,
    "endpoint_members": {k: {"sha256_at_signing": H, "sha256_now": H, "changed": False} for k in P.ENDPOINT_MEMBERS},
    "endpoint_bytes_moved": False, "resign_needed": False, "pre_apply_digest_restated": P.LIVE_DIGEST,
    "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}


def make(rec1=None, pkt=None, rec2=None):
    root = Path(tempfile.mkdtemp(prefix="c203_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    wt(root, "cli/chain.py", "import x\n\n\ndef other():\n    return 0\n\n\ndef chain_trigger():\n    return 1\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    r = copy.deepcopy(rec1 or ORION)
    r["pair_b"]["files"][0]["line"] = 8
    wt(root, P.REC1, r)
    wt(root, P.PKT1, pkt if pkt is not None else PKT)
    wt(root, P.REC2, rec2 or REC2)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "work")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-46s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = make()
for cid in P.CHECKS:
    expect("clean", cid, root, True)
shutil.rmtree(root, ignore_errors=True)


def mo(fn):
    o = copy.deepcopy(ORION)
    fn(o)
    return o


def my(fn):
    o = copy.deepcopy(REC2)
    fn(o)
    return o


for label, cid, kw in (
        ("a new function built alongside", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"].update({"new_function": True})))),
        ("a port", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"].update({"port": True})))),
        ("silver steps not chained", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"].update({"silver_steps_chained": False})))),
        ("re-timing that names no trigger", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"].update({"retiming": "the schedule moves into the 06:00 America/New_York fold of the morning"})))),
        ("no clock time in the completeness read", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"]["t1_completeness"].update({"statement": "Orion's T-1 is complete early enough on the days measured by the read"})))),
        ("a CLI not naming the chain", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"].update({"cli_retirement": "each manual CLI's bronze writes are removed and the scripts exit quietly"})))),
        ("a wrong file identifier", "IB203-1-AC1", dict(rec1=mo(lambda o: o["pair_b"]["files"][0].update({"identifier": "nope_function"})))),
        ("performance with 21 days", "IB203-1-AC2", dict(rec1=mo(lambda o: o["pair_a"]["feeds"]["performance"].update({"days": PERF[:-1], "keys": o["pair_a"]["feeds"]["performance"]["keys"][:-1]})))),
        ("a feed missing", "IB203-1-AC2", dict(rec1=mo(lambda o: o["pair_a"]["feeds"].pop("transactions")))),
        ("not through the chain's steps", "IB203-1-AC2", dict(rec1=mo(lambda o: o["pair_a"].update({"through_chain_steps": False})))),
        ("no chain step name", "IB203-1-AC2", dict(rec1=mo(lambda o: o["pair_a"]["feeds"]["positions"].update({"chain_step": ""})))),
        ("no ABSENT-AT-SOURCE policy", "IB203-1-AC2", dict(rec1=mo(lambda o: o["pair_a"].update({"absent_at_source_policy": "where the vendor returns nothing we write an empty key and move on quickly"})))),
        ("other dates touched", "IB203-1-AC2", dict(rec1=mo(lambda o: o["blast_radius"].update({"other_dates_touched": True})))),
        ("a packet too short", "IB203-1-AC3", dict(pkt="# packet\nshort. COO half UNSIGNED. CTO half UNSIGNED.\n")),
        ("a packet that does not supersede", "IB203-1-AC3", dict(pkt=PKT.replace("supersedes", "follows"))),
        ("one half signed", "IB203-1-AC3", dict(pkt=PKT.replace("CTO half UNSIGNED.", "CTO half signed."))),
        ("a vendor request already sent", "IB203-1-AC3", dict(rec1=mo(lambda o: o.update({"vendor_requests_sent": 1})))),
        ("the wrong live digest", "IB203-2-AC1", dict(rec2=my(lambda o: o.update({"live_codesha256": "tdpterTMfJl" + "A" * 31 + "="})))),
        ("the stale IB-pr-456 build", "IB203-2-AC1", dict(rec2=my(lambda o: o["candidate"].update({"codesha256": "AHxuDf7h" + "A" * 35 + "="})))),
        ("moved members not matching the count", "IB203-2-AC1", dict(rec2=my(lambda o: o["candidate"].update({"moved_count": 5})))),
        ("release 29's uploads.py moved", "IB203-2-AC2", dict(rec2=my(lambda o: o["candidate"]["moved_members"].append("a/uploads.py")))),
        ("an ENDPOINT member moved with no re-sign", "IB203-2-AC2", dict(rec2=my(lambda o: o["endpoint_members"]["submission.py"].update({"sha256_now": H2, "changed": True})))),
        ("changed flag disagreeing with the hashes", "IB203-2-AC2", dict(rec2=my(lambda o: o["endpoint_members"]["acceptance.py"].update({"changed": True})))),
        ("the pre-apply digest not restated", "IB203-2-AC3", dict(rec2=my(lambda o: o.update({"pre_apply_digest_restated": "tdpterTMfJl" + "A" * 31 + "="})))),
        ("a counter above 0", "IB203-2-AC3", dict(rec2=my(lambda o: o.update({"aws_writes_made": 1}))))):
    rt = make(**kw)
    expect(label, cid, rt, False)
    shutil.rmtree(rt, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
