# -*- coding: utf-8 -*-
# Semantic-pass specimen-sheet generator -- MP vertical, 16 items from
# ARTIFACT_CENSUS_MP.yaml @0c1dae3da (census vintage 2026-08-10).
# One template -> 16 HTML files; the notation block is IDENTICAL by construction.
import html as H
import json
import pathlib

OUT = pathlib.Path(__file__).parent

CSS = """
:root{
  --paper:#f2f4f8; --card:#ffffff; --ink:#1b2433; --ink-2:#4c5а68;
  --ink-2:#4c586b; --line:#d7dde8; --accent:#0e7c86; --accent-ink:#0a5a62;
  --mono-bg:#eaeef5; --live:#256d47; --live-bg:#e2f0e8; --unr:#8a5a12;
  --unr-bg:#f5ead4; --frozen:#973b34; --frozen-bg:#f6e2e0; --note-line:#c4cddb;
}
:root:not([data-theme="light"]){}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#131720; --card:#1b2130; --ink:#e2e8f2; --ink-2:#9aa7ba;
    --line:#2c3547; --accent:#4cc3cd; --accent-ink:#7ed7de; --mono-bg:#242c3d;
    --live:#7fc9a0; --live-bg:#1d3529; --unr:#dcae5e; --unr-bg:#3a2f18;
    --frozen:#e08e86; --frozen-bg:#402420; --note-line:#3a4558;
  }
}
:root[data-theme="dark"]{
  --paper:#131720; --card:#1b2130; --ink:#e2e8f2; --ink-2:#9aa7ba;
  --line:#2c3547; --accent:#4cc3cd; --accent-ink:#7ed7de; --mono-bg:#242c3d;
  --live:#7fc9a0; --live-bg:#1d3529; --unr:#dcae5e; --unr-bg:#3a2f18;
  --frozen:#e08e86; --frozen-bg:#402420; --note-line:#3a4558;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:60rem;margin:0 auto;padding:2.2rem 1.4rem 4rem}
.eyebrow{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent-ink);font-weight:600}
h1{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;
  font-size:clamp(1.15rem,3.2vw,1.7rem);margin:.35rem 0 .8rem;text-wrap:balance;
  word-break:break-all}
.chips{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 1.4rem}
.chip{font-size:.72rem;font-weight:600;letter-spacing:.05em;padding:.18rem .6rem;
  border-radius:999px;border:1px solid var(--line);color:var(--ink-2)}
.chip.live{color:var(--live);background:var(--live-bg);border-color:transparent}
.chip.unrendered{color:var(--unr);background:var(--unr-bg);border-color:transparent}
.chip.frozen{color:var(--frozen);background:var(--frozen-bg);border-color:transparent}
.coords{background:var(--card);border:1px solid var(--line);border-radius:8px;
  padding:.8rem 1rem;margin-bottom:1.2rem;font-size:.88rem}
.coords b{color:var(--accent-ink)}
.coords .arrow{color:var(--ink-2);padding:0 .35rem}
h2{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-2);margin:1.9rem 0 .6rem}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));
  gap:.7rem}
.fact{background:var(--card);border:1px solid var(--line);border-radius:8px;
  padding:.65rem .85rem}
.fact .k{font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-2);margin-bottom:.2rem}
.fact .v{font-size:.86rem;overflow-wrap:anywhere}
code,.mono{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;
  font-size:.85em;background:var(--mono-bg);padding:.08em .3em;border-radius:4px}
.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;
  background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:.84rem}
th{font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;text-align:left;
  color:var(--ink-2);padding:.55rem .8rem;border-bottom:1px solid var(--line)}
td{padding:.45rem .8rem;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
td.fname{font-family:ui-monospace,Consolas,monospace;white-space:nowrap;
  font-size:.8rem}
td.num{font-variant-numeric:tabular-nums}
.evid{font-size:.82rem;color:var(--ink-2);background:var(--card);
  border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:8px;padding:.7rem .95rem;margin:.5rem 0}
.qblock{margin-top:2.6rem;border:2px solid var(--accent);border-radius:10px;
  background:var(--card);padding:1.2rem 1.4rem 1.5rem}
.qblock .qhead{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent-ink);font-weight:700;margin-bottom:.9rem}
.q{margin:1.05rem 0 0}
.q .qn{font-weight:700;font-size:.9rem}
.q .qt{font-size:.9rem;margin:.15rem 0 .4rem;color:var(--ink)}
.q .blank{border-bottom:1px dashed var(--note-line);height:1.7rem}
.q .blank+.blank{margin-top:.35rem}
.foot{margin-top:2.2rem;font-size:.74rem;color:var(--ink-2)}
"""

