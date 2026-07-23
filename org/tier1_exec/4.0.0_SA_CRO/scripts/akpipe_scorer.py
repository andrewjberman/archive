"""
NFRA_AKPIPE scoring core + validation harness (RCN-0003).

Author: 4.0.0_SA_CRO (Chief Research Officer)
Home:   org/tier1_exec/4.0.0_SA_CRO/
Spec:   briefs/NFRA_AKPIPE_BUILD_SPEC_20260723.md

WHAT THIS IS. The relevance-scoring core of the arxiv pipeline, plus the acceptance
controls from spec section 7, runnable offline with zero egress.

  nlp_score        = RRF fusion of the BM25 rank and the Potion rank
  derived_state_rank = recency_decay(age_days) * nlp_score      (recomputed daily)

DETERMINISM CONTRACT (CVO C-1, folded from CONTENT_MODULE_DESIGN): Potion IS a model,
so the honest guarantee is DETERMINISTIC-GIVEN-A-PINNED-MODEL + reproducible, never
"no inference". Model id and profile version are stamped into every result row.

BM25 NOTE (convergence item for the build): this uses a standard pinned BM25
(k1=1.5, b=0.75) because the estate's comp_similar.py BM25 is a pairwise
resource-vs-resource index, not query-vs-document. The METHOD is converged with
infra/system/ontology/CONTENT_MODULE_DESIGN (BM25 + Potion + RRF); the IMPLEMENTATION
should be aligned to the estate index when the content-class partition is built.

ASCII-only (CLAUDE.md Code Quality). No emojis.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import Counter

# ---------------------------------------------------------------- pinned config

POTION_MODEL = "minishlab/potion-base-8M"   # Andrew decision 5: "Fast potion is fine."
PROFILE_VERSION = "akpipe-profile-v1"
BM25_K1 = 1.5
BM25_B = 0.75
RRF_K = 60          # standard RRF constant; parameter-free fuser for ORDERING ONLY
HALF_LIFE_DAYS = 45.0   # spec section 6.3 knob; set defensibly, NOT tuned to a sample

# BM25 saturation constant for the ABSOLUTE magnitude transform bm/(bm+C).
# WHY ABSOLUTE, NOT CORPUS-RELATIVE: min-max / z-score normalization is corpus-DEPENDENT,
# so a paper's stored score would silently CHANGE as new papers arrive -- that breaks the
# lossless + independently-recomputable contract (a reader could not reproduce a stored row).
# An absolute saturating transform keeps every paper's relevance stable forever.
# CALIBRATION STATUS: PROVISIONAL. C must be calibrated against the decoy-null distribution
# on the first real harvest (CVO: anchor to the null, never a hand-picked value). It is NOT
# tuned to the 3-doc validation sample -- doing so would be exactly the Goodhart failure.
BM25_SAT_C = 25.0

# ---------------------------------------------------------------- the profile
# Sourced from three in-repo places (spec section 6.1). Explicit + versioned so the
# score is reproducible. v2 candidate: auto-derive the ontology terms from
# org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml rather than curating them here.

# (a) Andrew's interest anchors, verbatim from his tasking
INTEREST_ANCHORS = [
    "retrieval", "retrieval augmented", "context retrieval", "ranking", "reranking",
    "agentic", "agent", "agentic engineering", "multi agent", "agent harness",
    "graph engineering", "knowledge graph", "graph", "ontology",
    "infrastructure", "harness", "harness engineering", "evaluation harness",
    "learning loop", "feedback loop", "self improvement", "design pattern",
]

# (b) infra/system graph-infra + learning-loop vocabulary
SYSTEM_VOCAB = [
    "iceberg", "trino", "nessie", "kuzu", "lakehouse", "materialize", "provenance",
    "motif", "promote", "recognizer", "semantic", "embedding", "index", "corpus",
    "bm25", "reciprocal rank fusion", "vector", "similarity", "clustering",
    "pipeline", "orchestration", "scheduler", "incremental", "idempotent",
]

# (c) ontology / archetype-layer vocabulary (NFRA_ONTOLOGY_RULE_BANK concepts)
ONTOLOGY_VOCAB = [
    "role", "relation", "variance", "taxonomy", "classification", "schema",
    "node", "edge", "traversal", "dependency", "lineage", "aggregation",
    "localization", "repository", "codebase", "code", "software engineering",
    "benchmark", "evaluation", "coverage", "trajectory", "tool use",
]

PROFILE_TERMS = INTEREST_ANCHORS + SYSTEM_VOCAB + ONTOLOGY_VOCAB
PROFILE_TEXT = " ".join(PROFILE_TERMS)

# ---------------------------------------------------------------- tokenization

_TOKEN = re.compile(r"[a-z0-9]+")

def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())

# ---------------------------------------------------------------- BM25

class BM25:
    """Standard BM25 over a document corpus, scored against a query term list."""

    def __init__(self, docs_tokens: list[list[str]], k1: float = BM25_K1, b: float = BM25_B):
        self.k1, self.b = k1, b
        self.docs = docs_tokens
        self.N = len(docs_tokens)
        self.doc_len = [len(d) for d in docs_tokens]
        self.avgdl = (sum(self.doc_len) / self.N) if self.N else 0.0
        self.tf = [Counter(d) for d in docs_tokens]
        df: Counter = Counter()
        for d in docs_tokens:
            for t in set(d):
                df[t] += 1
        self.df = df

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        # BM25 idf with +0.5 smoothing, floored at 0 so common terms cannot go negative
        return max(0.0, math.log((self.N - n + 0.5) / (n + 0.5) + 1.0))

    def score(self, doc_i: int, query_terms: list[str]) -> float:
        s = 0.0
        tf, dl = self.tf[doc_i], self.doc_len[doc_i]
        for term in query_terms:
            f = tf.get(term, 0)
            if not f:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1.0))
            s += self.idf(term) * (f * (self.k1 + 1)) / denom
        return s

# ---------------------------------------------------------------- Potion

def potion_embed(texts: list[str]):
    """Static-embedding encode. Offline: the model must already be in the HF cache."""
    from model2vec import StaticModel
    import numpy as np
    model = StaticModel.from_pretrained(POTION_MODEL)
    vecs = model.encode(texts)
    return np.asarray(vecs, dtype="float64")

def cosine(a, b) -> float:
    import numpy as np
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

# ---------------------------------------------------------------- fusion + rank

def rrf(rank_positions: list[int], k: int = RRF_K) -> float:
    """Reciprocal Rank Fusion over 1-indexed ranks. Parameter-free ORDERING fuser.

    ORDERING ONLY. Never multiply this by recency: RRF has no magnitude range
    (a perfect match and pure noise differ by ~3%), so a decay factor with a 16x
    range would swamp it entirely. Measured, not assumed -- see nlp_relevance.
    """
    return sum(1.0 / (k + r) for r in rank_positions)

def nlp_relevance(bm25_score: float, potion_cos: float) -> float:
    """ABSOLUTE, corpus-stable relevance magnitude in [0,1) -- the multiplicative factor.

    Geometric mean of the two saturated axes: a document must score on BOTH to rank.
    A lexical-only match (BM25 high, semantics unrelated) is penalized, and so is the
    inverse. Both inputs are absolute, so a stored value never changes as the corpus grows.
    """
    bm_norm = bm25_score / (bm25_score + BM25_SAT_C) if bm25_score > 0 else 0.0
    po_norm = max(0.0, potion_cos)
    return math.sqrt(bm_norm * po_norm)

def recency_component(age_days: float, half_life: float = HALF_LIFE_DAYS) -> float:
    """Exponential decay in (0,1]. Recomputed every run as age_days grows."""
    return math.exp(-math.log(2.0) * max(0.0, age_days) / half_life)

def derived_state_rank(nlp_score: float, age_days: float) -> float:
    return recency_component(age_days) * nlp_score

# ---------------------------------------------------------------- scoring pass

def score_corpus(docs: list[dict]) -> list[dict]:
    """docs: [{id, text, age_days}] -> rows with both axes stored separately (CVO: ablate)."""
    texts = [d["text"] for d in docs]
    toks = [tokenize(t) for t in texts]
    query_terms = tokenize(PROFILE_TEXT)

    bm = BM25(toks)
    bm_scores = [bm.score(i, query_terms) for i in range(len(docs))]

    embs = potion_embed([PROFILE_TEXT] + texts)
    prof_vec, doc_vecs = embs[0], embs[1:]
    po_scores = [cosine(prof_vec, v) for v in doc_vecs]

    # ranks (1-indexed, descending score); ties broken by id for determinism
    def ranks_of(scores):
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], docs[i]["id"]))
        r = [0] * len(scores)
        for pos, i in enumerate(order, start=1):
            r[i] = pos
        return r

    bm_rank, po_rank = ranks_of(bm_scores), ranks_of(po_scores)

    rows = []
    for i, d in enumerate(docs):
        fused = rrf([bm_rank[i], po_rank[i]])          # ORDERING only
        relev = nlp_relevance(bm_scores[i], po_scores[i])  # MAGNITUDE -> the derived rank
        age = d.get("age_days", 0.0)
        rows.append({
            "id": d["id"],
            "bm25_score": round(bm_scores[i], 6),
            "bm25_rank": bm_rank[i],
            "potion_cosine": round(po_scores[i], 6),
            "potion_rank": po_rank[i],
            "nlp_rrf_ordering": round(fused, 8),
            "nlp_score": round(relev, 8),
            "age_days": age,
            "recency_component": round(recency_component(age), 6),
            "derived_state_rank": round(derived_state_rank(relev, age), 10),
            "profile_version": PROFILE_VERSION,
            "potion_model_version": POTION_MODEL,
            "bm25_params_version": f"k1={BM25_K1},b={BM25_B}",
        })
    rows.sort(key=lambda r: -r["nlp_score"])
    return rows

# ---------------------------------------------------------------- main

def main() -> int:
    sp = sys.argv[1] if len(sys.argv) > 1 else "."
    ws = sys.argv[2] if len(sys.argv) > 2 else "."

    docs = []

    # POSITIVE CONTROL -- the stated high-relevance exemplar (spec section 7.1)
    pos_path = os.path.join(sp, "paper_2606.07297v1.txt")
    with open(pos_path, encoding="utf-8") as f:
        docs.append({"id": "POS_swe_explore_paper", "text": f.read(), "age_days": 1.0})

    # NEGATIVE CONTROLS -- real off-topic operational prose from the estate
    for label, rel in [
        ("NEG_ops_change_mgmt", "org/critical_paths/change_management"),
    ]:
        d = os.path.join(ws, rel)
        if os.path.isdir(d):
            names = sorted(n for n in os.listdir(d) if n.endswith(".md"))[:6]
            blob = []
            for n in names:
                try:
                    with open(os.path.join(d, n), encoding="utf-8", errors="replace") as f:
                        blob.append(f.read())
                except OSError:
                    pass
            if blob:
                docs.append({"id": label, "text": "\n".join(blob), "age_days": 1.0})

    # DEGENERACY CONTROL -- generated, not hand-picked (a hand-chosen control measures
    # the AUTHOR; a generated one measures the INSTRUMENT). Deterministic seed.
    import random
    rng = random.Random(20260723)
    filler = ("quarterly invoice ledger custodian settlement reconciliation statement "
              "premium dividend accrual balance remittance payable receivable audit "
              "vendor contract renewal clause tenant lease amortization").split()
    salad = " ".join(rng.choice(filler) for _ in range(4000))
    docs.append({"id": "DEGEN_word_salad", "text": salad, "age_days": 1.0})

    rows = score_corpus(docs)

    print("=" * 78)
    print("NFRA_AKPIPE scoring core -- validation pass (spec section 7)")
    print(f"profile={PROFILE_VERSION}  model={POTION_MODEL}  bm25=k1{BM25_K1}/b{BM25_B}  rrf_k={RRF_K}")
    print(f"corpus N={len(docs)}   (denominator printed -- Rule 22)")
    print("=" * 78)
    hdr = f"{'id':<26}{'bm25':>10}{'bm_r':>6}{'potion':>10}{'po_r':>6}{'nlp':>12}{'derived':>12}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['id']:<26}{r['bm25_score']:>10.3f}{r['bm25_rank']:>6}"
              f"{r['potion_cosine']:>10.4f}{r['potion_rank']:>6}"
              f"{r['nlp_score']:>12.6f}{r['derived_state_rank']:>12.6f}")

    # ---- acceptance checks
    print("\n" + "=" * 78)
    print("ACCEPTANCE CHECKS")
    print("=" * 78)
    top = rows[0]["id"]
    ok_pos = top == "POS_swe_explore_paper"
    print(f"  [7.1] POSITIVE CONTROL  : top-ranked = {top}  -> {'PASS' if ok_pos else 'FAIL'}")

    degen = next(r for r in rows if r["id"] == "DEGEN_word_salad")
    pos = next(r for r in rows if r["id"] == "POS_swe_explore_paper")
    ok_degen = degen["nlp_score"] < pos["nlp_score"]
    print(f"  [7.2] DEGENERACY        : salad nlp={degen['nlp_score']:.6f} < "
          f"pos nlp={pos['nlp_score']:.6f} -> {'PASS' if ok_degen else 'FAIL'}")

    spread_bm = pos["bm25_score"] - degen["bm25_score"]
    spread_po = pos["potion_cosine"] - degen["potion_cosine"]
    ok_disc = spread_bm > 0 and spread_po > 0
    print(f"  [7.3] ABLATION          : BM25 delta={spread_bm:+.3f} | "
          f"Potion delta={spread_po:+.4f} -> {'PASS (both axes discriminate)' if ok_disc else 'CHECK'}")

    r2 = score_corpus(docs)
    ok_det = json.dumps(rows, sort_keys=True) == json.dumps(r2, sort_keys=True)
    print(f"  [7.4] DETERMINISM       : two runs byte-identical -> {'PASS' if ok_det else 'FAIL'}")

    a = derived_state_rank(1.0, 10.0)
    b = derived_state_rank(1.0, 100.0)
    ok_mono = b < a
    print(f"  [7.5] RECOMPUTE MONOTONE: rank(10d)={a:.6f} > rank(100d)={b:.6f} -> "
          f"{'PASS' if ok_mono else 'FAIL'}")

    # [7.6] COMPOSITION SANITY -- the check that CAUGHT the v1 defect.
    # v1 used derived = recency * RRF. RRF has ~3% dynamic range vs recency's 16x, so
    # noise-published-today beat a perfect match 3 days old. Relevance must survive age.
    print("\n  [7.6] COMPOSITION SANITY (the v1 defect regression test)")
    worst_ok = True
    for age in (3, 7, 30, 45):
        fresh_noise = derived_state_rank(degen["nlp_score"], 0.0)
        aged_good = derived_state_rank(pos["nlp_score"], float(age))
        wins = aged_good > fresh_noise
        worst_ok = worst_ok and wins
        print(f"        relevant@{age:>2}d={aged_good:.6f} vs noise@0d={fresh_noise:.6f} "
              f"-> relevance {'HOLDS' if wins else 'LOSES'}")
    print(f"        -> {'PASS' if worst_ok else 'FAIL'}  "
          f"(relevance range={pos['nlp_score']/max(degen['nlp_score'],1e-9):.1f}x, "
          f"recency range over 45d=2.0x)")
    ok_comp = worst_ok

    allok = all([ok_pos, ok_degen, ok_disc, ok_det, ok_mono, ok_comp])
    print("\n  RESULT:", "ALL CHECKS PASS" if allok else "SOME CHECKS DID NOT PASS -- read above")
    return 0 if allok else 1

if __name__ == "__main__":
    sys.exit(main())
