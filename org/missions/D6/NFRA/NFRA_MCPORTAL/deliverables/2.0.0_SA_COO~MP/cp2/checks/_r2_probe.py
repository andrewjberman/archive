"""Writes the SSM params file for r2.AC3: argv[1] = output path. One command: the four no-identity status codes and the
served modules' own _compute timings and counts, run from the host's venv under the instance role."""
import json
import sys

PROBE = (
    "import time\n"
    "from app import admin_fabric_overlap as o, admin_fabric_gitstate as g, admin_fabric_calls as c\n"
    "t = time.time(); a = o._compute(6); ta = time.time() - t\n"
    "t = time.time(); b = g._compute(); tb = time.time() - t\n"
    "t = time.time(); d = c._compute('open'); td = time.time() - t\n"
    "print('overlap_s=%.1f deploys_read=%d gitstate_s=%.1f recorded=%d calls_s=%.1f published=%d' % (\n"
    "    ta, sum(1 for x in a['deploys'] if x['status'] == 'read'),\n"
    "    tb, sum(1 for x in b['boxes'] if x['status'] == 'recorded'),\n"
    "    td, sum(1 for x in d['boxes'] if x['status'] == 'published')))\n"
)

cmd = (
    "B=http://127.0.0.1:8080; "
    "echo \"/health=$(curl -s -o /dev/null -w %{http_code} $B/health)\"; "
    "for p in overlap gitstate calls; do echo \"$p=$(curl -s -o /dev/null -w %{http_code} $B/api/admin/fabric/$p)\"; done; "
    "echo \"close=$(curl -s -o /dev/null -w %{http_code} -X POST -H content-type:application/json -d {} "
    "$B/api/admin/fabric/calls/close)\"; "
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_r2_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_r2_probe.py 2>&1 "
    "| tail -1; rm -f /tmp/mp_r2_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
