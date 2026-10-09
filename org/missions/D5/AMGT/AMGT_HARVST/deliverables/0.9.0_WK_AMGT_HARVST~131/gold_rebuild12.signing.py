"""HARVST served gold rebuild #12 -- THE SIGNING DRY RUN (worker cell HVST-bs-5, NO WRITE).

Rebuild #12 serves R30 (HVST-br-1's capital-initial ALIAS rule). The list does NOT move: both the served and the proposed list
are rebuild #11's file `0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json`. This builds mention and daily with that file
and `--as-of 2026-10-08`, through the builders' own code and the capturing client, against the SERVED rebuild #11 parts as the
BEFORE (it refuses any other baseline), and applies `gold_rebuild12_rule.rule`. A removal counts in the R30 class only by
br-1's own classifier (`br1_census.mentions`): counted under the pre-R30 rule, not under R30. Every S3 access is a GET or a
LIST through a guard that refuses and counts any write call. Writes `gold_rebuild12.signing.json` and
`REBUILD12_REMOVED_SAMPLE.md`; stdout is `gold_rebuild12.signing.out`.
Run from the worktree root: `PYTHONPATH=. python <this file>`.
"""
import datetime
import importlib.util
import io
import json
import os
import pickle
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32C = os.path.join(PARENT, "2.0.0_SA_COO_H", "round32", "checks")
W129 = os.path.join(PARENT, "0.9.0_WK_AMGT_HARVST~129")
W126 = os.path.join(PARENT, "0.9.0_WK_AMGT_HARVST~126")
sys.path.insert(0, R32C)
sys.path.insert(0, HERE)
sys.path.insert(0, W126)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

import br1_census as br1  # noqa: E402  (br-1's own classifier: br1.mentions)
import gold_rebuild12_rule as r12  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

LIST_FILE = os.path.join(W129, "securities.universe.r75.json")
OUT = os.path.join(HERE, "gold_rebuild12.signing.json")
SAMPLE = os.path.join(HERE, "REBUILD12_REMOVED_SAMPLE.md")
AS_OF = datetime.date(2026, 10, 8)
EXPECT_M = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261009T045809Z.parquet"
EXPECT_D = "amgt/harvest/gold/chatter_daily/date=2026-10-08/part-20261009T061012Z.parquet"
CENSUS_NOTE = "br-1 census: 280 of 48,358 served"
WRITE_CALLS = {"put_object", "delete_object", "delete_objects", "copy_object", "upload_file", "upload_fileobj",
               "create_multipart_upload", "upload_part", "complete_multipart_upload", "put_object_acl",
               "put_object_tagging", "delete_object_tagging", "restore_object", "copy"}


class ReadOnlyGuard:
    """Wraps the real S3 client: any write-class call is REFUSED and counted (blocked), never sent."""

    def __init__(self, real):
        self._real = real
        self.blocked = 0

    def __getattr__(self, name):
        if name in WRITE_CALLS:
            def refuse(*a, **kw):
                self.blocked += 1
                raise RuntimeError("READ-ONLY dry run: %s refused" % name)
            return refuse
        return getattr(self._real, name)


def newest_key(client, table):
    """The key `_latest_gold_snapshot_rows` reads: same prefix, same sort (a LIST, read-only)."""
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]


def silver_hashes(rows, client):
    from lib.opal_data_harvest import harvest_grammar as hg
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",),
                                                client=client).items():
            result[key] = srow.get("record_hash")
    return result


def pub_day(row):
    value = row.get("published_utc")
    return value.isoformat()[:10] if value is not None else ""


def cell(value):
    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")


def log(msg):
    sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), msg))
    sys.stderr.flush()


def done(puts, reasons_text):
    print("RULE (rebuild #12): BREAKS: %s" % reasons_text)
    print("PUTS SENT %d" % puts)


