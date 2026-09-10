#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-4 / H4-AC2 -- CG-s-39.

WHO OR WHAT RAN THE BUILDS IN THE WINDOW.

THE BINDING IS POSITIVE, NOT ELIMINATIVE, AND THAT IS THE WHOLE POINT OF THIS
SCRIPT'S SHAPE. Each projection build's `_build_manifest.json` carries a
`nessie_commit_hash` -- the branch-head hash the projection loaded. Every writer
that advances that head logs the SAME hash in its own `MARKER_STAMPED` line
(infra/aws/globgrph/_provenance.py:416). So a build is attributed by finding the
one log line, in any writer family's own log group, whose hash EQUALS the
manifest's. That is a match on a 64-hex content identity, not "who else could it
have been". An actor named by elimination would be reported as UNATTRIBUTED; this
run does not need that branch and prints ELIMINATION_USED=false to say so.

COVERAGE: every instrument is swept and reported with what it CAN see, what it
CANNOT see, and its retention. An instrument that cannot have seen the window is
BLIND, never a zero -- a silent instrument and an absent event look identical.

READ ONLY. No publish, no run-task, no build start, no S3 write.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h4_lib as L  # noqa: E402

WINDOW_START = "2026-09-10T03:31:02"
WINDOW_END = "2026-09-10T05:32:57"
SWEEP_START = "2026-09-10T02:00:00Z"   # widened: a stamp precedes the build it causes
SWEEP_END = "2026-09-10T06:30:00Z"

BUILDS = ["2026-09-10T03:31:02.025931+00:00", "2026-09-10T05:32:57.959776+00:00"]

# Every writer family's OWN log group, plus the consumer that republishes.
WRITER_GROUPS = [
    ("/aws/lambda/opal-globgrph-incremental-updater",
     "the incremental_updater Lambda: SQS-delivered resource-change events -> one "
     "Nessie commit on globgrph.graph_nodes -> branch-head marker",
     "nothing about ECS-side derives; nothing older than its retention"),
    ("/ecs/globgrph-cse-producer",
     "the cse_producers_nightly ECS task: the nightly CSE producer legs and their "
     "marker stamp",
     "nothing about the Lambda plane; nothing older than its retention"),
    ("/ecs/globgrph/derive-runner",
     "the derive_runner ECS task: the full estate derive and its marker stamp",
     "nothing about the Lambda plane; nothing older than its retention"),
    ("/aws/ecs/opal-globgrph-projection-worker",
     "the projection worker: the EventBridge-Pipe records it woke on, the "
     "incremental refresh deltas, the artifact write and the pointer put",
     "it does not record WHY the warehouse moved, only that it did"),
]

CODEBUILD_PROJECTS = ["globgrph-derive-build", "opal-stitch-produce"]


def wrap(text, width, pad):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return [pad + o for o in out]


