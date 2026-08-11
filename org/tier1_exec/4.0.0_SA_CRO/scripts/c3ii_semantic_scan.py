#!/usr/bin/env python3
"""COMPREHENSIVE C3.ii VERTICAL SCAN -- SEMANTIC (Potion/model2vec + BM25), not grep.
Andrew-direct: use the model2vec/Potion/BM25 machinery over all PRDs/docs (it came out rich), NOT grep.
Reuses org/modules/graph/potion/potion_embed.PotionEmbedder (data-not-code static embedder).
Per C3.ii vertical: query = name + its C3.i structure meanings (derived, not hand-typed) -> Potion cosine
rank over the PRD/docs corpus -> top-K relevant docs with scores. Ablate-don't-fuse (Potion + BM25 side
by side per CONTENT_MODULE_DESIGN); null-honest (report scores, a low top-score = thin coverage, declared).
"""
from __future__ import annotations

import glob
import math
import os
import re
import sys
from collections import Counter

WS = os.path.abspath(os.getcwd())  # run from the workspace root
if not os.path.isdir(os.path.join(WS, "org", "modules", "graph", "potion")):
    WS = os.path.abspath(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
sys.path.insert(0, os.path.abspath(os.path.join(WS, "org", "modules", "graph", "potion")))

import numpy as np  # noqa: E402
from potion_embed import load_embedder  # noqa: E402

# ---- 28 verticals -> C3.i structures (from comp-estate --matrix) ----
V2STRUCT = {
    "advi-bd": ["sys-bd-medallion"], "advi-cot": ["sys-cot-mdpf-assets"],
    "advi-inf": ["sys-inf-medallion", "sys-partner-serving-platform"],
    "canonical-schwab": ["UNASSIGNED-RESIDUE"], "causality": ["sys-causality-engine"],
    "ceo-digest": ["UNASSIGNED-RESIDUE"], "cma": ["sys-yang-analytics-engine"],
    "correlation": ["sys-yang-analytics-engine"], "data-refresh": ["sys-partner-serving-platform"],
    "etf-reports": ["UNASSIGNED-RESIDUE"], "factor-tilts": ["sys-yang-analytics-engine"],
    "graph-platform": ["sys-estate-ops-platform"], "insurance": ["sys-estate-ops-platform"],
    "opal-mcp": ["sys-estate-ops-platform"], "macroeconomics": ["sys-macro-data-engine", "sys-yang-analytics-engine"],
    "market-overview": ["sys-market-intelligence-engine", "sys-yang-analytics-engine"],
    "model-portfolios": ["sys-cot-mdpf-assets", "sys-partner-serving-platform"],
    "news": ["sys-news-intelligence-engine", "sys-market-intelligence-engine"],
    "ops-internal": ["sys-estate-ops-platform"], "partners": ["sys-partner-serving-platform"],
    "portal-infra": ["sys-partner-serving-platform"],
    "portfolio-management": ["sys-portfolio-management-suite", "sys-estate-ops-platform"],
    "positioning": ["sys-yang-analytics-engine"], "security-scanner": ["sys-estate-ops-platform"],
    "smartx": ["sys-smartx-feed"], "ticketing": ["UNASSIGNED-RESIDUE"],
    "trade-submission": ["sys-trade-submission-engine", "sys-portfolio-management-suite"],
    "valuation": ["sys-yang-analytics-engine"],
}


def load_struct_meanings():
    import yaml
    y = yaml.safe_load(open(os.path.join(WS, "org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml"), encoding="utf-8"))
    out = {}
    for k, v in (y.get("c3_deterministic_structures") or {}).items():
        out[k] = (v or {}).get("meaning", "")
    return out


def vertical_query(v, meanings):
    parts = [v.replace("-", " ")]
    for s in V2STRUCT.get(v, []):
        parts.append(s.replace("sys-", "").replace("-", " "))
        if meanings.get(s):
            parts.append(meanings[s])
    return " ; ".join(parts)


def load_corpus():
    docs = []
    for pat in ("docs/**/*.md", "org/projects/*.json"):
        for p in glob.glob(os.path.join(WS, pat), recursive=True):
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if not t.strip():
                continue
            rel = os.path.relpath(p, WS).replace("\\", "/")
            docs.append((rel, t[:8000]))   # Potion mean-pools; cap dilution
    return docs


# --- a small BM25 (query vs corpus) for the parallel axis (ablate, do not fuse) ---
_TOK = re.compile(r"[a-z0-9_]+")
def toks(s): return _TOK.findall(s.lower())
def bm25_rank(query, docs, k1=1.5, b=0.75):
    doc_toks = [toks(t) for _, t in docs]
    N = len(docs)
    avgdl = (sum(len(d) for d in doc_toks) / N) if N else 0
    df = Counter()
    for d in doc_toks:
        for w in set(d):
            df[w] += 1
    qt = set(toks(query))
    scores = []
    for d in doc_toks:
        tf = Counter(d)
        s = 0.0
        for w in qt:
            if w not in tf:
                continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * (tf[w] * (k1 + 1)) / (tf[w] + k1 * (1 - b + b * len(d) / (avgdl or 1)))
        scores.append(s)
    return scores


def main():
    emb = load_embedder()
    if emb is None:
        print("POTION UNAVAILABLE -- cannot run semantic scan (fail-safe returned None).")
        return
    meanings = load_struct_meanings()
    docs = load_corpus()
    print("Potion embedder loaded (dim=%d). Corpus: %d docs (docs/**/*.md + org/projects/*.json)." % (emb.dim, len(docs)))
    doc_vecs = emb.embed_many([t for _, t in docs])
    print("=" * 100)
    for v in sorted(V2STRUCT):
        q = vertical_query(v, meanings)
        qv = emb.embed(q)
        cos = [float(np.dot(qv, doc_vecs[i])) for i in range(len(docs))]
        bm = bm25_rank(q, docs)
        top_sem = sorted(range(len(docs)), key=lambda i: cos[i], reverse=True)[:4]
        top_bm = sorted(range(len(docs)), key=lambda i: bm[i], reverse=True)[:2]
        print("\n### %s   (structures: %s)" % (v, ", ".join(V2STRUCT[v])))
        print("    top SEMANTIC (Potion cosine):")
        for i in top_sem:
            print("       %.3f  %s" % (cos[i], docs[i][0]))
        print("    top LEXICAL (BM25):")
        for i in top_bm:
            print("       %.2f   %s" % (bm[i], docs[i][0]))


if __name__ == "__main__":
    main()
