"""LGIC_ENFORCE round 19, cell EN-h-1 -- re-measure the HAND side of FWD-5 clause 3.

WHAT THIS BUILDS, AND WHAT IT REFUSES TO DO
-------------------------------------------
FWD-5 clause 3: "the totals agree with the ranking the naming work produced by hand."
Round 9 compared the two sides and did not close: 143 compared, 109 agree, 34 disagree,
and 30 of the 34 named the HAND side as the defective one. This builder re-measures the
HAND side at the census vintage the MACHINE side already used, and re-runs the comparison.

THE MACHINE SIDE IS NEVER RE-GRADED. `grade_at_census` is read from round 9's record
byte-for-byte and never recomputed. Re-running grade() so it agrees with a stale hand
side is the REFUSED reading (the graded party grading its own reference), and this file
has no call to grade() anywhere in it.

THE HAND SIDE IS NOT COPIED FROM THE MACHINE SIDE EITHER. That would be the same defect
wearing the other hat. The hand products state a WRITTEN RULE (GRADING_RULE.md R1: the
V1/V2/V3 verdicts are read from REGISTRY rows, `DATA.rows_owner`), and they applied it
against a 2026-09-13/14 registry. Re-measuring the hand side therefore means RE-APPLYING
THE HAND'S OWN RULE AGAINST THE REGISTRY AT THE CENSUS VINTAGE -- and the deciding
registry fact is READ, per case, out of the census-vintage bytes:

    infra/logic/registry/systems.json    @54659987c0  (the token's vocabulary class)
    infra/logic/registry/resources.json  @54659987c0  (the resource-to-system row that
                                                       fills a {system} placeholder)
    org/standards/NAMING_SCHEMA.json     @54659987c0  (aws_fixed, which puts a name
                                                       outside the grade's domain)

A case whose deciding fact CANNOT be verified in those bytes is NOT resolved. It keeps
its disagreement and says why. That is what stops this builder from being a rubber stamp.

THE POPULATION IS THREE SURFACES, NOT ONE. "The hand ranking" is singular in the analysis
and in the register, and it is three artifacts. Re-measuring TENSION_RANKING.md alone
would do 10 of 143 and report a closed comparison with every printed figure correct.

POSITIVE CONTROL (`--control`): the comparator is first run over the UNREVISED hand side
and must reproduce round 9's triple exactly -- 143/109/34 -- before any revised figure is
believed. A comparator that cannot reproduce the number it is replacing has not been shown
to measure anything.

Run:  python build_hand_remeasure_r19.py            (control, then build, then write)
      python build_hand_remeasure_r19.py --control  (control only, writes nothing)
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=HERE).decode("utf-8").strip()

WORKER = "0.9.0_WK_LGIC_ENFORCE~1"
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/" + WORKER
R9_PATH = DELIV + "/HAND_COMPARISON_R9.json"
OUT_PATH = DELIV + "/HAND_REMEASURE_R19.json"

NAMING = "org/missions/D14/LGIC/LGIC_NAMING/deliverables"
GRADING_RULE = NAMING + "/GRADING_RULE.md"
N6_TSV = NAMING + "/exercises/n6-grader-a.tsv"
TENSION = NAMING + "/TENSION_RANKING.md"

SIB_GRADING = NAMING + "/GRADING_RULE.REMEASURED_R19.md"
SIB_N6 = NAMING + "/exercises/n6-grader-a.REMEASURED_R19.tsv"
SIB_TENSION = NAMING + "/TENSION_RANKING.REMEASURED_R19.md"

CENSUS_COMMIT = "54659987c0bd95069d57ab78e425b28678dc32fb"
CENSUS_VINTAGE = ("Built from the estate as of 2026-09-18 12:17:28 UTC. Stitch source: "
                  "stitch-codebuild built 2026-09-18T03:01:14Z. manifest 247f3933a1fd")
CENSUS_REPORT = DELIV + "/NAMING_CENSUS_REPORT.r8.md"

# Round 9's declared tolerance for the per-surface comparison, restated here so the
# re-run uses the bar that was declared BEFORE any figure was computed.
TOL_APPROX, TOL_EXACT, TOL_FLOOR = 0.15, 0.10, 2


def rp(rel):
    return os.path.join(ROOT, rel)


def read_text(rel):
    with io.open(rp(rel), encoding="utf-8") as fh:
        return fh.read()


def read_json(rel):
    return json.loads(read_text(rel))


def at_commit(rel):
    """The file's bytes AT THE CENSUS VINTAGE -- the hand side's re-measure reads the
    registry the machine side was graded against, never the worktree's current copy."""
    out = subprocess.check_output(
        ["git", "cat-file", "-p", "%s:%s" % (CENSUS_COMMIT, rel)], cwd=ROOT)
    return json.loads(out.decode("utf-8"))


