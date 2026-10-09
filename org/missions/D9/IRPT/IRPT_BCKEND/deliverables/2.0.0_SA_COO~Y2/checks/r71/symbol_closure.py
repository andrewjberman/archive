"""Symbol closure of a built Lambda zip (IRPT_BCKEND round 71, issuer 2.0.0_SA_COO~Y2; row IRPT_BCKEND-D2-S16).

The build's import-closure gate proves every top-level MODULE an import names is packaged. It does not prove the NAME imported
from that module exists in the packaged copy. Release 4 failed exactly there: custody_submission.py did
`from composition import CUSTODY_POLICY_REVISION`, and the packaged composition.py (staged at an older pin) did not define it.

Usage: python symbol_closure.py <zip_path>
Reads every top-level *.py in the zip with ast (nothing is imported or executed). For each `from M import a, b` at module level
or inside functions (level 0, M a packaged top-level module, names not '*'), checks that each name is bound at the top level of
M (def, class, assignment, annotated assignment, import/import-from alias, or a name in M's __all__).
Prints one MISSING line per unresolved pair, then `symbol_closure modules=<n> pairs=<k> missing=<m>`, and `symbol_closure PASS` or
`symbol_closure FAIL` last.
"""
import ast
import sys
import zipfile


def top_level_bindings(tree):
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        names.add(n.id)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Import):
            for a in node.names:
                names.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                names.add(a.asname or a.name)
        elif isinstance(node, (ast.If, ast.Try)):
            # conditional / guarded definitions at top level count as bound
            for sub in ast.walk(node):
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    names.add(sub.name)
                elif isinstance(sub, ast.Assign):
                    for t in sub.targets:
                        if isinstance(t, ast.Name):
                            names.add(t.id)
                elif isinstance(sub, (ast.Import, ast.ImportFrom)):
                    for a in sub.names:
                        names.add((a.asname or a.name).split(".")[0])
    return names


def main():
    if len(sys.argv) != 2:
        print("usage: symbol_closure.py <zip_path>")
        print("symbol_closure FAIL")
        sys.exit(2)
    with zipfile.ZipFile(sys.argv[1]) as z:
        sources = {n[:-3]: z.read(n).decode("utf-8") for n in z.namelist() if n.endswith(".py") and "/" not in n}
    trees = {m: ast.parse(src, filename=m + ".py") for m, src in sources.items()}
    bound = {m: top_level_bindings(t) for m, t in trees.items()}
    pairs = missing = 0
    for m, tree in sorted(trees.items()):
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module in trees:
                for a in node.names:
                    if a.name == "*":
                        continue
                    pairs += 1
                    if a.name not in bound[node.module]:
                        missing += 1
                        print("MISSING %s.py:%d imports %s from %s" % (m, node.lineno, a.name, node.module))
    print("symbol_closure modules=%d pairs=%d missing=%d" % (len(trees), pairs, missing))
    print("symbol_closure %s" % ("PASS" if missing == 0 else "FAIL"))
    sys.exit(0 if missing == 0 else 1)


if __name__ == "__main__":
    main()
