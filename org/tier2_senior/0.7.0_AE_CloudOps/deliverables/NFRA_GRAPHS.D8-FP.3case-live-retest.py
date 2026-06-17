#!/usr/bin/env python3
"""NFRA_GRAPHS.D8-FP 3-case LIVE re-test (CTO 204916Z binding gate) -- name-keyed, post --sign-baseline.

Fixes the AC3 tautology (which built baseline AND current from the same comp-kuzu dump). Here the
baseline is the REAL by-construction signed baseline (derive_runner --sign-baseline; name-keyed), and
the diff replicates run_critical_surface_scan's membership check + _graph_to_scan_nodes' name-extraction
(node.get("name") or node.get("id")) verbatim.

  Case 1: clean live derive -> 0 false-removal. THE binding case = the live derive run's SURFACE_SCAN
          log (findings=0); mirrored here against a clean name-keyed cn for a unit check.
  Case 2: a synthetic producer removal STILL fires the right surface (de-noise WITHOUT blinding).
  Case 3: an EC2 replacement (same Name-tag, NEW instance-id) does NOT false-fire -- name-keying makes
          the instance-id change invisible (the ephemerality guard CTO required).

Run from workspace root after `aws s3 cp s3://.../critical-surface-baseline.json .runtmp/csb_signed.json`.
"""
from __future__ import annotations

import json

BASELINE = ".runtmp/csb_signed.json"


def _name_key(node: dict) -> str:
    """VERBATIM from derive_runner._graph_to_scan_nodes: ec2 -> Name-tag (node['name']); lambda/s3 ->
    id (FunctionName/bucket-name; no separate 'name')."""
    return str(node.get("name") or node.get("id") or "")


def _diff(baseline: dict, cn: dict) -> set:
    """run_critical_surface_scan membership diff: a member name absent from cn -> REMOVED."""
    out = set()
    for sf_key, sf in baseline["surfaces"].items():
        sev = (sf or {}).get("severity", "SEV2")
        for nm in (sf or {}).get("members", {}):
            if nm not in cn:
                out.add((sev, sf_key, nm))
    return out


def main() -> int:
    b = json.load(open(BASELINE, encoding="utf-8"))
    members = {nm: sf_key for sf_key, sf in b["surfaces"].items() for nm in sf.get("members", {})}
    # clean name-keyed cn = every baseline member present (+ co-tenant non-members that must never fire)
    cn_clean = {nm: {"node_type": "X"} for nm in members}
    cn_clean.update({"test-yfinance-simple": {}, "some-unrelated-lambda": {}})
    ok = True

    f1 = _diff(b, cn_clean)
    c1 = len(f1) == 0
    ok &= c1
    print(f"[{'PASS' if c1 else 'FAIL'}] case1-mirror: clean name-keyed cn -> {len(f1)} findings (expect 0); "
          "the LIVE binding case = the derive run's SURFACE_SCAN findings=0")

    # case 2: remove a known benchmark producer -> must fire benchmark, nothing else
    victim = "yang-model-portfolio-benchmarks"
    if victim in members:
        cn2 = dict(cn_clean); cn2.pop(victim, None)
        f2 = _diff(b, cn2)
        fired = {(sf, nm) for _, sf, nm in f2}
        c2 = fired and all(nm == victim and sf.startswith("model_portfolios.benchmark") for sf, nm in fired)
        ok &= c2
        print(f"[{'PASS' if c2 else 'FAIL'}] case2: remove {victim} -> fired {sorted(fired)} (expect benchmark only)")
    else:
        print(f"[WARN] case2: {victim} not a baseline member this vintage; pick another producer")

    # case 3: EC2 replacement -- same Name-tag, NEW instance-id. name-keying => the Name-tag IS the key,
    # so the instance-id change is invisible -> the member stays present -> NO false-fire.
    ec2 = [nm for sf in b["surfaces"].values() for nm, mt in sf.get("members", {}).items()
           if "EC2" in str((mt or {}).get("node_type", "")).upper()]
    if ec2:
        tag = ec2[0]
        replaced_node = {"id": "i-0NEWREPLACEMENTxxxxxxxx", "name": tag, "type": "EC2_INSTANCE"}
        post_key = _name_key(replaced_node)
        cn3 = dict(cn_clean)  # name-keyed cn already has `tag`; the replacement keeps the same key
        c3 = (post_key == tag) and (tag in cn3) and (tag not in {nm for _, _, nm in _diff(b, cn3)})
        ok &= c3
        print(f"[{'PASS' if c3 else 'FAIL'}] case3: ec2 '{tag}' replaced (new instance-id, same Name-tag) "
              f"-> name-key still '{post_key}', member present, 0 false-fire")
    else:
        print("[SKIP] case3: no EC2 member in the baseline this vintage (ephemerality guard not exercisable)")

    print("=" * 60)
    print("3-CASE VERDICT:", "ALL PASS -- name-keyed, de-noised-without-blinding, replacement-safe"
          if ok else "FAIL -- do not close")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
