"""r13_host.py -- runs ON the gateway host (shipped via SSM by r11.AC2.sh) under /opt/opal-gateway/.venv/bin/python.
Loads /opt/opal-gateway/.env the way systemd's EnvironmentFile does (split at the first '='), NEVER through a shell, then
runs the two round-12 instruments (shipped beside it in /tmp) against the DEPLOYED tree, its deployed catalog and its
own ENABLED_INTEGRATIONS. Prints only the instruments' PARTITION / SERVED / DISCOVER lines; never an env value.
"""
import os
import subprocess
import sys

ROOT = "/opt/opal-gateway"
env = dict(os.environ)
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env.setdefault(k.strip(), v.strip('"'))
enabled = env.get("ENABLED_INTEGRATIONS", "").replace(",", " ")
cat = os.path.join(ROOT, "app", "refs", "DATA_CATALOG.yaml")
for name, args in (("index", ["/tmp/c11_index.py", ROOT, cat, enabled]), ("discover", ["/tmp/c10_discover.py", ROOT])):
    p = subprocess.run([sys.executable] + args, env=env, cwd=ROOT, capture_output=True, text=True, timeout=240)
    for line in (p.stdout or "").splitlines():
        if line.startswith(("SERVED ", "PARTITION ", "DISCOVER ", "discover reads", "  MISSING")):
            print(line)
    print("RC %s=%d" % (name, p.returncode))
    if p.returncode not in (0, 1):
        print("ERR %s %s" % (name, (p.stderr or "").strip().splitlines()[-1:]))
