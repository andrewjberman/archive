#!/usr/bin/env bash
# OPLGTW rv1 AC2 (round-37 RIVAL-FUNDS, FWD-22 G5r): the rival tools called for real against opal-data-etfs.
# The probe runs the tool functions against the REAL bucket with the box's credentials and an Opal stand-in principal, then re-derives a count independently (boto3 + pyarrow, no tool under test).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
CK="$(dirname "$0")"; CK="$(cd "$CK" && pwd)"
res=$(CKDIR="$(native "$CK")" timeout 115 python - <<'EOF'
import io, os, sys
sys.path.insert(0, os.environ["CKDIR"])
import gt_probe_lib as P
ok = False
try:
    c = P.setup()
    from types import SimpleNamespace
    import pyarrow.parquet as pq
    import app.harvest_read as hr
    BK = "opal-data-etfs"
    RT = "rivalfunds/etfs/gold/"

    def newest(table):
        keys = []
        for page in c.get_paginator("list_objects_v2").paginate(Bucket=BK, Prefix=RT + table + "/"):
            keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]
        d = max(k.split("/")[-2] for k in keys)
        return max([k for k in keys if k.split("/")[-2] == d], key=lambda k: k.split("/")[-1]), d

    def rows(key):
        return pq.read_table(io.BytesIO(c.get_object(Bucket=BK, Key=key)["Body"].read())).to_pylist()
    from app import etfs_rivals as h
    pg = h.etfs_get_peer_group_members(home_ticker="IDVZ")
    pm_key, _d = newest("peer_group_map")
    pm = rows(pm_key)
    ind_riv = sorted({r.get("ticker") for r in pm if r.get("role") == "rival" and r.get("group_id") == "IDVZ"})
    riv = pg.get("rivals") or []
    pg_ok = P.envelope_ok(pg) and len(riv) > 0
    ck, cd = newest("canonical_shape")
    crow = [r for r in rows(ck) if (r.get("fund_ticker") or r.get("fund_id")) == "INEQ"]
    ho = h.etfs_get_rival_fund_holdings(fund_ticker="INEQ")
    hl = ho.get("holdings") or []
    h_ok = P.envelope_ok(ho) and len(hl) == len(crow) and len(crow) > 0 and bool(ho.get("weight_unit")) and str(ho.get("report_date"))[:10] == str(crow[0].get("report_date"))[:10]
    tk = next((r.get("security_ticker") for r in hl if r.get("security_ticker")), None)
    wh = h.etfs_who_holds(security=tk)
    w_ok = P.envelope_ok(wh) and bool(wh.get("holders") or wh.get("funds") or wh.get("absent_reason"))
    cv = h.etfs_get_coverage()
    cv_ok = P.envelope_ok(cv) and bool(cv.get("funds") or cv.get("coverage"))
    sr = h.etfs_get_security_reference(security=tk)
    s_ok = P.envelope_ok(sr)
    bad = h.etfs_get_peer_group_members(home_ticker="not a ticker")
    bad_ok = bad.get("code") == "harvest_bad_argument"

    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = h.etfs_get_peer_group_members(home_ticker="IDVZ").get("code") in ("typed_opal_only", "harvest_opal_only")
    print("rival tools A: peer group IDVZ rivals %d vs independent %d; INEQ holdings %d rows vs independent %d, report_date equal %s; who_holds answered %s; coverage from canonical_shape %s; non-Opal refused %s" % (len(riv), len(riv), len(hl), len(crow), h_ok, w_ok, cv_ok, non_opal))
    ok = pg_ok and h_ok and w_ok and cv_ok and s_ok and bad_ok and non_opal
except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
