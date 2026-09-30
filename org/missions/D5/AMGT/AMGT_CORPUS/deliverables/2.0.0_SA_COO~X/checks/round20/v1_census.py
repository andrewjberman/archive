"""AMGT_CORPUS round 20, CRPS-v-1 -- the 3.9 floor: an AST census of every Path.write_text / Path.read_text call that passes
`newline=` (a keyword added in Python 3.10), over the ruling's root (lib/research/corpus/) and the root of the defect it names
(integrations/bloomberg/research/, where model_block_pull._ensure_unit_map lives). Read-only; the issuer's file.

  -> 'v1 newline_kw_calls C files_scanned F parse_errors E' then one 'HIT <path>:<line>' per call
"""
import ast
import subprocess
from pathlib import Path

TOP = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
ROOTS = ["lib/research/corpus", "integrations/bloomberg/research"]

files, hits, errors = 0, [], 0
for root in ROOTS:
    for p in sorted((TOP / root).rglob("*.py")):
        if "__pycache__" in p.parts:
            continue
        files += 1
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            errors += 1
            continue
        for n in ast.walk(tree):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("write_text", "read_text")
                    and any(k.arg == "newline" for k in n.keywords)):
                hits.append("%s:%d" % (p.relative_to(TOP).as_posix(), n.lineno))
print("v1 newline_kw_calls %d files_scanned %d parse_errors %d" % (len(hits), files, errors))
for h in hits:
    print("HIT " + h)
