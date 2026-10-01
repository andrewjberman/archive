"""HVST-af-2 amendment 1 (runtime root = this worktree's, bbg.dpapi copied + bbg profile junctioned: the main root's worker.lock is held by the issuer's ft backfill, row Z-W91-S14): ONE bbg collector job (BA) in THIS process, under InputSourceMonitor for the whole job.
Counts the job's in-tab requests (TabSession.get) and stops it past 15."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib.opal_data_harvest import __main__ as cli, tab_transport  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

OUT = Path(__file__).resolve().parent
CAP = 15
count = {"n": 0, "log": []}
_orig = tab_transport.TabSession.get


def counted(self, url, *a, **k):
    if count["n"] >= CAP:
        raise SystemExit("REQUEST CAP %d reached" % CAP)
    count["n"] += 1
    r = _orig(self, url, *a, **k)
    count["log"].append({"n": count["n"], "url": url.split("?")[0][-90:], "status": r.status_code})
    return r


tab_transport.TabSession.get = counted
sys.argv = ["opal_data_harvest", "--runtime-root", str(ROOT / ".runtime/opal-data-harvest"),
            "run", "--harvest-grammar", "--retrieval-mode", "backfill", "--floor", "2026-09-24", "--new-only",
            "--no-sign-in", "--security-json", str(OUT / "af2_BA.security.json"), "--publishers", "bbg", "--max-jobs", "1"]
rc = None
with InputSourceMonitor() as monitor:
    try:
        rc = cli.main()
    except SystemExit as exc:
        rc = exc.code
(OUT / "af2_job_monitor.json").write_text(json.dumps({"rc": rc, "monitor": monitor.record(), "requests": count}, indent=1), encoding="utf-8")
print("DRIVER DONE rc=%r requests=%d" % (rc, count["n"]))
