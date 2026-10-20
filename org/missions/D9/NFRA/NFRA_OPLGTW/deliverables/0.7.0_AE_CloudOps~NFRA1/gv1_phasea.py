#!/usr/bin/env python
"""OG-gv-1 Phase A: Andrew's Schwab grant moves from its held stored account lists to the MASTER-WIDE scope (accounts[master] == ["*"] for each of his masters). NO WRITE of any kind: strong reads, an in-process prepare()
(it writes nothing), an in-process decide(). COUNTS, ROLES, KEYS AND HASHES ONLY in the repo: no account id, tid, oid or e-mail is written or printed. The candidate (which holds the tid and oid) lives off-repo in
X = %LOCALAPPDATA%/opal/og-salt/gv1/.
  python gv1_phasea.py        (repository root)
Writes W/GV1_BEFORE.json, W/GV1_DIFF.json, W/GV1_PREFLIGHT_DECIDE.json (download = the two booleans, ruling Z-S431 (a), order amended), W/GV1_DENY.json (facts) and X/andrew_candidate.json."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys

REPO = os.getcwd()
sys.path.insert(0, os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway"))
os.environ.setdefault("MOCK_GRAPH", "1")

import boto3  # noqa: E402
from boto3.dynamodb.types import TypeDeserializer  # noqa: E402

from app import access_state as acs  # noqa: E402
from app import data_entitlement as de  # noqa: E402
from ops import schwab_entitlement_admin as adm  # noqa: E402

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "gv1")
os.makedirs(X, exist_ok=True)
TABLE = "gateway-access-state-table"
TOOLS4 = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")


def num(o):
    return int(o) if o == int(o) else float(o)


def sha_json(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), default=num).encode("utf-8")).hexdigest()


def save(name, obj):
    io.open(W + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1, default=num) + "\n")


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
cands = [p for p in profiles if p.get("status") == "active" and str(p.get("email", "")).lower().split("@")[0] == "andrew"]
if len(cands) != 1:
    raise SystemExit("STOP: andrew resolves to %d active profiles" % len(cands))
pa = cands[0]
store = acs.AccessState(client=me)
profile, grant = adm.current_state(store, pa["tid"], pa["oid"])
if grant is None or grant.status != "active":
    raise SystemExit("STOP: andrew has no active grant in force")
gitem = store.get(de.grant_key(pa["tid"], pa["oid"], profile.grant_revision))
stored_scope = gitem["scope"]
masters = sorted(grant.scope.masters)
if any(de.is_master_wide(grant.scope, m) for m in masters):
    raise SystemExit("STOP: a master is already master-wide")
if not hasattr(de, "MASTER_WIDE"):
    raise SystemExit("STOP: this tree has no master-wide parser")

# candidate: accounts only
scope_raw = adm._scope_to_raw(grant.scope)
new_scope = json.loads(json.dumps(scope_raw))
new_scope["accounts"] = {m: [de.MASTER_WIDE] for m in masters}
raw = {"tid": pa["tid"], "oid": pa["oid"], "email": pa["email"], "scope": new_scope}
io.open(os.path.join(X, "andrew_candidate.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(raw))
sts = boto3.client("sts")
cred = sts.assume_role(RoleArn="arn:aws:iam::313476888478:role/opal-gateway-access-admin", RoleSessionName="og-gv1-phase-a", DurationSeconds=3600)["Credentials"]
op = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"], aws_session_token=cred["SessionToken"], region_name="us-east-1")
op_store = acs.AccessState(client=op.client("dynamodb"))
buf = io.StringIO()
plan = adm.prepare(op_store, raw, adm.load_contract(None), out=buf)       # writes nothing
old_n = json.loads(json.dumps(scope_raw, default=num))
changed = sorted(k for k in set(old_n) | set(new_scope) if json.dumps(old_n.get(k), sort_keys=True) != json.dumps(new_scope.get(k), sort_keys=True))
sans_acc_stored = {k: v for k, v in stored_scope.items() if k != "accounts"}
rest_stored = {k: v for k, v in stored_scope.items() if k not in ("accounts", "masters")}
rest_candidate = {k: v for k, v in new_scope.items() if k not in ("accounts", "masters")}
rest_matches = sha_json(rest_stored) == sha_json(rest_candidate) and sorted(stored_scope.get("masters", [])) == sorted(new_scope["masters"])

save("GV1_BEFORE.json", {"read_at": read_at,
                         "denominator": {"policy_items_scanned": len(pol), "principal_profiles": len(profiles), "all_items_scanned": len(items), "scan_pages": pages, "by_record_type": by_type},
                         "principal": {"role": "andrew", "pk_hash": hashlib.sha256(str(pa["pk"]).encode()).hexdigest()[:16], "profile_revision": int(profile.revision), "grant_revision": int(profile.grant_revision),
                                       "masters": masters, "accounts_before_counts": {m: len(grant.scope.accounts.get(m, ())) for m in masters},
                                       "scope_sans_accounts_sha256": sha_json(sans_acc_stored), "operations": sorted(grant.scope.operations)}})
save("GV1_DIFF.json", {"andrew": {"changed_keys": changed, "masters_after": sorted(new_scope["masters"]), "accounts_after": new_scope["accounts"],
                                  "rest_of_scope_matches_template": bool(rest_matches), "rest_sha256_after_expected": sha_json(rest_candidate),
                                  "prepare_accepted": True, "prepare_deny_emails": len(plan.deny_emails)}})

# decide() pre-flight on the CANDIDATE (the master-wide parser), in process
cscope = de.parse_scope(new_scope)
prof = de.Profile(profile.tid, profile.oid, "active", profile.revision + 1, profile.grant_revision + 1)
gr = de.Grant(profile.tid, profile.oid, profile.grant_revision + 1, "active", cscope)
acc = de.Access(True, prof, gr, de.allowed_tools(prof, gr))
admit = {t: de.decide(t, acc) is None for t in TOOLS4}
refuse = {"schwab_prepare_download": de.decide("schwab_prepare_download", acc) is not None}
wide = all(de.is_master_wide(cscope, m) for m in masters)
stored_dl = "download_filtered" in grant.scope.operations
save("GV1_PREFLIGHT_DECIDE.json", {"andrew": {"admit": admit, "download": {"stored_operations_include_download_filtered": bool(stored_dl), "prepare_download_admitted": not refuse["schwab_prepare_download"]},
                                              "master_wide_parsed": bool(wide)}})

# the email_deny finding: FACTS (read from the store and from the code)
deny_now = [store.get(acs.email_deny_key(e)) is not None for e in plan.deny_emails]
effect = ("The email_deny record is read by exactly two paths in the gateway: data_entitlement.email_denial(), called by the five browser routes (/login, /sprint, /sprint/, /sprint/archive, /sprint/{day}) and by the legacy /callback consent branch "
          "(token_broker.redeem_consent), which identify the caller by e-mail alone. A record means 403 there; an unreadable store means 503. It does not touch MCP tool calls, which are keyed by tenant and object id. "
          "A master admin passes the five browser routes before the store is read (OG-en-14, route_class internal_page); the legacy /callback consent branch has no such exemption, so his legacy consent sign-in would answer 403 after the activation.")
options = ["Activate and accept the effect: his browser pages stay open as master admin and his MCP tool calls are unaffected; only the legacy consent sign-in (/callback) answers 403 for him.",
           "Before the activation, add a master-admin exemption to the legacy /callback consent branch (a code change and its own release, separate from this order), then activate.",
           "Hold the activation until the legacy consent branch is retired, keeping the held revision-1 grant meanwhile (the OG-mg-2 option (b) state).",
           "Have the operator tool write the grant without the e-mail put (a change to ops/schwab_entitlement_admin.py and its tests, separate from this order); activate() stays unchanged until then."]
save("GV1_DENY.json", {"deny_record_present_before": bool(any(deny_now)), "activate_writes_deny": bool(len(plan.deny_emails) >= 1), "deny_emails_in_plan": len(plan.deny_emails),
                       "email_deny_records_in_store": by_type.get("email_deny", 0), "effect": effect, "options": options, "delete_proposed": False,
                       "ruling_requested_of": "1.0.0_SA_CTO~Z (his half names the handling)"})
print(json.dumps({"changed_keys": changed, "masters": masters, "rest_matches": rest_matches, "decide": {"admit": admit, "refuse": refuse, "wide": wide}, "deny_before": deny_now, "plan_deny_emails": len(plan.deny_emails),
                  "revs": [int(profile.revision), int(profile.grant_revision)], "counts_before": {m: len(grant.scope.accounts.get(m, ())) for m in masters}, "policy_items": len(pol)}, default=num))
