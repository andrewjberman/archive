"""MUTANT CONTROL for IB-s-10.

Four claims this cell rests on, each mutated in a process that edits no production file. The
risk this addresses is specific and it is not hypothetical here: an extractor and its certifier
were written by the same author in the same hour, against specimens that author also generated.
Three of the four things being graded could agree with each other for the wrong reason.

  M1  certification ignores the value           -> "every number ties to the PDF at its
                                                   coordinates" must break
  M2  certification ignores the LABEL           -> a transposed column must stop being caught,
                                                   which is the leg value-at-coordinates cannot
                                                   reach
  M3  a chart-only region is given a number     -> "no number from a visual guess" must break
  M4  the date-line exclusion is removed        -> the extractor must go back to harvesting the
                                                   DAY OF THE MONTH and the YEAR as values, and
                                                   certifying them, because the digits really
                                                   are at those coordinates

M4 is the one worth reading twice. It is not a hypothetical: before the rule existed the
extractor located 42 values per synthetic variant instead of 26, and every one of the extra
sixteen CERTIFIED, because a date line's digits sit exactly where the extractor said they did.
A control that only mutated the certifier would never have found it.

Run: python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/
     IB-s-10_mutant_control.py
"""
import json
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
IR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
PKG = os.path.join(IR, "ycharts", "extract")
for p in (os.path.join(PKG, "tests"), PKG):
    sys.path.insert(0, p)

import certify                     # noqa: E402
import extract                     # noqa: E402
import run_offline_suite as suite  # noqa: E402

CEN = suite.census()
VARIANT = "comparison"
DATA = suite.synthetic_bytes(VARIANT)

# Captured ONCE, from the unmutated module, at import time.
DATE_TOPS = {p["page"]: extract._date_line_tops(p["words"])
             for p in extract.read_pages(DATA)}


def fresh():
    return extract.extract(DATA, CEN, specimen_label="synthetic",
                           specimen_id="synthetic-%s" % VARIANT)


def value_probe(label):
    r = fresh()
    dc = certify.difference_control(r, DATA, census=CEN)
    return {"label": label, "verdict": dc["verdict"], "field": dc["field"],
            "value_before": dc["value_before"], "value_after": dc["value_after"],
            "arm_c_value_predicate_holds": dc["verdict"] == certify.FAIL_VALUE}


def label_probe(label):
    r = fresh()
    tc = certify.transposed_label_control(r, DATA, census=CEN)
    return {"label": label, "verdict": tc["verdict"],
            "label_swapped_to": tc.get("label_swapped_to"),
            "arm_c_label_predicate_holds": tc["verdict"] == certify.FAIL_LABEL}


def chart_probe(label, *, poison=False):
    r = fresh()
    if poison and r["charts"]:
        r["charts"][0] = dict(r["charts"][0], value=45.57, _emitted_values=1)
    census_out = certify.chart_value_census(r)
    graded = certify.certify(r["charts"], DATA, census=CEN)
    return {"label": label, "numeric_values_emitted": census_out["numeric_values_emitted"],
            "chart_regions": census_out["chart_regions"],
            "cert_by_verdict": graded["by_verdict"],
            "arm_d_predicate_holds": census_out["holds"] and graded["all_certified"]}


def date_probe(label):
    """Did any emitted value come off a row that IS a 'Data as of:' line?

    Detected GEOMETRICALLY -- the row's own top compared against the date-line tops on its page
    -- rather than by guessing from the token's shape. The first cut of this probe flagged any
    token ending in a comma, and it reported 4 false positives on the BASELINE: they were
    fragments of a list value rendered across a column boundary, not dates at all. A probe whose
    positives you have to explain away is not measuring the thing it names, and in that instance
    the false positives were hiding a SECOND real defect (now NON_SCALAR_UNITS) behind noise
    attributed to the first.
    """
    r = fresh()
    g = certify.certify(r["sections"], DATA, census=CEN)
    # THE REFERENCE SET IS CAPTURED BEFORE ANY MUTATION AND NEVER RECOMPUTED HERE. The first cut
    # called extract._date_line_tops() at probe time -- the EXACT function M4 patches out -- so
    # the probe went blind in precisely the run it existed to measure and reported a clean 0 on
    # a mutant that had just harvested 17 extra values. A probe that shares a dependency with
    # the thing it grades cannot see a defect in what they share.
    harvested = [s for s in r["sections"]
                 if any(abs(s["bbox"][1] - t) <= 1.5 for t in DATE_TOPS.get(s["page"], []))]
    return {"label": label, "located": len(r["sections"]),
            "certified": g["certified"], "checked": g["checked"],
            "values_taken_from_a_date_line": len(harvested),
            "sample": [{"label": s["_label"], "value": s["value"], "token": s["_token"],
                        "page": s["page"]} for s in harvested[:3]],
            "arm_a_predicate_holds": len(harvested) == 0}


out = {
    "baseline_value": value_probe("baseline"),
    "baseline_label": label_probe("baseline"),
    "baseline_chart": chart_probe("baseline"),
    "baseline_date": date_probe("baseline"),
}

# ---- M1: certification stops checking the VALUE ----------------------------
real_forms = certify._render_forms
certify._render_forms = lambda value, token: {"", str(token or "")} | {str(value)}
try:
    # A renderer that always includes whatever is printed there would pass anything; the
    # honest mutation is to make the accepted set include the ORIGINAL token unconditionally,
    # which is exactly what a careless "compare against what we extracted" implementation does.
    certify._render_forms = lambda value, token: {str(token or "0.30%")}
    out["M1_value_check_ignores_the_value"] = value_probe("M1")
finally:
    certify._render_forms = real_forms

# ---- M2: certification stops checking the LABEL ----------------------------
real_grade = certify._grade_row


def labelless_grade(row, pages, units_declared):
    return real_grade({k: v for k, v in row.items() if k != "_label"}, pages, units_declared)


certify._grade_row = labelless_grade
try:
    out["M2_label_check_removed"] = label_probe("M2")
finally:
    certify._grade_row = real_grade

# ---- M3: a chart-only region is given a number -----------------------------
out["M3_chart_region_given_a_value"] = chart_probe("M3", poison=True)

# ---- M4: the date-line exclusion is removed --------------------------------
real_tops = extract._date_line_tops
extract._date_line_tops = lambda words, **kw: []
try:
    out["M4_date_line_exclusion_removed"] = date_probe("M4")
finally:
    extract._date_line_tops = real_tops

out["verdict"] = {
    "baseline_value_holds": out["baseline_value"]["arm_c_value_predicate_holds"],
    "M1_breaks_it": not out["M1_value_check_ignores_the_value"]["arm_c_value_predicate_holds"],
    "baseline_label_holds": out["baseline_label"]["arm_c_label_predicate_holds"],
    "M2_breaks_it": not out["M2_label_check_removed"]["arm_c_label_predicate_holds"],
    "baseline_chart_holds": out["baseline_chart"]["arm_d_predicate_holds"],
    "M3_breaks_it": not out["M3_chart_region_given_a_value"]["arm_d_predicate_holds"],
    "baseline_date_holds": out["baseline_date"]["arm_a_predicate_holds"],
    "M4_breaks_it": not out["M4_date_line_exclusion_removed"]["arm_a_predicate_holds"],
}
out["verdict"]["mutants_fired_as_expected"] = all(out["verdict"].values())
print(json.dumps(out, indent=1, sort_keys=True))
