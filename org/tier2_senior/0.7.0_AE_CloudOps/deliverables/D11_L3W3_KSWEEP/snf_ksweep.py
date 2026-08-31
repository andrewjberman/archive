"""SNF k-sweep engine for NFRA_C3MATERIALIZE.TO-L3W3-COX (D11 L3 wave 3).

WHY THIS FILE EXISTS AS COMMITTED CODE. Wave 2's fusion artifacts are on origin; the code
that produced them was never committed and is ABSENT from this device (censused 2026-08-30,
0.7.0_AE_CloudOps~X msg 84585; issuer reading 84603, design lane 84600). Wave 3 re-implements
from the artifacts' own declared derivation and PINS THE IMPLEMENTATION, so wave 4 reads code
rather than a memory of code (2.0.0_SA_COO~X 84603 condition 1).

THIS IS A DIFFERENT IMPLEMENTATION FROM WAVE 2'S, AND THAT IS LOAD-BEARING
(1.0.0_SA_CTO~X 84600 precision 2, Addendum 1i(ii) @dd8ac390ef -- "the sign is
implementation-independent, the second decimal is not"; 0.5358 vs 0.5114 measured across two
implementations of the same fusion):
  * AC1 scores on the SIGN of the K trend on THIS implementation, never on value agreement
    with wave 2's decimals. A K=20 result reproducing 0.5358 to four places is a COINCIDENCE
    TO FLAG, not a confirmation.
  * Wave 3's own K=20 point is the baseline every other K is read against. No wave-2 number
    enters a wave-3 comparison as a baseline -- which is why AC3 makes C1 = SNF(view1, view1)
    PER K non-optional.

METHOD FIDELITY IS NOT A FREE PARAMETER (L3-C04, design record sec 3): SNF is RETAINED;
weighted combination, multilayer SBM and intersection are refused on the record. Any departure
from the declared form is stated on the artifact beside `method`, never discovered by the next
sweep.

DECLARED DERIVATION THIS FILE IMPLEMENTS, all quoted from the pinned artifacts:
  view 1  W1(i,j) = numerator(i,j) / 25, numerator = the count of the 25 partitions placing
          i and j in the same block.  Source: the SERVED factorized artifact
          s3://opal-313476888478-globgrph/c3materialize-b4/out/eb009c01-.../W_STRUCTURE_FACTORIZED.json
          sha256 e91d69910fc9d4eabb58eedb8a73165476225ab838977e8d6c16604af3f5e19a (2,662,267 B).
  view 2  W2(i,j) = |F(i) & F(j)| / |F(i) | F(j)| over motif-family sets (19 families =
          13 structural archetypes + 6 defect motifs, intersection 0, NEVER flattened into one
          19-valued enum).
  mask    BOTH_MEASURED iff v[i]==1 and v[j]==1, else ONE_VIEW. 4,147 measured of 19,482.
  domain  the metric domain for rho / J / the control is the BOTH-MEASURED pairs:
          C(4147,2) = 8,596,731 of 189,764,421 union pairs (4.53%).

⛔ ABSENT IS NOT ZERO. A 0.0 asserts measured low affinity; ABSENT asserts no evidence.
Collapsing them is the failure PRD sec 3 L3 names, and this module never does it: ABSENT
entities are carried by the mask and excluded from the metric domain, never coerced.

Author: 0.7.0_AE_CloudOps~X.  TO: NFRA_C3MATERIALIZE.TO-L3W3-COX.
"""

from __future__ import annotations

import hashlib
import json
from typing import Iterable

import numpy as np
from scipy import sparse

# The sweep's declared parameters. T is FIXED so K is the only moving parameter (AC1).
K_SWEEP = (20, 50, 100, 200)
T_FIXED = 20
VIEW1_DENOMINATOR = 25


# --------------------------------------------------------------------------------------
# view 1 -- the factorized consensus
# --------------------------------------------------------------------------------------

def load_view1_partitions(path: str) -> np.ndarray:
    """Return the 25 x n partition-label matrix from the served factorized artifact."""
    with open(path, "rb") as fh:
        raw = fh.read()
    doc = json.loads(raw.decode("utf-8"))
    parts = np.asarray(doc["partitions"], dtype=np.int64)
    if parts.shape[0] != doc["denominator"]:
        raise ValueError(
            "partition count %d does not equal the artifact's own denominator %d"
            % (parts.shape[0], doc["denominator"])
        )
    return parts


