"""OG-rl-15 R45 control (the form's fetch control): count bun's install-cache entries (top level and one level down) whose creation time OR modified time is at or after a start time.
usage: python r29_bun_cache_count.py <deploy_started_utc, e.g. 2026-10-07T21:00:00Z> <out.json> [<cache dir>]
Writes {"deploy_started_utc", "entries_counted", "entries_touched_since_start", "basis"} to <out.json> (Phase B writes RL14_BUN_CACHE.json) and prints the same.
READ-ONLY: os.scandir and os.stat only. It never runs bun and never opens a socket. The cache dir defaults the way ops/bun_cache_precheck.py does ($BUN_INSTALL_CACHE_DIR, else
$BUN_INSTALL/install/cache, else ~/.bun/install/cache). The cache path is not written to the output (it carries the user name).
Creation time: st_ctime on Windows (file creation time) and st_birthtime where the platform has it; modified time: st_mtime. An entry is touched when EITHER is >= the start.
Exit 0 always when the count was made; the CALLER compares entries_touched_since_start to 0 (above 0 is a fetch: roll back, BLOCKING row)."""
import datetime
import json
import os
import sys

start_s, out = sys.argv[1], sys.argv[2]
cache = sys.argv[3] if len(sys.argv) > 3 else (os.environ.get("BUN_INSTALL_CACHE_DIR") or (os.path.join(os.environ["BUN_INSTALL"], "install", "cache") if os.environ.get("BUN_INSTALL") else os.path.join(os.path.expanduser("~"), ".bun", "install", "cache")))
t0 = datetime.datetime.strptime(start_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()
if not os.path.isdir(cache):
    print("ERROR: cache directory absent")
    sys.exit(2)


def touched(st):
    created = getattr(st, "st_birthtime", None)
    if created is None:
        created = st.st_ctime            # Windows: creation time
    return created >= t0 or st.st_mtime >= t0


counted = hit = 0
for e in os.scandir(cache):
    counted += 1
    hit += 1 if touched(e.stat(follow_symlinks=False)) else 0
    if e.is_dir(follow_symlinks=False):
        for c in os.scandir(e.path):
            counted += 1
            hit += 1 if touched(c.stat(follow_symlinks=False)) else 0
doc = {"deploy_started_utc": start_s, "entries_counted": counted, "entries_touched_since_start": hit,
       "basis": "top level and one level down of bun's install cache; creation time OR modified time >= deploy_started_utc"}
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(json.dumps(doc, sort_keys=True))
