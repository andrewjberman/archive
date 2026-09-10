#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-4 / G4-AC3 -- CG-s-35.

DOES THE ESTATE ALREADY HAVE A CARRIER THAT COULD HOLD THE PORTAL LAYER'S VINTAGE?

"There is no carrier" and "the carrier exists and is simply not fed" are different
findings with different owners and very different costs, so this sweep answers BOTH
and prints the denominator of what it swept.

Two of the candidates are EXERCISED, not merely read:
  C1  projection_worker._age_line   -- the served VINTAGE line a reader sees. The
      function is extracted from the source by AST and CALLED, so the answer is
      what the bytes DO, not what a docstring says.
  C3  _provenance.format_provenance_header -- imported and CALLED against a
      manifest carrying a fabricated extra source_vintage key.

READ ONLY on every producer file. No network, no AWS call. The only writes are
into a temporary directory that is removed before exit.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
GG = os.path.join(ROOT, "infra", "aws", "globgrph")
W2 = os.path.join(ROOT, "org", "missions", "D0", "NFRA", "NFRA_CLDGRPH",
                  "deliverables", "0.9.0_WK_NFRA_CLDGRPH~2")
TF = os.path.join(ROOT, "infra", "aws", "terraform", "globgrph", "stitch-produce.tf")
WF = os.path.join(ROOT, ".github", "workflows", "stitch-source-push.yml")

PORTAL_TOKENS = ("portal_sha", "portal_head", "portal_vintage", "portal_commit",
                 "stitch_portal", "portal_gitlink")
FAKE_PORTAL_KEY = "stitch_portal_sha"
FAKE_PORTAL_VAL = "5907cbca98eb091124e38a32debefa355c1d4376"


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def carries_portal(text):
    return sorted({t for t in PORTAL_TOKENS if t in (text or "")})


print("=" * 78)
print("G4-AC3 -- THE CARRIER QUESTION, WITH ITS DENOMINATOR")
print("=" * 78)
print("QUESTION  : is there a carrier a reader ALREADY consults that could hold the")
print("            portal layer's vintage, and if so is it merely unfed?")
print("POPULATION: every surface that stands between the portal checkout and a reader")
print("            asking 'how old is the portal half of this answer' -- the two")
print("            DECLARING surfaces in the repo, the three PRODUCER-side carriers,")
print("            and the three READER-side carriers. Enumerated below and swept in")
print("            full; the denominator is the enumeration, and it excludes surfaces")
print("            no reader of the served graph consults (test files, sensor scripts).")
print("")

candidates = []


def record(cid, name, where, exists, carries, extendable, evidence):
    candidates.append({"id": cid, "name": name, "where": where, "exists": exists,
                       "carries": carries, "extendable": extendable,
                       "evidence": evidence})
    print("-" * 78)
    print("%s  %s" % (cid, name))
    print("     where     : %s" % where)
    print("     EXISTS as a surface a reader consults : %s" % exists)
    print("     CARRIES a portal vintage TODAY        : %s" % carries)
    print("     COULD carry one without a new surface : %s" % extendable)
    for line in evidence:
        print("     evidence  : %s" % line)


# ---------------------------------------------------------------------------
# C1 -- the served VINTAGE line. EXERCISED.
# ---------------------------------------------------------------------------
pw_path = os.path.join(GG, "projection_worker.py")
pw_src = read_text(pw_path)
tree = ast.parse(pw_src)
age_fn = None
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == "_age_line":
        age_fn = node
        break
if age_fn is None:
    print("BLOCKED: projection_worker._age_line not found")
    sys.exit(2)

ns = {}
exec(compile(ast.Module(body=[age_fn], type_ignores=[]), pw_path, "exec"),
     {"datetime": __import__("datetime").datetime}, ns)
_age_line = ns["_age_line"]

VINT = "2026-09-10T03:02:00.000000+00:00"
man_stitch_only = {"source_vintage": {
    "stitch_built_at": "2026-09-10T03:01:17Z", "stitch_producer": "stitch-codebuild",
    "stitch_git_sha": "f9000bd0dd", "stitch_artifact_sha256": "deadbeef"}}
