"""TO-DB-b-22 -- the concurrent completion of the ONE Black Diamond population pull (E3 / P-5): one coordinator, one shared bearer,
2 then 6 workers, one retry per call, FAILED recorded, one sweep.

Ruled by 1.0.0_SA_CTO RULINGS batch 249 (msg 105079: concurrent workers on ONE shared bearer) and batch 250 (msg 105082: one retry
per call; a twice-failed account is recorded, not fatal). The DB-b-20 pull (bd_population_pull_e3.py) and the DB-b-21 sequential
completion (bd_population_complete_e3.py) are imported by path and their address builder, plan derivation, denominators and canon
are reused, never copied.

Usage: python bd_population_concurrent_e3.py <repo_root> plan | run --go | sweep --go
  plan   OFFLINE (DRY_RUN=1, S3 list reads only). Writes BD_POPULATION_CONCURRENT_PLAN_E3.json: every field of the DB-b-21
         completion plan plus the `ruling` object, and prints both denominators (planned = landed + complement).
  run    LIVE, needs --go, run by the issuer and never by the worker that built it. Refuses unless --go is given, the plan exists
         and is re-derived identically from a fresh S3 listing, and its `ruling` object is present. One coordinator mints the shared
         bearer (one mint at a time under a lock; re-minted at mint_interval_s, or early on a 401 from a bearer older than
         fresh_mint_s). Worker threads take the complement from ONE queue under ONE shared rate limiter; ramp 2 -> 6 after
         ramp_after_s with no 401 and no 429; a 429 halves the workers; one retry per call; a call failing twice is recorded FAILED
         and the run continues. The run aborts on 3 consecutive failed calls, a 401 on a bearer younger than fresh_mint_s, any
         other 4xx, a landing failure, or FAILED above failed_cap. Writes BD_POPULATION_CONCURRENT_E3.json (checkpoint every 50
         calls and in a finally; an earlier record is renamed with a timestamp). A credential, bearer or body is never logged.
  sweep  LIVE, needs --go, the issuer's. Reads the last run record's FAILED set, refuses unless it is at most failed_cap and every
         class is transport, 5xx or 429, prints the set, requests each account once under the same coordinator rules, prints the
         residue, and writes BD_POPULATION_CONCURRENT_SWEEP_E3.json.
"""
import importlib.util
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
C21_PATH = HERE.parent / "0.9.0_WK_IRPT_DASHBD~7" / "bd_population_complete_e3.py"
PLAN_NAME = "BD_POPULATION_CONCURRENT_PLAN_E3.json"
RUN_NAME = "BD_POPULATION_CONCURRENT_E3.json"
SWEEP_NAME = "BD_POPULATION_CONCURRENT_SWEEP_E3.json"
PULL_DATE = "20261004"  # the ONE pull's partition, as in DB-b-21
CHECKPOINT_EVERY = 50
BACKOFF_DEFAULT_S = 30.0
SWEEPABLE = ("transport", "5xx", "429")
RULING = {
    "ruling_ids": ["1.0.0_SA_CTO RULINGS batch 249", "1.0.0_SA_CTO RULINGS batch 250"],
    "workers_start": 2, "workers_max": 6, "ramp_after_s": 600, "aggregate_rps": 2,
    "retries_per_call": 1, "consecutive_failures_abort": 3, "failed_cap": 105,
    "mint_interval_s": 120, "fresh_mint_s": 30,
}
_RETRY_AFTER = re.compile(r"retry-after\D{0,4}(\d+(?:\.\d+)?)", re.I)


