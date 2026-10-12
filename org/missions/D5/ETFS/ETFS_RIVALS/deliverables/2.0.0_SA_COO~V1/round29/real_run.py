"""ETFS_RIVALS round 29 -- the issuer's ONE REAL RUN of each outcome (LOCAL risk: offline, a scratch sink, no vendor, no S3).

    cd data/etfs/scripts && python <this file>

Each part drives the REAL entry point of one cell and prints what it produced:
  xa-1  publish_page.handler_entry -> audit.html read back from the sink: the legend paragraph's visible text
  xb-1  dramatic_move.serp_search with an injected attempt plan: calls, sleeps, the failure text
  xc-1  ai_accounts.run_chain twice on one shared frame dict: the correction text, the final openings
  xd-1  dramatic_move.run_for_day (a planted discontinuity) then publish_page.handler_entry: the published chart object
The check files' own fixtures are loaded by path so this run uses the same stubs the dry-runs used.
"""
import importlib.util
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.join(HERE, "checks")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(CHECKS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out = {}
    from rivalfunds import dramatic_move as dm
    from rivalfunds import guardrails, homes, publish_page, sinks
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    xa, xb, xc, xd = (_load(n) for n in ("xa1_axis_line_check", "xb1_retry_check", "xc1_frame_check", "xd1_planted_render_check"))

    # xd-1 + xa-1: one scratch sink, one planted move, one real publish
    tmp = tempfile.mkdtemp(prefix="riv29_real_")
    os.environ["RIVALFUNDS_PRODUCE_A1"] = "1"
    os.environ[guardrails.OVERRIDE_ENV] = json.dumps({"min_resolved_fraction": 0.0})
    sp = f"local:{tmp}"
    s = sinks.get_sink(sp)
    for step, d in enumerate(("2026-09-25", "2026-09-28", tp2.DAY)):
        tp2._put(s, d, {"TXUE": (tp2._book(step), "bloomberg", 0.1 * step), "BASG": (tp2._book(step), "issuer", 0.1 * step)})
    from rivalfunds import gold_trade_schedule
    assert gold_trade_schedule.handler_entry({"date": tp2.DAY, "mode": "replay", "batch_id": "g", "sink": sp})["status"] == "OK"
    xd._plant(s)
    rep = dm.run_for_day(xd.PLANT_DAY, s, search=xd._search(xd.PLANT_NAME, "https://example.test/planted", "September 29, 2026"))
    pub = publish_page.handler_entry(tp2._ev(sp, day=xd.PLANT_DAY))
    sec = json.loads(s.get(homes.page(xd.PLANT_DAY, "charts/TXUE.json")))["securities"][xd.PLANT_KEY]
    audit = s.get(homes.page(xd.PLANT_DAY, "audit.html")).decode("utf-8")
    out["xd-1"] = {
        "run_for_day": {k: rep[k] for k in ("candidates", "written", "failed", "calls") if k in rep},
        "publish_status": pub.get("status"),
        "chart_adjustment": [(a["event_type"], a["ratio"], a["ex_date"], a["claim"], a["source_url"]) for a in sec["adjustment"]],
        "chart_gaps": sec["gaps"],
        "drawn_points": [p for p in sec["points"] if p[0] >= "2026-09-24" and p[1] is not None],
    }
    legend = re.search(r'<p class="muted">Calendar legend:(.*?)</p>', audit, flags=re.S)
    vis = xa._visible(legend.group(1)) if legend else None
    out["xa-1"] = {"legend_visible_text": vis, "sentence_present_once_in_page": xa._visible(audit).count(xa.SENTENCE) == 1}

    # xb-1: the retry policy through the real function, attempts and sleeps recorded
    def attempt(*results):
        plan = xb.Plan(*results)
        slept = []
        try:
            got = dm.serp_search("Q", _call=plan, _sleep=slept.append)
            return {"result": "OK", "records": len(got), "calls": len(plan.calls), "sleeps": slept}
        except RuntimeError as e:
            return {"result": "RAISED", "message": str(e), "calls": len(plan.calls), "sleeps": slept}
    out["xb-1"] = {
        "vendor_502_twice_then_ok": attempt(xb._fail("VENDOR"), xb._fail("VENDOR"), xb.OK),
        "persistent_502": attempt(xb._fail("VENDOR")),
        "config_403": attempt(xb._fail("CONFIG", http=403, brd=None, code=None, msg="forbidden"), xb.OK),
        "captcha": attempt(xb._fail("VENDOR", brd=None, code="captcha", msg="captcha"), xb.OK),
    }

    # xc-1: two funds, the second opens in the first's frame; one correction, the corrected opening stands
    seen = {}
    first = xc.Stub("TST1", "Alpha Co is the clearest fund-specific tell: it was bought.")
    v1 = xc._verdict("TST1", first, seen)
    second = xc.Stub("TST2", "Beta Corp is the clearest fund-specific tell: it was sold.", "Gamma Co stands out most: it was sold.")
    v2 = xc._verdict("TST2", second, seen)
    fixed = xc._frame_corrections(second)
    out["xc-1"] = {
        "fund1_opening": v1["text"].split(".")[0], "fund1_corrections": len(xc._frame_corrections(first)),
        "fund2_corrections": len(fixed), "fund2_correction_text": (fixed[0][-260:] if fixed else None),
        "fund2_final_opening": v2["text"].split(":")[0], "frames_seen": seen,
    }
    print(json.dumps(out, indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    sys.exit(main() or 0)
