"""HVST-o-3: writes the proof_of_spec instance from the three recorded outputs (o3_ac1/2/3_output.txt).
Pure file work; no S3."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
os.chdir(ROOT)
D = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~63"
TO = "AMGT_HARVST.TO-HVST-o-3.silver-latest-tie-break-on-run-stamp"
BASE = "65aa9251bc3a07c38e5ffe386c50b69bf1a2ece4"

order = open("org/missions/D5/AMGT/AMGT_HARVST/task-orders/%s.md" % TO, encoding="utf-8").read()


def crit(i):
    m = re.search(r'<criterion id="%s"[^>]*><invocation>(.*?)</invocation><expect>(.*?)</expect>' % i, order, re.S)
    return m.group(1), m.group(2)


ac2 = open(D + "/o3_ac2_output.txt", encoding="utf-8").read()
ac1 = open(D + "/o3_ac1_output.txt", encoding="utf-8").read()
ac3 = open(D + "/o3_ac3_output.txt", encoding="utf-8").read()


def line(txt, needle):
    return [x for x in txt.splitlines() if needle in x][0].strip()


assert "19 passed" in ac1 and "258 passed" in ac3

ac1_ev = (
    "rc 0 (timeout 900). Final line: '%s'. Tests passed: test_tie_goes_to_the_later_run_stamp_and_newer_fetched_at_still_wins x6 "
    "(3 readers x natural/reversed layout, incl. the strictly-newer-fetched_at-in-the-EARLY-stamp-part plant), "
    "test_earlier_part_tie_row_is_not_returned x6, mutants x4 (silver_latest reverted -> silver_latest and _iter_latest_articles plants fail; "
    "_latest_articles_for_keys reverted -> its plants fail; shared comparator reverted -> all 3 readers fail; last-in-listing-wins -> all 3 fail "
    "on the reversed layout), test_part_order_key_sorts_stamps_and_collision_retry_suffixes, test_supersedes_rule, "
    "test_a_rebuilt_row_keeping_its_fetched_at_supersedes_through_silver_append. Full output: o3_ac1_output.txt"
    % line(ac1, " passed in ").strip("= ")
)
ac2_ev = (
    "rc 0 (timeout 900); full output o3_ac2_output.txt. Census: '%s'; '%s'; newest-wins readers: store.silver_latest (store.py:373), "
    "publication_gold._iter_latest_articles (:760, delegates), publication_gold._latest_articles_for_keys (:844), plus "
    "silver_from_bronze.rows_by_company_mention (:406, OUTSIDE paths -> row Z-W63-S1). Served ties: '%s' (each of the 8 pairs prints "
    "'tied newest-fetched_at across parts=0'). Bodies, OLD sha == NEW sha: AMZN_US_Equity 2026-09-07 "
    "5aecd79e8001bdff9a4d8ab032b4ee01d8893e47d25349815448f217455c53e5; HD_US_Equity 2026-08-18 "
    "de64cc82313f886e39dec240939f3fd59cbbebc387b0b96d62003d3e42bd931b; 992_HK_Equity 2026-08-13 "
    "dac6b73942cbe3af8347a8628b67d4393a984856cd12ed0da0b08c3b917209fe; 992_HK_Equity 2026-09-23 "
    "32b5257d204ee31a08411476b83aa7db4378a3113fccf3d710341bc6630499ed. Deciding line: '%s'"
    % (line(ac2, "denominator: 345"), line(ac2, "hits: 30"), line(ac2, "TOTAL over 8"), line(ac2, "OLD==NEW byte-equal on"))
)
ac3_ev = (
    "rc 0 (timeout 900). BASE (%s, git archive of lib/ + integrations/ run in a scratch copy): '239 passed'. AFTER (this worktree): "
    "'258 passed' = 239 base + 19 new in test_o3_silver_tie_break.py; 0 failed at either. One base test's assertion was edited in place: "
    "test_timeline_day_read_path.py::test_timeline_day_body_byte_equal_before_and_after_the_read_path_change asserted the OLD tie rule "
    "('sa2 tie A', first part); it now asserts 'sa2 tie B' (later run_stamp); it passes at base and after. Full output: o3_ac3_output.txt"
    % BASE[:10]
)
specs = [
    ("AC1", ac1_ev, r"19 passed", "19 tests: 12 plant tests (3 readers x 2 plants x 2 layouts), 4 mutants, 3 comparator/integration tests; 19 of 19 passed"),
    ("AC2", ac2_ev, r"tied across parts=0.*OLD==NEW byte-equal on 4 of 4 named days",
     "10 (source, table) silver pairs listed, 8 read (2 listing_hit tables are not collapsed by any reader), 489 record keys, 0 tied; 345 .py files scanned for the census; 4 of 4 named days OLD==NEW"),
    ("AC3", ac3_ev, r"258 passed", "258 of 258 passed after; 239 of 239 passed at base; 0 base-passing tests fail"),
]
rows = []
for cid, ev, exp, den in specs:
    i, e = crit(cid)
    rows.append({"criterion_id": cid, "criterion_verbatim": e, "method": "command", "invocation": i,
                 "output_evidence": ev, "denominator": den, "status": "PASS", "expect": exp})


def art(path, kind, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": "PENDING-THIS-COMMIT",
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE", "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": TO, "firm": "FABRIC", "phase": "NON-BUILD-OTHER",
    "spec_ref": {"doc": "org/missions/D5/AMGT/AMGT_HARVST/task-orders/%s.md" % TO, "group": "OTHER", "vintage_commit": BASE},
    "decomp_ref": {"doc": "org/missions/D5/AMGT/AMGT_HARVST/decompositions/AMGT_HARVST_DECOMP.md", "vintage_commit": BASE,
                   "to_ref": "org/missions/D5/AMGT/AMGT_HARVST/task-orders/%s.md" % TO},
    "assignee": "0.9.0_WK_AMGT_HARVST~63",
    "session_log": (
        "Worker 0.9.0_WK_AMGT_HARVST~63, L7 subagent of 2.0.0_SA_COO~H, worktree wk-hvst-r25-63 on branch wk-AMGT_HARVST-63 cut from 65aa9251bc, TREE-OK. "
        "Read-only S3 LIST/GET (a proxy exposing nothing else); no PUT, no delete, no vendor call, no deploy, no silver written. "
        "Change: store.py gains part_order_key and supersedes (a strictly newer fetched_at wins; on a tie the part with the later run_stamp wins, "
        "a -r<n> collision-retry suffix sorting after its base stamp) and silver_latest calls it; publication_gold._latest_articles_for_keys calls the same "
        "store.supersedes; _iter_latest_articles delegates to silver_latest. The census found a fourth newest-wins reader outside the paths "
        "(silver_from_bronze.rows_by_company_mention) -> row Z-W63-S1. The served silver has 0 tied keys, so all 4 named /timeline/day bodies are "
        "byte-identical under the old and new rule. MEASURED."
    ),
    "artifacts_produced": [
        art("lib/research/harvest/store.py", "script",
            "Adds part_order_key and supersedes; silver_latest applies them. Readers only; no served silver written; not redeployed (the scoped-API redeploy and the paired rebuild are later orders).",
            ["AC1", "AC2", "AC3"]),
        art("lib/research/harvest/publication_gold.py", "script",
            "_latest_articles_for_keys calls store.supersedes with per-source held part keys; _iter_latest_articles gains a comment only. publisher_coverage, daily_rows and build_daily untouched (HVST-o-1's).",
            ["AC1", "AC2", "AC3"]),
        art("lib/research/harvest/tests/test_o3_silver_tie_break.py", "test", "19 offline tests against an in-memory S3.", ["AC1", "AC3"]),
        art("lib/research/harvest/tests/test_timeline_day_read_path.py", "test",
            "One assertion and its comment updated from 'tie keeps the first part' to 'tie goes to the later run_stamp'.", ["AC3"]),
        art(D + "/scripts/o3_ac2_readers_and_served_ties.py", "script",
            "Read-only: S3 LIST/GET through a proxy that refuses every other call.", ["AC2"]),
    ],
    "acceptance": rows,
    "controls": {
        "mutant": {
            "description": "Adversary arm: one reader keeps the old first-in-listing-order rule while the others move (the page and the builder then disagree on the current row).",
            "expected": "the plants fail for the reverted reader and only for it; reverting the shared comparator fails all three readers",
            "observed": "4 mutant tests pass inside the 19: silver_latest reverted -> silver_latest and _iter_latest_articles plants raise AssertionError while _latest_articles_for_keys still passes; _latest_articles_for_keys reverted -> its plants fail while silver_latest passes; shared supersedes reverted to '>' -> 3 of 3 readers fail; '>=' (last-in-listing wins) -> 3 of 3 fail on the reversed layout.",
            "status": "FIRED-AS-EXPECTED"},
        "determinism": {
            "method": "AC2 run twice against the same store (the second after tightening the census pattern only)",
            "observed": "the served-tie section (0 tied of 489 record keys) and the four body sha256 values are identical across both runs; S3 call counts identical (125 LIST, 118 GET)",
            "status": "STABLE"}},
    "declared_exclusions": [
        {"item": "Any silver write, deploy, or vendor call", "reason": "Standing clause 0.1 and section 3 of the order; the paired served rebuild is HVST-o-4."},
        {"item": "silver_from_bronze.rows_by_company_mention (lib/opal_data_harvest/silver_from_bronze.py:406)",
         "reason": "Outside the order's <paths>; it takes rows with no part name and has no production caller. Filed as row AMGT_HARVST-Z-W63-S1."},
        {"item": "A tie between two rows inside ONE run_stamp (the same part name under two date partitions)",
         "reason": "The rule names run_stamp only; such a tie keeps the row read first, as before. None exists in the served silver (0 same-part duplicates at max fetched_at in every pair)."},
    ],
    "surprises": ["AMGT_HARVST-Z-W63-S1: a fourth newest-wins reader, silver_from_bronze.rows_by_company_mention, is outside the order's paths and keeps the first-seen tie rule; it has no production caller"],
    "compiler_tools": [{"tool": "safe-commit.sh",
                        "invocation": "bash .tools/safe-commit.sh --author \"0.9.0_WK_AMGT_HARVST~63 <0.9.0_WK_AMGT_HARVST~63@opal.agent>\" -F <msgfile> -- <paths>",
                        "result": "see the worker report"}],
}
with open(D + "/%s.proof_of_spec.json" % TO, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(inst, indent=2) + "\n")
print("wrote instance")
