"""EN-c-40 (LGIC_ENFORCE round 9) -- writes HAND_COMPARISON_R9.json.

Runs compare_hand_r9.py's comparison AT WRITE TIME (so every denominator in the record is re-measured when the
record is written), attaches a `why` to every disagreement from WHYS below, and REFUSES to write if any
disagreement lacks a why or any why names a case that is not a disagreement. The whys are this worker's reading;
the measurements beside them (registry intro commits, rule lines) are cited so a reader can re-check each.

Usage (from the worktree root):  python <this file>
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compare_hand_r9 as C  # noqa: E402

OUT = os.path.join(HERE, "HAND_COMPARISON_R9.json")
N6_AT = "n6-grader-a.tsv @388b07f486 (2026-09-14T13:42:15-04:00, its own `# base 3d671ff59c`)"
REG = "infra/logic/registry/systems.json"

_STALE_SYS = ("HAND SIDE STALE, grade() right at the census vintage: the hand row was graded at " + N6_AT +
              ", before the deciding registry row existed. `git log --reverse -S` on " + REG + " puts the token %s "
              "first at %s. R1 reads V1/V2/V3 from REGISTRY rows (GRADING_RULE.md R1, `DATA.rows_owner`), so the "
              "verdict moves when the row lands; the hand record is a vintage-pinned exercise and was never re-graded.")
_A = "a925c8a642 (2026-09-14T19:32:54-04:00)"
_B = "72d636db4f (2026-09-16T03:04:22-04:00)"
_G = "c19dcc8147 (2026-09-15T16:25:56-04:00)"
_RES = ("HAND SIDE STALE, grade() right at the census vintage: verdict AGREES (OUT-OF-PATTERN); only the canonical "
        "form differs, in the {system} slot. GRADING_RULE.md R1.d says the placeholder stands 'because the name does "
        "not carry its system (DATA.grade.placeholder: the registry's resource-to-system rows fill it)'. "
        "infra/logic/registry/resources.json gained this name's row (system advi) at %s, after the hand record "
        "was written, so grade() fills the slot the hand left open. The hand record was never re-graded.")

WHYS = {
    "grading_rule_worked_cases": {
        ("inf-silver-chain", "LAMBDA"): _RES % "43194e7a28 (2026-09-17T23:05:30-04:00)" +
        " GRADING_RULE.md was last changed at 7c1e9ffb26 (2026-09-16), a day before the row.",
        ("Inflection-SilverChain-DimConversionFailure", "CW_ALARM"): _RES % "f039acf201 (2026-09-17T17:18:11-04:00)" +
        " GRADING_RULE.md was last changed at 7c1e9ffb26 (2026-09-16), a day before the row.",
    },
    "n6_grader_rows": {
        ("inf-otp-relay-api", "API_GW"): _RES % "6c87bd0968 (2026-09-17T12:25:52-04:00)",
        ("inf-unified-account-dim-daily", "EVENT_RULE"): _RES % "7604292b33 (2026-09-18T02:33:05-04:00)",
        ("trade-submission-api", "API_GW"): _STALE_SYS % ("`trade` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("trade-pipeline-ses-complaints", "SNS_TOPIC"): _STALE_SYS % ("`trade` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("astn-wsjft-scraper", "EC2_INSTANCE"): _STALE_SYS % ("`astn` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("astn-wsjft-scraper-profile", "INSTANCE_PROFILE"): _STALE_SYS % ("`astn` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("astn-wsjft-scraper-sg", "SECURITY_GROUP"): _STALE_SYS % ("`astn` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("astn-wsjft-alerts", "SNS_TOPIC"): _STALE_SYS % ("`astn` (in `unresolved`, so R1.c RAISE)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("opal-data-news-av", "S3_BUCKET"): _STALE_SYS % ("`news` (in `unresolved`, so B2 finds no scope key and RAISES)", _A) +
        " The census carded this name (NOT-JUDGED) for the same step.",
        ("estate-report-seam-freshness-publisher", "CODEBUILD_PROJECT"): _STALE_SYS % ("`estate` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("/aws/codebuild/estate-report-seam-freshness-publisher", "LOG_GROUP"): _STALE_SYS % ("`estate` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("estate-report-runner", "EC2_INSTANCE"): _STALE_SYS % ("`estate` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("globgrph-comp-learns-producer", "ECS_TASK_DEFINITION"): _STALE_SYS % ("`globgrph` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("globgrph-nessie", "ECS_TASK_DEFINITION"): _STALE_SYS % ("`globgrph` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("globgrph-trino", "ECS_TASK_DEFINITION"): _STALE_SYS % ("`globgrph` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("opal-globgrph", "ECS_CLUSTER"): _STALE_SYS % ("`globgrph` (PLATFORM_SUBSYSTEM, V1)", _A) +
        " N2 already carries this same name re-graded (OUT-OF-PATTERN globgrph-cluster, citing S22 / R-5), so the "
        "two LGIC_NAMING hand products now contradict each other on it.",
        ("/aws/lambda/opal-globgrph-freeze-monitor", "LOG_GROUP"): _STALE_SYS % ("`globgrph` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("FIRMSEP-s3-direct-access-bypass", "EVENT_RULE"): _STALE_SYS % ("`firmsep` (PLATFORM_SUBSYSTEM, V1)", _A),
        ("semantic-clustering-lambda-build", "CODEBUILD_PROJECT"): _STALE_SYS % ("`semantic` (a V3 vocabulary token, so R1.d gives {system})", _A),
        ("user-permissions", "DYNAMODB_TABLE"): _STALE_SYS % ("`user` (a V3 vocabulary token, so R1.d gives {system})", _B),
        ("yield-curve-artifact-write", "IAM_POLICY"): _STALE_SYS % ("`yield` (a V3 vocabulary token, so R1.d gives {system})", _B),
        ("access-anomaly-scanner", "LAMBDA"): _STALE_SYS % ("`access` (a V3 vocabulary token, so R1.d gives {system})", _B),
        ("partner-etl-ops-queue", "SQS_QUEUE"): _STALE_SYS % ("`partner` (a V3 vocabulary token, so R1.d gives {system})", _B),
        ("opal-gateway", "LOAD_BALANCER"): _STALE_SYS % ("`gateway` (PLATFORM_SUBSYSTEM, V1, so R2 drops opal as a null prefix)", _G) +
        " N2 carries the same name re-graded to gateway-lb, so the two hand products contradict each other on it.",
        ("aws-waf-logs-opal-gateway", "LOG_GROUP"):
        "HAND SIDE STALE, grade() right: NAMING_SCHEMA.json aws_fixed.by_name.LOG_GROUP carries 'prefix: aws-waf-logs-' "
        "(first at de52d3db04, 2026-09-14T15:12:59-04:00, after " + N6_AT + "), so G2.1 puts the name outside the "
        "grade's domain: NOT-GRADED, never a RAISE (GRADING_RULE.md section 9's `default` case states the same rule). "
        "The census likewise excludes it among its 4 aws_fixed LOG_GROUP names.",
        ("ExecIncrParityFailure", "CW_ALARM"):
        "grade() SIDE departs from the WRITTEN rule; the hand follows it. Verdict agrees (OUT-OF-PATTERN); the "
        "canonical differs: hand exec-incr-parity-failure, grade() exec-incrparity-failure. GRADING_RULE.md N2 "
        "(line 106) splits before each capital and states no re-join; grade()'s token step re-joins the pieces of one "
        "original segment whose concatenation is a vocabulary word (rejoin landed in lib/opal_naming.py at "
        "828ac108db, 2026-09-14T20:55:52-04:00) and `incrparity` entered " + REG + " at " + _B + ". Either N2 is "
        "missing the re-join clause or grade() applies one the rule does not have; filed as a row, not decided here.",
        ("opal-cot-bd-session-fetch", "SSM_DOCUMENT"):
        "grade() SIDE WRONG against the written rule; the hand is right. Verdict agrees (OUT-OF-PATTERN); the "
        "canonical differs: hand opal-cot-blackdiamond-session-fetch-document, grade() opal-cot-bd-session-fetch-"
        "document. GRADING_RULE.md R3 (line 204): bd next to a V4 firm token (here cot) is the VENDOR, 'Either way it "
        "is an alias, and the canonical form spells blackdiamond'. grade() leaves `bd` in the function slot's "
        "canonical form, so its canonical form carries a refused token. Filed as a row.",
    },
    "tension_ranking_surfaces": {
        1: "Four of nine figures miss the declared bar (any bd/49f/inf/cot token: hand ~330, census 397; 49f anywhere: "
           "45 vs 68; 49financial: 4 vs 7; cot first-token: 30 vs 35). HAND SIDE is the weaker: TENSION_RANKING.md "
           "measures nothing ('Nothing was measured again for this file') and quotes 09_NAMING_CENSUS.md of "
           "2026-09-13, whose ~330 is the sum of four figures taken at mixed grains (bd 120, inf 140, cot 30 are "
           "FIRST-token counts from its s.3; 49f 45 has no stated grain), so the sum is not a count of names at any "
           "one grain. The three first-token figures read at their own grain agree (bd 120/120, inf 140/138, firm-first "
           "over four types 210/206). 49financial rising 4->7 is the direction the naming work moves names, so the "
           "census side is the current one.",
        4: "One of five figures misses: camel/Pascal CW alarms, hand 6. The census r8 live plane carries 13 CW_ALARM "
           "names with a capital (hyphens allowed, the hand source's own grain '6 Camel/Pascal-kebab') and 2 with no "
           "hyphen. HAND SIDE WRONG: its own source lists FIRMSEP-* 5, Inflection-* 3 and ExecIncrParityFailure in "
           "the same row (9 names), so '6' contradicts the census it quotes. The other four figures agree "
           "(policies 96/99, customer-managed 502/515, CloudWatchLogs 6/6, camel roles 6/6).",
        5: "Every figure misses by 2x-10x (339 vs 669; Lambda 15 vs 158). NEITHER SIDE IS SHOWN WRONG: the INSTRUMENTS "
           "differ. The hand figure is comp-find's drift_class LIVE-no-DECLARED over the live graph; the census r8 "
           "carries no drift class, so the only census-side reading is live (name,type) minus repo (name,type), and "
           "the repo plane reads only literal Terraform name attributes and source literals (132 expression names "
           "not judged), which inflates the difference. Recorded as DISAGREE because the census cannot reproduce "
           "the hand's figure, not because the hand's figure is shown false.",
        7: "Both figures miss: opal first-token names 445 vs 508 and types 18 vs 22 (with every LOG_GROUP tokenised on "
           "its resource part, the hand census s.2 grain); read without that stripping they are 437 and 21 "
           "(iv7_first_run), which puts the name count within tolerance but not the type count. HAND SIDE STALE and "
           "grain-ambiguous: 09_NAMING_CENSUS.md s.3 does not say whether its 445 counts log groups, and its "
           "type count of 18 is below the census's under either reading.",
        8: "One of four figures misses: s3-* purpose-first policies, hand 29, census 33 (tolerance +-2.9). The "
           "total 91/96, cross-* 39/40 and cloudwatch-* 23/23 agree. Four more s3-* policies in five days is "
           "estate drift: the HAND figure is the older vintage, not shown wrong at its own date.",
    },
}


def main():
    wc = C.worked_cases()
    header, n6_lines, n6 = C.n6_rows()
    cen = C.census()
    cc = C.census_commit()
    head = C.git("rev-parse", "HEAD").decode().strip()
    mod_c, t1 = C.load_grade(cc)
    mod_h, t2 = C.load_grade(head)
    try:
        n2 = C.compare_names(wc["worked_cases"], mod_c, mod_h, cen)
        nn6 = C.compare_names(n6, mod_c, mod_h, cen)
        iv = C.iv7(cen)
    finally:
        import shutil
        shutil.rmtree(t1, ignore_errors=True)
        shutil.rmtree(t2, ignore_errors=True)
    tension_text = io.open(C.TENSION, encoding="utf-8").read()
    import re
    iv7_rows = len(re.findall(r'\{"rank": \d+', tension_text))

    problems = []

    def name_block(res, key, instrument, value):
        whys = WHYS[key]
        dis = []
        for d in res["disagreements"]:
            k = (d["name"], d["type"])
            if k not in whys:
                problems.append("%s: no why for %r" % (key, k))
                continue
            dis.append({"name": d["name"], "type": d["type"], "hand": d["hand"], "grade_at_census": d["grade_at_census"],
                        "raise_step": d["raise_step"], "why": whys[k]})
        extra = set(whys) - set((d["name"], d["type"]) for d in res["disagreements"])
        if extra:
            problems.append("%s: whys for non-disagreements %r" % (key, sorted(extra)))
        return {"compared": res["compared"], "agree": res["agree"], "disagree": res["disagree"],
                "disagreements": dis,
                "denominator_measured_at_write_time": {"instrument": instrument, "value": value},
                "vintage_diffs_census_vs_head": res["vintage_diffs"],
                "per_case": [{"name": p["name"], "type": p["type"], "hand": p["hand"],
                              "grade_at_census": p["grade_at_census"], "result": p["result"],
                              "census_r8_rows": p["in_census_r8"]} for p in res["per_case"]]}

    s_n2 = name_block(n2, "grading_rule_worked_cases",
                      "len(worked_cases) of json.loads of the ONE json fence between '## 9. WORKED CASES' and '## 10.' "
                      "in " + C.GRADING_RULE + " (compare_hand_r9.worked_cases)", len(wc["worked_cases"]))
    s_n6 = name_block(nn6, "n6_grader_rows",
                      "non-empty lines of " + C.N6_TSV + " after the '# base' header line, split on TAB "
                      "(compare_hand_r9.n6_rows); %d non-empty lines = 1 header + %d rows" % (n6_lines, len(n6)), len(n6))
    tw = WHYS["tension_ranking_surfaces"]
    tdis = []
    for s in iv["per_surface"]:
        if s["result"] == "DISAGREE":
            if s["rank"] not in tw:
                problems.append("IV7: no why for rank %d" % s["rank"])
                continue
            tdis.append({"name": "rank %d: %s" % (s["rank"], s["surface"]), "why": tw[s["rank"]],
                         "figures": s["figures"]})
    extra = set(tw) - set(s["rank"] for s in iv["per_surface"] if s["result"] == "DISAGREE")
    if extra:
        problems.append("IV7: whys for non-disagreements %r" % sorted(extra))
    s_iv = {"compared": iv["compared"], "agree": iv["agree"], "disagree": iv["disagree"], "disagreements": tdis,
            "denominator_measured_at_write_time": {
                "instrument": "count of '{\"rank\": N' rows in the json fence of " + C.TENSION +
                              " (the ranked surfaces), cross-checked against the per-surface comparison's own length",
                "value": iv7_rows},
            "tolerance_declared_before_computing": C.IV7_TOLERANCE,
            "census_population": {"live_judged_plus_carded": iv["live_population"],
                                  "repo_judged_plus_carded": iv["repo_population"]},
            "per_surface": iv["per_surface"],
            "iv7_first_run": {
                "why_kept": "the grain of rank 1 (per-spelling, first-token), rank 4 (alarms) and LOG_GROUP tokenisation "
                            "was revised after this run to the grain 09_NAMING_CENSUS.md states for each figure; kept "
                            "so the revision can be judged against its effect. The tolerance was not changed.",
                "agree": 3, "disagree": 7,
                "changed_figures": {"rank1 bd": "any-position 144 -> first-token 120", "rank1 inf": "any 166 -> first 138",
                                    "rank1 cot": "any 65 -> first 35", "rank1 firm-first": "all types 239 -> four types 206",
                                    "rank2 bd first-token": "94 (log groups tokenised as /aws/...) -> 120",
                                    "rank4 alarms": "no-hyphen camel 2 -> any capital 13",
                                    "rank6 first-token codes": "25 total -> 28 (log groups)",
                                    "rank7 opal": "437 over 21 types -> 508 over 22 types (log groups)"}}}
    if iv7_rows != iv["compared"]:
        problems.append("IV7 json rows %d != surfaces compared %d" % (iv7_rows, iv["compared"]))

    from collections import Counter
    rec = {
        "cell": "EN-c-40", "to": "LGIC_ENFORCE.TO-EN-c-40-r9", "worker": "0.9.0_WK_LGIC_ENFORCE~1",
        "claim": "measured -- every count below re-derived by build_hand_comparison_r9.py at write time",
        "census": {"report": C.CENSUS, "commit": cc, "vintage": cen["vintage"], "registry": cen["registry"],
                   "grade_vintage": "grade() imported from `git archive %s` of %s; also run at HEAD %s -- "
                                    "vintage diffs: N2 %d, N6 %d" % (cc[:10], C.GRADE_INPUTS, head[:10],
                                                                      len(n2["vintage_diffs"]), len(nn6["vintage_diffs"]))},
        "agree_rule": {"per_name": "AGREE iff hand verdict == grade() verdict AND (hand gives no canonical form OR it "
                                   "equals grade()'s byte for byte); hand RAISE agrees only with RaiseDefect",
                       "per_surface": "AGREE iff every figure the surface states is within tolerance "
                                      "(approx 15%, exact 10%, floor +-2), all raw figures recorded"},
        "worked_cases": {
            "counted": len(wc["worked_cases"]),
            "by_verdict": dict(Counter(c["verdict"] for c in wc["worked_cases"])),
            "types": len(set(c["type"] for c in wc["worked_cases"])),
            "which_carrier_is_stale": (
                "43 is STALE; 45 is current. The stale carriers: org/missions/D14/LGIC/LGIC_ENFORCE/project.json (the "
                "register, round-9 'blocking' text: 'section 9 = 43 worked cases') and org/missions/D14/LGIC/"
                "LGIC_ENFORCE/deliverables/1.0.0_SA_CTO/LGIC_ENFORCE_ROUND8_ANALYSIS.md:151 ('s.9 = 43 worked "
                "cases'). 43 was true at GRADING_RULE.md @51b0952d71 (LN-g-1's own proof and EN-b-1's 'WORKED CASES: "
                "43'); the v1.9 re-cut @fd6ce8c330 added mdpf-lambda-lambda and orion-orion-lambda-lambda (EN-s-2 "
                "round 2's result record, census-comparison.r2.result.md:48, already measured 43 -> 45). R9_BASE.json's "
                "worked_cases_MEASURED 45 is the correct figure."),
            "denominator_measured_at_write_time": s_n2["denominator_measured_at_write_time"]},
        "surfaces": {"grading_rule_worked_cases": s_n2, "n6_grader_rows": s_n6, "tension_ranking_surfaces": s_iv},
    }
    for k, b in rec["surfaces"].items():
        if b["agree"] + b["disagree"] != b["compared"] or len(b["disagreements"]) != b["disagree"]:
            problems.append("%s does not close" % k)
    if problems:
        for p in problems:
            print("REFUSED:", p)
        return 1
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("worked cases counted %d" % rec["worked_cases"]["counted"])
    for k, b in rec["surfaces"].items():
        print("%s: agree %d + disagree %d = %d ; compared %d ; denominator %d"
              % (k, b["agree"], b["disagree"], b["agree"] + b["disagree"], b["compared"],
                 b["denominator_measured_at_write_time"]["value"]))
    print("WROTE", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
