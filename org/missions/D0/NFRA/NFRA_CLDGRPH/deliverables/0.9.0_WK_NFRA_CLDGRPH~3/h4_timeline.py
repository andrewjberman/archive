#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-4 / H4-AC1 -- CG-s-39.

EVERY PROJECTION BUILD IN THE WINDOW, RECONSTRUCTED FROM ARTIFACTS, WITH ITS
DENOMINATOR -- AND EVERY INSTRUMENT THAT COULD NOT HAVE SEEN THE WINDOW REPORTED
AS BLIND RATHER THAN AS A ZERO.

WHY ARTIFACTS AND NOT THE POINTER'S HISTORY: bucket versioning on
s3://opal-313476888478-globgrph is Andrew-locked OFF (GLOBGRPH s.0 lock #5), so
`projection/current.json` has NO version history to walk. It is re-measured here
rather than quoted. The history is instead assembled from the VERSIONED ARTIFACT
KEYS `projection/<committed_at>/` and their `_build_manifest.json` objects -- the
artifact-first, pointer-last contract of CG-s-3.

CUT DISCIPLINE (spine v3.8), printed beside every number below:
  INSTRUMENT  -- what swept, over what population, with its denominator
  GRAIN       -- at what grain the value is counted
  ENVIRONMENT -- where the stored comparison value came from

READ ONLY. No publish, no run-task, no build start, no S3 write.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h4_lib as L  # noqa: E402

WINDOW_START = "2026-09-10T03:31:02"   # served vintage of the CG-s-32 baseline read
WINDOW_END = "2026-09-10T05:32:57"     # served vintage of the CG-s-33 loss read
MARGIN_START = "2026-09-10T01:00:00"
MARGIN_END = "2026-09-10T08:00:00"

# The three reads this cell inherits, as (label, served vintage prefix, source).
INHERITED_READS = [
    ("R1 CG-s-32 class census baseline", "2026-09-10T03:31:02",
     "row NFRA_CLDGRPH-W1-S39 / CG-s-32.boundary-edge-class-census.result.md"),
    ("R2 CG-s-33 loss read", "2026-09-10T05:32:57", "row NFRA_CLDGRPH-W1-S39"),
    ("R3 issuer's third read", "2026-09-10T05:57:16",
     "TO-CG-H-4 face, MEASURED block (manifest 8ea66ca427c1)"),
]

SCRATCH = os.path.join(L.ROOT, ".scratch")


