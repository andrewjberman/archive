"""HARVST served gold rebuild -- THE ACT (issuer; only under the signed CTO + COO never-widen halves,
`round32/NEVER_WIDEN_HALF_COO_GOLD_REBUILD.md`).

1. BEFORE: record the served mention and daily snapshots (keys, row counts, digests).
2. GATE: re-run the serializing dry run (`checks/gold_rebuild.signing.py`); write nothing unless its RULE HOLDS.
3. ACT: the builders' own CLI, once each, as-of the UTC date: build-mention, then build-daily (each ONE never-overwrite
   part, the builder's own conditional put + read-back).
4. VERIFY on what was WRITTEN: mention gone 0 / changed 0 vs BEFORE; daily gone 0 and every changed row on a security
   with an added mention (OTHER 0).
5. ROLLBACK when step 4 fails: write the BEFORE snapshot rows back as a newer part of each table through the store's own
   `pg.write_gold` (never-overwrite, newer stamp), so readers of the newest part see BEFORE again; nothing is deleted.
Writes `round32/gold_rebuild_act_<stamp>.json`.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "checks"))
import ae1_common as c  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

# HVST_GOLD_UNIVERSE overrides the gold securities file (the signing dry run reads the same variable).
UNIVERSE = os.environ.get("HVST_GOLD_UNIVERSE") or os.path.join(
    c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")


def digest(rows):
    h = hashlib.sha256()
    for r in sorted(json.dumps(r, sort_keys=True, default=str) for r in rows):
        h.update(r.encode("utf-8") + b"\n")
    return h.hexdigest()


def newest_part(table):
    keys = sorted(k for k, _ in c.keys(store.table_prefix("amgt", "gold", table)) if k.endswith(".parquet"))
    return keys[-1] if keys else None


def snap():
    m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    return m, d


def rule(before_m, before_d, after_m, after_d):
    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    om = {mk(r): json.dumps(r, sort_keys=True, default=str) for r in before_m}
    nm = {mk(r): json.dumps(r, sort_keys=True, default=str) for r in after_m}
    gone = [k for k in om if k not in nm]
    changed = [k for k in nm if k in om and nm[k] != om[k]]
    # ADDENDUM 1 (gold universe 191 -> 212): a served row may change ONLY in the co-mention fields, and only when its new
    # co-mentions include an added security (one not in the BEFORE snapshot's security set).
    before_secs = {r.get("security_key") for r in before_m}
    after_rows = {mk(r): r for r in after_m}
    before_rows = {mk(r): r for r in before_m}
    co_fields = {"co_mention_count", "co_mentioned_securities", "is_roundup"}

    def co_mention_only(k):
        a, b = after_rows[k], before_rows[k]
        diff = {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}
        return diff <= co_fields and bool(set(a.get("co_mentioned_securities") or []) - before_secs)

    changed = [k for k in changed if not co_mention_only(k)]
    added_secs = {k[1] for k in nm if k not in om}
    od = {dk(r): json.dumps(r, sort_keys=True, default=str) for r in before_d}
    nd = {dk(r): json.dumps(r, sort_keys=True, default=str) for r in after_d}
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and nd[k] != od[k]]
    other = [k for k in d_changed if k[0] not in added_secs]
    return {"mention_gone": len(gone), "mention_changed": len(changed), "mention_added": len(nm) - len(om) + len(gone),
            "daily_gone": len(d_gone), "daily_changed": len(d_changed), "daily_other": len(other),
            "holds": not gone and not changed and not d_gone and not other}


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE}
    bm, bd = snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest": digest(bm), "daily_rows": len(bd), "daily_digest": digest(bd),
                        "mention_part": newest_part(pg.GOLD_TABLE), "daily_part": newest_part(pg.GOLD_DAILY_TABLE)}
    gate = subprocess.run([sys.executable, os.path.join(HERE, "checks", "gold_rebuild.signing.py")], cwd=c.ROOT,
                          capture_output=True, text=True, timeout=1800)
    record["gate"] = gate.stdout.strip().splitlines()[-6:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE: HOLDS" not in gate.stdout:
        record["result"] = "STOP: the dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            UNIVERSE, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=1800)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d" % (cmd, p.returncode)
            return finish(record, 1)
    am, ad = snap()
    record["after"] = {"mention_rows": len(am), "mention_digest": digest(am), "daily_rows": len(ad), "daily_digest": digest(ad),
                       "mention_part": newest_part(pg.GOLD_TABLE), "daily_part": newest_part(pg.GOLD_DAILY_TABLE)}
    verdict = rule(bm, bd, am, ad)
    record["verify"] = verdict
    print("VERIFY:", json.dumps(verdict))
    if verdict["holds"]:
        record["result"] = "DONE: rule holds on the written parts"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = snap()
    record["rollback"] = {"mention_digest_equal": digest(rm) == record["before"]["mention_digest"],
                          "daily_digest_equal": digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


if __name__ == "__main__":
    sys.exit(main())
