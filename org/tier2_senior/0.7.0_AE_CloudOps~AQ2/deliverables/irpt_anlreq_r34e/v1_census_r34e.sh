set -u
# IRPT_ANLREQ TO-APPLY-R34E step 5 (READ ONLY): V1 (d) the census of the r34c and r34d roots, (e) the Opal imports, (f) the pool pin and opal_pricing. Runs as ec2-user. Writes nothing.
R32=/opt/irpt-resident/0485393f3a-r34c
R34=/opt/irpt-resident/0485393f3a-r34e
PYD=/opt/investor-reporting-ycharts/pydeps
/usr/bin/python3.12 - "$R32" "$R34" "$PYD" <<'PYEOF'
import hashlib, json, os, sys
r32, r34, pyd = sys.argv[1:4]

def listing(root):
    out = {}
    for dp, dn, fn in os.walk(root, followlinks=False):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if os.path.islink(p):
                out[rel] = "LINK:" + os.readlink(p)
                continue
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            out[rel] = h.hexdigest()
    return out

a, b = listing(r32), listing(r34)
changed = sorted(k for k in a if k in b and a[k] != b[k])
added = sorted(k for k in b if k not in a)
removed = sorted(k for k in a if k not in b)
libnames = set(os.listdir(pyd))
def kind(rel):
    if "__pycache__" in rel or rel.endswith(".pyc"):
        return "pyc"
    return "lib" if rel.split("/")[0] in libnames else "pkg"
def split(keys):
    out = {"pkg": [], "lib": [], "pyc": []}
    for k in keys:
        out[kind(k)].append(k)
    return out
cs, ads, rms = split(changed), split(added), split(removed)
print("V1d full tree: r34c files %d, r34e files %d; changed %d, only in r34e %d, only in r34c %d" % (len(a), len(b), len(changed), len(added), len(removed)))
print("V1d PACKAGE scope (not under a pydeps top-level name, no bytecode): %d changed, %d only in r34e, %d only in r34c" % (len(cs["pkg"]), len(ads["pkg"]), len(rms["pkg"])))
print("V1d changed (package): %s" % cs["pkg"])
print("V1d only in r34e (package): %s" % ads["pkg"])
print("V1d only in r34c (package): %s" % rms["pkg"])
print("V1d LIBRARY scope (under a pydeps top-level name): %d changed, %d only in r34e, %d only in r34c" % (len(cs["lib"]), len(ads["lib"]), len(rms["lib"])))
print("V1d only in r34c (library): %s" % rms["lib"][:20])
print("V1d changed (library) names: %s" % sorted({x.split("/")[0] for x in cs["lib"]})[:30])
print("V1d BYTECODE: %d changed, %d only in r34e, %d only in r34c" % (len(cs["pyc"]), len(ads["pyc"]), len(rms["pyc"])))
print("V1d only in r34c (bytecode): %s" % rms["pyc"][:12])

sub = ["", "ycharts/research", "ycharts/generate", "ycharts/session", "intake", "ops", "reports", "lib"]
sys.path[:0] = [os.path.join(r34, s) if s else r34 for s in sub]
sys.path.append(pyd)
for name in ("swap_pass", "yahoo_history_days", "yfinance_check", "resident_session"):
    try:
        m = __import__(name)
        print("V1e IMPORT OK %s from %s" % (name, os.path.relpath(m.__file__, r34).replace(os.sep, "/")))
    except Exception as e:
        print("V1e IMPORT FAIL %s %s" % (name, type(e).__name__))
print("V1e intake/yfinance_check.py present in the r34e root: %s" % os.path.isfile(os.path.join(r34, "intake/yfinance_check.py")))

bind = json.load(open(os.path.join(r34, "reports/resident_bindings.json"), encoding="utf-8"))
pool = os.path.normpath(os.path.join(r34, "reports", bind["opal_swap_pool"]["path"]))
sha = hashlib.sha256(open(pool, "rb").read()).hexdigest()
print("V1f pool file %s sha256 %s binding %s EQUAL=%s" % (os.path.relpath(pool, r34).replace(os.sep, "/"), sha, bind["opal_swap_pool"]["sha256"], sha == bind["opal_swap_pool"]["sha256"]))
print("V1f opal_pricing enabled=%s" % bind["opal_pricing"]["enabled"])
PYEOF
