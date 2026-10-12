"""OG-ap-7 PHASE B2 step 5 verify -- adapted for THIS release's trigger set.

usage:  python ap7_verify.py before <state.json>
        python ap7_verify.py after  <state.json>

WHY THIS IS NOT ap6_verify.py. That verifier asserts the OG-ap-6 trigger set: exactly one tool
added (copy_site_file_to_s3) and exactly one .env key added (ADVI_FEE_STATEMENT_S3_ROOT). THIS
release adds NEITHER. Its triggers, from the ask's section 5 table and the COO half's conditions,
are: shipped md5 equals the RELEASE list; the tool list UNCHANGED; the .env key names UNCHANGED;
every .env value digest unchanged; ROUTES +3, exactly the three named and none removed;
dashboard/ unchanged; /health 200. Running ap6_verify.py here would have failed a correct deploy
on its tool and env assertions.

Every count is RELATIVE to the `before` read taken on the live base AT THE ACT. The only
absolutes are the three route paths the halves name.

ROLLBACK TRIGGERS are the regressions in that table and ONLY those (COO half condition B). A 403
or 409 at the SERVED grade is explicitly NOT a trigger here -- it is a finding, routed as an ARMED
row -- and the served grade is a separate step, not one of these checks.

Never printed: any .env value, bearer, token or identity. Only per-key sha256 digests leave the
host.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
NEW_ROUTES = [
    "/hx/teams/channels/{team_id}/{channel_id}/messages",
    "/hx/teams/teams",
    "/hx/teams/teams/{team_id}/channels",
]

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
dash = {}
for root, ds, fs in os.walk("dashboard"):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.join(root, f).replace(os.sep, "/")
        try:
            dash[p] = hashlib.md5(open(p, "rb").read()).hexdigest()
        except OSError:
            dash[p] = "ABSENT"
R["dash"] = dash
keys = []
hashes = {}
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.rstrip(chr(10)).rstrip(chr(13)))
    if m:
        keys.append(m.group(1))
        hashes[m.group(1)] = hashlib.sha256(m.group(2).encode("utf-8")).hexdigest()
R["env_keys"] = sorted(keys)
R["env_hashes"] = hashes
pid = R["mainpid"]
penv = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if kv.startswith(b"ENABLED_INTEGRATIONS="):
        penv["ENABLED_INTEGRATIONS"] = kv.split(b"=", 1)[1].decode("utf-8", "replace")
EI = penv.get("ENABLED_INTEGRATIONS", "")
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
out = subprocess.run(["env", "-i", "HOME=/tmp", "PATH=" + os.environ.get("PATH", ""), "MOCK_GRAPH=1",
                      "ENABLED_INTEGRATIONS=" + EI, "/opt/opal-gateway/.venv/bin/python", "-c", tool_src],
                     capture_output=True, text=True).stdout
tn = [l for l in out.split("\n") if l.startswith("TOOLNAMES ")]
R["tools"] = tn[0].split(" ", 1)[1].split(",") if tn else None
# ROUTE CENSUS -- this release's trigger is routes +3, so the routes must be enumerated.
route_src = """
import sys
sys.path.insert(0, "/opt/opal-gateway")
from app import server
paths = sorted(getattr(r, "path", "") or "" for r in server.app.routes)
print("ROUTEPATHS " + "\\n".join(p for p in paths if p))
"""
rout = subprocess.run(["env", "-i", "HOME=/tmp", "PATH=" + os.environ.get("PATH", ""), "MOCK_GRAPH=1",
                       "ENABLED_INTEGRATIONS=" + EI, "/opt/opal-gateway/.venv/bin/python", "-c", route_src],
                      capture_output=True, text=True)
if "ROUTEPATHS " in rout.stdout:
    body = rout.stdout.split("ROUTEPATHS ", 1)[1]
    R["routes"] = sorted(x for x in body.split("\n") if x.strip())
else:
    R["routes"] = None
    R["routes_stderr"] = (rout.stderr or "")[-300:]
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_ap7_verify_params_%d.json" % os.getpid())
    with open(pf, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps({"commands": commands, "executionTimeout": ["1800"]}))
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", comment,
             "--parameters", "file://" + pf.replace(chr(92), "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:300])
        sys.exit(2)
    cid = r.stdout.strip()
    st = ""
    for _ in range(polls):
        time.sleep(wait)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1",
                  "--query", "Status", "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1",
               "--query", "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    return st, out.replace(chr(13), ""), cid


def _list(fn):
    p = os.path.join(HERE, fn)
    return dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(p, encoding="utf-8") if ln.strip())


def host_read():
    md5 = open(os.path.join(HERE, "ap7_release_md5.txt"), encoding="utf-8").read().replace(chr(13), "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_ap7_verify_%d.py" % os.getpid()
    st, out, cid = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp),
                            "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp,
                            "echo LEFTOVER=$(ls /tmp/og_ap7_verify_* 2>/dev/null | wc -l)"],
                           "OG-ap-7 verify host read")
    line = [x for x in out.split(chr(10)) if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    print([x for x in out.split(chr(10)) if x.startswith("LEFTOVER=")])
    R = json.loads(line[0][len("HOSTJSON "):])
    R["_ssm_command_id"] = cid
    return R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    a = ap.parse_args()
    R = host_read()

    rel = _list("ap7_release_md5.txt")
    base = _list("ap7_live_md5.txt")
    differ = sorted(k for k in rel if base.get(k) != rel[k])

    if a.mode == "before":
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        md5_is_base = sorted(R["md5_bad"]) == differ
        ok = (R["health"] == 200 and R["active"] == "active" and bool(R["tools"])
              and bool(R["routes"]) and len(R["env_keys"]) > 0 and md5_is_base)
        print("BEFORE saved: MainPID %s, env names %d, env digests %d, tools %d, routes %d, /health %s, "
              "shipped md5 %d of %d vs the RELEASE list; mismatching %d"
              % (R["mainpid"], len(R["env_keys"]), len(R["env_hashes"]), len(R["tools"] or []),
                 len(R["routes"] or []), R["health"], R["md5_ok"], R["md5_listed"], len(R["md5_bad"])))
        print("  host is running the BASE: mismatches equal the base-vs-release differ set (%d): %s"
              % (len(differ), "yes" if md5_is_base else
                 "NO -- symmetric difference %s" % sorted(set(R["md5_bad"]) ^ set(differ))))
        for p in NEW_ROUTES:
            print("  route %-52s present BEFORE: %s" % (p, p in (R["routes"] or [])))
        print("  dashboard files: %d" % len(R.get("dash") or {}))
        print("BEFORE %s" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    B = json.load(open(a.state, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(bool(ok))
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200 and service active",
        R["health"] == 200 and R["active"] == "active",
        "health %s, service %s, MainPID %s (before %s)" % (R["health"], R["active"], R["mainpid"], B["mainpid"]))

    chk("shipped md5 = the RELEASE bytes (every listed file identical)",
        R["md5_ok"] == R["md5_listed"] and R["md5_listed"] == len(rel) and not R["md5_bad"],
        "%d of %d identical against a release list of %d; not-ok %s"
        % (R["md5_ok"], R["md5_listed"], len(rel), R["md5_bad"]))

    bt, at = set(B["tools"] or []), set(R["tools"] or [])
    chk("tool list UNCHANGED name for name (this release adds no tool)",
        bool(bt) and at == bt,
        "before %d after %d; added %s removed %s" % (len(bt), len(at), sorted(at - bt), sorted(bt - at)))

    bk, ak = set(B["env_keys"]), set(R["env_keys"])
    chk(".env key names UNCHANGED (this release adds no env key)",
        bool(bk) and ak == bk,
        "before %d after %d; added %s removed %s" % (len(bk), len(ak), sorted(ak - bk), sorted(bk - ak)))

    BH, AH = B.get("env_hashes") or {}, R.get("env_hashes") or {}
    changed = sorted(k for k in BH if AH.get(k) != BH[k])
    chk("every .env value digest unchanged",
        len(BH) > 0 and not changed,
        "before %d, after %d, equal %d of %d, changed %s" % (len(BH), len(AH), len(BH) - len(changed), len(BH), changed))

    br, ar = set(B["routes"] or []), set(R["routes"] or [])
    added, removed = sorted(ar - br), sorted(br - ar)
    chk("routes +3, exactly the three named, none removed",
        bool(br) and added == sorted(NEW_ROUTES) and not removed,
        "before %d after %d; added %s removed %s" % (len(br), len(ar), added, removed))

    BD, AD = B.get("dash") or {}, R.get("dash") or {}
    d_ch = sorted(k for k in BD if AD.get(k) != BD[k])
    d_go = sorted(k for k in BD if k not in AD)
    d_nw = sorted(k for k in AD if k not in BD)
    chk("dashboard/ unchanged across the deploy",
        len(BD) > 0 and not d_ch and not d_go and not d_nw,
        "before %d after %d; changed %s removed %s added %s" % (len(BD), len(AD), d_ch, d_go, d_nw))

    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK (ask section 5 / COO condition B -- these regressions and ONLY these): redeploy "
              "c3af8687e44a1e641259b37f992033ae02cdce3d with DEPLOY_BASE_REF set to the release sha, then file an "
              "ARMED row naming 2.0.0_SA_COO~O. NOTE a 403/409 at the SERVED grade is NOT one of these and is "
              "explicitly not a rollback trigger.")
    return 0 if ok else 1


sys.exit(main())
