"""Writes the SSM params file for the S1 served BODY read (the issuer's real run, MP-pf-4 item iii): argv[1] = output path. One read-only command on the
gateway host under the instance role: the SERVED breakdown module's own `_compute()` (the body `/api/admin/gateway/breakdown` answers), from the host's venv,
printed as ONE line `S1BODY <base64 of gzip of JSON>` (SSM truncates stdout at 24 KB, so the body travels compressed). `import app.server` comes first (row Z-S48).
The caller redacts every `holders[].who` before anything is written to the repo."""
import json
import sys

PROBE = (
    "import app.server\n"
    "import base64, gzip, json\n"
    "from app import admin_gateway_breakdown as B\n"
    "d = B._compute()\n"
    "raw = json.dumps(d, default=str, separators=(',', ':')).encode('utf-8')\n"
    "print('S1BODY ' + base64.b64encode(gzip.compress(raw)).decode('ascii'))\n"
)

cmd = (
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_pf4_body.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_pf4_body.py 2>&1 "
    "| grep -m1 '^S1BODY '; rm -f /tmp/mp_pf4_body.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
