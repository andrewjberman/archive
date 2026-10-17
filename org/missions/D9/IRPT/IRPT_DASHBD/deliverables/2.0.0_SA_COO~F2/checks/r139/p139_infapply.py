"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the APPLY of the signed Inflection transaction pair by 0.7.0_AE_CloudOps~IB2 (cell DB-f-2702).

  Packet NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md REVISION 2 (sha256 below; route B, the CTO's msg 10542): the four-statement policy lives on a NEW narrow role the runner
  role assumes. The applier's record is deliverables/0.7.0_AE_CloudOps~IB2/INFLECTION_RELEASE_RECORD.json. The criteria grade the record and then re-read the world FRESH (AWS GET, list
  and describe only).

  DBF139-2-AC1  gates, ledger, role audit (the runner role's 13 inline policies; the new role absent before), the plan (exactly 3 add / 0 change / 0 destroy, the three resources, the four
                sids) and the simulation lines (every ALLOW and DENY the packet names, the gold lines WITH the bucket policy as the resource policy) as the packet states them
  DBF139-2-AC2  fresh reads: the new role exists with its trust on the runner role only and the fixed session name, holds the four-statement policy; the runner role holds its 13 policies
                plus exactly one assume policy (one statement, sts:AssumeRole on the new role); the three new code objects and the new dispatch version exist with the recorded VersionIds
                and hashes, the prior dispatch version is still present, the receipt's bundle_sha256 equals the zip's, the runner is stopped
  DBF139-2-AC3  the dry run (S6 N of N, nothing written, the assumed role and session printed), the bounded first write (at most 25 days, 19 columns, the schema hash, valid claims, no
                repeated source line) and a fresh LIST of the target prefix equal to the recorded days, each partition with its data.parquet and manifest.json

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

APPLIER = "0.7.0_AE_CloudOps~IB2"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~IB2/INFLECTION_RELEASE_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md"
COO_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_INFLECTION_TRANSACTION_RELEASE_COO_HALF.md"
CTO_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_INFLECTION_TRANSACTION_RELEASE_CTO_HALF.md"
PACKET_SHA = "5bfd8e040939298b3c2d35fca6c3c3bce12c2931e6b444608c8e5b1a514f1126"
ROLE = "inf-gold-layer-ec2-role"
NEW_ROLE = "orion-inf-account-transaction-role"
SESSION_NAME = "g01-account-transaction"
NEW_ADDRESSES = ["aws_iam_role.inf_account_transaction", "aws_iam_role_policy.inf_gold_layer_account_transaction",
                 "aws_iam_role_policy.inf_gold_layer_assume_account_transaction"]
ASSUME_SID = "AssumeTheAccountTransactionRoleOnly"
SIDS = ["S1ReadOrionInflectionTransactionsSilverOnly", "S2ListOrionInflectionTransactionsSilverOnly", "S3PutInflectionAccountTransactionGoldOnly",
        "S4ListInflectionAccountTransactionGoldOnly"]
OTHER_POLICIES = ["cloudfront-invalidate", "cloudwatch-logs", "cloudwatch-put-metric", "cross-firm-bucket-deny", "describe-tags-self", "kms-ebs-decrypt",
                  "orion-inf-scope-account-feed-policy", "runner-shared-read", "s3-scoped-inf", "secrets-manager-orion-jwt", "self-stop", "sns-publish-chainfatal", "ssm-access"]
INSTANCE = "i-0ed5afded2ebd4ed4"
CODE_BUCKET = "opal-data-inf"
CODE_PREFIX = "code/gold/"
KEYS = {"launcher": CODE_PREFIX + "INF_G_01.account_transaction_gold.py", "zip": CODE_PREFIX + "INF_G_01.bundle.zip",
        "receipt": CODE_PREFIX + "INF_G_01.bundle.receipt.json", "dispatch": CODE_PREFIX + "orion-gold-dispatch.sh"}
