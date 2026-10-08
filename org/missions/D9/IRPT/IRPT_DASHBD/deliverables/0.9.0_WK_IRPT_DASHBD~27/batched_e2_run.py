"""TO-DB-b-48 (E2): the extended reporting-gold handler's own --local mode over its own population for ONE day, ONE batch size, ONE process.

Usage (from the worktree root): python <this file> <day> <batch_size> <outdir> <record.json>

handler.local(...) runs UNCHANGED apart from the batch size it is passed; this driver wraps three handler functions (`compute` = returns
stage, `class_days` = class stage, `lots_days` = lots stage) with a stopwatch and samples the process working set from a second thread.
Peak per stage = the largest working set sampled every 0.25 s while the stage ran, raised to the process's own `peak_wset` at the stage's
end when that counter rose during the stage. The total peak is the process `peak_wset`. Wall cap 3600 s: a watchdog writes a partial
record (`stopped_at_cap` true) and ends the process. Nothing here writes S3 or changes a limit.
"""
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
PRODUCER_REL = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
CAP = 3600
MB = 2 ** 20


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def main(day, batch_size, outdir, record_path):
    import psutil
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    proc = psutil.Process()
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
    import handler as h

    state = {"stage": "setup", "stages": {}, "stop": False, "pop": None, "set": None, "lots_refused": None}
    peak_mb = {}

    def wset():
        return proc.memory_info().wset

    def sampler():
        while not state["stop"]:
            v = wset() / MB
            cur = state["stage"]
            if v > peak_mb.get(cur, 0.0):
                peak_mb[cur] = v
            time.sleep(0.25)

    def reporter():
        while not state["stop"]:
            print("PROGRESS " + json.dumps({"elapsed_s": round(time.time() - state["t0"], 1), "stage": state["stage"],
                                            "wset_mb": round(wset() / MB, 1),
                                            "peak_wset_mb": round(proc.memory_info().peak_wset / MB, 1)}), flush=True)
            time.sleep(30)

    def wrap(name, fn):
        def wrapper(*a, **k):
            state["stage"] = name
            before = proc.memory_info().peak_wset
            peak_mb.setdefault(name, wset() / MB)
            t0 = time.time()
            state["stages"][name] = {"wall": 0.0, "done": False}
            ok = False
            try:
                r = fn(*a, **k)
                ok = True
                return r
            finally:
                pk = proc.memory_info().peak_wset
                if pk > before:
                    peak_mb[name] = max(peak_mb.get(name, 0.0), pk / MB)
                state["stages"][name] = {"wall": time.time() - t0, "done": ok}
                state["stage"] = "between"
        return wrapper

    h.compute = wrap("returns", h.compute)
    h.class_days = wrap("class", h.class_days)
    _lots = wrap("lots", h.lots_days)

    def lots_inspect(*a, **k):
        rows_by_day, failed = _lots(*a, **k)
        if failed:
            state["lots_refused"] = {"days_failed": sorted(failed), "reason_head": sorted(failed.values())[0][:160]}
            state["stages"]["lots"]["done"] = False
        return rows_by_day, failed
    h.lots_days = lots_inspect
    orig_pop, orig_set = h.population_accounts, h.account_set

    def pop_wrap(s3, firm):
        r = orig_pop(s3, firm)
        state["pop"] = list(r[1])
        return r

    def set_wrap(population, newest):
        r = orig_set(population, newest)
        state["set"] = list(r)
        return r
    h.population_accounts, h.account_set = pop_wrap, set_wrap

    def build(stopped, local_exit):
        stages = {}
        for s in ("returns", "class", "lots"):
            st = state["stages"].get(s)
            stages[s] = {"wall_seconds": None if st is None else round(st["wall"], 2),
                         "peak_mb": round(peak_mb.get(s, 0.0), 1) if (st is not None or s == state["stage"]) else None,
                         "completed": bool(st and st.get("done"))}
        total_wall = time.time() - state["t0"]
        return {
            "batch_size": int(batch_size), "day": day, "stopped_at_cap": bool(stopped), "cap_seconds": CAP,
            "stage_in_progress_at_stop": state["stage"] if stopped else None,
            "lots": {"wall_seconds": stages["lots"]["wall_seconds"], "peak_mb": stages["lots"]["peak_mb"],
                     "completed": stages["lots"]["completed"]},
            "returns": stages["returns"], "class": stages["class"],
            "total": {"wall_seconds": round(total_wall, 2), "peak_mb": round(proc.memory_info().peak_wset / MB, 1),
                      "peak_basis": "process peak_wset (Windows peak working set) from the start of the process"},
            "population_count": None if state["pop"] is None else len(state["pop"]),
            "accounts_run": None if state["set"] is None else len(state["set"]),
            "lots_refused": state["lots_refused"], "local_exit_head": local_exit}

    threading.Thread(target=sampler, daemon=True).start()
    state["t0"] = time.time()
    threading.Thread(target=reporter, daemon=True).start()

    def watchdog():
        while not state["stop"]:
            if time.time() - state["t0"] > CAP:
                rec = build(True, None)
                Path(record_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
                print("STOPPED_AT_CAP", flush=True)
                os._exit(3)
            time.sleep(1)
    threading.Thread(target=watchdog, daemon=True).start()
    local_exit = None
    try:
        h.local(day, out / "returns.parquet", accounts=None, workers=12, class_out=str(out / "class.parquet"),
                lots_out_dir=str(out), batch_size=int(batch_size))
    except SystemExit as exc:
        local_exit = str(exc)[:120]
        print("LOCAL_EXIT " + local_exit, flush=True)
    state["stop"] = True
    rec = build(False, local_exit)
    Path(record_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("DONE " + json.dumps({"batch_size": rec["batch_size"], "lots": rec["lots"], "total": rec["total"]}), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