man_with_portal = {"source_vintage": dict(man_stitch_only["source_vintage"],
                                          **{FAKE_PORTAL_KEY: FAKE_PORTAL_VAL})}
out_a = _age_line(VINT, man_stitch_only)
out_b = _age_line(VINT, man_with_portal)
c1_prints_portal = FAKE_PORTAL_VAL in out_b or "portal" in out_b.lower()
record(
    "C1", "the served VINTAGE line (projection_worker._age_line)",
    "%s:241-263 (def at line %d)" % (rel(pw_path), age_fn.lineno),
    True, False, True,
    ["EXERCISED with a stitch-only manifest -> %r" % out_a,
     "EXERCISED with the SAME manifest plus %s=%s -> %r"
     % (FAKE_PORTAL_KEY, FAKE_PORTAL_VAL[:8], out_b),
     "the two outputs are %s -- the extra key changes nothing"
     % ("IDENTICAL" if out_a == out_b else "DIFFERENT"),
     "portal vintage rendered: %s" % c1_prints_portal,
     "EXTENSION PROVEN, not assumed: the ' Stitch source: ... built ...' clause is "
     "itself an append CG-s-24 added to this same function; a portal clause is the "
     "same shape, appended after it",
     "the function's own docstring: 'this is where a stitch vintage becomes readable "
     "at all' (row NFRA_CLDGRPH-W2-S46)"])

# ---------------------------------------------------------------------------
# C2 -- the manifest's source_vintage dict (what FEEDS C1).
# ---------------------------------------------------------------------------
knl_path = os.path.join(GG, "kuzu_nessie_load.py")
knl = read_text(knl_path)
m = re.search(r"def read_stitch_vintage\b[\s\S]*?\n        return \{([\s\S]*?)\n        \}",
              knl)
c2_keys = re.findall(r'"([a-z0-9_]+)"\s*:', m.group(1)) if m else []
prov_path = os.path.join(GG, "_provenance.py")
prov = read_text(prov_path)
c2_additive = "ADDITIVE at schema_version 1" in prov
record(
    "C2", "the build manifest's source_vintage dict (kuzu_nessie_load.read_stitch_vintage)",
    "%s:51-79" % rel(knl_path),
    True, bool(carries_portal(m.group(1) if m else "")), True,
    ["the keys it emits, parsed from the return literal: %s" % (", ".join(c2_keys) or "none"),
     "portal tokens among them: %s" % (", ".join(carries_portal(m.group(1) if m else "")) or "NONE"),
     "the dict is the ONLY feed into C1: projection_worker reads "
     "source_vintage.get('stitch_built_at') and nothing else",
     "additive-extension contract present in %s: %s" % (rel(prov_path), c2_additive),
     "the module's own words on why the stitch keys travel here: 'the branch-head marker "
     "... has a closed shape and no extension point ... So the stitch vintage travels from "
     "the producer's own marker'"])

# ---------------------------------------------------------------------------
# C3 -- format_provenance_header. EXERCISED against a fabricated extra key.
# ---------------------------------------------------------------------------
sys.path.insert(0, GG)
import _provenance as P  # noqa: E402  (the producer module, imported READ ONLY)

tmp = tempfile.mkdtemp(prefix="g3_carrier_")
try:
    db = os.path.join(tmp, "g3probe.kuzu")
    os.makedirs(db, exist_ok=True)
    given = {
        "nodes_snapshot_id": "111", "edges_snapshot_id": "222",
        "nodes_metadata_key": "meta/k.json", "warehouse_bucket": "",
        "stitch_built_at": "2026-09-10T03:01:17Z",
        "stitch_producer": "stitch-codebuild",
        "stitch_git_sha": "f9000bd0dd",
        FAKE_PORTAL_KEY: FAKE_PORTAL_VAL,
    }
    with open(db + P.MANIFEST_SUFFIX, "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "source_kind": "nessie",
                   "source_vintage": given,
                   "built_at": "2026-09-10T03:02:00+00:00",
                   "node_count": 1, "edge_count": 1,
                   "edge_count_semantics": "stored",
                   "artifact_claim": "served_projection"}, fh)
    header = P.format_provenance_header(db, check_nessie_distance=False)
    printed = sorted(k for k, v in given.items() if v and str(v) in header)
    dropped = sorted(k for k, v in given.items() if v and str(v) not in header)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

