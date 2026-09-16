#!/usr/bin/env python3
"""og_i1.py -- the acceptance probe for NFRA_OPLGTW.TO-OG-i-1 (cell OG-i-1).

Usage:  og_i1.py AC<n>      n = 1..12

Each arm prints its measurement with its vintage (the UTC time of a live read, or the source's own timestamp) and its
denominator, then exactly one final line:  VERDICT: PASS-OGI1-AC<n>  or  VERDICT: FAIL-OGI1-AC<n> <reason>.

Arms and instruments:
  AC1  the saved plan og_i1.plan.json (redacted from `terraform show -json` of the saved planfile) -- a file. The only
       admitted changes to existing resources are the two WAF description backfills (ruling 97237; AC10 grades them).
  AC2  git: the commit that ADDED the ledger sentinel, against evidence/apply.json (the safe-apply run's recorded
       start), corroborated by the AWS-side creation times of the table and the operator role.
  AC3  git: the commit that DELETED the sentinel (the ledger close) with the entry reading CLOSED at that commit,
       against evidence/first_readback.json (written ONCE, by the first live read that finds the table).
  AC4  live: dynamodb describe-table, describe-continuous-backups, describe-time-to-live.
  AC5  live: the runtime policy document on opal-gateway-role, every other policy on that role, and
       iam simulate-principal-policy with dynamodb:LeadingKeys context.
  AC6  live: the operator role's trust and policy, a simulation of the Gateway role assuming it, and an exercised
       operator transaction (conditional POLICY update + operator_audit append) with a DeleteItem refusal.
  AC7  live, on the Gateway host through SSM with the instance's own role: a POLICY# write against a RUNTIME# write.
  AC8  live, operator role assumed from this checkout: two concurrent conditional revisions of one POLICY# record.
  AC9  live: a POLICY# probe record written by the operator path, strongly read back, against the live TTL name.
  AC10 the saved plan og_i1.plan.json: the changes outside this cell are exactly the two admitted WAF updates,
       description only, addresses absent from the diff; the in-apply plan the approval guard judged is printed beside.
  AC11 evidence/waf_pre.json + evidence/waf_post.json (get-ip-set immediately before/after the apply, written by
       og_i1_act.py: counts and sha256 of the sorted list, never the addresses) against evidence/apply.json's start
       and end, and the ledger entry at its close commit carrying both reads.
  AC12 a FRESH `terraform plan` of the root run by this arm (-lock=false, read-only), graded on the two WAF sets and
       this cell's four resources; its redacted summary is written to evidence/postplan.json.

Writes: only isolated RUNTIME#probe-og-i1-<utc> and POLICY#probe-og-i1-<utc> items, and only once the table exists.
DynamoDB has no TransactWriteItems IAM action: a transaction is authorized per item against PutItem / UpdateItem, so
"TransactWrite" is graded on those constituents carrying the LeadingKeys condition (row NFRA_OPLGTW-W1-S3).
Standard library + boto3. ASCII only.
"""
from __future__ import annotations

import datetime
import glob
import json
import os
import shlex
import subprocess
import sys
import threading
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
REPO = _top.stdout.strip() or os.path.abspath(os.path.join(DELIV, *[".."] * 6))

REGION = "us-east-1"
ACCOUNT = "313476888478"
TABLE = "opal-gateway-access-state"
TABLE_ARN = "arn:aws:dynamodb:%s:%s:table/%s" % (REGION, ACCOUNT, TABLE)
RUNTIME_ROLE = "opal-gateway-role"
RUNTIME_ROLE_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, RUNTIME_ROLE)
RUNTIME_POLICY = "opal-gateway-access-state-runtime"
ADMIN_ROLE = "opal-gateway-access-admin"
ADMIN_POLICY = "opal-gateway-access-admin-policy"
TTL_ATTR = "expires_at"
INSTANCE = "i-07dccb1615503ac99"
PLAN = os.path.join(DELIV, "og_i1.plan.json")
EVID = os.path.join(DELIV, "evidence")
APPLY_REC = os.path.join(EVID, "apply.json")
FIRST_READ = os.path.join(EVID, "first_readback.json")
SENTINEL = "org/critical_paths/.open_deploys/nfra-oplgtw-og-i-1-access-state.json"
ENTRY_GLOB = "org/critical_paths/change_management/*_nfra-oplgtw-og-i-1-access-state_deploy_completion.md"
EXPECTED_CREATES = {
    "aws_dynamodb_table.access_state",
    "aws_iam_role_policy.gw_access_state_runtime",
    "aws_iam_role.access_admin",
    "aws_iam_role_policy.access_admin_policy",
}
ADMITTED_UPDATES = {  # ruling 97237: the two WAF description backfills, admitted by name
    "aws_wafv2_ip_set.opal_blocked_ips_regional_v4",
    "aws_wafv2_ip_set.opal_blocked_ips_regional_v6",
}
WAF_PRE = os.path.join(EVID, "waf_pre.json")
WAF_POST = os.path.join(EVID, "waf_post.json")
POSTPLAN = os.path.join(EVID, "postplan.json")
TF = os.path.join(REPO, ".tools", "terraform.exe")
TF_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "opal-gateway")
WRITE_ACTIONS = {"putitem", "updateitem", "deleteitem", "batchwriteitem", "partiqlinsert", "partiqlupdate",
                 "partiqldelete", "conditioncheckitem"}
ADMIN_ACTIONS = {"createtable", "deletetable", "updatetable", "updatetimetolive", "updatecontinuousbackups",
                 "createbackup", "deletebackup", "restoretablefrombackup", "restoretabletopointintime",
                 "tagresource", "untagresource", "createglobaltable", "updateglobaltable", "putresourcepolicy",
                 "deleteresourcepolicy", "exporttabletopointintime", "importtable", "updatetablereplicaautoscaling",
                 "enablekinesisstreamingdestination", "disablekinesisstreamingdestination",
                 "updatekinesisstreamingdestination", "updatecontributorinsights"}


# --------------------------------------------------------------------------- helpers
def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t: datetime.datetime) -> str:
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def stamp() -> str:
    return now().strftime("%Y%m%dT%H%M%S%fZ")


