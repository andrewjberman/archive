"""Run the TO-L3W3-COX k-sweep: four arms per K, both frames, with the exact-zero census.

⛔ WRITES NO CELL VALUE. This produces the measurement artifact; the cells are written
separately, and only with their gate receipt cited (view P delivered @8e606c8ff8,
0.8.0_AE_CloudComp~Y 84776; issuer gate receipt 2.0.0_SA_COO~X 84894).

AC3's four arms, PER K, at the same T / implementation / population / pair predicate / frame:
  (i)   view 1 fused with view 2 REAL
  (ii)  view 1 fused with view 2 PERMUTED      -- C2's complement
  (iii) view 1 fused with P
  (iv)  view 1 fused with ITSELF (C1)          -- the method-intrinsic baseline

⛔ C1 IS COMPUTED ON EACH ARM'S OWN DOMAIN. Arms (i)/(ii) live on the 4,147 both-measured
entities; arm (iii) lives on P's 1,337. A C1 taken on one domain cannot bound method cost on
the other, and AC3's whole discriminating comparison ((iii) vs (ii) read against C1 at the
SAME K) collapses if the baseline is borrowed across domains.
"""

from __future__ import annotations

import collections
import hashlib
import json
import sys
import time

import numpy as np

sys.path.insert(0, "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP")
import snf_ksweep as M  # noqa: E402

SCRATCH = ("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
           "C--Users-AndrewBerman-Desktop-ajb-workspace/"
           "b3cf19c0-4b0d-4065-b24b-caf9685c8a2a/scratchpad/")
DELIV = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/"
PERM_SEED = 20260830


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def log(*a):
    print(*a, flush=True)


