#!/usr/bin/env python3
"""NFRA_CLDGRPH.TO-CG-D-10 -- join the served-vintage timeline to the answers and age each one.

Author: 0.9.0_WK_NFRA_CLDGRPH~1.  READ-ONLY; consumes raw log dumps cycle.sh already fetched.
Both inputs are `<epoch_ms> <TAB> <message>` exactly as `.tools/aws logs filter-log-events
--query 'events[].[timestamp,message]' --output text` emits them (CR already stripped).

METHOD, stated so its coverage is auditable:
  The serving process logs no vintage on the access line -- `log_message` emits
  `http "%s" %s %s` and nothing else (projection_server.py:499-500).  So an answer is
  PLACED against the timeline: the served vintage at instant t is the vintage of the
  LAST vintage-setting event at or before t, and age(t) = t - vintage.

  A vintage-setting event is either `projection swap complete: {...}` (the watcher's
  install, :406) or `initial verified projection open read-only: {...}` (startup's
  install, :514).  Startup does NOT emit a swap line -- install() returns "started",
  not "swapped" -- so a timeline built from swaps alone LOSES the vintage across a task
  replacement.  Both are read.

  EFFECTIVE-FROM IS THE CLOUDWATCH EVENT TIMESTAMP, not the message's `last_swap`.
  The log line is emitted AFTER install returns, so the event timestamp is >= the true
  instant the new vintage began being served.  Using it holds the OLD vintage active
  slightly longer than it really was, which makes every age an UPPER BOUND.  A ceiling
  arm should be strict against itself.

  An answer earlier than every timeline entry cannot be placed and is counted in
  UNPLACED_ANSWERS rather than silently dropped -- a zero there is the coverage claim.
"""
from __future__ import annotations

import bisect
import re
import sys
from datetime import datetime, timezone

VINTAGE_RE = re.compile(r"'vintage': '([^']+)'")
HTTP_RE = re.compile(r'http "([A-Z]+) (\S+) HTTP/[0-9.]+" ([0-9]{3})')


def parse_vintage(text: str) -> datetime:
    """'2026-09-05T02:11:10.919000+00:00' -> aware UTC datetime, without relying on
    fromisoformat's version-dependent offset handling."""
    body = text.strip()
    for suffix in ("+00:00", "Z"):
        if body.endswith(suffix):
            body = body[: -len(suffix)]
            break
    fmt = "%Y-%m-%dT%H:%M:%S.%f" if "." in body else "%Y-%m-%dT%H:%M:%S"
    return datetime.strptime(body, fmt).replace(tzinfo=timezone.utc)


def split_event(row: str) -> tuple[int, str] | None:
    head, _, rest = row.partition("\t")
    if not head.strip().isdigit():
        return None
    return int(head.strip()), rest


def load(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        return [line.rstrip("\r\n") for line in handle if line.strip()]


def main() -> int:
    if len(sys.argv) != 3:
        sys.stderr.write("usage: cycle_ages.py <timeline_raw.tsv> <http_raw.tsv>\n")
        return 2

    timeline_rows = load(sys.argv[1])
    http_rows = load(sys.argv[2])

    timeline: list[tuple[int, str, int]] = []
    for row in timeline_rows:
        parsed = split_event(row)
        if parsed is None:
            continue
        ts_ms, message = parsed
        found = VINTAGE_RE.search(message)
        if not found:
            continue
        vintage = found.group(1)
        timeline.append((ts_ms, vintage, int(parse_vintage(vintage).timestamp() * 1000)))
    timeline.sort(key=lambda item: item[0])

    answers: list[tuple[int, str, str]] = []
    for row in http_rows:
        parsed = split_event(row)
        if parsed is None:
            continue
        ts_ms, message = parsed
        found = HTTP_RE.search(message)
        if not found:
            continue
        answers.append((ts_ms, found.group(3), found.group(1) + found.group(2)))
    answers.sort(key=lambda item: item[0])

    print("TIMELINE_RAW_LINES=%d  TIMELINE_EVENTS_PARSED=%d" % (len(timeline_rows), len(timeline)))
    print("HTTP_RAW_LINES=%d  HTTP_LINES_PARSED=%d" % (len(http_rows), len(answers)))

    if not timeline:
        print("TIMELINE_READ=READ_FAILED_OR_EMPTY -- no vintage-setting event parsed; NO age is derivable")
        return 1
    if not answers:
        print("ANSWERS_READ=READ_FAILED_OR_EMPTY -- no http line parsed; NO age is derivable")
        return 1

    starts = [item[0] for item in timeline]
    unplaced = 0
    aged: list[tuple[float, int, str]] = []
    aged_any: list[float] = []
    by_status: dict[str, int] = {}
    by_route: dict[str, int] = {}

    for ts_ms, status, route in answers:
        by_status[status] = by_status.get(status, 0) + 1
        by_route[route] = by_route.get(route, 0) + 1
        index = bisect.bisect_right(starts, ts_ms) - 1
        if index < 0:
            unplaced += 1
            continue
        _, vintage, vintage_ms = timeline[index]
        age_s = (ts_ms - vintage_ms) / 1000.0
        aged_any.append(age_s)
        if route == "POST/cypher" and status == "200":
            aged.append((age_s, ts_ms, vintage))

    print("PLACEMENT_METHOD=last-vintage-setting-event-at-or-before-answer (event ts => UPPER BOUND age)")
    print("UNPLACED_ANSWERS=%d of %d" % (unplaced, len(answers)))
    for status in sorted(by_status):
        print("  http_status %s = %d" % (status, by_status[status]))
    for route in sorted(by_route):
        print("  route %s = %d" % (route, by_route[route]))

    print("SERVED_POST_CYPHER_200=%d" % len(aged))
    if not aged:
        print("OLDEST_AGE_CANDIDATE=NONE -- no placed 200 POST /cypher answer in the window")
        return 1

    aged.sort(reverse=True)
    print("TOP5_OLDEST_ANSWERS (age_s | answered_at | served_vintage):")
    for age_s, ts_ms, vintage in aged[:5]:
        answered = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
        print("  %.3f | %s | %s" % (age_s, answered.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), vintage))

    print("OLDEST_AGE_CANDIDATE=%.3f" % aged[0][0])
    print("WIDER_BOUND_OLDEST_AGE_ANY_HTTP_S=%.3f" % max(aged_any))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
