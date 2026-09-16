#!/usr/bin/env python3
"""og_i2.py -- the acceptance probe for NFRA_OPLGTW.TO-OG-i-2 (cell OG-i-2).

Usage:  og_i2.py AC<n>      n = 1..16

Each arm prints its measurement with its vintage (the UTC time of a live read, or the source's own timestamp) and its
denominator, then exactly one final line:  VERDICT: PASS-OGI2-AC<n>  or  VERDICT: FAIL-OGI2-AC<n> <reason>.

Arms and instruments:
  AC1  the saved plan og_i2.plan.json (redacted `terraform show -json`): exactly the ten creates, the two roles, the
       Gateway statement's policy on opal-gateway-role, the alias-key secret and its Gateway read policy. The Gateway
       statement's CONTENT is unknown in the plan (it references the created ARNs), so its applied document is read
       back live beside the plan and labelled so.
  AC2  the saved plan: every resource block declared in taxsma_gateway_iam.tf (parsed from the file, denominator
       printed) is no-op, and nothing outside this cell's creates is anything but no-op.
  AC3  live: the data role's inline and attached policies, graded statement by statement.
  AC4  live: the catalog role's inline and attached policies, graded statement by statement.
  AC5  live: both trust policies, compared with the ExternalIds secret (equality only, never a value printed).
  AC6..AC14  live, on the Gateway host i-07dccb1615503ac99 through SSM, under the instance's own role. ExternalIds are
       read ON the host from their secret; the Tax SMA ExternalId is read at run time from taxsma_gateway_iam.tf. No
       credential, ExternalId or object byte is printed or kept (get-object writes to /dev/null).
  AC15 evidence/og_i2/bucket_policy_pre.json and _post.json (written by og_i2_act.py around the apply) against the
       apply record's start/end, and a fresh live read now.
  AC16 reader-identities.result.md: a labelled policy-simulation section and a separate labelled live-exercised
       section, each with its own content. AC3/AC4 write evidence/og_i2/simulation_AC3.json / _AC4.json; the on-host
       arms write evidence/og_i2/live_AC<n>.json.

Writes: evidence files only. The one write attempt is AC10's PutObject of an EMPTY body to a key that does not exist,
checked absent before and after; if it ever succeeds the arm says STOP. Standard library + boto3. ASCII only.
botocore/boto3/urllib3 loggers are held at INFO or higher (row W3-S26).
"""
from __future__ import annotations

import datetime
import json
import logging
import os
import re
import subprocess
import sys
import time

for _n in ("botocore", "boto3", "urllib3"):
    logging.getLogger(_n).setLevel(logging.INFO)

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
REPO = _top.stdout.strip() or os.path.abspath(os.path.join(DELIV, *[".."] * 6))

REGION = "us-east-1"
ACCOUNT = "313476888478"
BUCKET = "opal-data-assets"
BUCKET_ARN = "arn:aws:s3:::" + BUCKET
INSTANCE = "i-07dccb1615503ac99"
GW_ROLE = "opal-gateway-role"
GW_ROLE_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, GW_ROLE)
GW_POLICY = "opal-gateway-assume-schwab-readers"
GW_SID = "AssumeSchwabReaderRoles"
DATA_ROLE = "opal-mcp-emp-menachem-schwab-read"
CAT_ROLE = "opal-mcp-schwab-catalog-read"
DATA_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, DATA_ROLE)
CAT_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, CAT_ROLE)
ALIAS_SECRET = "opal/mcp/opal-gateway-schwab-account-ref-key"
EXT_SECRET = "opal/mcp/opal-gateway-schwab-reader-external-ids"
EXT_FIELDS = {"data": "data_read", "catalog": "catalog_read"}
DATA_PREFIXES = [
    "schwab/08242234/silver/dim_position/",
    "schwab/08242234/silver/dim_balance/",
    "schwab/08242234/silver/dim_asset/",
    "schwab/08335338/silver/dim_position/",
    "schwab/08335338/silver/dim_balance/",
    "schwab/08335338/silver/dim_asset/",
]
COMPLETION_PREFIXES = ["schwab/08242234/meta/complete/", "schwab/08335338/meta/complete/"]
READ_ACTIONS = ["s3:GetObject", "s3:GetObjectVersion"]
SILVER_KEY = "schwab/08242234/silver/dim_position/date=2024-05-24/data.parquet"
COMPLETE_KEY = "schwab/08242234/meta/complete/date=2026-08-31.json"
OUTSIDE_PREFIX = "schwab/08242234/bronze/"
META_LIST_PREFIX = "schwab/08242234/meta/"
PLAN = os.path.join(DELIV, "og_i2.plan.json")
EVID = os.path.join(DELIV, "evidence", "og_i2")
APPLY_REC = os.path.join(EVID, "apply.json")
BP_PRE = os.path.join(EVID, "bucket_policy_pre.json")
BP_POST = os.path.join(EVID, "bucket_policy_post.json")
RESULT = os.path.join(DELIV, "reader-identities.result.md")
TAXSMA_TF = os.path.join(REPO, "infra", "aws", "terraform", "opal-gateway", "taxsma_gateway_iam.tf")
EXPECTED_CREATES = {
    "aws_iam_role.schwab_data_read",
    "aws_iam_role_policy.schwab_data_read_policy",
    "aws_iam_role.schwab_catalog_read",
    "aws_iam_role_policy.schwab_catalog_read_policy",
    "aws_iam_role_policy.gw_assume_schwab_readers",
    "aws_secretsmanager_secret.schwab_account_ref_key",
    "aws_secretsmanager_secret_policy.schwab_account_ref_key_gw_read",
    "aws_secretsmanager_secret.schwab_reader_external_ids",
    "aws_secretsmanager_secret_version.schwab_reader_external_ids",
    "aws_secretsmanager_secret_policy.schwab_reader_external_ids_gw_read",
}
SIM_SECTION = "## POLICY SIMULATION RESULTS (iam simulate-principal-policy -- modelled, NOT exercised)"
LIVE_SECTION = "## LIVE EXERCISED RESULTS (Gateway host i-07dccb1615503ac99 via SSM, instance role -- exercised)"


# --------------------------------------------------------------------------- helpers
def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t: datetime.datetime) -> str:
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def stamp() -> str:
    return now().strftime("%Y%m%dT%H%M%S%fZ")


