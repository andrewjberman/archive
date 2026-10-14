"""Build the three standalone holdings bundles from one tree with core.build_bundle_payload (no upload).

Usage: python -B build_bundles.py <tree_root> <out_dir>
Writes <out_dir>/<firm>.tar.gz, extracts each into <out_dir>/<firm>/ and writes <out_dir>/members.json
(member name -> sha256 of the member bytes, per firm). No S3 call is made: find_bundle and
build_bundle_payload read only the tree's own files.
"""
import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / ".tools"))
import safe_deploy_core as core  # noqa: E402

FIRMS = [("irpt_holdings_49f", "49financial"), ("irpt_holdings_cot", "cottonwood"), ("irpt_holdings_inf", "inflection")]
out.mkdir(parents=True, exist_ok=True)
summary = {}
for key, firm in FIRMS:
    hit = core.find_bundle(key)
    if hit is None:
        summary[firm] = {"error": "find_bundle returned None for " + key}
        continue
    label, bname, b = hit
    payload, shas, err = core.build_bundle_payload(b)
    if payload is None:
        summary[firm] = {"error": err}
        continue
    (out / (firm + ".tar.gz")).write_bytes(payload)
    dest = out / firm
    dest.mkdir(parents=True, exist_ok=True)
    members = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
        for m in tf.getmembers():
            data = tf.extractfile(m).read()
            members[m.name] = hashlib.sha256(data).hexdigest()
            target = dest / m.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    summary[firm] = {
        "label": label,
        "bundle": bname,
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "member_count": len(members),
        "members": members,
        "stamp_shas_keys": sorted(shas.keys()),
    }
    print("BUILT %s members=%d payload_sha256=%s" % (firm, len(members), hashlib.sha256(payload).hexdigest()))
(out / "members.json").write_text(json.dumps(summary, indent=1, sort_keys=True), encoding="utf-8")
print("WROTE %s" % (out / "members.json"))
