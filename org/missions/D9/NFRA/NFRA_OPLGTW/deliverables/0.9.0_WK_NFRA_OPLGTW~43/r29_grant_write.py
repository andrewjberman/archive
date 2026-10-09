"""OG-rl-15 PHASE C step 2: the 13-month grant write for ONE principal (Alyssa's), operator side.
usage: python r29_grant_write.py <before|write|after>

  before : read-only. Snapshots every POLICY# item (sha256 per (pk, sk)) off-repo, reads the holder's current profile+grant through the
           gateway's own access_state, checks it is the role `alyssa`, active, rolling_complete_window with NO calendar_days/calendar_months,
           builds candidate/rollback files OFF-REPO, runs prepare() (the operator CLI's own validate + scope diff; nothing written) and
           requires the diff to be exactly {dates: calendar_months None -> 13}. Writes RL15_GRANT_PRIOR.json (by role; no tid/oid/email).
  write  : repeats the `before` checks, then runs `schwab_entitlement_admin.py activate` (its main()) under the assumed operator role.
           The store's optimistic condition refuses a stale base.
  after  : re-snapshots, diffs against the before snapshot, and writes RL15_GRANT_FACTS.json (counts + field names; no ids).

Operator identity: `sts assume-role` on opal-gateway-access-admin, credentials held in THIS process' environment only.
Nothing here prints or commits a tid, oid or email; the off-repo directory X holds the candidate, rollback and snapshots."""
import copy
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while ROOT != os.path.dirname(ROOT) and not os.path.isdir(os.path.join(ROOT, ".tools")):
    ROOT = os.path.dirname(ROOT)
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "r29")
HOLDER = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "ga1", "holder_pks.json")
os.makedirs(X, exist_ok=True)
ROLE_ARN = "arn:aws:iam::313476888478:role/opal-gateway-access-admin"
CONTRACT = os.path.join(ROOT, "org", "standards", "NFRA_OPLGTW_CONTRACT.json")
APPROVER = "1.0.0_SA_CTO~O (CTO ruling msg 32087; OG-rl-15 halves signed)"
SOURCE_AUTH = ("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/{1.0.0_SA_CTO~O/NEVER_WIDEN_HALF_CTO_OG-rl-15_r29_20261009.md@d3f04813df,"
               "2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-15_r29_20261009.md@40b39ad88d,"
               "3.0.0_SA_CVO~Z/NEVER_WIDEN_HALF_CVO_OG-rl-15_r29_20261009.md@c348b51df9}; A7 D3 Alyssa only")
SUMMARY = "OG-rl-15 r29 Phase C: scope.dates.calendar_months 13 on the rolling_complete_window grant (revision 3 -> 4); no other field"
stage = sys.argv[1]
sys.path.insert(0, GW)
sys.path.insert(0, os.path.join(GW, "ops"))


def aws(args):
    shim = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
    p = subprocess.run([shim] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=110)
    return p.returncode, p.stdout


def assume():
    rc, out = aws(["sts", "assume-role", "--role-arn", ROLE_ARN, "--role-session-name", "wk43-rl15-grant", "--duration-seconds", "3600",
                   "--query", "Credentials", "--output", "json"])
    assert rc == 0, "assume-role failed rc=%d" % rc
    c = json.loads(out)
    os.environ.update({"AWS_ACCESS_KEY_ID": c["AccessKeyId"], "AWS_SECRET_ACCESS_KEY": c["SecretAccessKey"], "AWS_SESSION_TOKEN": c["SessionToken"],
                       "AWS_DEFAULT_REGION": "us-east-1"})
    for k in ("AWS_PROFILE",):
        os.environ.pop(k, None)


