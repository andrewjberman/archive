#!/usr/bin/env python
"""OG-mg-2 Phase B (option (b), COO half G1-G6): re-read step 1 (nothing may have moved), activate ALYSSA's candidate only through the module's `activate` under `opal-gateway-access-admin` (Andrew's record is HELD, not touched),
read back live, decide() on the LIVE grant. COUNTS, ROLES AND HASHES ONLY in the repo; the module prints a scope diff holding ids, which is captured in memory and NEVER printed or saved.
  python mg2_phaseb.py        (repository root)
Exit 0 only when the activation is read back as required; any other state prints a STOP line and writes nothing further."""
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
TABLE, BUCKET = "gateway-access-state-table", "opal-data-assets"
SRC = ("org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_172xZ_ALYSSA_3PM_SCHWAB_TEST_SENDS_YES_ROSTER_AS_OPEN_CALLS_SCHWAB_FULL_ACCOUNTS.md @65a05f6658; "
       "OG-mg-2 halves CTO, COO (option b) and CVO, ask sha256 b1244d6c235a")
TOOLS4 = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")


def num(o):
    return int(o) if o == int(o) else float(o)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=num).encode("utf-8")).hexdigest()


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


before = json.load(io.open(W + "MG2_BEFORE.json", encoding="utf-8"))
bef = {r["role"]: r for r in before["principals"]}
me = boto3.client("dynamodb", region_name="us-east-1")
store = acs.AccessState(client=me)

# ---- G2: re-read step 1; nothing may have moved
items = scan(me)
prof = {r: role_profile(items, r) for r in ("andrew", "alyssa")}
for r in ("andrew", "alyssa"):
    p = prof[r]
    if int(p["revision"]) != bef[r]["profile_revision"] or int(p["grant_revision"]) != bef[r]["grant_revision"]:
        stop("%s moved since Phase A (revision %s/%s against %s/%s): re-cut Phase A" % (r, p["revision"], p["grant_revision"], bef[r]["profile_revision"], bef[r]["grant_revision"]))
p = prof["alyssa"]
profile0, grant0 = adm.current_state(store, p["tid"], p["oid"])
gitem = store.get(de.grant_key(p["tid"], p["oid"], profile0.grant_revision))
if sha({k: v for k, v in gitem["scope"].items() if k != "accounts"}) != bef["alyssa"]["scope_sans_accounts_sha256"]:
    stop("alyssa's scope (without accounts) moved since Phase A")
