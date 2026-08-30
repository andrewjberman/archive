"""Emit the TO-L3W3-COX proof-of-spec instance.

⛔ criterion_verbatim IS EXTRACTED FROM THE FACE, NEVER RETYPED. The face is the spec; a
hand-copied oracle is a NEW string that merely resembles the one in force, and this session
already paid for that lesson once on a regex. Same rule, same reason.

Controls are EXERCISED, not declared (see the mutant/determinism blocks): a declared-but-unrun
falsifier is a promise. Both were run against the real artifacts and their observed values are
recorded here, including the negative control that proves the mutant arm refuses the mutant
rather than refusing everything.
"""

from __future__ import annotations

import json
import re

FACE = ("org/tier2_senior/0.7.0_AE_CloudOps/task_orders/"
        "NFRA_C3MATERIALIZE.TO-L3W3-COX.k-sweep.md")
D = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/"
DELIV_ROOT = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/"
# ⛔ ONE carrier for the proof's location. The artifacts row and the write used to derive it
# separately -- the row said D + name (inside D11_L3W3_KSWEEP/) while the write said the
# parent -- so the manifest declared a path `git cat-file` returns rc=128 on. Two carriers of
# one quantity disagree the moment either moves, and proof-of-spec-check has no arm on
# artifacts_produced path resolution, so the instance read VALID with a dead path in it.
# Found by 3.0.0_SA_CVO~X at pre-cert; confirmed here by git cat-file at the pin.
PROOF_NAME = "NFRA_C3MATERIALIZE.TO-L3W3-COX_PROOF_OF_SPEC.json"
PROOF_PATH = DELIV_ROOT + PROOF_NAME


def face_criteria():
    """(criterion_id, oracle_verbatim) straight out of the cut face."""
    text = open(FACE, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<criterion id="([^"]+)"[^>]*>(.*?)</criterion>', text, re.S):
        cid, body = m.group(1), m.group(2)
        o = re.search(r"<oracle>(.*?)</oracle>", body, re.S)
        out.append((cid, " ".join(o.group(1).split()) if o else ""))
    return out


