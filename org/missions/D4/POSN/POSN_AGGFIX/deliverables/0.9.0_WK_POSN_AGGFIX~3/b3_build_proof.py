#!/usr/bin/env python
"""
Build the PROOF-OF-SPEC instance for POSN_AGGFIX.TO-B3-1.

Every acceptance row's output_evidence is READ FROM THE RECORDED RUN FILE beside this script -- never
retyped -- so the instance and the committed evidence cannot drift. The artifact pins are read from
`git rev-parse HEAD` at build time, which is the commit that carries these scripts and outputs.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True,
                      text=True).stdout.strip()
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
D = "org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~3/"
TO = ("org/missions/D4/POSN/POSN_AGGFIX/task-orders/"
      "POSN_AGGFIX.TO-B3-1.five-model-views-and-the-aggregate-on-live-bytes.md")
OUT = D + "POSN_AGGFIX.TO-B3-1.five-model-views-and-the-aggregate-on-live-bytes.proof_of_spec.json"


def eff(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


AC1_INV = "timeout 300 python " + D + "b3_live_fixtures.py"
AC2_INV = "timeout 900 node " + D + "b_five_books_dom.mjs --prior-vs-new .scratch/b3_fixtures"
AC3_INV = ("timeout 900 node " + D + "b2_agg_dom.mjs --viewer opal-staff --remembered none "
           "--fixtures .scratch/b3_fixtures")
AC4_INV = ("timeout 900 node org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~2/"
           "c1_live_tier_arms.mjs --phase post")

AC5_READINGS = """JUDGMENT -- READINGS ONLY, NO VERDICT (graded by 3.0.0_SA_CVO~Z at L9).

READING 1 -- WHAT B3-AC2 COMPARED, AND WHAT IT DID NOT.
The compared value per capture is the rendered TEXT of the two panels: composition {tile_count, tiles,
legend, empty} and breakdown {header, row_count, holding_row_count, rows[], empty}, where rows[] is the
joined text of every cell of every holding row (ticker, name, weight and the ETF characteristic columns
as rendered). Ten captures -- advisor and client x UST ST INT LT ULT -- read IDENTICAL between the PRIOR
served shared file and the NEW one. So the identity is over the holdings and the weights AS DISPLAYED,
at the precision the page prints, for the two panels the Models view shows.
NOT in the compared value, though printed per capture: the book selector entries (identical in every
capture, ["UST","ST","INT","LT","ULT"] in all 20), the page location, the request counts, and anything
outside those two panels.
THE DEPLOY DID MOVE A VALUE THESE PANELS DO NOT SHOW: TO-A3-1 recorded each book's `aum` changing with
this run (UST 52,360,822.93 -> 65,550,660.5; ST 129,227,888.01 -> 133,205,460.44; INT 444,315,640.92 ->
456,971,348.29; LT 804,605,507.26 -> 883,977,496.68; ULT 206,634,320.89 -> 209,446,529.75), and the two
panels' text did not move at all. Read together: the panels render holdings and weights, not book aum.
THE COMPARISON IS SENSITIVE: the control -- the NEW fixture with ONE holding weight changed, VGSH
0.1451 -> 0.1951 -- reported DIFFERENT (composition tile_count 13 -> 14), so IDENTICAL is a measurement
and not an insensitive instrument.

