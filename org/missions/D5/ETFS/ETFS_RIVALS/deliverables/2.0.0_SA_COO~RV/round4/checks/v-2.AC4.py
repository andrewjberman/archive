"""RIV-v-2 AC4 (reopen, row ETFS_RIVALS-Z-S10) -- the vehicle's enrichment step is a real CLI with the collector's exit contract.

`scheduled_daily_pull.cmd` runs `python -m rivalfunds.enrichment_bloomberg --mode daily` and branches on 0 landed / 1 unreachable /
2 partial / 3 nothing written. Today the module has no __main__: it imports, exits 0, and the vehicle logs "landed" with nothing
pulled. No Bloomberg call is made here: handler_entry is replaced by a stub in a child process.
  - `python -m rivalfunds.enrichment_bloomberg --help` prints a usage naming --mode;
  - main() maps the stub's results: OK -> 0, unreachable -> 1, PARTIAL -> 2, SKIPPED -> 3;
  - the stub receives mode 'daily' from `--mode daily` (the CLI passes the vehicle's argument through)."""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

STUB = r"""
import json, sys
import rivalfunds.enrichment_bloomberg as e
seen = {}
def stub(ev, context=None):
    seen.update(ev)
    return json.loads(sys.argv[1])
e.handler_entry = stub
rc = e.main(["--mode", "daily", "--sink", "local:" + sys.argv[2]])
print("MODE=" + str(seen.get("mode")))
sys.exit(rc)
"""


def run(v):
    c.setup_path()
    scripts = str(pathlib.Path(__file__).resolve().parents[9] / "data" / "etfs" / "scripts")  # the worktree running the check
    env_cwd = scripts
    h = subprocess.run([sys.executable, "-m", "rivalfunds.enrichment_bloomberg", "--help"], cwd=env_cwd,
                       capture_output=True, text=True, timeout=60)
    print(f"--help rc={h.returncode} stdout_bytes={len(h.stdout)}")
    v.check(h.returncode == 0 and "--mode" in h.stdout, "`-m rivalfunds.enrichment_bloomberg --help` prints a usage naming --mode")
    tmp = c.tmpdir("rv_v2d_")
    cases = [('{"status": "OK"}', 0), ('{"status": "FAILED", "detail": {"unreachable": true}}', 1),
             ('{"status": "PARTIAL"}', 2), ('{"status": "SKIPPED"}', 3)]
    for res, want in cases:
        p = subprocess.run([sys.executable, "-c", STUB, res, str(tmp)], cwd=env_cwd, capture_output=True, text=True, timeout=60)
        mode = next((ln[5:] for ln in p.stdout.splitlines() if ln.startswith("MODE=")), None)
        print(f"stub {res} -> rc={p.returncode} mode={mode}" + (f" stderr={p.stderr.strip()[-160:]}" if p.returncode not in (0, 1, 2, 3) else ""))
        v.check(p.returncode == want and mode == "daily", f"result {res} exits {want} with mode daily")


failures = c.guarded("AC4", run)
print("AC4 RESULT: PASS 0 failures" if failures == 0 else f"AC4 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
