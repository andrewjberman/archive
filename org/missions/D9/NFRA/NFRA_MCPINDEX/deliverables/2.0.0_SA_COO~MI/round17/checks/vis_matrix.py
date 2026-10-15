"""vis_matrix.py <gateway root> -- prints, as JSON, which catalog rows (silver_datasets and portal_datasets entities) the gateway's discover shows to each principal.

Run it under the gateway tree you want to measure (its OWN app/ code and its OWN app/refs/DATA_CATALOG.yaml). For every silver_datasets row it calls the
tree's `app.integrations.opal_discover.integration._silver_answer(loaded, row, principal_class, principal_firm)` for these principals and records the entity
when the answer is not None: opal-internal; each KNOWN firm; an unknown firm id; an empty firm id. Read-only, no network."""
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
principals = [("opal-internal", catalog_gate.OPAL_INTERNAL, "")] + [("firm:" + f, "firm", f) for f in catalog_gate.KNOWN_FIRMS] + [
    ("firm:nosuchfirm", "firm", "nosuchfirm"), ("firm:", "firm", "")]
out = {"rows": len(rows), "firm_field": {r["entity"]: r.get("firm") for r in rows if "firm" in r}}
for label, cls, firm in principals:
    seen = []
    for r in rows:
        try:
            a = od._silver_answer(loaded, r, cls, firm)
        except Exception as exc:   # a crash is a defect, recorded, never a visible row
            out.setdefault("errors", []).append("%s %s %s" % (label, r["entity"], type(exc).__name__))
            continue
        if a is not None:
            seen.append(r["entity"])
    out[label] = sorted(seen)
print(json.dumps(out, sort_keys=True))
