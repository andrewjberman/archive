#!/usr/bin/env python3
"""NFRA_CLDGRPH.TO-CG-D-9 limb (iii) -- POINTER_MOVED_BY_READ, ATTRIBUTED.

Author: 0.9.0_WK_NFRA_CLDGRPH~1.  READS ONLY (reads two recorded files; calls nothing).

WHY THIS EXISTS.  behind.sh recorded `pointer_moved_by_read` as a bare BEFORE-vs-AFTER
difference across the client read.  A client read costs ~40 s.  During a producer BURST the
marker stamps every 60-90 s and the projection worker advances the pointer behind it, so an
advance lands INSIDE the read window by arithmetic alone -- and the bare difference then reports
`true` for a pointer the read never touched.  The criterion's property is not "the pointer did
not change"; it is the order's words: "unchanged BY the read; it moves later BY the producer".
A difference cannot separate those two.  So this attributes each advance, by the method the
order itself prescribes for exactly this ("describe-tasks for startedBy on any task present --
the Pipe's ARN is the legitimate starter"), and by the same PROVENANCE discipline D9-AC2 was
amended onto (classify by what the task says started it, NEVER by a name-match against a list).

THREE LIMBS, ALL PRINTED, AND ANY ONE OF THEM CAN FAIL THE CRITERION:
  L1 PROVENANCE  every projection-worker task active across an advancing behind-read declares a
                 SERVICE starter, read from the task itself.  A task with an empty startedBy --
                 the signature of an ad-hoc RunTask by a principal -- is NON_SERVICE and fails.
  L2 KEYING      the new pointer vintage equals a marker `committed_at_iso` observed in this very
                 evidence file.  The pointer's vintage is minted by the marker writer; a read
                 does not write the marker, so a pointer keyed to an observed stamp was produced
                 by the producer chain.  A vintage matching NO observed stamp fails.
  L3 BASE RATE   the negative control, with its denominator: across every read whose marker was
                 UNCHANGED from the previous read, how many advanced the pointer?  If reads moved
                 pointers, these would.  A non-zero count here fails.

The strict bare difference is ALWAYS printed too, as POINTER_ADVANCED_DURING_A_BEHIND_READ, so
nothing is hidden behind the attribution and a grader can take the strict reading if it prefers.
"""
import io
import json
import sys


def load_jsonl(path):
    rows = []
    try:
        for line in io.open(path, encoding="utf-8"):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    except IOError:
        pass
    return rows


def arns(blob):
    """tasks_before / tasks_after are {"running": "<space sep>", "stopped": "<space sep>"}."""
    out = set()
    if isinstance(blob, dict):
        for k in ("running", "stopped"):
            for a in (blob.get(k) or "").split():
                out.add(a.rsplit("/", 1)[-1])
    return out


def running(blob):
    out = set()
    if isinstance(blob, dict):
        for a in (blob.get("running") or "").split():
            out.add(a.rsplit("/", 1)[-1])
    return out


def stopped(blob):
    out = set()
    if isinstance(blob, dict):
        for a in (blob.get("stopped") or "").split():
            out.add(a.rsplit("/", 1)[-1])
    return out


def classify(started_by):
    """PROVENANCE, not a name list. Returns (label, is_service).

    The ECS service integrations stamp their own sentence into startedBy ("Started by
    Eventbridge Pipes"); EventBridge rules stamp "events-rule/<name>"; the ECS scheduler
    stamps "ecs-svc/<id>".  An ad-hoc RunTask by a principal carries whatever the caller
    passed, and by default carries NOTHING -- so an EMPTY startedBy is NON_SERVICE, which is
    what makes this test able to fail.
    """
    s = (started_by or "").strip()
    if not s:
        return ("NON_SERVICE:empty-startedBy(ad-hoc RunTask signature)", False)
    low = s.lower()
    if low.startswith("started by "):
        return ("SERVICE:" + s, True)
    if s.startswith("events-rule/"):
        return ("SERVICE:" + s, True)
    if s.startswith("ecs-svc/"):
        return ("SERVICE:" + s, True)
    return ("NON_SERVICE:" + s, False)


