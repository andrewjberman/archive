"""OG-rl-6 PHASE C-A step 15: the rollback tree (C:/tmp/og-rb12, detached at e91819e281) equals the live S3 artifact opal-gateway-e91819e281.tar.gz
file by file. usage: python rl6_cmp_rollback.py <scratch dir>  (the scratch dir is created, used and removed)."""
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile

scratch = sys.argv[1]
os.makedirs(scratch, exist_ok=True)
tgz = os.path.join(scratch, "art.tar.gz")
r = subprocess.run(["bash", "-c", 'aws s3 cp "$1" "$2" --region us-east-1', "x",
                    "s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-e91819e281.tar.gz", tgz], capture_output=True, text=True)
print("s3 cp rc", r.returncode, r.stderr.strip()[:200])
dest = os.path.join(scratch, "x")
with tarfile.open(tgz) as t:
    t.extractall(dest)


def tree(root):
    d = {}
    for rr, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(rr, f)
            d[os.path.relpath(p, root).replace(chr(92), "/")] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return d


a = tree(dest)
g = tree("C:/tmp/og-rb12/infra/aws/ec2/opal-gateway")
live = dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rl7_live_md5.txt"), encoding="utf-8") if ln.strip())
nd = [k for k in a if not k.startswith("dashboard/")]
print("artifact files", len(a), "non-dashboard", len(nd), "dashboard", len(a) - len(nd))
print("artifact non-dashboard equal to rb12 git tree", sum(1 for k in nd if g.get(k) == a[k]), "not equal", [k for k in nd if g.get(k) != a[k]][:5])
print("rb12 gateway files under the 94 live list equal to artifact", sum(1 for k, v in live.items() if a.get(k) == v), "of", len(live), "mismatch", [k for k, v in live.items() if a.get(k) != v][:5])
print("artifact files absent from rb12 (non-dashboard)", [k for k in nd if k not in g][:5])
shutil.rmtree(scratch)
print("scratch removed", not os.path.exists(scratch))