# ------------------------------------------------------------------ denominators
def denominators():
    """RE-DERIVED AT THIS CELL'S WRITE TIME from the three ORIGINAL carriers, each by the
    instrument round 9 named. Not inherited: two carriers at HEAD still say 43 worked
    cases, which was true at GRADING_RULE.md@51b0952d71 and stopped being true when the
    v1.9 re-cut @fd6ce8c330 added mdpf-lambda-lambda and orion-orion-lambda-lambda."""
    out = {}

    text = read_text(GRADING_RULE)
    i = text.index("## 9. WORKED CASES")
    j = text.index("## 10.", i)
    fences = re.findall(r"```(?:json)?\n(.*?)\n```", text[i:j], re.S)
    if len(fences) != 1:
        raise SystemExit("ERROR: expected ONE json fence in GRADING_RULE.md section 9, "
                         "found %d" % len(fences))
    worked = json.loads(fences[0])["worked_cases"]
    out["grading_rule_worked_cases"] = {
        "instrument": ("len(worked_cases) of json.loads of the ONE json fence between "
                       "'## 9. WORKED CASES' and '## 10.' in " + GRADING_RULE +
                       ", re-read at this cell's write time"),
        "value": len(worked),
    }

    lines = [ln for ln in read_text(N6_TSV).splitlines() if ln.strip()]
    rows = [ln for ln in lines if not ln.startswith("# base")]
    out["n6_grader_rows"] = {
        "instrument": ("non-empty lines of " + N6_TSV + " after the '# base' header line, "
                       "split on TAB, re-read at this cell's write time; %d non-empty "
                       "lines = 1 header + %d rows" % (len(lines), len(rows))),
        "value": len(rows),
    }

    ranks = re.findall(r'\{"rank":\s*\d+', read_text(TENSION))
    out["tension_ranking_surfaces"] = {
        "instrument": ("count of '{\"rank\": N' rows in the json fence of " + TENSION +
                       ", re-read at this cell's write time"),
        "value": len(ranks),
    }
    return out


# ------------------------------------------------------------------ census-vintage facts
class CensusVintage(object):
    """The registry AS THE MACHINE SIDE SAW IT. Every hand-side revision below is
    justified by a read out of these bytes, never by grade()'s output."""

    def __init__(self):
        sysd = at_commit("infra/logic/registry/systems.json")
        self.system_keys = set(s["key"] for s in sysd["systems"])
        self.unresolved = set(u["token"] for u in sysd["unresolved"])
        self.refused = set()
        for value in sysd["refused_keys"].values():
            if isinstance(value, list):
                self.refused |= set(str(x) for x in value)
            elif isinstance(value, dict):
                self.refused |= set(str(x) for x in value.keys())

        res = at_commit("infra/logic/registry/resources.json")["resources"]
        self.resource_system = dict(((r["name"], r["type"]), r["system"]) for r in res)

        schema = at_commit("org/standards/NAMING_SCHEMA.json")
        self.aws_fixed_by_name = schema.get("aws_fixed", {}).get("by_name", {})

    def token_class(self, token):
        where = []
        if token in self.system_keys:
            where.append("systems.json key (V1)")
        if token in self.unresolved:
            where.append("systems.json unresolved (V2)")
        if token in self.refused:
            where.append("systems.json refused_keys (V3)")
        return where

    def aws_fixed_hit(self, name, rtype):
        for entry in self.aws_fixed_by_name.get(rtype, []):
            if entry.startswith("prefix: ") and name.startswith(entry[len("prefix: "):]):
                return entry
            if entry == name:
                return entry
        return None


