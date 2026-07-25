#!/usr/bin/env python3
"""exec-commit-queue -- what is waiting on an exec's commit, sourced from the GATE'S OWN REFUSALS.

WHY THIS EXISTS (CTO~Z dispatch 181813Z, design read 182142Z, Option C ruled 182258Z):
The owned-paths pre-commit hook correctly refuses a lane's commit to an exec-locked path. It tells
the LANE "no" at commit time and tells the EXEC nothing, ever -- so the artifact's existence lives
only in whatever message the lane happened to send.

    >> A CORRECT GATE WITH NO QUEUE IS A DROP, NOT A HOLD. <<

A block whose only carrier is the blocked party's persistence resolves for whoever is loudest, which
is a terrible selection function: the lanes doing the most careful work mention it once and move on.

SOURCE, AND WHY NOT A TREE SCAN (measured, design read 182142Z):
A tree scan of exec-locked paths returned 41 hits with ZERO under 6h old -- the newest plausible
deliverable 42h, the bulk 30-day-old exec self-authored sediment. The dispatch's population is
TRANSIENT (it appears and clears within a session); a tree scan finds a persistent sediment instead.
Two different problems sharing one query. Worse, a tree scan CANNOT recover authorship: the path
encodes whose TREE a file is in, never who WROTE it, and for the population that matters the author
is by definition a different lane, on a file with no git author.

    >> The GATE is the only point where authorship AND intent are both known. <<

`.tools/git-hooks/owned-paths-check.sh:122` already appends, on every refusal:
    <ISO_TS> BLOCK  <AGENT>  <N_FILES>  (<N> violation(s): VIOLATION: <path> -- lane=<LANE> ...)
Agent (with ~lane suffix), path, owning lane, explicit-Z timestamp, intent certain. 673 entries.
So this tool CHANGES NOTHING: it is a pure reader. No hook edit, no write, no new failure mode on
the commit path -- the risk class a logging change would introduce simply does not arise.
(An earlier revision of this design proposed adding that logging. It was already there; I had not
read the refusal branch. The scope bound never blocked anything.)

>> ANDREW-DIRECT, STANDING -- DO NOT ADD A GOVERNANCE PREDICATE TO THIS TOOL. <<
Verbatim (direct to 1.0.0_SA_CTO, ~2026-07-25T185538Z, relayed by 1.0.0_SA_CTO~Z 185751Z):

    "our comp tools should absolutely never be limited on governance. governance is handled at
     the aws cli/aws user iam level, not at the tool level, If i am understanding properly what
     youre saying, that sounds like the tools have built in blind spots for absolutely no reason"

Binding on NFRA tool design generally: no comp-tool gets a governance predicate, a hold check, or
an `*_INCLUDE_HELD` env var. If a reader should not see a row, that is an IAM/filesystem decision,
NOT a filter here. This tool reports everything it can see and prints the denominator of what it
scanned. The ONE suppression it performs -- refusals whose path has since landed -- is the
RECONCILIATION (a BLOCK is an event, not a state), it is counted in the denominator block on every
run, and `--all` reveals it. That is the opposite shape from the banned one: it announces what it
withheld and hands the reader the switch.

The sharpest half of the ruling, worth keeping next to the code: several retired guards gated
*repo source reads* -- and IAM does not govern local file reads, so those paths were never
governed, only PRETEND-governed. No enforcement, real blindness, and the appearance of both
handled. A `startswith` check is not an access control.

CONTRACT -- EMIT ROWS AND DENOMINATORS, NEVER A HAND-SUMMARIZED VERDICT (2.0.0_SA_COO~Z, 182935Z):
This tool exists because a summary standing in for a measurable state loses the thing that matters.
Its author proved that the same day by hand-writing "14 files: 11 briefs" over correct data that
said 18 including a commissioned deliverable. So: print the rows, print every denominator, print
what was suppressed and why, and let the reader re-run the query. A count without its rows is the
defect this tool is about.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
AUDIT_LOG = os.path.join(WS, "org", "git-author-override-audit.log")

# 2026-07-25T15:05:39Z BLOCK  0.8.0_AE_CloudComp~E  2  (1 violation(s): VIOLATION: <path> -- lane=<LANE> (...
_BLOCK_RE = re.compile(r"^(?P<ts>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\s+BLOCK\s+(?P<agent>\S+)\s+(?P<nfiles>\d+)\s+\((?P<detail>.*)$")
_NVIOL_RE = re.compile(r"^(?P<n>\d+)\s+violation")
_VIOL_RE = re.compile(r"VIOLATION:\s+(?P<path>\S+)\s+--\s+lane=(?P<lane>[A-Z0-9_]+)")


def _git(args):
    p = subprocess.run(["git"] + args, cwd=WS, capture_output=True, text=True)
    return p.stdout


def _landed_since(path: str, ts_iso: str) -> bool:
    """Did ANY commit touching `path` land AFTER the refusal at ts_iso?

    THIS IS THE TOOL'S ONE JOB AND MY FIRST VERSION GOT IT WRONG. That version asked
    "is this path currently dirty?" -- which conflates NEVER LANDED with LANDED-THEN-TOUCHED-AGAIN.
    Both false positives were live on the first run:
        boundary_report.py  blocked 2026-07-25T15:05:39Z -> committed 48f5ab1037 AFTER the block,
                            then modified again -> dirty -> reported "never landed". FALSE.
        ts_source.py        blocked 2026-07-22T22:33Z    -> committed d34e1ed4d7, now shows ` D`.
                            FALSE.
    A queue that tells an exec to commit something already committed is worse than no queue: it
    spends the reader's trust on the first row they check. `--since` on the path is the predicate
    that actually answers the question the row claims to answer.

    NOTE ON THE CLOCK (the trap this author landed a record about the same day): the audit log's
    stamps are already explicit-Z at source, and `--since` is handed that exact string -- git parses
    the trailing Z as UTC. No local-time reformat, no hand-stamped Z anywhere in this path.
    """
    out = _git(["log", "--format=%h", "--since=%s" % ts_iso, "--", path])
    return bool(out.strip())


def main() -> int:
    ap = argparse.ArgumentParser(description="Artifacts blocked by the owned-paths gate and never landed.")
    ap.add_argument("--lane", help="only rows whose owning lane matches (e.g. BASE_EXEC)")
    ap.add_argument("--agent", help="only rows blocked from this agent serial (substring ok)")
    ap.add_argument("--days", type=float, default=None, help="only refusals within the last N days")
    ap.add_argument("--all", action="store_true", help="include rows whose path HAS since landed")
    args = ap.parse_args()

    if not os.path.exists(AUDIT_LOG):
        # Fail LOUD and explicitly: an absent source is not an empty queue.
        print("exec-commit-queue: AUDIT LOG NOT FOUND at %s" % AUDIT_LOG)
        print("  This is NOT 'nothing is queued' -- it is 'the source could not be read'.")
        return 3

    now = datetime.now(timezone.utc)
    lines = 0
    block_lines = 0
    unparsed = 0
    truncated_events = 0
    rows = []           # (ts, agent, path, lane, age_h)
    seen = set()

    with open(AUDIT_LOG, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            lines += 1
            m = _BLOCK_RE.match(raw.strip())
            if not m:
                continue
            block_lines += 1
            detail = m.group("detail")
            nv = _NVIOL_RE.match(detail)
            n_declared = int(nv.group("n")) if nv else None
            viols = list(_VIOL_RE.finditer(detail))
            if not viols:
                unparsed += 1
                continue
            # KNOWN SOURCE TRUNCATION: the hook logs only FIRST3 violations (owned-paths-check.sh:115).
            # A refusal naming >3 paths is under-represented AT SOURCE and no reader can recover the rest.
            if n_declared is not None and n_declared > len(viols):
                truncated_events += 1
            # ts is already explicit-Z at source -- parsed as UTC, never re-stamped.
            ts = datetime.strptime(m.group("ts"), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age_h = (now - ts).total_seconds() / 3600.0
            for v in viols:
                rows.append((ts, m.group("agent"), v.group("path"), v.group("lane"), age_h))

    # Filter FIRST, reconcile after -- one `git log` per surviving (path, agent), not per raw pair.
    pending, landed = [], 0
    for ts, agent, path, lane, age_h in rows:
        if args.days is not None and age_h > args.days * 24:
            continue
        if args.lane and lane != args.lane:
            continue
        if args.agent and args.agent not in agent:
            continue
        key = (path, agent)
        if key in seen:
            continue
        seen.add(key)
        resolved = _landed_since(path, ts.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if resolved:
            landed += 1
            if not args.all:
                continue
        pending.append((ts, agent, path, lane, age_h, not resolved))

    pending.sort(key=lambda r: r[0], reverse=True)

    print("=" * 78)
    print("EXEC COMMIT QUEUE -- artifacts a lane was REFUSED and that never landed")
    print("  source: org/git-author-override-audit.log (the gate's own refusals; read-only)")
    print("  now:    %s" % now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("=" * 78)
    if not pending:
        print("\n  no rows.\n")
    else:
        print()
        for ts, agent, path, lane, age_h, still in pending:
            print("  %s  %6.1fh  %-26s %s" % (ts.strftime("%Y-%m-%dT%H:%MZ"), age_h, agent, path))
            print("  %s  lane=%s%s" % (" " * 24, lane, "" if still else "   [HAS SINCE LANDED]"))
        print()

    # ---- DENOMINATORS. Every run. The count alone is the defect this tool is about. ----
    print("-" * 78)
    print("DENOMINATORS (print, never assume):")
    print("  audit-log lines read .................. %d" % lines)
    print("  BLOCK events parsed ................... %d" % block_lines)
    print("  BLOCK events with no parseable path ... %d" % unparsed)
    print("  (path, agent) refusal pairs ........... %d" % len(rows))
    print("  rows shown ............................ %d" % len(pending))
    print("  refusals whose path HAS since landed ... %d  (suppressed unless --all)" % landed)
    print("")
    print("  KNOWN SOURCE TRUNCATION -- NOT recoverable by this reader:")
    print("    BLOCK events naming MORE paths than were logged ... %d" % truncated_events)
    print("    owned-paths-check.sh:115 logs only the FIRST 3 violations per refusal.")
    print("    For those events this queue UNDER-REPORTS at source. A fix belongs in the")
    print("    hook, not here; this tool states the limit rather than hiding it.")
    print("")
    print("  WHAT THIS TOOL DOES NOT SEE:")
    print("    - a lane that hit the gate and never retried (no second refusal to log)")
    print("    - an artifact never staged at all (the gate only sees staged paths)")
    print("    - anything predating this log's retention")
    print("-" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
