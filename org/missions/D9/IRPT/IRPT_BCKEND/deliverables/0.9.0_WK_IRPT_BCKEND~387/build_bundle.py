"""Scratch (IB-pr-542 amendment): the Cottonwood bundle payload from a worktree tree, extracted. Read only: no S3 call."""
import hashlib
import shutil
import sys
import tarfile
from pathlib import Path

tree, name = Path(sys.argv[1]), sys.argv[2]
SCRATCH = Path("C:/dev/_scratch387")
sys.path.insert(0, str(tree / ".tools"))
import safe_deploy_core as core  # noqa: E402

bucket = "opal-data-cottonwood"
want_key = "irpt/cottonwood/code/gold/investor-reporting-holdings.tar.gz"
hits = [n for n, b in core.STANDALONE_BUNDLES.items() if b["bucket"] == bucket and b["s3_key"] == want_key]
assert len(hits) == 1, hits
found = core.find_bundle(hits[0])
assert found is not None and found[1] == hits[0]
tree_label, _, b = found
payload, shas, err = core.build_bundle_payload(b)
assert payload is not None, err
dest = SCRATCH / "toggle" / name
if dest.exists():
    shutil.rmtree(str(dest))
dest.mkdir(parents=True)
tar_path = SCRATCH / "dl" / ("%s.tar.gz" % name)
tar_path.write_bytes(payload)
with tarfile.open(str(tar_path), "r:gz") as tf:
    names = tf.getnames()
    for n in names:
        assert not n.startswith("/") and ".." not in n.split("/"), n
    tf.extractall(str(dest))
print("OK: %s %s entries=%d payload=%s" % (name, hits[0], len([n for n in names if not n.endswith("/")]),
                                           hashlib.sha256(payload).hexdigest()[:12]))
