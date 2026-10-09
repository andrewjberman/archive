"""OG-rl-15 runner: ships a host program behind a committed prelude to the opal-gateway host by SSM, runs it in the installed venv from a per-run
scratch dir that is removed in the same command list. Never sources /opt/opal-gateway/.env; PYTHONDONTWRITEBYTECODE is set.
usage: python r28_ssm.py <synth|real|route> <mode> <out-file> <served_release> [--stage <release gateway dir>] [--json <dir>]
  synth : r28_synth_host.py.txt behind ../0.9.0_WK_NFRA_OPLGTW~15/rl6_host_prelude.py.txt (all in memory, synthetic principals); OG_RL6_MODE=<mode>
  real  : r29_grant_host.py.txt behind ./ga1_host_prelude.py.txt (HybridStore; POLICY# reads real, read-only); OG_GA1_MODE=<mode>; the holder's tid/oid are read
          from the OFF-REPO file %LOCALAPPDATA%/opal/og-salt/ga1/holder_pks.json, passed only inside the SSM parameters, and the output is redacted of them
  route : r28_route_host.py.txt (the GuardMiddleware stack of the installed code in a separate process, env -i, synthetic signed-in identity, REAL S3 reads by the instance role); R28_ROUTE line (A3: the chart route + its two neighbours); env R28_BEFORE_ROUTE = the BEFORE neighbour values
  --stage : REHEARSAL -- a host scratch copy of app/ + deploy/ whose shipped files that DIFFER between r28_live_md5.txt and r28_release_md5.txt are taken from the given
            release gateway dir (zlib+base64, md5 printed); the installed tree is untouched
  --json  : (real only) write <dir>/GA1_DOWNLOAD.json and <dir>/GA1_QUERY.json ({"body", "ssm_command_id", "instance_id"}) from the host's GA1_BODY / GA1Q_BODY lines
The raw output goes to <out-file> (counts only; the redaction is applied before saving)."""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
a = sys.argv[1:]
kind, mode, outfile, release = a[0], a[1], a[2], a[3]
stage = a[a.index("--stage") + 1] if "--stage" in a else None
jdir = a[a.index("--json") + 1] if "--json" in a else None


def aws(x):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + x, capture_output=True, text=True, encoding="utf-8", errors="replace")


if kind == "route":
    prelude = ""
    prog = open(os.path.join(HERE, "r28_route_host.py.txt"), encoding="utf-8").read()
    secrets = []
elif kind == "synth":
    prelude = open(os.path.join(HERE, "..", "0.9.0_WK_NFRA_OPLGTW~15", "rl6_host_prelude.py.txt"), encoding="utf-8").read()
    prog = open(os.path.join(HERE, "r28_synth_host.py.txt"), encoding="utf-8").read()
    secrets = []
else:
    prelude = open(os.path.join(HERE, "ga1_host_prelude.py.txt"), encoding="utf-8").read()
    prog = open(os.path.join(HERE, "r29_grant_host.py.txt"), encoding="utf-8").read()
    X = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-salt", "ga1")
    pks = json.load(open(os.path.join(X, "holder_pks.json"), encoding="utf-8"))
    assert len(pks) == 1
    secrets = list(pks[0])
payload = prelude + "\n\n" + prog
b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
S = "/tmp/og_r29g_%s_%d" % (kind, os.getpid())   # its own scratch name per run (row Z-W28-S9)
cmds = ["S=%s; rm -rf $S; mkdir -p $S" % S]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % b64[i:i + 3000] for i in range(0, len(b64), 3000)]
STAGE = ""
if stage:
    def _md5s(fn):
        return dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(os.path.join(HERE, fn), encoding="utf-8") if ln.strip())
    lv, rv = _md5s("r28_live_md5.txt"), _md5s("r28_release_md5.txt")
    files = sorted(k for k in rv if lv.get(k) != rv[k] and (k.startswith("app/") or k.startswith("deploy/") or k == "identity_tool_allowlist.txt"))
    cmds += ["mkdir -p $S/gw && cp -r /opt/opal-gateway/app $S/gw/app && cp -r /opt/opal-gateway/deploy $S/gw/deploy && cp /opt/opal-gateway/identity_tool_allowlist.txt /opt/opal-gateway/requirements.txt $S/gw/ && find $S/gw -name __pycache__ -prune -exec rm -rf {} + ; true"]
    for n, rel in enumerate(files):
        pb = base64.b64encode(zlib.compress(open(os.path.join(stage, rel), "rb").read(), 9)).decode("ascii")
        cmds += ["printf '%%s' '%s' >> $S/rel%d.b64" % (pb[i:i + 3000], n) for i in range(0, len(pb), 3000)]
        cmds += ["base64 -d $S/rel%d.b64 | /opt/opal-gateway/.venv/bin/python -c 'import sys,zlib;sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' > $S/gw/%s; echo STAGE_RC=$?; md5sum $S/gw/%s" % (n, rel, rel)]
    STAGE = "OG_RL6_STAGE=$S/gw OG_GA1_STAGE=$S/gw OG_GW_DIR=$S/gw "
    print("STAGED_FILES", files)