def sha(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def snapshot():
    import boto3
    ddb = boto3.session.Session().client("dynamodb", region_name="us-east-1")   # its own session: never the process default that the operator write reads
    out, n = {}, 0
    for page in ddb.get_paginator("scan").paginate(TableName="gateway-access-state-table"):
        for it in page["Items"]:
            n += 1
            pk = (it.get("pk") or {}).get("S", "")
            if pk.startswith("POLICY#"):
                out["%s|%s" % (pk, (it.get("sk") or {}).get("S", ""))] = sha(it)
    return out, n


def load_holder():
    pks = json.load(open(HOLDER, encoding="utf-8"))
    assert len(pks) == 1
    return pks[0][0], pks[0][1]


def checks():
    """Returns (store, tid, oid, profile, grant, praw, raw_now, cand_raw, rollback_raw, plan_diff)."""
    from app import access_state as acs
    from app import data_entitlement as de
    import schwab_entitlement_admin as adm
    tid, oid = load_holder()
    store = acs.store()
    praw = store.get(de.profile_key(tid, oid))
    assert praw is not None, "holder profile absent"
    profile = de.parse_profile(praw, tid, oid)
    grant = de.parse_grant(store.get(de.grant_key(tid, oid, profile.grant_revision)), tid, oid, profile.grant_revision)
    email = (praw.get("email") or "").strip()
    assert email.split("@")[0].lower() == "alyssa", "holder is not the role alyssa"
    assert profile.status == "active" and grant.status == "active"
    sc = grant.scope
    assert sc.date_mode == "rolling_complete_window" and sc.calendar_months is None and getattr(sc, "calendar_days", None) is None, "prior reach is not the plain 30-day rolling window"
    raw_now = adm._scope_to_raw(sc)
    cand_scope = copy.deepcopy(raw_now)
    cand_scope["dates"]["calendar_months"] = 13
    cand = {"tid": tid, "oid": oid, "email": email, "scope": cand_scope}
    rb = {"tid": tid, "oid": oid, "email": email, "scope": copy.deepcopy(raw_now)}
    contract = adm.load_contract(__import__("pathlib").Path(CONTRACT))
    sink = io.StringIO()
    plan = adm.prepare(store, cand, contract, out=sink)
    d = plan.diff
    for dim in ("masters", "datasets", "operations", "portal_channels"):
        assert d[dim] == {"added": [], "removed": []}, "unexpected diff in " + dim
    for dim in ("accounts", "columns"):
        assert all(v == {"added": [], "removed": []} for v in d[dim].values()), "unexpected diff in " + dim
    dd = d["dates"]
    assert dd.get("old_mode") == dd.get("new_mode") == "rolling_complete_window" and dd.get("added") == [] and dd.get("removed") == []
    assert dd.get("old_calendar_months") is None and dd.get("new_calendar_months") == 13, dd
    assert [k for k in dd if k.startswith(("old_calendar", "new_calendar"))] == ["old_calendar_months", "new_calendar_months"], dd
    return store, tid, oid, profile, grant, praw, raw_now, cand, rb, d, acs, de


def role_counts(snap):
    pks = sorted(set(k.split("|")[0] for k in snap))
    return {"policy_items": len(snap), "policy_partitions": len(pks),
            "emaildeny_partitions": len([p for p in pks if p.startswith("POLICY#EMAILDENY#")])}


if stage in ("before", "write"):
    snap, scanned = snapshot()      # the scan runs under the caller's own identity (the operator role has no Scan)
    assume()
    store, tid, oid, profile, grant, praw, raw_now, cand, rb, d, acs, de = checks()
    email = cand["email"]
    deny_exists = ("%s|%s" % (acs.email_deny_key(email).pk, acs.email_deny_key(email).sk)) in snap
    assert deny_exists, "no email_deny record exists for the holder: activate would CREATE one (outside the blast radius)"
    pk = de.profile_key(tid, oid).pk
    holder_items = sorted(k.split("|")[1] for k in snap if k.split("|")[0] == pk)
    print("HOLDER role=alyssa profile_revision=%s grant_revision=%s status=active masters=%d datasets=%d operations=%s portal_channels=%d prior_dates_mode=%s calendar_days=None calendar_months=None"
          % (profile.revision, grant.revision, len(grant.scope.masters), len(grant.scope.datasets), sorted(grant.scope.operations),
             len(grant.scope.portal_channels), grant.scope.date_mode))
    print("HOLDER_PARTITION_RECORD_TYPES %s" % sorted(set(s.split("#")[0] if "#" in s else s for s in holder_items)))
    print("SNAPSHOT scanned_items=%d %s email_deny_for_holder_exists=%s" % (scanned, json.dumps(role_counts(snap), sort_keys=True), deny_exists))
    print("PREPARE_DIFF_CHANGED_KEYS dates.calendar_months None -> 13 ; every other dimension added=[] removed=[] (masters/datasets/operations/portal_channels/accounts/columns/mode)")
    if stage == "before":
        json.dump(cand, open(os.path.join(X, "candidate.json"), "w", encoding="utf-8"))
        json.dump(rb, open(os.path.join(X, "rollback.json"), "w", encoding="utf-8"))
        json.dump(snap, open(os.path.join(X, "snap_before.json"), "w", encoding="utf-8"))
        prior = {"principal": "alyssa", "key": "grant record (principal_profile + data_entitlement), by role",
                 "profile_revision": profile.revision, "grant_revision": grant.revision,
                 "prior_reach": {"dates_mode": grant.scope.date_mode, "calendar_days": None, "calendar_months": None,
                                 "effective_window": "30 calendar days (contract window)"},
                 "prior_scope_sha256": sha(raw_now), "rollback": "activate rollback candidate (a new revision 5 equal to revision 3's scope), BEFORE any gateway rollback",
                 "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "grant_item_sha256": snap.get("%s|%s" % (de.grant_key(tid, oid, grant.revision).pk, de.grant_key(tid, oid, grant.revision).sk)),
                 "profile_item_sha256": snap.get("%s|%s" % (de.profile_key(tid, oid).pk, de.profile_key(tid, oid).sk))}
        json.dump(prior, open(os.path.join(HERE, "RL15_GRANT_PRIOR.json"), "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
        print("WROTE RL15_GRANT_PRIOR.json (by role, no ids); candidate/rollback/snapshot OFF-REPO in X")
        sys.exit(0)
    # stage == write: the CLI's own main(), under the operator role, one activate
    import schwab_entitlement_admin as adm
    t0 = time.time()
    out = io.StringIO()
    rc = adm.main(["activate", "--candidate", os.path.join(X, "candidate.json"), "--approver", APPROVER, "--source-authorization", SOURCE_AUTH,
                   "--summary", SUMMARY], out=out)
    lines = [ln for ln in out.getvalue().splitlines() if ln.startswith(("ACTIVATED", "REFUSED"))]
    print("ACTIVATE rc=%d elapsed_s=%.1f %s" % (rc, time.time() - t0, " | ".join(lines)))
    sys.exit(rc)

if stage == "after":
    after, scanned = snapshot()
    assume()
    from app import access_state as acs
    from app import data_entitlement as de
    import schwab_entitlement_admin as adm
    before = json.load(open(os.path.join(X, "snap_before.json"), encoding="utf-8"))
    tid, oid = load_holder()
    pk = de.profile_key(tid, oid).pk
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    cpks = sorted(set(k.split("|")[0] for k in changed))
    principals_changed = len(cpks)
    other = len([p for p in cpks if p != pk])
    store = acs.store()
    praw = store.get(de.profile_key(tid, oid))
    profile = de.parse_profile(praw, tid, oid)
    g_new = de.parse_grant(store.get(de.grant_key(tid, oid, profile.grant_revision)), tid, oid, profile.grant_revision)
    g_old_key = "%s|%s" % (de.grant_key(tid, oid, 3).pk, de.grant_key(tid, oid, 3).sk)
    prior = json.load(open(os.path.join(HERE, "RL15_GRANT_PRIOR.json"), encoding="utf-8"))
    old_unchanged = before.get(g_old_key) == after.get(g_old_key)
    prior_rev = prior["grant_revision"]
    rb = json.load(open(os.path.join(X, "rollback.json"), encoding="utf-8"))["scope"]
    new_raw = adm._scope_to_raw(g_new.scope)
    fields = []
    for k in sorted(set(rb) | set(new_raw)):
        if k == "dates":
            for s in sorted(set(rb[k]) | set(new_raw[k])):
                if rb[k].get(s) != new_raw[k].get(s):
                    fields.append(s)
        elif rb.get(k) != new_raw.get(k):
            fields.append(k)
    facts = {"scanned_items": scanned, "changed_keys": len(changed), "changed_record_types": sorted(set(k.split("|")[1].split("#")[0] for k in changed)),
             "principals_changed": principals_changed, "other_principals_changed": other, "fields_changed": fields,
             "calendar_months_after": [g_new.scope.calendar_months], "profile_revision_after": profile.revision, "grant_revision_after": g_new.revision,
             "prior_grant_revision": prior_rev, "prior_grant_record_unchanged": old_unchanged,
             "prior_reach_recorded": 1 if prior.get("prior_scope_sha256") else 0, **role_counts(after)}
    json.dump(facts, open(os.path.join(HERE, "RL15_GRANT_FACTS.json"), "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
    print("FACTS " + json.dumps(facts, sort_keys=True))
    sys.exit(0)
print(__doc__)
sys.exit(2)
