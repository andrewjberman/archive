#!/usr/bin/env python3
"""I2-AC2 -- WHO DEPENDS ON `aws_keys` BEING SNAPSHOT-SHAPED.

TWO INSTRUMENTS ON TWO DIFFERENT AXES (they are not repetitions of each other):
  (1) REPO CENSUS -- comp-find over the whole corpus for the two names that carry the value
      (`aws_keys`, `_index_aws`), denominator PRINTED, hits classified by SUBTRACTION from
      that denominator rather than by a forward list of what I remembered to look for.
  (2) AST DATAFLOW inside the producer -- every bind and every read of `aws_keys` and of the
      `all_keys` it feeds, by line and by context. A text census cannot tell a LIVE read from
      a DEAD assignment; the AST can, and that distinction is the whole point of the criterion.

TREE: the census runs in THIS worktree and carries a positive control -- a file that exists
ONLY on this branch must appear among the hits, or the census read someone else's tree.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i2_fixture as F                                            # noqa: E402

WS = F.WS
PRODUCER = F.PRODUCER_ABS
# exists ONLY on this branch (created by this order, untracked at first run)
TREE_CONTROL_SUFFIX = "deliverables/0.9.0_WK_NFRA_CLDGRPH~2/i2_window.py"
EXEC_EXT = (".py", ".sh")


def comp_find(pattern: str):
    env = dict(os.environ)
    p = subprocess.run([sys.executable, str(WS / ".tools" / "comp-find"), pattern, "--all"],
                       capture_output=True, cwd=str(WS), env=env, timeout=110)
    out = p.stdout.decode("utf-8", "replace")
    m = re.search(r"DENOMINATOR:\s+(\d+)\s+hit\(s\) across (\d+) file\(s\) scanned", out)
    if not m:
        raise RuntimeError("ERROR: comp-find denominator line absent -- refusing to report a"
                           " number without its denominator. head=%r" % out[:300])
    hits = []
    for line in out.splitlines():
        s = line.strip()
        mm = re.match(r"^([^\s:]+\.[A-Za-z0-9_]+):(\d+):\s?(.*)$", s)
        if mm:
            hits.append((mm.group(1), int(mm.group(2)), mm.group(3)))
    return int(m.group(1)), int(m.group(2)), hits, out


def main() -> int:
    tf = F.tree_facts()
    print("I2-AC2 -- CONSUMERS OF THE aws_keys VALUE")
    print("  TREE          : %s (branch %s, HEAD %s)" % (tf["worktree"], tf["branch"], tf["head"]))
    print("  ENVIRONMENT   : comp-find corpus=all in THIS worktree; AST parse of the worktree"
          " copy of %s" % F.PRODUCER_REL)
    print("  GRAIN         : instrument 1 is TEXT (a mention and a call read alike);"
          " instrument 2 is AST (bind vs read, and dead vs live)")
    print("  COVERAGE      : names carrying the value = {aws_keys, _index_aws}."
          " A consumer that reaches the set through neither name is OUT OF REACH of this"
          " census and is declared, not assumed away.")

    hits_n, files_n, hits, raw = comp_find("aws_keys|_index_aws")
    print("")
    print("  INSTRUMENT 1 -- REPO CENSUS: %d hit(s) across %d file(s) scanned [corpus=all]"
          % (hits_n, files_n))

    # ---- TREE POSITIVE CONTROL --------------------------------------------------------
    ctrl = [h for h in hits if h[0].replace("\\", "/").endswith(TREE_CONTROL_SUFFIX)]
    tree_control = "FIRED" if ctrl else "DID-NOT-FIRE"
    print("  TREE CONTROL  : a file existing ONLY on this branch (%s) -> %d hit(s): %s"
          % (TREE_CONTROL_SUFFIX, len(ctrl), tree_control))

    # ---- SUBTRACTION from the printed denominator, never a forward list ----------------
    parsed = len(hits)
    exec_hits = [h for h in hits if h[0].lower().endswith(EXEC_EXT)]
    excl_nonexec = parsed - len(exec_hits)
    whole = [h for h in exec_hits
             if re.search(r"(?<![A-Za-z0-9_])(aws_keys|_index_aws)(?![A-Za-z0-9_])", h[2])]
    excl_substring = len(exec_hits) - len(whole)     # comp_aws_keys_in_comp_tools, aws_keys.txt
    own = [h for h in whole
           if "/0.9.0_WK_NFRA_CLDGRPH~2/i2_" in h[0].replace("\\", "/")]
    consumers = [h for h in whole if h not in own]
    prose = [h for h in consumers if h[2].lstrip().startswith(("#", '"', "snapshot,"))]
    consumers = [h for h in consumers if h not in prose]

    print("  SUBTRACTION   : %d parsed hit lines"
          " - %d non-executable (doc/json/log/config, a MENTION not a consumer)"
          " - %d substring-different-symbol (comp_aws_keys_in_comp_tools, aws_keys.txt)"
          " - %d this order's own harness files"
          " - %d comment/docstring lines inside executable files"
          " = %d CONSUMER LINE(S)"
          % (parsed, excl_nonexec, excl_substring, len(own), len(prose), len(consumers)))
    print("  (parsed hit lines %d <= %d reported hits: comp-find prints one line per hit and"
          " this parse keeps only path:line: forms)" % (parsed, hits_n))

    print("")
    print("  CONSUMER LINES, EACH NAMED:")
    for pth, ln, txt in sorted(consumers):
        print("    %s:%d  %s" % (pth.replace("\\", "/"), ln, txt.strip()[:110]))

    # ---- INSTRUMENT 2: AST dataflow inside the producer --------------------------------
    src = PRODUCER.read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "build_stitched_graph")
    uses = []
    for n in ast.walk(fn):
        if isinstance(n, ast.Name) and n.id in ("aws_keys", "all_keys"):
            uses.append((n.lineno, n.id, "BIND" if isinstance(n.ctx, ast.Store) else "READ"))
    uses.sort()
    print("")
    print("  INSTRUMENT 2 -- AST DATAFLOW in build_stitched_graph (%d line(s) in the file):"
          % len(src.splitlines()))
    for ln, name, role in uses:
        print("    :%d  %-9s %-4s | %s" % (ln, name, role, src.splitlines()[ln - 1].strip()[:90]))

    binds_all = [u for u in uses if u[1] == "all_keys" and u[2] == "BIND"]
    reads_all = [u for u in uses if u[1] == "all_keys" and u[2] == "READ"]
    dead = []
    if len(binds_all) >= 2:
        first, second = binds_all[0][0], binds_all[1][0]
        if not [r for r in reads_all if first < r[0] < second]:
            dead.append(first)
    print("")
    print("  FINDING (measured, by AST): all_keys is BOUND at %s and READ at %s."
          % ([b[0] for b in binds_all], [r[0] for r in reads_all]))
    if dead:
        print("  FINDING (measured): the bind at :%d is DEAD -- no read of all_keys occurs"
              " between it and the rebind at :%d. It is not a consumer of the snapshot shape;"
              " it is a leftover." % (dead[0], binds_all[1][0]))
    binds_aws = [u[0] for u in uses if u[1] == "aws_keys" and u[2] == "BIND"]
    reads_aws = [u[0] for u in uses if u[1] == "aws_keys" and u[2] == "READ"]
    live_reads_aws = [ln for ln in reads_aws if not (dead and ln == dead[0])]
    print("  FINDING (measured, by AST): aws_keys is BOUND at %s and READ at %s; of those"
          " reads, %s sit on the dead bind's own line, leaving %s LIVE read(s)."
          % (binds_aws, reads_aws, [ln for ln in reads_aws if dead and ln == dead[0]],
             len(live_reads_aws)))
    print("  FINDING (held, not measured): `aws_keys` also carries the DUAL IDENTITY of an AWS"
          " node (arn AND id, _index_aws:83-85, row W2-S68). Any remedy that simply DELETES the"
          " union would drop the arn alias for every AWS node whose id != arn and would"
          " re-open W2-S68. The remedy must PRESERVE the alias while re-deriving it from the"
          " post-collapse population.")

    print("")
    print("AWS_KEYS_CONSUMERS=%d of %d scanned" % (len(consumers), files_n))
    print("TREE_READ=WORKTREE")
    print("TREE_POSITIVE_CONTROL=%s" % tree_control)
    print("EACH_CONSUMER_NAMED: %s"
          % "; ".join("%s:%d" % (p.replace("\\", "/"), ln) for p, ln, _ in sorted(consumers)))
    print("OUT_OF_REACH_DECLARED: a consumer reaching the set through neither `aws_keys` nor"
          " `_index_aws` (e.g. a re-implementation) is not visible to this census.")
    return 0 if (tree_control == "FIRED" and consumers) else 1


if __name__ == "__main__":
    sys.exit(main())
