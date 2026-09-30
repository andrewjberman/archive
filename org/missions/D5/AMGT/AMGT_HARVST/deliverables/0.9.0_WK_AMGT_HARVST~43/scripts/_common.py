"""Shared core for HVST-f-1 (read-only: S3 GET of the silver article parts through the served
iterator; no put, no delete, no vendor call, no code change).

ADDED = what a candidate FORM would add over today's served alias set, measured with the SERVED
matcher's own pattern builder (`publication_gold._span_pattern`, longest-first, word-bounded,
one span one count): spans(aliases + [form]) minus spans(aliases), per title and per block."""
import json
import os
import random
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402

DELIV = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
SECURITIES = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~41", "securities.universe.json")
SEED = 20260929
SAMPLE_N = 10
LEAD_BLOCKS = 3  # publication_gold._security_mentions: lead_span = range(min(3, blocks_total))

CLASS_TICKER = "T1 ticker, exchange stripped"
CLASS_ROOT = "T2 ticker root (share-class suffix removed)"
CLASS_SHORT = "B1 short name (leading word of the company alias; DERIVED, no source artifact)"
CLASSES = [CLASS_TICKER, CLASS_ROOT, CLASS_SHORT]

NO_BRAND_SOURCE = "no brand source in the estate"

# A CURATED watch list -- author judgment, printed by AC1, NOT a dictionary (none is installed and
# none is in the estate; surprise row Z-W43-S1). Generic words a leading-word short name or a
# ticker would collide with.
CURATED_WORDS = {
    "now", "fix", "flex", "lite", "echo", "dell", "cost", "amp", "deck", "spot", "keys", "meta",
    "uber", "mar", "all", "best", "bank", "booking", "delta", "applied", "advanced",
    "american", "united", "national", "china", "british", "canadian", "international", "global",
    "first", "general", "new", "southwest", "hon", "home", "union", "state", "steel", "waste",
    "western", "globe", "orange", "comfort",
}


def load_securities():
    with open(SECURITIES, encoding="utf-8") as fh:
        return json.load(fh)


def load_articles():
    rows = list(pg._iter_latest_articles())
    rows.sort(key=lambda r: r["article_key"])
    return rows


def _norm(s):
    return s.casefold()


def ticker_forms(sec):
    """(T1, T2) for one security -- T2 None when identical to T1."""
    first = (sec.get("ticker") or "").split()
    if not first:
        return None, None
    t1 = first[0].strip("*/.-")
    if not t1:
        return None, None
    root = re.split(r"[/.]", t1)[0] if re.search(r"[A-Za-z0-9][/.][A-Za-z0-9]", t1) else t1
    t2 = root if root != t1 else None
    return t1, t2


def short_form(sec):
    """Leading word of the LONGEST alias when it has >= 2 tokens; None otherwise."""
    aliases = [a for a in sec.get("aliases") or [] if a]
    if not aliases:
        return None
    longest = max(aliases, key=len)
    toks = longest.split()
    if len(toks) < 2:
        return None
    return toks[0].strip(",.")


def generate_forms(securities):
    """[(class, form, security)] -- every derivable candidate form with its owning security."""
    out = []
    for sec in securities:
        t1, t2 = ticker_forms(sec)
        if t1:
            out.append((CLASS_TICKER, t1, sec))
        if t2:
            out.append((CLASS_ROOT, t2, sec))
        sf = short_form(sec)
        if sf:
            out.append((CLASS_SHORT, sf, sec))
    return out


def stopwords():
    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        return set(ENGLISH_STOP_WORDS)
    except Exception:  # noqa: BLE001
        return set()


STOP = stopwords()


def spans(text, aliases):
    pat = pg._span_pattern(aliases)
    if pat is None or not text:
        return []
    return [(m.start(), m.end(), m.group(0)) for m in pat.finditer(text)]


def texts_of(article):
    """[(where, text)] exactly as the served matcher reads it: the title, then each block."""
    out = [("title", article.get("title") or "")]
    for i, block in enumerate(article.get("text_blocks") or []):
        out.append(("block %d" % i, block or ""))
    return out


def already_covered(form, aliases):
    return any(_norm(form) == _norm(a) for a in aliases)


def asc(text):
    """Non-ASCII characters print as backslash escapes (ASCII-only output, offsets unaffected)."""
    return text.encode("ascii", "backslashreplace").decode("ascii")


