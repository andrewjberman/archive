#!/usr/bin/env python3
"""C3.ii SEMANTIC VERTICAL SCAN v2 -- HARDENED (null-gated, enriched, logs-extended).
Hardening per C3II_COMPREHENSIVE_SEMANTIC_COVERAGE_SCAN_20260811.md s.4 (Andrew: "harden this
scan then wire it into the calls"):
  1. NULL-ANCHORED DECOY GATE adopted from the estate's own design
     (infra/system/ontology/content_relate_prototype.py iter-2/iter-3): pooled Monte-Carlo decoy
     null (M seeded draws), family-wise threshold = quantile(1 - ALPHA/N_docs) of the pooled null
     -- expected false admits per vertical stays ALPHA independent of corpus size. Decoy queries
     are frequency-weighted random token draws from the corpus stream, length-matched to the real
     query (the retrieval analogue of the prototype's token-shuffle decoy corpora).
  2. QUERY ENRICHMENT: name + C3.i structure meanings (v1) + the vertical's resolver row --
     served-artifact LEAF names (baked prose stripped -- the B9 defect class must not enter the
     query) + producer function names. All DERIVED, nothing hand-typed.
  3. CORPUS EXTENDED to logs, PLANE-LABELED: docs / projects / logs reported separately --
     a hit in a log and a hit in a PRD mean different things; one pooled rank would hide that.
Axes stay ABLATED (Potion cosine + BM25 side by side, never fused -- RRF is corpus-invariant and
cannot gate, the prototype's iter-1 finding). Emits the JSON wiring artifact the friction/state
calls consume.
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict

WS = os.path.abspath(os.getcwd())
if not os.path.isdir(os.path.join(WS, "org", "modules", "graph", "potion")):
    WS = os.path.abspath(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
sys.path.insert(0, os.path.abspath(os.path.join(WS, "org", "modules", "graph", "potion")))

import numpy as np  # noqa: E402
from potion_embed import load_embedder  # noqa: E402

NULL_ALPHA = 0.05   # expected false-admit DOCS per vertical per axis (family-wise, prototype law)
NULL_M = 25         # pooled decoy draws (prototype iter-2 stability)
TOP_DISPLAY = 5     # display cap per plane; admission is by the gate, not this cap

# 28 ratified verticals -> C3.i structures (comp-estate --matrix; mdpf merged into model-portfolios
# per Andrew 08-07 -- the resolver still carries mdpf rows separately, declared roster drift).
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
# vertical -> resolver named_thread aliases (declared, not silent): opal-mcp's resolver row is
# m365-mcp; model-portfolios also pulls the mdpf rows (roster drift: merge not yet propagated).
VERT_THREAD_ALIASES = {"opal-mcp": ["m365-mcp"], "model-portfolios": ["model-portfolios", "mdpf"]}

_PROSE = re.compile(r"\s*\([^)]*\)\s*$")   # strip baked '(LastMod ...)' / '(243783B, fresh ...)'
_TOK = re.compile(r"[a-z0-9_]+")


def toks(s: str) -> list:
    return _TOK.findall(s.lower())


def load_struct_meanings() -> dict:
    import yaml
    y = yaml.safe_load(open(os.path.join(WS, "org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml"),
                            encoding="utf-8"))
    return {k: (v or {}).get("meaning", "") for k, v in (y.get("c3_deterministic_structures") or {}).items()}


def load_resolver_enrichment() -> dict:
    r = json.load(open(os.path.join(WS, "org/modules/graph/estate-coverage-resolver.json"), encoding="utf-8"))
    by_name = defaultdict(lambda: {"served": [], "producers": []})
    for t in r.get("threads", []):
        n = t.get("named_thread")
        if not n:
            continue
        for a in (t.get("served_artifacts") or []):
            leaf = _PROSE.sub("", str(a)).rstrip("/").split("/")[-1]
            if leaf:
                by_name[n]["served"].append(leaf)
        for p in (t.get("producers") or []):
            if isinstance(p, str) and p.strip():
                by_name[n]["producers"].append(p.split()[0].split("(")[0])
    return dict(by_name)


def vertical_query(v: str, meanings: dict, enrich: dict) -> str:
    parts = [v.replace("-", " ")]
    for s in V2STRUCT.get(v, []):
        parts.append(s.replace("sys-", "").replace("-", " "))
        if meanings.get(s):
            parts.append(meanings[s])
    for thread in VERT_THREAD_ALIASES.get(v, [v]):
        e = enrich.get(thread)
        if not e:
            continue
        leaves = sorted(set(e["served"]))[:20]
        prods = sorted(set(e["producers"]))[:20]
        if leaves:
            parts.append("serves " + " ".join(x.replace("_", " ").replace("-", " ").replace(".json", "")
                                              for x in leaves))
        if prods:
            parts.append("producers " + " ".join(x.replace("_", " ").replace("-", " ") for x in prods))
    return " ; ".join(parts)


def load_corpus() -> list:
    planes = (("docs", "docs/**/*.md"), ("projects", "org/projects/*.json"),
              ("logs", "org/**/logs/**/*.md"))
    out, seen = [], set()
    for plane, pat in planes:
        for p in glob.glob(os.path.join(WS, pat), recursive=True):
            rel = os.path.relpath(p, WS).replace("\\", "/")
            if rel in seen:
                continue
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if not t.strip():
                continue
            seen.add(rel)
            out.append((rel, plane, t[:8000]))
    return out


class BM25Index:
    """Inverted-index BM25 (query-time O(sum df(term)), not O(N*|q|)) -- 728 queries need it."""

    def __init__(self, docs: list, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.N = len(docs)
        self.doclen = np.zeros(self.N)
        self.post = defaultdict(list)
        for i, (_, _, t) in enumerate(docs):
            tf = Counter(toks(t))
            self.doclen[i] = sum(tf.values())
            for w, c in tf.items():
                self.post[w].append((i, c))
        self.avgdl = float(self.doclen.mean()) if self.N else 1.0

    def score(self, query_tokens: set) -> np.ndarray:
        s = np.zeros(self.N)
        for w in query_tokens:
            plist = self.post.get(w)
            if not plist:
                continue
            df = len(plist)
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
            for i, tfc in plist:
                s[i] += idf * (tfc * (self.k1 + 1)) / (
                    tfc + self.k1 * (1 - self.b + self.b * self.doclen[i] / self.avgdl))
        return s


def fw_threshold(pooled: np.ndarray, n_docs: int) -> dict:
    q_fw = 1.0 - NULL_ALPHA / max(1, n_docs)
    return {"null_n": int(pooled.size),
            "p99": float(np.quantile(pooled, 0.99)),
            "p999": float(np.quantile(pooled, 0.999)),
            "threshold_fw": float(np.quantile(pooled, q_fw)),
            "q_fw": q_fw}


def main() -> None:
    emb = load_embedder()
    if emb is None:
        print("POTION UNAVAILABLE -- fail-safe None; scan cannot run.")
        return
    meanings = load_struct_meanings()
    enrich = load_resolver_enrichment()
    docs = load_corpus()
    plane_counts = Counter(p for _, p, _ in docs)
    print("Corpus: %d docs, plane-labeled: %s" % (len(docs), dict(plane_counts)))
    print("Null gate: pooled decoy null, M=%d draws/vertical, family-wise alpha=%.2f over N=%d docs"
          % (NULL_M, NULL_ALPHA, len(docs)))

    doc_vecs = emb.embed_many([t for _, _, t in docs])
    bm = BM25Index(docs)
    token_stream = []
    for _, _, t in docs:
        token_stream.extend(toks(t)[:400])   # frequency-weighted draw pool (capped/doc for balance)
    print("Decoy draw pool: %d tokens (frequency-weighted stream)." % len(token_stream))

    result = {"meta": {"corpus": dict(plane_counts), "n_docs": len(docs), "alpha_fw": NULL_ALPHA,
                       "null_m": NULL_M, "embedder_dim": emb.dim,
                       "axes": "potion-cosine + bm25, ABLATED never fused",
                       "decoy_design": "frequency-weighted random token draws, length-matched per query, seeded sha1(vertical,m)",
                       "verticals_n": len(V2STRUCT),
                       "roster_note": "28 ratified; resolver drift declared (mdpf rows feed model-portfolios; opal-mcp aliases m365-mcp)"},
              "verticals": {}}

    for v in sorted(V2STRUCT):
        q = vertical_query(v, meanings, enrich)
        qt = set(toks(q))
        qv = emb.embed(q)
        cos = doc_vecs @ qv
        bms = bm.score(qt)

        null_cos, null_bm = [], []
        for m in range(NULL_M):
            seed = int(hashlib.sha1(("%s|%d" % (v, m)).encode()).hexdigest()[:8], 16)
            rng = random.Random(seed)
            decoy_toks = [rng.choice(token_stream) for _ in range(max(8, len(qt)))]
            dq = " ".join(decoy_toks)
            null_cos.append(doc_vecs @ emb.embed(dq))
            null_bm.append(bm.score(set(decoy_toks)))
        gate = {"potion": fw_threshold(np.concatenate(null_cos), len(docs)),
                "bm25": fw_threshold(np.concatenate(null_bm), len(docs))}

        entry = {"query_tokens": len(qt), "query_head": q[:160], "null": gate,
                 "admitted": {}, "admitted_at_p999": {}, "top_display": {}}
        for axis, scores in (("potion", cos), ("bm25", bms)):
            thr = gate[axis]["threshold_fw"]
            adm = [i for i in np.argsort(scores)[::-1] if scores[i] > thr]
            entry["admitted"][axis] = [
                {"path": docs[i][0], "plane": docs[i][1], "score": round(float(scores[i]), 4)}
                for i in adm]
            entry["admitted_at_p999"][axis] = int((scores > gate[axis]["p999"]).sum())
            by_plane = defaultdict(list)
            for i in np.argsort(scores)[::-1]:
                pl = docs[i][1]
                if len(by_plane[pl]) < TOP_DISPLAY:
                    by_plane[pl].append({"path": docs[i][0], "score": round(float(scores[i]), 4),
                                         "admitted": bool(scores[i] > thr)})
                if all(len(x) >= TOP_DISPLAY for x in by_plane.values()) and len(by_plane) == 3:
                    break
            entry["top_display"][axis] = dict(by_plane)
        pa = {d["path"] for d in entry["admitted"]["potion"]}
        ba = {d["path"] for d in entry["admitted"]["bm25"]}
        entry["ablation"] = {"both": sorted(pa & ba), "potion_only_n": len(pa - ba),
                             "bm25_only_n": len(ba - pa)}
        nb, npo = len(ba), len(pa)
        entry["verdict"] = ("RICH" if len(pa & ba) >= 2 else
                            "COVERED" if (nb + npo) >= 2 else
                            "THIN" if (nb + npo) == 1 else "NONE-DECLARED")
        result["verticals"][v] = entry
        print("%-22s potion_adm=%-3d bm25_adm=%-3d both=%-3d verdict=%s"
              % (v, npo, nb, len(pa & ba), entry["verdict"]))

    dst = os.path.join(WS, "org/tier1_exec/4.0.0_SA_CRO/deliverables/C3II_SEMANTIC_SCAN_V2_OUTPUT_20260811.json")
    json.dump(result, open(dst, "w", encoding="utf-8"), indent=1)
    verd = Counter(e["verdict"] for e in result["verticals"].values())
    print("\nVERDICTS over %d verticals: %s" % (len(V2STRUCT), dict(verd)))
    print("output -> %s" % dst)


if __name__ == "__main__":
    main()
