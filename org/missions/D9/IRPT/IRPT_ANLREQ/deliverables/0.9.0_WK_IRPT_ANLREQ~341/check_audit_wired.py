"""AR467-y-AC3 (IRPT_ANLREQ AR-y-467, AMENDMENT 2 S5): the audit is written after every successful attach through ONE shared
tail. Reads opal_packager.py BY AST (never imports it: no network, no AWS, no side effect).

The accepted shape: `_attach` is the shared attach tail; its audit-helper call (`_write_audit`) sits after its attach call
(`ports["attach"](...)`); `_attach` is called from exactly the two attach paths, handle_ready and handle_commentary_ready; the
helper is called from nowhere else; the writer (`write_audit`) is called once, inside the helper.

Prints exactly one line: AUDIT-WIRED-OK calls=1 after_attach=yes, or AUDIT-WIRED-BAD <why>. ASCII only."""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[7]  # org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<this>/ -> repo root
PACKAGER = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research" / "opal_packager.py"
ATTACH_PATHS = ("handle_ready", "handle_commentary_ready")
TAIL = "_attach"
AUDIT_HELPER = "_write_audit"
WRITER = "write_audit"


def _callee(node):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _calls(node, name):
    return [n for n in ast.walk(node) if isinstance(n, ast.Call) and _callee(n) == name]


def _port_attach_lines(node):
    """The lines of `ports["attach"](...)`: the I5 call itself, the thing the audit must follow."""
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Subscript):
            sl = n.func.slice
            if isinstance(sl, ast.Constant) and sl.value == "attach":
                out.append(n.lineno)
    return out


def verdict(source):
    """-> the one output line for a packager source text."""
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in ATTACH_PATHS + (TAIL, AUDIT_HELPER):
        if name not in funcs:
            return "AUDIT-WIRED-BAD no %s in the packager" % name
    writer_sites = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _callee(n) == WRITER]
    if len(writer_sites) != 1:
        return "AUDIT-WIRED-BAD writer calls=%d (want 1)" % len(writer_sites)
    writer_owners = [name for name, fn in funcs.items() if _calls(fn, WRITER)]
    if writer_owners != [AUDIT_HELPER]:
        return "AUDIT-WIRED-BAD the writer call sits in %s (want %s)" % (writer_owners, AUDIT_HELPER)
    helper_sites = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _callee(n) == AUDIT_HELPER]
    helper_owners = [name for name, fn in funcs.items() if _calls(fn, AUDIT_HELPER)]
    if len(helper_sites) != 1 or helper_owners != [TAIL]:
        return "AUDIT-WIRED-BAD the audit helper is called %d time(s) in %s (want 1 in %s)" % (
            len(helper_sites), helper_owners, TAIL)
    attach_owners = sorted(name for name, fn in funcs.items() if _calls(fn, TAIL))
    if attach_owners != sorted(ATTACH_PATHS):
        return "AUDIT-WIRED-BAD %s is called from %s (want the two attach paths %s)" % (TAIL, attach_owners, list(ATTACH_PATHS))
    port_lines = _port_attach_lines(funcs[TAIL])
    helper_lines = [n.lineno for n in _calls(funcs[TAIL], AUDIT_HELPER)]
    if len(port_lines) != 1 or not helper_lines or min(helper_lines) <= port_lines[0]:
        return "AUDIT-WIRED-BAD the audit helper is not after the attach call in %s" % TAIL
    return "AUDIT-WIRED-OK calls=1 after_attach=yes"


def main():
    line = verdict(PACKAGER.read_text(encoding="utf-8"))
    print(line)
    return 0 if line.startswith("AUDIT-WIRED-OK") else 1


if __name__ == "__main__":
    sys.exit(main())
