"""TO-DB-b-110: per-stage peak memory of the reporting-gold handler's --local run for ONE kit day, ONE process (S3 GETs only).

Usage (worktree root): python <this file> <day> <outdir> <record.json>

handler.local(...) runs UNCHANGED (default batch size, as a CLI run with no --batch-size does); this driver wraps handler stage functions
(compute = returns, class_days = class, lots_days = lots) and the producer's own sub-stage functions (read_window = lots_read,
classify_flow_days = lots_classify, unrealized_rows = lots_unrealized, realized_rows = lots_realized, apply_inkind_reference =
lots_inkind, check_rows = lots_check, activity_row = lots_activity) with a stack. The status write (record_lots_status) is called once
with a STUB client whose put_object only counts: no S3 write.

Memory = process RSS (psutil memory_info().rss; the Windows working set) sampled every 0.05 s from a second thread; a sample counts for
every stage on the stack. The record carries counts, sha256 and MB only: no account number.
"""
import hashlib
import importlib
import json
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
MB = 2 ** 20
TABLES = ("returns", "class", "account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily")


class StubS3:
    """record_lots_status's client: get_object finds nothing, put_object is counted and discards."""
    puts = 0

    def get_object(self, **k):
        class NoSuchKey(Exception):
            pass
        raise NoSuchKey("stub")

    def put_object(self, **k):
        StubS3.puts += 1
        return {}


def main(day, outdir, record_path):
    import psutil
    import pyarrow.parquet as pq
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    proc = psutil.Process()
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
    h = importlib.import_module("handler")
    aal = h.aal
    stack, peak, wall, state = [], {}, {}, {"stop": False}
    lock = threading.Lock()

    def sampler():
        while not state["stop"]:
            v = proc.memory_info().rss / MB
            with lock:
                for s in set(stack):
                    if v > peak.get(s, 0.0):
                        peak[s] = v
                state["proc"] = max(state.get("proc", 0.0), v)
            time.sleep(0.05)

    def wrap(mod, attr, name):
        fn = getattr(mod, attr)

        def wrapper(*a, **k):
            with lock:
                stack.append(name)
                peak.setdefault(name, proc.memory_info().rss / MB)
            t0 = time.time()
            try:
                return fn(*a, **k)
            finally:
                with lock:
                    stack.remove(name)
                    wall[name] = wall.get(name, 0.0) + time.time() - t0
        setattr(mod, attr, wrapper)

    wrap(h, "compute", "returns")
    wrap(h, "class_days", "class")
    wrap(h, "lots_days", "lots")
    for attr, name in (("read_window", "lots_read"), ("classify_flow_days", "lots_classify"), ("unrealized_rows", "lots_unrealized"),
                       ("realized_rows", "lots_realized"), ("apply_inkind_reference", "lots_inkind"), ("check_rows", "lots_check"),
                       ("activity_row", "lots_activity")):
        wrap(aal, attr, name)
    wrap(h, "record_lots_status", "status_write")
    threading.Thread(target=sampler, daemon=True).start()
    t0 = time.time()
    h.local(day, out / "returns.parquet", accounts=None, workers=12, class_out=str(out / "class.parquet"), lots_out_dir=str(out),
            batch_size=None)
    firm = h.ard.firm_scope(h.ard.source_entry(h.ard.load_declaration(), h.ard.declared_sources(h.ard.load_declaration())[0]))
    h.record_lots_status(StubS3(), firm, set(), {day: "harness stub"}, True)
    state["stop"] = True
    time.sleep(0.2)
    hashes = {}
    for t in TABLES:
        p = out / ("%s.parquet" % t)
        hashes[t] = {"rows": pq.ParquetFile(str(p)).metadata.num_rows, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    rec = {"day": day, "method": "process RSS (psutil memory_info().rss, Windows working set) sampled every 0.05 s; a sample counts for "
                                 "every stage on the stack",
           "stage_peak_mb": {k: round(v, 1) for k, v in sorted(peak.items())},
           "stage_wall_s": {k: round(v, 1) for k, v in sorted(wall.items())},
           "process_peak_mb": round(state["proc"], 1), "wall_s": round(time.time() - t0, 1), "status_stub_puts": StubS3.puts,
           "output_hashes": hashes,
           "code_sha256": {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in (
               "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py",
               "data/assets/scripts/gold/irpt_reporting/account_return_daily.py",
               "data/assets/scripts/gold/irpt_reporting/account_class_daily.py",
               "infra/aws/lambda/investor-reporting/reporting-gold/handler.py")}}
    Path(record_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("DONE " + json.dumps({"stage_peak_mb": rec["stage_peak_mb"], "process_peak_mb": rec["process_peak_mb"]}), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
