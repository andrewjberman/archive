"""host_read.py -- runs ON the gateway host via SSM, as ec2-user, under /opt/opal-gateway/.venv/bin/python.
READ-ONLY. Parses /opt/opal-gateway/.env in Python (never shell-sourced: row Z-S73). Prints: time, /health, the
ENABLED_INTEGRATIONS value (ids, not secret), the .env KEY names (never values), the line count, the non-secret
state of MAIL_SENDER_TABLE (empty / length only), and the sha256 of every deployed file."""

import hashlib
import os
import time
import urllib.request

ROOT = "/opt/opal-gateway"
print("---TIME", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
try:
    print(
        "---HEALTH",
        urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10).status,
    )
except Exception as e:
    print("---HEALTH EXC", type(e).__name__)
env = {}
n = 0
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        n += 1
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v
print("---ENABLED ENABLED_INTEGRATIONS=" + env.get("ENABLED_INTEGRATIONS", "<absent>"))
print("---ENVKEYS")
for k in sorted(env):
    print(k)
print("---ENVLINES", n, "KEYS", len(env), "DISTINCT", len(set(env)))
for k in (
    "MAIL_SENDER_TABLE",
    "MSP_CALLING_IDENTITIES",
    "TRANSCRIPT_MEETING_ALLOWLIST",
    "MAIL_PDF_MAX_BYTES",
    "TRANSCRIPT_BEARER_LABELS",
    "MAIL_BEARER_LABELS",
):
    v = env.get(k)
    print(
        "---STATE",
        k,
        "ABSENT"
        if v is None
        else (
            "EMPTY"
            if v == ""
            else "SET len=%d items=%d"
            % (len(v), len([x for x in v.split(",") if x.strip()]))
        ),
    )
for k in (
    "INTERNAL_READER_ROLE_ARN",
    "MASTER_ADMIN_PRINCIPALS",
    "WRITE_CAPABLE_PRINCIPALS",
    "BLACKDIAMOND_READER_ROLE_ARN",
    "BLACKDIAMOND_READER_EXTERNAL_ID",
):
    v = env.get(k)
    print("---PRESENT", k, "NO" if v is None else ("EMPTY" if v == "" else "YES"))
print("---HASHES")
out = []
for top in ("app", "deploy", "dashboard"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, top)):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for x in fn:
            if x.endswith(".log") or x.endswith(".pyc"):
                continue
            p = os.path.join(dp, x)
            out.append(
                (
                    os.path.relpath(p, ROOT).replace(os.sep, "/"),
                    hashlib.sha256(open(p, "rb").read()).hexdigest(),
                )
            )
for x in ("requirements.txt", "identity_tool_allowlist.txt"):
    p = os.path.join(ROOT, x)
    if os.path.exists(p):
        out.append((x, hashlib.sha256(open(p, "rb").read()).hexdigest()))
for rel, h in sorted(out):
    print("%s  %s" % (h, rel))
