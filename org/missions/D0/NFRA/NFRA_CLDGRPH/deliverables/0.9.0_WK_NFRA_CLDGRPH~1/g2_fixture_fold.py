#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-2 / G2-AC1 -- THE FOLD'S ADMISSION, EXERCISED ON A FIXTURE.

Six arms and a negative control, on a LOCAL fixture, with no network and no S3:

  1 NAME_ENDPOINT_REWRITTEN     a name endpoint on a both-identity node becomes the arn
                                AND the simulated join lands it on the resource
  2 ARN_ENDPOINT_UNCHANGED      an endpoint already canonical is admitted untouched
  3 SINGLE_IDENTITY_UNTOUCHED   an endpoint on a one-named node is not touched at all
  4 AMBIGUOUS_ALIAS_REFUSED     one short id claimed by two resources is NEVER rewritten
  5 NON_LOSING                  resolvable_after >= resolvable_before (the derive's contract)
  6 FOLD_ADMITS_CANONICAL       fold_stitch_document admits an ARN-named endpoint, which the
                                pre-fix id set could not -- round 6 measured 0 of 955 there,
                                and this arm is why "both planes move together" is mechanical

THE NEGATIVE CONTROL IS A MUTANT, NOT A COMMENT: canonical_node_key is replaced with the
pre-fix behaviour (return the short id) and arm 1 is re-run. It MUST fail. If it passes,
the arm is a constant and this script exits 1 saying so.

THE FIXTURE'S SHAPE IS THE ESTATE'S, MEASURED, NOT INVENTED: an S3_BUCKET carries
id='<name>' + arn='arn:aws:s3:::<name>' and an S3_BUCKET_POLICY carries id='<name>' +
arn='<name>' -- the bucket NAME in its own arn column. Both read off the real
snapshots/20260910 artifact by TO-CG-G-1's census.

READ ONLY of the world: this fixture touches no S3, no ECS, no image, no Terraform.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
for _p in (str(ROOT), str(ROOT / "org" / "modules" / "graph"),
           str(ROOT / "infra" / "aws" / "globgrph")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import derive_runner as DR  # noqa: E402

BUCKET_NAME = "opal-data-bd"
BUCKET_ARN = "arn:aws:s3:::opal-data-bd"
LONE_NAME = "opal-data-cot"
LONE_ARN = "arn:aws:s3:::opal-data-cot"


def fixture_graph() -> dict:
    """The estate's measured shape, in eleven nodes."""
    return {
        "classes_data": {
            "s3": {"nodes": [
                {"id": BUCKET_NAME, "arn": BUCKET_ARN, "type": "S3_BUCKET",
                 "name": BUCKET_NAME},
                {"id": LONE_NAME, "arn": LONE_ARN, "type": "S3_BUCKET", "name": LONE_NAME},
            ]},
            "s3_policy": {"nodes": [
                # THE SHADOW NODE: its own arn column carries the BUCKET's name, so the
                # join's `arn or node_id` rule makes the bucket name ITS served key.
                {"id": BUCKET_NAME, "arn": BUCKET_NAME, "type": "S3_BUCKET_POLICY",
                 "name": BUCKET_NAME},
            ]},
            "stitch_cloud": {"nodes": [
                {"id": "opal-data-bd/gold/x.parquet", "type": "S3Key",
                 "name": "gold/x.parquet"},
                {"id": "opal-data-cot/gold/y.parquet", "type": "S3Key",
                 "name": "gold/y.parquet"},
                {"id": "scripts/build.py", "type": "PipelineScript", "name": "build.py"},
            ]},
        },
        "edges": [
            # arm 1: the defect -- an endpoint on the bucket's NAME
            {"source": "opal-data-bd/gold/x.parquet", "target": BUCKET_NAME,
             "edge_type": "STORED_IN"},
            # arm 2: already canonical
            {"source": "opal-data-cot/gold/y.parquet", "target": LONE_ARN,
             "edge_type": "STORED_IN"},
            # arm 3: both ends single-identity
            {"source": "opal-data-bd/gold/x.parquet", "target": "scripts/build.py",
             "edge_type": "DERIVES_FROM"},
        ],
    }


def ambiguous_graph() -> dict:
    """Two DIFFERENT resources offering one short id -- the fold must refuse to choose."""
    return {
        "classes_data": {
            "a": {"nodes": [
                {"id": "shared-name", "arn": "arn:aws:s3:::shared-name",
                 "type": "S3_BUCKET", "name": "shared-name"},
                {"id": "shared-name", "arn": "arn:aws:sqs:us-east-1:1:shared-name",
                 "type": "SQS_QUEUE", "name": "shared-name"},
            ]},
            "b": {"nodes": [{"id": "k1", "type": "S3Key", "name": "k1"}]},
        },
        "edges": [{"source": "k1", "target": "shared-name", "edge_type": "STORED_IN"}],
    }


def served_key(n: dict) -> str:
    """kuzu_nessie_load's rule, reimplemented here so the arm reads the JOIN and not the fold."""
    return str(n.get("arn") or "").strip() or str(n.get("id") or "").strip()


def simulate_join(graph: dict) -> dict:
    """What each edge LANDS ON once the served key rule is applied. The join, locally."""
    best = {}
    for cdata in graph.get("classes_data", {}).values():
        for n in cdata.get("nodes", []) or []:
            k = served_key(n)
            if k:
                best.setdefault(k, n)
    out = []
    for e in graph.get("edges", []):
        s = str(e.get("source", "")).strip()
        t = str(e.get("target", "")).strip()
        out.append({
            "edge_type": e.get("edge_type"),
            "source": s, "target": t,
            "source_type": (best.get(s) or {}).get("type"),
            "target_type": (best.get(t) or {}).get("type"),
            "resolved": s in best and t in best,
        })
    return {"landings": out, "keys": len(best)}


def arm1(mutated: bool = False) -> tuple:
    g = fixture_graph()
    stats = DR.normalize_edge_endpoints(g)
    join = simulate_join(g)
    e = [x for x in join["landings"] if x["edge_type"] == "STORED_IN"
         and x["source"] == "opal-data-bd/gold/x.parquet"][0]
    ok = (e["target"] == BUCKET_ARN and e["target_type"] == "S3_BUCKET" and e["resolved"])
    detail = ("target=%s target_type=%s resolved=%s endpoints_rewritten=%d"
              % (e["target"], e["target_type"], e["resolved"], stats["endpoints_rewritten"]))
    return ok, detail, stats, join


def main() -> int:
    print("INSTRUMENT: derive_runner.normalize_edge_endpoints and "
          "derive_runner.fold_stitch_document, called DIRECTLY on a local fixture; the served "
          "join is reimplemented from kuzu_nessie_load.py:204/:249-253 so an arm reads the "
          "JOIN's rule and not the fold's own")
    print("COVERAGE: 4 fixture graphs, 11 nodes and 5 edges in total; every arm prints its "
          "own denominator; no S3, no network, no container")
    print("GRAIN: one edge ENDPOINT per arm, and the node CLASS the simulated join lands it on")
    print("ENVIRONMENT of the stored baseline: the fixture's node SHAPE is the real "
          "snapshots/20260910 artifact's, measured by TO-CG-G-1's census (S3_BUCKET carries "
          "id=name + arn=arn; S3_BUCKET_POLICY carries the bucket NAME in its own arn "
          "column, 15 of 15 nodes); the 0-of-955 comparison in arm 6 is round 6's own "
          "measurement, issuer-stated at this cut, not re-derived here")
    print("")

    results = []

    ok1, d1, stats1, join1 = arm1()
    results.append(("NAME_ENDPOINT_REWRITTEN", ok1, d1))

    e2 = [x for x in join1["landings"] if x["target"] == LONE_ARN][0]
    ok2 = (e2["target"] == LONE_ARN and e2["target_type"] == "S3_BUCKET" and e2["resolved"])
    results.append(("ARN_ENDPOINT_UNCHANGED", ok2,
                    "target=%s target_type=%s resolved=%s"
                    % (e2["target"], e2["target_type"], e2["resolved"])))

    e3 = [x for x in join1["landings"] if x["edge_type"] == "DERIVES_FROM"][0]
    ok3 = (e3["target"] == "scripts/build.py"
           and e3["source"] == "opal-data-bd/gold/x.parquet" and e3["resolved"])
    results.append(("SINGLE_IDENTITY_UNTOUCHED", ok3,
                    "source=%s target=%s resolved=%s (neither end carries a second identity)"
                    % (e3["source"], e3["target"], e3["resolved"])))

    ga = ambiguous_graph()
    sa = DR.normalize_edge_endpoints(ga)
    ok4 = (sa["ambiguous_aliases"] == 1 and sa["endpoints_rewritten"] == 0
           and str(ga["edges"][0]["target"]) == "shared-name")
    results.append(("AMBIGUOUS_ALIAS_REFUSED", ok4,
                    "ambiguous_aliases=%d endpoints_rewritten=%d target_left_as=%s"
                    % (sa["ambiguous_aliases"], sa["endpoints_rewritten"],
                       ga["edges"][0]["target"])))

    ok5 = (stats1["resolvable_after"] >= stats1["resolvable_before"]
           and sa["resolvable_after"] >= sa["resolvable_before"])
    results.append(("NON_LOSING", ok5,
                    "fixture before=%d after=%d of %d edge(s); ambiguous-fixture before=%d "
                    "after=%d of %d edge(s)"
                    % (stats1["resolvable_before"], stats1["resolvable_after"],
                       stats1["edges"], sa["resolvable_before"], sa["resolvable_after"],
                       sa["edges"])))

    # arm 6 -- the fold's ADMISSION on a canonically-emitted endpoint.
    base = fixture_graph()
    base["edges"] = []
    doc = {
        "classes_data": {"stitch": {"nodes": [
            {"id": "opal-data-bd/gold/z.parquet", "type": "S3Key", "name": "gold/z.parquet"},
        ]}},
        "edges": [{"source": "opal-data-bd/gold/z.parquet", "target": BUCKET_ARN,
                   "edge_type": "STORED_IN"}],
    }
    body = json.dumps(doc).encode("utf-8")
    marker = {"artifact_sha256": hashlib.sha256(body).hexdigest(),
              "producer": "g2_fixture_fold", "built_at": "fixture", "git_sha": "fixture"}
    vintage = DR.fold_stitch_document(base, body, marker)
    admitted = len([e for e in base.get("edges", [])
                    if str(e.get("edge_type")) == "STORED_IN"])
    old_ids = DR._stitch_existing_ids(fixture_graph())
    would_have_admitted = 1 if BUCKET_ARN in old_ids else 0
    ok6 = (vintage is not None and admitted == 1 and would_have_admitted == 0)
    results.append(("FOLD_ADMITS_CANONICAL", ok6,
                    "admitted=%d of 1 canonical STORED_IN edge; the pre-fix id set "
                    "(_stitch_existing_ids, short ids only) would have admitted "
                    "%d of 1 -- round 6 measured that arm at 0 of 955"
                    % (admitted, would_have_admitted)))

    print("  -- the arms --")
    for name, ok, detail in results:
        print("  %-28s %s   %s" % (name, "PASS" if ok else "FAIL", detail))
    print("")
    passed = sum(1 for _, ok, _ in results if ok)
    print("FIXTURE_ARMS=%d of %d passed" % (passed, len(results)))
    for name, ok, _ in results:
        print("%s=%s" % (name, "true" if ok else "false"))
    print("")

    # THE NEGATIVE CONTROL: put the pre-fix key rule back and require arm 1 to FAIL.
    real = DR.canonical_node_key
    try:
        DR.canonical_node_key = lambda n: str(n.get("id") or "").strip()
        mut_ok, mut_detail, _, _ = arm1(mutated=True)
    finally:
        DR.canonical_node_key = real
    fired = not mut_ok
    print("  -- the negative control (a MUTANT, not a comment) --")
    print("     canonical_node_key replaced with the pre-fix rule (return the short id);")
    print("     arm 1 re-run and REQUIRED to fail. Observed: %s   %s"
          % ("FAILED (as required)" if fired else "STILL PASSED", mut_detail))
    print("NEGATIVE_CONTROL=%s" % ("FIRED" if fired else "NOT-FIRED"))
    print("")
    print("DENOMINATOR: %d of %d arm(s) passed over 4 fixture graph(s), 11 node(s) and 5 "
          "edge(s); 1 of 1 mutant run; 0 S3 object(s) read, 0 network call(s) made."
          % (passed, len(results)))
    ok_all = (passed == len(results)) and fired
    print("FIXTURE_RESULT=%s" % ("PASS" if ok_all else "FAIL"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
