"""Committed self-test for the two carrier arms on TO-L3W3-COX's builder.

An exercise reported in a message is a claim; a committed test is an instrument the next reader
can run. 4.0.0_SA_CRO~X asked the successor to exercise a failing mutant naming its row, the
restored pass, and a clean committed file resolving to a git hex rather than PENDING -- all
three are arms here, plus the refusal branch nobody asked for but which decides whether the
identity function can fail at all.

⛔ THE BASELINE RUNS FIRST IN BOTH GROUPS. A mutant battery whose base does not pass reports
"all fired" and means nothing.

Run: python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/test_carrier_arms.py
"""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import os
import tempfile

BASE = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/"
CELLS = BASE + "cells.L3W3-COX.json"


def _builder():
    spec = importlib.util.spec_from_file_location("build_cells", BASE + "build_cells.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _row(doc):
    """The first AC6 artifact row -- the one the mutants name in their refusal message."""
    cell = [c for c in doc["cells"] if c["cell_id"] == "L3W3-b8a2-6"][0]
    return cell["value"]["artifacts_produced"][0]


def arms_digest(m):
    doc = json.load(open(CELLS, encoding="utf-8"))
    out = []

    # BASELINE FIRST: an untouched carrier must be ACCEPTED, or the refusals below prove nothing.
    m.refuse_bare_digests(doc)
    out.append(("baseline: untouched carrier", "ACCEPTED", True))

    for label, mutate in (
        ("digest_of removed", lambda d: _row(d).pop("digest_of")),
        ("off-enum digest_of (worktree-rendering)",
         lambda d: _row(d).__setitem__("digest_of", "worktree-rendering")),
        ("blob-at-pin with no pin on the row", lambda d: _row(d).pop("commit_or_etag")),
    ):
        mut = copy.deepcopy(doc)
        mutate(mut)
        try:
            m.refuse_bare_digests(mut)
            out.append((label, "NOT REFUSED", False))
        except ValueError as exc:
            names_row = "artifacts_produced[0]" in str(exc)
            out.append((label, "REFUSED (row named)" if names_row else "REFUSED", names_row))
    return out


def arms_identity(m):
    out = []
    pin, _ = m.artifact_identity(BASE + "ksweep_battery.json")
    ok = pin != "PENDING-THIS-COMMIT" and len(pin) == 40 and all(
        c in "0123456789abcdef" for c in pin)
    out.append(("clean committed file -> 40-char git hex, not PENDING", pin[:12] + "...", ok))

    probe = BASE + "_arm_probe.json"
    io.open(probe, "w", encoding="utf-8", newline="\n").write('{"probe": true}\n')
    try:
        pin2, _ = m.artifact_identity(probe)
        out.append(("dirty worktree file -> PENDING", pin2, pin2 == "PENDING-THIS-COMMIT"))
    finally:
        os.remove(probe)

    outside = os.path.join(tempfile.gettempdir(), "l3w3_arm_probe_outside_repo.json")
    io.open(outside, "w", encoding="utf-8").write("{}")
    try:
        m.artifact_identity(outside)
        out.append(("clean but in no commit -> refuse", "NOT REFUSED", False))
    except ValueError:
        out.append(("clean but in no commit -> refuse", "REFUSED", True))
    finally:
        os.remove(outside)
    return out


def main():
    m = _builder()
    rows = [("digest validator", a) for a in arms_digest(m)]
    rows += [("identity derivation", a) for a in arms_identity(m)]
    passed = sum(1 for _, (_, _, ok) in rows if ok)
    for group, (label, observed, ok) in rows:
        print("  [%s] %-22s %-46s %s" % ("PASS" if ok else "FAIL", group, label, observed))
    print("\n  %d of %d arms pass" % (passed, len(rows)))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
