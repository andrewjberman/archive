"""Print the SSM AWS-RunShellScript --parameters JSON for pr.AC3: on the gateway host, read gateway/principals/rosters
under the host's own role and print its SHAPE only (pair counts), never a value."""
import json

PARSE = (
    "import json,re,sys\n"
    "d=json.load(sys.stdin)\n"
    "r=re.compile(r'^[0-9a-fA-F-]{36}/[0-9a-fA-F-]{36}$')\n"
    "w=d['write_capable'].split(',')\n"
    "print('ROSTERS master %d write %d all-pairs %s' % (1 if r.match(d['master_admin']) else 0, len(w),"
    " all(r.match(x) for x in w)))\n"
)
CMD = (
    "aws secretsmanager get-secret-value --secret-id gateway/principals/rosters --region us-east-1"
    " --query SecretString --output text | python3.11 -c %s" % json.dumps(PARSE)
)
print(json.dumps({"commands": [CMD]}))
