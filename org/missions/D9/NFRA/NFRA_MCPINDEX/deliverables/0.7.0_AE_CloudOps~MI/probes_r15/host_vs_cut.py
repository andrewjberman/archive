"""host_vs_cut.py <deploy-only gateway dir (native)> <host_read.txt> <expected changed, comma-separated>: byte census, host vs the cut."""
import hashlib
import os
import sys
root, hr, exp = sys.argv[1], sys.argv[2], set(sys.argv[3].split(","))
host, sec = {}, False
for ln in open(hr, encoding="utf-8").read().splitlines():
    if ln == "---HASHES":
        sec = True
        continue
    if sec and "  " in ln:
        h, p = ln.split("  ", 1)
        host[p] = h
cut = {}
for top in ("app", "deploy"):
    for dp, dn, fn in os.walk(os.path.join(root, top)):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for x in fn:
            if x.endswith((".log", ".pyc")):
                continue
            p = os.path.join(dp, x)
            cut[os.path.relpath(p, root).replace(os.sep, "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
for x in ("requirements.txt", "identity_tool_allowlist.txt"):
    p = os.path.join(root, x)
    if os.path.exists(p):
        cut[x] = hashlib.sha256(open(p, "rb").read()).hexdigest()
# r15 (adapted this act): the deploy stages lib/ and app/refs/{partner_roster,scopes}.json from the checkout it runs in, so the census adds lib/ (argv[4] = the tree's lib dir) and reads the staged refs from the tree (argv[5] = tree root)
if len(sys.argv) > 4:
    for dp, dn, fn in os.walk(sys.argv[4]):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for x in fn:
            if x not in ("opal_naming.py", "trading_calendar.py") or dp != sys.argv[4]:
                continue
            p = os.path.join(dp, x)
            cut["lib/" + os.path.relpath(p, sys.argv[4]).replace(os.sep, "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
if len(sys.argv) > 5:
    for rel, src in (("app/refs/partner_roster.json", "data/mdpf/config/partner_roster.json"), ("app/refs/scopes.json", "infra/logic/registry/scopes.json")):
        cut[rel] = hashlib.sha256(open(os.path.join(sys.argv[5], src), "rb").read()).hexdigest()
hostc = {k: v for k, v in host.items() if not k.startswith("dashboard/")}
assert cut and hostc, ("ZERO DENOMINATOR", len(cut), len(hostc))
common = set(cut) & set(hostc)
diff = sorted(k for k in common if cut[k] != hostc[k])
print("cut files %d; host non-dashboard files %d; common %d; byte-identical %d; DIFFER %d: %s" % (len(cut), len(hostc), len(common), len(common) - len(diff), len(diff), diff))
print("cut-only %d %s; host-only %d %s" % (len(set(cut) - set(hostc)), sorted(set(cut) - set(hostc)), len(set(hostc) - set(cut)), sorted(set(hostc) - set(cut))))
print("EXPECTED CHANGED SET %s: %s" % (sorted(exp), "MATCH" if set(diff) == exp and not (set(cut) ^ set(hostc)) else "MISMATCH"))
