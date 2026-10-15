"""CA-l-4, the CTO's condition C1 (msg 109376, ruled (a) in msg 109378): before the act, scan every packaged .py for registry file names and require the set
to be a subset of the manifest, except names reachable ONLY behind `import opal_naming_rootcheck`, a module the build does not package.

Prints:  M4-SCAN ok=<True|False> named=<n> manifest=<n> outside=<n> excluded=<n> reason=<text>      then one line per name found and one per exclusion.
Run from the root of the checkout under test (the pinned worktree at the pin, built with build.sh so dist/pkg exists), by relative path:
    python "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r20/checks/check_m4_scan.py"
It reads the BUILT package when infra/aws/lambda/teams-chat-assist/dist/pkg exists (env M4_PKG overrides), else the source files build.sh copies.

Rules (the CTO's, verbatim in effect):
  1. A registry name is NAMED when a packaged .py holds a string constant equal to the file name, or a path ending /<name>, or the stem as a whole string constant,
     or the name inside any other string (a message or docstring: reported, not an open).
  2. Every NAMED name must be in registry_files.txt, OR be excluded: every mention of it lies in a function that itself contains `import opal_naming_rootcheck`
     or that is called, by name, only from functions that do (one level of callers inside the same module).
  3. The check prints each excluded name with the line of the import guard that makes it unreachable, and asserts opal_naming_rootcheck.py is NOT in the package.
     If that module is ever packaged, both names return to scope and this check fails.
No AWS, no network, nothing written. The repository is the git toplevel of the current directory (never this file's location); a plain directory works.
"""
import ast
import os
import subprocess
import sys
from pathlib import Path


def toplevel():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
    top = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else Path.cwd()
    return top if (top / "infra" / "aws" / "lambda" / "teams-chat-assist").is_dir() else Path.cwd()


ROOT = toplevel()
SRC = ROOT / "infra" / "aws" / "lambda" / "teams-chat-assist"
GUARD = "opal_naming_rootcheck"


