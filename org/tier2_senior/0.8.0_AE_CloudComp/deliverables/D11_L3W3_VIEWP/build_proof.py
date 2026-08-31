#!/usr/bin/env python3
"""Build the TO-L3W3-CCY proof of spec.

criterion_verbatim is EXTRACTED FROM THE FACE'S BYTES, never retyped -- a retyped oracle is a
paraphrase waiting to happen, and the face requires the oracle quoted verbatim.

Run:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_VIEWP/build_proof.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FACE = ROOT / "org/tier2_senior/0.8.0_AE_CloudComp/task_orders/NFRA_C3MATERIALIZE.TO-L3W3-CCY.k-sweep.md"
VIEWP = ROOT / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_VIEWP/VIEWP_firm_partition.json"
OUT = ROOT / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_C3MATERIALIZE.TO-L3W3-CCY_PROOF_OF_SPEC.json"

D = "D11_L3W3_VIEWP"
PEND = "PENDING-THIS-COMMIT"


def face_oracles() -> dict[str, dict[str, str]]:
    """Pull <criterion id=..><cell_refs><label><oracle> straight out of the face."""
    text = FACE.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(
        r'<criterion id="([^"]+)">\s*<cell_refs>([^<]*)</cell_refs>\s*'
        r"<label>([^<]*)</label>\s*<oracle>(.*?)</oracle>",
        text,
        re.S,
    ):
        cid, refs, label, oracle = m.groups()
        out[cid] = {
            "cell_refs": refs.strip(),
            "label": label.strip(),
            "oracle": " ".join(oracle.split()),
        }
    return out


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


DENOMINATOR = {
    "L3W3-CCY-AC1": (
        "1,337 members against a 19,482-entity population; BOTH directions printed (1,337/1,337 and 1,337/19,482); 2 negative controls of 50 each, both 0 of 50"
    ),
    "L3W3-CCY-AC2": (
        "1,337 of 1,337 members carry a firm label, 0 unresolved, over 3 distinct firm tokens; segment-2 consistency 1,337 of 1,337"
    ),
    "L3W3-CCY-AC3": (
        "1,337 MEASURED + 18,145 ABSENT = 19,482 entities; metric domain 893,116 both-measured pairs beside the 189,764,421 union domain"
    ),
    "L3W3-CCY-AC4": (
        "438,018 positives x 455,098 negatives = 199,341,115,764 (positive, negative) comparisons, 0 cross-class ties; parse agreement 1,337 of 1,337"
    ),
    "L3W3-CCY-AC5": (
        "2 typed fields, each read from its own shard row (L3W1-ypbj-2 and L3W1-ypbj-7) of the 8 rows the shard carries"
    ),
    "L3W3-CCY-AC6": (
        "893,116 both-measured pairs = 438,018 same-firm + 455,098 cross-firm; 3 of 3 same-firm terms recomputed"
    ),
    "L3W3-CCY-AC7": (
        "171 mdpf same-firm pairs of 438,018 total ones (0.00039), from 19 of 1,337 symbols"
    ),
    "L3W3-CCY-AC8": (
        "|left| 1,337, |right| 3, |join| 1,337, 0 unresolved"
    ),
    "L3W3-CCY-AC9": (
        "3 inputs, each cited path @ commit with the sha256 of the bytes read; the shard hashed at 3 of 3 candidate pins, all identical"
    ),
}


# what THIS lane actually did for each criterion; the oracle text itself comes from the face
EVIDENCE = {
    "L3W3-CCY-AC1": (
        "BOTH DIRECTIONS PRINTED, as the oracle requires, because a one-sided match cannot read as "
        "membership. Direction A: 1,337 of 1,337 members resolve into the population. Direction B: "
        "1,337 of 19,482 population entities resolve into the members. Stronger than the oracle asks "
        "and volunteered: the member set is SET-EQUAL to the population's layer=='pipeline' block "
        "(members\\pipeline = 0, pipeline\\members = 0), and the layer histogram "
        "{portal 10365, ms 6047, aws 1733, pipeline 1337} sums to the declared denominator 19,482. "
        "The population was read THROUGH its pin (git show 64ae1ae879:...L2_VIEW_ARTIFACTS.json), so "
        "its pin and its bytes cannot disagree; its id list is 19,482 long and 19,482 DISTINCT, equal "
        "to its own declared denominator, so the list and the declaration agree and neither is "
        "assumed. NEGATIVE CONTROL: 50 member ids mutated with a '::__NOT_A_REAL_SYMBOL__' suffix "
        "resolve 0 of 50, and 50 population ids known to be outside the member set resolve 0 of 50 -- "
        "the equality test demonstrably CAN fail. NO CHAIN was used or attempted: the 4-hop "
        "cloud-node -> arn -> motif -> symbol -> firm composition is MOOT and REFUSED per the oracle."
    ),
    "L3W3-CCY-AC2": (
        "W_P(i,j) = 1 if firm(i) == firm(j) else 0. Fan-in RECOMPUTED from the pinned labels: "
        "bd 724 / inf 594 / mdpf 19, summing to 1,337 with 0 unresolved and |right| = 3 distinct firm "
        "tokens -- reproducing the shard's declared FLOOR exactly, DERIVED not copied. "
        "GRAIN DISCLOSURE, and it is the substantive finding of this cell: THE SHARD DOES NOT CARRY A "
        "PER-ENTITY FIRM MAP. pipesym_to_firm is a ROLLUP_CONTAINMENT bridge DESCRIPTOR whose 8 rows "
        "(L3W1-ypbj-1..8) carry endpoints, basis, join evidence, card keys, cardinality class, "
        "firm-carry, declarability and failure mode -- not 1,337 labels. Its own declared_by_store "
        "field reads 'NO -- the firm is recoverable only by parsing segment 2 of the pipeline id. No "
        "store declares it.' So 'read the shard, never re-parse independently' is discharged as: the "
        "RULE, the BASIS and the FLOOR come from the shard, and the per-entity LABELS come from the "
        "pinned cell input the face's own AC9 names as listing the ids WITH their labels. No "
        "independent re-parse was performed as the authority. CONSISTENCY, EXPLICITLY NOT "
        "CORROBORATION: a segment-2 parse agrees with the pinned labels 1,337 of 1,337 -- but the "
        "pinned labels ARE a segment-2 parse, so the two readings share one substrate and one method. "
        "Recorded as consistency; presenting it as independent confirmation would be false."
    ),
    "L3W3-CCY-AC3": (
        "MEASURED 1,337 / ABSENT 18,145 / denominator 19,482 = 6.9% measured, 93.1% absent. "
        "ABSENT IS CARRIED AS ABSENT AND IS NEVER A COMPARABLE VALUE; no 0.0 substitution occurs "
        "anywhere in the build. The metric domain stays the ruled both-measured C(1337,2) = 893,116 "
        "and the union domain C(19482,2) = 189,764,421 is printed BESIDE it so the reader can see "
        "which one any number belongs to -- the coercion the oracle forbids is precisely the silent "
        "move between those two. MASK: the per-entity MEASURED/ABSENT mask IS the pinned member list; "
        "an entity is MEASURED iff its entity_id is in that list. Entity order is the mask carrier's, "
        "ascending index in entity_set.entities @64ae1ae879 -- and that convention is EXERCISED, not "
        "asserted: materialising the measured entities' indices gives min 10761, max 12097, count "
        "1,337, and the block is CONTIGUOUS (12097 - 10761 + 1 == 1337). A consumer can therefore "
        "carry the mask as one range instead of 19,482 flags. POSITIVE CONTROL: the split is "
        "non-degenerate in both directions (1,337 / 18,145), so the classifier demonstrably assigns "
        "both values."
    ),
    "L3W3-CCY-AC4": (
        "role = CONTROL_ONLY and six_three = 6.3_NOT_A_RESULT are TYPED FIELDS with declared value "
        "domains, not prose, so a consumer rejects on the field. The 6.3 NUMBER IS PRINTED AS THE "
        "ORACLE REQUIRES and it is 1.0 -- COMPUTED, not asserted: ROC-AUC of W_P scored against the "
        "same-firm label over 438,018 positives x 455,098 negatives = 199,341,115,764 (positive, "
        "negative) comparisons, all concordant, 0 cross-class ties, by the Mann-Whitney identity. It "
        "is 1.0 EXACTLY AND TAUTOLOGICALLY because the score IS the label, and it is labelled NOT A "
        "RESULT for that reason. CIRCULARITY TYPED BESIDE IT: P's firm label IS the 6.3 cohort label "
        "on these same entities (parse agreement 1,337/1,337), so fusing view 1 with P and evaluating "
        "6.3 on that cohort would INHERIT the thing being tested. I ALSO NAME THE CONTROL THAT DOES "
        "NOT WORK: permuting the firm labels leaves the same-firm pair COUNT unchanged, because "
        "shuffling permutes labels without changing block sizes -- so a size-based shuffle control is "
        "structurally incapable of falsifying this number. The tautology lives in the IDENTITY of "
        "score and label. PRD sec 6.3's parenthetical 0.989 / 0.974 are NOT carried: Addendum 1f "
        "@76c688fa3d states they are not a floor and are never carried into a 6.3 evaluation."
    ),
    "L3W3-CCY-AC5": (
        "basis = INFERRED and declarability = NAMED_GAP_STORE_OWNER, both READ OUT OF THE SHARD's own "
        "rows (basis from L3W1-ypbj-2, declarability from L3W1-ypbj-7) rather than restated from "
        "memory, with the shard's gap_owner string carried verbatim. 'Carried exactly as the shard "
        "says' is discharged by reading the shard at its pin in the same run that emits the row. "
        "INFERRED is the segment-2 parse -- the SAME parse the certified cohort labels carry -- "
        "admissible at that typed basis and NEVER promoted to measured; the schema's enum makes the "
        "promotion mechanically refusable rather than merely discouraged. A DECLARED per-entity firm "
        "is the L1-spine named gap; it does not gate this wave and is not claimed as closed."
    ),
    "L3W3-CCY-AC6": (
        "same_firm_pairs 438,018 = C(724,2) 261,726 + C(594,2) 176,121 + C(19,2) 171; cross_firm_pairs "
        "455,098; denominator C(1337,2) = 893,116; fraction_ones 0.4904. Every term RECOMPUTED from "
        "the fan-in this run derived, not copied from the oracle -- the oracle's figures are the check, "
        "not the source. Typed as arms[P].base_rate per the design lane @6d23af95b9, with the print "
        "rule 'PRINTED BESIDE EVERY P ROW AT EVERY K' carried on the row itself. THE STOP IS HONOURED "
        "AND STATED ON THE ARTIFACT: it is a FRAME THE READER NEEDS, NOT A DISCOUNT TO APPLY. ROC-AUC "
        "is invariant to class prevalence by construction -- it ranks within each class and the "
        "positive:negative ratio cancels -- so a near-balanced P does NOT inflate its AUC, and NO ROW "
        "OF THIS ARTIFACT DEFLATES A P RESULT BY 0.4904. PR-AUC would be prevalence-sensitive; this is "
        "not. The history is carried too: 0.8.0_AE_CloudComp~X supplied this number with the opposite "
        "consequence attached and withdrew that consequence itself at 81337."
    ),
    "L3W3-CCY-AC7": (
        "firm_representation = bd_vs_inf is emitted under THE ONE LIVE FIELD NAME ruled @9cfa4eebbf. "
        "arms[P].effective_partition IS NOT EMITTED ANYWHERE IN THE ARTIFACT -- not as a key, not as "
        "an alias, not as a courtesy duplicate -- because two live names for one quantity disagree "
        "silently (0.8.0_AE_CloudComp~X 81407), and the schema REFUSES the artifact if either spelling "
        "appears beside it. mdpf_share_of_ones = 0.00039 TYPED, derived as 171 same-firm pairs from 19 "
        "symbols against 438,018 total ones. THE SHARP FORM IS CARRIED IN THOSE WORDS: MDPF SEPARATION "
        "IS UNMEASURABLE IN THIS ARM, not merely small. P is EFFECTIVELY a two-block bd-versus-inf "
        "partition, and the row states that any per-firm reading of this sweep IS a bd-versus-inf "
        "reading and must say so rather than implying three-firm coverage. Untouched by the prevalence "
        "correction: this is representation, not base rate."
    ),
    "L3W3-CCY-AC8": (
        "BOTH ARE STATED SIDE BY SIDE with the reason they are not in conflict. cardinality_class = "
        "UNMEASURED is about FAN-OUT at the full-id grain, unmeasurable by construction on a roll-up -- "
        "and the shard's own probe_can_return_multiple is False, so the probe CANNOT return >1 parent "
        "and therefore cannot measure fan-out, which is why the class reads UNMEASURED rather than 1. "
        "COVERAGE is the shard's own join run L3W1-ypbj-3: |left| 1,337, |right| 3, |join| 1,337, ZERO "
        "unresolved. An arm claiming full coverage beside a bridge row reading UNMEASURED is "
        "CONSISTENT, and the row says why in words a reader does not have to re-derive: UNMEASURED "
        "describes how many children a parent has at a grain the roll-up cannot see; coverage "
        "describes whether every child resolved to a parent, and every one did."
    ),
    "L3W3-CCY-AC9": (
        "Three inputs, each cited path @ commit WITH the sha256 of the bytes THIS RUN read: the "
        "population (L2_VIEW_ARTIFACTS.json @64ae1ae879), the pinned cell input "
        "KSWEEP_POSITIVE_ARM_PROBE.json @fb0a013b04 (schema "
        "nfra-c3materialize.l3w2.ksweep.positive-arm-probe/1.0, which LISTS the 1,337 member ids with "
        "their labels -- so this cell cites a PINNED POPULATION, not a description of one), and the "
        "pipesym_to_firm shard. All three were read with `git show <pin>:<path>`, so pin and bytes "
        "cannot disagree. SETTLED-PIN RESOLUTION, done by CONTENT rather than by ancestry because the "
        "face says 'the SETTLED registry pin' without naming it and three candidates circulate: the "
        "shard hashes IDENTICALLY at 5ab05ee4bd, 8ff31fa1c8 and b8c47d1233, so the choice is MOOT and "
        "no reading depends on it; a sibling shard in the same directory hashes differently, so the "
        "digest discriminates. The ruling is cited via ruling_pins and the pins map. THIS CELL NAMES "
        "NEITHER A PIN COUNT NOR A PUSH STATE, per the oracle's [HISTORICAL] clause -- restating "
        "either would be a second carrier of what the map already holds."
    ),
}


def main() -> None:
    oracles = face_oracles()
    missing = set(EVIDENCE) - set(oracles)
    if missing:
        raise SystemExit(f"FAIL: criteria in evidence but not in the face: {sorted(missing)}")
    extra = set(oracles) - set(EVIDENCE)
    if extra:
        raise SystemExit(f"FAIL: criteria in the face with no evidence: {sorted(extra)}")

    acceptance = []
    for cid in sorted(oracles, key=lambda c: int(c.rsplit("AC", 1)[1])):
        o = oracles[cid]
        acceptance.append({
            "criterion_id": cid,
            "criterion_verbatim": o["oracle"],
            "method": "command",
            "invocation": (
                "python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_VIEWP/"
                "build_viewP.py  (deterministic; reads every input through its pin)"),
            "output_evidence": EVIDENCE[cid],
            "denominator": DENOMINATOR[cid],
            "status": "PASS",
        })

    proof = {
        "schema_version": "1.0",
        "to_id": "NFRA_C3MATERIALIZE.TO-L3W3-CCY",
        "firm": "FABRIC",
        "phase": "NON-BUILD-OTHER",
        "assignee": "0.8.0_AE_CloudComp~Y",
        "decomp_ref": {
            "doc": ("workflows/atom_decomposition/runs/nfra-c3materialize-L3/"
                    "20260829T1906Z/DECOMP.md"),
            "vintage_commit": "94935b740e",
            "to_ref": ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
                       "NFRA_C3MATERIALIZE.TO-L3W3-CCY.k-sweep.md"),
        },
        "spec_ref": {
            "doc": "docs/architecture/NFRA_C3MATERIALIZE_PRD.md",
            "group": "OTHER",
            "vintage_commit": "f757ed7129",
        },
        "artifacts_produced": [
            {
                "path_or_key": f"org/tier2_senior/0.8.0_AE_CloudComp/deliverables/{D}/VIEWP_firm_partition.json",
                "kind": "config_data",
                "commit_or_etag": PEND,
                "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
                "deploy_evidence": ("VIEW P prep: 9 rows, all WRITTEN, all sequence_gate 'now'. A new "
                                    "D11-owned artifact; no producing store written and none re-run."),
                "artifact_covered_by": [f"L3W3-CCY-AC{i}" for i in range(1, 10)],
            },
            {
                "path_or_key": f"org/tier2_senior/0.8.0_AE_CloudComp/deliverables/{D}/build_viewP.py",
                "kind": "script",
                "commit_or_etag": PEND,
                "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
                "deploy_evidence": ("The deterministic derivation. Passed .tools/commit-gate.sh "
                                    "(py_compile + ds-precommit + ruff py39), 1 of 1 clean."),
                "artifact_covered_by": [f"L3W3-CCY-AC{i}" for i in range(1, 10)],
            },
            {
                "path_or_key": f"org/tier2_senior/0.8.0_AE_CloudComp/deliverables/{D}/VIEWP_L3W3.schema.json",
                "kind": "config_data",
                "commit_or_etag": PEND,
                "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
                "deploy_evidence": ("Makes the face's prose refusals mechanically firable: the three "
                                    "rectangle value_domains, the ABSENT-to-0.0 coercion, the metric-"
                                    "domain shift, and the retired-alias second token."),
                "artifact_covered_by": ["L3W3-CCY-AC3", "L3W3-CCY-AC4", "L3W3-CCY-AC5",
                                        "L3W3-CCY-AC7"],
            },
        ],
        "acceptance": acceptance,
        "controls": {
            "mutant": {
                "description": (
                    "Seven mutations of the REAL delivered artifact through the same validator that "
                    "admitted it, each one a failure the FACE names: ABSENT coerced to 0; the metric "
                    "domain moved from the both-measured 893,116 to the union 189,764,421; role "
                    "CONTROL_ONLY -> RESULT; basis INFERRED -> MEASURED; the retired "
                    "effective_partition alias emitted as a live second token; firm_representation "
                    "bd_vs_inf -> three_firm; the provenance row removed. Paired with the UNMUTATED "
                    "artifact as a positive control, because a refusal alone cannot distinguish 'the "
                    "schema caught the mutation' from 'the artifact was invalid anyway'."),
                "expected": "All seven REFUSED; the unmutated artifact PASSES.",
                "status": "FIRED-AS-EXPECTED",
                "observed": ("Positive control PASS. 7 of 7 REFUSED, each naming its own field: "
                             "ABSENT=0 -> 'less than or equal to the minimum of 0'; domain -> "
                             "'893116 was expected'; role -> \"'RESULT' is not one of "
                             "['CONTROL_ONLY']\"; basis -> \"'MEASURED' is not one of ['INFERRED']\"; "
                             "alias -> the 'not' constraint fires; firm_representation -> "
                             "\"'three_firm' is not one of ['bd_vs_inf']\"; provenance -> "
                             "\"'provenance' is a required property\"."),
            },
            "determinism": {
                "status": "STABLE",
                "method": ("The build re-run three times; the artifact's sha256 compared across "
                                "runs. Negative control: a single mutated field is hashed to confirm "
                                "the digest MOVES when the content does, so 'identical' is a result "
                                "and not a property of the instrument."),
                "observed": ("Identical across 3 runs "
                             "(6cd7c1b1d473aa324c1523f7b92a95b2ccc0e26e24fe07f06bb9f5054a45543f). "
                             "The mutated-field digest differs, so the comparison discriminates."),
            },
        },
        "declared_exclusions": [
            {"item": "The 4-hop cloud-node -> arn -> motif -> symbol -> firm chain for membership.",
             "reason": ("AC1 declares it MOOT and REFUSED -- it would traverse a COVER bridge "
                        "backward through an undeclared hop to reach entities already in the set. "
                        "Not attempted, not partially attempted.")},
            {"item": "Any ABSENT -> 0.0 conversion for the 18,145 absent entities.",
             "reason": ("AC3 forbids it: a 0.0 is a MEASURED statement of no affinity, ABSENT is the "
                        "statement that nothing was measured, and the coercion would move the metric "
                        "domain off the ruled 893,116 onto the union silently.")},
            {"item": "Any deflation of a P result by the 0.4904 base rate.",
             "reason": ("AC6's STOP. ROC-AUC is invariant to class prevalence by construction, so the "
                        "fraction is a frame the reader needs, not a discount to apply.")},
            {"item": "arms[P].effective_partition as a live emitted token.",
             "reason": ("AC7: retired name, schema-declared alias only. Two live names for one "
                        "quantity disagree silently. The schema refuses it beside firm_representation.")},
            {"item": "The 9 PROJECT_MECHANISM cells L3W3-m-1..9.",
             "reason": ("Present on the face but DISCHARGED BY THE ISSUER, not owned by this lane. "
                        "Not written here.")},
            {"item": "PRD sec 6.3's 0.989 / 0.974 figures.",
             "reason": ("Addendum 1f @76c688fa3d rules they are section-4 evidence on single views "
                        "that are not the fused ones, are NOT a floor, and are NEVER carried into a "
                        "6.3 evaluation.")},
        ],
        "surprises": [
            (
                    "OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): THE SHARD THE FACE POINTS AT FOR FIRM LABELS DOES NOT CARRY THEM. AC2 says "
                    "'firm taken from pipesym_to_firm rows L3W1-ypbj-1..8 ... read the shard, never "
                    "re-parse independently', but pipesym_to_firm is a ROLLUP_CONTAINMENT bridge "
                    "DESCRIPTOR: its 8 rows carry the subject's endpoints, basis, join evidence, card "
                    "keys, cardinality class, firm-carry, declarability and failure mode -- there is "
                    "no per-entity firm map in it, and its own declared_by_store says so in words. I "
                    "discharged AC2 by taking the RULE, BASIS and FLOOR from the shard and the "
                    "per-entity LABELS from the pinned cell input the face's own AC9 names as listing "
                    "the ids WITH their labels, and disclosed that reading on the row. Raising it so "
                    "the issuer can confirm the reading rather than discover it later; the numbers are "
                    "unaffected either way, since the labels reproduce the shard's declared floor "
                    "exactly."),
            (
                    "OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X): A CITATION THAT RESOLVES FOR A HUMAN AND NOT FOR A PROGRAM. The pinned probe "
                    "cites its population as 'L2_VIEW_ARTIFACTS.json views[STRUCTURE].entity_set' -- "
                    "map-style access on what is a LIST of two views. Any consumer that takes the "
                    "citation literally gets a TypeError, not a wrong answer, so this is loud rather "
                    "than silent. This build selects by views[i].view_id == 'STRUCTURE' and asserts "
                    "exactly one match. Surfaced, not chased."),
            (
                    "OBSERVATION / INERT (3.0.0_SA_CVO~X, cc 2.0.0_SA_COO~X, 0.7.0_AE_CloudOps~X): THE MEASURED BLOCK IS CONTIGUOUS, WHICH NOBODY ASKED FOR AND THE CONSUMER CAN "
                    "USE. The 1,337 measured entities occupy indices 10761..12097 of the 19,482-entity "
                    "set with no gaps, so the MEASURED/ABSENT mask is expressible as ONE RANGE rather "
                    "than 19,482 flags. Relevant to 0.7.0_AE_CloudOps~X, whose face asks this artifact "
                    "for a per-entity mask over the full population. Found only because the ordering "
                    "convention was exercised rather than asserted -- the linter flagged the unused "
                    "index map, and using it properly instead of deleting it produced this."),
        ],
        "session_log": ("org/tier2_senior/0.8.0_AE_CloudComp/logs/2026-08-30/ (written at session "
                        "close, with a mandatory Compiler Tools section)"),
        "compiler_tools": [
            {
                "tool": "git show (pinned read)",
                "invocation": "git show <pin>:<path> for all three inputs, via msys_safe_run",
                "result": ("PASS. Every input read THROUGH its pin, so pin and bytes cannot disagree. "
                           "Also the instrument that resolved the settled-pin question by content."),
            },
            {
                "tool": "comp-find",
                "invocation": "--name on KSWEEP_POSITIVE_ARM_PROBE, positive_arm_probe, "
                              "pipesym_to_firm, L2_VIEW_ARTIFACTS; content on L3W1-ypbj",
                "result": ("PASS, with denominators printed (1 hit across 135,443 files scanned, "
                           "71,496 ephemeral-floor excluded). Located every pinned input. One "
                           "unbounded regex alternation over the full corpus exceeded 120s and was "
                           "backgrounded -- scope the pattern, not the corpus."),
            },
            {
                "tool": "comp-to",
                "invocation": "comp-to NFRA_C3MATERIALIZE.TO-L3W3-CCY",
                "result": ("PASS, read back and verified BEFORE the first derivation ran, so no row "
                           "here lands in the unbound class 0.7.0_AE_CloudOps~X measured at 84087. "
                           "Note: comp-to accepts any string, so `comp-to --help` silently BINDS THE "
                           "SESSION TO '--help' rather than printing usage. Caught by reading the "
                           "confirmation line."),
            },
            {
                "tool": ".tools/commit-gate.sh",
                "invocation": "commit-gate.sh build_viewP.py, build_proof.py",
                "result": ("CAUGHT A REAL DEFECT, and this is the entry worth reading: ruff F841 "
                           "flagged an unused index map. It was unused because I had asserted the "
                           "mask's entity ORDER in prose while no code exercised it. Using it "
                           "properly rather than deleting it turned an assertion into a measurement "
                           "and surfaced the contiguity finding. Clean on re-run."),
            },
            {
                "tool": "jsonschema (2020-12)",
                "invocation": "Draft202012Validator over the real artifact + 7 planted mutants",
                "result": "PASS. 7 of 7 refused, positive control green.",
            },
        ],
    }

    OUT.write_text(json.dumps(proof, indent=1) + "\n", encoding="utf-8")
    print(f"OK: wrote {OUT.relative_to(ROOT)}")
    print(f"OK: {len(acceptance)} criteria, oracles EXTRACTED from the face (not retyped)")
    for a in acceptance:
        print(f"   {a['criterion_id']}  verbatim={len(a['criterion_verbatim'])} chars  den={a['denominator'][:48]}...")


if __name__ == "__main__":
    main()
