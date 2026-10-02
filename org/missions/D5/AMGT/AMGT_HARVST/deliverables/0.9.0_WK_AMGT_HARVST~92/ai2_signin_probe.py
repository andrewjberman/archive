"""HVST-ai-2 experiment: sign in to ft INSIDE the persistent profile (the browser the collector then fetches with) instead of
seeding the profile from the harvester's bundle. The harvester (ft_harvest_session.py) logs in from a fresh non-persistent
Chrome that presents a forced `Chrome/126.0.0.0` User-Agent; the profile's Chrome presents its own. The credentials come
from Secrets by the collector's own name (astn/ft/credentials) and are never printed. No captcha solver is called: a
challenge is reported and the script ends. Prints the identity cookie's presence / expiry / sha8 only.

  OPAL_HARVEST_PROFILE_ROOT=<main>/.runtime/opal-data-harvest/browser-profiles python ai2_signin_probe.py
"""
import hashlib
import json
import sys

sys.path.insert(0, ".")
from lib.opal_data_harvest.credentials import SecretsReader  # noqa: E402
from lib.opal_data_harvest.tab_transport import TabSession, default_profile_root  # noqa: E402


def jar(tab):
    return {c["name"]: {"exp": c.get("expires"), "sha8": hashlib.sha256(c["value"].encode()).hexdigest()[:8]}
            for c in tab.context.cookies(["https://www.ft.com"]) if c["name"].startswith("FTSession")}


creds = SecretsReader().read_credentials("ft")
tab = TabSession("ft", str(default_profile_root()), "https://www.ft.com")
try:
    print(json.dumps({"step": "opened", "logged_in": tab.logged_in(), "jar": jar(tab), "ua": tab.page.evaluate("navigator.userAgent")}), flush=True)
    page = tab.page
    page.goto("https://accounts.ft.com/login", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2500)
    page.locator("#enter-email").fill(creds["username"])
    page.locator("#enter-email-next").click(timeout=15000)
    page.wait_for_timeout(2500)
    page.locator("#enter-password").fill(creds["password"])
    page.locator("#sign-in-button").click(timeout=15000)
    page.wait_for_timeout(6000)
    challenge = [f.url[:60] for f in page.frames if "hcaptcha.com" in f.url]
    print(json.dumps({"step": "submitted", "url": page.url[:60], "hcaptcha_frames": len(challenge)}), flush=True)
    page.goto("https://www.ft.com", wait_until="load")
    page.wait_for_timeout(2500)
    print(json.dumps({"step": "after", "logged_in": tab.logged_in(), "jar": jar(tab)}), flush=True)
finally:
    tab.close()