def parse_ts(s: str) -> datetime.datetime:
    s = s.strip().replace("Z", "+00:00")
    t = datetime.datetime.fromisoformat(s)
    if t.tzinfo is None:
        t = t.replace(tzinfo=datetime.timezone.utc)
    return t.astimezone(datetime.timezone.utc)


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace("\\", "/")


def verdict(n: int, ok: bool, reason: str = "") -> int:
    print("VERDICT: PASS-OGI1-AC%d" % n if ok else "VERDICT: FAIL-OGI1-AC%d %s" % (n, reason))
    return 0 if ok else 1


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("git %s rc=%d: %s" % (" ".join(args), r.returncode, r.stderr.strip()))
    return r.stdout


def commits(path: str, flt: str) -> list:
    out = git("log", "--diff-filter=" + flt, "--format=%H %cI", "--", path)
    return [(h, parse_ts(t)) for h, t in (ln.split() for ln in out.splitlines() if ln.strip())]


def session():
    import boto3
    return boto3.Session(region_name=REGION)


def err_code(e) -> str:
    return getattr(e, "response", {}).get("Error", {}).get("Code", type(e).__name__)


def table_exists(ddb) -> bool:
    try:
        ddb.describe_table(TableName=TABLE)
        return True
    except Exception as e:  # noqa: BLE001 -- the code is printed and decides
        if err_code(e) == "ResourceNotFoundException":
            return False
        raise


def record_first_read(arm: str, t: datetime.datetime) -> None:
    """Write-once: the first live read that FINDS the table stamps its time; later reads never move it."""
    if os.path.isfile(FIRST_READ):
        return
    os.makedirs(EVID, exist_ok=True)
    with open(FIRST_READ, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"arm": arm, "read_utc": iso(t), "table": TABLE_ARN}, fh, indent=1)
        fh.write("\n")
    print("RECORDED first readback: %s at %s" % (rel(FIRST_READ), iso(t)))


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def statements(doc: dict) -> list:
    return as_list(doc.get("Statement"))


def action_names(st: dict) -> list:
    return [a.split(":", 1)[1].lower() if a.lower().startswith("dynamodb:") else a.lower()
            for a in as_list(st.get("Action"))]


def leading_keys_bound(st: dict, pattern: str) -> bool:
    c = st.get("Condition") or {}
    fav = c.get("ForAllValues:StringLike") or {}
    nul = c.get("Null") or {}
    return as_list(fav.get("dynamodb:LeadingKeys")) == [pattern] and str(nul.get("dynamodb:LeadingKeys")).lower() == "false"


def grade_policy(doc: dict, prefix: str, label: str) -> list:
    """Return (check, ok, detail) rows for one DynamoDB grant document."""
    rows = []
    sts = statements(doc)
    allows = [s for s in sts if s.get("Effect") == "Allow"]
    all_actions = [a for s in allows for a in action_names(s)]
    res_ok = all(as_list(s.get("Resource")) == [TABLE_ARN] for s in allows)
    rows.append(("%s every Allow Resource == [table ARN]" % label, res_ok,
                 [as_list(s.get("Resource")) for s in allows]))
    rows.append(("%s GetItem allowed" % label, "getitem" in all_actions, sorted(set(all_actions))))
    for w in ("putitem", "updateitem"):
        holders = [s for s in allows if w in action_names(s)]
        ok = bool(holders) and all(leading_keys_bound(s, prefix) for s in holders)
        rows.append(("%s %s allowed only under LeadingKeys %s" % (label, w, prefix), ok,
                     [s.get("Condition") for s in holders]))
    unbound = [a for s in allows for a in action_names(s) if a in WRITE_ACTIONS and not leading_keys_bound(s, prefix)]
    rows.append(("%s no write action outside the LeadingKeys condition (covers every transaction item)" % label,
                 not unbound, unbound))
    banned = sorted({a for a in all_actions if a in ADMIN_ACTIONS or a in ("deleteitem", "batchwriteitem")
                     or a.startswith("partiql") or a in ("*", "dynamodb:*") or a.endswith("*")})
    rows.append(("%s no DeleteItem / BatchWriteItem / PartiQL / table-admin / wildcard action" % label,
                 not banned, banned))
    return rows


def simulate(iam, source_arn: str, action: str, resource: str, lk: str | None) -> str:
    kw = {"PolicySourceArn": source_arn, "ActionNames": [action], "ResourceArns": [resource]}
    if lk is not None:
        kw["ContextEntries"] = [{"ContextKeyName": "dynamodb:LeadingKeys", "ContextKeyValues": [lk],
                                 "ContextKeyType": "stringList"}]
    r = iam.simulate_principal_policy(**kw)
    return r["EvaluationResults"][0]["EvalDecision"]


def print_rows(rows: list) -> bool:
    ok_all = True
    for name, ok, detail in rows:
        ok_all = ok_all and ok
        print("  %s %s -- %s" % ("OK  " if ok else "NOT ", name, json.dumps(detail, default=str, sort_keys=True)))
    return ok_all


def admin_clients(sess):
    arn = sess.client("iam").get_role(RoleName=ADMIN_ROLE)["Role"]["Arn"]
    c = sess.client("sts").assume_role(RoleArn=arn, RoleSessionName="og-i1-probe-%s" % stamp()[:15])["Credentials"]
    import boto3
    s2 = boto3.Session(aws_access_key_id=c["AccessKeyId"], aws_secret_access_key=c["SecretAccessKey"],
                       aws_session_token=c["SessionToken"], region_name=REGION)
    return s2, arn


def operator_seed(ddb, pk: str) -> None:
    """The operator path's shape: the POLICY record and its operator_audit item land in ONE transaction."""
    ddb.transact_write_items(TransactItems=[
        {"Put": {"TableName": TABLE, "ConditionExpression": "attribute_not_exists(pk)",
                 "Item": {"pk": {"S": pk}, "sk": {"S": "PROFILE"}, "record_type": {"S": "principal_profile"},
                          "status": {"S": "pending"}, "revision": {"N": "1"}, "probe": {"S": "og-i1"}}}},
        {"Put": {"TableName": TABLE, "ConditionExpression": "attribute_not_exists(pk)",
                 "Item": {"pk": {"S": pk}, "sk": {"S": "AUDIT#0001"}, "record_type": {"S": "operator_audit"},
                          "revision": {"N": "1"}, "probe": {"S": "og-i1"}}}},
    ])


