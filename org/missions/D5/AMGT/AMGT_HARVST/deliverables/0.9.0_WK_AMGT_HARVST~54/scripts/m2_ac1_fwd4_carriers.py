"""m2_ac1_fwd4_carriers.py -- HVST-m-2 AC1: FWD-4 re-grade from the served store (READ-ONLY, MEASURES, GRADES NOTHING).

WHAT IT MEASURES
  Over the NEWEST served gold `article_security_mention` part (key printed):
  (a) CARRIER PRESENCE -- per (article, company) pair, for each of the six carriers FWD-4 names, how many pairs
      carry it, over the pair denominator. Column map (C-HV-ABSOLUTE-ONLY: no ratio is stored, so the "share" carrier
      is the absolute pair blocks_hit / blocks_total):
        1 in headline            mention_in_title              (bool, non-null = present)
        2 in the opening         mention_in_lead               (bool, non-null = present)
        3 how often named        mention_count                 (int >= 1 = present)
        4 how much names it      blocks_hit and blocks_total   (both non-null and blocks_total > 0 = present)
        5 other covered names    co_mentioned_securities       (list, non-null = present; non-empty is also counted)
        6 strength grade         signal_tier                   (one of A B C D = present)
  (b) RE-DERIVATION of every carrier and the grade from the STORED SILVER TEXT, by the rule below, implemented HERE
      and never by calling lib.research.harvest.publication_gold (no producer function is imported or called on its
      own output). Matched / mismatched counts per carrier and per pair, every mismatched pair listed.

THE RULE (re-implemented from the stored text; the producer's rule as documented in publication_gold.py's header)
  Text = the silver article row's `title` and `text_blocks` (list of strings).
  Alias set of a company = the union, over the WHOLE gold table, of that security_key's stored `match_forms` (the
  forms that actually won a text span for it). A form is CASE-SENSITIVE (a ticker form) iff it is upper-case, has
  2 or more characters, has a letter, and equals the first '_' token of the security_key; every other form is
  case-insensitive. (An alias that never matched anywhere in the table cannot change any count, so this set is
  sufficient for every pair in the table.)
  Match = word-bounded ((?<!\\w) form (?!\\w)), one alternation, longest form first, non-overlapping spans, each
  span counted once.
  in_title = title count > 0.   in_lead = any of the first min(3, blocks_total) blocks has count > 0.
  mention_count = title count + sum of block counts.   blocks_hit = blocks with count > 0.   blocks_total = len(blocks).
  co_mentioned = the sorted other security_keys (of the table's known securities) with mention count > 0 in the
  same article.
  GRADE (first match wins): A if in_title and in_lead; else B if in_title or in_lead or blocks_hit/blocks_total >= 0.3;
  else C if mention_count >= 2; else D.
  A second layer: the STORED grade is also checked against the rule applied to the pair's own STORED carriers.

SILVER JOIN: each gold pair is joined to the silver article row whose record_hash equals the pair's record_hash (the
row that produced it). If none matches, the newest-fetched_at silver row for the article_key is used and the pair is
counted under `silver_hash_mismatch` (silver has moved on since the gold build; a re-derivation there is by newer text).
An article whose silver row cannot be found at all is NOT MEASURABLE HERE and is listed.

MISSING-PAIR SCAN (extra, printed with its denominator): for each article in the gold table x each known security,
a silver recount > 0 with no gold pair is listed.

Reads S3 (GET/LIST) only. Writes only m2_ac1_* files beside this script's parent folder.
"""
import collections
import io
import json
import os
import re
import sys

import boto3
import pyarrow.parquet as pq

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 8)))
sys.path.insert(0, REPO)

import lib.research.harvest.store as store  # noqa: E402  (only table_prefix + bucket; no producer function)
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BUCKET = store.HARVEST_BUCKET
SHARE_B = 0.3
LEAD_BLOCKS = 3

client = boto3.client("s3", region_name="us-east-1")


def newest_part(table):
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    date_of = lambda k: re.search(r"date=(\d{4}-\d{2}-\d{2})", k).group(1)  # noqa: E731
    keys.sort(key=lambda k: (date_of(k), k))
    return keys[-1], len(keys)


