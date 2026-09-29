#!/usr/bin/env python3
"""HVST-w-2 AC1 -- THE CAPPED, --new-only CAPTURE for sa, run by the producer's own CLI entry point IN THIS PROCESS.

Andrew's word (ANDREW_DIRECT_20260928_1805Z ruling 2; resumed by AMENDMENT 1 behind three guards): publisher sa
only; at most 5 invocations of `--max-jobs 5` (25 jobs); `--new-only`; every network-reaching invocation ledgered;
ONE upload-harvest afterwards (AC2). NEVER re-authenticate.

GUARDS: this process installs _guards.install_guards() BEFORE it calls lib.opal_data_harvest.__main__.main(), and
REFUSES to call it unless every entry point resolves to the guard object in this same process. The guards
neutralise SessionManager.refresh / _refresh / get's no-envelope fallback / repair_verification, the browser launch
and the Moonshot POST; each raises GuardStop (a BaseException), which stops the whole runner.

  python ac1_capped_capture.py                          the capture (AC1)
  python ac1_capped_capture.py --planted-reauth-test    AC6: the planted calls run in THIS process instead of the producer
  HVST_W2_STUB=1 python ac1_capped_capture.py           development: a stub producer, scratch runtime, scratch ledger

STOP rules: a guard trip, an auth refresh, a verification repair, a browser, a bot wall (VerificationRequired /
request_rejected), an invocation whose every job is cooldown-suppressed, a known-active sa cooldown before an
invocation, a PAUSE file, or the wall-clock budget of the criterion's own 1800 s timeout.
"""
import contextlib
import datetime
import json
import os
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
assert (REPO / "org").is_dir() and (REPO / ".tools").is_dir(), REPO
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
import _guards  # noqa: E402

STUB = os.environ.get("HVST_W2_STUB") == "1"
PLANTED = "--planted-reauth-test" in sys.argv
SEAT = "0.9.0_WK_AMGT_HARVST~37"
MAX_INVOCATIONS, JOBS_PER_INVOCATION, JOB_CAP = 5, 5, 25
BUDGET_S = 1740          # the criterion's own timeout is 1800 s


def _main_tree():
    common = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--git-common-dir"], capture_output=True,
                            text=True, check=True).stdout.strip()
    return (Path(common) if Path(common).is_absolute() else (REPO / common)).resolve().parent


MAIN = _main_tree()
REAL_RT = (MAIN / ".runtime" / "opal-data-harvest").as_posix()
if STUB:
    SCR = REPO / ".scratch" / "w2_stub"
    SCR.mkdir(parents=True, exist_ok=True)
    RT = (SCR / "rt").as_posix()
    Path(RT).mkdir(parents=True, exist_ok=True)
    LEDGER = SCR / "VENDOR_CALLS_STUB.md"
    STATE = SCR / "ac1_state.json"
    OUT = SCR / "ac1_output.txt"
else:
    RT = REAL_RT
    LEDGER = REPO / "org/missions/D5/AMGT/AMGT_HARVST/ledger/VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_37.md"
    STATE = DELIV / "w2_ac1_state.json"
    OUT = DELIV / ("w2_ac6_planted_output.txt" if PLANTED else "w2_ac1_output.txt")

ARGV = ["run", "--publishers", "sa", "--harvest-grammar", "--new-only", "--all-securities", "--max-jobs",
        str(JOBS_PER_INVOCATION), "--runtime-root", RT]
CMDLINE = 'python -m lib.opal_data_harvest ' + " ".join('"%s"' % a if " " in a or "/" in a else a for a in ARGV)


class _Tee:
    def __init__(self, a, path):
        self.a, self.f = a, open(path, "w", encoding="utf-8")

    def write(self, x):
        self.a.write(x)
        self.f.write(x)

    def flush(self):
        self.a.flush()
        self.f.flush()


class _Buf:
    """Stdout capture that also passes every line straight through (verbatim, live)."""
    def __init__(self, passthrough):
        self.p, self.parts = passthrough, []

    def write(self, x):
        self.parts.append(x)
        self.p.write(x)

    def flush(self):
        self.p.flush()

    def text(self):
        return "".join(self.parts)


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


