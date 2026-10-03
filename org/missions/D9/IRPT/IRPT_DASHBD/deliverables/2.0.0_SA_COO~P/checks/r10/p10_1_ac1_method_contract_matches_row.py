"""DB10-1-AC1 -- rows IRPT_DASHBD-W1-S19 and W2-S3: the dim_return_method contract declares EXACTLY the columns the producer's
method row emits, as a versioned bump with method_version 2 recorded.

Grades org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json:
  - contract_version "0.3.0"; `supersedes.contract_version` "0.2.0";
  - the set of `columns[].name` equals the set of string keys of the row dict literal in
    data/assets/scripts/gold/irpt_reporting/account_return_daily.py emit_method_row (read with ast, never run);
  - `method_versions` has an entry with method_version 2 whose text cites "batch 193".
Usage: python <this file> <repo_root>
"""
import ast
import json
import sys
from pathlib import Path

CONTRACT = "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"


def fail(msg):
    print("FAIL: " + msg)
    print("DB10-1-AC1 FAIL")
    sys.exit(1)


def row_keys(src):
    """The string keys of the largest dict literal inside emit_method_row that carries "method_version"."""
    tree = ast.parse(src)
    fn = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "emit_method_row"), None)
    if fn is None:
        return None
    best = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Dict):
            keys = {k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
            if "method_version" in keys and len(keys) > len(best):
                best = keys
    return best


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    c = json.loads((root / CONTRACT).read_text(encoding="utf-8"))
    if c.get("contract_version") != "0.3.0":
        fail("contract_version is %r, not 0.3.0" % c.get("contract_version"))
    if (c.get("supersedes") or {}).get("contract_version") != "0.2.0":
        fail("supersedes.contract_version is not 0.2.0")
    keys = row_keys((root / PRODUCER).read_text(encoding="utf-8"))
    if not keys:
        fail("no method row dict found in emit_method_row")
    cols = {x.get("name") for x in c.get("columns") or []}
    if cols != keys:
        fail("columns differ from the emitted row: contract-only %s, row-only %s" % (sorted(cols - keys), sorted(keys - cols)))
    mv2 = [m for m in c.get("method_versions") or [] if m.get("method_version") == 2]
    if len(mv2) != 1 or "batch 193" not in json.dumps(mv2[0]):
        fail("no single method_versions entry for 2 citing batch 193")
    print("OK: contract 0.3.0 supersedes 0.2.0; %d columns equal the emitted row's keys; method_version 2 recorded" % len(cols))
    print("DB10-1-AC1 PASS")


if __name__ == "__main__":
    main()
