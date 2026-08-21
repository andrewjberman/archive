#!/usr/bin/env python3
"""A3/A4 evidence harness for comp-adversary self-test control 2.

Runs the control-2 evidence path and evaluates BOTH predicates -- the PRE-FIX
form and the LANDED form -- against the SAME composed output, so the two verdicts
are strictly comparable.

WINDOW ORACLE (the point of this harness): the defect lives in the gap between
self_test's HEAD read and compose()'s OWN HEAD read. That gap is sub-second. This
measures the crossing DIRECTLY -- setup's HEAD vs the sha compose stamped into its
own `read-vintage:` header -- rather than inferring it from HEAD before/after the
whole ~17s run, which is a window ~80x wider than the defect's.
"""
from __future__ import annotations
import argparse
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time

RV = re.compile(r"read-vintage: HEAD @([0-9a-f]+) ")


def load_tool(toolpath):
    loader = importlib.machinery.SourceFileLoader("compadv_under_test", toolpath)
    spec = importlib.util.spec_from_loader("compadv_under_test", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def old_pred(head, out):
    """PRE-FIX control 2, verbatim @0d48f454f6:  c2 = (head in out)"""
    return head in out


def new_pred(head, out):
    """LANDED control 2, verbatim @f5bbfaf66e."""
    return ("@%s : VERIFIED" % head in out
            and "(2 attempted / 1 verified / 1 UNVERIFIABLE)" in out
            and "@%s : UNVERIFIABLE" % head not in out)


def land_churn_commit(wt, tag):
    return subprocess.run(
        ["git", "-C", wt, "commit", "--allow-empty", "--no-gpg-sign", "-q",
         "-m", "a3-churn %s" % tag],
        capture_output=True, text=True).returncode


def one_iteration(mod, wt, inject, tag):
    with tempfile.TemporaryDirectory() as td:
        fx = os.path.join(td, "fixture.md")
        # ---- exactly self_test's setup, :259-260 ----
        setup_head = mod._git("rev-parse", "--short=10", "HEAD").stdout.strip()
        with open(fx, "w", encoding="utf-8") as f:
            f.write("Fixture cites @%s and @deadbeef99 plus "
                    "docs/architecture/PRD_AUTHORING_PROTOCOL.md\n" % setup_head)
        # ---- THE WINDOW. inject=True lands a commit INSIDE it: deterministic crossing ----
        injected = None
        if inject:
            rc = land_churn_commit(wt, tag)
            injected = (rc == 0)
        t0 = time.time()
        out = mod.compose(fx, None, cap=5)
        dt = time.time() - t0
        m = RV.search(out)
        observed_head = m.group(1) if m else None
    return {
        "tag": tag,
        "setup_head": setup_head,
        "compose_head": observed_head,
        "window_crossed": (observed_head is not None and setup_head != observed_head),
        "injected_commit": injected,
        "old_pred": old_pred(setup_head, out),
        "new_pred": new_pred(setup_head, out),
        "verified_line_present": ("@%s : VERIFIED" % setup_head) in out,
        "denominator_line": next((ln.strip() for ln in out.splitlines()
                                  if ln.startswith("### source 1")), None),
        "compose_secs": round(dt, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--worktree", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--iters", type=int, default=2)
    ap.add_argument("--inject", action="store_true",
                    help="land a commit INSIDE the setup->compose window (deterministic crossing)")
    a = ap.parse_args()

    os.chdir(a.worktree)
    mod = load_tool(a.tool)
    rows = []
    for i in range(1, a.iters + 1):
        r = one_iteration(mod, a.worktree, a.inject, "%s-%d" % (a.label, i))
        r["label"] = a.label
        rows.append(r)
        print("[%s iter %d] setup=%s compose=%s crossed=%-5s | OLD=%-5s NEW=%-5s | %ss"
              % (a.label, i, r["setup_head"], r["compose_head"], r["window_crossed"],
                 "PASS" if r["old_pred"] else "FAIL",
                 "PASS" if r["new_pred"] else "FAIL", r["compose_secs"]))
        sys.stdout.flush()
    print(json.dumps(rows))


if __name__ == "__main__":
    sys.exit(main())
