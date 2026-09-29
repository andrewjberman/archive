"""AMGT_RESAPP round 47, AMGT-vv-2 AC2 -- THE TEAM-CASE READ RUNS WHERE THE LAMBDA RUNS: no PDF library in reach.

The deployed opal-amgt-scoped-api packages pyarrow but NOT PyMuPDF (fitz). With `fitz` and `pymupdf` made unimportable, importing
`lib.research.api.scoped_amgt` and calling `_team_cases("ASML_NA_Equity")` must succeed and return a dict with the three cases.
Today `lib.research.corpus.dossier` imports `extract` at module level and `extract.py:56` imports fitz -- so this check FAILS until
that import is deferred (asked of AMGT_CORPUS, which owns dossier.py; msg 20260929T045710Z).
usage: python <this>   (from the repo root)"""
import os
import sys

sys.modules["fitz"] = None      # an import of either now raises ImportError, as in the Lambda
sys.modules["pymupdf"] = None
sys.path.insert(0, os.getcwd())

try:
    from lib.research.api import scoped_amgt as sa
    got = sa._team_cases("ASML_NA_Equity")
    shape = sorted(got) if isinstance(got, dict) else type(got).__name__
    ok = isinstance(got, dict) and all(k in got for k in ("base", "upside", "downside"))
    print("with fitz/pymupdf unimportable: _team_cases -> %s" % shape)
except Exception as exc:  # the failure IS the reading
    ok = False
    print("with fitz/pymupdf unimportable: %s: %s" % (type(exc).__name__, str(exc)[:160]))
print("TEAM-CASE READ RUNS WITHOUT A PDF LIBRARY: %s" % ("YES" if ok else "NO"))
sys.exit(0 if ok else 1)
