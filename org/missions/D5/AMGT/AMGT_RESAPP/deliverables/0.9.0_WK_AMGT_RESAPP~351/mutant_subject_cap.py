"""AMGT-nn-3 BUILD mutant control -- the serve-time cap decorator is the load-bearing behaviour.

Runs the issuer's r89_subject_cap.py main() with scoped_amgt._with_subject_cap replaced by the identity function, so
read_peer_set serves the stored subject exactly as stored. Expected: C1 FAIL, C3 FAIL, C2 PASS, R89 SUBJECT CAP: NO,
exit 1 (the control FIRED). Re-runnable:
  PYTHONPATH=<repo root> python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~351/mutant_subject_cap.py
"""
import importlib.util
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", ".."))
CHECK = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_RESAPP", "deliverables",
                     "2.0.0_SA_COO~R1", "round89_prep", "checks", "r89_subject_cap.py")


def main():
    sys.path.insert(0, ROOT)
    from lib.research.api import scoped_amgt
    scoped_amgt._with_subject_cap = lambda served, security_key: served  # the mutant: no decorator
    spec = importlib.util.spec_from_file_location("r89_subject_cap", CHECK)
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    return check.main()


if __name__ == "__main__":
    sys.exit(main())
