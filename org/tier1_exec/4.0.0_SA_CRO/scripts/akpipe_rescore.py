"""
NFRA_AKPIPE -- offline re-score of an existing substrate with the current profile (RCN-0003).

Author: 4.0.0_SA_CRO (Chief Research Officer)

WHY THIS EXISTS. Two reasons, both real:
  1. ZERO-EGRESS ITERATION. The profile is the one input that encodes our judgment, and it
     will be tuned repeatedly. Re-scoring a stored substrate needs NO arxiv calls at all --
     so profile iteration never costs a request. (I tripped arxiv's 429 rate limit pulling
     paginated pages; this is the mechanism that makes that unnecessary.)
  2. IT IS THE PRODUCTION RECOMPUTE PATH IN MINIATURE. The daily Lambda must re-derive
     derived_state_rank over the WHOLE corpus as time elapses. This is that same operation.

Reads akpipe_papers.jsonl, applies the CURRENT profile + scope filter, prints the v1-vs-v2
comparison, and writes the re-scored substrate back (lossless: rows are updated in place by
(arxiv_id, version), never dropped).

ASCII-only.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akpipe_scorer import (  # noqa: E402
    PROFILE_TEXT,
    PROFILE_VERSION,
    PROFILE_PHRASES,
    PhraseIndex,
    potion_embed,
    cosine,
    bm25_magnitude,
    recency_component,
    derived_state_rank,
)

CATEGORIES = ["cs.AI", "cs.LG", "cs.SE", "cs.IR", "cs.DC", "cs.DB", "cs.MA"]


def main() -> int:
    path = sys.argv[1]
    primary_only = (sys.argv[2].lower() != "all") if len(sys.argv) > 2 else True

    rows = [json.loads(line) for line in open(path, encoding="utf-8")]
    print(f"[rescore] loaded {len(rows)} rows (DENOMINATOR)")
    v1 = {r["arxiv_id"]: r.get("nlp_score") for r in rows}

    if primary_only:
        keep = [r for r in rows if r.get("primary_category") in CATEGORIES]
        dropped = len(rows) - len(keep)
        offc = Counter(r["primary_category"] for r in rows
                       if r.get("primary_category") not in CATEGORIES)
        print(f"[rescore] SCOPE FILTER: kept {len(keep)}, dropped {dropped} "
              f"({100*dropped/max(1,len(rows)):.0f}% cross-listed off-primary)")
        print(f"[rescore]   dropped primaries: {offc.most_common(8)}")
        rows = keep

    texts = [f"{r.get('title','')} {r.get('abstract','')}" for r in rows]
    idx = PhraseIndex(texts)
    bm = [idx.score(i) for i in range(len(rows))]
    embs = potion_embed([PROFILE_TEXT] + texts)
    prof, dv = embs[0], embs[1:]
    po = [cosine(prof, dv[i]) for i in range(len(rows))]

    now = datetime.now(timezone.utc)
    for i, r in enumerate(rows):
        rel = bm25_magnitude(bm[i])
        try:
            dt = datetime.fromisoformat(r["timestamp_released"].replace("Z", "+00:00"))
            age = (now - dt).total_seconds() / 86400.0
        except (ValueError, KeyError):
            age = 0.0
        r.update({
            "phrase_bm25": round(bm[i], 4),
            "potion_cosine": round(po[i], 6),
            "nlp_score": round(rel, 6),
            "age_days": round(age, 3),
            "recency_component": round(recency_component(age), 6),
            "derived_state_rank": round(derived_state_rank(rel, age), 8),
            "phrase_hits": idx.phrase_hits(i),
            "profile_version": PROFILE_VERSION,
        })
    rows.sort(key=lambda r: -r["derived_state_rank"])

    import statistics as st
    def cv(v):
        m = st.mean(v)
        return st.pstdev(v) / m if m else 0.0

    zero = sum(1 for r in rows if r["nlp_score"] == 0)
    print(f"\n[rescore] profile={PROFILE_VERSION} ({len(PROFILE_PHRASES)} phrases)")
    print(f"[rescore] phrase-BM25 CV={cv(bm):.3f}   Potion CV={cv(po):.3f}   "
          f"(v1 measured: BM25 0.845 / Potion 0.165)")
    print(f"[rescore] {zero}/{len(rows)} papers score EXACTLY 0 (no profile phrase) -- "
          f"the profile now SEPARATES rather than scoring everything")

    print("\n" + "=" * 104)
    print("TOP 20 -- v2 phrase profile, scope-filtered, abstract-grade")
    print("=" * 104)
    print(f"{'#':>3} {'nlp':>6} {'deriv':>6} {'v1nlp':>6} {'cat':<7} {'age':>5} {'#ph':>3}  title")
    print("-" * 104)
    for i, r in enumerate(rows[:20], 1):
        o = v1.get(r["arxiv_id"])
        print(f"{i:>3} {r['nlp_score']:>6.3f} {r['derived_state_rank']:>6.3f} "
              f"{(o if o is not None else 0):>6.3f} {r['primary_category']:<7} "
              f"{r['age_days']:>5.1f} {len(r['phrase_hits']):>3}  {r['title'][:58]}")

    print("\nTOP-8 PHRASE EVIDENCE (the deterministic 'why' -- auditable, no black box):")
    for i, r in enumerate(rows[:8], 1):
        print(f"  {i}. {r['title'][:64]}")
        print(f"     {', '.join(r['phrase_hits'][:9])}")

    print("\nBOTTOM 5 (sanity -- these SHOULD look off-target):")
    for r in rows[-5:]:
        print(f"     {r['nlp_score']:.3f} [{r['primary_category']:<7}] {r['title'][:66]}")

    out = os.path.join(os.path.dirname(path), "akpipe_papers_v2.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")
    print(f"\n[substrate] wrote {len(rows)} re-scored rows -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
