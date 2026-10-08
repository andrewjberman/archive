"""HARVST served gold rebuild #10 -- THE SIGNING DRY RUN the never-widen pair reads, and the act's GATE (issuer, NO WRITE).

It builds mention and daily with the list FILE the act will pass (`securities.universe.r72.json` beside this script), through
the capturing client (PUTS SENT 0), and applies `gold_rebuild10_rule.rule` against the served snapshot (rebuild #9, built
from `round64/securities.universe.r64.json`). AMENDMENT 1 (`1.0.0_SA_CTO~Z` R28, msg 31945): the list is FROZEN at the one rebuild #9 was served
from, and the gate requires the list file to equal THAT file; what `universe_securities.build()` yields at this HEAD is printed
for information only (the collector pointer moved at 203db573d4 and the builder reads it; that list move is rebuild #11). It prints
BNP's pair counts (row AMGT_HARVST-Z-W112-S1). Prints `RULE (rebuild #10): HOLDS` only when the rule holds, the list check
passes and no put was sent. `--write-list` first writes the list file from `build()`. Writes `gold_rebuild10.signing.json`.
"""
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32C = os.path.join(PARENT, "round32", "checks")
sys.path.insert(0, R32C)
sys.path.insert(0, HERE)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path, as the round-32 dry run does)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

import gold_rebuild10_rule as r9  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

R60 = os.path.join(PARENT, "round64", "securities.universe.r64.json")
R64 = os.path.join(HERE, "securities.universe.r72.json")
NAMED = os.path.join(HERE, "REBUILD10_NAMED_REMOVALS.json")
OUT = os.path.join(HERE, "gold_rebuild10.signing.json")


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def main():
    built_now, _summary = us.build()
    if "--write-list" in sys.argv[1:]:
        with io.open(R64, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(built_now, handle, indent=1, sort_keys=True)
        print("LIST FILE WRITTEN: %d securities" % len(built_now))
    served_list = json.load(open(R60, encoding="utf-8"))
    proposed = json.load(open(R64, encoding="utf-8"))
    list_equal = json.dumps(built_now, sort_keys=True) == json.dumps(proposed, sort_keys=True)
    same_as_served = json.dumps(served_list, sort_keys=True) == json.dumps(proposed, sort_keys=True)
    print("LIST EQUAL TO THE LIST REBUILD 9 WAS SERVED FROM (round64 r64): %s" % same_as_served)
    print("LIST FILE: %s (%d securities); equal to universe_securities.build() at this HEAD: %s" % (
        os.path.relpath(R64, c.ROOT).replace(os.sep, "/"), len(proposed), list_equal))
    sys.stdout.flush()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    cm = sg.CapturingClient(real)
    pg.build_mention(proposed, as_of, client=cm)
    (mkey, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    pg.build_daily(proposed, as_of, client=cd)
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    pg._latest_gold_snapshot_rows = orig

    named_doc = json.load(open(NAMED, encoding="utf-8"))
    named = [(row["article_key"], row["security_key"]) for row in named_doc["rows"]]
    true_lost = {(row["article_key"], row["security_key"]) for row in named_doc["rows"] if row["true_pair"]}
    v = r9.rule(served_m, served_d, mention, daily, served_list, proposed, silver_hashes(mention), as_of,
                named_removals=named)
    removed = {tuple(k) for k in v["mention_removed_named_keys"]}
    by_class = {}
    for row in named_doc["rows"]:
        key = (row["article_key"], row["security_key"])
        by_class.setdefault(row["class"], [0, 0])
        by_class[row["class"]][1] += 1
        by_class[row["class"]][0] += 1 if key in removed else 0
    puts = cm.sent + cd.sent
    out = dict(v, measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), as_of=str(as_of),
               list_file_equals_build=list_equal, list_equals_rebuild9_list=same_as_served, puts_sent=puts, mention_key=mkey, daily_key=dkey,
               mention_bytes=len(mbody), daily_bytes=len(dbody), removed_by_class=by_class,
               true_pairs_lost=[list(k) for k in sorted(true_lost & removed)])
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("MENTION REMOVED BY NAME: %d of %d named, by class (removed of named) %s; by security %s" % (
        v["mention_removed_named"], v["named_total"], by_class, v["mention_removed_named_by_security"]))
    print("TRUE PAIRS LOST BY NAME: %d of %d: %s" % (
        len(true_lost & removed), len(true_lost), sorted(true_lost & removed)))
    print("NAMED AND NOT GONE: %s" % v["named_not_gone"])
    print("REMOVED ON EXACT-CASE FORMS ALONE (the headline arm): %s" % v["mention_removed_named_on_exact_forms"])

    def bnp(rows):
        mine = [r for r in rows if r.get("security_key") == "BNP_FP_Equity"]
        only = [r for r in mine if list(r.get("match_forms") or []) == ["BNP"]]
        return len(mine), sorted(r.get("article_key") for r in only)

    b0, b1 = bnp(served_m), bnp(mention)
    print("BNP_FP_Equity (row Z-W112-S1, an unexplained 3 against the dry run 3 of rebuild 8): pairs served %d built %d; "
          "on the form alone served %d %s built %d %s" % (b0[0], b1[0], len(b0[1]), b0[1], len(b1[1]), b1[1]))
    print("MENTION LOST: %d %s" % (v["mention_lost"], v["mention_lost_keys"]))
    print("MENTION: served %d -> built %d; gone %d, added %d %s, changed %d by class %s, UNEXPLAINED %d %s" % (
        v["mention_served"], v["mention_built"], v["mention_gone"], v["mention_added"], v["mention_added_by"],
        v["mention_changed"], v["mention_changed_by_class"], v["mention_changed_unexplained"], v["mention_unexplained_fields"]))
    print("ADDED ON A MOVED SECURITY, by security: %s" % v["mention_added_by_moved_security"])
    print("CHANGED (g), by security: %s" % v["mention_changed_g_by_security"])
    print("MENTION COUNT DOWN: %d rows over %s; not allowed: %s" % (
        v["mention_count_down_rows"], v["mention_count_down_by_security"], v["mention_count_down_not_allowed"]))
    print("LISTS: list-moved %s; fallback %s; lost a served alias %s" % (
        v["securities_list_moved"], v["securities_fallback"], v["securities_lost_a_served_alias"]))
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d by class %s, OTHER %d" % (
        v["daily_served"], v["daily_built"], v["daily_gone"], v["daily_added"], v["daily_changed"],
        v["daily_changed_by_class"], v["daily_other_count"]))
    for key, fields in list(v["daily_other"].items())[:20]:
        print("  OTHER %s fields %s" % (key, fields))
    for row in v["mention_unexplained_sample"]:
        print("  UNEXPLAINED %s" % row)
    holds = v["holds"] and same_as_served and puts == 0
    print("RULE (rebuild #10): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % puts)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
