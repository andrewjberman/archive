"""AMGT-jj-2 transform (deliverable, not product code): repair NU's stored drafting document OFFLINE.

  py -3.12 build_repaired.py --stored <stored draft json> --excerpt <filing excerpt text> --out <repaired json>

Each sentence's `text` is a paraphrase glued onto a slice of the filing. The sentence's `quoted_spans` carry the filing's words;
locate each span in the stored filing excerpt (the latest silver filing_source row's excerpt text, read only), widen it to the
filing's own sentence boundaries (a sentence end, a short line end, or a bullet), and use that verbatim sentence as `text`.
`evidence`, `quoted_spans`, every other field and all 38 sentences are kept. `text_original` is set equal to `text` (the code's
convention for English text: drafting_build.py:321 and translate.py:171 -- text_original == text).
A span that matches 0 or more than 1 place (after the evidence passage narrows it) is a STOP.
"""
import argparse
import json
import re
import sys

ABBR = {"no", "u.s", "s.a", "inc", "ltd", "co", "corp", "vs", "approx", "mr", "mrs", "dr", "st", "e.g", "i.e", "etc"}
FOLD = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"'}
BULLETS = "\u25cf\u25cb\u2022"
CLOSERS = "\"')\u201d\u2019"
OPENERS = "\"(\u201c"


def norm(t):
    return re.sub(r"\s+", " ", t or "").strip()


def ascii_fold(t):
    """Length-preserving fold of quote characters (the stored spans carry ASCII quotes, the filing curly ones)."""
    return "".join(FOLD.get(c, c) for c in t)


def is_start(raw, q):
    """True if a filing sentence starts at index q of the RAW excerpt (line breaks kept)."""
    if q <= 0:
        return True
    if raw[q].isspace() or not (raw[q].isupper() or raw[q].isdigit() or raw[q] in OPENERS):
        return False
    j = q - 1
    ws = ""
    while j >= 0 and raw[j].isspace():
        ws += raw[j]
        j -= 1
    if j < 0:
        return True
    if raw[j] in BULLETS:
        return True
    if "\n" in ws:  # a line start after a real line end: wrapped lines are 130-150 chars, a short line is a heading/paragraph end
        ls = raw.rfind("\n", 0, j) + 1
        if j - ls + 1 < 118:
            return True
    if not ws:
        return False
    k = j
    while k >= 0 and raw[k] in CLOSERS:
        k -= 1
    if k < 0 or raw[k] not in ".!?":
        return False
    m = k
    while m > 0 and (raw[m - 1].isalpha() or raw[m - 1] == "."):
        m -= 1
    tok = raw[m:k].lower()
    return not (tok in ABBR or (len(tok) == 1 and tok.isalpha()))


def widen(raw, s, e):
    while s > 0 and not is_start(raw, s):
        s -= 1
    while e < len(raw):
        q = e
        while q < len(raw) and raw[q].isspace():
            q += 1
        if q >= len(raw) or (q > e and is_start(raw, q)) or raw[q] in BULLETS:
            break
        e += 1
    return s, e


def find_span(raw, rawf, span, passages):
    """Every place the span sits in the excerpt; when several, keep those whose widened sentence AND the 30 characters before it
    both sit in an evidence passage (the passage is the citation's own context)."""
    pat = r"\s+".join(re.escape(w) for w in ascii_fold(span).split())
    hits = [m.span() for m in re.finditer(pat, rawf)]
    if len(hits) > 1:
        pn = [norm(ascii_fold(p)) for p in passages]
        ok = []
        for h in hits:
            s0, e0 = widen(raw, *h)
            ctx = norm(rawf[max(0, s0 - 40):e0])
            if any(ctx[-(len(norm(rawf[s0:e0])) + 12):] in p for p in pn):
                ok.append(h)
        hits = ok
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stored", required=True)
    ap.add_argument("--excerpt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--first-only", default="", help="sentence numbers cut to the first filing sentence of their span (r85 K2 flags two "
                    "adjacent filing sentences that share two years as 'restated'; the two facts differ, so only one is kept)")
    a = ap.parse_args()
    doc = json.load(open(a.stored, encoding="utf-8"))
    raw = open(a.excerpt, encoding="utf-8").read()
    rawf = ascii_fold(raw)
    assert len(rawf) == len(raw)
    passages = {r["id"]: r.get("passage") or "" for r in doc.get("evidence_records") or []}
    first_only = {int(x) for x in a.first_only.split(",") if x.strip()}
    n = 0
    for sec in doc["sections"]:
        for s in sec["sentences"]:
            n += 1
            keep = [passages.get(i, "") for i in s.get("evidence") or []]
            ranges = []
            for q in s.get("quoted_spans") or []:
                hits = find_span(raw, rawf, q, keep)
                if len(hits) != 1:
                    print("sentence %d: span matches %d places -- STOP" % (n, len(hits)))
                    return 1
                ranges.append(widen(raw, *hits[0]))
            if not ranges:
                print("sentence %d has no quoted span -- STOP" % n)
                return 1
            st = min(r[0] for r in ranges)
            en = max(r[1] for r in ranges)
            if n in first_only:
                cut = next((q for q in range(st + 1, en) if is_start(raw, q)), en)
                en = cut
            new = norm(raw[st:en])
            print("%2d len %4d (was %4d) | %s ... %s" % (n, len(new), len(s["text"]), new[:70].encode("ascii", "replace").decode(),
                                                          new[-50:].encode("ascii", "replace").decode()))
            s["text"] = new
            s["text_original"] = new
    json.dump(doc, open(a.out, "w", encoding="utf-8", newline="\n"), indent=2)
    print("sentences written: %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
