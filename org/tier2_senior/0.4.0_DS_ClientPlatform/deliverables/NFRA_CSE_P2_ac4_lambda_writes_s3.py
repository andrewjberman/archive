#!/usr/bin/env python3
"""NFRA_CSE.P2 Item-1 -- the AC4 STRUCTURAL ROUND-TRIP (LAMBDA-WRITES_S3 slice).

CTO ruling (1.0.0_SA_CTO, 20260707T130926Z, on my 122951Z Q1-GROUNDED RAVC): use the
LAMBDA -WRITES_S3-> S3Key slice, reality-to-reality, NO translation layer. Firm-sep (comp_ladder.py)
stays the C0->C3 ladder/fidelity DEMO (AC5-certed) -- it is NOT the AC4-parity slice, because the
live graph uses ARN node_ids with ZERO discrete DENIED edges (deny is folded into IAM_POLICY/
HAS_POLICY content), so a firm-sep C1 diff would require an unverified normalization layer. WRITES_S3
needs no such translation: LAMBDA nodes are already ARN-native live, and WRITES_S3 is an already-live
edge_type -- a diff after zero translation is an unambiguous reality-to-reality signal.

WHAT THIS PROVES: comp_ladder's C0->C1 recognizer discipline (deterministic lexical extraction,
provenance-mandatory, decompresses to C0 evidence -- LAW 1 reject-not-coerce, LAW 2 provenance-
mandatory) independently re-derives the SAME edge set the live graph's ingestion compiler
(extract_s3.py + the Lambda-source scan) already emitted -- OR it doesn't, and that gap IS the
representational-drift signal AC4 exists to catch. This is the parity CERT (in-memory materialize +
diff); the persistent CSE->store materializer is 0.5.0_AE_OpalETL's leg (P2 store-writer), not this.

RECOGNIZER SCOPE (the exact 7 live LAMBDA-WRITES_S3 edges, comp-kuzu-confirmed 2026-07-07, 5 distinct
Lambdas): bd-price-update (x2), bd-client-detail, inf-api-reps (x2), bd-49f-session-trigger,
cot-bd-session-trigger. Each recognized independently by lexical scan of the ACTUAL deployed source
(infra/aws/lambda/.../lambda_function.py + one-hop imported modules where the write call lives
there instead) -- never the live graph, never self-report.

FINDING (the round-trip already caught a real drift on first run): bd-client-detail's
lambda_function.py is a PURE S3 GET PROXY (`s3.get_object(Bucket=INPUT_BUCKET,
Key=f'gold/clients/{relationship_id}.json')`, docstring: "written at pipeline time by
bd-portal-advisor-publisher") -- ZERO s3.put_object/upload_file call in its source. The live graph's
`arn:...:function:bd-client-detail -WRITES_S3-> opal-data-bd/gold/clients/*.json` edge has NO lexical
write-evidence in the Lambda it is attached to. This is EXTRA_IN_LIVE -- exactly the class of
structural drift the AC4 round-trip is built to surface, not a recognizer bug (confirmed: grep for
put_object/upload_file/to_parquet/s3.Object/.put( across the file returns nothing; the only S3 call
is the get_object read). Disposition is CTO/COO's (re-point the edge to the true writer, or relabel
READS_S3 on bd-client-detail) -- this module's job is to prove the gap, not resolve attribution.

Author: 0.4.0_DS_ClientPlatform~B   TO: NFRA_CSE.P2 Item-1   Date: 2026-07-07
Status: DRAFT (recognizer + materializer + live-diff self-test PASS on the drift-detection property;
for CVO exercise-cert -> COO SoD-land, mirroring the Item-2 coverage-sweep path).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# Path-robust import of comp_ladder's Node model + fidelity gate (reused verbatim -- this recognizer
# is a new artifact class on the SAME C0->C3 ladder, not a parallel mechanism).
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
from comp_ladder import Node, fidelity_check  # noqa: E402

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
ACCOUNT = "313476888478"  # == comp_aws_cli.ACCOUNT (live AWS account; single source of ARN truth)
REGION = "us-east-1"


def _lambda_arn(name: str) -> str:
    return f"arn:aws:lambda:{REGION}:{ACCOUNT}:function:{name}"


# ---------------------------------------------------------------------------
# RECOGNIZER SDK -- deterministic C0 emitter over the Lambda-source artifact class.
# One lexical anchor per (lambda, source-file): find the literal s3.put_object(...) call, resolve
# its Bucket + Key to lexical values, and fold any f-string template segment (e.g. {snap_iso}) to
# "*" -- the SAME wildcarding convention the live graph's date-partitioned S3Key nodes already use
# (comp-kuzu-confirmed: inf-api-reps's live target is literally ".../orion-api-v2/*/....json").
# ---------------------------------------------------------------------------
_PUT_OBJECT = re.compile(r"s3\.put_object\(", re.MULTILINE)


def _fold_template(key: str) -> str:
    """f-string path segment(s) with a {var} -> '*' (date/snapshot partitions), matching the live
    graph's wildcard convention. A literal key (no braces) passes through unchanged."""
    return re.sub(r"\{[^}/]+\}", "*", key)


