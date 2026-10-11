"""AMGT_CORPUS round 45, CRPS-au-8 -- the FWD-16 census at a NAMED dossier method version. READ-ONLY. Issuer's file.

  PYTHONPATH=. python au8_fwd16_census.py <amgt-corpus-dossier/N>

Round 40's ap8_fwd16_census.py reads, for every resolved name, the stored dossier of 2026-09-29 against "the one the served reader picks
today" (`dossier._read_dossier_detail`, which picks among objects whose method_version equals `dossier.METHOD_VERSION`). This wrapper
sets `dossier.METHOD_VERSION` to the version asked for and then runs that script unchanged, so the same census reads the written /10
and the served /11 side by side. Nothing is written; every call is a store read.
"""
import os
import runpy
import sys

sys.path.insert(0, os.getcwd())

from lib.research.corpus import dossier  # noqa: E402

CENSUS = ("org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round40/ap8_fwd16_census.py")


def main(argv):
    version = argv[0]
    if not version.startswith("amgt-corpus-dossier/"):
        print("usage: au8_fwd16_census.py amgt-corpus-dossier/<N>")
        return 2
    dossier.METHOD_VERSION = version
    print("au8 METHOD_VERSION %s (module default was set aside)" % dossier.METHOD_VERSION)
    runpy.run_path(CENSUS, run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
