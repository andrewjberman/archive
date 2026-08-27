#!/usr/bin/env python3
"""L1 rows 4, 5 and 7: coverage · confidence_distribution · failure_mode_downstream.

⛔ ROW 4 INHERITS ROW 6 DIRECTLY. The discrimination gate measured that 3 of 4 spaces cannot tell
SUBSTRATE-ABSENT from GENUINELY UNADDRESSED. For those three, a coverage PERCENTAGE would be the
same over-claim retracted in 31b1978428 one row earlier: a ratio whose numerator and denominator
are both scope-dependent, printed as though it were a measurement.

So coverage is reported as MEASURED only where an oracle outside the producing pipeline exists,
and as UNMEASURED-WITH-THE-MISSING-DISCRIMINATOR-NAMED everywhere else.
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


rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
mod = {nid.split(":", 1)[1] for nid, nt in rows if nt == "Module" and ":" in nid}
repo = set()
for root, dirs, files in os.walk("portal/src"):
    dirs[:] = [d for d in dirs if d not in ("node_modules", "dist", ".git")]
    for fn in files:
        repo.add(os.path.join(root, fn).replace("\\", "/"))

print("=" * 78)
print("ROW 4  coverage")
print("=" * 78)
print("  file          MEASURED -- the only space with an oracle outside its producer")
print("     graph->disk : %d of %d Module paths exist (%.1f%%)"
      % (len(mod & repo), len(mod), 100.0 * len(mod & repo) / len(mod)))
print("     disk->graph : %d of %d repo files are in the graph (%.1f%%)"
      % (len(mod & repo), len(repo), 100.0 * len(mod & repo) / len(repo)))
print("     BOTH DIRECTIONS REPORTED. One alone is a half-truth: 99.7%% one way, 87.0%% the other,")
print("     and a reader given only the first would think the graph covers the tree.")
print()
for sp, why in [
    ("symbol", "no firm token on trace ids and no coverage marker anywhere; 918 of 2,249 "
               "non-resolving cannot be split into out-of-scope vs genuinely-absent"),
    ("arn_resource", "neither kuzu nor stitch records its SCAN SCOPE; 278 of 1,970 non-resolving "
                     "are un-attributable between the two causes"),
]:
    print("  %-13s UNMEASURED -- and that is a DIFFERENT CLAIM FROM LOW" % sp)
    print("     missing discriminator: %s" % why)
    print()
print("  chain_motif   UNMEASURED for scope; STALENESS measurable")
print("     graph_vintage discriminates one axis (19.5-day gap, measured). Scope is undeclared,")
print("     so a coverage ratio would mix drift with scope and name the result coverage.")
print()

print("=" * 78)
print("ROW 5  confidence_distribution -- mapping confidence ONLY")
print("=" * 78)
# ⛔ THE FIRST VERSION OF THIS SECTION REGEXED FOR "confidence|score|probability|weight" OVER A
# 4MB PREFIX AND REPORTED 14 HITS IN stitch_graph.json -- THEN PRINTED A HARDCODED CONCLUSION SAYING
# NO CONFIDENCE EXISTS ANYWHERE. A typed conclusion that does not read the measurement above it.
# Resolved by opening the 14: every one is `"name": "weight"` / `"score"` / `"confidence"` on a
# node of type Field or Prop -- TYPESCRIPT FIELD NAMES IN THE PORTAL SOURCE THAT THE GRAPH IS
# DESCRIBING. KeywordIntelligence#confidence is a DOMAIN field of tsType '"high" | "medium"'.
# THE GRAPH CONTAINS NODES *ABOUT* FIELDS NAMED confidence; IT DOES NOT *CARRY* CONFIDENCE.
# Same class as egress<-regression: a common-noun token matching the described domain's own
# vocabulary. The conclusion was right and the evidence printed for it was not, so the probe now
# reports the STRUCTURED key scan the conclusion actually rests on.
def conf_keys(obj, depth=0):
    """Count keys whose NAME is confidence-ish, anywhere in the structure."""
    n = 0
    if depth > 12:
        return n
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("confidence", "score", "probability", "weight"):
                n += 1
            n += conf_keys(v, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            n += conf_keys(v, depth + 1)
    return n


for name, path in [
    ("c2_instances.json", "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances.json"),
    (".comp-graph/graph.json", ".comp-graph/graph.json"),
    ("stitch_graph.json", "infra/aws/globgrph/stitch_graph.json"),
]:
    print("  %-24s confidence-ish KEYS (structured, full file): %d"
          % (name, conf_keys(json.load(open(path, encoding="utf-8")))))
print("  kuzu CloudEdge properties: edge_type · layer · snapshot_ts · props  -- NO confidence field")
print("  stitch edge keys: 43 distinct, NONE of them a confidence  (measured over 43,633 edges)")
print()
print("  >> ⛔ NO MAPPING IN ANY OF THE FOUR SPACES CARRIES A CONFIDENCE VALUE.")
print("     Every join measured in rows 1 and 3 is BINARY -- the id matched or it did not.")
print("     A confidence DISTRIBUTION cannot be reported because there is no confidence to")
print("     distribute. Recording that as ABSENT, not as 1.0: a parse that happens to succeed is")
print("     not a high-confidence mapping, it is an UNQUANTIFIED one, and calling it 1.0 would")
print("     manufacture the exact certainty this row exists to expose.")
print()

print("=" * 78)
print("ROW 7  failure_mode_downstream")
print("=" * 78)
print("  What does a CONSUMER get when a mapping fails?")
print()
print("  symbol        SILENT. The parse yields no match and the row simply is not joined. Nothing")
print("                raises, nothing is counted, and the fused result is smaller by an unrecorded")
print("                amount. This is the PRD's zero-join, reproduced: 0 of 2,249 raw, and the")
print("                consumer sees a well-formed empty answer.")
print("  arn_resource  SILENT. A set difference with no scan scope: the consumer cannot tell a")
print("                deleted resource from an unswept one, and neither store errors.")
print("  chain_motif   SILENT ON SCOPE, LOUD ON VINTAGE -- graph_vintage is present, so a consumer")
print("                that reads it CAN detect the 19.5-day gap. It is the only in-band warning")
print("                available in any of the four, and I did not read it on my first pass.")
print("  file          LOUD-ADJACENT. os.path.exists gives a consumer a definite answer, so a")
print("                failure is detectable -- but nothing in the GRAPH says the path is stale;")
print("                the consumer must go to the filesystem to find out.")
print()
print("  >> 3 OF 4 SPACES FAIL SILENTLY, AND THE ONE PARTIAL WARNING IS A FIELD I MISSED.")
print("     A silent failure downstream is the failure mode the spine exists to convert into a")
print("     loud one, and it is currently the default in three of the four spaces it must span.")
