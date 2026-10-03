"""RIV-nm-1 AC2 (RFW-D05, RFW-D11, RFW-U14 data half): one display name per security -- the full name, never a
30-character cut, never a raw ticker while a real name exists, ALL-CAPS re-cased by one rule.

Pure, offline. Interface: new module `rivalfunds/names.py`,
`display_name(candidates: list[str | None]) -> str | None`:
  1. blanks (None, empty, whitespace) are dropped. A RAW TICKER is a candidate matching '<id> <2 letters> Equity' or
     its key form '<id>_<2 letters>_Equity'; a REAL NAME is any other candidate;
  2. among the real names the longest wins, except that a candidate of exactly 30 characters ranks below every other
     real name (a suspected source cut); with no real name the first raw ticker is returned (nm-1 AC3);
  3. a winner with no lower-case letter is re-cased: every run of letters (an apostrophe inside a run does not end
     it) becomes upper-case first letter + lower-case rest: 'MITSUBISHI UFJ FINANCIAL GROUP' ->
     'Mitsubishi Ufj Financial Group', "MOODY'S CORP" -> "Moody's Corp", '3M CO' -> '3M Co',
     'S&P GLOBAL INC' -> 'S&P Global Inc'. A winner with any lower-case letter is returned unchanged (stripped).
Graded here:
  - RFW-D11: the 30-character cut loses to its full form, in either order (two names the walk saw cut on IDVZ);
  - RFW-D05: a real name beats a raw ticker, including a ticker LONGER than the name and the '_'-key form;
  - RFW-U14: 'INTUIT INC' and 'Intuit Inc' display identically, as 'Intuit Inc'; the re-casing pins above."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

KCM_CUT, KCM = "Kimberly-Clark de Mexico SAB d", "Kimberly-Clark de Mexico SAB de CV"
ICT_CUT, ICT = "International Container Termin", "International Container Terminal Services Inc"


def run(v):
    c.setup_path()
    from rivalfunds.names import display_name as dn

    print("cut lengths:", len(KCM_CUT), len(ICT_CUT))
    got = {"kcm": dn([KCM_CUT, KCM]), "kcm_rev": dn([KCM, KCM_CUT]),
           "ict": dn([ICT_CUT, ICT]), "ict_rev": dn([ICT, ICT_CUT])}
    print(got)
    v.check(got["kcm"] == got["kcm_rev"] == KCM,
            "the 30-character cut loses to 'Kimberly-Clark de Mexico SAB de CV' in either order")
    v.check(got["ict"] == got["ict_rev"] == ICT, "the 30-character cut loses to the full ICTSI name in either order")

    mufg = dn(["8306 JP Equity", "MITSUBISHI UFJ FINANCIAL GROUP"])
    shell = dn(["SHEL LN Equity", "SHELL PLC"])
    sie = dn(["SIE_GR_Equity", "Siemens AG"])
    print("mufg:", repr(mufg), "| shell:", repr(shell), "| sie:", repr(sie))
    v.check(mufg == "Mitsubishi Ufj Financial Group",
            "the real name beats '8306 JP Equity' and is re-cased by the rule")
    v.check(shell == "Shell Plc", "a real name beats a raw ticker even when the ticker is the longer string")
    v.check(sie == "Siemens AG",
            "a real name beats the key form 'SIE_GR_Equity'; a mixed-case name is returned unchanged")

    caps = {n: dn([n]) for n in ("INTUIT INC", "Intuit Inc", "MOODY'S CORP", "3M CO", "S&P GLOBAL INC")}
    print(caps)
    v.check(caps["INTUIT INC"] == caps["Intuit Inc"] == "Intuit Inc",
            "RFW-U14: 'INTUIT INC' and 'Intuit Inc' display as 'Intuit Inc'")
    v.check(caps["MOODY'S CORP"] == "Moody's Corp" and caps["3M CO"] == "3M Co"
            and caps["S&P GLOBAL INC"] == "S&P Global Inc",
            "re-casing: an apostrophe does not start a word; a digit-led or '&'-joined word keeps its capitals")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