# ----------------------------------------------------------------------------------------------- planted (AC6)
def run_planted():
    print("AC6 PLANTED RE-AUTH TEST -- inside the capture runner's own process (pid %d)" % os.getpid())
    print("runner: %s  (invoked as: python %s --planted-reauth-test)" % (Path(__file__).name, Path(__file__).name))
    import lib.opal_data_harvest.auth as auth
    import lib.opal_data_harvest.storage as storage
    import lib.opal_data_harvest.verification as verification
    import lib.opal_data_harvest.verification_locator as locator
    import requests

    rows = _guards.resolve_entries()
    if not _guards.print_identity(rows):
        print("REFUSED: a guard is not loaded in this process; NO planted call is made")
        return 3
    print("all %d entry points resolve to the guard object in THIS process" % len(rows))

    counters = {"popen": 0, "socket_connect": 0, "dpapi_call": 0, "boto3_client": 0}

    def counting(name, exc_type=RuntimeError):
        def fn(*a, **k):
            counters[name] += 1
            raise exc_type("planted test: %s reached" % name)
        return fn

    class _Popen:
        def __init__(self, *a, **k):
            counters["popen"] += 1
            raise RuntimeError("planted test: subprocess reached")

    subprocess.Popen = _Popen
    socket.socket.connect = counting("socket_connect")
    storage.dpapi = counting("dpapi_call")
    import boto3
    boto3.client = counting("boto3_client")

    events = []
    tmp = tempfile.mkdtemp(prefix="hvst_w2_planted_")           # an EMPTY runtime root: no vault, no envelope
    mgr = auth.SessionManager(tmp, events.append)
    planted = [
        ("SessionManager.refresh('sa')", auth.SessionManager.refresh, lambda: mgr.refresh("sa")),
        ("SessionManager._refresh('sa')", auth.SessionManager._refresh, lambda: mgr._refresh("sa", Path(tmp) / "x")),
        ("SessionManager.get('sa') with NO saved envelope", auth.SessionManager.get, lambda: mgr.get("sa")),
        ("SessionManager.repair_verification('sa', {}, target_url=None)", auth.SessionManager.repair_verification,
         lambda: mgr.repair_verification("sa", {}, target_url=None)),
        ("verification.repair(...)", verification.repair, lambda: verification.repair("bbg", {}, Path(tmp), print)),
        ("verification.sync_playwright()", verification.sync_playwright, lambda: verification.sync_playwright()),
        ("verification_locator.locate(None, ...)  [the Moonshot POST]", locator.locate,
         lambda: locator.locate(None, "the press and hold button")),
        ("requests Session.request POST https://api.moonshot.ai/v1/chat/completions", requests.sessions.Session.request,
         lambda: requests.sessions.Session().request("POST", "https://api.moonshot.ai/v1/chat/completions")),
    ]
    refused = 0
    for name, target, thunk in planted:
        if not getattr(target, "_hvst_guard", None):
            print("REFUSED TO PLANT %s: its target is not a guard object; stopping the test here" % name)
            return 3
        before = dict(counters)
        try:
            thunk()
            print("[NOT REFUSED] %s  <-- the guard did not stop it" % name)
        except _guards.GuardStop as stop:
            refused += 1
            print("[REFUSED] %s -> %s" % (name, stop))
        except Exception as exc:
            print("[UNEXPECTED %s] %s -> %s" % (type(exc).__name__, name, exc))
        moved = {k: counters[k] - before[k] for k in counters}
        print("    browser_started: %s   credential_read: %s   network_attempted: %s   (instrument deltas %r)" % (
            bool(moved["popen"]), bool(moved["dpapi_call"] or moved["boto3_client"]), bool(moved["socket_connect"]), moved))
    print("recorded producer events during the planted calls (a reauth_started/verification_started would appear here): %r" % events)
    print("guard trips recorded in this process: %d %r" % (len(_guards.TRIPS), [t["entry"] for t in _guards.TRIPS]))
    print("PLANTED: %d of %d refused; instrument totals %r" % (refused, len(planted), counters))
    print("the UNGUARDED variant was never run")
    ok = refused == len(planted) and not any(counters.values()) and not events
    print("AC6 planted-reauth-is-refused: %s" % ("OK" if ok else "FAILED"))
    return 0 if ok else 1


