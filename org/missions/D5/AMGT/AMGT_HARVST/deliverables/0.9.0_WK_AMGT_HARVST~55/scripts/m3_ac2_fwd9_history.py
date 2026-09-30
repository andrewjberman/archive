"""HVST-m-3 AC2 -- FWD-9: publication history since the 2026-01-01 floor, per covered security. READ-ONLY.

Reads (S3 LIST/GET only): every silver article part (all rows, no collapse), the newest served
article_security_mention part, the newest served chatter_daily part, and searches for a stored
backfill plan / run record. First/last ARTICLE dates come from published_utc on articles, never from
the daily table's row range (which holds every day by construction). Nothing is graded.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m3_common as C  # noqa: E402

pg = C.pg
PUBS = sorted(C.SOURCES)


def newest_part(c, table):
    prefix = C.store.table_prefix("amgt", "gold", table)
    parts = [o for o in C.list_keys(c, prefix) if o["key"].endswith(".parquet")]
    parts.sort(key=lambda o: (pg._DATE_PARTITION_RE.search(o["key"]).group(1), o["key"]))
    return parts


def fmt(d):
    return d.isoformat() if d else "-"


def main():
    c = C.client()
    secs = C.load_universe()
    skeys = [s["security_key"] for s in secs]
    print("== HVST-m-3 AC2: FWD-9 history since %s per covered security (READ-ONLY) ==" % C.FLOOR)
    print("covered denominator: %d securities (%s), Lenovo (992_HK_Equity) first: %s" % (
        len(secs), C.a(C.UNIVERSE.replace(C.REPO, "").lstrip("\\/")), skeys[0] == "992_HK_Equity"))

    # ---------------- silver: every row of every part, per publisher ----------------
    print("\n-- silver article: rows and parts per publisher (no collapse) --")
    all_rows = []
    for p in PUBS:
        rows = C.silver_all_rows(c, p, "article")
        all_rows.extend(rows)
        print("  %-8s rows %d in %d parts" % (p, len(rows), len({k for k, _ in rows})))
    by_key = collections.defaultdict(list)
    for part, row in all_rows:
        by_key[row.get("article_key")].append((part, row))
    latest = {}
    for k, lst in by_key.items():
        latest[k] = max(lst, key=lambda pr: pr[1]["fetched_at"])[1]
    nopub = [k for k, r in latest.items() if r.get("published_utc") is None]
    print("  distinct article_key %d | rows %d | article_key without published_utc: %d" % (
        len(latest), len(all_rows), len(nopub)))
    rmode = collections.Counter(r.get("retrieval_mode") for _p, r in all_rows)
    print("  silver retrieval_mode counts: %s" % C.a(dict(rmode)))

    sil = collections.defaultdict(list)  # security_key -> [published date]
    for art in latest.values():
        for m in pg.mention_rows(art, secs):
            d = C.to_date(m["published_utc"])
            if d is not None:
                sil[m["security_key"]].append(d)

    # ---------------- served mention part ----------------
    mparts = newest_part(c, pg.GOLD_TABLE)
    mkey = mparts[-1]["key"]
    mrows = C.read_parquet_rows(c, mkey)
    print("\n-- served mention: %d parts; newest %s rows %d" % (len(mparts), mkey, len(mrows)))
    srv = collections.defaultdict(list)
    for r in mrows:
        d = C.to_date(r.get("published_utc"))
        if d is not None:
            srv[r["security_key"]].append(d)
    mdup = collections.Counter((r["article_key"], r["security_key"]) for r in mrows)
    print("   duplicate (article_key, security_key) in the newest mention part: %d of %d rows" % (
        sum(1 for v in mdup.values() if v > 1), len(mrows)))

    # ---------------- daily ----------------
    dparts = newest_part(c, pg.GOLD_DAILY_TABLE)
    dkey = dparts[-1]["key"]
    drows = C.read_parquet_rows(c, dkey)
    print("-- served daily: %d parts; newest %s rows %d" % (len(dparts), dkey, len(drows)))
    days = collections.defaultdict(set)
    dcount = collections.Counter()
    with_art = collections.defaultdict(list)
    status = collections.Counter()
    for r in drows:
        days[r["security_key"]].add(r["day"])
        dcount[(r["security_key"], r["day"])] += 1
        status[r.get("data_status")] += 1
        if (r.get("articles_total") or 0) > 0:
            with_art[r["security_key"]].append(r["day"])
    alldays = {d for s in days.values() for d in s}
    print("   daily data_status counts: %s" % C.a(dict(status)))
    print("   daily global day range: %s .. %s | distinct days %d | securities in daily %d" % (
        fmt(min(alldays)), fmt(max(alldays)), len(alldays), len(days)))
    print("   duplicate (security_key, day) rows in the newest daily part: %d" % sum(1 for v in dcount.values() if v > 1))

    # ---------------- per-security table ----------------
    floor = C.FLOOR
    print("\n-- per security: first/last ARTICLE date (silver via the gold mention rule, and served mention part),"
          " floor test, daily missing days --")
    print("  %-22s %5s %-10s %-10s %5s %-10s %-10s %-6s %8s %8s" % (
        "security_key", "s_n", "s_first", "s_last", "v_n", "v_first", "v_last", "floor", "d_days", "d_miss"))
    short = []
    none_ = []
    agree = 0
    miss_tot = 0
    miss_secs = 0
    ok_floor = 0
    for k in skeys:
        sd, vd = sorted(sil.get(k, [])), sorted(srv.get(k, []))
        sf, sl = (sd[0], sd[-1]) if sd else (None, None)
        vf, vl = (vd[0], vd[-1]) if vd else (None, None)
        if (sf, sl, len(sd)) == (vf, vl, len(vd)):
            agree += 1
        first = vf or sf
        if first is None:
            fl = "NOART"
            none_.append(k)
        elif first <= floor:
            fl = "ON/BEF"
            ok_floor += 1
        else:
            fl = "SHORT"
            short.append(k)
        have = days.get(k, set())
        if have:
            expected = set(pg._date_range(floor, max(have)))
            miss = sorted(expected - have)
        else:
            miss = ["ALL"]
        if miss:
            miss_secs += 1
            miss_tot += len(miss) if miss != ["ALL"] else 0
        if sd or vd or k == skeys[0]:
            print("  %-22s %5d %-10s %-10s %5d %-10s %-10s %-6s %8d %8s" % (
                k, len(sd), fmt(sf), fmt(sl), len(vd), fmt(vf), fmt(vl), fl, len(have),
                len(miss) if miss != ["ALL"] else "ALL"))
    print("  (securities with no article in silver or served are not listed above; they are counted next)")

    n = len(skeys)
    with_any = n - len(none_)
    print("\n-- FLOOR RESULT (first ARTICLE date on or before %s) --" % floor)
    print("  covered denominator %d | with at least one article %d | no article at all %d | first on/before floor %d"
          " | first AFTER floor (short) %d" % (n, with_any, len(none_), ok_floor, len(short)))
    print("  SHORT OF THE FLOOR (has articles, first after floor): %d of %d covered: %s" % (
        len(short), n, C.a(short)))
    print("  NO ARTICLE AT ALL (no first date exists): %d of %d covered: %s" % (len(none_), n, C.a(none_)))
    print("  silver-derived (mention rule) vs served-mention agree on (first,last,count): %d of %d securities" % (agree, n))
    allfirst = [min(v) for v in srv.values()] or [None]
    alllast = [max(v) for v in srv.values()] or [None]
    print("  served mention overall article date range: %s .. %s | mention rows %d over %d securities" % (
        fmt(min(allfirst)), fmt(max(alllast)), len(mrows), len(srv)))
    pubfirst = collections.defaultdict(list)
    for r in latest.values():
        d = C.to_date(r.get("published_utc"))
        if d:
            pubfirst[r["publisher"]].append(d)
    print("  silver article published range per publisher (all securities): %s" % C.a(
        {p: (fmt(min(v)), fmt(max(v)), len(v)) for p, v in sorted(pubfirst.items())}))

    print("\n-- DAILY SERIES: is there a row for every day from %s to the security's last day --" % floor)
    print("  securities with >=1 missing day: %d of %d | total missing days across securities: %d" % (
        miss_secs, n, miss_tot))
    lastdays = collections.Counter(max(v) for v in days.values())
    print("  per-security last day (value -> securities): %s" % C.a({fmt(d): v for d, v in sorted(lastdays.items())}))
    print("  Lenovo: rows %d, first day %s, last day %s, days with articles_total>0: %d (first %s, last %s)" % (
        len(days.get("992_HK_Equity", ())), fmt(min(days["992_HK_Equity"])) if days.get("992_HK_Equity") else "-",
        fmt(max(days["992_HK_Equity"])) if days.get("992_HK_Equity") else "-",
        len(with_art.get("992_HK_Equity", [])), fmt(min(with_art["992_HK_Equity"])) if with_art.get("992_HK_Equity") else "-",
        fmt(max(with_art["992_HK_Equity"])) if with_art.get("992_HK_Equity") else "-"))
    print("  NOTE: a daily row exists for every day by construction (dense series); the row range is NOT history."
          " Days carrying an article: total securities with >=1 such day %d of %d" % (len(with_art), n))

    # ---------------- duplicate article keys across runs ----------------
    print("\n-- DUPLICATE ARTICLE KEYS ACROSS RUNS ('running it again adds nothing') --")
    multi = {k: v for k, v in by_key.items() if len(v) > 1}
    same = [k for k, v in multi.items() if len({r['record_hash'] for _p, r in v}) == 1]
    print("  silver article_key held in >1 row: %d of %d distinct keys (identical record_hash: %d; changed: %d)" % (
        len(multi), len(by_key), len(same), len(multi) - len(same)))
    print("  silver rows per run_stamp prefix (date) : %s" % C.a(dict(sorted(collections.Counter(
        (r.get("run_stamp") or "")[:8] for _p, r in all_rows).items()))))
    bdup = 0
    btot = 0
    for p in PUBS:
        b = C.bronze_objects(c, p)
        btot += len(b)
        bdup += sum(1 for v in b.values() if len(v) > 1)
    print("  bronze article partitions holding >1 object: %d of %d partitions" % (bdup, btot))

    # ---------------- plan / run record ----------------
    print("\n-- STORED BACKFILL PLAN OR RUN RECORD (listing pages per publisher printed before a run) --")
    pat = re.compile(r"plan|backfill|listing[_-]?pages|run[_-]?record|pages[_-]?per", re.I)
    scanned = 0
    hits = []
    for page in c.get_paginator("list_objects_v2").paginate(Bucket=C.store.HARVEST_BUCKET):
        for o in page.get("Contents", []) or []:
            scanned += 1
            if pat.search(o["Key"]):
                hits.append(o["Key"])
    print("  S3: %d keys scanned in s3://%s/ (whole bucket); key names matching plan|backfill|listing pages|run record: %d %s" % (
        scanned, C.store.HARVEST_BUCKET, len(hits), C.a(hits[:10])))
    rt = C.runtime_root()
    rt_hits = []
    rt_scanned = 0
    for dp, _dn, fns in os.walk(rt or "."):
        if os.sep + "secrets" in dp or os.sep + "auth" in dp:
            continue
        for fn in fns:
            rt_scanned += 1
            if pat.search(fn):
                rt_hits.append(os.path.join(dp, fn))
    print("  desktop runtime %s: %d file names scanned (auth/ and secrets/ skipped); names matching: %d %s" % (
        C.a(rt), rt_scanned, len(rt_hits), C.a([h.replace(rt, "") for h in rt_hits[:10]])))
    mission = os.path.join(C.REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST")
    txt_hits = []
    m_scanned = 0
    cpat = re.compile(r"listing pages|pages (?:each|per) publisher|pages_planned|plan_pages", re.I)
    own = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    for dp, _dn, fns in os.walk(mission):
        if os.path.abspath(dp).startswith(own):
            continue  # this cell's own outputs are not a source it may read
        for fn in fns:
            if fn.endswith(("_PRD.md", "_DECOMP.md")) or "task-orders" in dp or "brief" in dp or "prd" in dp \
                    or "decompositions" in dp:
                continue
            if not fn.endswith((".txt", ".json", ".md", ".log")):
                continue
            m_scanned += 1
            try:
                with open(os.path.join(dp, fn), "r", encoding="utf-8", errors="replace") as fh:
                    body = fh.read()
            except OSError:
                continue
            if cpat.search(body):
                txt_hits.append(os.path.join(dp, fn).replace(mission, ""))
    print("  repo mission deliverables/ledger (PRD, decomp, task orders, briefs excluded): %d text files scanned; "
          "content naming listing pages per publisher: %d %s" % (m_scanned, len(txt_hits), C.a(txt_hits[:10])))
    plan_files = []
    for dp, _dn, fns in os.walk(os.path.join(mission, "deliverables")):
        for fn in fns:
            if re.search(r"(^|[._-])plan([._-]|$)", fn, re.I) and fn.endswith(".json")                     and "proof_of_spec" not in fn:
                plan_files.append(os.path.join(dp, fn))
    print("  mission deliverables: JSON files named plan: %d %s" % (
        len(plan_files), C.a([f.replace(mission, "") for f in plan_files])))
    import json as _json
    for f in plan_files:
        print("  PLAN RECORD %s" % C.a(f.replace(mission, "")))
        sib = os.path.join(os.path.dirname(f), "lenovo.security.json")
        if os.path.isfile(sib):
            with open(sib, "r", encoding="utf-8") as fh:
                sec = _json.load(fh)
            sec = sec[0] if isinstance(sec, list) and sec else sec
            print("     security file beside it: %s" % C.a({k: sec.get(k) for k in ("security_key", "key", "company", "ticker")}))
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    print("     %s" % C.a(line.strip()))
    covered_by_plan = set()
    for f in plan_files:
        sib = os.path.join(os.path.dirname(f), "lenovo.security.json")
        if os.path.isfile(sib):
            with open(sib, "r", encoding="utf-8") as fh:
                sec = _json.load(fh)
            sec = sec[0] if isinstance(sec, list) and sec else sec
            covered_by_plan.add(sec.get("security_key") or sec.get("key"))
    print("  securities with a stored plan: %d of %d covered: %s" % (len(covered_by_plan & set(skeys)), n, C.a(sorted(covered_by_plan))))
    print("  the `plan` CLI verb exists in lib/opal_data_harvest/__main__.py (prints; no stored output found above)")
    import sqlite3
    db = os.path.join(rt, "progress.sqlite3") if rt else None
    if db and os.path.isfile(db):
        con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)
        lo = con.execute("select publisher,query,page,fetched_at,status from harvest_listing_outbox order by id").fetchall()
        print("  listing pages actually FETCHED and held in the desktop harvest_listing_outbox (not a plan): %d" % len(lo))
        for r in lo:
            print("     %s" % C.a(r))
    if not plan_files and not hits and not rt_hits and not txt_hits:
        print("  RESULT: NOT MEASURABLE HERE -- no stored pre-run listing-page plan or run record was found in the"
              " S3 key names, the desktop runtime file names, or the mission's deliverable/ledger text (paths above).")
    else:
        print("  RESULT: candidate records listed above; inspect them (name match is not content proof).")
    print("\nEND AC2 (measured, not graded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
