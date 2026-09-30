"""HVST-n-2 AC3 -- "query by company" over the MENTION JOIN against `discovered_for`, side by side.

READ-ONLY: S3 GET/LIST only; nothing is written to S3 (the only files written are this cell's own
n2_ac3_output.txt / n2_ac3_result.json beside the scripts).

THE TWO KEYINGS (both over the same served silver `article` rows, all five publishers, all row versions):
  A. discovered_for : silver rows whose `discovered_for` list contains the security. "Found while searching
     for" -- FWD-3's provenance carrier. This is what the m1 query used.
  B. mention join   : the NEWEST served gold `article_security_mention` snapshot's pairs for the security
     (alias-matched: a pair exists only where the company's aliases matched the article text), joined to the
     silver row on `article_key` -- lib/opal_data_harvest/silver_from_bronze.rows_by_company_mention.
DAY: the silver fetch partition day (`fetched_at` UTC date = the silver `date=` partition), 2026-09-23, the
same day the m1 query filtered on; then the whole series (every day). Compared on DISTINCT article_key.
For a row only under A, the mention snapshot is asked whether it holds ANY pair for that article (any
security): none = the article post-dates the snapshot or matched no covered company; some = the article is in
the snapshot and its text did not match this security's aliases.
"""
import collections
import datetime
import io
import re

import pyarrow.parquet as pq

import n2_common as C

from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

DAY = datetime.date(2026, 9, 23)
NAMED_ROWS = {"sa:4429803": "AES", "sa:4411320": "Barrick", "sa:4411819": "Atlantic Power (third sa row of the query)"}
DATE_RE = re.compile(r"date=(\d{4}-\d{2}-\d{2})")


