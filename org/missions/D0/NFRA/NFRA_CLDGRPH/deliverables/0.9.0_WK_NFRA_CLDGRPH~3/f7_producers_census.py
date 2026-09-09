#!/usr/bin/env python3
"""TO-CG-F-7 / CG-s-27 -- F7-AC2: EVERY REMAINING PRODUCER STAMPS THE CLAIM.

An AST walk (never a grep: a call spanning six lines is one node here and six lines there)
over every .py under infra/aws/globgrph/ for calls of `write_manifest` / `_provenance.
write_manifest`, reporting for each whether it passes BOTH `edge_count_semantics` and
`artifact_claim`.

DENOMINATOR AND ITS EXCLUSIONS, PRINTED (a census whose exclusions are silent certifies the
set it chose, not the set that exists):
  - `kuzu_load.py` is EXCLUDED-IF-PRESENT: TO-CG-F-1 (slot ~1) retires it in this same round
    and it is outside this order's write grant. Its presence/absence is PRINTED either way.
  - `_provenance.py` itself holds the DEFINITION, not a producer call.
  - `tests/` call sites are counted and printed SEPARATELY: the CG-s-27 suite calls the
    writer deliberately WITHOUT the kwargs to prove the TypeError arm, so a test call that
    does not stamp is the contract working, not a producer that skipped it.

THE CONTROL (PRODUCER_PROBE_CONTROL): the same walker is run over two PLANTED modules in a
temp dir -- one call WITH the kwargs, one WITHOUT. A walker that cannot return NOT-STAMPING
on the negative plant is a constant, and `PRODUCERS_STAMPING=n of n` from a constant means
nothing. FIRED = the negative plant read NOT-STAMPING and the positive plant read STAMPING.

Run: python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_producers_census.py
"""
from __future__ import annotations

import ast
import os
import sys
import tempfile

ROOT = os.path.join("infra", "aws", "globgrph")
EXCLUDED_PRODUCERS = ("kuzu_load.py",)   # TO-CG-F-1 retires it; outside this grant
DEFINITION_FILE = "_provenance.py"
REQUIRED_KWARGS = ("edge_count_semantics", "artifact_claim")


def _is_write_manifest(node: ast.Call) -> bool:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id == "write_manifest"
    if isinstance(f, ast.Attribute):
        return f.attr == "write_manifest"
    return False


def scan_source(src: str, path: str) -> list:
    """[(path, lineno, stamped_bool, missing_list)] for every write_manifest CALL."""
    out = []
    for node in ast.walk(ast.parse(src, filename=path)):
        if isinstance(node, ast.Call) and _is_write_manifest(node):
            names = {kw.arg for kw in node.keywords if kw.arg}
            starstar = any(kw.arg is None for kw in node.keywords)
            missing = [k for k in REQUIRED_KWARGS if k not in names]
            # a **kwargs splat could carry them -- report it as UNDETERMINED, never as clean
            out.append((path, node.lineno, (not missing) and not starstar, missing, starstar))
    return out


def scan_file(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        return scan_source(fh.read(), path)


def legacy_helper_defs(root: str) -> list:
    """`_stamp_claim` FUNCTION DEFINITIONS outside the excluded file: the post-hoc claim
    stampers that the writer's required kwargs make dead."""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".py") or name in EXCLUDED_PRODUCERS:
                continue
            p = os.path.join(dirpath, name)
            with open(p, encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=p)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and node.name == "_stamp_claim":
                    hits.append((p, node.lineno))
    return hits


