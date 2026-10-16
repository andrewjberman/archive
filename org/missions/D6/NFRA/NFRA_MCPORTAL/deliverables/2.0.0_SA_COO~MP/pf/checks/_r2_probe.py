"""Writes the SSM params file for the MP-pf-6 (R2) read: argv[1] = output path. One command, read-only, on the host under the
instance role. It prints ONE line, `R2 {json}`, holding both principal sets as 12-hex digests of "tid:oid" (never a raw id),
their counts, and the page counts of the two Scans (so a truncated read shows).
  set A  `app.admin_gateway_breakdown._scan_principals(client)`, the host-role Scan the page and the People check iterate;
  set B  the distinct (tid, oid) of the grant writer's OWN changes table, `mcportal-grant-changes-table`, by a Scan of this
         probe's own that follows LastEvaluatedKey (admin_grants.read_changes_table reads ONE page and would truncate).
`import app.server` comes first: the served app registers its enabled integrations at that import (row Z-S48)."""
import json
import sys

PROBE = (
    "import app.server\n"
    "import hashlib, json\n"
    "from app import admin_gateway_breakdown as B, admin_grants as G\n"
    "from app.context import canonical_guid\n"
    "dg = lambda t, o: hashlib.sha256(('%s:%s' % (t, o)).encode()).hexdigest()[:12]\n"
    "a = sorted({dg(t, o) for t, o in B._scan_principals(B._ddb_client())})\n"
    "cl = G._changes_ddb_client(); start = None; pages = 0; items = 0; b = set(); bad = 0\n"
    "while True:\n"
    "    kw = {'TableName': 'mcportal-grant-changes-table'}\n"
    "    if start: kw['ExclusiveStartKey'] = start\n"
    "    r = cl.scan(**kw); pages += 1\n"
    "    for it in r.get('Items') or []:\n"
    "        items += 1\n"
    "        try: b.add(dg(canonical_guid(it['tid']['S']), canonical_guid(it['oid']['S'])))\n"
    "        except Exception: bad += 1\n"
    "    start = r.get('LastEvaluatedKey')\n"
    "    if not start: break\n"
    "print('R2 ' + json.dumps({'scan_set': a, 'scan_n': len(a), 'history_set': sorted(b), 'history_n': len(b),\n"
    "    'history_items': items, 'history_pages': pages, 'history_unparsed_items': bad}))\n"
)

cmd = (
    "printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_pf6_probe.py; "
    "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway "
    "MCPORTAL_CHANGES_TABLE=mcportal-grant-changes-table .venv/bin/python /tmp/mp_pf6_probe.py 2>&1 "
    "| tail -3; rm -f /tmp/mp_pf6_probe.py"
)

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
