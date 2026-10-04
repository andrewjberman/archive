"""OG-rl-4 helper: run a python program on the opal-gateway host by SSM (base64-shipped), print stdout.
usage: python rl4_ssm.py <prog.py> [md5file]   (@@MD5@@ in the program text is replaced by the md5 file's text, default rl4_live_md5.txt)
Never prints an .env value; the caller's program prints names/booleans/counts only."""
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
md5f = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "rl4_live_md5.txt")
prog = prog.replace("@@MD5@@", open(md5f, encoding="utf-8").read().replace("\r", ""))
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_rl4.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_rl4.py", "rm -f /tmp/og_rl4.py"]})
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl4_params.json")
open(pf, "w", encoding="utf-8", newline="\n").write(params)
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-4 host read",
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
os.remove(pf)
