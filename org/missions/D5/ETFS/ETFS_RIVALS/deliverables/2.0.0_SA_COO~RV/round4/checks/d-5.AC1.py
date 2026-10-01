"""RIV-d-5 AC1 (live, READ-ONLY) -- the SERVED page for the act's page day shows GQGU with issuer data (analysis ruling 4) and
grades identity per source against the floors the act set (ruling 3): no fund is not-updated by identity_coverage.

Reads d5_live.json `page_day` and `floors` {issuer, bloomberg, home_producer}; the served
s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=<page_day>/{index.html, manifest.json}; and the committed
`data/etfs/scripts/rivalfunds/guardrails_config.json` in the tree the check runs in (the deployed package's config)."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def run(v):
    rec = L.record()
    day, floors = rec.get("page_day"), rec.get("floors") or {}
    base = f"rivalfunds/etfs/platinum/page/date={day}/"
    html = L.get(base + "index.html").decode("utf-8")
    m = json.loads(L.get(base + "manifest.json"))
    print("page day", day, "updated", m.get("funds_updated"), "of", m.get("funds_total"), "floors", floors)
    blk = re.search(r'data-fund="GQGU"(.*?)(?=data-fund="|\Z)', html, re.S)
    body = blk.group(1) if blk else ""
    v.check("data-calendar" in body and 'data-source="issuer"' in body, "GQGU served with a calendar and an issuer badge")
    cfg = json.loads(pathlib.Path("data/etfs/scripts/rivalfunds/guardrails_config.json").read_text(encoding="utf-8"))
    mrf = ((cfg.get("thresholds") or cfg).get("min_resolved_fraction") or {})  # the file nests thresholds (load_config)
    vals = mrf.get("value", mrf) if isinstance(mrf, dict) else mrf
    v.check(isinstance(vals, dict) and {"issuer", "bloomberg", "home_producer"} <= set(vals)
            and all(float(vals[k]) == float(floors.get(k, -1)) for k in ("issuer", "bloomberg", "home_producer")),
            f"guardrails_config carries the per-source floors the act recorded ({vals})")
    idc_fail = sorted(k for k, e in (m.get("funds") or {}).items()
                      if any(x.get("check") == "identity_coverage" and x.get("status") == "FAIL" for x in e.get("checks", [])))
    v.check(not idc_fail, f"no fund is not-updated by identity_coverage ({idc_fail})")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
