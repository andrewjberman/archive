#!/usr/bin/env python3
"""NFRA_CLDGRPH.TO-CG-D-10 / D10-AC3 as AMENDED 2026-09-05 ~16:4xZ -- HAND_ENFORCED_CEILING.

Author: 0.9.0_WK_NFRA_CLDGRPH~1.  READ-ONLY; consumes files cycle.sh already fetched.

THE AMENDED QUESTION, and it is not the one pass 1 answered.
    Pass 1 counted hand-STARTED RunTasks and named the writer set.  Both numbers were
    right and both are still printed; neither is the bar any more.  The bar is now:
    over every hand-started task in the cycle (N), how many (n) had the EFFECT of making
    a SERVED ANSWER FRESHER THAN THE SCHEDULE ALONE WOULD HAVE MADE IT.  A hand-started
    task that rebuilt something else, or whose output was never served, does not enforce
    the ceiling.  The effect is read from the task and the artifact it produced, NEVER
    from the fact that a hand started it.

THE ATTRIBUTION RULE -- both limbs, or neither.
  A served vintage V is ATTRIBUTED to RunTask T iff:
   (i)  CONTAINMENT.  V's instant lies inside T's OWN execution window
        [RunTask eventTime, last event on T's own log stream].  V is the SOURCE-WAREHOUSE
        COMMIT instant, not a build time: the manifest carries the same value three times
        (`vintage`, `committed_at`, `source_vintage.*_metadata_last_modified`), so "the
        source data was committed while T was running" is READ FROM THE ARTIFACT.
   (ii) FAMILY CONSISTENCY.  V's manifest (writer_id, mode) is a form T's family produces.
  Containment alone would convict any task that merely overlapped somebody else's commit.
  Family consistency alone would convict every derive-runner that ever ran.  Both.
  A family with NO declared form FAILS CLOSED: containment alone ATTRIBUTES, loudly, so an
  unmodelled producer is never silently excused.

THE EFFECT IS COMPUTED, NOT ARGUED -- a counterfactual re-ageing.
  For a task T with attributed set S: rebuild the served-vintage timeline with every entry
  whose vintage is in S REMOVED, then re-age every answer against that reduced timeline.
  The previous vintage simply stays served for longer, which is exactly what would have
  happened had T never run.  T made a served answer fresher iff some answer's age STRICTLY
  INCREASES under the removal.  The per-answer delta and the affected interval are printed.
  STATED LIMIT of the counterfactual: a later INCREMENTAL build is assumed to keep its own
  vintage, because a vintage is the SOURCE commit instant and does not depend on which
  projection the incremental was layered onto.  Ages after the next scheduled swap are
  therefore unchanged by construction, and the effect this measures is bounded to the
  interval between T's swap and the next non-attributed swap.

AND THE ZERO IS CONTROLLED.  A per-task zero here is a claim of ABSENCE, so the same
counterfactual is run against a SCHEDULED producing task before any zero is reported.  If
the removal of a scheduled task's vintage does NOT move any age, the arm is dead and no
zero from it means anything -- the script says so and returns non-zero.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
from datetime import datetime, timezone

VINTAGE_RE = re.compile(r"'vintage': '([^']+)'")
HTTP_RE = re.compile(r'http "([A-Z]+) (\S+) HTTP/[0-9.]+" ([0-9]{3})')

PROVENANCE_FORMS = (
    (re.compile(r"^Started by Eventbridge Pipes"), "PIPE"),
    (re.compile(r"^events-rule/"), "SCHEDULER_EVENTS_RULE"),
    (re.compile(r"^chronos-schedule/"), "SCHEDULER_CHRONOS"),
    (re.compile(r"^ecs-svc/"), "SERVICE_SCHEDULER"),
    (re.compile(r"^Started by ECS Service"), "SERVICE_SCHEDULER"),
)

# The manifest forms each task FAMILY is known to produce.  Read from the manifests of the
# cycle's own vintages, not assumed: every `mode: full` vintage in this estate carries
# writer_id `derive_runner`, and the derive-runner family is the only producer of one.
FAMILY_WRITER_FORMS = {
    "globgrph-derive-runner": {("derive_runner", "full")},
    # globgrph-trino is DELIBERATELY ABSENT, not mapped to the empty set: an absent family
    # fails CLOSED (containment alone attributes it, loudly), so leaving it out cannot
    # quietly excuse it.  What excuses the trino tasks is their own log, printed by cycle.sh.
}


def parse_vintage(text: str) -> datetime:
    body = text.strip()
    for suffix in ("+00:00", "Z"):
        if body.endswith(suffix):
            body = body[: -len(suffix)]
            break
    fmt = "%Y-%m-%dT%H:%M:%S.%f" if "." in body else "%Y-%m-%dT%H:%M:%S"
    return datetime.strptime(body, fmt).replace(tzinfo=timezone.utc)


def vms(text: str) -> int:
    return int(parse_vintage(text).timestamp() * 1000)


def iso(ms: float) -> str:
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def split_event(row: str):
    head, _, rest = row.partition("\t")
    if not head.strip().isdigit():
        return None
    return int(head.strip()), rest


def load_rows(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        return [line.rstrip("\r\n") for line in handle if line.strip()]


def load_timeline(path: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for row in load_rows(path):
        parsed = split_event(row)
        if parsed is None:
            continue
        found = VINTAGE_RE.search(parsed[1])
        if found:
            out.append((parsed[0], found.group(1)))
    out.sort()
    return out


def load_answers(path: str) -> list[int]:
    out: list[int] = []
    for row in load_rows(path):
        parsed = split_event(row)
        if parsed is None:
            continue
        found = HTTP_RE.search(parsed[1])
        if found and found.group(1) == "POST" and found.group(2) == "/cypher" and found.group(3) == "200":
            out.append(parsed[0])
    out.sort()
    return out


def load_manifests(path: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in load_rows(path):
        parts = row.split("\t")
        if len(parts) < 5:
            continue
        out[parts[0]] = {"rc": parts[1], "writer_id": parts[2], "mode": parts[3], "built_at": parts[4]}
    return out


def load_windows(path: str) -> dict[str, dict[str, str]]:
    """TSV: task_id <TAB> rc <TAB> first_ms <TAB> last_ms."""
    out: dict[str, dict[str, str]] = {}
    for row in load_rows(path):
        parts = row.split("\t")
        if len(parts) < 4:
            continue
        out[parts[0]] = {"rc": parts[1], "first_ms": parts[2], "last_ms": parts[3]}
    return out


def label_of(started_by: str) -> str:
    for pattern, name in PROVENANCE_FORMS:
        if pattern.search(started_by):
            return name
    return "HAND"


def age_all(timeline: list[tuple[int, str]], answers: list[int]) -> list[float | None]:
    starts = [item[0] for item in timeline]
    out: list[float | None] = []
    for ts in answers:
        index = bisect.bisect_right(starts, ts) - 1
        if index < 0:
            out.append(None)
            continue
        out.append((ts - vms(timeline[index][1])) / 1000.0)
    return out


def counterfactual(timeline, answers, base_ages, drop: set[str], tag: str) -> tuple[int, float, str]:
    """Remove every timeline entry serving a vintage in `drop`, re-age, report the delta."""
    reduced = [item for item in timeline if item[1] not in drop]
    if not reduced:
        print("  %s COUNTERFACTUAL_UNDEFINED: removing this task's vintages empties the timeline" % tag)
        return -1, 0.0, "UNDEFINED"
    new_ages = age_all(reduced, answers)
    fresher = 0
    max_delta = 0.0
    first_ms = None
    last_ms = None
    for index, answer_ms in enumerate(answers):
        before, after = base_ages[index], new_ages[index]
        if before is None or after is None:
            continue
        delta = after - before
        if delta > 0.0:
            fresher += 1
            max_delta = max(max_delta, delta)
            first_ms = answer_ms if first_ms is None else first_ms
            last_ms = answer_ms
    span = "-" if first_ms is None else "%s .. %s" % (iso(first_ms), iso(last_ms))
    return fresher, max_delta, span


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--http", required=True)
    ap.add_argument("--manifests", required=True)
    ap.add_argument("--runtask", required=True)
    ap.add_argument("--windows", required=True)
    args = ap.parse_args()

    timeline = load_timeline(args.timeline)
    answers = load_answers(args.http)
    manifests = load_manifests(args.manifests)
    windows = load_windows(args.windows)

    if not timeline or not answers:
        print("EFFECT_INPUTS=READ_FAILED_OR_EMPTY timeline=%d answers=%d -- NO count is derivable"
              % (len(timeline), len(answers)))
        print("HAND_ENFORCED_VALUE=READ_FAILED")
        print("HAND_DENOM_VALUE=READ_FAILED")
        return 1

    base_ages = age_all(timeline, answers)
    print("EFFECT_BASE: answers=%d  timeline_entries=%d  unplaced=%d"
          % (len(answers), len(timeline), sum(1 for age in base_ages if age is None)))

    # ---------------------------------------------------------------- the tasks
    tasks = []
    for row in load_rows(args.runtask):
        try:
            event = json.loads(row)
        except Exception as exc:
            print("  UNPARSEABLE_RUNTASK_ROW %s -- FAILING CLOSED, cannot be classified" % exc)
            return 1
        params = event.get("requestParameters") or {}
        started_by = str(params.get("startedBy") or "")
        family = str(params.get("taskDefinition") or "-").split("/")[-1].split(":")[0]
        arns = [t.get("taskArn", "") for t in ((event.get("responseElements") or {}).get("tasks") or [])]
        task_id = arns[0].split("/")[-1] if arns else "-"
        tasks.append({
            "event_time": event.get("eventTime"),
            "label": label_of(started_by),
            "family": family,
            "started_by": started_by or "(empty)",
            "task_id": task_id,
            "identity": (event.get("userIdentity") or {}).get("arn", "-"),
        })
    tasks.sort(key=lambda item: item["event_time"] or "")

    served_vintages = sorted({vintage for _, vintage in timeline})

    def attribute(task) -> tuple[set[str], list[str]]:
        notes: list[str] = []
        window = windows.get(task["task_id"])
        if window is None or window["rc"] != "0":
            notes.append("WINDOW_READ_FAILED rc=%s -- FAILING CLOSED: cannot exclude this task"
                         % (window["rc"] if window else "ABSENT"))
            return set(served_vintages), notes
        lo = int(task_start_ms(task))
        hi = int(window["last_ms"])
        notes.append("own-log window %s .. %s (task ran %.1f s past its RunTask call)"
                     % (iso(lo), iso(hi), (hi - lo) / 1000.0))
        forms = FAMILY_WRITER_FORMS.get(task["family"])
        hit: set[str] = set()
        for vintage in served_vintages:
            if not (lo <= vms(vintage) <= hi):
                continue
            info = manifests.get(vintage)
            if info is None or info["rc"] != "0":
                notes.append("CONTAINED %s but its MANIFEST DID NOT READ -- FAILING CLOSED, attributed" % vintage)
                hit.add(vintage)
                continue
            form = (info["writer_id"], info["mode"])
            if forms is None:
                notes.append("CONTAINED %s and family %s has NO declared form -- FAILING CLOSED, attributed"
                             % (vintage, task["family"]))
                hit.add(vintage)
            elif form in forms:
                notes.append("ATTRIBUTED %s (contained AND writer_id=%s mode=%s is family %s's form)"
                             % (vintage, info["writer_id"], info["mode"], task["family"]))
                hit.add(vintage)
            else:
                notes.append("contained %s but writer_id=%s mode=%s is NOT family %s's form -- not attributed"
                             % (vintage, info["writer_id"], info["mode"], task["family"]))
        if not hit:
            notes.append("NO served vintage was committed inside this task's own window")
        return hit, notes

    def task_start_ms(task) -> int:
        return int(parse_vintage(task["event_time"]).timestamp() * 1000)

    # ---------------------------------------------------------------- positive control FIRST
    print("EFFECT_POSITIVE_CONTROL -- the counterfactual arm must FIRE on a SCHEDULED producer")
    print("  before any per-task zero below is spent as an absence.  Control: the cycle's own")
    print("  nightly derive-runner, started by an EventBridge rule, not by a hand.")
    controls = [t for t in tasks if t["label"] == "SCHEDULER_EVENTS_RULE" and t["family"] == "globgrph-derive-runner"]
    control_fired = False
    for task in controls:
        hit, notes = attribute(task)
        for note in notes:
            print("    %s" % note)
        if not hit:
            print("    CONTROL %s attributed nothing -- cannot fire" % task["event_time"])
            continue
        fresher, max_delta, span = counterfactual(timeline, answers, base_ages, hit, "CONTROL")
        print("    CONTROL %s (%s): removing its vintage would have aged %d answer(s), max +%.3f s, over %s"
              % (task["event_time"], task["started_by"], fresher, max_delta, span))
        if fresher > 0:
            control_fired = True
    if not control_fired:
        print("EFFECT_POSITIVE_CONTROL=DEAD -- the counterfactual moved NO age even for a scheduled")
        print("  producer whose artifact was served.  A zero from this instrument would be meaningless.")
        print("HAND_ENFORCED_VALUE=CONTROL_DEAD")
        print("HAND_DENOM_VALUE=CONTROL_DEAD")
        return 1
    print("EFFECT_POSITIVE_CONTROL=FIRED -- the arm can detect a freshening effect, so a per-task")
    print("  zero below is a MEASURED absence and not a dead instrument.")
    print("")

    # ---------------------------------------------------------------- the hand tasks
    hands = [t for t in tasks if t["label"] == "HAND"]
    print("HAND_TASKS_IN_CYCLE=%d (the denominator N; every one is examined below)" % len(hands))
    enforced = 0
    for task in hands:
        print("  HAND_TASK %s | family=%s | startedBy=%s | task=%s"
              % (task["event_time"], task["family"], task["started_by"], task["task_id"]))
        hit, notes = attribute(task)
        for note in notes:
            print("      %s" % note)
        if not hit:
            print("      EFFECT=NONE -- produced no vintage that was served; it did not enforce the")
            print("      ceiling and it does not void the arm.")
            continue
        fresher, max_delta, span = counterfactual(timeline, answers, base_ages, hit, "HAND")
        if fresher > 0:
            enforced += 1
            print("      EFFECT=FRESHER -- %d served answer(s) were fresher than the schedule alone"
                  % fresher)
            print("      would have made them, by up to %.3f s, over %s" % (max_delta, span))
            print("      THIS COUNTS: a hand made a served answer fresher.")
        else:
            print("      EFFECT=NONE -- its vintage was served but removing it moves NO answer's age")
            print("      (no answer was served while it was the current vintage).")
    print("HAND_ENFORCED_VALUE=%d" % enforced)
    print("HAND_DENOM_VALUE=%d" % len(hands))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
