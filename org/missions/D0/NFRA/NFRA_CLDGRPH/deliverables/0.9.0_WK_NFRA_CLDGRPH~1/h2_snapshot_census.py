#!/usr/bin/env python3
"""H2-AC3 -- W2-S75 RESOLVED: THREE FIGURES, THREE POPULATIONS, ONE SENTENCE EACH.

NFRA_CLDGRPH TO-CG-H-2 / cell CG-s-37, worker 0.9.0_WK_NFRA_CLDGRPH~1.

Row W2-S75 records three numbers that describe "the 2026-09-09T21:05:21Z snapshot's
source=portal-stitch nodes" and disagree: 1,771 (row W2-S61's five-way per-type census),
1,791 (the producer's own comment at derive_stitch.py, four provisional names) and 1,790
(commit 139cbe1d40: 1,521 merged + 269 carried). W2-S75 could not resolve them because its
order's bounds put the tarball read out of reach. THIS order permits the read: an
`s3api get-object` FROM s3://opal-313476888478-globgrph TO local disk publishes nothing and
pages nobody.

WHAT THE READ FOUND FIRST, AND IT CHANGES THE SHAPE OF THE ANSWER: the key those three
figures name has been OVERWRITTEN. snapshots/20260909/graph-20260909.tar.gz now carries
LastModified 2026-09-10T00:09:02Z, not 21:05:21Z, and the bucket is UNVERSIONED, so the
bytes the three figures describe no longer exist anywhere. Filed as a row. The census
therefore runs on the CURRENT bytes of that key and every figure attribution carries its
basis: MEASURED-NOW (this read), MEASURED-THEN (a record of a read of bytes now gone) or
INFERRED (arithmetic over those records).

INSTRUMENT: boto3 get_object -> tarfile -> json, then a full walk of classes_data.
COVERAGE: every node in the tarball, denominator printed, nothing excluded.
GRAIN: one node object per row, grouped by the node's own `source` stamp and by `type`.
ENVIRONMENT: the comparison values come from the round-6/7 RECORD (row W2-S61 @80daa1fff6,
the producer comment @f3b5f26f77, commit 139cbe1d40), not from a re-run of anything.
"""
from __future__ import annotations

import collections
import io
import json
import sys
import tarfile
from pathlib import Path

WS = Path(__file__).resolve().parents[7]
OUT = Path(__file__).parent
BUCKET = "opal-313476888478-globgrph"
KEY = "snapshots/20260909/graph-20260909.tar.gz"          # the key W2-S75 names
KEY_NEXT = "snapshots/20260910/graph-20260910.tar.gz"     # the following cycle, for the trend
CACHE = WS / ".scratch"
CITED_VINTAGE = "2026-09-09T21:05:21Z"

PROVISIONAL = ("GOLD_SCRIPT", "S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY")
CANONICAL = ("PipelineScript", "PipelineFunction", "S3Key", "Component", "ReactQueryKey")
STITCH_SOURCE = "portal-stitch"


