"""HVST-ae-3 confound arm (issuer direct act, after the 09:00Z first light): the SAME first-light probe, re-run with the
production harvesters' launch settings, so a challenge can be attributed to the box IP or to the automation flag.

Brief IV.4: first light launches without the setting every production harvester uses, so `navigator.webdriver` reads
true. The production settings (`org/tier1_exec/4.0.0_SA_CRO/scripts/ft_harvest_session.py:284-291`) are:
- `chromium.launch(..., args=["--disable-blink-features=AutomationControlled", "--no-first-run"])`;
- `new_context(viewport={"width": 1366, "height": 900}, ...)`;
- `ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")`.

This wrapper changes ONLY those three things, by patching Playwright's `launch` and `new_context`, and runs the armed
script's own `main()` (`org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/scripts/harvest_first_light.py`, unedited). Every
other behaviour is the armed probe's: stop each arm at its first challenge and never interact with it, no article text,
no cookie value, the stored session never written back. Always pass `--no-residential` (placement R7).

Usage (workspace root): python <this file> --no-residential [--publishers ft,bbg,wsj,barrons] [--dry-run]
Output: .runtime/harvest-first-light-confound/<run_id>/ (summary.json + per-publisher jsonl).
`--probe-webdriver` launches once under the patch against about:blank and prints what `navigator.webdriver` reads
(no network), then exits.
"""
import json
import runpy
import sys
from pathlib import Path

from playwright.sync_api import BrowserType, Browser  # noqa: F401

PROD_ARGS = ["--disable-blink-features=AutomationControlled", "--no-first-run"]
INIT = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
SCRIPT = Path.cwd() / "org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/scripts/harvest_first_light.py"
OUT = ".runtime/harvest-first-light-confound"

_launch = BrowserType.launch
_new_context = Browser.new_context


def _patched_launch(self, *args, **kwargs):
    extra = list(kwargs.get("args") or [])
    kwargs["args"] = extra + [a for a in PROD_ARGS if a not in extra]
    return _launch(self, *args, **kwargs)


def _patched_new_context(self, *args, **kwargs):
    kwargs.setdefault("viewport", {"width": 1366, "height": 900})
    ctx = _new_context(self, *args, **kwargs)
    ctx.add_init_script(INIT)
    return ctx


def probe_webdriver():
    from playwright.sync_api import sync_playwright
    BrowserType.launch = _patched_launch
    Browser.new_context = _patched_new_context
    with sync_playwright() as p:
        for label, patched in (("unpatched", False), ("patched", True)):
            launch = _patched_launch if patched else _launch
            browser = launch(p.chromium, channel="chrome", headless=False)
            try:
                ctx = _patched_new_context(browser) if patched else _new_context(browser)
                page = ctx.new_page()
                page.goto("about:blank")
                print("WEBDRIVER %s: %r" % (label, page.evaluate("navigator.webdriver")))
            finally:
                browser.close()
    return 0


def main():
    if "--probe-webdriver" in sys.argv:
        return probe_webdriver()
    if "--no-residential" not in sys.argv:
        print("REFUSED: the confound arm runs with --no-residential only (placement R7)")
        return 2
    if "--out" not in sys.argv:
        sys.argv += ["--out", OUT]
    BrowserType.launch = _patched_launch
    Browser.new_context = _patched_new_context
    sys.argv[0] = str(SCRIPT)
    print("CONFOUND ARM: launch args %s; viewport 1366x900; webdriver init script; script %s"
          % (json.dumps(PROD_ARGS), SCRIPT))
    runpy.run_path(str(SCRIPT), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