# --------------------------------------------------------------------------- arms
def ac1() -> int:
    if not os.path.isfile(PLAN):
        print("MEASURED: plan file absent at %s" % rel(PLAN))
        return verdict(1, False, "plan file absent")
    with open(PLAN, encoding="utf-8") as fh:
        d = json.load(fh)
    rc = d["resource_changes"]
    print("SOURCE: %s -- terraform %s, plan timestamp %s, source show-json sha256 %s"
          % (rel(PLAN), d.get("terraform_version"), d.get("timestamp"), d.get("source_sha256")))
    counts = Counter("+".join(r["actions"]) for r in rc)
    print("DENOMINATOR: %d resource_changes; by action %s" % (len(rc), json.dumps(dict(sorted(counts.items())))))
    creates = {r["address"] for r in rc if r["actions"] == ["create"]}
    others = [r for r in rc if r["actions"] not in (["create"], ["no-op"])]
    for a in sorted(creates):
        print("  create      %s" % a)
    for r in others:
        print("  NOT-CREATE  %s %s changed=%s" % (r["address"], "+".join(r["actions"]),
                                                  json.dumps(sorted(r.get("changed_attributes", {})))))
    missing, extra = sorted(EXPECTED_CREATES - creates), sorted(creates - EXPECTED_CREATES)
    destroys = [r["address"] for r in rc if "delete" in r["actions"]]
    admitted = [r for r in others if r["address"] in ADMITTED_UPDATES and r["actions"] == ["update"]]
    unadmitted = [r for r in others if r not in admitted]
    print("EXPECTED creates present: %d of %d; missing %s; extra %s"
          % (len(EXPECTED_CREATES & creates), len(EXPECTED_CREATES), missing, extra))
    print("changes to existing resources: %d of %d resource_changes; admitted WAF updates %d of %d; unadmitted %d; "
          "destroys %d" % (len(others), len(rc), len(admitted), len(ADMITTED_UPDATES), len(unadmitted), len(destroys)))
    if missing or extra:
        return verdict(1, False, "create set differs: missing %s extra %s" % (missing, extra))
    if destroys:
        return verdict(1, False, "destroy in plan: %s" % destroys)
    if unadmitted:
        return verdict(1, False, "%d unadmitted change(s) to existing resources: %s"
                       % (len(unadmitted), ", ".join("%s %s" % (r["address"], "+".join(r["actions"]))
                                                     for r in unadmitted)))
    return verdict(1, True)


def ac2() -> int:
    added = commits(SENTINEL, "A")
    print("MEASURED %s: commits that ADD %s: %d %s" % (iso(now()), SENTINEL, len(added),
                                                        [(h[:10], iso(t)) for h, t in added]))
    if not added:
        return verdict(2, False, "no commit adds the ledger sentinel -- no ledger entry was opened, so no apply ran")
    t_open = min(t for _, t in added)
    if not os.path.isfile(APPLY_REC):
        print("MEASURED: apply record absent at %s" % rel(APPLY_REC))
        return verdict(2, False, "no apply record")
    with open(APPLY_REC, encoding="utf-8") as fh:
        rec = json.load(fh)
    t_start = parse_ts(rec["start_utc"])
    print("APPLY RECORD %s: start %s rc %s command %s" % (rel(APPLY_REC), iso(t_start), rec.get("rc"), rec.get("command")))
    sess = session()
    t_tab = sess.client("dynamodb").describe_table(TableName=TABLE)["Table"]["CreationDateTime"]
    t_role = sess.client("iam").get_role(RoleName=ADMIN_ROLE)["Role"]["CreateDate"]
    print("AWS-SIDE: table CreationDateTime %s; operator role CreateDate %s" % (iso(t_tab), iso(t_role)))
    rows = [
        ("apply ran through safe-apply", "safe-apply.sh" in str(rec.get("command")), rec.get("command")),
        ("apply rc 0", rec.get("rc") == 0, rec.get("rc")),
        ("sentinel commit precedes the recorded apply start", t_open < t_start,
         "%s < %s" % (iso(t_open), iso(t_start))),
        ("sentinel commit precedes the AWS-side creation of both objects", t_open < t_tab and t_open < t_role,
         "%s < %s, %s" % (iso(t_open), iso(t_tab), iso(t_role))),
    ]
    print("DENOMINATOR: %d checks" % len(rows))
    ok = print_rows(rows)
    return verdict(2, ok, "" if ok else "a sequencing check failed (see NOT lines)")


def ac3() -> int:
    deleted = commits(SENTINEL, "D")
    print("MEASURED %s: commits that DELETE %s (the ledger close): %d %s"
          % (iso(now()), SENTINEL, len(deleted), [(h[:10], iso(t)) for h, t in deleted]))
    if not deleted:
        return verdict(3, False, "no commit deletes the ledger sentinel -- the ledger was never closed and committed")
    h_close, t_close = min(deleted, key=lambda x: x[1])
    entries = sorted(glob.glob(os.path.join(REPO, ENTRY_GLOB)))
    closed = False
    for e in entries:
        try:
            closed = closed or "CLOSED" in git("show", "%s:%s" % (h_close, rel(e)))
        except RuntimeError:
            pass
    print("ENTRY at close commit %s reads CLOSED: %s (entries found: %s)" % (h_close[:10], closed,
                                                                             [rel(e) for e in entries]))
    if not os.path.isfile(FIRST_READ):
        return verdict(3, False, "no first readback recorded")
    with open(FIRST_READ, encoding="utf-8") as fh:
        fr = json.load(fh)
    t_read = parse_ts(fr["read_utc"])
    print("FIRST READBACK %s: arm %s at %s" % (rel(FIRST_READ), fr.get("arm"), iso(t_read)))
    rows = [("entry reads CLOSED at the close commit", closed, h_close[:10]),
            ("close commit precedes the first readback", t_close < t_read, "%s < %s" % (iso(t_close), iso(t_read)))]
    print("DENOMINATOR: %d checks" % len(rows))
    ok = print_rows(rows)
    return verdict(3, ok, "" if ok else "a sequencing check failed (see NOT lines)")


