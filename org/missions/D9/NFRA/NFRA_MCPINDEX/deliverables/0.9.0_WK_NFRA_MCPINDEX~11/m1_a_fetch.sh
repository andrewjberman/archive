#!/usr/bin/env bash
# MX-m-1 (a) fetch: READ-ONLY. list-commands per BD document, list-command-invocations --details per command,
# S3 version list per log prefix, log object fetched BY VersionId. Writes only under $OUT (default .scratch/a).
# Cutoff: only commands requested at or before CUTOFF_UTC are analysed (the 22:10Z scheduled asset-dim run and later are excluded).
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
OUT=${OUT:-.scratch/a}; mkdir -p "$OUT/inv" "$OUT/logs"
DOCS="opal-bd-49f-session-fetch opal-bd-allocation-download opal-bd-asset-dim-download opal-bd-fees-download opal-bd-realized-download opal-bd-transaction-download opal-bd-unrealized-download"
timeout 120 .tools/aws ssm list-documents --filters Key=Owner,Values=Self --output json > "$OUT/documents.json"
for d in $DOCS; do
  timeout 300 .tools/aws ssm list-commands --filters key=DocumentName,value=$d --output json > "$OUT/cmds_$d.json"
  timeout 120 .tools/aws ssm get-document --name $d --document-version '$LATEST' --output json > "$OUT/latest_$d.json"
  timeout 60 .tools/aws ssm list-document-versions --name $d --output json > "$OUT/docvers_$d.json"
done
for d in $DOCS; do
  for id in $(python -c "
import json
for x in json.load(open('$OUT/cmds_$d.json',encoding='utf-8'))['Commands']: print(x['CommandId'])" | tr -d '\r'); do
    [ -s "$OUT/inv/$id.json" ] || timeout 60 .tools/aws ssm list-command-invocations --command-id $id --details --output json > "$OUT/inv/$id.json"
  done
done
for p in allocation asset-dim fees realized transaction unrealized; do
  timeout 120 .tools/aws s3api list-object-versions --bucket opal-data-bd --prefix logs/$p-download- --output json > "$OUT/ver_$p.json"
done
