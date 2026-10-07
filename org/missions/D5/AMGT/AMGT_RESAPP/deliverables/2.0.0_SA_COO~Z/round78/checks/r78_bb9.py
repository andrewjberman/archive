"""AMGT_RESAPP round 78 -- AMGT-bb-9: the country served in plain case (round-77 enrichment item 7; DSGN_AMGTV1 FWD-27
ground 2, "Country: UNITED STATES").

  --crit AC1|AC2 --where local

AC1 (build): `lib.research.api.country_name`:
    C1 `plain_country` re-cases each of the 22 country values served today (measured over the 95 covered names):
       "UNITED STATES" -> "United States", "HONG KONG" -> "Hong Kong", "BRITAIN" -> "Britain", 22 of 22;
    C2 small words stay lower inside a name ("ISLE OF MAN" -> "Isle of Man", "TRINIDAD AND TOBAGO" ->
       "Trinidad and Tobago") and each side of a hyphen is cased ("GUINEA-BISSAU" -> "Guinea-Bissau");
    C3 a value that already carries a lower-case letter, an empty string and a non-string come back unchanged;
    C4 `with_plain_country(header_figures)` returns a NEW list: the COUNTRY_FULL_NAME entry is a copy whose `value` is
       plain and whose `value_as_stored` is the stored text; every other entry is the same object; the input list and
       its entries are not changed.
AC2 (seam, the real neighbour): the stored company record of BA_US_Equity, read by `scoped_amgt.read_model_block`, through
    `scoped_amgt._header_figures` and then `with_plain_country`: the country reads "United States", the stored text
    "UNITED STATES" is kept beside it, the entry count is unchanged and no other entry's value moved.
Verdict: R78 BB9 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import copy
import sys

SERVED_TODAY = {
    "BRAZIL": "Brazil", "BRITAIN": "Britain", "CANADA": "Canada", "CHINA": "China", "FINLAND": "Finland",
    "FRANCE": "France", "GERMANY": "Germany", "HONG KONG": "Hong Kong", "INDIA": "India", "ITALY": "Italy",
    "JAPAN": "Japan", "MEXICO": "Mexico", "NETHERLANDS": "Netherlands", "PANAMA": "Panama",
    "PHILIPPINES": "Philippines", "SINGAPORE": "Singapore", "SPAIN": "Spain", "SWEDEN": "Sweden",
    "SWITZERLAND": "Switzerland", "TAIWAN": "Taiwan", "UNITED STATES": "United States", "URUGUAY": "Uruguay",
}
SHAPES = {"ISLE OF MAN": "Isle of Man", "TRINIDAD AND TOBAGO": "Trinidad and Tobago", "GUINEA-BISSAU": "Guinea-Bissau",
          "SOUTH KOREA": "South Korea"}
MNEMONIC = "COUNTRY_FULL_NAME"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    try:
        from lib.research.api import country_name
    except ImportError as err:
        clause("C0 lib.research.api.country_name imports", False, str(err))
        return verdict(a, ok)
    plain = getattr(country_name, "plain_country", None)
    wrap = getattr(country_name, "with_plain_country", None)
    if not callable(plain) or not callable(wrap):
        clause("C0 country_name.plain_country and with_plain_country exist", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        miss = [(k, plain(k)) for k, v in sorted(SERVED_TODAY.items()) if plain(k) != v]
        clause("C1 the 22 country values served today read in plain case", not miss,
               f"{len(SERVED_TODAY) - len(miss)} of {len(SERVED_TODAY)}; wrong {miss[:4]}")
        miss = [(k, plain(k)) for k, v in sorted(SHAPES.items()) if plain(k) != v]
        clause("C2 small words stay lower and hyphen parts are cased", not miss, f"wrong {miss}")
        same = [plain("United States") == "United States", plain("") == "", plain(None) is None, plain(7) == 7]
        clause("C3 a plain, empty or non-text value comes back unchanged", all(same), repr(same))
        figures = [
            {"scope": "header", "mnemonic": "NAME", "value": "BOEING CO/THE"},
            {"scope": "header", "mnemonic": MNEMONIC, "value": "UNITED STATES", "unit": "TEXT (string field)"},
            {"scope": "header", "mnemonic": "CNTRY_OF_DOMICILE", "value": "US"},
        ]
        before = copy.deepcopy(figures)
        out = wrap(figures)
        entry = next((f for f in out if f.get("mnemonic") == MNEMONIC), {})
        clause("C4 the country entry is a re-cased copy and nothing else moves",
               out is not figures and figures == before and len(out) == 3 and entry.get("value") == "United States"
               and entry.get("value_as_stored") == "UNITED STATES" and entry.get("unit") == "TEXT (string field)"
               and out[0] is figures[0] and out[2] is figures[2] and entry is not figures[1], repr(entry))
        return verdict(a, ok)

    from lib.research.api import scoped_amgt

    block = scoped_amgt.read_model_block("BA_US_Equity")
    stored = scoped_amgt._header_figures(block)
    before = copy.deepcopy(stored)
    out = wrap(stored)
    entry = next((f for f in out if f.get("mnemonic") == MNEMONIC), {})
    was = next((f for f in before if f.get("mnemonic") == MNEMONIC), {})
    moved = [f.get("mnemonic") for f, g in zip(out, before) if f.get("mnemonic") != MNEMONIC and f.get("value") != g.get("value")]
    print(f"   BA US: header entries {len(before)} -> {len(out)}; stored country {was.get('value')!r}; "
          f"served {entry.get('value')!r}; kept beside it {entry.get('value_as_stored')!r}; other values moved {moved}")
    clause("C1 the real record's country reads in plain case with the stored text kept",
           was.get("value") == "UNITED STATES" and entry.get("value") == "United States"
           and entry.get("value_as_stored") == "UNITED STATES")
    clause("C2 the entry count is unchanged and no other value moved", len(out) == len(before) and len(before) >= 7 and not moved,
           f"{len(out)} of {len(before)}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB9 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