# ----------------------------------------------------------------------------------------------------- capture
def _ro():
    return sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % RT, uri=True)


def sa_cooldown():
    con = _ro()
    try:
        row = con.execute("SELECT until,reason FROM cooldown WHERE publisher='sa'").fetchone()
    finally:
        con.close()
    return row


def events_size():
    p = Path(RT) / "events.jsonl"
    return p.stat().st_size if p.exists() else 0


def events_since(offset):
    p = Path(RT) / "events.jsonl"
    if not p.exists():
        return []
    with p.open("rb") as fh:
        fh.seek(offset)
        data = fh.read().decode("utf-8", "replace")
    out = []
    for line in data.splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def held_articles():
    con = _ro()
    try:
        rows = con.execute("SELECT security_key,article_id,path FROM articles WHERE publisher='sa'").fetchall()
    finally:
        con.close()
    out = []
    for key, aid, path in rows:
        rec = {}
        try:
            rec = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:  # noqa: S110 -- a missing saved file is recorded as absent, never fatal
            pass
        out.append({"security_key": key, "article_id": aid, "path": path, "title": rec.get("title"),
                    "url": rec.get("url"), "published": rec.get("published")})
    return out


def ledger_next_call_number():
    if not LEDGER.exists():
        return 1
    import re
    nums = [int(n) for n in re.findall(r"^## CALL (\d+) --", LEDGER.read_text(encoding="utf-8"), re.M)]
    return (max(nums) + 1) if nums else 1


def append_ledger(entry):
    with LEDGER.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)


def stub_main():
    """Development stand-in for the producer's CLI: canned JSON job_finished lines + receipts, no vendor, no lib."""
    import random
    root = Path(RT)
    (root / "runs").mkdir(parents=True, exist_ok=True)
    scenario = os.environ.get("HVST_W2_STUB_SCENARIO", "ok")
    for i in range(JOBS_PER_INVOCATION):
        jid = "STUB-%d-%d" % (int(time.time()), i)
        rec = {"job_id": jid, "publisher": "sa", "security_key": "stub-%d" % i, "mode": "new_only",
               "previously_stored": i, "accepted": [{"article_id": str(100 + i), "title": "t", "retrieval": "http"}],
               "rejected": [], "auth_refreshes": 0, "verification_repairs": 0, "status": "new_articles"}
        if scenario == "cooldown":
            rec = {"job_id": jid, "publisher": "sa", "security_key": "stub-%d" % i, "mode": "new_only",
                   "accepted": [], "rejected": [], "auth_refreshes": 0, "verification_repairs": 0, "status": "cooldown"}
        if scenario == "botwall" and i == 2:
            rec.update(status="error", error_type="VerificationRequired", accepted=[])
        if scenario == "guard" and i == 1:
            import lib.opal_data_harvest.auth as a
            if not getattr(a.SessionManager.refresh, "_hvst_guard", None):
                raise AssertionError("stub scenario refuses to call an unguarded refresh")
            a.SessionManager(root, print).refresh("sa")
        path = root / "runs" / (jid + ".json")
        path.write_text(json.dumps(rec), encoding="utf-8")
        ev = {"event": "job_finished", "publisher": "sa", "security_key": rec["security_key"], "status": rec["status"],
              "accepted": len(rec["accepted"]), "result": str(path), "at": utcnow().isoformat()}
        print(json.dumps(ev), flush=True)
        if scenario != "cooldown":
            with (root / "events.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"event": "http", "publisher": "sa", "host": "seekingalpha.com",
                                     "path": "/api/v3/symbols/x/news", "status": 200, "bytes": 1000,
                                     "at": utcnow().isoformat()}) + "\n")
        random.random()
    return 0


