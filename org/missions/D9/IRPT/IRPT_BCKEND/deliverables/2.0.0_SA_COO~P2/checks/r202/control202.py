"""Positive control and negatives for p202_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control202.py <real_repo_root>
Builds a temp root with a synthetic record, runs every criterion expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r202/p202_cells.py"
for sub in ("r196", "r202"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p202_cells as P  # noqa: E402

P6 = P.P6
REC = {
    "base_commit": "a" * 40,
    "writer": {"claim": "inferred", "kind": "ecs_task", "name": "inf-bronze-flat-writer", "statement": "a scheduled ECS task in the Inflection account writes the flat keys each morning after the parquet",
               "evidence": ["CloudTrail PutObject events on the flat keys name the task role in the window", "the task definition's command names the manual pull with the upload flag",
                            "the task's schedule fires at 11:35Z every weekday per its rule"]},
    "searched": {"cloudtrail": {"window": "2026-10-10 to 2026-10-14", "events_matching": 15, "method": "lookup-events on the bucket's object-level data events for the flat key prefix"},
                 "s3_access_logs": {"enabled": False, "result": "server access logging is not enabled on the source bucket"},
                 "lambda_functions_listed": 120, "eventbridge_rules_listed": 155, "ecs_clusters_listed": 3, "glue_jobs_listed": 0, "ec2_instances_listed": 40, "ssm_associations_listed": 12},
    "object_metadata": {"keys_examined": 6, "findings": "the objects carry the task role's session name and no custom metadata; content type is gzip"},
    "handover": "the task is disabled in the same ledger as the scheduled handler's first enabled day; its rule is kept as the rollback",
    "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120)
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def root_with(rec):
    root = Path(tempfile.mkdtemp(prefix="c202_"))
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
    return root


bad = 0


def expect(label, cid, rec, want):
    global bad
    root = root_with(rec)
    r = run(root, cid)
    shutil.rmtree(root, ignore_errors=True)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-46s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB202-1-" + ac, REC, True)


def m(fn):
    o = copy.deepcopy(REC)
    fn(o)
    return o


for label, ac, rec in (
        ("an unknown writer kind", "AC1", m(lambda o: o["writer"].update({"kind": "magic"}))),
        ("two evidence lines", "AC1", m(lambda o: o["writer"].update({"evidence": o["writer"]["evidence"][:2]}))),
        ("not_found claimed as measured", "AC1", m(lambda o: o["writer"].update({"kind": "not_found", "claim": "measured"}))),
        ("a writer with no name", "AC1", m(lambda o: o["writer"].update({"name": ""}))),
        ("no CloudTrail window dates", "AC2", m(lambda o: o["searched"]["cloudtrail"].update({"window": "last week"}))),
        ("a missing search count", "AC2", m(lambda o: o["searched"].pop("glue_jobs_listed"))),
        ("access logs state missing", "AC2", m(lambda o: o["searched"]["s3_access_logs"].pop("enabled"))),
        ("two keys examined", "AC3", m(lambda o: o["object_metadata"].update({"keys_examined": 2}))),
        ("no hand-over", "AC3", m(lambda o: o.update({"handover": ""}))),
        ("a vendor request sent", "AC3", m(lambda o: o.update({"vendor_requests_sent": 1}))),
        ("a long digit run", "AC3", m(lambda o: o.update({"notes": ["account 123456789012"]})))):
    expect(label, "IB202-1-" + ac, rec, False)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