DISPATCH_SHA12 = "7b206030bfc7"
PRIOR_DISPATCH_VERSION = "0JwOjjCwp0uaux9Ded7FlOAMNWtTfZdU"
SCHEMA_HASH = "ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a"
GOLD_BUCKET = "opal-data-inflection"
GOLD_PREFIX = "irpt/inflection/gold/account_transaction/"
MAX_DAYS = 25
# the simulation lines the packet's Act 3 names: (decision, short label)
# the new role is simulated; the gold-bucket lines carry the live bucket policy as the resource policy (without it the fence reads as allowed: a false green)
SIM_REQUIRED = [("allowed", "silver GetObject"), ("allowed", "silver ListBucket"), ("allowed", "gold PutObject"), ("allowed", "gold ListBucket on the gold prefix"),
                ("denied", "gold ListBucket on another prefix"), ("denied", "gold GetObject"), ("denied", "other firm gold PutObject"), ("denied", "other firm silver GetObject"),
                ("allowed", "runner AssumeRole on the new role")]
SIM_WITH_RESOURCE_POLICY = ["gold PutObject", "gold ListBucket on the gold prefix", "gold ListBucket on another prefix", "gold GetObject", "other firm gold PutObject"]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def head_problems(rec):
    pr = []
    keys = ["claim", "gates", "ledger_entry", "applier", "role_audit", "before", "plan", "apply_finished_utc", "simulation", "uploads", "runner", "dry_run", "first_write", "ledger_closed", "reads"]
    if not isinstance(rec, dict) or any(k not in rec for k in keys):
        return ["the record must carry %s" % keys]
    if rec["claim"] != "measured" or rec["applier"] != APPLIER:
        pr.append("claim must be measured and applier %s" % APPLIER)
    g = rec["gates"]
    ok = isinstance(g, dict) and g.get("packet_sha256") == PACKET_SHA and g.get("coo_half_signed") is True and g.get("cto_half_signed") is True and g.get("pins_ok") is True \
        and g.get("monday_49f_read_passed") is True and isinstance(g.get("one_change_at_a_time"), dict) and is_int(g["one_change_at_a_time"].get("worktrees_read")) \
        and g["one_change_at_a_time"]["worktrees_read"] > 0 and g["one_change_at_a_time"].get("open_markers_naming_this_surface") == 0
    if not ok:
        pr.append("gates must record the packet sha256, both halves signed, the pins, Monday's 49 Financial first-fire read PASSED, and the worktree denominator with 0 open markers naming this surface")
    if not (isinstance(rec["ledger_entry"], str) and rec["ledger_entry"].strip()):
        pr.append("ledger_entry must name the ledger")
    a = rec["role_audit"]
    if not (isinstance(a, dict) and a.get("new_role_absent_before") is True and isinstance(a.get("inline_policies"), list) and sorted(a["inline_policies"]) == sorted(OTHER_POLICIES)):
        pr.append("role_audit must show the runner role's 13 inline policies and that the new role %s is absent before (anything else STOPS the pair)" % NEW_ROLE)
    p = rec["plan"]
    if not (isinstance(p, dict) and p.get("add") == 3 and p.get("change") == 0 and p.get("destroy") == 0 and sorted(p.get("addresses", [])) == sorted(NEW_ADDRESSES)
            and sorted(p.get("statement_sids", [])) == sorted(SIDS) and p.get("replan_no_changes") is True and p.get("naming_gate_refuse") == 0):
        pr.append("plan must read exactly 3 add / 0 change / 0 destroy, the three addresses %r, the four sids, a re-plan of No changes and 0 naming REFUSE" % (NEW_ADDRESSES,))
    sim = rec["simulation"]
    lines = sim.get("lines") if isinstance(sim, dict) else None
    if not isinstance(lines, list):
        pr.append("simulation must carry its lines")
    else:
        got = sorted((x.get("decision"), x.get("label")) for x in lines if isinstance(x, dict))
        if got != sorted(SIM_REQUIRED):
            pr.append("the simulation lines must be exactly the packet's Act 3 lines: %r" % (SIM_REQUIRED,))
        elif sorted(x["label"] for x in lines if x.get("with_resource_policy") is True) != sorted(SIM_WITH_RESOURCE_POLICY):
            pr.append("the gold-bucket simulation lines (and only those) must be run WITH the live bucket policy as the resource policy: %r" % (SIM_WITH_RESOURCE_POLICY,))
    if rec["ledger_closed"] is not False:
        pr.append("the ledger stays open (ledger_closed false) until the CVO's sample")
    return pr


