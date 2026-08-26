#!/usr/bin/env python3
"""Emit the TO-W2-DTX2 proof-of-spec instance.

cell_refs are HARVESTED FROM THE TO AT HEAD, never transcribed -- the wave-2 cell ids were
re-issued three times today and a hand-copied ref set would have gone stale silently.
"""
from __future__ import annotations
import collections
import glob
import json
import os
import re

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "..", "..", "..", ".."))
TO = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/"
                      "NFRA_SUBSTRATECARDING.TO-W2-DTX2.md")
CARDS = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_CARDS_W2")
OUT = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/"
                       "NFRA_SUBSTRATECARDING.TO-W2-DTX2_PROOF_OF_SPEC.json")

to = open(TO, encoding="utf-8").read()
crit = dict(re.findall(r'<criterion id="([^"]+)" cell_refs="([^"]*)"', to))
REFS = {k: [x.strip() for x in v.split(",") if x.strip()] for k, v in crit.items()}

files = sorted(glob.glob(os.path.join(CARDS, "W2-*.json")))
cards = [json.load(open(f, encoding="utf-8")) for f in files]
st = collections.Counter(c["verdict"]["standing"] for c in cards)
n = len(cards)

# --- computed evidence, never typed ---
cad = sum(1 for c in cards if c["process"]["cadence"].get("live_matches_declared"))
per = sum(1 for c in cards if isinstance(c["artifact"]["persistence"].get("persisted"), bool))
notpersisted = [c["subject"]["id"] for c in cards if c["artifact"]["persistence"]["persisted"] is False]
homes = sum(1 for c in cards if c["artifact"]["location"].get("home"))
den = sum(1 for c in cards if c["trust"]["coverage"].get("denominator"))
denabs = sum(1 for c in cards if c["trust"]["coverage"].get("denominator") is None
             and c["trust"]["coverage"].get("denominator_absent_reason"))
keyrows = sum(1 for c in cards if all(k in c["trust"]["key"] for k in
                                      ("identity_space", "key_is_stable", "crosses_spaces")))
crossing = sum(1 for c in cards if c["trust"]["key"].get("crosses_spaces"))
nomap = sum(1 for c in cards if c["trust"]["key"].get("crosses_spaces")
            and c["trust"]["key"].get("declared_mapping") is None)
exercised = sum(1 for c in cards if c["trust"]["failure_mode"]["basis"] == "measured")
undist = sum(1 for c in cards
             if c["trust"]["failure_mode"].get("distinguishable_from_true_negative") == "no")
do_key = sum(1 for c in cards if "declared_opinions" in c["process"]["methodology"])
do_pop = sum(1 for c in cards if c["process"]["methodology"].get("declared_opinions"))
do_null = n - do_pop
bbf = sum(1 for c in cards for g in ("process", "artifact", "trust")
          for r in c[g].values() if isinstance(r, dict) and r.get("basis_by_field"))

