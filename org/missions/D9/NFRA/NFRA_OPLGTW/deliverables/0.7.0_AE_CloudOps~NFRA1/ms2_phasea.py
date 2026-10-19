#!/usr/bin/env python
"""OG-ms-2 Phase A: read, prepare, pre-flight. NO WRITE of any kind. COUNTS, ROLES, KEYS AND HASHES ONLY in the repo: no account id, tid, oid or e-mail is written or printed.
The candidate (which holds ids) lives in X = %LOCALAPPDATA%/opal/og-salt/ms2/ (off-repo).
  python ms2_phasea.py        (repository root)
Writes W/MS2_BEFORE.json, W/MS2_DIFF.json, W/MS2_PREFLIGHT_DECIDE.json, W/MS2_FACTS.json and X/alyssa_candidate.json.
The new master's current account set is the distinct `account_id` of schwab/08403355/silver/dim_balance/date=<latest complete>/ (the method OG-mg-2 used)."""
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
X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "ms2")
os.makedirs(X, exist_ok=True)
TABLE, BUCKET, NEW = "gateway-access-state-table", "opal-data-assets", "08403355"
TOOLS4 = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
DATASETS = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def num(o):
    return int(o) if o == int(o) else float(o)


def sha_json(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=num).encode("utf-8")).hexdigest()


def sha_ids(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def save(name, obj):
    io.open(W + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1, default=num) + "\n")


sts = boto3.client("sts")
cred = sts.assume_role(RoleArn="arn:aws:iam::313476888478:role/opal-gateway-access-admin", RoleSessionName="og-ms2-phase-a", DurationSeconds=3600)["Credentials"]
op = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"], aws_session_token=cred["SessionToken"], region_name="us-east-1")
me = boto3.client("dynamodb", region_name="us-east-1")
td = TypeDeserializer()
read_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

items, kw, pages = [], {"TableName": TABLE, "ConsistentRead": True}, 0
resp = {"LastEvaluatedKey": True}
while "LastEvaluatedKey" in resp:
    resp = me.scan(**kw)
    pages += 1
    items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
    if "LastEvaluatedKey" in resp:
        kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
pol = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
profiles = [i for i in pol if i.get("record_type") == "principal_profile"]
by_type = {}
for i in pol:
    by_type[i.get("record_type")] = by_type.get(i.get("record_type"), 0) + 1


def role_profile(role):
    c = [p for p in profiles if p.get("status") == "active" and str(p.get("email", "")).lower().split("@")[0] == role]
    if len(c) != 1:
        raise SystemExit("STOP: role %s resolves to %d active profiles" % (role, len(c)))
    return c[0]


pa, pn = role_profile("alyssa"), role_profile("andrew")
store = acs.AccessState(client=me)
profile, grant = adm.current_state(store, pa["tid"], pa["oid"])
if grant is None or grant.status != "active":
    raise SystemExit("STOP: alyssa has no active grant in force")
gitem = store.get(de.grant_key(pa["tid"], pa["oid"], profile.grant_revision))
stored_scope = gitem["scope"]
old_masters = sorted(grant.scope.masters)
if NEW in old_masters:
    raise SystemExit("STOP: the master is already in her grant")
if NEW not in de.MASTERS:
    raise SystemExit("STOP: the trunk code does not list the master in MASTERS")

