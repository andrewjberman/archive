"""HARVST served gold rebuild #5 -- THE ACT (issuer; only under the signed NEW never-widen pair for track C step 1,
`round37/NEVER_WIDEN_HALF_COO_GOLD_REBUILD5.md` + the CTO half).

Same five steps as round32/gold_rebuild.act.py (BEFORE snapshot; GATE = round37/gold_rebuild5.signing.py, writes nothing
unless `RULE (rebuild #5): HOLDS`; ACT = the builders' own CLI, once each; VERIFY on what was written; ROLLBACK = the
BEFORE rows written back as a newer part), with the rebuild-#5 rule:
- mention: gone 0; changed 0 on the PRE-EXISTING field set; every written row carries `title` and `published_precision`;
- daily: gone 0; OTHER 0 (every changed day row is on a security with an added mention).
Rollback equality is measured on the pre-existing field set (the BEFORE rows written under the new schema carry the two
new fields as null). Writes `round37/gold_rebuild5_act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32 = os.path.join(os.path.dirname(HERE), "round32")
ADDED_FIELDS = ("title", "published_precision")

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store, UNIVERSE = a32.c, a32.pg, a32.store, a32.UNIVERSE


def pre(r):
    return {k: v for k, v in r.items() if k not in ADDED_FIELDS}


def digest_pre(rows):
    return a32.digest([pre(r) for r in rows])


def rule(before_m, before_d, after_m, after_d):
    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    om = {mk(r): json.dumps(pre(r), sort_keys=True, default=str) for r in before_m}
    nm = {mk(r): json.dumps(pre(r), sort_keys=True, default=str) for r in after_m}
    gone = [k for k in om if k not in nm]
    changed = [k for k in nm if k in om and nm[k] != om[k]]
    missing_fields = sum(1 for r in after_m if any(f not in r for f in ADDED_FIELDS))
    titled = sum(1 for r in after_m if r.get("title"))
    added_secs = {k[1] for k in nm if k not in om}
    od = {dk(r): json.dumps(r, sort_keys=True, default=str) for r in before_d}
    nd = {dk(r): json.dumps(r, sort_keys=True, default=str) for r in after_d}
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and nd[k] != od[k]]
    other = [k for k in d_changed if k[0] not in added_secs]
    return {"mention_gone": len(gone), "mention_changed_pre_existing": len(changed),
            "mention_added": len(nm) - len(om) + len(gone), "mention_rows_missing_new_fields": missing_fields,
            "mention_rows_titled": titled, "daily_gone": len(d_gone), "daily_changed": len(d_changed),
            "daily_other": len(other),
            "holds": not gone and not changed and not missing_fields and not d_gone and not other}


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild5_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE, "rebuild": 5}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest_pre": digest_pre(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    gate = subprocess.run([sys.executable, os.path.join(HERE, "gold_rebuild5.signing.py")], cwd=c.ROOT,
                          capture_output=True, text=True, timeout=2400)
    record["gate"] = gate.stdout.strip().splitlines()[-8:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (rebuild #5): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the rebuild-#5 dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            UNIVERSE, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=2400)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d" % (cmd, p.returncode)
            return finish(record, 1)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest_pre": digest_pre(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    verdict = rule(bm, bd, am, ad)
    record["verify"] = verdict
    print("VERIFY:", json.dumps(verdict))
    if verdict["holds"]:
        record["result"] = "DONE: rebuild-#5 rule holds on the written parts"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_pre_equal": digest_pre(rm) == record["before"]["mention_digest_pre"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
