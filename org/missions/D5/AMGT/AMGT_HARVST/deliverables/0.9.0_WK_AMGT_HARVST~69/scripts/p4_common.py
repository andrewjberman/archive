"""HVST-p-4 shared readers. LOCAL READS ONLY: no network, no browser, no S3, no write to the runtime root.

Session files are touched with os.stat only (presence, size, mtime) -- never opened.
"""
import datetime as dt
import json
import os
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
WT = HERE
while WT != WT.parent and not (WT / "lib" / "opal_data_harvest").is_dir():
    WT = WT.parent
LIB = WT / "lib" / "opal_data_harvest"
SCRIPTS = WT / "org" / "tier1_exec" / "4.0.0_SA_CRO" / "scripts"
RUNTIME = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest")

# The three run records of HVST-o-5 (the barrons attempt-1 run, the four-publisher run, the second-pass run).
O5_RUNS = ["20260930T040818Z-run-25c129af", "20260930T044003Z-run-b75f9299", "20260930T045332Z-run-75d4c464"]
PUBS = ["barrons", "ft", "bbg", "wsj"]


def ts(value):
    return dt.datetime.fromisoformat(value)


def run_records():
    return {r: json.loads((RUNTIME / "run_records" / (r + ".json")).read_text(encoding="utf-8")) for r in O5_RUNS}


def job_files():
    """[(run_id, job dict from runs/<job_id>.json)] for every job of the o-5 run records."""
    out = []
    for run_id, rec in run_records().items():
        for job in rec["jobs"]:
            path = RUNTIME / "runs" / (job["job_id"] + ".json")
            out.append((run_id, json.loads(path.read_text(encoding="utf-8"))))
    return out


def events():
    lines = (RUNTIME / "events.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(x) for x in lines if x.strip()]


def job_events(job, all_events, slack=5.0):
    """Events of the job's publisher inside [started_at, finished_at + slack s]. The ledger carries no job id,
    so the window plus the publisher IS the join key (each publisher runs one job at a time under the WorkerLock)."""
    lo, hi = ts(job["started_at"]), ts(job["finished_at"]) + dt.timedelta(seconds=slack)
    return [e for e in all_events if e.get("publisher") == job["publisher"] and lo <= ts(e["at"]) <= hi]


def find_line(path, pattern, after=0):
    """1-based line number of the first line at/after `after` matching the literal `pattern`; asserts it exists."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for i, text in enumerate(lines, start=1):
        if i > after and pattern in text:
            return i
    raise AssertionError("pattern not found: %r in %s" % (pattern, path))


def cite(path, pattern, after=0):
    p = Path(path)
    try:
        rel = p.relative_to(WT).as_posix()
    except ValueError:
        rel = p.as_posix()
    n = find_line(p, pattern, after)
    return "%s:%d" % (rel, n), n


def line_text(path, n):
    return Path(path).read_text(encoding="utf-8").splitlines()[n - 1].strip()


def session_stat(publisher, at=None):
    """Presence / size / mtime of secrets/<pub>.dpapi via os.stat only. Never opened."""
    path = RUNTIME / "secrets" / (publisher + ".dpapi")
    if not path.exists():
        return {"present": False, "path": path.as_posix()}
    st = os.stat(path)
    mtime = dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc)
    out = {"present": True, "path": path.as_posix(), "bytes": st.st_size, "mtime_utc": mtime.isoformat()}
    if at is not None:
        out["age_at_run_days"] = round((ts(at) - mtime).total_seconds() / 86400, 2)
    out["age_now_days"] = round((dt.datetime.now(dt.timezone.utc) - mtime).total_seconds() / 86400, 2)
    return out


def auth_folders(publisher):
    """Names + mtimes of the auth/ artifacts folders for a publisher (folder names only)."""
    base = RUNTIME / "auth"
    out = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and ("-" + publisher + "-") in d.name:
            out.append((d.name, dt.datetime.fromtimestamp(d.stat().st_mtime, dt.timezone.utc).isoformat()))
    return out


def verification_folders(publisher):
    base = RUNTIME / "verification"
    out = []
    if base.is_dir():
        for d in sorted(base.iterdir()):
            if d.is_dir() and ("-" + publisher + "-") in d.name:
                out.append(d.name)
    return out


def cooldown_rows():
    p = (RUNTIME / "progress.sqlite3").as_posix()
    con = sqlite3.connect("file:" + p + "?mode=ro&immutable=1", uri=True)
    try:
        return con.execute("select publisher, until, reason from cooldown").fetchall()
    finally:
        con.close()


def block_sockets():
    """Assert-and-hold: make socket creation raise, then prove it raises. Returns the restore callable."""
    import socket
    original = socket.socket

    def refused(*a, **k):
        raise RuntimeError("HVST-p-4: socket creation blocked (read-only cell)")

    socket.socket = refused
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except RuntimeError:
        pass
    else:
        socket.socket = original
        raise AssertionError("socket creation was not blocked")

    def restore():
        socket.socket = original

    return restore