def parse_ts(s: str) -> datetime.datetime:
    t = datetime.datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
    return (t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)).astimezone(datetime.timezone.utc)


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace("\\", "/")


def verdict(n: int, ok: bool, reason: str = "") -> int:
    print("VERDICT: PASS-OGI2-AC%d" % n if ok else "VERDICT: FAIL-OGI2-AC%d %s" % (n, reason))
    return 0 if ok else 1


def session():
    import boto3
    return boto3.Session(region_name=REGION)


def err_code(e) -> str:
    return getattr(e, "response", {}).get("Error", {}).get("Code", type(e).__name__)


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)
        fh.write("\n")


def print_rows(rows: list) -> bool:
    for check, ok, detail in rows:
        print("  %s %s -- %s" % ("OK " if ok else "NOT", check, detail))
    n_ok = sum(1 for r in rows if r[1])
    print("DENOMINATOR: %d of %d checks OK" % (n_ok, len(rows)))
    return n_ok == len(rows) and rows


def plan_changes() -> tuple:
    d = load_json(PLAN)
    print("SOURCE: %s -- terraform %s, plan timestamp %s, source show-json sha256 %s, plan line %r"
          % (rel(PLAN), d.get("terraform_version"), d.get("timestamp"), d.get("source_sha256"), d.get("plan_line")))
    return d, {r["address"]: r for r in d["resource_changes"]}


def policy_doc(v) -> dict:
    if isinstance(v, dict):
        return v
    return json.loads(v)


def role_policies(iam, role: str) -> tuple:
    names = []
    for page in iam.get_paginator("list_role_policies").paginate(RoleName=role):
        names.extend(page["PolicyNames"])
    attached = []
    for page in iam.get_paginator("list_attached_role_policies").paginate(RoleName=role):
        attached.extend(a["PolicyArn"] for a in page["AttachedPolicies"])
    docs = {n: policy_doc(iam.get_role_policy(RoleName=role, PolicyName=n)["PolicyDocument"]) for n in names}
    return docs, attached


def by_sid(doc: dict) -> dict:
    return {s.get("Sid"): s for s in as_list(doc.get("Statement"))}


def taxsma_external_id() -> str:
    with open(TAXSMA_TF, encoding="utf-8") as fh:
        m = re.search(r'^\s*taxsma_external_id\s*=\s*"([^"]+)"', fh.read(), re.M)
    if not m:
        raise RuntimeError("taxsma_external_id not found in %s" % rel(TAXSMA_TF))
    return m.group(1)


def read_external_ids(sess) -> dict:
    return json.loads(sess.client("secretsmanager").get_secret_value(SecretId=EXT_SECRET)["SecretString"])


# --------------------------------------------------------------------------- AC1 / AC2 (plan)
def ac1() -> int:
    if not os.path.isfile(PLAN):
        print("MEASURED: plan file absent at %s" % rel(PLAN))
        return verdict(1, False, "plan file absent")
    d, rc = plan_changes()
    creates = {a for a, r in rc.items() if r["actions"] == ["create"]}
    others = {a: r["actions"] for a, r in rc.items() if r["actions"] not in (["create"], ["no-op"])}
    print("DENOMINATOR: %d resource_changes in the plan, counts %s" % (len(rc), json.dumps(d.get("counts"))))
    rows = [("creates == this cell's ten", creates == EXPECTED_CREATES,
             "extra %s missing %s" % (sorted(creates - EXPECTED_CREATES), sorted(EXPECTED_CREATES - creates))),
            ("no update/delete/replace anywhere", not others, others)]
    role_creates = sorted(r["after"]["name"] for a, r in rc.items()
                          if r["actions"] == ["create"] and r["type"] == "aws_iam_role")
    rows.append(("exactly two roles created, named per C6", role_creates == sorted([DATA_ROLE, CAT_ROLE]), role_creates))
    for addr, role in (("aws_iam_role_policy.schwab_data_read_policy", DATA_ROLE),
                       ("aws_iam_role_policy.schwab_catalog_read_policy", CAT_ROLE)):
        a = (rc.get(addr) or {}).get("after") or {}
        unk = (rc.get(addr) or {}).get("after_unknown") or {}
        rows.append(("%s has a policy for %s" % (addr, role),
                     a.get("name") == role + "-policy" and bool(a.get("policy")) and unk.get("role") is True,
                     "name %s, policy known %s, role unknown-until-apply %s"
                     % (a.get("name"), bool(a.get("policy")), unk.get("role"))))
    gw = rc.get("aws_iam_role_policy.gw_assume_schwab_readers") or {}
    ga = gw.get("after") or {}
    rows.append(("the Gateway statement's policy is created ON %s" % GW_ROLE, ga.get("role") == GW_ROLE,
                 "role %s, name %s, policy unknown-until-apply %s"
                 % (ga.get("role"), ga.get("name"), (gw.get("after_unknown") or {}).get("policy"))))
    gw_existing = [a for a, r in rc.items() if r["type"] == "aws_iam_role_policy" and a != gw.get("address")
                   and r["actions"] == ["create"] and (r.get("after") or {}).get("role") == GW_ROLE]
    rows.append(("no OTHER new policy on %s" % GW_ROLE, not gw_existing, gw_existing))
    sec = (rc.get("aws_secretsmanager_secret.schwab_account_ref_key") or {}).get("after") or {}
    rows.append(("alias-key secret created by name", sec.get("name") == ALIAS_SECRET, sec.get("name")))
    sp = (rc.get("aws_secretsmanager_secret_policy.schwab_account_ref_key_gw_read") or {}).get("after") or {}
    try:
        spd = policy_doc(sp.get("policy"))
        sts_ = as_list(spd.get("Statement"))
        ok = (len(sts_) == 1 and sts_[0].get("Effect") == "Allow"
              and as_list((sts_[0].get("Principal") or {}).get("AWS")) == [GW_ROLE_ARN]
              and as_list(sts_[0].get("Action")) == ["secretsmanager:GetSecretValue"])
        detail = "statements %d, principal %s, action %s" % (len(sts_), (sts_[0].get("Principal") if sts_ else None),
                                                              (sts_[0].get("Action") if sts_ else None))
    except Exception as e:  # noqa: BLE001
        ok, detail = False, "unparsed: %s" % e
    rows.append(("the Gateway's read grant on the alias-key secret (its resource policy): one Allow, Gateway role, "
                 "GetSecretValue only", ok, detail))
    print("PLAN CHECKS (%s):" % rel(PLAN))
    plan_ok = print_rows(rows)
    # the applied Gateway statement -- the plan cannot show its content
    sess = session()
    iam = sess.client("iam")
    t = now()
    live = []
    try:
        docs, attached = role_policies(iam, GW_ROLE)
        doc = docs.get(GW_POLICY) or {}
        sts_ = as_list(doc.get("Statement"))
        s = sts_[0] if sts_ else {}
        cond = (s.get("Condition") or {}).get("StringEquals") or {}
        ext_in_stmt = sorted(as_list(cond.get("sts:ExternalId")))
        ext = read_external_ids(sess)
        dedicated = sorted([ext[EXT_FIELDS["data"]], ext[EXT_FIELDS["catalog"]]])
        live += [("%s holds exactly ONE statement" % GW_POLICY, len(sts_) == 1, "%d statement(s)" % len(sts_)),
                 ("its Sid is %s" % GW_SID, s.get("Sid") == GW_SID, s.get("Sid")),
                 ("Allow sts:AssumeRole only", s.get("Effect") == "Allow" and as_list(s.get("Action")) == ["sts:AssumeRole"],
                  "%s %s" % (s.get("Effect"), s.get("Action"))),
                 ("Resource == exactly the two reader ARNs", sorted(as_list(s.get("Resource"))) == sorted([DATA_ARN, CAT_ARN]),
                  as_list(s.get("Resource"))),
                 ("Condition keys only StringEquals sts:ExternalId", list((s.get("Condition") or {})) == ["StringEquals"]
                  and list(cond) == ["sts:ExternalId"], "operators %s keys %s" % (list(s.get("Condition") or {}), list(cond))),
                 ("the ExternalIds in the statement == the two dedicated ExternalIds (equality only)",
                  ext_in_stmt == dedicated, "%d value(s), equal %s" % (len(ext_in_stmt), ext_in_stmt == dedicated)),
                 ("the Tax SMA ExternalId is NOT in the statement", taxsma_external_id() not in ext_in_stmt,
                  "absent %s" % (taxsma_external_id() not in ext_in_stmt))]
        del ext, dedicated, ext_in_stmt
    except Exception as e:  # noqa: BLE001
        live.append(("the applied Gateway statement is readable", False, err_code(e)))
    print("SUPPLEMENTARY APPLIED READBACK %s (live iam get-role-policy %s/%s -- the plan shows this policy as unknown):"
          % (iso(t), GW_ROLE, GW_POLICY))
    live_ok = print_rows(live)
    return verdict(1, bool(plan_ok) and bool(live_ok), "" if plan_ok and live_ok else "a check is NOT OK (see NOT lines)")


