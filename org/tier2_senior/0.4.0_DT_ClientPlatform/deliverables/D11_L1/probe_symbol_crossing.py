#!/usr/bin/env python3
"""L1-gqhb-1 / L1-gqhb-3: symbol id-space crossing property and roll-up cardinality.

Tests the hypothesis that kuzu_nessie_db's pipeline node_id is a PREFIXED form of the
trace-graph symbol id, i.e. that the two spaces are joinable only via a hand-written parse.
"""
import json
import re

import kuzu

DB = r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"
conn = kuzu.Connection(kuzu.Database(DB))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


pipe = [row[0] for row in q("MATCH (n:CloudNode) WHERE n.layer='pipeline' RETURN n.node_id")]
arns = [row[0] for row in q("MATCH (n:CloudNode) WHERE n.arn <> '' RETURN DISTINCT n.arn")]
g = json.load(open(".comp-graph/graph.json", encoding="utf-8"))
gnodes = set(g["nodes"].keys())

pat = re.compile(r"^pipeline:([a-z0-9]+):(.+)$")

print("=== HYPOTHESIS: kuzu pipeline node_id == 'pipeline:<firm>:' + trace-graph symbol id ===")
print("  raw join (no parse)      :", len(gnodes & set(pipe)), "of", len(gnodes), "trace-graph nodes")

stripped = {}
firms = set()
for p in pipe:
    m = pat.match(p)
    if m:
        firms.add(m.group(1))
        stripped.setdefault(m.group(2), []).append(p)

print("  kuzu pipeline ids matching the prefix pattern:", sum(len(v) for v in stripped.values()), "of", len(pipe))
print("  firm tokens observed:", sorted(firms))

inter = gnodes & set(stripped)
print()
print("  >> JOIN AFTER A HAND-WRITTEN PARSE: %d of %d trace-graph nodes (%.1f%%)"
      % (len(inter), len(gnodes), 100.0 * len(inter) / max(1, len(gnodes))))
print("     and %d of %d distinct stripped kuzu ids" % (len(inter), len(stripped)))

print()
print("  sample matched pairs:")
for k in list(inter)[:3]:
    print("    trace-graph : %s" % k)
    print("    kuzu        : %s" % stripped[k][:2])

print()
print("=== ROLL-UP CARDINALITY: is the mapping a FUNCTION or a RELATION? ===")
multi = {k: v for k, v in stripped.items() if len(v) > 1}
print("  stripped ids mapping to >1 kuzu node_id: %d of %d" % (len(multi), len(stripped)))
if multi:
    k = sorted(multi, key=lambda x: -len(multi[x]))[0]
    print("  MAX fan-out: %s -> %d targets" % (k, len(multi[k])))
    print("    targets:", multi[k][:4])

print()
print("=== NEGATIVE CONTROL -- the same parse against a set that must NOT match ===")
arn_hits = [a for a in arns if pat.match(a)]
print("  ARNs matching 'pipeline:<firm>:<rest>': %d of %d  -> %s"
      % (len(arn_hits), len(arns), "CONTROL HOLDS (0)" if not arn_hits else "*** CONTROL FAILED ***"))

print()
print("=== POSITIVE CONTROL -- the parse CAN produce a non-empty result ===")
print("  distinct stripped ids produced: %d -> %s"
      % (len(stripped), "parse is live" if stripped else "*** parse produced nothing ***"))
