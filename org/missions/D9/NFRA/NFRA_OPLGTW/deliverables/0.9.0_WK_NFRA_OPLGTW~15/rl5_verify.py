"""OG-rl-5 PHASE B verify (step 5), WRITTEN at Phase A and NEVER RUN against a deploy by the Phase A worker.

usage:  python rl5_verify.py before <state.json>
        python rl5_verify.py after  <state.json> --served-release <full deployed sha> [--out RL5_PAGING.json]

`before` (run immediately before the act) saves the host's BEFORE reads: service MainPID, the tool list, the .env key NAMES (never a value).
`after` (run IMMEDIATELY after safe-ec2-deploy.sh returns) runs every check below and exits 0 only if all PASS; any FAIL: roll back
(ANNOUNCE_OG-rl-5.md), re-verify, close ROLLED BACK. Never printed: any .env value, any bearer, any account id or CUSIP.

after-mode checks (host reads by SSM AWS-RunShellScript):
  1. host /health 200 and the service active;
  2. shipped md5 = release bytes (rl5_release_md5.txt, 94 files, including deploy/NFRA_OPLGTW_CONTRACT.json);
  3. tool list unchanged;
  4. .env key NAMES unchanged (50, equal to the BEFORE state);
  then the AFTER run on the host, through the DEPLOYED code (rl5_after_host.py.txt, composed with the census and paging programs):
  5. the paging pages of step 4: dim_position rows page OK, dim_asset rows page OK (before: REFUSED INCOMPLETE_SNAPSHOT snapshot_incomplete and
     REFUSED UNAVAILABLE asset_policy_selection_unavailable);
  6. the served census (census_after {servable_by_master, lacking_or_blank}): servable at BOTH masters, 0 lacking or blank an R9 column;
  7. the asset held-check (dim_asset_held_check {returned, unheld_returned}): returned > 0 and unheld_returned == 0;
  8. the download control (after_dim_asset_download): REFUSED UNAVAILABLE asset_policy_selection_unavailable;
  9. synthetic principal, grants_written 0, state_store_written False.
RL5_PAGING.json is written to --out (default: beside this file). The floor (rl4.AC1.sh, ht.AC2.sh) is run by rl5_verify.sh.
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
BEFORE_RESULT = {"dim_position": "REFUSED INCOMPLETE_SNAPSHOT snapshot_incomplete",
                 "dim_asset": "REFUSED UNAVAILABLE asset_policy_selection_unavailable"}
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
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=", line)
    if m:
        keys.append(m.group(1))
R["env_keys"] = sorted(keys)
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl5_verify_params.json")
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
    md5 = open(os.path.join(HERE, "rl5_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    st, out = ssm_run(["echo %s | base64 -d > /tmp/og_rl5_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_rl5_verify.py",
                       "rm -f /tmp/og_rl5_verify.py"], "OG-rl-5 verify host read")
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    return json.loads(line[0][len("HOSTJSON "):])


def cut_main(text):
    return text[:text.index("def main():")]


def compose_after_program(path):
    """The census and paging programs' definitions (everything before their main()) + the AFTER run; the prelude is added by rl5_ssm.py."""
    parts = []
    for name in ("rl5_census_host.py.txt", "rl5_paging_host.py.txt"):
        parts.append(cut_main(open(os.path.join(HERE, name), encoding="utf-8").read()))
    parts.append(open(os.path.join(HERE, "rl5_after_host.py.txt"), encoding="utf-8").read())
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n\n".join(parts))


