"""OG-rl-6 PHASE C-B T2 (i) runner: ships rl9_guard_arms_host.py.txt to the opal-gateway host by SSM and runs it, once per mode, as a SEPARATE process in the
installed venv with `env -i` (never the running service, never /opt/opal-gateway/.env), from a per-run scratch that is removed in the same command list.
usage: python rl9_guard_ssm.py <out-file> <mode> [<mode> ...]      modes: owner empty missing preflight
Prints the SSM id, status and the program output (codes, booleans, md5 of the loaded deployed files; no value). Writes the same to <out-file>."""
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


outfile = sys.argv[1]
modes = sys.argv[2:]
prog = open(os.path.join(HERE, "rl9_guard_arms_host.py.txt"), encoding="utf-8").read()
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
chunks = [b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds = ["S=/tmp/og_rl9_run; rm -rf $S; mkdir -p $S"]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % c for c in chunks]
cmds += ["base64 -d $S/p.b64 > $S/run.py", "md5sum $S/run.py", "cd /opt/opal-gateway"]
for m in modes:
    cmds.append("echo MODE=%s; env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S timeout 300 /opt/opal-gateway/.venv/bin/python $S/run.py %s; echo RUN_RC=$?" % (m, m))
cmds += ["rm -rf $S", "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)", "echo HOST_TMP_og_rl9_LEFTOVER=$(ls -d /tmp/og_rl9* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl9_params.json")
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["900"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-6 PhaseC-B T2 guard arms",
         "--timeout-seconds", "900", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
os.remove(pf)
if r.returncode != 0:
    print("SEND FAIL", r.stderr.strip()[:300])
    sys.exit(2)
cid = r.stdout.strip()
st = ""
for _ in range(300):
    time.sleep(4)
    st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
err = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardErrorContent", "--output", "text"]).stdout
text = "ssm %s status=%s\n%s" % (cid, st, out.replace("\r", ""))
if err.strip() and err.strip() != "None":
    text += "STDERR_TAIL: " + err[-1500:] + "\n"
print(text)
with open(outfile, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
ok = all(("T2_ARMS %s" % m) in out and ("T2_ARMS %s path" % m) in out for m in modes) and "RESULT: FAIL" not in out and "SCRATCH_REMOVED=yes" in out
sys.exit(0 if ok else 1)
