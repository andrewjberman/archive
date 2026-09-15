"""OG-a-3 probe (0.9.0_WK_NFRA_OPLGTW~3), TO-OG-a-3 as amended @6886ddd314.

AC8 (one-time record): at this cell's HEAD, the served route table equals the table at the cut base 7459929520
plus exactly the paths in BROWSER_PATHS.json, none removed or changed. Three readings:
  - the route declarations of app/server.py at the cut base and at HEAD, each read from its git object by AST
    (kind, path, served methods, and the whole declaration's structural dump, so a changed handler, method
    list or keyword is a CHANGED route);
  - BROWSER_PATHS.json read from its git object at HEAD;
  - the route table the app actually serves, imported from the worktree (which must equal HEAD under app/),
    which must equal the HEAD declarations row for row.
A route table at HEAD passes only when it is the base table, every base row unchanged and in order, plus
exactly the listed (path, methods) rows. The judge is controlled first against six synthetic tables.

AC10 (discriminating): the diff of tests/test_principal_cutover.py against the cut base is exactly two added
ROUTE_CLASS entries, /schwab/download/login and /schwab/download/callback, each "public", and no other line.
Both vintages are read from git objects. Two instruments: the -U0 diff's lines (0 removed; every added line
inside ROUTE_CLASS at HEAD; the added lines, read as dict entries, are exactly the two entries), and the
module's AST (ROUTE_CLASS at HEAD = the base's entries unchanged plus the two; the module with ROUTE_CLASS
blanked is structurally identical at both vintages, so no assertion or other statement moved). The judge is
controlled first against six synthetic modules.

A git read that fails or returns nothing is a FAIL, never an empty table.

Usage:  <python> og_a3.py AC8 | AC10
Prints the counts, then `VERDICT: PASS-OGA3-AC<n>` or `VERDICT: FAIL-OGA3-AC<n> <reason>`.
"""
from __future__ import annotations

import ast
import difflib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "7459929520"   # the cut base (OG-a-2 merged)
GATEWAY = "infra/aws/ec2/opal-gateway"
SERVER = GATEWAY + "/app/server.py"
CUTOVER = GATEWAY + "/tests/test_principal_cutover.py"
BROWSER_PATHS = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~3/BROWSER_PATHS.json"
NEW_ENTRIES = {"/schwab/download/login": "public", "/schwab/download/callback": "public"}
_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


# --- git ---------------------------------------------------------------------------------------------------
def _git(root, *args):
    proc = subprocess.run(["git", *args], cwd=str(root), capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")


def _root_head(tag):
    rc, top, err = _git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel")
    if rc != 0 or not top.strip():
        print("VERDICT: FAIL-%s git rev-parse --show-toplevel rc=%d %s" % (tag, rc, err.strip()))
        return None, None
    root = Path(top.strip())
    rc, head, err = _git(root, "rev-parse", "--short=10", "HEAD")
    if rc != 0 or not head.strip():
        print("VERDICT: FAIL-%s git rev-parse HEAD rc=%d %s" % (tag, rc, err.strip()))
        return None, None
    return root, head.strip()


def _show(root, rev, path):
    """(source, error): a failed or empty read is an error, never an empty source."""
    rc, src, err = _git(root, "show", "%s:%s" % (rev, path))
    if rc != 0 or not src.strip():
        return None, "git show %s:%s rc=%d bytes=%d %s" % (rev, path, rc, len(src), err.strip())
    return src, None


# --- AC8: the route tables -----------------------------------------------------------------------------------
def _eval_str(node, env):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name) and node.id in env:
        return env[node.id]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _eval_str(node.left, env) + _eval_str(node.right, env)
    raise ValueError(ast.dump(node))


def _constants(source):
    """The module-level string constants of a module (NAME = "..." / NAME = OTHER + "...")."""
    env = {}
    for node in ast.parse(source).body:
        target, value = None, None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target, value = node.targets[0].id, node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            target, value = node.target.id, node.value
        if target:
            try:
                env[target] = _eval_str(value, env)
            except ValueError:
                pass
    return env


