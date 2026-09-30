"""HVST-m-1 AC1 - FWD-1 MEASURED: bronze article objects (and the listing pages that found them)
re-read from s3://opal-data-harvest/ and compared byte-exact against the sha256 RECORDED at ingest
(object metadata `document-sha256`, written by lib/research/harvest/store.py bronze_put). The hash
compared is the recorded one; the reader computes only the fresh digest of the bytes it re-reads.
READ-ONLY: list/head/get only. Measures; grades nothing.
"""

import m1_common as C


def hash_check(key):
    body, meta = C.get(key)
    if body is None:
        return {"key": key, "cat": "unreadable", "detail": meta, "form": "unreadable"}
    rec = meta.get("document-sha256")
    form = C.received_form(meta)
    if not rec:
        return {"key": key, "cat": "no recorded hash", "form": form, "bytes": len(body)}
    cat = "matched" if C.sha256(body) == rec else "mismatched"
    return {"key": key, "cat": cat, "form": form, "bytes": len(body)}


def tally(rows):
    cats = C.Counter(r["cat"] for r in rows)
    return {k: cats.get(k, 0) for k in ("matched", "mismatched", "no recorded hash", "unreadable")}


def fmt(t, n):
    return "matched %d / mismatched %d / no recorded hash %d / unreadable %d  (denominator %d)" % (
        t["matched"], t["mismatched"], t["no recorded hash"], t["unreadable"], n)


