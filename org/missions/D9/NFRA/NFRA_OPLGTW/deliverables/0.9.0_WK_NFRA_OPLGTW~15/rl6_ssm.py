"""OG-rl-6 helper: run rl6_host_prelude.py.txt + <program.py> on the opal-gateway host by SSM, in the venv, from a per-run scratch dir
that is removed in the same command list.  usage: python rl6_ssm.py <program.py> [out-file]
Prints the SSM command id, status, the program's stdout (counts/names only) and the scratch-removal line. The program's own
stdout is also written to [out-file] when given. Never reads /opt/opal-gateway/.env; sets PYTHONDONTWRITEBYTECODE so root writes
no .pyc under /opt/opal-gateway."""
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


prelude = open(os.path.join(HERE, "rl6_host_prelude.py.txt"), encoding="utf-8").read()
prog = open(sys.argv[1], encoding="utf-8").read()
payload = prelude + "\n\n" + prog
b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
chunks = [b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds = ["S=/tmp/og_rl6_run; rm -rf $S; mkdir -p $S"]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % c for c in chunks]
PATCH = os.environ.get("OG_RL6_STAGE_FILE")   # REHEARSAL: stage a scratch app/ copy whose integration.py is the RELEASE file (shipped zlib+base64, md5 printed); the installed tree is untouched
STAGE = ""
if PATCH:
    import zlib
    pb = base64.b64encode(zlib.compress(open(PATCH, "rb").read(), 9)).decode("ascii")
    pchunks = [pb[i:i + 3000] for i in range(0, len(pb), 3000)]
    cmds += ["mkdir -p $S/gw && cp -r /opt/opal-gateway/app $S/gw/app && find $S/gw -name __pycache__ -prune -exec rm -rf {} + ; true"]
    cmds += ["printf '%%s' '%s' >> $S/rel.b64" % c for c in pchunks]
    cmds += ["base64 -d $S/rel.b64 | /opt/opal-gateway/.venv/bin/python -c 'import sys,zlib;sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' > $S/gw/app/integrations/schwab/integration.py; echo STAGE_RC=$?",
             "md5sum $S/gw/app/integrations/schwab/integration.py"]
    STAGE = "OG_RL6_STAGE=$S/gw "
cmds += ["base64 -d $S/p.b64 > $S/run.py",
         "df -h /tmp | tail -1",
         "cd /opt/opal-gateway && PYTHONDONTWRITEBYTECODE=1 " + STAGE + "TMPDIR=$S OG_RL6_SCRATCH=$S OG_RL6_MODE=" + os.environ.get("OG_RL6_MODE", "after") + " timeout 1500 /opt/opal-gateway/.venv/bin/python $S/run.py; echo RUN_RC=$?",
         "rm -rf $S",
         "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)",
         "echo HOST_TMP_og_rl6_LEFTOVER=$(ls -d /tmp/og_rl6* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl6_params.json")
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["1800"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-6 host run",
         "--timeout-seconds", "1800", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1",
         "--query", "Command.CommandId", "--output", "text"])
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
print("ssm %s status=%s" % (cid, st))
print(out)
if err.strip() and err.strip() != "None":
    print("STDERR_TAIL:", err[-1500:])
if len(sys.argv) > 2:
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as fh:
        fh.write("ssm %s status=%s\n" % (cid, st) + out.replace("\r", ""))
os.remove(pf)
