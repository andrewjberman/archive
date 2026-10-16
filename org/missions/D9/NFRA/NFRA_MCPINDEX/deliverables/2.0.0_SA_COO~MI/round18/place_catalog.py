"""place_catalog.py <worktree root> <issuer catalog file> <expected md5>: copy the issuer's emitted runtime catalog over the tracked one and prove it.

The issuer emits at the workspace root (the emitter needs portal/src/api); a worker in a sparse worktree only PLACES the file. It prints
`copied=1 equal=1` only when the destination is byte-equal to the source AND the source md5 is the one the order names; anything else prints
`copied=0 equal=0` and exits 1, with the destination restored. It never regenerates the catalog.
"""
import filecmp
import hashlib
import os
import shutil
import sys

root, src, want = sys.argv[1], sys.argv[2], sys.argv[3].lower()
rel = 'infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml'
dst = os.path.join(root, rel)
got = hashlib.md5(open(src, 'rb').read()).hexdigest()
if got != want:
    print('source md5 %s is not the expected %s' % (got, want))
    print('copied=0 equal=0')
    sys.exit(1)
backup = dst + '.before_place'
shutil.copyfile(dst, backup)
shutil.copyfile(src, dst)
same = filecmp.cmp(src, dst, shallow=False)
if not same:
    shutil.copyfile(backup, dst)
os.remove(backup)
print('cmp %s equal=%s md5=%s' % (rel, same, hashlib.md5(open(dst, 'rb').read()).hexdigest()))
print('copied=1 equal=%d' % (1 if same else 0))
sys.exit(0 if same else 1)
