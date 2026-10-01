"""HVST-ag-2 PHASE A: meet ft's and sa's web challenge read-only, FRESH anonymous profile each, <=5 requests per
publisher (counted: every navigation incl. the TabSession's initial goto), under InputSourceMonitor."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib.opal_data_harvest import tab_transport, bot_check  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

OUT = Path(__file__).resolve().parent
PROFILES = OUT / "r34-profiles"
ORIGINS = {"ft": "https://www.ft.com/search?q=Boeing&sort=date", "sa": "https://seekingalpha.com/market-news"}
CONTENT = {"ft": None, "sa": None}
CAP = 5


def scrub(html):
    html = re.sub(r"(?is)<script\b[^>]*>.*?</script>", "<script>[removed]</script>", html)
    html = re.sub(r'(?i)\svalue="[^"]*"', ' value="[removed]"', html)
    return html


def probe(pub):
    n = {"n": 0}
    log = []
    ts = tab_transport.TabSession(pub, PROFILES, ORIGINS[pub], headless=False)
    n["n"] += 1
    try:
        pg = ts.page
        pg.wait_for_timeout(6000)
        def snap(tag):
            html = pg.content()
            sig = bot_check.signature_of(html)
            title = pg.title()
            log.append({"step": tag, "url": pg.url.split("?")[0], "title": title, "signature": sig,
                        "frames": [f.url.split("?")[0][:120] for f in pg.frames], "bytes": len(html),
                        "px_visible": pg.locator("#px-captcha:visible").count() if pub == "sa" else None,
                        "press_hold_text": len(re.findall(r"(?i)press\s*&(?:amp;)?\s*hold", html))})
            return html, sig
        html, sig = snap("origin")
        if sig:
            (OUT / ("ag2_%s_challenge.html" % pub)).write_text(scrub(html), encoding="utf-8")
        target = CONTENT[pub]
        if not sig:
            links = pg.eval_on_selector_all("a[href*='/content/'], a[href*='/news/'], a[href*='/article/']", "els => els.map(e => e.href)")
            links = [u for u in links if "/content/" in u or re.search(r"/(news|article)/\d+", u)]
            target = links[0] if links else None
        if target and n["n"] < CAP:
            n["n"] += 1
            pg.goto(target, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(6000)
            html2, sig2 = snap("content")
            if sig2 and not sig:
                (OUT / ("ag2_%s_challenge.html" % pub)).write_text(scrub(html2), encoding="utf-8")
                sig = sig2
        return {"signature": sig, "requests": n["n"], "log": log}
    finally:
        ts.close()


res = {}
with InputSourceMonitor() as mon:
    for pub in sys.argv[1:] or ["ft", "sa"]:
        try:
            res[pub] = probe(pub)
        except Exception as exc:
            res[pub] = {"error": "%s: %s" % (type(exc).__name__, str(exc)[:300])}
(OUT / "ag2_explore_2.json").write_text(json.dumps({"monitor": mon.record(), "result": res}, indent=1), encoding="utf-8")
print(json.dumps({"monitor": mon.record(), "result": res}, indent=1))
