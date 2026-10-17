"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the APPLY of the signed Inflection transaction pair by 0.7.0_AE_CloudOps~IB2 (cell DB-f-2702).

  Packet NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md REVISION 1 (sha256 below), COO half signed @d5ebef57c2, CTO half signed @028ec74371. The applier's record is
  deliverables/0.7.0_AE_CloudOps~IB2/INFLECTION_RELEASE_RECORD.json. The criteria grade the record and then re-read the world FRESH (AWS GET, list and describe only).

  DBF139-2-AC1  gates, ledger, role audit (only the runner's instance profile assumes the role), the plan (exactly 1 add / 0 change / 0 destroy, the one resource, the four sids) and the
                simulation lines (every ALLOW and DENY the packet names) as the packet states them
  DBF139-2-AC2  fresh reads: the role holds the new inline policy with its four statements and its 13 other policies unchanged; the three new code objects and the new dispatch version exist
                with the recorded VersionIds and hashes, the prior dispatch version is still present, the receipt's bundle_sha256 equals the zip's, the runner is stopped
  DBF139-2-AC3  the dry run (S6 N of N, nothing written), the bounded first write (at most 25 days, 19 columns, the schema hash, valid claims, no repeated source line) and a fresh LIST of
                the target prefix equal to the recorded days, each partition with its data.parquet and manifest.json

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
PACKET_SHA = "ad67beeb8c5ce93838ce4b763c07d359d709758a454d7ca4c9807eba653cf215"
ROLE = "inf-gold-layer-ec2-role"
NEW_POLICY_RESOURCE = "aws_iam_role_policy.inf_gold_layer_account_transaction"
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
SIM_REQUIRED = [("allowed", "silver GetObject"), ("allowed", "silver ListBucket"), ("allowed", "gold PutObject"), ("allowed", "gold ListBucket on the gold prefix"),
                ("denied", "gold ListBucket on another prefix"), ("denied", "gold GetObject"), ("denied", "other firm gold PutObject"), ("denied", "other firm silver GetObject")]


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
    if not (isinstance(a, dict) and a.get("only_runner_instance_profile_assumes") is True and isinstance(a.get("inline_policies"), list) and sorted(a["inline_policies"]) == sorted(OTHER_POLICIES)):
        pr.append("role_audit must show the 13 inline policies and that ONLY the runner's instance profile can assume the role (anything else STOPS the pair)")
    p = rec["plan"]
    if not (isinstance(p, dict) and p.get("add") == 1 and p.get("change") == 0 and p.get("destroy") == 0 and p.get("addresses") == [NEW_POLICY_RESOURCE]
            and sorted(p.get("statement_sids", [])) == sorted(SIDS) and p.get("replan_no_changes") is True and p.get("naming_gate_refuse") == 0):
        pr.append("plan must read exactly 1 add / 0 change / 0 destroy, the one address %s, the four sids, a re-plan of No changes and 0 naming REFUSE" % NEW_POLICY_RESOURCE)
    sim = rec["simulation"]
    lines = sim.get("lines") if isinstance(sim, dict) else None
    if not isinstance(lines, list):
        pr.append("simulation must carry its lines")
    else:
        got = sorted((x.get("decision"), x.get("label")) for x in lines if isinstance(x, dict))
        if got != sorted(SIM_REQUIRED):
            pr.append("the simulation lines must be exactly the packet's Act 3 lines: %r" % (SIM_REQUIRED,))
    if rec["ledger_closed"] is not False:
        pr.append("the ledger stays open (ledger_closed false) until the CVO's sample")
    return pr


def events_problems(rec):
    pr = []
    dr, fw = rec["dry_run"], rec["first_write"]
    s6 = dr.get("s6") if isinstance(dr, dict) else None
    if not (isinstance(s6, dict) and is_int(s6.get("events")) and s6["events"] > 0 and s6.get("with_equal_amount_line") == s6["events"] and s6.get("missing") == 0):
        pr.append("the dry run's S6 must read N of N events with an equal-amount line, 0 missing, N printed")
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


def ac2(root):
    import tempfile
    rec = load_record(root)
    pr = []
    names = aws_json(root, ["iam", "list-role-policies", "--role-name", ROLE])["PolicyNames"]
    new = [n for n in names if n not in OTHER_POLICIES]
    if sorted(n for n in names if n in OTHER_POLICIES) != sorted(OTHER_POLICIES) or len(new) != 1:
        pr.append("the role must hold its 13 original inline policies and exactly ONE new one (found %d new)" % len(new))
    else:
        doc = aws_json(root, ["iam", "get-role-policy", "--role-name", ROLE, "--policy-name", new[0]])["PolicyDocument"]["Statement"]
        by = {s["Sid"]: s for s in doc}
        if sorted(by) != sorted(SIDS):
            pr.append("the new policy must carry exactly the four sids")
        else:
            def acts(s):
                a = s["Action"]
                return [a] if isinstance(a, str) else list(a)
            if acts(by[SIDS[0]]) != ["s3:GetObject"] or acts(by[SIDS[1]]) != ["s3:ListBucket"] or acts(by[SIDS[2]]) != ["s3:PutObject"] or acts(by[SIDS[3]]) != ["s3:ListBucket"]:
                pr.append("the four statements' actions must be GetObject, ListBucket, PutObject, ListBucket")
            for sid in (SIDS[1], SIDS[3]):
                if "s3:prefix" not in json.dumps(by[sid].get("Condition", {})):
                    pr.append("%s must be conditioned on s3:prefix" % sid)
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
           "role_audit": {"only_runner_instance_profile_assumes": True, "inline_policies": list(OTHER_POLICIES)},
           "before": {}, "apply_finished_utc": "2026-10-20T13:00:00Z", "uploads": {}, "runner": {},
           "plan": {"add": 1, "change": 0, "destroy": 0, "addresses": [NEW_POLICY_RESOURCE], "statement_sids": list(SIDS), "replan_no_changes": True, "naming_gate_refuse": 0},
           "simulation": {"lines": [{"decision": dec, "label": lab} for dec, lab in SIM_REQUIRED]},
           "dry_run": {"s6": {"events": 96, "with_equal_amount_line": 96, "missing": 0}, "target_objects_after": 0, "repeated_source_lines": 0, "window": {"newest_written": None}},
           "first_write": {"days_written": 2, "days": ["2026-10-15", "2026-10-16"], "columns": 19, "schema_hash": SCHEMA_HASH, "claims_ok": True, "repeated_source_lines": 0,
                           "since": "2026-10-15", "run_day": "2026-10-16"}}
    arm("head-green", head_problems(rec), [])
    arm("events-green", events_problems(rec), [])
    arm("plan-two-changes", len(head_problems(dict(rec, plan=dict(rec["plan"], change=1)))), 1)
    arm("audit-other-principal", len(head_problems(dict(rec, role_audit=dict(rec["role_audit"], only_runner_instance_profile_assumes=False)))), 1)
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
