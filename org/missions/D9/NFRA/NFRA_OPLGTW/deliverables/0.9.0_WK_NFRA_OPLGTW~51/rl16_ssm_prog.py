"""OG-rl-15 runner (from r24_ssm_prog.py): ships a host program (first arg) to the opal-gateway host by SSM and runs it, once per mode, as a SEPARATE process in the
installed venv with `env -i` (never the running service, never sourcing /opt/opal-gateway/.env), from a per-run scratch that is removed in the same command list.
usage: python r29_ssm_prog.py <program .py.txt> <out-file> <args-string> [<args-string> ...]   (each args-string is one run of the program, e.g. 'after')
Each run has its OWN scratch directory name /tmp/og_r29_<tag>_<pid> (row Z-W28-S9: a fixed name collides when two runs overlap).
env R28_STAGE_FROM=<gateway dir>: REHEARSAL -- stage a scratch copy of the installed app/ + deploy/ carrying the RELEASE bytes of every file whose md5 differs between
  r29_live_md5.txt and r29_release_md5.txt (or R28_STAGE_FILES, comma-separated), and run against it (OG_GW_DIR); the installed tree is untouched.
env R28_SECRET_ENV=<json {NAME: value}>: exported into the host command for the run (SSM parameters only; never written to the repo); every value is redacted from the output.
env R28_JSON_DIR=<dir> R28_JSON_SPECS=<json [[BODY_MARKER, DIGEST_MARKER, filename], ...]>: write <dir>/<filename> as {"body","ssm_command_id","instance_id"} from the host's own
  `<BODY_MARKER> {json}` line, only if the host also printed `<DIGEST_MARKER> sha256(json.dumps(body, sort_keys=True))` and it matches.
Prints the SSM id, status and the program output (codes, booleans, md5s; never a value). Writes the same to <out-file>."""
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


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace")


def _md5s(fn):
    return dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(os.path.join(HERE, fn), encoding="utf-8") if ln.strip())


progfile, outfile, modes = sys.argv[1], sys.argv[2], sys.argv[3:]
prog = open(progfile if os.path.exists(progfile) else os.path.join(HERE, progfile), encoding="utf-8").read()
tag = re.sub(r"[^a-z0-9]", "", os.path.basename(progfile).split(".")[0].lower())[:14] or "run"
SCR = "/tmp/og_r29_%s_%d" % (tag, os.getpid())
b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
cmds = ["S=%s; rm -rf $S; mkdir -p $S" % SCR]
cmds += ["printf '%%s' '%s' >> $S/p.b64" % b64[i:i + 3000] for i in range(0, len(b64), 3000)]
cmds += ["base64 -d $S/p.b64 > $S/run.py", "md5sum $S/run.py"]
STAGE_FROM = os.environ.get("R28_STAGE_FROM")
secret_env = json.loads(os.environ.get("R28_SECRET_ENV") or "{}")
RUNDIR, GWENV = "/opt/opal-gateway", ""
if STAGE_FROM:
    if os.environ.get("R28_STAGE_FILES"):
        FILES = os.environ["R28_STAGE_FILES"].split(",")
    else:
        lv, rv = _md5s("r29_live_md5.txt"), _md5s("r29_release_md5.txt")
        FILES = sorted(k for k in rv if lv.get(k) != rv[k] and (k.startswith("app/") or k.startswith("deploy/") or k == "identity_tool_allowlist.txt"))
    print("STAGED_FILES", FILES)
    cmds += ["mkdir -p $S/gw && cp -r /opt/opal-gateway/app $S/gw/app && cp -r /opt/opal-gateway/deploy $S/gw/deploy && cp /opt/opal-gateway/identity_tool_allowlist.txt /opt/opal-gateway/requirements.txt $S/gw/ && find $S/gw -name __pycache__ -prune -exec rm -rf {} + ; true"]
    for i, rel in enumerate(FILES):
        pb = base64.b64encode(zlib.compress(open(os.path.join(STAGE_FROM, rel), "rb").read(), 9)).decode("ascii")
        cmds += ["printf '%%s' '%s' >> $S/f%d.b64" % (pb[j:j + 3000], i) for j in range(0, len(pb), 3000)]
        cmds += ["base64 -d $S/f%d.b64 | /opt/opal-gateway/.venv/bin/python -c 'import sys,zlib;sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' > $S/gw/%s; md5sum $S/gw/%s" % (i, rel, rel)]
    RUNDIR, GWENV = "$S/gw", "OG_GW_DIR=$S/gw "