TOKEN_RE = re.compile(r"puts the token .([a-z0-9_]+).")


def remeasure_named_case(case, cv):
    """Re-apply the HAND'S OWN WRITTEN RULE at the census vintage for ONE name.

    Returns (hand_verdict, hand_form, basis, evidence). `basis` is one of:
      UNCHANGED-AGREEING    the case already agreed; the re-measure does not move it
      REVISED-REGISTRY-ROW  a resource-to-system row at the census vintage fills {system}
      REVISED-TOKEN-CLASS   the deciding token's vocabulary row exists at the census vintage
      REVISED-AWS-FIXED     aws_fixed puts the name outside the grade's domain
      UNREVISED-MACHINE-SIDE   round 9 found the MACHINE side departs from the written
                               rule and the hand follows it -- the hand does not move
      UNREVISED-UNVERIFIED     the deciding fact could NOT be read at the census vintage
    """
    hv, hf = case["hand"]
    gv, gf = case["grade_at_census"]
    if case["result"] == "AGREE":
        return hv, hf, "UNCHANGED-AGREEING", "agreed at round 9; the re-measure does not move it"

    why = case.get("why", "") or ""

    # Round 9 found the MACHINE side departing from the WRITTEN rule. Re-measuring the
    # HAND side cannot close that, and this cell must not re-grade the machine side.
    if why.startswith("grade() SIDE"):
        return hv, hf, "UNREVISED-MACHINE-SIDE", (
            "round 9: the machine side departs from the written rule and the hand follows "
            "it; a hand-side re-measure cannot close a machine-side departure, and "
            "re-grading the machine side is refused on this cell")

    # (a) a {system} placeholder the registry now fills -- GRADING_RULE.md R1.d
    if hf and "{system}" in hf:
        sysv = cv.resource_system.get((case["name"], case["type"]))
        if sysv:
            return hv, hf.replace("{system}", sysv), "REVISED-REGISTRY-ROW", (
                "infra/logic/registry/resources.json @%s carries the row (%s, %s) -> "
                "system %s; GRADING_RULE.md R1.d says the placeholder stands only until "
                "the registry's resource-to-system row fills it"
                % (CENSUS_COMMIT[:10], case["name"], case["type"], sysv))

    # (b) a name aws_fixed puts outside the grade's domain -- G2.1 / section 9 `default`
    hit = cv.aws_fixed_hit(case["name"], case["type"])
    if hit and gv == "NOT-GRADED":
        return gv, gf, "REVISED-AWS-FIXED", (
            "org/standards/NAMING_SCHEMA.json @%s aws_fixed.by_name.%s carries %r, which "
            "puts this name outside the grade's domain (NOT-GRADED, never a RAISE)"
            % (CENSUS_COMMIT[:10], case["type"], hit))

    # (c) the deciding vocabulary row -- GRADING_RULE.md R1 reads V1/V2/V3 from the registry
    match = TOKEN_RE.search(why)
    if match:
        token = match.group(1)
        where = cv.token_class(token)
        if where:
            return gv, gf, "REVISED-TOKEN-CLASS", (
                "infra/logic/registry/systems.json @%s carries the token %r in %s; "
                "GRADING_RULE.md R1 reads V1/V2/V3 from REGISTRY rows (DATA.rows_owner), "
                "so the hand's own rule re-applied at the census vintage moves this verdict"
                % (CENSUS_COMMIT[:10], token, " + ".join(where)))
        return hv, hf, "UNREVISED-UNVERIFIED", (
            "round 9 named the token %r as deciding, but it could NOT be found in "
            "systems.json @%s -- the revision is not verified, so the disagreement stands"
            % (token, CENSUS_COMMIT[:10]))

    return hv, hf, "UNREVISED-UNVERIFIED", (
        "no deciding registry fact could be identified and verified at the census vintage; "
        "the hand value is left as written and the disagreement stands")


