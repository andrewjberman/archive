"""OG-rl-14 PHASE B verify (form step 6; steps 11-12), WRITTEN at Phase A, never run against a deploy by the Phase A worker.
Release r28 = live 510c8cfed2 (r27) + SEVEN gateway files, ONE of them on the host: app/audit.py (the lake key builder, OG-lk-1). Deploy tool and source-only files
(deploy-to-ec2.sh, ops/bun_cache_precheck.py, 4 tests) do not reach the host. The host md5 list differs from live in exactly that one line (`r28_release_md5.txt` vs `r28_live_md5.txt`).
No tool and no route is added or removed: the tool list stays 66 and the route table is the live one (7a does not apply). The AFTER arms re-run the four r26 ROUTE arms in-process on the host
(r28_route_host.py.txt through r28_ssm.py route): chart_404, chart_400, day_page_unchanged, audit_page_unchanged. The new behaviour is read by r28_postdeploy.sh (RL14_READ.json).

usage:  python r28_verify.py before <state.json>
        python r28_verify.py after  <state.json> --served-release <full deployed sha>

`before` saves the host's reads (MainPID, tool list, .env key NAMES and per-key value sha256 -- a digest only, never a value) on the installed LIVE code, then runs the ROUTE `before` arm
(installed code, in-process, synthetic viewer, real S3 read) and saves the two neighbour pages' status, byte count and 16-hex body digest as state["route_before"]. Keep the state file OUT of the
repository (e.g. <worktree>/.scratch/r28_before.json).
`after` exits 0 only if all hold:
  1. host /health 200, service active (MainPID changes: the service restarts);
  2. shipped md5 = release bytes (r28_release_md5.txt: 97 files, 1 differs from live);
  3. tool list UNCHANGED, name for name (66 -> 66);
  4. .env key NAMES unchanged (the template equals live: 51) and EVERY value's sha256 unchanged;
  5. the four ROUTE arms on the INSTALLED release code (a rollback trigger each): chart_404 (/rivalfunds/2000-01-01/chart/ABC -> 404 'no chart for this fund and day'), chart_400
     (/rivalfunds/2026-10-06/chart/abc -> 400), day_page_unchanged and audit_page_unchanged (status, bytes and digest equal to the BEFORE values in the state file).
     The four values are written to r28_phaseB_route.json for r28_postdeploy.sh to fold into RL14_FLOOR.json.
The post-deploy READS (RL14_READ.json, RL14_FLOOR.json) are `r28_postdeploy.sh`; the floor (rl4.AC1.sh, ht.AC2.sh) is run by r28_verify.sh.
Never printed: any .env value, bearer, token or identity."""
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_r28_verify_params_%d.json" % os.getpid())
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


