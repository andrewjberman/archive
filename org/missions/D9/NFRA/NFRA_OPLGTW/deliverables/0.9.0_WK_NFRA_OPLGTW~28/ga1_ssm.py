"""OG-ga-1 helper: run ga1_host_prelude.py.txt + ga1_host.py.txt on the opal-gateway host by SSM, in the venv, from a per-run scratch
dir removed in the same command list.  usage: python ga1_ssm.py <before|after> <out-file> <served_release_sha>
The holder's tid/oid are read from the OFF-REPO file %LOCALAPPDATA%/opal/og-salt/ga1/holder_pks.json and passed ONLY inside the
SSM parameters (exported in the command list). Output is redacted of those two values before printing/saving."""
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
mode, outfile, release = sys.argv[1], sys.argv[2], sys.argv[3]
X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "ga1")
pks = json.load(open(os.path.join(X, "holder_pks.json"), encoding="utf-8"))
assert len(pks) == 1
tid, oid = pks[0]


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace")


payload = open(os.path.join(HERE, "ga1_host_prelude.py.txt"), encoding="utf-8").read() + "\n\n" + \
    open(os.path.join(HERE, "ga1_host.py.txt"), encoding="utf-8").read()
b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
chunks = [b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds = ["S=/tmp/og_ga1_run; rm -rf $S; mkdir -p $S"]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % c for c in chunks]
cmds += ["base64 -d $S/p.b64 > $S/run.py",
         "cd /opt/opal-gateway && GA1_TID='%s' GA1_OID='%s' GA1_SERVED_RELEASE='%s' PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S OG_GA1_SCRATCH=$S OG_GA1_MODE=%s timeout 1500 /opt/opal-gateway/.venv/bin/python $S/run.py 2>&1 | tail -40; echo RUN_RC=${PIPESTATUS[0]}" % (tid, oid, release, mode),
         "rm -rf $S",
         "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_ga1_params.json")
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["1800"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-ga-1 host run " + mode,
         "--timeout-seconds", "1800", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1",
         "--query", "Command.CommandId", "--output", "text"])
os.remove(pf)
if r.returncode != 0:
    print("SEND FAIL", r.stderr.strip()[:300])
    sys.exit(2)
cid = r.stdout.strip()
st = ""
for _ in range(400):
    time.sleep(5)
    st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1",
              "--query", "Status", "--output", "text"]).stdout.strip()
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1",
           "--query", "StandardOutputContent", "--output", "text"]).stdout
err = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1",
           "--query", "StandardErrorContent", "--output", "text"]).stdout


def red(t):
    return t.replace(tid, "<tid>").replace(oid, "<oid>").replace("\r", "")


text = "ssm %s status=%s\n%s" % (cid, st, red(out))
if err.strip() and err.strip() != "None":
    text += "STDERR_TAIL: " + red(err)[-1500:]
print(text)
with open(outfile, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