def run_probe_control() -> tuple:
    """Plant one stamping call and one NOT-stamping call; the walker must separate them."""
    neg = ("import _provenance\n"
           "_provenance.write_manifest('/tmp/f7_probe_db', source_kind='stitch',\n"
           "                           source_vintage={}, node_count=1, edge_count=1)\n")
    pos = ("import _provenance\n"
           "_provenance.write_manifest('/tmp/f7_probe_db', source_kind='stitch',\n"
           "                           source_vintage={}, node_count=1, edge_count=1,\n"
           "                           edge_count_semantics='stored',\n"
           "                           artifact_claim='served_projection')\n")
    with tempfile.TemporaryDirectory(prefix="f7_probe_") as td:
        pn = os.path.join(td, "f7_probe_negative.py")
        pp = os.path.join(td, "f7_probe_positive.py")
        for p, s in ((pn, neg), (pp, pos)):
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(s)
        rn = scan_file(pn)
        rp = scan_file(pp)
    neg_ok = len(rn) == 1 and rn[0][2] is False and rn[0][3] == list(REQUIRED_KWARGS)
    pos_ok = len(rp) == 1 and rp[0][2] is True
    return neg_ok, pos_ok, rn, rp


def main() -> int:
    if not os.path.isdir(ROOT):
        print("ERROR: %s not found -- run from the worktree root" % ROOT)
        return 2

    producers, tests, excluded_present, definition_calls = [], [], [], []
    files_scanned = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".py"):
                continue
            p = os.path.join(dirpath, name)
            files_scanned += 1
            calls = scan_file(p)
            if name in EXCLUDED_PRODUCERS:
                excluded_present.append((p, len(calls)))
                continue
            for c in calls:
                if os.path.basename(os.path.dirname(p)) == "tests":
                    tests.append(c)
                elif name == DEFINITION_FILE:
                    definition_calls.append(c)
                else:
                    producers.append(c)

    print("=== TO-CG-F-7 / CG-s-27 -- write_manifest producer census ===")
    print("SCOPE: %s | PY_FILES_SCANNED=%d" % (ROOT, files_scanned))
    if excluded_present:
        for p, n in excluded_present:
            print("EXCLUDED_PRESENT: %s (%d write_manifest call site(s)) -- retired by "
                  "TO-CG-F-1, outside this grant, NOT counted" % (p.replace("\\", "/"), n))
    else:
        print("EXCLUDED_PRESENT: none (kuzu_load.py absent at this HEAD)")
    print("DEFINITION_FILE_CALLS=%d (%s holds the def, not a producer call)"
          % (len(definition_calls), DEFINITION_FILE))
    print("TEST_CALL_SITES=%d (excluded and printed: the CG-s-27 suite calls the writer "
          "WITHOUT the kwargs on purpose, to prove the TypeError arm)" % len(tests))
    print("")
    print("PRODUCER CALL SITES (the denominator):")
    stamping = 0
    for p, line, ok, missing, splat in sorted(producers):
        note = "STAMPS" if ok else ("MISSING " + ",".join(missing) if missing else "")
        if splat and not missing:
            note = "UNDETERMINED (**kwargs splat -- cannot be read as stamping)"
        print("  %-52s :%-5d %s" % (p.replace("\\", "/"), line, note))
        if ok:
            stamping += 1
    total = len(producers)
    print("")

    helpers = legacy_helper_defs(ROOT)
    for p, line in helpers:
        print("LEGACY_HELPER: %s:%d" % (p.replace("\\", "/"), line))

    neg_ok, pos_ok, rn, rp = run_probe_control()
    print("PROBE_NEGATIVE: planted call without the kwargs -> %s"
          % ("NOT-STAMPING (caught)" if neg_ok else "NOT CAUGHT: %r" % (rn,)))
    print("PROBE_POSITIVE: planted call with the kwargs    -> %s"
          % ("STAMPING" if pos_ok else "NOT READ AS STAMPING: %r" % (rp,)))
    print("")
    print("PRODUCERS_STAMPING=%d of %d" % (stamping, total))
    print("LEGACY_HELPER_SITES=%d" % len(helpers))
    print("PRODUCER_PROBE_CONTROL=%s" % ("FIRED" if (neg_ok and pos_ok) else "DEAD"))
    return 0 if (stamping == total and total > 0 and not helpers and neg_ok and pos_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
