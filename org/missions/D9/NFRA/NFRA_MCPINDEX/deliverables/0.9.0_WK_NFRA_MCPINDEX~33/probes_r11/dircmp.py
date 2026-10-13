"""dircmp.py <a> <b> [--py-only-note]: file-by-file sha256 compare of two extracted trees. Prints counts and the lists."""

import hashlib
import os
import sys


def walk(r):
    d = {}
    for dp, dn, fn in os.walk(r):
        dn[:] = [x for x in dn if x != "__pycache__"]
        for f in fn:
            if f.endswith(".log") or f.endswith(".pyc"):
                continue
            p = os.path.join(dp, f)
            d[os.path.relpath(p, r).replace(os.sep, "/")] = hashlib.sha256(
                open(p, "rb").read()
            ).hexdigest()
    return d


a, b = walk(sys.argv[1]), walk(sys.argv[2])
only_a = sorted(set(a) - set(b))
only_b = sorted(set(b) - set(a))
diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
same = [k for k in set(a) & set(b) if a[k] == b[k]]
def py(ks):
    return sum(1 for k in ks if k.endswith(".py"))
print(
    "A=%s files=%d (py %d); B=%s files=%d (py %d)"
    % (sys.argv[1], len(a), py(a), sys.argv[2], len(b), py(b))
)
print("only in A (%d): %s" % (len(only_a), only_a))
print("only in B (%d): %s" % (len(only_b), only_b))
print("changed (%d): %s" % (len(diff), diff))
print(
    "identical %d of %d (py %d of %d)"
    % (len(same), len(set(a) | set(b)), py(same), py(set(a) | set(b)))
)