def read_parquet_rows(key):
    raw = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def silver_articles():
    """{article_key: [rows]} over EVERY silver article part of every enabled source."""
    by_key = collections.defaultdict(list)
    parts = 0
    for _code, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        prefix = store.table_prefix(source, "silver", "article")
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                if not obj["Key"].endswith(".parquet"):
                    continue
                parts += 1
                for row in read_parquet_rows(obj["Key"]):
                    by_key[row.get("article_key")].append(row)
    return by_key, parts


def build_pattern(forms, exact):
    pieces = sorted([(f, "(?i:%s)" % re.escape(f)) for f in forms if f not in exact]
                    + [(f, re.escape(f)) for f in exact], key=lambda p: len(p[0]), reverse=True)
    if not pieces:
        return None
    return re.compile(r"(?<!\w)(?:" + "|".join(p for _f, p in pieces) + r")(?!\w)")


def count_in(pattern, text):
    if pattern is None or not text:
        return 0
    return sum(1 for _m in pattern.finditer(text))


def derive_grade(in_title, in_lead, count, blocks_hit, blocks_total, share_b=SHARE_B):
    share = (blocks_hit / blocks_total) if blocks_total else 0.0
    if in_title and in_lead:
        return "A"
    if in_title or in_lead or share >= share_b:
        return "B"
    if count >= 2:
        return "C"
    return "D"


def is_ticker_form(form, security_key):
    first = security_key.split("_")[0]
    return form == first and form.upper() == form and len(form) >= 2 and any(c.isalpha() for c in form)