def taxsma_addresses() -> list:
    with open(TAXSMA_TF, encoding="utf-8") as fh:
        return ["%s.%s" % m for m in re.findall(r'^resource\s+"([A-Za-z0-9_]+)"\s+"([A-Za-z0-9_]+)"', fh.read(), re.M)]


def ac2() -> int:
    if not os.path.isfile(PLAN):
        return verdict(2, False, "plan file absent")
    d, rc = plan_changes()
    addrs = taxsma_addresses()
    print("DENOMINATOR: %d resource blocks declared in %s: %s" % (len(addrs), rel(TAXSMA_TF), addrs))
    rows = []
    for a in addrs:
        acts = (rc.get(a) or {}).get("actions")
        rows.append(("%s is no-op" % a, acts == ["no-op"], acts))
    named = {"aws_iam_role_policy.gw_assume_emp": "opal-gateway-assume-emp-roles",
             "aws_iam_role.emp_alyssa_read": "opal-mcp-emp-alyssa-read",
             "aws_iam_role.emp_alyssa_onboard": "opal-mcp-emp-alyssa-onboard"}
    for a, what in named.items():
        rows.append(("%s (%s) is in the graded set" % (a, what), a in addrs, a in addrs))
    alyssa = [a for a in rc if "alyssa" in a]
    rows.append(("every plan address naming alyssa is no-op (%d)" % len(alyssa),
                 bool(alyssa) and all(rc[a]["actions"] == ["no-op"] for a in alyssa), alyssa))
    outside = {a: r["actions"] for a, r in rc.items() if a not in EXPECTED_CREATES and r["actions"] != ["no-op"]}
    rows.append(("nothing outside this cell's ten creates changes (%d of %d resource_changes)"
                 % (len(rc) - len(EXPECTED_CREATES), len(rc)), not outside, outside))
    ok = print_rows(rows)
    return verdict(2, bool(ok), "" if ok else "a Tax SMA / alyssa / existing resource changes (see NOT lines)")


# --------------------------------------------------------------------------- AC3 / AC4 (live documents + simulation)
def simulate(iam, role_arn: str, cases: list) -> list:
    out = []
    for action, resource, ctx in cases:
        kw = {"PolicySourceArn": role_arn, "ActionNames": [action], "ResourceArns": [resource]}
        if ctx:
            kw["ContextEntries"] = [{"ContextKeyName": "s3:prefix", "ContextKeyValues": [ctx],
                                     "ContextKeyType": "string"}]
        r = iam.simulate_principal_policy(**kw)["EvaluationResults"][0]
        out.append({"action": action, "resource": resource, "s3_prefix": ctx, "decision": r["EvalDecision"],
                    "matched": sorted({m.get("SourcePolicyId") for m in r.get("MatchedStatements", [])})})
    return out


