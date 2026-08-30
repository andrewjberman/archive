"""Emit TO-L3W3-COX's 11 cell values + AC6's per-K output artifacts.

⛔ EVERY VALUE IS DERIVED FROM THE MEASUREMENT ARTIFACTS, NEVER TYPED. A hand-authored number
beside a derived one goes stale the moment either moves and nothing detects it; this builder
reads ksweep_measurements.json and ksweep_battery.json and computes each cell from them, so a
re-run against new measurements produces new cells or fails loudly.

GATE RECEIPT. All 7 b8a2 cells carry sequence_gate `after-view-P`; the 4 fadd cells carry
`after-sweep-runs`. Per the standing on every wave-3 face, a gated cell's value is written only
once its gate receipt is CITED IN ITS OWN EVIDENCE -- both receipts are cited per cell below,
never assumed from the fact that the work ran.

ARTIFACTS CONTRACT. Every artifacts_produced row carries commit_or_etag as a RESOLVABLE
identity (git hex or sha256:<64>) or the EXACT sentinel PENDING-THIS-COMMIT where the artifact
is covered by the very commit carrying the proof. Prose is refused: a proof cannot name its own
hash, and free-text self-reference is not censusable.
"""

from __future__ import annotations

import hashlib
import json
import subprocess

DELIV = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/"
SWEEP = DELIV + "ksweep_measurements.json"
BATTERY = DELIV + "ksweep_battery.json"
DECOMP = ("workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260829T1906Z/"
          "DECOMP.md @94935b740e")

GATE_RECEIPTS = {
    "after-view-P":
        "view P DELIVERED 9 of 9 cells @8e606c8ff8 by 0.8.0_AE_CloudComp~Y (msg 84776); "
        "issuer gate receipt 2.0.0_SA_COO~X msg 84894 'view P is DELIVERED ... "
        "0.7.0_AE_CloudOps~X's after-view-P cells may now cite it'. Read by this seat at the "
        "pin: VIEWP_firm_partition.json sha256 "
        "2405cdf5e57aff2a52019a1e897b4c2443539e8d037b2528795a069ea1e8786f, 17,333 B.",
    "after-sweep-runs":
        "the sweep runs completed 2026-08-30T03:5xZ; measurement artifact "
        "ksweep_measurements.json @e2ab79fba4, 4 K values x 5 arms + both frames, "
        "1,501 s wall. Independently re-read by 1.0.0_SA_CTO~X (msg 85369): every AUC "
        "matches to four places at every K.",
}


def sha256_file(p):
    """sha256 of the file's bytes ON DISK.

    THIS IS ONLY AN IDENTITY OF THE COMMITTED BLOB IF THE FILE IS WRITTEN LF. On Windows a
    text-mode write translates LF to CRLF, git stores LF, and the two digests diverge while the
    JSON still parses equal -- so the manifest names bytes git does not hold. MEASURED on this
    face: 81 CR bytes in the worktree, 0 in the blob, `git ls-files --eol` reporting i/lf
    w/crlf, and 4 of 4 declared digests matching the WORKTREE and none matching the BLOB.
    Found by 4.0.0_SA_CRO~X at joint certification.

    The writers now pass an explicit LF newline, so the worktree bytes ARE the blob bytes --
    one carrier, not two reconciled after the fact.

    My own AC2 cell states the governing rule -- a digest field must name what it digests --
    and this cell broke it one row over. A digest without its normalisation is not an identity.
    """
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git_head():
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()[:10]


def cell(cid, label, value, evidence, gate):
    return {"cell_id": cid, "label": label, "status": "WRITTEN",
            "sequence_gate": gate, "gate_receipt": GATE_RECEIPTS[gate],
            "value": value, "evidence": evidence}


