"""HARVST round 46 HVST-as-2 -- THE ACT (copied from round 43 ap-1's act; issuer; only under the signed never-widen pair,
`round46/NEVER_WIDEN_HALF_COO_WINDOW_UNION.md` + the CTO half). Union build list; as_of pinned to the served snapshot's.

BEFORE: the served `chatter_window` rows; GATE = round43/gold_window_zero.signing.py (writes nothing unless
`RULE (explicit zero rows): HOLDS`); ACT = `window_tone build`, once; VERIFY = the same rule on the WRITTEN part plus its
digest equal to the gate's; ROLLBACK = the BEFORE rows written back as a newer part (never-overwrite), so readers see the
618 rows again. Nothing is deleted. Writes `round43/gold_window_zero_act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
os.environ.setdefault("HVST_GOLD_UNIVERSE", os.path.join(HERE, "securities.union.r46.json"))
os.environ.setdefault("HVST_AS_OF", "2026-10-04")
EXPECT_ROWS = 699
SIGNED_DIGEST = "428298cfcde85c04ac77482c75015d3799753201b20fcce6c541e6f3f86fbde4"  # round46/as-2.signing.json, both halves
_spec = importlib.util.spec_from_file_location("zero_signing", os.path.join(HERE, "as-2.signing.py"))
zs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(zs)
w42, pg, store, wt = zs.w42, zs.pg, zs.store, zs.wt
UNIVERSE = os.environ["HVST_GOLD_UNIVERSE"]


def finish(record, rc):
    path = os.path.join(HERE, "as-2.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.date.fromisoformat(os.environ["HVST_AS_OF"])
    record = {"stamp": stamp, "as_of": str(as_of), "universe_file": UNIVERSE, "act": "chatter_window union build list (HVST-as-2)"}
    real = store._default_client()
    before = pg._latest_gold_snapshot_rows(wt.TABLE)
    record["before"] = {"parts": w42.window_parts(real), "rows": len(before), "digest": w42.digest(before)}
    gate_out = os.path.join(HERE, "as-2.signing_gate_%s.json" % stamp)
    gate = subprocess.run([sys.executable, os.path.join(HERE, "as-2.signing.py")], cwd=w42.c.ROOT,
                          capture_output=True, text=True, timeout=3000,
                          env=dict(os.environ, GOLD_WINDOW_ZERO_SIGNING_OUT=gate_out))
    record["gate"] = gate.stdout.strip().splitlines()[-5:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (explicit zero rows): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the explicit-zero dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    gate_digest = json.load(open(gate_out, encoding="utf-8"))["built_digest"]
    record["gate_digest"] = gate_digest
    if gate_digest != SIGNED_DIGEST:
        record["result"] = "STOP: gate digest %s != the signed %s; nothing written" % (gate_digest, SIGNED_DIGEST)
        print(record["result"])
        return finish(record, 1)
    p = subprocess.run([sys.executable, "-m", "lib.research.harvest.window_tone", "build", "--securities-json", UNIVERSE,
                        "--as-of", str(as_of)], cwd=w42.c.ROOT, capture_output=True, text=True, timeout=3000)
    record["build"] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}
    print("window_tone build rc", p.returncode)
    if p.returncode != 0:
        record["result"] = "STOP: window_tone build rc %d" % p.returncode
        return finish(record, 1)
    after = pg._latest_gold_snapshot_rows(wt.TABLE)
    k = lambda r: (r["security_key"], r["window_days"])  # noqa: E731
    old, new = {k(r): r for r in before}, {k(r): r for r in after}
    zero_names = {x[0] for x in new if x not in old}
    verdict = {"parts_after": w42.window_parts(real), "rows": len(after),
               "gone": sum(1 for x in old if x not in new),
               "changed": sum(1 for x in old if x in new and zs.dumps(old[x]) != zs.dumps(new[x])),
               "added": sum(1 for x in new if x not in old), "added_names": sorted(zero_names),
               "added_not_explicit_zero": sum(1 for x in new if x not in old
                                             and any(new[x][f] != v for f, v in zs.ZERO.items())),
               "digest_equals_gate": w42.digest(after) == gate_digest}
    verdict["holds"] = (verdict["rows"] == EXPECT_ROWS and not verdict["gone"] and not verdict["changed"]
                        and not verdict["added_not_explicit_zero"] and verdict["digest_equals_gate"])
    record["verify"] = verdict
    print("VERIFY:", json.dumps({x: v for x, v in verdict.items() if x != "parts_after"}))
    if verdict["holds"]:
        record["result"] = "DONE: the explicit-zero rule holds on the written part"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(wt.TABLE, before, as_of, run_stamp, schema=wt.GOLD_WINDOW_SCHEMA)
    back = pg._latest_gold_snapshot_rows(wt.TABLE)
    record["rollback"] = {"digest_equal": w42.digest(back) == record["before"]["digest"], "rows": len(back)}
    record["result"] = "ROLLED BACK: the rule failed on the written part"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
