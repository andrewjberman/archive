"""AMGT_RESAPP round-95 PREP -- the display-name casing of a short initialism (CTO round-94 analysis item 4).

  PYTHONPATH=<repo root> python r95_casing.py        (reads the crosswalk's registered names; no AWS write)

`scoped_amgt._clean_display_name` serves an ALL-CAPS name in title case, keeping the words DECLARED in `DISPLAY_NAME_ACRONYMS` upper. 'CSL LTD' (CSL_AU_Equity) is not
declared and serves 'Csl Ltd' (the CVO's L9 and the CTO's analysis: cosmetic, a short all-capitals initialism the registered name prints in capitals stays in capitals).
Measured 2026-10-11 over the 68 registered (crosswalk) names: exactly two carry an initialism the declared set lacks, CSL ('CSL LTD' -> 'Csl Ltd') and JD ('JD.COM INC-ADR'
-> 'Jd.Com Inc'); every other short token is a word (RIO, ELI, NIKE, VISA, UBER, COPA) or a legal or particle word the rule already handles.

    K1 'CSL LTD' is served 'CSL Ltd'.
    K2 'JD.COM INC-ADR' is served with its initialism in capitals: the cleaned name starts 'JD'.
    K3 the census: of the registered names, the names whose served form differs between the declared set WITHOUT 'CSL' and 'JD' and the set as it is now are
       exactly 'CSL LTD' and 'JD.COM INC-ADR' (every other registered name's casing is unchanged by the rule).
    K4 control: words that are not initialisms keep title case: 'ELI LILLY & CO' -> 'Eli Lilly & Co', 'RIO TINTO PLC' -> 'Rio Tinto PLC', 'NIKE INC -CL B' -> 'Nike Inc'.
    K5 control: a mixed-case name is served exactly as it was ('Banco Santander S.A.').
Verdict: R95 CASING: YES|NO (exit 0|1). At the base (2026-10-11): K1, K2, K3 FAIL; K4, K5 PASS.
"""
import sys

from lib.research.api import scoped_amgt

NEEDED = ("CSL", "JD")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    res = []
    clean = scoped_amgt._clean_display_name
    res.append(say(clean("CSL LTD") == "CSL Ltd", "K1 'CSL LTD' is served 'CSL Ltd'", repr(clean("CSL LTD"))))
    jd = clean("JD.COM INC-ADR")
    res.append(say(str(jd).startswith("JD"), "K2 'JD.COM INC-ADR' keeps its initialism in capitals", repr(jd)))
    registered = scoped_amgt._crosswalk_names()
    now = {v: clean(v) for v in registered.values()}
    saved = set(scoped_amgt.DISPLAY_NAME_ACRONYMS)
    try:
        scoped_amgt.DISPLAY_NAME_ACRONYMS.difference_update(NEEDED)
        before = {v: clean(v) for v in registered.values()}
    finally:
        scoped_amgt.DISPLAY_NAME_ACRONYMS.clear()
        scoped_amgt.DISPLAY_NAME_ACRONYMS.update(saved)
    changed = sorted(v for v in now if now[v] != before[v])
    res.append(say(changed == ["CSL LTD", "JD.COM INC-ADR"],
                   "K3 of %d registered names exactly CSL LTD and JD.COM INC-ADR depend on the two declared initialisms" % len(registered),
                   "changed %s" % changed))
    words = {"ELI LILLY & CO": "Eli Lilly & Co", "RIO TINTO PLC": "Rio Tinto PLC", "NIKE INC -CL B": "Nike Inc"}
    got = {k: clean(k) for k in words}
    res.append(say(got == words, "K4 control: words that are not initialisms keep title case", str(got)))
    res.append(say(clean("Banco Santander S.A.") == "Banco Santander S.A.", "K5 control: a mixed-case name is served as it was"))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R95 CASING: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