# (a) the only 0840 prefix, (b) the four datasets with data at the latest complete date
s3 = boto3.client("s3")
kids = [p["Prefix"].split("/")[1] for p in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/", Delimiter="/").get("CommonPrefixes", [])]
only_0840 = [k for k in kids if k.startswith("0840")]
marks = sorted(o["Key"].rsplit("/", 1)[-1] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/meta/complete/" % NEW).get("Contents", []))
latest = marks[-1][len("date="):-len(".json")]
table_objects, current = {}, set()
for t in DATASETS:
    objs = [o for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/silver/%s/date=%s/" % (NEW, t, latest)).get("Contents", []) if o["Key"].endswith(".parquet")]
    table_objects[t] = len(objs)
    if t == "dim_balance":
        for o in objs:
            f = pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
            current.update(str(x) for x in f.read(columns=["account_id"]).column(0).to_pylist() if x is not None)
if only_0840 != [NEW] or not all(table_objects.values()) or not current:
    raise SystemExit("STOP: prefix/dataset/account confirmation failed: %s %s %d" % (only_0840, table_objects, len(current)))

# candidate: masters and accounts only
scope_raw = adm._scope_to_raw(grant.scope)
new_scope = json.loads(json.dumps(scope_raw))
new_scope["masters"] = sorted(set(scope_raw["masters"]) | {NEW})
new_scope["accounts"][NEW] = sorted(current)
raw = {"tid": pa["tid"], "oid": pa["oid"], "email": pa["email"], "scope": new_scope}
io.open(os.path.join(X, "alyssa_candidate.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(raw))
op_store = acs.AccessState(client=op.client("dynamodb"))
buf = io.StringIO()
plan = adm.prepare(op_store, raw, adm.load_contract(None), out=buf)
old_n = json.loads(json.dumps(scope_raw, default=num))
changed = sorted(k for k in set(old_n) | set(new_scope) if json.dumps(old_n.get(k), sort_keys=True) != json.dumps(new_scope.get(k), sort_keys=True))
others_same = all(new_scope["accounts"][m] == scope_raw["accounts"][m] for m in old_masters)

sans_stored = {k: v for k, v in stored_scope.items() if k not in ("masters", "accounts")}
sans_candidate = {k: v for k, v in new_scope.items() if k not in ("masters", "accounts")}
before = {"read_at": read_at,
          "denominator": {"policy_items_scanned": len(pol), "principal_profiles": len(profiles), "all_items_scanned": len(items), "scan_pages": pages, "by_record_type": by_type},
          "principal": {"role": "alyssa", "pk_hash": hashlib.sha256(str(pa["pk"]).encode()).hexdigest()[:10], "profile_revision": int(profile.revision), "grant_revision": int(profile.grant_revision),
                        "masters": old_masters, "accounts_before": {m: len(grant.scope.accounts.get(m, ())) for m in old_masters},
                        "accounts_sha256": {m: sha_ids(grant.scope.accounts.get(m, ())) for m in old_masters},
                        "new_master": NEW, "new_master_accounts_current": len(current), "new_master_latest_complete_date": latest, "new_master_accounts_sha256": sha_ids(current),
                        "scope_sans_masters_accounts_sha256": sha_json(sans_stored), "scope_sans_masters_accounts_roundtrip_equals_stored": sha_json(sans_stored) == sha_json(sans_candidate),
                        "operations": sorted(grant.scope.operations)}}
save("MS2_BEFORE.json", before)
save("MS2_DIFF.json", {"alyssa": {"changed_keys": changed, "masters_added": sorted(set(new_scope["masters"]) - set(old_masters)), "added": {NEW: len(current)}, "other_masters_accounts_unchanged": others_same}})

# decide() pre-flight on the CANDIDATE, in process
cscope = de.parse_scope(new_scope)
prof = de.Profile(profile.tid, profile.oid, "active", profile.revision + 1, profile.grant_revision + 1)
gr = de.Grant(profile.tid, profile.oid, profile.grant_revision + 1, "active", cscope)
acc = de.Access(True, prof, gr, de.allowed_tools(prof, gr))
admit = {t: de.decide(t, acc) is None for t in TOOLS4}
refuse = {"schwab_prepare_download": de.decide("schwab_prepare_download", acc) is not None}
ops = {"list": "schwab_list_files", "describe": "schwab_describe_dataset", "query": "schwab_query"}


def scope_answers(scope, master):
    out = {}
    for op_name in ("list", "describe", "query", "download_filtered"):
        out[op_name] = [bool(de.check_scope(scope, {"operation": op_name, "master": master, "dataset": d})) for d in sorted(scope.datasets)]
    return out


new_ans = scope_answers(cscope, NEW)
in_scope = all(not any(new_ans[o]) for o in ops) and all(new_ans["download_filtered"])
existing_same = all(scope_answers(cscope, m) == scope_answers(grant.scope, m) for m in old_masters)
save("MS2_PREFLIGHT_DECIDE.json", {"alyssa": {"admit": admit, "refuse": refuse, "master_in_scope": bool(NEW in cscope.masters and in_scope), "download_refused_by_scope_on_new_master": all(new_ans["download_filtered"]),
                                               "existing_masters_answers_unchanged": existing_same}})

# comp-iam and the email_deny fact
iam = boto3.client("iam")
role_arn = iam.get_role(RoleName="opal-gateway-access-admin")["Role"]["Arn"]
table_arn = "arn:aws:dynamodb:us-east-1:313476888478:table/" + TABLE
sim = {}
for act in ("dynamodb:PutItem", "dynamodb:UpdateItem"):
    sim[act] = iam.simulate_principal_policy(PolicySourceArn=role_arn, ActionNames=[act], ResourceArns=[table_arn],
                                             ContextEntries=[{"ContextKeyName": "dynamodb:LeadingKeys", "ContextKeyValues": ["POLICY#x"], "ContextKeyType": "stringList"}])["EvaluationResults"][0]["EvalDecision"]
andrew_profile, andrew_grant = adm.current_state(store, pn["tid"], pn["oid"])
save("MS2_FACTS.json", {"only_0840_prefix": only_0840, "schwab_master_prefixes": len(kids), "completion_markers": len(marks), "table_objects_at_latest_complete": table_objects, "latest_complete_date": latest,
                        "simulate_principal_policy": sim, "deny_emails_in_plan": len(plan.deny_emails), "alyssa_email_deny_record_exists_now": [store.get(acs.email_deny_key(e)) is not None for e in plan.deny_emails],
                        "email_deny_records_in_store": by_type.get("email_deny", 0), "andrew_grant_revision": int(andrew_profile.grant_revision), "trunk_masters_lists_new_master": NEW in de.MASTERS,
                        "prepare_accepted": True})
print(json.dumps({"changed_keys": changed, "others_same": others_same, "added": len(current), "latest": latest, "tables": table_objects, "only_0840": only_0840, "decide": {"admit": admit, "refuse": refuse, "master_in_scope": bool(NEW in cscope.masters and in_scope),
                  "existing_same": existing_same}, "sim": sim, "deny_exists": [store.get(acs.email_deny_key(e)) is not None for e in plan.deny_emails], "rev": [int(profile.revision), int(profile.grant_revision)], "andrew_rev": int(andrew_profile.grant_revision)}, default=num))
