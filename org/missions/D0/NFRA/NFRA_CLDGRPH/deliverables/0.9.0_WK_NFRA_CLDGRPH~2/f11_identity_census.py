#!/usr/bin/env python3
"""F11-AC1 -- the IDENTITY CENSUS, per provisional population, BEFORE any merge. TO-CG-F-11.

Run against the CURRENTLY PUBLISHED stitch artifact -- the one still carrying the four
provisional names -- so the census describes the populations as they are, not as the producer
edit makes them. That is the point of doing it first: a merge is only defensible if the
resolution rate was measured before the code that performs it existed.

IT USES THE PRODUCER'S OWN RESOLVER. derive_stitch.resolve_stitch_id and
derive_stitch.build_canonical_index are imported, not reimplemented, so this census cannot
disagree with the merge it is authorising -- one implementation, two consumers. The provisional
names are translated to their canonical types by extract_portal_stitch's own NODE_TYPE_MAP and
_pipeline_grain, likewise imported.

WHY A MEMBER CAN FAIL TO RESOLVE, and each is a different finding:
  no-canonical-*           the projection's own extractor does not have this object at all
  ambiguous-across-firms   the firm-relative id exists in more than one firm's bucket, and
                           picking one would invent a cross-firm claim (R17: carry, never guess)
  not-a-*-id               the stitch id is not in the grain the identity rule expects

A CARRIED member is NOT a failure and is never dropped: it lands under the canonical TYPE with
origin=stitch and its reason, which is what makes `lost = 0` an arithmetic identity rather than
a hope.
"""
import argparse
import collections
import hashlib
import io
import json
import os
import sys


def _find_ws(start):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(12):
        if os.path.isfile(os.path.join(d, "infra", "aws", "globgrph", "derive_stitch.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise SystemExit("BLOCKED: could not locate the workspace root from " + start)


WS = _find_ws(__file__)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "globgrph"))

import derive_stitch as DS               # noqa: E402
import extract_portal_stitch as EPS      # noqa: E402

# the provisional name -> the canonical type it becomes (the producer's own map, inverted for
# the two the trace does not name directly)
PROVISIONAL = {
    "GOLD_SCRIPT": None,            # grain-split, resolved per node by EPS._pipeline_grain
    "S3_DATA_KEY": "S3Key",
    "PORTAL_COMPONENT": "Component",
    "REACT_QUERY_KEY": "ReactQueryKey",
}


