#!/usr/bin/env python
"""OG-ms-2 Phase B: re-read step 1 (nothing may have moved), activate ALYSSA's candidate only through the module's `activate` under `opal-gateway-access-admin`
(Andrew's grant is NOT touched), read back strongly consistent. COUNTS, ROLES AND HASHES ONLY in the repo; the module prints a scope diff holding ids, which is captured in memory and NEVER printed or saved.
  python ms2_phaseb.py        (repository root)
Exit 0 only when the activation is read back as required; any other state prints a STOP line and writes nothing further.
The decide() read-back of the DEPLOYED tree is the separate host run: python ms2_host_decide.py post W/ms2_pb/post.json."""
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
TABLE, BUCKET, NEW = "gateway-access-state-table", "opal-data-assets", "08403355"
SRC = ("org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261019_195xZ_ALYSSA_SCHWAB_MASTER_0840_ADD_TO_ENTITLEMENTS.md, relayed by 1.0.0_SA_CTO~Z msg 36102 and ruling (B) msg 36104; "
       "OG-ms-2 halves CTO 355bf20473, COO J1-J7 and CVO 10dfd87598, ask sha256 30351bdddf2d, GO 36159")


def num(o):
    return int(o) if o == int(o) else float(o)


def sha_json(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=num).encode("utf-8")).hexdigest()


