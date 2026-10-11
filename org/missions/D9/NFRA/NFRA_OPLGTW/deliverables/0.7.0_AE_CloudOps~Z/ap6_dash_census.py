"""OG-ap-6 B1 step 1 addendum: characterise the host's dashboard/ extras.

The shipped-file md5 comparison already read 104 of 104 identical with 0 mismatch. This
program answers only ONE question the extras list raised: of the dashboard/ assets on the
host, which are REFERENCED by the live dashboard/index.html and which are orphans from an
earlier bundle. dashboard/ is shipped from mcportal's dist, not from the gateway's git tree,
so it is outside this order's artifact; the census exists so the extras can be named exactly
rather than guessed at. Read-only: it opens files and prints names.

Matching is by BASENAME, which is sound here because Vite emits content-hashed, unique asset
filenames; a basename collision across directories would show up as a referenced name
appearing twice in DASH_PRESENT.
"""
import hashlib
import os
import re

os.chdir("/opt/opal-gateway")

idx = "dashboard/index.html"
if not os.path.exists(idx):
    print("DASH_INDEX absent")
    raise SystemExit(0)

html = open(idx, "rb").read().decode("utf-8", "replace")
print("DASH_INDEX_MD5 %s bytes=%d" % (hashlib.md5(html.encode("utf-8")).hexdigest(), len(html)))

ref_names = set()
for m in re.finditer(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']', html):
    ref_names.add(os.path.basename(m.group(1).split("?")[0]))

present = []
for root, ds, fs in os.walk("dashboard"):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        present.append(os.path.join(root, f).replace(os.sep, "/"))
present.sort()

referenced = sorted(p for p in present if os.path.basename(p) in ref_names)
orphans = sorted(p for p in present if p != idx and os.path.basename(p) not in ref_names)

print("DASH_INDEX_REFS %d %s" % (len(ref_names), sorted(ref_names)))
print("DASH_PRESENT %d %s" % (len(present), present))
print("DASH_REFERENCED_ON_DISK %d %s" % (len(referenced), referenced))
print("DASH_ORPHANS %d %s" % (len(orphans), orphans))
print("DENOMINATOR dashboard files walked %d = index.html 1 + referenced %d + orphans %d"
      % (len(present), len(referenced), len(orphans)))