def main():
    t_start = time.time()

    # ---- inputs, each pinned by the digest of the bytes actually read (AC2) ----
    v1_path = SCRATCH + "W_STRUCTURE_FACTORIZED.json"
    parts = M.load_view1_partitions(v1_path)
    mask = np.array(json.load(open(DELIV + "D11_L3W2_FUSION/mask_carrier_union.json",
                                   encoding="utf-8"))["vector"], dtype=np.uint8)
    cohort = json.load(open(DELIV + "D11_L3W2_FUSION/firm_cohort_shared.json",
                            encoding="utf-8"))["cohort"]
    L2 = json.load(open(SCRATCH + "L2_VIEW_ARTIFACTS.json", encoding="utf-8"))
    pop = [e["entity_id"] for e in
           [v for v in L2["views"] if v.get("view_id") == "STRUCTURE"][0]["entity_set"]["entities"]]

    # view 2 family sets, re-derived from the untracked stitch graph (content-addressed)
    sg = json.load(open("infra/aws/globgrph/stitch_graph.json", encoding="utf-8"))
    c2 = {n["id"] for n in sg["classes_data"]["c2c3_motif"]["nodes"] if n["type"] == "C2Motif"}
    F = collections.defaultdict(set)
    for e in sg["edges"]:
        if e["edge_type"] == "CONTAINS" and e["source"] in c2:
            F[e["target"]].add(e["source"])
    fam = [frozenset(F.get(eid, ())) for eid in pop]

    # view P
    vp = json.load(open(DELIV.replace("0.7.0_AE_CloudOps", "0.8.0_AE_CloudComp")
                        + "D11_L3W3_VIEWP/VIEWP_firm_partition.json", encoding="utf-8"))
    p_cov = vp["rows"]["coverage_measured_absent"]["value"]
    p_lo, p_hi = p_cov["measured_index_min"], p_cov["measured_index_max"]
    p_idx = np.arange(p_lo, p_hi + 1)

    firm_of = {c["entity_id"]: c["firm"] for c in cohort}

    bm_idx = np.flatnonzero(mask == 1)                  # 4,147 both-measured
    log("inputs: pop=%d bm=%d cohort=%d P=%d" % (len(pop), len(bm_idx), len(firm_of), len(p_idx)))

    # ---- the two domains ----
    W1_bm = M.view1_affinity(parts, bm_idx)
    W2_bm = M.view2_affinity(fam, bm_idx)
    W1_p = M.view1_affinity(parts, p_idx)
    WP = M.viewP_affinity(firm_of, [pop[i] for i in p_idx]) if all(
        pop[i] in firm_of for i in p_idx) else None
    if WP is None:                                       # P members not all firm-labelled
        lab = [firm_of.get(pop[i]) for i in p_idx]
        keep = np.array([x is not None for x in lab])
        log("P members carrying a cohort firm label: %d of %d" % (int(keep.sum()), len(p_idx)))
        p_idx = p_idx[keep]
        W1_p = M.view1_affinity(parts, p_idx)
        WP = M.viewP_affinity(firm_of, [pop[i] for i in p_idx])

    W2_perm = M.permute_view(W2_bm, PERM_SEED)

    # frames: A = full 1,941 cohort, B = the both-measured sub-cohort
    cohort_ids = [c["entity_id"] for c in cohort]
    pos_of = {e: i for i, e in enumerate(pop)}
    cohort_pop_idx = np.array([pos_of[e] for e in cohort_ids])
    in_bm = np.isin(cohort_pop_idx, bm_idx)
    log("frame A = %d cohort; frame B = %d both-measured (A - B = %d view2-ABSENT pass-through)"
        % (len(cohort_ids), int(in_bm.sum()), int((~in_bm).sum())))

    bm_pos = {int(g): i for i, g in enumerate(bm_idx)}
    W1_full = M.view1_affinity(parts, cohort_pop_idx)     # frame-A pass-through source
    firms_A = [firm_of[e] for e in cohort_ids]

    results = {"parameters": {"K_sweep": list(M.K_SWEEP), "T": M.T_FIXED,
                              "permutation_seed": PERM_SEED},
               "inputs": {"view1_served_sha256": sha(v1_path),
                          "stitch_graph_sha256": sha("infra/aws/globgrph/stitch_graph.json")},
               "frames": {"A_full_cohort": len(cohort_ids),
                          "B_both_measured": int(in_bm.sum()),
                          "P_arm_members": int(len(p_idx)),
                          "P_arm_pairs": int(len(p_idx) * (len(p_idx) - 1) // 2),
                          "union_pair_domain": 189764421},
               "arms": {}}

    for k in M.K_SWEEP:
        row = {}
        for name, views, dom_idx in (
            ("real",     [W1_bm, W2_bm],   bm_idx),
            ("permuted", [W1_bm, W2_perm], bm_idx),
            ("C1_bm",    [W1_bm, W1_bm],   bm_idx),
            ("P",        [W1_p,  WP],      p_idx),
            ("C1_P",     [W1_p,  W1_p],    p_idx),
        ):
            t0 = time.time()
            S = M.snf(views, k=k, t=M.T_FIXED)
            zeros = M.exact_zero_count(S)
            npair = S.shape[0] * (S.shape[0] - 1) // 2
            # AUC on the arm's own domain, restricted to cohort members present in it
            dom_pos = {int(g): i for i, g in enumerate(dom_idx)}
            sel = [(dom_pos[int(g)], firm_of[e])
                   for g, e in zip(cohort_pop_idx, cohort_ids) if int(g) in dom_pos]
            if sel:
                rows = np.array([s[0] for s in sel])
                fr = [s[1] for s in sel]
                auc, nw, nc, ties = M.firm_separation_auc(S[np.ix_(rows, rows)], fr)
            else:
                auc, nw, nc, ties = float("nan"), 0, 0, 0
            row[name] = {"auc": auc, "n_within": nw, "n_cross": nc, "ties_at_decision": ties,
                         "exact_zero_pairs": zeros, "pair_domain": npair,
                         "exact_zero_share": round(zeros / npair, 6) if npair else None,
                         "seconds": round(time.time() - t0, 1)}
            log("K=%-4d %-9s auc=%.6f  zeros=%9d/%9d (%.2f%%)  within=%d cross=%d  %.0fs"
                % (k, name, auc, zeros, npair, 100.0 * zeros / npair, nw, nc,
                   row[name]["seconds"]))
        # frame A: cohort with view-2-ABSENT members carrying view-1 pass-through, LABELLED
        SA = W1_full.copy()
        idxA = np.flatnonzero(in_bm)
        src = np.array([bm_pos[int(g)] for g in cohort_pop_idx[in_bm]])
        Sfull = M.snf([W1_bm, W2_bm], k=k, t=M.T_FIXED)
        SA[np.ix_(idxA, idxA)] = Sfull[np.ix_(src, src)]
        aucA, nwA, ncA, tA = M.firm_separation_auc(SA, firms_A)
        row["frame_A"] = {"auc": aucA, "n_within": nwA, "n_cross": ncA,
                          "pass_through_members": int((~in_bm).sum()),
                          "pass_through_labelled": True,
                          "note": "the %d view-2-ABSENT members carry view-1 pass-through, "
                                  "LABELLED as such and never presented as fused values"
                                  % int((~in_bm).sum())}
        aucB, nwB, ncB, tB = M.firm_separation_auc(SA[np.ix_(idxA, idxA)],
                                                   [firms_A[i] for i in idxA])
        row["frame_B"] = {"auc": aucB, "n_within": nwB, "n_cross": ncB}
        log("K=%-4d frame_A auc=%.6f (n=%d, %d pass-through) | frame_B auc=%.6f (n=%d)"
            % (k, aucA, len(firms_A), int((~in_bm).sum()), aucB, int(in_bm.sum())))
        results["arms"][str(k)] = row

    out = DELIV + "D11_L3W3_KSWEEP/ksweep_measurements.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    log("WROTE %s in %.0fs total" % (out, time.time() - t_start))


if __name__ == "__main__":
    main()