def events_problems(rec):
    pr = []
    dr, fw = rec["dry_run"], rec["first_write"]
    s6 = dr.get("s6") if isinstance(dr, dict) else None
    if not (isinstance(s6, dict) and is_int(s6.get("events")) and s6["events"] > 0 and s6.get("with_equal_amount_line") == s6["events"] and s6.get("missing") == 0):
        pr.append("the dry run's S6 must read N of N events with an equal-amount line, 0 missing, N printed")
    asm = dr.get("assumed") if isinstance(dr, dict) else None
    if not (isinstance(asm, dict) and asm.get("role") == NEW_ROLE and asm.get("session") == SESSION_NAME and isinstance(fw, dict) and fw.get("assumed") == asm):
        pr.append("the dry run and the first write must each print the assumed role %s and session %s" % (NEW_ROLE, SESSION_NAME))
    if not (dr.get("target_objects_after") == 0 and dr.get("repeated_source_lines") == 0 and isinstance(dr.get("window"), dict) and dr["window"].get("newest_written") is None):
        pr.append("the dry run must write nothing (0 objects at the target after), repeat no source line, and show an empty target (newest_written null)")
    ds = fw.get("days_written") if isinstance(fw, dict) else None
    if not (is_int(ds) and 1 <= ds <= MAX_DAYS and fw.get("columns") == 19 and fw.get("schema_hash") == SCHEMA_HASH and fw.get("claims_ok") is True
            and fw.get("repeated_source_lines") == 0 and isinstance(fw.get("days"), list) and len(fw["days"]) == ds and fw.get("since") and fw.get("run_day")):
        pr.append("the first write must be 1 to %d days with the day list, 19 columns, the contract's schema hash, valid claims, no repeated source line, its --since and run day" % MAX_DAYS)
    elif min(fw["days"]) < fw["since"]:
        pr.append("no partition may be older than --since")
    return pr


def sim_decision_ok(lines):
    return all(x.get("decision") in ("allowed", "denied") for x in lines)


def aws_json(root, args):
    shim = str(Path(root, ".tools", "aws.cmd"))
    run = subprocess.run([shim] + args + ["--output", "json"], capture_output=True, text=True, timeout=300)
    if run.returncode != 0:
        raise Fail("aws %s failed: %s" % (" ".join(args[:3]), (run.stderr or run.stdout)[-200:]))
    return json.loads(run.stdout or "null")


def aws_download(root, bucket, key, version, tmp):
    shim = str(Path(root, ".tools", "aws.cmd"))
    run = subprocess.run([shim, "s3api", "get-object", "--bucket", bucket, "--key", key, "--version-id", version, str(tmp)], capture_output=True, text=True, timeout=300)
    if run.returncode != 0:
        raise Fail("get-object %s failed: %s" % (key, (run.stderr or run.stdout)[-160:]))
    return Path(tmp).read_bytes()


def load_record(root):
    p = Path(root, REC_REL)
    need(p.is_file(), "missing the applier's record " + REC_REL)
    return json.loads(p.read_text(encoding="utf-8"))


