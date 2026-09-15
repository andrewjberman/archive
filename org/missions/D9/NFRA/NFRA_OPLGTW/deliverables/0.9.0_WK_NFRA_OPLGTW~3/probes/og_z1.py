"""OG-z-1 probe (0.9.0_WK_NFRA_OPLGTW~3), TO-OG-z-1 as amended @a8a250297c.

AC14 (discriminating): the diff of tests/test_principal_cutover.py against the cut base 7f1ab996a0 is EMPTY, or
exactly ROUTE_CLASS entries for the routes this cell adds -- one per new path -- and no other line.

Readings, every one from a git object (a failed or empty read is a FAIL, never an empty table):
  - the route declarations of app/server.py at the cut base and at HEAD, by AST (og_a3.declared_routes), giving
    the paths this cell ADDED;
  - tests/test_principal_cutover.py at the cut base and at HEAD, and the -U0 diff between them;
  - the same file in the worktree, which must equal HEAD (so the file the criteria ran is the file judged).
A route added with no matching entry, an entry with no added route, a removed or re-classed base entry, or any
changed line outside ROUTE_CLASS is a FAIL. The judge is controlled first against seven synthetic cases.

Usage:  <python> og_z1.py AC14
Prints the counts and the added paths with their classes, then `VERDICT: PASS-OGZ1-AC14` or
`VERDICT: FAIL-OGZ1-AC14 <reason>`.
"""
from __future__ import annotations

import ast
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import og_a3  # noqa: E402 -- the OG-a-3 probe's git, route-table and diff readers, reused unchanged

BASE = "7f1ab996a0"   # the cut base (OG-a-3 merged)
GATEWAY = og_a3.GATEWAY
SERVER = og_a3.SERVER
CUTOVER = og_a3.CUTOVER


def judge(base_src, head_src, diff_text, added_paths):
    """(problems, facts): ROUTE_CLASS at HEAD = the base's entries unchanged plus exactly one entry per added path,
    and nothing else in the module moved."""
    base_tree, head_tree = ast.parse(base_src), ast.parse(head_src)
    base_node, head_node = og_a3._route_class(base_tree), og_a3._route_class(head_tree)
    if base_node is None or head_node is None:
        return ["ROUTE_CLASS = {...} not found (base %s, HEAD %s)" % (base_node is not None, head_node is not None)], {}
    base_rc, head_rc = ast.literal_eval(base_node.value), ast.literal_eval(head_node.value)
    removed, added = og_a3._diff_lines(diff_text)
    span = (head_node.lineno, head_node.end_lineno)
    outside = [(n, t) for n, t in added if not span[0] <= n <= span[1]]
    new_keys = {k: head_rc[k] for k in head_rc if k not in base_rc}
    lost = sorted(k for k in base_rc if k not in head_rc)
    reclassed = sorted(k for k in base_rc if k in head_rc and head_rc[k] != base_rc[k])
    base_node.value, head_node.value = ast.Dict(keys=[], values=[]), ast.Dict(keys=[], values=[])
    rest_same = ast.dump(base_tree) == ast.dump(head_tree)
    facts = {"entries": (len(base_rc), len(head_rc)), "new": new_keys, "lost": lost, "reclassed": reclassed,
             "removed_lines": removed, "added_lines": added, "outside": outside, "rest_same": rest_same,
             "added_paths": sorted(added_paths)}
    problems = []
    if set(new_keys) != set(added_paths):
        problems.append("ROUTE_CLASS gained %s but the routes added are %s" % (sorted(new_keys), sorted(added_paths)))
    if lost or reclassed:
        problems.append("base entries removed %s / re-classed %s" % (lost, reclassed))
    if removed:
        problems.append("%d line(s) removed or changed: %s" % (len(removed), removed))
    if outside:
        problems.append("added line(s) outside ROUTE_CLASS: %s" % outside)
    if len(added) != len(new_keys):
        problems.append("%d added line(s) for %d new entr(y/ies): one line per entry required" % (len(added), len(new_keys)))
    if not rest_same:
        problems.append("the module outside ROUTE_CLASS changed structurally")
    return problems, facts


