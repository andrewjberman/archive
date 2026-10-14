import app.server  # noqa: F401 side-effect import: registers the served integrations (row Z-S48)
import json
from app import admin_people as P, admin_gateway_breakdown as BD, admin_fabric_gitstate as G
from app import data_entitlement as DE, context
from app import access_state as ACS

OUT = {}


def DATA(t):
    return t.startswith("schwab_") or t == "blackdiamond_list_fees"


try:
    people = P._compute()["people"]
    real = [x for x in people if x["kind"] == "person" and "data grant revision" in x["how"]]
    OUT["grant_rows"] = len(real)
    if len(real) != 1:
        raise SystemExit("PC6ERR grant_rows=%d" % len(real))
    p = real[0]
    OUT["person"] = p["who"]
    OUT["how"] = p["how"]
    OUT["page_person_tools"] = sorted({t["name"] for c in p["channels"] for t in c["tools"] if DATA(t["name"])})

    st = ACS.store()
    scanned = BD._scan_principals(BD._ddb_client())
    OUT["scan_denominator"] = len(scanned)
    hits = []
    for tid, oid in scanned:
        raw = st.get(DE.profile_key(tid, oid))
        if raw is None:
            continue
        email = str(raw.get("email") or "").strip().lower()
        key = context.principal_key(tid, oid)
        if p["who"] == (email or key):
            hits.append((tid, oid, raw))
    OUT["profile_matches"] = len(hits)
    if len(hits) != 1:
        raise SystemExit("PC6ERR profile_matches=%d" % len(hits))
    tid, oid, prof = hits[0]
    OUT["store_profile"] = {"status": prof.get("status"), "revision": prof.get("revision"),
                            "grant_revision": prof.get("grant_revision")}
    grant = st.get(DE.grant_key(tid, oid, prof.get("grant_revision")))
    if grant is None:
        raise SystemExit("PC6ERR grant_absent")
    scope = grant.get("scope") or {}
    ops = sorted(scope.get("operations") or [])
    masters = sorted(scope.get("masters") or [])
    pch = sorted(scope.get("portal_channels") or [])
    OUT["store_grant"] = {"status": grant.get("status"), "revision": grant.get("revision"), "operations": ops,
                          "masters": masters, "portal_channels": pch}
    active = prof.get("status") == "active" and grant.get("status") == "active"
    portal_only = bool(pch) and not masters
    OUT["store_tools"] = [] if (not active or portal_only) else sorted(
        t for t, op in DE.SCHWAB_TOOLS.items() if op is None or op in ops)

    b = BD._compute()
    chans = [c for c in b["channels"] if c["id"] != "m365"]
    ch = max(chans, key=lambda c: len(c["tools"]))
    held = [h for h in ch["holders"] if h["tools"]]
    pick = [h for h in held if h["who"] == "opalbloomberg@opalinvest.com"] or held
    if not pick:
        raise SystemExit("PC6ERR no_holder_in_channel=%s" % ch["id"])
    h = pick[0]
    OUT["channel"] = ch["id"]
    OUT["channel_catalog_tools"] = len(ch["tools"])
    OUT["breakdown_holder_who"] = h["who"]
    OUT["breakdown_holder_tools"] = sorted(h["tools"])
    page_rows = [x for x in people if x["who"] == h["who"]]
    OUT["page_rows_for_holder"] = len(page_rows)
    OUT["page_channel_tools"] = sorted({t["name"] for x in page_rows for c in x["channels"] if c["id"] == ch["id"]
                                        for t in c["tools"]})

    gs = G._compute()
    bx = {x["box"]: x for x in gs["boxes"]}
    OUT["gitstate_status"] = {k: bx[k]["status"] for k in ("laptop", "sitez", "dell1", "dell2") if k in bx}
    OUT["served_box_no"] = bx["laptop"]["integration_refused"]
    OUT["served_box_not_recorded"] = bx["sitez"]["integration_refused"]
except SystemExit as e:
    OUT["error"] = str(e)
except Exception as e:
    OUT["error"] = "%s: %s" % (type(e).__name__, e)
print("PC6 " + json.dumps(OUT, sort_keys=True, default=lambda o: int(o) if o == int(o) else float(o)))
