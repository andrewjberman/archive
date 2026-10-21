set -u
# IRPT_ANLREQ TO-APPLY-R34P step 5 (READ ONLY): V1 (d) the census of the r34o and r34p roots, (e) the bindings, (f) the imports, the pool pin and opal_pricing, (h) IRPT_TICKETS_TABLE as a closed word. The python part runs as ec2-user; the environment read runs as root. Writes nothing.
R32=/opt/irpt-resident/0485393f3a-r34o
R34=/opt/irpt-resident/0485393f3a-r34p
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
print("V1d full tree: r34p files %d, r34p files %d; changed %d, only in r34p %d, only in r34o %d" % (len(a), len(b), len(changed), len(added), len(removed)))
print("V1d PACKAGE scope (not under a pydeps top-level name, no bytecode): %d changed, %d only in r34p, %d only in r34o" % (len(cs["pkg"]), len(ads["pkg"]), len(rms["pkg"])))
print("V1d changed (package): %s" % cs["pkg"])
print("V1d only in r34p (package): %s" % ads["pkg"])
print("V1d only in r34o (package): %s" % rms["pkg"])
print("V1d LIBRARY scope (under a pydeps top-level name): %d changed, %d only in r34p, %d only in r34o" % (len(cs["lib"]), len(ads["lib"]), len(rms["lib"])))
print("V1d only in r34o (library): %s" % rms["lib"][:20])
print("V1d changed (library) names: %s" % sorted({x.split("/")[0] for x in cs["lib"]})[:30])
print("V1d BYTECODE: %d changed, %d only in r34p, %d only in r34o" % (len(cs["pyc"]), len(ads["pyc"]), len(rms["pyc"])))
print("V1d only in r34o (bytecode): %s" % rms["pyc"][:12])

sub = ["", "ycharts/research", "ycharts/generate", "ycharts/session", "intake", "ops", "reports", "lib"]
sys.path[:0] = [os.path.join(r34, s) if s else r34 for s in sub]
sys.path.append(pyd)
for name in ("resident_worker", "resident_installed", "resident_session", "opal_producer", "layout_overview", "model_source", "comparables", "ticket_audit_source", "analysis_audit", "swap_pass", "yfinance_check", "price_transport_ycharts"):
    try:
        m = __import__(name)
        print("V1g IMPORT OK %s from %s" % (name, os.path.relpath(m.__file__, r34).replace(os.sep, "/")))
    except Exception as e:
        print("V1g IMPORT FAIL %s %s missing_module=%s" % (name, type(e).__name__, getattr(e, "name", None)))
try:
    import jsonschema  # noqa: F401
    print("V1f import jsonschema on the host: yes")
except Exception:
    print("V1f import jsonschema on the host: no")
print("V1e intake/yfinance_check.py present in the r34p root: %s" % os.path.isfile(os.path.join(r34, "intake/yfinance_check.py")))

bind = json.load(open(os.path.join(r34, "reports/resident_bindings.json"), encoding="utf-8"))
print("V1e opal_map sha256 %s (want 661adac1efa8ee72cd95952f72815dfea90bfe83c4af162ee74daf3d4542143b) EQUAL=%s" % (bind["opal_map"].get("sha256"), bind["opal_map"].get("sha256") == "661adac1efa8ee72cd95952f72815dfea90bfe83c4af162ee74daf3d4542143b"))
prov = bind.get("provenance", {})
print("V1e provenance package_pin %s (want 919bb891fa72dd706493f094c9b4412503fcf42a) EQUAL=%s; files_from_count %s (want 47)" % (prov.get("package_pin"), prov.get("package_pin") == "919bb891fa72dd706493f094c9b4412503fcf42a", prov.get("files_from_count")))
pool = os.path.normpath(os.path.join(r34, "reports", bind["opal_swap_pool"]["path"]))
sha = hashlib.sha256(open(pool, "rb").read()).hexdigest()
print("V1f pool file %s sha256 %s binding %s EQUAL=%s" % (os.path.relpath(pool, r34).replace(os.sep, "/"), sha, bind["opal_swap_pool"]["sha256"], sha == bind["opal_swap_pool"]["sha256"]))
print("V1f opal_pricing enabled=%s tiers=%s" % (bind["opal_pricing"]["enabled"], bind["opal_pricing"].get("tiers")))
print("V1f ycharts_window_budget=%s" % json.dumps(bind.get("ycharts_window_budget"), sort_keys=True))
print("V1f price_transport_ycharts.py present in the r34p root: %s" % os.path.isfile(os.path.join(r34, "ycharts/research/price_transport_ycharts.py")))

# (e) the packager binding as closed words, and every other binding key against the r34o root's bindings (nothing printed of a URL or a secret value)
old = json.load(open(os.path.join(r32, "reports/resident_bindings.json"), encoding="utf-8"))
pk_new, pk_old = bind.get("packager", {}), old.get("packager", {})
host = pk_new.get("api_base", "")
alias = host == "https://opalinvest.dev"
print("V1e packager api_base=%s (r34o api_base=%s) secret_name=%s packager members=%s" % ("alias" if alias else "other", "alias" if pk_old.get("api_base") == "https://opalinvest.dev" else "other", "unchanged" if pk_new.get("secret_name") == pk_old.get("secret_name") else "changed", sorted(pk_new)))
others_new = {k: v for k, v in bind.items() if k != "packager"}
others_old = {k: v for k, v in old.items() if k != "packager"}
diff_keys = sorted(k for k in set(others_new) | set(others_old) if others_new.get(k) != others_old.get(k))
print("V1e other binding keys: %d compared, %d differ %s; packager keys other than api_base differing: %s" % (len(set(others_new) | set(others_old)), len(diff_keys), diff_keys, sorted(k for k in set(pk_new) | set(pk_old) if k != "api_base" and pk_new.get(k) != pk_old.get(k))))
PYEOF

# (e) THE CURE: a fresh interpreter over the r34p root, the registry reader of lib/opal_naming for the two revisions (first 16 hex only), and the packaged registry file
sudo -u ec2-user -H env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 - "$R34" <<'CUREEOF'
import hashlib, os, sys
root = sys.argv[1]
sys.path[:0] = [os.path.join(root, "lib"), root]
import opal_naming
for rev in ("irpt-anlreq-x10-v1", "irpt-dashbd-x10-v1"):
    print("V1cure %s policy_sha256 first16 %s from %s" % (rev, opal_naming.reporting_policy(rev)["policy_sha256"][:16], os.path.relpath(opal_naming.__file__, root).replace(os.sep, "/")))
reg = os.path.join(root, "infra/logic/registry/reporting_policies.json")
print("V1cure packaged registry file sha256 %s (want 229eca2d1ec7c6f8bf93a106ba788a213a19c189809f582b6d2a185b7adeb982)" % hashlib.sha256(open(reg, "rb").read()).hexdigest())
CUREEOF
UNIT=irpt-analysis-resident.service
PID=$(systemctl show -p MainPID --value $UNIT)
UN=$(systemctl show -p Environment --value $UNIT | tr ' ' '\n' | grep -c '^IRPT_TICKETS_TABLE=')
PR=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -c '^IRPT_TICKETS_TABLE=')
CTL=$(tr '\0' '\n' < /proc/$PID/environ 2>/dev/null | grep -c '^PATH=')
echo "V1h IRPT_TICKETS_TABLE unit=$([ "$UN" -gt 0 ] && echo set || echo unset) process(pid $PID)=$([ "$PR" -gt 0 ] && echo set || echo unset) (value never printed)"
echo "V1h control: process environment readable, PATH= entries=$CTL (must be 1 or more for the unset reading to count)"
