"""r14_ac4_host.py [catalog path] -- runs ON the gateway host (shipped via SSM by r14.AC4.sh) under /opt/opal-gateway/.venv/bin/python, or locally on a planted
catalog when given a path. Reads the app/refs/DATA_CATALOG.yaml and prints, for the round 17 catalog: version, harvest rows, table rows, table rows with a
key_template, retired table rows, the rows in all three sections, the rows with a non-empty nl_tags, the rows marked nl_tags_basis inferred, the rows
carrying a firm field, the distinct read_tool names, and the file's md5. Reads one file; prints no env value."""
import hashlib
import sys

import yaml

p = sys.argv[1] if len(sys.argv) > 1 else "/opt/opal-gateway/app/refs/DATA_CATALOG.yaml"
raw = open(p, "rb").read()
cat = yaml.safe_load(raw.decode("ascii"))
secs = ("silver_datasets", "portal_datasets", "harvest_datasets")
allrows = [r for k in secs for r in (cat.get(k) or []) if isinstance(r, dict)]
table = [r for k in ("silver_datasets", "portal_datasets") for r in (cat.get(k) or []) if isinstance(r, dict) and "contract" in r]
tools = sorted({str(r["read_tool"]) for r in allrows if r.get("read_tool")})
print("CATALOG version=%s harvest=%d table=%d key_template=%d retired=%d rows=%d nl_tags=%d inferred=%d firm=%d" % (
    cat.get("version"), len(cat.get("harvest_datasets") or []), len(table), sum(1 for r in table if r.get("key_template")),
    sum(1 for r in table if r.get("retired") is True), len(allrows),
    sum(1 for r in allrows if isinstance(r.get("nl_tags"), list) and r["nl_tags"]),
    sum(1 for r in allrows if r.get("nl_tags_basis") == "inferred"), sum(1 for r in allrows if r.get("firm"))))
print("TOOLS %s" % ",".join(tools))
print("MD5 %s" % hashlib.md5(raw).hexdigest())
sys.exit(0)
