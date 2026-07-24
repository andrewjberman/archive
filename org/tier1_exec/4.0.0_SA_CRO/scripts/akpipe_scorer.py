"""
NFRA_AKPIPE scoring core + validation harness (RCN-0003).

Author: 4.0.0_SA_CRO (Chief Research Officer)
Home:   org/tier1_exec/4.0.0_SA_CRO/
Spec:   briefs/NFRA_AKPIPE_BUILD_SPEC_20260723.md

WHAT THIS IS. The relevance-scoring core of the arxiv pipeline, plus the acceptance
controls (spec section 7), runnable offline with zero egress.

  nlp_score          = ABSOLUTE phrase-BM25 magnitude in [0,1)  (the multiplicand)
  nlp_rrf_ordering   = RRF of the BM25 and Potion ranks         (ORDERING diagnostic only)
  derived_state_rank = recency_decay(age_days) * nlp_score      (recomputed daily)

v2 (2026-07-24) -- five fixes measured on the first real harvest:
  1. PHRASE profile, not generic tokens. "graph"/"code"/"agent" alone matched every CS
     paper; the signal is in SPECIFIC PHRASES ("knowledge graph", "retrieval augmented",
     "code localization"). The curated phrase set IS the judgment; corpus idf weights
     specificity objectively on top.
  2. LENGTH neutralized -- phrase-BM25 with length normalization (b), and phrases are rare
     enough that raw-length bias collapses (measured in the harvest report).
  3. Potion put on the RECOVERY BAR: it is measured, not assumed. v1 measured Potion CV
     0.165 vs BM25 0.845 -- near-constant within CS. So the RANK is phrase-BM25; potion_cosine
     is kept as a stored component + a floor guard, and the harvest reports whether Potion
     recovers any BM25-missed paper (CONTENT_MODULE_DESIGN section 8 recovery bar).
  4/5. scope filter + back-window live in the harvest client, not here.

DETERMINISM CONTRACT (CVO C-1): Potion IS a model, so the honest guarantee is
DETERMINISTIC-GIVEN-A-PINNED-MODEL + reproducible. Model id + profile version stamped in.

IDF STABILITY NOTE (production item): idf here is computed over the SCORED corpus, which
makes a score corpus-dependent -- fine for a dev ranking pass, but the PRODUCTION store must
pin idf to a versioned reference corpus (part of profile_version) so a stored paper's score
never changes as new papers arrive (the lossless + recomputable contract). Flagged in the spec.

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
PROFILE_VERSION = "akpipe-profile-v3"
BM25_K1 = 1.5
BM25_B = 0.75
RRF_K = 60
HALF_LIFE_DAYS = 45.0
# Absolute saturation constant for bm/(bm+C). PROVISIONAL -- calibrate against the decoy null
# on a real harvest, NOT tuned to a sample. Phrase-BM25 magnitudes are smaller than token-BM25,
# so C is lower than v1's 25.
BM25_SAT_C = 6.0

# ---------------------------------------------------------------- the phrase profile
# Curated from Andrew's stated interests (retrieval, agentic engineering, graph engineering,
# infrastructure, harness engineering, learning-loop design patterns) + the SWE-Explore
# fingerprint. Every entry is a SPECIFIC phrase; generic single tokens are deliberately absent.
# The curation is the judgment; corpus idf weights specificity on top. v3 candidate: derive the
# ontology-side phrases from NFRA_ONTOLOGY_RULE_BANK.yaml rather than curating them.

PROFILE_PHRASES = [
    # retrieval
    "retrieval augmented generation", "retrieval augmented", "dense retrieval", "sparse retrieval",
    "semantic search", "reranking", "re ranking", "reciprocal rank fusion", "vector database",
    "vector search", "nearest neighbor", "context retrieval", "passage retrieval",
    "document retrieval", "query expansion", "hybrid retrieval", "graph rag", "retrieval pipeline",
    "learned sparse", "late interaction",
    # agentic engineering
    "agentic", "agentic workflow", "agent framework", "multi agent", "tool use", "tool calling",
    "function calling", "autonomous agent", "agent orchestration", "planning agent",
    "self evolving", "self improving", "closed loop", "memory augmented", "experience reuse",
    "language agent", "agent trajectory", "long horizon",
    # graph engineering
    "knowledge graph", "graph neural network", "graph database", "node embedding",
    "link prediction", "graph traversal", "ontology", "entity linking", "graph construction",
    "temporal graph", "property graph", "graph learning", "graph retrieval",
    # infrastructure / harness engineering
    "evaluation harness", "training pipeline", "data pipeline", "distributed training",
    "inference server", "vector index", "feature store", "test time", "scaffold",
    "serving system", "model serving", "orchestration framework",
    # learning-loop design patterns
    "learning loop", "feedback loop", "reinforcement learning", "curriculum learning",
    "self play", "online learning", "active learning", "continual learning", "reward model",
    "preference optimization", "self correction", "iterative refinement",
    # code / SWE agents (the SWE-Explore fingerprint)
    "code generation", "code localization", "repository level", "software engineering agent",
    "bug localization", "program repair", "code retrieval", "issue resolution", "code search",
    "repository understanding",
]

# a plain-text rendering of the profile for the Potion (semantic) axis
PROFILE_TEXT = " ".join(PROFILE_PHRASES)

# ---------------------------------------------------------------- tokenization

_TOKEN = re.compile(r"[a-z0-9]+")
_SEP = re.compile(r"[-‐‑‒–—_/]+")
_WSX = re.compile(r"\s+")

def normalize(text: str) -> str:
    """Lowercase + fold hyphens/dashes/underscores/slashes to spaces + collapse whitespace.

    NOT cosmetic -- this fixes a MEASURED false-negative class. "closed-loop" did not match
    the phrase "closed loop", so CLARK (Closed-loop Learning over Knowledge Graphs) -- a
    bullseye for the brief -- scored EXACTLY 0.0. Academic titles hyphenate constantly.
    """
    return _WSX.sub(" ", _SEP.sub(" ", text.lower()))

def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(normalize(text))

# ---------------------------------------------------------------- phrase BM25

class PhraseIndex:
    """BM25 over a fixed set of PHRASES (not free tokens), length-normalized, with idf
    computed across the scored corpus. Down-weights phrases common in the corpus and
    up-weights rare specific ones -- discrimination WITHIN a corpus of CS papers."""

    def __init__(self, docs_text: list[str], phrases: list[str] = None,
                 k1: float = BM25_K1, b: float = BM25_B):
        self.phrases = phrases or PROFILE_PHRASES
        self.k1, self.b = k1, b
        # Plural-tolerant on the FINAL word: "knowledge graph" must match "knowledge graphs".
        # \b after "graph" fails on "graphs", which silently zeroed perfect-match papers.
        self.pats = {p: re.compile(r"\b" + re.escape(normalize(p)) + r"(?:s|es)?\b")
                     for p in self.phrases}
        lowered = [normalize(t) for t in docs_text]
        self.doc_len = [max(1, len(tokenize(t))) for t in docs_text]
        self.N = len(docs_text)
        self.avgdl = (sum(self.doc_len) / self.N) if self.N else 1.0
        self.tf = [{p: len(self.pats[p].findall(dl)) for p in self.phrases} for dl in lowered]
        df: Counter = Counter()
        for tfd in self.tf:
            for p, c in tfd.items():
                if c > 0:
                    df[p] += 1
        self.df = df

    def idf(self, phrase: str) -> float:
        n = self.df.get(phrase, 0)
        return max(0.0, math.log((self.N - n + 0.5) / (n + 0.5) + 1.0))

    def score(self, doc_i: int) -> float:
        s = 0.0
        dl = self.doc_len[doc_i]
        tfd = self.tf[doc_i]
        for p in self.phrases:
            f = tfd[p]
            if not f:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1.0))
            s += self.idf(p) * (f * (self.k1 + 1)) / denom
        return s

    def phrase_hits(self, doc_i: int) -> list[str]:
        return [p for p in self.phrases if self.tf[doc_i][p] > 0]

# ---------------------------------------------------------------- Potion (semantic axis)

def potion_embed(texts: list[str]):
    """Static-embedding encode. Offline: the model must already be in the HF cache."""
    from model2vec import StaticModel
    import numpy as np
    model = StaticModel.from_pretrained(POTION_MODEL)
    return np.asarray(model.encode(texts), dtype="float64")

def cosine(a, b) -> float:
    import numpy as np
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

# ---------------------------------------------------------------- magnitude + fusion + recency

def bm25_magnitude(phrase_bm25: float) -> float:
    """Absolute, corpus-stable magnitude in [0,1). Multiplicand for the derived rank."""
    return phrase_bm25 / (phrase_bm25 + BM25_SAT_C) if phrase_bm25 > 0 else 0.0

def rrf(rank_positions: list[int], k: int = RRF_K) -> float:
    """Reciprocal Rank Fusion. ORDERING diagnostic ONLY -- never a multiplicand (v1 defect)."""
    return sum(1.0 / (k + r) for r in rank_positions)

def recency_component(age_days: float, half_life: float = HALF_LIFE_DAYS) -> float:
    return math.exp(-math.log(2.0) * max(0.0, age_days) / half_life)

def derived_state_rank(nlp_score: float, age_days: float) -> float:
    return recency_component(age_days) * nlp_score

# ---------------------------------------------------------------- scoring pass

def score_corpus(docs: list[dict]) -> list[dict]:
    """docs: [{id, text, age_days}] -> rows. RANK = phrase-BM25 magnitude; Potion stored."""
    texts = [d["text"] for d in docs]
    idx = PhraseIndex(texts)
    bm_scores = [idx.score(i) for i in range(len(docs))]

    embs = potion_embed([PROFILE_TEXT] + texts)
    prof_vec, doc_vecs = embs[0], embs[1:]
    po_scores = [cosine(prof_vec, v) for v in doc_vecs]

    def ranks_of(scores):
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], docs[i]["id"]))
        r = [0] * len(scores)
        for pos, i in enumerate(order, start=1):
            r[i] = pos
        return r

    bm_rank, po_rank = ranks_of(bm_scores), ranks_of(po_scores)

    rows = []
    for i, d in enumerate(docs):
        rel = bm25_magnitude(bm_scores[i])
        age = d.get("age_days", 0.0)
        rows.append({
            "id": d["id"],
            "phrase_bm25": round(bm_scores[i], 6),
            "bm25_rank": bm_rank[i],
            "potion_cosine": round(po_scores[i], 6),
            "potion_rank": po_rank[i],
            "nlp_rrf_ordering": round(rrf([bm_rank[i], po_rank[i]]), 8),
            "nlp_score": round(rel, 8),
            "age_days": age,
            "recency_component": round(recency_component(age), 6),
            "derived_state_rank": round(derived_state_rank(rel, age), 10),
            "phrase_hits": idx.phrase_hits(i),
            "profile_version": PROFILE_VERSION,
            "potion_model_version": POTION_MODEL,
            "bm25_params_version": f"k1={BM25_K1},b={BM25_B},C={BM25_SAT_C}",
        })
    rows.sort(key=lambda r: -r["nlp_score"])
    return rows

# ---------------------------------------------------------------- validation main

def main() -> int:
    sp = sys.argv[1] if len(sys.argv) > 1 else "."
    ws = sys.argv[2] if len(sys.argv) > 2 else "."

    docs = []
    with open(os.path.join(sp, "paper_2606.07297v1.txt"), encoding="utf-8") as f:
        docs.append({"id": "POS_swe_explore_paper", "text": f.read(), "age_days": 1.0})

    d = os.path.join(ws, "org/critical_paths/change_management")
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
            docs.append({"id": "NEG_ops_change_mgmt", "text": "\n".join(blob), "age_days": 1.0})

    import random
    rng = random.Random(20260723)
    filler = ("quarterly invoice ledger custodian settlement reconciliation statement premium "
              "dividend accrual balance remittance payable receivable audit vendor contract "
              "renewal clause tenant lease amortization").split()
    docs.append({"id": "DEGEN_word_salad",
                 "text": " ".join(rng.choice(filler) for _ in range(4000)), "age_days": 1.0})

    rows = score_corpus(docs)

    print("=" * 82)
    print("NFRA_AKPIPE scoring core -- validation pass (spec section 7)")
    print(f"profile={PROFILE_VERSION} ({len(PROFILE_PHRASES)} phrases)  model={POTION_MODEL}  "
          f"bm25=k1{BM25_K1}/b{BM25_B}/C{BM25_SAT_C}")
    print(f"corpus N={len(docs)}   (denominator printed -- Rule 22)")
    print("=" * 82)
    hdr = f"{'id':<26}{'ph_bm25':>10}{'bm_r':>6}{'potion':>10}{'po_r':>6}{'nlp':>10}{'derived':>10}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['id']:<26}{r['phrase_bm25']:>10.3f}{r['bm25_rank']:>6}"
              f"{r['potion_cosine']:>10.4f}{r['potion_rank']:>6}"
              f"{r['nlp_score']:>10.4f}{r['derived_state_rank']:>10.4f}")

    print("\n" + "=" * 82 + "\nACCEPTANCE CHECKS\n" + "=" * 82)
    pos = next(r for r in rows if r["id"] == "POS_swe_explore_paper")
    degen = next(r for r in rows if r["id"] == "DEGEN_word_salad")

    ok_pos = rows[0]["id"] == "POS_swe_explore_paper"
    print(f"  [7.1] POSITIVE CONTROL  : top = {rows[0]['id']} -> {'PASS' if ok_pos else 'FAIL'} "
          f"({len(pos['phrase_hits'])} profile phrases hit)")
    ok_degen = degen["nlp_score"] < pos["nlp_score"]
    print(f"  [7.2] DEGENERACY        : salad nlp={degen['nlp_score']:.4f} < pos={pos['nlp_score']:.4f} "
          f"-> {'PASS' if ok_degen else 'FAIL'}")
    ok_disc = (pos["phrase_bm25"] - degen["phrase_bm25"]) > 0
    print(f"  [7.3] ABLATION          : phrase-BM25 delta={pos['phrase_bm25']-degen['phrase_bm25']:+.3f} | "
          f"Potion delta={pos['potion_cosine']-degen['potion_cosine']:+.4f} -> {'PASS' if ok_disc else 'CHECK'}")
    ok_det = json.dumps(rows, sort_keys=True) == json.dumps(score_corpus(docs), sort_keys=True)
    print(f"  [7.4] DETERMINISM       : two runs byte-identical -> {'PASS' if ok_det else 'FAIL'}")
    a, b = derived_state_rank(1.0, 10.0), derived_state_rank(1.0, 100.0)
    ok_mono = b < a
    print(f"  [7.5] RECOMPUTE MONOTONE: rank(10d)={a:.4f} > rank(100d)={b:.4f} -> {'PASS' if ok_mono else 'FAIL'}")

    ok_comp = True
    print("  [7.6] COMPOSITION SANITY (v1 defect regression):")
    for age in (3, 7, 30, 45):
        good = derived_state_rank(pos["nlp_score"], float(age))
        noise = derived_state_rank(degen["nlp_score"], 0.0)
        ok_comp = ok_comp and good > noise
        print(f"        relevant@{age:>2}d={good:.4f} vs noise@0d={noise:.4f} -> "
              f"{'HOLDS' if good > noise else 'LOSES'}")

    allok = all([ok_pos, ok_degen, ok_disc, ok_det, ok_mono, ok_comp])
    print("\n  RESULT:", "ALL CHECKS PASS" if allok else "SOME CHECKS DID NOT PASS")
    return 0 if allok else 1

if __name__ == "__main__":
    sys.exit(main())
