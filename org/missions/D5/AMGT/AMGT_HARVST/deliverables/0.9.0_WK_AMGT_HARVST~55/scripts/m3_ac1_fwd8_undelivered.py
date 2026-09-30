"""HVST-m-3 AC1 -- FWD-8: the desktop's collected articles/links against the served store. READ-ONLY.

Inventory source: the desktop harvester's progress.sqlite3 (opened mode=ro) under the MAIN workspace's
.runtime/opal-data-harvest/ (derived from `git worktree list`, never typed). Each inventory article is
matched to the store by ARTICLE KEY (bronze partition article_hash=sha256(article_key); silver
article_key) and by URL (silver url). Nothing is graded.
"""
import collections
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m3_common as C  # noqa: E402

PUB_ORDER = ["sa", "bbg", "barrons", "wsj", "ft"]


def norm_url(u):
    if not u:
        return None
    u = u.strip()
    for p in ("https://", "http://"):
        if u.startswith(p):
            u = u[len(p):]
    host, _, rest = u.partition("/")
    if host.startswith("www."):
        host = host[4:]
    return (host + "/" + rest).rstrip("/").lower() if rest else host.lower()


def main():
    print("== HVST-m-3 AC1: FWD-8 collected-but-undelivered desktop articles vs the served store (READ-ONLY) ==")
    rt = C.runtime_root()
    db = os.path.join(rt, "progress.sqlite3") if rt else None
    searched = [db] if db else []
    print("main workspace root (derived from git worktree list): %s" % C.a(C.main_root()))
    print("paths searched for an inventory: %s" % C.a(searched))
    if not db or not os.path.isfile(db):
        print("NOT MEASURABLE HERE: no desktop progress.sqlite3 at the derived runtime root; paths searched above.")
        return 0
    print("inventory source: %s (opened mode=ro; size %d bytes)" % (C.a(db), os.path.getsize(db)))
    con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)

    objs = con.execute("select article_key,publisher,article_id,url,path,body_sha256 from article_objects").fetchall()
    links = con.execute("select security_key,article_key,path from article_links").fetchall()
    outbox = con.execute("select object_key,status from upload_outbox").fetchall()
    raw_outbox = con.execute("select publisher,status,count(*) from harvest_raw_outbox group by 1,2").fetchall()

    print("\n-- inventory counts (table -> rows) --")
    for t in ("article_objects", "article_aliases", "article_links", "articles", "upload_outbox",
              "harvest_raw_outbox", "harvest_listing_outbox"):
        print("  %-24s %d" % (t, con.execute("select count(*) from %s" % t).fetchone()[0]))
    ob = collections.Counter((k.split("/")[0], s) for k, s in outbox)
    print("  legacy upload_outbox by (prefix,status): %s" % C.a(dict(ob)))
    print("  harvest_raw_outbox by (publisher,status): %s" % C.a(raw_outbox))
    print("  NOTE: upload-legacy (HVST-h-9) reads the legacy tables read-only and never marks upload_outbox, so a")
    print("        'pending' outbox row is NOT evidence of an undelivered article; the store match below is.")

    by_pub = collections.Counter(o[1] for o in objs)
    print("\n-- bodies (article_objects) by publisher: %s  total %d" %
          ({p: by_pub[p] for p in PUB_ORDER if p in by_pub}, len(objs)))
    files_present = sum(1 for o in objs if o[4] and os.path.isfile(o[4]))
    print("   record files present on this desktop: %d of %d" % (files_present, len(objs)))
    link_pub = collections.Counter(lk[1].split(":", 1)[0] for lk in links)
    print("-- links (article_links) by publisher: %s  total %d" %
          ({p: link_pub[p] for p in PUB_ORDER if p in link_pub}, len(links)))

    c = C.client()
    bronze = {}
    silver = {}
    print("\n-- store side (S3 LIST/GET) --")
    for p in PUB_ORDER:
        bronze[p] = C.bronze_objects(c, p)
        silver[p] = C.silver_all_rows(c, p, "article")
        print("  %-8s bronze article partitions %d (objects %d) | silver article rows %d in %d parts" % (
            p, len(bronze[p]), sum(len(v) for v in bronze[p].values()), len(silver[p]),
            len({k for k, _ in silver[p]})))

    silver_by_key = collections.defaultdict(list)
    silver_by_url = collections.defaultdict(list)
    for p in PUB_ORDER:
        for part, row in silver[p]:
            silver_by_key[row.get("article_key")].append((part, row))
            nu = norm_url(row.get("url"))
            if nu:
                silver_by_url[(p, nu)].append(row.get("article_key"))

    print("\n-- per-publisher match of the desktop inventory to the store --")
    hdr = "  %-8s %6s %8s %8s %8s %10s %10s %11s" % (
        "pub", "bodies", "brz_key", "slv_key", "slv_url", "in_store", "NOT_IN", "dup_store")
    print(hdr)
    not_in = []
    dup_bronze = []
    dup_silver_same_hash = []
    dup_silver_diff_hash = []
    mismatch_hash = []
    tot = collections.Counter()
    for p in PUB_ORDER:
        rows = [o for o in objs if o[1] == p]
        n = len(rows)
        bk = sk = su = ins = ni = dp = 0
        for (akey, pub, aid, url, path, sha) in rows:
            h = C.hg.article_hash(pub, aid)
            if akey != "%s:%s" % (pub, aid):
                mismatch_hash.append(akey)
            in_b = h in bronze[p]
            in_s = akey in silver_by_key
            in_u = (p, norm_url(url)) in silver_by_url
            bk += in_b
            sk += in_s
            su += in_u
            if in_b or in_s or in_u:
                ins += 1
            else:
                ni += 1
                not_in.append(akey)
            if in_b and len(bronze[p][h]) > 1:
                dup_bronze.append((akey, len(bronze[p][h])))
            if in_s and len(silver_by_key[akey]) > 1:
                hashes = {r.get("record_hash") for _p, r in silver_by_key[akey]}
                (dup_silver_same_hash if len(hashes) == 1 else dup_silver_diff_hash).append(
                    (akey, len(silver_by_key[akey]), len(hashes)))
            dp += (1 if ((in_b and len(bronze[p][h]) > 1) or (in_s and len(silver_by_key[akey]) > 1)) else 0)
        print("  %-8s %6d %8d %8d %8d %10d %10d %11d" % (p, n, bk, sk, su, ins, ni, dp))
        for k, v in (("bodies", n), ("brz", bk), ("slv", sk), ("url", su), ("in", ins), ("not", ni), ("dup", dp)):
            tot[k] += v
    print("  %-8s %6d %8d %8d %8d %10d %10d %11d" % (
        "TOTAL", tot["bodies"], tot["brz"], tot["slv"], tot["url"], tot["in"], tot["not"], tot["dup"]))
    print("\nINVENTORY ARTICLES NOT IN THE STORE (by key or URL): %d of %d" % (len(not_in), len(objs)))
    for k in not_in:
        print("   not in store: %s" % C.a(k))
    print("article_key != publisher:article_id in the inventory: %d of %d" % (len(mismatch_hash), len(objs)))
    print("DUPLICATES of inventory articles in the store:")
    print("   bronze partitions holding >1 object: %d  %s" % (len(dup_bronze), C.a(dup_bronze[:20])))
    print("   silver article_key in >1 part, SAME record_hash (a re-stored identical row): %d  %s" % (
        len(dup_silver_same_hash), C.a(dup_silver_same_hash[:20])))
    print("   silver article_key in >1 part, DIFFERENT record_hash (a changed row appended): %d  %s" % (
        len(dup_silver_diff_hash), C.a(dup_silver_diff_hash[:20])))

    # links: is the (security, article) pair carried by the store row's discovered_for?
    print("\n-- links (article_links, legacy security keys) against silver discovered_for --")
    lin = lnot_art = lnot_pair = 0
    lpub = collections.defaultdict(lambda: [0, 0, 0])
    for (sec, akey, _path) in links:
        pub = akey.split(":", 1)[0]
        rows = silver_by_key.get(akey)
        if not rows:
            lnot_art += 1
            lpub[pub][1] += 1
            continue
        carried = any(sec in (r.get("discovered_for") or []) for _p, r in rows)
        if carried:
            lin += 1
            lpub[pub][0] += 1
        else:
            lnot_pair += 1
            lpub[pub][2] += 1
    print("  pair carried in silver discovered_for: %d | article in silver but pair absent: %d | article not in silver: %d"
          " | total %d" % (lin, lnot_pair, lnot_art, len(links)))
    for p in PUB_ORDER:
        if p in lpub:
            print("   %-8s carried %d | article not in silver %d | pair absent %d" % (
                p, lpub[p][0], lpub[p][1], lpub[p][2]))
    link_dupe = collections.Counter((s, k) for s, k, _ in links)
    print("  duplicate (security,article) link rows in the inventory: %d" % sum(1 for v in link_dupe.values() if v > 1))

    # store-only articles (informational; not part of the inventory)
    inv_keys = {o[0] for o in objs}
    store_only = collections.Counter()
    silver_keys = set(silver_by_key)
    only = sorted(k for k in silver_keys if k not in inv_keys)
    for k in only:
        store_only[k.split(":", 1)[0]] += 1
    print("\n-- store articles (silver article_key) with NO desktop inventory row, by publisher: %s (total %d of %d silver keys)" % (
        dict(store_only), len(only), len(silver_keys)))

    inv_hashes = {p: {C.hg.article_hash(o[1], o[2]) for o in objs if o[1] == p} for p in PUB_ORDER}
    b_only = {p: len([h for h in bronze[p] if h not in inv_hashes[p]]) for p in PUB_ORDER}
    print("-- bronze article partitions with NO desktop inventory row, by publisher: %s (the SA REST channel's own objects)" % b_only)

    # legacy retiring prefixes in the store, for the denominator
    print("\n-- legacy prefixes in the store (informational) --")
    for pre in ("publications/v1/", "publication-links/v1/"):
        print("  s3://%s/%s objects: %d" % (C.store.HARVEST_BUCKET, pre, len(C.list_keys(c, pre))))
    print("\nEND AC1 (measured, not graded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