def _controls():
    base = 'X = 1\nROUTE_CLASS = {\n    "/a": "public",\n}\n\n\ndef t():\n    assert X == 1\n'
    one = base.replace('    "/a": "public",\n', '    "/a": "public",\n    "/new": "access",\n')
    cases = (("no route added, file unchanged", base, set(), True),
             ("one route added, its one entry", one, {"/new"}, True),
             ("one route added, no entry", base, {"/new"}, False),
             ("an entry with no added route", one, set(), False),
             ("an assertion changed", base.replace("assert X == 1", "assert X == 2"), set(), False),
             ("a base entry re-classed", base.replace('"/a": "public"', '"/a": "access"'), set(), False),
             ("a comment added outside", base.replace("\n\ndef t", "\n# note\ndef t"), set(), False))
    ok = True
    for label, head, added_paths, expect in cases:
        diff = "".join(difflib.unified_diff(base.splitlines(True), head.splitlines(True), "a", "b", n=0))
        passed = not judge(base, head, diff, added_paths)[0]
        print("judge control: %s -> %s (expected %s)" % (label, "pass" if passed else "fail",
                                                           "pass" if expect else "fail"))
        ok = ok and passed == expect
    return ok


def _routes(root, rev):
    src, err = og_a3._show(root, rev, SERVER)
    if err:
        raise ValueError(err)

    def module_source(name):
        msrc, merr = og_a3._show(root, rev, "%s/app/%s.py" % (GATEWAY, name))
        if merr:
            raise ValueError(merr)
        return msrc
    return og_a3.declared_routes(src, module_source)


def ac14() -> int:
    if not _controls():
        print("VERDICT: FAIL-OGZ1-AC14 judge control misread")
        return 1
    root, head = og_a3._root_head("OGZ1-AC14")
    if root is None:
        return 1
    print("HEAD %s, cut base %s, file %s" % (head, BASE, CUTOVER))
    try:
        base_routes, head_routes = _routes(root, BASE), _routes(root, head)
    except ValueError as exc:
        print("VERDICT: FAIL-OGZ1-AC14 route declarations unreadable: %s" % exc)
        return 1
    base_paths = {r["path"] for r in base_routes}
    added_paths = {r["path"] for r in head_routes} - base_paths
    removed_paths = base_paths - {r["path"] for r in head_routes}
    print("server.py route declarations: base %d, HEAD %d; added by this cell %d %s; removed %d %s"
          % (len(base_routes), len(head_routes), len(added_paths), sorted(added_paths), len(removed_paths),
             sorted(removed_paths)))
    srcs = {}
    for rev in (BASE, head):
        src, err = og_a3._show(root, rev, CUTOVER)
        if err:
            print("VERDICT: FAIL-OGZ1-AC14 %s" % err)
            return 1
        srcs[rev] = src
    rc, diff, err = og_a3._git(root, "diff", "-U0", "--no-color", "--no-ext-diff", BASE, head, "--", CUTOVER)
    if rc != 0:
        print("VERDICT: FAIL-OGZ1-AC14 git diff %s %s -- %s rc=%d %s" % (BASE, head, CUTOVER, rc, err.strip()))
        return 1
    rc_wt, wt_diff, wt_err = og_a3._git(root, "diff", "--no-color", "--no-ext-diff", "HEAD", "--", CUTOVER)
    if rc_wt != 0:
        print("VERDICT: FAIL-OGZ1-AC14 git diff HEAD -- %s rc=%d %s" % (CUTOVER, rc_wt, wt_err.strip()))
        return 1
    problems, f = judge(srcs[BASE], srcs[head], diff, added_paths)
    if f:
        print("ROUTE_CLASS entries: base %d, HEAD %d; gained %s; removed %d; re-classed %d"
              % (f["entries"][0], f["entries"][1], f["new"], len(f["lost"]), len(f["reclassed"])))
        print("diff of %s, cut base %s -> HEAD %s: %d byte(s); %d line(s) removed or changed, %d added"
              % (CUTOVER, BASE, head, len(diff), len(f["removed_lines"]), len(f["added_lines"])))
        for path in sorted(f["new"]):
            print("  added path %s -> class %r" % (path, f["new"][path]))
        print("module outside ROUTE_CLASS structurally identical at both vintages: %s"
              % ("yes" if f["rest_same"] else "NO"))
    print("worktree == HEAD for the file: %s" % ("yes" if not wt_diff.strip() else "NO"))
    if wt_diff.strip():
        problems.append("the worktree's %s differs from HEAD" % CUTOVER)
    if not added_paths and diff.strip():
        problems.append("this cell adds no route, so the diff must be empty; it is %d byte(s)" % len(diff))
    if problems:
        print("VERDICT: FAIL-OGZ1-AC14 %s" % "; ".join(problems))
        return 1
    print("VERDICT: PASS-OGZ1-AC14")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "AC14":
        print("usage: og_z1.py AC14", file=sys.stderr)
        sys.exit(2)
    sys.exit(ac14())
