"""HARVST served gold rebuild #11 -- THE SIGNING DRY RUN (worker cell HVST-bs-1, NO WRITE).

Rebuild #11 serves the AIG_US_Equity / OMAB_MM_Equity / OMAB_US_Equity list move. This builds mention and daily with the list
FILE `securities.universe.r75.json` (beside this script) and `--as-of 2026-10-08`, through the builders' own code and the
capturing client (PUTS SENT 0), against the SERVED rebuild #10 parts as the BEFORE, and applies `gold_rebuild11_rule.rule`
(served list = round72 r72 file, proposed list = the r75 file, named removals = REBUILD11_NAMED_REMOVALS.json, empty).
`--write-list` first writes the r75 file from `universe_securities.build()` at HEAD. Writes `gold_rebuild11.signing.json` and
`REBUILD11_TITLES.md` (the first ten gone and the first ten added pairs per list-moved security, no verdict).
"""
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R72 = os.path.join(PARENT, "2.0.0_SA_COO_H", "round72")
R32C = os.path.join(PARENT, "2.0.0_SA_COO_H", "round32", "checks")
sys.path.insert(0, R32C)
sys.path.insert(0, HERE)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

import gold_rebuild11_rule as r11  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

SERVED_LIST = os.path.join(R72, "securities.universe.r72.json")
PROPOSED = os.path.join(HERE, "securities.universe.r75.json")
NAMED = os.path.join(HERE, "REBUILD11_NAMED_REMOVALS.json")
OUT = os.path.join(HERE, "gold_rebuild11.signing.json")
TITLES = os.path.join(HERE, "REBUILD11_TITLES.md")
AS_OF = datetime.date(2026, 10, 8)
EXPECT_M = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261008T225527Z.parquet"
EXPECT_D = "amgt/harvest/gold/chatter_daily/date=2026-10-08/part-20261008T232700Z.parquet"


def newest_key(client, table):
    """The key `_latest_gold_snapshot_rows` reads: same prefix, same sort (a LIST, read-only)."""
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    return sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]


def silver_hashes(rows):
    from lib.opal_data_harvest import harvest_grammar as hg
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def pub_day(row):
    value = row.get("published_utc")
    return value.isoformat()[:10] if value is not None else ""


def first_ten(rows):
    """First ten by (published date descending, article key ascending)."""
    by_key = sorted(rows, key=lambda r: r.get("article_key") or "")
    return sorted(by_key, key=lambda r: pub_day(r), reverse=True)[:10]


def cell(value):
    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")


