"""Fixed-input checker for LGIC_ENFORCE cell EN-n-2 -- the GRADING_RULE.md N2 re-join amendment.

PINNED AT THE CUT (2026-09-20, 2.0.0_SA_COO~G). Read-only; it edits nothing.

Two mechanical arms plus a self-test:

  doc-clause   PASS-N2R-DOC     GRADING_RULE.md's N2 now documents the camel RE-JOIN, and names the
                                registered-token mechanism rather than merely asserting it.
  code-frozen  PASS-N2R-FROZEN  lib/opal_naming.py is BYTE-IDENTICAL to its blob at the cut.
  selftest     PASS-N2R-ARMS    both arms discriminate: each refuses a mutant and accepts a
                                hand-built correct case.

WHY code-frozen EXISTS AND IS NOT CEREMONY. REMEDIATION_v2.md carries BOTH a superseded v9 entry
("a REAL grade() DEFECT ... Owed: a fix in lib/opal_naming.py grade()") and the v19 correction that
reverses it. A reader landing on the first match inherits the superseded remedy -- which happened to
a Tier-1 seat on 2026-09-20 (LGIC_ENFORCE-S122/S124). A worker inheriting it would patch a grader
1.0.0_SA_CTO ruled CORRECT (@98502), against 27 dependent census names, 15 of them LIVE.
THE CHEAPEST WRONG MOVE IS THE ONE THIS ARM REFUSES.
"""
import hashlib
import io
import os
import sys

GRADING_RULE = "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md"
GRADER = "lib/opal_naming.py"

# Pinned at the cut by `git rev-parse HEAD:<path>`.
GRADER_BLOB_AT_CUT = "5ce28d6d24b0f753761096b7b0d75efc63be3954"
GRADING_RULE_BLOB_AT_CUT = "5c98cb76e9ff349dac3704d244cde1591a327967"

# The clause must do BOTH: name the re-join, and name WHY (a registered multi-word token).
# Tokens are matched case-insensitively and are deliberately few -- the wording is the worker's
# and the CVO's to judge (N2R-AC3), not this checker's to dictate.
REJOIN_TOKENS = ("re-join", "rejoin", "joined back", "recombine")
REASON_TOKENS = ("registered", "vocabulary", "systems.json", "incrparity")


def _blob(path):
    """git's blob id for a file's CURRENT bytes on disk (not its committed state)."""
    data = io.open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def _n2_region(text):
    """The N2 bullet and everything up to the next top-level rule bullet.

    Returns (region, found). A clause added ANYWHERE in the file is not enough: the ruling is that
    *N2 absorbs* it, so the region is bounded and the denominator is printed.
    """
    low = text.lower()
    i = low.find("**n2 ")
    if i < 0:
        return "", False
    j = low.find("\n- **n3 ", i)
    return (text[i:j] if j > 0 else text[i:]), True


def doc_clause(verbose=True, text=None):
    if text is None:
        text = io.open(GRADING_RULE, encoding="utf-8").read()
    region, found = _n2_region(text)
    if not found:
        if verbose:
            print("FAIL-N2R-DOC: no N2 bullet found in %s" % GRADING_RULE)
        return False
    low = region.lower()
    hit_rejoin = [t for t in REJOIN_TOKENS if t in low]
    hit_reason = [t for t in REASON_TOKENS if t in low]
    if verbose:
        print("N2 region: %d chars of %d in the file (denominator printed, not a whole-file grep)"
              % (len(region), len(text)))
        print("  re-join tokens present: %s of %s" % (hit_rejoin or "NONE", list(REJOIN_TOKENS)))
        print("  reason  tokens present: %s of %s" % (hit_reason or "NONE", list(REASON_TOKENS)))
    if hit_rejoin and hit_reason:
        if verbose:
            print("PASS-N2R-DOC")
        return True
    if verbose:
        print("FAIL-N2R-DOC: N2 must BOTH name the re-join AND name why it is legitimate "
              "(a registered multi-word token), not merely assert the behaviour.")
    return False


def code_frozen(verbose=True):
    got = _blob(GRADER)
    ok = (got == GRADER_BLOB_AT_CUT)
    if verbose:
        print("%s blob now: %s" % (GRADER, got))
        print("%s blob at cut: %s" % (GRADER, GRADER_BLOB_AT_CUT))
        if ok:
            print("PASS-N2R-FROZEN")
        else:
            print("FAIL-N2R-FROZEN: THE GRADER MOVED. This cell is documentation-only. "
                  "@98502 ruled grade() CORRECT; the superseded v9 remediation entry that says "
                  "otherwise is NOT the live remedy (see LGIC_ENFORCE-S122/S124).")
    return ok


def selftest():
    """Each arm must REFUSE a mutant and ACCEPT a hand-built correct case (R-47: a mutant test
    alone cannot catch a vacuous pass, so a positive control runs beside every negative one)."""
    base = io.open(GRADING_RULE, encoding="utf-8").read()
    region, found = _n2_region(base)
    if not found:
        print("FAIL-N2R-ARMS: cannot locate N2 to build controls")
        return False
    results = []

    # doc-clause NEGATIVE: the file as it stands at the cut (clause absent) must FAIL.
    results.append(("doc/neg-at-cut", doc_clause(verbose=False, text=base) is False))

    # doc-clause POSITIVE: a hand-built correct N2 must PASS.
    good = base.replace(region, region.rstrip() +
                        "\n  Pieces are re-joined when the join is a registered token in the "
                        "vocabulary (see systems.json).\n", 1)
    results.append(("doc/pos-handbuilt", doc_clause(verbose=False, text=good) is True))

    # doc-clause MUTANT: re-join named but NO reason -> must still FAIL (half-credit refused).
    half = base.replace(region, region.rstrip() + "\n  Pieces are re-joined.\n", 1)
    results.append(("doc/mut-no-reason", doc_clause(verbose=False, text=half) is False))

    # doc-clause MUTANT: the clause placed OUTSIDE N2 -> must FAIL (the ruling says N2 absorbs it).
    outside = base + "\n\nPieces are re-joined when the join is a registered token (systems.json).\n"
    results.append(("doc/mut-outside-n2", doc_clause(verbose=False, text=outside) is False))

    # code-frozen POSITIVE: the unmodified grader must PASS.
    results.append(("code/pos-unmodified", code_frozen(verbose=False) is True))

    for name, ok in results:
        print("  %-22s %s" % (name, "ok" if ok else "BROKEN"))
    passed = all(ok for _, ok in results)
    print("%s (%d of %d arms discriminate)"
          % ("PASS-N2R-ARMS" if passed else "FAIL-N2R-ARMS",
             sum(1 for _, ok in results if ok), len(results)))
    return passed


def main(argv):
    if len(argv) != 2 or argv[1] not in ("doc-clause", "code-frozen", "selftest"):
        print("usage: check_en_n2.py doc-clause|code-frozen|selftest")
        return 2
    if not os.path.isfile(GRADING_RULE):
        print("FAIL: %s not found -- run from the worktree root" % GRADING_RULE)
        return 1
    fn = {"doc-clause": doc_clause, "code-frozen": code_frozen, "selftest": selftest}[argv[1]]
    return 0 if fn() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
