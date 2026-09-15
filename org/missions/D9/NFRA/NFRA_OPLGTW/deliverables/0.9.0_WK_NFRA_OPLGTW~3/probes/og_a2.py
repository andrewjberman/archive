"""OG-a-2 probe (0.9.0_WK_NFRA_OPLGTW~3), TO-OG-a-2 as amended @adc6874dea and @1efed70736.

AC13 (discriminating): for each of the three test modules granted FIXTURE-ONLY, the count of assert statements
(`assert`, `self.assert*`, `pytest.raises`) at HEAD equals the count at the cut base 3f94e0a024. Both vintages
are read from git objects (`git show <rev>:<path>`), never from the worktree; the worktree's agreement with HEAD
is printed as a disclosure only. A git read that fails or returns nothing is a FAIL, never a zero.

AC14 (discriminating): across the same three modules, the diff against the cut base changes exactly 3 assertion
lines -- the three ruling 97141 names (test_oauth_durable.py:710, test_jwt_cve_lock.py:117,
test_schwab_audit.py:342, line numbers at f8feaf081e) -- and each changed line still carries its original email
literal or variable. Two instruments per module: the assert statements matched structurally (ast.dump, no line
numbers) between base and HEAD, so an unmatched one is a changed assertion; and the `git diff -U0` hunks, whose
changed lines are counted where they fall inside an assert statement's span. Per module both must read 1, the
changed base assertion must be the named line at f8feaf081e, and the HEAD assertion must compare `["email"]` to
the base's `["sub"]` comparand while its own `["sub"]` comparand differs from it. Non-assertion lines changed since
f8feaf081e are printed as a disclosure.

Usage:  <python> og_a2.py AC13 | AC14
Prints per-module lines, then `VERDICT: PASS-OGA2-AC<n>` or `VERDICT: FAIL-OGA2-AC<n> <reason>`.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE = "3f94e0a024"
AMEND_PIN = "f8feaf081e"   # the vintage ruling 97141 cites its line numbers at
MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_oauth_durable.py",
    "infra/aws/ec2/opal-gateway/tests/test_jwt_cve_lock.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_audit.py",
)
NAMED = dict(zip(MODULES, (710, 117, 342)))   # ruling 97141's three assertion lines @AMEND_PIN
KINDS = ("assert", "self.assert*", "pytest.raises")
_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _git(root, *args):
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")


def _kind(node):
    """The assert kind of an AST node, or None."""
    if isinstance(node, ast.Assert):
        return "assert"
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)):
        owner, attr = node.func.value.id, node.func.attr
        if owner == "self" and attr.startswith("assert"):
            return "self.assert*"
        if owner == "pytest" and attr == "raises":
            return "pytest.raises"
    return None


def count(source: str) -> dict:
    """Assert statements by kind: `assert` statements, `self.assert*(...)` calls, `pytest.raises(...)` calls."""
    n = dict.fromkeys(KINDS, 0)
    for node in ast.walk(ast.parse(source)):
        kind = _kind(node)
        if kind:
            n[kind] += 1
    return n


def assertions(source: str) -> list:
    """[(first line, last line, structural key, node)] for every assert statement of the three kinds."""
    return [(node.lineno, node.end_lineno, ast.dump(node), node)
            for node in ast.walk(ast.parse(source)) if _kind(node)]


def _fmt(n: dict) -> str:
    return " ".join("%s=%d" % (k, n[k]) for k in KINDS) + " total=%d" % sum(n.values())


def _root_head(verdict_tag):
    rc, top, err = _git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel")
    if rc != 0 or not top.strip():
        print("VERDICT: FAIL-%s git rev-parse --show-toplevel rc=%d %s" % (verdict_tag, rc, err.strip()))
        return None, None
    root = Path(top.strip())
    rc, head, err = _git(root, "rev-parse", "--short=10", "HEAD")
    if rc != 0 or not head.strip():
        print("VERDICT: FAIL-%s git rev-parse HEAD rc=%d %s" % (verdict_tag, rc, err.strip()))
        return None, None
    return root, head.strip()


def _show(root, rev, path):
    """(source, error): a failed or empty read is an error, never an empty source."""
    rc, src, err = _git(root, "show", "%s:%s" % (rev, path))
    if rc != 0 or not src.strip():
        return None, "git show %s:%s rc=%d bytes=%d %s" % (rev, path, rc, len(src), err.strip())
    return src, None


def ac13() -> int:
    # Positive control on the counter: one of each kind must count 1 each, and a non-assert call 0.
    control = count("def t(self):\n    assert x\n    self.assertEqual(a, b)\n    self.fail()\n"
                    "    with pytest.raises(E):\n        pass\n    pytest.skip()\n")
    if control != {"assert": 1, "self.assert*": 1, "pytest.raises": 1}:
        print("VERDICT: FAIL-OGA2-AC13 counter positive control read %s" % control)
        return 1
    print("counter positive control: %s (expected 1/1/1)" % _fmt(control))
    root, head = _root_head("OGA2-AC13")
    if root is None:
        return 1
    print("HEAD %s, cut base %s, modules %d" % (head, BASE, len(MODULES)))
    unequal = []
    for path in MODULES:
        counts = {}
        for label, rev in (("HEAD", head), ("base", BASE)):
            src, err = _show(root, rev, path)
            if err:
                print("VERDICT: FAIL-OGA2-AC13 %s" % err)
                return 1
            counts[label] = (count(src), len(src.encode("utf-8")))
        (h, hb), (b, bb) = counts["HEAD"], counts["base"]
        same = sum(h.values()) == sum(b.values())
        rc_wt, _, _ = _git(root, "diff", "--quiet", "HEAD", "--", path)
        print("%s: HEAD %s (%d bytes) | base %s (%d bytes) | %s | worktree==HEAD: %s"
              % (Path(path).name, _fmt(h), hb, _fmt(b), bb, "EQUAL" if same else "DIFFER",
                 "yes" if rc_wt == 0 else "no"))
        if h != b and same:
            print("  note: totals equal, kinds differ")
        if not same:
            unequal.append("%s HEAD=%d base=%d" % (Path(path).name, sum(h.values()), sum(b.values())))
    print("modules equal: %d of %d" % (len(MODULES) - len(unequal), len(MODULES)))
    if unequal:
        print("VERDICT: FAIL-OGA2-AC13 %s" % "; ".join(unequal))
        return 1
    print("VERDICT: PASS-OGA2-AC13")
    return 0


def _hunks(diff_text):
    """(old line numbers, new line numbers) a -U0 diff changes."""
    old, new = set(), set()
    for line in diff_text.splitlines():
        m = _HUNK.match(line)
        if m:
            a, b = int(m.group(1)), int(m.group(2) or "1")
            c, d = int(m.group(3)), int(m.group(4) or "1")
            old.update(range(a, a + b))
            new.update(range(c, c + d))
    return old, new


def _inside(spans, lines):
    return sorted(n for n in lines if any(s[0] <= n <= s[1] for s in spans))


def _unmatched(items, other_keys):
    """The items whose structural key finds no partner among other_keys (a multiset)."""
    left = Counter(other_keys)
    out = []
    for item in items:
        if left[item[2]]:
            left[item[2]] -= 1
        else:
            out.append(item)
    return out


def _comparands(node, field):
    """The unparsed right-hand sides of every `<x>["field"] == <y>` inside node."""
    found = []
    for sub in ast.walk(node):
        if (isinstance(sub, ast.Compare) and len(sub.ops) == 1 and isinstance(sub.ops[0], ast.Eq)
                and isinstance(sub.left, ast.Subscript) and isinstance(sub.left.slice, ast.Constant)
                and sub.left.slice.value == field):
            found.append(ast.unparse(sub.comparators[0]))
    return found


def judge(base_src, head_src, diff_text, named_text):
    """One module's AC14 reading: (problems, facts)."""
    base, head = assertions(base_src), assertions(head_src)
    removed = _unmatched(base, [a[2] for a in head])
    added = _unmatched(head, [a[2] for a in base])
    old_lines, new_lines = _hunks(diff_text)
    old_assert, new_assert = _inside(base, old_lines), _inside(head, new_lines)
    facts = {"statements": (len(base), len(head)), "removed": len(removed), "added": len(added),
             "assert_lines": (old_assert, new_assert), "lines": (len(old_lines), len(new_lines))}
    problems = []
    if len(removed) != 1 or len(added) != 1:
        problems.append("assertion statements changed: %d removed, %d added (1 and 1 required)"
                        % (len(removed), len(added)))
    if len(old_assert) != 1 or len(new_assert) != 1:
        problems.append("changed assertion lines: base side %d, HEAD side %d (1 and 1 required)"
                        % (len(old_assert), len(new_assert)))
    if problems:
        return problems, facts
    r, a = removed[0], added[0]
    base_line = base_src.splitlines()[r[0] - 1]
    head_line = head_src.splitlines()[a[0] - 1]
    facts.update(base_line=(r[0], base_line.strip()), head_line=(a[0], head_line.strip()))
    if r[0] != r[1] or a[0] != a[1]:
        problems.append("a changed assertion spans more than one line (base %d-%d, HEAD %d-%d)"
                        % (r[0], r[1], a[0], a[1]))
    if base_line.strip() != named_text.strip():
        problems.append("the changed base assertion is not the named line @%s" % AMEND_PIN)
    orig = _comparands(r[3], "sub")
    if len(orig) != 1:
        problems.append("the base assertion carries %d `[\"sub\"] ==` comparisons (1 required)" % len(orig))
        return problems, facts
    email = orig[0]
    new_sub, new_email = _comparands(a[3], "sub"), _comparands(a[3], "email")
    facts.update(email=email, new_sub=new_sub, new_email=new_email)
    if email not in new_email:
        problems.append("the HEAD assertion does not compare [\"email\"] to the original %s" % email)
    if len(new_sub) != 1 or new_sub[0] == email:
        problems.append("the HEAD assertion's [\"sub\"] comparand is %s (one, re-targeted from %s, required)"
                        % (new_sub, email))
    if email not in head_line:
        problems.append("the HEAD line does not carry the text %s" % email)
    return problems, facts


