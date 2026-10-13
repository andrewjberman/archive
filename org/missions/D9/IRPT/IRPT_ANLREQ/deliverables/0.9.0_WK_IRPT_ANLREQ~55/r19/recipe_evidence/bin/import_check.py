"""Import check for the two reader members in the EXTRACTED package (outside the product tree).

Every `from X import a, b` (top-level and lazy, found by ast) in uploads.py and template_reader.py is resolved
against the package's own module path (the installer's sys.path order), and each name is checked with getattr.
Prints one line per import: OK or the ImportError / missing name. ASCII only.

usage: python -I import_check.py <package root>
"""
import ast
import importlib
import os
import sys

ROOT = os.path.abspath(sys.argv[1])
PATHS = ["intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract",
         "_scope", "_ids", "_contracts", "lib"]
for rel in reversed(PATHS):
    sys.path.insert(0, os.path.join(ROOT, rel))
sys.path.insert(0, os.path.join(ROOT, "intake"))

READERS = ["intake/uploads.py", "intake/template_reader.py"]
problems = 0
checked = 0
for rel in READERS:
    tree = ast.parse(open(os.path.join(ROOT, rel), encoding="utf-8").read(), filename=rel)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            try:
                mod = importlib.import_module(node.module)
            except Exception as exc:  # noqa: BLE001 - the instrument reports every failure
                problems += 1
                print("FAIL %s:%d import %s -> %s: %s" % (rel, node.lineno, node.module, type(exc).__name__, exc))
                continue
            for alias in node.names:
                checked += 1
                if not hasattr(mod, alias.name):
                    try:
                        importlib.import_module(node.module + "." + alias.name)
                    except Exception:  # noqa: BLE001
                        problems += 1
                        print("FAIL %s:%d %s has no name %s" % (rel, node.lineno, node.module, alias.name))
                        continue
                    print("note %s:%d %s.%s is a submodule" % (rel, node.lineno, node.module, alias.name))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                checked += 1
                try:
                    importlib.import_module(alias.name)
                except Exception as exc:  # noqa: BLE001
                    problems += 1
                    print("FAIL %s:%d import %s -> %s: %s" % (rel, node.lineno, alias.name, type(exc).__name__, exc))
print("from/import names checked %d, problems %d" % (checked, problems))
print("IMPORT-CHECK-OK" if problems == 0 else "IMPORT-CHECK-FAIL")
sys.exit(0 if problems == 0 else 1)
