#!/usr/bin/env python3
"""NFRA_CLDGRPH.TO-CG-V-1 / cell CG-s-10 -- measurement harness.

Measures ONE invocation of a globgrph projection engine (the FULL load
kuzu_nessie_load.py, or the INCREMENTAL path kuzu_incremental_refresh.py) and
emits a JSON record with wall clock, peak resident memory, process I/O, the
marker vintage at both ends of the run, and the engine's own stdout/stderr.

WHY TWO MEMORY INSTRUMENTS (they are not the same measurement):
  peak_wset_bytes      -- the OS's OWN peak, from GetProcessMemoryInfo via
                          psutil's Windows pfullmem. Monotonic and maintained by
                          the kernel, so it does NOT depend on this harness's
                          sampling cadence. AUTHORITATIVE.
  sampled_peak_rss     -- max of polled rss at SAMPLE_INTERVAL_S. A short spike
                          BETWEEN samples is invisible to it. Reported as a
                          CORROBORATING second instrument with a different
                          failure mode, never as the headline.
A disagreement between them is informative: sampled <= peak_wset always; a large
gap means the peak was brief.

RESIDUAL, stated rather than hidden: peak_wset is read by POLLING a live process,
so a spike in the final SAMPLE_INTERVAL_S before exit is not captured. Bounded by
SAMPLE_INTERVAL_S against a multi-second run.

NO REPO SOURCE IS EDITED BY THIS HARNESS. It invokes the engines unchanged, as
subprocesses, exactly as _canonical.py does.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

import psutil

def _repo_root() -> str:
    """DERIVE the workspace root (CLAUDE.md: never hardcode it, never count '..').

    git rev-parse is the authority; the walk-up is only a fallback for a
    detached copy, and it keys on a marker that exists at the root.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=here,
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and out.stdout.strip():
            return os.path.abspath(out.stdout.strip())
    except Exception:  # noqa: BLE001 -- fall through to the marker walk-up
        pass
    d = here
    while True:
        if os.path.isdir(os.path.join(d, "infra", "aws", "globgrph")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise RuntimeError("could not derive the workspace root from " + here)
        d = parent


GLOBGRPH_DIR = os.path.abspath(os.environ.get(
    "CGS10_GLOBGRPH_DIR",
    os.path.join(_repo_root(), "infra", "aws", "globgrph"),
))
WAREHOUSE_BUCKET = "opal-313476888478-globgrph"
SAMPLE_INTERVAL_S = 0.05


def read_marker() -> dict:
    """The branch-head marker at this instant -- the run's input vintage."""
    if GLOBGRPH_DIR not in sys.path:
        sys.path.insert(0, GLOBGRPH_DIR)
    try:
        import _provenance  # noqa: PLC0415 -- must resolve against GLOBGRPH_DIR
        m = _provenance.read_branch_head_marker(WAREHOUSE_BUCKET) or {}
        tm = m.get("table_metadata") or {}
        return {
            "committed_at_iso": m.get("committed_at_iso"),
            "nessie_commit_hash": m.get("nessie_commit_hash"),
            "writer_id": m.get("writer_id"),
            "graph_nodes_snapshot_id": (tm.get("graph_nodes") or {}).get("snapshot_id"),
            "graph_edges_snapshot_id": (tm.get("graph_edges") or {}).get("snapshot_id"),
            "graph_nodes_metadata_location": (tm.get("graph_nodes") or {}).get("metadata_location"),
            "graph_edges_metadata_location": (tm.get("graph_edges") or {}).get("metadata_location"),
            "read_status": "measured",
        }
    except Exception as ex:  # noqa: BLE001 -- an unreadable marker is a RESULT, not a crash
        return {"read_status": "unreadable", "error": f"{type(ex).__name__}: {ex}"}


def environment() -> dict:
    import platform
    vm = psutil.virtual_memory()
    mods = {}
    for name in ("kuzu", "pyiceberg", "pyarrow", "boto3", "psutil"):
        try:
            mods[name] = __import__(name).__version__
        except Exception as ex:  # noqa: BLE001
            mods[name] = f"ERR {type(ex).__name__}"
    return {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_logical": psutil.cpu_count(logical=True),
        "cpu_physical": psutil.cpu_count(logical=False),
        "ram_total_bytes": vm.total,
        "ram_available_bytes_at_start": vm.available,
        "module_versions": mods,
        "network_path_to_s3": "public internet -> s3.us-east-1.amazonaws.com "
                              "(dev laptop, NOT in-VPC; Nessie REST is unreachable from here, "
                              "so the engine anchors on the S3 branch-head marker)",
    }


def dir_size_bytes(path: str) -> int:
    """Total bytes of a Kuzu DB (a file, plus any sidecars sharing its name)."""
    total = 0
    if os.path.isfile(path):
        total += os.path.getsize(path)
    elif os.path.isdir(path):
        for root, _dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
    parent, base = os.path.dirname(path) or ".", os.path.basename(path)
    try:
        for entry in os.listdir(parent):
            if entry.startswith(base) and entry != base:
                p = os.path.join(parent, entry)
                if os.path.isfile(p):
                    total += os.path.getsize(p)
    except OSError:
        pass
    return total


def measure(cmd: list[str], cwd: str, out_db: str, label: str, operation: str) -> dict:
    marker_start = read_marker()
    env = os.environ.copy()

    t0_wall = time.time()
    t0 = time.monotonic()
    proc = subprocess.Popen(
        cmd, cwd=cwd, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )

    peak_wset = 0
    sampled_peak_rss = 0
    samples = 0
    io_read = io_write = 0
    try:
        p = psutil.Process(proc.pid)
    except psutil.NoSuchProcess:
        p = None

    # Drain pipes on threads so a full OS pipe buffer can never deadlock the child
    # (a blocked child would otherwise inflate the very wall clock being measured).
    import threading
    bufs: dict[str, list[str]] = {"out": [], "err": []}

    def _drain(stream, key):
        for line in stream:
            bufs[key].append(line)

    th_o = threading.Thread(target=_drain, args=(proc.stdout, "out"), daemon=True)
    th_e = threading.Thread(target=_drain, args=(proc.stderr, "err"), daemon=True)
    th_o.start()
    th_e.start()

    while proc.poll() is None:
        if p is not None:
            try:
                procs = [p] + p.children(recursive=True)
                rss_now = 0
                for q in procs:
                    try:
                        mi = q.memory_info()
                        rss_now += getattr(mi, "rss", 0)
                        pw = getattr(mi, "peak_wset", 0)
                        if pw > peak_wset:
                            peak_wset = pw
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                if rss_now > sampled_peak_rss:
                    sampled_peak_rss = rss_now
                try:
                    ioc = p.io_counters()
                    io_read, io_write = ioc.read_bytes, ioc.write_bytes
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    pass
                samples += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(SAMPLE_INTERVAL_S)

    rc = proc.wait()
    elapsed = time.monotonic() - t0
    t1_wall = time.time()
    th_o.join(timeout=10)
    th_e.join(timeout=10)
    marker_end = read_marker()

    return {
        "label": label,
        "operation": operation,
        "cmd": cmd,
        "cwd": cwd,
        "returncode": rc,
        "wall_clock_s": round(elapsed, 3),
        "wall_clock_instrument": "time.monotonic() around subprocess.Popen/wait "
                                 "(monotonic: immune to wall-clock adjustment)",
        "started_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0_wall)),
        "ended_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t1_wall)),
        "peak_memory_bytes": peak_wset,
        "peak_memory_instrument": "OS peak working set (GetProcessMemoryInfo via "
                                  "psutil memory_info().peak_wset), polled; kernel-maintained "
                                  "and monotonic, so NOT dependent on sample cadence",
        "sampled_peak_rss_bytes": sampled_peak_rss,
        "sampled_peak_rss_instrument": f"max of polled rss over process tree at "
                                       f"{SAMPLE_INTERVAL_S}s -- CORROBORATING second instrument; "
                                       f"blind to a spike between samples",
        "sample_count": samples,
        "sample_interval_s": SAMPLE_INTERVAL_S,
        "io_read_bytes": io_read,
        "io_write_bytes": io_write,
        "io_instrument": "psutil Process.io_counters() (all I/O incl. network sockets on Windows)",
        "output_db_path": out_db,
        "output_db_bytes": dir_size_bytes(out_db),
        "marker_at_start": marker_start,
        "marker_at_end": marker_end,
        "marker_moved_during_run": (marker_start.get("nessie_commit_hash")
                                    != marker_end.get("nessie_commit_hash")),
        "stdout": "".join(bufs["out"]),
        "stderr": "".join(bufs["err"]),
        "claim": "measured",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="CG-s-10 measurement harness")
    ap.add_argument("--operation", required=True, choices=["full", "incremental"])
    ap.add_argument("--db", required=True, help="TEMP output DB path (never the canonical)")
    ap.add_argument("--current", default=None, help="incremental only: the DB to diff from")
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, help="where to write the JSON record")
    a = ap.parse_args()

    canonical = os.path.join(GLOBGRPH_DIR, "kuzu_nessie_db")
    if os.path.abspath(a.db) == os.path.abspath(canonical):
        print("ERROR: refusing to target the CANONICAL db path", file=sys.stderr)
        return 2

    if a.operation == "full":
        cmd = [sys.executable, "kuzu_nessie_load.py", "--db", os.path.abspath(a.db)]
    else:
        if not a.current:
            print("ERROR: --current is required for the incremental operation", file=sys.stderr)
            return 2
        cmd = [sys.executable, "kuzu_incremental_refresh.py",
               "--current", os.path.abspath(a.current), "--db", os.path.abspath(a.db)]

    rec = measure(cmd, GLOBGRPH_DIR, os.path.abspath(a.db), a.label, a.operation)
    rec["environment"] = environment()
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
    print(f"OK: wrote {a.out} rc={rec['returncode']} wall={rec['wall_clock_s']}s "
          f"peak={rec['peak_memory_bytes']}B")
    return 0


if __name__ == "__main__":
    sys.exit(main())
