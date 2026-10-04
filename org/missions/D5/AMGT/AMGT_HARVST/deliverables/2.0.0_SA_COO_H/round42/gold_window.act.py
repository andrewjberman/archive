"""HARVST round 42 HVST-ao-1 -- THE ACT (issuer; only under the signed never-widen pair,
`round42/NEVER_WIDEN_HALF_COO_GOLD_WINDOW.md` + the CTO half).

BEFORE: `chatter_window` parts (0 at signing); GATE = round42/gold_window.signing.py (writes nothing unless
`RULE (window build): HOLDS`); ACT = `window_tone build`, once; VERIFY on the WRITTEN part = the same independent recompute
plus its digest equal to the gate's; ROLLBACK (a first mint has no BEFORE rows) = an EMPTY newer part through `write_gold`
(never-overwrite), so a reader sees no windows, as before the act. Nothing is deleted. Writes
`round42/gold_window_act_<stamp>.json`.
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
_spec = importlib.util.spec_from_file_location("win_signing", os.path.join(HERE, "gold_window.signing.py"))
ws = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ws)
c, pg, store, wt, fs, tc = ws.c, ws.pg, ws.store, ws.wt, ws.fs, ws.trading_calendar
UNIVERSE = os.environ["HVST_GOLD_UNIVERSE"]


def finish(record, rc):
    path = os.path.join(HERE, "gold_window_act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    record = {"stamp": stamp, "as_of": str(as_of), "universe_file": UNIVERSE, "act": "chatter_window first mint (HVST-ao-1)"}
    real = store._default_client()
    record["before"] = {"parts": ws.window_parts(real)}
    gate_out = os.path.join(HERE, "gold_window_signing_gate_%s.json" % stamp)
    gate = subprocess.run([sys.executable, os.path.join(HERE, "gold_window.signing.py")], cwd=c.ROOT, capture_output=True,
                          text=True, timeout=3000, env=dict(os.environ, GOLD_WINDOW_SIGNING_OUT=gate_out))
    record["gate"] = gate.stdout.strip().splitlines()[-6:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (window build): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the window-build dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    gate_digest = json.load(open(gate_out, encoding="utf-8"))["built_digest"]
    p = subprocess.run([sys.executable, "-m", "lib.research.harvest.window_tone", "build", "--securities-json", UNIVERSE,
                        "--as-of", str(as_of)], cwd=c.ROOT, capture_output=True, text=True, timeout=3000)
    record["build"] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}
    print("window_tone build rc", p.returncode)
    if p.returncode != 0:
        record["result"] = "STOP: window_tone build rc %d" % p.returncode
        return finish(record, 1)
    parts = ws.window_parts(real)
    rows = pg._latest_gold_snapshot_rows(wt.TABLE)
    wanted = {s["security_key"] for s in json.load(open(UNIVERSE, encoding="utf-8"))}
    mention = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_TABLE) if r.get("security_key") in wanted]
    window_end = tc.prev_trading_day(as_of)
    expect = ws.recompute(mention, fs.latest_scores(real), window_end)
    def same(r):
        e = expect.get((r["security_key"], r["window_days"]))
        if e is None or any(r[k] != e[k] for k in ("articles_total", "scored", "voters")):
            return False
        if r["tone"] is None or e["tone"] is None:
            return r["tone"] is None and e["tone"] is None
        return abs(r["tone"] - e["tone"]) < 1e-12
    mismatch = sum(1 for r in rows if not same(r))
    verdict = {"parts_after": parts, "new_parts": len(parts) - len(record["before"]["parts"]), "rows": len(rows),
               "mismatch": mismatch, "tone_null_not_iff_zero_voters": sum(1 for r in rows if (r["tone"] is None) != (r["voters"] == 0)),
               "digest_equals_gate": ws.digest(rows) == gate_digest}
    verdict["holds"] = (verdict["new_parts"] == 1 and rows and not mismatch and not verdict["tone_null_not_iff_zero_voters"]
                        and verdict["digest_equals_gate"])
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items() if k != "parts_after"}))
    if verdict["holds"]:
        record["result"] = "DONE: the window-build rule holds on the written part"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(wt.TABLE, [], as_of, run_stamp, schema=wt.GOLD_WINDOW_SCHEMA)
    record["rollback"] = {"rows_after_rollback": len(pg._latest_gold_snapshot_rows(wt.TABLE))}
    record["result"] = "ROLLED BACK: the rule failed on the written part (an empty newer part is served)"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
