"""OG-rl-15 amendment A2 (C1): total bytes of every file in bun's install cache, to full depth, and the file count. READ-ONLY (os.walk + os.lstat; never runs bun, never opens a socket).
usage: python r29_bun_cache_size.py <label> [<cache dir>]   -> prints one line  R28C_CACHE_SIZE {"label", "read_at", "bytes", "files", "dirs"}
The cache dir defaults the way ops/bun_cache_precheck.py and r29_bun_cache_count.py do. The cache path is not printed (it carries the user name)."""
import datetime
import json
import os
import sys

label = sys.argv[1]
cache = sys.argv[2] if len(sys.argv) > 2 else (os.environ.get("BUN_INSTALL_CACHE_DIR") or (os.path.join(os.environ["BUN_INSTALL"], "install", "cache") if os.environ.get("BUN_INSTALL") else os.path.join(os.path.expanduser("~"), ".bun", "install", "cache")))
if not os.path.isdir(cache):
    print("ERROR: cache directory absent")
    sys.exit(2)
total = files = dirs = 0
for root, ds, fs in os.walk(cache, followlinks=False):
    dirs += len(ds)
    for f in fs:
        files += 1
        total += os.lstat(os.path.join(root, f)).st_size
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print("R28C_CACHE_SIZE " + json.dumps({"label": label, "read_at": now, "bytes": total, "files": files, "dirs": dirs}, sort_keys=True))