def after_run():
    scratch = tempfile.mkdtemp(prefix="og_rl5_after_")   # local only; holds the composed program and its output (counts, codes, booleans)
    prog = os.path.join(scratch, "rl5_after_prog.py")
    compose_after_program(prog)
    outf = os.path.join(scratch, "rl5_after.out")
    r = subprocess.run([sys.executable, os.path.join(HERE, "rl5_ssm.py"), prog, outf], capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stdout.write(r.stdout[-3000:])
    line = [x for x in r.stdout.split("\n") if x.startswith("AFTER_RESULT ")]
    if not line:
        print("AFTER RUN FAILED (no AFTER_RESULT line)")
        sys.exit(2)
    scratch_removed = "SCRATCH_REMOVED=yes" in r.stdout and "HOST_TMP_og_rl5_LEFTOVER=0" in r.stdout
    return json.loads(line[0][len("AFTER_RESULT "):]), scratch_removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    ap.add_argument("--served-release")
    ap.add_argument("--out", default=os.path.join(HERE, "RL5_PAGING.json"))
    a = ap.parse_args()
    R = host_read()
    if a.mode == "before":
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: MainPID %s, env key names %d, tools %d, /health %s" % (R["mainpid"], len(R["env_keys"]), len(R["tools"] or []), R["health"]))
        return 0
    if not a.served_release or len(a.served_release) != 40:
        print("after needs --served-release <the 40-hex deployed sha>")
        return 2
    B = json.load(open(a.state, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(bool(ok))
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200", R["health"] == 200 and R["active"] == "active", "health %s, service %s, MainPID %s (before %s)" % (R["health"], R["active"], R["mainpid"], B["mainpid"]))
    chk("shipped md5 = release bytes (incl. deploy/NFRA_OPLGTW_CONTRACT.json)", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] > 0,
        "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    chk("tool list unchanged", R["tools"] is not None and R["tools"] == B["tools"], "before %d after %d tools" % (len(B["tools"] or []), len(R["tools"] or [])))
    chk(".env key names unchanged (50)", R["env_keys"] == B["env_keys"] and len(R["env_keys"]) == 50,
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), sorted(set(R["env_keys"]) - set(B["env_keys"])), sorted(set(B["env_keys"]) - set(R["env_keys"]))))
    A, scratch_removed = after_run()
    chk("host scratch removed", scratch_removed, "SCRATCH_REMOVED=yes and 0 leftovers" if scratch_removed else "see the SSM output above")
    chk("dim_position rows page OK (before REFUSED)", A["after"]["dim_position"] == "OK", "after %s" % A["after"]["dim_position"])
    chk("dim_asset rows page OK (before REFUSED)", A["after"]["dim_asset"] == "OK", "after %s" % A["after"]["dim_asset"])
    ca = A["census_after"]
    chk("served census: servable at both masters, 0 lacking or blank", all((ca["servable_by_master"].get(m) or 0) > 0 for m in ("08242234", "08335338")) and ca["lacking_or_blank"] == 0,
        "servable_by_master %s lacking_or_blank %s (snapshots %s)" % (ca["servable_by_master"], ca["lacking_or_blank"], ca["snapshots_censused"]))
    hc = A["dim_asset_held_check"]
    chk("dim_asset held-only: returned > 0, unheld_returned 0", hc["returned"] > 0 and hc["unheld_returned"] == 0 and not hc["error"],
        "returned %s unheld_returned %s over %s page(s); error %s" % (hc["returned"], hc["unheld_returned"], hc["pages"], hc["error"]))
    chk("dim_asset prepare_download still REFUSED asset_policy_selection_unavailable", A["after_dim_asset_download"] == "REFUSED UNAVAILABLE asset_policy_selection_unavailable",
        A["after_dim_asset_download"])
    chk("synthetic principal, grants_written 0, state_store_written False", A["synthetic_principal"] is True and A["grants_written"] == 0 and A["state_store_written"] is False,
        "synthetic %s grants_written %s state_store_written %s" % (A["synthetic_principal"], A["grants_written"], A["state_store_written"]))
    doc = {"served_release": a.served_release, "before": BEFORE_RESULT, "after": A["after"], "census_after": ca, "dim_asset_held_check": hc,
           "after_dim_asset_download": A["after_dim_asset_download"], "synthetic_principal": A["synthetic_principal"],
           "grants_written": A["grants_written"], "state_store_written": A["state_store_written"],
           "master": A["master"], "date": A["date"], "page_size": A["page_size"], "after_detail": A["after_detail"]}
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s" % a.out)
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb10 (ANNOUNCE_OG-rl-5.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
