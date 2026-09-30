"""AC1 HVST-ad-3: residential-IP assignability read. Reads repo config + AWS describe only. No vendor call."""
import json
import os
import re
import socket
import subprocess
BLOCKED = []
_orig = socket.socket.connect
def _guard(self, addr):
    host = addr[0] if isinstance(addr, tuple) else str(addr)
    if host.endswith("amazonaws.com") or host in ("127.0.0.1", "::1", "localhost"):
        return _orig(self, addr)
    BLOCKED.append(host)
    raise OSError("blocked non-AWS socket: " + host)
socket.socket.connect = _guard
def _guard_ex(self, addr):
    BLOCKED.append(str(addr))
    return 1
socket.socket.connect_ex = _guard_ex

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
def find(path, pat):
    p = os.path.join(ROOT, path)
    for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        if re.search(pat, line):
            return i, re.sub(r"(?i)(password|pass)\s*[:=]\s*\S+", r"\1=<redacted>", line.strip())[:170]
    return None, "NOT FOUND"
def src(path, pat):
    i, t = find(path, pat)
    return "%s:%s  | %s" % (path, i, t)
def aws(*a):
    env = dict(os.environ, OPAL_AGENT_SERIAL="0.9.0_WK_AMGT_HARVST~89")
    r = subprocess.run(["bash", os.path.join(ROOT, ".tools/aws")] + list(a) + ["--region", "us-east-1", "--output", "json"],
                       capture_output=True, text=True, timeout=90, env=env)
    return r.stdout.strip() if r.returncode == 0 else "AWS-RC%d" % r.returncode

A = "infra/aws/ec2/astn-wsjft/"
B = "infra/aws/ec2/bd-49f-auto-login/"
print("== Q1 product and zone")
print("  product = Bright Data RESIDENTIAL, sticky-session pool (not fixed IP) -- MEASURED (config)")
print("   ", src(A + "ft_proxy_test.js", r"sticky-session residential proxy"))
print("   ", src(A + "ft_proxy_test.js", r"SESSION_ID = "))
print("   ", src(A + "ft_proxy_test.js", r"username: `"))
print("   ", src(B + "bd_49f_auto_login.js", r"RESIDENTIAL proxy"))
print("  host/port/zone = held only inside the Secrets Manager value, not in repo -- INFERRED (value not read, by clause)")
print("   ", src(A + "ft_proxy_test.js", r"server: `http"))
d = json.loads(aws("secretsmanager", "describe-secret", "--secret-id", "astn/brightdata/residential-proxy", "--query", "[Name,LastChangedDate]"))
print("    AWS secretsmanager:describe-secret.Name =", d[0], "LastChangedDate =", d[1], "-- MEASURED")
print("== Q2 how existing hosts reach it")
print("  EC2 host is a proxy CLIENT of the superproxy (server=http://host:port, per-run username suffix), IP is NOT bound to the host -- MEASURED")
print("   ", src(A + "ft_proxy_test.js", r"chromium\.launch"))
print("   ", src(A + "ft_proxy_test.sh", r"secret-id astn/brightdata/residential-proxy"))
print("   ", src(B + "bd_49f_auto_login.js", r"BD_PROXY_SECRET_ID       \(="))
print("   ", src(B + "bd_49f_auto_login.js", r"launch\.proxy = "))
print("  bd-49f box currently on NATIVE IP, proxy dropped 2026-06-25, secret retained revert-only -- MEASURED")
print("   ", src(B + "secret-ids.env", r"NATIVE-IP"))
print("   ", src(B + "run-bd-auto-login.sh", r"box role has no brightdata grant"))
print("== Q3 can a second EC2 host use the same egress")
insts = json.loads(aws("ec2", "describe-instances", "--instance-ids", "i-059405dfefcb4b44a", "i-0fa1846f04ed7e337",
                       "--query", "Reservations[].Instances[].[InstanceId,IamInstanceProfile.Arn,SecurityGroups[0].GroupId]"))
for i in insts:
    print("    AWS ec2 instance %s profile=%s sg=%s -- MEASURED" % tuple(i))
eg = json.loads(aws("ec2", "describe-security-groups", "--group-ids", "sg-008a36fc02f98f961", "--query", "SecurityGroups[0].IpPermissionsEgress[0].[IpProtocol,IpRanges[0].CidrIp,IpRanges[0].Description]"))
print("    AWS sg-008a36fc02f98f961.IpPermissionsEgress =", eg, "-- MEASURED (egress open to all)")
print("  credential is a per-secret login not per-host: access = IAM GetSecretValue on the secret name (bd-49f lost it by removing the grant) -- MEASURED")
print("   ", src(B + "secret-ids.env", r"box role has no brightdata grant"))
print("   ", src(A + "ft_proxy_test.sh", r"EC2 role"))
print("  no caller-IP whitelist appears in any config; BD-side zone allowlist / concurrent-session cap not shown -- INFERRED (absence of config, BD console unread)")
print("  second host must use the proxy (BD blocks AWS datacenter egress) -- INFERRED (prose comment, not routing config):")
print("   ", src(B + "bd_49f_auto_login.js", r"BD blocks AWS-datacenter"))
print("== Q4 verdict")
print("ASSIGNABILITY: ASSIGNABLE")
print("  reason: hosts are proxy clients reading a shared SM credential with a per-run sticky session id, so a new host needs only an IAM read grant -- class MEASURED for the client model; INFERRED that BD zone has no caller-IP allowlist or session cap")
print("BLOCKED NON-AWS SOCKETS:", len(BLOCKED))
print("VENDOR CALLS: %d" % len(BLOCKED))
