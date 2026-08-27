#!/usr/bin/env python3
"""L1-oqif-1/2 + L1-gqhb-3 CORRECTED.

My first file probe regexed every portal id containing a '/' and called the result file paths.
It swept up `endpointurl:/api/general/...` -- URL ROUTES, a different id space -- and returned
4,978 where the file-grain population is far smaller. Extracting an id space BY PATTERN instead
of BY ITS DECLARED TYPE is the same class as every other defect found in me today.

This version keys on node_type, which the store declares, and measures the symbol->file roll-up
as a RELATION with its fan-out.
"""
import os
from collections import Counter, defaultdict

import kuzu

conn = kuzu.Connection(kuzu.Database(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_nessie_db"))


def q(cypher):
    r = conn.execute(cypher)
    out = []
    while r.has_next():
        out.append(r.get_next())
    return out


rows = q("MATCH (n:CloudNode) WHERE n.layer='portal' RETURN n.node_id, n.node_type")
print("portal layer nodes: %d" % len(rows))

# FILE grain: the store DECLARES it as node_type 'Module'
modules = {nid for nid, nt in rows if nt == "Module"}
mod_paths = {nid.split(":", 1)[1] for nid in modules if ":" in nid}
print()
print("=== FILE grain, taken from the DECLARED node_type 'Module' (not a regex) ===")
print("  Module nodes: %d -> %d distinct paths" % (len(modules), len(mod_paths)))
print("  samples:", sorted(mod_paths)[:3])

# the finer grains carry their file before the '#'
URL_PREFIXES = {"endpointurl", "endpoint"}
sym_to_file = defaultdict(set)
symbols = set()
for nid, nt in rows:
    if ":" not in nid:
        continue
    pref, rest = nid.split(":", 1)
    if pref in URL_PREFIXES:
        continue
    head = rest.split("#", 1)[0]
    # a file-shaped head has a slash and an extension
    if "/" in head and "." in head.rsplit("/", 1)[-1]:
        symbols.add(nid)
        sym_to_file[nid].add(head)

all_files_referenced = set()
for v in sym_to_file.values():
    all_files_referenced |= v

print()
print("=== SYMBOL -> FILE ROLL-UP, measured as a RELATION ===")
print("  symbol-grain nodes carrying a file head : %d" % len(symbols))
print("  distinct files they roll up to          : %d" % len(all_files_referenced))
fan = Counter(len(v) for v in sym_to_file.values())
print("  fan-out distribution (targets per symbol):", dict(fan))
per_file = Counter()
for s, fs in sym_to_file.items():
    for f in fs:
        per_file[f] += 1
print("  REVERSE fan-in (symbols per file): max=%d  mean=%.1f"
      % (max(per_file.values()), sum(per_file.values()) / max(1, len(per_file))))
top = per_file.most_common(3)
print("  heaviest files:", [(f[:52], n) for f, n in top])
print()
print("  >> THE ROLL-UP IS A RELATION: %d symbols -> %d files. Collapsing it to a function"
      % (len(symbols), len(all_files_referenced)))
print("     would discard a mean fan-in of %.1f symbols per file."
      % (sum(per_file.values()) / max(1, len(per_file))))

# crossing: do those files exist on the filesystem plane?
repo = set()
for root, dirs, files in os.walk("portal/src"):
    dirs[:] = [d for d in dirs if d not in ("node_modules", "dist", ".git")]
    for fn in files:
        repo.add(os.path.join(root, fn).replace("\\", "/"))
print()
print("=== CROSSING: kuzu file grain  vs  the FILESYSTEM plane ===")
print("  portal/src working tree files : %d" % len(repo))
print("  Module paths that EXIST on disk: %d of %d (%.1f%%)"
      % (len(mod_paths & repo), len(mod_paths), 100.0 * len(mod_paths & repo) / max(1, len(mod_paths))))
print("  referenced files that EXIST    : %d of %d (%.1f%%)"
      % (len(all_files_referenced & repo), len(all_files_referenced),
         100.0 * len(all_files_referenced & repo) / max(1, len(all_files_referenced))))
missing = sorted(all_files_referenced - repo)[:4]
print("  sample referenced-but-absent   :", missing)
print()
print("  NEGATIVE CONTROL: URL-route ids must NOT resolve as files")
urls = {nid.split(":", 1)[1] for nid, nt in rows if nid.split(":", 1)[0] in URL_PREFIXES}
print("     url ids: %d ; url n repo = %d -> %s"
      % (len(urls), len(urls & repo), "HOLDS" if not (urls & repo) else "*** FAILED ***"))
print("  POSITIVE CONTROL: repo non-empty and intersection machinery works: %s"
      % (len(mod_paths & repo) > 0))
