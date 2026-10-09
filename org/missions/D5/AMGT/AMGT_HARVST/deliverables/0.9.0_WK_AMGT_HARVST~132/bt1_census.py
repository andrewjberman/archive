"""AMGT_HARVST round 76, HVST-bt-1 -- THE CENSUS of `1.0.0_SA_CTO~DELL1` R31 (a common-word alias needs a second anchor),
worker 0.9.0_WK_AMGT_HARVST~132. AMENDMENT 1 (ADDENDUM 4): the common-word set is MEASURED FROM SILVER (`common_word_scan.py` writes
`common_word_aliases.json`); AMENDMENT 2 (ADDENDUM 5): an alias is common when LOWER / CAP_MID >= `_COMMON_WORD_RATIO` (0.2). This script reads that one file, through the matcher.
AMENDMENT 3 (ADDENDUM 6): the second anchor is any of A (ticker from the key + stored forms), B (company less legal suffix), C (full names in
the identity file `lib/opal_data_harvest/config.json` -> `symbol_resolution_source`, fields company.value + aliases.value), D (a sibling listing's
ticker), E (another non-common alias), with the one-and-two-letter-ticker and name-equals-alias guards; this script adds `ANCHORS USED:` per flagged alias.

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
COMMON_JSON = os.path.join(HERE, "common_word_aliases.json")
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
    (where, start, end, text, context, winning_alias). The SAME alias set as the matcher sees (aliases, anchored brands, ticker-anchor names; ticker forms exact-case); each span is
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
                out.append((where, m.start(), m.end(), m.group(0), around(text, m.start(), m.end()), forms[0]))
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
        picks[k] = [items[(i * len(items)) // 4] for i in range(4)] if len(items) > 4 else items
    out = []
    for rnd in range(4):
        for k in keys:
            if len(out) < n and rnd < len(picks[k]):
                out.append(picks[k][rnd])
    return out


def main():
    securities = {s["security_key"]: s for s in json.load(open(LIST, encoding="utf-8"))}
    counted = json.load(open(COMMON_JSON, encoding="utf-8"))
    assert pg._COMMON_WORD_LIST_PATH and os.path.samefile(pg._COMMON_WORD_LIST_PATH, COMMON_JSON)   # the matcher reads THIS file
    rows = counted["aliases"]
    common_by_sec = {}
    for sk, sec in securities.items():
        c = pg._common_word_aliases(sec)
        if c:
            common_by_sec[sk] = c
    n_alias = sum(len(v) for v in common_by_sec.values())
    ident_path = pg._identity_path()
    ident = pg._identity_index()
    emit("IDENTITY FILE (anchor kind C names, kind D siblings): %s" % os.path.relpath(ident_path, ROOT).replace("\\", "/"))
    emit("  fields read per record: company.value + aliases.value (full names, C), sa_symbol.value (sibling link and sibling ticker, D); "
         "pool_name is not read; records %d; path from lib/opal_data_harvest/config.json symbol_resolution_source" % len(ident["names"]))
    emit("COMMON-WORD ALIASES (silver): %d over %d securities; articles scanned %d"
         % (n_alias, len(common_by_sec), counted["articles_scanned"]))
    emit("RATIO RULE: flagged when LOWER / CAP_MID >= %s (CAP_MID = 0 with LOWER > 0 counts as flagged)" % pg._COMMON_WORD_RATIO)
    flagged = sorted((r for r in rows if pg._is_common_word(r["lower"], r["cap_mid"])), key=lambda r: (r["security_key"], r["alias"]))
    for r in flagged:
        emit("  %s: %s  LOWER %d  CAP_MID %d  ratio %.3f" % (r["security_key"], r["alias"], r["lower"], r["cap_mid"],
                                                           (float(r["lower"]) / r["cap_mid"]) if r["cap_mid"] else float("inf")))
    for sk in sorted(common_by_sec):
        specs = pg._anchor_specs(securities[sk], common_by_sec[sk])
        emit("ANCHOR FORMS %s: " % sk + "; ".join("%s %s" % (kind, [f for f, _rx in specs[kind]] or "-") for kind in "ABCD")
             + "; E %s; siblings %s" % ([a for a in securities[sk]["aliases"] if a not in common_by_sec[sk]] or "-", ident["siblings"].get(sk) or "-"))
    near = sorted((r for r in rows if not pg._is_common_word(r["lower"], r["cap_mid"]) and r["cap_mid"] > 0 and r["lower"] > 0),
                  key=lambda r: (-(float(r["lower"]) / r["cap_mid"]), r["security_key"], r["alias"]))
    seen, misses = set(), []
    for r in near:       # one line per alias text: an ADR and its ordinary share carry the same counts
        if r["alias"].lower() in seen:
            continue
        seen.add(r["alias"].lower())
        misses.append(r)
    emit("10 NEAREST MISSES (not flagged; highest LOWER / CAP_MID; one line per alias text):")
    for r in misses[:10]:
        emit("  %s: %s  LOWER %d  CAP_MID %d  ratio %.3f" % (r["security_key"], r["alias"], r["lower"], r["cap_mid"],
                                                          float(r["lower"]) / r["cap_mid"]))
    EXTRA.append("(file: %d (security, alias) rows, %d flagged; securities in the list %d; securities with an alias list %d)"
                 % (len(rows), len(flagged), len(securities), sum(1 for s_ in securities.values() if s_.get("aliases"))))

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
    anchors_used = collections.defaultdict(lambda: {"mentions": 0, "pairs": 0, "present": collections.Counter(),
                                                     "first": collections.Counter(), "only": collections.Counter()})
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
                discarded = list(spans)
                if len(discarded) == before - after:
                    span_control_ok += 1
                else:
                    span_control_bad += 1
                for where, start, end, text, ctx, form in discarded:
                    removed_spans.append({"security_key": sk, "article_key": key, "title": title, "where": where,
                                          "start": start, "span": text, "context": ctx, "alias": form})
            elif common and after > 0:
                spans = common_spans(article, sec, common)
                if spans:
                    kinds = pg._anchor_kinds(title, blocks, sec, common)
                    if not kinds:
                        # a counted common-alias span with no anchor cannot be: the rule would have dropped it
                        continue
                    first = next(k for k in "ABCDE" if k in kinds)
                    forms = {k: v[1] for k, v in kinds.items()}
                    for alias_text in sorted(set(sp[5] for sp in spans)):
                        n = sum(1 for sp in spans if sp[5] == alias_text)
                        slot = anchors_used[(sk, alias_text)]
                        slot["mentions"] += n
                        slot["pairs"] += 1
                        for k in kinds:
                            slot["present"][k] += n
                        slot["first"][first] += n
                        if len(kinds) == 1:
                            slot["only"][first] += n
                    where, start, end, text, ctx, _form = spans[0]
                    kept_mentions.append({"security_key": sk, "article_key": key, "title": title, "where": where, "start": start,
                                          "span": text, "context": ctx, "anchor_kind": first, "anchor_in": kinds[first][0],
                                          "anchor_form": forms[first], "kinds_present": "".join(sorted(kinds)),
                                          "common_spans_counted": len(spans)})
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
    down_by_sec = collections.Counter(sk for sk, _k, _b, a in removed_pairs if a > 0)
    gone_by_sec = collections.Counter(sk for sk, _k, _b, a in removed_pairs if a == 0)
    for sk in sorted(common_by_sec):
        emit("R31 BY SECURITY %s (%s): mentions removed %d, pairs removed %d, pairs counted down %d"
             % (sk, ", ".join(common_by_sec[sk]), men_by_sec[sk], gone_by_sec[sk], down_by_sec[sk]))

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

    emit("BRAND CHECK: flagged aliases that are also the company's ordinary trading name (the alias is the company name without "
         "its legal suffix, or its leading words); for 3.0.0_SA_CVO, no verdict:")
    suffix = re.compile(r"[\s,]+(inc|corp|corporation|co|company|ltd|limited|plc|s\.?a\.?|n\.?v\.?|ag|se|holdings?|group|llc|"
                        r"l\.?p\.?|sa|nv|spa|s\.p\.a\.|ab|asa|oyj|a/s|\.com)\.?$", re.I)
    brand, other = [], []
    for r in flagged:
        company = (securities[r["security_key"]].get("company") or "").strip()
        base = company
        while True:
            nxt = suffix.sub("", base).strip(" ,.")
            if nxt == base or not nxt:
                break
            base = nxt
        words = r["alias"].lower().split()
        cwords = base.lower().split()
        if cwords[:len(words)] == words and words:
            brand.append((r, company))
        else:
            other.append((r, company))
    for r, company in brand:
        emit("  BRAND %s: %s  (company %r)  LOWER %d  CAP_MID %d" % (r["security_key"], r["alias"], company, r["lower"], r["cap_mid"]))
    emit("  %d of %d flagged aliases are the company's own trading name; the other %d flagged are not (alias, company):"
         % (len(brand), len(flagged), len(other)))
    for r, company in other:
        emit("  OTHER %s: %s  (company %r)" % (r["security_key"], r["alias"], company))

    # AMENDMENT 2: for EACH flagged alias text, ten removed mentions by (article key ascending, every k-th). A mention shared by
    # two listings of one alias (Orange: ORA_FP and ORANY) is one line, with both securities named.
    sample = []
    for alias in sorted(set(r["alias"] for r in flagged)):
        pool = {}
        for r in removed_spans:
            if r["alias"] != alias:
                continue
            k = (r["article_key"], r["where"], r["start"])
            if k in pool:
                pool[k]["security_keys"].append(r["security_key"])
            else:
                pool[k] = dict(r, security_keys=[r["security_key"]])
        ordered = [pool[k] for k in sorted(pool)]
        step = max(1, len(ordered) // 10)
        picks = ordered[::step][:10]
        emit("REMOVED SAMPLE %s: 10 (of %d removed mentions on %d distinct (article, place) spans; every %dth by article key, "
             "%d shown)" % (alias, sum(1 for r in removed_spans if r["alias"] == alias), len(ordered), step, len(picks)))
        for r in picks:
            emit("  %s | %s | %s | [%s] %s" % ("+".join(sorted(set(r["security_keys"]))), r["article_key"], r["title"][:120],
                                              r["where"], r["context"]))
        sample.extend(picks)
    for (sk, alias_text) in sorted(anchors_used):
        slot = anchors_used[(sk, alias_text)]
        emit("ANCHORS USED %s %s: %d kept mentions over %d kept pairs" % (sk, alias_text, slot["mentions"], slot["pairs"]))
        emit("  kinds present in the kept article (a mention counts under every kind its article carries): "
             + ", ".join("%s %d" % (k, slot["present"][k]) for k in "ABCDE"))
        emit("  first kind in order A-E (each mention counted once): " + ", ".join("%s %d" % (k, slot["first"][k]) for k in "ABCDE"))
        emit("  the ONLY kind present: " + ", ".join("%s %d" % (k, slot["only"][k]) for k in "ABCDE"))
    ksample = spread_over_securities(kept_mentions, 20, 77)
    emit("KEPT SAMPLE 20: (of %d kept pairs with a counted common-alias mention over %d securities; this sample covers %d securities)"
         % (len(kept_mentions), len(set(r["security_key"] for r in kept_mentions)), len(set(r["security_key"] for r in ksample))))
    for r in ksample:
        emit("  %s | %s | %s | anchor: %s %r in %s (present %s) | [%s] %s" % (r["security_key"], r["article_key"], r["title"][:120],
                                                                 r["anchor_kind"], r["anchor_form"], r["anchor_in"], r["kinds_present"],
                                                                 r["where"], r["context"]))
    kept_by_kind = collections.Counter(r["anchor_kind"] for r in kept_mentions)
    EXTRA.append("KEPT PAIRS BY ANCHOR KIND: " + ", ".join("%s %d" % kv for kv in sorted(kept_by_kind.items())))
    emit("EXTRA MEASURES (not asked for; controls and denominators):")
    for line in EXTRA:
        emit("  " + line)
    result = {"served_pairs": len(served), "pairs_tested": tested, "mentions_before": m_before, "mentions_after": m_after,
              "pairs_removed": pairs_removed, "pairs_counted_down": pairs_down, "cvo_rows_removed": cvo_removed,
              "common_word_aliases": common_by_sec, "removed_by_security_pairs": dict(by_sec),
              "removed_by_security_mentions": dict(men_by_sec), "removed_sample": sample, "kept_sample": ksample,
              "kept_pairs_by_anchor_kind": dict(kept_by_kind),
              "anchors_used": {"%s|%s" % k: {"mentions": v["mentions"], "pairs": v["pairs"], "present": dict(v["present"]),
                                             "first": dict(v["first"]), "only": dict(v["only"])} for k, v in anchors_used.items()}, "articles_not_found_in_silver": not_found,
              "common_word_file": os.path.basename(COMMON_JSON), "articles_scanned": counted["articles_scanned"],
              "nearest_misses": misses[:10]}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=1, ensure_ascii=True, default=str)
    with io.open(OUT_TXT, "w", encoding="ascii", newline="\n") as handle:
        handle.write("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