def main():
    print("=" * 78)
    print("H4-AC2 -- WHO OR WHAT REPUBLISHED THE PROJECTION")
    print("=" * 78)
    L.tree_read("h4_actor")
    print("")
    print("WINDOW=%s .. %s   SWEEP=%s .. %s" % (WINDOW_START, WINDOW_END, SWEEP_START[:19], SWEEP_END[:19]))
    print("")

    scratch = os.path.join(L.ROOT, ".scratch")
    os.makedirs(scratch, exist_ok=True)

    # ------------------------------------------------------------------
    # 0. The builds' own identity claims.
    # ------------------------------------------------------------------
    manifests = {}
    for b in BUILDS:
        dest = os.path.join(scratch, "h4_a_%s.json" % b[:19].replace(":", ""))
        rc = L.aws_get_object("projection/%s/_build_manifest.json" % b, dest)
        if rc != 0:
            print("BLOCKED: manifest unreadable for %s (rc=%s)" % (b, rc))
            return 2
        manifests[b] = json.load(open(dest, encoding="utf-8"))

    print("THE BUILDS AND THE IDENTITIES THEY CARRY")
    for b in BUILDS:
        m = manifests[b]
        print("  build %s" % b)
        print("    writer_id (self-declared) : %s" % m.get("writer_id"))
        print("    nessie_commit_hash        : %s" % m.get("nessie_commit_hash"))
        print("    nodes_snapshot_id         : %s" % m.get("nodes_snapshot_id"))
        print("    edges_snapshot_id         : %s" % m.get("edges_snapshot_id"))
        print("    node/edge/skipped         : %s / %s / %s"
              % (m.get("node_count"), m.get("edge_count"),
                 m.get("edges_skipped_missing_endpoint")))
    print("")
    print("  NOTE ON GRAIN: `writer_id` is what the MARKER said, copied into the")
    print("  manifest by projection_worker.py:351. It is SELF-DECLARED (the marker")
    print("  records who claims to have stamped it). It is therefore treated here as a")
    print("  LEAD, and the attribution below is made on the HASH, which the writer and")
    print("  the reader compute independently of each other.")
    print("")

    # ------------------------------------------------------------------
    # 1. SWEEP. Every writer family's own log group.
    # ------------------------------------------------------------------
    s_ms, e_ms = L.ms(SWEEP_START), L.ms(SWEEP_END)
    instruments = []          # (name, sees, cannot_see, retention, verdict, detail)
    stamps = []               # every MARKER_STAMPED line found, with its group

    for group, sees, cannot in WRITER_GROUPS:
        d = L.aws_json("logs", "describe-log-groups", "--log-group-name-prefix", group)
        gs = (d or {}).get("logGroups", []) or []
        exact = [g for g in gs if g.get("logGroupName") == group]
        if not exact:
            instruments.append((group, sees, cannot, "n/a", "BLIND",
                                "log group does not exist in this account/region"))
            continue
        ret = exact[0].get("retentionInDays")
        ev = L.logs_all(group, s_ms, e_ms, pattern="MARKER_STAMPED")
        allev = L.logs_probe(group, s_ms, e_ms, limit=50)
        for e in ev:
            stamps.append((group, e["timestamp"], e["message"].strip()))
        if not allev:
            verdict, detail = "BLIND", ("0 events of ANY kind in the sweep -- retention "
                                        "%s day(s) has aged the window out, or the family "
                                        "did not run. THIS SCRIPT DOES NOT CONVERT THAT "
                                        "INTO A ZERO." % ret)
        else:
            verdict, detail = "SEES", ("liveness probe returned %d event(s) (bounded at "
                                       "50 -- a probe, not a census); the paginated "
                                       "MARKER_STAMPED sweep returned %d line(s)"
                                       % (len(allev), len(ev)))
        instruments.append((group, sees, cannot, "%s day(s)" % ret, verdict, detail))

    # CodeBuild build history.
    for proj in CODEBUILD_PROJECTS:
        d = L.aws_json("codebuild", "list-builds-for-project", "--project-name", proj,
                       "--sort-order", "DESCENDING")
        ids = (d or {}).get("ids", []) or []
        detail = "no builds returned"
        verdict = "BLIND" if not ids else "SEES"
        in_win = []
        if ids:
            bg = L.aws_json("codebuild", "batch-get-builds", "--ids", *ids[:20])
            for b in (bg or {}).get("builds", []) or []:
                st = str(b.get("startTime", ""))[:19]
                if SWEEP_START[:19] <= st <= SWEEP_END[:19]:
                    in_win.append((st, b.get("buildStatus"), b.get("initiator", "")))
            detail = ("%d build id(s) retained; %d started inside the sweep"
                      % (len(ids), len(in_win)))
            for t in in_win:
                detail += " | %s %s initiator=%s" % t
        instruments.append(("CodeBuild project %s" % proj,
                            "the build history of the container/source images this "
                            "estate publishes, with each build's initiator",
                            "nothing about what the built code then did at run time",
                            "AWS-managed build history", verdict, detail))

    # CloudTrail management events in the window.
    # start-time is INCLUSIVE at the second -- open at +1s and test BOTH ways.
    ct_a = L.aws_json("cloudtrail", "lookup-events",
                      "--start-time", WINDOW_START, "--end-time", WINDOW_END,
                      "--max-items", "50", timeout=90)
    ct_b = L.aws_json("cloudtrail", "lookup-events",
                      "--start-time", WINDOW_START[:-2] + "03", "--end-time", WINDOW_END,
                      "--max-items", "50", timeout=90)
    n_a = len((ct_a or {}).get("Events", []) or [])
    n_b = len((ct_b or {}).get("Events", []) or [])
    instruments.append((
        "CloudTrail lookup-events (management plane)",
        "management-plane API calls in the window (RunTask, StartBuild, "
        "UpdateFunctionCode, PutBucketPolicy and the like), 90-day history",
        "S3 object-level PutObject/GetObject (DATA events, absent from the lookup "
        "plane) and Lambda Invoke -- i.e. it cannot see the publish itself",
        "90 days",
        "SEES" if (n_a or n_b) else "BLIND",
        "inclusive-second control run BOTH ways (lookup-events --start-time is "
        "INCLUSIVE at the second): start=%s -> %d event(s); start=%s (+1s) -> %d "
        "event(s), both bounded at --max-items 50"
        % (WINDOW_START, n_a, WINDOW_START[:-2] + "03", n_b)))

    # The two instruments already measured BLIND in H4-AC1, restated here so the
    # coverage table is the WHOLE instrument set and not the subset that answered.
    v = L.aws_json("s3api", "get-bucket-versioning", "--bucket", L.BUCKET)
    instruments.append((
        "S3 object VERSION HISTORY of the pointer projection/current.json",
        "nothing here",
        "every prior state of the pointer object",
        "n/a",
        "BLIND",
        "get-bucket-versioning Status=%r -- versioning was never enabled "
        "(Andrew-locked OFF), so the pointer has one version and no history."
        % ((v or {}).get("Status") or "<absent>")))

    lt = L.aws_json("ecs", "list-tasks", "--cluster", "opal-globgrph",
                    "--desired-status", "STOPPED")
    n_stopped = len((lt or {}).get("taskArns", []) or [])
    instruments.append((
        "ECS STOPPED-TASK control-plane history (ecs describe-tasks)",
        "which task ran, on what task definition, with what exit code -- for tasks "
        "that stopped RECENTLY",
        "anything older than roughly one hour",
        "about 1 hour",
        "BLIND" if n_stopped == 0 else "SEES",
        "list-tasks --desired-status STOPPED returns %d retained task(s); the window "
        "closed at %s, hours before this run." % (n_stopped, WINDOW_END)))

    # ------------------------------------------------------------------
    # 2. ATTRIBUTE each build by HASH MATCH.
    # ------------------------------------------------------------------
    actors = []
    for b in BUILDS:
        m = manifests[b]
        h = m.get("nessie_commit_hash", "")
        hits = [(g, t, msg) for (g, t, msg) in stamps if h and h in msg]
        actors.append((b, m, h, hits))

    attributed = all(len(h) == 1 for (_, _, _, h) in actors)

    print("=" * 78)
    print("COVERAGE_TABLE printed -- every instrument swept, with what it can and")
    print("cannot see and its retention. A BLIND row contributes NO zero to any count.")
    print("=" * 78)
    for name, sees, cannot, ret, verdict, detail in instruments:
        print("  [%-5s] %s" % (verdict, name))
        print("          retention: %s" % ret)
        for ln in wrap("CAN SEE: " + sees, 66, "          "):
            print(ln)
        for ln in wrap("CANNOT SEE: " + cannot, 66, "          "):
            print(ln)
        for ln in wrap("MEASURED: " + detail, 66, "          "):
            print(ln)
    print("")

    print("=" * 78)
    print("ACTOR printed -- one named act per build, bound by content identity")
    print("=" * 78)
    for b, m, h, hits in actors:
        print("  BUILD %s" % b)
        if len(hits) == 1:
            g, t, msg = hits[0]
            print("    ACTOR      : %s" % _actor_name(g))
            print("    ACT        : the MARKER_STAMPED that advanced the Nessie branch head")
            print("                 the projection then loaded")
            print("    WHERE      : %s" % g)
            print("    WHEN       : %s" % L.hhmmss(t))
        elif len(hits) == 0:
            print("    ACTOR      : UNATTRIBUTED -- no MARKER_STAMPED line in ANY swept")
            print("                 group carries this build's nessie_commit_hash")
        else:
            print("    ACTOR      : UNATTRIBUTED -- %d competing stamps carry this hash" % len(hits))
    print("")

    print("=" * 78)
    print("EVIDENCE printed -- the lines themselves, verbatim, with the identity that")
    print("binds each to its build. The manifest and the log compute this hash")
    print("independently; neither reads the other.")
    print("=" * 78)
    for b, m, h, hits in actors:
        print("  BUILD %s" % b)
        print("    manifest nessie_commit_hash = %s" % h)
        print("    manifest nodes_snapshot_id  = %s" % m.get("nodes_snapshot_id"))
        for g, t, msg in hits:
            print("    LOG %s  %s" % (L.hhmmss(t), g))
            print("        %s" % msg[:260])
            ok_snap = str(m.get("nodes_snapshot_id")) in msg
            print("        HASH MATCH: yes    nodes_snap MATCH: %s" % ("yes" if ok_snap else "no"))
        if not hits:
            print("    (no matching stamp line)")
    print("")

    # The triggering records for the Lambda-attributed build, if any.
    lam = "/aws/lambda/opal-globgrph-incremental-updater"
    trig = L.logs_all(lam, L.ms("2026-09-10T05:32:00Z"), L.ms("2026-09-10T05:34:00Z"),
                      pattern="DERIVED")
    if trig:
        print("  WHAT WOKE THE ATTRIBUTED WRITER (the same Lambda's own records):")
        seen = []
        for e in trig:
            msg = e["message"].strip()
            if "arn=" in msg:
                a = msg.split("arn=")[1].split(" ")[0]
                if a not in seen:
                    seen.append(a)
        for a in seen[:8]:
            print("    resource-change event on %s" % a)
        print("    -> %d distinct resource ARN(s) in the batch(es) that produced this build"
              % len(seen))
        print("    -> these are S3 object writes; the Lambda collapses an object ARN to its")
        print("       BUCKET node (lambda_function.py:264-272) and upserts that node.")
    print("")

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("ATTRIBUTION=%s" % ("ATTRIBUTED" if attributed else "IMPOSSIBLE"))
    print("INSTRUMENTS_SWEPT=%d of %d" % (len(instruments), len(instruments)))
    print("COVERAGE_TABLE printed")
    print("ACTOR printed")
    print("EVIDENCE printed")
    print("ELIMINATION_USED=false")
    print("  (every actor above is named by a 64-hex content match between the build's")
    print("   own manifest and one writer's own log line, in that writer's own log")
    print("   group. No actor is named because the others were ruled out.)")
    print("BLIND_INSTRUMENTS=%d" % sum(1 for i in instruments if i[4] == "BLIND"))
    print("OK: H4-AC2 complete -- read only, nothing published.")
    return 0


def _actor_name(group):
    return {
        "/aws/lambda/opal-globgrph-incremental-updater":
            "AWS Lambda `opal-globgrph-incremental-updater` (writer_id "
            "incremental_updater), SQS-triggered by resource-change events",
        "/ecs/globgrph-cse-producer":
            "ECS task in cluster opal-globgrph, family globgrph-cse-producer "
            "(writer_id cse_producers_nightly), the nightly CSE producer",
        "/ecs/globgrph/derive-runner":
            "ECS task in cluster opal-globgrph, the derive_runner full estate derive",
    }.get(group, group)


if __name__ == "__main__":
    sys.exit(main())
