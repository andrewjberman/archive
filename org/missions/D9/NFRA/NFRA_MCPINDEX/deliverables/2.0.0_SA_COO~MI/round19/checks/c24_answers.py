"""c24_answers.py <gateway root> -- prints, as JSON, what the gateway's discover answers for every silver_datasets row, per principal.

Run it under the gateway tree you want to measure (its OWN app/ code and its OWN app/refs/DATA_CATALOG.yaml). For every silver_datasets row it calls the
tree's `app.integrations.opal_discover.integration._silver_answer(loaded, row, principal_class, principal_firm)` for these principals: opal-internal, two
known firms, an unknown firm id. The output maps "<principal>|<entity>" to the answer dict (or null when the principal may not see the row). Read-only, no network."""
import json
import os
import sys

gw = os.path.abspath(sys.argv[1])
sys.path.insert(0, gw)
os.chdir(gw)
os.environ.setdefault("MOCK_GRAPH", "1")
from app.graphql_plumbing import catalog_gate  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

loaded = od._loaded()
rows = [r for r in (loaded["catalog"].get("silver_datasets") or []) if isinstance(r, dict) and r.get("entity")]
principals = [("opal-internal", catalog_gate.OPAL_INTERNAL, "")] + [("firm:" + f, "firm", f) for f in sorted(catalog_gate.KNOWN_FIRMS)[:2]] + [
    ("firm:nosuchfirm", "firm", "nosuchfirm")]
out = {"_rows": len(rows), "_principals": [p[0] for p in principals], "answers": {}, "errors": []}
for label, cls, firm in principals:
    for r in rows:
        try:
            out["answers"]["%s|%s" % (label, r["entity"])] = od._silver_answer(loaded, r, cls, firm)
        except Exception as exc:   # a crash is a defect, recorded, never a visible row
            out["errors"].append("%s %s %s" % (label, r["entity"], type(exc).__name__))
print(json.dumps(out, sort_keys=True, default=str))
