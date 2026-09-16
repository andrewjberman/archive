"""Headful Dow Jones SSO session harvest; credentials stay in Secrets Manager.

Shared credentials: dowjones/credentials, us-east-1. Local bundles only unless
--park is explicit. Entitlement is measured independently for each publication.
Browser response capture is for API discovery, never article acceptance.
"""

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import boto3
from playwright.sync_api import sync_playwright

CREDENTIAL_SECRET = "dowjones/credentials"
SUBSCRIBER_TYPES = {"subscriber", "prosubscriber", "pro-subscriber"}


def entitlement_summary(value):
    return {
        "logged_in": value.get("isLoggedIn") is True,
        "user_type": value.get("type"),
        "subscriber": value.get("isLoggedIn") is True
        and value.get("type") in SUBSCRIBER_TYPES,
        "document_key_present": bool(value.get("documentKey")),
        "paywall_type": (value.get("paywall") or {}).get("paywallType"),
    }


def harvest(publisher, output_dir, wait_seconds=180, park=False):
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    creds = json.loads(sm.get_secret_value(SecretId=CREDENTIAL_SECRET)["SecretString"])
    host = f"www.{publisher}.com"
    events, entitlements, discovery = [], [], []

    def capture(response):
        parsed = urlparse(response.url)
        if not (parsed.hostname or "").endswith(("dowjones.com", f"{publisher}.com")):
            return
        for header in response.header_values("set-cookie"):
            events.append({"host": parsed.hostname, "path": parsed.path,
                           "cookie_name": header.split("=", 1)[0], "status": response.status})
        if parsed.hostname != host or response.request.resource_type not in ("xhr", "fetch"):
            return
        try:
            value = response.json()
        except Exception:
            return
        if parsed.path == "/client" and isinstance(value, dict):
            summary = entitlement_summary(value)
            entitlements.append(summary)
            print(json.dumps({"publisher": publisher, "entitlement": summary}), flush=True)
        # Only publisher JSON responses; SSO requests/passwords are never recorded.
        target = f"api-response-{len(discovery):03d}.json"
        (output_dir / target).write_text(json.dumps(value), encoding="utf-8")
        discovery.append({"url": response.url, "method": response.request.method,
                          "status": response.status, "response_file": target})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=False,
            args=["--no-first-run", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={"width": 1366, "height": 900})
        context.on("response", capture)
        page = context.new_page()
        try:
            page.goto(f"https://{host}/client/login?target=https%3A%2F%2F{host}%2F",
                      wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
            if urlparse(page.url).hostname != "sso.accounts.dowjones.com":
                raise RuntimeError("Expected observed Dow Jones SSO host before credential entry")
            page.locator('input[name="emailOrUsername"]').fill(creds["username"])
            page.get_by_role("button", name="Continue", exact=True).click()
            page.wait_for_timeout(2500)
            print(json.dumps({"publisher": publisher, "password_step": {
                "fields": page.locator("input").evaluate_all(
                    "els=>els.map(e=>({id:e.id,type:e.type,name:e.name}))"),
                "buttons": page.locator("button").all_text_contents()}}), flush=True)
            password = page.locator('input[type="password"]')
            password.wait_for(state="visible", timeout=20000)
            if urlparse(page.url).hostname != "sso.accounts.dowjones.com":
                raise RuntimeError("Unexpected credential destination")
            password.fill(creds["password"])
            page.get_by_role("button", name=re.compile(r"^Sign [Ii]n$")).click()
            print(f"{publisher}: credentials submitted; waiting for publisher redirect", flush=True)
            for _ in range(max(1, wait_seconds // 2)):
                page.wait_for_timeout(2000)
                # Observed new-account interstitial offers optional email verification
                # and an explicit Continue to WSJ/Barron's action. Continue the login.
                onward = page.get_by_role("button", name=re.compile(r"^Continue to (WSJ|Barron)", re.I))
                if not onward.count():
                    onward = page.get_by_role("link", name=re.compile(r"^Continue to (WSJ|Barron)", re.I))
                if onward.count() and onward.first.is_visible():
                    onward.first.click()
                    print(f"{publisher}: continued past optional email verification", flush=True)
                if urlparse(page.url).hostname == host and "/client/" not in urlparse(page.url).path:
                    break
            page.wait_for_timeout(4000)
            if urlparse(page.url).hostname == host:
                result = context.request.get(f"https://{host}/client?legacy=false",
                    headers={"Accept": "application/json", "Referer": f"https://{host}/",
                             "x-original-host": host, "x-original-url": "/"})
                if result.ok:
                    entitlements.append(entitlement_summary(result.json()))
            paid = any(e["subscriber"] for e in entitlements)
            logged_in = any(e["logged_in"] for e in entitlements)
            # Require a successful publisher auth callback cookie event in this run.
            network_ok = any(e["host"] == host and e["path"] == "/client/auth"
                             and 200 <= e["status"] < 400 for e in events)
            summary = {"publisher": publisher, "logged_in": logged_in, "subscriber": paid,
                       "network_auth_corroborated": network_ok, "entitlements": entitlements,
                       "final_host": urlparse(page.url).hostname,
                       "final_path": urlparse(page.url).path, "cloud_park": park}
            if logged_in and network_ok:
                bundle = {"publisher": publisher, "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                          "all_cookies": context.cookies(), "user_agent": page.evaluate("navigator.userAgent"),
                          "network_auth_corroborated": network_ok, "subscriber": paid,
                          "network_auth_events": events}
                target = output_dir / f"{publisher}_session_{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}.json"
                target.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
                if park:
                    secret = f"{publisher}/session"
                    try:
                        sm.put_secret_value(SecretId=secret, SecretString=json.dumps(bundle))
                    except sm.exceptions.ResourceNotFoundException:
                        sm.create_secret(Name=secret, SecretString=json.dumps(bundle))
            else:
                # Visible status only; mask the password if the login form remains.
                page.screenshot(path=str(output_dir / "login-status.png"), mask=[page.locator('input[type="password"]')])
                summary["visible_status"] = page.locator("body").inner_text()[:2000].replace(creds["username"], "[account]").replace(creds["password"], "[redacted]")
            (output_dir / "auth-evidence.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
            print(json.dumps(summary), flush=True)
            return 0 if paid and network_ok else 3
        finally:
            (output_dir / "api-discovery.json").write_text(json.dumps(discovery, indent=2), encoding="utf-8")
            (output_dir / "cookie-events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("publisher", choices=("wsj", "barrons"))
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--park", action="store_true")
    args = parser.parse_args()
    raise SystemExit(harvest(args.publisher, args.output_dir, args.wait_seconds, args.park))
