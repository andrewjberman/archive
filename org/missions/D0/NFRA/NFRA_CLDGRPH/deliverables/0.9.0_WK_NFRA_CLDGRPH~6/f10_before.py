"""THE BEFORE CENSUS -- run FIRST, against the tree AS HANDED OFF (NFRA_CLDGRPH.TO-CG-F-10 step 1).

Writes f10_baseline.json (the rc + stdout sha256 of each read-only subcommand, and the pre-change
rank/tuple/phrase counts) and prints f10_before.txt's content on stdout.

A before-census taken AFTER the edit is not a baseline. This script asserts nothing; it MEASURES.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f10_lib as L  # noqa: E402

print("=" * 96)
print("F-10 BEFORE CENSUS -- cell CG-s-30, worker 0.9.0_WK_NFRA_CLDGRPH~6")
print("worktree: %s" % L.WS)
print("=" * 96)

base = {"worktree": L.WS}

# ---- 1. comp-which over the four `when:` phrasings + the control ------------------------------
print("\n-- 1. comp-which RANKED LISTS (read from the SPILLED RANK FILE, never page 1) ----------")
rank = {}
for q in L.PHRASINGS + [L.CONTROL_PHRASING]:
    rc, out, path = L.comp_which(q)
    rows = L.rank_rows(path)
    hit = [i + 1 for i, t in enumerate(rows or []) if t == "comp-aws"]
    rank[q] = {"rc": rc, "rank_file": path, "tools_ranked": len(rows or []),
               "comp_aws_ranks": hit, "top3": (rows or [])[:3]}
    print("  Q: %s" % q)
    print("     rank_file=%s  tools_ranked=%d  comp-aws at rank(s)=%s  top3=%s"
          % (os.path.basename(path) if path else "(none)", len(rows or []), hit or "none",
             (rows or [])[:3]))
base["comp_which"] = rank
n_with = sum(1 for q in L.PHRASINGS if rank[q]["comp_aws_ranks"])
print("  BEFORE: comp-aws present in %d of %d phrasing ranked lists" % (n_with, len(L.PHRASINGS)))
print("  BEFORE: control %r top3=%s" % (L.CONTROL_PHRASING, rank[L.CONTROL_PHRASING]["top3"]))

# ---- 2. the curated vocabulary ----------------------------------------------------------------
print("\n-- 2. CURATED VOCABULARY in .tools/comp-which (the population the ranker walks) --------")
cur = L.curated_tuple_census()
base["curated"] = cur
print("  tuples_total=%d  tuples_naming_comp_aws=%d (lines %s)  code_lines_naming_comp_aws=%d (%s)"
      % (cur["tuples_total"], len(cur["tuples_naming_comp_aws"]), cur["tuples_naming_comp_aws"],
         len(cur["code_lines_naming_comp_aws"]), cur["code_lines_naming_comp_aws"]))

# ---- 3. the phrase domain ---------------------------------------------------------------------
print("\n-- 3. LAPTOP-PRODUCER PHRASE DOMAIN over the two registry files ------------------------")
ph = L.phrase_census()
base["phrases"] = ph
print("  PHRASE_DOMAIN=%d phrases" % len(L.PHRASE_DOMAIN))
for label, _ in L.PHRASE_DOMAIN:
    print("    %-42s scoped=%d  unscoped=%d" % (label, ph["scoped"][label], ph["unscoped"][label]))
print("  BEFORE scoped total=%d   unscoped total=%d   yaml_loads=%d of 2"
      % (sum(ph["scoped"].values()), sum(ph["unscoped"].values()), ph["yaml_loads"]))
for d in ph["detail"]:
    print("      %s" % d)
print("  COMP_AWS_KEYS_IN_COMP_TOOLS=%d" % L.comp_aws_keys_in_comp_tools())
base["comp_aws_keys"] = L.comp_aws_keys_in_comp_tools()

# ---- 4. the "as before" baseline: rc + stdout sha256 of each read-only subcommand --------------
print("\n-- 4. READ-ONLY SUBCOMMAND BASELINE (rc + stdout sha256, through the WRAPPER) ----------")
sub = {}
for argv in L.SUBCOMMANDS:
    key = " ".join(argv[:2])
    rc, out, err = L.run_wrapper(argv)
    sub[key] = {"argv": argv, "rc": rc, "stdout_sha256": L.sha256_of(out),
                "stdout_bytes": len(out), "stderr_bytes": len(err.encode("utf-8"))}
    print("  comp-aws %-28s rc=%d  stdout_bytes=%d  stdout_sha256=%s  stderr_bytes=%d"
          % (key, rc, len(out), L.sha256_of(out)[:32], len(err.encode("utf-8"))))
base["subcommands"] = sub

with open(L.BASELINE, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(base, indent=2, sort_keys=True, default=str) + "\n")
print("\nBASELINE WRITTEN: %s" % L.BASELINE)
print("BEFORE-CENSUS COMPLETE")