def _control() -> bool:
    """judge() must pass a one-line re-target that keeps the email half and fail one that drops it."""
    base = 'def t():\n    assert f(t)["sub"] == email\n'
    good = 'def t():\n    assert (c := f(t))["sub"] == K and c["email"] == email\n'
    bad = 'def t():\n    assert f(t)["sub"] == K\n'
    diff = "@@ -2 +2 @@\n"
    ok_good = not judge(base, good, diff, '    assert f(t)["sub"] == email')[0]
    ok_bad = bool(judge(base, bad, diff, '    assert f(t)["sub"] == email')[0])
    print("judge control: email half kept -> %s (expected pass); email half dropped -> %s (expected fail)"
          % ("pass" if ok_good else "fail", "fail" if ok_bad else "pass"))
    return ok_good and ok_bad


def ac14() -> int:
    if not _control():
        print("VERDICT: FAIL-OGA2-AC14 judge control misread")
        return 1
    root, head = _root_head("OGA2-AC14")
    if root is None:
        return 1
    print("HEAD %s, cut base %s, named lines @%s, modules %d" % (head, BASE, AMEND_PIN, len(MODULES)))
    failed, stmts, lines = [], 0, 0
    for path in MODULES:
        name = Path(path).name
        srcs = {}
        for rev in (head, BASE, AMEND_PIN):
            src, err = _show(root, rev, path)
            if err:
                print("VERDICT: FAIL-OGA2-AC14 %s" % err)
                return 1
            srcs[rev] = src
        rc, diff, err = _git(root, "diff", "-U0", "--no-color", "--no-ext-diff", BASE, head, "--", path)
        if rc != 0 or not diff.strip():
            print("VERDICT: FAIL-OGA2-AC14 git diff %s %s -- %s rc=%d bytes=%d %s"
                  % (BASE, head, path, rc, len(diff), err.strip()))
            return 1
        named_text = srcs[AMEND_PIN].splitlines()[NAMED[path] - 1]
        problems, f = judge(srcs[BASE], srcs[head], diff, named_text)
        stmts += f["removed"]
        lines += len(f["assert_lines"][1])
        print("%s: assert statements base %d / HEAD %d, unmatched base %d / HEAD %d; diff vs base %d/%d lines"
              " (base/HEAD side), inside an assertion %d/%d"
              % (name, f["statements"][0], f["statements"][1], f["removed"], f["added"], f["lines"][0],
                 f["lines"][1], len(f["assert_lines"][0]), len(f["assert_lines"][1])))
        if "base_line" in f:
            print("  base  :%d  %s" % f["base_line"])
            print("  HEAD  :%d  %s" % f["head_line"])
            print("  named :%d @%s is the changed base assertion: %s"
                  % (NAMED[path], AMEND_PIN, "yes" if f["base_line"][1] == named_text.strip() else "NO"))
        if "email" in f:
            print("  original [\"sub\"] comparand %s -> HEAD [\"sub\"] %s, HEAD [\"email\"] %s"
                  % (f["email"], f["new_sub"], f["new_email"]))
        rc, since, err = _git(root, "diff", "-U0", "--no-color", "--no-ext-diff", AMEND_PIN, head, "--", path)
        if rc != 0:
            print("VERDICT: FAIL-OGA2-AC14 git diff %s %s -- %s rc=%d %s" % (AMEND_PIN, head, path, rc, err.strip()))
            return 1
        _, new_since = _hunks(since)
        head_spans = assertions(srcs[head])
        other = [n for n in sorted(new_since) if n not in set(_inside(head_spans, new_since))]
        print("  since %s: %d HEAD-side line(s) changed, %d inside an assertion; other: %s"
              % (AMEND_PIN, len(new_since), len(_inside(head_spans, new_since)),
                 ["%d %s" % (n, srcs[head].splitlines()[n - 1].strip()) for n in other] or "none"))
        rc_wt, _, _ = _git(root, "diff", "--quiet", "HEAD", "--", path)
        print("  worktree==HEAD: %s" % ("yes" if rc_wt == 0 else "no"))
        for p in problems:
            failed.append("%s: %s" % (name, p))
    print("across %d modules: assertion statements changed %d, assertion lines changed %d (3 and 3 required)"
          % (len(MODULES), stmts, lines))
    if stmts != 3 or lines != 3:
        failed.append("totals %d statements, %d lines (3 and 3 required)" % (stmts, lines))
    if failed:
        print("VERDICT: FAIL-OGA2-AC14 %s" % "; ".join(failed))
        return 1
    print("VERDICT: PASS-OGA2-AC14")
    return 0


if __name__ == "__main__":
    _VERBS = {"AC13": ac13, "AC14": ac14}
    if len(sys.argv) != 2 or sys.argv[1] not in _VERBS:
        print("usage: og_a2.py AC13 | AC14", file=sys.stderr)
        sys.exit(2)
    sys.exit(_VERBS[sys.argv[1]]())