def grade_reader(n: int, role: str, role_arn: str, prefixes: list, outside_label: str, sim_cases: list) -> int:
    sess = session()
    iam = sess.client("iam")
    t = now()
    docs, attached = role_policies(iam, role)
    print("MEASURED %s: live iam list-role-policies/get-role-policy/list-attached-role-policies on %s: %d inline %s, "
          "%d attached" % (iso(t), role, len(docs), sorted(docs), len(attached)))
    obj_arns = sorted("%s/%s*" % (BUCKET_ARN, p) for p in prefixes)
    forms = sorted("%s*" % p for p in prefixes)
    rows = [("exactly one inline policy, zero attached", len(docs) == 1 and not attached,
             "%d inline, %d attached" % (len(docs), len(attached)))]
    doc = next(iter(docs.values())) if docs else {}
    sts_ = as_list(doc.get("Statement"))
    allows = [s for s in sts_ if s.get("Effect") == "Allow"]
    denies = [s for s in sts_ if s.get("Effect") == "Deny"]
    print("DENOMINATOR: %d statements (%d Allow, %d Deny)" % (len(sts_), len(allows), len(denies)))
    allow_actions = sorted({a for s in allows for a in as_list(s.get("Action"))})
    rows.append(("Allow actions are exactly GetObject, GetObjectVersion, ListBucket",
                 allow_actions == sorted(READ_ACTIONS + ["s3:ListBucket"]), allow_actions))
    rows.append(("no Allow uses NotAction/NotResource or a wildcard action",
                 all("NotAction" not in s and "NotResource" not in s and not any("*" in a for a in as_list(s.get("Action")))
                     for s in allows), len(allows)))
    get_allows = [s for s in allows if sorted(as_list(s.get("Action"))) == sorted(READ_ACTIONS)]
    rows.append(("GetObject/GetObjectVersion allowed on exactly the %d prefix object ARNs" % len(prefixes),
                 len(get_allows) == 1 and sorted(as_list(get_allows[0].get("Resource"))) == obj_arns and not get_allows[0].get("Condition"),
                 [sorted(as_list(s.get("Resource"))) for s in get_allows]))
    list_allows = [s for s in allows if as_list(s.get("Action")) == ["s3:ListBucket"]]
    rows.append(("ListBucket allowed on the bucket only under StringLike s3:prefix == the %d prefix forms" % len(prefixes),
                 len(list_allows) == 1 and as_list(list_allows[0].get("Resource")) == [BUCKET_ARN]
                 and list_allows[0].get("Condition") == {"StringLike": {"s3:prefix": forms}}
                 or (len(list_allows) == 1 and as_list(list_allows[0].get("Resource")) == [BUCKET_ARN]
                     and sorted(as_list(((list_allows[0].get("Condition") or {}).get("StringLike") or {}).get("s3:prefix"))) == forms
                     and list(list_allows[0].get("Condition") or {}) == ["StringLike"]),
                 [s.get("Condition") for s in list_allows]))
    write_actions = [a for s in allows for a in as_list(s.get("Action"))
                     if re.search(r"(put|delete|copy|restore|replicate|abort|create|update|write|tag)", a, re.I)]
    rows.append(("no write action allowed", not write_actions, write_actions))
    d_nonread = [s for s in denies if sorted(as_list(s.get("NotAction"))) == sorted(READ_ACTIONS + ["s3:ListBucket"])
                 and as_list(s.get("Resource")) == ["*"] and not s.get("Condition")]
    rows.append(("explicit Deny of every action but the three reads, on *", len(d_nonread) == 1, len(d_nonread)))
    d_reads = [s for s in denies if sorted(as_list(s.get("Action"))) == sorted(READ_ACTIONS)
               and sorted(as_list(s.get("NotResource"))) == obj_arns and not s.get("Condition")]
    rows.append(("explicit Deny of GetObject/GetObjectVersion outside the prefixes (%s included)" % outside_label,
                 len(d_reads) == 1, len(d_reads)))
    d_lb_other = [s for s in denies if as_list(s.get("Action")) == ["s3:ListBucket"]
                  and as_list(s.get("NotResource")) == [BUCKET_ARN]]
    rows.append(("explicit Deny of ListBucket on any other bucket", len(d_lb_other) == 1, len(d_lb_other)))
    d_lb_prefix = [s for s in denies if as_list(s.get("Action")) == ["s3:ListBucket"]
                   and as_list(s.get("Resource")) == [BUCKET_ARN]
                   and list(s.get("Condition") or {}) == ["StringNotLike"]
                   and sorted(as_list((s["Condition"]["StringNotLike"] or {}).get("s3:prefix"))) == forms]
    rows.append(("explicit Deny of ListBucket outside the prefix forms (StringNotLike)", len(d_lb_prefix) == 1,
                 len(d_lb_prefix)))
    rows.append(("statement census is exactly 2 Allow + 4 Deny", len(allows) == 2 and len(denies) == 4,
                 "%d Allow, %d Deny" % (len(allows), len(denies))))
    doc_ok = print_rows(rows)
    t2 = now()
    sim = simulate(iam, role_arn, sim_cases)
    sim_rows = [("simulate %s %s prefix=%s -> %s (expected %s)" % (c["action"], c["resource"], c["s3_prefix"],
                 c["decision"], exp), c["decision"] == exp, c["matched"]) for c, exp in zip(sim, [x[3] for x in SIM_EXPECT[n]])]
    print("SIMULATION %s (iam simulate-principal-policy on %s -- MODELLED, not exercised; recorded apart from the live arms):"
          % (iso(t2), role))
    sim_ok = print_rows(sim_rows)
    write_json(os.path.join(EVID, "simulation_AC%d.json" % n),
               {"kind": "POLICY SIMULATION (modelled, not exercised)", "instrument": "iam simulate-principal-policy",
                "read_utc": iso(t2), "role_arn": role_arn, "cases": sim,
                "expected": [x[3] for x in SIM_EXPECT[n]]})
    return verdict(n, bool(doc_ok) and bool(sim_ok), "" if doc_ok and sim_ok else "a check is NOT OK (see NOT lines)")


