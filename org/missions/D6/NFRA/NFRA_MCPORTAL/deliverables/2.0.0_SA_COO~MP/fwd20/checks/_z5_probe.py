"""Writes the SSM params file for z5.AC2: argv[1] = output path. One command: no-identity status codes on the new and
deep-link routes, then the served module's own _compute run from the host's venv under the instance role."""
import json
import sys

PROBE = (
    "import time\n"
    "from app import admin_gateway_breakdown as b\n"
    "t = time.time(); d = b._compute(); s = time.time() - t\n"
    "chans = d['channels']; tools = sum(len(c['tools']) for c in chans)\n"
    "names = [t['name'] for c in chans for t in c['tools']]\n"
    "held = sum(1 for c in chans if c['holders'])\n"
    "gs = d['grant_store']\n"
    "print('breakdown_s=%.1f channels=%d tools=%d dup_tools=%d channels_held=%d grant_store=%s principals=%s' % (\n"
    "    s, len(chans), tools, len(names) - len(set(names)), held, gs['status'], gs['principals']))\n"
)

cmd = (
    "B=http://127.0.0.1:8080; "
    "echo \"/health=$(curl -s -o /dev/null -w %{http_code} $B/health)\"; "
    "echo \"breakdown=$(curl -s -o /dev/null -w %{http_code} $B/api/admin/gateway/breakdown)\"; "
    "for p in control-plane open-calls gateway; do echo \"/$p=$(curl -s -o /dev/null -w %{http_code} $B/$p)\"; done; "
    "echo \"/no-such-page-z5=$(curl -s -o /dev/null -w %{http_code} $B/no-such-page-z5)\"; "
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_z5_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_z5_probe.py 2>&1 "
    "| tail -1; rm -f /tmp/mp_z5_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