def route_run(mode, served, before_route=None):
    """Runs the route program on the host through r28_ssm.py (its own scratch, one host run at a time); returns (rc, stdout, R28_ROUTE dict, ssm command id)."""
    outf = os.path.join(tempfile.mkdtemp(prefix="og_r28_route_"), "route_%s.out" % mode)
    env = dict(os.environ)
    if before_route:
        env["R28_BEFORE_ROUTE"] = json.dumps(before_route)
    else:
        env.pop("R28_BEFORE_ROUTE", None)
    rr = subprocess.run([sys.executable, os.path.join(HERE, "r28_ssm.py"), "route", mode, outf, served], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    o = rr.stdout
    sys.stdout.write("\n".join(x for x in o.split("\n") if x.startswith(("PASS", "FAIL", "R28_ROUTE", "ROUTE_ARMS", "INSTALLED_FILES", "ssm ", "SCRATCH_REMOVED", "HOST_TMP_og_r28")))[-2400:] + "\n")
    rl = [x for x in o.split("\n") if x.startswith("R28_ROUTE ")]
    cid = [x.split()[1] for x in o.split("\n") if x.startswith("ssm ")]
    return rr.returncode, o, (json.loads(rl[0][len("R28_ROUTE "):]) if rl else {}), (cid[0] if cid else None)


def host_read():
    md5 = open(os.path.join(HERE, "r28_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_r28_verify_%d.py" % os.getpid()      # its own name per run (row Z-W28-S9)
    st, out = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp), "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp], "OG-rl-14 verify host read")
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
        rrc, ro, RT0, _cid = route_run("before", a.served_release or "before")
        R["route_before"] = dict((k, RT0.get(k)) for k in ("day_status", "day_bytes", "day_sha16", "audit_status", "audit_bytes", "audit_sha16"))
        route_ok = rrc == 0 and RT0.get("chart_route_registered") is True and RT0.get("chart_404") is True and RT0.get("chart_400") is True and RT0.get("day_status") == 200 and RT0.get("audit_status") == 200 and "SCRATCH_REMOVED=yes" in ro
        print("BEFORE route arm on the installed code: chart route registered %s, day page %s %s bytes, audit page %s %s bytes => %s" % (
            RT0.get("chart_route_registered"), RT0.get("day_status"), RT0.get("day_bytes"), RT0.get("audit_status"), RT0.get("audit_bytes"), "PASS" if route_ok else "FAIL"))
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        ok = route_ok and R["health"] == 200 and R["active"] == "active" and len(R["tools"] or []) == 66 and STATUS_TOOL in (R["tools"] or [])
        print("BEFORE saved: MainPID %s, env value sha256 saved %d (hash only), env key names %d, tools %d (status tool registered: %s), /health %s, shipped md5 %d of %d vs the release list (the 1 differing file: %s) => %s" % (
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
    BR = B.get("route_before")
    chk("route arms: the BEFORE neighbour values are in the state file", bool(BR) and all(k in BR for k in ("day_status", "day_bytes", "day_sha16", "audit_status", "audit_bytes", "audit_sha16")), "route_before %s" % ("present" if BR else "ABSENT"))
    rrc, ro, RT, rcid = route_run("after", a.served_release, BR)
    chk("ROUTE ARM chart_404: /rivalfunds/2000-01-01/chart/ABC -> 404 with 'no chart for this fund and day'", bool(RT) and RT.get("chart_404") is True and RT.get("chart_route_registered") is True,
        "status %s, named body %s" % (RT.get("chart_404_status"), RT.get("chart_404_body_named")))
    chk("ROUTE ARM chart_400: /rivalfunds/2026-10-06/chart/abc -> 400", bool(RT) and RT.get("chart_400") is True, "status %s" % RT.get("chart_400_status"))
    chk("ROUTE ARM day_page_unchanged: /rivalfunds/2026-10-06 answers as before (status, bytes, digest)", bool(RT) and RT.get("day_page_unchanged") is True,
        "%s %s bytes sha16 %s" % (RT.get("day_status"), RT.get("day_bytes"), RT.get("day_sha16")))
    chk("ROUTE ARM audit_page_unchanged: /rivalfunds/2026-10-06/audit answers as before (status, bytes, digest)", bool(RT) and RT.get("audit_page_unchanged") is True,
        "%s %s bytes sha16 %s" % (RT.get("audit_status"), RT.get("audit_bytes"), RT.get("audit_sha16")))
    chk("route host scratch removed", "SCRATCH_REMOVED=yes" in ro and "HOST_TMP_og_r28_LEFTOVER=0" in ro, "SCRATCH_REMOVED=yes and 0 leftovers")
    if RT and all(RT.get(k) is True for k in ("chart_404", "chart_400", "day_page_unchanged", "audit_page_unchanged")):   # written only when all four arms hold (a failed run leaves no record for postdeploy)
        doc = {"body": dict((k, RT.get(k)) for k in ("chart_404", "chart_404_status", "chart_404_body_named", "chart_400", "chart_400_status", "day_page_unchanged", "day_status", "day_bytes", "day_sha16",
                                                   "audit_page_unchanged", "audit_status", "audit_bytes", "audit_sha16", "chart_no_identity_status")), "ssm_command_id": rcid, "instance_id": INST}
        with open(os.path.join(HERE, "r28_phaseB_route.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
            fh.write("\n")
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb22 (ANNOUNCE_OG-rl-14.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
