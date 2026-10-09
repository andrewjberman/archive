"""AMGT_RESAPP round-82 PREP (DRAFT, not issued) -- the print PDF says "date not stored with this figure" ONCE.

  python r82_print.py --crit AC1|AC2

The PDF's Header block (`render_pack.build_pack`, :709-711) prints one line per header figure through `_plain_figure_line`,
and every numeric header figure without its own date carries the phrase on its own line (10-11 times per pack at the base).
The cell adds `render_pack._header_print_lines(header_figs, trading_currency, reporting_currency) -> list[str]`, the lines
build_pack prints under "Header", and makes build_pack print exactly those.

AC1 (build): on the STORED model block of AMD_US_Equity (read only, via scoped_amgt.read_model_block):
    P1 `_header_print_lines` exists;
    P2 the phrase appears exactly ONCE across the header lines;
    P3 a plant whose numeric header figures all carry `quote_date` -> 0 times (no date-less figure, nothing to say);
    P4 a plant whose header figures are text only -> 0 times.
AC2 (build, equivalence -- FAILS at the base by construction: it needs the new helper): every header line other than the one note equals today's `_plain_figure_line` output for the same figure with
    only its " - date not stored with this figure" segment removed (same figures, same order, same values and sources).
Verdict: R82 PRINT ACn: YES|NO (exit 0|1). At the base AC1 reads NO (P1 absent).
"""
from __future__ import annotations

import argparse
import subprocess
import sys

KEY = "AMD_US_Equity"
PHRASE = "date not stored with this figure"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _setup():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root not in sys.path:
        sys.path.insert(0, root)
    from lib.research.api import scoped_amgt as S
    from lib.research.print import render_pack as R
    block = S.read_model_block(KEY) or {}
    header = [f for f in (block.get("figures") or []) if f.get("scope") == "header"]
    tc = R._currency_of(header, "CRNCY", "EQY_FUND_CRNCY")
    rc = R._currency_of(header, "EQY_FUND_CRNCY", "CRNCY")
    return R, header, tc, rc


def ac1():
    R, header, tc, rc = _setup()
    has = hasattr(R, "_header_print_lines")
    r = [say(has, "P1 render_pack._header_print_lines exists")]
    if not has:
        return False
    lines = R._header_print_lines(header, tc, rc)
    n = sum(line.count(PHRASE) for line in lines)
    r.append(say(len(header) > 0 and n == 1, "P2 %s: the phrase appears %d time(s) across %d header line(s)" % (KEY, n, len(lines))))
    dated = [{"scope": "header", "mnemonic": "PX_LAST", "value": 10.0, "unit": "PRICE", "quote_date": "2026-10-08"},
             {"scope": "header", "mnemonic": "CUR_MKT_CAP", "value": 100.0, "unit": "MILLIONS", "as_of_date": "2026-10-08"}]
    n3 = sum(line.count(PHRASE) for line in R._header_print_lines(dated, "USD", "USD"))
    r.append(say(n3 == 0, "P3 every numeric header figure dated -> the phrase %d time(s)" % n3))
    text_only = [{"scope": "header", "mnemonic": "NAME", "value": "Plant Co", "unit": ""}]
    n4 = sum(line.count(PHRASE) for line in R._header_print_lines(text_only, "USD", "USD"))
    r.append(say(n4 == 0, "P4 text-only header -> the phrase %d time(s)" % n4))
    return all(r)


def ac2():
    R, header, tc, rc = _setup()
    if not hasattr(R, "_header_print_lines"):
        return say(False, "B1 render_pack._header_print_lines exists (needed to compare)")
    new_fig = [line for line in R._header_print_lines(header, tc, rc) if PHRASE not in line]  # the note is the one line with it
    old = [R._plain_figure_line(f, tc, rc).replace(" - " + PHRASE, "") for f in R._header_figures_for_print(header, tc, rc)]
    diff = [(a, b) for a, b in zip(old, new_fig) if a != b]
    ok = len(old) == len(new_fig) and not diff
    return say(ok, "B1 header figure lines equal today's minus the phrase: %d of %d equal %s" % (len(old) - len(diff), len(old), diff[:2]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2"])
    a = ap.parse_args()
    ok = ac1() if a.crit == "AC1" else ac2()
    print("R82 PRINT %s: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