def declared_routes(source, module_source):
    """[{kind, path, methods, endpoint, dump}] of `app = Starlette(routes=[...])`. `module_source(name)` returns
    the source of app/<name>.py at the same vintage, for a path written as <module>.<CONSTANT>."""
    routes = None
    for node in ast.walk(ast.parse(source)):
        if (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "app" for t in node.targets)
                and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "Starlette"):
            routes = next((k.value for k in node.value.keywords if k.arg == "routes"), None)
            break
    if routes is None:
        raise ValueError("no app = Starlette(routes=[...]) in the source")
    out, envs = [], {}
    for call in routes.elts:
        kind, first = call.func.id, call.args[0]
        if isinstance(first, ast.Constant):
            path = first.value
        elif isinstance(first, ast.Attribute) and isinstance(first.value, ast.Name):
            name = first.value.id
            if name not in envs:
                envs[name] = _constants(module_source(name))
            if first.attr not in envs[name]:
                raise ValueError("%s.%s is not a string constant of app/%s.py" % (name, first.attr, name))
            path = envs[name][first.attr]
        else:
            raise ValueError("unresolvable route path %s" % ast.dump(first))
        if kind == "Mount":
            methods = None
        else:
            listed = next((k.value for k in call.keywords if k.arg == "methods"), None)
            served = {e.value for e in listed.elts} if listed is not None else {"GET"}
            if "GET" in served:
                served.add("HEAD")
            methods = tuple(sorted(served))
        endpoint = ast.unparse(call.args[1]) if len(call.args) > 1 else ""
        out.append({"kind": kind, "path": path, "methods": methods, "endpoint": endpoint, "dump": ast.dump(call)})
    return out


def judge_tables(base, head, listed):
    """(problems, facts): head must be base (each row unchanged, in order) plus exactly the listed rows."""
    key = lambda r: (r["kind"], r["path"])  # noqa: E731
    head_keys = [key(r) for r in head]
    base_keys = [key(r) for r in base]
    dupes = sorted({k for k in head_keys if head_keys.count(k) > 1})
    by_key = {key(r): r for r in head}
    removed = [r["path"] for r in base if key(r) not in by_key]
    changed = [r["path"] for r in base if key(r) in by_key
               and (by_key[key(r)]["dump"] != r["dump"] or by_key[key(r)]["methods"] != r["methods"])]
    kept = [k for k in head_keys if k in set(base_keys)]
    in_order = kept == [k for k in base_keys if k in by_key]
    added = [r for r in head if key(r) not in set(base_keys)]
    added_set = {(r["path"], r["methods"]) for r in added}
    facts = {"base": len(base), "head": len(head), "added": [r["path"] for r in added], "removed": removed,
             "changed": changed, "in_order": in_order, "dupes": dupes, "listed": len(listed)}
    problems = []
    if dupes:
        problems.append("paths declared more than once at HEAD: %s" % dupes)
    if removed:
        problems.append("base routes removed: %s" % removed)
    if changed:
        problems.append("base routes changed: %s" % changed)
    if not in_order:
        problems.append("base routes out of their base order")
    if added_set != set(listed) or len(added) != len(listed):
        problems.append("added %s != listed %s" % (sorted(added_set, key=str), sorted(listed, key=str)))
    if len(head) != len(base) + len(listed):
        problems.append("HEAD %d routes != base %d + listed %d" % (len(head), len(base), len(listed)))
    return problems, facts


def _row(path, methods=("GET", "HEAD"), endpoint="h"):
    return {"kind": "Route", "path": path, "methods": methods, "endpoint": endpoint,
            "dump": "Route(%r, %s, %r)" % (path, endpoint, methods)}


def _control_tables():
    a, b, c, x, y, z = (_row(p) for p in ("/a", "/b", "/c", "/x", "/y", "/z"))
    b2 = _row("/b", ("POST",))
    listed = {("/x", ("GET", "HEAD")), ("/y", ("GET", "HEAD"))}
    base = [a, b, c]
    cases = (("base + the 2 listed", [a, b, x, y, c], True),
             ("base + the 2 listed + 1 more", [a, b, x, y, z, c], False),
             ("a base route removed", [a, x, y, c], False),
             ("a base route's methods changed", [a, b2, x, y, c], False),
             ("one listed route missing", [a, b, x, c], False),
             ("base routes reordered", [b, a, x, y, c], False))
    ok = True
    for label, head, expect in cases:
        passed = not judge_tables(base, head, listed)[0]
        print("table judge control: %s -> %s (expected %s)"
              % (label, "pass" if passed else "fail", "pass" if expect else "fail"))
        ok = ok and passed == expect
    return ok


