"""IRPT_BCKEND workstream ~PO round 3 (issuer 2.0.0_SA_COO~P2) -- the check of the AWS READ for the unlocated Orion flat-key writer (CTO half of IB-pr-556, condition 1).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB202-1  IB-pr-559  READ ONLY: what writes the daily Orion Inflection flat keys (bronze/{positions,transactions,performance}/<date>.jsonl.gz) between 11:39 and 11:56Z
    AC1  the writer located (or absent with the search stated): kind, name, claim, evidence
    AC2  what was searched, as counts with their denominators (CloudTrail window, S3 access logs, Lambda, EventBridge, ECS, Glue, EC2, SSM)
    AC3  the object metadata read, the hand-over or stop path, notes, counters 0, no long digit run
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~403/IB202-1_flat_key_writer_read.json"
KINDS = ("lambda", "ecs_task", "glue_job", "ec2_instance", "ssm_association", "eventbridge_rule", "codebuild", "stepfunction", "external_person",
         "seat_session_cron", "other", "not_found")
CLAIMS = ("measured", "inferred", "absent")
COUNTS = ("lambda_functions_listed", "eventbridge_rules_listed", "ecs_clusters_listed", "glue_jobs_listed", "ec2_instances_listed", "ssm_associations_listed")
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    w = r.get("writer") or {}
    if w.get("claim") not in CLAIMS or w.get("kind") not in KINDS:
        fail("writer needs a claim (%s) and a kind (%s)" % ("/".join(CLAIMS), "/".join(KINDS)))
    text(w.get("statement"), 40, "writer.statement")
    ev = w.get("evidence")
    if not isinstance(ev, list) or len(ev) < 3 or not all(isinstance(x, str) and len(x) > 20 for x in ev):
        fail("writer needs at least three evidence lines (for not_found: what was searched, where, and what each search returned)")
    if w["kind"] == "not_found" and w["claim"] == "measured":
        fail("a writer that was not found cannot be a measured claim about the writer")
    if w["kind"] != "not_found":
        text(w.get("name"), 4, "writer.name (the resource name, never an id or an account number)")
    print("OK: the writer, its kind, its claim and three evidence lines")


def c2():
    r = load(REC)
    s = r.get("searched") or {}
    ct = s.get("cloudtrail") or {}
    if not isinstance(ct.get("window"), str) or not re.search(r"2026-10-\d\d", ct["window"]) or not is_int(ct.get("events_matching")) or ct["events_matching"] < 0:
        fail("searched.cloudtrail needs a window naming dates and events_matching as a count")
    text(ct.get("method"), 30, "searched.cloudtrail.method")
    sl = s.get("s3_access_logs") or {}
    if sl.get("enabled") not in (True, False):
        fail("searched.s3_access_logs.enabled must be true or false")
    text(sl.get("result"), 20, "searched.s3_access_logs.result")
    for k in COUNTS:
        if not is_int(s.get(k)) or s[k] < 0:
            fail("searched.%s must be a count" % k)
    print("OK: what was searched, with counts")


def c3():
    r = load(REC)
    om = r.get("object_metadata") or {}
    if not is_int(om.get("keys_examined")) or om["keys_examined"] < 3:
        fail("object_metadata.keys_examined must be at least 3 (one per feed)")
    text(om.get("findings"), 30, "object_metadata.findings")
    text(r.get("handover"), 40, "handover (how the writer is stopped or handed to the scheduled handler, or why not applicable)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: object metadata, hand-over, counters 0")


CHECKS = {"IB202-1-AC1": c1, "IB202-1-AC2": c2, "IB202-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p202_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
