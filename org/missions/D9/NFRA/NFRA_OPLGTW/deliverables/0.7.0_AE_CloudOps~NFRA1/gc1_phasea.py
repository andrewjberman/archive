#!/usr/bin/env python
"""OG-gc-1 Phase A: FACTS FIRST -- which gate denies the five client_* tools for Alyssa and Menachem today. READ ONLY: strong reads of the POLICY# partitions and the gateway's OWN decide()/person_denial() functions on trunk code
over the stored records. Nothing is written; no person_access record is written. Roles, counts and decisions only: no tid, oid or e-mail is written or printed.
  python gc1_phasea.py        (repository root)   -> W/GC1_GATES.json and W/GC1_FACTS.json"""
from __future__ import annotations

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
from app.tier import Tier  # noqa: E402

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
TOOLS = ("client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees")
me = boto3.client("dynamodb", region_name="us-east-1")
td = TypeDeserializer()
items, kw = [], {"TableName": "gateway-access-state-table", "ConsistentRead": True}
resp = {"LastEvaluatedKey": True}
while "LastEvaluatedKey" in resp:
    resp = me.scan(**kw)
    items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
    if "LastEvaluatedKey" in resp:
        kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
pol = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
store = acs.AccessState(client=me)


def role_profile(role):
    c = [i for i in pol if i.get("record_type") == "principal_profile" and str(i.get("email", "")).lower().split("@")[0] == role]
    return c[0] if len(c) == 1 else None


facts = {"policy_items_scanned": len(pol), "person_access_records_in_store": sum(1 for i in pol if i.get("record_type") == "person_access"), "principal_profiles": sum(1 for i in pol if i.get("record_type") == "principal_profile")}
principals = {}
for role in ("alyssa", "menachem"):
    pr = role_profile(role)
    present = pr is not None
    row = {"role": role, "profile_present": present}
    if present:
        from app.context import Principal
        principal = Principal(pr["tid"], pr["oid"], pr["email"])
        access = de.current_access(principal, store)
        rec = de.person_access(principal, store)
        row["profile"] = {"status": access.profile.status, "revision": int(access.profile.revision), "grant_revision": int(access.profile.grant_revision), "grant_status": access.grant.status if access.grant else None,
                          "granted_tools_from_scope": sorted(access.tools), "person_access_record_present": rec is not None}
        decisions, person = {}, {}
        for t in TOOLS:
            d_none = de.decide(t, access, None)
            d_admin = de.decide(t, access, Tier.MASTER_ADMIN)
            decisions[t] = {"decide_non_master_admin": (d_none or {}).get("code", "admitted"), "decide_if_master_admin_tier": (d_admin or {}).get("code", "admitted")}
            person[t] = (de.person_denial(t, rec) or {}).get("code", "no_narrowing") if rec is not None else "no_record"
        row["decisions"], row["person_access_narrowing"] = decisions, person
    else:
        access = de.Access(False, None, None, frozenset())
        row["decisions"] = {t: {"decide_non_master_admin": (de.decide(t, access, None) or {}).get("code", "admitted"), "decide_if_master_admin_tier": (de.decide(t, access, Tier.MASTER_ADMIN) or {}).get("code", "admitted")} for t in TOOLS}
        row["note"] = "no principal_profile record for this role in the store (%d profiles, %d with an e-mail); the unprofiled branch of decide() is graded on a profile-less Access, which does not depend on the identity" % (facts["principal_profiles"], sum(1 for i in pol if i.get("record_type") == "principal_profile" and i.get("email")))
    principals[role] = row

facts["principals"] = principals
facts["code_read"] = {"decide": "app/data_entitlement.py decide(): an ACTIVE profile is confined on DATA_GRANT_TOOLS (which includes the five client_* tools) to access.tools = allowed_tools(profile, grant), which maps only SCHWAB_TOOLS to scope.operations; "
                                "so a profiled principal is denied each client_* tool (entitlement_denied) unless its resolved tier is master_admin; an unprofiled principal is denied each unless master_admin (TIER_ADMITTED_TOOLS).",
                      "person_access": "app/data_entitlement.py person_denial() only NARROWS (stopped, tools_deny, channels_deny) and is read AFTER decide(); person_widens() widens ONLY at the identity-scope floor (identity_scope.check), only for an Opal principal and a served tool. "
                                       "It never overrides a decide() denial, so a tools_allow record cannot admit a client_* tool for a principal that decide() denies.",
                      "tier": "tier comes from the deploy-time rosters (Andrew is the sole MASTER_ADMIN_EMAILS entry; Alyssa is on WRITE_CAPABLE_EMAILS: W/../0.7.0_AE_CloudOps~OG/G-C_CONTROLLED_IDENTITY_AND_GRANT_EVIDENCE.md line 57); neither principal is master_admin.",
                      "admit_scope": "client_core._admit: typed_scope.admit_scope over the 'client/' scope (a catalog-segment check), reached only after the dispatch guard admits the call."}
io.open(W + "GC1_FACTS.json", "w", encoding="utf-8", newline="\n").write(json.dumps(facts, indent=1) + "\n")


def tools_row(role):
    row = principals[role]
    return {t: ("admitted" if row["decisions"][t]["decide_non_master_admin"] == "admitted" else "denied:entitlements") for t in TOOLS}


gates = {"principals": {}, "write_path": {
    "mechanism": "person_access is written only by NFRA_MCPORTAL's grant writer (action set_person_access, invoked from the gateway's admin route /api/admin/people/{tid}/{oid}/access with the owner's forwarded identity header). It cannot fix this denial: person_access NARROWS after decide() and widens only at the identity-scope floor; the denial here is decide()'s entitlement_denied. A fix is a CODE change (allowed_tools or the client family's rule) or a tier-roster change, neither a record.",
    "needs_owner_session": True, "writer": "NFRA_MCPORTAL grant writer (mcportal-grant-writer-lambda); not a seat-owned path, and not the right instrument for this denial"}}
for role in ("alyssa", "menachem"):
    ct = tools_row(role)
    denied = any(v.startswith("denied:") for v in ct.values())
    gates["principals"][role] = {"role": role, "profile_present": principals[role]["profile_present"], "client_tools": ct,
                                 "gates_read": ["tool_denial", "entitlements", "person_access", "tier", "admit_scope", "identity_scope"], "needs_write": denied,
                                 "reason": ("decide() denies all five client tools (entitlement_denied): %s. A person_access record cannot admit them (it narrows after decide() and widens only at the identity-scope floor), so the instrument is a code or roster change, not a record."
                                            % ("an active profile is confined to the grant's Schwab tools" if principals[role]["profile_present"] else "no profile, and the principal is not master_admin"))}
io.open(W + "GC1_GATES.json", "w", encoding="utf-8", newline="\n").write(json.dumps(gates, indent=1) + "\n")
print(json.dumps({r: {"profile_present": principals[r]["profile_present"], "client_tools": tools_row(r)} for r in principals}))
print(json.dumps({r: principals[r].get("profile") for r in principals}, default=str))
print(json.dumps({r: principals[r].get("decisions", {}).get("client_resolve_account") for r in principals}))
