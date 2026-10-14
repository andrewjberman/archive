"""Import proof: every .py closure member imported in its own clean `python -I -c` process, per firm, from the
extracted BUILT bundle tree. The closure is read by ast from the NEW-pin core file (not imported).

Usage: python -B import_proof.py <new_core_file> <scratch_new_dir> <out_json>
A module counts as imported only when the module it names resolves (__file__) to the member path inside that
firm's extracted tree; a stem that resolves to another file is recorded as an import error, not a pass.
"""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

core_file, new_dir, out_json = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
src = Path(core_file).read_text(encoding="utf-8")
closure = None
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_IRPT_HOLDINGS_CLOSURE" for t in node.targets):
        closure = [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
assert closure, "no closure tuple"
py_members = sorted(m for m in closure if m.endswith(".py"))

CHILD = r'''
import sys, json, importlib, os
from pathlib import Path
expect = os.path.normcase(os.path.abspath(sys.argv[1]))
stem = sys.argv[2]
dirs = sys.argv[3:]
sys.path[:0] = dirs
try:
    m = importlib.import_module(stem)
    got = os.path.normcase(os.path.abspath(getattr(m, "__file__", "") or ""))
    print(json.dumps({"stem": stem, "ok": got == expect, "file": got}))
except BaseException as e:
    print(json.dumps({"stem": stem, "ok": False, "error": type(e).__name__ + ": " + str(e)[:300]}))
'''

result = {}
for firm in ["49financial", "cottonwood", "inflection"]:
    tree = (new_dir / firm).resolve()
    member_dirs = sorted({str((tree / m).parent) for m in py_members} | {str(tree / "lib")})
    imported, errors, per_member = [], [], []
    for m in py_members:
        target = (tree / m)
        stem = Path(m).stem
        p = subprocess.run([sys.executable, "-I", "-c", CHILD, str(target), stem] + member_dirs,
                           capture_output=True, text=True, timeout=120)
        line = (p.stdout.strip().splitlines() or [""])[-1]
        try:
            rec = json.loads(line)
        except ValueError:
            rec = {"stem": stem, "ok": False, "error": "no JSON; rc=%d stderr=%s" % (p.returncode, p.stderr[-300:])}
        rec["member"] = m
        per_member.append(rec)
        if rec.get("ok") is True:
            imported.append(m)
        else:
            errors.append({"module": m, "error": rec.get("error", "unknown")})
    # count files in the tree, excluding interpreter bytecode caches
    files = []
    for root, dirs, fnames in os.walk(tree):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in fnames:
            files.append(os.path.relpath(os.path.join(root, f), tree).replace("\\", "/"))
    result[firm] = {
        "python_flags": "-I",
        "members_imported": sorted(imported),
        "import_errors": errors,
        "bundle_tree_members": len(files),
        "bundle_tree_files_sample_has_sums": "SHA256SUMS" in files,
        "py_members_attempted": len(py_members),
        "per_member": per_member,
    }
    print("%s imported=%d errors=%d tree_files=%d" % (firm, len(imported), len(errors), len(files)))
Path(out_json).write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
print("WROTE", out_json)