def main():
    guard = ReadOnlyGuard(store._default_client())
    store._default_client = lambda: guard
    proposed = json.load(open(LIST_FILE, encoding="utf-8"))
    served_list = json.load(open(LIST_FILE, encoding="utf-8"))
    securities = {s["security_key"]: s for s in proposed}
    print("LIST FILE: %s (%d securities); served list == proposed list (the list does not move)" % (
        os.path.relpath(LIST_FILE, os.path.join(HERE, *[".."] * 7)).replace("\\", "/"), len(proposed)))
    assert pg._CAPITAL_INITIAL_ALIAS_RULE is True, "publication_gold R30 flag is not on at HEAD"
    mkey_served = newest_key(guard, pg.GOLD_TABLE)
    dkey_served = newest_key(guard, pg.GOLD_DAILY_TABLE)
    print("SERVED BASELINE: %s, %s" % (mkey_served, dkey_served))
    sys.stdout.flush()
    if (mkey_served, dkey_served) != (EXPECT_M, EXPECT_D):
        done(guard.blocked, "served baseline %s, %s is not rebuild #11's parts (%s, %s); REFUSED, nothing built" % (
            mkey_served, dkey_served, EXPECT_M, EXPECT_D))
        return 1

    ck = os.path.join(HERE, "..", "..", "..", "..", "..", "..", "..", ".scratch", "r12_ckpt_build.pkl")
    ck = os.path.abspath(ck)
    if os.path.exists(ck):
        state = pickle.load(open(ck, "rb"))
        log("RESUMED the captured build from %s" % ck)
    else:
        log("reading served parts")
        served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=guard)
        served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE, client=guard)
        log("build_mention")
        cm = sg.CapturingClient(guard)
        pg.build_mention(proposed, AS_OF, client=cm)
        (mkey, mbody), = cm.puts.items()
        mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
        log("build_daily")
        orig = pg._latest_gold_snapshot_rows
        pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == pg.GOLD_TABLE else orig(table, client=client)
        cd = sg.CapturingClient(guard)
        try:
            pg.build_daily(proposed, AS_OF, client=cd)
        finally:
            pg._latest_gold_snapshot_rows = orig
        (dkey, dbody), = cd.puts.items()
        state = dict(served_m=served_m, served_d=served_d, mkey=mkey, mbody=mbody, dkey=dkey, dbody=dbody,
                     sent=cm.sent + cd.sent)
        pickle.dump(state, open(ck, "wb"))
        log("checkpoint written")
    served_m, served_d = state["served_m"], state["served_d"]
    mkey, mbody, dkey, dbody = state["mkey"], state["mbody"], state["dkey"], state["dbody"]
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()

    om = {(r["article_key"], r["security_key"]): r for r in served_m}
    nm = {(r["article_key"], r["security_key"]): r for r in mention}
    gone = [k for k in om if k not in nm]
    own_changed = [k for k in nm if k in om and r12.r8._dump(nm[k]) != r12.r8._dump(om[k])
                   and (r12.r8._fields(om[k], nm[k]) & r12.r8.OWN_FIELDS)]
    need = {k[0] for k in gone} | {k[0] for k in own_changed}
    print("CLASSIFYING: %d gone pair(s), %d kept pair(s) with own-field changes, over %d article(s)" % (
        len(gone), len(own_changed), len(need)))
    sys.stdout.flush()
    articles = {}
    log("classifier: reading silver")
    for article in pg._iter_latest_articles(client=guard):
        if article.get("article_key") in need:
            articles[article["article_key"]] = article
    log("classifier: silver read, %d article(s)" % len(articles))
    missing = sorted(need - set(articles))
    r30_class, r30_partial, no_security = set(), set(), []
    for k in gone:
        article, sec = articles.get(k[0]), securities.get(k[1])
        if article is None or sec is None:
            no_security.append(k)
            continue
        if br1.mentions(article, sec, False) and not br1.mentions(article, sec, True):
            r30_class.add(k)
    for k in own_changed:
        article, sec = articles.get(k[0]), securities.get(k[1])
        if article is None or sec is None:
            continue
        before, after = br1.mentions(article, sec, False), br1.mentions(article, sec, True)
        if before > after > 0:
            r30_partial.add(k)

    log("rule")
    v = r12.rule(served_m, served_d, mention, daily, served_list, proposed, silver_hashes(mention, guard), AS_OF,
                 r30_class=r30_class, r30_partial=r30_partial)
    puts = guard.blocked + state["sent"]

    print("AS OF %s; built mention key %s (%d bytes), daily key %s (%d bytes) -- CAPTURED, NOT WRITTEN" % (
        AS_OF, mkey, len(mbody), dkey, len(dbody)))
    print("TABLE           served    built     gone    added  changed")
    print("mention  %12d %8d %8d %8d %8d   changed by class %s, UNEXPLAINED %d %s" % (
        v["mention_served"], v["mention_built"], v["mention_gone"], v["mention_added"], v["mention_changed"],
        v["mention_changed_by_class"], v["mention_changed_unexplained"], v["mention_unexplained_fields"]))
    print("daily    %12d %8d %8d %8d %8d   changed by class %s, OTHER %d" % (
        v["daily_served"], v["daily_built"], v["daily_gone"], v["daily_added"], v["daily_changed"],
        v["daily_changed_by_class"], v["daily_other_count"]))
    print("R30 REMOVALS: %d (%s)" % (v["r30_removals"], CENSUS_NOTE))
    print("OUTSIDE R30 CLASS: %d" % v["outside_count"])
    for row in v["outside_rows"]:
        art = articles.get(row["article_key"]) or {}
        print("  OUTSIDE %s | %s | %s | match_forms %s | %s | %s" % (
            row["article_key"], row["security_key"], cell(art.get("title") or
                                                         (om.get((row["article_key"], row["security_key"])) or {}).get("title")),
            row["match_forms"], row["kind"], row["why"]))
    if v["mention_added"]:
        print("MENTION ADDED (reported, silver grown since the served build; not a rule reason): %d over %s" % (
            v["mention_added"], v["mention_added_by_security"]))
    if missing or no_security:
        print("CLASSIFIER INPUT MISSING: articles not in silver %s; gone pairs without article or list security %s" % (
            missing[:20], no_security[:20]))
    for key, fields in list(v["daily_other"].items())[:20]:
        print("  OTHER %s fields %s" % (key, fields))

    per_sec = {}
    for sec in sorted(v["removed_by_security"]):
        served_n = sum(1 for k in om if k[1] == sec)
        built_n = sum(1 for k in nm if k[1] == sec)
        per_sec[sec] = {"served": served_n, "built": built_n, "removed": v["removed_by_security"][sec]}
        print("%s: served %d, built %d, removed %d" % (sec, served_n, built_n, v["removed_by_security"][sec]))

    reasons = list(v["reasons"])
    if puts:
        reasons.append("%d put(s) sent" % puts)
    if missing or no_security:
        reasons.append("classifier input missing for %d article(s) / %d gone pair(s)" % (len(missing), len(no_security)))
    holds = not reasons
    print("RULE (rebuild #12): %s" % ("HOLDS" if holds else "BREAKS: " + "; ".join(reasons)))

    out = dict(v, measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), as_of=str(AS_OF),
               served_mention_key=mkey_served, served_daily_key=dkey_served, baseline_ok=True, puts_sent=puts,
               built_mention_key=mkey, built_daily_key=dkey, mention_bytes=len(mbody), daily_bytes=len(dbody),
               per_security=per_sec, rule_holds=holds, all_reasons=reasons, census_note=CENSUS_NOTE)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)

    removed = sorted(((k[1], k[0]) for k in r30_class if k in set(gone)))
    k_step = max(1, len(removed) // 30)
    picks = [removed[i * k_step] for i in range(30) if i * k_step < len(removed)]
    lines = ["# REBUILD12_REMOVED_SAMPLE -- gold rebuild #12 signing dry run (HVST-bs-5)", "",
             "Served baseline: `%s`, `%s`. Built (captured, not written) as of %s." % (mkey_served, dkey_served, AS_OF),
             "Every removed pair (%d), ordered by (security_key ascending, article_key ascending); every k-th with "
             "k = floor(%d / 30) = %d, starting at the first: %d pairs. Rows are the SERVED row. No verdict, no grade: "
             "`3.0.0_SA_CVO` grades them after serve." % (len(removed), len(removed), k_step, len(picks)), "",
             "| # | security_key | article_key | date | publisher | title | match_forms |", "|---|---|---|---|---|---|---|"]
    for i, (sec, art) in enumerate(picks, 1):
        r = om[(art, sec)]
        lines.append("| %d | %s | %s | %s | %s | %s | %s |" % (
            i, sec, cell(art), pub_day(r), cell(r.get("publisher")), cell(r.get("title")),
            cell(json.dumps(list(r.get("match_forms") or []), ensure_ascii=True))))
    with io.open(SAMPLE, "w", encoding="ascii", errors="backslashreplace", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("PUTS SENT %d" % puts)
    return 0 if holds else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        log("EXIT %r" % (exc,))
        raise
