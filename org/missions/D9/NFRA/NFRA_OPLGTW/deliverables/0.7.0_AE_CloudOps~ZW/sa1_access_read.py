"""OG-sa-1 step 1, as amended A1 (msg 34234, order @13f6bb6c7f): ONE account read through the MAIN TREE's sa browser profile.

Replaces sa1_access_probe.py, which built the whole Publisher (token resolution from Secrets Manager / DPAPI, and a bundle
SEED into the profile) -- more than A1 allows. This reads the ACCOUNT state only:
  - opens the harvester's own TabSession on the main tree's browser-profiles/sa (one Chrome launch, one origin page load:
    the session's own construction, counted and reported, not hidden),
  - reads the profile's own user_id cookie (a bool is recorded, never the value),
  - makes ONE request: GET /api/v3/account/<id>/info?include=proSubscription through the tab (the endpoint sa_rest_fetch.check
    uses), records the status and data.type and the number of subscription items, never the body or the id,
  - closes the tab.
No stored bundle is read or seeded, no Secrets Manager call, no sign-in, nothing is copied from this profile anywhere.

usage (cwd = the runner pin's worktree, so the TabSession read is the code the runner runs):
  python sa1_access_read.py --profile-root <main tree browser-profiles> --out <json>
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())

from lib.opal_data_harvest.publishers import TAB_ORIGINS  # noqa: E402
from lib.opal_data_harvest.tab_transport import TabSession  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--profile-root", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

origin = TAB_ORIGINS["sa"]
result = {"profile_root": args.profile_root, "origin": origin, "chrome_launches": 0, "origin_page_loads": 0,
          "account_requests": 0, "read_at": None, "profile_has_user_id": None, "http_status": None, "data_type": None,
          "subscription_items": None, "error": None}
inner = None
try:
    if not (Path(args.profile_root) / "sa").is_dir():
        raise RuntimeError("no sa profile directory under the profile root; nothing launched")
    result["chrome_launches"] = 1
    result["origin_page_loads"] = 1  # TabSession.__init__ launches the persistent context and loads the origin
    inner = TabSession("sa", args.profile_root, origin)
    ids = {str(c.get("value")) for c in inner.context.cookies([origin]) if c.get("name") == "user_id" and c.get("value")}
    result["profile_has_user_id"] = len(ids) == 1
    if len(ids) == 1:
        uid = next(iter(ids))
        result["read_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        result["account_requests"] = 1
        resp = inner.get(origin + "/api/v3/account/%s/info?include=proSubscription" % uid, headers={"Accept": "application/json"})
        result["http_status"] = int(resp.status_code if hasattr(resp, "status_code") else resp.status)
        try:
            body = json.loads(resp.text)
            result["data_type"] = (body.get("data") or {}).get("type")
            result["subscription_items"] = sum(1 for i in (body.get("included") or []) if "ubscription" in str(i.get("type")))
        except Exception as exc:  # noqa: BLE001 - the body is not echoed
            result["error"] = "body not JSON (%s)" % type(exc).__name__
except Exception as exc:  # noqa: BLE001
    result["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
finally:
    if inner is not None:
        try:
            inner.close()
        except Exception as exc:  # noqa: BLE001
            result["close_error"] = type(exc).__name__
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(result, indent=1, sort_keys=True))
