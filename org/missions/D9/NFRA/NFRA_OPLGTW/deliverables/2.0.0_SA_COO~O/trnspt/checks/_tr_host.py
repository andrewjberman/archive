"""Print the SSM AWS-RunShellScript --parameters JSON for tr.AC1's host reads: the sha256 of the served
app/taxsma_workbook.py, the .env key-name count, whether both TAXSMA_WORKBOOK_ keys are present, and whether the
identity value is empty (capability OFF). Key names and booleans only; no value is ever printed; .env is never sourced
(row Z-S32 standing rule). The parser travels base64 (row Z-W18-S4)."""
import base64
import json

PROG_LINES = [
    "import hashlib, re",
    "import os",
    "f = '/opt/opal-gateway/app/taxsma_workbook.py'",
    "mod = open(f, 'rb').read() if os.path.exists(f) else None",
    "keys, ident_empty, bearer_empty = [], None, None",
    "for line in open('/opt/opal-gateway/.env', encoding='utf-8'):",
    "    m = re.match(r'^([A-Z0-9_]+)=(.*)$', line.rstrip(chr(10)))",
    "    if not m: continue",
    "    keys.append(m.group(1))",
    "    if m.group(1) == 'TAXSMA_WORKBOOK_IDENTITY': ident_empty = (m.group(2).strip() == '')",
    "    if m.group(1) == 'TAXSMA_WORKBOOK_BEARER': bearer_empty = (m.group(2).strip() == '')",
    "print('HOST module_sha256 %s' % (hashlib.sha256(mod).hexdigest() if mod is not None else 'ABSENT'))",
    "print('HOST env_keys %d taxsma_keys %d identity_empty %s bearer_empty %s' % (len(keys),"
    " sum(1 for k in keys if k.startswith('TAXSMA_WORKBOOK_')), ident_empty, bearer_empty))",
]
B64 = base64.b64encode((chr(10).join(PROG_LINES) + chr(10)).encode("ascii")).decode("ascii")
print(json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_tr_ac1.py" % B64, "python3.11 /tmp/og_tr_ac1.py",
                               "rm -f /tmp/og_tr_ac1.py"]}))
