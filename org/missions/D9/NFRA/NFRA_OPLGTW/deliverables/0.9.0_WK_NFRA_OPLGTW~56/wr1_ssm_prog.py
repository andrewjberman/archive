# OG-wr-1 host program (NFRA_OPLGTW round 34, E5). Runs on the gateway host with the INSTALLED code and venv (/opt/opal-gateway), as a separate
# process under env -i (never the running service, never /opt/opal-gateway/.env sourced). For every master/dataset pair in the 13-month grant's scope:
#   PRIME   one catalog.availability() pass over the 13-month window (calendar_months=13), timed -> cold_seconds. It reads the completion records and
#           persists each missing snapshot WRITE-ONCE (IF_ABSENT) to the real access-state table through the catalog's own persist(), exactly as a served read does.
#   MEASURE the same read again with a fresh per-request cache, timed -> warm_seconds.
# The holder's tid/oid arrive in the process environment (SSM parameters) and are never printed; masters print as m0, m1. The grant is only READ.
# Prints WR1_PAIR lines, WR1_BODY {json} and WR1_DIGEST <sha256 of json.dumps(body, sort_keys=True)>.
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, "/opt/opal-gateway")
os.environ.update({
    "NFRA_OPLGTW_CONTRACT_PATH": "/opt/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json",
    "SCHWAB_READER_ROLE_ARN": "arn:aws:iam::313476888478:role/gateway-schwab-read-role",
    "SCHWAB_CATALOG_ROLE_ARN": "arn:aws:iam::313476888478:role/gateway-schwab-catalog-read-role",
    "SCHWAB_EXTERNAL_IDS_SECRET_ID": "opal/mcp/opal-gateway-schwab-reader-external-ids",
})


def main():
    from app import access_state as acs
    from app import data_entitlement as de
    from app.integrations.schwab import aws_roles
    from app.integrations.schwab import catalog as cat

    tid, oid = os.environ["GA1_TID"], os.environ["GA1_OID"]
    store = acs.store()                                   # the REAL table, instance-role credentials
    contract = cat.load_contract()
    configs = aws_roles.role_configs(contract.raw, aws_roles.environ_with_external_ids(os.environ))
    catalog = cat.Catalog(contract=contract, catalog_role=aws_roles.AssumedRole(configs[aws_roles.CATALOG]),
                          data_role=aws_roles.AssumedRole(configs[aws_roles.READER]), store=store)
    praw = store.get(de.profile_key(tid, oid))
    assert praw is not None, "holder profile not found in the store"
    profile = de.parse_profile(praw, tid, oid)
    grant = de.parse_grant(store.get(de.grant_key(tid, oid, profile.grant_revision)), tid, oid, profile.grant_revision)
    assert grant.status == "active"
    scope = grant.scope
    print("WR1_GRANT grant_revision=%s date_mode=%s calendar_months=%s masters=%d datasets=%s" % (
        grant.revision, scope.date_mode, scope.calendar_months, len(scope.masters), sorted(scope.datasets)))
    assert scope.date_mode == "rolling_complete_window" and scope.calendar_months == 13
    check = lambda: True                                  # noqa: E731 -- the grant was read above; this program asks the catalog only
    pairs = []
    for mi, master in enumerate(sorted(scope.masters)):
        listed = catalog.list_dates(master, check)
        for dataset in sorted(scope.datasets):
            c1 = {}
            t0 = time.time()
            avail = catalog.availability(master, dataset, check, date_mode=scope.date_mode, dates=(), cache=c1, calendar_months=13)
            cold = time.time() - t0
            c2 = {}
            t1 = time.time()
            avail2 = catalog.availability(master, dataset, check, date_mode=scope.date_mode, dates=(), cache=c2, calendar_months=13)
            warm = time.time() - t1
            w = avail2.get("window") or {}
            first, last = w.get("first"), w.get("last")
            wdates = [d for d in listed if first and last and first <= d <= last]
            primed = sum(1 for d in wdates if d in {k[1] for k, r in c2.items() if r.reused})
            row = {"master": "m%d" % mi, "dataset": dataset, "window_dates": len(wdates), "primed_dates": primed,
                   "cold_seconds": round(cold, 1), "warm_seconds": round(warm, 1)}
            pairs.append(row)
            print("WR1_PAIR " + json.dumps(row, sort_keys=True) + " available_cold=%d available_warm=%d first=%s last=%s" % (
                len(avail.get("available_dates") or []), len(avail2.get("available_dates") or []), first, last))
    body = {"pairs": pairs}
    s = json.dumps(body, sort_keys=True)
    print("WR1_BODY " + s)
    print("WR1_DIGEST " + hashlib.sha256(s.encode("utf-8")).hexdigest())


main()
