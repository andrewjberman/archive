"""NFRA_OPLGTW OG-v-6 shared helpers: AWS shim calls (read-only S3 by VersionId), the outside-repo
work cache, and the declared grain. Carries NO customer data and never reads or imports
infra/aws/ec2/opal-gateway/app/integrations/schwab/ (the declared grain is inlined from the task order,
which took it from query.py:136-140 @73e5968e67).
"""
from __future__ import annotations

import json
import os
import subprocess

CELL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CELL_DIR, "..", "..", "..", "..", "..", "..", ".."))
AWS_SHIM = os.path.join(REPO_ROOT, ".tools", "aws.cmd")
BUCKET = "opal-data-assets"
MASTERS = {"08242234": "SmartX", "08335338": "BlackDiamond"}
DATASETS = ("dim_position", "dim_balance", "dim_asset")

# Declared grain, source column names, inlined from the order (query.py:136-140 @73e5968e67).
DECLARED_GRAIN = {
    "dim_position": ("account_id", "cusip", "l_s"),
    "dim_balance": ("account_id",),
    "dim_asset": ("cusip",),
}

_LOCAL = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
SEALED_DIR = os.environ.get("OG_SEALED_DIR") or os.path.join(_LOCAL, "opal", "og-salt", "v2")
WORK_DIR = os.path.join(SEALED_DIR, "work")

GRAIN_PATH = os.path.join(CELL_DIR, "GRAIN_DECLARATION.json")
SEALED_PATH = os.path.join(CELL_DIR, "SEALED_EXPECTED_V2.json")


def aws(args, timeout=120):
    out = subprocess.run([AWS_SHIM] + list(args), capture_output=True, text=True, timeout=timeout)
    if out.returncode != 0:
        raise RuntimeError(f"aws rc={out.returncode} args={args[:3]}: {out.stderr[:300]}")
    return out.stdout


def get_marker(master: str, date: str, version_id: str) -> dict:
    os.makedirs(WORK_DIR, exist_ok=True)
    path = os.path.join(WORK_DIR, f"marker_{master}_{date}_{version_id}.json")
    if not os.path.exists(path):
        meta = json.loads(aws(["s3api", "get-object", "--bucket", BUCKET,
                               "--key", f"schwab/{master}/meta/complete/date={date}.json",
                               "--version-id", version_id, path]))
        if meta.get("VersionId") != version_id:
            raise RuntimeError("marker VersionId mismatch")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def fetch_silver(key: str, version_id: str, local_name: str) -> str:
    """GetObject by VersionId into the outside-repo work cache; returns the local path."""
    os.makedirs(WORK_DIR, exist_ok=True)
    path = os.path.join(WORK_DIR, local_name)
    meta = json.loads(aws(["s3api", "get-object", "--bucket", BUCKET, "--key", key,
                           "--version-id", version_id, path]))
    if meta.get("VersionId") != version_id:
        raise RuntimeError(f"VersionId mismatch on {key}")
    return path
