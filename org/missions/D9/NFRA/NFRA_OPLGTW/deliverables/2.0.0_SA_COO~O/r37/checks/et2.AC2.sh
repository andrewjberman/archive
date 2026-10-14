#!/usr/bin/env bash
# OPLGTW et2 AC2 (round-37 G1-TYPED, FWD-22): the two fund tools called for real against opal-data-etfs.
# The probe runs the tool function itself against the REAL bucket with the box's credentials and an Opal stand-in
# principal, then re-derives the answer independently (gt_probe_lib: boto3 + pyarrow, no tool under test).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
CK="$(dirname "$0")"; CK="$(cd "$CK" && pwd)"
res=$(CKDIR="$(native "$CK")" timeout 110 python - <<'EOF'
import os, sys
sys.path.insert(0, os.environ["CKDIR"])
import gt_probe_lib as P
ok = False
try:
    c = P.setup()

    import io
    from types import SimpleNamespace
    import pyarrow.parquet as pq
    import app.harvest_read as hr
    from app import etfs_funds as h
    BK = "opal-data-etfs"
    t = pq.read_table(io.BytesIO(c.get_object(Bucket=BK, Key="silver/netassets_daily.parquet")["Body"].read()))
    rows = t.to_pylist()
    dmax = max(r["date"] for r in rows)
    import datetime as dt
    dmin = dmax - dt.timedelta(days=30)
    sel = sorted([r for r in rows if r["ticker"] == "IDVZ" and dmin <= r["date"] <= dmax], key=lambda r: r["date"])
    nav = h.etfs_get_fund_nav_history(fund_ticker="IDVZ", start=dmin.date().isoformat(), end=dmax.date().isoformat())
    ser = nav.get("series") or []
    n_ok = len(ser) == len(sel) and len(sel) > 0 and abs(float(ser[-1].get("nav")) - float(sel[-1]["nav"])) < 1e-9 and P.envelope_ok(nav)
    bad = h.etfs_get_fund_nav_history(fund_ticker="NOPE")
    bad_ok = bad.get("code") == "harvest_bad_argument"
    hold = h.etfs_get_fund_holdings(fund_ticker="IDVZ")
    h_ok = P.envelope_ok(hold) and bool(hold.get("holdings")) and bool(hold.get("weight_unit")) and bool(hold.get("source_keys"))
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = h.etfs_get_fund_nav_history(fund_ticker="IDVZ").get("code") in ("typed_opal_only", "harvest_opal_only")
    print("etf funds: IDVZ nav series %d rows vs independent %d, last nav equal %s; unknown ticker refused %s; holdings answered with a weight unit %s (%d rows); non-Opal refused %s"
          % (len(ser), len(sel), n_ok, bad_ok, h_ok, len(hold.get("holdings") or []), non_opal))
    ok = n_ok and bad_ok and h_ok and non_opal

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
