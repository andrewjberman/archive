"""OPLGTW round 32 (R54) -- the tool-classification census, read STATICALLY (ast; nothing is imported or run).

Denominator: every function in infra/aws/ec2/opal-gateway/app/tools.py decorated with `@mcp.tool(...)`.
Classified: a name in destructive_ops.SAFE_TOOLS, or a key of DESTRUCTIVE_OPS or TOOL_WRITE_CLASS.
Prints the denominator, the classified count and every UNCLASSIFIED name (sorted), one per line.

  python tool_class_census.py <repo_root> [--worker-record <json>]

With --worker-record, the record's `unclassified` list must equal this census's list exactly.
Exit 0 and `RESULT: PASS` only when opal_asker_query is in SAFE_TOOLS, is not unclassified, and (when given)
the worker's record agrees with this census.
"""
import ast
import json
import sys
from pathlib import Path


def _decorated_tools(src: str) -> list:
    names = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                target = dec.func if isinstance(dec, ast.Call) else dec
                if isinstance(target, ast.Attribute) and target.attr == "tool" \
                        and isinstance(target.value, ast.Name) and target.value.id == "mcp":
                    names.append(node.name)
    return names


def _assigned(src: str, name: str):
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node.value
    return None


def _string_set(node) -> set:
    if isinstance(node, ast.Call) and node.args:      # frozenset({...})
        node = node.args[0]
    if isinstance(node, (ast.Set, ast.List, ast.Tuple)):
        return {e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)}
    if isinstance(node, ast.Dict):
        return {k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return set()


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    app = root / "infra/aws/ec2/opal-gateway/app"
    tools_src = (app / "tools.py").read_text(encoding="utf-8")
    dop_src = (app / "destructive_ops.py").read_text(encoding="utf-8")
    registered = sorted(set(_decorated_tools(tools_src)))
    safe = _string_set(_assigned(dop_src, "SAFE_TOOLS"))
    destructive = _string_set(_assigned(dop_src, "DESTRUCTIVE_OPS"))
    write_class = _string_set(_assigned(dop_src, "TOOL_WRITE_CLASS"))
    classified = safe | destructive | write_class
    unclassified = [n for n in registered if n not in classified]
    print("registered in tools.py (denominator): %d" % len(registered))
    print("SAFE_TOOLS %d, DESTRUCTIVE_OPS %d, TOOL_WRITE_CLASS %d" % (len(safe), len(destructive), len(write_class)))
    print("classified %d of %d; unclassified %d" % (len(registered) - len(unclassified), len(registered),
                                                   len(unclassified)))
    for n in unclassified:
        print("  UNCLASSIFIED: " + n)
    ok = True
    if "opal_asker_query" not in safe:
        print("opal_asker_query in SAFE_TOOLS: NO")
        ok = False
    else:
        print("opal_asker_query in SAFE_TOOLS: yes")
    if "--worker-record" in argv:
        rec_path = Path(argv[argv.index("--worker-record") + 1])
        if not rec_path.is_file():
            print("worker record absent: %s" % rec_path)
            ok = False
        else:
            rec = json.loads(rec_path.read_text(encoding="utf-8"))
            theirs = sorted(rec.get("unclassified", []))
            agree = theirs == unclassified and rec.get("registered") == len(registered)
            print("worker record agrees with this census: %s (record registered=%s, unclassified=%s)"
                  % ("yes" if agree else "NO", rec.get("registered"), theirs))
            ok = ok and agree
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
