"""OG-tr-1 CVO guard M1 (cvoO_NEVER_WIDEN_OG-tr-1_SECOND_HALF_20261001.md @00cb40bfff), host-side over SSM.

usage: python tr_m1.py compare   # BEFORE any upload: Tax secret vs each live bearer token, EQUAL/DIFFER per key only
       python tr_m1.py arm       # AFTER the deploy: the mail bearer and the transcripts bearer each presented to
                                 # /ms/taxsma-workbook must read 401 UNAUTHORIZED_CAPABILITY

Secrets are read into the host process memory (Secrets Manager via the host role for the Tax / mail / transcripts
secrets; /proc/<MainPID>/environ for the live .env keys, never sourcing .env) and are NEVER printed.
Exit 0 = every key DIFFER (compare) / both arms 401 UNAUTHORIZED_CAPABILITY (arm); 1 otherwise; 2 = host read failed.
"""
import base64
import json
import os
import subprocess
import sys
import time

INST = "i-07dccb1615503ac99"
HOST_PROG = r'''
import hmac, json, subprocess, sys, urllib.request, urllib.error
MODE = "@@MODE@@"
R = {"mode": MODE}
pid = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
R["mainpid"] = pid
env = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if b"=" in kv:
        k, v = kv.split(b"=", 1)
        env[k.decode()] = v.decode()
def sm(sid):
    out = subprocess.run(["aws", "secretsmanager", "get-secret-value", "--secret-id", sid, "--region", "us-east-1",
                          "--query", "SecretString", "--output", "text"], capture_output=True, text=True)
    v = out.stdout.strip() if out.returncode == 0 else ""
    return "" if v == "None" else v
if MODE == "compare":
    tax = sm("gateway/global/taxsma-workbook-token")
    R["tax_read_nonempty"] = bool(tax)
    res = {}
    for key in ("TRANSCRIPT_BEARER", "MAIL_BEARER", "OTP_BEARER", "MS_INGEST_BEARER", "GRAPH_READ_BEARER"):
        raw = env.get(key, "")
        toks = raw.split()
        if not toks:
            res[key] = ["ABSENT"]
            continue
        res[key] = ["EQUAL" if (tax and hmac.compare_digest(tax.encode(), t.encode())) else "DIFFER" for t in toks]
    R["compare"] = res
else:
    res = {}
    for name, sid, key in (("mail", "gateway/mail/bearer", "MAIL_BEARER"), ("transcripts", "gateway/transcripts/bearer", "TRANSCRIPT_BEARER")):
        tok = sm(sid)
        res[name + "_secret_nonempty"] = bool(tok)
        req = urllib.request.Request("http://localhost:8080/ms/taxsma-workbook")
        req.add_header("Authorization", "Bearer " + tok)
        try:
            code, body = urllib.request.urlopen(req, timeout=20).status, ""
        except urllib.error.HTTPError as e:
            code, body = e.code, e.read(600).decode("utf-8", "replace")
        res[name] = {"status": code, "UNAUTHORIZED_CAPABILITY": "UNAUTHORIZED_CAPABILITY" in body}
    R["arm"] = res
print("HOSTJSON " + json.dumps(R))
'''

def aws(args):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")

def main():
    mode = sys.argv[1]
    prog = HOST_PROG.replace("@@MODE@@", mode)
    b64 = base64.b64encode(prog.encode()).decode()
    params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_tr_m1.py" % b64, "/opt/opal-gateway/.venv/bin/python /tmp/og_tr_m1.py", "rm -f /tmp/og_tr_m1.py"]})
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_tr_m1_params.json")
    with open(pf, "w", encoding="utf-8", newline="\n") as f:
        f.write(params)
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-tr-1 M1 " + mode,
             "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:300])
        return 2
    cid = r.stdout.strip()
    st = ""
    for _ in range(40):
        time.sleep(3)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    line = [x for x in out.split("\n") if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-600:])
        return 2
    R = json.loads(line[0][9:])
    if mode == "compare":
        print("tax secret read non-empty on host: %s" % R["tax_read_nonempty"])
        for k, v in R["compare"].items():
            print("M1 %s: %s" % (k, " ".join(v)))
        ok = R["tax_read_nonempty"] and all(x == "DIFFER" for v in R["compare"].values() for x in v)
        print("M1 COMPARE: %s" % ("ALL DIFFER" if ok else "STOP (an EQUAL, ABSENT or empty read)"))
        return 0 if ok else 1
    a = R["arm"]
    for n in ("mail", "transcripts"):
        print("M1 ARM %s bearer (secret non-empty %s) -> /ms/taxsma-workbook status %s UNAUTHORIZED_CAPABILITY %s" % (n, a[n + "_secret_nonempty"], a[n]["status"], a[n]["UNAUTHORIZED_CAPABILITY"]))
    ok = all(a[n]["status"] == 401 and a[n]["UNAUTHORIZED_CAPABILITY"] and a[n + "_secret_nonempty"] for n in ("mail", "transcripts"))
    print("M1 ARM: %s" % ("PASS 2 of 2" if ok else "FAIL"))
    return 0 if ok else 1

sys.exit(main())