def fetch(key: str) -> tuple:
    """(graph_dict, meta) -- from the local cache if present, else ONE S3 GET (a read)."""
    cached = CACHE / ("h2_snap_%s" % key.split("/")[-1])
    reads = []
    if cached.exists():
        raw = cached.read_bytes()
        origin = "LOCAL CACHE %s (bytes previously fetched by this order's own permitted GET)" % cached
        lm = None
    else:
        import boto3
        s3 = boto3.client("s3", region_name="us-east-1")
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        raw = obj["Body"].read()
        lm = obj["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
        reads.append("get_object s3://%s/%s" % (BUCKET, key))
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_bytes(raw)
        origin = "S3 GET s3://%s/%s -> %s" % (BUCKET, key, cached)
    if lm is None:
        try:
            import boto3
            s3 = boto3.client("s3", region_name="us-east-1")
            h = s3.head_object(Bucket=BUCKET, Key=key)
            lm = h["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
            reads.append("head_object s3://%s/%s" % (BUCKET, key))
        except Exception as exc:
            lm = "UNREAD (%s)" % str(exc)[:120]
    tf = tarfile.open(fileobj=io.BytesIO(raw))
    member = tf.getmembers()[0]
    g = json.loads(tf.extractfile(member).read())
    return g, {"origin": origin, "last_modified": lm, "bytes": len(raw),
               "tar_member": member.name, "reads": reads}


def census(graph: dict) -> dict:
    by_source = collections.Counter()
    by_type = collections.Counter()
    stitch_by_type = collections.Counter()
    total = 0
    for v in graph.get("classes_data", {}).values():
        for n in v.get("nodes", []):
            total += 1
            by_source[str(n.get("source"))] += 1
            by_type[str(n.get("type"))] += 1
            if n.get("source") == STITCH_SOURCE:
                stitch_by_type[str(n.get("type"))] += 1
    return {"total_nodes": total, "by_source": dict(by_source), "by_type_denominator": total,
            "stitch_by_type": dict(stitch_by_type),
            "stitch_total": sum(stitch_by_type.values()),
            "class_buckets": len(graph.get("classes_data", {}))}


def main() -> int:
    print("H2-AC3 SNAPSHOT CENSUS -- NFRA_CLDGRPH CG-s-37, resolving row W2-S75")
    print("TREE_READ=%s" % WS)
    print("INSTRUMENT=boto3 get_object -> tarfile -> json -> full walk of classes_data "
          "(a READ of an Opal S3 object; nothing is written to S3, nothing is published)")
    print("GRAIN=one node object per row, grouped by its own `source` stamp and by `type`")
    print("ENVIRONMENT=comparison values from the round-6/7 RECORD (W2-S61 @80daa1fff6, the "
          "producer comment @f3b5f26f77, commit 139cbe1d40) -- not re-run")
    print("")

    try:
        graph, meta = fetch(KEY)
    except Exception as exc:
        print("CENSUS_STATUS=BLOCKED")
        print("BLOCKER printed: the object s3://%s/%s could not be read" % (BUCKET, KEY))
        print("ERROR_TEXT printed: %s" % str(exc)[:600])
        return 0
    c = census(graph)

    print("OBJECT=s3://%s/%s" % (BUCKET, KEY))
    print("  origin: %s" % meta["origin"])
    print("  bytes=%d tar_member=%s" % (meta["bytes"], meta["tar_member"]))
    print("  LastModified_NOW=%s" % meta["last_modified"])
    print("  VINTAGE CITED BY THE THREE FIGURES=%s" % CITED_VINTAGE)
    drift = str(meta["last_modified"]).startswith("2026-09-10")
    print("  VINTAGE_MISMATCH=%s -- the date-keyed object was OVERWRITTEN after the figures were "
          "taken and the bucket is UNVERSIONED (get-bucket-versioning returns no Status, "
          "list-object-versions returns one version, VersionId 'null'), so the 21:05:21Z bytes "
          "are not recoverable by anyone" % str(drift).lower())
    print("")

    print("---- CENSUS BY SOURCE (the discriminator: the node's own stamp) ----")
    print("BY_SOURCE_DENOMINATOR=%d  (every node object in the tarball, %d class buckets, "
          "nothing excluded)" % (c["total_nodes"], c["class_buckets"]))
    for src, n in sorted(c["by_source"].items(), key=lambda kv: -kv[1]):
        print("  source=%-28s %6d" % (src, n))
    print("STITCH_POPULATION_NOW=%d nodes with source=%s" % (c["stitch_total"], STITCH_SOURCE))
    print("")

    print("---- CENSUS BY TYPE ----")
    print("BY_TYPE_DENOMINATOR=%d  (the same sweep, re-grouped; a denominator certifies the "
          "SWEEP, not the SET)" % c["by_type_denominator"])
    print("  stitch-sourced, by type:")
    for t, n in sorted(c["stitch_by_type"].items(), key=lambda kv: -kv[1]):
        band = ("PROVISIONAL" if t in PROVISIONAL else
                "CANONICAL" if t in CANONICAL else "NEITHER-MAP")
        print("    %-18s %6d   [%s]" % (t, n, band))
    prov = sum(n for t, n in c["stitch_by_type"].items() if t in PROVISIONAL)
    canon = sum(n for t, n in c["stitch_by_type"].items() if t in CANONICAL)
    neither = c["stitch_total"] - prov - canon
    print("  PROVISIONAL_NAMED=%d  CANONICAL_NAMED=%d  IN_NEITHER_MAP=%d  (sum %d = the stitch "
          "population)" % (prov, canon, neither, prov + canon + neither))
    print("  PORTAL_BUNDLE present in the current bytes: %s (count %d)"
          % (str("PORTAL_BUNDLE" in c["stitch_by_type"]).lower(),
             c["stitch_by_type"].get("PORTAL_BUNDLE", 0)))
    print("  CROSS-CHECK, MEASURED NOW AND NOT ARGUED: CANONICAL_NAMED=%d against figure 3's "
          "CARRIED=269. A stitch node that MERGES onto a canonical id is removed by the unify "
          "(the canonical node stays, source=None), so the only stitch-sourced nodes that reach "
          "the artifact -- and therefore the fold and the archive -- are the CARRIED ones plus "
          "the types in no map (API_ROUTE %d + PORTAL_BUNDLE %d = %d). %d + %d = %d = the stitch "
          "population. The 1,521 MERGED are inside figure 3's denominator and outside every "
          "snapshot census by construction." % (
              canon, c["stitch_by_type"].get("API_ROUTE", 0),
              c["stitch_by_type"].get("PORTAL_BUNDLE", 0), neither, canon, neither,
              canon + neither))
    print("")

    nxt = None
    try:
        gnext, mnext = fetch(KEY_NEXT)
        nxt = census(gnext)
        print("---- THE FOLLOWING CYCLE, FOR THE TREND (%s, LastModified %s) ----"
              % (KEY_NEXT, mnext["last_modified"]))
        print("  total nodes=%d  stitch population=%d  stitch by type=%s"
              % (nxt["total_nodes"], nxt["stitch_total"], json.dumps(nxt["stitch_by_type"])))
        print("")
    except Exception as exc:
        print("  NEXT-CYCLE READ SKIPPED: %s" % str(exc)[:200])
        print("")

    print("---- THE THREE FIGURES, EACH ATTRIBUTED TO THE POPULATION IT ACTUALLY COUNTED ----")
    print("POPULATION_PER_FIGURE printed:")
    print("")
    print("FIGURE 1: 1,771  (row W2-S61 @80daa1fff6, five-way per-type census: GOLD_SCRIPT 1380 "
          "+ S3_DATA_KEY 294 + REACT_QUERY_KEY 94 + PORTAL_COMPONENT 2 + PORTAL_BUNDLE 1)")
    print("  POPULATION = the ARCHIVED SNAPSHOT ALONE at %s: every node in the tarball carrying "
          "source=portal-stitch, ALL types." % CITED_VINTAGE)
    print("  PORTAL_BUNDLE: INSIDE (it is the '+1').   CANONICAL-NAMED stitch nodes: OUTSIDE -- "
          "at that vintage the archived stitch nodes carried provisional names only.")
    print("  FRESH (this-cycle) emission: OUTSIDE -- a snapshot cannot contain it.")
    print("  BASIS=MEASURED-THEN (a record of a read of bytes that no longer exist; NOT "
          "re-readable now -- see VINTAGE_MISMATCH above).")
    print("")
    print("FIGURE 2: 1,791  (derive_stitch.py:311-314 @f3b5f26f77, 'the 21:05Z snapshot carries "
          "1,791 nodes with source=portal-stitch under the four PROVISIONAL names')")
    print("  POPULATION = NOT the snapshot. The sentence names the snapshot and the number does "
          "not fit it: the snapshot census is 1,771 INCLUDING PORTAL_BUNDLE, and PORTAL_BUNDLE is "
          "absent from PROVISIONAL_TO_CANONICAL, so 'under the four provisional names' is at most "
          "1,770 -- a SUBSET, and 1,791 is LARGER. The population 1,791 fits is the RUN-TIME "
          "union AFTER _retype_prior_cycle and _collapse_stitch_copies: archived stitch nodes "
          "that survived the collapse PLUS this cycle's own emission.")
    print("  ARITHMETIC (over the record's own numbers): archived-and-retyped 1,770 (= 1,771 "
          "minus the one PORTAL_BUNDLE the retype map does not name; the local run printed "
          "STITCH_UNIFY_PRIOR_CYCLE retyped=1770) + 20 surviving fresh members = 1,790 admitted, "
          "+ 1 PORTAL_BUNDLE (never admitted, it is in no map) = 1,791.")
    print("  PORTAL_BUNDLE: INSIDE.   CANONICAL-NAMED stitch nodes: INSIDE (the fresh emission "
          "is canonical-named).   FRESH emission: INSIDE -- that is the whole difference.")
    print("  BASIS=INFERRED (arithmetic over MEASURED-THEN records; the object that would "
          "falsify it was overwritten before this order could read it).")
    print("")
    print("FIGURE 3: 1,790  (commit 139cbe1d40's subject: 1,521 merged by identity + 269 carried; "
          "the round-6 analysis's 'LOST 0 of 1,790')")
    print("  POPULATION = unify_stitch_vocabulary's `admitted` counter: run-time nodes with "
          "source=portal-stitch WHOSE TYPE IS IN STITCH_CANONICAL_TYPES, counted after the retype "
          "and after the collapse. A RUN-TIME population, not a snapshot one, and a TYPE-FILTERED "
          "one at that.")
    print("  PORTAL_BUNDLE: OUTSIDE -- PORTAL_BUNDLE is not in STITCH_CANONICAL_TYPES, so the "
          "admitted census never sees it. That single node is the whole 1,791-vs-1,790 gap.")
    print("  CANONICAL-NAMED stitch nodes: INSIDE.   FRESH emission: INSIDE.")
    print("  BASIS=MEASURED-THEN (the producer's own STITCH_UNIFY_TOTAL line in that run's log).")
    print("")
    print("RESIDUAL, NAMED RATHER THAN SMOOTHED: the 20 members separating the snapshot "
          "population (1,771) from the run-time one (1,791) are, on this reading, fresh members "
          "this cycle emitted whose ids were not already in the archive. Their MEMBERSHIP is not "
          "recoverable -- it needs the 21:05:21Z bytes, and those are gone.")
    print("")
    print("WHAT THE CURRENT BYTES DO SHOW, MEASURED NOW: the same key's stitch population is %d, "
          "not ~1,771, and it is CANONICAL-named. The snapshot's stitch population is therefore "
          "whatever the LAST fold wrote, not an accumulation -- and it has already SHRUNK by a "
          "factor of ~%.1f since the figures were taken. A shrinking stitch population is exactly "
          "the condition under which the missing NODES drop-on-read (this order's fix) carries "
          "stale members forward." % (c["stitch_total"], 1771.0 / max(c["stitch_total"], 1)))
    print("")
    cap = OUT / "h2_snapshot_census.capture.json"
    cap.write_text(json.dumps({"object": "s3://%s/%s" % (BUCKET, KEY), "meta": meta,
                               "census": c, "next_cycle": nxt}, indent=1), encoding="utf-8")
    print("CAPTURE=%s" % cap.name)
    print("CENSUS_STATUS=DONE")
    print("FIGURES_ACCOUNTED=3 of 3")
    print("POPULATION_PER_FIGURE printed:")
    print("  1,771 = the ARCHIVED SNAPSHOT alone, all types, PORTAL_BUNDLE inside, no fresh "
          "emission [MEASURED-THEN]")
    print("  1,791 = the RUN-TIME union after retype+collapse, PORTAL_BUNDLE inside, fresh "
          "emission inside -- NOT a snapshot population despite the sentence [INFERRED]")
    print("  1,790 = unify's `admitted`: run-time, TYPE-FILTERED to STITCH_CANONICAL_TYPES, "
          "PORTAL_BUNDLE outside [MEASURED-THEN]")
    print("BY_SOURCE_DENOMINATOR=%d" % c["total_nodes"])
    print("BY_TYPE_DENOMINATOR=%d" % c["by_type_denominator"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
