"""Build a test mirror of the repo at the pin with the extracted ZIP tree overlaid on every investor-reporting package directory.
    python -I mkmirror_426.py <extracted_zip_dir> <dest> <pin>   (run from inside the worktree)
<dest>/ = the pin's infra/aws/lambda/investor-reporting, docs/contracts, infra/logic/registry, org/standards, data/firm_registry.json (git archive; test
support and fixtures only); then the zip's flat members are copied over EVERY investor-reporting/<d>/ so a test that imports a packaged module
by bare name imports THE ZIP'S file. No lib/ is placed at <dest> root (a root lib/opal_naming.py would shadow the zip's own)."""
import io
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
import os
R = os.environ.get("IB426_ROOT") or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip()
tree, dest, PIN = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
if dest.exists():
    shutil.rmtree(dest)
dest.mkdir(parents=True)
for path in ["infra/aws/lambda/investor-reporting", "docs/contracts", "infra/logic/registry", "org/standards/NAMING_SCHEMA.json", "data/firm_registry.json"]:
    r = subprocess.run(["git", "archive", "--format=tar", PIN, path], cwd=R, capture_output=True)
    if r.returncode:
        print("archive failed", path, r.stderr[:200])
        continue
    with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tf:
        tf.extractall(dest)
base = dest / "infra/aws/lambda/investor-reporting"
n = 0
for d in sorted(p for p in base.iterdir() if p.is_dir()):
    shutil.copytree(tree, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
    n += 1
print("ok", dest, "dirs overlaid:", n)