OUT_KEY_ARN = "%s/%s" % (BUCKET_ARN, "schwab/08242234/bronze/acc/20240116/CRS20240116.ACC")
SIM_EXPECT = {
    3: [("s3:GetObject", "%s/%s" % (BUCKET_ARN, SILVER_KEY), None, "allowed"),
        ("s3:GetObjectVersion", "%s/%s" % (BUCKET_ARN, SILVER_KEY), None, "allowed"),
        ("s3:GetObject", "%s/%s" % (BUCKET_ARN, COMPLETE_KEY), None, "explicitDeny"),
        ("s3:GetObject", OUT_KEY_ARN, None, "explicitDeny"),
        ("s3:PutObject", "%s/%s" % (BUCKET_ARN, SILVER_KEY), None, "explicitDeny"),
        ("s3:DeleteObject", "%s/%s" % (BUCKET_ARN, SILVER_KEY), None, "explicitDeny"),
        ("s3:ListBucket", BUCKET_ARN, DATA_PREFIXES[0], "allowed"),
        ("s3:ListBucket", BUCKET_ARN, META_LIST_PREFIX, "explicitDeny"),
        ("sts:AssumeRole", CAT_ARN, None, "explicitDeny")],
    4: [("s3:GetObject", "%s/%s" % (BUCKET_ARN, COMPLETE_KEY), None, "allowed"),
        ("s3:GetObjectVersion", "%s/%s" % (BUCKET_ARN, COMPLETE_KEY), None, "allowed"),
        ("s3:GetObject", "%s/%s" % (BUCKET_ARN, SILVER_KEY), None, "explicitDeny"),
        ("s3:GetObject", "%s/schwab/08242234/meta/backfill-status.json" % BUCKET_ARN, None, "explicitDeny"),
        ("s3:PutObject", "%s/%s" % (BUCKET_ARN, COMPLETE_KEY), None, "explicitDeny"),
        ("s3:ListBucket", BUCKET_ARN, COMPLETION_PREFIXES[0], "allowed"),
        ("s3:ListBucket", BUCKET_ARN, DATA_PREFIXES[0], "explicitDeny"),
        ("sts:AssumeRole", DATA_ARN, None, "explicitDeny")],
}


def ac3() -> int:
    return grade_reader(3, DATA_ROLE, DATA_ARN, DATA_PREFIXES, "meta/*",
                        [(a, r, c) for a, r, c, _ in SIM_EXPECT[3]])


def ac4() -> int:
    return grade_reader(4, CAT_ROLE, CAT_ARN, COMPLETION_PREFIXES, "silver/* and other meta/*",
                        [(a, r, c) for a, r, c, _ in SIM_EXPECT[4]])


# --------------------------------------------------------------------------- AC5 (trust)
def ac5() -> int:
    sess = session()
    iam = sess.client("iam")
    t = now()
    ext = read_external_ids(sess)
    tax = taxsma_external_id()
    rows = []
    trust_ids = {}
    for label, role in (("data", DATA_ROLE), ("catalog", CAT_ROLE)):
        doc = policy_doc(iam.get_role(RoleName=role)["Role"]["AssumeRolePolicyDocument"])
        sts_ = as_list(doc.get("Statement"))
        s = sts_[0] if sts_ else {}
        principal = s.get("Principal") or {}
        cond = s.get("Condition") or {}
        ids = as_list((cond.get("StringEquals") or {}).get("sts:ExternalId"))
        trust_ids[label] = ids
        rows += [("%s trust: exactly one statement" % role, len(sts_) == 1, len(sts_)),
                 ("%s trust: Allow sts:AssumeRole" % role,
                  s.get("Effect") == "Allow" and as_list(s.get("Action")) == ["sts:AssumeRole"],
                  "%s %s" % (s.get("Effect"), s.get("Action"))),
                 ("%s trust: Principal is ONLY %s" % (role, GW_ROLE),
                  list(principal) == ["AWS"] and as_list(principal.get("AWS")) == [GW_ROLE_ARN], principal),
                 ("%s trust: Condition is only StringEquals sts:ExternalId, one value" % role,
                  list(cond) == ["StringEquals"] and list(cond["StringEquals"]) == ["sts:ExternalId"] and len(ids) == 1,
                  "operators %s, %d value(s)" % (list(cond), len(ids))),
                 ("%s trust: that ExternalId == the secret's %s field (equality only)" % (role, EXT_FIELDS[label]),
                  ids == [ext.get(EXT_FIELDS[label])], ids == [ext.get(EXT_FIELDS[label])]),
                 ("%s trust: that ExternalId is NOT the Tax SMA ExternalId" % role, tax not in ids, tax not in ids),
                 ("%s trust: no NotPrincipal / NotAction" % role, "NotPrincipal" not in s and "NotAction" not in s, True)]
    rows.append(("the two dedicated ExternalIds differ", trust_ids["data"] != trust_ids["catalog"],
                 trust_ids["data"] != trust_ids["catalog"]))
    del ext, tax, trust_ids
    print("MEASURED %s: live iam get-role (AssumeRolePolicyDocument) x2, secretsmanager get-secret-value %s (compared "
          "in memory, no value printed), Tax SMA ExternalId read from %s" % (iso(t), EXT_SECRET, rel(TAXSMA_TF)))
    ok = print_rows(rows)
    return verdict(5, bool(ok), "" if ok else "a trust check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- on-host harness
HOST_PRELUDE = r"""
R=us-east-1
echo "CALLER $(aws sts get-caller-identity --region $R --query Arn --output text 2>&1)"
SECRET_OUT=$(aws secretsmanager get-secret-value --region $R --secret-id '%(ext_secret)s' --query SecretString --output text 2>&1); SRC=$?
if [ $SRC -eq 0 ]; then echo "EXTERNAL_IDS_SECRET_READ rc=0"; else echo "EXTERNAL_IDS_SECRET_READ rc=$SRC err=$(printf '%%s' "$SECRET_OUT" | grep -o 'An error occurred ([A-Za-z]*)' | head -1)"; SECRET_OUT='{}'; fi
ext() { printf '%%s' "$SECRET_OUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('$1',''))"; }
DATA_EXT=$(ext data_read); CAT_EXT=$(ext catalog_read); TAX_EXT='%(tax)s'
echo "EXTERNAL_IDS_PRESENT data=$([ -n "$DATA_EXT" ] && echo yes || echo no) catalog=$([ -n "$CAT_EXT" ] && echo yes || echo no)"
errc() { printf '%%s' "$1" | grep -o 'An error occurred ([A-Za-z]*)' | head -1 | sed 's/An error occurred //'; }
assume() {
  local out; out=$(aws sts assume-role --region $R --role-arn "$1" --role-session-name "$3" --external-id "$2" --duration-seconds 900 --output json 2>&1); ARC=$?
  if [ $ARC -eq 0 ]; then
    CREDS=$(printf '%%s' "$out" | python3 -c "import json,sys;c=json.load(sys.stdin)['Credentials'];print(c['AccessKeyId'],c['SecretAccessKey'],c['SessionToken'])")
    AARN=$(printf '%%s' "$out" | python3 -c "import json,sys;print(json.load(sys.stdin)['AssumedRoleUser']['Arn'])"); AERR=none
  else CREDS=""; AARN=""; AERR=$(errc "$out"); fi
  out=""
}
as_creds() { local c="$1"; shift; set -- $c "$@"; AWS_ACCESS_KEY_ID=$1 AWS_SECRET_ACCESS_KEY=$2 AWS_SESSION_TOKEN=$3 "${@:4}"; }
"""


def ssm_run(sess, n: int, body: str, budget_s: int = 95) -> tuple:
    ssm = sess.client("ssm")
    script = HOST_PRELUDE % {"ext_secret": EXT_SECRET, "tax": taxsma_external_id()} + body
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                           Parameters={"commands": [script], "executionTimeout": ["80"]},
                           Comment="NFRA_OPLGTW OG-i-2 AC%d probe" % n)["Command"]["CommandId"]
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