def manifest():
    names = []
    for line in (SRC / "registry_files.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip().rstrip("\r")
        if line and not line.startswith("#"):
            names.append(line)
    return names


def packaged_py():
    pkg = Path(os.environ.get("M4_PKG") or SRC / "dist" / "pkg")
    if pkg.is_dir():
        return pkg, sorted(p for p in pkg.rglob("*.py"))
    files = [ROOT / "infra/aws/lambda/teams-chat-assist/handlers.py", ROOT / "infra/aws/terraform/modules/ldo/runtime/ldo.py",
             ROOT / "lib/opal_naming.py", ROOT / "daily_reports/eod/post_format.py"]
    files += sorted((ROOT / "data/transcripts/scripts/teams_chat").glob("*.py"))
    return None, files


def funcs_of(tree):
    """[(name, start, end, node)] for every function, innermost last."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append((n.name, n.lineno, getattr(n, "end_lineno", n.lineno), n))
    return out


def guard_lines(node):
    lines = []
    for n in ast.walk(node):
        if isinstance(n, ast.Import) and any(a.name == GUARD for a in n.names):
            lines.append(n.lineno)
        if isinstance(n, ast.ImportFrom) and n.module == GUARD:
            lines.append(n.lineno)
    return lines


def main():
    reg_dir = ROOT / "infra" / "logic" / "registry"
    reg = sorted(p.name for p in reg_dir.glob("*.json"))
    man = manifest()
    pkg, files = packaged_py()
    found = {}      # name -> [(file, line, enclosing function or None, kind)]
    guards = {}     # (file, function name) -> [guard lines]; filled for functions
    infos = {}
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(txt)
        except SyntaxError:
            continue
        fl = funcs_of(tree)
        infos[f] = (tree, fl)
        for name, s, e, node in fl:
            g = guard_lines(node)
            if g:
                guards[(f, name)] = g
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                v = n.value
                for r in reg:
                    stem = r[:-5]
                    if v == r or v.endswith("/" + r) or v == stem:
                        kind = "open"
                    elif r in v:
                        kind = "text"
                    else:
                        continue
                    spans = [(name, s, e) for name, s, e, _ in fl if s <= n.lineno <= e]
                    encl = min(spans, key=lambda t: t[2] - t[1]) if spans else None
                    found.setdefault(r, []).append((f, n.lineno, encl[0] if encl else None, kind))
    # raw-text pass: a name in a comment or in a string the AST pass did not see (a tuple split over lines, concatenation) is still NAMED
    for f in files:
        if f not in infos:
            continue
        fl = infos[f][1]
        seen_lines = {(r, ff, ln) for r, items in found.items() for (ff, ln, _, _) in items}
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for r in reg:
                if (r in line or ('"%s"' % r[:-5]) in line) and (r, f, i) not in seen_lines:
                    spans = [(name, a, b) for name, a, b, _ in fl if a <= i <= b]
                    encl = min(spans, key=lambda t: t[2] - t[1]) if spans else None
                    found.setdefault(r, []).append((f, i, encl[0] if encl else None, "text"))
    named = sorted(found)
    outside = [r for r in named if r not in man]

    def callers_of(f, fn):
        tree, fl = infos[f]
        out = set()
        for cname, cs, ce, cnode in fl:
            if cname == fn:
                continue
            for call in ast.walk(cnode):
                if isinstance(call, ast.Call):
                    t = call.func
                    nm = t.id if isinstance(t, ast.Name) else (t.attr if isinstance(t, ast.Attribute) else None)
                    if nm == fn:
                        out.add(cname)
                        break
        return out

    def guarded(f, fn, seen=None):
        """(True, guard line, chain) when fn has the guard import itself, or every caller of fn (same module) is guarded, transitively."""
        seen = seen or set()
        if fn in seen:
            return True, None, []                    # a cycle adds no new entry point
        seen = seen | {fn}
        g = guards.get((f, fn))
        if g:
            return True, g[0], [fn]
        cs = callers_of(f, fn) if f in infos else set()
        if not cs:
            return False, None, [fn]
        line, chain = None, [fn]
        for c in sorted(cs):
            ok, ln, ch = guarded(f, c, seen)
            if not ok:
                return False, None, [fn, c]
            line = line or ln
            chain = chain + ch
        return True, line, chain

    excluded, bad, notes = [], [], []
    for r in outside:
        why, ok = [], True
        for (f, line, fn, kind) in found[r]:
            if not fn:
                if kind == "open":
                    ok = False
                    why.append("%s:%d at module level (open)" % (f.name, line))
                else:
                    notes.append("%s: text mention at %s:%d at module level (not an open)" % (r, f.name, line))
                continue
            ok2, gl, chain = guarded(f, fn)
            if ok2:
                why.append("%s:%d (%s) in %s() reachable only via %s, behind `import %s` at line %s" % (
                    f.name, line, kind, fn, "->".join(dict.fromkeys(chain)), GUARD, gl))
            elif kind == "open":
                ok = False
                why.append("%s:%d in %s() REACHABLE (open)" % (f.name, line, fn))
            else:
                notes.append("%s: text mention at %s:%d in %s() (a message or docstring, not an open; not behind the guard)" % (r, f.name, line, fn))
        (excluded if ok else bad).append((r, why))
    pkg_has = bool(pkg) and any(p.name == GUARD + ".py" for p in pkg.rglob("*.py"))
    src_has = (ROOT / "lib" / (GUARD + ".py")).exists()
    for r in named:
        print("NAMED %-30s %s%s" % (r, "manifest" if r in man else "OUTSIDE", "" if r in man else ""))
    for r, why in excluded:
        for w in why:
            print("EXCLUDED %s: %s" % (r, w))
    for r, why in bad:
        for w in why:
            print("FAIL %s: %s" % (r, w))
    for note in notes:
        print("NOTE " + note)
    reason = []
    if bad:
        reason.append("name(s) outside the manifest reachable: %s" % ",".join(r for r, _ in bad))
    if pkg_has:
        reason.append("%s.py IS in the built package" % GUARD)
    if pkg is None:
        print("NOTE no dist/pkg: scanned the source files build.sh copies; the built-package assertion is skipped (source lib/%s.py exists=%s)" % (GUARD, src_has))
    if len(man) == 0:
        reason.append("manifest empty")
    ok = not reason
    print("M4-SCAN ok=%s named=%d manifest=%d outside=%d excluded=%d reason=%s"
          % (ok, len(named), len(man), len(outside), len(excluded), "; ".join(reason) or "none"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
