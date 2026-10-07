"""ETFS_RIVALS round 22 -- the proof 1.0.0_SA_CTO~Z's ruling msg 31031 words for row ETFS_RIVALS-Z-C-S64 (2.0.0_SA_COO~RV).

    python marker_proof.py <before layer root> <after layer root> <page day> <out json>

`before` is the real run made BEFORE the fold (round 19: GQGU's CUSIP-keyed securities still had their own dialogs and
markers); `after` is the round-22 real run of the same day. Both are local layers of one real day; nothing is read from
or written to S3.

1. Markers per fund, before and after, for all 13 funds. Round 22 also (a) drops a zero-dollar trade and (b) adds a trade
   whose window ends on the page day, so the totals are reconciled, not compared bare:
       after == before - zero_dollar_before + page_day_after + other
   and `other` is printed per fund (0 means every marker is accounted for).
2. GQGU: the keys in `before` and not in `after` (the folded CUSIP keys), their markers, and the markers now under the
   Bloomberg keys the fold moved them to (matched marker by marker on side, start, end and dollars).
3. The page: dialogs where a buying section sits above a trade list saying "No trades" -- counted on the static page
   (the caption's static sentence) and on the objects (a fund-security whose section shows a strip with a bought or sold
   month while its object holds 0 markers)."""
import collections
import glob
import json
import re
import sys

BEFORE, AFTER, DAY, OUT = sys.argv[1].rstrip("/\\"), sys.argv[2].rstrip("/\\"), sys.argv[3], sys.argv[4]
PAGE = "/opal-data-etfs/rivalfunds/etfs/platinum/page/date=" + DAY + "/"


def load(root):
    objs = {}
    for f in sorted(glob.glob(root + PAGE + "charts/*.json")):
        o = json.load(open(f, encoding="utf-8"))
        objs[o["fund"]] = o
    return objs


def sig(m):
    return (m["side"], m["start"], m["end"], round(float(m["usd"]), 2))


b, a = load(BEFORE), load(AFTER)
rec = {"day": DAY, "funds": {}, "asof_before": sorted({o["asof"] for o in b.values()}), "asof_after": sorted({o["asof"] for o in a.values()})}
print(f"{'fund':<6} {'before':>6} {'zero$':>6} {'after':>6} {'pageday':>7} {'other':>6}")
tot = collections.Counter()
for f in sorted(set(b) | set(a)):
    mb = [m for v in (b.get(f, {}).get("securities") or {}).values() for m in v.get("markers") or []]
    ma = [m for v in (a.get(f, {}).get("securities") or {}).values() for m in v.get("markers") or []]
    asof = a[f]["asof"] if f in a else None
    zero = sum(1 for m in mb if float(m["usd"]) == 0.0)
    pday = sum(1 for m in ma if asof and m["end"] > asof)
    other = len(ma) - (len(mb) - zero + pday)
    sb = collections.Counter(sig(m) for m in mb if float(m["usd"]) != 0.0)
    sa = collections.Counter(sig(m) for m in ma if not (asof and m["end"] > asof))
    rec["funds"][f] = {"before": len(mb), "zero_dollar_before": zero, "after": len(ma), "page_day_after": pday, "other": other,
                       "same_markers_by_content": sb == sa, "only_before": sum((sb - sa).values()), "only_after": sum((sa - sb).values())}
    for k, n in (("before", len(mb)), ("zero", zero), ("after", len(ma)), ("pday", pday)):
        tot[k] += n
    print(f"{f:<6} {len(mb):>6} {zero:>6} {len(ma):>6} {pday:>7} {other:>6}   same by content: {sb == sa}"
          + ("" if sb == sa else f" (only before {sum((sb - sa).values())}, only after {sum((sa - sb).values())})"))
rec["totals"] = dict(tot)
rec["funds_reconciled"] = f"{sum(1 for x in rec['funds'].values() if x['other'] == 0)} of {len(rec['funds'])}"
rec["funds_same_markers_by_content"] = f"{sum(1 for x in rec['funds'].values() if x['same_markers_by_content'])} of {len(rec['funds'])}"
print("totals:", dict(tot), "| funds reconciled:", rec["funds_reconciled"], "| same markers by content:", rec["funds_same_markers_by_content"])

gb, ga = b["GQGU"]["securities"], a["GQGU"]["securities"]
folded = sorted(k for k in gb if k not in ga)
lost = [m for k in folded for m in gb[k].get("markers") or []]
after_sigs = collections.Counter(sig(m) for v in ga.values() for m in v.get("markers") or [])
found = sum(1 for m in lost if float(m["usd"]) != 0.0 and after_sigs[sig(m)] > 0)
homes_ = collections.Counter()
for k, v in ga.items():
    s = {sig(m) for m in v.get("markers") or []}
    n = sum(1 for m in lost if sig(m) in s)
    if n:
        homes_[k] = n
rec["gqgu"] = {"folded_keys": folded, "their_markers_before": len(lost), "of_those_zero_dollar": sum(1 for m in lost if float(m["usd"]) == 0.0),
               "found_after_by_content": found, "now_under": dict(homes_)}
print("GQGU folded keys:", folded)
print("their markers before:", len(lost), "| zero-dollar among them:", rec["gqgu"]["of_those_zero_dollar"], "| found after by content:", found)
print("now under:", dict(homes_))

html = open(AFTER + PAGE + "index.html", encoding="utf-8").read()
static_none = len(re.findall(r"data-chart-trades[^>]*>\s*No trades", html))
contra = 0
frames = 0
ex = []
for seg in html.split('data-sec-dialog="')[1:]:
    key = seg.split('"', 1)[0]
    for sec in re.split(r"(?=<section data-fund=)", seg)[1:]:
        fm = re.match(r"<section data-fund=[\"']?([A-Za-z0-9_]+)", sec)
        if not fm or "data-chart-fund" not in sec:
            continue
        frames += 1
        fund = fm.group(1)
        st = re.search(r"data-month-chart>(.*?)</div>", sec)
        traded = bool(st and re.search(r"<i class=[ud]\b", st.group(1)))
        n = len(((a.get(fund, {}).get("securities") or {}).get(key) or {}).get("markers") or [])
        if traded and n == 0:
            contra += 1
            if len(ex) < 8:
                ex.append(f"{fund}:{key}")
rec["page"] = {"chart_frames": frames, "static_no_trades_sentences": static_none,
               "sections_with_a_traded_strip_and_0_markers": contra, "examples": ex}
print("page: chart frames", frames, "| static 'No trades' in a trades element:", static_none,
      "| sections whose strip shows a bought or sold month and whose object holds 0 markers:", contra, ex)
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1)
