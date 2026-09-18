#!/usr/bin/env python3
"""R-45 TWO-LEG CONSISTENCY for the investor_reporting bundle's DISTRIBUTION members.

A DISTRIBUTION member (safe_deploy_core CODE_TREES, `"distribution": True`) is deployed on TWO legs
per commit: its own per-file (loose) key and, inside the bundle tarball, under its repo path. Each leg
verifies only its own bytes, so a commit where one leg lands and the other does not reads green on
whichever leg is inspected. This check reads BOTH legs against the ONE authority -- the git blob at a
ref -- per member:

    loose leg   : head-object ETag of the member's per-file key  == md5(blob)
    bundle leg  : sha256 of the member's bytes INSIDE the tarball == sha256(blob)

Subjects are the REAL served objects (bound 12). `--version-id` grades a specific bundle version from
the key's history -- which is how a MUTANT (a bundle minted from a stale tree) is re-graded after the
fact without minting anything. Nothing here writes.

usage: py -3.12 consistency_ib_rtc_2.py [--ref HEAD] [--version-id <bundle VersionId>]
prints one line per member and a verdict; rc 0 CONSISTENT, 1 DIVERGED, 2 could not evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import pathlib
import subprocess
import sys
import tarfile

WS = pathlib.Path(__file__).resolve().parents[7]
sys.path.insert(0, str(WS / ".tools"))
import safe_deploy_core as sdc  # noqa: E402

BUNDLE = "investor_reporting"


def blob(ref: str, rel: str) -> bytes:
    r = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], capture_output=True, cwd=str(WS),
                       timeout=30)
    if r.returncode != 0:
        raise RuntimeError("git show %s:%s failed: %s" % (ref, rel, r.stderr.decode("utf-8", "replace")))
    return r.stdout


def check(ref: str = "HEAD", version_id: "str | None" = None,
          loose_versions: "dict | None" = None):
    """Returns (verdict, lines, rows). verdict in {CONSISTENT, DIVERGED, NOT-EVALUATED}.

    Bind to IDENTITY for a later grader: `ref` a commit hash, `version_id` the bundle version and
    `loose_versions` {repo_path: VersionId} the loose versions an act produced. Omitted, each leg is
    read at its CURRENT served version (the living state)."""
    loose_versions = loose_versions or {}
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    hit = sdc.find_bundle(BUNDLE)
    if not hit:
        return "NOT-EVALUATED", ["no bundle named %s is declared" % BUNDLE], []
    b = hit[2]
    dist = sorted((name, spec) for name, spec in b["members"].items() if sdc.is_distribution_spec(spec))
    if not dist:
        return "NOT-EVALUATED", ["0 DISTRIBUTION members declared -- VACUOUS, not a pass"], []
    kw = {"Bucket": b["bucket"], "Key": b["s3_key"]}
    if version_id:
        kw["VersionId"] = version_id
    obj = s3.get_object(**kw)
    raw = obj["Body"].read()
    lines = ["bundle s3://%s/%s  VersionId %s  ETag %s  sha256 %s"
             % (b["bucket"], b["s3_key"], obj.get("VersionId"), obj["ETag"].strip('"'),
                hashlib.sha256(raw).hexdigest())]
    rows = []
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        names = set(tf.getnames())
        for name, spec in dist:
            rel = spec["repo_path"]
            ref_bytes = blob(ref, rel)
            md5, sha = hashlib.md5(ref_bytes).hexdigest(), hashlib.sha256(ref_bytes).hexdigest()
            tgt = sdc.file_to_s3_target(rel)
            hk = {"Bucket": tgt[0], "Key": tgt[1]} if tgt else None
            if hk and loose_versions.get(rel):
                hk["VersionId"] = loose_versions[rel]
            loose_head = s3.head_object(**hk) if hk else {}
            loose_etag = loose_head.get("ETag", "").strip('"') or None
            member_sha = hashlib.sha256(tf.extractfile(name).read()).hexdigest() if name in names else None
            loose_ok = loose_etag == md5
            bundle_ok = member_sha == sha
            rows.append({"member": rel, "loose_key": "s3://%s/%s" % (tgt[0], tgt[1]) if tgt else None,
                         "loose_version": loose_head.get("VersionId"),
                         "loose_etag": loose_etag, "repo_md5": md5, "loose_ok": loose_ok,
                         "bundle_member_sha256": member_sha, "repo_sha256": sha, "bundle_ok": bundle_ok})
            lines.append("%-9s %s" % ("BOTH-OK" if loose_ok and bundle_ok else "DIVERGED", rel))
            lines.append("          loose  %s v=%s ETag %s %s repo md5 %s"
                         % (rows[-1]["loose_key"], rows[-1]["loose_version"], loose_etag,
                            "==" if loose_ok else "!=", md5))
            lines.append("          bundle member sha256 %s %s repo sha256 %s"
                         % (member_sha, "==" if bundle_ok else "!=", sha))
    good = sum(1 for r in rows if r["loose_ok"] and r["bundle_ok"])
    verdict = "CONSISTENT" if good == len(rows) else "DIVERGED"
    lines.append("CONSISTENCY %s: %d of %d DISTRIBUTION members agree on both legs (ref %s)"
                 % (verdict, good, len(rows), ref))
    return verdict, lines, rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--version-id", default=None)
    a = ap.parse_args()
    v, out, _ = check(a.ref, a.version_id)
    print("\n".join(out))
    sys.exit({"CONSISTENT": 0, "DIVERGED": 1}.get(v, 2))
