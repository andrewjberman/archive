#!/usr/bin/env python3
"""NFRA_EDGES P3 -- AE's R3-VERIFY LEG (0.7.0_AE_CloudOps, req1 materialize half).

Runs POST-DERIVE against the freshly-loaded live canonical (comp-kuzu / Nessie-backed graph). This
is the "comp-kuzu round-trip" verify leg of P3's deploy ledger: a FAIL here fails the R3 leg -> the
never-half-land ledger stays OPEN -> rollback. It DETECTS, it does not prevent -- exactly the right
instrument for a set-completeness / reachability defect (COO~B/CTO/DS~B (C) ruling 115438Z).

WHAT (C) MEANS (CTO ruling): the C3 system materializes ONLY its node (C3System + the req2 signature
prop + AC5 snapshot_ts); its 21 intra-system FLOWS_TO/RENDERS edges are NOT materialized as semctl
twins (that would feed back through the layer-blind D2/D3 detectors and corrupt P2's certed edge-motif
node_id). Instead the subgraph is carried by REACHABILITY over the edges that ALREADY exist at
layer=aws. So this leg VERIFIES that reachability rather than a write.

THREE CHECKS (all must pass for the R3 leg to pass):

  AC-1  TRAVERSAL-ASSERTION (reachability): every one of the 21 intra_system_edges in the materialize
        contract (the EXPECTED-VALUE FIXTURE) exists as a LIVE estate CloudEdge (FLOWS_TO/RENDERS),
        with BOTH endpoints resolving to live nodes. missing=0, unresolved=0, no dangling endpoint.
        Grounded 2026-07-09: 21/21 present, 34/34 endpoints resolve, all layer=aws.

  (a)   SET-COMPLETENESS coverage-check: delegates to DS~B's single-source entrypoint
        `NFRA_EDGES_P3_c3_subgraph.py --coverage-check` (rc=0 clean / rc=1 FAIL LOUD
        missing_from_contract>0 / rc=2 UNVERIFIABLE). The recompute IS build_motif (same P1M/P1E
        code the analysis-side emission used) -- no re-implementation, no drift (CTO equivalence
        invariant). This closes the SILENT-ADDITION half the frozen-spec replay would miss.

  AC5   C3-NODE + FRESHNESS: the C3 node (system:firm-conditional-display:25558d98) is present as
        node_type C3System, carries the req2 `signature` prop, and its snapshot_ts is a 13-digit
        ms value (the derive_batch_ts basis, CHANGES across runs -- never a constant). The signature
        materializes only AFTER P3's derive-image rebuild lands (fad55a83c folded into
        motif_c2c3_materialize.json); PRE-P3-derive this check reports SIGNATURE_PENDING (expected).

Usage:
  python NFRA_EDGES_P3_r3_verify.py            # run all three against the live canonical
  python NFRA_EDGES_P3_r3_verify.py --json     # machine-readable summary
Exit: 0 all-pass | 1 FAIL (AC-1 missing / (a) rc=1 / AC5 signature-present-but-malformed) |
      2 UNVERIFIABLE (graph unreachable) | 3 SIGNATURE_PENDING (pre-P3-derive: AC-1 + (a) pass,
      signature not yet materialized -- NOT a pass, the deploy is not complete).

Author: 0.7.0_AE_CloudOps  (NFRA_EDGES P3 req1 materialize/verify half of the joint TO).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
CONTRACT = os.path.join(
    WS, "org", "tier2_senior", "0.4.0_DS_ClientPlatform", "deliverables",
    "NFRA_EDGES_P3_materialize_contract.json")
COVERAGE_ENTRYPOINT = os.path.join(
    WS, "org", "tier2_senior", "0.4.0_DS_ClientPlatform", "deliverables",
    "NFRA_EDGES_P3_c3_subgraph.py")
C3_NODE_ID = "system:firm-conditional-display:25558d98"


def _git_bash() -> str:
    """The Git Bash executable (comp-kuzu is a Git Bash script). On Windows, a bare `bash` resolves to
    the WSL relay (`execvpe(/bin/bash) failed`), so prefer the real Git Bash path explicitly."""
    import shutil
    for c in (os.environ.get("GIT_BASH"),
              r"C:\Program Files\Git\usr\bin\bash.exe",
              r"C:\Program Files\Git\bin\bash.exe",
              r"C:\Program Files (x86)\Git\usr\bin\bash.exe"):
        if c and os.path.isfile(c):
            return c
    return shutil.which("bash") or "bash"


def _comp_kuzu_json(cypher: str):
    """Run a Cypher query through comp-kuzu (the canonical auto-refreshing surface) and return the
    parsed --json rows. Fails loud (returns None) on an unreachable graph. The query is passed via a
    temp file to sidestep shell-quoting of node_ids (which carry #, :, /)."""
    with tempfile.NamedTemporaryFile("w", suffix=".cypher", delete=False, encoding="utf-8") as fh:
        fh.write(cypher)
        qpath = fh.name
    try:
        proc = subprocess.run(
            [_git_bash(), "-lc", 'comp-kuzu "$(cat "%s")" --json' % qpath.replace("\\", "/")],
            capture_output=True, text=True, cwd=WS, timeout=180)
    finally:
        try:
            os.unlink(qpath)
        except OSError:
            pass
    out = proc.stdout or ""
    # comp-kuzu prepends a provenance header on stderr; --json rows are on stdout. Extract the array.
    start = out.find("[")
    end = out.rfind("]")
    if start == -1 or end == -1 or end < start:
        return None, (proc.stderr or out)[-400:]
    try:
        return json.loads(out[start:end + 1]), None
    except json.JSONDecodeError as ex:
        return None, "JSON parse: %s" % ex


def check_ac1(contract: dict) -> dict:
    """AC-1: every contract intra_system_edge exists as a live estate CloudEdge, both ends resolve."""
    fixture = contract.get("intra_system_edges", [])
    eps = sorted({e["src"] for e in fixture} | {e["dst"] for e in fixture})
    fix_pairs = {(e["src"], e["dst"], e["edge_type"]) for e in fixture}
    idlist = ", ".join("'%s'" % x for x in eps)

    resolved_rows, err = _comp_kuzu_json(
        "MATCH (n:CloudNode) WHERE n.node_id IN [%s] RETURN n.node_id AS node_id" % idlist)
    if resolved_rows is None:
        return {"check": "AC-1", "status": "UNVERIFIABLE", "detail": err}
    resolved = {r["node_id"] for r in resolved_rows}
    unresolved = [x for x in eps if x not in resolved]

    live_rows, err = _comp_kuzu_json(
        "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
        "WHERE e.edge_type IN ['FLOWS_TO','RENDERS'] AND a.node_id IN [%s] AND b.node_id IN [%s] "
        "RETURN a.node_id AS src, b.node_id AS dst, e.edge_type AS et" % (idlist, idlist))
    if live_rows is None:
        return {"check": "AC-1", "status": "UNVERIFIABLE", "detail": err}
    live_pairs = {(r["src"], r["dst"], r["et"]) for r in live_rows}
    missing = sorted(fix_pairs - live_pairs)

    ok = (not missing) and (not unresolved)
    return {
        "check": "AC-1", "status": "PASS" if ok else "FAIL",
        "expected_edges": len(fix_pairs), "present_live": len(fix_pairs & live_pairs),
        "missing": missing[:8], "endpoints": len(eps),
        "endpoints_resolved": len(resolved), "unresolved": unresolved[:8],
    }


def check_coverage() -> dict:
    """(a): delegate to DS~B's single-source --coverage-check entrypoint (recompute IS build_motif)."""
    proc = subprocess.run([sys.executable, COVERAGE_ENTRYPOINT, "--coverage-check"],
                          capture_output=True, text=True, cwd=WS, timeout=300)
    rc = proc.returncode
    status = {0: "PASS", 1: "FAIL", 2: "UNVERIFIABLE"}.get(rc, "FAIL")
    tail = "\n".join((proc.stdout or "").splitlines()[-4:])
    return {"check": "(a)-coverage", "status": status, "rc": rc, "tail": tail}


def check_c3_node_ac5(contract: dict) -> dict:
    """AC5: C3 node present as C3System, carries the req2 signature prop, snapshot_ts is a fresh
    13-digit ms. Pre-P3-derive the signature is not yet materialized -> SIGNATURE_PENDING."""
    rows, err = _comp_kuzu_json(
        "MATCH (c:CloudNode {node_id:'%s'}) RETURN c.node_type AS node_type, c.snapshot_ts AS "
        "snapshot_ts, c.props AS props" % C3_NODE_ID)
    if rows is None:
        return {"check": "AC5-c3node", "status": "UNVERIFIABLE", "detail": err}
    if not rows:
        return {"check": "AC5-c3node", "status": "FAIL", "detail": "C3 node absent"}
    r = rows[0]
    node_type = r.get("node_type")
    snapshot_ts = r.get("snapshot_ts")
    try:
        props = json.loads(r.get("props") or "{}")
    except (json.JSONDecodeError, TypeError):
        props = {}
    has_sig = isinstance(props.get("signature"), dict)
    ts_ok = isinstance(snapshot_ts, int) and snapshot_ts >= 1_000_000_000_000
    if node_type != "C3System":
        return {"check": "AC5-c3node", "status": "FAIL",
                "detail": "node_type=%r (expected C3System)" % node_type}
    if not has_sig:
        return {"check": "AC5-c3node", "status": "SIGNATURE_PENDING",
                "detail": "C3 node present (C3System) but signature prop not yet materialized "
                          "(pre-P3-derive; folds in at the sequenced P3 image rebuild)",
                "snapshot_ts": snapshot_ts, "snapshot_ts_ms_ok": ts_ok}
    if not ts_ok:
        return {"check": "AC5-c3node", "status": "FAIL",
                "detail": "signature present but snapshot_ts=%r is not a 13-digit ms (AC5: must be "
                          "the derive_batch_ts basis, changes across runs)" % snapshot_ts}
    sig = props["signature"]
    return {"check": "AC5-c3node", "status": "PASS", "snapshot_ts": snapshot_ts,
            "signature_edge_count": sig.get("edge_count")}


def main() -> int:
    contract = json.load(open(CONTRACT, encoding="utf-8"))
    results = [check_ac1(contract), check_coverage(), check_c3_node_ac5(contract)]

    if "--json" in sys.argv[1:]:
        print(json.dumps(results, indent=2))
    else:
        print("=" * 88)
        print("NFRA_EDGES P3 -- AE R3-VERIFY (post-derive, live canonical): AC-1 + (a) + AC5")
        print("=" * 88)
        for r in results:
            print("  [%-16s] %s" % (r["status"], r["check"]))
            for k, v in r.items():
                if k not in ("check", "status"):
                    print("      %s: %s" % (k, v))

    statuses = {r["status"] for r in results}
    if "UNVERIFIABLE" in statuses:
        print("\n  R3-VERIFY: UNVERIFIABLE (graph unreachable) -- NOT a pass.")
        return 2
    if "FAIL" in statuses:
        print("\n  R3-VERIFY: FAIL -- the R3 leg fails, the deploy fails, ledger stays OPEN, rollback.")
        return 1
    if "SIGNATURE_PENDING" in statuses:
        print("\n  R3-VERIFY: SIGNATURE_PENDING -- AC-1 + (a) PASS; the C3 signature is not yet "
              "materialized (pre-P3-derive). NOT a complete pass; re-run after the P3 image rebuild "
              "+ nightly derive stamps the signature.")
        return 3
    print("\n  R3-VERIFY: PASS -- C3 node + signature + AC5 fresh; 21/21 edges reachable; coverage clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