def main():
    lines = []
    result = {"validation_security": C.VALIDATION_SECURITY, "publishers": {}}
    lines.append("FWD-1 MEASURED (read-only re-read of s3://%s/; compared to document-sha256 recorded at ingest)" % C.BUCKET)
    all_rows = []
    for pub, store in C.PUBLISHERS:
        lines.append("")
        lines.append("=== publisher %s (store prefix %s/harvest/) ===" % (pub, store))
        arts = C.bronze_articles(store)
        checks = [hash_check(k) for k, _ in arts]
        all_rows += checks
        n = len(checks)
        lines.append("ARTICLE bronze objects re-read: " + fmt(tally(checks), n))
        forms = C.Counter((r["form"], r["cat"]) for r in checks)
        for (form, cat), v in sorted(forms.items()):
            lines.append("    by received-form label [%s]: %s = %d" % (form, cat, v))
        lines.append("    (received-form is the ingest label in object metadata: as_received = response bytes; "
                     "normalised_record = a record the collector rebuilt, so the bytes compared are the stored record, not the publisher's response)")

        silver, unreadable = C.silver_row_dicts(store)
        if unreadable:
            lines.append("    silver parts unreadable: %s" % unreadable)
        by_bronze = {}
        for _pk, row, _cols in silver:
            by_bronze.setdefault(row.get("bronze_key"), []).append(row)
        art_keys = set(k for k, _ in arts)
        no_silver = [k for k in art_keys if k not in by_bronze]
        lines.append("    bronze articles with no silver row pointing at them (unattributable to a security): %d of %d" % (len(no_silver), n))
        silver_orphans = [k for k in by_bronze if k not in art_keys]
        lines.append("    silver rows whose bronze_key names no listed bronze article object: %d keys of %d distinct bronze_keys" % (len(silver_orphans), len(by_bronze)))

        # validation security line
        val_keys = set()
        for _pk, row, _cols in silver:
            if C.VALIDATION_SECURITY in C.discovered_for_list(row.get("discovered_for")):
                val_keys.add(row.get("bronze_key"))
        val_checks = [r for r in checks if r["key"] in val_keys]
        lines.append("VALIDATION SECURITY %s articles (silver discovered_for contains it): " % C.VALIDATION_SECURITY
                     + (fmt(tally(val_checks), len(val_checks)) if val_checks else "0 articles for this publisher (denominator 0)"))

        # listing pages
        listing_objs = C.list_keys("%s/harvest/bronze/news_listing/" % store)
        hits, hit_unreadable = C.silver_row_dicts(store, "listing_hit")
        explicit = 0
        for _pk, row, cols in silver:
            if any("listing" in c.lower() for c in cols) and any("news_listing" in str(row.get(c, "")) for c in cols):
                explicit += 1
        lines.append("LISTING pages: bronze news_listing objects in store for %s: %d; silver listing_hit rows: %d (unreadable parts %d)" % (
            pub, len(listing_objs), len(hits), len(hit_unreadable)))
        lines.append("    articles whose own record (silver row) names a listing object explicitly (a column or value naming news_listing): %d of %d silver rows" % (explicit, len(silver)))
        # derived join by discovery position: (search_query, search_page, search_rank)
        pos = {}
        for _pk, row, _cols in hits:
            pos.setdefault((row.get("search_query"), row.get("search_page"), row.get("search_rank")), []).append(row)
        linked = []
        idcheck = 0
        for _pk, row, _cols in silver:
            pk = (row.get("search_query"), row.get("search_page"), row.get("search_rank"))
            if pk[2] is None or pk[1] is None:
                continue
            m = pos.get(pk)
            if m:
                linked.append((row, m))
                if any(h.get("article_id") and str(h.get("article_id")) == str(row.get("article_id")) for h in m):
                    idcheck += 1
        lines.append("    DERIVED join (reader-built, NOT a recorded link): silver article (search_query, search_page, search_rank) = listing_hit position: "
                     "%d of %d silver articles matched a listing_hit row (%d of those also agree on article_id)" % (len(linked), len(silver), idcheck))
        no_pos = sum(1 for _pk, row, _cols in silver if row.get("search_rank") is None or row.get("search_page") is None)
        lines.append("    silver articles with no recorded listing position (search_rank or search_page absent): %d of %d -> no listing object can be linked" % (no_pos, len(silver)))
        linked_listing_keys = sorted(set(h["bronze_key"] for _r, m in linked for h in m))
        lchecks = [hash_check(k) for k in linked_listing_keys]
        lines.append("    listing objects reached by the derived join, re-read: " + (fmt(tally(lchecks), len(lchecks)) if lchecks else "0 objects (denominator 0)"))
        # every listing object in the store
        achecks = [hash_check(k) for k, _ in listing_objs]
        all_rows += achecks
        lines.append("    ALL bronze news_listing objects in store, re-read: " + (fmt(tally(achecks), len(achecks)) if achecks else "0 objects (this publisher's store holds no listing pages)"))
        no_listing = sum(1 for _pk, row, _cols in silver) - len(linked)
        lines.append("    articles with NO linked listing object (recorded link: none exists; derived join: unmatched): recorded-link basis %d of %d; derived-join basis %d of %d" % (
            len(silver), len(silver), no_listing, len(silver)))
        result["publishers"][pub] = {
            "article_objects": n, "article_tally": tally(checks), "no_silver_row": len(no_silver),
            "validation_articles": len(val_checks), "validation_tally": tally(val_checks),
            "listing_objects_in_store": len(listing_objs), "listing_tally": tally(achecks),
            "silver_articles": len(silver), "explicit_listing_link": explicit,
            "derived_join_matched": len(linked), "derived_join_id_agree": idcheck,
            "received_form": {"%s|%s" % k: v for k, v in forms.items()},
        }

    # non-article objects excluded from the denominator, printed so the exclusion is visible
    lines.append("")
    lines.append("=== objects EXCLUDED from the article denominator (printed, not hidden) ===")
    for store in ("seeking-alpha", "bloomberg"):
        cls = C.Counter()
        for key, _s in C.list_keys("%s/harvest/bronze/" % store):
            parts = key.split("/")
            cls[parts[3]] += 1
        lines.append("%s bronze classes (all objects): %s" % (store, C.counter_line(cls)))
    sa_other = []
    for cls in ("analysis", "news", "report", "symbol"):
        sa_other += [k for k, _ in C.list_keys("seeking-alpha/harvest/bronze/%s/" % cls)]
    sc = [hash_check(k) for k in sa_other]
    all_rows += sc
    lines.append("sa per-security non-article bronze (analysis/news/report/symbol) re-read: " + fmt(tally(sc), len(sc)))
    lines.append("bloomberg non-article bronze (bestdata/histdata/refdata/identity/exec_officers/histdata_daily_px) is market/reference data, not publisher articles: counted above, not re-read.")
    lines.append("")
    lines.append("TOTAL objects re-read this run (articles + listings + sa per-security): " + fmt(tally(all_rows), len(all_rows)))
    lines.append("NOT MEASURABLE HERE: a re-read of the PUBLISHER'S ORIGINAL response for the normalised_record objects - the response bytes are not held anywhere in the store (only response_sha256 inside the record), and no vendor call is permitted; 'byte for byte as received' is therefore measurable only for the as_received-labelled objects.")
    lines.append("NOT MEASURABLE HERE: a recorded link from an article to the listing page that found it - no article field carries a listing object key; the derived join above is the reader's, not the store's.")
    C.emit("ac1", "\n".join(lines), result)


if __name__ == "__main__":
    main()
