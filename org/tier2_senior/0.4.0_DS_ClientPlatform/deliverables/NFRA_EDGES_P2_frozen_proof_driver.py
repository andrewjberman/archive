#!/usr/bin/env python3
"""NFRA_EDGES P2 -- frozen-vintage proof driver (reproducibility affordance for the CTO arch-gate + CVO cert).

WHY THIS EXISTS (a live graph-infra incident, NOT a P2 design choice):
  The canonical Kuzu surface is BEHIND Nessie HEAD, and its auto-refresh self-heal is BROKEN. Every
  query on the canonical path calls _canonical.ensure_fresh() (kuzu_cli.py:_run_query, gated on
  is_canonical(db_path)) -> a rebuild that FAILS:

      WARN: stealing dead rebuild lock (age 901s)
      INFO: canonical auto-refresh (BEHIND Nessie HEAD ...) -> rebuilding kuzu_nessie_db
      WARN: canonical rebuild failed (RuntimeError: kuzu_nessie_load failed rc=143:
            arrow::fs::FinalizeS3 was not called ... segmentation fault at exit); serving existing

  It burns minutes on the doomed rebuild before "serving existing", so the D1/D2/D3 expansion queries
  blow MOTIF_KUZU_TIMEOUT (observed: >300s each). Rule 20's "BEHIND self-heals" does NOT hold today.
  Escalated to 0.7.0_AE_CloudOps (graph infra) + COO~B.

  kuzu_cli.py:36 -- "DBs reached via explicit --db-path are never auto-refreshed" -- but _run_query
  gates the refresh on is_canonical(db_path), so a NON-canonical path is required to bypass it.
  This driver therefore queries a FROZEN COPY of the canonical pin.

DISCLOSURE (Rule 20, non-negotiable): a --db-path DB is a FROZEN VINTAGE, never "the estate".
  This driver proves the P2 MECHANISM composes on REAL rows. It does NOT assert estate-current
  counts. When the canonical rebuild is fixed, re-run the module's own default path:
      python NFRA_EDGES_P2_edge_motifs.py
  and the counts become estate-current. THAT is the run to quote as live.

Usage (from the workspace root):
  # 1. freeze a copy of the canonical pin (read the provenance header first; record the pin!)
  cp -r infra/aws/globgrph/kuzu_nessie_db /tmp/kuzu_frozen_db
  # 2. prove
  python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_EDGES_P2_frozen_proof_driver.py \
      --frozen-db /tmp/kuzu_frozen_db [--counterfactual]

Author: 0.4.0_DS_ClientPlatform~B (NFRA_EDGES P2 owner). TO NFRA_EDGES.P2.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
CLI = os.path.join(WS, "infra", "aws", "globgrph", "kuzu_cli.py")

sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "globgrph"))

import _canonical  # noqa: E402
import NFRA_EDGES_P1_edge_reification as P1E  # noqa: E402
import NFRA_EDGES_P2_edge_motifs as P2  # noqa: E402
import NFRA_MOTIF_P1_c2_catalog as P1M  # noqa: E402

_FROZEN_DB = None


def frozen_kuzu(query: str) -> tuple:
    """P1M.comp_kuzu's contract (fail-loud; NEVER a silent [] a caller misreads as 'no motif'),
    pinned to the frozen DB so no auto-refresh/rebuild is attempted."""
    proc = subprocess.run(
        [sys.executable, CLI, "--db-path", _FROZEN_DB, "--json", query],
        capture_output=True, text=True, cwd=WS, timeout=600,
    )
    if proc.returncode != 0:
        raise P1M.GraphUnavailable("frozen kuzu_cli rc=%d -- %s"
                                   % (proc.returncode, (proc.stderr or "").strip()[:300]))
    out = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    idx = out.find("\n[")
    if idx < 0:
        idx = out.find("[")
    if idx < 0:
        raise P1M.GraphUnavailable("frozen kuzu_cli rc=0 but no JSON array -- %s" % query[:100])
    try:
        return json.loads(out[idx:].strip()), {"frozen": True}
    except json.JSONDecodeError:
        start = out.find("[", idx)
        depth, end = 0, -1
        for i in range(start, len(out)):
            if out[i] == "[":
                depth += 1
            elif out[i] == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end <= 0:
            raise P1M.GraphUnavailable("unbalanced JSON array from frozen kuzu_cli")
        return json.loads(out[start:end]), {"frozen": True}


def _collect_deduped_edges(snapshot_ts: int) -> list:
    """Reify the firm detectors' defining edges, deduped by the AC4 edge id (D2/D3 overlap BY DESIGN)."""
    pairs = []
    for spec in P1M.CATALOG:
        if spec["id"] not in P2._FIRM_DETECTORS:
            continue
        edge_nodes, cloud_records = P1E.reify_motif_edges(spec, snapshot_ts)
        pairs.extend(zip(edge_nodes, cloud_records))
    seen, uniq = set(), []
    for node, rec in pairs:
        if node.nid in seen:
            continue
        seen.add(node.nid)
        uniq.append((node, rec))
    return uniq


