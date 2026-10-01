"""AMGT_CORPUS round 28 CRPS-ad-4 -- which changed producer-dir files are in the act's IMPORT CLOSURE (aa-4 AMENDMENT 1).

Usage (repo root, PYTHONPATH=<root>;<root>/integrations/bloomberg/research): python -u ad4_closure.py <changed-files.txt>
  -> 'IN <path>' per changed file the act imports; 'ad4_closure changed C in_closure N'
"""
import os
import sys

import build_unit_map  # noqa: F401
import model_block_pull  # noqa: F401
from lib.research.corpus import dossier  # noqa: F401


def norm(p):
    return os.path.normcase(os.path.abspath(p))


changed = [line.strip() for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
loaded = {norm(m.__file__) for m in list(sys.modules.values()) if getattr(m, "__file__", None)}
inside = [c for c in changed if norm(c) in loaded]
for c in inside:
    print("IN %s" % c)
print("ad4_closure changed %d in_closure %d" % (len(changed), len(inside)))
