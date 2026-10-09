"""AMGT_HARVST round 76, HVST-bt-1 -- THE CENSUS of `1.0.0_SA_CTO~DELL1` R31 (a common-word alias needs a second anchor),
worker 0.9.0_WK_AMGT_HARVST~132.

Built from round 74's `br1_census.py` (worker ~126); only the rule tested is changed. POPULATION: the SERVED gold mention part
`amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261009T093755Z.parquet` (rebuild #12) read by an S3 GET, its
(article_key, security_key) pairs; the article text is silver, read the same way (`_iter_latest_articles`, GETs only). The list
is `0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json`. BEFORE = R30 on, R31 off; AFTER = both on. The grain is the MENTION
(`mention_count` of `_security_mentions`, summed over every tested pair). Nothing is written to S3; the only files written are
`bt1_census.out` and `bt1_census.json` beside this script. Run from the worktree root as `PYTHONPATH=. python <this file>`.
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

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

LIST = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "0.9.0_WK_AMGT_HARVST~129",
                    "securities.universe.r75.json")
GOLD_KEY = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261009T093755Z.parquet"
SOURCE_JSON = os.path.join(HERE, "WORDLIST_SOURCE.json")
OUT_TXT = os.path.join(HERE, "bt1_census.out")
OUT_JSON = os.path.join(HERE, "bt1_census.json")
WIDTH = 160

# the 14 rows the CVO grade names: 8 "Visa" (security V_US_Equity) and 6 "Orange" (ORA_FP_Equity and ORANY_US_Equity, 3 each)
CVO_V = ["bbg:T613YXKK3NY900", "bbg:T9XNUNKK3NY800", "bbg:TDYE9YKJH6V400", "bbg:TF8KOAKGZAPG00", "bbg:TH2CITKK3NYC00",
         "bbg:TIMBVUKK3NY900", "bbg:TKC1ZCKJH6V900", "wsj:220e5904-"]      # the last is a prefix (the grade prints it cut)
CVO_O = ["bbg:T8ERVUT96OSM00", "bbg:TEPZPSKJH6V600", "sa:4603901"]
CVO_WANT = [("V_US_Equity", a) for a in CVO_V] + [(sk, a) for sk in ("ORA_FP_Equity", "ORANY_US_Equity") for a in CVO_O]

LINES = []
EXTRA = []
LIMIT = int(os.environ.get("BT1_LIMIT", "0"))      # smoke runs only: stop after this many matched articles, write to .scratch
if LIMIT:
    OUT_TXT = os.path.join(ROOT, ".scratch", "bt1_smoke.out")
    OUT_JSON = os.path.join(ROOT, ".scratch", "bt1_smoke.json")


def emit(line=""):
    line = line.encode("ascii", "replace").decode("ascii")
    LINES.append(line)
    print(line)
    sys.stdout.flush()


def mentions(article, sec, r31):
    pg._COMMON_WORD_SECOND_ANCHOR_RULE = r31
    try:
        return pg._security_mentions(article, sec).get("mention_count") or 0
    finally:
        pg._COMMON_WORD_SECOND_ANCHOR_RULE = True


def around(text, start, end):
    half = max(0, (WIDTH - (end - start)) // 2)
    return re.sub(r"\s+", " ", text[max(0, start - half):end + half])


def pair_texts(article):
    yield "title", article.get("title") or ""
    for i, block in enumerate(article.get("text_blocks") or []):
        yield "block%d" % i, block or ""


def common_spans(article, sec, common):
    """Every span the matcher counts under R30 whose WINNING form is a common alias of `sec`: (where, start, end, text, context).
    The SAME alias set as the matcher sees (aliases, anchored brands, ticker-anchor names; ticker forms exact-case); each span is
    graded by running the real `_match_counts` on the span alone, which gives its winning form."""
    aliases = pg._security_aliases(sec) + list(sec.get("anchored_aliases") or []) + list(sec.get("ticker_anchor_aliases") or [])
    exact = pg._security_exact_aliases(sec)
    pattern = pg._span_pattern(aliases, exact)
    out = []
    if pattern is None:
        return out
    for where, text in pair_texts(article):
        for m in pattern.finditer(text):
            count, forms = pg._match_counts(m.group(0), aliases, exact)
            if count > 0 and forms and all(f in common for f in forms):
                out.append((where, m.start(), m.end(), m.group(0), around(text, m.start(), m.end())))
    return out


def spread_over_securities(rows, n, seed):
    """n rows spread over as many securities as there are: a seeded round-robin over the securities, each security's rows taken
    evenly strided in a fixed order."""
    by = collections.defaultdict(list)
    for r in rows:
        by[r["security_key"]].append(r)
    keys = sorted(by)
    random.Random(seed).shuffle(keys)
    picks = {}
    for k in keys:
        items = sorted(by[k], key=lambda r: (r["article_key"], r.get("where", ""), r.get("start", 0)))
        picks[k] = [items[(i * len(items)) // 3] for i in range(3)] if len(items) > 3 else items
    out = []
    for rnd in range(3):
        for k in keys:
            if len(out) < n and rnd < len(picks[k]):
                out.append(picks[k][rnd])
    return out


def main():
    securities = {s["security_key"]: s for s in json.load(open(LIST, encoding="utf-8"))}
    src = json.load(open(SOURCE_JSON, encoding="utf-8"))
    words = pg._common_word_set()
    emit("WORD LIST: %d words, sha256 %s" % (src["lines"], src["sha256"]))
    common_by_sec = {}
    for sk, sec in securities.items():
        c = pg._common_word_aliases(sec)
        if c:
            common_by_sec[sk] = c
    n_alias = sum(len(v) for v in common_by_sec.values())
    emit("COMMON-WORD ALIASES: %d over %d securities" % (n_alias, len(common_by_sec)))
    for sk in sorted(common_by_sec):
        for a in common_by_sec[sk]:
            emit("  %s: %s" % (sk, a))
    EXTRA.append("(word list loaded: %d distinct lower-case words; securities in the list %d; securities with an alias list %d)"
         % (len(words), len(securities), sum(1 for s in securities.values() if s.get("aliases"))))

    client = store._default_client()
    body = client.get_object(Bucket=store.HARVEST_BUCKET, Key=GOLD_KEY)["Body"].read()
    table = pq.read_table(io.BytesIO(body), columns=["article_key", "security_key", "mention_count"])
    served = table.to_pylist()
    pairs = collections.defaultdict(list)
    served_count = {}
    for row in served:
        pairs[row["article_key"]].append(row["security_key"])
        served_count[(row["article_key"], row["security_key"])] = row["mention_count"]
    EXTRA.append("SERVED PAIRS %d over %d articles (%s)" % (len(served), len(pairs), GOLD_KEY))

    tested = no_aliases = not_in_list = 0
    m_before = m_after = 0
    pairs_removed = pairs_down = 0
    served_equal = served_unequal = 0
    removed_pairs, removed_spans, kept_mentions = [], [], []
    span_control_ok = span_control_bad = 0
    cvo_hit = {}
    found = set()
    for article in pg._iter_latest_articles():
        key = article.get("article_key")
        if key not in pairs:
            continue
        found.add(key)
        if LIMIT and len(found) > LIMIT:
            break
        title = article.get("title") or ""
        blocks = article.get("text_blocks") or []
        for sk in pairs[key]:
            sec = securities.get(sk)
            if sec is None:
                not_in_list += 1
                continue
            if not sec.get("aliases"):
                no_aliases += 1
                continue
            tested += 1
            common = common_by_sec.get(sk)
            if common:
                before, after = mentions(article, sec, False), mentions(article, sec, True)
            else:
                before = after = mentions(article, sec, True)
            m_before += before
            m_after += after
            if before == served_count[(key, sk)]:
                served_equal += 1
            else:
                served_unequal += 1
            for want_sk, want_key in CVO_WANT:
                if sk == want_sk and key.startswith(want_key):
                    cvo_hit[(sk, key)] = (before, after)
            if after < before:
                if after == 0:
                    pairs_removed += 1
                else:
                    pairs_down += 1
                removed_pairs.append((sk, key, before, after))
                spans = common_spans(article, sec, common)
                discarded = [s for s in spans]
                if len(discarded) == before - after:
                    span_control_ok += 1
                else:
                    span_control_bad += 1
                for where, start, end, text, ctx in discarded:
                    removed_spans.append({"security_key": sk, "article_key": key, "title": title, "where": where,
                                          "start": start, "span": text, "context": ctx})
            elif common and after > 0:
                spans = common_spans(article, sec, common)
                if spans:
                    anchor = pg._second_anchor(title, blocks, sec, common)
                    if anchor is None:
                        # a counted common-alias span with no anchor cannot be: the rule would have dropped it
                        continue
                    kind, where_a = anchor
                    what = {"ticker": ",".join(list(sec.get("ticker_aliases") or []) + list(sec.get("ticker_anchor_symbols") or [])),
                            "company": sec.get("company"),
                            "alias": ",".join(a for a in sec.get("aliases") if a not in common)}[kind]
                    where, start, end, text, ctx = spans[0]
                    kept_mentions.append({"security_key": sk, "article_key": key, "title": title, "where": where, "start": start,
                                          "span": text, "context": ctx, "anchor_kind": kind, "anchor_in": where_a,
                                          "anchor_form": what, "common_spans_counted": len(spans)})
    not_found = len(set(pairs) - found)
    EXTRA.append("TESTED %d pairs on securities with aliases (%d on securities with no alias list, %d on securities not in the list, "
         "not affected); articles not found in silver %d" % (tested, no_aliases, not_in_list, not_found))
    EXTRA.append("CONTROL: BEFORE mention_count equals the served gold mention_count on %d of %d tested pairs (%d differ)"
         % (served_equal, tested, served_unequal))
    emit("R31 MENTIONS: before %d, after %d, removed %d" % (m_before, m_after, m_before - m_after))
    emit("R31 PAIRS REMOVED: %d" % pairs_removed)
    emit("R31 PAIRS COUNTED DOWN: %d" % pairs_down)
    EXTRA.append("CONTROL: discarded common-alias spans equal (before - after) on %d of %d changed pairs"
         % (span_control_ok, span_control_ok + span_control_bad))
    by_sec = collections.Counter(sk for sk, _k, _b, _a in removed_pairs)
    men_by_sec = collections.Counter()
    for sk, _k, b, a in removed_pairs:
        men_by_sec[sk] += b - a
    EXTRA.append("REMOVED BY SECURITY (pairs, mentions): " + "; ".join("%s %d, %d" % (sk, n, men_by_sec[sk]) for sk, n in by_sec.most_common()))

    cvo_removed = 0
    cvo_lines = []
    for want_sk, want_key in CVO_WANT:
        hits = [(k, v) for k, v in cvo_hit.items() if k[0] == want_sk and k[1].startswith(want_key)]
        if not hits:
            cvo_lines.append("  %s %s: NOT FOUND among the tested pairs" % (want_sk, want_key))
        for (sk, key), (b, a) in hits:
            gone = b > 0 and a == 0
            cvo_removed += 1 if gone else 0
            cvo_lines.append("  %s %s: before %d, after %d%s" % (sk, key, b, a, " -> REMOVED" if gone else ""))
    emit("CVO ROWS: %d of 14 removed" % cvo_removed)
    for line in cvo_lines:
        emit(line)

    sample = spread_over_securities(removed_spans, 20, 76)
    emit("REMOVED SAMPLE 20: (of %d discarded mentions over %d securities; this sample covers %d securities)"
         % (len(removed_spans), len(set(r["security_key"] for r in removed_spans)), len(set(r["security_key"] for r in sample))))
    for r in sample:
        emit("  %s | %s | %s | [%s] %s" % (r["security_key"], r["article_key"], r["title"][:120], r["where"], r["context"]))
    ksample = spread_over_securities(kept_mentions, 20, 77)
    emit("KEPT SAMPLE 20: (of %d kept pairs with a counted common-alias mention over %d securities; this sample covers %d securities)"
         % (len(kept_mentions), len(set(r["security_key"] for r in kept_mentions)), len(set(r["security_key"] for r in ksample))))
    for r in ksample:
        emit("  %s | %s | %s | anchor: %s %r in %s | [%s] %s" % (r["security_key"], r["article_key"], r["title"][:120],
                                                                 r["anchor_kind"], r["anchor_form"], r["anchor_in"], r["where"],
                                                                 r["context"]))
    kept_by_kind = collections.Counter(r["anchor_kind"] for r in kept_mentions)
    EXTRA.append("KEPT PAIRS BY ANCHOR KIND: " + ", ".join("%s %d" % kv for kv in sorted(kept_by_kind.items())))
    emit("EXTRA MEASURES (not asked for; controls and denominators):")
    for line in EXTRA:
        emit("  " + line)
    result = {"served_pairs": len(served), "pairs_tested": tested, "mentions_before": m_before, "mentions_after": m_after,
              "pairs_removed": pairs_removed, "pairs_counted_down": pairs_down, "cvo_rows_removed": cvo_removed,
              "common_word_aliases": common_by_sec, "removed_by_security_pairs": dict(by_sec),
              "removed_by_security_mentions": dict(men_by_sec), "removed_sample": sample, "kept_sample": ksample,
              "kept_pairs_by_anchor_kind": dict(kept_by_kind), "articles_not_found_in_silver": not_found,
              "word_list": src}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=1, ensure_ascii=True, default=str)
    with io.open(OUT_TXT, "w", encoding="ascii", newline="\n") as handle:
        handle.write("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
