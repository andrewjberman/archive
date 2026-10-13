"""AMGT_RESAPP round-102 PREP -- the overlay's per-phase log lines (`AMGT-bi-1`): the lines are there, in order, add up, and move NO served byte.

  PYTHONPATH=<repo root> python r102_overlay_phase_check.py [--candidate-file <path to a scoped_amgt.py>] [--subjects ASML_NA_Equity,ADBE_US_Equity]

BASE is the merged blob `9f72b58aa87e` of `lib/research/api/scoped_amgt.py` (the live package's), read with `git cat-file blob` and loaded as its own module. CANDIDATE is the checkout's
`lib.research.api.scoped_amgt` (or `--candidate-file`, used for the dry-run at the base). Both handlers run in ONE process, on the same live pool, READ-ONLY (S3 reads, no function invoke,
no write), the base first. Arms, per resolved subject unless stated:
  A1  the candidate prints `AMGT_PHASE route=overlay phase=<name> ms=<n>` lines for exactly these phases, in this order: identity, model_block, axis_reads, check_face, feed,
      description, research_coverage, posture, peers, provenance, top_band, input_provenance, read_security_overlay, serialize
  A2  the BASE prints none (the negative arm: the instrument can tell a build from a base)
  A3  the status and the body are byte-equal between base and candidate
  A4  the eleven inner phases (model_block ... input_provenance) sum to `read_security_overlay` within max(5 percent, 5 ms); identity + read_security_overlay + serialize sum to the
      handler call's own measured time within max(5 percent, 5 ms)
  A5  every printed line that is NOT an `AMGT_PHASE route=overlay` line is the same set of lines in base and candidate (a trailing `=<ms>` number blanked)
  Once: B1 an unresolved key (`ZZZZ_XX_Equity`) answers the same status and the same body in base and candidate; B2 the thesis route for the first subject prints no
  `route=overlay` line in the candidate.
Verdict line `R102 OVERLAY PHASE LOG: YES|NO`, exit 0 on YES. Writes nothing.
"""
import contextlib
import importlib.util
import io
import re
import subprocess
import sys
import time

BASE_BLOB = "9f72b58aa87e"
PHASES = ["identity", "model_block", "axis_reads", "check_face", "feed", "description", "research_coverage", "posture", "peers", "provenance", "top_band",
          "input_provenance", "read_security_overlay", "serialize"]
INNER = PHASES[1:12]
PHASE_LINE = re.compile(r"^AMGT_PHASE route=overlay phase=(\S+) ms=(\d+)\s*$")


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def event(key, leaf):
    return {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, leaf), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
            "headers": {"x-firm-id": "opal"}}


def run(mod, key, leaf):
    buf = io.StringIO()
    t0 = time.monotonic()
    with contextlib.redirect_stdout(buf):
        resp = mod.handler(event(key, leaf))
    wall_ms = (time.monotonic() - t0) * 1000.0
    return resp, buf.getvalue().splitlines(), wall_ms


def within(a, b):
    return abs(a - b) <= max(0.05 * max(a, b), 5.0)


def main(argv):
    def opt(name, default):
        return argv[argv.index(name) + 1] if name in argv else default

    subjects = opt("--subjects", "ASML_NA_Equity,ADBE_US_Equity").split(",")
    base_src = subprocess.run(["git", "cat-file", "blob", BASE_BLOB], capture_output=True, check=True).stdout
    base_path = "r102_base_scoped_amgt.py"
    import os
    import tempfile

    tmp = tempfile.mkdtemp(prefix="r102base_")
    base_path = os.path.join(tmp, base_path)
    with open(base_path, "wb") as fh:
        fh.write(base_src)
    base = load_file("scoped_amgt_base", base_path)
    cand_file = opt("--candidate-file", None)
    if cand_file:
        cand = load_file("scoped_amgt_candidate", cand_file)
    else:
        from lib.research.api import scoped_amgt as cand  # noqa: WPS433

    arms = []

    def arm(name, ok, detail=""):
        arms.append((name, ok))
        print("   %s %s %s" % ("PASS" if ok else "FAIL", name, detail))

    for sj in subjects:
        b_resp, b_lines, _ = run(base, sj, "overlay")
        c_resp, c_lines, c_wall = run(cand, sj, "overlay")
        c_phase = [PHASE_LINE.match(x) for x in c_lines]
        c_phase = [m for m in c_phase if m]
        names = [m.group(1) for m in c_phase]
        ms = {m.group(1): int(m.group(2)) for m in c_phase}
        arm("A1 %s phases in order" % sj, names == PHASES, "got %s" % names)
        b_n = sum(1 for x in b_lines if PHASE_LINE.match(x))
        arm("A2 %s base prints no overlay phase line" % sj, b_n == 0, "base lines %d" % b_n)
        same = b_resp.get("statusCode") == c_resp.get("statusCode") and b_resp.get("body") == c_resp.get("body")
        arm("A3 %s status and body byte-equal" % sj, same, "status %s/%s body %s/%s bytes" % (b_resp.get("statusCode"), c_resp.get("statusCode"),
                                                                                           len(b_resp.get("body") or ""), len(c_resp.get("body") or "")))
        if names == PHASES:
            inner = sum(ms[n] for n in INNER)
            outer = ms["identity"] + ms["read_security_overlay"] + ms["serialize"]
            arm("A4a %s inner phases sum to read_security_overlay" % sj, within(inner, ms["read_security_overlay"]), "%d ms against %d ms" % (inner, ms["read_security_overlay"]))
            arm("A4b %s outer phases sum to the handler call" % sj, within(outer, c_wall), "%d ms against %.0f ms" % (outer, c_wall))
        else:
            arm("A4a %s inner phases sum to read_security_overlay" % sj, False, "phases missing")
            arm("A4b %s outer phases sum to the handler call" % sj, False, "phases missing")
        # the existing `AMGT_SEGMENT <stage>=<ms>` timing lines carry a per-run number: compare the line with its trailing number blanked
        b_rest = sorted(re.sub(r"=\d+\s*$", "=N", x) for x in b_lines if not PHASE_LINE.match(x))
        c_rest = sorted(re.sub(r"=\d+\s*$", "=N", x) for x in c_lines if not PHASE_LINE.match(x))
        arm("A5 %s other printed lines unchanged" % sj, b_rest == c_rest, "base %d candidate %d" % (len(b_rest), len(c_rest)))
    ub, _, _ = run(base, "ZZZZ_XX_Equity", "overlay")
    uc, ulines, _ = run(cand, "ZZZZ_XX_Equity", "overlay")
    arm("B1 unresolved key: same status and body", ub.get("statusCode") == uc.get("statusCode") and ub.get("body") == uc.get("body"),
        "status %s/%s" % (ub.get("statusCode"), uc.get("statusCode")))
    _, tlines, _ = run(cand, subjects[0], "thesis")
    arm("B2 the thesis route prints no overlay phase line", not any(PHASE_LINE.match(x) for x in tlines), "thesis lines %d" % len(tlines))
    passed = sum(1 for _, ok in arms if ok)
    print("   arms passed %d of %d" % (passed, len(arms)))
    verdict = "YES" if passed == len(arms) else "NO"
    print("R102 OVERLAY PHASE LOG: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
