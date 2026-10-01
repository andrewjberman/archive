"""HVST-ai-2 helper: ONE renewal through the collector's existing path (auth.SessionManager.refresh), run from this
worktree against the main tree's runtime. Prints the event stream and the saved bundle's cookie NAMES only."""
import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
from lib.opal_data_harvest.auth import SessionManager

ROOT = Path(sys.argv[1])
mgr = SessionManager(ROOT, lambda e: print(json.dumps(e), flush=True))
env = mgr.refresh("ft")
print(json.dumps({"renewed": True, "captured_at": env.get("captured_at"), "cookie_names": sorted(env["bundle"])[:80]}))
