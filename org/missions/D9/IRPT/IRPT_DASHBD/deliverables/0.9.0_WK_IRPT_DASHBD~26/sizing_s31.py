"""TO-DB-b-46 (row S31): the extended reporting-gold handler measured over its own population for ONE trading day, in ONE process.

Usage (from the worktree root):
  python <this file> run <day> <outdir> <record.json>

The handler and the producer are imported and run UNCHANGED (`handler.local(...)`, the same population function the scheduled fire
uses). This driver only wraps three handler functions (`compute` = returns stage, `class_days` = class stage, `lots_days` = lots
stage) and a few producer functions with a stopwatch, and samples the process working set from a second thread. Nothing here edits
the handler or the producer, writes to S3, or changes a limit.

Peak memory per stage = the largest working set sampled while the stage ran (every 0.25 s), raised to the process's own
`peak_wset` at the stage's end when that counter rose during the stage (then it is exact). The total peak is the process `peak_wset`.
Wall cap 3600 s: a watchdog thread writes a partial record (`stopped_at_cap` true) and ends the process.
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


def pct(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q
    f = int(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def main(day, outdir, record_path):
    import psutil
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    proc = psutil.Process()
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
    t_import = time.time()
    import handler as h
    aal = h.aal
    imp_s = time.time() - t_import

    state = {"stage": "setup", "stages": {}, "acct_times": [], "sub": {}, "lock": threading.Lock(), "pop": None, "set": None,
             "stop": False, "stage_started": None}
    peak_mb = {}
    t_start = time.time()

    def wset():
        return proc.memory_info().wset

    def sampler():
        while not state["stop"]:
            cur = state["stage"]
            v = wset() / MB
            if v > peak_mb.get(cur, 0.0):
                peak_mb[cur] = v
            time.sleep(0.25)

    def progress_line():
        return {"elapsed_s": round(time.time() - t_start, 1), "stage": state["stage"], "wset_mb": round(wset() / MB, 1),
                "peak_wset_mb": round(proc.memory_info().peak_wset / MB, 1), "accounts_in_activity_loop": len(state["acct_times"])}

    def reporter():
        while not state["stop"]:
            print("PROGRESS " + json.dumps(progress_line()), flush=True)
            time.sleep(30)

    def machine():
        return {"cores_physical": psutil.cpu_count(logical=False), "cores_logical": psutil.cpu_count(),
                "ram_gb": round(psutil.virtual_memory().total / 2 ** 30, 1)}

    def tail(vals):
        return {"p50": pct(vals, 0.50), "p95": pct(vals, 0.95), "p99": pct(vals, 0.99), "max": max(vals) if vals else None}

    def build(stopped):
        stages = {}
        for s in ("returns", "class", "lots"):
            st = state["stages"].get(s)
            stages[s] = {"wall_seconds": None if st is None else round(st["wall"], 2),
                         "peak_mb": round(peak_mb.get(s, 0.0), 1) if st is not None or s == state["stage"] else None,
                         "completed": st is not None and st.get("done", False)}
        total_wall = time.time() - state["local_t0"] if state.get("local_t0") else None
        total_peak = proc.memory_info().peak_wset / MB
        lots = state["stages"].get("lots")
        accts = state["set"]
        lots_wall = lots["wall"] if lots else None
        at = state["acct_times"]
        limits = {"timeout_s": 900, "memory_mb": 2048}
        breach = []
        if stopped or (total_wall is not None and total_wall > 900):
            breach.append({"limit": "timeout_s", "limit_value": 900,
                           "measured": None if total_wall is None else round(total_wall, 1),
                           "over_by_seconds": None if total_wall is None else round(total_wall - 900, 1),
                           "note": "run stopped at the cap, so the true total is at least this" if stopped else ""})
        if total_peak > 2048:
            breach.append({"limit": "memory_mb", "limit_value": 2048, "measured": round(total_peak, 1),
                           "over_by_mb": round(total_peak - 2048, 1)})
        fits = (not stopped) and total_wall is not None and total_wall <= 900 and total_peak <= 2048
        rec = {
            "task_order": "IRPT_DASHBD.TO-DB-b-46", "worker": "0.9.0_WK_IRPT_DASHBD~26", "day": day,
            "population_count": None if state["pop"] is None else len(state["pop"]),
            "population_day": state.get("pop_day"),
            "account_set_count": None if accts is None else len(accts),
            "accounts_run": 0 if accts is None else (len(accts) if not stopped else state.get("accounts_finished", 0)),
            "stopped_at_cap": bool(stopped), "cap_seconds": CAP,
            "stage_in_progress_at_stop": state["stage"] if stopped else None,
            "lots_stage_completed": "lots_refused" not in state and state["stages"].get("lots", {}).get("done", False),
            "lots_refused": state.get("lots_refused"),
            "accounts_run_note": ("accounts_run = the accounts the run was given and read through in all three stages' reads; "
                                  "see lots_stage_completed and lots_refused for how far the lots stage got"),
            "stages": stages,
            "stage_other_seconds": {"population_and_setup": round(state.get("pop_wall", 0.0), 2),
                                    "returns_parquet_write": round(state.get("write_wall", 0.0), 2)},
            "total": {"wall_seconds": None if total_wall is None else round(total_wall, 2), "peak_mb": round(total_peak, 1),
                      "peak_basis": "process peak_wset (Windows peak working set), from the start of the process"},
            "limits": limits,
            "per_account_seconds": {k: (None if v is None else round(v, 6)) for k, v in tail(at).items()},
            "per_account_basis": ("seconds in the producer's per-account `activity_row` call, the only per-account step the lots stage "
                                  "runs; the stage's reads and classification are batched over all accounts and are not per-account"),
            "per_account_samples": len(at),
            "lots_stage_seconds_per_account_mean": (None if not (lots_wall and accts) else round(lots_wall / len(accts), 4)),
            "lots_substeps_seconds": {k: round(v, 2) for k, v in sorted(state["sub"].items())},
            "verdict": "FITS" if fits else "BREACH", "breach": breach,
            "handler_sha256": sha(HANDLER_REL), "producer_sha256": sha(PRODUCER_REL),
            "machine": machine(), "workers": 12, "handler_import_seconds": round(imp_s, 2),
            "peak_method": "max working set sampled every 0.25 s while the stage ran, raised to process peak_wset at stage end when it rose in the stage",
        }
        return rec

    def stage_wrap(name, fn):
        def wrapper(*a, **k):
            state["stage"] = name
            peak_before = proc.memory_info().peak_wset
            peak_mb.setdefault(name, wset() / MB)
            t0 = time.time()
            state["stages"][name] = {"wall": 0.0, "done": False}
            try:
                return fn(*a, **k)
            finally:
                wall = time.time() - t0
                pk = proc.memory_info().peak_wset
                if pk > peak_before:
                    peak_mb[name] = max(peak_mb.get(name, 0.0), pk / MB)
                state["stages"][name] = {"wall": wall, "done": True}
                state["stage"] = "between"
        return wrapper

    def sub_wrap(mod, attr, label):
        fn = getattr(mod, attr)

        def wrapper(*a, **k):
            t0 = time.time()
            try:
                return fn(*a, **k)
            finally:
                if state["stage"] == "lots":
                    state["sub"][label] = state["sub"].get(label, 0.0) + (time.time() - t0)
        setattr(mod, attr, wrapper)

    def acct_wrap(fn):
        def wrapper(*a, **k):
            t0 = time.time()
            try:
                return fn(*a, **k)
            finally:
                with state["lock"]:
                    state["acct_times"].append(time.time() - t0)
        return wrapper

    # the stage wrappers: the handler's own functions, called by the handler's own local()
    h.compute = stage_wrap("returns", h.compute)
    h.class_days = stage_wrap("class", h.class_days)
    _lots = stage_wrap("lots", h.lots_days)

    def lots_inspect(*a, **k):
        rows_by_day, failed = _lots(*a, **k)
        if failed:
            reason = sorted(failed.values())[0]
            state["lots_refused"] = {
                "days_failed": sorted(failed),
                "reason_class": reason.split(":")[0] + ": " + ("REFUSED: realized lot id repeats in one frame"
                                                               if "appears twice in one frame" in reason else reason[:160]),
                "reason_sha256": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
                "refused_at_wall_seconds_into_run": round(time.time() - state["local_t0"], 1),
                "activity_loop_accounts_reached": len(state["acct_times"])}
            if state["stages"].get("lots"):
                state["stages"]["lots"]["done"] = False
        return rows_by_day, failed
    h.lots_days = lots_inspect
    # the handler's population functions, timed and captured
    orig_pop = h.population_accounts
    orig_set = h.account_set

    def pop_wrap(s3, firm):
        t0 = time.time()
        r = orig_pop(s3, firm)
        state["pop_day"], state["pop"] = r[0], list(r[1])
        state["pop_wall"] = state.get("pop_wall", 0.0) + (time.time() - t0)
        return r

    def set_wrap(population, newest):
        r = orig_set(population, newest)
        state["set"] = list(r)
        return r
    h.population_accounts = pop_wrap
    h.account_set = set_wrap
    # per-account step and lots sub-steps
    aal.activity_row = acct_wrap(aal.activity_row)
    for attr in ("read_window", "classify_flow_days", "unrealized_rows", "realized_rows", "apply_inkind_reference"):
        sub_wrap(aal, attr, attr)
    sub_wrap(aal.ard, "first_data_dates", "first_data_dates")

    def watchdog():
        while not state["stop"]:
            if time.time() - state["local_t0"] > CAP:
                state["accounts_finished"] = 0
                rec = build(True)
                rec["accounts_finished_note"] = ("the stages are batched over all accounts; none of the %d accounts had finished "
                                                 "all three stages when the cap passed" % (len(state["set"] or [])))
                Path(record_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
                print("STOPPED_AT_CAP " + json.dumps(progress_line()), flush=True)
                os._exit(3)
            time.sleep(1)

    threading.Thread(target=sampler, daemon=True).start()
    threading.Thread(target=reporter, daemon=True).start()
    state["local_t0"] = time.time()
    threading.Thread(target=watchdog, daemon=True).start()
    # the handler's own --local mode: no explicit accounts, so it takes its own population
    local_exit = None
    try:
        h.local(day, out / "returns.parquet", accounts=None, workers=12, class_out=str(out / "class.parquet"),
                lots_out_dir=str(out))
    except SystemExit as exc:
        # the handler's own --local refuses when the lots stage refuses; the stages up to it are measured, the refusal is recorded
        local_exit = str(exc)[:80]
        print("LOCAL_EXIT " + local_exit, flush=True)
    state["stop"] = True
    total = time.time() - state["local_t0"]
    accounted = sum(s["wall"] for s in state["stages"].values()) + state.get("pop_wall", 0.0)
    state["write_wall"] = max(0.0, total - accounted)
    rec = build(False)
    rec["local_exit_head"] = local_exit
    Path(record_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("DONE " + json.dumps({"total": rec["total"], "stages": rec["stages"], "verdict": rec["verdict"]}), flush=True)


if __name__ == "__main__":
    if sys.argv[1] != "run":
        raise SystemExit("usage: run <day> <outdir> <record.json>")
    main(sys.argv[2], sys.argv[3], sys.argv[4])