def sha_ids(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def stop(msg):
    print("STOP: " + msg)
    raise SystemExit(3)


def scan(client):
    items, kw = [], {"TableName": TABLE, "ConsistentRead": True}
    resp = {"LastEvaluatedKey": True}
    td = TypeDeserializer()
    while "LastEvaluatedKey" in resp:
        resp = client.scan(**kw)
        items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
        if "LastEvaluatedKey" in resp:
            kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    return items


def role_profile(items, role):
    c = [i for i in items if i.get("record_type") == "principal_profile" and i.get("status") == "active" and str(i.get("email", "")).lower().split("@")[0] == role]
    if len(c) != 1:
        stop("role %s resolves to %d active profiles" % (role, len(c)))
    return c[0]


def current_new_set(s3):
    marks = sorted(o["Key"].rsplit("/", 1)[-1] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/meta/complete/" % NEW).get("Contents", []))
    latest = marks[-1][len("date="):-len(".json")]
    ids = set()
    for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/silver/dim_balance/date=%s/" % (NEW, latest)).get("Contents", []):
        if o["Key"].endswith(".parquet"):
            f = pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
            ids.update(str(x) for x in f.read(columns=["account_id"]).column(0).to_pylist() if x is not None)
    return latest, ids


before = json.load(io.open(W + "MS2_BEFORE.json", encoding="utf-8"))["principal"]
mg2 = {r["role"]: r for r in json.load(io.open(W + "MG2_BEFORE.json", encoding="utf-8"))["principals"]}
me = boto3.client("dynamodb", region_name="us-east-1")
store = acs.AccessState(client=me)

# ---- step 6: re-read step 1; nothing may have moved
items = scan(me)
pa, pn = role_profile(items, "alyssa"), role_profile(items, "andrew")
if int(pa["revision"]) != before["profile_revision"] or int(pa["grant_revision"]) != before["grant_revision"]:
    stop("alyssa moved since Phase A (revision %s/%s against %s/%s): re-cut Phase A once" % (pa["revision"], pa["grant_revision"], before["profile_revision"], before["grant_revision"]))
if int(pn["grant_revision"]) != int(mg2["andrew"]["grant_revision"]):
    stop("andrew's grant revision moved")
profile0, grant0 = adm.current_state(store, pa["tid"], pa["oid"])
gitem = store.get(de.grant_key(pa["tid"], pa["oid"], profile0.grant_revision))
for m, h in before["accounts_sha256"].items():
    if sha_ids(grant0.scope.accounts.get(m, ())) != h:
        stop("alyssa's account set for master %s moved since Phase A" % m)
if sha_json({k: v for k, v in gitem["scope"].items() if k not in ("masters", "accounts")}) != before["scope_sans_masters_accounts_sha256"]:
    stop("alyssa's scope (without masters and accounts) moved since Phase A")
cand_path = os.path.join(X, "alyssa_candidate.json")
raw = json.load(io.open(cand_path, encoding="utf-8"))
latest, ids = current_new_set(boto3.client("s3"))
if latest != before["new_master_latest_complete_date"] or sha_ids(ids) != before["new_master_accounts_sha256"] or sorted(ids) != sorted(raw["scope"]["accounts"][NEW]):
    stop("the current S3 set of the new master moved since Phase A: re-cut")
print("step 6 re-read: nothing moved (alyssa revisions %s/%s; new master %d accounts at %s equal the candidate; andrew grant revision %s)" % (pa["revision"], pa["grant_revision"], len(ids), latest, pn["grant_revision"]))

# ---- step 7: the ONE write, through the module's CLI main(), under the operator role
cred = boto3.client("sts").assume_role(RoleArn="arn:aws:iam::313476888478:role/opal-gateway-access-admin", RoleSessionName="og-ms2-phase-b", DurationSeconds=3600)["Credentials"]
op = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"], aws_session_token=cred["SessionToken"], region_name="us-east-1")
buf = io.StringIO()
at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rc = adm.main(["activate", "--candidate", cand_path, "--approver", "Andrew Berman", "--source-authorization", SRC, "--summary", "OG-ms-2: add Schwab master 08403355 to alyssa's grant (scope.masters and scope.accounts[08403355] only)", "--at", at],
              store=acs.AccessState(client=op.client("dynamodb")), sts_client=op.client("sts"), out=buf)
lines = [ln for ln in buf.getvalue().splitlines() if ln.startswith(("ACTIVATED", "REFUSED"))]
line = lines[-1] if lines else "NO RESULT LINE"
print("alyssa:", line, "(rc=%s)" % rc)
io.open(W + "MS2_WRITE.md", "w", encoding="utf-8", newline="\n").write(
    "# OG-ms-2 Phase B -- write\n\nApplier: `0.7.0_AE_CloudOps~NFRA1`. Written at %s under `opal-gateway-access-admin`, approver `Andrew Berman`, GO msg 36159, ask sha256 `30351bdddf2d`.\n\n"
    "- alyssa (pk_hash `%s`): `%s`\n- andrew: NOT WRITTEN (not in this order); his grant revision stays %s.\n\nThe module's scope diff holds account ids and was neither printed nor saved.\n" % (at, before["pk_hash"], line, mg2["andrew"]["grant_revision"]))
if not line.startswith("ACTIVATED") or rc != 0:
    stop("the activation did not report ACTIVATED: %s" % line)

# ---- step 8: strongly consistent read-back (the DEPLOYED tree's decide() is the separate host run)
items2 = scan(me)
pa2, pn2 = role_profile(items2, "alyssa"), role_profile(items2, "andrew")
prof1, grant1 = adm.current_state(acs.AccessState(client=me), pa2["tid"], pa2["oid"])
g1 = acs.AccessState(client=me).get(de.grant_key(pa2["tid"], pa2["oid"], prof1.grant_revision))
counts = {m: len(v) for m, v in grant1.scope.accounts.items()}
old_same = all(sha_ids(grant1.scope.accounts.get(m, ())) == h for m, h in before["accounts_sha256"].items())
rest_same = sha_json({k: v for k, v in g1["scope"].items() if k not in ("masters", "accounts")}) == before["scope_sans_masters_accounts_sha256"]
after = {"read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "policy_items_scanned": sum(1 for i in items2 if str(i.get("pk", "")).startswith("POLICY#")),
         "alyssa": {"profile_status": prof1.status, "profile_revision": int(prof1.revision), "grant_status": grant1.status, "grant_revision": int(prof1.grant_revision), "masters": len(grant1.scope.masters), "accounts": counts,
                    "new_master_count_equals_current": counts.get(NEW) == before["new_master_accounts_current"], "other_masters_accounts_unchanged": old_same, "rest_of_scope_unchanged": rest_same},
         "andrew": {"grant_revision_unchanged": int(pn2["grant_revision"]) == int(mg2["andrew"]["grant_revision"])},
         "email_deny_records_in_store": sum(1 for i in items2 if i.get("record_type") == "email_deny")}
io.open(W + "MS2_AFTER.json", "w", encoding="utf-8", newline="\n").write(json.dumps(after, indent=1, default=num) + "\n")
ok = (after["alyssa"]["profile_status"] == "active" and after["alyssa"]["grant_status"] == "active" and after["alyssa"]["grant_revision"] > before["grant_revision"] and after["alyssa"]["masters"] == 3
      and after["alyssa"]["new_master_count_equals_current"] and old_same and rest_same and after["andrew"]["grant_revision_unchanged"])
print(json.dumps({"alyssa": after["alyssa"], "andrew": after["andrew"], "email_deny_records": after["email_deny_records_in_store"], "READBACK_OK": ok}, default=num))
raise SystemExit(0 if ok else 4)