def ac4() -> int:
    ddb = session().client("dynamodb")
    t0 = now()
    try:
        d = ddb.describe_table(TableName=TABLE)["Table"]
    except Exception as e:  # noqa: BLE001
        print("MEASURED %s: describe-table %s -> %s" % (iso(t0), TABLE, err_code(e)))
        return verdict(4, False, "table absent: %s" % err_code(e))
    record_first_read("AC4", t0)
    pitr = ddb.describe_continuous_backups(TableName=TABLE)["ContinuousBackupsDescription"]
    pitr_s = (pitr.get("PointInTimeRecoveryDescription") or {}).get("PointInTimeRecoveryStatus")
    ttl = ddb.describe_time_to_live(TableName=TABLE)["TimeToLiveDescription"]
    ks = ",".join("%s:%s" % (k["AttributeName"], k["KeyType"]) for k in d["KeySchema"])
    ad = ",".join(sorted("%s:%s" % (a["AttributeName"], a["AttributeType"]) for a in d["AttributeDefinitions"]))
    print("MEASURED %s: %s status %s" % (iso(t0), d["TableArn"], d.get("TableStatus")))
    rows = [
        ("SSEDescription.Status == ENABLED", (d.get("SSEDescription") or {}).get("Status") == "ENABLED",
         d.get("SSEDescription")),
        ("PointInTimeRecoveryStatus == ENABLED", pitr_s == "ENABLED", pitr_s),
        ("BillingMode == PAY_PER_REQUEST", (d.get("BillingModeSummary") or {}).get("BillingMode") == "PAY_PER_REQUEST",
         d.get("BillingModeSummary")),
        ("TTL attribute set: %s ENABLED|ENABLING" % TTL_ATTR,
         ttl.get("AttributeName") == TTL_ATTR and ttl.get("TimeToLiveStatus") in ("ENABLED", "ENABLING"), ttl),
        ("KeySchema == pk:HASH,sk:RANGE", ks == "pk:HASH,sk:RANGE", ks),
        ("AttributeDefinitions == pk:S,sk:S", ad == "pk:S,sk:S", ad),
    ]
    print("DENOMINATOR: %d properties" % len(rows))
    ok = print_rows(rows)
    return verdict(4, ok, "" if ok else "a table property differs (see NOT lines)")


def ac5() -> int:
    sess = session()
    iam = sess.client("iam")
    t0 = now()
    try:
        doc = iam.get_role_policy(RoleName=RUNTIME_ROLE, PolicyName=RUNTIME_POLICY)["PolicyDocument"]
    except Exception as e:  # noqa: BLE001
        print("MEASURED %s: get-role-policy %s/%s -> %s" % (iso(t0), RUNTIME_ROLE, RUNTIME_POLICY, err_code(e)))
        return verdict(5, False, "runtime grant absent: %s" % err_code(e))
    print("MEASURED %s: %s/%s = %s" % (iso(t0), RUNTIME_ROLE, RUNTIME_POLICY, json.dumps(doc, sort_keys=True)))
    rows = grade_policy(doc, "RUNTIME#*", "runtime")
    inline = iam.list_role_policies(RoleName=RUNTIME_ROLE)["PolicyNames"]
    attached = iam.list_attached_role_policies(RoleName=RUNTIME_ROLE)["AttachedPolicies"]
    other_ddb = []
    for p in inline:
        if p == RUNTIME_POLICY:
            continue
        d2 = iam.get_role_policy(RoleName=RUNTIME_ROLE, PolicyName=p)["PolicyDocument"]
        if "dynamodb" in json.dumps(d2).lower() or '"*"' in json.dumps(as_list(d2.get("Statement"))):
            other_ddb.append(p)
    for a in attached:
        pol = iam.get_policy(PolicyArn=a["PolicyArn"])["Policy"]
        d2 = iam.get_policy_version(PolicyArn=a["PolicyArn"], VersionId=pol["DefaultVersionId"])["PolicyVersion"]["Document"]
        if "dynamodb" in json.dumps(d2).lower():
            other_ddb.append(a["PolicyArn"])
    rows.append(("no OTHER policy on %s mentions dynamodb (%d inline + %d attached read)"
                 % (RUNTIME_ROLE, len(inline), len(attached)), not other_ddb, other_ddb))
    sims = [("dynamodb:GetItem", "POLICY#probe-og-i1-sim", "allowed"),
            ("dynamodb:PutItem", "RUNTIME#probe-og-i1-sim", "allowed"),
            ("dynamodb:PutItem", "POLICY#probe-og-i1-sim", "implicitDeny"),
            ("dynamodb:UpdateItem", "RUNTIME#probe-og-i1-sim", "allowed"),
            ("dynamodb:UpdateItem", "POLICY#probe-og-i1-sim", "implicitDeny"),
            ("dynamodb:DeleteItem", "RUNTIME#probe-og-i1-sim", "implicitDeny"),
            ("dynamodb:DeleteTable", None, "implicitDeny"),
            ("dynamodb:UpdateTable", None, "implicitDeny")]
    for act, lk, want in sims:
        got = simulate(iam, RUNTIME_ROLE_ARN, act, TABLE_ARN, lk)
        rows.append(("simulate %s LeadingKeys=%s -> %s" % (act, lk, want), got == want, got))
    print("TransactWrite: no IAM action exists (row NFRA_OPLGTW-W1-S3); transaction items are authorized against "
          "PutItem/UpdateItem, graded by the LeadingKeys rows below")
    print("DENOMINATOR: %d checks" % len(rows))
    ok = print_rows(rows)
    return verdict(5, ok, "" if ok else "a runtime-grant check failed (see NOT lines)")