def agrees(hand, grade):
    """Round 9's agree_rule, unchanged: AGREE iff hand verdict == grade() verdict AND
    (hand gives no canonical form OR it equals grade()'s byte for byte)."""
    hv, hf = hand
    gv, gf = grade
    if hv != gv:
        return False
    return hf is None or hf == gf


def tolerance_for(fig):
    pct = TOL_APPROX if fig.get("hand_is_approx") else TOL_EXACT
    return max(float(TOL_FLOOR), pct * float(fig["hand"]))


# rank 5's two sides come from DIFFERENT INSTRUMENTS -- comp-find's drift_class over the
# live graph on the hand side, live-minus-repo on the census side. Round 9: "NEITHER SIDE
# IS SHOWN WRONG ... the census cannot reproduce the hand's figure". Re-quoting the census
# at a newer vintage cannot close an instrument gap, so this row is NOT revised.
INSTRUMENT_GAP_RANKS = (5,)


def build(cv, r9, control_only=False):
    surfaces, revisions, per_surface_detail = {}, [], {}
    dens = denominators()

    # ---------------- the two per-name surfaces
    for key, carrier, sibling in (
            ("grading_rule_worked_cases", GRADING_RULE, SIB_GRADING),
            ("n6_grader_rows", N6_TSV, SIB_N6)):
        src = r9["surfaces"][key]
        why_by = dict(((d["type"], d["name"]), d.get("why", ""))
                      for d in src["disagreements"])
        cases, agree, disagree = [], 0, 0
        for case in src["per_case"]:
            case = dict(case)
            case["why"] = why_by.get((case["type"], case["name"]), "")
            if control_only:
                hv, hf = case["hand"]
                basis, evidence = "CONTROL-UNREVISED", "positive control: hand side as written"
            else:
                hv, hf, basis, evidence = remeasure_named_case(case, cv)
            ok = agrees((hv, hf), case["grade_at_census"])
            agree += 1 if ok else 0
            disagree += 0 if ok else 1
            cases.append({
                "key": "%s::%s" % (case["type"], case["name"]),
                "name": case["name"], "type": case["type"],
                "hand_at_round_9": case["hand"],
                "hand_remeasured": [hv, hf],
                "grade_at_census_UNTOUCHED": case["grade_at_census"],
                "basis": basis, "evidence": evidence,
                "result": "AGREE" if ok else "DISAGREE",
                "round_9_result": case["result"],
            })
        surfaces[key] = {
            "carrier": carrier, "sibling_path": sibling,
            "compared": len(cases), "agree": agree, "disagree": disagree,
            "compared_keys": [c["key"] for c in cases],
            "denominator_measured_at_write_time": dens[key],
        }
        per_surface_detail[key] = cases
        revisions.append({
            "surface": key, "carrier": carrier, "sibling_path": sibling,
            "census_vintage": CENSUS_VINTAGE,
            "census_commit": CENSUS_COMMIT,
            "revised_cases": sum(1 for c in cases if c["basis"].startswith("REVISED")),
        })

    # ---------------- the per-surface tension ranking
    key = "tension_ranking_surfaces"
    src = r9["surfaces"][key]
    rows, agree, disagree = [], 0, 0
    for ps in src["per_surface"]:
        figs, within_all = [], True
        for fig in ps["figures"]:
            census = fig["census_r8_live"]
            if control_only or ps["rank"] in INSTRUMENT_GAP_RANKS:
                hand = fig["hand"]
                basis = ("CONTROL-UNREVISED" if control_only
                         else "UNREVISED-INSTRUMENT-GAP")
            else:
                # TENSION_RANKING.md's own instrument is "quote the naming census"; it
                # states "Nothing was measured again for this file". Re-measuring the hand
                # side is RE-RUNNING THAT INSTRUMENT at the r8 census vintage.
                hand = census
                basis = "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
            tol = tolerance_for(dict(hand=hand, hand_is_approx=fig.get("hand_is_approx")))
            ok = abs(float(census) - float(hand)) <= tol
            within_all = within_all and ok
            figs.append({
                "figure": fig["figure"], "hand_at_round_9": fig["hand"],
                "hand_remeasured": hand, "census_r8_live_UNTOUCHED": census,
                "tolerance": tol, "within": ok, "basis": basis,
            })
        agree += 1 if within_all else 0
        disagree += 0 if within_all else 1
        rows.append({"key": "rank-%d" % ps["rank"], "rank": ps["rank"],
                     "surface": ps["surface"], "figures": figs,
                     "result": "AGREE" if within_all else "DISAGREE",
                     "round_9_result": ps["result"]})
    surfaces[key] = {
        "carrier": TENSION, "sibling_path": SIB_TENSION,
        "compared": len(rows), "agree": agree, "disagree": disagree,
        "compared_keys": [r["key"] for r in rows],
        "denominator_measured_at_write_time": dens[key],
    }
    per_surface_detail[key] = rows
    revisions.append({
        "surface": key, "carrier": TENSION, "sibling_path": SIB_TENSION,
        "census_vintage": CENSUS_VINTAGE, "census_commit": CENSUS_COMMIT,
        "revised_cases": sum(1 for r in rows for f in r["figures"]
                             if f["basis"].startswith("REVISED")),
    })

    totals = {
        "compared": sum(s["compared"] for s in surfaces.values()),
        "agree": sum(s["agree"] for s in surfaces.values()),
        "disagree": sum(s["disagree"] for s in surfaces.values()),
    }
    return surfaces, revisions, per_surface_detail, totals


