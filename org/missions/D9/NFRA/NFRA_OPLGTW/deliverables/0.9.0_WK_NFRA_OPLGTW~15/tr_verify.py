"""OG-tr-1 PHASE B verify (row NFRA_OPLGTW-Z-W15-S18), written at PHASE A, run IMMEDIATELY after the deploy returns.

usage:  python tr_verify.py before <state.json>      # BEFORE reads on the live host, saved (run before the act)
        python tr_verify.py after  <state.json>      # AFTER reads + every comparison; exit 0 = all PASS, 1 = a FAIL (roll back)

Host reads only, by SSM AWS-RunShellScript. Key NAMES and booleans only: no .env value is ever printed, the file is never
sourced (standing rule Z-S32); the one value read from /proc/<pid>/environ (MS_INGEST_BEARER, for a 200 probe) is never
echoed. The shipped-file md5 list is tr_release_md5.txt beside this file (the release branch HEAD's app/**, deploy/**,
requirements.txt, identity_tool_allowlist.txt).

after-mode checks: host /health 200; shipped md5 = release bytes (all files); tool list unchanged; .env keys 46 -> 48 with
the other 46 unchanged and both TAXSMA_WORKBOOK_ keys present and non-empty; ENABLED_INTEGRATIONS unchanged; /ms/*, /hx/*,
/otp/*, /mcp probe codes unchanged from BEFORE; /ms/taxsma-workbook with no bearer = 401 UNAUTHORIZED_CAPABILITY (BEFORE 404).
"""
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
HOST_PROG = r'''
import hashlib, json, os, re, subprocess, sys, urllib.request, urllib.error
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
keys, vals = [], {}
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.rstrip("\n"))
    if m:
        keys.append(m.group(1)); vals[m.group(1)] = m.group(2)
R["env_keys"] = sorted(keys)
R["enabled_integrations"] = vals.get("ENABLED_INTEGRATIONS")
R["taxsma_nonempty"] = {k: (vals.get(k, "").strip() != "") for k in ("TAXSMA_WORKBOOK_BEARER", "TAXSMA_WORKBOOK_IDENTITY")}
R["taxsma_module_present"] = os.path.exists("app/taxsma_workbook.py")
tool_src = """
import asyncio, os, sys
sys.path.insert(0, "/opt/opal-gateway")
from app import tools, integrations
ids = os.environ["ENABLED_INTEGRATIONS"].split()
rep = integrations.register_enabled(tools.mcp, ids)
from mcp.server.fastmcp import FastMCP
names = sorted(t.name for t in asyncio.run(FastMCP.list_tools(tools.mcp)))
print("TOOLNAMES", ",".join(names))
print("INTEGRATION_ERRORS", len([k for k, v in rep.items() if "error" in v]))
"""
out = subprocess.run(["env", "-i", "HOME=/tmp", "PATH=" + os.environ.get("PATH", ""), "MOCK_GRAPH=1",
                      "ENABLED_INTEGRATIONS=" + (vals.get("ENABLED_INTEGRATIONS") or ""), "/opt/opal-gateway/.venv/bin/python", "-c", tool_src],
                     capture_output=True, text=True).stdout
tn = [l for l in out.split("\n") if l.startswith("TOOLNAMES ")]
R["tools"] = tn[0].split(" ", 1)[1].split(",") if tn else None
R["tool_integration_errors"] = [l for l in out.split("\n") if l.startswith("INTEGRATION_ERRORS")]
pid = R["mainpid"]; msb = None
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if kv.startswith(b"MS_INGEST_BEARER="):
        msb = kv.split(b"=", 1)[1].decode()
def code(path, bearer=None):
    req = urllib.request.Request("http://localhost:8080" + path)
    if bearer is not None:
        req.add_header("Authorization", "Bearer " + bearer)
    try:
        return urllib.request.urlopen(req, timeout=15).status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.read(400).decode("utf-8", "replace")
    except Exception as e:
        return "ERR:" + type(e).__name__, ""
Z = "0" * 64
P = {}
P["/health"] = code("/health")[0]
P["/ms/health none/bad/ms"] = [code("/ms/health")[0], code("/ms/health", Z)[0], code("/ms/health", msb or "absent")[0]]
P["/ms/sites none/bad"] = [code("/ms/sites")[0], code("/ms/sites", Z)[0]]
P["/hx/mail/messages/<id> none/bad"] = [code("/hx/mail/messages/AAA")[0], code("/hx/mail/messages/AAA", Z)[0]]
P["/hx/mail/messages (listing) none/bad"] = [code("/hx/mail/messages")[0], code("/hx/mail/messages", Z)[0]]
P["/hx/transcripts/meetings/<m>/transcripts none/bad"] = [code("/hx/transcripts/meetings/M/transcripts")[0], code("/hx/transcripts/meetings/M/transcripts", Z)[0]]
P["/otp/health none/bad"] = [code("/otp/health")[0], code("/otp/health", Z)[0]]
P["/mcp unauth"] = code("/mcp")[0]
c, body = code("/ms/taxsma-workbook")
P["/ms/taxsma-workbook no-bearer"] = c
R["taxsma_no_bearer_unauthorized_capability"] = "UNAUTHORIZED_CAPABILITY" in body
R["probes"] = P
print("HOSTJSON " + json.dumps(R))
'''