def main():
    key, nparts = newest_part("article_security_mention")
    pairs = read_parquet_rows(key)
    n = len(pairs)
    print("NEWEST SERVED article_security_mention PART: s3://%s/%s  (%d part(s) under the prefix)" % (BUCKET, key, nparts))
    print("PAIR DENOMINATOR: %d pairs, %d articles, %d securities"
          % (n, len({p["article_key"] for p in pairs}), len({p["security_key"] for p in pairs})))

    # ---- (a) carrier presence ------------------------------------------------------------------
    def present(p):
        return {
            "in_headline": p.get("mention_in_title") is not None,
            "in_opening": p.get("mention_in_lead") is not None,
            "how_often_named": isinstance(p.get("mention_count"), int) and p["mention_count"] >= 1,
            "share_of_article": (p.get("blocks_hit") is not None and p.get("blocks_total") is not None
                                 and p["blocks_total"] > 0),
            "co_mentioned": isinstance(p.get("co_mentioned_securities"), list),
            "strength_grade": p.get("signal_tier") in ("A", "B", "C", "D"),
        }
    carrier_counts = collections.Counter()
    for p in pairs:
        for name, ok in present(p).items():
            carrier_counts[name] += 1 if ok else 0
    print("\nAC1 (a) CARRIER PRESENT-COUNTS over %d pairs:" % n)
    for name in ("in_headline", "in_opening", "how_often_named", "share_of_article", "co_mentioned", "strength_grade"):
        print("  %-18s %d of %d" % (name, carrier_counts[name], n))
    value_facts = {
        "in_headline_true": sum(1 for p in pairs if p["mention_in_title"]),
        "in_opening_true": sum(1 for p in pairs if p["mention_in_lead"]),
        "co_mentioned_nonempty": sum(1 for p in pairs if p["co_mentioned_securities"]),
        "grade_distribution": dict(sorted(collections.Counter(p["signal_tier"] for p in pairs).items())),
    }
    print("  value facts: %s" % json.dumps(value_facts, sort_keys=True))

    # ---- (b) re-derivation from stored silver text --------------------------------------------
    forms_by_sec = collections.defaultdict(set)
    for p in pairs:
        forms_by_sec[p["security_key"]].update(p["match_forms"] or [])
    patterns = {}
    for sec, forms in forms_by_sec.items():
        exact = {f for f in forms if is_ticker_form(f, sec)}
        patterns[sec] = build_pattern(sorted(forms), exact)
    print("\nALIAS SETS derived from stored match_forms: %d securities, %d forms, %d treated case-sensitive (ticker)"
          % (len(forms_by_sec), sum(len(v) for v in forms_by_sec.values()),
             sum(1 for s, v in forms_by_sec.items() for f in v if is_ticker_form(f, s))))

    silver, sparts = silver_articles()
    print("SILVER article parts read: %d; distinct article_keys: %d; rows: %d"
          % (sparts, len(silver), sum(len(v) for v in silver.values())))

    articles = sorted({p["article_key"] for p in pairs})
    hash_mismatch = 0
    no_silver = []
    silver_row_for_pair = {}
    for p in pairs:
        rows = silver.get(p["article_key"]) or []
        if not rows:
            silver_row_for_pair[(p["article_key"], p["security_key"])] = None
            continue
        exact_row = [r for r in rows if r.get("record_hash") == p["record_hash"]]
        if exact_row:
            silver_row_for_pair[(p["article_key"], p["security_key"])] = (exact_row[0], True)
        else:
            newest = max(rows, key=lambda r: str(r.get("fetched_at")))
            silver_row_for_pair[(p["article_key"], p["security_key"])] = (newest, False)
    for ak in articles:
        rows = silver.get(ak) or []
        if not rows:
            no_silver.append(ak)

    def article_counts(row):
        title = row.get("title") or ""
        blocks = list(row.get("text_blocks") or [])
        out = {}
        for sec, pat in patterns.items():
            tc = count_in(pat, title)
            bc = [count_in(pat, b) for b in blocks]
            out[sec] = (tc, bc)
        return out, len(blocks)

    cache = {}
    per_carrier = {c: [0, 0] for c in ("in_headline", "in_opening", "how_often_named", "share_of_article",
                                       "co_mentioned", "strength_grade")}
    pair_all_match = 0
    pair_measured = 0
    control_lead1 = 0   # NEGATIVE CONTROL: same text, mutated rule (opening = first 1 block; share_b 0.6)
    control_lead1_grade = 0
    mismatches = []
    stored_grade_vs_own_carriers = [0, 0]
    own_mismatch = []
    for p in pairs:
        # second layer: stored grade vs the rule applied to the pair's own stored carriers
        own = derive_grade(p["mention_in_title"], p["mention_in_lead"], p["mention_count"],
                           p["blocks_hit"], p["blocks_total"])
        if own == p["signal_tier"]:
            stored_grade_vs_own_carriers[0] += 1
        else:
            stored_grade_vs_own_carriers[1] += 1
            own_mismatch.append({"article_key": p["article_key"], "security_key": p["security_key"],
                                 "stored": p["signal_tier"], "from_own_carriers": own})
        srow = silver_row_for_pair.get((p["article_key"], p["security_key"]))
        if srow is None:
            continue
        row, exact_hash = srow
        if not exact_hash:
            hash_mismatch += 1
        ak = p["article_key"]
        ckey = (ak, row.get("record_hash"))
        if ckey not in cache:
            cache[ckey] = article_counts(row)
        counts, blocks_total = cache[ckey]
        tc, bc = counts[p["security_key"]]
        in_title = tc > 0
        in_lead = any(c > 0 for c in bc[:LEAD_BLOCKS])
        count = tc + sum(bc)
        blocks_hit = sum(1 for c in bc if c > 0)
        co = sorted(s for s, (t, b) in counts.items() if s != p["security_key"] and (t + sum(b)) > 0)
        grade = derive_grade(in_title, in_lead, count, blocks_hit, blocks_total)
        mut_lead = any(c > 0 for c in bc[:1])
        if mut_lead != p["mention_in_lead"]:
            control_lead1 += 1
        if derive_grade(in_title, mut_lead, count, blocks_hit, blocks_total, share_b=0.6) != p["signal_tier"]:
            control_lead1_grade += 1
        got = {
            "in_headline": (in_title, p["mention_in_title"]),
            "in_opening": (in_lead, p["mention_in_lead"]),
            "how_often_named": (count, p["mention_count"]),
            "share_of_article": ((blocks_hit, blocks_total), (p["blocks_hit"], p["blocks_total"])),
            "co_mentioned": (co, sorted(p["co_mentioned_securities"] or [])),
            "strength_grade": (grade, p["signal_tier"]),
        }
        pair_measured += 1
        bad = []
        for name, (mine, stored) in got.items():
            if mine == stored:
                per_carrier[name][0] += 1
            else:
                per_carrier[name][1] += 1
                bad.append({"carrier": name, "re_derived": mine, "stored": stored})
        if bad:
            mismatches.append({"article_key": ak, "security_key": p["security_key"],
                               "silver_record_hash_matches": exact_hash, "mismatches": bad})
        else:
            pair_all_match += 1

    print("\nAC1 (b) RE-DERIVATION FROM STORED SILVER TEXT (rule in the script header):")
    print("  pairs joined to a silver row: %d of %d  (silver_hash_mismatch: %d; articles with no silver row: %d %s)"
          % (pair_measured, n, hash_mismatch, len(no_silver), no_silver))
    for name, (m, x) in per_carrier.items():
        print("  %-18s matched %d  mismatched %d  (of %d measured)" % (name, m, x, pair_measured))
    print("  GRADE re-derived from text: matched %d, mismatched %d of %d" %
          (per_carrier["strength_grade"][0], per_carrier["strength_grade"][1], pair_measured))
    print("  ALL SIX carriers matched on %d of %d measured pairs; %d pair(s) with at least one mismatch"
          % (pair_all_match, pair_measured, len(mismatches)))
    print("  stored grade vs rule applied to the pair's OWN stored carriers: matched %d, mismatched %d of %d"
          % (stored_grade_vs_own_carriers[0], stored_grade_vs_own_carriers[1], n))
    print("  NEGATIVE CONTROL (mutated rule, same text: opening = first 1 block, share_b 0.6): the comparator reports"
          " %d opening mismatches and %d grade mismatches of %d -- it can fail"
          % (control_lead1, control_lead1_grade, pair_measured))
    print("\nEVERY MISMATCHED PAIR (%d):" % len(mismatches))
    for m in mismatches:
        print("  " + json.dumps(m, sort_keys=True, default=str))
    print("EVERY STORED-GRADE-vs-OWN-CARRIERS MISMATCH (%d):" % len(own_mismatch))
    for m in own_mismatch:
        print("  " + json.dumps(m, sort_keys=True))

    # ---- missing-pair scan -------------------------------------------------------------------
    have = {(p["article_key"], p["security_key"]) for p in pairs}
    missing = []
    scanned = 0
    for ak in articles:
        rows = silver.get(ak) or []
        if not rows:
            continue
        pair_hashes = {p["record_hash"] for p in pairs if p["article_key"] == ak}
        row = next((r for r in rows if r.get("record_hash") in pair_hashes), None)
        if row is None:
            row = max(rows, key=lambda r: str(r.get("fetched_at")))
        ckey = (ak, row.get("record_hash"))
        if ckey not in cache:
            cache[ckey] = article_counts(row)
        counts, _bt = cache[ckey]
        for sec, (t, b) in counts.items():
            scanned += 1
            if (t + sum(b)) > 0 and (ak, sec) not in have:
                missing.append({"article_key": ak, "security_key": sec, "recount": t + sum(b)})
    print("\nMISSING-PAIR SCAN: %d (article, known-security) cells scanned over %d articles; %d recount>0 with no gold pair"
          % (scanned, len(articles), len(missing)))
    for m in missing:
        print("  " + json.dumps(m, sort_keys=True))

    result = {
        "gold_key": key, "pair_denominator": n, "carrier_present_counts": dict(carrier_counts),
        "value_facts": value_facts, "measured_pairs": pair_measured, "silver_hash_mismatch": hash_mismatch,
        "articles_without_silver": no_silver,
        "per_carrier_matched_mismatched": per_carrier, "pairs_all_six_matched": pair_all_match,
        "mismatched_pairs": mismatches,
        "stored_grade_vs_own_carriers": {"matched": stored_grade_vs_own_carriers[0],
                                         "mismatched": stored_grade_vs_own_carriers[1], "list": own_mismatch},
        "negative_control": {"opening_mismatches": control_lead1, "grade_mismatches": control_lead1_grade},
        "missing_pairs": missing, "missing_scan_cells": scanned,
    }
    with open(os.path.join(OUT_DIR, "m2_ac1_result.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote m2_ac1_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
