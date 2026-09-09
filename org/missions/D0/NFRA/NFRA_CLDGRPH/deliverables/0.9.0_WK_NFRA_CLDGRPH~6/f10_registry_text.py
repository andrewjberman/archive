"""F10-AC4 -- NO AGENT-FACING TEXT DESCRIBES A LAPTOP AS A PRODUCER.

THE DOMAIN IS DECLARED, NOT DISCOVERED (TAXONOMY LAW i -- hunt the uncovered member): the seven
phrases are the issuer's, printed in full below with their per-phrase counts, over the two registry
files org/modules/graph/comp-tools.yaml and org/modules/graph/comp-aws-agent-usage.yaml.

TWO READS, BOTH PRINTED (CLAUDE.md Rule 22 -- one UNSCOPED read after a scoped pass):
  SCOPED    every scalar reachable under an agent-facing key, at any depth, in the parsed YAML.
  UNSCOPED  the same regexes over the RAW BYTES of both files, comments included. A scoped census
            cannot see a phrase in a YAML comment, and the criterion's number is the scoped one --
            so the unscoped number is printed beside it rather than left unmeasured.

THE CONTROL: a planted phrasing is injected into an in-memory copy of each file and must be CAUGHT.
A censor that cannot return non-zero on a positive is a constant wearing a measurement's clothes.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f10_lib as L  # noqa: E402

print("F10-AC4 -- no agent-facing text describes a laptop as a producer")
print("")
print("  FILES (%d):" % len(L.REGISTRY_FILES))
for p in L.REGISTRY_FILES:
    print("    %s" % os.path.relpath(p, L.WS).replace(os.sep, "/"))
print("  AGENT-FACING FIELD SET (%d): %s" % (len(L.AGENT_FACING_FIELDS),
                                             ", ".join(L.AGENT_FACING_FIELDS)))
print("")

ph = L.phrase_census()
print("  %-44s scoped  unscoped" % "PHRASE (the declared domain)")
for label, rx in L.PHRASE_DOMAIN:
    print("    %-42s %-7d %-d" % (label, ph["scoped"][label], ph["unscoped"][label]))
scoped_total = sum(ph["scoped"].values())
unscoped_total = sum(ph["unscoped"].values())
print("")
for d in ph["detail"]:
    print("      %s" % d)
if not ph["detail"]:
    print("      (no hit in either read)")
print("")

keys = L.comp_aws_keys_in_comp_tools()

# ---- the planted control ----------------------------------------------------------------------
planted = "  output: \"Typed cloud graph -> .comp-graph; snapshot tarballs -> opal-313476888478-globgrph\"\n"
caught = 0
for path in L.REGISTRY_FILES:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        mutated = fh.read() + planted
    n = sum(len(re.findall(rx, mutated)) for _, rx in L.PHRASE_DOMAIN)
    base = sum(len(re.findall(rx, mutated[:len(mutated) - len(planted)]))
               for _, rx in L.PHRASE_DOMAIN)
    if n > base:
        caught += 1
print("  PLANTED CONTROL: a laptop-producer `output:` line appended to an IN-MEMORY copy of each")
print("  file is caught in %d of %d files (delta > 0 against the same file unplanted)."
      % (caught, len(L.REGISTRY_FILES)))
print("")

print("PHRASE_DOMAIN=%d phrases" % len(L.PHRASE_DOMAIN))
print("LAPTOP_PRODUCER_PHRASINGS=%d of %d" % (scoped_total, len(L.PHRASE_DOMAIN)))
print("UNSCOPED_READ=%d hit(s) over the raw bytes of both files (comments included)" % unscoped_total)
print("COMP_AWS_KEYS_IN_COMP_TOOLS=%d" % keys)
print("YAML_LOADS=%d of %d" % (ph["yaml_loads"], len(L.REGISTRY_FILES)))
print("PHRASE_PROBE_CONTROL=%s" % ("FIRED" if caught == len(L.REGISTRY_FILES) else "DID-NOT-FIRE"))

ok = (scoped_total == 0 and unscoped_total == 0 and keys == 1
      and ph["yaml_loads"] == len(L.REGISTRY_FILES) and caught == len(L.REGISTRY_FILES))
print("RC=%d" % (0 if ok else 1))
sys.exit(0 if ok else 1)
