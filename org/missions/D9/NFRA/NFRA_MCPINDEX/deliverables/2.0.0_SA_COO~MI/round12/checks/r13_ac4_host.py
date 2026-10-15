"""r13_ac4_host.py -- runs ON the gateway host (shipped via SSM by r13.AC4.sh) under /opt/opal-gateway/.venv/bin/python.
Reads the DEPLOYED catalog app/refs/DATA_CATALOG.yaml and prints, for the round 13/14/16 catalog: version, harvest rows, table rows, table rows
with a key_template, retired table rows, the distinct read_tool names the rows name, and the file's md5. Reads one file; prints no env value."""
import hashlib
import sys

import yaml

p = "/opt/opal-gateway/app/refs/DATA_CATALOG.yaml"
raw = open(p, "rb").read()
cat = yaml.safe_load(raw.decode("ascii"))
rows = [r for k in ("silver_datasets", "portal_datasets") for r in (cat.get(k) or [])]
table = [r for r in rows if isinstance(r, dict) and "contract" in r]
tools = set()
for sec in ("silver_datasets", "portal_datasets", "harvest_datasets"):
    for r in (cat.get(sec) or []):
        if isinstance(r, dict) and r.get("read_tool"):
            tools.add(str(r["read_tool"]))
print("CATALOG version=%s harvest=%d table=%d key_template=%d retired=%d" % (
    cat.get("version"), len(cat.get("harvest_datasets") or []), len(table), sum(1 for r in table if r.get("key_template")),
    sum(1 for r in table if r.get("retired") is True)))
print("TOOLS %s" % ",".join(sorted(tools)))
print("MD5 %s" % hashlib.md5(raw).hexdigest())
sys.exit(0)
