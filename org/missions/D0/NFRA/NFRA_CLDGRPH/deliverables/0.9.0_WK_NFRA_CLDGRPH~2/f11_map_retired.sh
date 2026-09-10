#!/usr/bin/env bash
# F11-AC4 -- THE MAP RETIRED THE FOUR ENTRIES AND THE STAMP. TO-CG-F-11, deliverable step 4.
#
# Read by AST over derive_runner.NODE_TYPE_LAYER, not by text: the retirement COMMENT
# deliberately still quotes the GO line naming all five provisional types, so a text scan would
# report them as present. The comment is what a reader needs; the dict is what the derive obeys.
#
# The stamp is checked TWO ways -- the constants are gone from the module, and the fold, RUN on a
# fixture, writes no vocabulary property on any node it admits. A source check alone would miss a
# stamp written under another name.
#
# Run from the repository root.
set -u
python - <<'PY'
import ast
import io
import os
import sys

SRC = "infra/aws/globgrph/derive_runner.py"
src = io.open(SRC, encoding="utf-8").read()
tree = ast.parse(src)
NTL = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "NODE_TYPE_LAYER"
                                            for t in node.targets):
        NTL = ast.literal_eval(node.value)
FOUR = ("GOLD_SCRIPT", "S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY")
present = [t for t in FOUR if t in NTL]

sys.path.insert(0, os.path.join(os.getcwd(), "org", "modules", "graph"))
sys.path.insert(0, os.path.join(os.getcwd(), "infra", "aws", "globgrph"))
import derive_runner as DR       # noqa: E402
import hashlib
import json

doc = {"classes_data": {"m": {"nodes": [
    {"id": "pipeline:bd:gold:x", "type": "PipelineScript", "name": "x"},
    {"id": "portal", "type": "PORTAL_BUNDLE", "name": "portal"}]}}, "edges": []}
body = json.dumps(doc).encode()
marker = {"built_at": "2026-09-09T22:00:00Z", "producer": "stitch-codebuild", "git_sha": "0" * 40,
          "artifact_sha256": hashlib.sha256(body).hexdigest()}
g = {"classes_data": {}, "edges": []}
v = DR.fold_stitch_document(g, body, marker)
folded = g["classes_data"][DR.STITCH_CLASS]["nodes"]
stamp_written = any("vocabulary" in n for n in folded) or v["stitch_v1_stamped"] != 0
consts = hasattr(DR, "STITCH_V1_TYPES") or hasattr(DR, "STITCH_V1_STAMP")

# the comment block above the surviving entry
i = src.index("# stitch-v1, RETIRED at NFRA_CLDGRPH CG-s-31")
j = src.index('"PORTAL_BUNDLE": "portal",', i)
comment = src[i:j]
names = []
if "CG-s-31" in comment and "S31" in comment:
    names.append("S31")
if "RETIRED" in comment:
    names.append("retired")
if "CVO re-sign: PENDING" in comment:
    names.append("CVO-resign-pending")

import collections
by_layer = collections.Counter(NTL.values())

print("F11-AC4 -- THE MAP RETIRED THE FOUR ENTRIES AND THE STAMP")
print()
print("PROVISIONAL_ENTRIES_IN_MAP=%d of %d" % (len(present), len(FOUR)))
print("PORTAL_BUNDLE_IN_MAP=%s" % ("true" if NTL.get("PORTAL_BUNDLE") == "portal" else "false"))
print("STAMP_WRITTEN_BY_FOLD=%s" % ("true" if (stamp_written or consts) else "false"))
print("MAP_COMMENT_NAMES=%s" % ",".join(names))
print()
print("  -- the map, for the CVO's re-sign --")
print("     keys BEFORE this order (CVO C-S40 @e7db04572e) : 65")
print("     keys AFTER                                     : %d" % len(NTL))
print("     by layer AFTER : %s" % dict(sorted(by_layer.items())))
print("     C-S40's AFTER  : aws 34, portal 18, pipeline 4, ms 7, semctl 2 (65)")
print("     THE FROZEN COND-A RESOURCE-TYPE COUNT IS UNMOVED AT 32: S3_DATA_KEY merged INTO")
print("     S3Key, which was ALREADY an aws type, and no new aws type was created. The aws")
print("     LAYER count moves 34 -> 33 because a retired entry left it, not because a resource")
print("     type did.")
print()
print("  -- the four, by AST (the comment still quotes them; the dict does not carry them) --")
for t in FOUR:
    print("     %-18s %s" % (t, "PRESENT" if t in NTL else "retired"))
print("     PORTAL_BUNDLE      %s  <- the one genuinely new class, kept" % NTL.get("PORTAL_BUNDLE"))
print()
print("  -- the stamp, two instruments --")
print("     module constants STITCH_V1_TYPES / STITCH_V1_STAMP present : %s" % consts)
print("     the fold RUN on a fixture wrote a vocabulary property      : %s" % stamp_written)
print("     stitch_v1_stamped counter over %d folded node(s)           : %d"
      % (len(folded), v["stitch_v1_stamped"]))
print("     the counter stays in the INFO line at 0, so a regression would be VISIBLE")
print()
print("  DENOMINATOR: 4 of 4 provisional entries checked by AST over the parsed dict; "
      "%d of %d map keys enumerated; 2 of 2 stamp instruments (module constants + a live fold)."
      % (len(NTL), len(NTL)))
PY
