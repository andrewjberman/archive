"""HARVST served gold rebuild #8 (round 60) -- THE ACT (issuer; ONLY under the signed never-widen pair,
`round60/NEVER_WIDEN_HALF_COO_GOLD_REBUILD8.md` + the CTO half).

The served gold moves from the hand-carried list `round33/securities.universe.r33.json` (212 names) to the list the code
builds, saved as `round60/securities.universe.r60.json` (242 names): legal names from the collector's identity record, `Meta`
as a gold brand, `Lilly` anchored, the decorated pool names out, eight ticker forms refused on their graded census.

Same five steps as round49/av-2.act.py:
  1. BEFORE  snapshot of both served tables (rows, digests, newest part keys);
  2. GATE    `gold_rebuild8.signing4.py`, which writes nothing; it must print `RULE (rebuild #8): HOLDS`;
  3. ACT     the builders' own CLI, once each, with the r60 list file;
  4. VERIFY  `gold_rebuild8_rule.rule` on what was WRITTEN, against the BEFORE snapshot;
  5. ROLLBACK when VERIFY fails: the BEFORE rows written back as a newer part of each table (never-overwrite; nothing deleted).
Writes `gold_rebuild8.act_<stamp>.json`. `--gate-only` stops after step 2 and writes nothing to S3.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32 = os.path.join(PARENT, "round32")
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store = a32.c, a32.pg, a32.store

import gold_rebuild8_rule as r8  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402

R33 = os.path.join(PARENT, "round33", "securities.universe.r33.json")
R60 = os.path.join(HERE, "securities.universe.r60.json")
NAMED = os.path.join(HERE, "ICT_US_SERVED_PAIRS.json")
ALIAS_RULE = os.path.join(c.ROOT, "lib", "research", "harvest", "whole_brand_aliases.json")
GATE = os.path.join(HERE, "gold_rebuild8.signing4.py")
HOLDS = "RULE (rebuild #8): HOLDS"


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def verify(before_m, before_d, after_m, after_d, as_of):
    served_list = json.load(open(R33, encoding="utf-8"))
    proposed = json.load(open(R60, encoding="utf-8"))
    refused = [e["ticker"] for e in json.load(open(ALIAS_RULE, encoding="utf-8"))["ticker_refusals"]]
    named_doc = json.load(open(NAMED, encoding="utf-8"))
    named = [(row["article_key"], named_doc["security_key"]) for row in named_doc["rows"]]
    return r8.rule(before_m, before_d, after_m, after_d, served_list, proposed, silver_hashes(after_m), as_of,
                   refused_forms=refused, named_removals=named)


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild8.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    gate_only = "--gate-only" in sys.argv[1:]
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    as_of = now.date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": R60, "served_universe_file": R33, "rebuild": 8,
              "gate_only": gate_only}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest": a32.digest(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    print("BEFORE: mention %d rows, daily %d rows; parts %s | %s" % (
        len(bm), len(bd), record["before"]["mention_part"], record["before"]["daily_part"]))
    sys.stdout.flush()
    gate = subprocess.run([sys.executable, GATE], cwd=c.ROOT, capture_output=True, text=True, timeout=9000)
    record["gate"] = gate.stdout.strip().splitlines()[-12:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or HOLDS not in gate.stdout or "PUTS SENT: 0" not in gate.stdout:
        record["result"] = "STOP: the rebuild-#8 dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    if gate_only:
        record["result"] = "GATE ONLY: the rule holds on the dry run; nothing written"
        print(record["result"])
        return finish(record, 0)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            R60, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=5400)
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
    verdict = verify(bm, bd, am, ad, as_of)
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items()
                                 if k not in ("daily_other", "mention_removed_h_keys", "mention_unexplained_sample")}))
    if verdict["holds"]:
        record["result"] = "DONE: the rebuild-#8 rule holds on the written parts"
        print(record["result"])
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_equal": a32.digest(rm) == record["before"]["mention_digest"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