env = "PYTHONDONTWRITEBYTECODE=1 %sTMPDIR=$S OG_RL6_SCRATCH=$S OG_GA1_SCRATCH=$S OG_RL6_MODE=%s OG_GA1_MODE=%s " % (STAGE, mode, mode)
if kind == "real":
    env += "GA1_TID='%s' GA1_OID='%s' GA1_SERVED_RELEASE='%s' RL15G_MODE='%s' RL15G_FACTS='%s' " % (
        secrets[0], secrets[1], release, mode, os.environ.get("RL15G_FACTS", "{}"))
if kind == "route":
    bef = os.environ.get("R28_BEFORE_ROUTE")      # (A3) json of the neighbour pages' BEFORE values (status, bytes, 16-hex digest); no secret
    if bef:
        json.loads(bef)
    run = "cd %s && env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S R28_SCRATCH=$S %s%stimeout 600 /opt/opal-gateway/.venv/bin/python $S/run.py %s 2>&1 | tail -60; echo RUN_RC=${PIPESTATUS[0]}" % (
        "$S/gw" if stage else "/opt/opal-gateway", "OG_GW_DIR=$S/gw " if stage else "", ("R28_BEFORE_ROUTE='%s' " % bef) if bef else "", mode)
else:
    run = "cd /opt/opal-gateway && " + env + "timeout 1500 /opt/opal-gateway/.venv/bin/python $S/run.py 2>&1 | tail -60; echo RUN_RC=${PIPESTATUS[0]}"
cmds += ["base64 -d $S/p.b64 > $S/run.py", run,
         "rm -rf $S",
         "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)",
         "echo HOST_TMP_og_r29g_LEFTOVER=$(ls -d /tmp/og_r29g* 2>/dev/null | wc -l)"]
pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r29g_params_%d.json" % os.getpid())
with open(pf, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"commands": cmds, "executionTimeout": ["1800"]}))
r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-15 grant host run " + kind + " " + mode,
         "--timeout-seconds", "1800", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
os.remove(pf)
if r.returncode != 0:
    print("SEND FAIL", r.stderr.strip()[:300])
    sys.exit(2)
cid = r.stdout.strip()
st = ""
for _ in range(400):
    time.sleep(5)
    st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
err = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardErrorContent", "--output", "text"]).stdout


def red(t):
    for i, s in enumerate(secrets):
        t = t.replace(s, "<tid>" if i == 0 else "<oid>")
    # (row Z-W28-S17) the host body prints the Schwab "master" account id; it never reaches a saved output
    return re.sub(r'"master": "[0-9]+"', '"master": "<master>"', t.replace("\r", ""))


text = "ssm %s status=%s\n%s" % (cid, st, red(out))
if err.strip() and err.strip() != "None":
    text += "STDERR_TAIL: " + red(err)[-1500:] + "\n"
print(text)
with open(outfile, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
if jdir and kind == "real" and mode == "after" and st == "Success" and "RUN_RC=0" in out:
    for tag, fn in (("RL15G_BODY ", "RL15_GRANTS.json"),):
        m = re.search(r"^" + re.escape(tag) + r"(\{.*\})$", out.replace("\r", ""), re.M)
        assert m, tag
        dg = re.search(r"^RL15G_DIGEST ([0-9a-f]{64})$", out.replace("\r", ""), re.M)
        assert dg and hashlib.sha256(json.dumps(json.loads(m.group(1)), sort_keys=True).encode("utf-8")).hexdigest() == dg.group(1), "digest mismatch"
        with open(os.path.join(jdir, fn), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"body": json.loads(m.group(1)), "instance_id": INST, "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
        print("wrote", os.path.join(jdir, fn))
ok = st == "Success" and "SCRATCH_REMOVED=yes" in out and "RUN_RC=0" in out
sys.exit(0 if ok else 1)