# ------------------------------------------------------------------ siblings
def write_siblings(detail, r9):
    head = ("<!-- ADDITIVE SIBLING. The original is READ-ONLY and not one byte of it "
            "moved.\n     Author: %s, LGIC_ENFORCE round 19, cell EN-h-1.\n"
            "     Hand side re-measured at the census vintage the MACHINE side used:\n"
            "       %s\n       %s @%s\n"
            "     The machine side is NOT re-graded here and grade() is never called.\n"
            "-->\n" % (WORKER, CENSUS_VINTAGE, CENSUS_REPORT, CENSUS_COMMIT[:10]))

    # --- GRADING_RULE sibling
    cases = detail["grading_rule_worked_cases"]
    body = {
        "vintage": CENSUS_VINTAGE,
        "note": ("Re-measured hand side of GRADING_RULE.md section 9's worked cases. Each "
                 "verdict/canonical_form is the WRITTEN RULE re-applied against the "
                 "registry at %s; `basis` names the row that decided it. The original "
                 "GRADING_RULE.md is unchanged." % CENSUS_COMMIT[:10]),
        "worked_cases": [{
            "name": c["name"], "type": c["type"],
            "verdict": c["hand_remeasured"][0],
            "canonical_form": c["hand_remeasured"][1],
            "verdict_at_round_9": c["hand_at_round_9"][0],
            "canonical_form_at_round_9": c["hand_at_round_9"][1],
            "basis": c["basis"], "evidence": c["evidence"],
        } for c in cases],
    }
    text = (head + "\n# GRADING_RULE -- WORKED CASES, HAND SIDE RE-MEASURED (round 19)\n\n"
            "Sibling of `%s`. %d worked cases, re-derived at this cell's write time.\n\n"
            "```json\n%s\n```\n" % (GRADING_RULE, len(cases),
                                    json.dumps(body, indent=1, ensure_ascii=False)))
    with io.open(rp(SIB_GRADING), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # --- n6 sibling (same 4-column TSV shape as the original)
    cases = detail["n6_grader_rows"]
    lines = ["# base %s  (census vintage; re-measured hand side, additive sibling of %s)"
             % (CENSUS_COMMIT, N6_TSV)]
    for c in cases:
        form = c["hand_remeasured"][1]
        lines.append("\t".join([c["type"], c["name"], c["hand_remeasured"][0],
                                "" if form is None else form]))
    with io.open(rp(SIB_N6), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")

    # --- TENSION sibling
    rows = detail["tension_ranking_surfaces"]
    orig = re.findall(r"```(?:json)?\n(.*?)\n```", read_text(TENSION), re.S)[0]
    orig_rows = dict((r["rank"], r) for r in json.loads(orig)["rows"])
    body = {
        "vintage": CENSUS_VINTAGE,
        "note": ("Re-measured hand side of TENSION_RANKING.md. The original states "
                 "'Nothing was measured again for this file' and quotes "
                 "infra/logic/09_NAMING_CENSUS.md of 2026-09-13; its instrument is "
                 "'quote the naming census', so the re-measure RE-RUNS THAT INSTRUMENT "
                 "at %s. Rank 5 is NOT re-quoted: its hand figure comes from comp-find's "
                 "drift_class over the live graph, which the census cannot reproduce, so "
                 "re-quoting would fabricate an agreement." % CENSUS_COMMIT[:10]),
        "rows": [{
            "rank": r["rank"],
            "surface": orig_rows[r["rank"]]["surface"],
            "cost": orig_rows[r["rank"]].get("cost"),
            "figures": [{
                "figure": f["figure"],
                "hand_remeasured": f["hand_remeasured"],
                "hand_at_round_9": f["hand_at_round_9"],
                "basis": f["basis"],
            } for f in r["figures"]],
            "result_against_the_census": r["result"],
        } for r in rows],
    }
    text = (head + "\n# TENSION RANKING -- HAND SIDE RE-MEASURED (round 19)\n\n"
            "Sibling of `%s`. %d ranked surfaces, re-quoted at the r8 census vintage.\n\n"
            "```json\n%s\n```\n" % (TENSION, len(rows),
                                    json.dumps(body, indent=1, ensure_ascii=False)))
    with io.open(rp(SIB_TENSION), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="LGIC_ENFORCE r19 EN-h-1 hand-side re-measure")
    ap.add_argument("--control", action="store_true",
                    help="run the positive control only; write nothing")
    args = ap.parse_args()

    r9 = read_json(R9_PATH)
    r9_totals = {"compared": 143, "agree": 109, "disagree": 34}

    # ---- POSITIVE CONTROL: reproduce round 9 from the UNREVISED hand side.
    _, _, _, ctl = build(None, r9, control_only=True)
    print("CONTROL (hand side unrevised, must reproduce round 9): %s" % json.dumps(ctl))
    print("CONTROL round 9 as recorded:                           %s" % json.dumps(r9_totals))
    if ctl != r9_totals:
        print("ERROR: the comparator does NOT reproduce round 9's triple. Every revised "
              "figure below would be unexplained. Refusing to write.")
        return 1
    print("OK: comparator reproduces round 9 exactly -- 143/109/34.")
    if args.control:
        return 0

    cv = CensusVintage()
    surfaces, revisions, detail, totals = build(cv, r9)

    base_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT).decode("utf-8").strip()

    record = {
        "_about": ("LGIC_ENFORCE round 19, cell EN-h-1. The HAND side of FWD-5 clause 3, "
                   "re-measured at the census vintage the MACHINE side used, across ALL "
                   "THREE hand surfaces. The machine side is read from round 9 and never "
                   "re-graded; grade() is not called anywhere in the builder."),
        "cell": "EN-h-1",
        "to": "LGIC_ENFORCE.TO-EN-h-1-r19",
        "worker": WORKER,
        "claim": "measured",
        "actor_base_sha": base_sha,
        "builder": DELIV + "/build_hand_remeasure_r19.py",
        "rerun_instrument": ("python " + DELIV + "/build_hand_remeasure_r19.py "
                             "(re-derives all three denominators from the ORIGINAL "
                             "carriers at write time, re-applies the hand's written rule "
                             "against the registry at " + CENSUS_COMMIT[:10] + ", and "
                             "re-runs round 9's agree_rule; --control reproduces round "
                             "9's 143/109/34 from the unrevised hand side first)"),
        "census_the_hand_side_was_re_measured_at": {
            "report": CENSUS_REPORT, "commit": CENSUS_COMMIT, "vintage": CENSUS_VINTAGE,
            "why": ("the machine side's own vintage. A hand figure re-measured against a "
                    "DIFFERENT vintage from the machine figure it is compared with "
                    "re-creates this defect one layer down."),
        },
        "agree_rule": r9["agree_rule"],
        "machine_side": {
            "regraded": False,
            "source": "round 9's grade_at_census / census_r8_live, read byte-for-byte",
            "why": ("re-running grade() so it agrees with a stale hand side is the REFUSED "
                    "reading -- the graded party grading its own reference"),
        },
        "positive_control": {
            "what": ("the comparator run over the UNREVISED hand side must reproduce round "
                     "9's triple before any revised figure is believed"),
            "result": ctl, "round_9_as_recorded": r9_totals,
            "passed": ctl == r9_totals,
        },
        "surfaces": surfaces,
        "revisions": revisions,
        "totals": totals,
        "round_9_totals": r9_totals,
        "surviving_disagreements": [],
        "per_case_detail": detail,
    }

    surviving = []
    for key in ("grading_rule_worked_cases", "n6_grader_rows"):
        for c in detail[key]:
            if c["result"] == "DISAGREE":
                surviving.append({"surface": key, "key": c["key"],
                                  "basis": c["basis"], "why": c["evidence"]})
    for r in detail["tension_ranking_surfaces"]:
        if r["result"] == "DISAGREE":
            surviving.append({"surface": "tension_ranking_surfaces", "key": r["key"],
                              "basis": "UNREVISED-INSTRUMENT-GAP",
                              "why": ("the hand figure and the census figure come from "
                                      "different INSTRUMENTS; re-quoting the census at a "
                                      "newer vintage cannot close an instrument gap")})
    record["surviving_disagreements"] = surviving

    with io.open(rp(OUT_PATH), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    write_siblings(detail, r9)

    print("")
    for key in sorted(surfaces):
        s = surfaces[key]
        print("  %-28s compared %3d  agree %3d  disagree %2d   (round 9: %d/%d/%d)"
              % (key, s["compared"], s["agree"], s["disagree"],
                 r9["surfaces"][key]["compared"], r9["surfaces"][key]["agree"],
                 r9["surfaces"][key]["disagree"]))
    print("  %-28s compared %3d  agree %3d  disagree %2d   (round 9: 143/109/34)"
          % ("TOTALS", totals["compared"], totals["agree"], totals["disagree"]))
    print("")
    print("SURVIVING DISAGREEMENTS: %d" % len(surviving))
    for s in surviving:
        print("  %-28s %-34s %s" % (s["surface"], s["key"], s["basis"]))
    print("")
    print("wrote %s" % OUT_PATH)
    for p in (SIB_GRADING, SIB_N6, SIB_TENSION):
        print("wrote %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
