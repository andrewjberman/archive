"""env_render.py <deploy-to-ec2.sh> <host_read.txt>: take the script's .env printf line, substitute its deploy-time values (
by plain substitution of the four deploy-time values), execute ONLY its .env printf with dummy host-side variables, and print KEY NAMES against the
host's key set (keys only, never values; nothing here is a real value)."""

import re
import subprocess
import sys

script = open(sys.argv[1], encoding="utf-8").read()
line = next(ln for ln in script.splitlines() if ln.startswith("printf 'MOCK_GRAPH=0"))
for k, v in (
    ("${REGION}", "us-east-1"),
    ("${GATEWAY_PORT}", "8080"),
    ("${REMOTE_DIR}", "/opt/opal-gateway"),
    ("${OG_MAIL_SENDER_TABLE}", "dummy@example.com"),
):
    line = line.replace(k, v)
line = line.replace(chr(92) + "$", "$")
line = line.split(" | sudo -u ec2-user tee")[0]
dummy = "TENANT_ID=t CLIENT_ID=c CLIENT_SECRET=s FERNET_KEY=f OTP_BEARER=o MS_INGEST_BEARER=m GRAPH_READ_BEARER=g MASTER_ADMIN_PRINCIPALS=a/b WRITE_CAPABLE_PRINCIPALS=c/d TRANSCRIPT_BEARER=t2 MAIL_BEARER=mb BD_READER_EXTERNAL_ID=bd"
out = subprocess.run(
    ["bash", "-c", "export " + dummy + "; " + line],
    capture_output=True,
    text=True,
    encoding="utf-8",
).stdout
keys = [
    ln.split("=", 1)[0]
    for ln in out.split("\n")
    if "=" in ln and re.match(r"[A-Za-z_]", ln)
]
host = open(sys.argv[2], encoding="utf-8").read()
hk = host.split("---ENVKEYS\n")[1].split("---ENVLINES")[0].split()
print(
    "rendered keys: %d (distinct %d); host keys: %d (distinct %d)"
    % (len(keys), len(set(keys)), len(hk), len(set(hk)))
)
print("host keys NOT rendered (dropped):", sorted(set(hk) - set(keys)))
print("rendered keys NOT on host (added):", sorted(set(keys) - set(hk)))
en = [ln for ln in out.split("\n") if ln.startswith("ENABLED_INTEGRATIONS=")]
print("rendered ENABLED_INTEGRATIONS:", en)
hen = re.search(r"ENABLED_INTEGRATIONS=(.*)", host).group(1)
print(
    "host     ENABLED_INTEGRATIONS: ['ENABLED_INTEGRATIONS=%s']" % hen,
    "EQUAL" if en and en[0].split("=", 1)[1] == hen else "DIFFERENT",
)
# value lines other than the secret-fed ones: compare to the host state is impossible (values never read); compare script-vs-live-script instead
