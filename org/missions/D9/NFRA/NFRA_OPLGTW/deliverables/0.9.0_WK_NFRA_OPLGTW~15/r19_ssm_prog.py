"""OG-rl-7 runner (from rl9_guard_ssm.py): ships a host program (first arg)  to the opal-gateway host by SSM and runs it, once per mode, as a SEPARATE process in the
installed venv with `env -i` (never the running service, never /opt/opal-gateway/.env), from a per-run scratch that is removed in the same command list.
usage: python r19_ssm_prog.py <program .py.txt> <out-file> <args-string> [<args-string> ...]   (each args-string is one run of the program, e.g. 'configured after')
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


progfile = sys.argv[1]
outfile = sys.argv[2]
modes = sys.argv[3:]
prog = open(os.path.join(HERE, progfile) if not os.path.isabs(progfile) and not os.path.exists(progfile) else progfile, encoding="utf-8").read()
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
chunks = [b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds = ["S=/tmp/og_r19_run; rm -rf $S; mkdir -p $S"]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % c for c in chunks]
cmds += ["base64 -d $S/p.b64 > $S/run.py", "md5sum $S/run.py"]
STAGE_FROM = os.environ.get("R19_STAGE_FROM")   # REHEARSAL: a scratch copy of the installed app/ + deploy/ carrying the RELEASE bytes of the three shipped service files
RUNDIR, GWENV = "/opt/opal-gateway", ""
if STAGE_FROM:
    import zlib
    cmds += ["mkdir -p $S/gw && cp -r /opt/opal-gateway/app $S/gw/app && cp -r /opt/opal-gateway/deploy $S/gw/deploy && find $S/gw -name __pycache__ -prune -exec rm -rf {} + ; true"]
    for i, rel in enumerate(("app/server.py", "app/admin_refusals.py", "app/integrations/schwab/envelope.py")):
        pb = base64.b64encode(zlib.compress(open(os.path.join(STAGE_FROM, rel), "rb").read(), 9)).decode("ascii")
        cmds += ["printf '%%s' '%s' >> $S/f%d.b64" % (pb[j:j + 3000], i) for j in range(0, len(pb), 3000)]
        cmds += ["base64 -d $S/f%d.b64 | /opt/opal-gateway/.venv/bin/python -c 'import sys,zlib;sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' > $S/gw/%s; md5sum $S/gw/%s" % (i, rel, rel)]
    RUNDIR, GWENV = "$S/gw", "OG_GW_DIR=$S/gw "
cmds += ["cd " + RUNDIR]
for m in modes:
    cmds.append("echo MODE=%s; env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S %s timeout 300 /opt/opal-gateway/.venv/bin/python $S/run.py %s; echo RUN_RC=$?" % (m.replace(" ", "_"), GWENV.strip(), m))
cmds += ["rm -rf $S", "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)", "echo HOST_TMP_og_r19_LEFTOVER=$(ls -d /tmp/og_r19* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r19_params.json")
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["900"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-7 PhaseA host program",
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
