"""AMGT_CORPUS round 24, CRPS-z-4 -- C-SLASH-SAFE-KEY finished in code. A static census plus two controls; read-only. The issuer's file.

(1) Every function (unless it carries the marker '# slash-safe: not a per-security path (<reason>)') under lib/research/ and integrations/bloomberg/research/ (tests excluded) whose OWN string literals
    (docstrings excluded) build one of the per-security path templates the research names. A site is ENCODED when the function
    references `slash_safe_key`, RAW otherwise.
(2) The encoder on BP/_LN_Equity and BRK/B_US_Equity: the encoded form carries no '/', and it round-trips.
(3) The planted control: a raw-slash partition refuses at opal_naming's segment check.

  -> 'z4 sites S encoded E raw R bp_encoded <form> brk_encoded <form> roundtrip True|False planted_refuses True|False'
     followed by one 'RAW <file>:<line> <function>' per raw site
"""
import ast
import re
import subprocess
from pathlib import Path

TOP = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
ROOTS = ["lib/research", "integrations/bloomberg/research"]
TEMPLATE = re.compile(r"(drafting/v1/|packs/|management/v1/|peers/v1/|posture/v1/|derived/model_block/|model_block_%s|model_block_\{|^derived/$|^derived/%s|%s_%s\.json)")
MARKER = "# slash-safe: not a per-security path"

sites, raw = 0, []
for root in ROOTS:
    for p in sorted((TOP / root).rglob("*.py")):
        if "tests" in p.parts or "__pycache__" in p.parts:
            continue
        try:
            src = p.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except (SyntaxError, UnicodeDecodeError):
            continue
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = fn.body[1:] if (fn.body and isinstance(fn.body[0], ast.Expr)
                                   and isinstance(getattr(fn.body[0], "value", None), ast.Constant)
                                   and isinstance(fn.body[0].value.value, str)) else fn.body
            strs, names = [], set()
            for stmt in body:
                for n in ast.walk(stmt):
                    if isinstance(n, ast.Constant) and isinstance(n.value, str):
                        strs.append(n.value)
                    elif isinstance(n, ast.Name):
                        names.add(n.id)
                    elif isinstance(n, ast.Attribute):
                        names.add(n.attr)
            if not any(TEMPLATE.search(s) for s in strs):
                continue
            seg = ast.get_source_segment(src, fn) or ""
            if MARKER in seg:
                continue
            sites += 1
            if "slash_safe_key" not in names:
                raw.append("%s:%d %s" % (p.relative_to(TOP).as_posix(), fn.lineno, fn.name))

import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("xw_z4", TOP / "lib/research/identity/crosswalk.py")
xw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xw)
bp = xw.slash_safe_key("BP/_LN_Equity")
brk = xw.slash_safe_key("BRK/B_US_Equity")
unsafe = getattr(xw, "from_slash_safe_key", None) or getattr(xw, "unslash_safe_key", None)
rt = "/" not in bp and "/" not in brk and (unsafe is None or (unsafe(bp) == "BP/_LN_Equity" and unsafe(brk) == "BRK/B_US_Equity"))
spec2 = importlib.util.spec_from_file_location("on_z4", TOP / "lib/opal_naming.py")
on = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(on)
try:
    on._segment("partition", "security_key=BP/_LN_Equity")
    refuses = False
except Exception:  # noqa: BLE001 -- any refusal is the pass
    refuses = True
print("z4 sites %d encoded %d raw %d bp_encoded %s brk_encoded %s roundtrip %s planted_refuses %s" % (
    sites, sites - len(raw), len(raw), bp, brk, rt, refuses))
for r in raw:
    print("RAW " + r)
