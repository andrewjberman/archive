"""HARVST served gold rebuild #12 (round 75, workstream R12) -- THE ACT (issuer; ONLY under the signed never-widen pair,
`round75/NEVER_WIDEN_HALF_COO_GOLD_REBUILD12.md` + the CTO half).

Gold's matcher at HEAD carries R30 (HVST-br-1, merged @3255a9156d). The list does not move (the r75 file on both sides).
The pair signs TWO classes, from HVST-bs-5's dry run (@a7a06fbc3c) and `1.0.0_SA_CTO~DELL1` ADDENDUM 2 (msg 2181):
  - R30 REMOVAL: a served pair that is gone, which br-1's classifier (`br1_census.mentions`) counts under the pre-R30 rule
    and not under R30;
  - R30-PARTIAL COUNT-DOWN: a kept pair whose own fields changed, which the classifier counts before > after > 0.
Anything else is a STOP. The steps:
  1. BEFORE  the served snapshot; refused unless the newest parts are rebuild #11's;
  2. ACT     the builders' own CLI, once each, with the r75 list file and `--as-of 2026-10-08`;
  3. VERIFY  `gold_rebuild12_rule.rule` on what was WRITTEN, with both classes computed by br-1's classifier on the
             written rows; it holds only when every change outside co-mention classes is in one of the two classes;
  4. ROLLBACK on a break: the BEFORE rows are written again as the newest part (no delete);
  5. RECORD  the parts, the class counts and the mention delta, beside the dry run's (285 removals, 113 count-downs,
             delta 762).
There is no separate gate run: the pair is signed on bs-5's measured diff, and VERIFY on the written rows is the same rule
with the same classifier. Writes `gold_rebuild12.act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(os.path.dirname(HERE))  # .../AMGT_HARVST/deliverables
CELL = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~131")
W126 = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~126")
W129 = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~129")
R32 = os.path.join(DELIV, "2.0.0_SA_COO_H", "round32")
sys.path.insert(0, CELL)
sys.path.insert(0, W126)

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store = a32.c, a32.pg, a32.store

import br1_census as br1  # noqa: E402  (br-1's own classifier)
import gold_rebuild12_rule as r12  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402

AS_OF = "2026-10-08"
LIST_FILE = os.path.join(W129, "securities.universe.r75.json")
EXPECT_M = "amgt/harvest/gold/article_security_mention/date=2026-10-08/part-20261009T045809Z.parquet"
EXPECT_D = "amgt/harvest/gold/chatter_daily/date=2026-10-08/part-20261009T061012Z.parquet"
DRY = {"r30_removals": 285, "r30_partial": 113, "mention_delta": 762}


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def classify(before_m, after_m, securities):
    """Both signed classes, by br-1's classifier, on the rows actually written (bs-5's code path)."""
    om = {(r["article_key"], r["security_key"]): r for r in before_m}
    nm = {(r["article_key"], r["security_key"]): r for r in after_m}
    gone = [k for k in om if k not in nm]
    own_changed = [k for k in nm if k in om and r12.r8._dump(nm[k]) != r12.r8._dump(om[k])
                   and (r12.r8._fields(om[k], nm[k]) & r12.r8.OWN_FIELDS)]
    need = {k[0] for k in gone} | {k[0] for k in own_changed}
    articles = {a["article_key"]: a for a in pg._iter_latest_articles() if a.get("article_key") in need}
    r30_class, r30_partial, missing = set(), set(), []
    for k in gone:
        article, sec = articles.get(k[0]), securities.get(k[1])
        if article is None or sec is None:
            missing.append(k)
            continue
        if br1.mentions(article, sec, False) and not br1.mentions(article, sec, True):
            r30_class.add(k)
    for k in own_changed:
        article, sec = articles.get(k[0]), securities.get(k[1])
        if article is None or sec is None:
            missing.append(k)
            continue
        if br1.mentions(article, sec, False) > br1.mentions(article, sec, True) > 0:
            r30_partial.add(k)
    delta = sum(int(om[k].get("mention_count") or 0) for k in r30_class)
    delta += sum(int(om[k].get("mention_count") or 0) - int(nm[k].get("mention_count") or 0) for k in r30_partial)
    return r30_class, r30_partial, missing, delta


def judge(v, r30_partial, missing):
    """ADDENDUM 2: the rule's only admitted reason is UNEXPLAINED rows that are ALL R30-partial count-downs."""
    reasons = []
    for reason in v["reasons"]:
        if reason.startswith("%d changed mention row(s) UNEXPLAINED" % v["mention_changed_unexplained"]):
            continue
        reasons.append(reason)
    not_partial = [r for r in v["outside_rows"]
                   if not (r["kind"] == "changed" and (r["article_key"], r["security_key"]) in r30_partial)]
    if not_partial:
        reasons.append("%d OUTSIDE row(s) not in either signed class: %s" % (
            len(not_partial), [(r["article_key"], r["security_key"], r["kind"]) for r in not_partial[:20]]))
    if missing:
        reasons.append("classifier input missing for %d pair(s)" % len(missing))
    return reasons


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild12.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    proposed = json.load(open(LIST_FILE, encoding="utf-8"))
    securities = {s["security_key"]: s for s in proposed}
    record = {"stamp": stamp, "as_of": AS_OF, "universe_file": LIST_FILE, "rebuild": 12, "dry_run": DRY}
    assert pg._CAPITAL_INITIAL_ALIAS_RULE is True, "publication_gold R30 flag is not on at HEAD"
    mpart, dpart = a32.newest_part(pg.GOLD_TABLE), a32.newest_part(pg.GOLD_DAILY_TABLE)
    record["before_parts"] = [mpart, dpart]
    print("BEFORE PARTS:", mpart, dpart)
    if (mpart, dpart) != (EXPECT_M, EXPECT_D):
        record["result"] = "STOP: the served baseline is not rebuild #11's parts; nothing written"
        print(record["result"])
        return finish(record, 1)
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest": a32.digest(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd)}
    print("BEFORE: mention %d rows, daily %d rows" % (len(bm), len(bd)))
    sys.stdout.flush()
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            LIST_FILE, "--as-of", AS_OF], cwd=c.ROOT, capture_output=True, text=True, timeout=7200)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        sys.stdout.flush()
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d (a mention part may be written; VERIFY and ROLLBACK follow by hand)" % (
                cmd, p.returncode)
            return finish(record, 1)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest": a32.digest(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    r30_class, r30_partial, missing, delta = classify(bm, am, securities)
    v = r12.rule(bm, bd, am, ad, proposed, proposed, silver_hashes(am), AS_OF,
                 r30_class=r30_class, r30_partial=r30_partial)
    reasons = judge(v, r30_partial, missing)
    record["verify"] = dict(v, outside_rows=v["outside_rows"][:200])
    record["classes"] = {"r30_removals": v["r30_removals"], "r30_partial": len(r30_partial), "mention_delta": delta}
    record["reasons"] = reasons
    print("CLASSES: R30 removals %d (dry run %d); R30-partial count-downs %d (dry run %d); mention delta %d (dry run %d)" % (
        v["r30_removals"], DRY["r30_removals"], len(r30_partial), DRY["r30_partial"], delta, DRY["mention_delta"]))
    print("VERIFY: lost %d, added %d, daily gone %d, daily OTHER %d" % (
        v["mention_lost"], v["mention_added"], v["daily_gone"], v["daily_other_count"]))
    if not reasons:
        record["result"] = "DONE: rebuild #12 holds on the written parts, both signed classes only"
        print(record["result"])
        return finish(record, 0)
    print("BREAKS:", "; ".join(reasons))
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, AS_OF, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, AS_OF, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_equal": a32.digest(rm) == record["before"]["mention_digest"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule broke on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
