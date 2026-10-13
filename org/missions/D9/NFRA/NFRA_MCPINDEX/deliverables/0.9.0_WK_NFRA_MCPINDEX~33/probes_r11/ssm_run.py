"""ssm_run.py <script.py> <out.txt>: READ-ONLY. Ships a probe to the gateway host via SSM AWS-RunShellScript (base64), runs it under the host venv as ec2-user, writes stdout. No write to AWS beyond the SSM command itself."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
AWS = os.path.join(os.getcwd(), ".tools", "aws")
INSTANCE = "i-07dccb1615503ac99"
src = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
cmd = ('echo ' + src + ' | base64 -d > /tmp/r9_probe.py; cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r9_probe.py 2>&1; rm -f /tmp/r9_probe.py')
p = os.path.join(tempfile.mkdtemp(), "params.json")
json.dump({"commands": [cmd]}, open(p, "w", encoding="utf-8"))
def run(a):
    return subprocess.run(["bash", AWS] + a, capture_output=True, text=True, encoding="utf-8", timeout=60).stdout.strip()
cid = run(["ssm", "send-command", "--instance-ids", INSTANCE, "--document-name", "AWS-RunShellScript", "--parameters", "file://" + p, "--query", "Command.CommandId", "--output", "text"])
st = ""
for _ in range(30):
    time.sleep(4)
    st = run(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INSTANCE, "--query", "Status", "--output", "text"])
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
o = run(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INSTANCE, "--query", "StandardOutputContent", "--output", "text"])
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(o.replace("\r", "") + "\n")
print("ssm command", cid, "status", st, "bytes", len(o))