class _NoEgress:
    """Refuses every non-loopback connect and name lookup while the app is imported; counts attempts."""

    def __init__(self):
        self.attempts = []

    def __enter__(self):
        self._connect, self._gai = socket.socket.connect, socket.getaddrinfo
        guard = self

        def connect(sock, address):
            host = address[0] if isinstance(address, tuple) else str(address)
            if host not in ("127.0.0.1", "::1", "localhost"):
                guard.attempts.append(("connect", host))
                raise OSError("probe refuses egress to %s" % host)
            return guard._connect(sock, address)

        def getaddrinfo(host, *args, **kw):
            if host not in (None, "127.0.0.1", "::1", "localhost"):
                guard.attempts.append(("getaddrinfo", host))
                raise socket.gaierror("probe refuses name lookup of %s" % host)
            return guard._gai(host, *args, **kw)

        socket.socket.connect, socket.getaddrinfo = connect, getaddrinfo
        return self

    def __exit__(self, *exc):
        socket.socket.connect, socket.getaddrinfo = self._connect, self._gai
        return False


def served_routes(root):
    """(kind, path, methods, endpoint) of the app imported from the worktree, config pointed at a temp dir."""
    tmp = tempfile.mkdtemp(prefix="og_a3_")
    for name, value in {"MOCK_GRAPH": "1", "AUDIT_PATH": os.path.join(tmp, "audit.jsonl"),
                        "TOKEN_CACHE_DIR": os.path.join(tmp, "cache"), "AUDIT_S3_BUCKET": "",
                        "AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing",
                        "AWS_SESSION_TOKEN": "testing", "AWS_DEFAULT_REGION": "us-east-1",
                        "AWS_CONFIG_FILE": os.path.join(tmp, "no-config"),
                        "AWS_SHARED_CREDENTIALS_FILE": os.path.join(tmp, "no-credentials")}.items():
        os.environ[name] = value
    os.environ.pop("AWS_PROFILE", None)
    sys.path.insert(0, str(root / GATEWAY))
    from starlette.routing import Mount
    with _NoEgress() as guard:
        import app.server as server
    out = []
    for r in server.app.routes:
        if isinstance(r, Mount):
            out.append(("Mount", r.path, None, type(r.app).__name__))
        else:
            out.append(("Route", r.path, tuple(sorted(r.methods or ())),
                        r.endpoint.__module__ + "." + r.endpoint.__qualname__))
    return out, guard.attempts


def ac8() -> int:
    if not _control_tables():
        print("VERDICT: FAIL-OGA3-AC8 table judge control misread")
        return 1
    root, head = _root_head("OGA3-AC8")
    if root is None:
        return 1
    print("HEAD %s, cut base %s" % (head, BASE))
    tables = {}
    for label, rev in (("base", BASE), ("HEAD", head)):
        src, err = _show(root, rev, SERVER)
        if err:
            print("VERDICT: FAIL-OGA3-AC8 %s" % err)
            return 1

        def module_source(name, _rev=rev):
            msrc, merr = _show(root, _rev, "%s/app/%s.py" % (GATEWAY, name))
            if merr:
                raise ValueError(merr)
            return msrc

        try:
            tables[label] = declared_routes(src, module_source)
        except ValueError as exc:
            print("VERDICT: FAIL-OGA3-AC8 %s declarations unreadable: %s" % (label, exc))
            return 1
    raw, err = _show(root, head, BROWSER_PATHS)
    if err:
        print("VERDICT: FAIL-OGA3-AC8 %s" % err)
        return 1
    entries = json.loads(raw)["paths"]
    listed = {(e["path"], tuple(sorted(e["methods"]))) for e in entries}
    print("BROWSER_PATHS.json @%s: %d entries, %d distinct (path, methods): %s"
          % (head, len(entries), len(listed), sorted(listed)))
    if len(listed) != len(entries):
        print("VERDICT: FAIL-OGA3-AC8 BROWSER_PATHS.json lists a path more than once")
        return 1
    problems, f = judge_tables(tables["base"], tables["HEAD"], listed)
    print("declared routes: base %d (git object %s), HEAD %d (git object %s)" % (f["base"], BASE, f["head"], head))
    print("added %d %s; removed %d %s; changed %d %s; base order kept: %s; duplicate paths %d"
          % (len(f["added"]), f["added"], len(f["removed"]), f["removed"], len(f["changed"]), f["changed"],
             "yes" if f["in_order"] else "NO", len(f["dupes"])))
    # The served table: the app imported from the worktree, which must be HEAD under the Gateway's app/.
    rc, status, serr = _git(root, "status", "--porcelain", "--", GATEWAY + "/app")
    if rc != 0:
        print("VERDICT: FAIL-OGA3-AC8 git status rc=%d %s" % (rc, serr.strip()))
        return 1
    if status.strip():
        print("VERDICT: FAIL-OGA3-AC8 the worktree's app/ differs from HEAD, so the served table is not HEAD's: %s"
              % status.strip().splitlines())
        return 1
    try:
        served, attempts = served_routes(root)
    except Exception as exc:  # noqa: BLE001 -- any import failure is a FAIL with its reason
        print("VERDICT: FAIL-OGA3-AC8 the app did not import: %s: %s" % (type(exc).__name__, exc))
        return 1
    declared = [(r["kind"], r["path"], r["methods"]) for r in tables["HEAD"]]
    same = [row[:3] for row in served] == declared
    browser_served = sorted((row[1], row[2]) for row in served if row[3].startswith("app.browser_oidc."))
    print("served routes (app imported from the worktree, app/ == HEAD): %d; equal to the HEAD declarations row "
          "for row (kind, path, methods): %s; served by app.browser_oidc: %s; egress attempts during import %d %s"
          % (len(served), "yes" if same else "NO", browser_served, len(attempts), attempts))
    if not same:
        problems.append("the served table differs from the HEAD declarations")
    if set(browser_served) != listed:
        problems.append("the routes served by app.browser_oidc %s != listed" % browser_served)
    if attempts:
        problems.append("egress attempted during import: %s" % attempts)
    if problems:
        print("VERDICT: FAIL-OGA3-AC8 %s" % "; ".join(problems))
        return 1
    print("VERDICT: PASS-OGA3-AC8")
    return 0