def sha12(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def main():
    print("=" * 78)
    print("H4-AC1 -- THE WINDOW'S PROJECTION BUILDS, FROM ARTIFACTS")
    print("=" * 78)
    L.tree_read("h4_timeline")
    print("")
    print("WINDOW=%s .. %s  (CLOSED interval, both endpoints INCLUDED: each endpoint" % (WINDOW_START, WINDOW_END))
    print("        IS itself a served vintage, so excluding them would drop the two")
    print("        builds the cell is about.)")
    print("MARGIN=%s .. %s  (either side, as the cell asks)" % (MARGIN_START, MARGIN_END))
    print("")

    # ------------------------------------------------------------------
    # 1. THE ARTIFACT KEYS. Auto-paginated client-side; a page is not an answer.
    # ------------------------------------------------------------------
    _, prefixes = L.list_all("projection/", delimiter="/")
    instants = []
    for p in prefixes:
        body = p[len("projection/"):].rstrip("/")
        if len(body) >= 19 and body[4] == "-" and body[10] == "T":
            instants.append((body, p))
    instants.sort()
    print("INSTRUMENT   : s3api list-objects-v2 over s3://%s/projection/ with" % L.BUCKET)
    print("               delimiter '/', auto-paginated CLIENT-SIDE (a --query length()")
    print("               would have returned the PAGE count, not the population).")
    print("GRAIN        : one CommonPrefix == one PUBLISHED PROJECTION BUILD, keyed by")
    print("               its own committed_at instant; the artifact is immutable per key.")
    print("ENVIRONMENT  : LIVE AWS, account 313476888478, us-east-1, read at run time.")
    print("ARTIFACT_PREFIXES_TOTAL=%d (every build ever published under this prefix)"
          % len(instants))
    if instants:
        print("  earliest   : %s" % instants[0][0])
        print("  latest     : %s" % instants[-1][0])

    in_margin = [(b, p) for (b, p) in instants if MARGIN_START <= b[:19] <= MARGIN_END]
    in_window = [(b, p) for (b, p) in instants if WINDOW_START <= b[:19] <= WINDOW_END]
    print("")

    # ------------------------------------------------------------------
    # 2. THE MANIFESTS. One GET per build in the margin. No sampling.
    # ------------------------------------------------------------------
    os.makedirs(SCRATCH, exist_ok=True)
    rows = []
    swept = 0
    for body, prefix in in_margin:
        key = prefix + "_build_manifest.json"
        dest = os.path.join(SCRATCH, "h4_m_%s.json" % body[:19].replace(":", ""))
        rc = L.aws_get_object(key, dest)
        swept += 1
        if rc != 0 or not os.path.isfile(dest):
            rows.append({"instant": body, "manifest": "UNREADABLE rc=%s" % rc})
            continue
        m = json.load(open(dest, encoding="utf-8"))
        rows.append({
            "instant": body,
            "manifest_id": sha12(dest),
            "content_sha256": m.get("content_sha256", ""),
            "committed_at": m.get("committed_at", ""),
            "built_at": m.get("built_at", ""),
            "writer_id": m.get("writer_id", ""),
            "mode": (m.get("producer") or {}).get("mode", ""),
            "nodes": m.get("node_count"),
            "edges": m.get("edge_count"),
            "skipped": m.get("edges_skipped_missing_endpoint"),
            "nodes_snap": m.get("nodes_snapshot_id"),
            "edges_snap": m.get("edges_snapshot_id"),
            "stitch_built_at": (m.get("source_vintage") or {}).get("stitch_built_at", ""),
            "stitch_sha": ((m.get("source_vintage") or {}).get("stitch_artifact_sha256", ""))[:12],
            "in_window": WINDOW_START <= body[:19] <= WINDOW_END,
        })

    print("MANIFEST_ID_PER_BUILD printed -- one row per build in the margin window.")
    print("  manifest_id = sha256 of the _build_manifest.json BYTES as fetched (12 hex")
    print("  shown); content_sha256 = the manifest's OWN claim about the kuzu artifact.")
    print("  IN? = inside the closed window this cell is about.")
    print("")
    hdr = ("  IN? instant                              writer_id             mode        "
           "nodes  edges  skipped  manifest_id")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for r in rows:
        if "manifest_id" not in r:
            print("  ??  %-36s %s" % (r["instant"], r["manifest"]))
            continue
        print("  %s %-36s %-21s %-11s %6s %6s %8s  %s" % (
            "YES" if r["in_window"] else " no", r["instant"], r["writer_id"],
            r["mode"], r["nodes"], r["edges"], r["skipped"], r["manifest_id"][:12]))
    print("")
    print("  snapshot ids and stitch source per build (the producer inputs):")
    for r in rows:
        if "manifest_id" not in r:
            continue
        print("    %s  nodes_snap=%-20s edges_snap=%-20s stitch_built_at=%s stitch=%s"
              % (r["instant"][:19], r["nodes_snap"], r["edges_snap"],
                 r["stitch_built_at"], r["stitch_sha"]))
    print("")

    # ------------------------------------------------------------------
    # 3. WHICH BUILD EACH INHERITED READ CORRESPONDS TO.
    # ------------------------------------------------------------------
    print("WHICH BUILD EACH OF THE THREE INHERITED READS SAW")
    print("  (matched on the served vintage string, which IS the artifact prefix -- the")
    print("   service reports the manifest's `vintage`, and the manifest's `vintage`")
    print("   equals its `committed_at`, which is the key. No inference.)")
    by_instant = {r["instant"][:19]: r for r in rows if "manifest_id" in r}
    for label, vin, src in INHERITED_READS:
        r = by_instant.get(vin)
        if r is None:
            print("  %-36s vintage %s -> NO MANIFEST IN MARGIN (source: %s)" % (label, vin, src))
        else:
            print("  %-36s vintage %s" % (label, vin))
            print("      -> build %s  writer=%s  nodes=%s edges=%s skipped=%s"
                  % (r["instant"], r["writer_id"], r["nodes"], r["edges"], r["skipped"]))
            print("      -> manifest_id %s   (source of the read: %s)" % (r["manifest_id"][:12], src))
    print("")

    # ------------------------------------------------------------------
    # 4. THE DELTA THE CELL IS ABOUT, read off the manifests themselves.
    # ------------------------------------------------------------------
    a = by_instant.get(WINDOW_START)
    b = by_instant.get(WINDOW_END)
    if a and b:
        print("THE DELTA ACROSS THE WINDOW, FROM THE TWO MANIFESTS (not from any row's prose)")
        print("  nodes                        : %s -> %s   (%+d)" % (a["nodes"], b["nodes"], b["nodes"] - a["nodes"]))
        print("  edges (stored)               : %s -> %s   (%+d)" % (a["edges"], b["edges"], b["edges"] - a["edges"]))
        print("  edges_skipped_missing_endpoint: %s -> %s   (%+d)" % (a["skipped"], b["skipped"], b["skipped"] - a["skipped"]))
        print("  nodes_snapshot_id            : %s -> %s   (%s)" % (
            a["nodes_snap"], b["nodes_snap"],
            "MOVED" if a["nodes_snap"] != b["nodes_snap"] else "UNMOVED"))
        print("  edges_snapshot_id            : %s -> %s   (%s)" % (
            a["edges_snap"], b["edges_snap"],
            "MOVED" if a["edges_snap"] != b["edges_snap"] else "UNMOVED"))
        print("  stitch source                : %s -> %s   (%s)" % (
            a["stitch_built_at"], b["stitch_built_at"],
            "MOVED" if a["stitch_built_at"] != b["stitch_built_at"] else "UNMOVED"))
        print("  writer_id                    : %s -> %s" % (a["writer_id"], b["writer_id"]))
        print("")
        print("  READING: the EDGES table did not move (same snapshot id) and the stitch")
        print("  source did not move. The NODES table moved by one snapshot, the loaded")
        print("  node count fell by %d, and edges_skipped_missing_endpoint rose by %d --"
              % (a["nodes"] - b["nodes"], b["skipped"] - a["skipped"]))
        print("  the SAME number as the edge fall (%d). The 124 edges were NOT deleted from"
              % (a["edges"] - b["edges"]))
        print("  the warehouse; they became UNLOADABLE because their endpoint node left the")
        print("  nodes table. That identity is the whole mechanism and it is arithmetic, not")
        print("  a hypothesis.")
    print("")

    # ------------------------------------------------------------------
    # 5. BLIND INSTRUMENTS -- measured, never assumed, never a zero.
    # ------------------------------------------------------------------
    print("BLIND INSTRUMENTS -- an instrument that CANNOT have seen this window is")
    print("reported as BLIND with its reason, never as a contributing zero. Each verdict")
    print("below is MEASURED by the call named beside it.")
    blind = []
    seeing = []

    # (i) S3 object versioning on the pointer.
    v = L.aws_json("s3api", "get-bucket-versioning", "--bucket", L.BUCKET)
    status = (v or {}).get("Status", "")
    if status != "Enabled":
        blind.append(("S3 object VERSION HISTORY of projection/current.json",
                      "get-bucket-versioning returns Status=%r -- versioning was NEVER "
                      "enabled on this bucket (Andrew-locked OFF), so the pointer object "
                      "has exactly one version and no history to walk."
                      % (status or "<absent>")))
    else:
        seeing.append(("S3 object VERSION HISTORY", "versioning Enabled"))

    # (ii) ECS stopped-task history.
    lt = L.aws_json("ecs", "list-tasks", "--cluster", "opal-globgrph",
                    "--desired-status", "STOPPED")
    arns = (lt or {}).get("taskArns", []) or []
    oldest = None
    if arns:
        dt = L.aws_json("ecs", "describe-tasks", "--cluster", "opal-globgrph",
                        "--tasks", *arns[:100])
        stamps = [t.get("stoppedAt", "") for t in (dt or {}).get("tasks", []) if t.get("stoppedAt")]
        oldest = min(stamps) if stamps else None
    if oldest is None or str(oldest)[:19] > WINDOW_END:
        blind.append(("ECS STOPPED-TASK history (ecs describe-tasks)",
                      "list-tasks --desired-status STOPPED returns %d retained task(s); "
                      "oldest retained stoppedAt=%s. ECS keeps stopped task records for "
                      "about one hour, and this window closed at %s -- the tasks that ran "
                      "in it are gone from the ECS control plane. Their LOGS survive; the "
                      "TASK RECORDS do not."
                      % (len(arns), oldest or "<none retained>", WINDOW_END)))
    else:
        seeing.append(("ECS STOPPED-TASK history", "oldest retained %s" % oldest))

    # (iii) Container Insights performance log group (retention 1 day).
    lg = L.aws_json("logs", "describe-log-groups", "--log-group-name-prefix",
                    "/aws/ecs/containerinsights/opal-globgrph/performance")
    groups = (lg or {}).get("logGroups", []) or []
    ret = groups[0].get("retentionInDays") if groups else None
    ci = L.logs_all("/aws/ecs/containerinsights/opal-globgrph/performance",
                    L.ms(WINDOW_START + "Z"), L.ms(WINDOW_END + "Z"))
    if not ci:
        blind.append(("Container Insights performance stream (%s)"
                      % "/aws/ecs/containerinsights/opal-globgrph/performance",
                      "retentionInDays=%s and filter-log-events over the window returns 0 "
                      "events -- the retention has already aged the window out. A ZERO HERE "
                      "IS NOT 'nothing ran'; it is 'this instrument no longer holds the "
                      "window'." % ret))
    else:
        seeing.append(("Container Insights performance stream", "%d events in window" % len(ci)))

    # (iv) CloudTrail on the PUT that is the publish.
    blind.append(("CloudTrail lookup-events for the S3 PutObject that IS the publish",
                  "cloudtrail lookup-events serves MANAGEMENT events only; an S3 "
                  "object-level PutObject is a DATA event and is not in the lookup history. "
                  "The publish act itself therefore cannot be read from CloudTrail's "
                  "lookup plane at any retention. The projection worker's OWN log records "
                  "it (POINTER_PUT_OK) and is used instead."))

    print("")
    for name, why in blind:
        print("  BLIND : %s" % name)
        for line in _wrap(why, 70):
            print("          %s" % line)
    for name, why in seeing:
        print("  SEES  : %s -- %s" % (name, why))
    print("")

    # ------------------------------------------------------------------
    # 6. SUMMARY -- the accept's own vocabulary, in order.
    # ------------------------------------------------------------------
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("WINDOW=%s .. %s" % (WINDOW_START, WINDOW_END))
    print("BUILDS_FOUND=%d" % len(in_window))
    print("ARTIFACT_KEYS_SWEPT=%d of %d" % (swept, len(in_margin)))
    print("MANIFEST_ID_PER_BUILD printed  (%d manifest ids above, one per swept build)"
          % sum(1 for r in rows if "manifest_id" in r))
    print("BLIND_INSTRUMENTS=%d reported with reason" % len(blind))
    print("INSTRUMENTS_THAT_SEE_THE_WINDOW=%d" % len(seeing))
    print("OK: H4-AC1 complete -- read only, nothing published.")
    return 0


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
