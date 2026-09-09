#!/usr/bin/env python3
"""NFRA_CLDGRPH.TO-CG-D-10 -- the ceiling's arithmetic, the writer census, the RunTask census.

Author: 0.9.0_WK_NFRA_CLDGRPH~1.  READ-ONLY; consumes files cycle.sh already fetched.
Emits `<KEY>_VALUE=` lines that cycle.sh lifts into the single canonical KEY=value block, so
no criterion key is ever printed twice in one run (a duplicate would reorder the graded greps).

THE CEILING (the order's definition, and FWD-4's "the ceiling belongs to the schedule"):
    CEILING_S = 86400 + (built_at - vintage of the cycle's NIGHTLY) + 60
  86400  = the schedule's own period, cron(0 2 * * ? *) at item2a.tf:438-443.
  chain  = the nightly build's own duration, read from ITS OWN manifest, not assumed.
  60     = PROJECTION_WATCH_INTERVAL_SECONDS, the pointer-to-swap lag ceiling
           (projection_server.py:36, corroborated by the process's own startup line
           "pointer watcher interval 60.0 seconds").

THE NIGHTLY IS IDENTIFIED BY ITS OWN PROPERTIES, never by "newest" or by a typed date:
  a vintage served in the cycle whose manifest carries producer.mode == "full" AND
  writer_id == "derive_runner", whose swap landed in the 02:00-04:00Z band.  If that
  set is not exactly one, this prints the whole set and refuses to pick -- an ambiguous
  nightly is a finding, not a tie to break silently.

THE RUNTASK CENSUS CLASSIFIES BY PROVENANCE FORM, never by an enumeration of role names
(the defect row W1-S15 recorded: a name-list classifier convicted a chronos-scheduled
producer as a human).  Every per-row label is printed beside the count so the labels and
the total must agree, and CloudTrail's own unspoofable userIdentity is printed with it.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone

VINTAGE_RE = re.compile(r"'vintage': '([^']+)'")

PROVENANCE_FORMS = (
    (re.compile(r"^Started by Eventbridge Pipes"), "PIPE"),
    (re.compile(r"^events-rule/"), "SCHEDULER_EVENTS_RULE"),
    (re.compile(r"^chronos-schedule/"), "SCHEDULER_CHRONOS"),
    (re.compile(r"^ecs-svc/"), "SERVICE_SCHEDULER"),
    (re.compile(r"^Started by ECS Service"), "SERVICE_SCHEDULER"),
)


def parse_iso(text: str) -> datetime:
    body = text.strip()
    for suffix in ("+00:00", "Z"):
        if body.endswith(suffix):
            body = body[: -len(suffix)]
            break
    fmt = "%Y-%m-%dT%H:%M:%S.%f" if "." in body else "%Y-%m-%dT%H:%M:%S"
    return datetime.strptime(body, fmt).replace(tzinfo=timezone.utc)


def load_timeline(path: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            row = raw.rstrip("\r\n")
            head, _, rest = row.partition("\t")
            if not head.strip().isdigit():
                continue
            found = VINTAGE_RE.search(rest)
            if found:
                out.append((int(head.strip()), found.group(1)))
    out.sort()
    return out


def load_manifests(path: str) -> dict[str, dict[str, str]]:
    """TSV: vintage <TAB> rc <TAB> writer_id <TAB> mode <TAB> built_at."""
    out: dict[str, dict[str, str]] = {}
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            parts = raw.rstrip("\r\n").split("\t")
            if len(parts) < 5:
                continue
            out[parts[0]] = {
                "rc": parts[1],
                "writer_id": parts[2],
                "mode": parts[3],
                "built_at": parts[4],
            }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--manifests", required=True)
    ap.add_argument("--runtask", required=True)
    ap.add_argument("--seed-vintage", required=True)
    args = ap.parse_args()

    timeline = load_timeline(args.timeline)
    manifests = load_manifests(args.manifests)

    # ---------------------------------------------------------------- writers
    served = [args.seed_vintage] + [vintage for _, vintage in timeline]
    distinct = sorted(set(served))
    print("VINTAGES_SERVED_IN_CYCLE=%d distinct (incl. the seed served at CYCLE_START)" % len(distinct))
    failed = [v for v in distinct if manifests.get(v, {}).get("rc") != "0"]
    missing = [v for v in distinct if v not in manifests]
    print("MANIFEST_READS_OK=%d of %d" % (len(distinct) - len(failed) - len(missing), len(distinct)))
    if failed or missing:
        print("MANIFEST_READ_FAILED=%d  MANIFEST_ABSENT=%d" % (len(failed), len(missing)))
        for vintage in failed + missing:
            print("  READ_FAILED %s" % vintage)
        print("WRITERS_VALUE=READ_FAILED")
    else:
        writers: dict[str, int] = {}
        for vintage in distinct:
            writer = manifests[vintage]["writer_id"]
            writers[writer] = writers.get(writer, 0) + 1
        for writer in sorted(writers):
            print("  writer %s = %d vintage(s)" % (writer, writers[writer]))
        print("WRITERS_VALUE={%s}" % ", ".join(sorted(writers)))

    # ---------------------------------------------------------------- nightly + ceiling
    candidates = []
    for ts_ms, vintage in timeline:
        info = manifests.get(vintage)
        if not info or info["rc"] != "0":
            continue
        hour = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc).hour
        if info["mode"] == "full" and info["writer_id"] == "derive_runner" and 2 <= hour < 4:
            candidates.append((ts_ms, vintage, info))
    print("NIGHTLY_CANDIDATES=%d (full + derive_runner + swap in the 02:00-04:00Z band)" % len(candidates))
    for ts_ms, vintage, info in candidates:
        at = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
        print("  %s | vintage %s | built_at %s" % (at.strftime("%Y-%m-%dT%H:%M:%SZ"), vintage, info["built_at"]))

    if len(candidates) != 1:
        print("NIGHTLY_SWAP_AT_VALUE=AMBIGUOUS_OR_ABSENT")
        print("CHAIN_S_VALUE=AMBIGUOUS_OR_ABSENT")
        print("CEILING_S_VALUE=AMBIGUOUS_OR_ABSENT")
    else:
        ts_ms, vintage, info = candidates[0]
        swap_at = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
        chain_s = (parse_iso(info["built_at"]) - parse_iso(vintage)).total_seconds()
        ceiling = 86400.0 + chain_s + 60.0
        print("CEILING_ARITHMETIC: 86400 (cron period) + %.6f (built_at %s - vintage %s) + 60 (watcher interval) = %.6f"
              % (chain_s, info["built_at"], vintage, ceiling))
        print("NIGHTLY_SWAP_AT_VALUE=%s" % swap_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
        print("CHAIN_S_VALUE=%.3f" % chain_s)
        print("CEILING_S_VALUE=%.3f" % ceiling)

    # ---------------------------------------------------------------- RunTask census
    labels: dict[str, int] = {}
    hand_rows: list[str] = []
    total = 0
    with open(args.runtask, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            row = raw.strip()
            if not row:
                continue
            try:
                event = json.loads(row)
            except Exception as exc:  # a malformed row must never be counted as clean
                total += 1
                labels["UNPARSEABLE"] = labels.get("UNPARSEABLE", 0) + 1
                hand_rows.append("UNPARSEABLE %s" % exc)
                continue
            total += 1
            started_by = str((event.get("requestParameters") or {}).get("startedBy") or "")
            identity = event.get("userIdentity") or {}
            invoked_by = str(identity.get("invokedBy") or "-")
            label = "HAND"
            for pattern, name in PROVENANCE_FORMS:
                if pattern.search(started_by):
                    label = name
                    break
            labels[label] = labels.get(label, 0) + 1
            if label == "HAND":
                hand_rows.append("%s | startedBy=%r | invokedBy=%s | identity=%s/%s"
                                 % (event.get("eventTime"), started_by, invoked_by,
                                    identity.get("type"), identity.get("arn")))
    print("RUNTASK_EVENTS_CLASSIFIED=%d" % total)
    for label in sorted(labels):
        print("  label %s = %d" % (label, labels[label]))
    label_sum = sum(labels.values())
    print("RUNTASK_LABEL_SUM=%d (must equal RUNTASK_EVENTS_CLASSIFIED=%d): %s"
          % (label_sum, total, "AGREE" if label_sum == total else "DISAGREE"))
    for row in hand_rows:
        print("  HAND_ROW %s" % row)
    print("RUNTASK_HAND_VALUE=%d" % labels.get("HAND", 0))
    print("RUNTASK_TOTAL_VALUE=%d" % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
