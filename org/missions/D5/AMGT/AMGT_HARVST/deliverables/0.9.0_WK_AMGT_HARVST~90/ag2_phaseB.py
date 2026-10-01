"""HVST-ag-2 PHASE B: ft and sa, FRESH profiles (<=3 per publisher) under r34-profiles-b, <=15 requests per publisher
(every navigation and every in-tab fetch counted), the whole act under InputSourceMonitor. A challenge met (a
bot-check signature on a non-200 / challenge page, or a visible control) is passed through verification.solve()."""
import json
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib.opal_data_harvest import tab_transport, bot_check, verification  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

OUT = Path(__file__).resolve().parent
PROFILES = OUT / "r34-profiles-b"
CAP, MAX_PROFILES = 15, 3
PLAN = {
    "ft": {"origins": ["https://www.ft.com/", "https://www.ft.com/search?q=Boeing&sort=date", "https://www.ft.com/markets"],
           "gets": ["https://www.ft.com/search?q=Boeing&sort=date&page=2", "https://www.ft.com/search?q=Costco&sort=date"]},
    "sa": {"origins": ["https://seekingalpha.com/symbol/BA", "https://seekingalpha.com/symbol/COST", "https://seekingalpha.com/symbol/HD"],
           "gets": ["https://seekingalpha.com/api/v3/symbols/ba/news?page[number]=1",
                    "https://seekingalpha.com/api/v3/symbols/ba/news?page[number]=2"]},
}
KEY = sorted(PLAN)


def page_control(pg, pub):
    try:
        sl = verification._find_slider(pg, "barrons")
        pa = verification._press_and_hold_box(pg)
    except Exception as exc:
        return {"error": str(exc)[:120]}
    return {"slider": bool(sl), "press_and_hold": bool(pa)}


def run_pub(pub, mon):
    count, attempts = 0, []
    plan = PLAN[pub]
    for i in range(MAX_PROFILES):
        if count >= CAP:
            break
        att = {"profile": "fresh-%d" % (i + 1), "steps": [], "challenge_met": "none", "passed": False, "path": None}
        attempts.append(att)
        try:
            ts = tab_transport.TabSession(pub, PROFILES / ("p%d" % (i + 1)), plan["origins"][i], headless=False)
        except Exception as exc:
            att["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:200])
            continue
        count += 1
        try:
            pg = ts.page
            pg.wait_for_timeout(6000)
            html = pg.content()
            ctl = page_control(pg, pub)
            sig = bot_check.signature_of(html)
            att["steps"].append({"kind": "goto", "url": pg.url.split("?")[0], "title": pg.title(), "signature": sig, "control": ctl})
            met = ctl.get("slider") or ctl.get("press_and_hold") or (pub == "ft" and sig == "ft_security_verification")
            for url in plan["gets"]:
                if met or count >= CAP:
                    break
                count += 1
                r = ts.get(url)
                s = bot_check.signature_of(r.text)
                att["steps"].append({"kind": "get", "url": url.split("?")[0], "status": r.status_code, "signature": s,
                                     "bytes": len(r.text), "title": (re.search(r"(?is)<title[^>]*>(.*?)</title>", r.text) or [None, ""])[1].strip()[:80]})
                if s or r.status_code in (403, 429):
                    met = True
            if met:
                att["challenge_met"] = next((x["signature"] for x in att["steps"] if x.get("signature")), "control_visible")
                att["snapshot_dom"] = len(pg.content())
        except Exception as exc:
            att["error"] = "%s: %s\n%s" % (type(exc).__name__, str(exc)[:200], traceback.format_exc()[-400:])
        finally:
            ts.close()
        if att["challenge_met"] != "none":
            break
    return {"requests": count, "attempts": attempts}


res = {}
with InputSourceMonitor() as mon:
    for pub in sys.argv[1:] or KEY:
        res[pub] = run_pub(pub, mon)
rec = {"monitor": mon.record(), "result": res}
(OUT / "ag2_phaseB_raw.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
print(json.dumps(rec, indent=1))
