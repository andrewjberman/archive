"""Writes the SSM params file for pc5.AC2: argv[1] = output path. One command: no-identity status codes on the new route
and its deep link, then the SERVED modules' own _compute for /people and /fabric/gitstate, run from the host's venv under
the instance role. `import app.server` comes first: the served app registers its enabled integrations at that import
(row Z-S48), and without it _compute sees a channel set the live process does not serve."""
import json
import sys

PROBE = (
    "import app.server\n"
    "import time\n"
    "from app import admin_people as p, admin_fabric_gitstate as g\n"
    "t = time.time(); d = p._compute(); s = time.time() - t\n"
    "ppl = d['people']; persons = [x for x in ppl if x['kind'] == 'person']; pop = [x for x in ppl if x['kind'] == 'population']\n"
    "tools = [t for x in ppl for c in x['channels'] for t in c['tools']]\n"
    "cad = sum(1 for t in tools if t['cadence']['claim'] == 'absent')\n"
    "gs = g._compute()\n"
    "boxes = gs['boxes'] if isinstance(gs, dict) else gs\n"
    "st = []\n"
    "for b in boxes:\n"
    "    r = b.get('integration_refused')\n"
    "    st.append('not recorded' if r == 'not recorded' else ('refused' if r.get('refused') else 'no'))\n"
    "print('people_s=%.1f persons=%d population=%d tools=%d cadence_absent=%d grant_store=%s refused_states=%s' % (\n"
    "    s, len(persons), len(pop), len(tools), cad, d['grant_store']['status'], ','.join(sorted(set(st)))))\n"
)

cmd = (
    "B=http://127.0.0.1:8080; "
    "echo \"/health=$(curl -s -o /dev/null -w %{http_code} $B/health)\"; "
    "echo \"people=$(curl -s -o /dev/null -w %{http_code} $B/api/admin/people)\"; "
    "echo \"/people=$(curl -s -o /dev/null -w %{http_code} $B/people)\"; "
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_pc5_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_pc5_probe.py 2>&1 "
    "| tail -1; rm -f /tmp/mp_pc5_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
