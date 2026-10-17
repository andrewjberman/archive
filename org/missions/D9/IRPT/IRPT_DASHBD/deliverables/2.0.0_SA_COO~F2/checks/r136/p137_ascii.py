"""IRPT_DASHBD round 137, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the TEN NON-ASCII CHARACTERS out of `data/inf/scripts/gold/orion-gold-dispatch.sh` (cell DB-f-2401).

  The CTO's round-135 ADDENDUM 1 (msg 10025): the issuer owns the 10 non-ASCII characters in the dispatch script; a round-137 cell takes ALL 10 out, never a subset (CLAUDE.md
  section 4: in a file that already carries non-ASCII the only two safe moves are ALL out or every reader explicit). The base is the repo copy after the round-135 insertion
  (pinned below): 8 EM DASHES (U+2014) and 2 SECTION SIGNS (U+00A7), one per line on 10 lines. The mapping is fixed: each em dash becomes two hyphen-minus characters; each section sign (always directly before a digit) becomes the word "section" and one space. Nothing else in the file changes. NOT DEPLOYED: the live copy is the pre-round-135 one.
  DBF137-4-AC1 (the file), DBF137-4-AC2 (the tests)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

DISPATCH = "data/inf/scripts/gold/orion-gold-dispatch.sh"
BASE = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/dispatch_r137_base.sh.txt"
BASE_SHA256 = "70b5774422c6"  # first 12 hex of the base copy's sha256, checked as a prefix
TESTS = "data/inf/scripts/gold/tests/test_dispatch_txn_block.py"
OTHER_TESTS = ("data/inf/scripts/gold/tests/test_aor_resolution.py", "data/inf/scripts/gold/tests/test_aor_fold_derivation.py",
               "data/inf/manual_api/test_pull_inflection_scope_account_returns.py")
EM_DASH = chr(0x2014)
SECTION = chr(0xA7)


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def mapped(line):
    """The one line the mapping gives: each em dash to two hyphen-minus characters; each section sign directly before a digit to 'section ' (a section sign elsewhere is refused)."""
    out = line.replace(EM_DASH, "--")
    out = re.sub(SECTION + r"(?=[0-9])", "section ", out)
    return out


def line_problems(base_lines, new_lines):
    pr = []
    if len(base_lines) != len(new_lines):
        return ["the file must keep its %d lines (found %d): only characters change, no line is added or removed" % (len(base_lines), len(new_lines))]
    changed = 0
    for i, (b, n) in enumerate(zip(base_lines, new_lines), 1):
        want = mapped(b) if not b.isascii() else b
        if SECTION in want:
            pr.append("line %d: a section sign not directly before a digit has no mapping" % i)
        if n != want:
            pr.append("line %d must be %r, found %r" % (i, want[:90], n[:90]))
        elif n != b:
            changed += 1
    if changed != sum(1 for b in base_lines if not b.isascii()):
        pr.append("every one of the base's non-ASCII lines must change (changed %d)" % changed)
    return pr


def ac1(root):
    new = Path(root, DISPATCH).read_bytes()
    bp = Path(root, BASE)
    need(bp.is_file(), "missing the pinned base copy " + BASE)
    base = bp.read_bytes()
    need(hashlib.sha256(base).hexdigest().startswith(BASE_SHA256), "the pinned base copy is not the base the order names (sha256 prefix)")
    need(b"\r" not in new or b"\r" in base, "the file must keep LF line endings")
    need(not [c for c in new.decode("utf-8") if ord(c) > 127], "the dispatch script must hold no non-ASCII character (all ten out)")
    pr = line_problems(base.decode("utf-8").split("\n"), new.decode("utf-8").split("\n"))
    need(not pr, "; ".join(pr[:5]))
    run = subprocess.run(["bash", "-n", str(Path(root, DISPATCH))], capture_output=True, text=True, timeout=120)
    need(run.returncode == 0, "bash -n failed: %s" % (run.stderr or "")[:200])


def ac2(root):
    tp = Path(root, TESTS)
    need(tp.is_file(), "missing " + TESTS)
    text = tp.read_text(encoding="utf-8")
    names = re.findall(r"^def (test_\w+)", text, re.M)
    need(len(names) >= 29, "the dispatch test file must hold at least 29 tests (28 at the base plus the whole-file ASCII test): found %d" % len(names))
    need(any("ascii" in n.lower() and "whole" in n.lower() for n in names), "the dispatch test file needs a test whose name holds `whole` and `ascii` asserting the entire file is ASCII")
    for t in (TESTS,) + OTHER_TESTS:
        run = subprocess.run([sys.executable, "-m", "pytest", t, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True, text=True, timeout=600)
        need(run.returncode == 0, "pytest %s failed: %s" % (t, (run.stdout or "")[-250:]))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    base = ["a", "b " + EM_DASH + " c", "see brief " + SECTION + "4.3.", "d"]
    good = ["a", "b -- c", "see brief section 4.3.", "d"]
    arm("mapped-dash", mapped("x " + EM_DASH + " y"), "x -- y")
    arm("mapped-section", mapped("brief " + SECTION + "4.3"), "brief section 4.3")
    arm("lines-green", line_problems(base, good), [])
    arm("lines-wrong-replacement", len(line_problems(base, ["a", "b - c", "see brief section 4.3.", "d"])) >= 1, True)
    arm("lines-ascii-line-changed", len(line_problems(base, ["A", "b -- c", "see brief section 4.3.", "d"])), 1)
    arm("lines-added", len(line_problems(base, good + ["e"])), 1)
    arm("lines-left-non-ascii", len(line_problems(base, base)) >= 1, True)
    arm("section-not-before-digit", len(line_problems(["x " + SECTION + " y"], ["x " + SECTION + " y"])) >= 1, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF137-4-AC1": ac1, "DBF137-4-AC2": ac2}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
