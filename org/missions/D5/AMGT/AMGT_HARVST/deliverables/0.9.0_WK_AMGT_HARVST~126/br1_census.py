"""AMGT_HARVST round 74, HVST-br-1 -- THE CENSUS of `1.0.0_SA_CTO~Z` R30 (a capital-initial ALIAS rule), worker 0.9.0_WK_AMGT_HARVST~126.

Started from round 73's `stored_case_census.py`; only the rule tested is changed. The SAME served pairs (rebuild #9's dump,
48,358) and the SAME list (round64). A pair is REMOVED when the security's mention count in the article falls to 0 with
`_CAPITAL_INITIAL_ALIAS_RULE` True (BEFORE: False). Silver is read (S3 GET only); nothing is written but this folder.
Run from the worktree root as `PYTHONPATH=. python <this file>`.
"""
import collections
import io
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, ROOT)

from lib.research.harvest import publication_gold as pg  # noqa: E402

LIST = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "2.0.0_SA_COO_H", "round64",
                    "securities.universe.r64.json")
DUMP = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/harvest-backfill/r72_dump/served_mention.json"
OUT_TXT = os.path.join(HERE, "br1_census.out")
OUT_JSON = os.path.join(HERE, "br1_census.json")
READ_KEYS = ["V_US_Equity", "CDNS_US_Equity", "BKNG_US_Equity", "ORA_FP_Equity"]
WIDTH = 160

LINES = []


def emit(line=""):
    line = line.encode("ascii", "replace").decode("ascii")
    LINES.append(line)
    print(line)
    sys.stdout.flush()


def mentions(article, sec, rule):
    pg._CAPITAL_INITIAL_ALIAS_RULE = rule
    try:
        return pg._security_mentions(article, sec).get("mention_count") or 0
    finally:
        pg._CAPITAL_INITIAL_ALIAS_RULE = True


def scan(text, sec):
    """Every span the alternation finds in `text` for `sec`, as (start, end, counted_with_rule, counted_without_rule).
    The SAME alias set the matcher sees (aliases, anchored brands, ticker-anchor names; ticker forms exact-case). A span is
    graded by running the real `_match_counts` on the span alone."""
    aliases = pg._security_aliases(sec) + list(sec.get("anchored_aliases") or []) + list(sec.get("ticker_anchor_aliases") or [])
    exact = pg._security_exact_aliases(sec)
    pattern = pg._span_pattern(aliases, exact)
    out = []
    if pattern is None:
        return out
    for m in pattern.finditer(text or ""):
        span = m.group(0)
        pg._CAPITAL_INITIAL_ALIAS_RULE = True
        on = pg._match_counts(span, aliases, exact)[0] > 0
        pg._CAPITAL_INITIAL_ALIAS_RULE = False
        off = pg._match_counts(span, aliases, exact)[0] > 0
        pg._CAPITAL_INITIAL_ALIAS_RULE = True
        out.append((m.start(), m.end(), on, off))
    return out


