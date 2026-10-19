#!/usr/bin/env python
"""OG-mg-2 Phase A: read, prepare, pre-flight. NO WRITE of any kind (no DynamoDB write, no SSM, no S3 write). COUNTS, ROLES, KEYS AND HASHES ONLY in the repo: no account id, tid, oid or e-mail is written to a repo file or printed.
Candidates (which hold ids) live in X = %LOCALAPPDATA%/opal/og-salt/mg2/ (off-repo).
  python mg2_phasea.py        (repository root)
Writes W/MG2_BEFORE.json, W/MG2_DIFF.json, W/MG2_PREFLIGHT_DECIDE.json, W/MG2_FACTS.json (extra facts for the ask) and X/<role>_candidate.json.
The CURRENT account set of a master is the distinct `account_id` of schwab/<master>/silver/dim_balance/date=<latest complete>/ (one row per account); the latest complete date is the newest meta/complete/date=*.json marker."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys

REPO = os.getcwd()
GW = os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
os.environ.setdefault("MOCK_GRAPH", "1")

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from boto3.dynamodb.types import TypeDeserializer  # noqa: E402

from app import access_state as acs  # noqa: E402
from app import data_entitlement as de  # noqa: E402
from ops import schwab_entitlement_admin as adm  # noqa: E402

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "mg2")
os.makedirs(X, exist_ok=True)
TABLE = "gateway-access-state-table"
BUCKET = "opal-data-assets"
ROLES = ("andrew", "alyssa")
TOOLS4 = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")


def num(o):
    return int(o) if o == int(o) else float(o)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=num).encode("utf-8")).hexdigest()


def save(name, obj):
    io.open(W + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1, default=num) + "\n")


sts = boto3.client("sts")
cred = sts.assume_role(RoleArn="arn:aws:iam::313476888478:role/opal-gateway-access-admin", RoleSessionName="og-mg2-phase-a", DurationSeconds=3600)["Credentials"]
op_sess = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"], aws_session_token=cred["SessionToken"], region_name="us-east-1")
ddb_me = boto3.client("dynamodb", region_name="us-east-1")
td = TypeDeserializer()
read_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# 1. strongly consistent, fully paginated scan (the CALLING principal reads; the operator role writes only)
items, kw, pages = [], {"TableName": TABLE, "ConsistentRead": True}, 0
resp = {"LastEvaluatedKey": True}
while "LastEvaluatedKey" in resp:
    resp = ddb_me.scan(**kw)
    pages += 1
    items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
    if "LastEvaluatedKey" in resp:
        kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
pol = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
profiles = [i for i in pol if i.get("record_type") == "principal_profile"]
by_type = {}
for i in pol:
    by_type[i.get("record_type")] = by_type.get(i.get("record_type"), 0) + 1

store = acs.AccessState(client=ddb_me)
found = {}
for role in ROLES:
    cands = [p for p in profiles if p.get("status") == "active" and str(p.get("email", "")).lower().split("@")[0] == role]
    if len(cands) != 1:
        raise SystemExit("STOP: role %s resolves to %d active profile(s), not 1" % (role, len(cands)))
    found[role] = cands[0]

# 2. the current account set per master, from S3 (the method stated in the ask)
s3 = boto3.client("s3")
state = {}
masters_needed = set()
for role in ROLES:
    p = found[role]
    profile, grant = adm.current_state(store, p["tid"], p["oid"])
    if profile is None or grant is None or grant.status != "active":
        raise SystemExit("STOP: role %s has no active grant in force" % role)
    state[role] = (profile, grant)
    masters_needed |= set(grant.scope.masters)

current, latest = {}, {}
for m in sorted(masters_needed):
    marks = sorted(o["Key"].rsplit("/", 1)[-1] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/meta/complete/" % m).get("Contents", []))
    latest[m] = marks[-1][len("date="):-len(".json")]
    pre = "schwab/%s/silver/dim_balance/date=%s/" % (m, latest[m])
    ids = set()
    objs = [o for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=pre).get("Contents", []) if o["Key"].endswith(".parquet")]
    for o in objs:
        f = pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
        ids.update(str(x) for x in f.read(columns=["account_id"]).column(0).to_pylist() if x is not None)
    current[m] = ids
    if not ids:
        raise SystemExit("STOP: master %s read 0 accounts" % m)

# 3. candidates, diffs, prepare() under the operator role (validates and writes nothing)
op_store = acs.AccessState(client=op_sess.client("dynamodb"))
before_rec, diff_rec, facts = [], {}, {"deny": {}}
cand_scope, plans = {}, {}
for role in ROLES:
    p = found[role]
    profile, grant = state[role]
    gitem = store.get(de.grant_key(p["tid"], p["oid"], profile.grant_revision))
    stored_scope = gitem["scope"]
    scope_raw = adm._scope_to_raw(grant.scope)
    sans_stored = {k: v for k, v in stored_scope.items() if k != "accounts"}
    sans_round = {k: v for k, v in scope_raw.items() if k != "accounts"}
    new_scope = json.loads(json.dumps(scope_raw))
    new_scope["accounts"] = {m: sorted(current[m]) for m in sorted(grant.scope.masters)}
    raw = {"tid": p["tid"], "oid": p["oid"], "email": p["email"], "scope": new_scope}
    io.open(os.path.join(X, "%s_candidate.json" % role), "w", encoding="utf-8", newline="\n").write(json.dumps(raw))
    buf = io.StringIO()
    plan = adm.prepare(op_store, raw, adm.load_contract(None), out=buf)
    plans[role] = plan
    before_n = {m: len(grant.scope.accounts.get(m, ())) for m in sorted(grant.scope.masters)}
    cur_n = {m: len(current[m]) for m in sorted(grant.scope.masters)}
    added = {m: len(current[m] - set(grant.scope.accounts.get(m, ()))) for m in sorted(grant.scope.masters)}
    removed = {m: len(set(grant.scope.accounts.get(m, ())) - current[m]) for m in sorted(grant.scope.masters)}
    old_n = json.loads(json.dumps(scope_raw, default=num))
    changed = sorted(k for k in set(old_n) | set(new_scope) if json.dumps(old_n.get(k), sort_keys=True) != json.dumps(new_scope.get(k), sort_keys=True))
    stored_vs_round = sha(sans_stored) == sha(sans_round)
    before_rec.append({"role": role, "pk_hash": hashlib.sha256(str(p["pk"]).encode()).hexdigest()[:10], "profile_revision": int(profile.revision), "grant_revision": int(profile.grant_revision),
                       "masters": sorted(grant.scope.masters), "accounts_before": before_n, "accounts_current": cur_n, "scope_sans_accounts_sha256": sha(sans_stored),
                       "scope_sans_accounts_roundtrip_equals_stored": stored_vs_round, "operations": sorted(grant.scope.operations)})
    diff_rec[role] = {"changed_keys": changed, "added": added, "removed": removed}
    ek = [acs.email_deny_key(e) for e in plan.deny_emails]
    facts["deny"][role] = {"deny_emails_in_plan": len(plan.deny_emails), "email_deny_records_exist_now": [store.get(k) is not None for k in ek]}
    cand_scope[role] = (profile, grant, new_scope)

save("MG2_BEFORE.json", {"read_at": read_at, "denominator": {"policy_items_scanned": len(pol), "principal_profiles": len(profiles), "all_items_scanned": len(items), "scan_pages": pages, "by_record_type": by_type},
                         "principals": before_rec, "current_set_method": {"source": "distinct account_id of dim_balance (one row per account) at the latest complete date, per master",
                                                                         "bucket_prefix": "opal-data-assets / schwab/<master>/silver/dim_balance/date=<latest complete>/", "latest_complete_date": latest,
                                                                         "latest_complete_basis": "newest schwab/<master>/meta/complete/date=*.json marker"}})
save("MG2_DIFF.json", diff_rec)

# 4. decide() pre-flight on the CANDIDATES (in process, no network, no write)
dec = {}
for role in ROLES:
    profile, grant, new_scope = cand_scope[role]
    cscope = de.parse_scope(new_scope)
    prof = de.Profile(profile.tid, profile.oid, "active", profile.revision + 1, grant.revision + 1)
    gr = de.Grant(profile.tid, profile.oid, grant.revision + 1, "active", cscope)
    acc = de.Access(True, prof, gr, de.allowed_tools(prof, gr))
    admit = {t: de.decide(t, acc) is None for t in TOOLS4}
    dec[role] = {"admit": admit, "refuse": {"schwab_prepare_download": de.decide("schwab_prepare_download", acc) is not None}}
save("MG2_PREFLIGHT_DECIDE.json", dec)

# 5. comp-iam: re-simulate the writes under the operator role
iam = boto3.client("iam")
role_arn = iam.get_role(RoleName="opal-gateway-access-admin")["Role"]["Arn"]
table_arn = "arn:aws:dynamodb:us-east-1:313476888478:table/" + TABLE
sim = {}
for act in ("dynamodb:PutItem", "dynamodb:UpdateItem"):
    r = iam.simulate_principal_policy(PolicySourceArn=role_arn, ActionNames=[act], ResourceArns=[table_arn],
                                      ContextEntries=[{"ContextKeyName": "dynamodb:LeadingKeys", "ContextKeyValues": ["POLICY#x"], "ContextKeyType": "stringList"}])["EvaluationResults"][0]["EvalDecision"]
    sim[act] = r
facts["simulate_principal_policy"] = sim
facts["operator_role_assumed"] = True
facts["roles_resolved"] = {r: "exactly one active profile by e-mail prefix" for r in ROLES}
facts["ops_by_role"] = {b["role"]: b["operations"] for b in before_rec}
facts["current_counts_note"] = "counts only"
save("MG2_FACTS.json", facts)
print(json.dumps({"before": [{k: b[k] for k in ("role", "pk_hash", "profile_revision", "grant_revision", "masters", "accounts_before", "accounts_current", "scope_sans_accounts_roundtrip_equals_stored")} for b in before_rec],
                  "diff": diff_rec, "decide": dec, "facts": facts, "denominator": {"policy": len(pol), "profiles": len(profiles), "types": by_type}, "latest": latest}, indent=1, default=num))
