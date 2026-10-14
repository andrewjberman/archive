#!/usr/bin/env bash
# OPLGTW OG-ec-1 AC2 (round-37 FWD22-W8, row Z-S117): the vendored eclipse schema declares every column the REAL bronze portfolios_simple objects carry.
#  - reads eclipse/inflection/bronze/<date>/portfolios_simple.json for the dates 2026-10-10..2026-10-14 (read only) in opal-data-assets;
#  - declared = the vendored copy's arrow_schema("eclipse","portfolios_simple").names; extra and missing (ignoring the converter's own '_' provenance columns) must be empty;
#  - the vendored copy is byte-equal to the source, and defaultTradingEngineId is declared.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(timeout 110 python - <<'EOF'
import sys, json, filecmp
sys.path.insert(0, "infra/aws/lambda/opal-assets/opal-assets-silver-eclipse")
ok = False
try:
    import importlib
    ms = importlib.import_module("mirror_schemas")
    decl = list(ms.arrow_schema("eclipse", "portfolios_simple").names)
    import boto3
    c = boto3.client("s3"); BK = "opal-data-assets"
    days = ["2026-10-10", "2026-10-11", "2026-10-12", "2026-10-13", "2026-10-14"]
    checked = 0; extra = 0; missing = 0
    for d in days:
        try:
            o = json.loads(c.get_object(Bucket=BK, Key="eclipse/inflection/bronze/%s/portfolios_simple.json" % d)["Body"].read())
        except Exception:
            continue
        rows = o if isinstance(o, list) else next((v for v in o.values() if isinstance(v, list)), []) if isinstance(o, dict) else []
        keys = set()
        for r in rows:
            if isinstance(r, dict):
                keys |= set(r)
        checked += 1
        extra += len(keys - set(decl))
        missing += len([k for k in set(decl) - keys if not k.startswith("_")])
    same = filecmp.cmp("data/assets/scripts/silver/mirror_schemas.py", "infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_schemas.py", shallow=False)
    has = "defaultTradingEngineId" in decl
    print("eclipse portfolios_simple: bronze objects checked %d (2026-10-10..2026-10-14); extra columns %d; missing columns %d; vendored copy byte-equal to source %s; defaultTradingEngineId declared %s"
          % (checked, extra, missing, "yes" if same else "no", "yes" if has else "no"))
    ok = checked >= 3 and extra == 0 and missing == 0 and same and has
except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160]))
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
