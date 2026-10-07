"""ETFS_RIVALS round 15 -- the issuer's one real run (2.0.0_SA_COO~RV): build the two period tables and the page for a
published day from the LIVE inputs without writing S3.

    python real_run.py <code root> <YYYY-MM-DD> <out dir>

Round 12's real run (../round12/real_run.py) read the day's published A1 tables. Round 15 changes those tables (30 / 90 / 365
calendar days), so this run first rebuilds gold holding_contribution and buying_trend through the same read-only overlay
(reads: local layer, then live S3; every write lands in <out dir>/layer), then publishes with the A1 producer pre-step off so
the page reads the tables just built. No AI call, no Bloomberg call, no S3 write. The AI accounts on the page are the day's
published ones (written on the old periods): cell RIV-pd-3 is exercised only by a deployed sweep.

Prints and writes <out dir>/real_run_<day>.json: each stage's status, the periods each table carries, the page and audit
measures of round 12, the script count, the chart frames, and the per-fund chart objects with their bytes."""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY = sys.argv[2]
OUT = pathlib.Path(sys.argv[3]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))

_spec = importlib.util.spec_from_file_location("r12_real_run", pathlib.Path(__file__).resolve().parent.parent / "round12" / "real_run.py")
r12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r12)  # binds ROOT / DAY / OUT from the same argv; main() is not called

from rivalfunds import gold_buying_trend, gold_holding_contribution, homes, publish_page, render  # noqa: E402


def _brief(r: dict) -> dict:
    d = r.get("detail") if isinstance(r.get("detail"), dict) else {}
    return {"status": r.get("status"), "detail": {k: d[k] for k in sorted(d) if k in (
        "rows", "funds", "periods", "r30_window_was", "r30_window_is", "written", "uri", "reason")} or str(r.get("detail"))[:400]}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    s = r12.OverlaySink(OUT / "layer")
    rec = {"day": DAY, "code_root": str(ROOT), "dialog_soft_cap": render.DIALOG_SOFT_CAP}
    rec["gold_holding_contribution"] = _brief(gold_holding_contribution.handler_entry({"date": DAY, "sink": s}))
    rec["gold_buying_trend"] = _brief(gold_buying_trend.handler_entry({"date": DAY, "sink": s}))
    rec["local_layer_objects_after_gold"] = sorted(str(p.relative_to(OUT / "layer")).replace("\\", "/")
                                                   for p in (OUT / "layer").rglob("*") if p.is_file())
    os.environ[publish_page.PRODUCE_ENV] = "0"
    batch = "r15-real-run-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    r = publish_page.handler_entry({"date": DAY, "mode": "replay", "batch_id": batch, "sink": s})
    rec.update({"batch_id": batch, "status": r.get("status"), "detail": r.get("detail")})
    for name in ("index.html", "audit.html"):
        uri = homes.page(DAY, name)
        if s.local.exists(uri):
            html = s.local.get(uri).decode("utf-8")
            m = dict(r12.measure(html), source="rendered (local layer)")
            m["script_blocks"] = len(re.findall(r"<script\b", html, re.I))
            m["chart_frames"] = len(re.findall(r"\bdata-chart-key=", html))
            m["period_radios"] = re.findall(r"<label[^>]*>\s*(30d|90d|365d|MTD|QTD|YTD)\s*</label>", html)[:6]
            m["mentions_MTD_QTD_YTD"] = {w: len(re.findall(rf"\b{w}\b", re.sub(r"<script\b.*?</script\s*>", "", html, flags=re.I | re.S)))
                                         for w in ("MTD", "QTD", "YTD")}
            rec[name] = m
    man = homes.page(DAY, "manifest.json")
    if s.local.exists(man):
        mf = json.loads(s.local.get(man))
        rec["manifest"] = {k: mf.get(k) for k in ("holding_dialogs", "audit_bytes", "index_bytes", "funds_updated", "funds_total",
                                                  "ai_grounding", "charts")}
    charts = {}
    for uri in s.local.list(homes.page(DAY, "charts/")):
        body = s.local.get(uri)
        try:
            o = json.loads(body)
            secs = o.get("securities") or {}
            charts[uri.rsplit("/", 1)[-1]] = {
                "bytes": len(body), "ranges": o.get("ranges"), "securities": len(secs), "thinned": o.get("thinned", False),
                "points": sum(len(v.get("points") or []) for v in secs.values()),
                "priced_points": sum(1 for v in secs.values() for p in (v.get("points") or []) if p[1] is not None),
                "markers": sum(len(v.get("markers") or []) for v in secs.values()),
                "source_codes": sorted({p[2] for v in secs.values() for p in (v.get("points") or []) if p[2]})}
        except Exception as e:  # noqa: BLE001 -- a chart object that does not parse is the finding
            charts[uri.rsplit("/", 1)[-1]] = {"bytes": len(body), "error": f"{type(e).__name__}: {e}"}
    rec["chart_objects"] = charts
    (OUT / f"real_run_{DAY}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
    print(json.dumps(rec, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
