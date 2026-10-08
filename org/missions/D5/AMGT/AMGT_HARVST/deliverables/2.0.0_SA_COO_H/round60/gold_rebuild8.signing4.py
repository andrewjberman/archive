"""HARVST served gold rebuild #8 -- THE SIGNING DRY RUN the never-widen pair reads, and the act's GATE (issuer, NO WRITE).

It builds mention and daily with the list FILE the act will pass (`securities.universe.r60.json` beside this script), through
the capturing client (PUTS SENT 0), and applies `gold_rebuild8_rule.rule` against the served snapshot. It also checks that the
list file equals what `universe_securities.build()` yields at this HEAD, so the signed list is the code's list.
Prints `RULE (rebuild #8): HOLDS` only when the rule holds, the list check passes and no put was sent.
Writes `gold_rebuild8.signing4.json`.
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

import gold_rebuild8_rule as r8  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

R33 = os.path.join(PARENT, "round33", "securities.universe.r33.json")
R60 = os.path.join(HERE, "securities.universe.r60.json")
NAMED = os.path.join(HERE, "ICT_US_SERVED_PAIRS.json")
ALIAS_RULE = os.path.join(c.ROOT, "lib", "research", "harvest", "whole_brand_aliases.json")
OUT = os.path.join(HERE, "gold_rebuild8.signing4.json")


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def main():
    served_list = json.load(open(R33, encoding="utf-8"))
    proposed = json.load(open(R60, encoding="utf-8"))
    built_now, _summary = us.build()
    list_equal = json.dumps(built_now, sort_keys=True) == json.dumps(proposed, sort_keys=True)
    print("LIST FILE: %s (%d securities); equal to universe_securities.build() at this HEAD: %s" % (
        os.path.relpath(R60, c.ROOT).replace(os.sep, "/"), len(proposed), list_equal))
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

    refused = [e["ticker"] for e in json.load(open(ALIAS_RULE, encoding="utf-8"))["ticker_refusals"]]
    named_doc = json.load(open(NAMED, encoding="utf-8"))
    named = [(row["article_key"], named_doc["security_key"]) for row in named_doc["rows"]]
    verdict = r8.rule(served_m, served_d, mention, daily, served_list, proposed, silver_hashes(mention), as_of,
                      refused_forms=refused, named_removals=named)
    puts = cm.sent + cd.sent
    out = dict(verdict, measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), as_of=str(as_of),
               list_file_equals_build=list_equal, puts_sent=puts, mention_key=mkey, daily_key=dkey,
               mention_bytes=len(mbody), daily_bytes=len(dbody))
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    v = verdict
    print("MENTION REMOVED (h): %d of %d named, by security %s; LOST %d %s" % (
        v["mention_removed_h"], len(named), v["mention_removed_h_by_security"], v["mention_lost"], v["mention_lost_keys"]))
    print("FOLLOWING THE (h) REMOVALS: co-mention rows %d; daily rows %d" % (
        v["co_mention_rows_following_h"], v["daily_rows_following_h"]))
    print("MENTION: served %d -> built %d; gone %d, added %d %s, changed %d by class %s, UNEXPLAINED %d %s" % (
        v["mention_served"], v["mention_built"], v["mention_gone"], v["mention_added"], v["mention_added_by"],
        v["mention_changed"], v["mention_changed_by_class"], v["mention_changed_unexplained"], v["mention_unexplained_fields"]))
    print("MENTION COUNT DOWN: %d rows over %s; not on a security that lost a served alias: %s" % (
        v["mention_count_down_rows"], v["mention_count_down_by_security"], v["mention_count_down_not_on_a_lost_alias"]))
    print("LISTS: alias set differs on %d common securities; lost a served alias: %s" % (
        v["securities_alias_differs"], v["securities_lost_a_served_alias"]))
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d by class %s, OTHER %d" % (
        v["daily_served"], v["daily_built"], v["daily_gone"], v["daily_added"], v["daily_changed"],
        v["daily_changed_by_class"], v["daily_other_count"]))
    for key, fields in list(v["daily_other"].items())[:20]:
        print("  OTHER %s fields %s" % (key, fields))
    for row in v["mention_unexplained_sample"]:
        print("  UNEXPLAINED %s" % row)
    holds = v["holds"] and list_equal and puts == 0
    print("RULE (rebuild #8): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % puts)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
