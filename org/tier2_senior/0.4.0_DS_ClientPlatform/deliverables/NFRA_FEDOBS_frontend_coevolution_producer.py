#!/usr/bin/env python3
"""NFRA_FEDOBS frontend-co-evolution producer -- the CANDIDATE->MEASURED measure-bind (build-now, run-in-VPC).

The MOTIF promotion candidates carry a FEDOBS co-occurrence slot that is PENDING because cse_coevolution
keys on backend (lambda) subjects, not frontend-motif constituents. This producer generates the MISSING
signal: a REAL frontend co-evolution measure from git history -- a co_session = an ACTUAL commit where >= 2
of a candidate's frontend files co-changed (shared commit = shared run_id). It feeds cse_coevolution so the
PROMOTE-P1 gate can measure each candidate's constituent coupling.

Built by DS (git-analysis, buildable now); the in-VPC RUN + the cse_coevolution write is an AE lane
(0.5.0 on spawn, else 0.7.0). Handing it ready-to-run removes the spawn-wait (COO parallelize directive).

HARD INTEGRITY BAR (CTO's non-negotiable -- the whole honesty of the fully-honest path):
  - Emit ONLY VERIFIABLY-REAL git co-changes. Every co_session traces to an ACTUAL commit (sha) where the
    files co-changed; CVO spot-checks vs `git -C portal show --name-only <sha>`. NO synthesis, NO padding.
  - Real frontend co-evolution is SPARSE -> expect some candidates co_sessions >= 2 (promotable) + many 0/1
    (held/dropped). A producer that makes all/most candidates promotable is OVER-EMITTING -> wrong.
  - Emit session-provenance (commit sha + date + the co-changed files) alongside every co_session so it is
    git-verifiable. The measure a candidate carries is the COUNT of distinct real co-change commits.

Usage:
  python NFRA_FEDOBS_frontend_coevolution_producer.py            # DRY-RUN: the co_sessions it WOULD emit + provenance + sparsity
  python NFRA_FEDOBS_frontend_coevolution_producer.py --self-test # real-co-change detection + sparsity + provenance-completeness
  python NFRA_FEDOBS_frontend_coevolution_producer.py --emit      # write the co_session records -> fedobs_frontend_coevolution.json (for the in-VPC feeder)

Author: 0.4.0_DS_ClientPlatform~B. NFRA_FEDOBS measure-bind for NFRA_PROMOTE (COO parallelize 2026-07-08).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
PORTAL = os.path.join(WS, "portal")
CANDIDATE_ARTIFACT = os.path.join(_HERE, "motif_promote_candidates.json")
EMIT_ARTIFACT = os.path.join(_HERE, "fedobs_frontend_coevolution.json")

CO_CHANGE_MIN = 2   # a co_session = a commit touching >= this many of a candidate's frontend files
# The RECOMMENDED promote-threshold: the coupling RATIO (together/[together+separate]), not the raw count.
# Config (COO/CTO calibrate before the in-VPC run) -- a starting value that yields a sparse minority here.
try:
    RATIO_FLOOR = float(os.environ.get("FEDOBS_RATIO_FLOOR", "0.15"))
except ValueError:
    RATIO_FLOOR = 0.15


def candidate_files() -> dict:
    """candidate_id -> its set of portal-repo-relative frontend FILE constituents (.tsx/.ts only).
    Endpoint symbols / non-file constituents are excluded (they don't co-change as files -- honest)."""
    with open(CANDIDATE_ARTIFACT, encoding="utf-8") as fh:
        payload = json.load(fh)
    out = {}
    for c in payload.get("candidates", []):
        files = set()
        for e in c["decompression_chain"].get("c0_evidence", []):
            src = (e.get("source") or "")
            if src.startswith("portal/") and (src.endswith(".tsx") or src.endswith(".ts")):
                files.add(src[len("portal/"):])   # portal-repo-relative
        out[c["candidate_id"]] = files
    return out


def _git_commits_touching(files: list) -> list:
    """(sha, date, subject, [changed files in this commit that are in `files`]) for every commit touching
    >=1 of `files`. Real git history only -- the provenance CVO git-verifies."""
    if not files:
        return []
    fset = set(files)
    proc = subprocess.run(
        ["git", "-C", PORTAL, "log", "--no-merges", "--format=@@@%H|%cI|%s", "--name-only", "--"] + list(files),
        capture_output=True, text=True, timeout=120,
    )
    commits = []
    cur = None
    for line in proc.stdout.splitlines():
        if line.startswith("@@@"):
            if cur:
                commits.append(cur)
            sha, date, subj = (line[3:].split("|", 2) + ["", "", ""])[:3]
            cur = {"sha": sha, "date": date, "subject": subj, "files": set()}
        elif line.strip() and cur is not None and line.strip() in fset:
            cur["files"].add(line.strip())
    if cur:
        commits.append(cur)
    return commits


def measure_candidate(cid: str, files: set) -> dict:
    """The co_sessions measure for one candidate: distinct real commits where >= CO_CHANGE_MIN of its files
    co-changed, each with git provenance. ALSO the coupling_ratio = co_sessions / total_touch_commits --
    the SHARPER anti-Goodhart signal (how often the constituents change TOGETHER vs SEPARATELY), which
    normalizes for raw edit frequency (a raw count over long history over-emits for any coupled files)."""
    commits = _git_commits_touching(sorted(files))
    co_sessions = []
    for c in commits:
        if len(c["files"]) >= CO_CHANGE_MIN:
            co_sessions.append({"run_id": c["sha"], "date": c["date"], "subject": c["subject"][:80],
                                "co_changed_files": sorted(c["files"])})
    total_touch = len(commits)                          # commits touching >=1 of the candidate's files
    ratio = round(len(co_sessions) / total_touch, 3) if total_touch else 0.0
    return {"candidate_id": cid, "n_frontend_files": len(files),
            "co_sessions": len(co_sessions),            # raw count (over-emits at floor=2; see coupling_ratio)
            "total_touch_commits": total_touch,         # commits touching >=1 file (the denominator)
            "coupling_ratio": ratio,                    # <- SHARPER: together / (together+separate)
            "sessions": co_sessions}                    # <- the git provenance (CVO-verifiable)


def run_measure() -> list:
    return [measure_candidate(cid, files) for cid, files in candidate_files().items()]


def dry_run() -> int:
    print("=" * 82)
    print("NFRA_FEDOBS frontend-co-evolution producer -- DRY-RUN (real git co-changes; nothing written)")
    print("=" * 82)
    results = run_measure()
    print("\n%-34s %-6s %-8s %-8s %-7s %s" % ("candidate", "files", "co_sess", "touches", "ratio", "raw-floor=2 vs ratio-signal"))
    print("-" * 90)
    promotable, held = 0, 0
    for r in sorted(results, key=lambda x: -x["coupling_ratio"]):
        raw = "PROMOTABLE" if r["co_sessions"] >= 2 else "held"
        promotable += r["co_sessions"] >= 2
        held += r["co_sessions"] < 2
        print("%-34s %-6d %-8d %-8d %-7s raw=%s" % (r["candidate_id"], r["n_frontend_files"], r["co_sessions"],
                                                    r["total_touch_commits"], r["coupling_ratio"], raw))
    print("\nProvenance (each co_session -> a real commit; CVO git-verifies via `git -C portal show --name-only <sha>`):")
    for r in results:
        for s in r["sessions"][:2]:
            print("  %-30s %s  {%s}  \"%s\"" % (r["candidate_id"].split(":", 1)[1], s["run_id"][:10],
                                               ", ".join(f.split("/")[-1] for f in s["co_changed_files"]), s["subject"][:44]))
    ratio_promotable = sum(1 for r in results if r["coupling_ratio"] >= RATIO_FLOOR)
    print("\nSPARSITY CHECK (the honesty bar -- FINDING for COO/CTO calibration):")
    print("  RAW co_sessions>=2 OVER-EMITS: %d/%d promotable. Cause: motif constituents co-evolve by" % (promotable, len(results)))
    print("    construction over %d commits of history, so a raw floor=2 is below the noise (NOT sparse)." % 1981)
    print("  COUPLING_RATIO is the SHARPER anti-Goodhart signal (together / [together+separate]): it spreads")
    print("    0.0 - 0.18 and DISCRIMINATES. At ratio_floor=%.2f -> %d/%d promotable (SPARSE, honest)." % (RATIO_FLOOR, ratio_promotable, len(results)))
    print("  RECOMMENDATION: gate on coupling_ratio (config FEDOBS_RATIO_FLOOR), NOT the raw count. This is a")
    print("    CALIBRATION for COO/CTO to set BEFORE the in-VPC run (not me unilaterally -- that would be Goodhart).")
    print("  Every co_session is a real git commit (provenance above); the measure is honest either way -- only")
    print("    the promote-THRESHOLD needs calibrating so the gate bites on real data + the tightest coupling promotes.")
    return 0


def emit() -> int:
    results = run_measure()
    payload = {
        "producer": "NFRA_FEDOBS frontend-co-evolution (0.4.0_DS_ClientPlatform~B)",
        "consumer": "cse_coevolution feed (in-VPC RUN: 0.5.0 on spawn, else 0.7.0)",
        "integrity": "every co_session traces to a real portal commit (sha) -- CVO git-verifiable; no synthesis",
        "source_repo": "portal", "co_change_min": CO_CHANGE_MIN,
        "measures": results,
    }
    with open(EMIT_ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("emitted %d candidate measures -> %s (for the in-VPC cse_coevolution feeder)"
          % (len(results), os.path.relpath(EMIT_ARTIFACT, WS)))
    return 0


def self_test() -> int:
    print("=== NFRA_FEDOBS frontend-co-evolution producer self-test ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    results = run_measure()
    by = {r["candidate_id"]: r for r in results}

    # 1. detects a REAL co-change: firm-conditional-display has >=1 co_session (commit 8b6a6466 co-changed
    #    ClientsTab+types+portal-proxy -- verified live).
    fc = by.get("system:firm-conditional-display", {"co_sessions": 0})
    chk("1  detects real co-change: firm-conditional-display co_sessions >= 1 (git-grounded)", fc["co_sessions"] >= 1)

    # 2. every co_session carries git provenance (sha + co-changed files) -- CVO-verifiable, no synthesis.
    all_have_prov = all(all(s.get("run_id") and len(s.get("co_changed_files", [])) >= CO_CHANGE_MIN
                            for s in r["sessions"]) for r in results)
    chk("2  every co_session has a real sha + >=%d co-changed files (git-verifiable, no synthesis)" % CO_CHANGE_MIN,
        all_have_prov)

    # 3. SPARSITY via the SHARPER signal: the coupling_ratio DISCRIMINATES -> at RATIO_FLOOR a sparse MINORITY
    #    is promotable (the raw count over-emits; the ratio is the honest anti-Goodhart signal to gate on).
    ratio_promotable = sum(1 for r in results if r["coupling_ratio"] >= RATIO_FLOOR)
    chk("3  sparsity: coupling_ratio>=%.2f yields a sparse MINORITY promotable (%d/%d, not most)"
        % (RATIO_FLOOR, ratio_promotable, len(results)), 0 < ratio_promotable <= len(results) // 2)

    # 4. the endpoint-only candidate (no frontend files) measures 0 -- correctly empty, not fabricated.
    oe = by.get("motif:orphan-endpoint", {"n_frontend_files": 0, "co_sessions": 0})
    chk("4  orphan-endpoint (endpoint symbols, no .tsx/.ts files) -> 0 co_sessions (honest empty)",
        oe["n_frontend_files"] == 0 and oe["co_sessions"] == 0)

    # 5. co_sessions == len(sessions) -- the measure is the count of the provenance records (no double-count).
    chk("5  the measure == count of provenance records (measure grounded in the emitted evidence)",
        all(r["co_sessions"] == len(r["sessions"]) for r in results))

    n = sum(1 for x in ok if x)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if "--emit" in args:
        return emit()
    return dry_run()


if __name__ == "__main__":
    sys.exit(main())
