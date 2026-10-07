"""OG-rl-9 runner (from r19_ssm_prog.py): ships a host program (first arg) to the opal-gateway host by SSM and runs it, once per mode, as a SEPARATE process in the
installed venv with `env -i` (never the running service, never /opt/opal-gateway/.env), from a per-run scratch that is removed in the same command list.
usage: python r20_ssm_prog.py <program .py.txt> <out-file> <args-string> [<args-string> ...]   (each args-string is one run of the program, e.g. 'after')
env R23_STAGE_FROM=<gateway dir>: REHEARSAL -- stage a scratch copy of the installed app/ + deploy/ carrying the RELEASE bytes of R23_STAGE_FILES
(comma-separated, default the three shipped files) and run against it (OG_GW_DIR); the installed tree is untouched.
env R23_NO_ENVI=1: not used. Prints the SSM id, status and the program output (codes, booleans, md5s; no value). Writes the same to <out-file>."""
import base64
import json
import os
import subprocess
import sys
import time
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
SCR = "/tmp/og_r23_run"


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace")


progfile = sys.argv[1]
outfile = sys.argv[2]
modes = sys.argv[3:]
prog = open(progfile if os.path.exists(progfile) else os.path.join(HERE, progfile), encoding="utf-8").read()
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
chunks = [b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds = ["S=%s; rm -rf $S; mkdir -p $S" % SCR]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % c for c in chunks]
cmds += ["base64 -d $S/p.b64 > $S/run.py", "md5sum $S/run.py"]
STAGE_FROM = os.environ.get("R23_STAGE_FROM")
FILES = os.environ.get("R23_STAGE_FILES", "app/server.py,app/audit.py,app/integrations/schwab/engine.py").split(",")
RUNDIR, GWENV = "/opt/opal-gateway", ""
if STAGE_FROM:
    cmds += ["mkdir -p $S/gw && cp -r /opt/opal-gateway/app $S/gw/app && cp -r /opt/opal-gateway/deploy $S/gw/deploy && find $S/gw -name __pycache__ -prune -exec rm -rf {} + ; true"]
    for i, rel in enumerate(FILES):
        pb = base64.b64encode(zlib.compress(open(os.path.join(STAGE_FROM, rel), "rb").read(), 9)).decode("ascii")
        cmds += ["printf '%%s' '%s' >> $S/f%d.b64" % (pb[j:j + 3000], i) for j in range(0, len(pb), 3000)]
        cmds += ["base64 -d $S/f%d.b64 | /opt/opal-gateway/.venv/bin/python -c 'import sys,zlib;sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' > $S/gw/%s; md5sum $S/gw/%s" % (i, rel, rel)]
    RUNDIR, GWENV = "$S/gw", "OG_GW_DIR=$S/gw "
cmds += ["cd " + RUNDIR]
for m in modes:
    cmds.append("echo MODE=%s; env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S R23_SCRATCH=$S %s timeout 300 /opt/opal-gateway/.venv/bin/python $S/run.py %s; echo RUN_RC=$?" % (m.replace(" ", "_"), GWENV.strip(), m))
cmds += ["rm -rf $S", "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)", "echo HOST_TMP_og_r23_LEFTOVER=$(ls -d /tmp/og_r23* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r23_params_%d.json" % os.getpid())
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["900"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-9 PhaseA host program",
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
ok = "SCRATCH_REMOVED=yes" in out and "RESULT: FAIL" not in out and out.count("RUN_RC=0") == len(modes)
sys.exit(0 if ok else 1)
