"""Writes the SSM params file for n1.AC3: argv[1] = output path. One command: /health and the no-identity status of
GET /api/admin/fabric/gitstate, then the SERVED module's own cold _compute, run in a fresh interpreter from the host's venv
under the instance role against the LIVE store, through a proxy that counts get_object calls."""
import json
import sys

PROBE = (
    "import time\n"
    "from app import admin_fabric_gitstate as g\n"
    "class P:\n"
    "    def __init__(self, c):\n"
    "        self.c, self.n = c, 0\n"
    "    def get_object(self, **kw):\n"
    "        self.n += 1\n"
    "        return self.c.get_object(**kw)\n"
    "    def get_paginator(self, name):\n"
    "        return self.c.get_paginator(name)\n"
    "p = P(g._s3_client()); t = time.time(); b = g._compute(p); dt = time.time() - t\n"
    "print('gitstate_s=%.1f body_fetches=%d recorded=%d' % (dt, p.n, sum(1 for x in b['boxes'] if x['status'] == 'recorded')))\n"
)

cmd = (
    "B=http://127.0.0.1:8080; "
    "echo \"/health=$(curl -s -o /dev/null -w %{http_code} $B/health)\"; "
    "echo \"gitstate=$(curl -s -o /dev/null -w %{http_code} $B/api/admin/fabric/gitstate)\"; "
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_n1_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_n1_probe.py 2>&1 "
    "| tail -1; rm -f /tmp/mp_n1_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