def ac6() -> int:
    sess = session()
    iam = sess.client("iam")
    t0 = now()
    try:
        role = iam.get_role(RoleName=ADMIN_ROLE)["Role"]
        doc = iam.get_role_policy(RoleName=ADMIN_ROLE, PolicyName=ADMIN_POLICY)["PolicyDocument"]
    except Exception as e:  # noqa: BLE001
        print("MEASURED %s: get-role/get-role-policy %s -> %s" % (iso(t0), ADMIN_ROLE, err_code(e)))
        return verdict(6, False, "operator role absent: %s" % err_code(e))
    trust = role["AssumeRolePolicyDocument"]
    print("MEASURED %s: operator role %s trust %s" % (iso(t0), role["Arn"], json.dumps(trust, sort_keys=True)))
    print("MEASURED %s: %s/%s = %s" % (iso(t0), ADMIN_ROLE, ADMIN_POLICY, json.dumps(doc, sort_keys=True)))
    principals = json.dumps([s.get("Principal") for s in statements(trust)])
    excl = json.dumps([s.get("Condition") for s in statements(trust)])
    rows = [("operator role ARN differs from the runtime role ARN", role["Arn"] != RUNTIME_ROLE_ARN, role["Arn"]),
            ("trust names no Gateway role principal", RUNTIME_ROLE_ARN not in principals, principals),
            ("trust refuses the Gateway role by aws:PrincipalArn", "ArnNotEquals" in excl and RUNTIME_ROLE_ARN in excl,
             excl),
            ("simulate %s sts:AssumeRole on the operator role -> implicitDeny" % RUNTIME_ROLE,
             simulate(iam, RUNTIME_ROLE_ARN, "sts:AssumeRole", role["Arn"], None) == "implicitDeny", None)]
    rows += grade_policy(doc, "POLICY#*", "operator")
    for act, lk, want in [("dynamodb:PutItem", "POLICY#probe-og-i1-sim", "allowed"),
                          ("dynamodb:UpdateItem", "POLICY#probe-og-i1-sim", "allowed"),
                          ("dynamodb:PutItem", "RUNTIME#probe-og-i1-sim", "implicitDeny"),
                          ("dynamodb:DeleteItem", "POLICY#probe-og-i1-sim", "implicitDeny"),
                          ("dynamodb:UpdateTable", None, "implicitDeny")]:
        got = simulate(iam, role["Arn"], act, TABLE_ARN, lk)
        rows.append(("simulate operator %s LeadingKeys=%s -> %s" % (act, lk, want), got == want, got))
    ddb_admin = None
    if table_exists(sess.client("dynamodb")):
        record_first_read("AC6", t0)
        s2, _ = admin_clients(sess)
        ddb_admin = s2.client("dynamodb")
        pk = "POLICY#probe-og-i1-%s" % stamp()
        print("EXERCISE %s: operator transactions on %s" % (iso(now()), pk))
        try:
            operator_seed(ddb_admin, pk)
            ddb_admin.transact_write_items(TransactItems=[
                {"Update": {"TableName": TABLE, "Key": {"pk": {"S": pk}, "sk": {"S": "PROFILE"}},
                            "UpdateExpression": "SET revision = :n, #s = :st",
                            "ConditionExpression": "revision = :e",
                            "ExpressionAttributeNames": {"#s": "status"},
                            "ExpressionAttributeValues": {":n": {"N": "2"}, ":e": {"N": "1"}, ":st": {"S": "revoked"}}}},
                {"Put": {"TableName": TABLE, "ConditionExpression": "attribute_not_exists(pk)",
                         "Item": {"pk": {"S": pk}, "sk": {"S": "AUDIT#0002"}, "record_type": {"S": "operator_audit"},
                                  "revision": {"N": "2"}, "probe": {"S": "og-i1"}}}},
            ])
            tx = "SUCCESS"
        except Exception as e:  # noqa: BLE001
            tx = err_code(e)
        rows.append(("operator conditional POLICY update + operator_audit append in ONE transaction", tx == "SUCCESS", tx))
        try:
            ddb_admin.delete_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": "PROFILE"}})
            de = "SUCCESS"
        except Exception as e:  # noqa: BLE001
            de = err_code(e)
        rows.append(("operator DeleteItem on the POLICY# probe -> AccessDeniedException", de == "AccessDeniedException", de))
        got = ddb_admin.get_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": "PROFILE"}}, ConsistentRead=True)
        rev = got.get("Item", {}).get("revision", {}).get("N")
        audits = [ddb_admin.get_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": s}}, ConsistentRead=True)
                  .get("Item") is not None for s in ("AUDIT#0001", "AUDIT#0002")]
        rows.append(("strong read-back: revision 2 and 2 of 2 audit items", rev == "2" and all(audits),
                     {"revision": rev, "audits_present": audits}))
    else:
        rows.append(("exercise: table present for the operator transaction", False, "ResourceNotFoundException"))
    print("DENOMINATOR: %d checks" % len(rows))
    ok = print_rows(rows)
    return verdict(6, ok, "" if ok else "an operator-principal check failed (see NOT lines)")


def _ssm_run(sess, lines: list, budget_s: int = 90) -> tuple:
    ssm = sess.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                           Parameters={"commands": lines}, Comment="NFRA_OPLGTW OG-i-1 AC7 probe")["Command"]["CommandId"]
    deadline = time.time() + budget_s
    inv = {}
    while time.time() < deadline:
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception as e:  # noqa: BLE001
            if err_code(e) == "InvocationDoesNotExist":
                continue
            raise
        if inv.get("Status") in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    return cid, inv.get("Status"), inv.get("StandardOutputContent", ""), inv.get("StandardErrorContent", "")


