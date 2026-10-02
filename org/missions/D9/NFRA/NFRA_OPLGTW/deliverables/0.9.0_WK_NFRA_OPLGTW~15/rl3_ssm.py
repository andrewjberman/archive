"""OG-rl-3 helper: run a python program on the opal-gateway host by SSM (base64-shipped), print stdout.
usage: python rl3_ssm.py <prog.py>   (the program text may contain @@MD5@@, replaced by tr_release_md5.txt's text)
Never prints an .env value; the caller's program is responsible for printing names/booleans only."""
import base64
import json
import os
import subprocess
import sys
import time
HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace")
prog = open(sys.argv[1], encoding="utf-8").read()
prog = prog.replace("@@MD5@@", open(os.path.join(HERE, "tr_release_md5.txt"), encoding="utf-8").read().replace("\r", ""))
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_rl3.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_rl3.py", "rm -f /tmp/og_rl3.py"]})
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl3_params.json")
open(pf, "w", encoding="utf-8", newline="\n").write(params)
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-3 host read",
         "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
if r.returncode != 0:
    print("SEND FAIL", r.stderr.strip()[:300])
    sys.exit(2)
cid = r.stdout.strip()
st = ""
for _ in range(40):
    time.sleep(3)
    st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
print("ssm %s status=%s" % (cid, st))
print(out)
