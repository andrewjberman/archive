"""HARVST served gold rebuild #11 (round 75) -- THE ACT (issuer; ONLY under the signed never-widen pair,
`round75/NEVER_WIDEN_HALF_COO_GOLD_REBUILD11.md` + the CTO half).

The served gold moves from the frozen r72 list to the list `universe_securities.build()` yields at HEAD
(`0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json`): AIG_US_Equity, OMAB_MM_Equity and OMAB_US_Equity change their
own fields. The matcher does not move. The pair signs the RULE (`gold_rebuild11_rule.py`, HVST-bs-1 @2ba8e449f5), and the
act re-reads it on what it writes. Rebuild #10's act script (`round72/gold_rebuild10.act.py`) with two changes: AS_OF is
pinned to the signed dry run's date (2026-10-08, T-1 of this act) instead of the clock, and step 5 writes the changed
own-field rows of the three list-moved securities for `3.0.0_SA_CVO`'s grade (`1.0.0_SA_CTO~DELL1` msg 1579).

  1. BEFORE  the served snapshot of mention and daily, read and kept in the record;
  2. GATE    `gold_rebuild11.signing.py`, which writes nothing; it must print `RULE (rebuild #11): HOLDS` and `PUTS SENT 0`;
  3. ACT     the builders' own CLI, once each, with the r75 list file and `--as-of 2026-10-08`;
  4. VERIFY  `gold_rebuild11_rule.rule` on what was WRITTEN, against the BEFORE snapshot; a broken rule rolls back by
             writing the BEFORE rows again as the newest part (no delete);
  5. RECORD  the parts written, the counts, the changed list-moved rows, the rollback key per part.
Writes `gold_rebuild11.act_<stamp>.json` and `REBUILD11_CHANGED_ROWS.json`. `--gate-only` stops after step 2.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(os.path.dirname(HERE))  # .../AMGT_HARVST/deliverables
CELL = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~129")
R32 = os.path.join(DELIV, "2.0.0_SA_COO_H", "round32")
R72 = os.path.join(DELIV, "2.0.0_SA_COO_H", "round72")
sys.path.insert(0, CELL)

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store = a32.c, a32.pg, a32.store

import gold_rebuild11_rule as r11  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402

AS_OF = "2026-10-08"
SERVED_LIST = os.path.join(R72, "securities.universe.r72.json")
PROPOSED = os.path.join(CELL, "securities.universe.r75.json")
NAMED = os.path.join(CELL, "REBUILD11_NAMED_REMOVALS.json")
GATE = os.path.join(CELL, "gold_rebuild11.signing.py")
HOLDS = "RULE (rebuild #11): HOLDS"
PUTS0 = "PUTS SENT 0"
MOVED = ("AIG_US_Equity", "OMAB_MM_Equity", "OMAB_US_Equity")
EXPECTED_CHANGED = 22  # CTO half condition 2 (@100b9af433)
CHANGED_OUT = os.path.join(HERE, "REBUILD11_CHANGED_ROWS.json")


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def named_pairs():
    doc = json.load(open(NAMED, encoding="utf-8"))
    rows = doc.get("rows", []) if isinstance(doc, dict) else doc
    return [(row["article_key"], row["security_key"]) for row in rows]


def verify(before_m, before_d, after_m, after_d):
    served_list = json.load(open(SERVED_LIST, encoding="utf-8"))
    proposed = json.load(open(PROPOSED, encoding="utf-8"))
    return r11.rule(before_m, before_d, after_m, after_d, served_list, proposed, silver_hashes(after_m), AS_OF,
                    named_removals=named_pairs())


def changed_moved_rows(before_m, after_m):
    """Every mention row of a list-moved security whose key is in both snapshots and whose content differs: the key,
    then each field that moved, before and after. This is the set `3.0.0_SA_CVO` grades (msg 1579)."""
    def index(rows):
        return {(r.get("article_key"), r.get("security_key")): r for r in rows if r.get("security_key") in MOVED}
    old, new = index(before_m), index(after_m)
    out = []
    for key in sorted(set(old) & set(new)):
        o, n = old[key], new[key]
        fields = sorted(f for f in set(o) | set(n) if json.dumps(o.get(f), default=str, sort_keys=True)
                        != json.dumps(n.get(f), default=str, sort_keys=True))
        if fields:
            out.append({"article_key": key[0], "security_key": key[1], "title": n.get("title"),
                        "published_date": n.get("published_date"), "publisher": n.get("publisher"),
                        "changed": {f: {"before": o.get(f), "after": n.get(f)} for f in fields}})
    return out


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild11.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    gate_only = "--gate-only" in sys.argv[1:]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record = {"stamp": stamp, "as_of": AS_OF, "universe_file": PROPOSED, "served_universe_file": SERVED_LIST,
              "rebuild": 11, "gate_only": gate_only, "list_moved": list(MOVED)}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest": a32.digest(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    print("BEFORE: mention %d rows, daily %d rows; parts %s | %s" % (
        len(bm), len(bd), record["before"]["mention_part"], record["before"]["daily_part"]))
    sys.stdout.flush()
    gate = subprocess.run([sys.executable, GATE], cwd=c.ROOT, capture_output=True, text=True, timeout=9000)
    record["gate"] = gate.stdout.strip().splitlines()[-20:]
    print("\n".join(record["gate"]))
    sys.stdout.flush()
    if gate.returncode != 0 or HOLDS not in gate.stdout or PUTS0 not in gate.stdout:
        record["result"] = "STOP: the rebuild-#11 dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    if gate_only:
        record["result"] = "GATE ONLY: the rule holds on the dry run; nothing written"
        print(record["result"])
        return finish(record, 0)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            PROPOSED, "--as-of", AS_OF], cwd=c.ROOT, capture_output=True, text=True, timeout=5400)
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
    changed = changed_moved_rows(bm, am)
    json.dump({"as_of": AS_OF, "stamp": stamp, "count": len(changed), "rows": changed},
              open(CHANGED_OUT, "w", encoding="utf-8"), indent=1, default=str)
    record["changed_moved_rows"] = {"count": len(changed), "file": CHANGED_OUT}
    print("CHANGED LIST-MOVED ROWS: %d (%s)" % (len(changed), CHANGED_OUT))
    verdict = verify(bm, bd, am, ad)
    # CTO half condition 2 (@100b9af433): exactly the 22 signed rows changed, and no other changed row anywhere.
    changed_all = verdict.get("mention_changed")
    if len(changed) != EXPECTED_CHANGED or changed_all != EXPECTED_CHANGED:
        verdict = dict(verdict, holds=False, reasons=list(verdict.get("reasons") or []) + [
            "CTO condition 2: changed list-moved rows %d, changed mention rows %s; expected %d and %d" % (
                len(changed), changed_all, EXPECTED_CHANGED, EXPECTED_CHANGED)])
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items()
                                 if k not in ("daily_other", "mention_removed_named_keys", "mention_unexplained_sample")},
                                default=str))
    if verdict["holds"]:
        record["result"] = "DONE: the rebuild-#11 rule holds on the written parts"
        print(record["result"])
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, AS_OF, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, AS_OF, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_equal": a32.digest(rm) == record["before"]["mention_digest"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