def kv(out: str, tag: str) -> dict:
    for ln in out.splitlines():
        if ln.startswith(tag + " ") or ln == tag:
            return dict(p.split("=", 1) for p in ln[len(tag):].split() if "=" in p)
    return {}


def host_arm(n: int, title: str, body: str, grade) -> int:
    sess = session()
    t0 = now()
    cid, status, out, err = ssm_run(sess, n, body)
    t1 = now()
    for secretish in ("AccessKeyId", "SecretAccessKey", "SessionToken", taxsma_external_id()):
        if secretish in out or secretish in err:
            print("REFUSED: the host output carries a credential/ExternalId token; nothing recorded")
            return verdict(n, False, "host output not clean")
    print("EXERCISE %s..%s: ssm send-command %s on %s, status %s, under the instance role" % (iso(t0), iso(t1), cid,
                                                                                            INSTANCE, status))
    print("HOST STDOUT:\n" + "\n".join("  | " + ln for ln in out.splitlines()))
    if err.strip():
        print("HOST STDERR (%d lines, first 5):\n%s" % (len(err.splitlines()),
                                                      "\n".join("  ! " + ln for ln in err.splitlines()[:5])))
    base = [("SSM invocation Success", status == "Success", status),
            ("caller is opal-gateway-role on the instance",
             "assumed-role/%s/%s" % (GW_ROLE, INSTANCE) in out, (kv(out, "CALLER") or out.splitlines()[:1])),
            ("the ExternalIds secret was readable on the host", kv(out, "EXTERNAL_IDS_SECRET_READ").get("rc") == "0",
             kv(out, "EXTERNAL_IDS_SECRET_READ"))]
    rows = base + grade(out)
    print("%s:" % title)
    ok = print_rows(rows)
    write_json(os.path.join(EVID, "live_AC%d.json" % n),
               {"kind": "LIVE EXERCISED (Gateway host via SSM, instance role)", "criterion": "OGI2-AC%d" % n,
                "ssm_command_id": cid, "instance": INSTANCE, "status": status, "start_utc": iso(t0), "end_utc": iso(t1),
                "stdout": out.splitlines(), "checks": [{"check": c, "ok": o, "detail": str(d)} for c, o, d in rows]})
    return ok


def ac6() -> int:
    body = r"""
for pair in "data %s" "catalog %s"; do
  set -- $pair; L=$1; ARN=$2
  if [ "$L" = data ]; then DED="$DATA_EXT"; else DED="$CAT_EXT"; fi
  assume "$ARN" "$TAX_EXT" og-i2-ac6-taxsma; echo "ASSUME_TAXSMA_$L rc=$ARC err=$AERR"
  assume "$ARN" "$DED" og-i2-ac6-dedicated; echo "ASSUME_DEDICATED_$L rc=$ARC err=$AERR arn=$AARN"
  CREDS=""
done
""" % (DATA_ARN, CAT_ARN)

    def grade(out):
        rows = []
        for L, role in (("data", DATA_ROLE), ("catalog", CAT_ROLE)):
            tx, dd = kv(out, "ASSUME_TAXSMA_" + L), kv(out, "ASSUME_DEDICATED_" + L)
            rows.append(("%s: assume with the Tax SMA ExternalId FAILS AccessDenied" % role,
                         tx.get("rc") not in (None, "0") and tx.get("err") == "(AccessDenied)", tx))
            rows.append(("%s: assume with its dedicated ExternalId SUCCEEDS" % role,
                         dd.get("rc") == "0" and ("assumed-role/%s/" % role) in dd.get("arn", ""), dd))
        return rows
    ok = host_arm(6, "DIFFERENCE (Tax SMA ExternalId vs dedicated ExternalId, same host, same minute)", body, grade)
    return verdict(6, bool(ok), "" if ok else "a difference arm is NOT OK (see NOT lines)")


def s3_body(role_arn: str, ext_var: str, session_name: str, cmds: str) -> str:
    return r"""
assume "%s" "$%s" %s; echo "ASSUME rc=$ARC err=$AERR arn=$AARN"
C="$CREDS"; CREDS=""
""" % (role_arn, ext_var, session_name) + cmds


def get_cmd(tag: str, key: str) -> str:
    return r"""
o=$(as_creds "$C" aws s3api get-object --region $R --bucket %s --key '%s' /dev/null --query ContentLength --output text 2>&1); rc=$?
if [ $rc -eq 0 ]; then echo "%s rc=0 content_length=$o bytes_kept=0"; else echo "%s rc=$rc err=$(errc "$o")"; fi
""" % (BUCKET, key, tag, tag)


def exists_locally(key: str) -> tuple:
    s3 = session().client("s3")
    try:
        h = s3.head_object(Bucket=BUCKET, Key=key)
        return True, "HeadObject 200 ContentLength %s LastModified %s (operator identity, positive control)" % (
            h.get("ContentLength"), h.get("LastModified"))
    except Exception as e:  # noqa: BLE001
        return False, "HeadObject %s (operator identity)" % err_code(e)


