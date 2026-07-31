#!/usr/bin/env python3
"""Reproducer for WS_E6_ITEM3_GATE_JUDGEMENT.md -- the measurement behind the item-3 GATED verdict.

Author: 0.7.0_AE_CloudOps~E. TO: NFRA_VELOCITY_ESTATE.WS-E6.harness-r4-trigger-binding.

WHY THIS SHIPS BESIDE THE JUDGEMENT: a gate recommendation resting on a chat message is not
reproducible. Run this to re-derive every figure in the report.

PREDICATE (printed at run time, never assumed by a reader):
  population  = ALL regular files under .tools/ named comp-*
  emitter     = the string "comp_log_auto" appears in that file's source
  A TEXT MATCH, so a file MENTIONING it without calling it counts as an emitter. The invisible
  count is therefore a FLOOR, never a ceiling. The error direction is conservative and deliberate.

READ-ONLY. Run from the workspace root (native Windows python cannot resolve /cygdrive paths).

NOTE ON DRIFT: the rail log is append-only and live, so counts move between runs. The RATIOS are
the durable claim; absolute counts are timestamped in the report for traceability, not frozen.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter

TOOL_VALUED = ("ROUTE-POSTERIOR", "ROUTE-POSTERIOR-DISAMBIG")
RAIL = os.path.join("org", "mcp", "comp-which-rail.log")
TOOLS = ".tools"


def classify_tools():
    """-> (emitters, non_emitters, style_counts). Source read, not sink inference."""
    emit, nonemit = set(), set()
    style = {"emit": Counter(), "nonemit": Counter()}
    for name in sorted(os.listdir(TOOLS)):
        path = os.path.join(TOOLS, name)
        if not name.startswith("comp-") or not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                src = fh.read()
        except Exception:
            src = ""
        first = src.split("\n", 1)[0] if src else ""
        kind = "python" if "python" in first else ("shell" if "sh" in first else "other")
        if "comp_log_auto" in src:
            emit.add(name)
            style["emit"][kind] += 1
        else:
            nonemit.add(name)
            style["nonemit"][kind] += 1
    return emit, nonemit, style


def main():
    if not os.path.isdir(TOOLS) or not os.path.exists(RAIL):
        sys.stderr.write("run from the workspace root (need .tools/ and %s)\n" % RAIL)
        return 2

    emit, nonemit, style = classify_tools()
    total = len(emit) + len(nonemit)

    print("=" * 74)
    print("WS-E6 ITEM 3 GATE MEASUREMENT")
    print("=" * 74)
    print("PREDICATE: all regular .tools/comp-* files; emitter = source contains comp_log_auto")
    print("           (text match -> the invisible count is a FLOOR, not a ceiling)")
    print()
    print("POPULATION : %d   EMIT: %d   NO-EMIT: %d" % (total, len(emit), len(nonemit)))
    print("  emitters    by style: %s" % dict(style["emit"]))
    print("  non-emitters by style: %s" % dict(style["nonemit"]))
    print("  -> invisibility tracks IMPLEMENTATION LANGUAGE, an axis orthogonal to path quality")
    print()

    all_vis = some_inv = all_inv = 0
    routes = 0
    inv_reco = Counter()
    unresolved = Counter()
    fam_of_all_inv = Counter()
    tool_re = re.compile(r"intent=(\S+)")

    with open(RAIL, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) < 2 or parts[1] not in TOOL_VALUED:
                continue
            m = tool_re.search(line)
            if not m:
                continue
            names = [n for n in m.group(1).split("+") if n]
            if not names:
                continue
            routes += 1
            vis = [n for n in names if n in emit]
            inv = [n for n in names if n in nonemit]
            for n in names:
                if n in nonemit:
                    inv_reco[n] += 1
                elif n not in emit:
                    unresolved[n] += 1      # recommended but not a comp-* file at all
            if inv and not vis:
                all_inv += 1
                fam_of_all_inv[parts[1]] += 1
            elif inv:
                some_inv += 1
            elif vis:
                all_vis += 1

    def pct(n):
        return (100.0 * n / routes) if routes else 0.0

    print("ROUTES (tool-valued families): %d" % routes)
    print("  ALL recommended VISIBLE      : %6d  (%.1f%%)" % (all_vis, pct(all_vis)))
    print("  SOME recommended invisible   : %6d  (%.1f%%)" % (some_inv, pct(some_inv)))
    print("  EVERY recommended INVISIBLE  : %6d  (%.1f%%)  <- UNCONVERTIBLE BY CONSTRUCTION"
          % (all_inv, pct(all_inv)))
    print("     family split (guards against counting category rows): %s" % dict(fam_of_all_inv))
    print("  ANY-of-N converts, so an all-invisible route can never register a conversion")
    print("  however perfectly the agent complied. Those paths are guaranteed to read as dead.")
    print()

    print("MOST-RECOMMENDED INVISIBLE TOOLS (each a permanently dead path):")
    for name, n in inv_reco.most_common(12):
        print("  %6d  %s" % (n, name))
    print()

    print("F6 -- RECOMMENDED NAMES THAT DO NOT RESOLVE TO ANY comp-* FILE:")
    if unresolved:
        for name, n in unresolved.most_common():
            here = "in .tools/" if os.path.exists(os.path.join(TOOLS, name)) else "ABSENT"
            print("  %6d  %-24s %s" % (n, name, here))
        print("  NOTE: `pipescript` is under a flat Andrew-direct prohibition (2026-07-29) and is")
        print("  a retired rc=2 stub per CLAUDE.md. Check its LAST-SEEN timestamp in the rail log")
        print("  before calling this historical -- it was recommended 2026-07-31T15:42:18Z.")
        print("  Run a POSITIVE CONTROL on a known-current token (e.g. comp-blast) so a stale-log")
        print("  artifact cannot masquerade as this finding.")
    else:
        print("  (none)")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
