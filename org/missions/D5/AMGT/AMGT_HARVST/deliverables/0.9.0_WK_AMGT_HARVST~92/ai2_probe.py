"""HVST-ai-2 diagnosis probe (<= 30 ft requests): hold ONE ft session in the main tree's profile at a LOW request rate
(one request per --every seconds, alternating an in-tab fetch and a navigation of the same article) and log, per tick,
the page's own isUserLoggedIn flag and the identity cookie's presence, expiry and a sha8 of its value (never the value).
Stops at the first logged-out reading or at --max requests. Usage (a fifth argument `fetch-only` never navigates after the launch):
  OPAL_HARVEST_PROFILE_ROOT=<main>/.runtime/opal-data-harvest/browser-profiles python ai2_probe.py <runtime_root> <out.jsonl>
"""
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
from lib.opal_data_harvest.publishers import ft_page_state, seed_cookies
from lib.opal_data_harvest.storage import SessionVault
from lib.opal_data_harvest.tab_transport import TabSession, default_profile_root

RUNTIME, OUT = Path(sys.argv[1]), Path(sys.argv[2])
EVERY = int(sys.argv[3]) if len(sys.argv) > 3 else 240
MAX = int(sys.argv[4]) if len(sys.argv) > 4 else 22
FETCH_ONLY = len(sys.argv) > 5 and sys.argv[5] == "fetch-only"   # no navigation after the one the launch makes
URL = "https://www.ft.com/content/47019489-f00e-4c96-bb79-5c628c89b3a1"


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S")


def snap(tab):
    out = {}
    for c in tab.context.cookies(["https://www.ft.com"]):
        if c["name"].startswith("FTSession"):
            out[c["name"]] = {"exp": c.get("expires"), "sha8": hashlib.sha256(c["value"].encode()).hexdigest()[:8]}
    return out


def log(row):
    row["at"] = now()
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps(row), flush=True)


bundle = SessionVault(RUNTIME).load("ft")["bundle"]
tab = TabSession("ft", str(default_profile_root()), "https://www.ft.com")
log({"step": "opened", "profile": str(tab.profile), "logged_in_on_load": tab.logged_in(), "jar": snap(tab), "requests": 1})
log({"step": "seed", "seeded": tab.seed(seed_cookies("ft", bundle)), "jar": snap(tab)})
requests = 1
try:
    for i in range(1, MAX):
        mode = "fetch" if (i % 2 or FETCH_ONLY) else "goto"
        if mode == "fetch":
            r = tab.get(URL, headers={"Referer": "https://www.ft.com/"})
            state = ft_page_state(r.text)
        else:
            tab.page.goto(URL, wait_until="domcontentloaded")
            state = {"logged_in": tab.logged_in(), "barrier": None}
        requests += 1
        row = {"step": i, "mode": mode, "requests": requests, "state": state, "jar": snap(tab)}
        log(row)
        if state["logged_in"] is False:
            log({"step": "DEAD", "after_requests": requests})
            break
        time.sleep(EVERY)
finally:
    tab.close()
