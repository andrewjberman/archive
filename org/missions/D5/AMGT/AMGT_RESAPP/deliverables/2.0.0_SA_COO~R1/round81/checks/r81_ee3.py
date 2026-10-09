"""AMGT_RESAPP round 81 -- AMGT-ee-3, PyMuPDF imported only where a PDF is read (CTO~DELL1 round-80 analysis R1 fallback).

  python r81_ee3.py --crit AC1|AC2

AC1 (build): in a fresh interpreter where `fitz` is made UNIMPORTABLE (a meta-path finder that raises ImportError for it),
    `import lib.research.filings.document`, `...fetch` and `...analyze` all succeed, and `document.cut` still cuts a 10-K
    plant; `fitz` appears in document.py only inside function bodies (no module-level import).
AC2 (bound): with a stub `fitz` on the path, the whole filings test folder passes (0 failed).
Verdict: R81 EE3 ACn SERVED: YES|NO (exit 0|1). At the base (2026-10-09) AC1 reads NO (document.py:56 imports fitz at the top).
"""
from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
import tempfile

BLOCK = r'''
import sys
class _NoFitz:
    def find_spec(self, name, path=None, target=None):
        if name == "fitz" or name.startswith("fitz.") or name == "pymupdf" or name.startswith("pymupdf."):
            raise ImportError("fitz blocked by r81_ee3")
        return None
sys.meta_path.insert(0, _NoFitz())
import lib.research.filings.document as d
import lib.research.filings.fetch
import lib.research.filings.analyze
text = "PART I\nItem 1A. Risk Factors\n" + ("A risk sentence about the business and nothing else. " * 60) + "\nItem 1B. Unresolved Staff Comments\nNone.\n"
s = d.cut(text, "10-K")
print("IMPORTS-OK risk_status=%s" % (s.get("risk", {}).get("status") if isinstance(s.get("risk"), dict) else type(s.get("risk")).__name__))
'''


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1(root):
    env = dict(os.environ, PYTHONPATH=root)
    p = subprocess.run([sys.executable, "-c", BLOCK], cwd=root, capture_output=True, text=True, env=env)
    tail = (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]
    r = [say(p.returncode == 0 and "IMPORTS-OK" in p.stdout, "F1 document, fetch and analyze import with fitz unimportable: %s" % tail[0][:160])]
    src = open(os.path.join(root, "lib/research/filings/document.py"), encoding="utf-8").read()
    top = [n for n in ast.parse(src).body if isinstance(n, (ast.Import, ast.ImportFrom))
           and any((a.name or "").split(".")[0] in ("fitz", "pymupdf") for a in n.names)]
    r.append(say(not top, "F2 no module-level fitz/pymupdf import in document.py (found %d)" % len(top)))
    return all(r)


def ac2(root):
    with tempfile.TemporaryDirectory() as stub:
        open(os.path.join(stub, "fitz.py"), "w").close()
        env = dict(os.environ, PYTHONPATH=stub + os.pathsep + root)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "lib/research/filings/tests"],
                           cwd=root, capture_output=True, text=True, env=env)
    last = (p.stdout.strip().splitlines() or [""])[-1]
    return say(p.returncode == 0 and " failed" not in last and "error" not in last, "B1 the filings test folder: %s" % last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2"])
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    ok = ac1(root) if a.crit == "AC1" else ac2(root)
    print("R81 EE3 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
