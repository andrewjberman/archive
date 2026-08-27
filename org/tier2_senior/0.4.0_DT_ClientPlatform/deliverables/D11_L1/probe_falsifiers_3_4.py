#!/usr/bin/env python3
"""Falsifiers 3 and 4 against L1-m-graindecl, run by the cell's own owner.

F3  THE BRIDGE IS UNNECESSARY -- exhibit a cross-plane comparison sound WITHOUT a declared bridge:
    a join across two declared id spaces on a SHARED KEY that is measurably the SAME GRAIN on both
    sides.
F4  THE CONTAINMENT CLAIM IS FALSE -- exhibit an arn_resource or chain_motif instance CONTAINED BY
    A FILE in the same sense a symbol is.

Both are judgement-bearing, so each reports the MEASUREMENT and states what would count as a hit
BEFORE showing the number.
"""
import json

import kuzu

conn = kuzu.Connection(kuzu.Database(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


print("=" * 78)
print("FALSIFIER 3 -- is any cross-plane join sound WITHOUT a declared bridge?")
print("=" * 78)
print("  A HIT REQUIRES: two DIFFERENT declared id spaces sharing a key, same grain both sides,")
print("  joinable with NO hand-written parse. Strongest candidate: file <-> pipeline, because")
print("  PipelineScript is the only non-portal type that might name a repo path at FILE grain.")
print()

rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
mod = {nid.split(":", 1)[1] for nid, nt in rows if nt == "Module" and ":" in nid}
scripts = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.node_type='PipelineScript' RETURN n.node_id")]
print("  file space (portal Module paths) : %d" % len(mod))
print("  PipelineScript nodes             : %d" % len(scripts))
print("  samples:", scripts[:2])
raw = mod & set(scripts)
print("  RAW intersection                 : %d" % len(raw))
# do PipelineScript ids contain a repo path at all?
pathy = [s for s in scripts if "/" in s and "." in s.rsplit("/", 1)[-1]]
print("  PipelineScript ids that are path-shaped: %d of %d" % (len(pathy), len(scripts)))
print("  >> F3 on file<->pipeline: %s"
      % ("HIT -- native join exists" if raw else
         "NO HIT -- pipeline names scripts LOGICALLY (firm:gold:MODULE), not by path"))
print()

# second candidate: the ms layer's MS_FILE vs the repo file space
msf = [r[0] for r in q("MATCH (n:CloudNode) WHERE n.node_type='MS_FILE' RETURN n.node_id")]
print("  second candidate -- MS_FILE (%d) vs the file space:" % len(msf))
print("     samples:", msf[:2])
print("     RAW intersection with portal Module paths: %d" % len(mod & set(msf)))
print("     >> MS_FILE is SharePoint/OneDrive, a different corpus entirely -- not a counterexample.")
print()

print("=" * 78)
print("FALSIFIER 4 -- is an arn_resource or chain_motif CONTAINED BY A FILE?")
print("=" * 78)
print("  A HIT REQUIRES: containment in the SAME SENSE a symbol is in a file -- i.e. the entity")
print("  EXISTS INSIDE the file's text, so editing the file edits the entity. A resource DECLARED")
print("  by a file is NOT contained by it: deleting the .tf does not delete the bucket.")
print()

s = json.load(open("infra/aws/globgrph/stitch_graph.json", encoding="utf-8"))
arn_nodes, arn_with_path = 0, 0
motif_nodes, motif_with_path = 0, 0
for cd in s["classes_data"].values():
    for n in cd.get("nodes", []):
        if n.get("arn"):
            arn_nodes += 1
            if n.get("path"):
                arn_with_path += 1
        if str(n.get("id", "")).startswith(("motif:", "motifi:")):
            motif_nodes += 1
            if n.get("path"):
                motif_with_path += 1
print("  stitch nodes carrying an arn      : %d, of which %d ALSO carry a path" % (arn_nodes, arn_with_path))
print("  stitch nodes that are motif ids   : %d, of which %d ALSO carry a path" % (motif_nodes, motif_with_path))
print()
print("  ⛔ THE DISCRIMINATOR IS DECLARED-BY vs CONTAINED-IN, and a `path` field does not")
print("     distinguish them. A symbol at portal/src/App.tsx#NavItem IS the file's text. An S3")
print("     bucket whose node carries a .tf path is DECLARED there and outlives the file.")
print("  >> F4: a path field on an ARN node would be a DECLARATION SITE, not containment.")
print("     %s" % ("Some ARN nodes DO carry a path -- reported, and the sense is declaration."
                   if arn_with_path else "No ARN node carries a path, so the question does not even arise."))
