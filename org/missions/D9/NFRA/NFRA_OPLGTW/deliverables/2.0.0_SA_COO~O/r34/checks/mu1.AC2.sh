#!/usr/bin/env bash
# OPLGTW OG-mu-1 AC2 (round-34 E1, row W49-S4, route (a)): infra/aws/terraform/opal-gateway carries ONE PutObject
# statement for the market_update prefix, whose resource derives from a REQUIRED variable market_update_s3_root (no
# default) validated to end in /bronze/market_update/. No bucket or prefix literal is hand-typed in the statement.
# terraform validate passes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
python - <<'PY'
import glob, re
src = "\n".join(open(p, encoding="utf-8").read() for p in sorted(glob.glob("infra/aws/terraform/opal-gateway/*.tf")))
var = re.search(r'variable\s+"market_update_s3_root"\s*\{(.*?)\n\}', src, re.S)
has_var = bool(var); no_default = has_var and "default" not in var.group(1)
validated = has_var and "/bronze/market_update/" in var.group(1) and "validation" in var.group(1)
stmts = [m for m in re.finditer(r'(?s)"s3:PutObject".{0,600}?var\.market_update_s3_root|var\.market_update_s3_root.{0,600}?"s3:PutObject"', src)]
typed = re.findall(r'arn:aws:s3:::opal-data-transcripts/sharepoint/transcripts/bronze/market_update', src)
print("variable market_update_s3_root: %s; required (no default): %s; validated to /bronze/market_update/: %s; "
      "PutObject statements on the var: %d (want 1); hand-typed market_update ARNs: %d (want 0)"
      % (has_var, no_default, validated, len(stmts), len(typed)))
raise SystemExit(0 if (has_var and no_default and validated and len(stmts) == 1 and not typed) else 1)
PY
static=$?
( cd infra/aws/terraform/opal-gateway && { [ -d .terraform ] || timeout 110 terraform init -backend=false -input=false -no-color >/dev/null 2>&1; } )
val=$(cd infra/aws/terraform/opal-gateway && timeout 110 terraform validate -no-color 2>&1 | tr -d '\r' | grep -m1 -E 'Success|Error' )
echo "terraform validate: ${val:-NO VERDICT LINE}"
[ "$static" = 0 ] && printf '%s' "$val" | grep -q "Success" && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
