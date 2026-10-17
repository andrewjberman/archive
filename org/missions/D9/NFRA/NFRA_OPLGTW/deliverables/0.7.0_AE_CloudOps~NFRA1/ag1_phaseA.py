#!/usr/bin/env python
"""OG-ap-35 Phase A steps 1 (except usage), 2 and 3 -- READ-ONLY. NOTHING IS WRITTEN TO THE STORE.

Identifiers never reach the repo. The identities and the candidate (which carry tid, oid and email) live ONLY under
X = %LOCALAPPDATA%/opal/og-salt/ag1/, asserted at run time to resolve outside the worktree. The repo-side records carry hashes (first 10 hex of sha256),
roles, operation NAMES (fixed words), counts and changed-key NAMES only.
  W/AG1_BEFORE_state.json   the principals' state (merged with the usage census into AG1_BEFORE.json by ag1_merge.py)
  W/AG1_PREFLIGHT.md        operator identity, the two simulated IAM actions, the candidate's changed keys and diff line count
  X/ag1_identities.json, X/alyssa_narrow_candidate.json, X/ag1_prepare_diff.txt   (off-repo)
usage: python ag1_phaseA.py   (from the repo root of the worktree)"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import io
import json
import os
import sys

import boto3

TABLE = "gateway-access-state-table"
REGION = "us-east-1"
SECRET = "gateway/principals/rosters"
BBG_OID_PREFIX = "517aa5ee"          # Part D 2026-09-30, named in OG-mg-1
ROLE = "opal-gateway-access-admin"
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1")
DROP = "download_filtered"


def h10(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def x_dir() -> str:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    d = os.path.join(base, "opal", "og-salt", "ag1")
    os.makedirs(d, exist_ok=True)
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree (%s)" % d)
    return d


def sval(item: dict, key: str) -> str:
    v = item.get(key) or {}
    return v.get("S") or v.get("N") or ""


def changed_keys(a: dict, b: dict, path: str = "") -> list:
    out = []
    for k in sorted(set(a) | set(b)):
        p = "%s.%s" % (path, k) if path else k
        va, vb = a.get(k), b.get(k)
        if isinstance(va, dict) and isinstance(vb, dict):
            out.extend(changed_keys(va, vb, p))
        elif va != vb:
            out.append(p)
    return out


def main() -> int:
    X = x_dir()
    sys.path.insert(0, os.path.abspath(GW))
    import app.access_state as acs                      # noqa: E402
    sys.path.insert(0, os.path.abspath(os.path.join(GW, "ops")))
    import schwab_entitlement_admin as sea              # noqa: E402

    ddb = boto3.client("dynamodb", region_name=REGION)
    items, token, pages = [], None, 0
    while True:
        kw = {"TableName": TABLE, "ConsistentRead": True}
        if token:
            kw["ExclusiveStartKey"] = token
        r = ddb.scan(**kw)
        items += r["Items"]
        pages += 1
        token = r.get("LastEvaluatedKey")
        if not token:
            break
    pol = [it for it in items if sval(it, "pk").startswith("POLICY#")]
    print("  scan: %d item(s) over %d page(s), strongly consistent, fully paginated; POLICY# %d" % (len(items), pages, len(pol)))
    profiles = [it for it in pol if sval(it, "record_type") == "principal_profile" and sval(it, "status") == "active"]
    sm = boto3.client("secretsmanager", region_name=REGION)
    roster = json.loads(sm.get_secret_value(SecretId=SECRET)["SecretString"])
    pairs = {k: [p.strip() for p in v.split(",") if "/" in p] for k, v in roster.items() if isinstance(v, str) and "/" in v}
    andrew = pairs.get("master_admin", [None])[0]
    bbg = next((p for v in pairs.values() for p in v if p.split("/")[-1].startswith(BBG_OID_PREFIX)), None)
    pk_of = lambda pair: None if not pair else "POLICY#%s#%s" % tuple(pair.split("/", 1))      # noqa: E731
    known = {"andrew": pk_of(andrew), "bbg": pk_of(bbg)}
    alyssa_prof = None
    for it in profiles:
        email = sval(it, "email")
        role = email.split("@")[0].split(".")[0].lower() if email else "unknown"
        if role == "alyssa":
            alyssa_prof = it
            known["alyssa"] = sval(it, "pk")
    if alyssa_prof is None:
        raise SystemExit("STOP (BLOCKING row): no ACTIVE principal_profile resolves to the alyssa role")
    store = acs.AccessState()
    out_p = {}
    raw_scopes = {}
    for role, pk in known.items():
        if not pk:
            out_p[role] = {"pk_hash": None}
            continue
        tid, oid = pk.split("#")[1], pk.split("#")[2]
        prof, grant = sea.current_state(store, tid, oid)
        scope_raw = sea._scope_to_raw(grant.scope) if grant is not None else None
        raw_scopes[role] = scope_raw
        out_p[role] = {"pk_hash": h10(pk), "profile_revision": None if prof is None else prof.revision, "grant_revision": None if prof is None else prof.grant_revision,
                       "profile_kind": None if prof is None else getattr(prof, "kind", None),
                       "operations": sorted(scope_raw["operations"]) if scope_raw else [],
                       "grant_hash": h10(canon(scope_raw)) if scope_raw else None,
                       "scope_without_operations_hash": h10(canon({k: v for k, v in scope_raw.items() if k != "operations"})) if scope_raw else None}
    a = out_p["alyssa"]
    if DROP not in a["operations"]:
        raise SystemExit("STOP (BLOCKING row): her live operations do not carry %s" % DROP)
    # the side-writes the module's activate() will make, read before they are asked for: her email_deny record and its attribute names
    a_tid, a_oid = known["alyssa"].split("#")[1], known["alyssa"].split("#")[2]
    stored_email = sval(alyssa_prof, "email")
    deny_item = store.get(acs.email_deny_key(stored_email))
    deny_state = {"email_deny_record_present": deny_item is not None,
                  "email_deny_keys": sorted(deny_item.keys()) if isinstance(deny_item, dict) else None,
                  "email_deny_status_active": isinstance(deny_item, dict) and deny_item.get("status") == "active"}
    audit_items = [it for it in pol if sval(it, "record_type") == "operator_audit" and sval(it, "pk") == known["alyssa"]]
    first_at = min(sval(it, "at") for it in audit_items) if audit_items else None
    added_at = None
    for it in audit_items:
        if DROP in sval(it, "summary"):
            added_at = max(added_at or "", sval(it, "at"))
    before = {"read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "denominator": {"policy_items_scanned": len(pol), "items_scanned_total": len(items), "scan_pages": pages,
                              "active_principal_profiles": len(profiles), "alyssa_operator_audit_records": len(audit_items)},
              "method": "strongly consistent Scan, fully paginated, under the calling principal's own read access; no identifier in this file by construction",
              "alyssa": {k: a[k] for k in ("pk_hash", "profile_revision", "grant_revision", "operations", "scope_without_operations_hash")},
              "others_hash": {"andrew": out_p["andrew"]["grant_hash"], "bbg": out_p["bbg"]["grant_hash"]},
              "others_state": {r: {"grant_revision": out_p[r]["grant_revision"], "operations": out_p[r]["operations"]} for r in ("andrew", "bbg")},
              "alyssa_grant_timeline": {"first_activation_at": first_at, "download_filtered_added_at": added_at},
              "side_write_state": deny_state}
    with io.open(os.path.join(W, "AG1_BEFORE_state.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(before, fh, indent=1)
        fh.write("\n")
    with io.open(os.path.join(X, "ag1_identities.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"alyssa_pk": known["alyssa"], "alyssa_tid": a_tid, "alyssa_oid": a_oid, "stored_email_present": bool(stored_email)}, fh, indent=1)
        fh.write("\n")

    # ---- step 2: operator identity and the simulated IAM actions ------------------------------------------------------------
    sts = boto3.client("sts", region_name=REGION)
    me = sts.get_caller_identity()
    acct = me["Account"]
    role_arn = "arn:aws:iam::%s:role/%s" % (acct, ROLE)
    cr = sts.assume_role(RoleArn=role_arn, RoleSessionName="ag1-phasea-readonly")["Credentials"]
    op_sts = boto3.client("sts", region_name=REGION, aws_access_key_id=cr["AccessKeyId"], aws_secret_access_key=cr["SecretAccessKey"], aws_session_token=cr["SessionToken"])
    op_arn = op_sts.get_caller_identity()["Arn"].replace(acct, "<acct>")
    iam = boto3.client("iam", region_name=REGION)
    table_arn = "arn:aws:dynamodb:%s:%s:table/%s" % (REGION, acct, TABLE)
    sims = []
    for action, ctx_entries in (("dynamodb:GetItem", None), ("dynamodb:PutItem", "POLICY#test"), ("dynamodb:UpdateItem", "POLICY#test"), ("dynamodb:PutItem", None),
                                ("dynamodb:DeleteItem", "POLICY#test"), ("dynamodb:Scan", None)):
        kw = {"PolicySourceArn": role_arn, "ActionNames": [action], "ResourceArns": [table_arn]}
        if ctx_entries:
            kw["ContextEntries"] = [{"ContextKeyName": "dynamodb:LeadingKeys", "ContextKeyValues": [ctx_entries], "ContextKeyType": "stringList"}]
        dec = iam.simulate_principal_policy(**kw)["EvaluationResults"][0]["EvalDecision"]
        sims.append((action, ctx_entries is not None, dec))

    # ---- step 3: the candidate and prepare() under the OPERATOR role (nothing is written) ---------------------------------------
    os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"], os.environ["AWS_SESSION_TOKEN"] = cr["AccessKeyId"], cr["SecretAccessKey"], cr["SessionToken"]
    op_store = acs.AccessState()
    prof, grant = sea.current_state(op_store, a_tid, a_oid)
    live_raw = sea._scope_to_raw(grant.scope)
    cand_scope = copy.deepcopy(live_raw)
    cand_scope["operations"] = sorted(o for o in live_raw["operations"] if o != DROP)
    cand = {"tid": a_tid, "oid": a_oid, "email": stored_email, "scope": cand_scope}
    buf = io.StringIO()
    try:
        plan = sea.prepare(op_store, cand, sea.load_contract(None), out=buf)
        ok, err = True, None
    except Exception as exc:
        plan, ok, err = None, False, "%s: %s" % (type(exc).__name__, exc)
    keys = changed_keys(live_raw, cand_scope)
    diff_text = buf.getvalue()
    with io.open(os.path.join(X, "alyssa_narrow_candidate.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cand, fh, indent=1)
        fh.write("\n")
    with io.open(os.path.join(X, "ag1_prepare_diff.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(diff_text)
    live_ok = (plan is not None and plan.base_profile_revision == int(a["profile_revision"]) and plan.base_grant_revision == int(a["grant_revision"]))
    pre = {"prepare_accepted": ok, "prepare_error_class": None if ok else err.split(":")[0], "changed_keys": keys, "diff_line_count": len([ln for ln in diff_text.split("\n") if ln.strip()]),
           "base_profile_revision": None if plan is None else plan.base_profile_revision, "base_grant_revision": None if plan is None else plan.base_grant_revision,
           "base_equals_live": live_ok, "deny_email_count": None if plan is None else len(plan.deny_emails),
           "candidate_operations": cand_scope["operations"], "next_profile_revision": None if plan is None else (plan.base_profile_revision or 0) + 1,
           "next_grant_revision": None if plan is None else (plan.base_grant_revision or 0) + 1}
    lines = ["# OG-ap-35 Phase A -- operator identity, the IAM preflight and the candidate (NO write ran)", "",
             "Seat `0.7.0_AE_CloudOps~NFRA1`, %s. Identifiers appear nowhere in this file: roles, operation names, counts and key names only." % before["read_at"], "",
             "## 1. Operator identity", "",
             "- calling principal: an IAM user of the account (read access used for the before-record scan and the roster read)",
             "- operator role: `%s` (assumed for real: `sts get-caller-identity` names `%s`)" % (ROLE, op_arn),
             "", "## 2. Simulated actions on the role (one resource, `dynamodb:LeadingKeys` context where marked)", "",
             "| action | LeadingKeys POLICY# context | decision |", "|---|---|---|"]
    lines += ["| `%s` | %s | **%s** |" % (act, "yes" if c else "no", dec) for act, c, dec in sims]
    lines += ["", "The act needs `PutItem` and `UpdateItem` with the context (allowed means no STOP). `DeleteItem` and `Scan` are expected implicitDeny: the writer's `activate()` builds only Put operations and never deletes.", "",
              "## 3. The candidate and prepare() under the operator role", "",
              "- prepare accepted: %s%s" % (ok, "" if ok else " (%s)" % pre["prepare_error_class"]),
              "- base revisions read by prepare: profile %s, grant %s; equal to the live read: %s" % (pre["base_profile_revision"], pre["base_grant_revision"], live_ok),
              "- **Changed keys (candidate scope against her live grant): %s**" % (", ".join(keys) if keys else "none"),
              "- diff line count printed by prepare: %d" % pre["diff_line_count"],
              "- candidate operations: %s (live: %s)" % (", ".join(cand_scope["operations"]), ", ".join(sorted(live_raw["operations"]))),
              "- next revisions if activated: profile %s, grant %s" % (pre["next_profile_revision"], pre["next_grant_revision"]),
              "- deny emails the plan would put: %s" % pre["deny_email_count"],
              "", "## 4. What `activate()` writes besides the grant (read from the module, not assumed)", "",
              "One transaction: the principal_profile put (revision +1, grant_revision +1), the data_entitlement put (the new revision), the operator_audit append, and one email_deny put per plan deny email, conditioned `attribute_not_exists(pk) OR (tid = :tid AND oid = :oid)`.",
              "Her email_deny record today: present %s, status active %s, attribute names %s." % (deny_state["email_deny_record_present"], deny_state["email_deny_status_active"], ", ".join(deny_state["email_deny_keys"] or [])),
              "The put's item carries tid, oid and status active; the browser-route deny state therefore stays what it is (a restricted principal that is denied the browser routes by contract C2 stays denied)."]
    with io.open(os.path.join(W, "AG1_PREFLIGHT.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with io.open(os.path.join(W, "AG1_PREFLIGHT_record.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"operator_role": ROLE, "simulations": [{"action": a_, "leadingkeys_context": c_, "decision": d_} for a_, c_, d_ in sims], "candidate": pre, "side_write_state": deny_state}, fh, indent=1)
        fh.write("\n")
    print("  alyssa: profile rev %s, grant rev %s, ops %s" % (a["profile_revision"], a["grant_revision"], a["operations"]))
    print("  sims:", [(x[0].split(":")[1], x[1], x[2]) for x in sims])
    print("  prepare accepted %s; changed keys %s; diff lines %d; base==live %s; deny emails %s" % (ok, keys, pre["diff_line_count"], live_ok, pre["deny_email_count"]))
    print("  email_deny present %s active %s keys %s" % (deny_state["email_deny_record_present"], deny_state["email_deny_status_active"], deny_state["email_deny_keys"]))
    print("  timeline: first activation %s, download_filtered added %s" % (first_at, added_at))
    return 0


if __name__ == "__main__":
    sys.exit(main())
