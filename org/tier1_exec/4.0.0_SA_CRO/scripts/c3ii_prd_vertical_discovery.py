#!/usr/bin/env python3
"""c3ii_prd_vertical_discovery.py -- derive semantic verticals from the PRD CORPUS, not the registry.

Andrew-direct 2026-08-07: *"you should actually scan the associated PRDs with some kind of rare
token search or bm25, some kind of structured discovery ... it should make it very very obvious what
the relevant semantic verticals are."*

>> WHY THE REGISTRY-ONLY APPROACH WAS TOO THIN, measured. <<
The first C3.ii join derived each macro's join key from ONE TABLE ROW -- surface-area name, portal
dir, pipeline name -- yielding 3-5 tokens per code. After ambiguity filtering FIVE codes retained no
usable key at all, and 31% of the emitted "undeclared vertical" candidates were false. A 35-row table
is not a corpus. The PRDs ARE the corpus: 428 documents, 9.7 MB of prose written ABOUT these
verticals, and none of it was being read.

>> RUNG 2 -- THE ENGINE IS REUSED, NOT REIMPLEMENTED. <<
`dup_scan.BM25` is the estate's canonical implementation; `state_scan.py` (comp-state) already reuses
it rather than writing its own, saying so in its import line. This is the THIRD consumer. It already
carries the discriminative-token cutoff (`max_df_ratio`) that a naive BM25 lacks.

WHAT THIS PRODUCES
  1. A per-macro DISTINCTIVE TERM PROFILE -- the vocabulary that separates documents about that
     vertical from every other document. This is the join key the registry could not supply.
  2. The UNLABELED residue -- PRDs that belong to no declared macro. These are candidate verticals
     from the DOCUMENT side, independent of the resource side, which is a second and unrelated
     line of evidence for the same cell.

⛔ IT NAMES NOTHING. Naming is sovereign; this surfaces candidates and their evidence.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join("org", "modules", "graph", "debtscan"))
from dup_scan import BM25  # noqa: E402 -- the estate's proven engine, reused not reimplemented

# Prose stopwords + estate boilerplate that appears in nearly every governance doc and therefore
# discriminates nothing. Kept small deliberately: BM25's idf already suppresses common terms, and an
# over-large hand stoplist is the roster-not-predicate defect this whole engagement is about.
STOP = set("""a an the and or but if then else for to of in on at by with without from into over
under is are was were be been being do does did doing have has had having this that these those it
its as not no yes we you they he she i me my our your their them us who whom which what when where
why how all any both each few more most other some such only own same so than too very can will just
should now also per via each new old use used using make made get got see seen say said one two three
first second third next last more less least much many via etc eg ie vs
prd doc docs document documentation section sections appendix status owner date version rev
opal andrew agent agents fabric estate commit commits git repo record records file files path paths
must should shall may never always ensure verify verified verification check checked
""".split())

TOK = re.compile(r"[a-z][a-z0-9_]{2,}")


def tok(s: str) -> list[str]:
    return [t for t in TOK.findall(s.lower()) if t not in STOP]


def load_macro_codes(path="org/projects/MACRO_CODES.md"):
    """The DECLARED plane -- codes + their surface-area words, for labelling only."""
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^\|\s*`([A-Z0-9]{4})`\s*\|\s*([^|]*)", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def label_doc(fname, text, codes, surface_words):
    """Label a document to a macro. Filename first (strong), then CONTENT (weaker, declared).

    Returns (code, basis) or (None, reason). A doc that cannot be labelled is NOT forced into a
    bucket -- an unlabelled PRD is a finding, not a failure.
    """
    up = fname.upper()
    for c in codes:
        if up.startswith(c + "_") or up.startswith(c + "-") or ("_" + c + "_") in up:
            return c, "filename"
    # content fallback: the code token itself, or the macro's surface-area words, in the first 4KB
    head = text[:4000].upper()
    hits = [c for c in codes if re.search(r"\b" + c + r"\b", head)]
    if len(hits) == 1:
        return hits[0], "content:code"
    body = set(tok(text[:8000]))
    scored = []
    for c, words in surface_words.items():
        w = set(tok(words)) - STOP
        if w and len(w & body) >= max(2, len(w) // 2):
            scored.append((len(w & body), c))
    if len(scored) == 1:
        return scored[0][1], "content:surface"
    if scored:
        scored.sort(reverse=True)
        if len(scored) > 1 and scored[0][0] > scored[1][0]:
            return scored[0][1], "content:surface-top"
    return None, ("ambiguous" if hits or scored else "no-signal")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="*", default=["docs/architecture"])
    ap.add_argument("--top", type=int, default=12, help="distinctive terms per macro")
    ap.add_argument("--out", default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()

    vintage = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    codes = load_macro_codes()
    docs, names, unread = [], [], []
    for root in args.roots:
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if not f.endswith(".md"):
                    continue
                p = os.path.join(dp, f)
                try:
                    txt = open(p, encoding="utf-8", errors="replace").read()
                except Exception as e:
                    unread.append((p, str(e)[:60]))
                    continue
                docs.append(txt)
                names.append(p.replace(os.sep, "/"))

    labels, bases = [], collections.Counter()
    for n, t in zip(names, docs):
        c, basis = label_doc(os.path.basename(n), t, codes, codes)
        labels.append(c)
        bases[basis] += 1

    toks = [tok(t) for t in docs]
    bm = BM25(toks)

    # ---- per-macro DISTINCTIVE terms -------------------------------------------------
    # A term is distinctive for macro M when it is FREQUENT INSIDE M and RARE OUTSIDE it.
    # score = (in-macro doc frequency ratio) x idf. idf comes from the shared engine, so
    # "rare" is measured against the whole corpus rather than asserted.
    by_macro = collections.defaultdict(list)
    for i, c in enumerate(labels):
        if c:
            by_macro[c].append(i)

    profiles = {}
    for c, idxs in sorted(by_macro.items()):
        inside = collections.Counter()
        for i in idxs:
            for t in set(toks[i]):
                inside[t] += 1
        n_in = len(idxs)
        scored = []
        for t, k in inside.items():
            # SUPPORT FLOOR, not a proportion threshold. A >=30%-of-own-docs bar is unusable at both
            # ends: it admits nothing for a 120-doc heterogeneous macro, and at 2 docs it admits any
            # identifier that happens to appear twice. Support scales sub-linearly instead.
            if k < 3 or k < math.sqrt(n_in):
                continue
            df = bm.df.get(t, 0)
            if df == 0:
                continue
            outside = df - k
            # >> CONCENTRATION AS A LOWER BOUND, NEVER A POINT ESTIMATE. <<
            # k/df treats 2-of-2 as identical to 25-of-27. It is not: the first is one coincidence,
            # the second is a pattern. Wilson lower bound at 95% penalises thin support exactly as
            # much as the evidence warrants -- the same correction applied to the TO-0 column
            # denominator, for the same reason, and NOT a threshold tuned until the output looked
            # right (Andrew-direct 2026-08-06: no overfitting a scorer to its own eval cases).
            p = k / df
            z = 1.96
            d = 1 + z * z / df
            centre = (p + z * z / (2 * df)) / d
            half = z * math.sqrt(p * (1 - p) / df + z * z / (4 * df * df)) / d
            conc_lo = max(0.0, centre - half)
            if conc_lo < 0.35:
                continue
            scored.append((conc_lo * bm.idf.get(t, 0.0), t, k, outside, round(conc_lo, 2)))
        scored.sort(reverse=True)
        profiles[c] = {
            "n_docs": n_in,
            "terms": [{"term": t, "in_docs": k, "out_docs": o, "concentration": cc,
                       "score": round(s, 2)} for s, t, k, o, cc in scored[:args.top]],
        }

    # ---- the UNLABELLED residue = candidate verticals from the DOCUMENT side ----------
    unl = [i for i, c in enumerate(labels) if c is None]
    cand = collections.Counter()
    for i in unl:
        for t in set(toks[i]):
            df = bm.df.get(t, 0)
            if 2 <= df <= max(3, len(docs) * 0.05):     # rare across the corpus
                cand[t] += 1

    hdr = {
        "artifact": "c3ii_prd_vertical_discovery",
        "vintage": vintage,
        "engine": "dup_scan.BM25 (estate canonical, REUSED -- 3rd consumer after debtscan + comp-state)",
        "roots": args.roots,
        "denominator_grain": "MARKDOWN DOCUMENTS (not lines, not bytes)",
        "docs_scanned": len(docs),
        "docs_unreadable": len(unread),
        "declared_macro_codes": len(codes),
        "labelled": sum(1 for c in labels if c),
        "unlabelled": len(unl),
        "label_basis": dict(bases),
        "macros_with_docs": len(by_macro),
        "macros_with_NO_docs": sorted(set(codes) - set(by_macro)),
    }
    print(json.dumps(hdr, indent=2))

    print("\n=== PER-MACRO DISTINCTIVE VOCABULARY (the join key the registry could not supply) ===")
    for c, p in sorted(profiles.items(), key=lambda kv: -kv[1]["n_docs"]):
        if not p["terms"]:
            print(f"\n  {c}  ({p['n_docs']} docs)  -- NO distinctive terms cleared the bar")
            continue
        print(f"\n  {c}  ({p['n_docs']} docs)")
        for t in p["terms"]:
            print(f"      {t['term']:<28} in={t['in_docs']:<3} out={t['out_docs']:<4} "
                  f"conc={t['concentration']:<5} score={t['score']}")

    print(f"\n=== UNLABELLED RESIDUE: {len(unl)} PRDs belong to NO declared macro ===")
    print("    (candidate verticals from the DOCUMENT side -- independent of the resource side)")
    for t, n in cand.most_common(30):
        print(f"      {n:>3} docs   {t}")

    if args.out:
        json.dump({"_header": hdr, "profiles": profiles,
                   "unlabelled": [names[i] for i in unl],
                   "candidate_terms": cand.most_common(60)},
                  open(args.out, "w", encoding="utf-8"), indent=2)
        print(f"\nwrote {args.out}")
    return 0


def self_test():
    fails = []

    def check(c, label):
        print(("  PASS  " if c else "  FAIL  ") + label)
        if not c:
            fails.append(label)

    check("the" not in tok("The quick brown"), "stopword dropped")
    check(tok("Advisor-Intelligence_V3") == ["advisor", "intelligence_v3"] or
          "advisor" in tok("Advisor-Intelligence_V3"), "tokenizer splits on punctuation")
    d = [tok("alpha beta gamma"), tok("alpha beta"), tok("alpha")]
    bm = BM25(d)
    check(bm.N == 3, "estate BM25 constructs over an arbitrary corpus")
    check(bm.idf["gamma"] > bm.idf["alpha"], "RARE token scores HIGHER idf than common one")
    check(bm.df["alpha"] == 3 and bm.df["gamma"] == 1, "document frequencies correct")
    codes = load_macro_codes() if os.path.exists("org/projects/MACRO_CODES.md") else {}
    if codes:
        check(len(codes) >= 30, f"macro codes parsed ({len(codes)})")
        c, b = label_doc("ADVI_V1VERS_PRD.md", "x", codes, codes)
        check(c == "ADVI" and b == "filename", "filename labelling works")
        c2, b2 = label_doc("TOTALLY_UNRELATED.md", "nothing here", codes, codes)
        check(c2 is None, "NEGATIVE CONTROL: an unrelated doc is NOT forced into a bucket")
    print(f"\nself-test: {len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