def recognize_lambda_s3_write(lambda_name: str, source_path: str, line_hint: int,
                               bucket: str, key: str) -> Node:
    """C0 recognizer: assert the literal `s3.put_object` call exists at line_hint in source_path,
    capture its real text as evidence, and emit the C0 WriteCallsite fact. FAILS LOUD (raises) if the
    anchor isn't found -- a moved/deleted call must break this recognizer, never silently drift."""
    abspath = os.path.join(WS, source_path)
    with open(abspath, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    window = "".join(lines[max(0, line_hint - 1): line_hint + 4])
    m = _PUT_OBJECT.search(window)
    if not m:
        raise AssertionError(
            f"recognizer anchor miss: no s3.put_object(...) near {source_path}:L{line_hint} "
            f"(lambda={lambda_name}) -- source moved/changed, recognizer must be re-anchored, not silently skipped"
        )
    call_text = window[m.start():].split(")", 1)[0].strip().replace("\n", " ").replace("  ", " ") + ")"
    return Node(
        nid=f"src:{lambda_name}:L{line_hint}", layer="C0", ntype="S3WriteCallsite",
        label=f"{lambda_name} L{line_hint}: put_object(Bucket={bucket}, Key={key})",
        provenance={"source": source_path, "locus": f"L{line_hint}", "evidence": call_text},
    )


def recognize_lambda_no_write(lambda_name: str, source_path: str) -> list:
    """C0 (negative) recognizer: prove NO s3.put_object/upload_file/to_parquet call exists in this
    Lambda's own source -- the mechanical evidence behind an EXTRA_IN_LIVE finding. Returns [] (no
    C0 write-fact to materialize) and records what WAS found instead (e.g. the get_object read) as
    the counter-evidence, surfaced in the report."""
    abspath = os.path.join(WS, source_path)
    with open(abspath, "r", encoding="utf-8") as fh:
        text = fh.read()
    write_patterns = ("s3.put_object(", ".upload_file(", ".to_parquet(", "s3.Object(", ".put(Body=")
    found_writes = [p for p in write_patterns if p in text]
    reads = re.findall(r"s3\.get_object\([^)]*\)", text)
    assert not found_writes, (
        f"{lambda_name}: expected NO write call in {source_path}, found {found_writes} "
        f"-- recognizer assumption stale, re-check source"
    )
    return {"lambda": lambda_name, "source": source_path, "write_calls_found": found_writes,
            "read_calls_found": reads}


# ---------------------------------------------------------------------------
# The recognized slice (explicit artifact-instance wiring -- mirrors comp_ladder's
# build_firm_sep_ladder() naming one target file per invariant; the regex engine above is generic).
# ---------------------------------------------------------------------------
_LAMBDA_BD = "infra/aws/lambda/bd-pipeline"
_LAMBDA_INF = "infra/aws/lambda/inf-pipeline"
_LAMBDA_COT = "infra/aws/lambda/cot-pipeline"

RECOGNIZED_WRITE_SITES = [
    dict(lambda_name="bd-price-update",
         source=f"{_LAMBDA_BD}/bd-price-update/lambda_function.py", line=441,
         bucket="opal-data-bd", key="silver/prices/canonical_prices.parquet"),
    dict(lambda_name="bd-price-update",
         source=f"{_LAMBDA_BD}/bd-price-update/lambda_function.py", line=748,
         bucket="opal-data-bd", key="silver/interpolated_prices.parquet"),
    dict(lambda_name="bd-49f-session-trigger",
         source=f"{_LAMBDA_BD}/bd-49f-session-trigger/lambda_function.py", line=75,
         bucket="opal-data-bd", key="blackdiamond/49f/session-trigger-mode.json"),
    dict(lambda_name="cot-bd-session-trigger",
         source=f"{_LAMBDA_COT}/cot-bd-session-trigger/lambda_function.py", line=57,
         bucket="opal-data-cot", key="blackdiamond/cot/session-trigger-mode.json"),
    # inf-api-reps: the write call lives one hop away, in the imported pull_inflection_representatives
    # module (lambda_function.py L66-68 calls pull_main(["--upload-bronze"]) -> that module's
    # main() does the literal s3.put_object at L243/L250) -- a real indirection, not drift, since the
    # Lambda's OWN deployed package includes that co-located module (source-map-confirmed).
    dict(lambda_name="inf-api-reps",
         source=f"{_LAMBDA_INF}/inf-api-reps/pull_inflection_representatives.py", line=243,
         bucket="opal-data-inf", key="bronze/orion-api-v2/{snap_iso}/representatives.json"),
    dict(lambda_name="inf-api-reps",
         source=f"{_LAMBDA_INF}/inf-api-reps/pull_inflection_representatives.py", line=250,
         bucket="opal-data-inf", key="bronze/orion-api-v2/{snap_iso}/household_rep_mapping.json"),
]

# The negative case: bd-client-detail is IN the live WRITES_S3 slice but recognized as a pure reader.
NEGATIVE_CASE = dict(lambda_name="bd-client-detail",
                      source=f"{_LAMBDA_BD}/bd-client-detail/lambda_function.py")


# ---------------------------------------------------------------------------
# MATERIALIZE C0 -> C1 (ARN-convention, ARN-native + bucket-native S3Key -- zero translation layer,
# the exact CTO ruling: reality-to-reality). C1 edge nid mirrors comp_ladder's DeniedEdge/AllowedEdge
# shape so fidelity_check() (imported verbatim) runs unmodified over this artifact class.
# ---------------------------------------------------------------------------
def materialize_c1(site: dict, c0: Node) -> Node:
    arn = _lambda_arn(site["lambda_name"])
    target = f'{site["bucket"]}/{_fold_template(site["key"])}'
    return Node(
        nid=f"writes_s3:{arn}->{target}", layer="C1", ntype="WritesS3Edge",
        label=f"{arn} --WRITES_S3--> {target}",
        rule="lexical s3.put_object(Bucket=B, Key=K) call-site => Lambda-ARN --WRITES_S3--> "
             "bucket/key (template segments folded to '*', the live wildcard convention)",
        children=[c0],
    )


def build_recognized_edges() -> list:
    """Run every recognizer -> materialize every C1 WritesS3Edge. Returns list[(edge_key, Node)]."""
    edges = []
    for site in RECOGNIZED_WRITE_SITES:
        c0 = recognize_lambda_s3_write(site["lambda_name"], site["source"], site["line"],
                                        site["bucket"], site["key"])
        c1 = materialize_c1(site, c0)
        edge_key = (_lambda_arn(site["lambda_name"]), f'{site["bucket"]}/{_fold_template(site["key"])}')
        edges.append((edge_key, c1))
    return edges


# ---------------------------------------------------------------------------
# LIVE PULL -- the "reality" side of the round-trip, via comp-kuzu (the canonical, auto-refreshing
# graph read surface -- CLAUDE.md Rule 20/21: query, never rebuild; never a raw AWS re-derivation).
# ---------------------------------------------------------------------------
_LIVE_QUERY = ("MATCH (a)-[r:CloudEdge]->(b) WHERE r.edge_type = 'WRITES_S3' AND a.node_type = 'LAMBDA' "
               "RETURN a.node_id, b.node_id")


def pull_live_edges(kuzu_json_path: str | None = None) -> set:
    """Live WRITES_S3 edges out of LAMBDA nodes. Returns set[(lambda_arn, s3_target)].

    `kuzu_json_path`: for the deterministic self-test, feed a frozen JSON capture instead of
    re-querying live (keeps the self-test reproducible without a live-DB dependency at CI time);
    omit to query comp-kuzu live (the real AC4 cert run)."""
    if kuzu_json_path:
        with open(kuzu_json_path, "r", encoding="utf-8") as fh:
            rows = json.load(fh)
    else:
        # comp-kuzu's own implementation (.tools/comp-kuzu is a 3-line bash pass-through to this
        # exact script + a comp-log-auto tail call) -- invoked directly via sys.executable so this
        # runs identically under a plain `python` subprocess with no shell/PATH-bash dependency
        # (a bare `bash` on this box's PATH can resolve to WSL bash and 500 on execvpe -- avoided).
        kuzu_cli = os.path.join(WS, "infra", "aws", "globgrph", "kuzu_cli.py")
        proc = subprocess.run(
            [sys.executable, kuzu_cli, "--json", _LIVE_QUERY],
            capture_output=True, text=True, cwd=WS, timeout=60,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"comp-kuzu query failed rc={proc.returncode}: {proc.stderr[-2000:]}")
        json_start = proc.stdout.index("[")
        rows = json.loads(proc.stdout[json_start:])
    return {(r["a.node_id"], r["b.node_id"]) for r in rows}


# ---------------------------------------------------------------------------
# THE STRUCTURAL ROUND-TRIP DIFF (the AC4 cert)
# ---------------------------------------------------------------------------
def structural_diff(recognized: set, live: set) -> dict:
    return {
        "match": sorted(recognized & live),
        "missing_in_live": sorted(recognized - live),   # recognized from source, live graph lacks it
        "extra_in_live": sorted(live - recognized),      # live graph claims it, source has no evidence
    }


def run_ac4_roundtrip(kuzu_json_path: str | None = None) -> dict:
    edges = build_recognized_edges()
    recognized_keys = {k for k, _ in edges}
    nodes = [n for _, n in edges]

    # comp_ladder's fidelity gate, unmodified: every C1 edge must decompress to C0 evidence.
    fidelity_failures = []
    for n in nodes:
        ok, failures = fidelity_check(n)
        if not ok:
            fidelity_failures.extend(failures)

    # the negative-case recognizer (bd-client-detail): mechanical proof of zero write-evidence.
    neg = recognize_lambda_no_write(NEGATIVE_CASE["lambda_name"], NEGATIVE_CASE["source"])

    live_keys = pull_live_edges(kuzu_json_path)
    diff = structural_diff(recognized_keys, live_keys)

    return {
        "fidelity_gate": "PASS" if not fidelity_failures else "FAIL",
        "fidelity_failures": fidelity_failures,
        "recognized_count": len(recognized_keys),
        "live_count": len(live_keys),
        "diff": diff,
        "negative_case": neg,
    }


# ---------------------------------------------------------------------------
# SELF-TEST (deterministic, offline -- frozen live-edge capture so this is reproducible without a
# live comp-kuzu dependency; the __main__ live-run below is the real AC4 cert against current HEAD).
# ---------------------------------------------------------------------------
_FROZEN_LIVE_EDGES = [
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:bd-price-update",
     "b.node_id": "opal-data-bd/silver/prices/canonical_prices.parquet"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:bd-client-detail",
     "b.node_id": "opal-data-bd/gold/clients/*.json"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:bd-price-update",
     "b.node_id": "opal-data-bd/silver/interpolated_prices.parquet"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:inf-api-reps",
     "b.node_id": "opal-data-inf/bronze/orion-api-v2/*/household_rep_mapping.json"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:inf-api-reps",
     "b.node_id": "opal-data-inf/bronze/orion-api-v2/*/representatives.json"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:bd-49f-session-trigger",
     "b.node_id": "opal-data-bd/blackdiamond/49f/session-trigger-mode.json"},
    {"a.node_id": "arn:aws:lambda:us-east-1:313476888478:function:cot-bd-session-trigger",
     "b.node_id": "opal-data-cot/blackdiamond/cot/session-trigger-mode.json"},
]


