"""Writes the SSM params file for the S1 served arm (the issuer's real run, MP-pf-4): argv[1] = output path. One read-only command on the
gateway host under the instance role: the SERVED breakdown module's own `_compute`, from the host's venv. Prints ONE line, `S1 {json}`:
channels (id, kind, tool count), and for each channel that carries `segments`, every (vendor, firm, tool count). `import app.server` comes first
(the served app registers its enabled integrations at that import, row Z-S48)."""
import json
import sys

PROBE = (
    "import app.server\n"
    "import json\n"
    "from app import admin_gateway_breakdown as B\n"
    "d = B._compute()\n"
    "ch = [{'id': c['id'], 'kind': c['kind'], 'tools': len(c['tools'])} for c in d['channels']]\n"
    "seg = {c['id']: [[s['vendor'], s['firm'], len(s['tools'])] for s in c['segments']] for c in d['channels'] if c.get('segments')}\n"
    "print('S1 ' + json.dumps({'channels': ch, 'segments': seg, 'tools': sum(c['tools'] for c in ch)}))\n"
)

cmd = (
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_pf4_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_pf4_probe.py 2>&1 "
    "| grep -m1 '^S1 ' ; rm -f /tmp/mp_pf4_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