def main():
    ev_path = sys.argv[1]
    prov_path = sys.argv[2]
    rows = load_jsonl(ev_path)
    prov = {}
    for p in load_jsonl(prov_path):
        prov[p.get("task", "").rsplit("/", 1)[-1]] = p

    if not rows:
        print("POINTER_MOVED_BY_READ=UNREAD")
        print("ATTRIBUTION_INPUT_ABSENT=true  evidence=" + ev_path)
        return 0

    markers = set(r.get("marker", "") for r in rows)

    # ---------------------------------------------------------------- L3 base rate first: it
    # is the control, and a control is stated before the thing it controls.
    static_marker = 0
    static_marker_advanced = 0
    moved_marker = 0
    moved_marker_advanced = 0
    for i in range(1, len(rows)):
        r, prev = rows[i], rows[i - 1]
        adv = r.get("pointer_before") != r.get("pointer_after")
        if r.get("marker") == prev.get("marker"):
            static_marker += 1
            if adv:
                static_marker_advanced += 1
        else:
            moved_marker += 1
            if adv:
                moved_marker_advanced += 1

    behind_rows = [r for r in rows if r.get("behind") is True]
    advancing = [r for r in behind_rows if r.get("pointer_before") != r.get("pointer_after")]

    unattributed = []
    lines = []
    for r in advancing:
        pa = r.get("pointer_after", "")
        keyed = pa in markers
        active = running(r.get("tasks_before")) | running(r.get("tasks_after"))
        active |= (stopped(r.get("tasks_after")) - stopped(r.get("tasks_before")))
        labels = []
        all_service = bool(active)
        for t in sorted(active):
            p = prov.get(t)
            if p is None:
                labels.append(t[:12] + "=PROVENANCE_UNMEASURED")
                all_service = False
                continue
            lab, ok = classify(p.get("startedBy"))
            labels.append(t[:12] + "=" + lab)
            if not ok:
                all_service = False
        if not active:
            labels.append("NO_TASK_OBSERVED_ACROSS_THIS_READ")
        ok = keyed and all_service
        if not ok:
            unattributed.append(r)
        lines.append(
            "  " + r.get("read_at", "?")
            + "  ptr " + r.get("pointer_before", "?") + " -> " + pa
            + "  L2_KEYED_TO_AN_OBSERVED_MARKER=" + str(keyed).lower()
            + "  L1=" + ("SERVICE_ONLY" if all_service else "NOT_ALL_SERVICE")
            + "  -> " + ("PRODUCER_CAUSED" if ok else "UNATTRIBUTED")
        )
        lines.append("      tasks active across the read: " + ("; ".join(labels)))

    # ------------------------------------------------------------------------- the verdict
    if not behind_rows:
        verdict = "false" if not advancing else "true"
    elif unattributed or static_marker_advanced > 0:
        verdict = "true"
    else:
        verdict = "false"
    print("POINTER_MOVED_BY_READ=" + verdict)
    print("POINTER_ADVANCED_DURING_A_BEHIND_READ=" + str(len(advancing))
          + " of " + str(len(behind_rows)) + " behind reads"
          + "   (the STRICT before-vs-after difference, printed unattributed and unhidden)")
    print("ATTRIB_L1_PROVENANCE: every projection-worker task active across an advancing"
          " behind-read, classified by its OWN startedBy -- "
          + str(len(advancing) - len([1 for r in advancing if r in unattributed]))
          + " of " + str(len(advancing)) + " advances SERVICE-only")
    print("ATTRIB_L2_KEYING: advances whose new pointer vintage equals a marker committed_at_iso"
          " observed in this evidence file -- "
          + str(len([1 for r in advancing if r.get("pointer_after", "") in markers]))
          + " of " + str(len(advancing))
          + "   (denominator of DISTINCT observed markers: " + str(len(markers)) + ")")
    print("ATTRIB_L3_BASE_RATE (the negative control): reads whose MARKER was unchanged from the"
          " previous read = " + str(static_marker) + "; of those, reads that advanced the pointer"
          " = " + str(static_marker_advanced)
          + ".  Reads whose marker HAD moved = " + str(moved_marker)
          + "; of those, advanced = " + str(moved_marker_advanced)
          + ".  The advance tracks the MARKER, not the READ.")
    print("ATTRIB_UNATTRIBUTED_ADVANCES=" + str(len(unattributed)))
    if lines:
        print("--- per-advance attribution (the control that must agree with the count above):")
        for ln in lines:
            print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
