"""Scratch (round 197, IB-pr-545): build each firm's bundle payload from the PIN-2 tree via core.build_bundle_payload,
extract to built/<firm>/. Read only: no S3 write. Run with python -I from the scratch directory."""
import hashlib
import json
import shutil
import sys
import tarfile
from pathlib import Path

PIN_TREE = Path("C:/dev/wk-ib545-pin")
SCRATCH = Path("C:/dev/_scratch390")
sys.path.insert(0, str(PIN_TREE / ".tools"))
import safe_deploy_core as core  # noqa: E402

assert Path(core.__file__).resolve().is_relative_to(PIN_TREE.resolve()) if hasattr(Path, "is_relative_to") else True
FIRM_KEY = {
    "49financial": "opal-data-49financial",
    "cottonwood": "opal-data-cottonwood",
    "inflection": "opal-data-inflection",
}
out = {"core_file": str(Path(core.__file__).resolve())}
for firm, bucket in FIRM_KEY.items():
    want_key = "irpt/%s/code/gold/investor-reporting-holdings.tar.gz" % firm
    hits = [name for name, b in core.STANDALONE_BUNDLES.items() if b["bucket"] == bucket and b["s3_key"] == want_key]
    assert len(hits) == 1, (firm, hits)
    name = hits[0]
    found = core.find_bundle(name)
    assert found is not None and found[1] == name
    tree_label, _, b = found
    payload, shas, err = core.build_bundle_payload(b)
    assert payload is not None, (firm, err)
    dest = SCRATCH / "built" / firm
    if dest.exists():
        shutil.rmtree(str(dest))
    dest.mkdir(parents=True)
    tar_path = SCRATCH / "dl" / firm / "built.tar.gz"
    tar_path.write_bytes(payload)
    with tarfile.open(str(tar_path), "r:gz") as tf:
        names = tf.getnames()
        for n in names:
            assert not n.startswith("/") and ".." not in n.split("/"), n
        tf.extractall(str(dest))
    members = [n for n in names if not n.endswith("/")]
    out[firm] = {
        "bundle_name": name,
        "tree_label": tree_label,
        "member_entries": len(members),
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "shas": shas,
        "closure_members": len(b["members"]),
    }
    print("OK:", firm, name, "entries=%d" % len(members), "payload=%s" % out[firm]["payload_sha256"][:12])
Path(SCRATCH / "built_meta.json").write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
