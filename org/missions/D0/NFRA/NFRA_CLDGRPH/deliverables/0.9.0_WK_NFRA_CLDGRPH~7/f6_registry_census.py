#!/usr/bin/env python3
"""F6-AC5 instrument -- census the REGISTRY CARRIERS for the retired names.

The three carriers the order names, plus the generated mirror of the first:

    org/modules/graph/graph-call-manifest.yaml
    org/modules/graph/comp-tools.yaml
    org/modules/graph/TOOL_MASTER.yaml
    .tools/tool_index.py                     (generated FROM the manifest)

Two grains, both printed, because they answer different questions:

  TOTAL_MENTIONS      every line in those files matching kuzu_stitch_db|
                      kuzu_stitch_load, banded. This is the DENOMINATOR and it
                      is never suppressed.
  NEEDING_DISPOSITION the subset that R14/R15 leave open. R14 (PRD v0.6 s.6):
                      the retirement of a registry ENTRY is entry-grained --
                      `status: retired` on the entry. R15: a declared retired
                      RECORD (alias-name OR entry) is exempt, so an honest
                      historical record is never scored as an instruction.
                      A COMMENT that cites the call form is such a record.
                      A field of a LIVE entry that points a reader at the
                      retired artifact is NOT: it is a live instruction.

The yaml carriers are additionally LOADED (not grepped) to answer the R14
question directly: is there any ENTRY whose id/tool IS a retired name?

usage: f6_registry_census.py
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import os
import re
import sys

CARRIERS = [
    "org/modules/graph/graph-call-manifest.yaml",
    "org/modules/graph/comp-tools.yaml",
    "org/modules/graph/TOOL_MASTER.yaml",
    ".tools/tool_index.py",
]
NAMES = re.compile(r"(?<![A-Za-z0-9_])(kuzu_stitch_db|kuzu_stitch_load)(?![A-Za-z0-9_])")
COMMENT = re.compile(r"^\s*#")


def main() -> int:
    print("--- REGISTRY CARRIER CENSUS (R14 entry-grain / R15 record exemption) ---")
    print("CARRIERS (%d): %s" % (len(CARRIERS), ", ".join(CARRIERS)))
    total, needing = [], []
    for path in CARRIERS:
        if not os.path.exists(path):
            print("  MISSING CARRIER %s -- printed, not silently skipped" % path)
            continue
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        hits = [(i, ln) for i, ln in enumerate(lines, 1) if NAMES.search(ln)]
        print("  FILE %s  lines=%d  mentions=%d" % (path, len(lines), len(hits)))
        for i, ln in hits:
            if COMMENT.match(ln):
                band = "COMMENT/RECORD -- R15 exempt (cites the call form; not an instruction)"
                exempt = True
            elif "retired_aliases" in ln or "status: retired" in ln:
                band = "RETIRED-ALIAS -- R14/R15 declared"
                exempt = True
            else:
                band = "LIVE FIELD -- points a reader at the retired artifact; NEEDS DISPOSITION"
                exempt = False
            print("    %s:%d [%s]" % (path, i, band))
            print("        %s" % ln.strip()[:200])
            total.append((path, i))
            if not exempt:
                needing.append((path, i))

    print()
    print("--- R14 QUESTION, ANSWERED BY LOADING THE YAML (not by grep) ---")
    try:
        import yaml   # noqa: PLC0415
    except ImportError as ex:
        print("  YAML_LOAD=unavailable (%s) -- the entry-grain answer is UNMEASURED here" % ex)
    else:
        for path in CARRIERS[:3]:
            if not os.path.exists(path):
                continue
            try:
                doc = yaml.safe_load(open(path, encoding="utf-8"))
            except Exception as ex:                      # noqa: BLE001
                print("  %s LOAD FAILED: %s" % (path, ex))
                continue
            subjects = []

            def visit(node):
                if isinstance(node, dict):
                    for k in ("id", "tool", "name", "alias"):
                        v = node.get(k)
                        if isinstance(v, str) and NAMES.search(v):
                            subjects.append((k, v, node.get("status", "(no status key)")))
                    for v in node.values():
                        visit(v)
                elif isinstance(node, list):
                    for v in node:
                        visit(v)

            visit(doc)
            print("  %s -> ENTRIES WHOSE SUBJECT IS A RETIRED NAME: %d" % (path, len(subjects)))
            for k, v, st in subjects:
                print("      %s=%s status=%s" % (k, v, st))

    print()
    print("TOTAL_MENTIONS=%d across %d carrier(s)" % (len(total), len(CARRIERS)))
    print("MENTIONS_R15_EXEMPT=%d" % (len(total) - len(needing)))
    print("MENTIONS_NEEDING_DISPOSITION=%d" % len(needing))
    for path, i in needing:
        print("  NEEDS_DISPOSITION %s:%d" % (path, i))
    return 0


if __name__ == "__main__":
    sys.exit(main())
