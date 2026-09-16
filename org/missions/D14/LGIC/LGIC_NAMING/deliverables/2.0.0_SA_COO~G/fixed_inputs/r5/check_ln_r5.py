#!/usr/bin/env python3
"""check_ln_r5.py -- the mechanical criteria of LGIC_NAMING round 5, the CLOSING round
(decomposition v7 s.0f), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-5 issuance. Run from the worktree root:
`python <this file> <subcommand>`. Every subcommand prints its evidence, a DENOMINATOR where one
exists, and exactly one line `VERDICT: PASS-<X>` or `VERDICT: FAIL-<X>`, and exits 0. A missing
input is a FAIL verdict, never a traceback. No PASS string is a substring of another subcommand's
PASS or FAIL string, because proof-of-spec-check greps <expect> UNANCHORED.

`--list` prints the subcommands. `selftest-arms` is the discriminating self-test: it drives each
arm against a DOCTORED input in memory and asserts the arm FAILS. See WHY below.

ROUND 5 runs four cells:
  LN-g-1  GRADING_RULE.md's coverage at NAMING_SCHEMA v1.10 (item 3) + the 68 forms arm (item 5b)
  LN-g-2  the two globgrph worked cases re-verdicted FROM THE BUILDER (item 1, S22/R-5)
          + G1R4-AC6 re-graded by the fixed checker (item 5a)
  LN-f-1  the gaps re-run at HEAD (item 2, W4-S3/C-S25)                       -- REPO plane
  LN-f-2  FWD-3's live half (item 4, R-17)                                    -- LIVE plane

=============================================================================================
WHY THIS FILE CARRIES A DISCRIMINATING SELF-TEST, and it is not defensive boilerplate.
=============================================================================================
SIX instrument defects were found in THIS SEAT'S fixed inputs in one session, each one an
instrument reading a different object from the one its name claimed:

  LGIC_CANON-W2-S3   a docstring CLAIMED a negative control; the subcommand planted nothing
  LGIC_CANON-W3-S2   \\S+ single-token regexes could not read multi-word labels round 1 read fine
  LGIC_CANON-W8-S4   counted token OCCURRENCES (9) where the claim was marked ROWS (5 of 9)
  LGIC_CANON-W5-S2   a whole-file \\bR<n>\\b blob scan could not tell REACHED from NOT REACHED
  LGIC_ENFORCE-S55   an ANSI strip with no ESC in its pattern -- inert, and LIVE-blind in the
                     sibling, which passed no --color flag at all
  LGIC_NAMING-S24    the same inert strip, surviving only because --color=no held beside it

3.0.0_SA_CVO's line on the first four is the right one: "four in one round is a rate, not a
coincidence." A checker that only ever runs against the TRUE tree cannot tell you it works; it
tells you the tree passes. So every arm here is exercised against a doctored input by
`selftest-arms`, and an arm that cannot be made to FAIL is itself a FAIL.

THE ANSI LESSON IS BUILT IN RATHER THAN DESCRIBED (S55/S24). `_plain()` strips a REAL CSI
sequence -- ESC, then '[', then params, then a final letter -- and `_pytest()` ALSO passes
--color=no at the source. BOTH, and `selftest-arms` exercises the strip ALONE against forced
colour, because two defences tested together tell you only that their union works. The strip
that shipped in r4 and in check_en_r2.py had NO \\x1b in its pattern and removed nothing that
mattered; it is the reason this paragraph exists.

Standard library only. ASCII only. LF endings.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# 9 levels: r5 / fixed_inputs / <serial> / deliverables / LGIC_NAMING / LGIC / D14 / missions / org
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 9)))
BASE = "org/missions/D14/LGIC/LGIC_NAMING"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
RULE = BASE + "/deliverables/GRADING_RULE.md"
LIB = "lib/opal_naming.py"
TESTS = "lib/tests/test_opal_naming.py"
REGISTRY = "infra/logic/registry"

# The two cases S22 holds open. Expectation is the BUILDER'S OWN OUTPUT, measured at the cut
# (2026-09-16, grade() at HEAD), never a form typed here by the issuer -- Rule 30.
GLOBGRPH_CASES = (
    ("globgrph-serving", "ECS_TASK_DEFINITION", "OUT-OF-PATTERN", "globgrph-serving-task"),
    ("opal-globgrph", "ECS_CLUSTER", "OUT-OF-PATTERN", "globgrph-cluster"),
)

# A REAL CSI sequence: ESC, '[', params, final letter. The \x1b is the whole point (S55).
_CSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_FAILED = re.compile(r"^FAILED (\S+)", re.M)
_COUNTS = re.compile(r"(\d+) failed|(\d+) passed")


def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)


def read(path):
    p = path if os.path.isabs(path) else os.path.join(REPO, path)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_json(path):
    t = read(path)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def missing(path, tag):
    say("FAIL-%s" % tag, "the input is absent: %s" % path)
    return 0


def _plain(s):
    """Strip real ANSI CSI sequences. The ESC is IN the pattern -- see S55."""
    return _CSI.sub("", s)


def _pytest(extra=()):
    """Run the suite. --color=no at the SOURCE *and* _plain() on the way out: belt AND brace,
    and `selftest-arms` exercises each alone, which is the check that was never run in r4."""
    cmd = [sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider",
           "--color=no", os.path.join(REPO, TESTS)] + list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    return _plain(r.stdout + r.stderr)


def suite_counts(out):
    """(passed, failed, named) from pytest's tail. Denominator is passed+failed, printed."""
    passed = failed = 0
    m = re.search(r"(\d+) failed", out)
    if m:
        failed = int(m.group(1))
    m = re.search(r"(\d+) passed", out)
    if m:
        passed = int(m.group(1))
    return passed, failed, sorted(set(_FAILED.findall(out)))