def _ctx(text, s, e, w=70):
    a = max(0, s - w)
    b = min(len(text), e + w)
    return asc(("..." if a else "") + text[a:s] + "[[" + text[s:e] + "]]" + text[e:b] + ("..." if b < len(text) else ""))


def added_for(article, sec, form):
    """None when the form adds nothing. Else dict: hits, added_count, base_count, flips."""
    aliases = list(pg._security_aliases(sec))
    if already_covered(form, aliases):
        return None
    combined = aliases + [form]
    hits = []
    base_title = base_lead = comb_title = comb_lead = False
    base_total = comb_total = 0
    for idx, (where, text) in enumerate(texts_of(article)):
        b = spans(text, aliases)
        c = spans(text, combined)
        base_total += len(b)
        comb_total += len(c)
        if b:
            if where == "title":
                base_title = True
            elif idx - 1 < LEAD_BLOCKS:
                base_lead = True
        if c:
            if where == "title":
                comb_title = True
            elif idx - 1 < LEAD_BLOCKS:
                comb_lead = True
        bset = {(s, e) for s, e, _ in b}
        for s, e, m in c:
            if (s, e) not in bset:
                hits.append({"where": where, "offset": s, "matched": m, "context": _ctx(text, s, e)})
    if not hits:
        return None
    return {"hits": hits, "added_count": len(hits), "delta_count": comb_total - base_total,
            "base_count": base_total,
            "title_flip": comb_title and not base_title,
            "lead_flip": comb_lead and not base_lead}


def corpus_lowercase_counts(forms, articles):
    """How often the form appears in the corpus in ordinary lower case (`v`, `all`, `best`):
    evidence the string is an ordinary word here. A proxy, printed, never a dictionary."""
    alltexts = [t for a in articles for _w, t in texts_of(a)]
    out = {}
    for f in forms:
        p = re.compile(r"(?<!\w)" + re.escape(f) + r"(?!\w)", re.I)
        n = 0
        for t in alltexts:
            for m in p.finditer(t):
                if m.group(0) != f and m.group(0) == m.group(0).lower():
                    n += 1
        out[f] = n
    return out


def flags(form, low):
    f = []
    if len(form) <= 3:
        f.append("SHORT<=3")
    c = form.casefold()
    if c in STOP or c in CURATED_WORDS:
        f.append("DICT-WORD(stopword/curated)")
    if low.get(form, 0) > 0:
        f.append("DICT-WORD(lowercase in corpus x%d)" % low[form])
    return f


def compute():
    """The whole census as data: (securities, articles, rows) with one row per generated form."""
    securities = load_securities()
    articles = load_articles()
    gen = generate_forms(securities)
    forms = sorted({f for _c, f, _s in gen})
    low = corpus_lowercase_counts(forms, articles)
    rows = []
    for cls, form, sec in gen:
        aliases = list(pg._security_aliases(sec))
        row = {"class": cls, "form": form, "security_key": sec["security_key"],
               "company": sec["company"], "covered": already_covered(form, aliases),
               "flags": flags(form, low), "pairs": 0, "new_pairs": 0, "added_count": 0,
               "title_flips": 0, "lead_flips": 0, "hits": [], "anomalies": 0}
        if not row["covered"]:
            for art in articles:
                r = added_for(art, sec, form)
                if not r:
                    continue
                row["pairs"] += 1
                if r["base_count"] == 0:
                    row["new_pairs"] += 1
                row["added_count"] += r["added_count"]
                row["title_flips"] += int(r["title_flip"])
                row["lead_flips"] += int(r["lead_flip"])
                if r["delta_count"] != r["added_count"]:
                    row["anomalies"] += 1
                for h in r["hits"]:
                    h = dict(h)
                    h.update({"article_key": art["article_key"], "headline": asc(art.get("title") or ""),
                              "security_key": sec["security_key"]})
                    row["hits"].append(h)
        rows.append(row)
    return securities, articles, rows


def sample(row):
    hits = sorted(row["hits"], key=lambda h: (h["article_key"], h["where"], h["offset"]))
    if len(hits) <= SAMPLE_N:
        return hits
    rng = random.Random("%s|%s|%s|%s" % (SEED, row["class"], row["form"], row["security_key"]))
    return sorted(rng.sample(hits, SAMPLE_N), key=lambda h: (h["article_key"], h["where"], h["offset"]))