# The IDENTICAL semantic-pass notation block (verbatim on every artifact).
QUESTIONS = [
 ("Q1 -- Canonical name",
  "What is this artifact's canonical name in DATA_CATALOG v0.2?"),
 ("Q2 -- Business meaning",
  "In one sentence: what does this artifact mean to the business?"),
 ("Q3 -- Vintage semantics",
  "Which field is THE vintage, and what does its date mean (T-1 trading frontier / generation time / month-end / other)?"),
 ("Q4 -- Analyst serve/deny",
  "May OPAL_ANALYST serve figures from this artifact? SERVE / DENY / SERVE-WITH-CAVEAT (name the caveat)."),
 ("Q5 -- Disposition",
  "Keep as-is / consolidate / migrate / decommission?"),
 ("Q6 -- Notes",
  "Anything else on this item."),
]

def chips(it):
    out = [f'<span class="chip {it["state_class"]}">{H.escape(it["state"])}</span>',
           f'<span class="chip">{H.escape(it["tier"])}</span>',
           f'<span class="chip">{H.escape(it["rendered"])}</span>']
    if it.get("family"):
        out.append(f'<span class="chip">{H.escape(it["family"])}</span>')
    return "\n".join(out)

def facts(it):
    cells = ""
    for k, v in it["facts"]:
        cells += f'<div class="fact"><div class="k">{H.escape(k)}</div><div class="v">{v}</div></div>\n'
    return cells

def fields_table(it):
    if not it.get("fields"):
        return ""
    rows = "".join(
        f'<tr><td class="fname">{H.escape(n)}</td><td>{H.escape(t)}</td>'
        f'<td>{H.escape(x)}</td></tr>' for n, t, x in it["fields"])
    return (f'<h2>Fields (census-grounded, live read 2026-08-10)</h2>'
            f'<div class="tblwrap"><table><thead><tr><th>field</th><th>type</th>'
            f'<th>note / example</th></tr></thead><tbody>{rows}</tbody></table></div>')

def qblock():
    qs = "".join(
        f'<div class="q"><div class="qn">{H.escape(n)}</div>'
        f'<div class="qt">{H.escape(t)}</div>'
        f'<div class="blank"></div><div class="blank"></div></div>'
        for n, t in QUESTIONS)
    return (f'<div class="qblock"><div class="qhead">Andrew notation -- semantic pass '
            f'(identical block on every artifact)</div>{qs}</div>')

def page(it, idx, total):
    coords = it.get("coords") or "no visual site on any page (served-but-unrendered)"
    evid = "".join(f'<div class="evid">{e}</div>' for e in it["evidence"])
    return f"""<title>MP {idx:02d} · {H.escape(it['short'])}</title>
<style>{CSS}</style>
<div class="wrap">
  <div class="eyebrow">Opal semantic pass · Model Portfolios vertical · item {idx} of {total} · census @0c1dae3da (2026-08-10)</div>
  <h1>{H.escape(it['key'])}</h1>
  <div class="chips">{chips(it)}</div>
  <div class="coords"><b>Coordinates</b><span class="arrow">→</span>{coords}</div>
  <h2>Facts</h2>
  <div class="facts">{facts(it)}</div>
  {fields_table(it)}
  <h2>Evidence</h2>
  {evid}
  {qblock()}
  <div class="foot">Author 0.5.0_AE_OpalETL~Z · all evidence first-hand · source of truth: ARTIFACT_CENSUS_MP.yaml @0c1dae3da · ruling record @d2f2e01d9</div>
</div>"""

ITEMS = json.loads((OUT / "items.json").read_text(encoding="utf-8"))
for i, it in enumerate(ITEMS, 1):
    p = OUT / f"mp_{i:02d}_{it['slug']}.html"
    p.write_text(page(it, i, len(ITEMS)), encoding="utf-8")
    print(p.name)
