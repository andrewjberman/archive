"""Print the SSM AWS-RunShellScript --parameters JSON for the OG-rl-3 host reads: the sha256 of the served
app/teams_route.py and app/taxsma_workbook.py, the .env key-name count, whether TEAMS_BEARER is present and non-empty,
whether TEAMS_BEARER_LABELS reads exactly 'teamsassist', and whether both TAXSMA_WORKBOOK_ values are still non-empty.
Key names and booleans only; no value is ever printed; .env is never sourced (row Z-S32 standing rule). The parser
travels base64 (row Z-W18-S4)."""
import base64
import json

PROG_LINES = [
    "import hashlib, os, re",
    "def sha(f):",
    "    return hashlib.sha256(open(f, 'rb').read()).hexdigest() if os.path.exists(f) else 'ABSENT'",
    "print('HOST teams_route_sha256 %s' % sha('/opt/opal-gateway/app/teams_route.py'))",
    "print('HOST taxsma_workbook_sha256 %s' % sha('/opt/opal-gateway/app/taxsma_workbook.py'))",
    "keys, vals = [], {}",
    "for line in open('/opt/opal-gateway/.env', encoding='utf-8'):",
    "    m = re.match(r'^([A-Z0-9_]+)=(.*)$', line.rstrip(chr(10)))",
    "    if not m: continue",
    "    keys.append(m.group(1)); vals[m.group(1)] = m.group(2).strip().strip(chr(34))",
    "tb = vals.get('TEAMS_BEARER')",
    "print('HOST env_keys %d teams_bearer_present %s teams_bearer_empty %s teams_labels_ok %s tax_nonempty %s' % ("
    " len(keys), tb is not None, (tb or '') == '', vals.get('TEAMS_BEARER_LABELS') == 'teamsassist',"
    " bool(vals.get('TAXSMA_WORKBOOK_BEARER')) and bool(vals.get('TAXSMA_WORKBOOK_IDENTITY'))))",
]
B64 = base64.b64encode((chr(10).join(PROG_LINES) + chr(10)).encode("ascii")).decode("ascii")
print(json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_ht_ac.py" % B64, "python3.11 /tmp/og_ht_ac.py",
                               "rm -f /tmp/og_ht_ac.py"]}))