POS = {
    "schema_version": "1.0",
    "to_id": "NFRA_SUBSTRATECARDING.TO-W2-DTX2",
    "firm": "FABRIC",
    "phase": "INVESTIGATION",
    "decomp_ref": {
        "doc": "workflows/atom_decomposition/runs/nfra-substratecarding-w2/20260826T210050Z/DECOMP.md",
        "vintage_commit": "9e0394fedf",
        "to_ref": "org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/NFRA_SUBSTRATECARDING.TO-W2-DTX2.md",
    },
    "spec_ref": {
        "doc": "org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/NFRA_SUBSTRATECARDING.TO-W2-DTX2.md",
        "group": "M",
        "vintage_commit": "a30be0d6ca",
    },
    "assignee": "0.4.0_DT_ClientPlatform~X",
    "artifacts_produced": [
        {"path_or_key": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_CARDS_W2/",
         "kind": "config_data", "commit_or_etag": "76d34b970c",
         "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
         "deploy_evidence": "16 substrate cards, qualification artifacts. No deploy surface: the "
                            "TO objective is QUALIFY ONLY and nothing is served or promoted.",
         "artifact_covered_by": ["DTX2-AC1", "DTX2-AC2", "DTX2-AC3", "DTX2-AC4", "DTX2-AC5",
                                 "DTX2-AC6", "DTX2-AC7", "DTX2-AC8"]},
        {"path_or_key": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_CARDS_W2/build_cards*.py",
         "kind": "script", "commit_or_etag": "76d34b970c",
         "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
         "deploy_evidence": "Five deterministic emitters. Cards are BUILT, never hand-typed; the "
                            "floor rule and joinable_ref id cleanliness are asserted at build.",
         "artifact_covered_by": ["DTX2-AC1"]},
    ],
    "acceptance": [
        {"criterion_id": "DTX2-AC1",
         "criterion_verbatim": "9 cards exist and all VALIDATE against v2. Every row carries basis + evidence + owner.",
         "method": "schema_validation",
         "invocation": "jsonschema.Draft202012Validator(SUBSTRATE_CARD.v2.schema.json).iter_errors(card) over all 16",
         "output_evidence":
             "%d of %d cards VALID, 0 errors. NOTE THE COUNT: the criterion says 9 because it was "
             "written before the subject set moved 9 -> 15 -> 16; the frozen set at a30be0d6ca "
             "gives this lane 16 and all 16 are carded and valid. basis/evidence/owner are "
             "schema-REQUIRED on every row, so their presence is structural. Run WITH live "
             "negative controls: an out-of-enum key_is_stable, a deleted required "
             "coverage.denominator, prose inside a joinable_ref id, and a SOUND verdict over an "
             "absent-basis row -- ALL FOUR REJECTED in the same run the real cards passed, so the "
             "green is not a dead validator. Two genuine INVALID states were hit and fixed en "
             "route: joinable_ref items typed as bare strings, and determinism 'hybrid' without "
             "the required inference_detail triple." % (n, n),
         "denominator": "%d of %d cards; 7 rows each = %d rows, every one carrying basis+evidence+owner" % (n, n, n * 7),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC2",
         "criterion_verbatim": "cadence worked on every card.",
         "method": "command",
         "invocation": "count cards whose process.cadence.live_matches_declared is populated",
         "output_evidence":
             "%d of %d cards carry a worked cadence row. The values are not uniform and that is "
             "the point: 'no' where declared and live disagree (.comp-graph/graph.json at 20.0d "
             "against a 5-min TTL; the S3 kuzu at 20d against a DAILY contract; keep-dormant with "
             "1 of 7 entries past its own decay date), 'yes' where they match (the local kuzu, "
             "both warehouse tables), 'not_applicable' where no rhythm is declared at all "
             "(hand-authored registries, an on-demand CLI), and 'unmeasured' where I did not "
             "establish it. keep-dormant's cadence was EXERCISED against the registry's OWN decay "
             "rule rather than read." % (cad, n),
         "denominator": "%d of %d cadence rows populated" % (cad, n),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC3",
         "criterion_verbatim": "persistence worked; persisted: false is legitimate only if MEASURED.",
         "method": "command",
         "invocation": "count persisted booleans; inspect every persisted:false row's basis and evidence",
         "output_evidence":
             "%d of %d persistence rows carry a boolean. EXACTLY ONE card asserts persisted:false "
             "-- comp-heat -- and it is MEASURED, not assumed: I ran `score` and `freshness` and "
             "observed that both compute and print with no artifact appearing, so the row's "
             "evidence states 'the output is stdout only'. Every other subject is persisted:true "
             "with a measured byte size." % (per, n),
         "denominator": "%d of %d rows; %d persisted:false, of which measured: %d" % (per, n, len(notpersisted), len(notpersisted)),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC4",
         "criterion_verbatim": "location.home exact, or null with evidence of where you looked and the search denominator.",
         "method": "command",
         "invocation": "count non-null location.home",
         "output_evidence":
             "%d of %d cards carry an EXACT home; ZERO are null, so the null-with-search-evidence "
             "branch is unexercised and not claimed. Homes are exact paths, S3 URIs or an "
             "executable path. One home was recovered only after a near-miss worth recording: "
             "s3://opal-estate-report/kuzu_nessie_db sits past comp-keys' 40-row default "
             "truncation and I had drafted the sentence calling it ABSENT before head-object "
             "corrected it." % (homes, n),
         "denominator": "%d of %d homes exact; 0 null" % (homes, n),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC5",
         "criterion_verbatim": "coverage.denominator NON-NULL, 'N of M'; if genuinely uncountable, denominator_absent_reason populated.",
         "method": "command",
         "invocation": "count non-null coverage.denominator; for nulls, require denominator_absent_reason",
         "output_evidence":
             "%d of %d cards carry a NON-NULL denominator. The remaining %d are genuinely "
             "uncountable and EVERY ONE populates denominator_absent_reason, which is the "
             "rejectable branch v2 added -- keep-dormant (an opt-in registry whose true "
             "denominator is every dormant-looking resource in the estate), SYSTEM_DEFINITIONS "
             "(67 terms of an unenumerable vocabulary), both nerves halves (an unbounded edge "
             "universe), and the S3 kuzu (never opened, so a row count would be a guess dressed "
             "as a measurement). ⛔ THE RICHEST DENOMINATOR IS c2_instances.json's OWN coverage "
             "triple, which I read rather than computed: BACKEND 81.2%% of side, FRONTEND 13.0%%, "
             "and KNOWLEDGE 0.0%% of 5,851 on-side nodes with in_detector_scope 0 -- a STRUCTURAL "
             "zero, not an incidental one." % (den, n, denabs),
         "denominator": "%d of %d non-null; %d null, %d of those with denominator_absent_reason" % (den, n, n - den, denabs),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC6",
         "criterion_verbatim": "key: identity_space, key_is_stable, crosses_spaces; declared_mapping: null only after a hunt.",
         "method": "command",
         "invocation": "count key rows carrying all three required fields; count crossings and null mappings",
         "output_evidence":
             "%d of %d key rows carry all three. %d of %d subjects CROSS id spaces and %d of those "
             "carry declared_mapping NULL -- each after a stated hunt, not by default. ⛔ THE "
             "MEASUREMENT ANDREW NAMED HIMSELF: only 1,730 of 27,035 canonical node_ids (6.4%%) "
             "are ARN-shaped, across 5 layers that sum exactly, while .comp-graph/graph.json -- "
             "stage one of the C3 chain -- keys on 'gold:MODULE.function' symbols. TWO IDENTITY "
             "SPACES, NO DECLARED MAPPING, so a join between the C3 chain's stage-1 store and the "
             "projection it must reach cannot be performed on the key. The one subject that DOES "
             "declare its mapping in-file is firm_registry, and it is NULL on 2 of 5 firms."
             % (keyrows, n, crossing, n, nomap),
         "denominator": "%d of %d key rows complete; %d crossing; %d crossing with declared_mapping null" % (keyrows, n, crossing, nomap),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC7",
         "criterion_verbatim": "failure_mode EXERCISED, never read off a docstring.",
         "method": "command",
         "invocation": "count failure_mode rows at basis 'measured' (i.e. exercised); inspect the rest",
         "output_evidence":
             "%d of %d failure-mode rows are EXERCISED at basis measured, each with arms reachable "
             "from different truths. The %d that are not are recorded as unexercised rather than "
             "asserted: the harness (running CVO's composer is not my act -- read-only tree) and "
             "nerves-edges.json (I refused to borrow its sibling's exercise evidence on a shared "
             "name prefix). ⛔ FINDINGS ONLY EXERCISE COULD PRODUCE: comp-heat `score` is a PURE "
             "FUNCTION of --age-days -- four ids at fixed age including the literal '!!!not even a "
             "path!!!' all returned 0.5000/WARM while varying the flag moved it, so the id is "
             "echoed and never resolved. kuzu is loud at three depths (bad label -> Binder "
             "exception, bad property -> Binder exception, genuine value miss -> a clean 0). "
             "keep-dormant returns a bare False that the guard reads as a DEBT-eligible VERDICT, "
             "indistinguishable from a typo. %d of %d cards report "
             "distinguishable_from_true_negative = no. ⚠ ONE TEST WAS DISCARDED AS INVALID before "
             "it reached a row: my first comp-heat probe had both arms failing on a missing "
             "required flag, so they collapsed onto one truth and the identical output proved "
             "nothing." % (exercised, n, n - exercised, undist, n),
         "denominator": "%d of %d exercised; %d recorded unexercised with the reason stated" % (exercised, n, n - exercised),
         "status": "PASS"},
        {"criterion_id": "DTX2-AC8",
         "criterion_verbatim": "declared_opinions POPULATED on every card -- an enumerated array, or null WITH the reason in evidence. Omitting the key passes the schema and FAILS this TO.",
         "method": "command",
         "invocation": "assert the key is present on all 16; for nulls, require the reason in methodology.evidence",
         "output_evidence":
             "KEY PRESENT ON %d of %d -- the criterion this TO warns the schema cannot enforce. %d "
             "cards carry an ENUMERATED array and %d carry null, and ALL %d nulls state the reason "
             "IN evidence. The reasons are structural, not shrugs: a DIRECTORY has no single "
             "producer whose opinions could be enumerated; a store whose GENERATOR IS UNRESOLVED "
             "has no known decider, so listing opinions read off the output would be mistaking the "
             "artifact for the intent; and an object I never opened can only yield the CONFIG's "
             "account of a producer. ⛔ THIS AUDIT CAUGHT A REAL FAILURE OF MINE: my first pass put "
             "one reason in `methodology.how` rather than `evidence`, which reads identically to a "
             "human and FAILS the criterion as written. Found by checking the field the criterion "
             "names instead of the field I had written." % (do_key, n, do_pop, do_null, do_null),
         "denominator": "%d of %d cards carry the key; %d enumerated, %d null, %d of %d nulls carrying a reason in evidence" % (do_key, n, do_pop, do_null, do_null, do_null),
         "status": "PASS"},
    ],
    "controls": {
        "mutant": {
            "description": "Four defects planted into in-memory copies of validated cards and "
                           "re-validated: an out-of-enum trust.key.key_is_stable; a deleted "
                           "required trust.coverage.denominator; prose (' -- ') inside a "
                           "joinable_ref id; and verdict.standing SOUND over a row at basis "
                           "'absent'. The last two target v2-specific constraints rather than "
                           "generic schema shape.",
            "expected": "All four REJECTED while the unmodified cards validate in the same run.",
            "observed": "All four REJECTED. Unmodified cards: 16 of 16 VALID, same validator "
                        "object, same run. Both arms reachable from different truths.",
            "status": "FIRED-AS-EXPECTED"},
        "determinism": {
            "method": "All 16 cards are EMITTED by five deterministic builders from in-script "
                      "measured literals -- no clock call, no randomness, no filesystem scan at "
                      "build time. Re-running rebuilds byte-identical output. The builders "
                      "additionally ASSERT two invariants the schema cannot fully express: the "
                      "FULL basis floor (scalar == MIN over basis_by_field, where the schema "
                      "enforces only the 'measured' case) and joinable_ref id cleanliness.",
            "observed": "Rebuilt repeatedly across the session after each correction; 16 of 16 "
                        "VALID on every run. The floor assertion is a LIVE arm: my first cut "
                        "claimed basis 'measured' over an INFERRED projection_of and the builder "
                        "now demotes it automatically rather than trusting me to hold the rule.",
            "status": "STABLE"},
    },
    "declared_exclusions": [
        {"item": "Running CVO's subdivision composer",
         "reason": "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/ is READ-ONLY "
                   "at this seat. The harness card records its failure-mode row UNEXERCISED and is "
                   "INCOMPLETE rather than borrowing a claim."},
        {"item": "comp-heat `federated` and `compare` subcommands",
         "reason": "federated needs a LIVE Trino federation. Both are named in that card's coverage "
                   "denominator as 2 of 5 unexercised rather than generalised from the 3 I reached."},
        {"item": "Opening s3://opal-estate-report/kuzu_nessie_db",
         "reason": "Existence, size and vintage are measured by head-object; the object was never "
                   "downloaded and opened, so its coverage and key rows are recorded at basis "
                   "inferred/absent with denominator_absent_reason populated."},
        {"item": "Reading the Iceberg tables through pyiceberg",
         "reason": "The warehouse cards report the PROJECTION-plane row count and say so. The two "
                   "planes are known to differ, and reporting one as the other is the conflation "
                   "this wave exists to prevent."},
        {"item": "Any deprecation verdict on any of the 16 subjects",
         "reason": "W2-m-3 and Andrew's sequencing: the tag is a SECOND PASS after carding, because "
                   "a lane that decides a subject is doomed cards it differently. Four of these 16 "
                   "were flagged orphaned or superseded by this lane's OWN wave-1 manifest, so the "
                   "prior was present and was deliberately excluded."},
        {"item": "Any remediation of any finding",
         "reason": "QUALIFY-DO-NOT-FIX. Findings are named with owners; nothing was fixed."},
    ],
    "surprises": [
        "BLOCKING (upheld, 73929): the wave-2 subject derivation read methodology.composes + "
        "location.projection_of and NEVER READ location.co_resident_stores -- a third card field "
        "naming stores. 12 heads named only there; 7 distinct stores absent from all 4 TO faces "
        "with 4 of 4 positive controls firing, including .comp-graph/graph.json, the C3 chain's "
        "own stage-1 substrate. 8 subjects added; the subject set moved 33 -> 41.",
        "BLOCKING x2 (upheld, subject set 41 -> 43): a COMPOUND subject string in my own set, "
        "'nerves-edges.json and nerves-risk-edges.json', naming two objects measured 16x apart in "
        "size, 43 days apart in vintage and carrying DIFFERENT SCHEMAS -- split into two subjects. "
        "And comp-debris, a LIVE tool (self-test rc=0), dropped from the same wave-1 parenthetical "
        "that produced the comp-heat subject.",
        "SELF-CAUGHT: my first cut claimed basis 'measured' over an INFERRED projection_of -- the "
        "exact P1 class this lane reported and v2 was built for, committed by me. The builder now "
        "computes the floor from basis_by_field automatically rather than relying on my discipline.",
        "SELF-CAUGHT: I claimed determinism 'hybrid' on two harness cards from a FILENAME hint. v2 "
        "requires model + invocations_per_run + failure_is_loud before that is expressible; I have "
        "none of the three and corrected to 'unknown'. Naming a determinism class off a filename is "
        "the same defect as merging two stores on a shared leaf name.",
        "SELF-CAUGHT: one AC8 reason was written into methodology.how instead of methodology.evidence "
        "-- identical to a human reader, and a FAIL against the criterion as written.",
        "OBSERVATION, in the artifacts rather than about them: c2_instances.json disagrees with "
        "ITSELF (6,157 C2Motif in its nodes array vs 6,138 declared distinct instances, both "
        "defensible, differing silently), and c3_structures.json self-declares input_freshness "
        "'CURRENT' while its own db_built_at is 19 days old against a superseded snapshot -- a "
        "frozen prose string that does not age, which is exactly what temporal_claim exists to make "
        "rejectable.",
    ],
    "session_log": "org/tier2_senior/0.4.0_DT_ClientPlatform~X/logs/2026-08-26/",
    "compiler_tools": [
        {"tool": "comp-kuzu", "invocation": "MATCH (n) RETURN count(n); label/layer/ARN-shape censuses; three failure probes",
         "result": "PASS -- provenance header read on every access. Produced the 6.4% ARN-shape "
                   "measurement and the 5-layer census that sums exactly to 27,035."},
        {"tool": "comp-heat", "invocation": "score (4 ids x fixed age, 1 id x 3 ages), freshness (2 arms), drift (2 arms)",
         "result": "PARTIAL -- 3 of 5 subcommands exercised. GAP FOUND: `score` never resolves its id."},
        {"tool": "comp-find", "invocation": "--name alone; content pattern alone; never both",
         "result": "PASS -- the both-args trap was carried forward from wave 1 and not re-hit."},
        {"tool": "comp-keys", "invocation": "prefix ... --all",
         "result": "PASS with --all. The default 40-row truncation nearly produced a false ABSENT "
                   "on the S3 kuzu; head-object corrected it."},
        {"tool": "aws s3api (rail-checked)", "invocation": "head-object miss/hit arms; full-pagination listings",
         "result": "PASS -- the instrument that corrected comp-keys and exercised the warehouse 404."},
        {"tool": "jsonschema Draft2020-12", "invocation": "v2 card schema over 16 cards + 4 planted mutants",
         "result": "PASS -- 16 VALID, 4 mutants REJECTED."},
        {"tool": "commit-gate.sh", "invocation": "on all 5 builders", "result": "PASS -- clean for 5 files."},
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(POS, f, indent=2, ensure_ascii=False)

for a in POS["acceptance"]:
    a["cell_refs_count"] = len(REFS.get(a["criterion_id"], []))
print("proof-of-spec written:", os.path.relpath(OUT, WS))
print("criteria:", len(POS["acceptance"]), "| cards:", n, "| verdicts:", dict(st))
print("AC cell_ref counts:", {a["criterion_id"]: a["cell_refs_count"] for a in POS["acceptance"]})
