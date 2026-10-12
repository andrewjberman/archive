"""IB-pr-482: writes IB167-2_release_census.json and IB167-2_release_counts.json from the scratch artifacts (built zip, live zip, the eight measured
cells, the replay arms). From the worktree root:  python -I <this file> <scratch_dir>
Counts, sha256 and reason codes only: no account id, balance, fee or flow. ASCII only."""
import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path(sys.argv[1])
D = Path("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~337")
IR = "infra/aws/lambda/investor-reporting"
PERF = IR + "/performance"
base = subprocess.run(["git", "rev-parse", "05219b8444"], capture_output=True, check=True).stdout.decode().strip()
pin = base
LIVE_CODESHA = "kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc="


def hexb64(h):
    return base64.b64encode(bytes.fromhex(h)).decode()


def blob_sha(path):
    r = subprocess.run(["git", "show", "%s:%s" % (pin, path)], capture_output=True, check=True)
    return hashlib.sha256(r.stdout).hexdigest()


built = S / "b1/lambda-artifact-irpt-performance-adapter.zip"
built2 = S / "b2/lambda-artifact-irpt-performance-adapter.zip"
live = S / "live.zip"
bh, b2h, lh = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (built, built2, live))
assert hexb64(lh) == LIVE_CODESHA
mem = json.loads((S / "members.json").read_text())
bm, lm = mem["built"], mem["live"]
differ = sorted(k for k in bm if k in lm and bm[k] != lm[k])
only_b, only_l = sorted(set(bm) - set(lm)), sorted(set(lm) - set(bm))
smap = json.loads(subprocess.run(["git", "show", pin + ":infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode())
repo_of = {s["packaged_as"]: s["repo_path"] for s in smap["functions"]["irpt-performance-adapter"]["staged_from"]}
changed = []
for n in differ:
    rp = repo_of.get(n) or (PERF + "/" + n)
    changed.append({"name": n, "repo_path": rp, "built_member_sha256": bm[n], "repo_blob_sha256_at_pin": blob_sha(rp), "live_member_sha256": lm[n]})
arms_b = [json.loads(x) for x in (S / "arms_built.jsonl").read_text().splitlines() if x.strip()]
arms_l = [json.loads(x) for x in (S / "arms_live.jsonl").read_text().splitlines() if x.strip()]
EXPECT = ["measured", "inferred", "inferred", "inferred"]
arms = []
for i, (b, lv) in enumerate(zip(arms_b, arms_l)):
    claim_same = b["claim"] == lv["claim"]
    fig_same = b["figure"] == lv["figure"]
    assert b["claim"] == EXPECT[i], b
    arms.append({"arm": b["arm"], "expected_built_claim": EXPECT[i], "built_claim": b["claim"], "live_claim": lv["claim"],
                 "built_value_facts_claim": b["value_facts_claim"], "live_value_facts_claim": lv["value_facts_claim"],
                 "built_days_without_base": b["days_without_base"], "built_days_with_return_left_out": b["days_with_return_left_out"],
                 "live_days_without_base": lv["days_without_base"], "live_days_with_return_left_out": lv["days_with_return_left_out"],
                 "days_excluded_built_live": [b["days_excluded"], lv["days_excluded"]], "days_linked_built_live": [b["days_linked"], lv["days_linked"]],
                 "figure_built": b["figure"], "figure_live": lv["figure"], "figure_verdict": "identical" if fig_same else "UNEXPECTED",
                 "claim_verdict": "identical" if claim_same else "expected-diff",
                 "verdict": "expected-diff" if (not claim_same or b["days_without_base"] is not None) else "identical",
                 "verdict_reason": ("claim measured -> inferred; the figure is the same number" if not claim_same else
                                    "claim and figure the same; the two new integers appear beside days_linked on built only"),
                 "frames": "synthetic, the four of performance/tests/test_chain_claim.py, 7 trading days 2026-03-02..2026-03-10, no AWS"})
assert all(a["figure_verdict"] == "identical" for a in arms)
census = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-482", "base_commit": base, "pin_commit": pin, "uploaded": False,
    "build_command": "BUILD_ONLY=1 TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate_source_map_482.json> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter",
    "candidate_map": str(D / "candidate_source_map_482.json").replace("\\", "/"),
    "real_source_map_sha256_before": (S / "map_before.sha").read_text().split()[0],
    "real_source_map_sha256_after": hashlib.sha256(Path("infra/aws/lambda/ci/lambda-source-map.json").read_bytes()).hexdigest(),
    "functions": [{
        "function": "irpt-performance-adapter",
        "built_sha256": bh, "built_codesha256_b64": hexb64(bh), "built_bytes": built.stat().st_size,
        "live_sha256": lh, "live_codesha256_b64": LIVE_CODESHA, "live_bytes": live.stat().st_size,
        "sha256_form": "built_sha256 and live_sha256 are the zip's SHA-256 in hex; _codesha256_b64 is the same value in base64, the form Lambda's CodeSha256 and build-and-upload print",
        "built_twice_identical": bh == b2h, "second_build_sha256": b2h,
        "built_signature_mismatched": 0, "built_attribute_mismatched": 0,
        "built_instrument_last_line": "signature_closure calls=186 checked=186 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=114 attr_mismatched=0",
        "live_instrument_last_line": "signature_closure calls=186 checked=186 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=114 attr_mismatched=0",
        "live_signature_mismatched": 0, "live_attribute_mismatched": 0,
        "instrument": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py",
        "members_built": len(bm), "members_live": len(lm), "members_only_in_built": only_b, "members_only_in_live": only_l,
        "changed_members": changed,
        "unintended_changed_members": [n for n in differ if n != "holdings_gold.py"],
        "replay_arms": arms,
    }],
}
(D / "IB167-2_release_census.json").write_text(json.dumps(census, indent=1) + "\n", encoding="utf-8", newline="\n")

WIN = ("SI", "YTD", "QTD", "1Y")
cells = {(e, w): json.loads((S / "cache" / ("cell166_%s_%s.json" % (e, w))).read_text()) for e in ("49F", "orion") for w in WIN}
reach = {e: {w: cells[(e, w)]["accounts_where_the_new_rule_fires"] for w in WIN} for e in ("49F", "orion")}
moves = {e: {w: cells[(e, w)]["accounts_whose_claim_moves_measured_to_inferred"] for w in WIN} for e in ("49F", "orion")}
already = {e: {w: cells[(e, w)]["accounts_where_the_new_rule_fires_but_the_base_claim_was_already_inferred"] for w in WIN} for e in ("49F", "orion")}
for e in reach:
    for w in WIN:
        assert reach[e][w] == moves[e][w] + already[e][w], (e, w)


def line_of(path, pat, nth=1):
    ls = Path(path).read_text(encoding="utf-8").splitlines()
    k = 0
    for i, ln in enumerate(ls, 1):
        if re.search(pat, ln):
            k += 1
            if k == nth:
                return i
    raise SystemExit("pattern %r not in %s" % (pat, path))


def cite(path, pat, extra=0, nth=1):
    n = line_of(path, pat, nth)
    return "%s:%d" % (path, n) if not extra else "%s:%d-%d" % (path, n, n + extra)


HG, NZ, EN = PERF + "/holdings_gold.py", PERF + "/normalize.py", PERF + "/entry.py"
PT = "portal/src/pages/InvestorReporting"
T = PERF + "/tests"
cons = [
    {"cite": cite(HG, r"node\.value_facts = \{", 4), "reads": "WRITES value_facts: start_value, end_value, days_linked, days_observed, days_excluded and the two new integers days_without_base and days_with_return_left_out (the two sum to days_excluded)",
     "read_through": "%s: the no-base arm reads (2, 0) and the left-out arms read (0, 1); test_chain_claim.py with test_partial_only_when_absence_holds.py run at the pin: 23 passed" % cite(T + "/test_chain_claim.py", r"def test_an_account_whose_excluded_days_are_only_no_base")},
    {"cite": cite(HG, r"claim = CLAIM_INFERRED if", 5), "reads": "DECIDES the claim from the missing-trading-day list and days_with_return_left_out (C-CHAINCLAIM) and writes it to value_facts.claim",
     "read_through": "%s (ALL-HOLDINGS-EXCLUDED reads inferred, the figure unchanged); and the 8-cell run over %d figures, figures_unchanged true" % (cite(T + "/test_chain_claim.py", r"def test_an_account_with_one_all_holdings_excluded_day_reads_inferred"), sum(v["figures_compared"] for v in cells.values()))},
    {"cite": cite(HG, r'"claim": claim\}'), "reads": "RETURNS the same claim as the outcome's claim key",
     "read_through": "%s (out['claim'] reads inferred on a missing day); test_holdings_gold_calendar_gap.py at the pin: 6 passed, 1 failed (the fallback-calendar test, which fails on the absent pandas_market_calendars and reads no claim)" % cite(T + "/test_holdings_gold_calendar_gap.py", r'assert out\["claim"\] != "measured"')},
    {"cite": cite(NZ, r'"value_facts": primary\.value_facts'), "reads": "copies the node's value_facts, claim and both counts included, into report.optional_facts.value_facts; sets supported from its presence (no member read)",
     "read_through": "%s (the _value_facts reader over the answer); test_holdings_gold.py at the pin: 23 passed" % cite(T + "/test_holdings_gold.py", r"def _value_facts")},
    {"cite": cite(PERF + "/orion_selected.py", r"if node\.value_facts:", 1), "reads": "truthy test, then copies value_facts with period_start/period_end replaced; reads no claim or count (the copy keeps the claim and both new members)",
     "read_through": "code read; test_performance_adapters.py at the pin: 28 passed"},
    {"cite": cite(PERF + "/bd_adapter.py", r"node\.value_facts is None", 0), "reads": "a writer's own guard on the Black Diamond path; writes value_facts without a claim and without the two integers, so its answers are unchanged",
     "read_through": "%s (value_facts from the vendor's end value); test_performance_adapters.py at the pin: 28 passed" % cite(T + "/test_performance_adapters.py", r"def test_value_facts_come_from_the_vendors_own_end_value")},
    {"cite": cite(EN, r'partial = bool\(outcome\.get\("absences"\)', 7), "reads": "reads the absences and refusals lists only (never the claim or the counts) to choose PARTIAL or READY; this is why PARTIAL stays",
     "read_through": "%s (PARTIAL with the reader's real absences, READY with none); run at the pin: 23 passed" % cite(T + "/test_partial_only_when_absence_holds.py", r"def test_the_entry_state_follows_the_absences_list")},
    {"cite": cite(EN, r'"_status": status\}'), "reads": "returns the report with optional_facts.value_facts (claim and both counts) to the wire",
     "read_through": "%s (PerformanceReport schema validation of the wire document); test_entry_selection.py at the pin: 39 passed" % cite(T + "/test_entry_selection.py", r"jsonschema\.Draft202012Validator")},
    {"cite": cite(PERF + "/retained.py", r'\["lineage"\]\["source_revision"\]'), "reads": "persists the report; the calculation revision comes from lineage.source_revision, not from the claim",
     "read_through": "%s; test_retained_performance.py at the pin: 21 passed" % cite(T + "/test_retained_performance.py", r'revision = outcome\["report"\]\["lineage"\]\["source_revision"\]')},
    {"cite": cite(IR + "/reports/repository.py", r"revision = hashlib\.sha256\(data\)\.hexdigest\(\)"), "reads": "the stored revision is the sha256 of the whole record, report body included, so a changed claim is a new revision and never overwrites a stored one",
     "read_through": "code read only (no run)"},
    {"cite": cite(IR + "/_contracts/PerformanceReport.schema.json", r'"value_facts": \{', 12), "reads": "value_facts is an object or null and its other members stay open, so the claim and the two integers are admitted",
     "read_through": "%s (calculate runs normalize.validate_report on every answer); run at the pin" % cite(T + "/test_chain_claim.py", r"def _answer")},
    {"cite": cite(IR + "/ops/status.py", r'answer_bearing = envelope\.get\("state"\)'), "reads": "treats PARTIAL as an answer-bearing state (business_date required); unchanged, PARTIAL stays",
     "read_through": "%s; ops/tests/test_status.py at the pin with PYTHONPATH=ycharts/generate: 23 passed (14 fail without that path on ModuleNotFoundError submission, a test-path matter)" % cite(IR + "/ops/tests/test_status.py", r"PARTIAL")},
    {"cite": cite(IR + "/_authz/served.py", r"ANSWER_BEARING_STATES = "), "reads": "lists PARTIAL among the answer-bearing states; unchanged",
     "read_through": "%s (state PARTIAL on the entry's answer); test_entry_selection.py at the pin: 39 passed" % cite(T + "/test_entry_selection.py", r'\("PARTIAL" if arm == "partial"')},
    {"cite": cite(IR + "/narrative/fixtures/performance_report_inf.json", r'"value_facts": \{'), "reads": "a recorded report fixture carrying a value_facts object without claim or counts; no narrative code reads value_facts",
     "read_through": "code read only (0 of the narrative package's python files name value_facts, row-331 census)"},
    {"cite": cite(IR + "/narrative/evidence.py", r'"claim": "measured"\}'), "reads": "the narrative packet writes its OWN claim strings on its own evidence rows; it reads no claim from a performance answer",
     "read_through": "code read only"},
    {"cite": cite(IR + "/_contracts/fixtures/PerformanceReport.valid.json", r'"value_facts"'), "reads": "contract fixture carrying value_facts null; the absent path",
     "read_through": "the _contracts suite at the pin: 203 passed, 2 failed (the two red-list tests of ADDENDUM 18), unchanged"},
    {"cite": cite("data/assets/scripts/gold/runners_49f/parity_period_returns.py", r'row\["days_linked"\] = int'), "reads": "found by census: the 49F gold's own days_linked column; it is not the reader's value_facts and carries no claim",
     "read_through": "code read only (not a consumer of the claim)"},
    {"cite": cite(PT + "/contracts/adapt.ts", r"const values = wire\.optional_facts\.value_facts", 2), "reads": "PORTAL: reads value_facts.period_start, period_end and currency only to decide hasValues; reads neither claim, days_without_base nor days_with_return_left_out",
     "read_through": "code read; native Grep for the word claim over contracts/, render/performance/, tabs/reporting/, state/ of the portal tree in this worktree finds no read of a performance claim (row-334 record IB166-4: 39 of 1395 portal files name value_facts or a value member)"},
    {"cite": cite(PT + "/contracts/wire/PerformanceReport.ts", r"readonly value_facts\?:"), "reads": "PORTAL wire type: value_facts is Readonly<Record<string, unknown>> or null, so the claim and the two integers pass as carried data",
     "read_through": "code read only (a bun run is the portal cell's, not this build's)"},
    {"cite": cite(PT + "/tabs/reporting/PerformanceHeadline.tsx", r"const endingText", 1), "reads": "PORTAL tile renders beginningValue and endingValue (from start_value/end_value via the adapter); it renders no claim label, so the claim change shows no new text",
     "read_through": "code read only"},
    {"cite": cite(PT + "/contracts/wire/HoldingsSnapshot.ts", r"readonly claim:"), "reads": "PORTAL: the one claim member in the portal's wire types belongs to the HOLDINGS snapshot, not to the performance report's value_facts",
     "read_through": "code read only"},
]
bad = [c["cite"] for c in cons if not Path(c["cite"].split(":")[0]).is_file()]
assert not bad, bad
counts = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-482", "base_commit": base, "pin_commit": pin, "counts_taken_at_pin": pin, "latest_landed_day": "2026-10-08",
    "reader_as_built": "the reader at the pin (%s:%s/holdings_gold.py, blob sha256 %s) over the cached served gold, versus the LIVE zip's holdings_gold.py (blob sha256 %s, the same bytes as 4650422c34 and 361c44fa9d)" % (pin[:10], PERF, bm["holdings_gold.py"], lm["holdings_gold.py"]),
    "rule_reach": reach, "claim_moves": moves, "already_inferred_at_base": already,
    "rule_reach_in_words": "accounts the C-CHAINCLAIM rule reaches (days_with_return_left_out above 0)",
    "claim_moves_in_words": "accounts whose served claim goes measured to inferred (measured with the live reader, inferred with the reader as built)",
    "already_inferred_at_base_in_words": "reach minus moves: accounts the rule reaches that the live reader already says inferred (a missing trading day)",
    "partitions_read": {"49F": cells[("49F", "SI")]["partitions_read"], "orion": cells[("orion", "SI")]["partitions_read"]},
    "partitions_listed": {"49F": 567, "orion": 1620, "used_le_cap_2026-10-08": {"49F": 566, "orion": 1619}},
    "accounts_read_per_cell": {"%s/%s" % k: v["accounts_read"] for k, v in cells.items()},
    "figures_compared_per_cell": {"%s/%s" % k: v["figures_compared"] for k, v in cells.items()},
    "figures_compared": sum(v["figures_compared"] for v in cells.values()),
    "figures_unchanged": all(v["figures_equal"] for v in cells.values()),
    "figures_hash_base": {"%s/%s" % k: v["figures_hash_base"] for k, v in cells.items()},
    "figures_hash_after": {"%s/%s" % k: v["figures_hash_after"] for k, v in cells.items()},
    "accounts_refused_base_and_after": {"%s/%s" % k: [v["accounts_refused_old"], v["accounts_refused_new"]] for k, v in cells.items()},
    "claim_at_base": {"%s/%s" % k: v["old_claim"] for k, v in cells.items()},
    "claim_after": {"%s/%s" % k: v["new_claim"] for k, v in cells.items()},
    "accounts_inferred_to_measured": sum(v["accounts_inferred_to_measured"] for v in cells.values()),
    "consumers_read_through": cons,
    "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "accounts_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
}
(D / "IB167-2_release_counts.json").write_text(json.dumps(counts, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"reach": reach, "moves": moves, "already": already, "consumers": len(cons), "changed": [c["name"] for c in changed], "twice": bh == b2h}))
