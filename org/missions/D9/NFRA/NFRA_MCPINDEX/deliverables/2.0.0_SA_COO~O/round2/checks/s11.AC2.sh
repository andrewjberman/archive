#!/usr/bin/env bash
# MX-s-11 AC2 (the negative control, run on the PUBLISHED bytes): the pull module and its pin, fetched from the
# bucket into a scratch tree that holds NO lib/ at all, import cleanly, and the (bucket, key) the module writes for a
# fixed partition equals what the pre-pin module computed through opal_naming (oracle: the module at 7b98791aeb,
# run in this repo). An import that still needs opal_naming fails here, because the scratch tree cannot supply it.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
P=2026-09-28
t=$(mktemp -d); d="$t/data/black_diamond/scripts/bronze"; mkdir -p "$d"
for f in pull_bd_asset_dim_rest.py _asset_dim_rest_pin.py; do
  timeout 60 "$AWS" s3 cp "s3://opal-data-bd/code/bronze/$f" "$(native "$d/$f")" >/dev/null 2>&1
done
[ -f "$d/pull_bd_asset_dim_rest.py" ] && [ -f "$d/_asset_dim_rest_pin.py" ] || {
  echo "published pull+pin fetched=no -- lib-free import=no target equal=no -- RESULT: FAIL"; exit 1; }
git show 7b98791aeb:data/black_diamond/scripts/bronze/pull_bd_asset_dim_rest.py > "$t/pre.py"
exp=$(AWS_DEFAULT_REGION=us-east-1 python - "$(native "$t/pre.py")" "$P" <<'PY' 2>&1 | tr -d '\r'
import sys, importlib.util, os
sys.path.insert(0, os.getcwd())
s = importlib.util.spec_from_file_location("pre", sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
from lib import opal_naming
print("%s|%s/assets_dim_rest.parquet" % (m.S3_BUCKET, opal_naming.key(m.VENDOR, m.FIRM_SCOPE, "bronze", "assets_dim_rest", sys.argv[2])))
PY
)
got=$(cd "$t" && AWS_DEFAULT_REGION=us-east-1 python - "$(native "$d/pull_bd_asset_dim_rest.py")" "$P" <<'PY' 2>&1 | tr -d '\r'
import sys, importlib.util
s = importlib.util.spec_from_file_location("pub", sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
assert "lib.opal_naming" not in sys.modules and "opal_naming" not in sys.modules, "opal_naming was imported"
print("%s|%s" % (m.S3_BUCKET, m.bronze_key(sys.argv[2])))
PY
)
imp=no; printf '%s' "$got" | grep -q '|' && ! printf '%s' "$got" | grep -q 'Traceback' && imp=yes
eq=no; [ "$imp" = yes ] && [ "$(printf '%s' "$got" | tail -1)" = "$(printf '%s' "$exp" | tail -1)" ] && printf '%s' "$exp" | grep -q '|' && eq=yes
echo "published pull+pin fetched=yes lib-free import=$imp target equal=$eq"
[ "$imp" = yes ] || printf '%s\n' "$got" | tail -2
if [ "$imp" = yes ] && [ "$eq" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