def ac7() -> int:
    sess = session()
    t0 = now()
    if not table_exists(sess.client("dynamodb")):
        print("MEASURED %s: describe-table %s -> ResourceNotFoundException; no on-host write attempted" % (iso(t0), TABLE))
        return verdict(7, False, "precondition: table absent")
    record_first_read("AC7", t0)
    u = stamp()
    exp = str(int(time.time()) + 3600)
    pol, run = "POLICY#probe-og-i1-%s" % u, "RUNTIME#probe-og-i1-%s" % u

    def item(pk, sk, ttl):
        it = {"pk": {"S": pk}, "sk": {"S": sk}, "probe": {"S": "og-i1-ac7"}}
        if ttl:
            it[TTL_ATTR] = {"N": exp}
        return it

    arms = [
        ("CALLER", ["sts", "get-caller-identity", "--query", "Arn", "--output", "text"]),
        ("POLICY_PUT", ["dynamodb", "put-item", "--table-name", TABLE, "--item", json.dumps(item(pol, "PROBE-AC7", False))]),
        ("RUNTIME_PUT", ["dynamodb", "put-item", "--table-name", TABLE, "--item", json.dumps(item(run, "PROBE-AC7", True))]),
        ("POLICY_TX", ["dynamodb", "transact-write-items", "--transact-items",
                       json.dumps([{"Put": {"TableName": TABLE, "Item": item(pol, "PROBE-AC7-TX", False)}}])]),
        ("RUNTIME_TX", ["dynamodb", "transact-write-items", "--transact-items",
                        json.dumps([{"Put": {"TableName": TABLE, "Item": item(run, "PROBE-AC7-TX", True)}}])]),
        ("MIXED_TX", ["dynamodb", "transact-write-items", "--transact-items",
                      json.dumps([{"Put": {"TableName": TABLE, "Item": item(run, "PROBE-AC7-MIX", True)}},
                                  {"Put": {"TableName": TABLE, "Item": item(pol, "PROBE-AC7-MIX", False)}}])]),
        ("RUNTIME_DELETE", ["dynamodb", "delete-item", "--table-name", TABLE, "--key",
                            json.dumps({"pk": {"S": run}, "sk": {"S": "PROBE-AC7"}})]),
        ("POLICY_STRONG_READ", ["dynamodb", "get-item", "--consistent-read", "--table-name", TABLE, "--key",
                                json.dumps({"pk": {"S": pol}, "sk": {"S": "PROBE-AC7"}})]),
    ]
    lines = ["export AWS_DEFAULT_REGION=%s" % REGION]
    for name, args in arms:
        lines.append("echo '=== %s'; aws %s 2>&1; echo \"RC_%s=$?\"" % (name, " ".join(shlex.quote(a) for a in args), name))
    cid, status, out, err = _ssm_run(sess, lines)
    print("EXERCISE %s: ssm %s on %s status %s, keys %s / %s" % (iso(now()), cid, INSTANCE, status, pol, run))
    print(out.rstrip())
    if err.strip():
        print("STDERR: %s" % err.strip())
    res = {}
    for name, _ in arms:
        seg = out.split("=== %s" % name, 1)[-1].split("=== ", 1)[0]
        rc_line = [ln for ln in seg.splitlines() if ln.startswith("RC_%s=" % name)]
        res[name] = (rc_line[0].split("=", 1)[1] if rc_line else None, seg)
    caller_ok = ":assumed-role/%s/" % RUNTIME_ROLE in res["CALLER"][1]
    denied = lambda n: res[n][0] not in (None, "0") and "AccessDeniedException" in res[n][1]  # noqa: E731
    rows = [("caller is the instance role %s" % RUNTIME_ROLE, caller_ok, res["CALLER"][1].strip().splitlines()[:1]),
            ("POLICY# put-item -> AccessDeniedException", denied("POLICY_PUT"), res["POLICY_PUT"][0]),
            ("RUNTIME# put-item (same harness) -> rc 0", res["RUNTIME_PUT"][0] == "0", res["RUNTIME_PUT"][0])]
    supp = [("POLICY# transact-write -> AccessDeniedException", denied("POLICY_TX"), res["POLICY_TX"][0]),
            ("RUNTIME# transact-write -> rc 0", res["RUNTIME_TX"][0] == "0", res["RUNTIME_TX"][0]),
            ("mixed RUNTIME#+POLICY# transaction -> AccessDeniedException", denied("MIXED_TX"), res["MIXED_TX"][0]),
            ("RUNTIME# delete-item -> AccessDeniedException", denied("RUNTIME_DELETE"), res["RUNTIME_DELETE"][0]),
            ("POLICY# strong read -> rc 0", res["POLICY_STRONG_READ"][0] == "0", res["POLICY_STRONG_READ"][0])]
    print("DECIDING (%d):" % len(rows))
    ok = print_rows(rows)
    print("SUPPLEMENTARY (%d, printed, not deciding):" % len(supp))
    print_rows(supp)
    return verdict(7, ok, "" if ok else "the POLICY#/RUNTIME# difference did not hold (see NOT lines)")


def ac8() -> int:
    sess = session()
    t0 = now()
    if not table_exists(sess.client("dynamodb")):
        print("MEASURED %s: describe-table %s -> ResourceNotFoundException; no race attempted" % (iso(t0), TABLE))
        return verdict(8, False, "precondition: table absent")
    record_first_read("AC8", t0)
    s2, arn = admin_clients(sess)
    pk = "POLICY#probe-og-i1-%s-race" % stamp()
    seed_c = s2.client("dynamodb")
    operator_seed(seed_c, pk)
    clients = [s2.client("dynamodb"), s2.client("dynamodb")]
    for c in clients:  # warm both connections so the barrier releases two ready calls
        c.get_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": "PROFILE"}}, ConsistentRead=True)
    barrier = threading.Barrier(2)
    results = [None, None]
    times = [None, None]

    def racer(i):
        barrier.wait()
        t_a = now()
        try:
            clients[i].update_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": "PROFILE"}},
                                   UpdateExpression="SET revision = :n, rev_by = :who",
                                   ConditionExpression="revision = :e",
                                   ExpressionAttributeValues={":n": {"N": "2"}, ":e": {"N": "1"},
                                                              ":who": {"S": "racer-%d" % i}})
            results[i] = "SUCCESS"
        except Exception as e:  # noqa: BLE001
            results[i] = err_code(e)
        times[i] = (iso(t_a), iso(now()))

    th = [threading.Thread(target=racer, args=(i,)) for i in (0, 1)]
    for t in th:
        t.start()
    for t in th:
        t.join(60)
    got = seed_c.get_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": "PROFILE"}}, ConsistentRead=True)["Item"]
    print("EXERCISE %s: operator %s, record %s; instrument: two concurrent conditional UpdateItem calls "
          "(ConditionExpression revision = 1), released by one barrier" % (iso(t0), arn, pk))
    for i in (0, 1):
        print("  racer-%d %s start %s end %s" % (i, results[i], times[i][0] if times[i] else None,
                                                 times[i][1] if times[i] else None))
    print("  strong read-back: revision %s rev_by %s" % (got.get("revision", {}).get("N"), got.get("rev_by", {}).get("S")))
    c = Counter(results)
    winner = "racer-%d" % results.index("SUCCESS") if "SUCCESS" in results else None
    rows = [("exactly 1 of 2 SUCCESS", c.get("SUCCESS") == 1, dict(c)),
            ("exactly 1 of 2 ConditionalCheckFailedException", c.get("ConditionalCheckFailedException") == 1, dict(c)),
            ("read-back revision 2 written by the winner", got.get("revision", {}).get("N") == "2"
             and got.get("rev_by", {}).get("S") == winner, winner)]
    print("DENOMINATOR: 2 concurrent revisions; %d checks" % len(rows))
    ok = print_rows(rows)
    return verdict(8, ok, "" if ok else "the race did not yield one success and one ConditionalCheckFailed")


