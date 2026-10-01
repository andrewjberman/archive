"""Print the SSM AWS-RunShellScript --parameters JSON for pr.AC3: on the gateway host, read gateway/principals/rosters
under the host's own role and print its SHAPE only (pair counts), never a value.

The parser travels base64-encoded and is decoded to a file on the host, so no shell quoting touches it (row
Z-W18-S4: a literal backslash-n inside a double-quoted `python3.11 -c` argument raised a SyntaxError on the host)."""
import base64
import json

PARSE_LINES = [
    "import json, re, sys",
    "d = json.load(sys.stdin)",
    "r = re.compile(r'^[0-9a-fA-F-]{36}/[0-9a-fA-F-]{36}$')",
    "w = d['write_capable'].split(',')",
    "m = 1 if r.match(d['master_admin']) else 0",
    "print('ROSTERS master %d write %d all-pairs %s' % (m, len(w), all(r.match(x) for x in w)))",
]
PARSE = chr(10).join(PARSE_LINES) + chr(10)
B64 = base64.b64encode(PARSE.encode("ascii")).decode("ascii")
CMDS = [
    "echo %s | base64 -d > /tmp/og_pr_ac3.py" % B64,
    "aws secretsmanager get-secret-value --secret-id gateway/principals/rosters --region us-east-1"
    " --query SecretString --output text | python3.11 /tmp/og_pr_ac3.py",
    "rm -f /tmp/og_pr_ac3.py",
]
print(json.dumps({"commands": CMDS}))
