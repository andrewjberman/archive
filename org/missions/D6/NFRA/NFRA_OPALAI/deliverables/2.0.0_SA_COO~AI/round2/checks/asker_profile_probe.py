"""Arm (b) pre-fire read (CVO condition on UB-20261009T133624Z-e1ca): does a Teams sender hold ANY asker profile or grant?

Reads gateway-access-state-table (one read-only `dynamodb scan`, the OA-g-3 g3_scan.py pattern) and reports, for ONE
sender Entra oid, how many POLICY records carry that oid (any status) and how many of those are an ACTIVE principal
profile. Prints the verdict and counts only, never a tid, another oid or an email. The scan pages are followed.
Usage: python asker_profile_probe.py <sender-oid> <workspace-root>
Verdict line: PROFILE: NONE (fire allowed) | PROFILE: PRESENT active=<n> any=<n> (skip) | SCAN-FAILED (do not fire).
"""
import json
import os
import subprocess
import sys

from boto3.dynamodb.types import TypeDeserializer


def scan_all(aws_shim):
    """Every item of the table, following NextToken; None when a page cannot be read."""
    deser = TypeDeserializer()
    out, token, n_pages = [], None, 0
    while True:
        argv = ["bash", aws_shim, "dynamodb", "scan", "--table-name", "gateway-access-state-table", "--output", "json"]
        if token:
            argv += ["--starting-token", token]
        proc = subprocess.run(argv, capture_output=True, timeout=120)
        try:
            page = json.loads(proc.stdout.decode("utf-8"))
        except Exception:
            print("SCAN-FAILED rc=%s" % proc.returncode)
            return None, n_pages
        n_pages += 1
        out += [{k: deser.deserialize(v) for k, v in it.items()} for it in page.get("Items", [])]
        token = page.get("NextToken")
        if not token:
            return out, n_pages


def main():
    oid, root = sys.argv[1].strip().lower(), sys.argv[2]
    sys.path.insert(0, os.path.join(root, "infra", "aws", "ec2", "opal-gateway"))
    from app import data_entitlement as de

    items, pages = scan_all(os.path.join(root, ".tools", "aws"))
    if items is None:
        raise SystemExit(2)
    policy = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
    mine = [i for i in policy if str(i.get("oid", "")).lower() == oid or oid in str(i.get("pk", "")).lower()]
    active = [i for i in mine if i.get("sk") == de.PROFILE and i.get("status") == "active"]
    print("scan: pages=%d items=%d policy=%d; records naming this oid=%d; active profiles=%d" % (
        pages, len(items), len(policy), len(mine), len(active)))
    print("PROFILE: NONE (fire allowed)" if not mine else "PROFILE: PRESENT active=%d any=%d (skip)" % (len(active), len(mine)))


if __name__ == "__main__":
    main()
