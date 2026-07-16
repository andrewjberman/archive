#!/usr/bin/env python3
"""comp_which_zero_rate_harness.py -- the ZERO-RESULT before/after under ONE construct
(NFRA_GRAPHFEED TO-4 measurement follow-up; CTO methodology ruling 033402Z/213402Z-thread:
"define YOUR construct, print it, re-derive BOTH sides under it").

THE CONSTRUCT (label-free, printed in full, applied IDENTICALLY to both eras):
  Replay every DISTINCT logged routing query through ONE FIXED ranker -- today's
  `.tools/comp-which --json` at the git blob recorded in the results header. A routed
  outcome is ZERO-RESULT iff the fixed ranker returns routed == [] (kind=fallback/abstain:
  comp-which itself serves no candidate and hands off to a search primitive).
  Era zero-rate = sum(occurrences of q where zero) / era routing decisions.

WHAT THIS MEASURES (stated honestly): of the questions agents ACTUALLY ASKED in each era,
the fraction today's catalog+ranker cannot serve -- the query-population-vs-catalog-coverage
measure under one fixed instrument. It does NOT isolate the c52f83612 build's causal effect
(era-2 questions were asked WITH the build live; no log-only construct can un-confound that).
The prior 34.0% (SS0 errata, cohort-R filter) is a PRIOR MEASUREMENT WITH ITS OWN FILTER,
cited for history, never compared row-for-row against these numbers.

POLLUTION DISCLOSURE: every replay appends a rail-log row. The replay window (start/end ts,
this host, serial 0.8.0_AE_CloudComp~Z) is printed in the results header -- future tallies
exclude the window. The probe set is drawn FROM the log (the routing-test's own control note:
a replayed q is byte-identical to an agent asking it; it cannot pollute the QUESTION population,
only the row count).

Resume-safe: results append to comp_which_zero_rate_results.jsonl keyed by query; a re-run
skips already-replayed queries.

Usage: python comp_which_zero_rate_harness.py [--limit N] [--report-only]
Author: 0.8.0_AE_CloudComp~Z  2026-07-16
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
RAIL = os.path.join(WS, "org", "mcp", "comp-which-rail.log")
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comp_which_zero_rate_results.jsonl")
CUT = "2026-07-13T22:07"  # c52f83612 (top-3 + programmatic abstain) landed 2026-07-13 18:07 ET
ROUTING_TAGS = {"ROUTE", "ROUTE-POSTERIOR", "ROUTE-POSTERIOR-DISAMBIG", "ROUTE-SURFACE",
                "ROUTE-POINTER", "NOFIT-POSTERIOR", "RUN-GREP", "RUN-GLOB"}
PER_CALL_TIMEOUT_S = 90


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect() -> tuple:
    """Every comp-which routing decision row -> (pre Counter, post Counter) of q strings.
    Denominator discipline: counts are DECISIONS (row occurrences), replay is per DISTINCT q."""
    pre, post = collections.Counter(), collections.Counter()
    total_lines = unparsed = 0
    with open(RAIL, encoding="utf-8", errors="replace") as f:
        for ln in f:
            total_lines += 1
            m = re.match(r'^(\S+)\s+(\S+)\s+tool=comp-which\s+.*q="(.*)"\s*$', ln.strip())
            if not m:
                unparsed += 1
                continue
            ts, tag, q = m.groups()
            if tag not in ROUTING_TAGS:
                continue
            (post if ts >= CUT else pre)[q] += 1
    print(f"INFO: COLLECT lines={total_lines} (non-matching {unparsed} incl. non-comp-which rows) "
          f"pre_decisions={sum(pre.values())} pre_distinct={len(pre)} "
          f"post_decisions={sum(post.values())} post_distinct={len(post)}")
    return pre, post


def load_done() -> dict:
    done = {}
    if os.path.isfile(RESULTS):
        with open(RESULTS, encoding="utf-8") as f:
            for ln in f:
                try:
                    r = json.loads(ln)
                    done[r["q"]] = r
                except (ValueError, KeyError):
                    pass
    return done


def replay(q: str) -> dict:
    """One fixed-ranker verdict for one query. NEVER raises."""
    try:
        p = subprocess.run([sys.executable, os.path.join(WS, ".tools", "comp-which"), q, "--json"],
                           capture_output=True, text=True, timeout=PER_CALL_TIMEOUT_S,
                           cwd=WS, encoding="utf-8", errors="replace")
        out = (p.stdout or "").strip()
        start = out.find("{")
        d = json.loads(out[start:]) if start >= 0 else {}
        routed = d.get("routed")
        if routed is None:
            return {"q": q, "verdict": "UNPARSEABLE", "rc": p.returncode}
        return {"q": q, "verdict": "ZERO" if routed == [] else "SERVED",
                "kind": d.get("kind"), "n_routed": len(routed), "rc": p.returncode}
    except subprocess.TimeoutExpired:
        return {"q": q, "verdict": "TIMEOUT"}
    except Exception as e:  # noqa: BLE001
        return {"q": q, "verdict": f"ERROR:{type(e).__name__}"}


def report(pre: collections.Counter, post: collections.Counter, done: dict) -> None:
    def era(counter, name):
        decisions = sum(counter.values())
        classified = zero = served = other = 0
        for q, n in counter.items():
            r = done.get(q)
            if not r:
                continue
            classified += n
            if r["verdict"] == "ZERO":
                zero += n
            elif r["verdict"] == "SERVED":
                served += n
            else:
                other += n
        print(f"  {name}: decisions={decisions} classified={classified} "
              f"({100.0*classified/decisions if decisions else 0:.1f}% coverage) | "
              f"ZERO={zero} ({100.0*zero/classified if classified else 0:.2f}%) "
              f"SERVED={served} other(timeout/unparseable)={other}")

    print("=" * 90)
    print("ZERO-RESULT RATE -- one construct, both eras (construct printed in the module header)")
    print(f"  fixed ranker: .tools/comp-which --json at blob {_blob()}")
    print("  construct: ZERO iff routed==[] (kind=fallback/abstain) on replay")
    era(pre, "PRE  (< 2026-07-13T22:07Z, before c52f83612)")
    era(post, "POST (>= cut)")
    print("  history note: the SS0-errata 34.0% used the cohort-R filter -- prior measurement, "
          "own filter, NOT row-comparable to these numbers.")
    print("=" * 90)


def _blob() -> str:
    try:
        r = subprocess.run(["git", "-C", WS, "rev-parse", "HEAD:.tools/comp-which"],
                           capture_output=True, text=True, timeout=15)
        return r.stdout.strip()[:12]
    except Exception:  # noqa: BLE001
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="replay at most N new queries this run")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    pre, post = collect()
    done = load_done()
    if args.report_only:
        report(pre, post, done)
        return 0

    todo = [q for q in list(pre) + [q for q in post if q not in pre] if q not in done]
    # de-dup preserving order
    seen = set()
    todo = [q for q in todo if not (q in seen or seen.add(q))]
    if args.limit:
        todo = todo[:args.limit]
    print(f"INFO: REPLAY_START todo={len(todo)} already_done={len(done)} at={_now_iso()} "
          f"(POLLUTION WINDOW OPENS -- exclude rail rows from this window in future tallies)")
    with open(RESULTS, "a", encoding="utf-8") as f:
        for i, q in enumerate(todo, 1):
            r = replay(q)
            f.write(json.dumps(r) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"INFO: REPLAY_PROGRESS {i}/{len(todo)} at={_now_iso()}")
    print(f"INFO: REPLAY_END at={_now_iso()} (POLLUTION WINDOW CLOSES)")
    done = load_done()
    report(pre, post, done)
    return 0


if __name__ == "__main__":
    sys.exit(main())
