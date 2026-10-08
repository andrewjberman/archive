"""E-Y4 leg 3 on an EXTRACTED deployed zip: search every text member with check_624's TOKEN regex.

Usage: python -I zip_trace.py <extracted_zip_dir> [plant]
"""
import os
import re
import sys

root = sys.argv[1]
plant = len(sys.argv) > 2
TOKEN = re.compile(r"""fixtures[/\\]har|["']har["']|FIXTURE_MANIFEST""")
hits, n = [], 0
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith((".py", ".json", ".sh", ".txt")):
            continue
        n += 1
        path = os.path.join(dp, f)
        if TOKEN.search(open(path, encoding="utf-8", errors="replace").read()):
            hits.append(os.path.relpath(path, root))
if plant:
    n += 1
    if TOKEN.search('open("fixtures/har/status_ok.json").read()\n'):
        hits.append("planted_runtime_reader.py")
print(("PLANT " if plant else "") + "zip trace: %d reader(s) across %d text members %s" % (len(hits), n, hits))
