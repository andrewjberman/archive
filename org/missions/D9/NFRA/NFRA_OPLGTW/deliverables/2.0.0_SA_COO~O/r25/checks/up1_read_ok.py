import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
ok = (d.get("terminal_status") in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED")
      and isinstance(d.get("overlapped_restart"), bool)
      and str(d.get("execution_start_utc", "")).startswith("2026-10-07T01:")
      and bool(d.get("execution_arn_sha256")))
sys.exit(0 if ok else 1)
