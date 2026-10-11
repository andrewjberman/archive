"""OG-wr-1 runner (from OG-rl-15's r29_ssm_grant.py 'real' branch): ships wr1_ssm_prog.py to the opal-gateway host as ONE SSM RunShellScript, runs it in the
installed venv under env -i from a per-run scratch removed in the same command list, saves the output redacted of the holder's tid/oid and masters, and writes
WR1_READ.json from the host's WR1_BODY line only if the host's WR1_DIGEST matches. usage: python wr1_ssm_run.py <out-file> <json-dir>"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
outfile, jdir = sys.argv[1], sys.argv[2]


def aws(x):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + x, capture_output=True, text=True, encoding="utf-8", errors="replace")


pks = json.load(open(os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "ga1", "holder_pks.json"), encoding="utf-8"))
assert len(pks) == 1
secrets = list(pks[0])
b64 = base64.b64encode(open(os.path.join(HERE, "wr1_ssm_prog.py"), encoding="utf-8").read().encode("utf-8")).decode("ascii")
S = "/tmp/og_wr1_%d" % os.getpid()
cmds = ["S=%s; rm -rf $S; mkdir -p $S" % S]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds += ["base64 -d $S/p.b64 > $S/run.py; md5sum $S/run.py",
         "cd /opt/opal-gateway && env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S GA1_TID='%s' GA1_OID='%s' timeout 1700 /opt/opal-gateway/.venv/bin/python $S/run.py 2>&1 | tail -80; echo RUN_RC=${PIPESTATUS[0]}" % (secrets[0], secrets[1]),
         "rm -rf $S", "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)", "echo HOST_TMP_og_wr1_LEFTOVER=$(ls -d /tmp/og_wr1* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_wr1_params_%d.json" % os.getpid())
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["1800"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-wr-1 prime and measure the 13-month read",
         "--timeout-seconds", "1800", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
os.remove(pf)
if r.returncode != 0:
    print("SEND FAIL", r.stderr.strip()[:300])
    sys.exit(2)
cid = r.stdout.strip()
print("SENT", cid, flush=True)
st = ""
for _ in range(400):
    time.sleep(5)
    st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
def q(f):
    return aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", f, "--output", "text"]).stdout


out, err = q("StandardOutputContent"), q("StandardErrorContent")


def red(t):
    for i, s in enumerate(secrets):
        t = t.replace(s, "<tid>" if i == 0 else "<oid>")
    return re.sub(r'"master": "[0-9]+"', '"master": "<master>"', t.replace("\r", ""))


text = "ssm %s status=%s\n%s" % (cid, st, red(out))
if err.strip() and err.strip() != "None":
    text += "STDERR_TAIL: " + red(err)[-1500:] + "\n"
print(text)
open(outfile, "w", encoding="utf-8", newline="\n").write(text)
o = out.replace("\r", "")
m = re.search(r"^WR1_BODY (\{.*\})$", o, re.M)
dg = re.search(r"^WR1_DIGEST ([0-9a-f]{64})$", o, re.M)
if st == "Success" and m and dg and hashlib.sha256(json.dumps(json.loads(m.group(1)), sort_keys=True).encode("utf-8")).hexdigest() == dg.group(1):
    open(os.path.join(jdir, "WR1_READ.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"body": json.loads(m.group(1)), "instance_id": INST, "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
    print("wrote WR1_READ.json")
else:
    print("NOT WRITTEN (status/marker/digest)")
sys.exit(0 if st == "Success" and "SCRATCH_REMOVED=yes" in out and "RUN_RC=0" in out else 1)
