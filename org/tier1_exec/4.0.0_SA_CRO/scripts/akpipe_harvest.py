"""
NFRA_AKPIPE harvest client (RCN-0003) -- DEV RUN form.

Author: 4.0.0_SA_CRO (Chief Research Officer)
Spec:   briefs/NFRA_AKPIPE_BUILD_SPEC_20260723.md

EGRESS POSTURE. Andrew-direct amendment 2026-07-23: DEV/local runs permitted for
NFRA_AKPIPE development; the PRODUCTION daily pipeline stays cloud-Lambda-only.
arxiv ONLY. Read-only. Public paper metadata + full text. Polite rate limiting.

WHAT IT DOES
  1. Harvest recent papers in the target categories via the official arxiv Atom API.
  2. Score on title+abstract using the pinned scorer (BM25 + potion-8M -> magnitude).
  3. Fetch FULL TEXT for the top-N (Andrew decision 3: full-text rescore) via
     /html/{id} when the LaTeX render exists, else the PDF, and RESCORE.
  4. Emit the ranked table + an append-only JSONL substrate row per paper.

The transport here is the Atom API because it is the clean way to pull "recent N in
these categories". The PRODUCTION backbone stays OAI-PMH ListRecords (exhaustive
from/until delta with resumptionToken) per spec section 2 -- this dev client does not
replace it.

ASCII-only (CLAUDE.md Code Quality).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akpipe_scorer import (  # noqa: E402
    PROFILE_TEXT,
    PROFILE_VERSION,
    POTION_MODEL,
    PhraseIndex,
    potion_embed,
    cosine,
    bm25_magnitude,
    rrf,
    recency_component,
    derived_state_rank,
)

ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"

UA = "OpalCapital-NFRA_AKPIPE/0.1 (research harvest; contact andrew@opalinvest.com)"
API = "http://export.arxiv.org/api/query"
POLITE_SLEEP = 3.0          # arxiv asks ~1 request / 3s
FULLTEXT_TIMEOUT = 60

CATEGORIES = ["cs.AI", "cs.LG", "cs.SE", "cs.IR", "cs.DC", "cs.DB", "cs.MA"]


def _get(url: str, timeout: int = 90, retries: int = 4) -> bytes:
    """GET with exponential backoff. arxiv throttles with 503 + Retry-After and can stall
    on deep pages -- a single-shot fetch is a real robustness gap (the Lambda needs this too)."""
    delay = 5.0
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (503, 429):
                wait = float(e.headers.get("Retry-After") or delay)
                print(f"    [retry {attempt}/{retries}] HTTP {e.code}, waiting {wait:.0f}s")
                time.sleep(wait)
            elif e.code in (500, 502, 504):
                print(f"    [retry {attempt}/{retries}] HTTP {e.code}, waiting {delay:.0f}s")
                time.sleep(delay)
            else:
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
            print(f"    [retry {attempt}/{retries}] {type(e).__name__}, waiting {delay:.0f}s")
            time.sleep(delay)
        delay *= 2
    raise RuntimeError(f"GET failed after {retries} attempts: {url[:90]} ({last})")


def _parse_page(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    out = []
    for e in root.findall(f"{ATOM}entry"):
        idurl = (e.findtext(f"{ATOM}id") or "").strip()
        m = re.search(r"abs/([^v]+)v(\d+)", idurl)
        if not m:
            continue
        arxiv_id, version = m.group(1), "v" + m.group(2)
        prim = e.find(f"{ARX}primary_category")
        out.append({
            "arxiv_id": arxiv_id, "version": version,
            "title": " ".join((e.findtext(f"{ATOM}title") or "").split()),
            "abstract": " ".join((e.findtext(f"{ATOM}summary") or "").split()),
            "authors": [" ".join((a.findtext(f"{ATOM}name") or "").split())
                        for a in e.findall(f"{ATOM}author")],
            "primary_category": prim.get("term") if prim is not None else "",
            "categories": [c.get("term") for c in e.findall(f"{ATOM}category") if c.get("term")],
            "timestamp_released": (e.findtext(f"{ATOM}published") or "").strip(),
            "timestamp_updated": (e.findtext(f"{ATOM}updated") or "").strip(),
            "doi": e.findtext(f"{ARX}doi"),
            "source_channel": "atom", "fulltext_fetched": False,
        })
    return out


def harvest(total: int = 400, page: int = 100, primary_only: bool = True) -> list[dict]:
    """Pull recent submissions across the target categories, paginated (back-window),
    then FILTER to target PRIMARY categories (fix 4: kills the cross-listing scope leak)."""
    q = "+OR+".join(f"cat:{c}" for c in CATEGORIES)
    raw_rows: list[dict] = []
    for start in range(0, total, page):
        url = (f"{API}?search_query={q}&sortBy=submittedDate&sortOrder=descending"
               f"&start={start}&max_results={page}")
        print(f"[harvest] GET start={start} max={page}")
        chunk = _parse_page(_get(url))
        raw_rows.extend(chunk)
        if len(chunk) < page:
            break
        time.sleep(POLITE_SLEEP)
    # dedup on (arxiv_id, version)
    seen, dedup = set(), []
    for r in raw_rows:
        k = (r["arxiv_id"], r["version"])
        if k not in seen:
            seen.add(k)
        dedup.append(r)
    print(f"[harvest] pulled {len(raw_rows)} entries, {len(dedup)} unique (id,version)")
    if primary_only:
        keep = [r for r in dedup if r["primary_category"] in CATEGORIES]
        dropped = len(dedup) - len(keep)
        print(f"[harvest] SCOPE FILTER: kept {len(keep)}, dropped {dropped} cross-listed "
              f"({100*dropped/max(1,len(dedup)):.0f}% off-primary) -- DENOMINATOR {len(dedup)}")
        return keep
    return dedup


_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def fetch_fulltext(arxiv_id: str, version: str) -> tuple[str, str]:
    """Return (text, source). Prefer the LaTeX HTML render; fall back to the PDF."""
    # 1) /html/{id}{v} -- cheapest clean text when the render exists
    try:
        raw = _get(f"https://arxiv.org/html/{arxiv_id}{version}", timeout=FULLTEXT_TIMEOUT)
        html = raw.decode("utf-8", errors="replace")
        html = re.sub(r"(?is)<(script|style|math)\b.*?</\1>", " ", html)
        text = _WS.sub(" ", _TAG.sub(" ", html)).strip()
        if len(text) > 3000:
            return text, "html"
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        pass
    # 2) PDF fallback
    try:
        raw = _get(f"https://arxiv.org/pdf/{arxiv_id}{version}", timeout=FULLTEXT_TIMEOUT)
        import fitz
        doc = fitz.open(stream=raw, filetype="pdf")
        text = " ".join(p.get_text() for p in doc)
        return _WS.sub(" ", text).strip(), "pdf"
    except Exception:
        return "", "none"


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def score_rows(rows: list[dict], field: str) -> dict:
    """Score rows on rows[i][field] with phrase-BM25 (rank) + Potion (stored component).
    Returns a recovery-bar report: does Potion promote any phrase-BM25-missed paper?"""
    texts = [r[field] for r in rows]
    idx = PhraseIndex(texts)
    bm_scores = [idx.score(i) for i in range(len(rows))]
    embs = potion_embed([PROFILE_TEXT] + texts)
    prof, docvecs = embs[0], embs[1:]
    po_scores = [cosine(prof, docvecs[i]) for i in range(len(rows))]

    def ranks(scores):
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], rows[i]["arxiv_id"]))
        r = [0] * len(scores)
        for pos, i in enumerate(order, 1):
            r[i] = pos
        return r
    bm_rank, po_rank = ranks(bm_scores), ranks(po_scores)

    now = datetime.now(timezone.utc)
    for i, r in enumerate(rows):
        rel = bm25_magnitude(bm_scores[i])
        try:
            rel_dt = datetime.fromisoformat(r["timestamp_released"].replace("Z", "+00:00"))
            age = (now - rel_dt).total_seconds() / 86400.0
        except (ValueError, KeyError):
            age = 0.0
        r.update({
            "phrase_bm25": round(bm_scores[i], 4),
            "potion_cosine": round(po_scores[i], 6),
            "nlp_rrf_ordering": round(rrf([bm_rank[i], po_rank[i]]), 8),
            "nlp_score": round(rel, 6),
            "age_days": round(age, 3),
            "recency_component": round(recency_component(age), 6),
            "derived_state_rank": round(derived_state_rank(rel, age), 8),
            "phrase_hits": idx.phrase_hits(i),
            "scored_on": field,
            "profile_version": PROFILE_VERSION,
            "potion_model_version": POTION_MODEL,
        })

    # recovery bar: papers Potion ranks in top-K that phrase-BM25 buries below top-K
    import statistics as _st
    K = max(5, len(rows) // 4)
    recovered = [rows[i]["arxiv_id"] for i in range(len(rows))
                 if po_rank[i] <= K and bm_rank[i] > K]
    def cv(v):
        m = _st.mean(v)
        return _st.pstdev(v) / m if m else 0.0
    return {"K": K, "recovered": recovered,
            "bm25_cv": round(cv(bm_scores), 3), "potion_cv": round(cv(po_scores), 3)}


def _corr(xs, ys) -> float:
    import statistics as st
    if len(xs) < 3:
        return 0.0
    mx, my = st.mean(xs), st.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return num / den if den else 0.0


def main() -> int:
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    n_meta = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    n_full = int(sys.argv[3]) if len(sys.argv) > 3 else 15

    rows = harvest(total=n_meta, primary_only=True)
    if not rows:
        print("[harvest] NOTHING RETURNED -- stopping (a zero needs a positive control)")
        return 1

    for r in rows:
        r["_abstract_blob"] = f"{r['title']} {r['abstract']}"
    rep1 = score_rows(rows, "_abstract_blob")
    rows.sort(key=lambda r: -r["derived_state_rank"])

    ages = [r["age_days"] for r in rows]
    print("\n" + "=" * 104)
    print(f"PASS 1 -- ABSTRACT-GRADE RANKING (N={len(rows)}, profile={PROFILE_VERSION})")
    print(f"  age window: {min(ages):.1f}..{max(ages):.1f} days  |  "
          f"BM25 CV={rep1['bm25_cv']} Potion CV={rep1['potion_cv']}  |  "
          f"Potion recovered {len(rep1['recovered'])} into top-{rep1['K']}")
    print("=" * 104)
    print(f"{'#':>3} {'nlp':>6} {'deriv':>6} {'cat':<8} {'age':>5}  {'#ph':>3}  title")
    print("-" * 104)
    for i, r in enumerate(rows[:20], 1):
        print(f"{i:>3} {r['nlp_score']:>6.3f} {r['derived_state_rank']:>6.3f} "
              f"{r['primary_category']:<8} {r['age_days']:>5.1f}  {len(r['phrase_hits']):>3}  "
              f"{r['title'][:62]}")

    top = rows[:n_full]
    print("\n" + "=" * 104)
    print(f"PASS 2 -- FULL-TEXT FETCH + RESCORE (top {len(top)}; polite {POLITE_SLEEP}s)")
    print("=" * 104)
    for r in top:
        text, src = fetch_fulltext(r["arxiv_id"], r["version"])
        r["_full"] = text if text else r["_abstract_blob"]
        r["fulltext_fetched"] = bool(text)
        r["fulltext_source"] = src
        r["fulltext_chars"] = len(text)
        emails = sorted(set(EMAIL_RE.findall(text[:25000]))) if text else []
        r["author_emails"] = [e for e in emails if not e.lower().endswith((".png", ".jpg", ".pdf"))]
        print(f"  {r['arxiv_id']}{r['version']:<4} src={src:<4} chars={len(text):>7} "
              f"emails={len(r['author_emails'])}  {r['title'][:46]}")
        time.sleep(POLITE_SLEEP)

    rep2 = score_rows(top, "_full")
    top.sort(key=lambda r: -r["derived_state_rank"])

    # length-bias measurement (fix 2 verification)
    lb = _corr([r["fulltext_chars"] for r in top if r["fulltext_fetched"]],
               [r["phrase_bm25"] for r in top if r["fulltext_fetched"]])

    print("\n" + "=" * 104)
    print("PASS 2 RESULT -- FULL-TEXT RANKING (the production basis)")
    print(f"  length-bias corr(chars, phrase_bm25) = {lb:+.3f}  (v1 was +0.60; near 0 = fixed)")
    print(f"  Potion recovery on full text: {len(rep2['recovered'])} papers into top-{rep2['K']} "
          f"(BM25 CV={rep2['bm25_cv']} Potion CV={rep2['potion_cv']})")
    print("=" * 104)
    print(f"{'#':>3} {'nlp':>6} {'deriv':>6} {'ph_bm':>7} {'pot':>6} {'src':<4} {'ch':>7} {'#ph':>3}  title")
    print("-" * 104)
    for i, r in enumerate(top, 1):
        print(f"{i:>3} {r['nlp_score']:>6.3f} {r['derived_state_rank']:>6.3f} "
              f"{r['phrase_bm25']:>7.2f} {r['potion_cosine']:>6.3f} "
              f"{r['fulltext_source']:<4} {r['fulltext_chars']:>7} {len(r['phrase_hits']):>3}  "
              f"{r['title'][:48]}")

    print("\n  TOP-5 phrase evidence (WHY each ranked -- the deterministic explanation):")
    for i, r in enumerate(top[:5], 1):
        print(f"   {i}. {r['title'][:60]}")
        print(f"      hits: {', '.join(r['phrase_hits'][:10])}")

    path = os.path.join(outdir, "akpipe_papers.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            rec = {k: v for k, v in r.items() if not k.startswith("_")}
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")
    print(f"\n[substrate] wrote {len(rows)} rows -> {path}  "
          f"(unique id,version = {len({(r['arxiv_id'], r['version']) for r in rows})})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
