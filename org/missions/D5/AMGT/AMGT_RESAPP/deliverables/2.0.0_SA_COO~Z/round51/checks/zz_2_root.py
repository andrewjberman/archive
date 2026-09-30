"""AMGT_RESAPP round 51, AMGT-zz-2 AC1 -- price_axis_pull derives its root from its own tree; nothing outside that tree goes on sys.path
at import (CTO round-50 ruling 2, row Z-W1-S18; CLAUDE.md: derive, don't hardcode).

(a) STATIC: `integrations/bloomberg/research/price_axis_pull.py` carries no absolute-path literal for a repo root (no drive-letter path,
    no 'ajb_workspace', no 'Desktop' literal) -- at the cut, line 97 hardcodes r"C:\\Users\\Opal Bloomberg\\Desktop\\ajb_workspace".
(b) DYNAMIC: importing it in a clean subprocess (OPAL_WS_ROOT unset, cwd = this checkout's root) adds to sys.path ONLY entries inside
    this checkout (the module's own tree, `Path(__file__).parents[3]`); an entry pointing at any other checkout is a FAIL.
usage: python <this>   (from the repo root)"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MOD = Path("integrations/bloomberg/research/price_axis_pull.py")
LITERAL = re.compile(r"""['"][^'"\n]*(?:[A-Za-z]:[\\/]|ajb_workspace|[\\/]Desktop[\\/])[^'"\n]*['"]""")

PROBE = r"""
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "integrations", "bloomberg", "research"))
before = list(sys.path)
try:
    import price_axis_pull  # noqa: F401
    err = None
except Exception as exc:  # an import failure is reported, not hidden
    err = "%s: %s" % (type(exc).__name__, str(exc)[:160])
added = [p for p in sys.path if p not in before]
print(json.dumps({"added": added, "error": err}))
"""


def main():
    root = Path(os.getcwd()).resolve()
    src = MOD.read_text(encoding="utf-8")
    hits = [(i + 1, m.group(0)[:90]) for i, line in enumerate(src.splitlines()) for m in LITERAL.finditer(line)]
    print("(a) hardcoded root literals in %s: %d %s" % (MOD, len(hits), hits[:3]))
    env = {k: v for k, v in os.environ.items() if k != "OPAL_WS_ROOT"}
    env["PYTHONPATH"] = str(root)
    p = subprocess.run([sys.executable, "-c", PROBE], cwd=str(root), env=env, capture_output=True, text=True, timeout=90)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        print("probe produced no JSON (rc=%s): %s" % (p.returncode, (p.stderr or p.stdout)[-200:]))
        print("PRICE_AXIS_PULL DERIVES ITS ROOT: NO")
        return 1
    outside = []
    for entry in out["added"]:
        try:
            Path(entry).resolve().relative_to(root)
        except ValueError:
            outside.append(entry)
    print("(b) import error: %s; sys.path entries added: %d, outside this checkout: %d %s" % (
        out["error"], len(out["added"]), len(outside), outside[:3]))
    ok = not hits and out["error"] is None and not outside
    print("PRICE_AXIS_PULL DERIVES ITS ROOT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
