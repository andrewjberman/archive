#!/usr/bin/env python3
"""LIVE_ASSOCIATION_READ_C1 -- POSN_AGGFIX.TO-C1-1, criteria C1-AC18 (--before-apply) and C1-AC12 (no flag).

Reads the LIVE distribution config of EVTSA9VEHNZVH (never Terraform, never the re-plan) and lists every
lambda_function_association whose ARN names auth-validator-edge.

  --before-apply  prints `AUTH-VALIDATOR ASSOCIATIONS <n> -- AT VERSION <v> <k> of <n>` and records <v> as the
                  rollback target in .scratch/c1_rollback_target.json.
  (no flag)       polls get-distribution Status until `Deployed` (bounded: 80 polls x 20 s, each printed), then
                  reads the newest published version of auth-validator-edge (list-versions-by-function, every
                  page) and prints `AUTH-VALIDATOR ASSOCIATIONS <n> -- AT NEW VERSION <k> of <n>` and the count
                  at any other version. The new version must differ from the recorded rollback target.
Exit 0 when the expectation holds; 1 when it does not; 2 on a read failure.
"""
from __future__ import annotations

import collections
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("c1_edge_route_census", HERE / "c1_edge_route_census.py")
census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(census)
ROOT = census.ROOT
DIST_ID = "EVTSA9VEHNZVH"
FN = "auth-validator-edge"
TARGET_FILE = ROOT / ".scratch" / "c1_rollback_target.json"
EXPECTED_N = 25


def aws_json(args: str) -> dict:
    rc, out, err = census.run_bash(f"aws {args} --output json", timeout=180)
    if rc != 0:
        print(f"ERROR: aws {args} rc={rc}: {err.strip()[:300]}")
        sys.exit(2)
    return json.loads(out)


def associations() -> tuple[str, int, list[tuple[str, str, str]]]:
    live = aws_json(f"cloudfront get-distribution-config --id {DIST_ID}")
    cfg = live["DistributionConfig"]
    behaviours = [("/* [default]", cfg["DefaultCacheBehavior"])] + [
        (b["PathPattern"], b) for b in cfg["CacheBehaviors"].get("Items", [])]
    rows = []
    for pattern, b in behaviours:
        lfa = b.get("LambdaFunctionAssociations", {})
        items = lfa.get("Items", [])
        if lfa.get("Quantity", len(items)) != len(items):
            print(f"WARN: {pattern} LambdaFunctionAssociations Quantity {lfa.get('Quantity')} != items {len(items)}")
        for a in items:
            arn = a["LambdaFunctionARN"]
            if f":function:{FN}:" in arn:
                rows.append((pattern, a["EventType"], arn))
    return live.get("ETag", ""), len(behaviours), rows


def main() -> int:
    before = "--before-apply" in sys.argv[1:]
    print(f"C1-{'AC18' if before else 'AC12'} LIVE_ASSOCIATION_READ_C1 -- distribution {DIST_ID}, function {FN}")
    if not before:
        for i in range(1, 81):
            d = aws_json(f"cloudfront get-distribution --id {DIST_ID}")["Distribution"]
            print(f"  poll {i}: Status {d['Status']} LastModifiedTime {d.get('LastModifiedTime')} at "
                  f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
            if d["Status"] == "Deployed":
                break
            time.sleep(20)
        else:
            print("STATUS NOT Deployed within 80 polls -- association read NOT graded")
            return 1
    etag, n_beh, rows = associations()
    print(f"  live config ETag {etag}; behaviours {n_beh}")
    for pattern, ev, arn in rows:
        print(f"  {pattern:<52} {ev:<16} {arn}")
    versions = collections.Counter(arn.rsplit(":", 1)[-1] for _p, _e, arn in rows)
    n = len(rows)
    count_note = "" if n == EXPECTED_N else f" (the config's own count is {n}, not {EXPECTED_N})"
    if before:
        if len(versions) == 1:
            v = next(iter(versions))
            print(f"AUTH-VALIDATOR ASSOCIATIONS {n} -- AT VERSION {v} {versions[v]} of {n}{count_note}")
        else:
            print(f"AUTH-VALIDATOR ASSOCIATIONS {n} -- MIXED VERSIONS {dict(versions)}{count_note}")
            v = versions.most_common(1)[0][0]
        TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
        TARGET_FILE.write_text(json.dumps({"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                           "etag": etag, "associations": n, "versions": dict(versions),
                                           "rollback_target_version": v}, indent=2) + "\n", encoding="utf-8")
        print(f"  ROLLBACK TARGET VERSION {v} recorded to {TARGET_FILE}")
        return 0 if (len(versions) == 1 and n == EXPECTED_N) else 1
    listed = aws_json(f"lambda list-versions-by-function --function-name {FN} --region us-east-1")
    nums = sorted(int(x["Version"]) for x in listed.get("Versions", []) if x["Version"] != "$LATEST")
    newest = str(nums[-1]) if nums else "?"
    prior = None
    if TARGET_FILE.exists():
        prior = json.loads(TARGET_FILE.read_text(encoding="utf-8")).get("rollback_target_version")
    print(f"  published versions read {len(nums)}; newest {newest}; rollback target recorded before apply {prior}")
    at_new = versions.get(newest, 0)
    other = n - at_new
    print(f"AUTH-VALIDATOR ASSOCIATIONS {n} -- AT NEW VERSION {at_new} of {n} (version {newest}); "
          f"AT ANY OTHER VERSION {other}{count_note}")
    ok = n == EXPECTED_N and at_new == n and other == 0 and prior is not None and newest != str(prior)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
