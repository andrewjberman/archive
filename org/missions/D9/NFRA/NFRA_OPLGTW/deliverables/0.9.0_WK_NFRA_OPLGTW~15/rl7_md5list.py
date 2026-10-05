"""OG-rl-6 PHASE C-A: print the 'md5  relpath' list of what the deploy tarball ships from a gateway tree (app/, deploy/, requirements.txt,
identity_tool_allowlist.txt; minus __pycache__/*.log/.env/audit.jsonl as deploy-to-ec2.sh excludes). usage: python rl7_md5list.py <gateway dir>"""
import hashlib
import os
import sys
root = sys.argv[1]
out = []
for top in ("app", "deploy"):
    for r, ds, fs in os.walk(os.path.join(root, top)):
        ds[:] = [d for d in ds if d != "__pycache__"]
        for f in fs:
            if f.endswith(".log") or f in (".env", "audit.jsonl", ".token_cache") or f.endswith(".pyc"):
                continue
            p = os.path.join(r, f)
            out.append((os.path.relpath(p, root).replace(chr(92), "/"), hashlib.md5(open(p, "rb").read()).hexdigest()))
for f in ("requirements.txt", "identity_tool_allowlist.txt"):
    out.append((f, hashlib.md5(open(os.path.join(root, f), "rb").read()).hexdigest()))
for p, h in sorted(out):
    print("%s  %s" % (h, p))