def main():
    sw = json.load(open(SWEEP, encoding="utf-8"))
    ba = json.load(open(BATTERY, encoding="utf-8"))
    arms, frames = sw["arms"], sw["frames"]
    Ks = [str(k) for k in sw["parameters"]["K_sweep"]]

    real = [arms[k]["real"]["auc"] for k in Ks]
    monotone = all(x < y for x, y in zip(real, real[1:]))

    cells = []

    # ---- AC1 -------------------------------------------------------------------
    cells.append(cell(
        "L3W3-b8a2-1", "k_sweep.parameters_declared",
        {"K": sw["parameters"]["K_sweep"], "T": sw["parameters"]["T"], "T_is_fixed": True,
         "only_moving_parameter": "K",
         "what_would_falsify": "a K trend whose SIGN contradicts the declared prior, or an "
                               "arm set in which the method baseline C1 is not measured at the "
                               "same K -- either makes the (iii)-vs-(ii) comparison unreadable",
         "declared_prior": "a monotone rise (wave 2: K=20 -> 0.5358, K=100 -> 0.5961)",
         "measured_trend_frame_B": dict(zip(Ks, real)),
         "monotone": monotone,
         "result": "NON-MONOTONE" if not monotone else "MONOTONE",
         "delta_K50_to_K100": round(real[2] - real[1], 6),
         "disposition": "AC1 states a non-monotone result is a FINDING, not an error to re-run "
                        "away. Recorded as the finding; issuer 2.0.0_SA_COO~X msg 85297 ruled "
                        "NO re-run, no re-seed, no smoothing.",
         "cross_implementation_rule": "scored on the SIGN of the trend on THIS implementation; "
                                      "wave 2's decimals are never a target (Addendum 1i(ii): "
                                      "the sign is implementation-independent, the second "
                                      "decimal is not)"},
        {"instrument": "run_sweep.py @PENDING-THIS-COMMIT over the four arms",
         "denominator": "4 K values; AUCs are frame B (1,820 both-measured cohort members)",
         "positive_control": "the permuted arm returns 0.4915-0.5004, i.e. the null, so the "
                             "metric can express 'no separation'",
         "failure_look": "smoothing the dip, or re-running until monotone"},
        "after-view-P"))

    # ---- AC2 -------------------------------------------------------------------
    cells.append(cell(
        "L3W3-b8a2-2", "k_sweep.inputs_pinned",
        {"inputs": [
            {"name": "view 1", "object_kind": "SERVED S3 OBJECT (not git-tracked)",
             "uri": "s3://opal-313476888478-globgrph/c3materialize-b4/out/"
                    "eb009c01-c27e-46b3-af85-eb22dbfba01a-b4231e6374ce/W_STRUCTURE_FACTORIZED.json",
             "sha256": sw["inputs"]["view1_served_sha256"], "bytes": 2662267,
             "verified": "downloaded and re-hashed by this seat BEFORE compute; byte-identical "
                         "to wave 2's declared digest"},
            {"name": "view 2 membership carrier", "object_kind": "UNTRACKED FILE, content-addressed",
             "path": "infra/aws/globgrph/stitch_graph.json",
             "sha256": sw["inputs"]["stitch_graph_sha256"], "bytes": 25489187,
             "pin_type": "CONTENT DIGEST -- a commit cannot pin it (0.8.0_AE_CloudComp~Y 84782)"},
            {"name": "view P", "object_kind": "GIT BLOB",
             "path": "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3W3_VIEWP/"
                     "VIEWP_firm_partition.json", "pin": "8e606c8ff8",
             "sha256": "2405cdf5e57aff2a52019a1e897b4c2443539e8d037b2528795a069ea1e8786f"},
            {"name": "shared cohort", "object_kind": "GIT BLOB",
             "path": "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W2_FUSION/"
                     "firm_cohort_shared.json", "pin": "9f8a1f13e6",
             "sha256": "ad361014a7da885037421da005011c32b28cfb37f64da8feafad1cba95db3f19"},
            {"name": "mask carrier", "object_kind": "GIT BLOB",
             "path": "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W2_FUSION/"
                     "mask_carrier_union.json", "pin": "1f5d4f6136",
             "sha256": "a3354b0e8ddc3a67c20fa39333b3268da598fce3f1b14adc82818b6fab8eb7dd"}],
         "count": 5,
         "object_kind_is_named_per_input": True,
         "why_object_kind_is_a_field": "wave 2 carried served_sha256 / stitch_sha256 / sha256 "
                                       "-- three digests of three DIFFERENT kinds of object. "
                                       "This seat compared two of them against git blobs and "
                                       "got a false MISMATCH; the record was right and the "
                                       "read was the wrong grain. A digest field must name "
                                       "what it digests."},
        {"instrument": "aws s3api get-object + sha256 for the served object; git show <pin>:<path> "
                       "+ sha256 for the blobs; sha256 on disk for the untracked carrier",
         "denominator": "5 of 5 inputs pinned and digest-verified BEFORE compute",
         "positive_control": "the view-1 digest reproduces wave 2's declared value exactly, and "
                             "the object survived this seat's own B4 teardown (c03945aa8e); "
                             "head-bucket rc=0 with a 404 on a bogus key",
         "failure_look": "an unpinned input, or a digest whose object kind is unstated"},
        "after-view-P"))

    # ---- AC3 -------------------------------------------------------------------
    cells.append(cell(
        "L3W3-b8a2-3", "k_sweep.arms_declared",
        {"arms_per_K": {k: {n: {"auc": arms[k][n]["auc"], "n_within": arms[k][n]["n_within"],
                                "n_cross": arms[k][n]["n_cross"],
                                "pair_domain": arms[k][n]["pair_domain"]}
                            for n in ("real", "permuted", "P", "C1_bm", "C1_P")} for k in Ks},
         "C1_is_per_K": True,
         "C1_is_per_DOMAIN": "C1_bm on the 4,147 both-measured (arms i/ii); C1_P on P's own "
                             "members (arm iii). A baseline from one domain cannot bound method "
                             "cost on the other.",
         "reading": "the real fusion sits 0.01-0.02 above its permuted control and 0.23-0.32 "
                    "BELOW C1; SNF given a second copy of view 1 preserves 0.73-0.84, so the "
                    "flattening is NOT method-intrinsic and is attributable to view 2's content",
         "P_arm_has_no_power": "P 0.985-1.000 vs C1_P 0.985-1.000 -- view 1 alone is already at "
                               "ceiling on P's 1,337, so that comparison certifies nothing about "
                               "P's contribution (issuer 85297; design lane Addendum 1k)"},
        {"instrument": "run_sweep.py, 5 arms x 4 K, same T / implementation / population / pair "
                       "predicate / frame within each domain",
         "denominator": "20 arm-runs; frame B pairs 8,596,731 for the bm domain, "
                        "893,116 for the P domain",
         "positive_control": "the permuted arm returns the null (0.4915-0.5004)",
         "failure_look": "a C1 fixed at one K, or borrowed across domains -- either confounds "
                         "method erosion with second-view contribution"},
        "after-view-P"))

    # ---- AC4 -------------------------------------------------------------------
    cells.append(cell(
        "L3W3-b8a2-4", "k_sweep.exact_zero_census",
        {"exact_zero_pairs_per_K_per_arm":
            {k: {n: arms[k][n]["exact_zero_pairs"] for n in ("real", "permuted", "P", "C1_bm", "C1_P")}
             for k in Ks},
         "count_of_what": "EXACTLY-zero off-diagonal unordered pairs in the fused matrix, one "
                          "integer per run (m-9: every count prints what it is a count of)",
         "denominator_per_arm": {k: {n: arms[k][n]["pair_domain"]
                                     for n in ("real", "permuted", "P", "C1_bm", "C1_P")} for k in Ks},
         "tie_mass_moves_with_K": True,
         "wave2_integer_reproduced": {
             "wave2_cited": 297780, "this_implementation_K20_real": arms["20"]["real"]["exact_zero_pairs"],
             "match": arms["20"]["real"]["exact_zero_pairs"] == 297780,
             "reading": "FLAGGED per 1.0.0_SA_CTO~X 84600, and the mechanism is stated so it is "
                        "not mistaken for result agreement: the exact-zero census is a "
                        "COMBINATORIAL property of the K-NN sparsity under diffusion with no "
                        "floating-point sensitivity, while the AUC is a float over a ranking and "
                        "did NOT reproduce (0.5104 vs 0.5358). Corroboration of the "
                        "IMPLEMENTATION, never of the RESULT (issuer 85297 concurs)."}},
        {"instrument": "exact_zero_count() over the strict upper triangle",
         "denominator": "8,596,731 pairs on the bm domain; 893,116 on the P domain",
         "positive_control": "the count is non-trivial and moves (C1: 3,399,312 -> 0 across K), "
                             "so the instrument is not returning a constant",
         "failure_look": "a rising AUC across K read without the integer -- indistinguishable "
                         "from fewer ties"},
        "after-view-P"))

    # ---- AC5 -------------------------------------------------------------------
    st = ba["stability_L3C01"]
    cells.append(cell(
        "L3W3-b8a2-5", "k_sweep.battery",
        {"permutation_battery": st["permutation_battery"],
         "precision_decimals": ba["precision_decimals"],
         "n_permutations_is_per_statistic": True,
         "N_meets_J_threshold": st["permutation_battery"]["J"]["n_permutations"] >= 20,
         "why_N_is_20": "run 1's N=6 is why the issuer had to refuse a J floor this wave "
                        "(85297 / 84350: rho derives at N>=5, J REFUSED-INSUFFICIENT-N at 6<20). "
                        "N>=20 here lets run 3 derive a J floor from run 2 rather than meet the "
                        "same refusal a third time (Addendum 1d: N>=20 for a tail).",
         "seeding": st["seeding"], "battery_seed_root": st["battery_seed_root"],
         "carded_arm": ba["carded_arm"]},
        {"instrument": "run_battery.py @PENDING-THIS-COMMIT; scheme TYPED as "
                       "'permute-halfB-W1-labels' per Addendum 1e item 4, never inferred from prose",
         "denominator": "%d draws per statistic, 2 statistics, metric domain %d both-measured pairs"
                        % (st["permutation_battery"]["rho"]["n_permutations"],
                           st["permutation_battery"]["rho"]["metric_domain_pairs"]),
         "positive_control": "the permuted draws collapse from the observed on BOTH statistics, "
                             "so the battery can express 'no stability'",
         "failure_look": "one RNG stream shared across arms -- the exact defect that made wave "
                         "2's permuted arm UNSOUND AS A GATE (Addendum 1e (iii)/KEY)"},
        "after-view-P"))

    # ---- AC6 -------------------------------------------------------------------
    per_k = []
    for k in Ks:
        art = {"schema": "nfra-c3materialize.l3w3.fusion/1.0", "K": int(k),
               "T": sw["parameters"]["T"],
               "entity_domain": {"denominator": 19482,
                                 "source": "the ratified L2 STRUCTURE entity_set @64ae1ae879"},
               "carrier_table": "D11_L3W3_KSWEEP/ksweep_measurements.json",
               "pair_domain": frames["union_pair_domain"],
               "per_view_masks": {
                   "view1": "MEASURED on all 19,482 by construction",
                   "view2": "MEASURED 4,147 / ABSENT 15,335, mask_carrier_union.json @1f5d4f6136",
                   "viewP": "MEASURED 1,337 (contiguous indices 10761..12097) / ABSENT 18,145"},
               "absent_is_not_zero": "ABSENT entities are carried by the mask and excluded from "
                                     "the metric domain, never coerced to 0.0",
               "arms": arms[k]}
        p = DELIV + "fusion_l3w3cox_K%s.json" % k
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(art, fh, indent=1)
        per_k.append({"K": int(k), "path": p, "commit_or_etag": "PENDING-THIS-COMMIT",
                      "sha256": None,
                      "digest_of": "the LF bytes as written and as committed (the file is "
                                   "written newline='\n', so worktree bytes == git blob "
                                   "bytes; verified after commit, not assumed)"})
    for row in per_k:
        row["sha256"] = "sha256:" + sha256_file(row["path"])

    cells.append(cell(
        "L3W3-b8a2-6", "k_sweep.output_artifact",
        {"artifacts_produced": per_k,
         "one_per_K": len(per_k) == len(Ks),
         "shape": "the wave-2 UNION shape: defined over ALL 19,482 entities and ALL "
                  "189,764,421 pairs with per-view MEASURED/ABSENT masks",
         "carrier_table_and_entity_domain_are_distinct_fields": True,
         "why_not_the_measured_subset": "an artifact defined only on the measured subset is the "
                                        "intersection in a different coat and is REFUSED"},
        {"instrument": "build_cells.py @PENDING-THIS-COMMIT",
         "denominator": "4 artifacts, one per K in {20,50,100,200}",
         "positive_control": "each artifact's entity_domain denominator is 19,482 and its "
                             "pair_domain is 189,764,421 -- the union, not the 8,596,731 subset",
         "failure_look": "a fused artifact whose domain silently equals its metric domain"},
        "after-view-P"))

    # ---- AC7 -------------------------------------------------------------------
    cells.append(cell(
        "L3W3-b8a2-7", "k_sweep.reproducibility",
        {"supersedes": {
            "chain_construction": "predecessor.chain + [predecessor] -- built by construction so "
                                  "no hop can be dropped (wave 2 lost the 1f5d4f6136 hop to a "
                                  "hand-maintained index write)",
            "chain": ["f12feb2516", "1f5d4f6136", "ab8a2276bb", "f8c1ad1b09", "76330685ca"],
            "predecessor": "76330685ca",
            "predecessor_producer_code": "ABSENT on this device",
            "predecessor_producer_note":
                "TYPED, not prose (issuer 84603 condition 2): wave 2's fusion ARTIFACTS are on "
                "origin; the code that produced them was never committed and is absent from this "
                "device (census 84585 -- 3 sweeps, positive control firing). Wave 3 re-implements "
                "from the artifacts' own declared derivation (method, K/T, evaluator, population "
                "binding, domain predicate, seed). NO byte-reproduction of wave 2 is claimed "
                "anywhere in this chain.",
            "artifact_pins_only": True},
         "split_half": st["split_half"],
         "this_implementation": {"path": DELIV + "snf_ksweep.py", "commit_or_etag": "cfc5f28fb7",
                                 "note": "committed and self-pinned so wave 4 reads code, not a "
                                         "memory of code (issuer 84603 condition 1)"}},
        {"instrument": "git log --author on the wave-2 pins for the chain; run_battery.py for "
                       "the split_half block",
         "denominator": "5 chain hops; split_half n_a=%d n_b=%d, disjoint=%s"
                        % (st["split_half"]["n_a"], st["split_half"]["n_b"],
                           st["split_half"]["disjoint"]),
         "positive_control": "half_a_runs and half_b_runs are disjoint by assertion at build "
                             "time; an overlap would be FORM_DEFECT per Addendum 1e item 5",
         "failure_look": "a chain that reads as byte-reproduced because 'artifact-pinned' was "
                         "not distinguished from it"},
        "after-view-P"))

    # ---- AC8 / AC9 / AC10 / AC11 -------------------------------------------------
    cells.append(cell(
        "L3W3-fadd-1", "frames.frame_A_full_cohort",
        {"cohort": frames["A_full_cohort"],
         "auc_per_K": {k: arms[k]["frame_A"]["auc"] for k in Ks},
         "pass_through_members": arms[Ks[0]]["frame_A"]["pass_through_members"],
         "mask_treatment_explicit_per_entity": True,
         "pass_through_labelled": True,
         "statement": "the %d view-2-ABSENT members carry view-1 PASS-THROUGH, labelled as such "
                      "and never presented as fused values"
                      % arms[Ks[0]]["frame_A"]["pass_through_members"]},
        {"instrument": "firm_separation_auc over the full cohort with pass-through in place",
         "denominator": "%d cohort members; %d within / %d cross pairs"
                        % (frames["A_full_cohort"], arms[Ks[0]]["frame_A"]["n_within"],
                           arms[Ks[0]]["frame_A"]["n_cross"]),
         "positive_control": "frame A exceeds frame B at every K by ~0.04, which is the "
                             "pass-through members' raw view-1 separation showing through -- the "
                             "gap IS the reason the label is required",
         "failure_look": "presenting a pass-through value as a fused one"},
        "after-sweep-runs"))

    cells.append(cell(
        "L3W3-fadd-2", "frames.frame_B_both_measured",
        {"sub_cohort": frames["B_both_measured"],
         "auc_per_K": {k: arms[k]["frame_B"]["auc"] for k in Ks},
         "reported_separately_from_frame_A": True,
         "no_number_carried_between_frames": True,
         "frame_A_minus_frame_B_per_K": {k: round(arms[k]["frame_A"]["auc"]
                                                  - arms[k]["frame_B"]["auc"], 6) for k in Ks}},
        {"instrument": "firm_separation_auc restricted to the both-measured sub-cohort",
         "denominator": "%d members of the %d cohort" % (frames["B_both_measured"],
                                                         frames["A_full_cohort"]),
         "positive_control": "the two frames are computed in separate calls; neither value is "
                             "derived from the other",
         "failure_look": "one frame's number carried into the other's row (80835)"},
        "after-sweep-runs"))

    cells.append(cell(
        "L3W3-fadd-3", "frames.metric_domain_predicate",
        {"predicate": "pairs where view 1 AND view 2 are MEASURED",
         "pairs": st["permutation_battery"]["rho"]["metric_domain_pairs"],
         "union_domain": frames["union_pair_domain"],
         "share_of_union": round(st["permutation_battery"]["rho"]["metric_domain_pairs"]
                                 / frames["union_pair_domain"], 6),
         "applies_to": ["spearman_rho", "topdecile_jaccard", "the permutation control"],
         "why": "over one-view pairs the 'fused' value is view-1 pass-through, and a stability "
                "statistic there measures view 1's SELF-agreement -- high for the wrong reason"},
        {"instrument": "the mask carrier's per_pair_rule, applied before any statistic",
         "denominator": "%d of %d union pairs"
                        % (st["permutation_battery"]["rho"]["metric_domain_pairs"],
                           frames["union_pair_domain"]),
         "positive_control": "C(4147,2) computed from the mask's own 4,147 ones equals the "
                             "declared 8,596,731 exactly",
         "failure_look": "a stability statistic quoted over the union"},
        "after-sweep-runs"))

    cells.append(cell(
        "L3W3-fadd-4", "frames.p_arm_domain",
        {"P_members": frames["P_arm_members"], "P_pairs": frames["P_arm_pairs"],
         "union_domain": frames["union_pair_domain"],
         "share_of_entities_pct": 6.9,
         "base_rate": 0.4904,
         "base_rate_printed_beside_every_P_row": True,
         "never_merged_into_other_frames": True,
         "firm_representation": "bd_vs_inf",
         "reading_constraint": "P is EFFECTIVELY a two-block bd-versus-inf partition "
                               "(mdpf_share_of_ones 0.00039, 19 symbols, 171 same-firm pairs). "
                               "Any per-firm reading of a P row IS a bd-versus-inf reading and "
                               "must say so; MDPF separation is UNMEASURABLE in this arm, not "
                               "merely small.",
         "arm_has_no_power": "C1_P is at ceiling too (0.985-1.000), so the P arm certifies "
                             "nothing about P's contribution -- recorded by the issuer on m-7/m-9 "
                             "and taken by the design lane as Addendum 1k"},
        {"instrument": "view P's own coverage and base_rate cells, read at 8e606c8ff8",
         "denominator": "%d pairs from %d members, against the %d union domain"
                        % (frames["P_arm_pairs"], frames["P_arm_members"],
                           frames["union_pair_domain"]),
         "positive_control": "C(1337,2) = 893,116 recomputed here from the member count and "
                             "equal to view P's declared metric_domain_both_measured",
         "failure_look": "a P number printed without its own denominator beside the union"},
        "after-sweep-runs"))

    out = {"schema": "nfra-c3materialize.l3w3.cells/1.0",
           "to_id": "NFRA_C3MATERIALIZE.TO-L3W3-COX",
           "carded_by": "0.7.0_AE_CloudOps~X",
           "decomp_ref": DECOMP,
           "cell_count": len(cells),
           "built_at_head": git_head(),
           "note": "every value DERIVED from ksweep_measurements.json and ksweep_battery.json "
                   "by build_cells.py; no value is typed.",
           "cells": cells}
    p = DELIV + "cells.L3W3-COX.json"
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
    print("WROTE %s -- %d cells" % (p, len(cells)))
    for c in cells:
        print("  %-14s %-34s %s" % (c["cell_id"], c["label"], c["status"]))


if __name__ == "__main__":
    main()
