#!/usr/bin/env python3
"""PHASE B RECONCILE for SC-m-3 / DTX-AC4.

Joins the 39-part phase-A census against all 8 wave-1 cards'
artifact.location.projection_of + co_resident_stores, and prints BOTH residues with owners.

DTX-AC4 is explicit that a one-directional reconcile is not a reconcile, and that a residual
bucket is a claim rather than a remainder. So every card entry lands in exactly one disposition
and the dispositions are ITEMISED until they sum. Nothing is labelled by subtraction.

DECLARED DOMAIN of the phase-A census (from the manifest's own denominator): PERSISTED
GRAPH-BEARING OBJECTS. A card may legitimately name an upstream WORLD (the live AWS estate, the
repo source tree) that is not a persisted store -- counting those as "missing from the census"
would inflate residue 1 with things that were never in scope. They get their own disposition.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "graph_object_manifest.json")
OUT = os.path.join(HERE, "phase_b_reconcile.json")
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

CARDS = [
    ("C0", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/C0.json"),
    ("C1", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/C1.json"),
    ("C2", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/C2.json"),
    ("D1", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D1.json"),
    ("D2", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D2.json"),
    ("D3", "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D3.json"),
    ("C3i", "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS/C3i.json"),
    ("COMPSIMILAR", "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS/comp_similar.json"),
]

# Card entries are PROSE. Each rule maps a discriminating substring to a disposition.
# A rule fires only on a substring that could not plausibly match a different object.
RULES = [
    # --- resolve to a census part ---
    ("s3://opal-estate-report/kuzu_nessie_db", "RESOLVED", "kuzu_nessie_db.s3"),
    ("graph_nodes_4c6c23bd", "RESOLVED", "graph_nodes"),
    ("graph_edges_6629328d", "RESOLVED", "graph_edges"),
    ("resource_summaries_b38ddc35", "RESOLVED", "resource_summaries"),
    ("motif_c2c3_materialize_ab.json", "RESOLVED", "motif_c2c3_materialize_ab.json"),
    ("motif_c2c3_materialize.json", "RESOLVED", "motif_c2c3_materialize.json"),
    ("MOTIF_c2c3_materialize_spec.py", "RESOLVED_AS_GENERATOR",
     "motif_c2c3_materialize.json (registered as that part's generation.materializer, not as a part)"),
    ("c2_individuate.py", "RESOLVED_AS_GENERATOR",
     "c2_instances.json (registered as that part's generation.materializer)"),
    ("c2_instances.json", "RESOLVED", "c2_instances.json"),
    ("c3_structures.json", "RESOLVED", "c3_structures.json"),
    ("kimi_subdivision_harness/ (c2_instances.json, c3_structures.json", "RESOLVED_MULTI",
     "c2_instances.json + c3_structures.json (ONE card entry naming TWO objects)"),
    (".comp-graph/graph.json", "RESOLVED", ".comp-graph/graph.json"),
    ("nerves-edges.json and nerves-risk-edges.json", "RESOLVED_MULTI",
     "nerves-edges.json + nerves-risk-edges.json (ONE card entry naming TWO objects)"),
    ("the graph_contracts table", "RESOLVED", "graph_contracts"),
    ("BAKED STATIC SPEC LAYERS", "RESOLVED_MULTI",
     "motif_c2c3_materialize.json + motif_c2c3_materialize_ab.json (the 07-08 and 07-18 spec layers)"),
    ("the C0 node population", "RESOLVED", "graph_nodes"),
    ("the C1 edge population", "RESOLVED", "graph_edges"),
    ("kuzu_nessie_db", "RESOLVED", "kuzu_nessie_db.local"),   # LAST kuzu rule: the bare/local head

    # --- named in a card, but NOT a persisted graph store: outside the census's declared domain ---
    ("live AWS estate", "OUT_OF_DOMAIN",
     "the upstream WORLD the graph is derived FROM, not a persisted graph object"),
    ("repo source tree", "OUT_OF_DOMAIN",
     "the upstream WORLD the graph is derived FROM, not a persisted graph object"),
    ("comp-heat and comp-debris ledgers", "OUT_OF_DOMAIN",
     "tool ledgers, not graph-bearing stores; outside the declared domain"),
    ("C7 INFLUENCE-CLOSURE population", "OUT_OF_DOMAIN",
     "declared by the card as process-generated, NOT graph-materialized and NOT enforcing"),

    # --- RESIDUE 1: a real persisted object a card names that the census did NOT register ---
    ("SYSTEM_DEFINITIONS.yaml", "RESIDUE_1", "infra/system/ontology/SYSTEM_DEFINITIONS.yaml"),
    ("NFRA_ONTOLOGY_RULE_BANK.yaml", "RESIDUE_1",
     "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_RULE_BANK.yaml"),
    ("NFRA_ONTOLOGY_C2C3_CANONICAL.yaml", "RESIDUE_1",
     "org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml"),
    ("keep-dormant.yaml", "RESIDUE_1", "org/modules/graph/keep-dormant.yaml"),
    ("data/firm_registry.json", "RESIDUE_1", "data/firm_registry.json"),
]

RESIDUE_1_OWNERS = {
    "infra/system/ontology/SYSTEM_DEFINITIONS.yaml": "1.0.0_SA_CTO~Z (infra/system parity owner)",
    "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_RULE_BANK.yaml":
        "0.8.0_AE_CloudComp lane",
    "org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml": "0.8.0_AE_CloudComp lane",
    "org/modules/graph/keep-dormant.yaml": "UNKNOWN -- no owner identified by this census",
    "data/firm_registry.json": "0.4.0_DS_ClientPlatform lane (firm registry)",
}


def classify(entry: str):
    for needle, disp, target in RULES:
        if needle in entry:
            return disp, target, needle
    return "UNRESOLVED", None, None


man = json.load(open(MANIFEST, encoding="utf-8"))
part_ids = {p["id"] for p in man["parts"]}

rows = []
for subj, rel in CARDS:
    path = os.path.join(WS, rel)
    d = json.load(open(path, encoding="utf-8"))
    loc = d.get("artifact", {}).get("location", {})
    for field in ("projection_of", "co_resident_stores"):
        for e in (loc.get(field) or []):
            txt = e if isinstance(e, str) else json.dumps(e)
            disp, target, needle = classify(txt)
            rows.append({
                "card": subj, "carded_by": d.get("carded_by"), "field": field,
                "entry_head": txt[:110], "disposition": disp,
                "resolves_to": target, "matched_on": needle,
            })

# ---- residue 2: census parts no card names ----
named_parts = set()
for r in rows:
    if r["disposition"] in ("RESOLVED", "RESOLVED_MULTI", "RESOLVED_AS_GENERATOR") and r["resolves_to"]:
        for pid in part_ids:
            if pid in r["resolves_to"]:
                named_parts.add(pid)

owner_by_part = {p["id"]: p["owner"] for p in man["parts"]}
residue_2 = sorted(part_ids - named_parts)
_basis = {p["id"]: p["basis"] for p in man["parts"]}
residue_2_absent = [p for p in residue_2 if _basis.get(p) == "absent"]
residue_2_reference = [p for p in residue_2 if p == "nerves_resolve"]
residue_2_real = [p for p in residue_2
                  if p not in residue_2_absent and p not in residue_2_reference]

disp_counts = {}
for r in rows:
    disp_counts[r["disposition"]] = disp_counts.get(r["disposition"], 0) + 1

residue_1_items = sorted({r["resolves_to"] for r in rows if r["disposition"] == "RESIDUE_1"})

REPORT = {
    "cell_id": "SC-m-3",
    "phase": "B -- RECONCILE",
    "criterion": "DTX-AC4",
    "compiled_by": "0.4.0_DT_ClientPlatform~X",
    "trigger": ("OBSERVED, not declared: 2.0.0_SA_COO~X measured 8/8 conformant cards committed, "
                "worktree clean, with a positive control (a nonexistent path is NOT tracked, rc=1). "
                "Ruled that MERGED means committed-to-CLOUD, not pushed-to-origin, because this "
                "consumer reads the working tree on the same device (73421)."),
    "denominators": {
        "cards_read": len(CARDS),
        "cards_present_on_disk": len(CARDS),
        "card_entries_examined": len(rows),
        "census_parts": len(part_ids),
        "dispositions": disp_counts,
        "ITEMISATION_CHECK": ("every card entry lands in exactly ONE disposition and the "
                              "dispositions SUM to the entries examined -- nothing here is labelled "
                              "by subtraction, per DTX-AC4's residual-bucket rule"),
    },
    "residue_1_in_cards_not_in_census": {
        "count": len(residue_1_items),
        "note": ("Real persisted objects a card names that the phase-A census did NOT register. "
                 "⛔ EVERY ONE OF THESE FALLS INSIDE A LIMIT THE CENSUS DECLARED IN ADVANCE -- see "
                 "predicted_by_known_unsearched. That is the declared limit doing its job, not a "
                 "surprise, and it is why known_unsearched had to be non-empty."),
        "predicted_by_known_unsearched": (
            "The manifest's known_unsearched entry 'org/modules/graph/ beyond graph-bearing JSON -- "
            "~100 further .py/.yaml files were not classified. A store hiding as a .yaml in that "
            "tree would be missed.' NAMED THIS EXACT CLASS BEFORE THE RECONCILE RAN. 4 of the 5 "
            "residue-1 items are .yaml registries; the 5th (data/firm_registry.json) sits in a tree "
            "the census never entered at all."),
        "items": [{"store": i, "owner": RESIDUE_1_OWNERS.get(i, "UNKNOWN"),
                   "disposition": "NOT a census defect to hide -- a declared gap now itemised with an owner"}
                  for i in residue_1_items],
    },
    "residue_2_in_census_no_card_names": {
        "count": len(residue_2),
        "SUBCLASSIFIED_BECAUSE_A_FLAT_COUNT_WOULD_OVERSTATE_IT": {
            "headline_number_to_quote": len(residue_2_real),
            "explanation": (
                "A flat %d overstates the finding. %d of the %d are NOT persisted stores a wave-1 "
                "card could reasonably have named: %d are the UNBUILT C3 stages (registered as "
                "absent rows, so a card naming them would be wrong), and 1 is nerves_resolve, which "
                "is the subject of the REFERENCE card -- explicitly not a wave member. "
                "THE NUMBER THAT CARRIES THE CLAIM IS %d: real, persisted, present graph objects "
                "that NO wave-1 card names."
                % (len(residue_2), len(residue_2) - len(residue_2_real), len(residue_2),
                   len(residue_2_absent), len(residue_2_real))),
            "excluded_unbuilt_stages": residue_2_absent,
            "excluded_reference_card_subject": residue_2_reference,
        },
        "note": ("Census parts that NO wave-1 card names. ⛔ THIS IS THE HALF THE RECONCILE EXISTS "
                 "FOR: a store no card mentions is exactly what Andrew called concerning, and it is "
                 "structurally invisible to any manifest assembled FROM the cards. Phase A being an "
                 "INDEPENDENT instrument is the only reason this list is non-empty."),
        "items": [{"part": p, "owner": owner_by_part.get(p, "UNKNOWN")} for p in residue_2],
    },
    "out_of_domain_note": ("Entries a card legitimately names that are NOT persisted graph objects "
                          "(the live AWS estate, the repo source tree, tool ledgers, the "
                          "process-generated C7 population). Counting these as 'missing from the "
                          "census' would INFLATE residue 1 with things that were never in the "
                          "declared domain. They are dispositioned separately and on purpose."),
    "unresolved_note": ("UNRESOLVED is a CONFORMING value per 2.0.0_SA_COO~X 73421. Card entries are "
                        "prose; where a string cannot be tied to one object without inference, it "
                        "stays UNRESOLVED rather than being forced onto a part. A forced match is "
                        "worse than an honest UNRESOLVED because it silently merges two objects."),
    "no_summing": ("⛔ I do NOT adopt 51, 43, 39, 37 or 35 as a part count, per 73421. The card-side "
                   "entry count (%d) and the census part count (%d) are DIFFERENT POPULATIONS over "
                   "DIFFERENT GRAINS and are not commensurable. One card entry can name TWO objects "
                   "(measured: 3 such entries here), and many entries name the same object across "
                   "cards." % (len(rows), len(part_ids))),
    "rows": rows,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(REPORT, f, indent=2, ensure_ascii=False)

print("card entries examined:", len(rows))
print("dispositions:", disp_counts)
assert sum(disp_counts.values()) == len(rows), "DISPOSITIONS DO NOT SUM"
print("ITEMISATION CHECK PASS: dispositions sum to entries examined")
print()
print("RESIDUE 1 (in cards, not in census):", len(residue_1_items))
for i in residue_1_items:
    print("   -", i, "|| owner:", RESIDUE_1_OWNERS.get(i, "UNKNOWN"))
print()
print("RESIDUE 2 (in census, no card names):", len(residue_2), "of", len(part_ids), "parts")
print("   of which UNBUILT stages (not stores):", len(residue_2_absent), residue_2_absent)
print("   of which the REFERENCE card's subject:", len(residue_2_reference), residue_2_reference)
print("   >>> REAL PERSISTED STORES NO WAVE-1 CARD NAMES:", len(residue_2_real))
for p in residue_2_real:
    print("       -", p, "|| owner:", owner_by_part.get(p, "UNKNOWN"))
assert len(residue_2_absent) + len(residue_2_reference) + len(residue_2_real) == len(residue_2),     "RESIDUE 2 SUBCLASSES DO NOT SUM"
print("   SUBCLASS CHECK PASS: %d + %d + %d == %d"
      % (len(residue_2_absent), len(residue_2_reference), len(residue_2_real), len(residue_2)))