def main():
    built_now, _summary = us.build()
    if "--write-list" in sys.argv[1:]:
        with io.open(PROPOSED, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(built_now, handle, indent=1, sort_keys=True)
        print("LIST FILE WRITTEN: %d securities" % len(built_now))
    served_list = json.load(open(SERVED_LIST, encoding="utf-8"))
    proposed = json.load(open(PROPOSED, encoding="utf-8"))
    list_equal = json.dumps(built_now, sort_keys=True) == json.dumps(proposed, sort_keys=True)
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in proposed}
    moved_keys = sorted(k for k in set(old) | set(new)
                        if json.dumps(old.get(k), sort_keys=True) != json.dumps(new.get(k), sort_keys=True))

    real = store._default_client()
    mkey_served = newest_key(real, pg.GOLD_TABLE)
    dkey_served = newest_key(real, pg.GOLD_DAILY_TABLE)
    print("SERVED BASELINE: %s, %s" % (mkey_served, dkey_served))
    print("LIST FILE EQUAL TO build() AT HEAD: %s" % list_equal)
    print("LIST MOVED: %s" % ", ".join(moved_keys))
    sys.stdout.flush()
    baseline_ok = (mkey_served == EXPECT_M and dkey_served == EXPECT_D)

    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    cm = sg.CapturingClient(real)
    pg.build_mention(proposed, AS_OF, client=cm)
    (mkey, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    try:
        pg.build_daily(proposed, AS_OF, client=cd)
    finally:
        pg._latest_gold_snapshot_rows = orig
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    puts = cm.sent + cd.sent

    named_doc = json.load(open(NAMED, encoding="utf-8"))
    named = [(row["article_key"], row["security_key"]) for row in named_doc["rows"]]
    v = r11.rule(served_m, served_d, mention, daily, served_list, proposed, silver_hashes(mention), AS_OF,
                 named_removals=named)

    om = {(r["article_key"], r["security_key"]): r for r in served_m}
    nm = {(r["article_key"], r["security_key"]): r for r in mention}
    print("AS OF %s; built mention key %s (%d bytes), daily key %s (%d bytes) -- CAPTURED, NOT WRITTEN" % (
        AS_OF, mkey, len(mbody), dkey, len(dbody)))
    print("TABLE           served    built     gone    added  changed")
    print("mention  %12d %8d %8d %8d %8d   changed by class %s, UNEXPLAINED %d %s" % (
        v["mention_served"], v["mention_built"], v["mention_gone"], v["mention_added"], v["mention_changed"],
        v["mention_changed_by_class"], v["mention_changed_unexplained"], v["mention_unexplained_fields"]))
    print("daily    %12d %8d %8d %8d %8d   changed by class %s, OTHER %d" % (
        v["daily_served"], v["daily_built"], v["daily_gone"], v["daily_added"], v["daily_changed"],
        v["daily_changed_by_class"], v["daily_other_count"]))
    print("MENTION GONE by security: %s" % v["mention_gone_by_security"])
    print("MENTION ADDED by class %s; on a list-moved or fallback security: %s" % (
        v["mention_added_by"], v["mention_added_by_security_moved"]))
    print("CHANGED (g), by security: %s" % v["mention_changed_g_by_security"])
    print("MENTION COUNT DOWN: %d rows over %s; not allowed: %s" % (
        v["mention_count_down_rows"], v["mention_count_down_by_security"], v["mention_count_down_not_allowed"]))
    print("LISTS: list-moved %s; fallback %s; lost a served alias %s" % (
        v["securities_list_moved"], v["securities_fallback"], v["securities_lost_a_served_alias"]))
    print("MENTION LOST: %d %s" % (v["mention_lost"], v["mention_lost_keys"]))
    for key, fields in list(v["daily_other"].items())[:20]:
        print("  OTHER %s fields %s" % (key, fields))
    for row in v["mention_unexplained_sample"]:
        print("  UNEXPLAINED %s" % row)

    per_sec = {}
    for sec in moved_keys:
        served_n = sum(1 for k in om if k[1] == sec)
        built_n = sum(1 for k in nm if k[1] == sec)
        gone = [k for k in om if k[1] == sec and k not in nm]
        added = [k for k in nm if k[1] == sec and k not in om]
        per_sec[sec] = (served_n, built_n, gone, added)
        print("%s: pairs served %d, built %d, gone %d, added %d" % (sec, served_n, built_n, len(gone), len(added)))

    reasons = list(v["reasons"])
    if not list_equal:
        reasons.append("the r75 list file is not universe_securities.build() at HEAD")
    if not baseline_ok:
        reasons.append("served baseline %s, %s is not rebuild #10's parts" % (mkey_served, dkey_served))
    if puts:
        reasons.append("%d put(s) sent" % puts)
    if v["named_not_gone"]:
        reasons.append("named and not gone: %s" % v["named_not_gone"])
    holds = not reasons
    print("RULE (rebuild #11): %s" % ("HOLDS" if holds else "BREAKS: " + "; ".join(reasons)))

    out = dict(v, measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), as_of=str(AS_OF),
               list_file_equals_build=list_equal, list_moved=moved_keys, baseline_ok=baseline_ok,
               served_mention_key=mkey_served, served_daily_key=dkey_served, puts_sent=puts,
               built_mention_key=mkey, built_daily_key=dkey, mention_bytes=len(mbody), daily_bytes=len(dbody),
               per_security={s: {"served": a[0], "built": a[1], "gone": len(a[2]), "added": len(a[3])}
                             for s, a in per_sec.items()}, rule_holds=holds, all_reasons=reasons)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)

    lines = ["# REBUILD11_TITLES -- gold rebuild #11 signing dry run (HVST-bs-1)", "",
             "Served baseline: `%s`, `%s`. Built (captured, not written) as of %s." % (mkey_served, dkey_served, AS_OF),
             "For each list-moved security: the FIRST TEN gone pairs and the FIRST TEN added pairs, ordered by "
             "(published date descending, article key ascending). Gone pairs are read from the SERVED row, added pairs "
             "from the BUILT row. No verdict, no grade: `3.0.0_SA_CVO~Z` grades the titles.", ""]
    for sec in moved_keys:
        served_n, built_n, gone, added = per_sec[sec]
        lines.append("## %s -- pairs served %d, built %d, gone %d, added %d" % (sec, served_n, built_n, len(gone), len(added)))
        lines.append("")
        for label, keys, src in (("GONE", gone, om), ("ADDED", added, nm)):
            rows = first_ten([src[k] for k in keys])
            lines.append("### %s: %d of %d shown" % (label, len(rows), len(keys)))
            lines.append("")
            if not rows:
                lines.append("(none)")
                lines.append("")
                continue
            lines.append("| # | article_key | date | publisher | title | match_forms |")
            lines.append("|---|---|---|---|---|---|")
            for i, r in enumerate(rows, 1):
                forms = r.get("match_forms") or []
                lines.append("| %d | %s | %s | %s | %s | %s |" % (
                    i, cell(r.get("article_key")), pub_day(r), cell(r.get("publisher")), cell(r.get("title")),
                    cell(json.dumps(list(forms), ensure_ascii=True))))
            lines.append("")
    with io.open(TITLES, "w", encoding="ascii", errors="backslashreplace", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("PUTS SENT %d" % puts)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
