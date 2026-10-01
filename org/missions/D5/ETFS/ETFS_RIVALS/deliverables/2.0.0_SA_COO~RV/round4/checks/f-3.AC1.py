"""RIV-f-3 AC1 -- identity_coverage grades each fund against ITS SOURCE'S floor (analysis ruling 3: issuer-sourced,
Bloomberg-sourced and home funds -- by name -- each against their own floor), never one floor over mixed sources.

Real data: the last 2 IDVZ-group captures + the 2 newest BASG issuer days + the Positioning home landings for the capture
dates run to the page in a local sink. publish_page runs with the environment variable RIVALFUNDS_GUARDRAILS_OVERRIDE set (the
interface this cell adds in `guardrails.load_config()`: a JSON object merged over guardrails_config.json for that process only)
setting PER-SOURCE floors
{"bloomberg": 1.01, "issuer": 0.0, "home_producer": 0.0} for `min_resolved_fraction` -- an impossible Bloomberg floor, so the
grading is visible. Then, in the manifest:
  - TXUE (Bloomberg-sourced) FAILS identity_coverage, with a reason naming the source 'bloomberg' and its floor;
  - IDVZ (home, resolved 0.0) PASSES identity_coverage (its own floor 0.0);
  - BASG (issuer) PASSES identity_coverage.
The production floors are measured per source by RIV-d-5, not here."""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

OVERRIDE = {"min_resolved_fraction": {"bloomberg": 1.01, "issuer": 0.0, "home_producer": 0.0}}


def run(v):
    c.setup_path()
    from rivalfunds import gold_peer_group_map, publish_page

    sink = c.tmpdir("rv_f3_")
    files = c.idvz_captures(2)
    for f in files:
        c.mirror_s3(sink, c.HOME_LANDING_FMT.format(d=c.capture(f)["requested_date"]))
    c.land(sink, c.archive_files(2))
    c.replay("silver_issuer", sink, c.archive_meta(c.archive_files(1)[0])["requested_date"])
    c.run_idvz_chain(sink, files, "trades")
    date = c.capture(files[-1])["requested_date"]
    for m in ("gold_holdings_coverage", "gold_trade_schedule"):
        c.replay(m, sink, date, batch_id="f3")
    gold_peer_group_map.handler_entry({"mode": "daily", "date": date, "batch_id": "f3", "sink": f"local:{sink}"})
    os.environ["RIVALFUNDS_GUARDRAILS_OVERRIDE"] = json.dumps(OVERRIDE)
    try:
        r = publish_page.handler_entry({"mode": "daily", "date": date, "batch_id": "f3", "sink": f"local:{sink}"})
    finally:
        os.environ.pop("RIVALFUNDS_GUARDRAILS_OVERRIDE", None)
    print("publish:", r.get("status"))
    mp = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={date}")) / "manifest.json"
    m = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else {}

    def idc(fund):
        e = next((e for k, e in (m.get("funds") or {}).items() if k.split("/")[-1] == fund), None) or {}
        x = next((x for x in e.get("checks", []) if x.get("check") == "identity_coverage"), {})
        print(f"  {fund}: {x.get('status')} -- {str(x.get('reason'))[:140]}")
        return x.get("status"), str(x.get("reason") or "")

    st, why = idc("TXUE")
    v.check(st == "FAIL" and "bloomberg" in why.lower(), "TXUE (bloomberg) FAILS its own impossible floor, reason names the source")
    st, _ = idc("IDVZ")
    v.check(st == "PASS", "IDVZ (home, 0.0 resolved) PASSES its own floor")
    st, _ = idc("BASG")
    v.check(st == "PASS", "BASG (issuer) PASSES its own floor")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