def discovered_list(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    return [str(v)]


def newest_mention_snapshot():
    client = C.client()
    prefix = store.table_prefix("amgt", "gold", "article_security_mention")
    keys = [k for k in C.list_keys(prefix) if k.endswith(".parquet")]
    newest = sorted(keys, key=lambda k: (DATE_RE.search(k).group(1), k))[-1]
    raw = client.get_object(Bucket=C.BUCKET, Key=newest)["Body"].read()
    return newest, len(keys), pq.read_table(io.BytesIO(raw)).to_pylist()


def label(row_by_key, key):
    r = row_by_key[key]
    return "%s | %s | %s" % (key, str(r.get("title"))[:80], NAMED_ROWS.get(key, ""))


def compare(name, silver_all, mentions, pairs_any, fetch_date, L, result, snapshot_at):
    """One comparison at one day scope (fetch_date None = whole series)."""
    scope = "fetch day %s" % fetch_date if fetch_date else "WHOLE SERIES (every day)"
    in_scope = [r for r in silver_all if fetch_date is None or sfb._date_of(r["fetched_at"]) == fetch_date]
    a_rows = [r for r in in_scope if C.SECURITY in discovered_list(r.get("discovered_for"))]
    b_rows, unjoined = sfb.rows_by_company_mention(C.SECURITY, mentions, silver_all, fetch_date=fetch_date)
    a_keys = {r["article_key"] for r in a_rows}
    b_keys = {r["article_key"] for r in b_rows}
    row_by_key = {}
    for r in in_scope:
        row_by_key.setdefault(r["article_key"], r)
    for r in b_rows:
        row_by_key[r["article_key"]] = r
    pub_of = lambda k: k.split(":")[0]  # noqa: E731
    L.append("")
    L.append("=== %s ===" % scope)
    L.append("denominator: silver rows in scope %d (distinct article_key %d)" % (len(in_scope), len({r["article_key"] for r in in_scope})))
    L.append("A discovered_for contains %s: %d distinct articles (%s)" % (
        C.SECURITY, len(a_keys), ", ".join("%s=%d" % kv for kv in sorted(collections.Counter(map(pub_of, a_keys)).items())) or "none"))
    L.append("B mention join (gold pair for %s -> silver on article_key): %d distinct articles (%s); mention pairs with NO silver row on any day: %d %s" % (
        C.SECURITY, len(b_keys), ", ".join("%s=%d" % kv for kv in sorted(collections.Counter(map(pub_of, b_keys)).items())) or "none", len(unjoined), unjoined[:5]))
    both = sorted(a_keys & b_keys)
    only_a = sorted(a_keys - b_keys)
    only_b = sorted(b_keys - a_keys)
    L.append("in BOTH: %d | ONLY discovered_for (A not B): %d | ONLY mention join (B not A): %d" % (len(both), len(only_a), len(only_b)))
    L.append("-- rows that DIFFER, listed by title --")
    for k in only_a:
        if k in pairs_any:
            why = "article IS in the mention snapshot (%d pairs, none for %s): its text did not match the security's aliases" % (
                len(pairs_any[k]), C.SECURITY)
        elif row_by_key[k]["fetched_at"] < snapshot_at:
            why = ("NO pair for any security although fetched %s, BEFORE the snapshot (%s): the gold writes a pair only "
                   "where mention_count > 0, so no covered security's alias matched its text" % (row_by_key[k]["fetched_at"].isoformat(), snapshot_at.isoformat()))
        else:
            why = "NO pair for any security and fetched AFTER the snapshot: post-dates it"
        L.append("  ONLY discovered_for | %s | %s" % (label(row_by_key, k), why))
    for k in only_b:
        L.append("  ONLY mention join   | %s | discovered_for=%s" % (label(row_by_key, k), discovered_list(row_by_key[k].get("discovered_for"))))
    named_state = {}
    for k, who in sorted(NAMED_ROWS.items()):
        named_state[k] = {"in_scope": k in {r["article_key"] for r in in_scope},
                          "under_discovered_for": k in a_keys, "under_mention_join": k in b_keys,
                          "pairs_in_snapshot_any_security": len(pairs_any.get(k, []))}
        L.append("  NAMED %-11s %-10s in scope=%s | under discovered_for=%s | under mention join=%s | snapshot pairs (any security)=%d"
                 % (k, who.split(" ")[0], named_state[k]["in_scope"], named_state[k]["under_discovered_for"],
                    named_state[k]["under_mention_join"], named_state[k]["pairs_in_snapshot_any_security"]))
    result[name] = {"scope": scope, "silver_rows_in_scope": len(in_scope), "discovered_for": len(a_keys),
                    "mention_join": len(b_keys), "both": len(both), "only_discovered_for": only_a,
                    "only_mention_join": only_b, "unjoined_pairs": len(unjoined), "named": named_state}


def main():
    L = ["AC3 - query by company: MENTION JOIN vs discovered_for, side by side (S3 GET/LIST only; nothing written)"]
    result = {}
    key, nparts, mentions = newest_mention_snapshot()
    L.append("gold article_security_mention: newest snapshot s3://%s/%s (%d snapshot part(s) under the prefix)" % (C.BUCKET, key, nparts))
    sec_pairs = [p for p in mentions if p["security_key"] == C.SECURITY]
    L.append("mention snapshot: %d pairs, %d articles, %d securities; pairs for %s: %d (%s)" % (
        len(mentions), len({p["article_key"] for p in mentions}), len({p["security_key"] for p in mentions}), C.SECURITY, len(sec_pairs),
        ", ".join("%s=%d" % kv for kv in sorted(collections.Counter(p["publisher"] for p in sec_pairs).items())) or "none"))
    stamp = re.search(r"part-(\d{8}T\d{6}Z)", key).group(1)
    snapshot_at = datetime.datetime.strptime(stamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
    L.append("snapshot build stamp (part name): %s" % snapshot_at.isoformat())
    pairs_any = collections.defaultdict(list)
    for p in mentions:
        pairs_any[p["article_key"]].append(p["security_key"])
    silver_all = []
    per_pub = {}
    for pub, st in C.PUBLISHERS:
        n = 0
        for _pk, rows in C.silver_parts(st):
            for r in rows:
                silver_all.append(r)
                n += 1
        per_pub[pub] = n
    L.append("served silver article rows read (all versions, all days): %d (%s)" % (len(silver_all), ", ".join("%s=%d" % kv for kv in sorted(per_pub.items()))))
    result["snapshot"] = {"key": key, "pairs": len(mentions), "pairs_for_security": len(sec_pairs), "silver_rows": len(silver_all)}
    compare("day_2026_09_23", silver_all, mentions, pairs_any, DAY, L, result, snapshot_at)
    compare("whole_series", silver_all, mentions, pairs_any, None, L, result, snapshot_at)
    C.emit("ac3", "\n".join(L), result)


if __name__ == "__main__":
    main()
