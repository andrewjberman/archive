#!/usr/bin/env python3
"""L1 row 3 groundwork + L1-m-graindecl evidence.

Before a canonical grain can be DECLARED it has to be shown that each space CAN roll up to the
candidate, and with what fan-out. AC5: "Roll-up fan-out cardinality recorded per space. Not one
collapses to a single target."

Every roll-up here is reported as a RELATION with its cardinality distribution. A single number
would be the exact collapse the TO forbids.
"""
import re
from collections import Counter, defaultdict

import kuzu

conn = kuzu.Connection(kuzu.Database(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


def rollup(name, pairs, declared):
    """pairs: iterable of (child, parent). Reports the RELATION, never a count."""
    m = defaultdict(set)
    for c, p in pairs:
        m[c].add(p)
    fan_out = Counter(len(v) for v in m.values())
    fan_in = Counter()
    for c, ps in m.items():
        for p in ps:
            fan_in[p] += 1
    print("  %-34s children %5d -> parents %5d" % (name, len(m), len(fan_in)))
    print("     fan-OUT (parents per child): %s" % dict(sorted(fan_out.items())))
    if fan_in:
        mx = max(fan_in.values())
        print("     fan-IN  (children per parent): max %d, mean %.2f"
              % (mx, sum(fan_in.values()) / len(fan_in)))
        heavy = fan_in.most_common(2)
        print("     heaviest: %s" % [(h[0][:46], h[1]) for h in heavy])
    print("     DECLARED BY THE STORE? %s" % declared)
    collapses = all(v == 1 for v in fan_in.values()) if fan_in else True
    print("     >> collapses to a single target? %s" % ("YES -- would be a function" if collapses else "NO -- it is a RELATION"))
    print()


print("=" * 78)
print("ROLL-UP CANDIDATES, per id space")
print("=" * 78)

# ---------------- symbol -> file
rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
URL = {"endpointurl", "endpoint"}
pairs = []
for nid, nt in rows:
    if nt == "Module" or ":" not in nid:
        continue
    pref, rest = nid.split(":", 1)
    if pref in URL:
        continue
    head = rest.split("#", 1)[0]
    # a file head may be followed by :LINE:name -- strip from the first ':' AFTER the extension
    mm = re.match(r"^([^:]+\.[A-Za-z0-9]+)(?::.*)?$", head)
    if mm:
        pairs.append((nid, mm.group(1)))
rollup("symbol -> file (portal)", pairs,
       "NO -- 0 of 16,811 portal edges target a Module; parse-only")

# ---------------- chain_motif instance -> family
sem = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='semctl' RETURN n.node_id")]
pairs = []
for nid in sem:
    if nid.startswith("motifi:"):
        parts = nid.split(":")
        if len(parts) >= 3:
            pairs.append((nid, "motif:" + parts[1]))
rollup("chain_motif instance -> family", pairs,
       "PARTIALLY -- the family id EXISTS as a node in the same store (19 of them)")

# ---------------- arn_resource -> service
arns = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.arn <> '' RETURN DISTINCT n.arn")]
pairs = []
for a in arns:
    m = re.match(r"^arn:aws:([^:]+):", a)
    pairs.append((a, "service:" + (m.group(1) if m else "NON_ARN")))
rollup("arn_resource -> service", pairs, "NO -- derived by parsing the ARN string")

# ---------------- pipeline symbol -> (firm, script)
pipe = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.layer='pipeline' RETURN n.node_id")]
pairs = []
for p in pipe:
    m = re.match(r"^pipeline:([a-z0-9]+):(.+)$", p)
    if m:
        pairs.append((p, "firm:" + m.group(1)))
rollup("pipeline symbol -> firm", pairs, "NO -- parse of the id prefix")

print("=" * 78)
print("⛔ THE GRAIN QUESTION THE DECLARATION MUST ANSWER")
print("=" * 78)
print("  Do the four spaces share ANY common parent grain?")
layers = q("MATCH (n:CloudNode) RETURN n.layer, count(*) ORDER BY n.layer")
print("  kuzu layers:", {r[0]: r[1] for r in layers})
print()
print("  symbol and file are in a CONTAINMENT relation (symbol is inside file).")
print("  arn_resource is a CLOUD RESOURCE -- not inside any file.")
print("  chain_motif instances span MEMBERS across planes (their props name shape_matched).")
print("  >> No single natural grain contains all four. The declaration must therefore name a")
print("     canonical grain AND the roll-up each space uses to reach it, or say it is per-plane.")