def counterfactual() -> int:
    """AC4 on REAL rows: what a condition-LESS signature would silently MERGE."""
    ts = P2.derive_batch_ts()
    uniq = _collect_deduped_edges(ts)
    real = P2.group_edges_by_signature(uniq)
    cf: dict = {}
    for node, rec in uniq:
        p = rec["props"]
        cf.setdefault((p["edge_type"], p["edge_kind"]), []).append(node)

    print("\n" + "=" * 78)
    print("AC4 COUNTERFACTUAL on REAL rows (frozen vintage)")
    print("=" * 78)
    n_motifs = sum(1 for v in real.values() if len(v) >= P1M.AC3_THRESHOLD)
    n_inst = sum(1 for v in real.values() if len(v) < P1M.AC3_THRESHOLD)
    print("  distinct reified *Edge C1 instances      : %d" % len(uniq))
    print("  WITH condition in identity (P2, correct) : %d distinct idioms" % len(real))
    print("     -> %d motifs (recur>=%d) + %d instances (recur 1)" % (n_motifs, P1M.AC3_THRESHOLD, n_inst))
    print("  WITHOUT condition (the merge bug)        : %d group(s)" % len(cf))
    for k, v in cf.items():
        print("     -> %s[%s] would absorb ALL %d edges into ONE motif id" % (k[0], k[1], len(v)))
    print("\n  SILENT LOSS AVERTED: %d distinct edge idioms would collapse into %d id(s);"
          % (len(real), len(cf)))
    print("  %d idiom(s) destroyed by a store-side MERGE on the shared id." % (len(real) - len(cf)))
    return 0


def main() -> int:
    global _FROZEN_DB
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--frozen-db", required=True, help="path to a FROZEN COPY of the canonical kuzu DB")
    ap.add_argument("--counterfactual", action="store_true", help="also run the AC4 merge counterfactual")
    a = ap.parse_args()

    _FROZEN_DB = os.path.abspath(a.frozen_db)
    if not os.path.exists(_FROZEN_DB):
        print("ERROR: frozen db not found: %s" % _FROZEN_DB)
        return 3
    if _canonical.is_canonical(_FROZEN_DB):
        print("ABORT: %s resolves as CANONICAL -- querying it would trigger the broken auto-refresh." % _FROZEN_DB)
        print("       Copy it to a scratch path first (a frozen vintage), then re-run.")
        return 3

    print("FROZEN-VINTAGE PROOF -- Rule 20 disclosure: this is NOT the estate-current surface.")
    print("  frozen db    : %s" % _FROZEN_DB)
    print("  is_canonical : False  (=> no auto-refresh, no doomed rebuild)")
    print("  WHY frozen   : canonical auto-refresh is BROKEN (kuzu_nessie_load rc=143, arrow FinalizeS3).")
    print("  Re-run `python NFRA_EDGES_P2_edge_motifs.py` (canonical default) once that is fixed.\n")

    P1M.comp_kuzu = frozen_kuzu   # P1E calls P1M.comp_kuzu -> same module object -> patched
    rc = P2.prove_edge_motifs()
    if a.counterfactual and rc == 0:
        rc = counterfactual()
    return rc


if __name__ == "__main__":
    sys.exit(main())