def main():
    sw = json.load(open(D + "ksweep_measurements.json", encoding="utf-8"))
    ba = json.load(open(D + "ksweep_battery.json", encoding="utf-8"))
    cells = {c["cell_id"]: c for c in
             json.load(open(D + "cells.L3W3-COX.json", encoding="utf-8"))["cells"]}
    arms, frames = sw["arms"], sw["frames"]
    Ks = [str(k) for k in sw["parameters"]["K_sweep"]]
    B = ba["stability_L3C01"]["permutation_battery"]
    real = [arms[k]["real"]["auc"] for k in Ks]

    # criterion_id -> (cell, method, invocation, output_evidence, denominator, status)
    ev = {
      "L3W3-COX-AC1": ("L3W3-b8a2-1",
        "command",
        "run_sweep.py -- declare K and T, run the sweep, read the trend's SIGN on this implementation (K in {20,50,100,200}, T=20 fixed)",
        "frame B real-arm AUC %s -> NON-MONOTONE (K50->K100 delta %+.6f). Recorded as the "
        "finding per AC1; issuer 85297 ruled no re-run, no re-seed, no smoothing."
        % (dict(zip(Ks, real)), real[2] - real[1]),
        "4 K values, AUCs over 1,820 both-measured cohort members", "PASS"),
      "L3W3-COX-AC2": ("L3W3-b8a2-2",
        "command",
        "aws s3api get-object + sha256; git show <pin>:<path> + sha256; sha256 on disk -- each input resolved and hashed BEFORE compute",
        "5 of 5 pinned with object_kind named per input; view 1 re-hashed byte-identical "
        "(e91d6991..., 2,662,267 B), view 2's carrier UNTRACKED and content-addressed "
        "(7ac11d01..., 25,489,187 B), view P 2405cdf5... @8e606c8ff8",
        "5 of 5 inputs", "PASS"),
      "L3W3-COX-AC3": ("L3W3-b8a2-3",
        "command",
        "run_sweep.py -- run all four arms PER K, with C1 on each arm's OWN domain, 5 arm-runs x 4 K",
        "real 0.510-0.518 / permuted 0.492-0.500 / C1_bm 0.729-0.838 on the bm domain; "
        "P 0.985-1.000 vs C1_P 0.985-1.000 on P's domain. The (iii)-vs-(ii) comparison read "
        "against C1 at the same K attributes the flattening to view 2's CONTENT, not to SNF.",
        "20 arm-runs; 8,596,731 bm pairs and 893,116 P pairs", "PASS"),
      "L3W3-COX-AC4": ("L3W3-b8a2-4",
        "command",
        "exact_zero_count() over the strict upper triangle -- one integer per run, counting EXACTLY-zero off-diagonal unordered pairs",
        "per K per arm; real 297,780 -> 0 -> 0 -> 0, C1_bm 3,399,312 -> 1,116,738 -> 52,912 -> 0. "
        "The K=20 real integer equals wave 2's cited 297,780 EXACTLY -- flagged, and recorded as "
        "corroboration of the IMPLEMENTATION (a combinatorial property with no float "
        "sensitivity) never of the RESULT (the AUC did not reproduce: 0.5104 vs 0.5358).",
        "20 integers, denominators 8,596,731 / 893,116 printed per arm", "PASS"),
      "L3W3-COX-AC5": ("L3W3-b8a2-5",
        "command",
        "run_battery.py -- split-half battery with an independently seeded permutation per draw (scheme permute-halfB-W1-labels, K=20, T=20, N=20)",
        "rho n=20 observed 0.956264 null +0.000723 spread 0.031595; J n=20 observed 0.931001 "
        "null +0.055421 spread 0.017860; both clear null+3*spread. 1e tolerance arms run by the "
        "producer against its own output: |null-mean| 3.5e-07/4.0e-07 and |spread-sd| "
        "2.91e-07/4.14e-07, all <= 1e-06. N=20 >= the J threshold, so run 3 can derive a J floor.",
        "20 draws per statistic, 2 statistics, 8,596,731 both-measured pairs", "PASS"),
      "L3W3-COX-AC6": ("L3W3-b8a2-6",
        "command",
        "build_cells.py -- emit one artifact per K in the wave-2 UNION shape -> fusion_l3w3cox_K{20,50,100,200}.json",
        "4 artifacts, each entity_domain 19,482 and pair_domain 189,764,421 with per-view "
        "MEASURED/ABSENT masks; carrier_table and entity_domain are distinct fields",
        "4 of 4 K values", "PASS"),
      "L3W3-COX-AC7": ("L3W3-b8a2-7",
        "command",
        "build_cells.py -- build the chain by construction and type the split_half (chain = predecessor.chain + [predecessor]); run_battery.py (split_half)",
        "chain 5 hops ending 76330685ca; predecessor_producer_code ABSENT typed as a field per "
        "issuer 84603 condition 2, so 'artifact-pinned' cannot be misread as 'byte-reproduced'. "
        "split_half all 7 fields, disjoint ASSERTED and MEASURED (intersection 0), n_a 12 + "
        "n_b 13 = 25. Implementation self-pinned at cfc5f28fb7.",
        "5 chain hops; 25 runs split 12/13", "PASS"),
      "L3W3-COX-AC8": ("L3W3-fadd-1",
        "command",
        "firm_separation_auc over the 1,941 cohort -- frame A with view-1 pass-through in place and LABELLED",
        "AUC %s; %d view-2-ABSENT members carry view-1 pass-through, labelled, never presented "
        "as fused. Frame A exceeds frame B by ~0.04 at every K -- that gap IS the pass-through "
        "showing through, and is why the label is required."
        % ({k: arms[k]["frame_A"]["auc"] for k in Ks},
           arms[Ks[0]]["frame_A"]["pass_through_members"]),
        "1,941 cohort members; %d within / %d cross pairs"
        % (arms[Ks[0]]["frame_A"]["n_within"], arms[Ks[0]]["frame_A"]["n_cross"]), "PASS"),
      "L3W3-COX-AC9": ("L3W3-fadd-2",
        "command",
        "firm_separation_auc restricted to the both-measured sub-cohort -- a separate call from frame A; no number carried between frames",
        "AUC %s, computed in a separate call from frame A; neither value derived from the other"
        % ({k: arms[k]["frame_B"]["auc"] for k in Ks}),
        "1,820 of the 1,941 cohort", "PASS"),
      "L3W3-COX-AC10": ("L3W3-fadd-3",
        "command",
        "the mask carrier's per_pair_rule applied before any statistic -- the metric domain stated AS the predicate, with its denominator",
        "both-measured pairs = %d of %d union pairs (%.2f%%); applies to rho, J and the control. "
        "C(4147,2) recomputed from the mask's own 4,147 ones equals the declared value exactly."
        % (B["rho"]["metric_domain_pairs"], frames["union_pair_domain"],
           100.0 * B["rho"]["metric_domain_pairs"] / frames["union_pair_domain"]),
        "%d of %d" % (B["rho"]["metric_domain_pairs"], frames["union_pair_domain"]), "PASS"),
      "L3W3-COX-AC11": ("L3W3-fadd-4",
        "command",
        "view P's coverage and base_rate cells read at 8e606c8ff8 -- P's frame printed as its own denominator, never merged",
        "C(1337,2) = 893,116 against the 189,764,421 union, arm at 6.9%% of entities, base rate "
        "0.4904 printed beside every P row. Recorded: P is a bd-versus-inf partition "
        "(mdpf_share_of_ones 0.00039) and MDPF separation is UNMEASURABLE in this arm; and the "
        "arm has NO POWER because C1_P is at ceiling too (issuer 85297, design Addendum 1k).",
        "893,116 P pairs from 1,337 members against 189,764,421", "PASS"),
    }

    acceptance = []
    for cid, verbatim in face_criteria():
        cell_id, method, inv, out, den, status = ev[cid]
        # ⛔ A CRITERION MAY NOT CLAIM PASS AHEAD OF ITS CELL. ruff flagged `cells` as loaded
        # and unused, which was true and was the tell: the status_reason ASSERTED "cell WRITTEN
        # with its gate receipt cited" while nothing read the cell to check it. Using the map
        # turns that assertion into a measurement.
        c = cells.get(cell_id)
        if c is None:
            raise ValueError("%s references cell %s, which the carrier does not contain"
                             % (cid, cell_id))
        if c["status"] != "WRITTEN" or not c.get("gate_receipt"):
            raise ValueError("%s claims PASS but cell %s is status=%s gate_receipt=%s"
                             % (cid, cell_id, c["status"], bool(c.get("gate_receipt"))))
        acceptance.append({"criterion_id": cid, "criterion_verbatim": verbatim,
                           "method": method, "invocation": inv, "output_evidence": out,
                           "denominator": den, "status": status,
                           "status_reason": "cell %s status=%s, gate %s receipt cited (verified "
                                            "against the carrier at build time, not asserted)"
                                            % (cell_id, c["status"], c["sequence_gate"])})

    COVERED_BY = {
        "snf_ksweep.py": ["L3W3-COX-AC3", "L3W3-COX-AC4", "L3W3-COX-AC5"],
        "build_proof.py": ["L3W3-COX-AC1"],
        "NFRA_C3MATERIALIZE.TO-L3W3-COX_PROOF_OF_SPEC.json": ["L3W3-COX-AC1"],
    }
    arts = [dict({"path_or_key": D + n, "kind": k, "commit_or_etag": c,
                  "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE", "deploy_evidence":
                  "repo artifact; this face deploys nothing to a served plane"},
                 **({"artifact_covered_by": COVERED_BY[n]} if n in COVERED_BY else {}))
            for n, k, c in [
                ("snf_ksweep.py", "script", "cfc5f28fb7"),
                ("run_sweep.py", "script", "e2ab79fba4"),
                ("ksweep_measurements.json", "config_data", "e2ab79fba4"),
                ("run_battery.py", "script", "2234620592"),
                ("ksweep_battery.json", "config_data", "2234620592"),
                ("build_cells.py", "script", "2234620592"),
                ("cells.L3W3-COX.json", "config_data", "2234620592"),
                ("fusion_l3w3cox_K20.json", "config_data", "2234620592"),
                ("fusion_l3w3cox_K50.json", "config_data", "2234620592"),
                ("fusion_l3w3cox_K100.json", "config_data", "2234620592"),
                ("fusion_l3w3cox_K200.json", "config_data", "2234620592"),
                # ⛔ PENDING, not c36a309f4d. The CVO/issuer instruction to pin this
                # row at c36 rested on "build_proof.py will not be carried by the
                # repair commit" -- true of a proof-ONLY patch. This repair fixes the
                # ROOT (one carrier for the proof path) so the builder IS carried,
                # and naming c36 would cite the version that HELD the defect.
                ("build_proof.py", "script", "PENDING-THIS-COMMIT")]]
    # the proof itself: declared at the path it is actually WRITTEN to, and the only
    # row that may still say PENDING -- the repair commit carries this file.
    arts.append({"path_or_key": PROOF_PATH, "kind": "config_data",
                 "commit_or_etag": "PENDING-THIS-COMMIT",
                 "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
                 "deploy_evidence": "repo artifact; this face deploys nothing to a "
                                    "served plane",
                 "artifact_covered_by": ["L3W3-COX-AC1"]})

    proof = {
        "schema_version": "1.0",
        "to_id": "NFRA_C3MATERIALIZE.TO-L3W3-COX",
        # OBJECT form {doc, vintage_commit, to_ref}, read at .tools/proof-of-spec-check.py:300-313.
        # A bare string raises a TypeError the tool deliberately labels NOT-A-VERDICT, because a
        # shape error used to exit rc=1 byte-identically to a legitimate INVALID.
        "decomp_ref": {
            "doc": ("workflows/atom_decomposition/runs/nfra-c3materialize-L3/"
                    "20260829T1906Z/DECOMP.md"),
            "vintage_commit": "94935b740e",
            "to_ref": FACE},
        "phase": "INVESTIGATION",
        "spec_ref": {"doc": FACE, "group": "OTHER",
                     "vintage_commit": "b8c47d1233"},
        "assignee": "0.7.0_AE_CloudOps~X",
        "artifacts_produced": arts,
        "acceptance": acceptance,
        "controls": {
            "mutant": {
                "description": "split halves made to OVERLAP (run 11 in both) -- Addendum 1e "
                               "item 5 makes that FORM_DEFECT, so the builder must refuse it",
                "expected": "refusal",
                "observed": "REFUSED with 'halves overlap -> FORM_DEFECT by 1e item 5'. "
                            "NEGATIVE CONTROL run in the same pass: the REAL halves (12/13, "
                            "intersection 0) are ACCEPTED -- so the arm refuses the mutant "
                            "rather than refusing everything.",
                "status": "FIRED-AS-EXPECTED"},
            "determinism": {
                "method": "recompute the K=20 real arm end-to-end from the pinned inputs and "
                          "compare its exact-zero integer to the committed artifact",
                "observed": "recomputed 297,780 == committed 297,780",
                "status": "STABLE"}},
        "declared_exclusions": [
            {"item": "a J floor derived this wave",
             "reason": "run 1's battery is N=6 against a threshold of 20; the issuer ruled "
                       "REFUSED-INSUFFICIENT-N (85297/84350). This face EMITS N=20 so run 3 can "
                       "derive one, but derives none itself -- 1b prohibits same-run derivation."},
            {"item": "any wave-2 number used as a wave-3 baseline",
             "reason": "Addendum 1i(ii): the sign is implementation-independent, the second "
                       "decimal is not. Wave 3's own K=20 is the baseline; wave 2's decimals "
                       "are never a target."},
            {"item": "a sec-6 test discharge",
             "reason": "m-7: wave 3 discharges no sec-6 test by its own rule; it gates whether "
                       "L4 is safe to build."},
            {"item": "a verdict on the P arm's design",
             "reason": "the arm is measured exactly as the certified cells specify; the ceiling "
                       "finding is the issuer's (m-7/m-9) and the design lane's (Addendum 1k), "
                       "not this lane's to re-cut."}],
        "surprises": [
            "OBSERVATION/INERT -- the K=20 real-arm exact-zero integer reproduces wave 2's "
            "297,780 EXACTLY across two implementations. Flagged per 84600; the mechanism is "
            "stated (a combinatorial property of the K-NN sparsity under diffusion, versus a "
            "float AUC that did NOT reproduce) so it reads as corroboration of the "
            "IMPLEMENTATION, never agreement of the RESULT. Issuer 85297 concurs.",
            "OBSERVATION/INERT -- the P arm's own baseline C1_P is at ceiling (0.985-1.000) "
            "on P's 1,337 members, so that arm certifies nothing about P's contribution; and "
            "P is the firm indicator while the metric is firm separation. Recorded by the "
            "issuer on m-7/m-9 and taken by the design lane as Addendum 1k.",
            "OBSERVATION/INERT -- wave 2's fusion PRODUCER CODE is absent from this device "
            "while its artifacts are on origin. Censused (84585: 3 sweeps, firing positive "
            "control), scoped to this device, accepted on-spec by 84603/84600, and carried as "
            "a typed field on AC7's chain so no reader mistakes artifact-pinned for "
            "byte-reproduced.",
        ],
        "session_log": ("org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-08-30/"
                        "session_TO-L3W3-COX.md"),
        "compiler_tools": [
            {"tool": "comp-to", "invocation": "comp-to NFRA_C3MATERIALIZE.TO-L3W3-COX.k-sweep",
             "result": "PASS -- session TO_ID bound before any other act, closing the 57-of-57 "
                       "unbound-rows gap this lane measured on its own predecessor (84087)"},
            {"tool": "comp-find", "invocation": "comp-find 'l3w2cox|394bdac4c227' --all --files",
             "result": "PASS -- 115 hits / 131,581 files, DEF band 0: wave 2's producer code "
                       "exists in no executable on this device"},
            {"tool": "comp-find", "invocation": "comp-find 'def .*snf|similarity_network|"
                                                "fuse_views|def fuse' --all --files",
             "result": "PASS -- 115 hits / 131,563 files; every DEF-band hit is decomposition "
                       "tooling or vendored sklearn/scipy"},
            {"tool": "comp-find", "invocation": "comp-find 'Msg-ID:\\*\\* 83671' --all",
             "result": "PASS -- positive control that a lane inbox read/ file is inside the "
                       "corpus, run before converting any zero into an absence"}],
    }
    p = PROOF_PATH
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(proof, fh, indent=1)
    print("WROTE %s -- %d criteria, %d artifacts" % (p, len(acceptance), len(arts)))
    for a in acceptance:
        print("  %-16s %-6s %s" % (a["criterion_id"], a["status"], a["criterion_verbatim"][:64]))


if __name__ == "__main__":
    main()
