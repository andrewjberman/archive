"""ETFS_RIVALS round 22 (round 19's script with the cell pattern widened for quoted labels and data-part) -- read the real run's month strips against its own data (2.0.0_SA_COO~RV).

    python measure_month_strips.py <local layer root> <YYYY-MM-DD> <out json>

1. gold buying_trend: for every row with a trend_mark, is the month of `window_end` the month the mark's last token
   stands for (the rule cell RIV-ml-1 labels by)? Tokens are counted, by period.
2. The rendered index.html: every month strip, its cell count, and whether every cell carries `data-m`; the labels of
   the last cell of each strip.
3. Dialog strips against the chart objects: for each chart frame's fund section that holds a strip, the months labelled
   bought or sold (as year-months counted back from the page day's month), against the year-months in which that fund's markers for the security end (from the fund's chart object).
   A labelled month with no marker ending in it, or a marker month the strip calls 'no trade', is a disagreement."""
import collections
import glob
import json
import re
import sys

import pandas as pd

ROOT, DAY, OUT = sys.argv[1].rstrip("/\\"), sys.argv[2], sys.argv[3]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base = ROOT + "/opal-data-etfs/rivalfunds/etfs/"
rec = {"day": DAY}

bt = pd.read_parquet(sorted(glob.glob(base + f"gold/buying_trend/date={DAY}/*.parquet"))[-1])
m = bt[bt.trend_mark.notna() & (bt.trend_mark.astype(str).str.strip() != "")]
rec["trend_rows_with_a_mark"] = int(len(m))
rec["window_end_values"] = {str(k)[:10]: int(v) for k, v in m.window_end.astype(str).str[:10].value_counts().items()}
rec["tokens_by_period"] = {p: dict(collections.Counter(int(len(str(s).split())) for s in g.trend_mark))
                           for p, g in m.groupby("period")}
ok = 0
for r in m.itertuples():
    n = len(str(r.trend_mark).split())
    ws, we = pd.Timestamp(str(r.window_start)[:10]), pd.Timestamp(str(r.window_end)[:10])
    span = (we.year - ws.year) * 12 + we.month - ws.month + 1
    ok += int(n <= span + 1 and n >= 1)
rec["rows_whose_token_count_fits_window_start_to_window_end_months"] = ok

html = open(base + f"platinum/page/date={DAY}/index.html", encoding="utf-8").read()
strips = re.findall(r"data-month-chart>(.*?)</div>", html)
CELL = re.compile(r'<i class=(\w)[^>]*?data-m=(?:"([^"]+)"|(\w{3}))[^>]*>')


def cells_of(s):
    """[(class, label)] of a strip; the label may be quoted and carry a year, and the cell may carry data-part (rounds 21, 22)."""
    return [(k, (q or u)[:3]) for k, q, u in CELL.findall(s)]


cells = [cells_of(s) for s in strips]
rec["cells_with_no_data_m"] = sum(len(re.findall(r"<i class=", s)) for s in strips) - sum(len(c) for c in cells)
rec["strips"] = len(strips)
rec["strips_every_cell_labelled"] = sum(1 for c in cells if c and all(lab for _, lab in c))
rec["cells_per_strip"] = dict(collections.Counter(len(c) for c in cells))
rec["last_cell_label"] = dict(collections.Counter(c[-1][1] for c in cells if c))
rec["positional_css_rules_left"] = len(re.findall(r'nth-child\(\d+\)::before\{content:"[A-Za-z]{3}"\}', html))
rec["attr_css_present"] = "attr(data-m)" in html

objs = {}
for f in glob.glob(base + f"platinum/page/date={DAY}/charts/*.json"):
    o = json.load(open(f, encoding="utf-8"))
    objs[o["fund"]] = o["securities"]
agree = disagree = no_strip = label_names_ok = 0
examples = []
for seg in html.split('data-sec-dialog="')[1:]:
    key = seg.split('"', 1)[0]
    for sec in re.split(r"(?=<section data-fund=)", seg)[1:]:
        fm = re.match(r"<section data-fund=[\"']?([A-Za-z0-9_]+)", sec)
        if not fm or "data-chart-fund" not in sec:
            continue
        fund = fm.group(1)
        st = re.search(r"data-month-chart>(.*?)</div>", sec)
        if not st:
            no_strip += 1
            continue
        got = cells_of(st.group(1))
        y, mo = int(DAY[:4]), int(DAY[5:7])
        yms = []
        for _ in got:
            yms.append(f"{y:04d}-{mo:02d}")
            y, mo = (y - 1, 12) if mo == 1 else (y, mo - 1)
        yms.reverse()
        lab = {ym: k for ym, (k, _name) in zip(yms, got)}
        names_ok = all(MON[int(ym[5:7]) - 1] == name for ym, (_k, name) in zip(yms, got))
        traded = {ym for ym, k in lab.items() if k in ("u", "d")}
        mk = (objs.get(fund, {}).get(key) or {}).get("markers") or []
        mk_months = {x["end"][:7] for x in mk}
        label_names_ok += int(names_ok)
        if traded == (mk_months & set(lab)):
            agree += 1
        else:
            disagree += 1
            if len(examples) < 8:
                examples.append({"fund": fund, "key": key, "strip_traded": sorted(traded), "marker_months": sorted(mk_months),
                                 "labels": list(lab)})
rec["dialog_strips_whose_labels_count_back_from_the_page_month"] = label_names_ok
rec["dialog_strips_compared"] = agree + disagree
rec["dialog_strips_agreeing_with_marker_months"] = agree
rec["dialog_strips_disagreeing"] = disagree
rec["fund_sections_with_a_chart_and_no_strip"] = no_strip
rec["disagreement_examples"] = examples
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=2)
print(json.dumps(rec, indent=2))