def ac9() -> int:
    sess = session()
    t0 = now()
    ddb = sess.client("dynamodb")
    if not table_exists(ddb):
        print("MEASURED %s: describe-table %s -> ResourceNotFoundException; no probe record written" % (iso(t0), TABLE))
        return verdict(9, False, "precondition: table absent")
    record_first_read("AC9", t0)
    ttl_name = ddb.describe_time_to_live(TableName=TABLE)["TimeToLiveDescription"].get("AttributeName")
    s2, _ = admin_clients(sess)
    c = s2.client("dynamodb")
    pk = "POLICY#probe-og-i1-%s-ttl" % stamp()
    operator_seed(c, pk)
    items = {}
    for sk in ("PROFILE", "AUDIT#0001"):
        items[sk] = c.get_item(TableName=TABLE, Key={"pk": {"S": pk}, "sk": {"S": sk}}, ConsistentRead=True).get("Item")
    print("MEASURED %s: live TTL attribute name %s; probe %s" % (iso(t0), ttl_name, pk))
    rows = [("live TTL attribute name is set", bool(ttl_name), ttl_name)]
    for sk, it in items.items():
        names = sorted((it or {}).keys())
        rows.append(("%s#%s present and carries no %s" % (pk, sk, ttl_name), it is not None and ttl_name not in names,
                     names))
    print("DENOMINATOR: %d probe POLICY# items read; %d checks" % (len(items), len(rows)))
    ok = print_rows(rows)
    return verdict(9, ok, "" if ok else "a POLICY# probe record carries the TTL attribute or is absent")


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def ac10() -> int:
    if not os.path.isfile(PLAN):
        print("MEASURED: plan file absent at %s" % rel(PLAN))
        return verdict(10, False, "plan file absent")
    d = load_json(PLAN)
    rc = d["resource_changes"]
    print("SOURCE: %s -- terraform %s, plan timestamp %s, source show-json sha256 %s, plan line %r"
          % (rel(PLAN), d.get("terraform_version"), d.get("timestamp"), d.get("source_sha256"), d.get("plan_line")))
    outside = [r for r in rc if r["address"] not in EXPECTED_CREATES and r["actions"] != ["no-op"]]
    destroys = [r["address"] for r in rc if "delete" in r["actions"]]
    print("DENOMINATOR: %d resource_changes; %d are outside this cell's %d creates and not no-op"
          % (len(rc), len(outside), len(EXPECTED_CREATES)))
    rows = [("exactly 2 out-of-cell changes", len(outside) == 2, [r["address"] for r in outside]),
            ("their addresses == the two admitted WAF sets", {r["address"] for r in outside} == ADMITTED_UPDATES,
             sorted(r["address"] for r in outside))]
    for r in outside:
        a = r["address"]
        ch = sorted(r.get("changed_attributes", {}))
        rows.append(("%s actions == [update]" % a, r["actions"] == ["update"], r["actions"]))
        rows.append(("%s changes only description" % a, ch == ["description"],
                     {k: r["changed_attributes"][k] for k in ch}))
        rows.append(("%s addresses absent from the diff" % a,
                     "addresses" not in ch and "addresses" not in r.get("unknown_after", []),
                     {"changed": ch, "unknown_after": r.get("unknown_after"),
                      "addresses_count_before": r.get("addresses_count_before"),
                      "addresses_count_after": r.get("addresses_count_after")}))
        rows.append(("%s no replace_paths" % a, not r.get("replace_paths"), r.get("replace_paths")))
    rows.append(("nothing destroyed (delete actions in the plan)", not destroys, destroys))
    ok = print_rows(rows)
    if os.path.isfile(APPLY_REC):
        g = load_json(APPLY_REC).get("guard") or {}
        print("SUPPLEMENTARY (not deciding): the in-apply plan the approval guard judged -- plan line %r, creates %s, "
              "updates %s, attribute lines %s, other headers %s, verdict ok=%s"
              % (g.get("plan_line"), sorted(g.get("creates", [])), sorted(g.get("updates", [])),
                 json.dumps(g.get("update_attr_lines"), sort_keys=True), g.get("other_headers"), g.get("ok")))
    return verdict(10, ok, "" if ok else "the out-of-cell changes are not exactly the two admitted description updates")


