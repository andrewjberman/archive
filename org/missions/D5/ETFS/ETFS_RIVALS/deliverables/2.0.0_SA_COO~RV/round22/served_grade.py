"""ETFS_RIVALS round 22 deploy -- the served read after the republish (2.0.0_SA_COO~RV; ledger etfs-rivalfunds-r22 leg L3).

    python served_grade.py <code root> <YYYY-MM-DD> <prediction json> <out dir>

Read-only on S3 (list + get under the day's page prefix); writes the downloaded objects and one record under <out dir>.
CTO half C1: manifest.json's stamp is not older than index.html's and 13 chart objects exist. C2: of the AI accounts on
the page, how many name a month, a quarter or year to date in their text, with examples."""
import html as htmllib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, PRED, OUT = sys.argv[2], json.load(open(sys.argv[3], encoding="utf-8")), pathlib.Path(sys.argv[4])
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
import boto3  # noqa: E402

from rivalfunds import homes, render  # noqa: E402

base = homes.page(DAY, "index.html")[: -len("index.html")]
bucket, prefix = base[len("s3://"):].split("/", 1)
c = boto3.client("s3")
objs = {}
for page in c.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
    for o in page.get("Contents", []):
        k = o["Key"][len(prefix):]
        if not k.startswith("revisions/"):
            objs[k] = o
OUT.mkdir(parents=True, exist_ok=True)
body = {}
for k in objs:
    b = c.get_object(Bucket=bucket, Key=prefix + k)["Body"].read()
    p = OUT / k
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)
    body[k] = b
rec = {"day": DAY, "prefix": base, "objects": {k: {"bytes": o["Size"], "last_modified_utc": o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")} for k, o in sorted(objs.items())}}
charts = sorted(k for k in objs if k.startswith("charts/"))
idx_t, man_t = objs["index.html"]["LastModified"], objs["manifest.json"]["LastModified"]
rec["c1"] = {"manifest_not_older_than_index": bool(man_t >= idx_t), "chart_objects": len(charts),
             "whole": bool(man_t >= idx_t and len(charts) == 13)}
print("objects (revisions aside):", len(objs))
for k, v in rec["objects"].items():
    print(f"  {k:<22} {v['bytes']:>9}  {v['last_modified_utc']}")
print("C1:", rec["c1"])

html = body["index.html"].decode("utf-8")
man = json.loads(body["manifest.json"].decode("utf-8"))
pc = PRED["chart_objects"]
cmp_ = {"index_bytes": (len(body["index.html"]), PRED["index.html"]["bytes"]),
        "audit_bytes": (len(body["audit.html"]), PRED["audit.html"]["bytes"]),
        "chart_objects": (len(charts), len(pc)),
        "chart_bytes_total": (sum(objs[k]["Size"] for k in charts), sum(v["bytes"] for v in pc.values())),
        "chart_markers_total": (sum(len(m.get("markers") or []) for k in charts for m in json.loads(body[k])["securities"].values()),
                                sum(v["markers"] for v in pc.values()))}
rec["served_vs_prediction"] = {k: {"served": a, "predicted": b, "equal": a == b} for k, (a, b) in cmp_.items()}
for k, v in rec["served_vs_prediction"].items():
    print(f"  {k:<20} served {v['served']:>9}  predicted {v['predicted']:>9}  equal {v['equal']}")
rec["manifest"] = {k: man.get(k) for k in ("fund_sections", "ai_grounding", "audit_trades_left_out", "funds_updated", "funds_total", "holding_dialogs")}
rec["manifest"]["a1_produced"] = man.get("a1_produced")
rec["manifest"]["charts_listed"] = len(man.get("charts") or {})
print("manifest:", json.dumps(rec["manifest"])[:900])
rec["page"] = {"fund_sections_census": render.fund_section_census(html), "grounding_census": render.grounding_census(html),
               "script_blocks": len(re.findall(r"<script\b", html)), "audit_script_blocks": len(re.findall(r"<script\b", body["audit.html"].decode("utf-8"))),
               "period_radios": sorted(set(re.findall(r">(30d|90d|365d)<", html))), "MTD_QTD_YTD_words": {w: len(re.findall(r"\b%s\b" % w, html)) for w in ("MTD", "QTD", "YTD")}}
print("page:", rec["page"])

# C2: the AI accounts' period words
PERIOD = re.compile(r"\b(month[- ]to[- ]date|quarter[- ]to[- ]date|year[- ]to[- ]date|MTD|QTD|YTD|this month|this quarter|this year|the month|the quarter|"
                    r"so far this (?:month|quarter|year)|month|quarter)\b", re.I)
accounts = []
for m in re.finditer(r'<div class="rf-ai[^"]*" data-ai-kind="([^"]+)">', html):
    seg = html[m.end(): m.end() + 60000]
    nxt = re.search(r'<div class="rf-ai[^"]*" data-ai-kind=|data-fund-panel=|data-ai-fund=', seg)
    seg = seg[: nxt.start()] if nxt else seg
    fund = re.findall(r'data-ai-fund="([^"]+)"', html[: m.start()])
    text = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", seg))).strip()
    hits = sorted({h.lower() for h in PERIOD.findall(text)})
    accounts.append({"fund": fund[-1] if fund else None, "kind": m.group(1), "period_words": hits,
                     "example": next((s.strip() for s in re.split(r"(?<=[.!?]) ", text) if PERIOD.search(s)), None)})
named = [a for a in accounts if a["period_words"]]
rec["c2"] = {"accounts": len(accounts), "by_kind": {k: sum(1 for a in accounts if a["kind"] == k) for k in sorted({a["kind"] for a in accounts})},
             "naming_a_month_quarter_or_year_to_date": len(named), "named": named}
print(f"C2: {len(named)} of {len(accounts)} AI accounts name a month, a quarter or year to date; kinds {rec['c2']['by_kind']}")
for a in named[:6]:
    print(f"  {a['fund']} {a['kind']} {a['period_words']}: {str(a['example'])[:230]}")
(OUT / f"served_grade_{DAY}.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
