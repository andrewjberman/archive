"""c12_route.py -- MX-c-10 AC2 instrument (ROUND_ANALYSIS.round11.md ruling 2): per-table discover routing for the
seven research tables (FWD-14's rule: a phrase reaches its table).

Usage: python c12_route.py <gateway dir>
For EACH research row in harvest_datasets (prefix under amgt/harvest/gold/research): every one of its example_questions,
asked of in-process discover as the Opal-internal principal, returns that row as its FIRST harvest_datasets match. A row
with no example question fails. Plus two issuer anchors that no worker wrote: "security analysis research dossier"
reaches a research dossier table first, and "research sector template passages" reaches research-sector-template
first. The denominator (rows, questions) is printed.
"""
import os
import sys

gw = os.path.abspath(sys.argv[1])
sys.path.insert(0, gw)
os.chdir(gw)
import yaml  # noqa: E402
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

doc = yaml.safe_load(open(os.path.join(gw, "app", "refs", "DATA_CATALOG.yaml"), encoding="ascii"))
rows = [r for r in (doc.get("harvest_datasets") or []) if str(r.get("prefix", "")).startswith("amgt/harvest/gold/research")]


def first_harvest(q):
    ms = od.discover(q, g.OPAL_INTERNAL).get("matches") or []
    h = [m.get("dataset") for m in ms if m.get("channel") == "harvest_datasets"]
    return h[0] if h else None


qs = ok = rows_ok = 0
for r in rows:
    eq = [str(q) for q in (r.get("example_questions") or []) if str(q).strip()]
    good_row = bool(eq)
    for q in eq:
        qs += 1
        got = first_harvest(q)
        hit = got == r.get("entity")
        ok += hit
        good_row = good_row and hit
        print("ROUTE %-34s %-60s first=%s %s" % (r.get("entity"), q[:60], got, "HIT" if hit else "MISS"))
    rows_ok += good_row
anchors = [("security analysis research dossier", {"harvest_research-dossier", "harvest_research_dossier"}),
           ("research sector template passages", {"harvest_research-sector-template"})]
a_ok = 0
for q, want in anchors:
    got = first_harvest(q)
    a_ok += got in want
    print("ANCHOR %-45s first=%s %s" % (q, got, "HIT" if got in want else "MISS"))
print("ROUTING research rows %d; rows reached by every own question %d of %d; questions %d of %d; anchors %d of %d"
      % (len(rows), rows_ok, len(rows), ok, qs, a_ok, len(anchors)))
sys.exit(0 if len(rows) == 7 and rows_ok == 7 and a_ok == len(anchors) else 1)
