"""HVST-q-6 AC2: replay HVST-p-4's recorded event shapes through the NEW code on stubs.

The recorded shapes are read (READ ONLY, never written) from the collector's runtime ledger:
  barrons 2026-09-23 (job 20260923T003256Z-barrons-b22a5594cd) and 2026-09-30 (20260930T040818Z-barrons-cfedbf8fb4):
    logged-out /client -> reauth -> /client -> /search 401 (challenge) -> /client -> request_rejected
  ft 2026-09-23 (20260923T002759Z-ft-f09c4304f9) and 2026-09-30 (20260930T044529Z-ft-a1a3265ed2):
    /search 403 (~270 KB) -> request_rejected, body thrown away
Each recorded (path, status, bytes) request is answered by a stub of that status and size (bodies are
SYNTHESISED to the recorded size; the recorded bodies do not exist). Where the new code goes past what
was recorded, the stub answers as a repaired session would. Session files are never touched; sockets are
blocked and asserted; nothing is sent to any publisher.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~75/scripts/q6_ac2_replay_recorded_shapes.py
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WT = HERE
while WT != WT.parent and not (WT / "lib" / "opal_data_harvest").is_dir():
    WT = WT.parent
sys.path.insert(0, str(WT))

from lib.opal_data_harvest import test_q6_barrons_guard_ft_body as q6  # noqa: E402


def runtime_root():
    override = os.environ.get("HARVEST_RUNTIME_ROOT")
    if override:
        return Path(override)
    common = subprocess.run(["git", "-C", str(WT), "rev-parse", "--git-common-dir"], capture_output=True,
                            text=True, check=True).stdout.strip()
    return (WT / common).resolve().parent / ".runtime" / "opal-data-harvest"


RUNTIME = runtime_root()
JOBS = [
    ("barrons", "2026-09-23", "20260923T003256Z-barrons-b22a5594cd"),
    ("barrons", "2026-09-30", "20260930T040818Z-barrons-cfedbf8fb4"),
    ("ft", "2026-09-23", "20260923T002759Z-ft-f09c4304f9"),
    ("ft", "2026-09-30", "20260930T044529Z-ft-a1a3265ed2"),
]
FAILURES = []


def check(label, condition):
    print("    [%s] %s" % ("ok" if condition else "FAIL", label))
    if not condition:
        FAILURES.append(label)


def ts(value):
    return dt.datetime.fromisoformat(value)


def recorded_job(job_id):
    """(the job's runs/<id>.json, its events in [started_at, finished_at + 5 s] for its publisher)."""
    job = json.loads((RUNTIME / "runs" / (job_id + ".json")).read_text(encoding="utf-8"))
    lo, hi = ts(job["started_at"]), ts(job["finished_at"]) + dt.timedelta(seconds=5)
    lines = (RUNTIME / "events.jsonl").read_text(encoding="utf-8").splitlines()
    events = [json.loads(x) for x in lines if x.strip()]
    window = [e for e in events if e.get("publisher") == job["publisher"] and lo <= ts(e["at"]) <= hi]
    return job, window


def describe(window):
    parts = []
    for e in window:
        if e["event"] == "http":
            parts.append("%s %s(%s B)" % (e["path"], e["status"], e["bytes"]))
        else:
            parts.append(e["event"] + (":" + e["status"] if e.get("status") else ""))
    return " | ".join(parts)


def main():
    with q6.blocked_network() as net:
        print("SOCKETS: creation blocked and asserted for the duration of this script")
        print("RUNTIME ROOT (read only): %s" % RUNTIME)
        print("NOW_UTC: %s" % dt.datetime.now(dt.timezone.utc).isoformat())
        mods = q6.real_mods()
        for publisher, day, job_id in JOBS:
            print("\n" + "=" * 100)
            print("%s %s  recorded job %s" % (publisher.upper(), day, job_id))
            job, window = recorded_job(job_id)
            recorded = [{"path": e["path"], "status": e["status"], "bytes": e["bytes"]}
                        for e in window if e["event"] == "http"]
            print("  RECORDED : status=%s auth_refreshes=%s verification_repairs=%s" %
                  (job["status"], job["auth_refreshes"], job["verification_repairs"]))
            print("             " + describe(window))
            with tempfile.TemporaryDirectory() as tmp:
                out = q6.run_case(mods, Path(tmp) / "root", publisher, recorded=list(recorded))
                result = out.result
                print("  NEW CODE : status=%s auth_refreshes=%s verification_repairs=%s attempts=%s" %
                      (result["status"], result["auth_refreshes"], result["verification_repairs"], len(out.attempts)))
                print("             session manager calls: %s" % " -> ".join(out.sessions))
                for i, call in enumerate(out.http, start=1):
                    print("             %d. gen%d %-8s %s (%s B)  [%s]" % (i, call["generation"], call["path"], call["status"],
                                                                      call["bytes"], call["origin"]))
                check("the recorded request shapes were consumed in order (no divergence)",
                      all(c["origin"] != "" and not c["origin"].startswith("DIVERGES") for c in out.http)
                      and sum(1 for c in out.http if c["origin"] == "recorded") == len(recorded))
                if publisher == "barrons":
                    check("PATH: reauth once, then the challenge met the repair once, then the replay reached /search",
                          out.sessions == ["get", "reauth", "repair"] and out.attempts == [0, 1, 2])
                    check("recorded terminal was request_rejected with verification_repairs=0; new code repairs once "
                          "(verification_repairs=1, auth_refreshes=1) and no loop (3 attempts)",
                          job["status"] == "request_rejected" and job["verification_repairs"] == 0
                          and result["verification_repairs"] == 1 and result["auth_refreshes"] == 1)
                    check("the replay after the repair got the stub's /search 200 (the challenge is not repeated)",
                          [(c["generation"], c["status"]) for c in q6.search_calls(out)] == [(1, 401), (2, 200)])
                else:
                    info, body = q6.kept_body(out)
                    print("             rejected_response: status=%s bytes_received=%s bytes_kept=%s truncated=%s path=%s" %
                          (info["status"], info["bytes_received"], info["bytes_kept"], info["truncated"], info["path"]))
                    check("PATH: bare 403 -> request_rejected, no reauth, no repair (unchanged)",
                          out.sessions == ["get"] and result["auth_refreshes"] == 0 and result["verification_repairs"] == 0
                          and result["status"] == "request_rejected")
                    check("the 403 body is now KEPT in the local run artifacts, capped (%d B of %d B received)" %
                          (info["bytes_kept"], info["bytes_received"]),
                          info["bytes_received"] == recorded[0]["bytes"] and info["bytes_kept"] == q6._transport.REJECTED_BODY_CAP)
                    persisted = json.dumps(result) + (Path(tmp) / "root" / "events.jsonl").read_text(encoding="utf-8")
                    check("no request credential in the kept body, the job result or the event ledger",
                          all(s.encode() not in body and s not in persisted for s in q6.FT_SECRETS))
        print("\n" + "=" * 100)
        print("ASSERTIONS FAILED: %d" % len(FAILURES))
        for label in FAILURES:
            print("  FAIL: " + label)
        print("NETWORK CALLS MADE: %d (socket entry points replaced by a refusing stub and asserted)" % len(net))
        return 1 if FAILURES or net else 0


if __name__ == "__main__":
    sys.exit(main())
