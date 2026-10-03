"""OG-rl-4 PHASE B verify (row Z-W15-S18, filed as Z-W15-S30), written at PHASE A, run IMMEDIATELY after the deploy returns.

usage:  python rl4_verify.py before <state.json>      # BEFORE reads on the live host + the three route reads, saved (run before the act)
        python rl4_verify.py after  <state.json>      # AFTER reads + every comparison; exit 0 = all PASS, 1 = a FAIL (roll back)

HOST reads are by SSM AWS-RunShellScript; the route reads are HTTPS GETs to the public gateway. Never printed: any .env value, any bearer,
any identifier. The state file holds key NAMES, 16-hex hash prefixes of the service PROCESS's environment values (what systemd actually
handed the app; used only to prove unchanged-ness) and status codes: keep it out of the repository (it is written to the path given).
The shipped-file md5 list is rl4_release_md5.txt beside this file (the release HEAD's app/**, deploy/**, requirements.txt,
identity_tool_allowlist.txt, 94 files).

after-mode checks:
  1. host /health 200 and service active;
  2. shipped md5 = release bytes (94 files);
  3. tool list unchanged;
  4. .env key NAMES equal r14/RL4_ENV_KEYS_BEFORE.txt (50) and equal the BEFORE state's names;
  5. every service-process environment value hash equals its BEFORE hash (the quoting changed no value the app reads: 50 of 50);
  6. ENABLED_INTEGRATIONS unchanged; both TAXSMA_WORKBOOK_ keys non-empty;
  7. every host /ms/* /hx/* /otp/* /mcp probe code as before;
  8. ONE authorized read each with the route's OWN bearer (Secrets Manager, in memory): /hx/mail listing 200; /hx/teams/me 200;
     /hx/transcripts: the bearer is ACCEPTED (403 meeting_not_allowed, or 200) and NOT refused (401) -- see row Z-W15-S31: the live
     TRANSCRIPT_MEETING_ALLOWLIST is empty, so no 200 exists to read; the symmetric refusal returns 401 unauthorized, so 403 vs 401
     is exactly the discriminator (a shared value would read 401). The same three codes are saved at BEFORE for comparison.
Then rl4.AC1.sh, tr.AC1.sh and ht.AC2.sh run from rl4_verify.sh.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
BASE = "https://mcp.opalinvest.dev"
BEFORE_NAMES = os.path.join(HERE, "..", "2.0.0_SA_COO~O", "r14", "RL4_ENV_KEYS_BEFORE.txt")
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
pid = R["mainpid"]
penv = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if b"=" in kv:
        k, v = kv.split(b"=", 1)
        penv[k.decode("utf-8", "replace")] = v
R["proc_env_hash"] = {k: hashlib.sha256(penv[k]).hexdigest()[:16] for k in keys if k in penv}
R["proc_env_missing"] = sorted(k for k in keys if k not in penv)
R["enabled_integrations"] = penv.get("ENABLED_INTEGRATIONS", b"").decode("utf-8", "replace")
R["taxsma_nonempty"] = {k: (penv.get(k, b"").strip() != b"") for k in ("TAXSMA_WORKBOOK_BEARER", "TAXSMA_WORKBOOK_IDENTITY")}
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
                      "ENABLED_INTEGRATIONS=" + R["enabled_integrations"], "/opt/opal-gateway/.venv/bin/python", "-c", tool_src],
                     capture_output=True, text=True).stdout
tn = [l for l in out.split("\n") if l.startswith("TOOLNAMES ")]
R["tools"] = tn[0].split(" ", 1)[1].split(",") if tn else None
msb = penv.get("MS_INGEST_BEARER", b"").decode("utf-8", "replace") or None
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
P["/hx/teams/me none/bad"] = [code("/hx/teams/me")[0], code("/hx/teams/me", Z)[0]]
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
    md5 = open(os.path.join(HERE, "rl4_release_md5.txt"), encoding="utf-8").read()
    prog = HOST_PROG.replace("@@MD5@@", md5.replace("\r", ""))
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_rl4_verify.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_rl4_verify.py",
                                      "rm -f /tmp/og_rl4_verify.py"]})
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl4_verify_params.json")
    with open(pf, "w", encoding="utf-8", newline="\n") as f:
        f.write(params)
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-4 verify host read",
             "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
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


def secret(sid):
    r = aws(["secretsmanager", "get-secret-value", "--region", "us-east-1", "--secret-id", sid, "--query", "SecretString", "--output", "text"])
    return r.stdout.strip() if r.returncode == 0 else ""


def get(path, bearer):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + bearer})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read().decode("utf-8", "replace")
            code = r.status
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read(2000).decode("utf-8", "replace")
    try:
        d = json.loads(body)
    except ValueError:
        d = None
    err = d.get("error") if isinstance(d, dict) else None
    keys = sorted(d.keys()) if isinstance(d, dict) else None
    return code, err, keys


def route_reads():
    """ONE authorized read per route with its OWN bearer, in memory. Returns status codes, error codes and top-level key names only."""
    now = datetime.now(timezone.utc).replace(microsecond=0)

    def fmt(t):
        return t.strftime("%Y-%m-%dT%H:%M:%SZ")

    out = {}
    b = secret("gateway/mail/bearer")
    sender = os.environ.get("OG_RL4_MAIL_SENDER", "").strip().lower()   # an address from the shipped sender table, set by rl4_verify.sh
    if not sender:
        print("OG_RL4_MAIL_SENDER unset: run through rl4_verify.sh")
        sys.exit(2)
    out["mail_listing"] = get("/hx/mail/messages?sender=%s&received_from=%s&received_to=%s&page_size=1" % (sender, fmt(now - timedelta(days=2)), fmt(now)), b) if b else (0, "bearer-read-empty", None)
    b = secret("gateway/transcripts/bearer")
    out["transcripts_meeting"] = get("/hx/transcripts/meetings/OG-RL4-VERIFY-NOT-ON-ALLOWLIST/transcripts", b) if b else (0, "bearer-read-empty", None)
    b = secret("gateway/teams/bearer")
    out["teams_me"] = get("/hx/teams/me", b) if b else (0, "bearer-read-empty", None)
    b = None
    return {k: list(v) for k, v in out.items()}


def main():
    mode, path = sys.argv[1], sys.argv[2]
    R = host_read()
    R["routes"] = route_reads()
    if mode == "before":
        json.dump(R, open(path, "w", encoding="utf-8"), indent=1)
        print("BEFORE saved: env keys %d, process-env hashes %d, tools %s, /health %s, routes %s" % (
            len(R["env_keys"]), len(R["proc_env_hash"]), len(R["tools"] or []), R["probes"]["/health"],
            {k: v[:2] for k, v in R["routes"].items()}))
        return 0
    B = json.load(open(path, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(ok)
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200", R["probes"]["/health"] == 200 and R["active"] == "active", "health %s, service %s, MainPID %s (before %s)" % (R["probes"]["/health"], R["active"], R["mainpid"], B["mainpid"]))
    chk("shipped md5 = release bytes", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] > 0, "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    chk("tool list unchanged", R["tools"] == B["tools"] and R["tools"] is not None, "before %s after %s tools" % (len(B["tools"] or []), len(R["tools"] or [])))
    want = sorted(ln.strip() for ln in open(BEFORE_NAMES, encoding="utf-8") if ln.strip() and not ln.startswith("#"))
    chk(".env key names = RL4_ENV_KEYS_BEFORE.txt (50) = the BEFORE state", R["env_keys"] == want and R["env_keys"] == B["env_keys"] and len(want) == 50,
        "names %d vs list %d; added %s removed %s" % (len(R["env_keys"]), len(want), sorted(set(R["env_keys"]) - set(want)), sorted(set(want) - set(R["env_keys"]))))
    same = {k for k, h in R["proc_env_hash"].items() if B["proc_env_hash"].get(k) == h}
    diff = sorted(k for k in set(R["proc_env_hash"]) | set(B["proc_env_hash"]) if R["proc_env_hash"].get(k) != B["proc_env_hash"].get(k))
    chk("every service-process env value equals its BEFORE value (hash prefix)", not diff and not R["proc_env_missing"] and len(R["proc_env_hash"]) == 50,
        "%d of %d identical; differing names %s; absent from the process %s" % (len(same), len(R["proc_env_hash"]), diff, R["proc_env_missing"]))
    chk("ENABLED_INTEGRATIONS unchanged; both TAXSMA_WORKBOOK_ keys non-empty", R["enabled_integrations"] == B["enabled_integrations"] and all(R["taxsma_nonempty"].values()),
        "integrations %s; taxsma non-empty %s" % (R["enabled_integrations"], R["taxsma_nonempty"]))
    same_p = {k: (B["probes"].get(k), v) for k, v in R["probes"].items()}
    diff_p = {k: x for k, x in same_p.items() if x[0] != x[1]}
    chk("host probe codes as before", not diff_p, "%d probes compared; differing %s" % (len(same_p), diff_p))
    rr = R["routes"]
    chk("/hx/mail listing, own bearer: 200", rr["mail_listing"][0] == 200, "status %s keys %s (before %s)" % (rr["mail_listing"][0], rr["mail_listing"][2], B["routes"]["mail_listing"][0]))
    chk("/hx/teams/me, own bearer: 200", rr["teams_me"][0] == 200, "status %s keys %s (before %s)" % (rr["teams_me"][0], rr["teams_me"][2], B["routes"]["teams_me"][0]))
    tm = rr["transcripts_meeting"]
    chk("/hx/transcripts, own bearer ACCEPTED (403 meeting_not_allowed or 200; 401 = the refusal fired)", (tm[0] == 403 and tm[1] == "meeting_not_allowed") or tm[0] == 200,
        "status %s error %s (before %s %s)" % (tm[0], tm[1], B["routes"]["transcripts_meeting"][0], B["routes"]["transcripts_meeting"][1]))
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy the og-rb9 command (ANNOUNCE_OG-rl-4.md), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