def _naming():
    """Import lib/opal_naming.py from the worktree under test, not from anywhere else."""
    import importlib.util
    p = os.path.join(REPO, LIB)
    if not os.path.isfile(p):
        return None
    spec = importlib.util.spec_from_file_location("opal_naming_r5", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ LN-g-2 (item 1, S22/R-5)
def _grade_globgrph(mod):
    """The builder's verdict for each held case. Returns [(name, type, got, want), ...]."""
    rows = []
    for name, typ, want_v, want_c in GLOBGRPH_CASES:
        try:
            got = mod.grade(name, typ)
        except Exception as exc:                                  # a raise is a result, not a crash
            got = ("RAISED:%s" % type(exc).__name__, str(exc)[:60])
        rows.append((name, typ, got, (want_v, want_c)))
    return rows


def g2_globgrph():
    mod = _naming()
    if mod is None:
        return missing(LIB, "G2-GLOBGRPH")
    rows = _grade_globgrph(mod)
    ok = all(got == want for _, _, got, want in rows)
    print("S22 / R-5: the two held cases, verdicted BY THE BUILDER (grade()), denominator %d" % len(rows))
    for name, typ, got, want in rows:
        print("  %-18s %-22s got %-46r want %r" % (name, typ, got, want))
    say(("PASS-GLOBGRPH-FROM-BUILDER" if ok else "FAIL-GLOBGRPH-FROM-BUILDER"),
        "the canonical forms are the builder's output, never a form typed into this checker (Rule 30)")
    return 0


def g2_suite():
    out = _pytest()
    passed, failed, named = suite_counts(out)
    total = passed + failed
    print("SUITE %s -- denominator %d (passed %d, failed %d)" % (TESTS, total, passed, failed))
    for n in named:
        print("  FAILED %s" % n)
    esc = out.count("\x1b")
    print("  ANSI escapes surviving into the parsed text: %d (must be 0 -- S55)" % esc)
    ok = failed == 0 and total > 0 and esc == 0
    say("PASS-SUITE-ALL-GREEN" if ok else "FAIL-SUITE-ALL-GREEN",
        "S22 holds FWD-5 open until this reads 0 failed")
    return 0


# ------------------------------------------------------------------ LN-g-1 (item 3 + item 5b)
def _schema_fields(doc):
    """Top-level keys; where a key is an object, its second-level keys instead. Metadata excluded.
    Same GRAIN as r4's field_diff, restated here so this file is readable on its own (W3-S6)."""
    META = ("version", "changelog", "ratified_by")
    out = set()
    for k, v in (doc or {}).items():
        if k in META:
            continue
        if isinstance(v, dict) and v:
            for k2 in v:
                out.add("%s.%s" % (k, k2))
        else:
            out.add(k)
    return out


_STEP = re.compile(r"^\s*(?:-\s*)?(?:COVERS\s+)?(R\d+(?:\.\d+)?[a-d]?)\b[^\n]*$", re.M)


def _states_step(rule_text, field):
    """Does a STEP line of GRADING_RULE.md read this field BY NAME?

    NOTE: NOT a substring test on the leaf. The first draft of this asked `"bd" in rule`, where `bd` is
    the leaf of `alias_adjacency.bd` AND a firm alias that appears all over the document -- so the
    arm passed vacuously and would have passed against a rule that never mentioned adjacency at all.
    That is LGIC_CANON-W8-S4's class (a token's OCCURRENCES standing in for the marked object) and it
    got into this file on its first write, which is the rate the docstring is about.

    The claim is the ANALYSIS's: "GRADING_RULE.md states the step that reads alias_adjacency (R3)".
    So: a line that names a step label AND carries the FULL dotted field or its parent key.
    """
    parent = field.split(".")[0]
    for line in rule_text.splitlines():
        if not _STEP.match(line):
            continue
        if field in line or parent in line:
            return True
    return False


def g1_alias_adjacency():
    """Item 3: v1.10 lands alias_adjacency (A-3); GRADING_RULE.md must state the step that reads it."""
    doc = load_json(SCHEMA)
    rule = read(RULE)
    if doc is None:
        return missing(SCHEMA, "G1-ADJACENCY")
    if rule is None:
        return missing(RULE, "G1-ADJACENCY")
    fields = _schema_fields(doc)
    present = sorted(f for f in fields if "alias_adjacency" in f)
    covered = [f for f in present if _states_step(rule, f)]
    print("NAMING_SCHEMA %s -- fields %d; alias_adjacency fields %d"
          % (doc.get("version"), len(fields), len(present)))
    for f in present:
        print("  %-42s a STEP in GRADING_RULE.md reads it: %s" % (f, f in covered))
    ok = bool(present) and len(covered) == len(present)
    say("PASS-ADJACENCY-STATED" if ok else "FAIL-ADJACENCY-STATED",
        "N of N = %d of %d" % (len(covered), len(present)))
    return 0


SUBCOMMANDS = {
    "g2-globgrph": g2_globgrph,
    "g2-suite": g2_suite,
    "g1-adjacency": g1_alias_adjacency,
}


# ------------------------------------------------------------------ the discriminating self-test
def selftest_arms():
    """Drive each arm against a DOCTORED input and assert it FAILS. An arm that cannot fail is a FAIL.

    This is the check r4 never ran, and it is why LGIC_ENFORCE-S55 existed: two defences tested
    together tell you only that their union works."""
    results = []

    # ARM: the ANSI strip, ALONE, against forced colour -- the exact case that defeated r4's.
    cmd = [sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider",
           "--color=yes", os.path.join(REPO, TESTS)]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    raw = r.stdout + r.stderr
    stripped = _plain(raw)
    results.append(("strip-alone-removes-every-ESC", raw.count("\x1b") > 0 and stripped.count("\x1b") == 0,
                    "raw ESC %d -> stripped ESC %d" % (raw.count("\x1b"), stripped.count("\x1b"))))
    results.append(("strip-alone-finds-the-failures",
                    len(_FAILED.findall(stripped)) == len(_FAILED.findall(_plain(_pytest()))),
                    "forced-colour parse %d == --color=no parse %d"
                    % (len(_FAILED.findall(stripped)), len(_FAILED.findall(_plain(_pytest()))))))

    # ARM: g2-globgrph must FAIL when the builder's answer is doctored.
    class _Doctored:
        def grade(self, name, typ):
            return ("CONFORMANT", name)
    rows = _grade_globgrph(_Doctored())
    results.append(("g2-globgrph-fails-on-a-doctored-builder",
                    not all(g == w for _, _, g, w in rows), "doctored builder returns CONFORMANT"))

    # ARM: the field reader must SEE a field, so removing it must change the count.
    doc = load_json(SCHEMA) or {}
    full = _schema_fields(doc)
    less = _schema_fields({k: v for k, v in doc.items() if k != "alias_adjacency"})
    results.append(("g1-field-reader-sees-alias_adjacency", len(less) < len(full),
                    "fields %d -> %d with the key removed" % (len(full), len(less))))

    # ARM: the COVERAGE test must fail on a rule that never names the field. This is the arm the
    # first draft lacked, which is exactly why its substring bug survived one run and one read.
    # NOTE: The positive here is SYNTHETIC, deliberately. The live GRADING_RULE.md is the PRE-state --
    # stating this step is the work LN-g-1 is cut to do -- so an arm that asserted True against the
    # live file would be asserting the cell had already run. A self-test must not depend on the
    # deliverable it is testing the checker for.
    yes = "- COVERS R3: reads alias_adjacency for the firm's sanctioned neighbours\n"
    no = "- COVERS R3: reads the firm's short form\n"
    results.append(("g1-coverage-discriminates-stated-from-not",
                    _states_step(yes, "alias_adjacency.bd") and not _states_step(no, "alias_adjacency.bd"),
                    "synthetic rule naming the field -> True; one that does not -> False"))

    # ARM: suite_counts must not read a green tail out of a red one.
    p, f, n = suite_counts("2 failed, 80 passed in 0.40s\nFAILED lib/tests/x.py::test_a\n")
    results.append(("suite-counts-reads-failed", (p, f, n) == (80, 2, ["lib/tests/x.py::test_a"]),
                    "parsed passed=%d failed=%d named=%r" % (p, f, n)))

    ok = all(r[1] for r in results)
    print("DISCRIMINATING SELF-TEST -- denominator %d arms" % len(results))
    for name, good, detail in results:
        print("  %-42s %-5s %s" % (name, "PASS" if good else "FAIL", detail))
    say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE",
        "an arm that cannot be made to fail is a constant wearing a measurement's clothes")
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l"):
        for k in sorted(SUBCOMMANDS):
            print(k)
        print("selftest-arms")
        return 0
    cmd = args[0]
    if cmd == "selftest-arms":
        return selftest_arms()
    fn = SUBCOMMANDS.get(cmd)
    if fn is None:
        say("FAIL-NO-SUCH-SUBCOMMAND", "unknown subcommand: %s" % cmd)
        return 0
    return fn()


if __name__ == "__main__":
    sys.exit(main())
