"""AC5's permutation battery + AC7's split-half carrier, in Addendum 1c/1d/1e's typed shape.

⛔ N >= 20 ON PURPOSE. Run 1's battery was N=6, which is why the issuer had to refuse a J floor
this wave (85297 / 84350: rho DERIVES at N>=5, J REFUSED-INSUFFICIENT-N at 6 < 20). Emitting
N >= 20 here is what lets run 3 derive a J floor from run 2 instead of meeting the same
refusal a third time.

THE SPLIT-HALF PROTOCOL, read at source rather than reconstructed
(D11_L3_WAVE1_BOUNDARY_DECLARATIONS_20260829.md Addendum 1e item 5, and wave 2's own
draws_0_provenance): view 1's 25 partition RUNS are split into two DISJOINT halves; W1 is
built from each half; each is fused with view 2 at the carded (K, T) = (20, 20); the two fused
matrices are compared on the both-measured pair domain by Spearman rho and top-decile Jaccard.
A null draw permutes THE ENTITY LABELS OF HALF-B's W1, re-fuses, and re-compares -- scheme
`permute-halfB-W1-labels`, typed here as a string because 1e item 4 forbids a consumer
inferring a scheme from prose.

⛔ ONE INDEPENDENTLY SEEDED GENERATOR PER DRAW. Addendum 1e (iii)/KEY records that wave 2's
permuted arm was UNSOUND AS A GATE partly because a single RNG stream was consumed by another
arm first, making the permutation a function of an unrelated arm's draw count and not
reproducible under any edit above it. Here every draw gets its own child stream from a
declared root seed via SeedSequence.spawn, so draw i is reproducible regardless of what any
other arm did.

Emits, per Addendum 1c/1e: precision_decimals, scheme (typed), n_permutations PER STATISTIC,
null, spread = SAMPLE sd (ddof=1), draws[], and the split_half block with all six named fields
{battery_id, seed, half_a_runs, half_b_runs, disjoint, n_a, n_b}.
"""

from __future__ import annotations

import collections
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

BATTERY_ID = "L3W3-COX-BATTERY-1"
BATTERY_SEED = 20260830
SPLIT_HALF_SEED = 20260830
N_PERM = 20                      # >= 20 so a J floor can derive at run 3 (Addendum 1d)
K_CARDED, T_CARDED = 20, 20      # the carded arm; any other K is a DIFFERENT arm (1i)
PRECISION_DECIMALS = 6


def log(*a):
    print(*a, flush=True)