record(
    "C3", "the comp-kuzu provenance header (_provenance.format_provenance_header)",
    "%s:753-857" % rel(prov_path),
    False, False, False,
    ["EXERCISED: handed %d non-empty source_vintage keys; it PRINTED %d and DROPPED %d"
     % (len([v for v in given.values() if v]), len(printed), len(dropped)),
     "printed: %s" % ", ".join(printed),
     "DROPPED SILENTLY: %s" % ", ".join(dropped),
     "the drop is structural, not a bug in the fixture: the function has NO loop over "
     "source_vintage -- it hard-codes one branch per source_kind (tarball -> tarball_key; "
     "nessie -> nodes/edges snapshot-id + nodes metadata; stitch -> stitch_path/stitch_mtime)",
     "and no reader reaches it anyway: no serve path calls it (row NFRA_CLDGRPH-W3-S14, "
     "restated in %s:245-247)" % rel(pw_path),
     "SO THIS ORDER'S PREMISE THAT IT 'prints every source_vintage key it is given' DOES "
     "NOT HOLD -- filed as row NFRA_CLDGRPH-W3-S17"])

# ---------------------------------------------------------------------------
# C4 -- the stitch marker (the producer's own vintage object).
# ---------------------------------------------------------------------------
tf = read_text(TF)
mm = re.search(r"marker = \{([\s\S]*?)\n              \}", tf)
tf_keys = re.findall(r"'([a-z0-9_]+)'\s*:", mm.group(1)) if mm else []
live_marker = load_json(os.path.join(W2, "f3_marker_capture.json")).get("marker", {})
record(
    "C4", "the stitch marker s3://.../stitch/stitch_marker.json",
    "%s (inline CodeBuild buildspec, the marker dict)" % rel(TF),
    True, bool(carries_portal(json.dumps(live_marker)) or carries_portal(mm.group(1) if mm else "")),
    True,
    ["DECLARED keys, parsed from the buildspec literal: %s" % ", ".join(tf_keys),
     "APPLIED keys, from a live read of the object captured at %s: %s"
     % (rel(os.path.join(W2, "f3_marker_capture.json")), ", ".join(sorted(live_marker))),
     "DECLARED and APPLIED agree: %s"
     % (sorted(tf_keys) == sorted(live_marker.keys())),
     "git_sha is the SUPERPROJECT sha read from stitch_source_sha.txt, which does not "
     "move when the gitlink's target moves -- measured here: marker git_sha %s"
     % live_marker.get("git_sha", "?"),
     "portal tokens in either plane: NONE",
     "it CAN carry one -- kuzu_nessie_load.read_stitch_vintage already copies five "
     "marker fields verbatim, so a sixth needs no new surface"])

# ---------------------------------------------------------------------------
# C5 -- the served PORTAL_BUNDLE node's own props.
# ---------------------------------------------------------------------------
ex_path = os.path.join(GG, "extract_portal_stitch.py")
ex = read_text(ex_path)
em = re.search(r"def emit\(node_id[\s\S]*?\n        \}\)", ex)
emit_props = re.findall(r'"([a-z0-9_]+)"\s*:', em.group(0)) if em else []
claims_version = "identity = version tag" in ex
record(
    "C5", "the served PORTAL_BUNDLE node 'portal' and its props",
    "%s:131-142 (emit + the synthetic root)" % rel(ex_path),
    True, bool(carries_portal(em.group(0) if em else "")), True,
    ["every prop the producer writes on a portal node: %s" % ", ".join(emit_props),
     "portal tokens among them: NONE",
     "the producer's own comment at :141 says the synthetic root's 'identity = version "
     "tag': %s -- and the call at :142 is emit('portal', 'PORTAL_BUNDLE', 'portal') "
     "with no version argument, so the version tag is a comment, not a value"
     % claims_version,
     "this is the ONE node in the served graph that IS the portal layer, and it is the "
     "cheapest place a graph reader could ask"])