def ac11() -> int:
    missing = [rel(p) for p in (WAF_PRE, WAF_POST, APPLY_REC) if not os.path.isfile(p)]
    if missing:
        print("MEASURED %s: evidence absent %s" % (iso(now()), missing))
        return verdict(11, False, "evidence absent: %s" % missing)
    pre, post, rec = load_json(WAF_PRE), load_json(WAF_POST), load_json(APPLY_REC)
    t_pre, t_post = parse_ts(pre["read_utc"]), parse_ts(post["read_utc"])
    t_start, t_end = parse_ts(rec["start_utc"]), parse_ts(rec["end_utc"])
    print("SOURCES: %s (read %s), %s (read %s), %s (apply start %s end %s rc %s); instrument %s"
          % (rel(WAF_PRE), pre["read_utc"], rel(WAF_POST), post["read_utc"], rel(APPLY_REC), rec["start_utc"],
             rec["end_utc"], rec.get("rc"), pre.get("instrument")))
    rows, supp = [], []
    for k in ("v4", "v6"):
        a, b = pre["sets"][k], post["sets"][k]
        print("  %s %s (%s): PRE count %d sha256 %s | POST count %d sha256 %s | lock token %s -> %s"
              % (k, a["name"], a["id"], a["count"], a["sha256_sorted"], b["count"], b["sha256_sorted"],
                 a["lock_token_sha256_12"], b["lock_token_sha256_12"]))
        rows.append(("%s address list identical before/after (count %d == %d, sha256 of the sorted list equal)"
                     % (k, a["count"], b["count"]),
                     a["count"] == b["count"] and a["sha256_sorted"] == b["sha256_sorted"], None))
        supp.append(("%s lock token rotated pre->post (the reads bracket an applied UpdateIPSet)" % k,
                     a["lock_token_sha256_12"] != b["lock_token_sha256_12"], None))
        supp.append(("%s description present after the apply" % k, b["description_present"], a["description_present"]))
    rows.append(("the bracketed apply completed (rc 0 and an Apply complete line)",
                 rec.get("rc") == 0 and bool(rec.get("apply_complete")),
                 {"rc": rec.get("rc"), "answer": rec.get("answer"), "apply_complete": rec.get("apply_complete")}))
    rows.append(("pre read precedes the apply start", t_pre <= t_start,
                 "%.1f s before" % (t_start - t_pre).total_seconds()))
    rows.append(("post read follows the apply end", t_post >= t_end,
                 "%.1f s after" % (t_post - t_end).total_seconds()))
    deleted = commits(SENTINEL, "D")
    text, h_close = "", None
    if deleted:
        h_close = min(deleted, key=lambda x: x[1])[0]
        for e in sorted(glob.glob(os.path.join(REPO, ENTRY_GLOB))):
            try:
                text += git("show", "%s:%s" % (h_close, rel(e)))
            except RuntimeError:
                pass
    tokens = ["PRE %s" % pre["read_utc"], "POST %s" % post["read_utc"]]
    for w in (pre, post):
        for k in ("v4", "v6"):
            tokens.append("%s count=%d sha256=%s" % (k, w["sets"][k]["count"], w["sets"][k]["sha256_sorted"][:16]))
    absent = [t for t in tokens if t not in text]
    rows.append(("both reads recorded in the change-management entry at its close commit %s (%d of %d tokens)"
                 % (h_close[:10] if h_close else None, len(tokens) - len(absent), len(tokens)),
                 bool(h_close) and not absent, absent))
    print("DECIDING (%d):" % len(rows))
    ok = print_rows(rows)
    print("SUPPLEMENTARY (%d, printed, not deciding):" % len(supp))
    print_rows(supp)
    return verdict(11, ok, "" if ok else "the before/after address lists or their record did not hold (see NOT lines)")


def ac12() -> int:
    scratch = os.path.join(REPO, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    pf = os.path.join(scratch, "og_i1.post.%s.tfplan" % stamp())
    t0 = now()
    r = subprocess.run([TF, "-chdir=%s" % TF_ROOT, "plan", "-input=false", "-lock=false", "-no-color",
                        "-detailed-exitcode", "-out=%s" % pf], capture_output=True, text=True, timeout=95)
    t1 = now()
    summary = [ln.strip() for ln in r.stdout.splitlines() if ln.startswith("Plan:") or ln.startswith("No changes.")]
    print("MEASURED %s..%s: terraform plan -lock=false -detailed-exitcode rc %d (0 no changes, 2 changes, 1 error); %s"
          % (iso(t0), iso(t1), r.returncode, summary))
    if r.returncode not in (0, 2):
        print("STDERR: %s" % r.stderr.strip()[-2000:])
        return verdict(12, False, "fresh plan failed rc %d" % r.returncode)
    s = subprocess.run([TF, "-chdir=%s" % TF_ROOT, "show", "-json", pf], capture_output=True, text=True, timeout=60)
    try:
        os.remove(pf)
    except OSError:
        pass
    d = json.loads(s.stdout)
    rcs = d.get("resource_changes", [])
    by = {x["address"]: x["change"]["actions"] for x in rcs}
    counts = Counter("+".join(v) for v in by.values())
    graded = sorted(EXPECTED_CREATES | ADMITTED_UPDATES)
    elsewhere = sorted(a for a, v in by.items() if v != ["no-op"] and a not in graded)
    print("DENOMINATOR: %d resource_changes in the fresh plan, by action %s; %d graded (2 WAF sets + this cell's 4)"
          % (len(rcs), json.dumps(dict(sorted(counts.items()))), len(graded)))
    rows = [("%s -> no-op" % a, by.get(a) == ["no-op"], by.get(a)) for a in graded]
    ok = print_rows(rows)
    print("SUPPLEMENTARY (not deciding): changes elsewhere in the root: %s" % (elsewhere or "none"))
    write_json(POSTPLAN, {"plan_utc": iso(t0), "terraform_version": d.get("terraform_version"),
                          "rc_detailed_exitcode": r.returncode, "summary": summary,
                          "counts": dict(sorted(counts.items())), "graded": {a: by.get(a) for a in graded},
                          "changes_elsewhere": elsewhere})
    print("RECORDED %s" % rel(POSTPLAN))
    return verdict(12, ok, "" if ok else "a graded resource is not no-op in the fresh plan (see NOT lines)")


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)
        fh.write("\n")


ARMS = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7, "AC8": ac8, "AC9": ac9,
        "AC10": ac10, "AC11": ac11, "AC12": ac12}


def main(argv: list) -> int:
    if len(argv) != 2 or argv[1].upper() not in ARMS:
        print("usage: og_i1.py AC<1..12>")
        return 2
    arm = argv[1].upper()
    n = int(arm[2:])
    print("PROBE og_i1.py %s run %s (repo %s)" % (arm, iso(now()), REPO))
    try:
        return ARMS[arm]()
    except Exception as e:  # noqa: BLE001 -- a probe that cannot measure says so, never passes
        print("ERROR: %s: %s" % (type(e).__name__, e))
        return verdict(n, False, "probe error %s" % err_code(e))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
