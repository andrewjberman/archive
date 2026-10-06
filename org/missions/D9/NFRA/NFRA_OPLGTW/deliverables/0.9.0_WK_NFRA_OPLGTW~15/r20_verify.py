"""OG-rl-8 PHASE B verify (form step 6; steps 11-12), WRITTEN at Phase A, never run against a deploy by the Phase A worker.
Release r20 = live cf4b036e62 + 5 gateway files (3 ship: app/server.py, app/audit.py, app/integrations/schwab/engine.py; tests/test_login_admit_r24.py and tests/test_schwab_rss_poll.py are source-only).

usage:  python r20_verify.py before <state.json>
        python r20_verify.py after  <state.json> --served-release <full deployed sha> [--out RL8_LOGIN.json] [--admit-set r20_admit_set.json]

`before` saves the host's reads (MainPID, tool list, .env key NAMES and per-key value sha256 -- a digest only, never a value) and runs the BEFORE /login arms on the installed LIVE code.
`after` exits 0 only if all hold:
  1. host /health 200, service active (MainPID changes: the service restarts);
  2. shipped md5 = release bytes (r20_release_md5.txt: 96 files, 3 differ from live: server.py, audit.py, engine.py);
  3. tool list unchanged (name-for-name);
  4. .env key NAMES unchanged (the template equals live: 51 before, 51 after, 0 added, 0 removed) and EVERY value's sha256 unchanged;
  5. /login on the INSTALLED code, separate process (env -i, no .env, no store, scratch audit sink): non-restricted ADMITTED, Analyst service identity ADMITTED, restricted REFUSED 403,
     server-held ADMITTED, planted/no identity 401, the fail-closed tier arm, exactly ONE gw_login record per /login request, no address/token/state in any record (10 arms);
  6. engine RSS-poll sanity on the installed code (3 arms);
  7. host scratch removed.
RL8_LOGIN.json is written ONLY when every check passes (rl8.AC1.sh anchors served_release to the manifest's deployed_commit); a failing run writes RL8_LOGIN.failed.json.
The floor (rl4.AC1.sh with RL4_ENV_KEYS_BASELINE=r17/ENV_KEYS_R17B.txt, ht.AC2.sh with HT_ENV_KEYS_COUNT=51) is run by r20_verify.sh. Never printed: any .env value, bearer or identity.
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r20_verify_params_%d.json" % os.getpid())
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
    md5 = open(os.path.join(HERE, "r20_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    st, out = ssm_run(["echo %s | base64 -d > /tmp/og_r20_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_r20_verify.py",
                       "rm -f /tmp/og_r20_verify.py"], "OG-rl-8 verify host read")
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    return json.loads(line[0][len("HOSTJSON "):])


def host_arms(prog, outname, modes):
    """Runs a host program (installed code, venv, separate process) through r20_ssm_prog.py; returns (rc, stdout)."""
    outf = os.path.join(tempfile.mkdtemp(prefix="og_r20_arms_"), outname)
    r = subprocess.run([sys.executable, os.path.join(HERE, "r20_ssm_prog.py"), os.path.join(HERE, prog), outf] + modes, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def parse_json_lines(txt, tag):
    return [json.loads(x[len(tag):]) for x in txt.split("\n") if x.startswith(tag)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    ap.add_argument("--served-release")
    ap.add_argument("--out", default=os.path.join(HERE, "RL8_LOGIN.json"))
    ap.add_argument("--admit-set", default=os.path.join(HERE, "r20_admit_set.json"))
    a = ap.parse_args()
    R = host_read()
    if a.mode == "before":
        rc2, o2 = host_arms("r20_login_arms_host.py.txt", "login_before.out", ["before"])
        R["before_login_ok"] = rc2 == 0 and "LOGIN_ARMS before: 8 of 8" in o2
        R["before_login"] = parse_json_lines(o2, "LOGIN_JSON ")
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: MainPID %s, env value sha256 saved %d (hash only), env key names %d, tools %d, /health %s; /login before arm %s (live admits any verified identity, writes no gw_login record: %s)" % (
            R["mainpid"], len(R["env_hashes"]), len(R["env_keys"]), len(R["tools"] or []), R["health"], "PASS" if R["before_login_ok"] else "FAIL",
            [(d["nonrestricted"], d["restricted"], d["audit_records"]) for d in R["before_login"]]))
        return 0 if R["before_login_ok"] else 1
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
    rc2, o2 = host_arms("r20_login_arms_host.py.txt", "login_after.out", ["after"])
    sys.stdout.write("\n".join(x for x in o2.split("\n") if x.startswith(("PASS", "FAIL", "LOGIN_ARMS")))[-2600:] + "\n")
    chk("/login on the INSTALLED code (10 arms): admit/refuse per the tier rule, ONE gw_login record per request", rc2 == 0 and "LOGIN_ARMS after: 10 of 10" in o2 and "SCRATCH_REMOVED=yes" in o2, "ssm rc %s" % rc2)
    rc3, o3 = host_arms("r20_engine_host.py.txt", "engine_after.out", ["release"])
    sys.stdout.write("\n".join(x for x in o3.split("\n") if x.startswith(("PASS", "FAIL", "ENGINE_ARMS")))[-900:] + "\n")
    chk("engine RSS-poll sanity on the installed code (3 arms)", rc3 == 0 and "ENGINE_ARMS release: 3 of 3" in o3, "ssm rc %s" % rc3)
    chk("host scratch removed", "SCRATCH_REMOVED=yes" in o2 and "HOST_TMP_og_r20_LEFTOVER=0" in o2 and "SCRATCH_REMOVED=yes" in o3 and "HOST_TMP_og_r20_LEFTOVER=0" in o3, "SCRATCH_REMOVED=yes and 0 leftovers on both runs")
    lj = [d for d in parse_json_lines(o2, "LOGIN_JSON ") if d.get("expect") == "after"]
    ad = json.load(open(a.admit_set, encoding="utf-8"))
    doc = {"served_release": a.served_release,
           "files_shipped": ["app/server.py", "app/audit.py", "app/integrations/schwab/engine.py"],
           "admit_before": sorted(set(ad["admit_before"])), "admit_after": sorted(set(ad["admit_after"])),
           "lost_nonrestricted": ad["lost_nonrestricted"], "admit_set_note": "computed at Phase A (r20_admit_set.json) over the principal population read then; digests = audit.email_digest",
           "after": {"nonrestricted": lj[0]["nonrestricted"] if lj else "UNREAD", "analyst_service_identity": lj[0]["analyst"] if lj else "UNREAD",
                     "restricted": lj[0]["restricted"] if lj else "UNREAD", "server_held": lj[0]["server_held"] if lj else "UNREAD",
                     "requests": lj[0]["requests"] if lj else -1, "audit_records": lj[0]["audit_records"] if lj else -2},
           "exercise": "synthetic, host-local: /login through GuardMiddleware on the INSTALLED code in a separate process (env -i, no .env, no store, no lake); email-deny read stubbed; consent stubbed; scratch audit sink",
           "grants_written": 0}
    ok = all(res)
    out = a.out if ok else os.path.join(os.path.dirname(os.path.abspath(a.out)), "RL8_LOGIN.failed.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s" % out)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb16 (ANNOUNCE_OG-rl-8.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