def spearman_rho(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman rho via average ranks -- ties matter here and are averaged, not broken."""
    def rank(x):
        order = np.argsort(x, kind="mergesort")
        r = np.empty(x.size, dtype=np.float64)
        s = x[order]
        i = 0
        while i < s.size:
            j = i
            while j + 1 < s.size and s[j + 1] == s[i]:
                j += 1
            r[order[i:j + 1]] = 0.5 * (i + j) + 1.0
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    ra -= ra.mean()
    rb -= rb.mean()
    d = np.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / d) if d else float("nan")


def topdecile_jaccard(a: np.ndarray, b: np.ndarray) -> float:
    """Jaccard of the two top-decile pair sets. Ties at the cut are INCLUDED on both sides."""
    n = a.size
    k = max(1, n // 10)
    ta = np.argpartition(-a, k - 1)[:k]
    tb = np.argpartition(-b, k - 1)[:k]
    sa, sb = set(ta.tolist()), set(tb.tolist())
    u = len(sa | sb)
    return float(len(sa & sb) / u) if u else float("nan")


def main():
    t0 = time.time()
    parts = M.load_view1_partitions(SCRATCH + "W_STRUCTURE_FACTORIZED.json")
    mask = np.array(json.load(open(DELIV + "D11_L3W2_FUSION/mask_carrier_union.json",
                                   encoding="utf-8"))["vector"], dtype=np.uint8)
    L2 = json.load(open(SCRATCH + "L2_VIEW_ARTIFACTS.json", encoding="utf-8"))
    pop = [e["entity_id"] for e in
           [v for v in L2["views"] if v.get("view_id") == "STRUCTURE"][0]["entity_set"]["entities"]]
    sg = json.load(open("infra/aws/globgrph/stitch_graph.json", encoding="utf-8"))
    c2 = {n["id"] for n in sg["classes_data"]["c2c3_motif"]["nodes"] if n["type"] == "C2Motif"}
    F = collections.defaultdict(set)
    for e in sg["edges"]:
        if e["edge_type"] == "CONTAINS" and e["source"] in c2:
            F[e["target"]].add(e["source"])
    fam = [frozenset(F.get(eid, ())) for eid in pop]

    bm = np.flatnonzero(mask == 1)
    W2 = M.view2_affinity(fam, bm)

    # ---- the DISJOINT split of view 1's 25 runs, declared as a field (1e item 5) ----
    rs = np.random.default_rng(SPLIT_HALF_SEED)
    perm_runs = rs.permutation(parts.shape[0])
    half_a = sorted(int(x) for x in perm_runs[: parts.shape[0] // 2])
    half_b = sorted(int(x) for x in perm_runs[parts.shape[0] // 2:])
    assert not (set(half_a) & set(half_b)), "halves overlap -> FORM_DEFECT by 1e item 5"
    log("split_half: n_a=%d n_b=%d disjoint=True" % (len(half_a), len(half_b)))

    W1a = M.view1_affinity(parts[half_a], bm) * (M.VIEW1_DENOMINATOR / len(half_a))
    W1b = M.view1_affinity(parts[half_b], bm) * (M.VIEW1_DENOMINATOR / len(half_b))

    FA = M.snf([W1a, W2], k=K_CARDED, t=T_CARDED)
    FB = M.snf([W1b, W2], k=K_CARDED, t=T_CARDED)
    va, vb = M.pair_vector(FA), M.pair_vector(FB)
    obs_rho = spearman_rho(va, vb)
    obs_J = topdecile_jaccard(va, vb)
    log("OBSERVED  rho=%.6f  J=%.6f  over %d both-measured pairs" % (obs_rho, obs_J, va.size))

    # ---- the battery: one INDEPENDENT child stream per draw (1e (iii)/KEY) ----
    children = np.random.SeedSequence(BATTERY_SEED).spawn(N_PERM)
    draws_rho, draws_J = [], []
    for i, child in enumerate(children):
        rng = np.random.default_rng(child)
        p = rng.permutation(W1b.shape[0])
        FBp = M.snf([W1b[np.ix_(p, p)], W2], k=K_CARDED, t=T_CARDED)
        vbp = M.pair_vector(FBp)
        r, j = spearman_rho(va, vbp), topdecile_jaccard(va, vbp)
        draws_rho.append(round(r, PRECISION_DECIMALS))
        draws_J.append(round(j, PRECISION_DECIMALS))
        log("draw %2d/%d  rho=%+.6f  J=%.6f  (%.0fs elapsed)" % (i + 1, N_PERM, r, j, time.time() - t0))

    def block(draws, observed, stat):
        arr = np.array(draws, dtype=np.float64)
        return {"scheme": "permute-halfB-W1-labels",
                "n_permutations": len(draws),
                "null": round(float(arr.mean()), PRECISION_DECIMALS),
                "spread": round(float(arr.std(ddof=1)), PRECISION_DECIMALS),
                "spread_status": "MEASURED",
                "spread_basis": "SAMPLE sd, ddof=1",
                "observed": round(float(observed), PRECISION_DECIMALS),
                "draws": draws,
                "metric_domain": "both-measured",
                "metric_domain_pairs": int(va.size),
                "statistic": stat}

    out = {
        "schema": "nfra-c3materialize.l3w3.battery/1.0",
        "to_id": "NFRA_C3MATERIALIZE.TO-L3W3-COX",
        "executor": "0.7.0_AE_CloudOps~X",
        "carded_arm": {"K": K_CARDED, "T": T_CARDED,
                       "note": "the carded arm is (K,T)=(20,20); any other K is a DIFFERENT arm (1i)"},
        "precision_decimals": PRECISION_DECIMALS,
        "stability_L3C01": {
            "metric_domain_predicate":
                "pairs where view 1 AND view 2 are MEASURED: %d of 189,764,421" % va.size,
            "permutation_battery": {"rho": block(draws_rho, obs_rho, "spearman_rho"),
                                    "J": block(draws_J, obs_J, "topdecile_jaccard")},
            "split_half": {"battery_id": BATTERY_ID, "seed": SPLIT_HALF_SEED,
                           "half_a_runs": half_a, "half_b_runs": half_b,
                           "disjoint": True, "n_a": len(half_a), "n_b": len(half_b)},
            "battery_seed_root": BATTERY_SEED,
            "seeding": "one independent SeedSequence child per draw; draw i does not depend on "
                       "any other arm's draw count (Addendum 1e (iii)/KEY)",
        },
    }
    p = DELIV + "D11_L3W3_KSWEEP/ksweep_battery.json"
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    log("WROTE %s in %.0fs" % (p, time.time() - t0))


if __name__ == "__main__":
    main()
