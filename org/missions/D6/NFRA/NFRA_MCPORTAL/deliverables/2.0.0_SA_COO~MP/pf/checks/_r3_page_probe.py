"""Writes the SSM params file for the MP-pf-7 (R3) PAGE-side read: argv[1] = output path. One read-only command on the gateway host under
the instance role: the set the People view lists, i.e. `app.admin_gateway_breakdown._scan_principals(client)` (the host-role Scan of
`principal_profile` rows that `admin_people` and the People checks iterate). Prints ONE line, `R3PAGE {json}`: the set as 12-hex digests of
"<tid>:<oid>" (canonical lower-case GUIDs; never a raw id) and its size. `import app.server` comes first (row Z-S48)."""
import json
import sys

PROBE = (
    "import app.server\n"
    "import hashlib, json\n"
    "from app import admin_gateway_breakdown as B\n"
    "dg = lambda t, o: hashlib.sha256(('%s:%s' % (t, o)).encode()).hexdigest()[:12]\n"
    "a = sorted({dg(t, o) for t, o in B._scan_principals(B._ddb_client())})\n"
    "print('R3PAGE ' + json.dumps({'page_set': a, 'page_n': len(a)}))\n"
)

cmd = (
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_pf7_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_pf7_probe.py 2>&1 "
    "| grep -m1 '^R3PAGE '; rm -f /tmp/mp_pf7_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
