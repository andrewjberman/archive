set -u
# IRPT_ANLREQ TO-APPLY-R34N step 5 (READ ONLY): V1 (d) the census of the r34m and r34n roots, (e) the Opal imports, (f) the pool pin and opal_pricing. Runs as ec2-user. Writes nothing.
R32=/opt/irpt-resident/0485393f3a-r34m
R34=/opt/irpt-resident/0485393f3a-r34n
PYD=/opt/investor-reporting-ycharts/pydeps
sudo -u ec2-user -H env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 - "$R32" "$R34" "$PYD" <<'PYEOF'
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
print("V1d full tree: r34m files %d, r34n files %d; changed %d, only in r34n %d, only in r34m %d" % (len(a), len(b), len(changed), len(added), len(removed)))
print("V1d PACKAGE scope (not under a pydeps top-level name, no bytecode): %d changed, %d only in r34n, %d only in r34m" % (len(cs["pkg"]), len(ads["pkg"]), len(rms["pkg"])))
print("V1d changed (package): %s" % cs["pkg"])
print("V1d only in r34n (package): %s" % ads["pkg"])
print("V1d only in r34m (package): %s" % rms["pkg"])
print("V1d LIBRARY scope (under a pydeps top-level name): %d changed, %d only in r34n, %d only in r34m" % (len(cs["lib"]), len(ads["lib"]), len(rms["lib"])))
print("V1d only in r34m (library): %s" % rms["lib"][:20])
print("V1d changed (library) names: %s" % sorted({x.split("/")[0] for x in cs["lib"]})[:30])
print("V1d BYTECODE: %d changed, %d only in r34n, %d only in r34m" % (len(cs["pyc"]), len(ads["pyc"]), len(rms["pyc"])))
print("V1d only in r34m (bytecode): %s" % rms["pyc"][:12])

sub = ["", "ycharts/research", "ycharts/generate", "ycharts/session", "intake", "ops", "reports", "lib"]
sys.path[:0] = [os.path.join(r34, s) if s else r34 for s in sub]
sys.path.append(pyd)
for name in ("swap_pass", "yahoo_history_days", "yfinance_check", "resident_session", "resident_worker", "price_transport_ycharts", "operation_lease", "price_form_ycharts", "ycharts_client"):
    try:
        m = __import__(name)
        print("V1g IMPORT OK %s from %s" % (name, os.path.relpath(m.__file__, r34).replace(os.sep, "/")))
    except Exception as e:
        print("V1g IMPORT FAIL %s %s missing_module=%s" % (name, type(e).__name__, getattr(e, "name", None)))
print("V1e intake/yfinance_check.py present in the r34n root: %s" % os.path.isfile(os.path.join(r34, "intake/yfinance_check.py")))

bind = json.load(open(os.path.join(r34, "reports/resident_bindings.json"), encoding="utf-8"))
pool = os.path.normpath(os.path.join(r34, "reports", bind["opal_swap_pool"]["path"]))
sha = hashlib.sha256(open(pool, "rb").read()).hexdigest()
print("V1f pool file %s sha256 %s binding %s EQUAL=%s" % (os.path.relpath(pool, r34).replace(os.sep, "/"), sha, bind["opal_swap_pool"]["sha256"], sha == bind["opal_swap_pool"]["sha256"]))
print("V1f opal_pricing enabled=%s tiers=%s" % (bind["opal_pricing"]["enabled"], bind["opal_pricing"].get("tiers")))
print("V1f ycharts_window_budget=%s" % json.dumps(bind.get("ycharts_window_budget"), sort_keys=True))
print("V1f price_transport_ycharts.py present in the r34n root: %s" % os.path.isfile(os.path.join(r34, "ycharts/research/price_transport_ycharts.py")))

# (e) the packager binding as closed words, and every other binding key against the r34m root's bindings (nothing printed of a URL or a secret value)
old = json.load(open(os.path.join(r32, "reports/resident_bindings.json"), encoding="utf-8"))
pk_new, pk_old = bind.get("packager", {}), old.get("packager", {})
host = pk_new.get("api_base", "")
alias = host == "https://opalinvest.dev"
print("V1e packager api_base=%s (r34m api_base=%s) secret_name=%s packager members=%s" % ("alias" if alias else "other", "alias" if pk_old.get("api_base") == "https://opalinvest.dev" else "other", "unchanged" if pk_new.get("secret_name") == pk_old.get("secret_name") else "changed", sorted(pk_new)))
others_new = {k: v for k, v in bind.items() if k != "packager"}
others_old = {k: v for k, v in old.items() if k != "packager"}
diff_keys = sorted(k for k in set(others_new) | set(others_old) if others_new.get(k) != others_old.get(k))
print("V1e other binding keys: %d compared, %d differ %s; packager keys other than api_base differing: %s" % (len(set(others_new) | set(others_old)), len(diff_keys), diff_keys, sorted(k for k in set(pk_new) | set(pk_old) if k != "api_base" and pk_new.get(k) != pk_old.get(k))))
PYEOF