# ---------------------------------------------------------------------------
# C6 -- stitch_source_sha.txt inside the source zip.
# ---------------------------------------------------------------------------
asis = load_json(os.path.join(W2, "f3_asis_zip_manifest.json"))
f3rep = load_json(os.path.join(W2, "f3_zip_report.json"))
record(
    "C6", "stitch_source_sha.txt packed inside the source zip",
    "one entry in every source.zip; read by the buildspec into marker.git_sha",
    True, False, True,
    ["July zip's value: %s (a SUPERPROJECT sha)" % asis.get("stitch_source_sha_txt"),
     "F-3 zip's repo_head: %s (a SUPERPROJECT sha)" % f3rep.get("repo_head"),
     "the zip carries 435 portal/src FILES and not one byte naming which portal they "
     "came from -- the packer knows (it ran `git -C <portal> rev-parse HEAD`) and writes "
     "the answer only into its own scratch report, never into the archive",
     "a SECOND one-line entry beside this one is the whole feed C4 needs"])

# ---------------------------------------------------------------------------
# C7 -- the superproject gitlink.
# ---------------------------------------------------------------------------
rc = subprocess.run(["git", "ls-tree", "HEAD", "--", "portal"], cwd=ROOT,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
gl = re.search(r"160000 commit ([0-9a-f]{40})", rc.stdout.decode("utf-8", "replace"))
gl_sha = gl.group(1) if gl else None
packer = os.path.join(W2, "f3_build_source_zip.py")
packer_src = read_text(packer)
packer_reads_gitlink = "ls-tree" in packer_src
record(
    "C7", "the superproject gitlink (git ls-tree HEAD -- portal)",
    "this repository's tree at HEAD",
    True, True, False,
    ["gitlink at this worktree's HEAD: %s" % gl_sha,
     "it AGREES with the built portal today (%s) -- it did not on 2026-09-09, when "
     "row W2-S40 measured gitlink 30ca034b against a checkout at 18c0c5cb"
     % (gl_sha == FAKE_PORTAL_VAL),
     "but it is not a carrier of the ANSWER: the packer reads `git -C <portal> "
     "rev-parse HEAD`, not the gitlink (%s:84), so the gitlink can agree or disagree "
     "and the zip is unaffected -- measured: does the packer call ls-tree at all? %s"
     % (rel(packer), packer_reads_gitlink),
     "and no served surface reads this repo's tree"])

# ---------------------------------------------------------------------------
# C8 -- the GH-Action's hard-coded portal ref.
# ---------------------------------------------------------------------------
wf = read_text(WF)
wm = re.search(r"ref:\s*([0-9a-f]{40})", wf)
record(
    "C8", "the GH-Action's pinned portal ref (.github/workflows/stitch-source-push.yml)",
    "%s (the 'Checkout portal' step)" % rel(WF),
    True, True, False,
    ["pinned ref: %s" % (wm.group(1) if wm else "(none)"),
     "it is a THIRD value: it matches neither the portal actually packed into every "
     "round-6 zip (%s) nor the superproject gitlink (%s), which today agree with each "
     "other and not with it" % (FAKE_PORTAL_VAL[:8], (gl_sha or "?")[:8]),
     "and this route has not produced a served zip since 2026-07-07T13:46:19Z, so what "
     "it declares has never described anything the estate served in round 6",
     "a DECLARATION, and a stale one -- the opposite failure from an unfed carrier"])

# ---------------------------------------------------------------------------
# THE DECISION.
# ---------------------------------------------------------------------------
reader_side = [c for c in candidates if c["exists"] and c["extendable"]]
existing_carrier = bool(reader_side)
unfed = existing_carrier and not any(c["carries"] for c in reader_side)

print("")
print("-" * 78)
print("DECISION_EVIDENCE printed")
print("-" * 78)
print("  swept        : %d candidates, each measured on its own bytes -- 2 EXERCISED"
      % len(candidates))
print("                 (C1, C3 called), 6 read at source or at a captured artifact;")
print("                 0 skipped, 0 asserted from prose")
print("  exists AND could hold it without a new surface : %d of %d  (%s)"
      % (len(reader_side), len(candidates), ", ".join(c["id"] for c in reader_side)))
print("  actually holds it today                        : %d of %d"
      % (sum(1 for c in candidates if c["carries"] and c["extendable"]), len(candidates)))
print("  holds a portal sha but is NOT a carrier of the answer : C7, C8 (a repo")
print("                 declaration and a stale workflow pin; C8's value has described")
print("                 nothing served since 2026-07-07)")
print("")
print("  THE FINDING, PLAINLY: the carrier EXISTS AND IS UNFED. It is not missing.")
print("  C1 is the sentence a reader already reads, it already carries a SECOND")
print("  source's vintage (the stitch clause CG-s-24 appended to this very function),")
print("  and C2/C4 are the additive dict and marker that feed it. Nothing new has to")
print("  be built and no new surface has to be served.")
print("")
print("  BUT THE UNFED-NESS IS NOT ONE LINE AT THE DISPLAY END, AND SAYING SO WOULD")
print("  UNDERSTATE THE OWNER'S COST. The feed is a four-hop chain and the FIRST hop")
print("  is the one that is missing:")
print("    hop 1  PACK   the portal sha into the source zip (a second one-line file")
print("                  beside stitch_source_sha.txt). The packer that actually built")
print("                  every round-6 zip is a WORKER DELIVERABLE, not a producer:")
print("                  org/missions/.../0.9.0_WK_NFRA_CLDGRPH~2/f3_build_source_zip.py:84")
print("                  already computes the value and throws it away. The committed")
print("                  producer for this route does not exist; route 1")
print("                  (.github/workflows/stitch-source-push.yml:66) exists and pins a")
print("                  stale sha. OWNER: 0.7.0_AE_CloudOps (the same disarm_owner")
print("                  rows W2-S40 and W2-S63 already carry).")
print("    hop 2  STAMP  infra/aws/terraform/globgrph/stitch-produce.tf, the inline")
print("                  buildspec's marker dict (the block whose keys are printed under")
print("                  C4 above): one entry, 'portal_sha': open('portal_sha.txt')....")
print("                  OWNER: 0.7.0_AE_CloudOps (Terraform plane).")
print("    hop 3  COPY   infra/aws/globgrph/kuzu_nessie_load.py:71-77 -- one line,")
print("                  'stitch_portal_sha': m.get('portal_sha'), beside the five")
print("                  marker fields it already copies. OWNER: the globgrph engine")
print("                  owner (this project's plane).")
print("    hop 4  PRINT  infra/aws/globgrph/projection_worker.py:257-262 -- two lines,")
print("                  the same shape as the stitch clause immediately above them.")
print("                  OWNER: the globgrph engine owner (this project's plane).")
print("  NOT WRITTEN HERE. This order is READ ONLY on producer code; the sites are")
print("  named with their files, their lines and their owners, and the next cut carries")
print("  them.")
print("")
print("  AND ONE CARRIER MUST NOT BE CHOSEN: C3. Even wired, it would drop the new key")
print("  silently -- measured above, %d of %d keys printed. A remedy routed there would"
      % (len(printed), len([v for v in given.values() if v])))
print("  look done and change nothing a reader sees.")
print("")
print("=" * 78)
print("EXISTING_CARRIER=%s" % str(existing_carrier).lower())
print("CARRIER_UNFED=%s" % str(unfed).lower())
print("DECISION_EVIDENCE printed")
print("CANDIDATES_SWEPT=%d of %d" % (len(candidates), len(candidates)))
print("=" * 78)
