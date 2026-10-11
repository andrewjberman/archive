"""AMGT-nn-2 BUILD mutant control: the round-89 peer identity check with the new decorator removed from the route.

Run from the repo root:  PYTHONPATH="$(pwd)" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~351/mutant_listed_decorator.py
Expected: FAIL I1 (0 of 7) and R89 PEER IDENTITY: NO, main rc=1.
"""
import importlib.util
import sys

from lib.research.api import scoped_amgt

CHECK = ("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round89_prep/checks/r89_peer_identity.py")
spec = importlib.util.spec_from_file_location("r89", CHECK)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

scoped_amgt._with_listed_identity = lambda served: served  # MUTANT: decorator removed from the route
sys.argv = ["r89", "--where", "local"]
rc = mod.main()
print("MUTANT main rc=%d" % rc)
