#!/usr/bin/env bash
# MX-s-9 AC2 (the pulled bronze, read from the served object): the seat's result file names ONE output on a line
# 'OUTPUT_KEY=s3://opal-data-bd/...'. That object exists, was written after the issuance, holds >=1 row, and its
# asset_id column is unique (one row per asset). Counts only are printed.
. "$(dirname "$0")/_root.sh"
R=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.4.0_DS_ClientPlatform~D/bd-asset-dim-rest.result.md
[ -f "$R" ] || { echo "result file absent: $R -- RESULT: FAIL"; exit 1; }
KEY=$(sed -n 's/^OUTPUT_KEY=\(s3:\/\/opal-data-bd\/[^ ]*\)$/\1/p' "$R" | head -1)
[ -n "$KEY" ] || { echo "no OUTPUT_KEY=s3://opal-data-bd/... line in the result -- RESULT: FAIL"; exit 1; }
ISSUED="$(git log -1 --format=%cI --grep='issue(NFRA_MCPINDEX.TO-MX-s-9' HEAD)"
AWS="$(pwd)/.tools/aws"; T="${TMPDIR:-/tmp}/mx_s9_ac2_$$"; mkdir -p "$T"; W=$(cygpath -m "$T" 2>/dev/null || echo "$T")
timeout 120 "$AWS" s3 cp "$KEY" "$W/out.bin" >/dev/null 2>&1
out=$(python - "$W/out.bin" "$KEY" "$ISSUED" <<'PY' 2>&1 | tr -d '\r'
import sys, os, datetime
p, key, issued = sys.argv[1], sys.argv[2], sys.argv[3]
if not os.path.exists(p) or os.path.getsize(p) == 0:
    print('object unreadable'); print('NOT-OK'); raise SystemExit(0)
import pandas as pd
df = pd.read_parquet(p) if key.endswith('.parquet') else pd.read_csv(p)
col = next((c for c in df.columns if c.lower() in ('asset_id', 'assetid')), None)
uniq = col is not None and df[col].is_unique
print('rows=%d asset_id column=%s unique=%s' % (len(df), col, uniq))
print('OK' if (len(df) >= 1 and uniq) else 'NOT-OK')
PY
)
lm=$(timeout 60 "$AWS" s3api head-object --bucket opal-data-bd --key "${KEY#s3://opal-data-bd/}" --query LastModified --output text 2>&1 | tr -d '\r')
rm -rf "$T"
after=$(python -c "import sys,datetime as d; a=d.datetime.fromisoformat(sys.argv[1].replace('Z','+00:00')); b=d.datetime.fromisoformat(sys.argv[2]); print('yes' if a>b else 'no')" "$lm" "$ISSUED" 2>/dev/null || echo no)
echo "key under opal-data-bd; LastModified after issue=$after; $(printf '%s\n' "$out" | head -1)"
if [ "$after" = yes ] && printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