def view1_affinity(partitions: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """Dense W1 over the entities named by `idx`, exact, from the factorized partitions.

    W1(i,j) = (# partitions placing i and j in the same block) / 25. Computed by counting
    agreements across the 25 label rows -- the artifact's evaluator verbatim, not a
    reconstruction of it.
    """
    lab = partitions[:, idx]                       # 25 x m
    m = lab.shape[1]
    num = np.zeros((m, m), dtype=np.int16)
    for r in range(lab.shape[0]):
        row = lab[r]
        num += (row[:, None] == row[None, :]).astype(np.int16)
    return num.astype(np.float64) / float(VIEW1_DENOMINATOR)


def view1_numerator_histogram(partitions: np.ndarray) -> np.ndarray:
    """The full 26-cell numerator histogram over every unordered pair, via signatures.

    This is the falsifier for the loader: the served artifact publishes this histogram, so a
    re-implementation that reproduces all 26 cells over 189,764,421 pairs has been checked
    against the producer rather than against itself. Collapsing n nodes to their distinct
    25-label signatures turns C(n,2) pair comparisons into C(S,2) signature comparisons.
    """
    lab = partitions.T                             # n x 25
    uniq, counts = np.unique(lab, axis=0, return_counts=True)
    hist = np.zeros(VIEW1_DENOMINATOR + 1, dtype=np.int64)
    # pairs inside one signature agree on all 25 by construction
    hist[VIEW1_DENOMINATOR] += int((counts * (counts - 1) // 2).sum())
    for i in range(len(uniq) - 1):
        agree = (uniq[i + 1:] == uniq[i]).sum(axis=1)
        np.add.at(hist, agree, counts[i] * counts[i + 1:])
    return hist


# --------------------------------------------------------------------------------------
# view 2 -- Jaccard over motif-family sets
# --------------------------------------------------------------------------------------

def view2_affinity(family_sets: list[frozenset], idx: np.ndarray) -> np.ndarray:
    """Dense W2 over `idx` as Jaccard over motif-family sets.

    A member in two families contributes to BOTH and is never penalised (ANDREW-DIRECT
    2026-08-29 02:03Z R-2). An empty union yields 0.0 affinity for a MEASURED pair -- callers
    must not hand ABSENT entities to this function; ABSENT is carried by the mask.
    """
    sel = [family_sets[i] for i in idx]
    m = len(sel)
    out = np.zeros((m, m), dtype=np.float64)
    for a in range(m):
        fa = sel[a]
        for b in range(a, m):
            fb = sel[b]
            union = len(fa | fb)
            out[a, b] = out[b, a] = (len(fa & fb) / union) if union else 0.0
    return out


# --------------------------------------------------------------------------------------
# SNF
# --------------------------------------------------------------------------------------

def _full_kernel(W: np.ndarray) -> np.ndarray:
    """P: the row-normalised full similarity, diagonal carrying half the mass (Wang et al.)."""
    A = W.copy()
    np.fill_diagonal(A, 0.0)
    rs = A.sum(axis=1)
    rs[rs == 0] = 1.0
    P = A / (2.0 * rs[:, None])
    np.fill_diagonal(P, 0.5)
    return P


def _knn_kernel(W: np.ndarray, k: int) -> sparse.csr_matrix:
    """S: the K-NN sparsified, row-normalised local similarity.

    ⛔ HARD-K SPARSIFICATION IS WHY AC4 EXISTS. Entries outside a row's top-K are left at
    EXACTLY 0.0 and reach the fused matrix as exact zeros through diffusion. Rank AUC is NOT
    tie-invariant and the tie mass moves WITH K, so a rising AUC cannot be told from fewer
    ties without the exact-zero integer printed beside it.
    """
    n = W.shape[0]
    A = W.copy()
    np.fill_diagonal(A, 0.0)
    kk = min(k, n - 1)
    # top-kk per row, ties broken by index -- deterministic, no random tie-break
    part = np.argpartition(-A, kk - 1, axis=1)[:, :kk]
    rows = np.repeat(np.arange(n), kk)
    cols = part.ravel()
    vals = A[rows, cols]
    S = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    rs = np.asarray(S.sum(axis=1)).ravel()
    rs[rs == 0] = 1.0
    return sparse.diags(1.0 / rs) @ S


def snf(views: Iterable[np.ndarray], k: int, t: int = T_FIXED) -> np.ndarray:
    """Similarity Network Fusion over `views` at neighbourhood size k for t iterations.

    P_v <- S_v (mean of P_u, u != v) S_v^T, then the fused matrix is the mean of the P_v.
    With one view passed twice this is C1 -- the method-intrinsic baseline AC3 requires PER K,
    because K changes SNF itself and a C1 fixed at one K cannot bound method cost at another.
    """
    Ws = [np.asarray(W, dtype=np.float64) for W in views]
    if len(Ws) < 2:
        raise ValueError("SNF needs at least two views; pass view 1 twice for the C1 arm")
    P = [_full_kernel(W) for W in Ws]
    S = [_knn_kernel(W, k) for W in Ws]
    m = len(Ws)
    for _ in range(t):
        nxt = []
        for v in range(m):
            others = sum(P[u] for u in range(m) if u != v) / float(m - 1)
            nxt.append(np.asarray(S[v] @ others @ S[v].T))
        P = nxt
    fused = sum(P) / float(m)
    return (fused + fused.T) / 2.0


# --------------------------------------------------------------------------------------
# the census AC4 refuses a row without
# --------------------------------------------------------------------------------------

def exact_zero_count(M: np.ndarray) -> int:
    """Count of EXACTLY-zero off-diagonal unordered pairs. One integer per run.

    AC4: "its absence REFUSES the row". Returned as a Python int so it serialises as an
    integer and never as a float that a reader could mistake for a rate.
    """
    iu = np.triu_indices_from(M, k=1)
    return int(np.count_nonzero(M[iu] == 0.0))


def pair_vector(M: np.ndarray) -> np.ndarray:
    """The strict upper triangle as a flat vector -- the unordered-pair domain, in index order."""
    iu = np.triu_indices_from(M, k=1)
    return M[iu]


def sha256_of_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# --------------------------------------------------------------------------------------
# view P -- the firm partition (0.8.0_AE_CloudComp~Y, TO-L3W3-CCY)
# --------------------------------------------------------------------------------------

def viewP_affinity(firm_of: dict, ids: list[str]) -> np.ndarray:
    """W_P(i,j) = 1 if firm(i) == firm(j) else 0, over the measured members.

    ⛔ P IS EFFECTIVELY A TWO-BLOCK bd-VERSUS-inf PARTITION (view P's own
    firm_representation cell: mdpf_share_of_ones 0.00039, 19 symbols, 171 same-firm pairs,
    "MDPF SEPARATION IS UNMEASURABLE IN THIS ARM -- not merely small"). Any per-firm reading
    of a P row IS a bd-versus-inf reading and must say so rather than implying three-firm
    coverage. Its base rate 0.4904 is PRINTED BESIDE EVERY P ROW AT EVERY K, by that cell's
    own print_rule.
    """
    f = [firm_of[i] for i in ids]
    arr = np.array(f, dtype=object)
    return (arr[:, None] == arr[None, :]).astype(np.float64)


# --------------------------------------------------------------------------------------
# the firm-separation metric
# --------------------------------------------------------------------------------------

def firm_separation_auc(M: np.ndarray, firms: list, mask_measured: np.ndarray | None = None):
    """AUC that within-firm pairs outrank cross-firm pairs, ties credited 0.5.

    Returns (auc, n_within, n_cross, n_ties_at_the_decision). Rank AUC is NOT tie-invariant,
    which is why AC4's exact-zero integer travels beside every AUC this function produces --
    the same value can be reached by genuinely better ordering or by fewer ties, and the two
    are different findings.
    """
    n = len(firms)
    iu = np.triu_indices(n, k=1)
    vals = M[iu]
    a = np.asarray(firms, dtype=object)
    same = (a[iu[0]] == a[iu[1]])
    if mask_measured is not None:
        keep = mask_measured[iu[0]] & mask_measured[iu[1]]
        vals, same = vals[keep], same[keep]
    pos, neg = vals[same], vals[~same]
    if pos.size == 0 or neg.size == 0:
        return float("nan"), int(pos.size), int(neg.size), 0
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    ranks = np.empty(order.size, dtype=np.float64)
    srt = np.concatenate([pos, neg])[order]
    i = 0
    while i < srt.size:                      # average ranks within tie groups
        j = i
        while j + 1 < srt.size and srt[j + 1] == srt[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    rp = ranks[:pos.size].sum()
    auc = (rp - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size)
    ties = int(np.count_nonzero(np.isin(pos, neg)))
    return float(auc), int(pos.size), int(neg.size), ties


def permute_view(W: np.ndarray, seed: int) -> np.ndarray:
    """C2's complement: permute the ENTITY LABELS of a view, re-fuse, re-measure.

    The permuted object is the view's entity labelling -- not its values -- so the marginal
    distribution of affinities is preserved exactly and only the correspondence to entities is
    destroyed. A permutation that changed the value distribution would test a different
    hypothesis than the one the arm names.
    """
    rng = np.random.default_rng(seed)
    p = rng.permutation(W.shape[0])
    return W[np.ix_(p, p)]
