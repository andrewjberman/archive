"""IRPT_ANLREQ AR-y-469 AC2: does the packager build (make_packager) supply both audit ports from make_audit_source?

Stdlib only, offline, no AWS call. Reads reports/resident_installed.py by AST (never by text search) and looks inside the
function make_packager only: the packager's ports are built there (AMENDMENT 1; the wiring site is not resident_worker.py).
A port counts as supplied when the function passes it as a dict key, a keyword argument or a subscript assignment:
  audit_source  must be a call of make_audit_source (or a name bound to one), and make_audit_source must be imported;
  audit_put     must be a lambda whose body calls a put (put_object) or a name/attribute whose identifier contains "put".

  AUDIT-LIVE-WIRED-OK source=yes put=yes            (rc 0)
  AUDIT-LIVE-WIRED-BAD <why>                        (rc 1)

--selftest: removes each port from the parsed tree in memory, in turn. It prints CONTROL-FIRES only when the unmodified
module reads OK AND both removals read BAD; otherwise CONTROL-DOES-NOT-FIRE with the reason (rc 1).
"""
import ast
import copy
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
WORKER = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "reports" / "resident_installed.py"
BUILDER = "make_packager"
PORTS = ("audit_source", "audit_put")
SOURCE_MAKER = "make_audit_source"
PUT_NAME = re.compile(r"put", re.IGNORECASE)


def _name_of(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _port_key(node):
    """The port name a dict key, a keyword name or a subscript slice spells, or None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _supplied(tree):
    """-> {port: value node} for every site in the module that passes a port."""
    supplied = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if _port_key(key) in PORTS:
                    supplied.setdefault(_port_key(key), value)
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg in PORTS:
                    supplied.setdefault(keyword.arg, keyword.value)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and _port_key(target.slice) in PORTS:
                    supplied.setdefault(_port_key(target.slice), node.value)
    return supplied


def _bound_to_source_maker(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and _name_of(node.value.func) == SOURCE_MAKER:
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return names


def _imports_source_maker(tree):
    return any(isinstance(node, ast.ImportFrom) and any(alias.name == SOURCE_MAKER for alias in node.names)
               for node in ast.walk(tree))


def _builder(tree):
    """The make_packager FunctionDef of the module, or None."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == BUILDER:
            return node
    return None


def _check(tree):
    """-> (ok, source_flag, put_flag, why)."""
    scope = _builder(tree)
    if scope is None:
        return (False, False, False, "no %s function in resident_installed.py" % BUILDER)
    supplied = _supplied(scope)
    bound = _bound_to_source_maker(scope)
    imported = _imports_source_maker(scope)
    value = supplied.get("audit_source")
    source_ok = (value is not None and imported
                 and ((isinstance(value, ast.Call) and _name_of(value.func) == SOURCE_MAKER)
                      or (isinstance(value, ast.Name) and value.id in bound)))
    value = supplied.get("audit_put")
    put_ok = value is not None and (
        (isinstance(value, ast.Lambda) and isinstance(value.body, ast.Call) and PUT_NAME.search(_name_of(value.body.func) or ""))
        or (isinstance(value, (ast.Name, ast.Attribute)) and PUT_NAME.search(_name_of(value) or "")))
    reasons = []
    if not source_ok:
        reasons.append("audit_source is not supplied as make_audit_source(...) with make_audit_source imported"
                       if "audit_source" in supplied else "audit_source is not supplied by the packager call")
    if not put_ok:
        reasons.append("audit_put is not supplied as an S3 put function" if "audit_put" in supplied
                       else "audit_put is not supplied by the packager call")
    return (not reasons, source_ok, put_ok, "; ".join(reasons))


class _Strip(ast.NodeTransformer):
    """Removes one port from the tree: a dict entry, a keyword argument or a subscript assignment."""

    def __init__(self, port):
        self.port = port

    def visit_Dict(self, node):
        self.generic_visit(node)
        kept = [(k, v) for k, v in zip(node.keys, node.values) if _port_key(k) != self.port]
        node.keys = [k for k, _ in kept]
        node.values = [v for _, v in kept]
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        node.keywords = [kw for kw in node.keywords if kw.arg != self.port]
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        if any(isinstance(t, ast.Subscript) and _port_key(t.slice) == self.port for t in node.targets):
            return None
        return node


def _parse(path=WORKER):
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _line(result):
    ok, source_flag, put_flag, why = result
    if ok:
        return "AUDIT-LIVE-WIRED-OK source=%s put=%s" % ("yes" if source_flag else "no", "yes" if put_flag else "no")
    return "AUDIT-LIVE-WIRED-BAD " + why


def selftest():
    tree = _parse()
    baseline = _check(tree)
    print(_line(baseline))
    if not baseline[0]:
        print("CONTROL-DOES-NOT-FIRE baseline=BAD (the unmodified module must read OK before a removal can be a control)")
        return 1
    for port in PORTS:
        removed = _check(_Strip(port).visit(copy.deepcopy(tree)))
        print("REMOVED %s -> %s" % (port, _line(removed)))
        if removed[0]:
            print("CONTROL-DOES-NOT-FIRE removal of %s still reads OK" % port)
            return 1
    print("CONTROL-FIRES removed=%s" % ",".join(PORTS))
    return 0


def main(argv):
    if argv[1:] == ["--selftest"]:
        return selftest()
    result = _check(_parse())
    print(_line(result))
    return 0 if result[0] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