def run_capture():
    started = time.monotonic()
    t0 = utcnow()
    print("AC1 -- HVST-w-2 capped --new-only capture, sa only. seat %s. start %s" % (SEAT, t0.isoformat()))
    print("stub mode: %s   runtime root passed to the producer: %s" % (STUB, RT))

    rows = _guards.resolve_entries()
    if not _guards.print_identity(rows):
        print("REFUSED: a guard is not loaded in this process; the producer is NOT called")
        return 3
    print("all %d entry points resolve to the guard object in THIS process; the producer's CLI is called in this same process" % len(rows))

    if not STUB and STATE.exists():
        print("REFUSED: w2_ac1_state.json already exists -- a second capture exceeds the word")
        return 2
    if STUB:
        con = sqlite3.connect(RT + "/progress.sqlite3")
        con.executescript("CREATE TABLE IF NOT EXISTS state(key TEXT PRIMARY KEY,value TEXT NOT NULL);"
                          "CREATE TABLE IF NOT EXISTS cooldown(publisher TEXT PRIMARY KEY,until REAL NOT NULL,reason TEXT);"
                          "CREATE TABLE IF NOT EXISTS articles(publisher TEXT,security_key TEXT,article_id TEXT,"
                          "body_sha256 TEXT,path TEXT);")
        con.commit()
        con.close()

    import lib.opal_data_harvest.__main__ as producer
    from lib.opal_data_harvest.storage import content_hash
    cfg = json.loads(Path(REPO / "lib/opal_data_harvest/config.json").read_text(encoding="utf-8"))
    universe = producer.universe(cfg)
    by_key = {s["key"]: s for s in universe}
    plan_key = "cursor:" + content_hash(json.dumps([(s["key"], "sa") for s in universe]))
    con = _ro()
    try:
        row = con.execute("SELECT value FROM state WHERE key=?", (plan_key,)).fetchone()
    finally:
        con.close()
    cursor0 = int(row[0]) if row else 0
    n_sym = sum(1 for s in universe if s.get("sa_symbol"))
    print("universe: %d securities, %d with an sa_symbol (%d without); plan cursor at start: %d" % (
        len(universe), n_sym, len(universe) - n_sym, cursor0))
    planned = [universe[(cursor0 + i) % len(universe)] for i in range(JOB_CAP)]
    print("the next %d planned jobs (cap %d): %s" % (JOB_CAP, JOB_CAP, [(s["key"][:22], s.get("sa_symbol")) for s in planned]))
    cd = sa_cooldown()
    print("sa cooldown row at start: %r  (now %.0f)" % (cd, time.time()))

    state = {"seat": SEAT, "stub": STUB, "started_at": t0.isoformat(), "runtime_root": RT, "command": CMDLINE,
             "cursor_at_start": cursor0, "universe_size": len(universe), "sa_symbol_count": n_sym,
             "held_before": held_articles(), "invocations": [], "stop_reason": None, "guard_trips": [],
             "planned_jobs": [{"key": s["key"], "sa_symbol": s.get("sa_symbol")} for s in planned]}
    print("held sa articles BEFORE (progress.sqlite3 articles table): %d" % len(state["held_before"]))

    popen_calls = {"n": 0}
    real_popen = subprocess.Popen

    class _CountingPopen(real_popen):
        def __init__(self, *a, **k):
            argv = str(a[0] if a else k.get("args", "")).lower()
            if any(t in argv for t in ("chrome", "msedge", "playwright", "harvest_session", "harvest_local", "node")):
                popen_calls["n"] += 1
                raise RuntimeError("HVST-w-2: a browser/harvester launch during the capture is a stop (%r)" % (argv[:120],))
            super().__init__(*a, **k)

    subprocess.Popen = _CountingPopen

    total_jobs, total_requests = 0, 0
    durations = []
    stop = None
    blocking = False
    for n in range(1, MAX_INVOCATIONS + 1):
        elapsed = time.monotonic() - started
        est = 1.3 * max(durations) if durations else 0
        if n > 1 and elapsed + est > BUDGET_S:
            stop = "wall-clock budget: %.0f s elapsed + est %.0f s for another invocation > %d s (the criterion's own timeout)" % (
                elapsed, est, BUDGET_S)
            break
        if (Path(RT) / "PAUSE").exists():
            stop = "PAUSE file present in the runtime root"
            break
        cd = sa_cooldown()
        if cd and cd[0] > time.time():
            stop = "sa cooldown active before invocation %d until %.0f (%s): not invoked into a known suppression" % (n, cd[0], cd[1])
            break
        print("\n" + "=" * 100)
        print("INVOCATION %d of at most %d   (jobs so far %d of %d cap)" % (n, MAX_INVOCATIONS, total_jobs, JOB_CAP))
        print("COMMAND LINE (verbatim; executed by calling lib.opal_data_harvest.__main__.main() in this process):")
        print("  " + CMDLINE)
        off = events_size()
        t_start = utcnow()
        m0 = time.monotonic()
        sys.argv = ["python -m lib.opal_data_harvest"] + ARGV
        buf = _Buf(sys.stdout)
        rc, exc_text, guard_stop = None, None, None
        print("---- producer STDOUT (VERBATIM) ----")
        with contextlib.redirect_stdout(buf):
            try:
                rc = stub_main() if STUB else producer.main()
            except _guards.GuardStop as g:
                guard_stop = str(g)
            except SystemExit as e:
                rc = e.code
            except Exception:
                exc_text = traceback.format_exc()
        dur = time.monotonic() - m0
        durations.append(dur)
        print("---- end producer STDOUT ----")
        if exc_text:
            print("PRODUCER RAISED (verbatim traceback):\n" + exc_text)
        print("invocation %d rc=%r duration=%.0fs guard_stop=%r" % (n, rc, dur, guard_stop))
        t_end = utcnow()

        evs = events_since(off)
        http = [e for e in evs if e.get("event") == "http" and e.get("publisher") == "sa"]
        other = [e for e in evs if e.get("event") != "http"]
        forbidden = [e for e in evs if e.get("event") in (
            "reauth_started", "reauth_succeeded", "verification_started", "verification_action",
            "verification_succeeded", "retry_after_reauth", "retry_after_verification")]
        finished = [json.loads(line) for line in buf.text().splitlines() if line.startswith("{") and '"job_finished"' in line]
        jobs = []
        for f in finished:
            rec = {}
            try:
                rec = json.loads(Path(f["result"]).read_text(encoding="utf-8"))
            except Exception:
                rec = {"status": f.get("status"), "unreadable_receipt": f.get("result")}
            sec = by_key.get(rec.get("security_key") or f.get("security_key"), {})
            status = rec.get("status")
            detail = rec.get("detail") or ""
            if status == "cooldown":
                bucket = "cooldown_suppressed"
            elif status == "contract_unavailable" and "symbol" in detail.lower():
                bucket = "skipped_missing_sa_symbol"
            else:
                bucket = "attempted"
            jobs.append({"invocation": n, "job_id": rec.get("job_id"), "security_key": rec.get("security_key"),
                         "sa_symbol": sec.get("sa_symbol"), "status": status, "bucket": bucket, "mode": rec.get("mode"),
                         "previously_stored": rec.get("previously_stored", "ABSENT"),
                         "accepted": [{"article_id": a.get("article_id"), "title": a.get("title"),
                                       "retrieval": a.get("retrieval")} for a in rec.get("accepted", [])],
                         "rejected": len(rec.get("rejected", [])), "auth_refreshes": rec.get("auth_refreshes"),
                         "verification_repairs": rec.get("verification_repairs"),
                         "error_type": rec.get("error_type"), "started_at": rec.get("started_at"),
                         "finished_at": rec.get("finished_at"), "receipt": f.get("result")})
        print("\nPER-JOB (invocation %d): mode | previously_stored | status | accepted | bucket" % n)
        for j in jobs:
            print("  %-24s sym=%-7s mode=%-9s previously_stored=%-6s status=%-22s accepted=%d rejected=%d  [%s]" % (
                str(j["security_key"])[:24], j["sa_symbol"], j["mode"], j["previously_stored"], j["status"],
                len(j["accepted"]), j["rejected"], j["bucket"]))
        auth_refreshes = sum(int(j["auth_refreshes"] or 0) for j in jobs)
        repairs = sum(int(j["verification_repairs"] or 0) for j in jobs)
        print("invocation %d: %d jobs; vendor requests (events.jsonl delta, sa http) = %d; auth_refreshes: %d; verification_repairs: %d; "
              "forbidden events %d; browser/subprocess launches %d" % (n, len(jobs), len(http), auth_refreshes, repairs,
                                                                       len(forbidden), popen_calls["n"]))
        inv = {"n": n, "started_at": t_start.isoformat(), "finished_at": t_end.isoformat(), "duration_s": round(dur, 1),
               "rc": rc, "guard_stop": guard_stop, "exception": exc_text, "jobs": jobs,
               "http_events": [{"path": e["path"], "status": e["status"], "bytes": e["bytes"], "host": e.get("host"),
                                "at": e["at"]} for e in http],
               "other_events": [e.get("event") for e in other], "forbidden_events": [e.get("event") for e in forbidden],
               "auth_refreshes": auth_refreshes, "verification_repairs": repairs, "stdout": buf.text()}
        state["invocations"].append(inv)
        total_jobs += len(jobs)
        total_requests += len(http)

        if http:
            num = ledger_next_call_number()
            hosts = sorted({e.get("host") for e in http})
            tried = [(j["security_key"], j["sa_symbol"], j["status"], len(j["accepted"])) for j in jobs]
            entry = """
## CALL %d -- seekingalpha.com, %s -> %s

| field | value |
|---|---|
| seat | `%s` (worker of `2.0.0_SA_COO~H`, task order `HVST-w-2` AC1, invocation %d of at most %d) |
| vendor | seeking-alpha (%s) |
| endpoint class | REST: `/api/v3/account/{id}/info`, `/api/v3/symbols/{symbol}/news`, `/api/v3/articles/{id}` |
| mechanism | `%s` -- executed by calling `lib.opal_data_harvest.__main__.main()` INSIDE `ac1_capped_capture.py`'s own process with the re-auth / browser / Moonshot guards installed and verified in that process (AMENDMENT 1); rc %r |
| agent-turn fetch? | **NO.** Scripted producer only, driven by the committed runner from the command line; the worker made no request by hand |
| scope attempted | %d jobs: %s |
| requests made | **%d**, from `events.jsonl` (sa http events, delta over this invocation): %s |
| authorization | Andrew-direct 2026-09-28 ~18:05Z, `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260928_1805Z_OPEN_CALLS_FOUR_RULINGS.md` ruling 2 (`w-2` YES, stated cap, `--new-only`); resumed by the CTO ruling @`74e1eea534` behind three guards. Spend, contracts, entitlements and hold-lifts NOT covered |
| credential used | the SAVED sa session envelope `.runtime/opal-data-harvest/secrets/sa.dpapi` in the MAIN tree (the producer's designed read); no login |
| re-auth fired? | **NO -- measured.** receipts auth_refreshes=%d, verification_repairs=%d; forbidden events %d; guard trips %d; browser/subprocess launches %d |
| result | rc %r; job statuses %s |
| bytes retained | %d article bodies accepted into the LOCAL outbox (harvest_raw / harvest_listing); nothing else |
| S3 written | not by this call (`run` writes the local outbox; AC2's `upload-harvest` is the S3 leg) |
| spend | none |
| evidence | `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~37/w2_ac1_output.txt`, `w2_ac1_state.json` |
""" % (num, t_start.strftime("%Y-%m-%dT%H:%M:%SZ"), t_end.strftime("%H:%M:%SZ"), SEAT, n, MAX_INVOCATIONS,
       ", ".join(hosts), CMDLINE, rc, len(jobs), tried, len(http),
       [(e["path"].rsplit("/", 1)[-1][:24], e["status"], e["bytes"]) for e in http],
       auth_refreshes, repairs, len(forbidden), len(_guards.TRIPS), popen_calls["n"], rc,
       sorted({str(j["status"]) for j in jobs}), sum(len(j["accepted"]) for j in jobs))
            append_ledger(entry)
            print("=== LEDGER CALL %d AS WRITTEN (%s) ===" % (num, LEDGER.name))
            print(entry)
        else:
            print("invocation %d reached NO network (0 http events): no ledger CALL entry is owed" % n)

        # ---- stop rules ----
        if guard_stop or _guards.TRIPS:
            stop, blocking = "GUARD TRIP: %s" % (guard_stop or _guards.TRIPS), True
        elif auth_refreshes or repairs or forbidden or popen_calls["n"]:
            stop, blocking = "auth refresh / verification repair / browser signal observed (auth %d, repairs %d, events %r, launches %d)" % (
                auth_refreshes, repairs, [e.get("event") for e in forbidden], popen_calls["n"]), True
        elif exc_text:
            stop = "producer raised an exception (traceback above)"
        else:
            walls = [j for j in jobs if j["error_type"] == "VerificationRequired" or j["status"] == "request_rejected"]
            if walls:
                w = walls[0]
                stop = "BOT WALL at job %s (%s, status=%s, error_type=%s): stopped, never repaired" % (
                    w["job_id"], w["security_key"], w["status"], w["error_type"])
            elif not jobs:
                stop = "the producer reported no jobs (paused or none remaining)"
            elif all(j["bucket"] == "cooldown_suppressed" for j in jobs):
                stop = "every job of invocation %d was cooldown-suppressed" % n
            elif total_jobs >= JOB_CAP:
                stop = "job cap reached: %d of %d" % (total_jobs, JOB_CAP)
        state["stop_reason"] = stop
        state["guard_trips"] = list(_guards.TRIPS)
        state["blocking"] = blocking
        STATE.write_text(json.dumps(state, indent=1, default=str) + "\n", encoding="utf-8")
        if stop:
            break
    if stop is None:
        stop = "all %d invocations completed (%d jobs of the %d cap)" % (MAX_INVOCATIONS, total_jobs, JOB_CAP)
    state["stop_reason"] = stop
    state["blocking"] = blocking
    state["finished_at"] = utcnow().isoformat()
    state["guard_trips"] = list(_guards.TRIPS)
    state["popen_launches"] = popen_calls["n"]
    state["requests_hosts_via_requests_lib"] = dict(_guards.REQUEST_HOSTS)
    STATE.write_text(json.dumps(state, indent=1, default=str) + "\n", encoding="utf-8")
    subprocess.Popen = real_popen

    alljobs = [j for i in state["invocations"] for j in i["jobs"]]
    print("\n" + "=" * 100)
    print("STOP REASON: %s" % stop)
    print("invocations run: %d of at most %d" % (len(state["invocations"]), MAX_INVOCATIONS))
    print("total jobs: %d (cap %d)" % (len(alljobs), JOB_CAP))
    d = len(alljobs) or 1
    att = [j for j in alljobs if j["bucket"] == "attempted"]
    print("jobs attempted (reached the vendor path):            %d of %d" % (len(att), len(alljobs)))
    print("jobs skipped for a missing sa_symbol:                %d of %d" % (
        sum(j["bucket"] == "skipped_missing_sa_symbol" for j in alljobs), len(alljobs)))
    print("jobs cooldown-suppressed (NO previously_stored field): %d of %d  [previously_stored ABSENT on %d]" % (
        sum(j["bucket"] == "cooldown_suppressed" for j in alljobs), len(alljobs),
        sum(j["previously_stored"] == "ABSENT" for j in alljobs)))
    print("jobs that returned rows (accepted > 0):              %d of %d attempted (%d of %d all jobs); articles accepted: %d" % (
        sum(1 for j in att if j["accepted"]), len(att), sum(1 for j in alljobs if j["accepted"]), d,
        sum(len(j["accepted"]) for j in alljobs)))
    print("jobs with previously_stored > 0 (--new-only had held articles to skip): %d of %d attempted" % (
        sum(1 for j in att if isinstance(j["previously_stored"], int) and j["previously_stored"] > 0), len(att)))
    print("total vendor requests (events.jsonl deltas): %d" % total_requests)
    tot_auth = sum(int(i["auth_refreshes"]) for i in state["invocations"])
    print("auth_refreshes: %d" % tot_auth)
    print("verification_repairs: %d" % sum(int(i["verification_repairs"]) for i in state["invocations"]))
    print("browser_started: %s" % bool(popen_calls["n"] or any(t["entry"] == "verification.sync_playwright" for t in _guards.TRIPS)))
    print("guard trips: %d %r" % (len(_guards.TRIPS), [t["entry"] for t in _guards.TRIPS]))
    print("Moonshot/vision calls (requests-library hosts seen): %r" % dict(_guards.REQUEST_HOSTS))
    print("state written: %s" % STATE.name)
    return 1 if blocking else 0


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sys.stdout = _Tee(sys.stdout, OUT)
    _guards.install_guards()
    try:
        code = run_planted() if PLANTED else run_capture()
    except _guards.GuardStop as g:
        print("GUARD STOP escaped to the top level: %s" % g)
        code = 1
    sys.exit(code)