def load_c21():
    """The DB-b-21 script, imported by path (importlib); nothing of it is copied."""
    spec = importlib.util.spec_from_file_location("bd_population_complete_e3_imported", str(C21_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_plan(c21, e20_plan, landed_ids):
    """The concurrent plan: the DB-b-21 completion plan plus the ruling. Pure; the same inputs give the same plan."""
    plan = c21.derive_plan(e20_plan, landed_ids)
    plan["ruling"] = json.loads(json.dumps(RULING))
    return plan


def _status_of(exc):
    msg = str(exc)
    return int(msg.split("HTTP ")[1].split(":")[0]) if "HTTP " in msg else -1


def _retry_after(exc):
    m = _RETRY_AFTER.search(str(exc))
    return float(m.group(1)) if m else BACKOFF_DEFAULT_S


def _class_of(status):
    if status == 429:
        return "429"
    if 500 <= status <= 599:
        return "5xx"
    return None


class Bearer:
    """The ONE coordinator of the shared bearer: a mint happens here, one at a time under a lock, never per worker."""

    def __init__(self, h, clock, mint_interval_s, fresh_mint_s):
        self.h, self.clock = h, clock
        self.mint_interval_s, self.fresh_mint_s = mint_interval_s, fresh_mint_s
        self.lock = threading.Lock()
        self.token, self.gen, self.mints = None, 0, 0
        self.minted = {}

    def _mint(self):
        self.token = self.h.get_clientview_token(self.h.load_bd_session())
        self.gen += 1
        self.mints += 1
        self.minted[self.gen] = self.clock()

    def current(self):
        with self.lock:
            if self.token is None or self.clock() - self.minted[self.gen] >= self.mint_interval_s:
                self._mint()
            return self.token, self.gen

    def age_of(self, gen):
        return self.clock() - self.minted[gen]

    def remint_after_401(self, gen_used):
        """Early re-mint. If another worker already replaced the bearer this call used, nothing is minted."""
        with self.lock:
            if self.gen == gen_used:
                self._mint()
            return self.token, self.gen


class Pacer:
    """ONE rate limiter shared by every worker: slots are handed out aggregate_rps apart."""

    def __init__(self, rps, clock, sleep):
        self.interval = 1.0 / float(rps)
        self.clock, self.sleep = clock, sleep
        self.lock = threading.Lock()
        self.next = 0.0

    def wait(self):
        with self.lock:
            now = self.clock()
            slot = max(now, self.next)
            self.next = slot + self.interval
            delay = slot - now
        if delay > 0:
            self.sleep(delay)


class Run:
    def __init__(self, todo, path, h, s3, on, b20, ruling, clock, sleep, checkpoint=None):
        self.todo, self.path, self.h, self.s3, self.on, self.b20 = todo, path, h, s3, on, b20
        self.ruling, self.clock, self.sleep, self.checkpoint = ruling, clock, sleep, checkpoint
        self.bearer = Bearer(h, clock, ruling["mint_interval_s"], ruling["fresh_mint_s"])
        self.pacer = Pacer(ruling["aggregate_rps"], clock, sleep)
        self.q = queue.Queue()
        for r in todo:
            self.q.put(r)
        self.lock = threading.Lock()
        self.records, self.events, self.threads = [], [], []
        self.target = self.active = self.next_idx = 0
        self.in_flight = self.peak_before_ramp = self.peak = 0
        self.ramped = self.saw_401 = self.saw_429 = False
        self.vendor_calls = self.failed = self.consecutive = 0
        self.abort_reason = None
        self.start = clock()
        self.started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # -- state, all under self.lock ------------------------------------------------------------------------------------
    def _abort(self, reason):
        with self.lock:
            if self.abort_reason is None:
                self.abort_reason = reason

    def _event(self, name, **kw):
        kw.update({"event": name, "t": round(self.clock() - self.start, 3)})
        self.events.append(kw)

    def _spawn_locked(self):
        while self.active < self.target:
            idx = self.next_idx
            self.next_idx += 1
            self.active += 1
            t = threading.Thread(target=self._worker, args=(idx,), daemon=True)
            self.threads.append(t)
            t.start()

    def _snapshot(self, final=False):
        with self.lock:
            recs = list(self.records)
            failed = [{"account": r["account"], "bd_account": r["bd_account"], "class": r["class"]}
                      for r in recs if r["status"] == "FAILED"]
            return {"ruling": self.ruling, "vendor_calls": self.vendor_calls, "bearer_mints": self.bearer.mints,
                    "calls_recorded": len(recs), "landed_this_run": sum(1 for r in recs if r["landed"]),
                    "failed_count": len(failed), "failed": failed, "aborted": self.abort_reason, "complete": final,
                    "not_requested": self.q.qsize(), "workers_target": self.target, "ramped": self.ramped,
                    "peak_in_flight": self.peak, "peak_in_flight_before_ramp": self.peak_before_ramp,
                    "events": list(self.events), "started_at": self.started_at,
                    "elapsed_s": round(self.clock() - self.start, 3), "records": recs}

    def _finish(self, rec, ok):
        with self.lock:
            self.records.append(rec)
            if ok:
                self.consecutive = 0
            elif rec["status"] == "FAILED":
                self.failed += 1
                self.consecutive += 1
                if self.consecutive >= self.ruling["consecutive_failures_abort"] and self.abort_reason is None:
                    self.abort_reason = "%d consecutive failed calls" % self.consecutive
                if self.failed > self.ruling["failed_cap"] and self.abort_reason is None:
                    self.abort_reason = "FAILED %d above failed_cap %d" % (self.failed, self.ruling["failed_cap"])
            due = self.checkpoint is not None and len(self.records) % CHECKPOINT_EVERY == 0
        if due:
            self.checkpoint(self._snapshot())

    # -- workers -------------------------------------------------------------------------------------------------------
    def _maybe_ramp(self):
        with self.lock:
            if (not self.ramped and not self.saw_401 and not self.saw_429 and self.target < self.ruling["workers_max"]
                    and self.clock() - self.start >= self.ruling["ramp_after_s"]):
                self.ramped = True
                self.target = self.ruling["workers_max"]
                self._event("ramp", workers=self.target)
                self._spawn_locked()

    def _worker(self, idx):
        while True:
            self._maybe_ramp()
            with self.lock:
                if self.abort_reason is not None or self.active > self.target:
                    self.active -= 1
                    return
            try:
                r = self.q.get_nowait()
            except queue.Empty:
                with self.lock:
                    self.active -= 1
                return
            self._call(idx, r)

    def _halve(self):
        with self.lock:
            self.saw_429 = True
            self.target = max(1, self.target // 2)
            self._event("halve", workers=self.target)

    def _call(self, idx, r):
        bd = str(r["bd_account"])
        rec = {"account": r["account"], "bd_account": bd, "worker": idx, "ranges": len(r["segments"]),
               "bearer_generation": None, "status": None, "http_status": None, "class": None, "retried": False,
               "landed": None}
        with self.lock:
            self.in_flight += 1
            self.peak = max(self.peak, self.in_flight)
            if not self.ramped:
                self.peak_before_ramp = max(self.peak_before_ramp, self.in_flight)
        try:
            ok = self._attempts(rec, r, bd)
        finally:
            with self.lock:
                self.in_flight -= 1
        self._finish(rec, ok)

    def _attempts(self, rec, r, bd):
        """Up to two attempts (one retry per CALL). Returns True when the response landed."""
        attempts = 0
        while True:
            attempts += 1
            token, gen = self.bearer.current()
            rec["bearer_generation"] = gen
            self.pacer.wait()
            with self.lock:
                self.vendor_calls += 1
            try:
                payload = self.h._request("POST", self.path, token=token, body=r["body"], raw=True)
            except RuntimeError as e:  # HTTP error from the estate client; only the status is kept, never the body
                status = _status_of(e)
                rec["http_status"] = status
                if status == 401:
                    with self.lock:
                        self.saw_401 = True
                    if self.bearer.age_of(gen) < self.ruling["fresh_mint_s"]:
                        rec.update({"status": "STOPPED", "class": "401-fresh-bearer"})
                        self._abort("401 on a bearer younger than fresh_mint_s: a stop, not a retry")
                        return False
                    if attempts == 1:
                        self.bearer.remint_after_401(gen)
                        rec["retried"] = True
                        self._event("remint-401", generation=gen)
                        continue
                    rec.update({"status": "STOPPED", "class": "401-twice"})
                    self._abort("401 twice on one call")
                    return False
                cls = _class_of(status)
                if cls is None:
                    rec.update({"status": "STOPPED", "class": "4xx-other" if 400 <= status < 500 else "unparsed"})
                    self._abort("non-transient error HTTP %d" % status)
                    return False
                if status == 429:
                    self._halve()
                if attempts == 1:
                    rec["retried"] = True
                    if status == 429:
                        self.sleep(_retry_after(e))
                    continue
                rec.update({"status": "FAILED", "class": cls})
                return False
            except (urllib.error.URLError, OSError, TimeoutError):  # transport error
                rec["http_status"] = 0
                if attempts == 1:
                    rec["retried"] = True
                    continue
                rec.update({"status": "FAILED", "class": "transport"})
                return False
            rec["http_status"] = 200
            try:  # a landing failure is non-transient and is recorded, so the record always exists
                json.loads(payload)
                addr = self.b20._address(self.on, PULL_DATE, bd)
                bkt, key = addr[len("s3://"):].split("/", 1)
                self.s3.put_object(Bucket=bkt, Key=key, Body=payload, ContentType="application/json")
                rec.update({"landed": addr, "status": "LANDED"})
                return True
            except Exception as e:
                rec.update({"status": "STOPPED", "class": "landing: %s" % type(e).__name__})
                self._abort("landing failure")
                return False

    def go(self):
        try:
            with self.lock:
                self.target = min(self.ruling["workers_start"], self.ruling["workers_max"])
                self._event("start", workers=self.target)
                self._spawn_locked()
            i = 0
            while True:
                with self.lock:
                    if i >= len(self.threads):
                        break
                    t = self.threads[i]
                t.join()
                i += 1
        except BaseException:
            self._abort("interrupted")
            raise
        finally:
            if self.checkpoint is not None:
                self.checkpoint(self._snapshot(final=True))
        return self._snapshot(final=True)


def run_concurrent(todo, path, h, s3, on, b20, ruling, landed_set=(), clock=time.monotonic, sleep=time.sleep,
                   checkpoint=None):
    """Request ONLY `todo` (list of request dicts), each account once by ONE queue, on ONE shared bearer."""
    ids = [str(r["bd_account"]) for r in todo]
    if len(set(ids)) != len(ids) or any(i in set(landed_set) for i in ids):
        raise SystemExit("ERROR: the todo list repeats an account or overlaps the landed set")
    return Run(todo, path, h, s3, on, b20, dict(ruling), clock, sleep, checkpoint).go()


def refusal_checks(out_dir, argv, mode):
    """Every refusal that needs no network. Returns the parsed plan (for run) or None (for sweep)."""
    if len(argv) < 4 or argv[2] != mode or "--go" not in argv:
        raise SystemExit("ERROR: live mode needs: %s --go" % mode)
    cp = out_dir / PLAN_NAME
    if not cp.is_file():
        raise SystemExit("ERROR: no concurrent plan %s; run plan first" % PLAN_NAME)
    written = json.loads(cp.read_text(encoding="utf-8"))
    if not isinstance(written.get("ruling"), dict) or written["ruling"] != RULING:
        raise SystemExit("ERROR: the plan's ruling object is absent or differs from batches 249/250; re-run plan")
    return written


def check_sweep_set(failed, cap):
    """The sweep's refusal: the FAILED set is at most failed_cap and every class is transport, 5xx or 429."""
    bad = [f for f in failed if f.get("class") not in SWEEPABLE]
    if len(failed) > cap or bad:
        raise SystemExit("ERROR: the FAILED set (%d, cap %d) is over the cap or holds a class outside %s" % (len(failed), cap, SWEEPABLE))


def print_denominators(c21, plan):
    c21.print_denominators(plan)


def _roll(path):
    if path.exists():  # an earlier record is kept, never overwritten
        path.rename(path.with_name("%s.%s.json" % (path.stem, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))))


def _writer(path):
    def write(snap):
        path.write_text(json.dumps(snap, indent=1) + "\n", encoding="utf-8")
    return write


def _live_env(root):
    os.environ["DRY_RUN"] = "1"
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    c21 = load_c21()
    b20 = c21.load_b20()
    e20 = json.loads((c21.B20_DIR / b20.PLAN_NAME).read_text(encoding="utf-8"))
    s3 = boto3.client("s3", region_name="us-east-1")
    return c21, b20, e20, on, s3


def _lift_dry(root):
    # The estate client refuses egress while DRY_RUN=1; lift it only here, after every refusal passed.
    os.environ["DRY_RUN"] = "0"
    sys.path.insert(0, str(root / "infra/aws/lambda/investor-reporting/performance"))
    import bd_adapter
    h = bd_adapter.load_bd_helpers(force=True)
    if h.DRY_RUN:
        raise SystemExit("ERROR: helper still DRY")
    return h


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    root = Path(argv[1]).resolve()
    mode = argv[2] if len(argv) > 2 else ""
    out_dir = HERE
    if mode == "plan":
        c21, b20, e20, on, s3 = _live_env(root)
        plan = make_plan(c21, e20, c21.list_landed(s3, on, b20))
        (out_dir / PLAN_NAME).write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print_denominators(c21, plan)
        print("vendor_calls %d dry_run %d" % (plan["vendor_calls"], plan["dry_run"]))
        print("ruling " + json.dumps(plan["ruling"], sort_keys=True))
        return 0
    if mode not in ("run", "sweep"):
        raise SystemExit("ERROR: mode must be plan | run --go | sweep --go")
    written = refusal_checks(out_dir, argv, mode)
    c21, b20, e20, on, s3 = _live_env(root)
    fresh = make_plan(c21, e20, c21.list_landed(s3, on, b20))
    by_bd = {str(r["bd_account"]): r for r in e20["request_list"]}
    path = e20["route"]["paths"]["performancePeriod"]
    if mode == "run":
        if c21._canon(fresh) != written:
            raise SystemExit("ERROR: the re-derived plan differs from the written plan; re-run plan, refusing to call")
        todo = [by_bd[b] for b in written["complement_accounts"]]
        target = out_dir / RUN_NAME
    else:
        last = out_dir / RUN_NAME
        if not last.is_file():
            raise SystemExit("ERROR: no run record %s; nothing to sweep" % RUN_NAME)
        failed = json.loads(last.read_text(encoding="utf-8")).get("failed", [])
        check_sweep_set(failed, written["ruling"]["failed_cap"])
        still = set(fresh["complement_accounts"])
        todo = [by_bd[str(f["bd_account"])] for f in failed if str(f["bd_account"]) in still]
        print("sweep: FAILED set %d, still unlanded %d" % (len(failed), len(todo)))
        for f in failed:
            print("FAILED", f["account"], f["bd_account"], f["class"])
        target = out_dir / SWEEP_NAME
    print_denominators(c21, fresh)
    h = _lift_dry(root)
    _roll(target)
    rec = run_concurrent(todo, path, h, s3, on, b20, written["ruling"], landed_set=fresh["landed_accounts"],
                         checkpoint=_writer(target))
    print("denominators: planned %d = landed before %d + landed this %s %d + FAILED %d + not requested %d + other %d" % (
        written["requests_planned"], written["landed"], mode, rec["landed_this_run"], rec["failed_count"], rec["not_requested"],
        len(todo) - rec["landed_this_run"] - rec["failed_count"] - rec["not_requested"]))
    if mode == "sweep":
        print("residue: %d account(s) still FAILED" % rec["failed_count"])
    print(json.dumps({k: rec[k] for k in ("vendor_calls", "bearer_mints", "landed_this_run", "failed_count", "aborted",
                                          "ramped", "workers_target")}, indent=1))
    return 1 if rec["aborted"] else 0


if __name__ == "__main__":
    sys.exit(main())
