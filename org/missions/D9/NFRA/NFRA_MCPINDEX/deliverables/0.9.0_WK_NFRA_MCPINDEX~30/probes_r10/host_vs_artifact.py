"""host_vs_artifact.py <extracted artifact root (native path)> <host_read.txt>: plane-2 byte census. Asserts a non-zero denominator."""
import hashlib
import os
import sys
root, hr = sys.argv[1], sys.argv[2]
host = {}
sec = False
for ln in open(hr, encoding="utf-8").read().splitlines():
    if ln == "---HASHES":
        sec = True
        continue
    if sec and "  " in ln:
        h, p = ln.split("  ", 1)
        host[p] = h
art = {}
for top in ("app", "deploy", "dashboard"):
    for dp, dn, fn in os.walk(os.path.join(root, top)):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for x in fn:
            if x.endswith((".log", ".pyc")):
                continue
            p = os.path.join(dp, x)
            art[os.path.relpath(p, root).replace(os.sep, "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
for x in ("requirements.txt", "identity_tool_allowlist.txt"):
    p = os.path.join(root, x)
    if os.path.exists(p):
        art[x] = hashlib.sha256(open(p, "rb").read()).hexdigest()
assert art and host, ("ZERO DENOMINATOR", len(art), len(host))
common = set(art) & set(host)
diff = sorted(k for k in common if art[k] != host[k])
print("artifact files %d; host files %d; common %d; byte-identical %d; DIFFER %d %s; artifact-only %d %s; host-only %d %s" % (
    len(art), len(host), len(common), len(common) - len(diff), len(diff), diff, len(set(art) - set(host)), sorted(set(art) - set(host)),
    len(set(host) - set(art)), sorted(set(host) - set(art))))
