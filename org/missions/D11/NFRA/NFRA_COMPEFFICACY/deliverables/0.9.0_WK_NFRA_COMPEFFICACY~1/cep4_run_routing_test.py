"""P4-AC1 arm (g) runner -- runs the router's OWN harness against the WORKING tree, once.

Out of band because the harness runs longer than P4-AC1's own `timeout 600` bound. Writes:
  cep4_routing_test.log       the harness's combined stdout+stderr, verbatim
  cep4_routing_test.rc.json   rc + the blob it measured + the window + the invocation
  cep4_routing_test_report.json  the harness's own report (its --out target)

The battery re-reads the .rc.json under a grain control (the recorded blob must equal
`git hash-object .tools/comp-which` at battery time), so a stale record cannot pass.

WHY THE TWO FLAGS -- see row NFRA_COMPEFFICACY-W1-S3:
  --binary-ref WORKING  the default is 'HEAD', which extracts the COMMITTED blob and cannot
                        see an uncommitted change (routing-test :1134, :1177, :1181).
  --out <here>          the default writes the AE lane's committed baseline artifact
                        (:1653), outside this worker's grant, which the flag's own help
                        says a regression run must not clobber.
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cep4_lib as L  # noqa: E402

RT = os.path.join(L.WS, ".tools", "comp-which-routing-test.py")
LOG = os.path.join(L.HERE, "cep4_routing_test.log")
RCJ = os.path.join(L.HERE, "cep4_routing_test.rc.json")
REPORT = os.path.join(L.HERE, "cep4_routing_test_report.json")
BOUND_S = 2400


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    argv = [sys.executable, RT, "--binary-ref", "WORKING", "--out", REPORT]
    blob = subprocess.run(["git", "-C", L.WS, "hash-object", L.COMP_WHICH],
                          capture_output=True, text=True, timeout=60).stdout.strip()
    started = _utc()
    print("START %s   blob %s" % (started, blob))
    print("  %s" % " ".join(argv[1:]))
    try:
        r = subprocess.run(argv, cwd=L.WS, capture_output=True, text=True, timeout=BOUND_S)
        rc, out = r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as exc:
        rc = 124
        out = _decode(exc.stdout) + _decode(exc.stderr) + \
            "\n[TIMEOUT after %d s -- rc 124 IS the recorded output]\n" % BOUND_S
    ended = _utc()

    with open(LOG, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    rec = {
        "invocation": " ".join(["python"] + argv[1:]),
        "rc": rc,
        "blob": blob,
        "started": started,
        "ended": ended,
        "bound_s": BOUND_S,
        "report": os.path.relpath(REPORT, L.WS).replace("\\", "/"),
        "log": os.path.relpath(LOG, L.WS).replace("\\", "/"),
        "run_by": "0.9.0_WK_NFRA_COMPEFFICACY~1",
        "bare_form_control": (
            "`python .tools/comp-which-routing-test.py` with NO flags: rc 124 at a 580 s bound "
            "on the UNPATCHED HEAD bytes (2026-09-09 23:42:21Z -> 23:52:01Z, 153 lines) and "
            "rc 124 at a 580 s bound on the patched bytes (290 lines). It also measures the "
            "COMMITTED blob, not the change, and writes outside this worker's grant."),
    }
    with open(RCJ, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, ensure_ascii=True, indent=2, sort_keys=True)
        fh.write("\n")
    print("END   %s   rc=%d   log=%s" % (ended, rc, LOG))
    return 0


def _decode(v):
    if v is None:
        return ""
    return v.decode("utf-8", "replace") if isinstance(v, bytes) else v


if __name__ == "__main__":
    raise SystemExit(main())
