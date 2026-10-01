"""HVST-ai-2 experiment: the collector's existing ft renewal (auth.SessionManager.refresh -> harvest_local_session ->
ft_harvest_session.py) with ONE string changed in a scratch copy of the scripts directory: the harvester's forced
`Chrome/126.0.0.0` User-Agent becomes the installed Chrome's own (`Chrome/154.0.0.0`, as the profile's navigator.userAgent
reports it). Everything else -- the login steps, any challenge handling, the vault write -- is the repository's own script.
Prints the event stream and cookie NAMES only.
  python ai2_renew_ua.py <runtime_root> <scratch_dir>
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, ".")
import lib.opal_data_harvest.auth as auth  # noqa: E402

runtime, scratch = Path(sys.argv[1]), Path(sys.argv[2])
if scratch.exists():
    shutil.rmtree(scratch)
shutil.copytree(auth.SCRIPTS, scratch, ignore=shutil.ignore_patterns("__pycache__"))
target = scratch / "ft_harvest_session.py"
text = target.read_text(encoding="utf-8")
patched, n = re.subn(r"Chrome/126\.0\.0\.0", "Chrome/154.0.0.0", text)
assert n == 1, n
target.write_text(patched, encoding="utf-8")
auth.SCRIPTS = scratch
env = auth.SessionManager(runtime, lambda e: print(json.dumps(e), flush=True)).refresh("ft")
print(json.dumps({"renewed": True, "captured_at": env.get("captured_at"), "ua_patched": True}))