def packet_problems(root):
    p = Path(root, PACKET_REL)
    need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes are not the signed ones (sha256)")
    for rel, who in ((COO_REL, "COO"), (CTO_REL, "CTO")):
        t = Path(root, rel)
        txt = t.read_text(encoding="utf-8") if t.is_file() else ""
        need(PACKET_SHA in txt or PACKET_SHA[:8] in txt, "the %s half is missing or does not name the packet's sha256" % who)
        need("SIGNED" in txt, "the %s half is not SIGNED" % who)


def ac1(root):
    packet_problems(root)
    pr = head_problems(load_record(root))
    need(not pr, "; ".join(pr))


def acts_of(stmt):
    a = stmt["Action"]
    return [a] if isinstance(a, str) else list(a)


def role_world_problems(root):
    """Fresh reads: the runner role (13 + exactly one assume policy) and the new role (trust, one inline policy with the four statements)."""
    pr = []
    names = aws_json(root, ["iam", "list-role-policies", "--role-name", ROLE])["PolicyNames"]
    new = [n for n in names if n not in OTHER_POLICIES]
    if sorted(n for n in names if n in OTHER_POLICIES) != sorted(OTHER_POLICIES) or len(new) != 1:
        pr.append("the runner role must hold its 13 original inline policies and exactly ONE new one (found %d new)" % len(new))
    else:
        doc = aws_json(root, ["iam", "get-role-policy", "--role-name", ROLE, "--policy-name", new[0]])["PolicyDocument"]["Statement"]
        doc = doc if isinstance(doc, list) else [doc]
        if len(doc) != 1 or doc[0].get("Sid") != ASSUME_SID or acts_of(doc[0]) != ["sts:AssumeRole"] or "*" in json.dumps(doc[0].get("Resource")) \
                or not json.dumps(doc[0].get("Resource")).endswith(":role/%s\"" % NEW_ROLE):
            pr.append("the runner's new policy must be ONE statement %s: sts:AssumeRole on the new role's ARN only" % ASSUME_SID)
    role = aws_json(root, ["iam", "get-role", "--role-name", NEW_ROLE])["Role"]
    trust = role["AssumeRolePolicyDocument"]["Statement"]
    trust = trust if isinstance(trust, list) else [trust]
    runner_arn = aws_json(root, ["iam", "get-role", "--role-name", ROLE])["Role"]["Arn"]
    ok = len(trust) == 1 and trust[0].get("Effect") == "Allow" and trust[0].get("Principal") == {"AWS": runner_arn} and trust[0].get("Action") == "sts:AssumeRole" \
        and trust[0].get("Condition") == {"StringEquals": {"sts:RoleSessionName": SESSION_NAME}}
    if not ok:
        pr.append("the new role's trust must be the runner role only, sts:AssumeRole, conditioned on the session name %s" % SESSION_NAME)
    inl = aws_json(root, ["iam", "list-role-policies", "--role-name", NEW_ROLE])["PolicyNames"]
    if len(inl) != 1:
        pr.append("the new role must hold exactly ONE inline policy (found %d)" % len(inl))
    else:
        by = {x["Sid"]: x for x in aws_json(root, ["iam", "get-role-policy", "--role-name", NEW_ROLE, "--policy-name", inl[0]])["PolicyDocument"]["Statement"]}
        if sorted(by) != sorted(SIDS):
            pr.append("the new role's policy must carry exactly the four sids")
        else:
            if [acts_of(by[k]) for k in SIDS] != [["s3:GetObject"], ["s3:ListBucket"], ["s3:PutObject"], ["s3:ListBucket"]]:
                pr.append("the four statements' actions must be GetObject, ListBucket, PutObject, ListBucket")
            for sid in (SIDS[1], SIDS[3]):
                if "s3:prefix" not in json.dumps(by[sid].get("Condition", {})):
                    pr.append("%s must be conditioned on s3:prefix" % sid)
    if aws_json(root, ["iam", "list-attached-role-policies", "--role-name", NEW_ROLE])["AttachedPolicies"]:
        pr.append("the new role must hold no attached policy")
    return pr


