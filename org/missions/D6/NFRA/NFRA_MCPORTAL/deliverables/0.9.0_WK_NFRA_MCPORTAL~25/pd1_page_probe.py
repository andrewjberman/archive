import app.server  # noqa: F401 side-effect import: registers the served integrations (row Z-S48)
import json
from app import admin_people as P, admin_gateway_breakdown as BD

# MP-pd-1 served page probe (run on the host over SSM, as ec2-user, from /opt/opal-gateway with its .venv).
# Reads the PAGE side only: the /api/admin/people rows that carry a data grant, with their data-grant tools,
# and the principal (tid, oid) keys the served scan returns. The store is read separately under the operator role.


def DATA(t):
    return t.startswith("schwab_") or t == "blackdiamond_list_fees"


OUT = {}
try:
    people = P._compute()["people"]
    real = [x for x in people if x["kind"] == "person" and "data grant revision" in x["how"]]
    OUT["page_rows_with_grant"] = len(real)
    OUT["page_rows"] = [{"who": x["who"], "how": x["how"],
                         "page_tools": sorted({t["name"] for c in x["channels"] for t in c["tools"] if DATA(t["name"])})}
                        for x in real]
    scanned = BD._scan_principals(BD._ddb_client())
    OUT["scan_denominator"] = len(scanned)
    OUT["scan_principals"] = [[tid, oid] for tid, oid in scanned]
except Exception as e:
    OUT["error"] = "%s: %s" % (type(e).__name__, e)
print("PD1PAGE " + json.dumps(OUT, sort_keys=True))
