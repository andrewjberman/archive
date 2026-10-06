"""OG-rl-10 PHASE B verify (form step 6; steps 11-12), WRITTEN at Phase A, never run against a deploy by the Phase A worker.
Release r24 = live 2c27f3a795 + ONE gateway file on the host: app/integrations/opal_portal/integration.py (md5 cc08e21e; live f8d19990).

usage:  python r24_verify.py before <state.json>
        python r24_verify.py after  <state.json> --served-release <full deployed sha>

`before` saves the host's reads (MainPID, tool list, .env key NAMES and per-key value sha256 -- a digest only, never a value).
`after` exits 0 only if all hold:
  1. host /health 200, service active (MainPID changes: the service restarts);
  2. shipped md5 = release bytes (r24_release_md5.txt: 96 files, 1 differs from live);
  3. tool list unchanged (name-for-name);
  4. .env key NAMES unchanged (the template equals live) and EVERY value's sha256 unchanged;
  5. the INSTALLED integration is the release file and its login rides the front door: r24_login_host.py.txt in `check` mode through r24_ssm_prog.py (separate process,
     env -i, the real service secret read as the service reads it; the outcome only -- never a token, email or password): login OK, auth host www.opalinvest.dev, module md5 cc08e21e, not staged;
  6. host scratch removed.
The floor (rl4.AC1.sh with RL4_ENV_KEYS_BASELINE=r17/ENV_KEYS_R17B.txt, ht.AC2.sh with HT_ENV_KEYS_COUNT=51) is run by r24_verify.sh. Never printed: any .env value, bearer or identity.
The recorded post-deploy login (RL10_LOGIN.json) is a SEPARATE run right after this script: R24_JSON_DIR=<W> python r24_ssm_prog.py r24_login_host.py.txt <out> "after <sha>".
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
REL_INTEG_MD5 = "cc08e21e"
HOST_PROG = r'''
import hashlib, json, os, re, subprocess, urllib.request, urllib.error
R = {}
os.chdir("/opt/opal-gateway")
R["mainpid"] = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
R["active"] = subprocess.check_output(["systemctl", "is-active", "opal-gateway"]).decode().strip()
MD5 = """@@MD5@@"""
want = [l.split("  ", 1) for l in MD5.strip().split("\n") if l.strip()]
bad = []
for h, f in want:
    try:
        got = hashlib.md5(open(f, "rb").read()).hexdigest()
    except OSError:
        got = "ABSENT"
    if got != h:
        bad.append(f)
R["md5_listed"] = len(want); R["md5_ok"] = len(want) - len(bad); R["md5_bad"] = bad
keys = []
hashes = {}
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.rstrip(chr(10)).rstrip(chr(13)))
    if m:
        keys.append(m.group(1))
        hashes[m.group(1)] = hashlib.sha256(m.group(2).encode("utf-8")).hexdigest()   # only the digest leaves the host; no value is printed or stored
R["env_keys"] = sorted(keys)
R["env_hashes"] = hashes
tool_src = """
import asyncio, os, sys
sys.path.insert(0, "/opt/opal-gateway")
from app import tools, integrations
ids = os.environ["ENABLED_INTEGRATIONS"].split()
rep = integrations.register_enabled(tools.mcp, ids)
from mcp.server.fastmcp import FastMCP
names = sorted(t.name for t in asyncio.run(FastMCP.list_tools(tools.mcp)))
print("TOOLNAMES", ",".join(names))
"""
pid = R["mainpid"]
penv = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if kv.startswith(b"ENABLED_INTEGRATIONS="):
        penv["ENABLED_INTEGRATIONS"] = kv.split(b"=", 1)[1].decode("utf-8", "replace")
out = subprocess.run(["env", "-i", "HOME=/tmp", "PATH=" + os.environ.get("PATH", ""), "MOCK_GRAPH=1",
                      "ENABLED_INTEGRATIONS=" + penv.get("ENABLED_INTEGRATIONS", ""), "/opt/opal-gateway/.venv/bin/python", "-c", tool_src],
                     capture_output=True, text=True).stdout
tn = [l for l in out.split("\n") if l.startswith("TOOLNAMES ")]
R["tools"] = tn[0].split(" ", 1)[1].split(",") if tn else None
try:
    R["health"] = urllib.request.urlopen("http://localhost:8080/health", timeout=15).status
except urllib.error.HTTPError as e:
    R["health"] = e.code
except Exception as e:
    R["health"] = "ERR:" + type(e).__name__
print("HOSTJSON " + json.dumps(R))
'''


def aws(args):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def ssm_run(commands, comment, polls=60, wait=3):
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r24_verify_params_%d.json" % os.getpid())
    with open(pf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"commands": commands, "executionTimeout": ["1800"]}))
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", comment,
             "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:300])
        sys.exit(2)
    cid = r.stdout.strip()
    st = ""
    for _ in range(polls):
        time.sleep(wait)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status",
                  "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query",
               "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    return st, out.replace("\r", "")


def host_read():
    md5 = open(os.path.join(HERE, "r24_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    st, out = ssm_run(["echo %s | base64 -d > /tmp/og_r24_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_r24_verify.py",
                       "rm -f /tmp/og_r24_verify.py"], "OG-rl-10 verify host read")
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    return json.loads(line[0][len("HOSTJSON "):])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    ap.add_argument("--served-release")
    a = ap.parse_args()
    R = host_read()
    if a.mode == "before":
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: MainPID %s, env value sha256 saved %d (hash only), env key names %d, tools %d, /health %s" % (
            R["mainpid"], len(R["env_hashes"]), len(R["env_keys"]), len(R["tools"] or []), R["health"]))
        return 0 if R["health"] == 200 else 1
    if not a.served_release or len(a.served_release) != 40:
        print("after needs --served-release <the 40-hex deployed sha>")
        return 2
    B = json.load(open(a.state, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(bool(ok))
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200", R["health"] == 200 and R["active"] == "active", "health %s, service %s, MainPID %s (before %s)" % (R["health"], R["active"], R["mainpid"], B["mainpid"]))
    chk("shipped md5 = release bytes", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] > 0, "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    chk("tool list unchanged", R["tools"] is not None and R["tools"] == B["tools"], "before %d after %d tools" % (len(B["tools"] or []), len(R["tools"] or [])))
    added = sorted(set(R["env_keys"]) - set(B["env_keys"]))
    removed = sorted(set(B["env_keys"]) - set(R["env_keys"]))
    chk(".env key names unchanged (the template equals live)", not added and not removed and len(R["env_keys"]) == len(B["env_keys"]) == len(set(R["env_keys"])),
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), added, removed))
    BH, AH = B.get("env_hashes") or {}, R.get("env_hashes") or {}
    changed = sorted(k for k in BH if AH.get(k) != BH[k])
    chk("every .env value has the SAME sha256 before and after (hash only; changed names listed)", len(BH) > 0 and not changed,
        "before hashes %d, after hashes %d, equal %d of %d, changed %s" % (len(BH), len(AH), len(BH) - len(changed), len(BH), changed))
    outf = os.path.join(tempfile.mkdtemp(prefix="og_r24_login_"), "login_check.out")
    rr = subprocess.run([sys.executable, os.path.join(HERE, "r24_ssm_prog.py"), os.path.join(HERE, "r24_login_host.py.txt"), outf, "check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    o2 = rr.stdout
    sys.stdout.write("\n".join(x for x in o2.split("\n") if x.startswith(("RL10_LOGIN", "RL10_MODULE", "RL10_AUTH_HOST", "ssm ")))[-1200:] + "\n")
    chk("INSTALLED integration is the release file and its login rides the front door: login OK, auth host www.opalinvest.dev",
        rr.returncode == 0 and "RL10_LOGIN mode=check login=OK" in o2 and "RL10_AUTH_HOST www.opalinvest.dev" in o2
        and "RL10_MODULE integration.py md5 %s staged=False" % REL_INTEG_MD5 in o2, "expected module md5 prefix %s" % REL_INTEG_MD5)
    chk("host scratch removed", "SCRATCH_REMOVED=yes" in o2 and "HOST_TMP_og_r24_LEFTOVER=0" in o2, "SCRATCH_REMOVED=yes and 0 leftovers")
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb17 (ANNOUNCE_OG-rl-10.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
