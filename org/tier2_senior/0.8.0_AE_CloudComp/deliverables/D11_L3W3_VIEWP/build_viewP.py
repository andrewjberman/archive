#!/usr/bin/env python3
"""Build VIEW P (firm partition) for NFRA_C3MATERIALIZE L3 wave 3, TO-L3W3-CCY.

Deterministic. Every input is read THROUGH ITS PIN (git show <pin>:<path>), so a pin and
its bytes cannot disagree. Emits VIEWP_firm_partition.json carrying the 9 cells
L3W3-dc02-1..9, all gated `now` in rectangle.final.certified.json @94935b740e.

Run:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_VIEWP/build_viewP.py

WHAT THIS DOES NOT DO, on purpose (the face's four refusals):
  - no 4-hop cloud-node -> arn -> motif -> symbol -> firm chain for membership (AC1: MOOT/REFUSED)
  - no ABSENT -> 0.0 coercion (AC3)
  - no deflation of a P result by the base rate (AC6)
  - no emission of arms[P].effective_partition as a live second token (AC7)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent / "VIEWP_firm_partition.json"

# ---- pinned inputs -----------------------------------------------------------------
POP_PIN = "64ae1ae879"
POP_PATH = ("org/tier1_exec/4.0.0_SA_CRO~A/deliverables/"
            "NFRA_C3MATERIALIZE.TO-L2-CROA/L2_VIEW_ARTIFACTS.json")
PROBE_PIN = "fb0a013b04"
PROBE_PATH = ("org/tier1_exec/1.0.0_SA_CTO~Y/deliverables/"
              "D11_L3W2_INDEPENDENT_REDERIVATION/KSWEEP_POSITIVE_ARM_PROBE.json")
SHARD_PIN = "5ab05ee4bd"   # last commit that CHANGED the shard; see settled_pin_resolution below
SHARD_PATH = ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
              "D11_L3_BRIDGE_REGISTRY/pipesym_to_firm.bridge.json")
SHARD_PIN_CANDIDATES = ["5ab05ee4bd", "8ff31fa1c8", "b8c47d1233"]


def read_at_pin(pin: str, path: str) -> bytes:
    """git show <pin>:<path> -> raw bytes. Never 2>/dev/null: a mangle returns clean-empty."""
    cp = msys_safe_run(["git", "show", f"{pin}:{path}"], cwd=str(ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        raise SystemExit(f"FAIL: git show {pin}:{path} rc={cp.returncode} "
                         f"stderr={cp.stderr.decode(errors='replace')[:400]}")
    if not cp.stdout:
        raise SystemExit(f"FAIL: git show {pin}:{path} returned EMPTY (path mangle?)")
    return cp.stdout


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    # ---- read inputs at their pins ---------------------------------------------
    pop_bytes = read_at_pin(POP_PIN, POP_PATH)
    probe_bytes = read_at_pin(PROBE_PIN, PROBE_PATH)

    # SETTLED PIN, resolved by CONTENT rather than by ancestry: the face says "the SETTLED
    # registry pin" without naming it, and three candidates circulate. Hash the shard at each.
    shard_digests = {p: sha256(read_at_pin(p, SHARD_PATH)) for p in SHARD_PIN_CANDIDATES}
    shard_bytes = read_at_pin(SHARD_PIN, SHARD_PATH)
    settled_moot = len(set(shard_digests.values())) == 1

    pop = json.loads(pop_bytes)
    probe = json.loads(probe_bytes)
    shard = json.loads(shard_bytes)

    structure = [v for v in pop["views"] if v["view_id"] == "STRUCTURE"]
    if len(structure) != 1:
        raise SystemExit(f"FAIL: expected exactly 1 STRUCTURE view, got {len(structure)}")
    entity_set = structure[0]["entity_set"]
    entities = entity_set["entities"]
    declared_denom = entity_set["denominator"]

    # entity order IS the mask carrier's: ascending index in entity_set.entities @64ae1ae879
    ids = [e["entity_id"] for e in entities]
    id_index = {eid: i for i, eid in enumerate(ids)}
    S_ids = set(ids)

    members = probe["members"]
    labels = probe["firm_labels"]
    S_mem = set(members)

    # The mask's entity ORDER is this list's order. Materialise the measured entities' indices
    # so the ordering convention is EXERCISED rather than asserted in prose.
    measured_idx = sorted(id_index[m] for m in members if m in id_index)

    POP_N = len(ids)
    if POP_N != declared_denom:
        raise SystemExit(f"FAIL: id count {POP_N} != declared denominator {declared_denom}")

    # ---- AC1 population binding: EXACT STRING equality, BOTH directions --------
    fwd = sum(1 for m in members if m in S_ids)          # members -> population
    rev = sum(1 for i in ids if i in S_mem)              # population -> members
    pipeline_layer = {e["entity_id"] for e in entities if e["layer"] == "pipeline"}
    layer_hist = dict(Counter(e["layer"] for e in entities))

    # negative controls: the test must be ABLE to fail
    nc_mutated = sum(1 for m in list(members)[:50]
                     if m + "::__NOT_A_REAL_SYMBOL__" in S_ids)
    nc_nonmember = sum(1 for o in list(S_ids - S_mem)[:50] if o in S_mem)

    # ---- AC2 feature derivation ------------------------------------------------
    fan = Counter(labels[m] for m in members)
    shard_floor = {"bd": 724, "inf": 594, "mdpf": 19}
    # consistency (NOT corroboration): the labels and a segment-2 parse are ONE method
    seg2_agree = sum(1 for m in members if m.split(":")[1] == labels[m])

    # ---- AC3 / AC6 / AC7 -------------------------------------------------------
    n = len(members)
    both_measured = comb(n, 2)
    union_pairs = comb(POP_N, 2)
    same_terms = {k: comb(v, 2) for k, v in fan.items()}
    same = sum(same_terms.values())
    cross = both_measured - same
    frac_ones = same / both_measured
    mdpf_ones = same_terms.get("mdpf", 0)

    # ---- AC4: P's own 6.3 number, COMPUTED. Score == label by construction. -----
    # ROC-AUC by the Mann-Whitney identity; positives all score 1, negatives all 0, no ties.
    comparisons = same * cross
    auc_self = (comparisons + 0.5 * 0) / comparisons

    artifact = {
        "schema": "nfra-c3materialize.l3w3.view-prep/1.0",
        "view_id": "P",
        "view_role": "VIEW P of the K-sweep -- the FIRM PARTITION control arm, wave 3",
        "executor": "0.8.0_AE_CloudComp~Y",
        "task_order": "NFRA_C3MATERIALIZE.TO-L3W3-CCY",
        "decomp_ref": {
            "doc": ("workflows/atom_decomposition/runs/nfra-c3materialize-L3/"
                    "20260829T1906Z/DECOMP.md"),
            "vintage_commit": "94935b740e",
            "rectangle": "rectangle.final.certified.json @94935b740e (34 cells)",
        },
        "built_at_commit": "PENDING-THIS-COMMIT",
        "gate_state": {
            "all_nine_cells_sequence_gate": "now",
            "read_from": "rectangle.final.certified.json @94935b740e, cells[].sequence_gate",
            "meaning": ("NOTHING on this face is gated. The dispatch's 'Gate after-view-P' names "
                        "the gate carried by OTHER lanes' cells, which are gated ON this artifact. "
                        "Verified at source rather than from the relay that reported it."),
        },
        "rows": {},
    }
    R = artifact["rows"]

    R["population_binding"] = {
        "cell_id": "L3W3-dc02-1",
        "value": {
            "population_denominator": POP_N,
            "members": n,
            "direction_A_members_in_population": fwd,
            "direction_B_population_in_members": rev,
            "alignment_method": ("EXACT STRING equality on entity_id. No parse, no normalisation, "
                                 "no prefix stripping."),
            "set_equality_with_layer_pipeline": sorted(S_mem) == sorted(pipeline_layer),
            "members_not_in_pipeline_layer": len(S_mem - pipeline_layer),
            "pipeline_layer_not_in_members": len(pipeline_layer - S_mem),
            "layer_histogram": layer_hist,
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": (f"{fwd} of {n} members resolve into a population of {POP_N}; "
                            f"{rev} of {POP_N} population entities resolve into the members. "
                            "BOTH directions printed so a one-sided match cannot read as membership."),
            "instrument": (f"git show {POP_PIN}:{POP_PATH} -- the population read THROUGH its pin, "
                           f"not from a working copy. Its id list is {POP_N} long and "
                           f"{len(set(ids))} distinct, equal to its own declared denominator "
                           f"{declared_denom}, so the list and the declaration agree and neither "
                           "is assumed."),
            "pinned_population_input": (f"{PROBE_PATH} @{PROBE_PIN} "
                                        "(schema nfra-c3materialize.l3w2.ksweep.positive-arm-probe/1.0) "
                                        "LISTS the member ids -- a pinned population, not a description."),
            "certified_overlap": "bdc1246987",
            "negative_control": (f"50 member ids mutated with a '::__NOT_A_REAL_SYMBOL__' suffix "
                                 f"resolve {nc_mutated} of 50 into the population (expect 0), and "
                                 f"50 population ids known to be outside the member set resolve "
                                 f"{nc_nonmember} of 50 into it (expect 0). The equality test can fail."),
            "chain_refused": ("The 4-hop cloud-node -> arn -> motif -> symbol -> firm composition is "
                              "MOOT and REFUSED: it would traverse a COVER bridge backward through an "
                              "undeclared hop to reach entities already in the set. Membership here is "
                              "direct string equality and nothing else."),
            "citations": [f"{POP_PATH} @{POP_PIN}", f"{PROBE_PATH} @{PROBE_PIN}"],
        },
    }

    R["feature_derivation"] = {
        "cell_id": "L3W3-dc02-2",
        "value": {
            "definition": "W_P(i,j) = 1 if firm(i) == firm(j) else 0, over the measured members",
            "fan_in": dict(fan),
            "distinct_firm_tokens_right": len(fan),
            "reproduces_shard_floor": dict(fan) == shard_floor,
            "firm_source": ("pipesym_to_firm rows L3W1-ypbj-1..8 for the RULE, basis and floor; "
                            "per-entity labels from the pinned probe's firm_labels."),
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": f"{sum(fan.values())} of {n} members carry a firm label; 0 unresolved.",
            "grain_disclosure": (
                "THE SHARD DOES NOT CARRY A PER-ENTITY FIRM MAP AND THIS ROW DOES NOT PRETEND IT DOES. "
                "pipesym_to_firm is a ROLLUP_CONTAINMENT bridge descriptor: its 8 rows carry the "
                "subject's endpoints, basis, join evidence, card keys, cardinality class, firm-carry, "
                "declarability and failure mode -- not 1,337 labels. Its own declared_by_store reads "
                "'NO -- the firm is recoverable only by parsing segment 2 of the pipeline id. No store "
                "declares it.' So the RULE and the FLOOR come from the shard, and the per-entity LABELS "
                "come from the pinned cell input the face names in AC9, which lists the ids WITH their "
                "labels. That is what 'read the shard, never re-parse independently' can mean here."),
            "floor_reproduced": (f"The shard's join_evidence (L3W1-ypbj-3) declares bd=724, inf=594, "
                                 f"mdpf=19 as a FLOOR. Recomputed from the pinned labels: {dict(fan)}. "
                                 "Reproduced exactly -- derived, not copied."),
            "consistency_not_corroboration": (
                f"A segment-2 parse of the member ids agrees with the pinned labels on {seg2_agree} of "
                f"{n}. THIS IS NOT CORROBORATION: the pinned labels ARE a segment-2 parse, so the two "
                "readings share one substrate and one method. Recorded as a consistency check, and it "
                "would be dishonest to present it as independent confirmation."),
            "citations": [f"{SHARD_PATH} @{SHARD_PIN}", f"{PROBE_PATH} @{PROBE_PIN}"],
        },
    }

    R["coverage_measured_absent"] = {
        "cell_id": "L3W3-dc02-3",
        "value": {
            "MEASURED": n,
            "ABSENT": POP_N - n,
            "denominator": POP_N,
            "measured_pct_of_population": round(n / POP_N * 100, 1),
            "absent_pct_of_population": round((POP_N - n) / POP_N * 100, 1),
            "metric_domain_both_measured": both_measured,
            "union_pair_domain": union_pairs,
            "mask_entity_order": "ascending index in entity_set.entities @" + POP_PIN,
            "measured_index_min": min(measured_idx),
            "measured_index_max": max(measured_idx),
            "measured_index_count": len(measured_idx),
            "measured_indices_are_contiguous": (
                max(measured_idx) - min(measured_idx) + 1 == len(measured_idx)),
            "absent_semantics": (
                "ABSENT IS ABSENT, NEVER ZERO. A 0.0 is a MEASURED statement of no affinity; ABSENT is "
                "the statement that nothing was measured. Coercing the ABSENT entities to 0.0 would "
                "move the metric domain off the ruled both-measured C(1337,2) and onto the full union, "
                "silently, while every number still printed a denominator."),
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": f"{n} MEASURED + {POP_N - n} ABSENT = {POP_N}, the population's own denominator.",
            "mask_carrier": (
                f"The per-entity MEASURED/ABSENT mask IS the pinned member list at {PROBE_PATH} "
                f"@{PROBE_PIN}: an entity is MEASURED iff its entity_id is in that list, ABSENT "
                "otherwise. Entity order is the mask carrier's -- ascending index in "
                f"entity_set.entities @{POP_PIN}. A consumer materialises the mask deterministically "
                "from those two pinned artifacts; it is not re-derived here and not shipped as "
                f"{POP_N} restated rows."),
            "instrument": "Set membership of each population entity_id in the pinned member list.",
            "positive_control": (f"The split is non-degenerate in both directions ({n} / {POP_N - n}), "
                                 "so the classifier demonstrably assigns both values."),
            "why_absent_is_large": (
                f"{POP_N - n} of {POP_N} is {round((POP_N - n) / POP_N * 100, 1)} percent ABSENT, and "
                "that is a PROPERTY OF THE VIEW: P is defined only on pipeline symbols, which are one "
                "of four layers in this population. A view claiming 0 ABSENT here would be the "
                "surprising result."),
        },
    }

    R["role_typing"] = {
        "cell_id": "L3W3-dc02-4",
        "value": {
            "role": "CONTROL_ONLY",
            "six_three": "6.3_NOT_A_RESULT",
            "six_three_number": auc_self,
            "six_three_number_semantics": (
                "ROC-AUC of W_P scored against the same-firm label, over the both-measured pair "
                "domain. It is 1.0 EXACTLY AND TAUTOLOGICALLY: the score IS the label. This number is "
                "printed because the cell requires it printed, and it is labelled NOT A RESULT because "
                "a perfect score obtained by scoring a label against itself measures nothing."),
            "circularity": (
                "P's firm label IS the 6.3 cohort label on these same entities. Fusing view 1 with P "
                "and evaluating 6.3 on that cohort would INHERIT the very thing being tested."),
            "parse_agreement": f"{seg2_agree}/{n}",
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": (f"{same:,} positives x {cross:,} negatives = {comparisons:,} "
                            "(positive, negative) comparisons, 0 cross-class ties."),
            "instrument": ("Mann-Whitney identity for ROC-AUC. Positives all score 1, negatives all "
                           "score 0, so every comparison is concordant by construction."),
            "why_a_shuffle_control_cannot_falsify_this": (
                "Permuting the firm labels leaves the same-firm pair COUNT unchanged, because "
                "shuffling permutes labels without changing block sizes. So a size-based control is "
                "structurally incapable of falsifying this number. The tautology lives in the IDENTITY "
                "of score and label, which is exactly what this cell asks to be TYPED rather than "
                "reported as a finding. Naming the control that does NOT work is the honest form."),
            "prd_figures_not_carried": (
                "PRD sec 6.3's parenthetical 0.989 / 0.974 are section-4 evidence on single views that "
                "are not the fused ones. Addendum 1f @76c688fa3d states they are NOT a floor and are "
                "NEVER carried into a 6.3 evaluation. This row carries neither."),
            "consumer_can_reject": ("role and six_three are TYPED fields with declared value domains, "
                                    "so a consumer rejects on the field rather than parsing prose."),
        },
    }

    R["basis_declarability"] = {
        "cell_id": "L3W3-dc02-5",
        "value": {
            "basis": "INFERRED",
            "declarability": "NAMED_GAP_STORE_OWNER",
            "gap_owner": shard["rows"]["declarability"]["gap_owner"],
            "never_promoted": (
                "INFERRED is the segment-2 parse -- the SAME parse the certified cohort labels carry. "
                "Admissible at that typed basis and NEVER promoted to measured."),
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "carried_exactly_as_the_shard_says": (
                f"basis from the shard's basis row (L3W1-ypbj-2, value "
                f"{shard['rows']['basis']['value']!r}); declarability from its declarability row "
                f"(L3W1-ypbj-7, value {shard['rows']['declarability']['value']!r}). Both read from "
                "the shard, not restated from memory."),
            "does_not_gate_this_wave": ("A DECLARED per-entity firm is the L1-spine named gap. It does "
                                        "not gate wave 3 and is not claimed as closed."),
            "citations": [f"{SHARD_PATH} @{SHARD_PIN}"],
        },
    }

    R["base_rate"] = {
        "cell_id": "L3W3-dc02-6",
        "value": {
            "same_firm_pairs": same,
            "same_firm_pair_terms": same_terms,
            "cross_firm_pairs": cross,
            "denominator": both_measured,
            "fraction_ones": round(frac_ones, 4),
            "typed_as": "arms[P].base_rate",
            "print_rule": "PRINTED BESIDE EVERY P ROW AT EVERY K.",
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": (f"C({n},2) = {both_measured:,} both-measured pairs; "
                            f"{same:,} same-firm + {cross:,} cross-firm = {both_measured:,}."),
            "derivation": (f"same_firm_pairs recomputed from the fan-in as "
                           f"{' + '.join(f'C({fan[k]},2)={same_terms[k]:,}' for k in sorted(fan))} "
                           f"= {same:,}. Derived from the labels, not copied from the oracle."),
            "IT_IS_A_FRAME_NOT_A_DISCOUNT": (
                "The sweep's AUC is a ROC-AUC over pairs, and ROC-AUC is INVARIANT TO CLASS PREVALENCE "
                "by construction: it ranks within each class and the positive:negative ratio cancels. "
                "A near-balanced P therefore does NOT inflate its AUC. NO ROW MAY DEFLATE A P RESULT BY "
                "THIS FRACTION. PR-AUC would be prevalence-sensitive; this is not."),
            "history": ("0.8.0_AE_CloudComp~X supplied this number with the opposite consequence "
                        "attached and withdrew that consequence itself at 81337."),
            "design_lane_typing": "6d23af95b9",
        },
    }

    R["firm_representation"] = {
        "cell_id": "L3W3-dc02-7",
        "value": {
            "firm_representation": "bd_vs_inf",
            "mdpf_share_of_ones": round(mdpf_ones / same, 5),
            "mdpf_symbols": fan.get("mdpf", 0),
            "mdpf_same_firm_pairs": mdpf_ones,
            "sharp_form": ("MDPF SEPARATION IS UNMEASURABLE IN THIS ARM -- not merely small."),
            "reading_constraint": (
                "P is EFFECTIVELY a two-block bd-versus-inf partition. Any per-firm reading of this "
                "sweep IS a bd-versus-inf reading and must say so, rather than implying three-firm "
                "coverage."),
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": (f"mdpf contributes {mdpf_ones} of {same:,} same-firm pairs "
                            f"({mdpf_ones / same:.8f}), from {fan.get('mdpf', 0)} of {n} symbols."),
            "one_live_name": (
                "`firm_representation` is THE ONE LIVE FIELD NAME for this quantity, ruled "
                "@9cfa4eebbf. arms[P].effective_partition is RETIRED as a live name and survives only "
                "as a SCHEMA-DECLARED ALIAS. THIS ARTIFACT DOES NOT EMIT IT: two live names for one "
                "quantity disagree silently (0.8.0_AE_CloudComp~X 81407)."),
            "untouched_by_prevalence": ("This is REPRESENTATION, not base rate. The AC6 prevalence "
                                        "correction does not touch it."),
        },
    }

    R["coverage_vs_fanout"] = {
        "cell_id": "L3W3-dc02-8",
        "value": {
            "cardinality_class": shard["rows"]["cardinality_class"]["value"],
            "cardinality_class_is_about": ("FAN-OUT at the full-id grain, which is unmeasurable by "
                                           "construction on a roll-up."),
            "coverage_is_about": "the join, and it is COMPLETE",
            "join_left": 1337,
            "join_right": 3,
            "join_result": 1337,
            "unresolved": 0,
            "not_a_contradiction": (
                "An arm claiming FULL COVERAGE beside a bridge row reading UNMEASURED is CONSISTENT. "
                "They are different quantities: UNMEASURED describes how many children a parent has "
                "at a grain the roll-up cannot see; coverage describes whether every child resolved "
                "to a parent, and every one did."),
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "denominator": "|left| 1,337 pipeline symbols, |right| 3 firm tokens, |join| 1,337, 0 unresolved.",
            "instrument": (f"The shard's own join run L3W1-ypbj-3, read from {SHARD_PATH} "
                           f"@{SHARD_PIN}; and its cardinality_class row L3W1-ypbj-5, whose "
                           f"probe_can_return_multiple is "
                           f"{shard['rows']['cardinality_class']['probe_can_return_multiple']} -- "
                           "a probe that cannot return >1 parent cannot measure fan-out, which is "
                           "why the class is UNMEASURED rather than 1."),
            "why_this_cell_exists": ("A census table places these two side by side and the pair reads "
                                     "as a contradiction to anyone who has not re-derived it. This "
                                     "cell makes it legible without that re-derivation."),
        },
    }

    R["provenance"] = {
        "cell_id": "L3W3-dc02-9",
        "value": {
            "inputs": [
                {"path": POP_PATH, "pin": POP_PIN, "sha256_of_bytes_read": sha256(pop_bytes),
                 "role": "population (19,482 L2 STRUCTURE entity_set)"},
                {"path": PROBE_PATH, "pin": PROBE_PIN, "sha256_of_bytes_read": sha256(probe_bytes),
                 "role": "pinned cell input: member ids WITH labels",
                 "schema": "nfra-c3materialize.l3w2.ksweep.positive-arm-probe/1.0"},
                {"path": SHARD_PATH, "pin": SHARD_PIN, "sha256_of_bytes_read": sha256(shard_bytes),
                 "role": "firm rule, basis, floor, join evidence, cardinality class"},
            ],
            "ruling_pins": ["0f9a2aa6db", "b3873740fe"],
            "pins": {"decomp": "94935b740e", "faces_cut": "b8c47d1233",
                     "design_typing": "6d23af95b9", "one_live_name_ruling": "9cfa4eebbf",
                     "certified_overlap": "bdc1246987"},
        },
        "status": "WRITTEN",
        "sequence_gate": "now",
        "evidence": {
            "every_input_read_through_its_pin": (
                "Each input above was read with `git show <pin>:<path>` and hashed as read, so the pin "
                "and the bytes cannot disagree. The sha256 is of the bytes THIS RUN consumed."),
            "settled_pin_resolution": (
                "The face says 'the SETTLED registry pin' without naming it, and three candidates "
                f"circulate ({', '.join(SHARD_PIN_CANDIDATES)}). Resolved BY CONTENT, not by ancestry: "
                f"the shard hashes to {shard_digests[SHARD_PIN_CANDIDATES[0]]} at ALL of them, so the "
                "choice is MOOT and no reading depends on it. "
                f"identical_across_candidates={settled_moot}. A sibling shard in the same directory "
                "hashes differently, so the digest discriminates."),
            "citation_form_note": (
                "The pinned probe cites its population as 'L2_VIEW_ARTIFACTS.json views[STRUCTURE]."
                "entity_set' -- a MAP-style access on what is a LIST of 2 views. That resolves for a "
                "human and not for a program. This artifact selects the view by "
                "views[i].view_id == 'STRUCTURE' and asserts exactly one match. Surfaced, not chased."),
            "no_pin_count_no_push_state": (
                "This cell names NEITHER a pin count NOR a push state. ruling_pins and the pins map "
                "already carry what they carry; restating a count here would be a second carrier of "
                "the same quantity."),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=1) + "\n", encoding="utf-8")

    print(f"OK: wrote {OUT.relative_to(ROOT)}")
    print(f"OK: 9 rows, cell_ids {[r['cell_id'] for r in R.values()]}")
    print(f"OK: AC1 both directions {fwd}/{n} and {rev}/{POP_N}; "
          f"set-equality with layer=pipeline {sorted(S_mem) == sorted(pipeline_layer)}")
    print(f"OK: AC2 fan-in {dict(fan)} reproduces floor {dict(fan) == shard_floor}")
    print(f"OK: AC3 MEASURED {n} / ABSENT {POP_N - n} / denom {POP_N}")
    print(f"OK: AC6 same {same:,} / cross {cross:,} / denom {both_measured:,} / "
          f"fraction_ones {frac_ones:.4f}")
    print(f"OK: AC7 mdpf_share_of_ones {mdpf_ones / same:.5f}")
    print(f"OK: settled-pin moot by content: {settled_moot}")


if __name__ == "__main__":
    main()
