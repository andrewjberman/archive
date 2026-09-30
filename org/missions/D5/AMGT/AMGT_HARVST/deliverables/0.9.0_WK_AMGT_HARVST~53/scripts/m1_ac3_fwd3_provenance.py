"""HVST-m-1 AC3 - FWD-3 MEASURED: per publisher, the discovery record every stored article carries
(LIST or SEARCH, the words, the position) and the dedupe evidence the store holds. READ-ONLY
(list/get). Measures; grades nothing.

Mapping used for LIST vs SEARCH (lib/opal_data_harvest/publishers.py _discovery(): the rung name the
collector wrote): retrieval_rung 'symbol_listing' = the publisher's own list for that symbol (LIST);
'name_search' = a search on the company name (SEARCH). Any other/absent rung = UNSTATED.
"""

import m1_common as C

RUNG_KIND = {"symbol_listing": "LIST", "name_search": "SEARCH"}


def present(v):
    return v is not None and str(v) != ""


def main():
    lines = ["FWD-3 MEASURED (read-only; discovery provenance and dedupe evidence over s3://%s/)" % C.BUCKET]
    result = {}
    for pub, store in C.PUBLISHERS:
        lines.append("")
        lines.append("=== publisher %s ===" % pub)
        arts = C.bronze_articles(store)
        silver, unreadable = C.silver_row_dicts(store)
        n = len(silver)
        lines.append("bronze article objects: %d; silver article rows (the stored articles carrying a discovery record): %d (unreadable parts %d)" % (len(arts), n, len(unreadable)))
        bronze_with_silver = set(r.get("bronze_key") for _p, r, _c in silver)
        lost = [k for k, _ in arts if k not in bronze_with_silver]
        lines.append("    bronze article objects with NO silver row, hence no discovery record anywhere in the store: %d of %d" % (len(lost), len(arts)))
        kinds = C.Counter(RUNG_KIND.get(r.get("retrieval_rung"), "UNSTATED") for _p, r, _c in silver)
        lines.append("    discovery kind over %d silver rows: %s" % (n, C.counter_line(kinds)))
        modes = C.Counter(str(r.get("retrieval_mode")) for _p, r, _c in silver)
        lines.append("    retrieval_mode: " + C.counter_line(modes))
        per_kind = {}
        for kind in sorted(kinds):
            rows = [r for _p, r, _c in silver if RUNG_KIND.get(r.get("retrieval_rung"), "UNSTATED") == kind]
            k = len(rows)
            words = sum(1 for r in rows if present(r.get("search_query")))
            rank = sum(1 for r in rows if present(r.get("search_rank")))
            page = sum(1 for r in rows if present(r.get("search_page")))
            both = sum(1 for r in rows if present(r.get("search_rank")) and present(r.get("search_page")))
            dfor = sum(1 for r in rows if present(r.get("discovered_for")))
            first = sum(1 for r in rows if present(r.get("first_discovered_at")))
            lines.append("    %s (%d rows): search words present %d / absent %d; result position (rank) present %d / absent %d; page present %d / absent %d; rank AND page %d / %d; discovered_for present %d / %d; first_discovered_at present %d / %d" % (
                kind, k, words, k - words, rank, k - rank, page, k - page, both, k, dfor, k, first, k))
            per_kind[kind] = {"rows": k, "words_present": words, "rank_present": rank, "page_present": page, "both": both}
        by_mode = C.Counter((str(r.get("retrieval_mode")), RUNG_KIND.get(r.get("retrieval_rung"), "UNSTATED"),
                             present(r.get("search_rank")) and present(r.get("search_page"))) for _p, r, _c in silver)
        lines.append("    (retrieval_mode, kind, has rank+page): " + C.counter_line({"%s/%s/%s" % k: v for k, v in by_mode.items()}))

        # dedupe evidence
        by_key = {}
        for pk, r, _c in silver:
            by_key.setdefault(r.get("article_key"), []).append((pk, r))
        dups = {k: v for k, v in by_key.items() if len(v) > 1}
        lines.append("DEDUPE - silver rows %d over %d distinct article_key; article_keys with >1 silver row (duplicate keys across runs/parts): %d" % (n, len(by_key), len(dups)))
        same_hash = 0
        diff_hash = 0
        same_day = 0
        for k, v in dups.items():
            hs = set(r.get("record_hash") for _pk, r in v)
            if len(hs) == 1:
                same_hash += 1
            else:
                diff_hash += 1
            days = C.Counter(str(r.get("fetched_at"))[:10] for _pk, r in v)
            stamps = set(r.get("run_stamp") for _pk, r in v)
            if any(c > 1 for c in days.values()) and len(stamps) > 1:
                same_day += 1
        lines.append("    of those: identical record_hash (an unchanged row written again) %d; differing record_hash %d" % (same_hash, diff_hash))
        lines.append("    article_keys fetched in >1 distinct run_stamp on the same UTC date (a same-day re-fetch of an article already held, derived from silver fetched_at, NOT from run records): %d of %d distinct keys" % (same_day, len(by_key)))
        for k, v in list(dups.items())[:6]:
            lines.append("      dup %s: %s" % (k, "; ".join("%s run=%s hash=%s" % (pk.rsplit("/", 1)[-1], r.get("run_stamp"), str(r.get("record_hash"))[:8]) for pk, r in v)))
        # bronze duplicates: >1 object under one article_hash prefix
        per_hash = C.Counter(k.split("/")[4] for k, _s in arts)
        multi = {h: c for h, c in per_hash.items() if c > 1}
        lines.append("    bronze article_hash partitions with >1 object (the same article fetched again): %d of %d partitions" % (len(multi), len(per_hash)))
        result[pub] = {"bronze": len(arts), "silver_rows": n, "no_silver_row": len(lost), "kinds": dict(kinds),
                       "per_kind": per_kind, "distinct_article_keys": len(by_key), "dup_keys": len(dups),
                       "dup_same_hash": same_hash, "dup_diff_hash": diff_hash, "same_day_multi_run": same_day,
                       "bronze_multi_object_hashes": len(multi)}

    # run records: does the store hold any?
    lines.append("")
    lines.append("RUN RECORDS: a same-day re-run's 'fetched an article already held' verdict needs a run record (fetch/skip counts per run).")
    run_like = []
    for top in ("amgt", "issuer-site", "lib", "publications", "publication-links", "raw", "derived"):
        for key, _s in C.list_keys(top + "/"):
            low = key.lower()
            if any(t in low for t in ("run_record", "run-record", "runrecord", "/runs/", "run_manifest", "harvest_run")):
                run_like.append(key)
    for pub, store in C.PUBLISHERS:
        for key, _s in C.list_keys(store + "/harvest/"):
            low = key.lower()
            if any(t in low for t in ("run_record", "run-record", "runrecord", "/runs/", "run_manifest", "harvest_run")):
                run_like.append(key)
    lines.append("    keys matching a run-record name across the harvest prefixes searched (%d prefixes): %d" % (12, len(run_like)))
    lines.append("NOT MEASURABLE HERE: whether a same-day re-run fetched an already-held article - the store holds no run record (0 keys named as one); the collector's own run log is not in the bucket. The silver-derived line above is the only same-day evidence available and is not a run record.")
    C.emit("ac3", "\n".join(lines), result)


if __name__ == "__main__":
    main()