READING 2 -- WHAT AN ADVISOR OR A CLIENT REACHED IN B3-AC4'S RESPONSES.
On both aggregate URLs, advisor-class and client-class tokens received 401 with a 62-byte body,
{"error":"Opal-only resource: not authorized for this viewer"} (rows 7-10). Every AMENDMENT 1 form --
percent-encoded upper and lower, the /json/ path, the query form -- returned the same 401 and the same
62 bytes for both classes (rows 15-18, 20-23); the double-slash form returned S3's own 243-byte
AccessDenied XML error document (rows 19, 24), which is the origin answering, and carries no aggregate
content. The aggregate body itself, 14,410 bytes beginning {"status":"OK",..., was returned only to the
Opal-staff and Dev tokens (rows 3-6).
ON THE CONTROL URL all four classes received 200, len 67,273, sha256 86314ec65f3877e6, with the printed
prefix ending inside `note`. WHETHER THAT BODY REVEALS OPAL'S MODEL MIX OR TOTAL WAS NOT READ BY THIS
CRITERION'S INSTRUMENT: the named script never inspects the control body for current_holdings.AGG (row
POSN_AGGFIX-Z-W3-S5), which is why B3-AC4 is recorded FAIL rather than PASS.
A NEIGHBOURING FACT ON A DIFFERENT PLANE, STATED AS SUCH AND NOT OFFERED AS THAT READING: B3-AC1 read the
S3 OBJECT at the new VersionId (dFjRdciig4Y.4DBiK_F0eyHtn1.YBCOC) and found current_holdings UST ST INT
LT ULT with no AGG; the control rows carry generated_at 2026-09-15T22:12:22Z at len 67,273 where the same
script's 21:08Z run read generated_at 2026-09-15T11:06:19Z at len 80,704. That is an object read plus a
served-header read, not an inspection of the served body, and the CVO grades it as such."""

instance = {
    "schema_version": "1.0",
    "to_id": "POSN_AGGFIX.TO-B3-1",
    "phase": "BUILD-GENERAL",
    "decomp_ref": {
        "doc": "org/missions/D4/POSN/POSN_AGGFIX/decompositions/POSN_AGGFIX_DECOMP.md",
        "vintage_commit": "605c03f81f",
        "to_ref": TO,
    },
    "spec_ref": {
        "doc": "org/missions/D4/POSN/POSN_AGGFIX/prd/POSN_AGGFIX_PRD.md",
        "group": "B",
        "vintage_commit": "cbd85e5cff",
    },
    "assignee": "0.9.0_WK_POSN_AGGFIX~3",
    "artifacts_produced": [
        {
            "path_or_key": D + "b3_live_fixtures.py",
            "kind": "script",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + " on wk-posn_aggfix-1-3. A measurement script: it "
                                "performs read-only S3 GETs by VersionId and writes fixtures to .scratch. "
                                "Nothing in TO-B3-1 deploys, serves, promotes or pushes."),
            "artifact_covered_by": ["B3-AC1"],
        },
        {
            "path_or_key": D + "b_five_books_dom.mjs",
            "kind": "test",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + " on wk-posn_aggfix-1-3. TO-B1-1's render harness, "
                                "extended ADDITIVELY with the --prior-vs-new mode this order names; no "
                                "existing mode was touched, and the usage line now lists it."),
            "artifact_covered_by": ["B3-AC2"],
        },
        {
            "path_or_key": D + "b2_agg_dom.mjs",
            "kind": "test",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + " on wk-posn_aggfix-1-3. TO-B2-1's aggregate harness, "
                                "extended ADDITIVELY with --fixtures <dir>: every TO-B2-1 arm is unchanged on "
                                "the default path, and the B3 screenshot takes its own filename so TO-B2-1's "
                                "committed screenshot is never overwritten."),
            "artifact_covered_by": ["B3-AC3"],
        },
        {
            "path_or_key": D + "b3_ac2_prior_vs_new_3ec1f83cab.json",
            "kind": "doc",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + ". The full per-capture record of both arms at portal "
                                "HEAD 3ec1f83cab -- every composition and breakdown value the IDENTITY verdict "
                                "was computed from, so the verdict is re-derivable without a re-run."),
            "artifact_covered_by": ["B3-AC2", "B3-AC5"],
        },
        {
            "path_or_key": D + "b3_ac3_opal_staff_live_aggregate.png",
            "kind": "doc",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + ". The screenshot B3-AC3 names, of the Aggregate book "
                                "rendered on the live Opal-only bytes as Opal staff."),
            "artifact_covered_by": ["B3-AC3"],
        },
        {
            "path_or_key": D + "b3_fixtures.manifest.json",
            "kind": "doc",
            "commit_or_etag": PIN,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": ("LOCAL commit " + PIN + ". The provenance of the three fixtures: the source "
                                "instance and its commit, the ids each locus yielded, and every VersionId, "
                                "LastModified, stored byte count and stored md5 read live."),
            "artifact_covered_by": ["B3-AC1"],
        },
    ],
    "acceptance": [
        {
            "criterion_id": "B3-AC1",
            "criterion_verbatim": (
                "the prior and new VersionIds of json/positioning/positioning_data.json read from TO-A3-1's "
                "proof instance and printed; both objects fetched by VersionId (LastModified printed, the "
                "prior one earlier); the prior carrying current_holdings UST ST INT LT ULT AGG and the new one "
                "UST ST INT LT ULT; the live json/positioning/opal_aggregate.json fetched with its VersionId, "
                "decompressed, status OK and a non-empty current_holdings.AGG.holdings; three fixture files "
                "written."),
            "method": "live_read",
            "invocation": AC1_INV,
            "output_evidence": "$ " + AC1_INV + "\n" + eff("b3_ac1_live_fixtures.txt") + "\nrc=0",
            "denominator": (
                "checks 15 of 15 HOLD; ids cross-checked across 2 loci of the instance (A3-AC8, A3-AC9), 3 of 3 "
                "compared and 0 disagreements; prior current_holdings 6 of 6 keys (UST ST INT LT ULT AGG), new "
                "5 of 5 (no AGG); aggregate holdings 30, model_breakdown non-empty on 30 of 30 across 5 of 5 "
                "codes; bytes fetched == ContentLength on 3 of 3 objects; fixture files 3 of 3 written and the "
                "directory holds exactly 3."),
            "status": "PASS",
        },
        {
            "criterion_id": "B3-AC2",
            "criterion_verbatim": (
                "at your portal branch HEAD, as an advisor and as a client, Models mode, UST ST INT LT ULT: the "
                "composition labels and the breakdown rows rendered on the PRIOR shared file and on the NEW "
                "shared file IDENTICAL per book (`IDENTICAL 10 of 10`); and the control -- the NEW fixture with "
                "one holding weight mutated -- reported as a difference."),
            "method": "live_read",
            "invocation": AC2_INV,
            "output_evidence": "$ " + AC2_INV + "\n" + eff("b3_ac2_prior_vs_new.txt"),
            "denominator": (
                "IDENTICAL 10 of 10 (advisor and client x UST ST INT LT ULT) at portal HEAD "
                "3ec1f83cabb1780d4468c4f80fd16453df800f00; control 1 of 1 reported DIFFERENT; page errors 0 in "
                "4 of 4 viewer sessions; unfixtured 404s identical (7 distinct) in 4 of 4 sessions; the two "
                "non-shared feeds pinned to 1 VersionId each, identical in both arms."),
            "status": "PASS",
        },
        {
            "criterion_id": "B3-AC3",
            "criterion_verbatim": (
                "on the NEW shared file and the LIVE aggregate bytes: the page lands on Aggregate; the Portfolio "
                "Composition entries and the Holdings Breakdown rows each count equal to the live "
                "current_holdings.AGG.holdings length; the five Model Breakdown columns present with three "
                "sampled cells equal to model_breakdown x 100 at one decimal; a screenshot saved."),
            "method": "live_read",
            "invocation": AC3_INV,
            "output_evidence": "$ " + AC3_INV + "\n" + eff("b3_ac3_aggregate_live.txt"),
            "denominator": (
                "composition data nodes 30 of 30 live AGG holdings; breakdown holding rows 30 of 30; Model "
                "Breakdown columns 5 of 5 after Weight (UST ST INT LT ULT); sampled cells EQUAL 3 of 3 (IEFA, "
                "VCSH, TBIL); aggregate requests 1, served 1; page errors 0; screenshot 1 of 1 saved."),
            "status": "PASS",
        },
        {
            "criterion_id": "B3-AC4",
            "criterion_verbatim": (
                "the script is the one TO-C1-1's instance names for C1-AC13 (its path printed first); on the "
                "live distribution after TO-A3-1: Opal-staff and Dev tokens on "
                "/api/general/positioning/opal_aggregate.json return 200 with a body whose status is OK; "
                "advisor-class and client-class tokens on both aggregate URLs return 401; all four classes on "
                "/api/general/positioning/positioning_data.json return 200 and that body carries no "
                "current_holdings.AGG."),
            "method": "live_read",
            "invocation": AC4_INV,
            "output_evidence": (
                eff("b3_ac4_named_script.txt") + "\n\n$ " + AC4_INV + "\n"
                + eff("b3_ac4_live_tier_arms_post.txt")),
            "denominator": (
                "table rows MATCH 24 of 24; of the criterion's four named readings, 3 are present in the output "
                "and 1 is absent; aggregate 200 rows 4 of 4 (opal and dev x two URLs); advisor and client 401 "
                "rows 4 of 4; control-URL 200 rows 4 of 4; AMENDMENT forms 10 of 10 refused or non-aggregate; "
                "process rc=1, from the families limb only (row POSN_AGGFIX-Z-W3-S6)."),
            "status": "FAIL",
            "status_reason": (
                "REFUSED AS WRITTEN, per the order's refusal clause. The invocation ran verbatim on the script "
                "TO-C1-1's instance names for C1-AC13, with its path printed first from that instance's own "
                "`invocation` field, and three of the four named readings are in its output. The fourth -- "
                "'that body carries no current_holdings.AGG' -- is produced by NO limb of that script: the "
                "control loop (:202-205) grades on `r.status === 200` alone and its row prints status, length, "
                "sha256 and the first 120 bytes, which end inside `note`; the file's only current_holdings.AGG "
                "predicate (:212) is scoped to the AMENDMENT_URLS rows for the advisor and client classes and "
                "is never applied to the control URL. The script is TO-C1-1's deliverable, outside this order's "
                "<paths> grant, so it cannot be extended here; and the criterion was NOT satisfied by a second "
                "read of the served body, because the refusal clause forbids satisfying a criterion by another "
                "route. Filed as POSN_AGGFIX-Z-W3-S5. Separately, the process exit is 1 because the script "
                "resolves its C1-AC17 families baseline to the RUNNING worktree's .scratch, where this worker "
                "has none (POSN_AGGFIX-Z-W3-S6); that limb is not named by this criterion and none of the rows "
                "it does name is affected."),
        },
        {
            "criterion_id": "B3-AC5",
            "criterion_verbatim": (
                "`B3-AC5` -- **JUDGMENT, GRADED BY `3.0.0_SA_CVO~Z` AT L9:** whether B3-AC2's identity across "
                "the deploy is the FWD-8 bar (\"the same holdings and weights\") on the page advisors and "
                "clients read, and whether anything an advisor or a client can reach in B3-AC4's responses "
                "reveals Opal's model mix or total. Record the readings and offer NO verdict."),
            "method": "manual_read_with_citation",
            "invocation": "JUDGMENT -- no invocation; graded at L9",
            "judgment": True,
            "output_evidence": AC5_READINGS,
            "denominator": (
                "reading 1 over 10 of 10 captures and 5 of 5 book aum values TO-A3-1 recorded as moved; reading "
                "2 over 24 of 24 live rows, of which 14 are advisor-class or client-class requests."),
            "status": "UNVERIFIABLE-BY-INSTRUMENT",
            "status_reason": (
                "JUDGMENT criterion: the task order marks it judgment=\"true\" and names 3.0.0_SA_CVO~Z at L9 as "
                "the oracle. The readings are recorded and NO verdict is offered here."),
        },
    ],
    "controls": {
        "mutant": {
            "description": (
                "THREE controls, one per instrument that could otherwise only pass. (1) B3-AC2: the NEW shared "
                "fixture with ONE holding weight changed (current_holdings.UST.holdings[0] VGSH 0.1451 -> "
                "0.1951), rendered as an advisor on UST and compared against the NEW arm's own capture the same "
                "way -- this is the discriminator for IDENTICAL 10 of 10. (2) B3-AC1: the VersionIds were read "
                "from TWO loci of TO-A3-1's instance and required to agree, so a mis-parsed id cannot pass "
                "silently. (3) B3-AC1: every fetched object is required to match its own head-object "
                "ContentLength, and the prior shared file's stored md5 is compared against the independent "
                "manifest TO-B1-1 pinned at 15:18Z."),
            "expected": (
                "the mutated capture reads DIFFERENT; the two loci agree on every shared id; the fetched byte "
                "counts equal ContentLength and the prior object's md5 equals TO-B1-1's manifest value"),
            "observed": (
                "(1) 'CONTROL advisor/UST, the NEW arm vs the mutated NEW fixture: DIFFERENT -- "
                ".composition.tile_count: BEFORE=13  NOW=14'. (2) 'the instance's two loci agree on every id "
                "they share  ids compared across loci 3; disagreements none'. (3) 'bytes fetched == "
                "ContentLength' on 3 of 3 objects, and the prior object's stored md5 "
                "797a5947d5c2a4a93920c6dd9d3096e8 is the same value b_fixtures.mjs MANIFEST[0] pinned for that "
                "VersionId at 15:18Z -- two fetches, hours apart, of the same version, byte-identical."),
            "status": "FIRED-AS-EXPECTED",
        },
        "determinism": {
            "method": (
                "Every render read settles only on three consecutive identical DOM reads. B3-AC2 renders the "
                "SAME five books twice per viewer class within one run (the PRIOR arm and the NEW arm are "
                "separate browser contexts against separate fixture sets), and advisor and client are "
                "independent sessions, so each book is read four times in one run. The live reads are pinned by "
                "VersionId rather than by key, so a scheduled pipeline run between them cannot move what is "
                "read."),
            "observed": (
                "Per book, all four sessions agree exactly: UST tiles 13 / 14 holding rows; ST 15 / 15; INT 19 "
                "/ 19; LT 16 / 16; ULT 16 / 16 -- in the PRIOR and NEW arms and for advisor and client alike, "
                "with 146 requests and 7 distinct unfixtured 404s in 4 of 4 sessions. The live head read before "
                "the fetches reported the same VersionIds TO-A3-1 recorded (aggregate M8FOApCmYnAQB_3946XGOHSe"
                "qEzcL2j. equal to the recorded id), so no scheduled run intervened."),
            "status": "STABLE",
        },
    },
    "declared_exclusions": [
        {
            "item": "reading the SERVED control body for current_holdings.AGG by any route other than the "
                    "script B3-AC4 names",
            "reason": "The order's refusal clause: a criterion that cannot be satisfied as written is REFUSED "
                      "with its measurement, never repaired, widened or satisfied by another route. B3-AC4 is "
                      "recorded FAIL and rows POSN_AGGFIX-Z-W3-S5 / -S6 carry the finding.",
        },
        {
            "item": "the three behaviour families C1-AC17 captured, and the FAMILIES UNMOVED comparison",
            "reason": "B3-AC4 names the aggregate rows, the 401 rows and the control rows, and names no "
                      "families rows. The baseline is a scratch file in another worker's worktree and was not "
                      "copied (row POSN_AGGFIX-Z-W3-S6).",
        },
        {
            "item": "the served page after Andrew's promote word",
            "reason": "The order's <decomp_ref>: it is read at L10 by the grader, not here. This order is "
                      "read-only toward the cloud -- no deploy, no served write, no promote, no push.",
        },
        {
            "item": "Opal staff rendered over the five model books on live bytes",
            "reason": "AF1-s-16 names the advisor and the client for the five-book comparison; Opal staff is "
                      "read on the aggregate by B3-AC3. The Opal-staff five-book path was measured at this "
                      "portal HEAD by TO-B2-1.",
        },
        {
            "item": "the CloudFront cache window after TO-A3-1's invalidation",
            "reason": "Named in the order's preflight as not covered. B3-AC4 reads the served body through the "
                      "live distribution and records what it returned at 2026-09-15T22:57:39Z; B3-AC1 and "
                      "B3-AC2 read S3 by VersionId, which no cache can move.",
        },
        {
            "item": "the correctness of the edge token script itself",
            "reason": "Named in the order's preflight: its correctness is TO-C1-1's proof. This order runs it "
                      "unmodified and records its output.",
        },
    ],
    "surprises": [
        "POSN_AGGFIX-Z-W3-S5: B3-AC4 names four readings on one invocation and the script it names produces "
        "three -- no limb parses the control body for current_holdings.AGG, so that reading is absent from its "
        "output at any vintage; the criterion is recorded REFUSED rather than satisfied by a second read.",
        "POSN_AGGFIX-Z-W3-S6: that script resolves its C1-AC17 families baseline to the RUNNING worktree's "
        ".scratch, so the invocation exits 1 for every worker but the one that captured it while all 24 printed "
        "rows MATCH -- the process exit is not a usable verdict for that invocation outside that worktree.",
    ],
    "session_log": D,
    "compiler_tools": [
        {
            "tool": "python 3.11.9 + boto3 1.43.46 (b3_live_fixtures.py)",
            "invocation": AC1_INV,
            "result": "rc=0, CHECKS HOLD 15 of 15. Read-only S3: head-object and get-object by VersionId on "
                      "three objects; no write to any bucket.",
        },
        {
            "tool": "playwright-core + system Edge, vite started from this worktree's portal (b_five_books_dom."
                    "mjs, b2_agg_dom.mjs)",
            "invocation": AC2_INV + "  |  " + AC3_INV,
            "result": "both EXIT=0 at portal HEAD 3ec1f83cab. The two modes are ADDITIVE: --prior-vs-new is a "
                      "new branch beside the existing three, and --fixtures <dir> swaps the fixture source for "
                      "the arm B3-AC3 runs while every TO-B2-1 arm keeps the VersionId-pinned build on the "
                      "default path. The B3-AC2 run was executed in the background under its own `timeout 900` "
                      "so a tool-level cap could not truncate a 900 s-bounded run.",
        },
        {
            "tool": "c1_live_tier_arms.mjs (TO-C1-1's deliverable, run UNMODIFIED)",
            "invocation": AC4_INV,
            "result": "rc=1 with TABLE ROWS 24; MATCH 24 of 24. The path was read from TO-C1-1's instance and "
                      "printed first. The script was NOT edited: it lies outside this order's <paths> grant. "
                      "Its key read is `comp-secrets get opal/auth/jwt-private-key --reveal` inside the signing "
                      "process; no key or token is printed, written, placed in argv or committed, and the "
                      "tokens carry exp = iat + 300.",
        },
        {
            "tool": "proof-of-spec-check.py (this worktree's copy)",
            "invocation": ("python .tools/proof-of-spec-check.py " + OUT
                           + " B3-AC1,B3-AC2,B3-AC3,B3-AC4,B3-AC5"),
            "result": "see b3_proof_check.txt beside this instance.",
        },
    ],
}


def main():
    blob = json.dumps(instance, indent=1) + "\n"
    n = len(blob.encode("utf-8")) - len(blob)
    if n:
        print("ERROR: %d non-ASCII byte(s) in the instance" % n)
        return 1
    dest = os.path.join(ROOT, OUT)
    with open(dest, "wb") as fh:
        fh.write(blob.encode("utf-8"))
    back = open(dest, "rb").read().decode("utf-8")
    print("WROTE %s bytes=%d read-back-equal=%s" % (OUT, len(blob), back == blob))
    print("ARTIFACT PIN (git rev-parse HEAD at build time): %s" % PIN)
    rows = json.loads(back)["acceptance"]
    print("ACCEPTANCE ROWS %d: %s" % (len(rows), ", ".join(
        "%s=%s" % (r["criterion_id"], r["status"]) for r in rows)))
    print("SURPRISES: %d" % len(json.loads(back)["surprises"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