cmds += ["cd " + RUNDIR]
sec = "".join("%s='%s' " % (k, v.replace("'", "'\\''")) for k, v in secret_env.items())
for m in modes:
    cmds.append("echo MODE=%s; env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S R28_SCRATCH=$S %s%s timeout 600 /opt/opal-gateway/.venv/bin/python $S/run.py %s; echo RUN_RC=$?" % (m.replace(" ", "_"), GWENV, sec, m))
cmds += ["rm -rf $S", "echo SCRATCH_REMOVED=$([ -e $S ] && echo no || echo yes)", "echo HOST_TMP_og_r29_LEFTOVER=$(ls -d /tmp/og_r29* 2>/dev/null | wc -l)"]
LIMIT = 80000   # SSM refuses a document over ~97KB: the command list goes out in batches, each defining $S, the LAST one removing it (r29)


def batches(cs):
    out, cur, size = [], [], 0
    for c in cs:
        if cur and size + len(c) + 6 > LIMIT:
            out.append(cur)
            cur, size = [], 0
        cur.append(c)
        size += len(c) + 6
    out.append(cur)
    return out


def send_batch(bcmds, comment):
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r29_params_%d.json" % os.getpid())
    with open(pf, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps({"commands": bcmds, "executionTimeout": ["1800"]}))
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", comment,
             "--timeout-seconds", "1800", "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
    if r.returncode != 0:
        return None, "SendFail", "", r.stderr.strip()[:300]
    cid = r.stdout.strip()
    st = ""
    for _ in range(400):
        time.sleep(4)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    o = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
    e = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardErrorContent", "--output", "text"]).stdout
    return cid, st, o, e


# the final two lines of cmds are the removal; they ride the last batch. A mid-way failure sends the removal alone.
removal = cmds[-3:]
body_cmds = cmds[:-3]
bs = batches(body_cmds)
cid, st, out, err = None, "", "", ""
ids = []
for n, b in enumerate(bs):
    if n > 0:
        b = ["S=%s" % SCR] + b
    last = n == len(bs) - 1
    if last:
        b = b + ["S=%s" % SCR] + removal if n > 0 else b + removal
    cid, st, o, e = send_batch(b, "OG-rl-15 host run %d/%d" % (n + 1, len(bs)))
    ids.append(cid)
    out += o
    err += e
    if st != "Success" and not last:
        print("BATCH %d FAILED status=%s; sending the removal" % (n + 1, st))
        send_batch(["S=%s" % SCR] + removal, "OG-rl-15 cleanup")
        break
print("SSM batches %d ids %s" % (len(bs), ids))
cid = ids[-1]


def red(t):
    for v in secret_env.values():
        if v:
            t = t.replace(v, "<redacted>")
    return t.replace("\r", "")


text = "ssm %s status=%s\n%s" % (cid, st, red(out))
if err.strip() and err.strip() != "None":
    text += "STDERR_TAIL: " + red(err)[-1500:] + "\n"
print(text)
with open(outfile, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
jdir, specs = os.environ.get("R28_JSON_DIR"), json.loads(os.environ.get("R28_JSON_SPECS") or "[]")
if jdir and st == "Success":
    o = red(out)
    for bm, dm, fn in specs:
        mb = re.search(r"^" + re.escape(bm) + r" (\{.*\})$", o, re.M)
        md = re.search(r"^" + re.escape(dm) + r" ([0-9a-f]{64})$", o, re.M)
        if mb and md and hashlib.sha256(json.dumps(json.loads(mb.group(1)), sort_keys=True).encode("utf-8")).hexdigest() == md.group(1):
            with open(os.path.join(jdir, fn), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps({"body": json.loads(mb.group(1)), "instance_id": INST, "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
            print("wrote", os.path.join(jdir, fn))
        else:
            print("NOT WRITTEN (marker or digest missing/mismatch):", fn)
ok = "SCRATCH_REMOVED=yes" in out and "RESULT: FAIL" not in out and out.count("RUN_RC=0") == len(modes)
sys.exit(0 if ok else 1)
