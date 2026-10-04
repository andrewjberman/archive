"""HARVST round 41 HVST-an-3 -- THE ACT (issuer; only under the signed never-widen pair,
`round41/NEVER_WIDEN_HALF_COO_GOLD_EVENT.md` + the CTO half).

BEFORE snapshot of the served `chatter_event` rows; GATE = round41/gold_event.signing.py (writes nothing unless
`RULE (event rebuild): HOLDS`); ACT = `publication_gold build-event`, once; VERIFY = the same rule on the WRITTEN part
plus its digest equal to the gate's dry-run digest; ROLLBACK = the BEFORE rows written back as a newer part
(never-overwrite), so readers see BEFORE again. Writes `round41/gold_event_act_<stamp>.json`.
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
_spec = importlib.util.spec_from_file_location("ev_signing", os.path.join(HERE, "gold_event.signing.py"))
ev = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ev)
c, pg, store = ev.c, ev.pg, ev.store
UNIVERSE = os.environ["HVST_GOLD_UNIVERSE"]


def finish(record, rc):
    path = os.path.join(HERE, "gold_event_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE, "rebuild": "event (HVST-an-3)"}
    be = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    record["before"] = {"events": len(be), "digest": ev.digest(be)}
    gate_out = os.path.join(HERE, "gold_event_signing_gate_%s.json" % stamp)
    gate = subprocess.run([sys.executable, os.path.join(HERE, "gold_event.signing.py")], cwd=c.ROOT,
                          capture_output=True, text=True, timeout=3000,
                          env=dict(os.environ, GOLD_EVENT_SIGNING_OUT=gate_out))
    record["gate"] = gate.stdout.strip().splitlines()[-7:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (event rebuild): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the event-rebuild dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    gate_digest = json.load(open(gate_out, encoding="utf-8"))["built_digest"]
    p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", "build-event", "--securities-json",
                        UNIVERSE, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=3000)
    record["build-event"] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}
    print("build-event rc", p.returncode)
    if p.returncode != 0:
        record["result"] = "STOP: build-event rc %d" % p.returncode
        return finish(record, 1)
    ae = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    universe_keys = {s.get("security_key") for s in json.load(open(UNIVERSE, encoding="utf-8"))}
    verdict = ev.check(ae, pg._latest_gold_snapshot_rows(pg.GOLD_TABLE), pg._headline_by_article_key(), universe_keys)
    verdict["digest_equals_gate"] = ev.digest(ae) == gate_digest
    verdict["holds"] = verdict["holds"] and verdict["digest_equals_gate"]
    record["after"] = {"events": len(ae), "digest": ev.digest(ae)}
    record["verify"] = verdict
    print("VERIFY:", json.dumps(verdict))
    if verdict["holds"]:
        record["result"] = "DONE: the event-rebuild rule holds on the written part"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_EVENT_TABLE, be, as_of, run_stamp, schema=pg.GOLD_EVENT_SCHEMA)
    re_ = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    record["rollback"] = {"digest_equal": ev.digest(re_) == record["before"]["digest"], "events": len(re_)}
    record["result"] = "ROLLED BACK: the rule failed on the written part"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
