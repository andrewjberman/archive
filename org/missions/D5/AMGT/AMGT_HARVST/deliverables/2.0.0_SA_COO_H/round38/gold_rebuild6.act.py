"""HARVST served gold rebuild #6 -- THE ACT, STRICT variant: the ft QUARANTINE ALONE (issuer; only under the signed
never-widen pair `round38/NEVER_WIDEN_HALF_COO_GOLD_REBUILD6.md` plus the CTO half; CTO msgs 28715 ruling 3 and 28731).

Five steps, as in round37/gold_rebuild5.act.py:
1. BEFORE snapshot.
2. GATE: `round38/gold_rebuild6.signing.py` with HVST_R6_STRICT=1 on the round-33 universe. Nothing is written unless it
   prints `RULE (rebuild #6): HOLDS`.
3. ACT:
   - mention = the BEFORE served rows minus the quarantined (ft) rows, each gaining the 3 tone fields as NULL, put once
     through `publication_gold.write_gold`. Nothing is added from collection since rebuild #5.
   - daily = the builder's own `build-daily` CLI, once. It reads the newest mention snapshot, which is the part just
     written.
4. VERIFY on the written parts:
   - mention keys = BEFORE minus ft exactly; 0 changed on the pre-existing fields; 0 ft; every tone value NULL;
   - daily: 0 gone, and every changed row inside the quarantine bounds (class q); OTHER 0.
5. ROLLBACK if VERIFY fails: the BEFORE rows are written back as a newer part of each table, and nothing is deleted.
Writes `round38/gold_rebuild6_act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32 = os.path.join(os.path.dirname(HERE), "round32")
TONE = ("sentiment_finbert_label", "sentiment_finbert_score", "sentiment_scorer")
UNIVERSE_R33 = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round33/securities.universe.r33.json"

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store = a32.c, a32.pg, a32.store
_spec6 = importlib.util.spec_from_file_location("r6_signing", os.path.join(HERE, "gold_rebuild6.signing.py"))
s6 = importlib.util.module_from_spec(_spec6)
_spec6.loader.exec_module(s6)


def pre(r):
    return {k: v for k, v in r.items() if k not in TONE}


def digest_pre(rows):
    return a32.digest([pre(r) for r in rows])


def rule(before_m, before_d, after_m, after_d):
    q = set(pg.QUARANTINED_PUBLISHERS)
    graded = list(pg.GRADED_PUBLISHERS)
    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    ft_secs = {r.get("security_key") for r in before_m if pg.is_quarantined(r)}
    want = {mk(r): json.dumps(pre(r), sort_keys=True, default=str) for r in before_m if not pg.is_quarantined(r)}
    got = {mk(r): json.dumps(pre(r), sort_keys=True, default=str) for r in after_m}
    m_missing = [k for k in want if k not in got]
    m_extra = [k for k in got if k not in want]
    m_changed = [k for k in got if k in want and got[k] != want[k]]
    m_ft = sum(1 for r in after_m if pg.is_quarantined(r))
    tone_valued = sum(1 for r in after_m if any(r.get(f) is not None for f in TONE))
    tone_missing = sum(1 for r in after_m if any(f not in r for f in TONE))
    od, nd = {dk(r): r for r in before_d}, {dk(r): r for r in after_d}
    d_gone = [k for k in od if k not in nd]
    d_added = [k for k in nd if k not in od]
    d_changed = [k for k in nd if k in od and s6.dumps(nd[k]) != s6.dumps(od[k])]
    other, other_bounds, transitions = [], {}, {}
    for k in d_changed:
        ok, qb = s6.quarantine_bounds(od[k], nd[k], graded, ft_secs, q)
        t = "%s->%s" % (od[k].get("data_status"), nd[k].get("data_status"))
        if od[k].get("data_status") != nd[k].get("data_status"):
            transitions[t] = transitions.get(t, 0) + 1
        if not ok:
            other.append(k)
            if len(other_bounds) < 20:
                other_bounds["|".join(k)] = qb
    return {"mention_before": len(before_m), "mention_before_ft": len(before_m) - len(want),
            "mention_after": len(after_m), "mention_missing": len(m_missing), "mention_extra": len(m_extra),
            "mention_changed_pre_existing": len(m_changed), "mention_ft_after": m_ft,
            "tone_valued": tone_valued, "tone_missing": tone_missing,
            "daily_gone": len(d_gone), "daily_added": len(d_added), "daily_changed": len(d_changed),
            "daily_other": len(other), "daily_other_bounds": other_bounds, "status_transitions": transitions,
            "holds": not (m_missing or m_extra or m_changed or m_ft or tone_valued or tone_missing
                          or d_gone or d_added or other)}


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild6_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE_R33, "rebuild": 6, "variant": "STRICT"}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest_pre": digest_pre(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    # CTO half @5eb4e11b3d condition (1): the counts signed at ~22:3xZ. A moved count is a STOP and a re-sign.
    signed = {"mention_rows": 23691, "mention_ft": 926, "daily_rows": 58300}
    seen = {"mention_rows": len(bm), "mention_ft": sum(1 for r in bm if pg.is_quarantined(r)), "daily_rows": len(bd)}
    record["signed_counts"], record["before_counts"] = signed, seen
    print("SIGNED COUNTS %s; BEFORE COUNTS %s" % (signed, seen))
    if seen != signed:
        record["result"] = "STOP: a signed count moved (%s != %s); re-sign before any write" % (seen, signed)
        print(record["result"])
        return finish(record, 1)
    env = dict(os.environ, HVST_R6_STRICT="1", HVST_GOLD_UNIVERSE=UNIVERSE_R33)
    gate = subprocess.run([sys.executable, "-u", os.path.join(HERE, "gold_rebuild6.signing.py")], cwd=c.ROOT, env=env,
                          capture_output=True, text=True, timeout=3000)
    record["gate"] = gate.stdout.strip().splitlines()[-9:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (rebuild #6): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the rebuild-#6 STRICT dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    rows = [dict(r, **{f: None for f in TONE}) for r in bm if not pg.is_quarantined(r)]
    receipt = pg.write_gold(pg.GOLD_TABLE, rows, datetime.date.fromisoformat(as_of), run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    record["write-mention"] = {"rows": len(rows), "key": receipt.get("key")}
    print("write-mention", len(rows), receipt.get("key"))
    p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", "build-daily", "--securities-json",
                        UNIVERSE_R33, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=3000)
    record["build-daily"] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
    print("build-daily rc", p.returncode)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest_pre": digest_pre(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    verdict = rule(bm, bd, am, ad) if p.returncode == 0 else {"holds": False, "reason": "build-daily rc %d" % p.returncode}
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items() if k != "daily_other_bounds"}))
    if verdict["holds"]:
        record["result"] = "DONE: rebuild-#6 (ft quarantine, STRICT) rule holds on the written parts"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, datetime.date.fromisoformat(as_of), run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, datetime.date.fromisoformat(as_of), run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_pre_equal": digest_pre(rm) == record["before"]["mention_digest_pre"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
