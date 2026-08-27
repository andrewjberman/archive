#!/usr/bin/env python3
"""L1 row 2: population_census for all four id spaces.

⛔ THE CENSUS IS A UNION WITH PER-SUBSTRATE DENOMINATORS, NOT A COUNT. Three of the four spaces
span more than one substrate, so a single integer would silently pick one plane and call it the
population -- the wrong-population shape this whole directive keeps measuring.

Every number here names the substrate it came from and the instrument that produced it.

⛔ CORRECTION AFTER ROW 6: the UNION deltas printed below are UNMEASURED, not population facts.
I published "+119" and "+48" as union deltas in msg 75002, then measured in row 6 that neither
arn_resource store records its scan scope and that the two chain_motif substrates are 19.5 days
apart in vintage -- AND DID NOT APPLY EITHER FINDING BACK TO MY OWN EARLIER CLAIM. 2.0.0_SA_COO~X
did that for me in 75057. Producing the falsifying measurement is not the same as applying it
backward, and nothing in my process made me revisit the earlier number.

WHAT STANDS: the EQUALITY result. PRD 1,851 == kuzu's arn count exactly; PRD 6,207 == semctl's
instance count exactly. Equality needs no scan scope and no shared vintage to hold.
"""
import json
import os

import kuzu

conn = kuzu.Connection(kuzu.Database(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


def report(space, prd, substrates):
    """substrates: list of (name, instrument, set)"""
    print("=" * 76)
    print("%s   PRD-claimed %s" % (space, prd))
    print("=" * 76)
    union = set()
    for name, instr, s in substrates:
        print("  %-34s %6d   [%s]" % (name, len(s), instr))
        union |= s
    print("  %-34s %6d" % ("UNION (distinct ids)", len(union)))
    if len(substrates) > 1:
        print("  pairwise overlaps:")
        for i in range(len(substrates)):
            for j in range(i + 1, len(substrates)):
                a, b = substrates[i], substrates[j]
                print("    %-22s n %-22s = %d" % (a[0][:22], b[0][:22], len(a[2] & b[2])))
    delta = len(union) - prd if isinstance(prd, int) else None
    if delta is not None:
        # ⛔ THE DELTA IS NOT A POPULATION FACT AND THIS PRINT USED TO IMPLY IT WAS.
        # Falsified by my OWN row-6 discrimination work (probe_discrimination_gate.py) and by
        # 2.0.0_SA_COO~X msg 75057, who applied it to the arn_resource delta before I did:
        #   arn_resource  neither kuzu nor stitch records its SCAN SCOPE, so "in one and not the
        #                 other" cannot be told from "the other never swept it"
        #   chain_motif   c2_instances declares graph_vintage 8601547680771488785 @2026-08-07 vs
        #                 kuzu 2902399899597701830 @2026-08-26 -- a 19.5-DAY CROSS-VINTAGE compare
        # A SET DIFFERENCE IS A CLAIM ABOUT TWO SCOPES, NOT A REMAINDER. The EQUALITY result
        # (PRD == exactly one substrate's count) is unaffected: it needs no scan scope to hold.
        print("  >> UNION vs PRD: %+d   ⛔ UNMEASURED, NOT A POPULATION DELTA" % delta)
        print("     (set difference across stores with no declared scan scope and/or")
        print("      differing vintages -- see probe_discrimination_gate.py)")
    print()
    return union


# ------------------------------------------------------------------ arn_resource
kuzu_arn = {r[0] for r in q("MATCH (n:CloudNode) WHERE n.arn <> '' RETURN DISTINCT n.arn")}
s = json.load(open("infra/aws/globgrph/stitch_graph.json", encoding="utf-8"))
stitch_arn, stitch_id = set(), set()
for cd in s["classes_data"].values():
    for n in cd.get("nodes", []):
        if n.get("arn"):
            stitch_arn.add(n["arn"])
        if n.get("id"):
            stitch_id.add(n["id"])
report("arn_resource", 1851, [
    ("kuzu_nessie_db.arn", "cypher DISTINCT n.arn", kuzu_arn),
    ("stitch_graph.json.arn", "json walk classes_data", stitch_arn),
])

# ------------------------------------------------------------------ chain_motif
c2 = json.load(open("org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances.json",
                    encoding="utf-8"))
# ⛔ THE KEY IS node_id, NOT id. My first census took n["id"] and returned a SILENT ZERO for a
# substrate I had measured at 6,161 ten minutes earlier. Caught only by disagreeing with my own
# prior number. AND THE GRAIN MUST BE SPLIT: motif:<family> and motifi:<family>:<hash> are TWO
# grains sharing a prefix, and my first crossing figure of 6,113 mixed them -- in the id space
# whose entire purpose is grain.
_c2_all = {n["node_id"] for n in c2.get("nodes", []) if isinstance(n, dict) and n.get("node_id")}
c2_ids = {x for x in _c2_all if x.startswith("motifi:")}
semctl = {r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='semctl' RETURN n.node_id")
                 if r[0].startswith("motifi:")}   # INSTANCE grain only, per the split above
report("chain_motif", 6207, [
    ("c2_instances.json INSTANCE grain", "json nodes[].node_id, motifi: only", c2_ids),
    ("kuzu semctl INSTANCE grain", "cypher layer=semctl, motifi: only", semctl),
])

# ------------------------------------------------------------------ symbol
g = json.load(open(".comp-graph/graph.json", encoding="utf-8"))
trace = set(g["nodes"].keys())
portal_rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
FILE_TYPES = {"Module"}
portal_sym = {nid for nid, nt in portal_rows if nt not in FILE_TYPES}
pipeline = {r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='pipeline' RETURN n.node_id")}
report("symbol", 19482, [
    (".comp-graph/graph.json nodes", "json keys", trace),
    ("kuzu portal non-Module nodes", "cypher layer='portal' type<>Module", portal_sym),
    ("kuzu pipeline nodes", "cypher layer='pipeline'", pipeline),
])

# ------------------------------------------------------------------ file
mod = {nid.split(":", 1)[1] for nid, nt in portal_rows if nt == "Module" and ":" in nid}
repo = set()
for root, dirs, files in os.walk("portal/src"):
    dirs[:] = [d for d in dirs if d not in ("node_modules", "dist", ".git")]
    for fn in files:
        repo.add(os.path.join(root, fn).replace("\\", "/"))
report("file", 3532, [
    ("kuzu portal Module (declared)", "cypher node_type='Module'", mod),
    ("portal/src filesystem", "os.walk", repo),
])

print("=" * 76)
print("⛔ THE FILE SPACE IS THE ONE I CANNOT CLOSE FROM HERE")
print("=" * 76)
print("  The PRD's 3,532 is the CO-CHANGE corpus -- git history over the whole workspace, not the")
print("  portal component tree. Neither substrate above is that corpus. Reporting 374 or 429 as")
print("  'the file population' would be a well-formed answer about the wrong object, which is the")
print("  exact failure `space_is_crossing` exists to prevent one row earlier.")
cc = os.path.exists(".tools/comp-cochange")
print("  comp-cochange present on disk: %s -- an instrument exists; its CORPUS is not yet located." % cc)
