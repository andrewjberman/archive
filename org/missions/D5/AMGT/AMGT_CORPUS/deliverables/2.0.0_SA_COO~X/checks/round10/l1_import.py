"""AMGT_CORPUS round 10 -- l1_AC4's checker (amendment on 2.0.0_SA_COO~Z msg 26444). Writes nothing.

Imports `lib.research.corpus.dossier` in a fresh interpreter and reports whether a PDF library (fitz / pymupdf) was loaded
by that import, and whether `read_dossier` is still reachable.
"""
import sys
import warnings

warnings.simplefilter("ignore")
import lib.research.corpus.dossier as dossier  # noqa: E402

loaded = sorted(m for m in ("fitz", "pymupdf") if m in sys.modules)
print("l1 dossier_import pdf_libs_loaded %s read_dossier_callable %s"
      % (",".join(loaded) if loaded else "none", callable(getattr(dossier, "read_dossier", None))))
