"""OG-rl-6 PHASE C verify (A1 steps 16 and 20), extended from rl6_verify.py. WRITTEN at Phase C-A; the Phase C-A worker runs `before` and a
NEGATIVE CONTROL of `after` against the UNDEPLOYED host, never `after` against a deploy.

usage:  python rl7_verify.py before <state.json>
        python rl7_verify.py after  <state.json> --served-release <full deployed sha> [--out RL6_DOWNLOAD.json]

`before` saves the host's reads (MainPID, tool list, .env key NAMES; never a value) AND runs the on-host program (rl6_host.py.txt, mode after: synthetic
principal, in-memory grant) on the LIVE release e91819e281, so the r17 download behaviour is on record BEFORE the act. `after` exits 0 only if all hold:
  1. host /health 200, service active;  2. shipped md5 = release bytes (rl7_release_md5.txt: 96 files = the 94 live + app/yearinreview_view.py +
     app/static/yearinreview/index.html, app/server.py replaced);  3. tool list unchanged (65);  4. .env key NAMES unchanged (50);
  5. host-local GET http://localhost:8080/yearinreview with NO identity -> 401 (404 before);
  6. public unauthenticated GET https://mcp.opalinvest.dev/yearinreview -> 302 to login.microsoftonline.com (ALB wall; not followed);
  7. the r17 download behaviour RE-READ through the deployed code: download OK, held-only (unheld 0, graded when held < universe), empty-holdings
     REFUSED asset_read_denied_unqualified, query OK with the same held set, and each equal to the pre-act read; synthetic, grants_written 0.
RL6_DOWNLOAD.json is rewritten ONLY when every check passes (so rl6.AC1.sh, anchored to the manifest's deployed_commit, can read served_release = the
new sha): `before` is CARRIED from the r17 file (RL6_DOWNLOAD.r17.json, copied from RL6_DOWNLOAD.json first), because the pre-r17 REFUSED is the only
'before' that exists for that outcome; `after` is the fresh re-read. A failing run writes RL6_DOWNLOAD.r17b_failed.json beside it instead.
The floor (rl6.AC1.sh, rl4.AC1.sh, ht.AC2.sh) is run by rl7_verify.sh. Never printed: any .env value, bearer, account id or CUSIP.
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
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
try:
    urllib.request.build_opener(_NoRedirect).open("http://localhost:8080/yearinreview", timeout=15)
    R["yir_local"] = 200
except urllib.error.HTTPError as e:
    R["yir_local"] = e.code
except Exception as e:
    R["yir_local"] = "ERR:" + type(e).__name__
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl6c_verify_params.json")
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
    md5 = open(os.path.join(HERE, "rl7_release_md5.txt"), encoding="utf-8").read().replace("\r", "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    st, out = ssm_run(["echo %s | base64 -d > /tmp/og_rl6c_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_rl6c_verify.py",
                       "rm -f /tmp/og_rl6c_verify.py"], "OG-rl-6 PhaseC verify host read")
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    return json.loads(line[0][len("HOSTJSON "):])


def public_get():
    import http.client
    c = http.client.HTTPSConnection("mcp.opalinvest.dev", timeout=20)
    c.request("GET", "/yearinreview")
    r = c.getresponse()
    loc = r.getheader("Location") or ""
    c.close()
    return r.status, loc


def after_run():
    scratch = tempfile.mkdtemp(prefix="og_rl6c_after_")   # local only; holds the program output (counts, codes, booleans)
    outf = os.path.join(scratch, "rl6_after.out")
    env = dict(os.environ, OG_RL6_MODE="after")
    r = subprocess.run([sys.executable, os.path.join(HERE, "rl6c_ssm.py"), os.path.join(HERE, "rl6_host.py.txt"), outf], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    sys.stdout.write(r.stdout[-3000:])
    line = [x for x in r.stdout.split("\n") if x.startswith("RL6_RESULT ")]
    if not line:
        print("AFTER RUN FAILED (no RL6_RESULT line)")
        sys.exit(2)
    scratch_removed = "SCRATCH_REMOVED=yes" in r.stdout and "HOST_TMP_og_rl6c_LEFTOVER=0" in r.stdout
    return json.loads(line[0][len("RL6_RESULT "):]), scratch_removed


def before_run():
    outf = os.path.join(tempfile.mkdtemp(prefix="og_rl6c_before_"), "rl6_before.out")
    env = dict(os.environ, OG_RL6_MODE="after")
    r = subprocess.run([sys.executable, os.path.join(HERE, "rl6c_ssm.py"), os.path.join(HERE, "rl6_host.py.txt"), outf], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    sys.stdout.write(r.stdout[-2000:])
    line = [x for x in r.stdout.split("\n") if x.startswith("RL6_RESULT ")]
    if not line:
        print("BEFORE RUN FAILED (no RL6_RESULT line)")
        sys.exit(2)
    return json.loads(line[0][len("RL6_RESULT "):])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    ap.add_argument("--served-release")
    ap.add_argument("--out", default=os.path.join(HERE, "RL6_DOWNLOAD.json"))
    a = ap.parse_args()
    R = host_read()
    if a.mode == "before":
        R["before_run"] = before_run()
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: MainPID %s, env key names %d, tools %d, /health %s, host-local /yearinreview %s; dim_asset download %s; dim_asset query %s" % (
            R["mainpid"], len(R["env_keys"]), len(R["tools"] or []), R["health"], R["yir_local"], R["before_run"]["dim_asset_download"], R["before_run"]["dim_asset_query"]))
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
    chk("shipped md5 = release bytes", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] > 0, "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    chk("tool list unchanged", R["tools"] is not None and R["tools"] == B["tools"], "before %d after %d tools" % (len(B["tools"] or []), len(R["tools"] or [])))
    chk(".env key names unchanged (50)", R["env_keys"] == B["env_keys"] and len(R["env_keys"]) == 50,
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), sorted(set(R["env_keys"]) - set(B["env_keys"])), sorted(set(B["env_keys"]) - set(R["env_keys"]))))
    A, scratch_removed = after_run()
    chk("host scratch removed", scratch_removed, "SCRATCH_REMOVED=yes and 0 leftovers" if scratch_removed else "see the SSM output above")
    chk("host-local GET /yearinreview with no identity is 401", R["yir_local"] == 401, "host-local code %s (before %s)" % (R["yir_local"], B.get("yir_local")))
    pc, loc = public_get()
    chk("public unauthenticated GET is 302 to login.microsoftonline.com", pc == 302 and "login.microsoftonline.com" in loc,
        "code %s, Location host %s" % (pc, loc.split("/")[2] if loc.count("/") >= 2 else loc[:40]))
    chk("pre-act read (live e91819e281): download OK", B["before_run"]["dim_asset_download"] == "OK", "pre-act %s" % B["before_run"]["dim_asset_download"])
    same = [k for k in ("dim_asset_download", "dim_asset_query", "empty_holdings_download", "held_check", "query_held_equal_download_held") if B["before_run"].get(k) == A.get(k)]
    chk("r17 behaviour unchanged by the act (5 fields equal the pre-act read)", len(same) == 5, "equal fields %d of 5: %s" % (len(same), same))
    chk("dim_asset download OK", A["dim_asset_download"] == "OK", "after %s" % A["dim_asset_download"])
    hc = A["held_check"]
    chk("held-only: returned > 0, unheld_returned 0", hc["returned"] > 0 and hc["unheld_returned"] == 0, "returned %s unheld_returned %s distinct %s" % (hc["returned"], hc["unheld_returned"], hc["distinct_returned"]))
    chk("held check GRADED (CVO Q2): held_cusips_in_dim_position < asset_universe_cusips", 0 < hc["held_cusips_in_dim_position"] < hc["asset_universe_cusips"],
        "held %s of asset universe %s (if held reaches the universe the check is UNGRADED: re-run with fewer accounts before closing)" % (hc["held_cusips_in_dim_position"], hc["asset_universe_cusips"]))
    chk("empty-holdings download REFUSED asset_read_denied_unqualified", "asset_read_denied_unqualified" in str(A["empty_holdings_download"]), A["empty_holdings_download"])
    chk("dim_asset query OK and its held set equals the download's", A["dim_asset_query"] == "OK" and A["query_held_equal_download_held"] is True,
        "query %s, query_returned %s, equal %s" % (A["dim_asset_query"], A["query_returned"], A["query_held_equal_download_held"]))
    chk("synthetic principal, grants_written 0, state_store_written False", A["synthetic_principal"] is True and A["grants_written"] == 0 and A["state_store_written"] is False,
        "synthetic %s grants_written %s state_store_written %s" % (A["synthetic_principal"], A["grants_written"], A["state_store_written"]))
    r17 = os.path.join(os.path.dirname(os.path.abspath(a.out)), "RL6_DOWNLOAD.r17.json")
    src = r17 if os.path.exists(r17) else a.out
    r17doc = json.load(open(src, encoding="utf-8")) if os.path.exists(src) else {"before": {"dim_asset_download": "ABSENT", "dim_asset_query": "ABSENT"}}
    doc = {"served_release": a.served_release, "before": r17doc["before"],
           "before_source": "carried from the r17 Phase B read (served_release %s)" % r17doc.get("served_release"),
           "pre_act_read_on_live": {"dim_asset_download": B["before_run"]["dim_asset_download"], "dim_asset_query": B["before_run"]["dim_asset_query"]},
           "after": {"dim_asset_download": A["dim_asset_download"], "empty_holdings_download": A["empty_holdings_download"], "dim_asset_query": A["dim_asset_query"]},
           "held_check": hc, "query_held_equal_download_held": A["query_held_equal_download_held"], "synthetic_principal": A["synthetic_principal"],
           "grants_written": A["grants_written"], "state_store_written": A["state_store_written"], "master": A["master"], "date": A["date"],
           "granted_accounts": A["granted_accounts"]}
    ok = all(res)
    out = a.out
    if ok:
        if not os.path.exists(r17) and os.path.exists(a.out):
            import shutil
            shutil.copyfile(a.out, r17)
    elif os.path.basename(a.out) == "RL6_DOWNLOAD.json":
        out = os.path.join(os.path.dirname(os.path.abspath(a.out)), "RL6_DOWNLOAD.r17b_failed.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s" % out)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy from /c/tmp/og-rb12 (ANNOUNCE_OG-rl-6-C.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
