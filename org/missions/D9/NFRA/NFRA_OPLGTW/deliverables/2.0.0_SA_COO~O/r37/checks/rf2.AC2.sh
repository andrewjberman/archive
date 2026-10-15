#!/usr/bin/env bash
# OPLGTW rf2 AC2 (round-37 RIVAL-FUNDS, FWD-22 G5r): the rival tools called for real against opal-data-etfs.
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
    from app import etfs_rivals_flow as h
    tk_, td = newest("trade_schedule")
    trows = rows(tk_)
    fcol = "fund_ticker"
    ind = [r for r in trows if r.get(fcol) == "INEQ"]
    tr = h.etfs_get_fund_trades(fund_ticker="INEQ")
    trl = tr.get("trades") or []
    t_ok = P.envelope_ok(tr) and len(trl) == len(ind)
    fl = h.etfs_get_fund_flows(fund_ticker="INEQ")
    f_ok = P.envelope_ok(fl)
    cb = h.etfs_compare_peers(home_ticker="IDVZ", period="YTD", axis="security")
    c_ok = P.envelope_ok(cb) and bool((cb.get("buying") or {}).get("rows") or (cb.get("buying") or {}).get("absent_reason")) and "contribution" in cb
    rn = h.etfs_get_research_notes(fund_ticker="INEQ")
    notes = rn.get("notes") or rn.get("items") or []
    r_ok = P.envelope_ok(rn) and all(n_.get("ai_generated") is True and n_.get("model_version") for n_ in notes)
    pgs = h.etfs_get_rival_page_status()
    pg_ok = P.envelope_ok(pgs) and bool(pgs.get("funds")) and bool(pgs.get("source_keys")) and all("as_published" in str(f) and "as_in_canonical_shape" in str(f) for f in (pgs.get("funds") or [])[:1])
    bad = h.etfs_get_fund_trades(fund_ticker="INEQ", peer_group="IDVZ")
    bad_ok = bad.get("code") == "harvest_bad_argument"

    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = h.etfs_get_fund_flows(fund_ticker="INEQ").get("code") in ("typed_opal_only", "harvest_opal_only")
    print("rival tools B: INEQ trades window rows %d vs independent %d; flows answered %s; compare_peers both sections %s; research notes AI-labelled %s; page status newest revision %s; non-Opal refused %s" % (len(trl), len(ind), f_ok, c_ok, r_ok, pg_ok, non_opal))
    ok = t_ok and f_ok and c_ok and r_ok and pg_ok and bad_ok and non_opal
except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