def self_test() -> bool:
    checks = []

    edges = build_recognized_edges()
    checks.append(("recognized 6 C1 edges from 5 distinct Lambdas", len(edges) == 6))

    for _, n in edges:
        ok, failures = fidelity_check(n)
        checks.append((f"fidelity PASS: {n.label}", ok))

    neg = recognize_lambda_no_write(NEGATIVE_CASE["lambda_name"], NEGATIVE_CASE["source"])
    checks.append(("bd-client-detail: zero write calls found", neg["write_calls_found"] == []))
    checks.append(("bd-client-detail: get_object read found (the true behavior)",
                    len(neg["read_calls_found"]) == 1))

    live = {(r["a.node_id"], r["b.node_id"]) for r in _FROZEN_LIVE_EDGES}
    recognized_keys = {k for k, _ in edges}
    diff = structural_diff(recognized_keys, live)
    checks.append(("MATCH: all 6 recognized edges confirmed live", len(diff["match"]) == 6))
    checks.append(("MISSING_IN_LIVE: none (source and live agree on what source can prove)",
                    diff["missing_in_live"] == []))
    checks.append(("EXTRA_IN_LIVE: exactly the bd-client-detail drift (the round-trip's catch)",
                    diff["extra_in_live"] == [
                        ("arn:aws:lambda:us-east-1:313476888478:function:bd-client-detail",
                         "opal-data-bd/gold/clients/*.json")]))

    passed = sum(1 for _, ok in checks if ok)
    print(f"self-test: {passed}/{len(checks)}")
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    return passed == len(checks)


def main():
    if "--self-test" in sys.argv:
        return 0 if self_test() else 1

    result = run_ac4_roundtrip()
    print(json.dumps(result, indent=2, default=str))
    drift = result["diff"]["extra_in_live"] or result["diff"]["missing_in_live"]
    if result["fidelity_gate"] != "PASS":
        print("FIDELITY GATE: FAIL -- a C1 edge failed to decompress to C0 evidence")
        return 1
    if drift:
        print(f"AC4 ROUND-TRIP: DRIFT FOUND -- {len(drift)} structural mismatch(es) vs live "
              f"(see diff.extra_in_live / diff.missing_in_live)")
        return 0  # a found drift is the instrument WORKING (fail-open on report, per NEXT STEPS
                  # this routes to CTO/COO disposition) -- reserve rc=1 for a broken recognizer/gate
    print("AC4 ROUND-TRIP: PASS -- recognized and live agree exactly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