def ac7() -> int:
    ex, exd = exists_locally(SILVER_KEY)
    print("KEY: s3://%s/%s -- %s" % (BUCKET, SILVER_KEY, exd))
    body = s3_body(DATA_ARN, "DATA_EXT", "og-i2-ac7", get_cmd("GET_SILVER_AS_DATA_ROLE", SILVER_KEY)) + r"""
C=""; """ + get_cmd("GET_SILVER_AS_INSTANCE_ROLE_CONTROL", SILVER_KEY).replace('as_creds "$C" ', "")

    def grade(out):
        g, c = kv(out, "GET_SILVER_AS_DATA_ROLE"), kv(out, "GET_SILVER_AS_INSTANCE_ROLE_CONTROL")
        return [("the key exists (operator HeadObject)", ex, exd),
                ("data role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME")),
                ("data role GetObject on the silver key SUCCEEDS (body to /dev/null)", g.get("rc") == "0", g),
                ("control: the same GetObject under the bare instance role is denied (the success is the role's)",
                 c.get("rc") not in (None, "0") and c.get("err") == "(AccessDenied)", c)]
    ok = host_arm(7, "DATA ROLE GetObject on a listed silver prefix", body, grade)
    return verdict(7, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def denied_get_arm(n: int, title: str, role_arn: str, ext_var: str, key: str, allowed_control: tuple | None) -> int:
    ex, exd = exists_locally(key)
    print("KEY: s3://%s/%s -- %s" % (BUCKET, key, exd))
    body = s3_body(role_arn, ext_var, "og-i2-ac%d" % n, get_cmd("GET_TARGET", key))
    if allowed_control:
        body += get_cmd("GET_CONTROL", allowed_control[0])

    def grade(out):
        g = kv(out, "GET_TARGET")
        rows = [("the key exists (operator HeadObject), so a denial is not a 404", ex, exd),
                ("role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME")),
                ("GetObject on the target key is DENIED (AccessDenied)",
                 g.get("rc") not in (None, "0") and g.get("err") == "(AccessDenied)", g)]
        if allowed_control:
            c = kv(out, "GET_CONTROL")
            rows.append(("control in the same session: GetObject on %s succeeds" % allowed_control[1],
                         c.get("rc") == "0", c))
        return rows
    return host_arm(n, title, body, grade)


def ac8() -> int:
    ok = denied_get_arm(8, "DATA ROLE GetObject on a meta/complete/ key", DATA_ARN, "DATA_EXT", COMPLETE_KEY,
                        (SILVER_KEY, "a listed silver key"))
    return verdict(8, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def outside_key() -> str:
    s3 = session().client("s3")
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix=OUTSIDE_PREFIX, MaxKeys=1)
    keys = [o["Key"] for o in r.get("Contents", [])]
    return keys[0] if keys else OUTSIDE_PREFIX + "absent"


