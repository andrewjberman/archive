#!/usr/bin/env python3
"""NFRA_GRAPHS.D8-FP AC3 -- the binding de-noise-WITHOUT-blinding test.

Exercises the per-surface AWS-backend MEMBERSHIP diff (the exact logic deployed in
derive_runner.run_critical_surface_scan) over a synthetic-removal matrix: a removed backend
member of a surface MUST fire that surface (REMOVED finding), a co-tenant non-member MUST fire
NOTHING, and firm-separation must hold (a bd-producer removal must not fire inf/cot ADVI). The
in-derive scan cannot be run ad-hoc (it is the Fargate derive task vs the in-VPC graph -- a
manufactured run is banned), so the removal-matrix is proven here against the membership baseline;
the next scheduled nightly proves the real SNS egress on the AWS derive (0 false-fires).

Run from the workspace root (after producing the node dump):
  comp-kuzu --json "MATCH (n:CloudNode) RETURN n.name AS name, n.node_id AS node_id,
                    n.node_type AS node_type, n.drift_class AS drift_class" 2>/dev/null > .runtmp/d8fp_allnodes.json
  python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_GRAPHS.D8-FP.ac3-egress-test.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "org/modules/graph")
import resign_surface_baseline as rs   # noqa: E402  (the re-sign tool builds the membership)

NODES_JSON = ".runtmp/d8fp_allnodes.json"


def _diff_findings(baseline: dict, current_ids: set) -> set:
    """The exact run_critical_surface_scan membership diff: a member node_id absent from the
    current AWS graph -> REMOVED finding for that surface x firm. Returns {(severity, sf_key)}."""
    out = set()
    for sf_key, sf in baseline["surfaces"].items():
        sev = sf.get("severity", "SEV2")
        for nid in sf.get("members", {}):
            if nid not in current_ids:
                out.add((sev, sf_key))
    return out


def main() -> int:
    baseline = rs.build_baseline(NODES_JSON)
    node_map = rs._load_node_map(NODES_JSON)            # name -> {node_id,...}
    name2id = {nm: v["node_id"] for nm, v in node_map.items()}
    all_ids = {v["node_id"] for v in node_map.values()}  # full current AWS-node universe

    # (scenario name, [removed member NAMEs], {surface_keys that MUST fire}, {that MUST NOT fire})
    MATRIX = [
        ("drop benchmark producer", ["yang-model-portfolio-benchmarks"],
         {"model_portfolios.benchmark__all"},
         {"advisor_intelligence__bd", "advisor_intelligence__inf", "model_portfolios.peers__all"}),
        ("drop peers producer", ["yang-generate-peer-performance"],
         {"model_portfolios.peers__all"},
         {"model_portfolios.benchmark__all", "advisor_intelligence__bd"}),
        ("drop mdpf AUA producer", ["mdpf-daily-runner"],
         {"model_portfolios.headline__all", "model_portfolios.aum__all"},
         {"model_portfolios.benchmark__all", "advisor_intelligence__bd", "advisor_intelligence__inf"}),
        ("drop bd-gold producer (firm-sep)", ["bd-gold-layer-runner"],
         {"advisor_intelligence__bd"},
         {"advisor_intelligence__inf", "model_portfolios.benchmark__all"}),
        ("drop inf ADVI producer (firm-sep)", ["inf-portal-advisor-publisher"],
         {"advisor_intelligence__inf"},
         {"advisor_intelligence__bd", "model_portfolios.headline__all"}),
        ("drop serving Lambda (category: serving)", ["opal-portal-data-proxy"],
         {"model_portfolios.benchmark__all", "model_portfolios.peers__all",
          "model_portfolios.headline__all", "model_portfolios.aum__all"},
         {"advisor_intelligence__bd", "advisor_intelligence__inf"}),
        ("drop served bucket opal-data-inf (category: bucket)", ["opal-data-inf"],
         {"advisor_intelligence__inf"},
         {"advisor_intelligence__bd", "model_portfolios.benchmark__all",
          "model_portfolios.headline__all"}),
        ("CONTROL: drop co-tenant non-member", ["test-yfinance-simple"],
         set(), {"model_portfolios.benchmark__all", "model_portfolios.headline__all",
                 "model_portfolios.aum__all", "model_portfolios.peers__all",
                 "advisor_intelligence__bd", "advisor_intelligence__inf"}),
    ]

    all_pass = True
    for label, removed_names, must_fire, must_not_fire in MATRIX:
        removed_ids = {name2id[n] for n in removed_names if n in name2id}
        missing = [n for n in removed_names if n not in name2id]
        cn = all_ids - removed_ids
        fired = {sf for _, sf in _diff_findings(baseline, cn)}
        ok_fire = must_fire <= fired
        ok_not = not (must_not_fire & fired)
        ok = ok_fire and ok_not and not missing
        all_pass &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
        print(f"        removed={removed_names} -> fired={sorted(fired) or 'NONE'}")
        if missing:
            print(f"        FAIL: removed name(s) not in graph (test setup): {missing}")
        if not ok_fire:
            print(f"        FAIL: expected-fire missing: {sorted(must_fire - fired)}")
        if not ok_not:
            print(f"        FAIL: must-NOT-fire leaked: {sorted(must_not_fire & fired)}")
    print("=" * 60)
    print("AC3 VERDICT:", "ALL PASS -- de-noised + firm-separated + co-tenant control clean"
          if all_pass else "FAIL -- do not close")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