cand_path = os.path.join(X, "alyssa_candidate.json")
raw = json.load(io.open(cand_path, encoding="utf-8"))
s3 = boto3.client("s3")
now_counts = {}
for m, want in sorted(raw["scope"]["accounts"].items()):
    marks = sorted(o["Key"].rsplit("/", 1)[-1] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/meta/complete/" % m).get("Contents", []))
    latest = marks[-1][len("date="):-len(".json")]
    ids = set()
    for o in s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/silver/dim_balance/date=%s/" % (m, latest)).get("Contents", []):
        if o["Key"].endswith(".parquet"):
            f = pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
            ids.update(str(x) for x in f.read(columns=["account_id"]).column(0).to_pylist() if x is not None)
    now_counts[m] = len(ids)
    if sorted(ids) != sorted(want) or latest != before["current_set_method"]["latest_complete_date"][m]:
        stop("the current S3 set of master %s moved since Phase A: re-cut" % m)
print("G2 re-read: nothing moved (alyssa revisions %s/%s; S3 sets equal the candidate: %s)" % (p["revision"], p["grant_revision"], now_counts))

# ---- the ONE write: Alyssa's activation through the module's CLI main(), under the operator role
sts = boto3.client("sts")
cred = sts.assume_role(RoleArn="arn:aws:iam::313476888478:role/opal-gateway-access-admin", RoleSessionName="og-mg2-phase-b", DurationSeconds=3600)["Credentials"]
op = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"], aws_session_token=cred["SessionToken"], region_name="us-east-1")
buf = io.StringIO()
at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rc = adm.main(["activate", "--candidate", cand_path, "--approver", "Andrew Berman", "--source-authorization", SRC, "--summary", "OG-mg-2: alyssa's Schwab grant re-activated at each granted master's current account set (only scope.accounts changes)", "--at", at],
              store=acs.AccessState(client=op.client("dynamodb")), sts_client=op.client("sts"), out=buf)
lines = [ln for ln in buf.getvalue().splitlines() if ln.startswith(("ACTIVATED", "REFUSED"))]
line = lines[-1] if lines else "NO RESULT LINE"
print("alyssa:", line, "(rc=%s)" % rc)
held = "Andrew's grant is HELD under option (b) (COO half G3; CTO half): activating it re-creates his email_deny record, which the legacy consent sign-in enforces, and removing it is a delete this order forbids. His grant revision is unchanged (%s). Follow-on order after the session." % bef["andrew"]["grant_revision"]
io.open(W + "MG2_WRITE.md", "w", encoding="utf-8", newline="\n").write(
    "# OG-mg-2 Phase B -- writes (option (b))\n\nApplier: `0.7.0_AE_CloudOps~NFRA1`. Written at %s under `opal-gateway-access-admin`, approver `Andrew Berman`.\n\n- alyssa (pk_hash `%s`): `%s`\n- andrew (pk_hash `%s`): NOT WRITTEN. %s\n\nThe module's scope diff holds account ids and was neither printed nor saved.\n" % (at, bef["alyssa"]["pk_hash"], line, bef["andrew"]["pk_hash"], held))
io.open(W + "MG2_ANDREW_HELD.md", "w", encoding="utf-8", newline="\n").write("Held under option (b), COO half G3 and CTO half: activating Andrew's grant re-creates his email_deny record (legacy consent sign-in 403) and removing it is a delete this order forbids; his grant revision stays %s; a follow-on order handles it.\n" % bef["andrew"]["grant_revision"])
if not line.startswith("ACTIVATED") or rc != 0:
    stop("the activation did not report ACTIVATED: %s" % line)

# ---- read-back: a fresh strongly consistent scan; decide() on Alyssa's LIVE grant
items2 = scan(me)
pa = role_profile(items2, "alyssa")
st2 = acs.AccessState(client=me)
prof1, grant1 = adm.current_state(st2, pa["tid"], pa["oid"])
acc = de.Access(True, prof1, grant1, de.allowed_tools(prof1, grant1))
admit = {t: de.decide(t, acc) is None for t in TOOLS4}
refuse = {"schwab_prepare_download": de.decide("schwab_prepare_download", acc) is not None}
io.open(W + "MG2_READBACK_DECIDE.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"alyssa": {"admit": admit, "refuse": refuse}}, indent=1) + "\n")
gnew = st2.get(de.grant_key(pa["tid"], pa["oid"], prof1.grant_revision))
sans = sha({k: v for k, v in gnew["scope"].items() if k != "accounts"})
counts = {m: len(v) for m, v in gnew["scope"]["accounts"].items()}
andrew_now = role_profile(items2, "andrew")
after = {"read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "policy_items_scanned": sum(1 for i in items2 if str(i.get("pk", "")).startswith("POLICY#")),
         "alyssa": {"profile_status": prof1.status, "profile_revision": int(prof1.revision), "grant_status": grant1.status, "grant_revision": int(prof1.grant_revision), "accounts": counts,
                    "counts_equal_current": counts == bef["alyssa"]["accounts_current"], "scope_sans_accounts_unchanged": sans == bef["alyssa"]["scope_sans_accounts_sha256"]},
         "andrew": {"held": True, "grant_revision_unchanged": int(andrew_now["grant_revision"]) == bef["andrew"]["grant_revision"]},
         "email_deny_records_in_store": sum(1 for i in items2 if i.get("record_type") == "email_deny")}
io.open(W + "MG2_AFTER.json", "w", encoding="utf-8", newline="\n").write(json.dumps(after, indent=1) + "\n")
ok = (after["alyssa"]["profile_status"] == "active" and after["alyssa"]["grant_status"] == "active" and after["alyssa"]["grant_revision"] > bef["alyssa"]["grant_revision"]
      and after["alyssa"]["counts_equal_current"] and after["alyssa"]["scope_sans_accounts_unchanged"] and all(admit.values()) and refuse["schwab_prepare_download"] and after["andrew"]["grant_revision_unchanged"])
print(json.dumps({"alyssa": after["alyssa"], "andrew": after["andrew"], "decide": {"admit": admit, "refuse": refuse}, "email_deny_records": after["email_deny_records_in_store"], "READBACK_OK": ok}, default=num))
raise SystemExit(0 if ok else 4)