def around(text, start, end):
    half = max(0, (WIDTH - (end - start)) // 2)
    chunk = text[max(0, start - half):end + half]
    return re.sub(r"\s+", " ", chunk)


def sentence_initial(text, start):
    return start == 0 or text[start - 1] in "\r\n" or text[max(0, start - 2):start] in (". ", "? ", "! ")


def pair_texts(article):
    yield "title", article.get("title") or ""
    for i, block in enumerate(article.get("text_blocks") or []):
        yield "block%d" % i, block


def first_discarded(article, sec):
    for where, text in pair_texts(article):
        for start, end, on, off in scan(text, sec):
            if off and not on:
                return where, around(text, start, end)
    return None, ""


def counted_contexts(article, sec):
    ctx, initial = [], []
    for where, text in pair_texts(article):
        for start, end, on, _off in scan(text, sec):
            if on:
                ctx.append("[%s] %s" % (where, around(text, start, end)))
                initial.append(sentence_initial(text, start))
    return ctx, initial


def spread(items, n):
    """n items evenly strided over `items` (already in a fixed order)."""
    if len(items) <= n:
        return list(items)
    return [items[(i * len(items)) // n] for i in range(n)]


def main():
    securities = {s["security_key"]: s for s in json.load(open(LIST, encoding="utf-8"))}
    served = json.load(open(DUMP, encoding="utf-8"))
    pairs = collections.defaultdict(list)
    for row in served:
        pairs[row["article_key"]].append(row["security_key"])
    emit("SERVED PAIRS %d over %d articles; securities in the list %d" % (len(served), len(pairs), len(securities)))
    seen, no_aliases, removed, kept_read = 0, 0, [], collections.defaultdict(list)
    found = set()
    for article in pg._iter_latest_articles():
        key = article.get("article_key")
        if key not in pairs:
            continue
        found.add(key)
        for sk in pairs[key]:
            sec = securities.get(sk)
            if sec is None:
                continue
            if not sec.get("aliases"):
                no_aliases += 1
                continue
            seen += 1
            before = mentions(article, sec, False)
            after = mentions(article, sec, True)
            if before and not after:
                where, ctx = first_discarded(article, sec)
                removed.append({"article_key": key, "security_key": sk, "title": article.get("title") or "",
                                "aliases": sec.get("aliases"), "where": where, "context": ctx})
            elif after and sk in READ_KEYS:
                ctx, initial = counted_contexts(article, sec)
                kept_read[sk].append({"article_key": key, "title": article.get("title") or "", "contexts": ctx,
                                      "sentence_initial": bool(initial) and all(initial)})
    not_found = len(set(pairs) - found)
    by_sec = collections.Counter(r["security_key"] for r in removed)
    emit("TESTED %d pairs on securities with aliases (%d on securities with none, not affected); articles not found in silver %d"
         % (seen, no_aliases, not_found))
    emit("R30 REMOVES %d of %d tested pairs (%d of %d served), over %d securities"
         % (len(removed), seen, len(removed), len(served), len(by_sec)))
    for sk, n in by_sec.most_common():
        sample_titles = [r["title"][:90] for r in removed if r["security_key"] == sk][:2]
        emit("  %-20s %5d  aliases %s  e.g. %s" % (sk, n, securities[sk].get("aliases"), sample_titles))

    # REMOVED SAMPLE 30: at most 3 per security, spread over as many securities as there are (seeded round-robin)
    emit("REMOVED SAMPLE 30:")
    keys = sorted(by_sec)
    random.Random(74).shuffle(keys)
    picks = {k: spread(sorted((r for r in removed if r["security_key"] == k), key=lambda r: r["article_key"]), 3) for k in keys}
    sample = []
    for rnd in range(3):
        for k in keys:
            if len(sample) < 30 and rnd < len(picks[k]):
                sample.append(picks[k][rnd])
    for r in sample:
        emit("  %s | %s | %s | [%s] %s" % (r["security_key"], r["article_key"], r["title"][:120], r["where"], r["context"]))
    emit("  (sample covers %d securities of %d with a removal)" % (len(set(r["security_key"] for r in sample)), len(by_sec)))

    emit("KEPT READ:")
    total_read = total_initial = 0
    read_rows = {}
    for sk in READ_KEYS:
        rows = sorted(kept_read.get(sk, []), key=lambda r: r["article_key"])
        chosen = spread(rows, 10)
        read_rows[sk] = chosen
        emit("  %s: %d kept pairs in all; %d read%s" % (sk, len(rows), len(chosen),
                                                        "" if len(chosen) == 10 else " (FEWER than 10 kept pairs)"))
        for r in chosen:
            total_read += 1
            total_initial += 1 if r["sentence_initial"] else 0
            emit("    %s | %s | %s%s" % (sk, r["article_key"], r["title"][:100],
                                         " | SENTENCE-INITIAL" if r["sentence_initial"] else ""))
            for c in r["contexts"]:
                emit("        " + c)
    result = {"served_pairs": len(served), "pairs_tested": seen, "pairs_on_a_security_with_no_aliases": no_aliases,
              "articles_not_found_in_silver": not_found, "removed": len(removed), "removed_by_security": dict(by_sec.most_common()),
              "removed_rows": removed, "removed_sample": sample, "kept_read": read_rows,
              "sentence_initial": total_initial, "kept_read_count": total_read}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=1, ensure_ascii=True)
    emit("SENTENCE-INITIAL %d of %d kept pairs read" % (total_initial, total_read))
    with io.open(OUT_TXT, "w", encoding="ascii", newline="\n") as handle:
        handle.write("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
