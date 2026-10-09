"""AMGT_RESAPP round-84 PREP -- the source `language` stamp (row AMGT_RESAPP-D1-W332-S1).

  python r84_language.py --crit AC1 [--cache DIR]

Drives the REAL `lib.research.filings.fetch.build_source_object` (the EDGAR-by-CIK path the store half runs) fully
OFFLINE: `latest_filing`, `http_get` and `html_to_text` are replaced in-process so the cached, already-extracted filing
text (default `.scratch/r82_20f/<KEY>.txt`, the round-82 cache) is the document, and `time.sleep` is a no-op. No SEC GET,
no store read or write, no model call. Whatever line in fetch.py stamps `language` is what is graded.

AC1:
    L1 each of the five cached 20-F filings (ASML_NA, BABA_US, NU_US, PBR_US, SAP_GY -- all English filings) is stamped `en`.
       At the base fetch.py:417 stamps from the head of the WHOLE text (its first 40,000 chars are the inline-XBRL fact
       header: tag names, URLs, dates), so BABA reads `pt` (`e` from "E-Commerce", `com` from URLs) and SAP `es`.
    L2 NEGATIVE CONTROL: a planted filing whose 40,000+-char header is stopword-free XBRL noise but whose cut sections are
       Portuguese prose is stamped `pt` -- a genuinely non-English filing must stay non-English, and a repair that simply
       hard-codes `en` fails here. At the base the head read sees only the noise and falls to `en`, so L2 FAILs too.
Verdict: R84 LANGUAGE AC1: YES|NO (exit 0|1). At the base it reads NO.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import types

NAMES = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity")

PT_PROSE = (
    "A Companhia atua no setor de energia e tem como objetivo gerar valor para os acionistas. "
    "Nossas atividades incluem a exploracao e a producao de petroleo e gas natural em aguas profundas, "
    "o refino, o transporte e a comercializacao de derivados. A empresa mantem uma estrategia de "
    "investimentos que prioriza os ativos de maior retorno e a reducao de custos. Os resultados do "
    "exercicio foram influenciados pela variacao do preco do petroleo e pela taxa de cambio. "
    "Para mais informacoes, veja as notas explicativas das demonstracoes financeiras. "
)


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _imports(root):
    if root and root not in sys.path:
        sys.path.insert(0, root)
    try:
        import fitz  # noqa: F401
    except Exception:
        sys.modules["fitz"] = types.ModuleType("fitz")  # PyMuPDF does not load on dell1; no PDF is read here
    from lib.research.filings import fetch as F
    return F


def _planted_pt():
    # The header carries NO stopword of any language (so the base's head-of-document read finds < 3 hits and falls to
    # "en"), and is longer than the detector's 40,000-char sample: only a stamp read from the cut sections sees `pt`.
    header = "20-F\nFY 00000 false true " + " ".join(
        "http://fasb.org/us-gaap/2025#FiniteLivedIntangibleAssetsNet 2025-04-01 2026-03-31 0" for _ in range(600))
    body = (
        "\nITEM 3. KEY INFORMATION\nD. Risk Factors\n" + PT_PROSE * 40
        + "\nITEM 4. INFORMATION ON THE COMPANY\nB. Business Overview\n" + PT_PROSE * 40
        + "\nITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS\n" + PT_PROSE * 40
        + "\nITEM 6. DIRECTORS, SENIOR MANAGEMENT AND EMPLOYEES\n" + PT_PROSE * 4
    )
    return header + body


def _stamp(F, key, text):
    """Run build_source_object offline on `text`; return (status, language, excerpt chars)."""
    located = {
        "resolved": True, "accession": "0000000000-26-000000", "accession_raw": "000000000026000000",
        "form": "20-F", "filing_date": "2026-01-01", "url": "offline://%s" % key, "primary_document": "%s.htm" % key,
        "entity_name": key,
    }
    saved = (F.latest_filing, F.http_get, F.html_to_text, F.time.sleep)
    F.latest_filing = lambda cik, form_expected, timeout=90: dict(located)
    F.http_get = lambda url, timeout=90, retries=2: text.encode("utf-8")
    F.html_to_text = lambda raw: text
    F.time.sleep = lambda s: None
    try:
        obj = F.build_source_object(key, 1, "20-F")
    finally:
        F.latest_filing, F.http_get, F.html_to_text, F.time.sleep = saved
    return obj.get("status"), obj.get("language"), ((obj.get("excerpt") or {}).get("chars"))


def ac1(root, cache):
    F = _imports(root)
    good = 0
    for key in NAMES:
        path = os.path.join(cache, key + ".txt")
        if not os.path.isfile(path):
            print("FAIL L1 %-16s no cached filing at %s" % (key, path))
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        status, lang, chars = _stamp(F, key, text)
        ok = status == "RESOLVED" and lang == "en"
        good += ok
        print("%s L1 %-16s status %s language %s (excerpt %s chars)" % ("PASS" if ok else "FAIL", key, status, lang, chars))
    l1 = good == len(NAMES)
    print("   L1 denominator: %d of %d cached English filings stamped en" % (good, len(NAMES)))
    status, lang, chars = _stamp(F, "PLANTED_PT", _planted_pt())
    l2 = status == "RESOLVED" and lang == "pt"
    print("%s L2 negative control: a planted Portuguese filing behind an XBRL-noise header is stamped %s (status %s, "
          "excerpt %s chars; want pt)" % ("PASS" if l2 else "FAIL", lang, status, chars))
    return l1 and l2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--cache", default=None)
    a = ap.parse_args()
    root = _root()
    cache = a.cache or os.path.join(root or ".", ".scratch", "r82_20f")
    ok = ac1(root, cache)
    print("R84 LANGUAGE AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
