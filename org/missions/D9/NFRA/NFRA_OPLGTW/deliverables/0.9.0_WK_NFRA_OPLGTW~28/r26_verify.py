"""OG-rl-12 PHASE B verify (form step 6; steps 11-12), WRITTEN at Phase A, never run against a deploy by the Phase A worker.
Release r26 = live 240ac2fe5a + 6 gateway files, TWO on the host: app/integrations/opal_portal/integration.py and identity_tool_allowlist.txt (the gateway root; the deploy
tarball carries it to /opt/opal-gateway/identity_tool_allowlist.txt) = the two lines of `r26_release_md5.txt` that differ from `r26_live_md5.txt`; source-only: tests/test_identity_scope_status_row.py,
tests/test_opal_portal_dedupe_content.py, tests/test_opal_portal_send_split.py, tests/test_opal_portal_status_id_shape.py. No tool is added or removed: the tool list stays 66.

usage:  python r26_verify.py before <state.json>
        python r26_verify.py after  <state.json> --served-release <full deployed sha>

`before` saves the host's reads (MainPID, tool list, .env key NAMES and per-key value sha256 -- a digest only, never a value) on the installed LIVE code. Keep the state file OUT of the
repository (e.g. <worktree>/.scratch/r26_before.json).
`after` exits 0 only if all hold:
  1. host /health 200, service active (MainPID changes: the service restarts);
  2. shipped md5 = release bytes (r26_release_md5.txt: 97 files, 2 differ from live);
  3. tool list UNCHANGED, name for name (66 -> 66);
  4. .env key NAMES unchanged (the template equals live: 51) and EVERY value's sha256 unchanged.
The post-deploy READS (RL12_ALLOW.json, RL12_FLOOR.json) are `r26_postdeploy.sh`; the floor (rl4.AC1.sh, ht.AC2.sh) is run by r26_verify.sh.
Never printed: any .env value, bearer, token or identity."""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
STATUS_TOOL = "opal_data_refresh_status"
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r26_verify_params_%d.json" % os.getpid())
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
    md5 = open(os.path.join(HERE, "r26_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_r26_verify_%d.py" % os.getpid()      # its own name per run (row Z-W28-S9)
    st, out = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp), "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp], "OG-rl-12 verify host read")
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
        ok = R["health"] == 200 and R["active"] == "active" and len(R["tools"] or []) == 66 and STATUS_TOOL in (R["tools"] or [])
        print("BEFORE saved: MainPID %s, env value sha256 saved %d (hash only), env key names %d, tools %d (status tool registered: %s), /health %s, shipped md5 %d of %d vs the release list (the 2 differing files: %s) => %s" % (
            R["mainpid"], len(R["env_hashes"]), len(R["env_keys"]), len(R["tools"] or []), STATUS_TOOL in (R["tools"] or []), R["health"], R["md5_ok"], R["md5_listed"], R["md5_bad"],
            "PASS" if ok else "FAIL"))
        return 0 if ok else 1
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
    bt, at = set(B["tools"] or []), set(R["tools"] or [])
    chk("tool list unchanged, name for name (66 -> 66)", bool(bt) and at == bt and len(R["tools"]) == len(B["tools"]) == 66,
        "before %d after %d tools; added %s removed %s" % (len(bt), len(at), sorted(at - bt), sorted(bt - at)))
    added = sorted(set(R["env_keys"]) - set(B["env_keys"]))
    removed = sorted(set(B["env_keys"]) - set(R["env_keys"]))
    chk(".env key names unchanged (the template equals live)", not added and not removed and len(R["env_keys"]) == len(B["env_keys"]) == len(set(R["env_keys"])),
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), added, removed))
    BH, AH = B.get("env_hashes") or {}, R.get("env_hashes") or {}
    changed = sorted(k for k in BH if AH.get(k) != BH[k])
    chk("every .env value has the SAME sha256 before and after (hash only; changed names listed)", len(BH) > 0 and not changed,
        "before hashes %d, after hashes %d, equal %d of %d, changed %s" % (len(BH), len(AH), len(BH) - len(changed), len(BH), changed))
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb20 (ANNOUNCE_OG-rl-12.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