# --- AC10: the ROUTE_CLASS diff ------------------------------------------------------------------------------
def _route_class(tree):
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "ROUTE_CLASS" and isinstance(node.value, ast.Dict)):
            return node
    return None


def _diff_lines(diff_text):
    """(removed line texts, [(new line number, added line text)]) of a -U0 unified diff."""
    removed, added, new_no = [], [], None
    for line in diff_text.splitlines():
        m = _HUNK.match(line)
        if m:
            new_no = int(m.group(3))
            continue
        if line.startswith(("+++", "---")) or new_no is None:
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append((new_no, line[1:]))
            new_no += 1
    return removed, added


def judge_route_class(base_src, head_src, diff_text):
    """(problems, facts) of AC10: exactly the two NEW_ENTRIES added to ROUTE_CLASS, and no other line."""
    base_tree, head_tree = ast.parse(base_src), ast.parse(head_src)
    base_node, head_node = _route_class(base_tree), _route_class(head_tree)
    if base_node is None or head_node is None:
        return ["ROUTE_CLASS = {...} not found (base %s, HEAD %s)" % (base_node is not None, head_node is not None)], {}
    base_rc, head_rc = ast.literal_eval(base_node.value), ast.literal_eval(head_node.value)
    removed, added = _diff_lines(diff_text)
    span = (head_node.lineno, head_node.end_lineno)
    outside = [(n, t) for n, t in added if not span[0] <= n <= span[1]]
    try:
        added_entries = ast.literal_eval("{" + "\n".join(t for _, t in added) + "}") if added else {}
    except (SyntaxError, ValueError):
        added_entries = None
    new_keys = {k: head_rc[k] for k in head_rc if k not in base_rc}
    lost = sorted(k for k in base_rc if k not in head_rc)
    reclassed = sorted(k for k in base_rc if k in head_rc and head_rc[k] != base_rc[k])
    # The module with ROUTE_CLASS blanked, at both vintages: any other statement changed shows here.
    base_node.value, head_node.value = ast.Dict(keys=[], values=[]), ast.Dict(keys=[], values=[])
    rest_same = ast.dump(base_tree) == ast.dump(head_tree)
    facts = {"entries": (len(base_rc), len(head_rc)), "new": new_keys, "lost": lost, "reclassed": reclassed,
             "removed_lines": len(removed), "added_lines": added, "outside": outside,
             "added_entries": added_entries, "rest_same": rest_same, "span": span}
    problems = []
    if new_keys != NEW_ENTRIES:
        problems.append("ROUTE_CLASS gained %s (exactly %s required)" % (new_keys, NEW_ENTRIES))
    if lost or reclassed:
        problems.append("base entries removed %s / re-classed %s" % (lost, reclassed))
    if removed:
        problems.append("%d line(s) removed or changed: %s" % (len(removed), removed))
    if outside:
        problems.append("added line(s) outside ROUTE_CLASS: %s" % outside)
    if added_entries != NEW_ENTRIES:
        problems.append("the added lines read as %s, not exactly the two entries" % added_entries)
    if not rest_same:
        problems.append("the module outside ROUTE_CLASS changed structurally")
    return problems, facts


