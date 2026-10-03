"""HARVST round 41 HVST-an-2 -- THE ACT (issuer; only under the signed never-widen pair,
`round41/NEVER_WIDEN_HALF_COO_GOLD_TONE.md` + the CTO half).

Five steps, as rebuild #5 (round37/gold_rebuild5.act.py): BEFORE snapshot; GATE = round41/gold_tone.signing.py, which
writes nothing unless `RULE (tone rebuild): HOLDS`; ACT = the builders' own CLI, once each; VERIFY on the written parts;
ROLLBACK = the BEFORE rows written back as a newer part of each table (never-overwrite), so readers see BEFORE again.
VERIFY reuses the rebuild-#5 rule with the 4 `sentiment_*` fields as the added set, plus the tone join on the written
mention part. Writes `round41/gold_tone_act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
os.environ.setdefault("HVST_GOLD_UNIVERSE", os.path.join(DELIV, "round33", "securities.universe.r33.json"))
TONE_FIELDS = ("sentiment_finbert_label", "sentiment_finbert_score", "sentiment_scorer", "sentiment_content_key")

_spec = importlib.util.spec_from_file_location("r37_act", os.path.join(DELIV, "round37", "gold_rebuild5.act.py"))
a5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a5)
a5.ADDED_FIELDS = TONE_FIELDS  # the rebuild-#5 rule, with the tone fields as the added set
a32, c, pg, store = a5.a32, a5.c, a5.pg, a5.store
UNIVERSE = os.environ["HVST_GOLD_UNIVERSE"]

from lib.research.harvest import finbert_sentiment as fs  # noqa: E402


def finish(record, rc):
    path = os.path.join(HERE, "gold_tone_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def tone_join(rows, scores):
    keyed = [r for r in rows if r.get("sentiment_content_key")]
    scored = [r for r in keyed if r["sentiment_content_key"] in scores]
    mismatch = sum(1 for r in scored
                   if r.get("sentiment_finbert_label") != scores[r["sentiment_content_key"]].get("label")
                   or r.get("sentiment_finbert_score") != scores[r["sentiment_content_key"]].get("score"))
    return {"rows": len(rows), "content_keyed": len(keyed), "scored": len(scored), "join_mismatch": mismatch,
            "labelled": sum(1 for r in rows if r.get("sentiment_finbert_label") is not None)}


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE, "rebuild": "tone (HVST-an-2)"}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest_pre": a5.digest_pre(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    gate = subprocess.run([sys.executable, os.path.join(HERE, "gold_tone.signing.py")], cwd=c.ROOT,
                          capture_output=True, text=True, timeout=3000)
    record["gate"] = gate.stdout.strip().splitlines()[-9:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (tone rebuild): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the tone-rebuild dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            UNIVERSE, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=3000)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d" % (cmd, p.returncode)
            return finish(record, 1)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest_pre": a5.digest_pre(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    verdict = a5.rule(bm, bd, am, ad, as_of=as_of)
    tone = tone_join(am, fs.latest_scores())
    verdict["tone"] = tone
    verdict["holds"] = verdict["holds"] and tone["join_mismatch"] == 0
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items() if k != "daily_bounds"}))
    if verdict["holds"]:
        record["result"] = "DONE: the tone-rebuild rule holds on the written parts"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_pre_equal": a5.digest_pre(rm) == record["before"]["mention_digest_pre"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
