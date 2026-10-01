#!/usr/bin/env bash
# MS-d-2 read-back RB (the CTO half's added void condition, CTO_NEVER_WIDEN_HALF_MS-d-2_20261001.md:36): on the LIVE host,
# in-process, as ec2-user with the deployed venv, call app.query_v0._fetch_capped on one firm key and one global key that
# query_v0 serves, with INTERNAL_READER_ROLE_ARN taken from the host .env when present (no other .env value is read or
# printed). Prints, per key, `ok bytes=N` or `err=<ExceptionClass>`, plus whether the ARN was set. Run it on 05e3eff563
# BEFORE the deploy (the baseline) and AFTER: an error class present after and absent before, for the same key, VOIDS
# the CTO half -> roll back.
. "$(dirname "$0")/_root.sh"
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_d2_rb.XXXXXX")"
python - "$T/params.json" <<'EOF'
import json, sys
py = r'''
import os, sys
sys.path.insert(0, "/opt/opal-gateway")
arn = ""
for line in open("/opt/opal-gateway/.env", encoding="utf-8"):
    if line.startswith("INTERNAL_READER_ROLE_ARN="):
        arn = line.split("=", 1)[1].strip()
if arn:
    os.environ["INTERNAL_READER_ROLE_ARN"] = arn
print("arn_set=%s" % ("yes" if arn else "no"))
from app import query_v0
for tag, key in (("firm", "platinum/mdpf/inflection/aum-metrics.json"), ("global", "json/benchmarks/etf_returns.json")):
    try:
        body, n = query_v0._fetch_capped(key)
        print("%s=ok bytes=%d" % (tag, n))
    except Exception as e:
        print("%s=err=%s" % (tag, type(e).__name__))
'''
cmd = "cd /opt/opal-gateway && sudo -u ec2-user /opt/opal-gateway/.venv/bin/python - <<'PYEOF'\n" + py + "\nPYEOF"
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"; rm -rf "$T"
v() { printf '%s\n' "$SSM_OUT" | sed -n "s/^$1=//p"; }
echo "ssm command=$SSM_CID status=$SSM_ST; arn_set=$(v arn_set); firm=$(v firm); global=$(v global)"
case "$(v firm)$(v global)" in *err=*) echo "RESULT: ERROR-CLASS-PRESENT"; exit 1;; esac
[ "$SSM_ST" = Success ] && { echo "RESULT: READS-OK"; exit 0; }
echo "RESULT: FAIL"; exit 1