def ac2(root):
    import tempfile
    rec = load_record(root)
    pr = []
    pr += role_world_problems(root)
    up = rec["uploads"]
    with tempfile.TemporaryDirectory() as td:
        for name in ("launcher", "zip", "receipt", "dispatch"):
            u = up.get(name) if isinstance(up, dict) else None
            if not (isinstance(u, dict) and u.get("key") == KEYS[name] and u.get("version_id") and u.get("sha256")):
                pr.append("uploads.%s must record key, version_id and sha256" % name)
                continue
            vers = aws_json(root, ["s3api", "list-object-versions", "--bucket", CODE_BUCKET, "--prefix", KEYS[name], "--max-items", "5"])
            ids = {v["VersionId"]: v for v in vers.get("Versions", []) if v["Key"] == KEYS[name]}
            if u["version_id"] not in ids or not ids[u["version_id"]].get("IsLatest"):
                pr.append("%s: the recorded version is not the current one" % name)
                continue
            blob = aws_download(root, CODE_BUCKET, KEYS[name], u["version_id"], Path(td, name))
            h = hashlib.sha256(blob).hexdigest()
            if h != u["sha256"]:
                pr.append("%s: the object's sha256 is not the recorded one" % name)
            if name == "dispatch":
                if not h.startswith(DISPATCH_SHA12):
                    pr.append("the dispatch object must be the packet's pinned script (%s)" % DISPATCH_SHA12)
                if PRIOR_DISPATCH_VERSION not in ids:
                    pr.append("the prior dispatch version %s must still be present (the rollback target)" % PRIOR_DISPATCH_VERSION)
            if name == "receipt":
                r = json.loads(blob.decode("utf-8"))
                if r.get("bundle_sha256") != up["zip"]["sha256"] or len(r.get("shared_pins", {})) != 14:
                    pr.append("the receipt's bundle_sha256 must equal the zip's sha256 and it must pin the 14 shared members")
    st = aws_json(root, ["ec2", "describe-instances", "--instance-ids", INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
    if st != "stopped":
        pr.append("the runner must be stopped at the end (found %s)" % st)
    need(not pr, "; ".join(pr[:6]))


def ac3(root):
    rec = load_record(root)
    pr = events_problems(rec)
    if not pr:
        fw = rec["first_write"]
        r = aws_json(root, ["s3api", "list-objects-v2", "--bucket", GOLD_BUCKET, "--prefix", GOLD_PREFIX, "--delimiter", "/"]) or {}
        parts = sorted(c["Prefix"][len(GOLD_PREFIX):].strip("/").replace("date=", "") for c in r.get("CommonPrefixes", []))
        if parts != sorted(fw["days"]):
            pr.append("the target prefix holds %d partitions, the record names %d days (they must be the same days)" % (len(parts), len(fw["days"])))
        else:
            for d in parts:
                objs = aws_json(root, ["s3api", "list-objects-v2", "--bucket", GOLD_BUCKET, "--prefix", "%sdate=%s/" % (GOLD_PREFIX, d)]) or {}
                keys = sorted(o["Key"].rsplit("/", 1)[-1] for o in objs.get("Contents", []))
                if keys != ["data.parquet", "manifest.json"]:
                    pr.append("partition %s must hold exactly data.parquet and manifest.json (found %r)" % (d, keys))
                    break
    need(not pr, "; ".join(pr[:6]))


def selftest():
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    rec = {"claim": "measured", "applier": APPLIER, "ledger_entry": "x", "ledger_closed": False, "reads": {},
           "gates": {"packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pins_ok": True, "monday_49f_read_passed": True,
                     "one_change_at_a_time": {"worktrees_read": 90, "open_markers_naming_this_surface": 0}},
           "role_audit": {"new_role_absent_before": True, "inline_policies": list(OTHER_POLICIES)},
           "before": {}, "apply_finished_utc": "2026-10-20T13:00:00Z", "uploads": {}, "runner": {},
           "plan": {"add": 3, "change": 0, "destroy": 0, "addresses": list(NEW_ADDRESSES), "statement_sids": list(SIDS), "replan_no_changes": True, "naming_gate_refuse": 0},
           "simulation": {"lines": [{"decision": dec, "label": lab, "with_resource_policy": lab in SIM_WITH_RESOURCE_POLICY} for dec, lab in SIM_REQUIRED]},
           "dry_run": {"assumed": {"role": NEW_ROLE, "session": SESSION_NAME}, "s6": {"events": 96, "with_equal_amount_line": 96, "missing": 0}, "target_objects_after": 0, "repeated_source_lines": 0, "window": {"newest_written": None}},
           "first_write": {"assumed": {"role": NEW_ROLE, "session": SESSION_NAME}, "days_written": 2, "days": ["2026-10-15", "2026-10-16"], "columns": 19, "schema_hash": SCHEMA_HASH, "claims_ok": True, "repeated_source_lines": 0,
                           "since": "2026-10-15", "run_day": "2026-10-16"}}
    arm("head-green", head_problems(rec), [])
    arm("events-green", events_problems(rec), [])
    arm("plan-two-changes", len(head_problems(dict(rec, plan=dict(rec["plan"], change=1)))), 1)
    arm("audit-new-role-present-before", len(head_problems(dict(rec, role_audit=dict(rec["role_audit"], new_role_absent_before=False)))), 1)
    arm("plan-one-add", len(head_problems(dict(rec, plan=dict(rec["plan"], add=1)))), 1)
    nores = [dict(x, with_resource_policy=False) for x in rec["simulation"]["lines"]]
    arm("sim-without-resource-policy", len(head_problems(dict(rec, simulation={"lines": nores}))), 1)
    arm("write-no-assumed-role", len(events_problems(dict(rec, dry_run=dict(rec["dry_run"], assumed={"role": ROLE, "session": SESSION_NAME})))), 1)
    arm("sim-missing-line", len(head_problems(dict(rec, simulation={"lines": rec["simulation"]["lines"][:-1]}))), 1)
    arm("gate-monday-not-passed", len(head_problems(dict(rec, gates=dict(rec["gates"], monday_49f_read_passed=False)))), 1)
    arm("ledger-closed", len(head_problems(dict(rec, ledger_closed=True))), 1)
    arm("s6-missing", len(events_problems(dict(rec, dry_run=dict(rec["dry_run"], s6={"events": 96, "with_equal_amount_line": 95, "missing": 1})))), 1)
    arm("dry-run-wrote", len(events_problems(dict(rec, dry_run=dict(rec["dry_run"], target_objects_after=3)))), 1)
    arm("write-too-many-days", len(events_problems(dict(rec, first_write=dict(rec["first_write"], days_written=26, days=["d"] * 26)))), 1)
    arm("write-before-since", len(events_problems(dict(rec, first_write=dict(rec["first_write"], days=["2026-10-14", "2026-10-16"])))), 1)
    arm("write-bad-hash", len(events_problems(dict(rec, first_write=dict(rec["first_write"], schema_hash="0" * 64)))), 1)
    arm("sim-decisions", sim_decision_ok(rec["simulation"]["lines"]), True)
    arm("keys", sorted(KEYS), ["dispatch", "launcher", "receipt", "zip"])
    arm("sim-labels-unique", len({lab for _d, lab in SIM_REQUIRED}), len(SIM_REQUIRED))
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF139-2-AC1", "DBF139-2-AC2", "DBF139-2-AC3"):
        print("usage: p139_infapply.py <repo_root> DBF139-2-AC1|AC2|AC3 | --selftest")
        return 2
    try:
        {"DBF139-2-AC1": ac1, "DBF139-2-AC2": ac2, "DBF139-2-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