def aws(args):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def host_read():
    md5 = open(os.path.join(HERE, "tr_release_md5.txt"), encoding="utf-8").read()
    prog = HOST_PROG.replace("@@MD5@@", md5.replace("\r", ""))
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_tr_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_tr_verify.py",
                                      "rm -f /tmp/og_tr_verify.py"]})
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_tr_verify_params.json")
    with open(pf, "w", encoding="utf-8", newline="\n") as f:
        f.write(params)
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-tr-1 verify host read",
             "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:300])
        sys.exit(2)
    cid = r.stdout.strip()
    st = ""
    for _ in range(40):
        time.sleep(3)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status",
                  "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query",
               "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    return json.loads(line[0][len("HOSTJSON "):])


def main():
    mode, path = sys.argv[1], sys.argv[2]
    R = host_read()
    if mode == "before":
        json.dump(R, open(path, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: env keys %d, tools %s, taxsma module present %s, /ms/taxsma-workbook %s, /health %s" % (
            len(R["env_keys"]), len(R["tools"] or []), R["taxsma_module_present"], R["probes"]["/ms/taxsma-workbook no-bearer"], R["probes"]["/health"]))
        return 0
    B = json.load(open(path, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(ok)
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200", R["probes"]["/health"] == 200 and R["active"] == "active", "health %s, service %s, MainPID %s (before %s)" % (R["probes"]["/health"], R["active"], R["mainpid"], B["mainpid"]))
    chk("shipped md5 = release bytes", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] > 0, "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    chk("tool list unchanged", R["tools"] == B["tools"] and R["tools"] is not None, "before %s after %s tools" % (len(B["tools"] or []), len(R["tools"] or [])))
    kb, ka = set(B["env_keys"]), set(R["env_keys"])
    added, removed = sorted(ka - kb), sorted(kb - ka)
    chk(".env keys 46 -> 48, the other 46 unchanged", len(kb) == 46 and len(ka) == 48 and added == ["TAXSMA_WORKBOOK_BEARER", "TAXSMA_WORKBOOK_IDENTITY"] and not removed,
        "before %d after %d added %s removed %s" % (len(kb), len(ka), added, removed))
    chk("both TAXSMA keys non-empty (capability ON)", all(R["taxsma_nonempty"].values()), "%s" % R["taxsma_nonempty"])
    chk("ENABLED_INTEGRATIONS unchanged", R["enabled_integrations"] == B["enabled_integrations"], "%s" % R["enabled_integrations"])
    same = {k: (B["probes"].get(k), v) for k, v in R["probes"].items() if not k.startswith("/ms/taxsma")}
    diff = {k: x for k, x in same.items() if x[0] != x[1]}
    chk("/ms/*, /hx/*, /otp/*, /mcp probe codes as before", not diff, "%d probes compared; differing %s" % (len(same), diff))
    chk("/ms/taxsma-workbook no bearer = 401 UNAUTHORIZED_CAPABILITY", R["probes"]["/ms/taxsma-workbook no-bearer"] == 401 and R["taxsma_no_bearer_unauthorized_capability"],
        "host status %s (before %s), body names UNAUTHORIZED_CAPABILITY %s" % (R["probes"]["/ms/taxsma-workbook no-bearer"], B["probes"].get("/ms/taxsma-workbook no-bearer"), R["taxsma_no_bearer_unauthorized_capability"]))
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy the og-rb6 command (ANNOUNCE_OG-tr-1.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
