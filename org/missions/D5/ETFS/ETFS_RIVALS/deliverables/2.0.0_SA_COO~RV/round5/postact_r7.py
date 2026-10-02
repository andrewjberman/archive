"""r7 post-act read from the SERVED objects (CTO~Z addendum-6 condition). Read-only. Run from /c/tmp/rv-apply."""
import io
import json
import re
import sys

import pandas as pd

sys.path.insert(0, "data/etfs/scripts")
from rivalfunds import homes, revision, sinks  # noqa: E402

s = sinks.get_sink("s3")
DAY = "2026-10-01"
pre = json.load(open("C:/tmp/r7_pre/pre.json"))
KEYS = {"holding_contribution": ["fund_id", "period", "axis", "bucket"], "buying_trend": ["fund_id", "axis", "lean", "rank"],
        "input_census": ["date", "input_kind", "subject", "fund_id"]}
out = {"day": DAY, "tables": {}, "page": {}}
served = {}
for t, k in KEYS.items():
    pfx = homes.address("rivalfunds", "etfs", "gold", t, f"date={DAY}") + "/"
    us = [u for u in s.list(pfx) if u.endswith(".parquet")]
    n = revision.newest(us)
    a = pd.read_parquet(f"C:/tmp/r7_pre/{t}.parquet")
    b = pd.read_parquet(io.BytesIO(s.get(n)))
    served[t] = b
    rec = {"pre_object": pre[t]["uri"].rsplit("/", 1)[-1], "served_object": n.rsplit("/", 1)[-1],
           "new_object_written": n != pre[t]["uri"], "objects_now": len(us), "rows_pre": len(a), "rows_served": len(b),
           "columns_added": sorted(set(b.columns) - set(a.columns)), "columns_removed": sorted(set(a.columns) - set(b.columns))}
    m = a.merge(b, on=k, how="outer", suffixes=("_p", "_s"), indicator=True)
    rec["rows_unmatched"] = int((m["_merge"] != "both").sum())
    diff = {}
    for c in sorted((set(a.columns) & set(b.columns)) - set(k)):
        x, y = m[f"{c}_p"], m[f"{c}_s"]
        same = (x.astype(str) == y.astype(str)) | (x.isna() & y.isna())
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            same = same | ((x - y).abs() <= 1e-9 * pd.concat([x.abs(), y.abs()], axis=1).max(axis=1).clip(lower=1.0))
        d = int((~same & (m["_merge"] == "both")).sum())
        if d:
            diff[c] = d
    rec["values_compared"] = int((m["_merge"] == "both").sum()) * len((set(a.columns) & set(b.columns)) - set(k))
    rec["values_changed"] = diff
    if t == "buying_trend" and "sector_source" in b.columns:
        rec["sector_source_counts"] = {ax: {str(v): int(c) for v, c in b[b["axis"] == ax]["sector_source"].astype(object)
                                            .where(b[b["axis"] == ax]["sector_source"].notna(), "null").value_counts().items()}
                                       for ax in ("security", "sector")}
    out["tables"][t] = rec


def segs(html):
    """component segments keyed by data-rank-fund/period and data-trend-fund"""
    pos = [(mm.start(), mm.group(0)) for mm in re.finditer(r'data-(?:rank-fund="[^"]+" data-rank-period="[^"]+"|trend-fund="[^"]+"|ai-fund="[^"]+"|fund-panel="[^"]+")', html)]
    res = {}
    for i, (p, tag) in enumerate(pos):
        end = pos[i + 1][0] if i + 1 < len(pos) else html.find('id="audit"', p)
        res[tag] = html[p:end]
    return res


pre_html = open("C:/tmp/r7_pre/index.html", encoding="utf-8").read()
post_html = s.get(homes.page(DAY, "index.html")).decode("utf-8")
man = json.loads(s.get(homes.page(DAY, "manifest.json")))
P, Q = segs(pre_html), segs(post_html)
hidden = lambda h: "Sectors not shown" in h  # noqa: E731


def share(rows, col, alt=None):
    if not len(rows):
        return None
    v = rows[col].where(rows[col].notna(), rows[alt] if alt else 0).fillna(0).abs() if alt else rows[col].dropna().abs()
    tot = float(v.sum())
    unc = float(v[rows.loc[v.index, "bucket"].astype(str) == "Unclassified"].sum())
    return unc / tot if tot > 0 else None


hc, bt = served["holding_contribution"], served["buying_trend"]
rank_rows, trend_rows, mism = [], [], []
for tag, h in Q.items():
    if tag.startswith("data-rank-fund"):
        f, per = re.findall(r'"([^"]+)"', tag)
        sh = share(hc[(hc.fund_id == f) & (hc.period == per) & (hc.axis == "sector")], "contribution")
        pred = sh is not None and sh > 0.5
        rank_rows.append((f, per, None if sh is None else round(sh, 3), hidden(h), hidden(P.get(tag, ""))))
        if pred != hidden(h):
            mism.append(("rank", f, per, sh, hidden(h)))
    elif tag.startswith("data-trend-fund"):
        f = re.findall(r'"([^"]+)"', tag)[0]
        sh = share(bt[(bt.fund_id == f) & (bt.axis == "sector")], "gross_notional_base", "net_notional_base")
        pred = sh is not None and sh > 0.5
        trend_rows.append((f, None if sh is None else round(sh, 3), hidden(h), hidden(P.get(tag, ""))))
        if pred != hidden(h):
            mism.append(("trend", f, sh, hidden(h)))
changed = sorted(t for t in set(P) | set(Q) if P.get(t) != Q.get(t) and not t.startswith("data-fund-panel"))
out["page"] = {"batch": man.get("batch_id"), "bytes_pre": len(pre_html.encode()), "bytes_served": len(post_html.encode()),
               "script_tags": post_html.count("<script"),
               "rank_panels": len(rank_rows), "rank_panels_hidden_served": sum(r[3] for r in rank_rows),
               "rank_panels_hidden_pre": sum(r[4] for r in rank_rows),
               "trend_cards": len(trend_rows), "trend_hidden_served": [r[0] for r in trend_rows if r[2]],
               "trend_hidden_pre": [r[0] for r in trend_rows if r[3]],
               "trend_unclassified_share": {r[0]: r[1] for r in trend_rows},
               "rule_mismatches": mism, "components_changed": changed}
four = bt[bt.fund_id.isin(["ETFT", "GQGU", "IDVZ", "PCLG"]) & (bt.axis == "sector")]
out["four_funds_hidden_sector_rows"] = four[["fund_id", "lean", "rank", "bucket", "net_notional_base", "gross_notional_base",
                                             "sector_source"]].round(0).astype(object).values.tolist()
print(json.dumps(out, indent=1, default=str))
json.dump(out, open("C:/tmp/r7_postact.json", "w"), indent=1, default=str)