def _control_route_class():
    base = ('X = 1\nROUTE_CLASS = {\n    "/a": "public",\n}\n\n\ndef t():\n    assert X == 1\n')
    good = base.replace('    "/a": "public",\n',
                        '    "/a": "public",\n    "/schwab/download/login": "public",\n'
                        '    "/schwab/download/callback": "public",\n')
    cases = (("the two entries, public", good, True),
             ("one entry classed access", good.replace('callback": "public"', 'callback": "access"'), False),
             ("a third entry", good.replace('    "/schwab/download/login"', '    "/z": "public",\n'
                                                                           '    "/schwab/download/login"'), False),
             ("an assertion changed", good.replace("assert X == 1", "assert X == 2"), False),
             ("a base entry re-classed", good.replace('"/a": "public"', '"/a": "access"'), False),
             ("a comment added outside", good.replace("\n\ndef t", "\n# note\ndef t"), False))
    ok = True
    for label, head, expect in cases:
        diff = "".join(difflib.unified_diff(base.splitlines(True), head.splitlines(True), "a", "b", n=0))
        passed = not judge_route_class(base, head, diff)[0]
        print("ROUTE_CLASS judge control: %s -> %s (expected %s)"
              % (label, "pass" if passed else "fail", "pass" if expect else "fail"))
        ok = ok and passed == expect
    return ok


def ac10() -> int:
    if not _control_route_class():
        print("VERDICT: FAIL-OGA3-AC10 ROUTE_CLASS judge control misread")
        return 1
    root, head = _root_head("OGA3-AC10")
    if root is None:
        return 1
    print("HEAD %s, cut base %s, file %s" % (head, BASE, CUTOVER))
    srcs = {}
    for rev in (BASE, head):
        src, err = _show(root, rev, CUTOVER)
        if err:
            print("VERDICT: FAIL-OGA3-AC10 %s" % err)
            return 1
        srcs[rev] = src
    rc, diff, err = _git(root, "diff", "-U0", "--no-color", "--no-ext-diff", BASE, head, "--", CUTOVER)
    if rc != 0 or not diff.strip():
        print("VERDICT: FAIL-OGA3-AC10 git diff %s %s -- %s rc=%d bytes=%d %s"
              % (BASE, head, CUTOVER, rc, len(diff), err.strip()))
        return 1
    problems, f = judge_route_class(srcs[BASE], srcs[head], diff)
    if f:
        print("ROUTE_CLASS entries: base %d, HEAD %d; gained %s; removed %d; re-classed %d"
              % (f["entries"][0], f["entries"][1], f["new"], len(f["lost"]), len(f["reclassed"])))
        print("diff vs base: %d line(s) removed or changed, %d added (ROUTE_CLASS spans HEAD lines %d-%d)"
              % (f["removed_lines"], len(f["added_lines"]), f["span"][0], f["span"][1]))
        for n, text in f["added_lines"]:
            print("  +%d  %s" % (n, text.strip()))
        print("added lines outside ROUTE_CLASS %d; added lines read as entries: %s; module outside ROUTE_CLASS "
              "structurally identical at both vintages: %s"
              % (len(f["outside"]), f["added_entries"], "yes" if f["rest_same"] else "NO"))
    rc_wt, _, _ = _git(root, "diff", "--quiet", "HEAD", "--", CUTOVER)
    print("worktree==HEAD: %s" % ("yes" if rc_wt == 0 else "no"))
    if problems:
        print("VERDICT: FAIL-OGA3-AC10 %s" % "; ".join(problems))
        return 1
    print("VERDICT: PASS-OGA3-AC10")
    return 0


if __name__ == "__main__":
    _VERBS = {"AC8": ac8, "AC10": ac10}
    if len(sys.argv) != 2 or sys.argv[1] not in _VERBS:
        print("usage: og_a3.py AC8 | AC10", file=sys.stderr)
        sys.exit(2)
    sys.exit(_VERBS[sys.argv[1]]())
