"""IRPT_DASHBD round 125, workstream B-49F, cell DB-b-255 (worker 0.9.0_WK_IRPT_DASHBD~208): the MEMORY of the Cottonwood
account-return landing function, measured LOCAL and read-only.

It imports the handler of THIS worktree and calls lambda_handler in dry-run for two days: 2026-07-10 and the newest silver
fact_allocations partition. The reader is one real CottonwoodBlackDiamondSilverReader, and its client refuses every operation
but GetObject and ListObjectsV2. The s3 argument is an object with no methods, so no write call can be reached from it. A
daemon thread samples the process resident set size every SAMPLE_SECONDS over the whole measured section, and a direct
reading is taken before and after each day. The process holds the interpreter, pandas, pyarrow and boto3, which a Lambda also
holds; nothing is subtracted.

It writes one private counts copy to the directory given as its only argument, and nothing else.

Usage: python -I <this file> <private_dir>
"""
import json
import re
import sys
import threading
import time
from pathlib import Path

import psutil

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
HANDLER_DIR = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "account-return-daily"
sys.path.insert(0, str(HANDLER_DIR))

import handler as h  # noqa: E402

FIRST_DAY = "2026-07-10"
ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}$")
READ_OPS = ("GetObject", "ListObjectsV2")
SAMPLE_SECONDS = 0.1
MB = 1048576.0
SIZES_MB = [512, 1024, 1536, 2048, 3008, 4096, 6144, 8192, 10240]
THRESHOLD = 0.7
COUNTS = {}


class NoWrite(object):
    """The s3 argument of the handler: it has no methods, so any use of it raises AttributeError."""


def _hook(model=None, **kwargs):
    name = model.name if model is not None else "unnamed"
    if name not in READ_OPS:
        raise SystemExit("REFUSED: S3 operation %s is not a read; this measurement reads only" % name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def _phase(name, fn):
    try:
        return fn()
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        print("BLOCKED: phase %s raised %s" % (name, type(exc).__name__))
        sys.exit(2)


class Sampler(threading.Thread):
    def __init__(self, proc):
        threading.Thread.__init__(self)
        self.daemon = True
        self.proc = proc
        self.halt = threading.Event()
        self.lock = threading.Lock()
        self.samples = []

    def take(self):
        value = self.proc.memory_info().rss
        with self.lock:
            self.samples.append(value)
        return value

    def run(self):
        while not self.halt.is_set():
            self.take()
            self.halt.wait(SAMPLE_SECONDS)

    def mark(self):
        with self.lock:
            return len(self.samples)

    def peak_since(self, index):
        with self.lock:
            window = self.samples[index:]
        return max(window)

    def count(self):
        with self.lock:
            return len(self.samples)

    def stop(self):
        self.halt.set()
        self.join()


def choose(peak_mb):
    for s in SIZES_MB:
        if s >= 512 and peak_mb <= THRESHOLD * s:
            return s
    return None


def newest_day(reader):
    parts = [p for p in reader.list_partitions("fact_allocations") if ISO.match(p)]
    if not parts:
        print("BLOCKED: phase newest_day found no fact_allocations partition")
        sys.exit(2)
    return parts[-1]


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python -I <this file> <private_dir>")
    priv = Path(argv[1])
    proc = psutil.Process()
    baseline = proc.memory_info().rss
    reader = h.cbd.CottonwoodBlackDiamondSilverReader()
    reader._api().meta.events.register("before-call.s3", _hook)
    sampler = Sampler(proc)
    sampler.start()
    newest = _phase("newest_day", lambda: newest_day(reader))
    measured = []
    for day in (FIRST_DAY, newest):
        i0 = sampler.mark()
        sampler.take()
        t0 = time.perf_counter()
        out = _phase("lambda_handler", lambda: h.lambda_handler({"day": day, "dry_run": True}, None, s3=NoWrite(), reader=reader))
        secs = time.perf_counter() - t0
        res = out["results"][day]
        if res.get("held") or out.get("held"):
            print("BLOCKED: the handler holds day %s: %s" % (day, res.get("reason")))
            sampler.stop()
            sys.exit(2)
        accounts = _phase("accounts_in_partition", lambda: len(h.cbd.accounts_in_partition(reader, day)))
        sampler.take()
        peak = sampler.peak_since(i0)
        measured.append({"day": day, "accounts": accounts, "rows": int(res["rows"]), "seconds": round(secs, 3),
                         "peak_rss_mb": round(peak / MB, 1), "held": False})
        print("OK: day %s measured: %d account(s), %d row(s), %.3f s, peak %.1f MB" % (day, accounts, res["rows"], secs, peak / MB))
    sampler.stop()
    peak_all = max(d["peak_rss_mb"] for d in measured)
    chosen = choose(peak_all)
    result = {
        "firm": "cottonwood",
        "days": measured,
        "baseline_rss_mb": round(baseline / MB, 1),
        "peak_rss_mb": peak_all,
        "threshold_fraction": THRESHOLD,
        "sizes_mb": SIZES_MB,
        "chosen_memory_mb": chosen,
        "sampler": {
            "interval_seconds": SAMPLE_SECONDS,
            "samples": sampler.count(),
            "method": "psutil.Process().memory_info().rss read by a daemon thread every 0.1 s over the measured section, "
                      "plus a direct reading before and after each day",
        },
        "s3_calls_by_operation": dict(sorted(COUNTS.items())),
        "s3_reads": sum(COUNTS.values()),
        "reader_reads": reader.reads,
    }
    priv.mkdir(parents=True, exist_ok=True)
    (priv / "cot_memory_r125.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("OK: baseline %.1f MB, peak %.1f MB, chosen %s MB, samples %d, S3 reads %d"
          % (baseline / MB, peak_all, chosen, result["sampler"]["samples"], result["s3_reads"]))
    print("OK: private copy written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
