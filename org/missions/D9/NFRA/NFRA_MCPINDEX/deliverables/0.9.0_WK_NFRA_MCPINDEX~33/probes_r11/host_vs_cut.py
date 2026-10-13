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
hostc = {k: v for k, v in host.items() if not k.startswith("dashboard/")}
assert cut and hostc, ("ZERO DENOMINATOR", len(cut), len(hostc))
common = set(cut) & set(hostc)
diff = sorted(k for k in common if cut[k] != hostc[k])
print("cut files %d; host non-dashboard files %d; common %d; byte-identical %d; DIFFER %d: %s" % (len(cut), len(hostc), len(common), len(common) - len(diff), len(diff), diff))
print("cut-only %d %s; host-only %d %s" % (len(set(cut) - set(hostc)), sorted(set(cut) - set(hostc)), len(set(hostc) - set(cut)), sorted(set(hostc) - set(cut))))
print("EXPECTED CHANGED SET %s: %s" % (sorted(exp), "MATCH" if set(diff) == exp and not (set(cut) ^ set(hostc)) else "MISMATCH"))
