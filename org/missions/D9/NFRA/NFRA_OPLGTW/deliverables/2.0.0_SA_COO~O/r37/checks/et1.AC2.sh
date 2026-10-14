#!/usr/bin/env bash
# OPLGTW et1 AC2 (round-37 G1-TYPED, FWD-22): the three ownership tools called for real against opal-data-etfs.
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

    import json
    from types import SimpleNamespace
    import app.harvest_read as hr
    from app import etfs_ownership as h
    BK = "opal-data-etfs"
    def lst(prefix, delim=None):
        out = []
        kw = {"Bucket": BK, "Prefix": prefix}
        if delim:
            kw["Delimiter"] = delim
        for page in c.get_paginator("list_objects_v2").paginate(**kw):
            out += [o["Key"] for o in page.get("Contents", [])]
            out += [("P:" + p["Prefix"]) for p in page.get("CommonPrefixes", [])]
        return out
    def rows_of(obj):
        if isinstance(obj, list):
            return len(obj)
        if isinstance(obj, dict):
            ls = [v for v in obj.values() if isinstance(v, list)]
            return max((len(v) for v in ls), default=0)
        return 0
    keys = [k for k in lst("daily/49financial/") if k.endswith(".json")]
    newest = max(keys) if keys else None
    indep_rows = rows_of(json.loads(c.get_object(Bucket=BK, Key=newest)["Body"].read())) if newest else None
    d1 = h.etfs_get_partner_ownership(firm="49financial")
    d_src = d1.get("source_keys") or []
    d_ok = bool(newest) and d_src == [newest] and len(d1.get("rows") or []) == indep_rows and P.envelope_ok(d1)
    bad = [h.etfs_get_partner_ownership(firm=f) for f in ("", "49financial,cottonwood", "not-a-partner")]
    bad_ok = all(b.get("code") == "harvest_bad_argument" for b in bad)
    roll = h.etfs_get_ownership_rollup()
    roll_ok = (roll.get("source_keys") == ["platinum/etf_ownership_dashboard.json"]) and P.envelope_ok(roll) and str(roll.get("as_of") or "") in c.get_object(Bucket=BK, Key="platinum/etf_ownership_dashboard.json")["Body"].read().decode("utf-8", "replace")
    months = sorted(p[2:].rstrip("/").split("/")[-1] for p in lst("platinum/reports/", "/") if p.startswith("P:") and p[2:].rstrip("/").split("/")[-1][:2] == "20")
    month = months[-1] if months else None
    mon = h.etfs_get_monthly_report(month=month)
    cov_ok = bool(month)
    cov_tool = mon.get("coverage") or {}
    for k in lst("platinum/reports/%s/" % month):
        if k.endswith(".csv"):
            partner = k.rsplit("/", 1)[1].split("_")[1]
            txt = c.get_object(Bucket=BK, Key=k)["Body"].read().decode("utf-8", "replace")
            line = next((ln for ln in txt.splitlines() if ln.lstrip().startswith("# coverage:")), None)
            want = line.split("# coverage:", 1)[1].strip() if line else None
            cov_ok = cov_ok and want is not None and str(cov_tool.get(partner, "")).strip() == want
    verdict_read = any("coverage_verdict" in k for k in (mon.get("source_keys") or []))
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = h.etfs_get_ownership_rollup().get("code") in ("typed_opal_only", "harvest_opal_only")
    print("etf ownership: partner file %s rows %s vs independent %s; firm-required refusals %s; rollup own as-of %s; monthly coverage from each csv %s, verdict not read %s; non-Opal refused %s"
          % ("newest" if d_ok else "MISMATCH", len(d1.get("rows") or []), indep_rows, bad_ok, roll_ok, cov_ok, not verdict_read, non_opal))
    ok = d_ok and bad_ok and roll_ok and cov_ok and (not verdict_read) and non_opal

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
