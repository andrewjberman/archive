"""AR467-y-AC3 (IRPT_ANLREQ AR-y-467): the audit writer is called exactly once in the packager, after the attach, in the
commentary-ready path. Reads opal_packager.py BY AST (never imports it: no network, no AWS, no side effect).
Prints exactly one line: AUDIT-WIRED-OK calls=1 after_attach=yes, or AUDIT-WIRED-BAD <why>. ASCII only."""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[7]  # org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<this>/ -> repo root
PACKAGER = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research" / "opal_packager.py"
HANDLER = "handle_commentary_ready"
ATTACH = "_attach_commentary"
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


def verdict(source):
    """-> the one output line for a packager source text."""
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if HANDLER not in funcs:
        return "AUDIT-WIRED-BAD no %s in the packager" % HANDLER
    if ATTACH not in funcs or not _calls(funcs[ATTACH], "_attach"):
        return "AUDIT-WIRED-BAD %s does not carry the attach" % ATTACH
    writer_sites = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _callee(n) == WRITER]
    owners = [name for name, fn in funcs.items() if _calls(fn, WRITER)]
    calls = len(writer_sites)
    if calls != 1:
        return "AUDIT-WIRED-BAD writer calls=%d (want 1)" % calls
    if owners != [AUDIT_HELPER]:
        return "AUDIT-WIRED-BAD the writer call sits in %s (want %s)" % (owners, AUDIT_HELPER)
    handler_helper_calls = _calls(funcs[HANDLER], AUDIT_HELPER)
    if len(handler_helper_calls) != 1:
        return "AUDIT-WIRED-BAD %s calls the audit helper %d times in %s (want 1)" % (HANDLER, len(handler_helper_calls), HANDLER)
    attach_lines = [n.lineno for n in _calls(funcs[HANDLER], ATTACH)]
    if not attach_lines or handler_helper_calls[0].lineno <= max(attach_lines):
        return "AUDIT-WIRED-BAD the audit helper is not after the attach in %s" % HANDLER
    return "AUDIT-WIRED-OK calls=1 after_attach=yes"


def main():
    line = verdict(PACKAGER.read_text(encoding="utf-8"))
    print(line)
    return 0 if line.startswith("AUDIT-WIRED-OK") else 1


if __name__ == "__main__":
    sys.exit(main())