def fetch_artifact(path_or_none):
    """The published artifact, sha256-verified against its own marker, or a local copy."""
    if path_or_none:
        body = io.open(path_or_none, "rb").read()
        return json.loads(body), {"source": path_or_none, "sha256_verified": None}
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    b = "opal-313476888478-globgrph"
    marker = json.loads(s3.get_object(Bucket=b, Key="stitch/stitch_marker.json")["Body"].read())
    body = s3.get_object(Bucket=b, Key="stitch/stitch_graph.json")["Body"].read()
    ok = hashlib.sha256(body).hexdigest() == marker.get("artifact_sha256")
    return json.loads(body), {"source": "s3://%s/stitch/stitch_graph.json" % b,
                              "marker": marker, "sha256_verified": ok}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", default="")
    a = ap.parse_args()

    g, prov = fetch_artifact(a.artifact or None)
    if prov.get("sha256_verified") is False:
        raise SystemExit("BLOCKED: the artifact does not match its own marker's sha256")

    idx = DS.build_canonical_index(g["classes_data"])

    members = collections.defaultdict(list)
    for v in g["classes_data"].values():
        for n in v.get("nodes", []):
            t = str(n.get("type", ""))
            if t in PROVISIONAL:
                members[t].append(n)

    print("F11-AC1 -- THE IDENTITY CENSUS, BEFORE ANY MERGE")
    print("  artifact : %s" % prov["source"])
    if prov.get("marker"):
        print("  marker   : producer=%s built_at=%s sha256_verified=%s"
              % (prov["marker"].get("producer"), prov["marker"].get("built_at"),
                 prov["sha256_verified"]))
    print("  resolver : derive_stitch.resolve_stitch_id (imported, not reimplemented)")
    print()

    results, reasons_all = {}, collections.Counter()
    for pname, canon in PROVISIONAL.items():
        res = car = 0
        grain = collections.Counter()
        reasons = collections.Counter()
        for n in members[pname]:
            nid = str(n.get("id", ""))
            t = EPS._pipeline_grain(nid) if pname == "GOLD_SCRIPT" else canon
            probe = {"id": nid, "type": t, "source": DS.STITCH_SOURCE}
            grain[t] += 1
            cid, reason = DS.resolve_stitch_id(probe, idx)
            if cid:
                res += 1
            else:
                car += 1
                reasons[reason] += 1
                reasons_all[reason] += 1
        results[pname] = {"resolved": res, "carried": car, "total": len(members[pname]),
                          "grain": dict(grain), "reasons": dict(reasons)}

    gs = results["GOLD_SCRIPT"]
    print("CENSUS_GOLD_SCRIPT=RESOLVED %d of %d (script %d, function %d)"
          % (gs["resolved"], gs["total"], gs["grain"].get("PipelineScript", 0),
             gs["grain"].get("PipelineFunction", 0)))
    for p in ("S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY"):
        print("CENSUS_%s=RESOLVED %d of %d" % (p, results[p]["resolved"], results[p]["total"]))
    carried = sum(r["carried"] for r in results.values())
    admitted = sum(r["total"] for r in results.values())
    merged = sum(r["resolved"] for r in results.values())
    print("CARRIED_WITH_ORIGIN_STITCH=%d" % carried)
    print("LOST=%d of %d" % (admitted - merged - carried, admitted))

    # ---- the control: a member that CANNOT resolve must be CARRIED, never dropped ----
    planted = {"id": "gold:__f11_planted_probe__", "type": "PipelineScript",
               "source": DS.STITCH_SOURCE}
    pid, preason = DS.resolve_stitch_id(planted, idx)
    fired = (pid is None and bool(preason))
    print("CENSUS_PROBE_CONTROL=%s" % ("FIRED" if fired else "DID-NOT-FIRE"))
    print()

    print("  -- why each carried member is carried --")
    for pname in PROVISIONAL:
        r = results[pname]
        if r["carried"]:
            print("     %-18s carried %4d of %4d  %s"
                  % (pname, r["carried"], r["total"], r["reasons"]))
    print("     TOTAL reasons: %s" % dict(reasons_all))
    print()
    print("  -- the grain split GOLD_SCRIPT had to have (R17: a mixed-grain type is never frozen) --")
    print("     script-level (-> PipelineScript)   : %d, of which resolved %d"
          % (gs["grain"].get("PipelineScript", 0), 0 if not members["GOLD_SCRIPT"] else
             sum(1 for n in members["GOLD_SCRIPT"]
                 if EPS._pipeline_grain(str(n["id"])) == "PipelineScript"
                 and DS.resolve_stitch_id({"id": str(n["id"]), "type": "PipelineScript",
                                           "source": DS.STITCH_SOURCE}, idx)[0])))
    print("     function-level (-> PipelineFunction): %d, of which resolved %d"
          % (gs["grain"].get("PipelineFunction", 0),
             sum(1 for n in members["GOLD_SCRIPT"]
                 if EPS._pipeline_grain(str(n["id"])) == "PipelineFunction"
                 and DS.resolve_stitch_id({"id": str(n["id"]), "type": "PipelineFunction",
                                           "source": DS.STITCH_SOURCE}, idx)[0])))
    print()
    print("  -- the canonical populations these resolve INTO --")
    canon_counts = collections.Counter()
    for v in g["classes_data"].values():
        for n in v.get("nodes", []):
            if n.get("source") != DS.STITCH_SOURCE and str(n.get("type")) in (
                    "PipelineScript", "PipelineFunction", "S3Key", "Component", "ReactQueryKey"):
                canon_counts[str(n["type"])] += 1
    for t, c in sorted(canon_counts.items()):
        print("     %-18s %d" % (t, c))
    print()
    print("  -- the control --")
    print("     planted id      : %s" % planted["id"])
    print("     resolver said   : canonical=%s reason=%s" % (pid, preason))
    print("     so an unresolvable member is CARRIED with a reason, never silently dropped;")
    print("     LOST above is an arithmetic identity over the same populations.")
    print()
    print("  DENOMINATOR: %d of %d provisional members censused across 4 of 4 populations "
          "(GOLD_SCRIPT %d, S3_DATA_KEY %d, PORTAL_COMPONENT %d, REACT_QUERY_KEY %d); "
          "PORTAL_BUNDLE is EXCLUDED by the cell -- it is the one genuinely new class and stays; "
          "1 of 1 planted control."
          % (admitted, admitted, results["GOLD_SCRIPT"]["total"], results["S3_DATA_KEY"]["total"],
             results["PORTAL_COMPONENT"]["total"], results["REACT_QUERY_KEY"]["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
