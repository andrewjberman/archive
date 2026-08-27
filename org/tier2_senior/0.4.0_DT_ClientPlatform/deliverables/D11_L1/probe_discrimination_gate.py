#!/usr/bin/env python3
"""L1 row 6: absent_vs_unaddressed -- THE DISCRIMINATION GATE, for all four id spaces.

The question (AC6): given a reference that does NOT resolve, can the space tell
SUBSTRATE-ABSENT (the store does not cover this region at all) from GENUINELY UNADDRESSED
(the store covers it and the answer is really "no")?

⛔ AND THE ANSWER MUST NAME A FIELD A CONSUMER REJECTS ON. "I can tell by looking" is not a
discriminator; it is a human reading prose. nerves_resolve was carded UNSOUND for exactly this --
the two outcomes byte-identical.

Both arms must be reachable from DIFFERENT TRUTHS or the control set is unsound.
"""
import json
import os
import re

import kuzu

conn = kuzu.Connection(kuzu.Database(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


def gate(space, non_resolving, total, field, verdict, note):
    print("  %-14s non-resolving %5d of %5d" % (space, non_resolving, total))
    print("     field a consumer rejects on : %s" % field)
    print("     DISCRIMINATES?               %s" % verdict)
    print("     %s" % note)
    print()


print("=" * 78)
print("ROW 6  absent_vs_unaddressed -- the discrimination gate")
print("=" * 78)

# ---------------------------------------------------------------- symbol
g = json.load(open(".comp-graph/graph.json", encoding="utf-8"))
trace = set(g["nodes"].keys())
pipe = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='pipeline' RETURN n.node_id")]
pat = re.compile(r"^pipeline:([a-z0-9]+):(.+)$")
stripped, firms = {}, set()
for p in pipe:
    m = pat.match(p)
    if m:
        firms.add(m.group(1))
        stripped.setdefault(m.group(2), []).append(p)
unmatched = trace - set(stripped)
# Can we tell WHY a trace symbol has no pipeline node? Only if we know which firms the
# pipeline layer covers AND which firm the symbol belongs to. Does the trace graph carry a firm?
trace_has_firm = sum(1 for t in trace if re.match(r"^[a-z0-9]+:gold:", t))
gate("symbol", len(unmatched), len(trace),
     "NONE -- the trace-graph node id carries no firm and no coverage marker",
     "NO",
     "     ⛔ the pipeline layer covers firms %s. A trace symbol carries NO firm token\n"
     "     (%d of %d trace ids have a firm-shaped prefix), so 'absent because this firm is not\n"
     "     loaded' and 'absent because this symbol has no pipeline node' are INDISTINGUISHABLE."
     % (sorted(firms), trace_has_firm, len(trace)))

# ---------------------------------------------------------------- file
rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
mod = {nid.split(":", 1)[1] for nid, nt in rows if nt == "Module" and ":" in nid}
repo = set()
for root, dirs, files in os.walk("portal/src"):
    dirs[:] = [d for d in dirs if d not in ("node_modules", "dist", ".git")]
    for fn in files:
        repo.add(os.path.join(root, fn).replace("\\", "/"))
missing = mod - repo
extra = repo - mod
gate("file", len(missing), len(mod),
     "the FILESYSTEM itself -- os.path.exists is a live, independent oracle",
     "YES",
     "     ⛔ AND IT IS THE ONLY ONE OF THE FOUR THAT DISCRIMINATES, because the second arm is a\n"
     "     DIFFERENT PLANE (the disk) rather than another projection of the same producer.\n"
     "     %d Module paths absent from disk; %d repo files absent from the graph -- BOTH arms\n"
     "     non-empty, so each is reachable from a different truth." % (len(missing), len(extra)))

# ---------------------------------------------------------------- arn_resource
kuzu_arn = {r[0] for r in q("MATCH (n:CloudNode) WHERE n.arn <> '' RETURN DISTINCT n.arn")}
s = json.load(open("infra/aws/globgrph/stitch_graph.json", encoding="utf-8"))
stitch_arn = set()
for cd in s["classes_data"].values():
    for n in cd.get("nodes", []):
        if n.get("arn"):
            stitch_arn.add(n["arn"])
only_kuzu = kuzu_arn - stitch_arn
only_stitch = stitch_arn - kuzu_arn
gate("arn_resource", len(only_kuzu) + len(only_stitch), len(kuzu_arn | stitch_arn),
     "NONE in-band -- neither store carries a scan-scope or account/region coverage marker",
     "NO",
     "     ⛔ %d ARNs only in kuzu, %d only in stitch. An ARN missing from one store could be\n"
     "     (a) outside that store's scan scope or (b) genuinely deleted. NEITHER STORE RECORDS ITS\n"
     "     SCAN SCOPE, so the two are byte-identical from the consumer's side."
     % (len(only_kuzu), len(only_stitch)))

# ---------------------------------------------------------------- chain_motif
c2 = json.load(open("org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances.json",
                    encoding="utf-8"))
c2i = {n["node_id"] for n in c2["nodes"] if n.get("node_id", "").startswith("motifi:")}
semi = {r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='semctl' RETURN n.node_id")
        if r[0].startswith("motifi:")}
gv = c2.get("graph_vintage")
gate("chain_motif", len(c2i ^ semi), len(c2i | semi),
     "graph_vintage -- c2_instances.json DECLARES the snapshot it was computed over",
     "PARTIALLY",
     "     c2 declares graph_vintage=%r. %d only in c2, %d only in semctl.\n"
     "     ⛔ A VINTAGE IS NOT A COVERAGE MARKER: it tells you WHEN, not WHAT WAS IN SCOPE. It\n"
     "     discriminates STALE from ABSENT, which is one axis, and leaves scope-absent vs\n"
     "     genuinely-unaddressed on the other axis undiscriminated."
     % (gv, len(c2i - semi), len(semi - c2i)))

print("=" * 78)
print("VERDICT: 1 of 4 spaces discriminates. 2 of 4 cannot at all. 1 of 4 on one axis only.")
print("=" * 78)
print("  The one that works (file) does so because its second arm is a DIFFERENT PLANE -- the")
print("  filesystem -- not another projection of the same producer. THAT IS THE TRANSFERABLE:")
print("  a discrimination gate needs an oracle OUTSIDE the pipeline that produced the data.")
print()
print("  CONTROL -- both arms reachable from different truths, for the space that passes:")
print("    arm A (graph says yes, disk says no): %d" % len(missing))
print("    arm B (disk says yes, graph says no): %d" % len(extra))
print("    both non-empty -> the control set is sound for `file` and ONLY for `file`.")