def ac9() -> int:
    key = outside_key()
    ok = denied_get_arm(9, "DATA ROLE GetObject on a key outside the six prefixes", DATA_ARN, "DATA_EXT", key,
                        (SILVER_KEY, "a listed silver key"))
    return verdict(9, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def ac10() -> int:
    key = "%sog-i2-denial-probe-%s.txt" % (DATA_PREFIXES[0], stamp())
    ex, exd = exists_locally(key)
    print("KEY: s3://%s/%s -- before: %s" % (BUCKET, key, exd))
    body = s3_body(DATA_ARN, "DATA_EXT", "og-i2-ac10", r"""
o=$(as_creds "$C" aws s3api put-object --region $R --bucket %s --key '%s' --body /dev/null 2>&1); rc=$?
if [ $rc -eq 0 ]; then echo "PUT rc=0 WRITE_SUCCEEDED=STOP"; else echo "PUT rc=$rc err=$(errc "$o")"; fi
""" % (BUCKET, key))

    def grade(out):
        p = kv(out, "PUT")
        after, afterd = exists_locally(key)
        if p.get("rc") == "0" or after:
            print("STOP: a probe write SUCCEEDED -- file an ARMED row naming 0.9.0_WK_NFRA_OPLGTW~1 as disarm owner")
        return [("the target key did not exist before", not ex, exd),
                ("role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME")),
                ("PutObject (empty body) under a listed prefix is DENIED (AccessDenied)",
                 p.get("rc") not in (None, "0") and p.get("err") == "(AccessDenied)", p),
                ("the key still does not exist after", not after, afterd)]
    ok = host_arm(10, "DATA ROLE PutObject under a listed prefix", body, grade)
    return verdict(10, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def list_cmd(tag: str, prefix: str) -> str:
    return r"""
o=$(as_creds "$C" aws s3api list-objects-v2 --region $R --bucket %s --prefix '%s' --max-keys 1 --query KeyCount --output text 2>&1); rc=$?
if [ $rc -eq 0 ]; then echo "%s rc=0 key_count=$o"; else echo "%s rc=$rc err=$(errc "$o")"; fi
""" % (BUCKET, prefix, tag, tag)


def ac11() -> int:
    body = s3_body(DATA_ARN, "DATA_EXT", "og-i2-ac11", list_cmd("LIST_OUTSIDE", META_LIST_PREFIX)
                   + list_cmd("LIST_NO_PREFIX", "") + list_cmd("LIST_CONTROL", DATA_PREFIXES[0]))

    def grade(out):
        a, b, c = kv(out, "LIST_OUTSIDE"), kv(out, "LIST_NO_PREFIX"), kv(out, "LIST_CONTROL")
        return [("role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME")),
                ("ListBucket with prefix %s is DENIED" % META_LIST_PREFIX,
                 a.get("rc") not in (None, "0") and a.get("err") == "(AccessDenied)", a),
                ("ListBucket with an empty prefix is DENIED",
                 b.get("rc") not in (None, "0") and b.get("err") == "(AccessDenied)", b),
                ("control in the same session: ListBucket with prefix %s succeeds" % DATA_PREFIXES[0],
                 c.get("rc") == "0", c)]
    ok = host_arm(11, "DATA ROLE ListBucket outside its prefix forms", body, grade)
    return verdict(11, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def ac12() -> int:
    body = s3_body(DATA_ARN, "DATA_EXT", "og-i2-ac12", r"""
for t in "CATALOG %s CAT_EXT" "SELF %s DATA_EXT" "ALYSSA_READ %s TAX_EXT"; do
  set -- $t; TAG=$1; ARN=$2; EV=$3
  o=$(as_creds "$C" aws sts assume-role --region $R --role-arn "$ARN" --role-session-name og-i2-ac12-chain --external-id "${!EV}" --output json 2>&1); rc=$?
  if [ $rc -eq 0 ]; then echo "CHAIN_$TAG rc=0 CHAINED=STOP"; else echo "CHAIN_$TAG rc=$rc err=$(errc "$o")"; fi
  o=""
done
""" % (CAT_ARN, DATA_ARN, "arn:aws:iam::%s:role/opal-mcp-emp-alyssa-read" % ACCOUNT))

    def grade(out):
        rows = [("data role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME"))]
        for tag in ("CATALOG", "SELF", "ALYSSA_READ"):
            c = kv(out, "CHAIN_" + tag)
            rows.append(("from the data-role session, AssumeRole on %s is DENIED" % tag,
                         c.get("rc") not in (None, "0") and c.get("err") == "(AccessDenied)", c))
        return rows
    ok = host_arm(12, "ROLE CHAINING from a data-role session (3 targets)", body, grade)
    return verdict(12, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def ac13() -> int:
    ex, exd = exists_locally(COMPLETE_KEY)
    print("KEY: s3://%s/%s -- %s" % (BUCKET, COMPLETE_KEY, exd))
    body = s3_body(CAT_ARN, "CAT_EXT", "og-i2-ac13", get_cmd("GET_COMPLETE", COMPLETE_KEY))

    def grade(out):
        g = kv(out, "GET_COMPLETE")
        return [("the key exists (operator HeadObject)", ex, exd),
                ("catalog role assumed", kv(out, "ASSUME").get("rc") == "0", kv(out, "ASSUME")),
                ("catalog role GetObject on the meta/complete/ key SUCCEEDS (body to /dev/null)", g.get("rc") == "0", g)]
    ok = host_arm(13, "CATALOG ROLE GetObject on a meta/complete/ key", body, grade)
    return verdict(13, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def ac14() -> int:
    ok = denied_get_arm(14, "CATALOG ROLE GetObject on a silver key", CAT_ARN, "CAT_EXT", SILVER_KEY,
                        (COMPLETE_KEY, "a meta/complete/ key"))
    return verdict(14, bool(ok), "" if ok else "NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC15 / AC16
def ac15() -> int:
    for p in (BP_PRE, BP_POST, APPLY_REC):
        if not os.path.isfile(p):
            print("MEASURED: %s absent" % rel(p))
            return verdict(15, False, "evidence absent: %s" % rel(p))
    pre, post, ap = load_json(BP_PRE), load_json(BP_POST), load_json(APPLY_REC)
    sess = session()
    t = now()
    text = sess.client("s3").get_bucket_policy(Bucket=BUCKET)["Policy"]
    import hashlib
    live = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print("SOURCES: %s read %s, %s read %s, apply %s..%s rc %s; live get-bucket-policy %s"
          % (rel(BP_PRE), pre["read_utc"], rel(BP_POST), post["read_utc"], ap["start_utc"], ap["end_utc"], ap["rc"], iso(t)))
    rows = [("pre read precedes the apply start", parse_ts(pre["read_utc"]) <= parse_ts(ap["start_utc"]),
             "%s <= %s" % (pre["read_utc"], ap["start_utc"])),
            ("post read follows the apply end", parse_ts(post["read_utc"]) >= parse_ts(ap["end_utc"]),
             "%s >= %s" % (post["read_utc"], ap["end_utc"])),
            ("the bracketed apply completed", ap.get("rc") == 0 and bool(ap.get("apply_complete")),
             "rc %s %s" % (ap.get("rc"), ap.get("apply_complete"))),
            ("sha256 before == sha256 after", pre["policy_sha256"] == post["policy_sha256"],
             "%s == %s" % (pre["policy_sha256"], post["policy_sha256"])),
            ("supplementary: live sha256 now == before", live == pre["policy_sha256"], live)]
    ok = print_rows(rows)
    return verdict(15, bool(ok), "" if ok else "NOT OK (see NOT lines)")


def section(text: str, header: str) -> str:
    if header not in text:
        return ""
    body = text.split(header, 1)[1]
    m = re.search(r"^## ", body, re.M)
    return body[:m.start()] if m else body


def ac16() -> int:
    if not os.path.isfile(RESULT):
        return verdict(16, False, "result file absent")
    with open(RESULT, encoding="utf-8") as fh:
        text = fh.read()
    print("SOURCE: %s (%d bytes, %d lines)" % (rel(RESULT), len(text), len(text.splitlines())))
    sim, live = section(text, SIM_SECTION), section(text, LIVE_SECTION)
    sim_ids = sorted(set(re.findall(r"OGI2-AC\d+", sim)))
    live_ids = sorted(set(re.findall(r"OGI2-AC\d+", live)))
    live_cmds = re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", live)
    rows = [("labelled simulation section present: %r" % SIM_SECTION, bool(sim.strip()), "%d chars" % len(sim)),
            ("labelled live-exercised section present: %r" % LIVE_SECTION, bool(live.strip()), "%d chars" % len(live)),
            ("the two sections are separate (headers once each, distinct bodies)",
             text.count(SIM_SECTION) == 1 and text.count(LIVE_SECTION) == 1 and sim.strip() != live.strip(), True),
            ("simulation section carries simulate-principal-policy results", "simulate-principal-policy" in sim
             and ("allowed" in sim and "explicitDeny" in sim), sim_ids),
            ("simulation section carries no SSM command id", not re.search(
                r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", sim), True),
            ("live section cites the on-host criteria AC6..AC14 (9 of 9)",
             all("OGI2-AC%d" % i in live_ids for i in range(6, 15)), live_ids),
            ("live section cites an SSM command id per on-host criterion (>= 9)", len(set(live_cmds)) >= 9,
             "%d distinct" % len(set(live_cmds)))]
    ok = print_rows(rows)
    return verdict(16, bool(ok), "" if ok else "NOT OK (see NOT lines)")


ARMS = {1: ac1, 2: ac2, 3: ac3, 4: ac4, 5: ac5, 6: ac6, 7: ac7, 8: ac8, 9: ac9, 10: ac10, 11: ac11, 12: ac12,
        13: ac13, 14: ac14, 15: ac15, 16: ac16}


def main(argv: list) -> int:
    m = re.fullmatch(r"AC(\d+)", argv[1]) if len(argv) == 2 else None
    if not m or int(m.group(1)) not in ARMS:
        print("usage: og_i2.py AC<n>   n = 1..16")
        return 2
    n = int(m.group(1))
    print("OG-i-2 probe AC%d at %s (repo %s)" % (n, iso(now()), rel(REPO) or "."))
    try:
        return ARMS[n]()
    except Exception as e:  # noqa: BLE001 -- the arm's failure is itself the recorded output
        print("ERROR: %s: %s" % (type(e).__name__, err_code(e)))
        return verdict(n, False, "arm raised %s" % err_code(e))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
