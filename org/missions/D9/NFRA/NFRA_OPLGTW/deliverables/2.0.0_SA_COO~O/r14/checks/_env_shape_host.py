"""Print the SSM AWS-RunShellScript --parameters JSON for a host read of /opt/opal-gateway/.env's SHAPE: per key, its
name, whether its value holds whitespace, whether it is double-quoted, and whether a systemd-style parse and a
bash-style (shlex) parse of the value agree; plus the sha256 of the host deploy/ contract copy (or ABSENT). Key names
and booleans only; no value is ever printed; .env is never sourced (row Z-S32 standing rule). The parser travels
base64 (row Z-W18-S4)."""
import base64
import json

PROG_LINES = [
    "import hashlib, os, re, shlex",
    "def sysd(v):",
    "    v = v.strip()",
    "    if len(v) >= 2 and v[0] == v[-1] and v[0] in (chr(34), chr(39)):",
    "        return v[1:-1]",
    "    return v",
    "def bash(v):",
    "    try:",
    "        p = shlex.split(v, posix=True)",
    "    except ValueError:",
    "        return None",
    "    return p[0] if len(p) == 1 else (None if p else '')",
    "rows = []",
    "for line in open('/opt/opal-gateway/.env', encoding='utf-8'):",
    "    m = re.match(r'^([A-Z0-9_]+)=(.*)$', line.rstrip(chr(10)))",
    "    if not m: continue",
    "    k, v = m.group(1), m.group(2)",
    "    ws = any(c.isspace() for c in sysd(v))",
    "    q = len(v) >= 2 and v[0] == v[-1] == chr(34)",
    "    agree = (sysd(v) == bash(v))",
    "    rows.append((k, ws, q, agree))",
    "for k, ws, q, agree in rows:",
    "    print('KEY %s ws=%s quoted=%s parsers_agree=%s' % (k, ws, q, agree))",
    "print('HOST env_keys %d whitespace_values %d disagreeing %d' % (len(rows), sum(1 for r in rows if r[1]),"
    " sum(1 for r in rows if not r[3])))",
    "f = '/opt/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json'",
    "print('HOST contract_sha256 %s' % (hashlib.sha256(open(f, 'rb').read()).hexdigest() if os.path.exists(f) else 'ABSENT'))",
]
B64 = base64.b64encode((chr(10).join(PROG_LINES) + chr(10)).encode("ascii")).decode("ascii")
print(json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_r14_env.py" % B64, "python3.11 /tmp/og_r14_env.py",
                               "rm -f /tmp/og_r14_env.py"]}))
