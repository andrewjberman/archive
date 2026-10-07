"""RIV-fe-1 AC1 (ROUND_ANALYSIS.round11.md rulings 1-2 @3ae96d6bc7; CVO C-S47 + row Z-S50; Andrew-direct 2026-10-06 ~16:3xZ "the
modal popup for that fund's engagement with that security"): every security button inside fund F's panel opens a modal that
carries F's section, and the page counts that itself.

Measured on the served 10-06 page (CVO census, C-S47): 15 mentions (3 securities, 2 funds) open a modal with no section for the
linking fund -- Nebius (two keys, S43, pk-1), Alphabet (a share-class name crossing to the other listing), SpaceX (a fresh GQGU
entry with no contribution row, so `_sec_dialogs` writes no GQGU section).

Interface (prescribed):
  - a name mention inside fund F's panel links to the key F holds or traded among the keys carrying that name (a name two
    listings share resolves by F's own holdings, Z-S50); only when F holds none of them does the page-wide rule apply;
  - `_sec_dialogs` writes a `section data-fund=<_fid(F)>` for EVERY fund F with a contribution row OR a trend row for that key
    (a trend-only fund's section states its buying; no contribution table);
  - `render.fund_section_census(html) -> {"buttons": n, "with_section": m, "missing": k}` counts every `data-sec` button inside a
    `data-fund-panel` and whether its target modal carries that fund's section; `publish_page` puts it in the manifest
    (`fund_sections`) and prints a line starting `FAIL: fund sections missing` when k > 0.
Fixture: round 8's fc-1 AC1 page (IDVZ home, TXUE rival; Apple and Microsoft ranked and in the trend) plus: a trend-only TXUE line
in SPCX_US_Equity "Space Exploration Technologies Corp" in the 30-day period only (no contribution row, no YTD trend row), named in TXUE's AI text; IDVZ ranks GOOGL_US_Equity and TXUE ranks
GOOG_US_Equity, both named "Alphabet Inc"; IDVZ's AI account reads "IDVZ added Alphabet Inc over the last 30 trading days."
  - (a) per-button census, by this check's own walk: every data-sec button in a fund panel opens a modal with that fund's
    section (missing 0), and `render.fund_section_census` returns the same three counts;
  - (b) SpaceX: the button in TXUE's panel opens a modal carrying section data-fund=TXUE;
  - (c) Alphabet: the mention in IDVZ's AI text links to GOOGL_US_Equity (the listing IDVZ holds);
  - (d) control: Apple in IDVZ's rankings still opens Apple's modal, which carries IDVZ's section.
FAIL at base: (a), (b), (c) FAIL; (d) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PERIODS = ("R30", "QTD", "YTD")


def fixture():
    import _ui7 as u
    ctx = c.load_fc1().fixture()
    a1 = ctx["a1"]
    hc = a1["holding_contribution"]
    extra = []
    for r in hc:
        if r.get("axis") == "security" and r.get("bucket") == "MSFT_US_Equity":
            if r["fund_id"] == "IDVZ":
                extra.append(dict(r, bucket="GOOGL_US_Equity", security_name="Alphabet Inc"))
            else:
                extra.append(dict(r, bucket="GOOG_US_Equity", security_name="Alphabet Inc"))
    hc.extend(extra)
    bt = a1["buying_trend"]
    add = [dict(r, bucket="SPCX_US_Equity", security_name="Space Exploration Technologies Corp")
           for r in bt if r.get("fund_id") == "TXUE" and r.get("axis") == "security" and r.get("bucket") == "MSFT_US_Equity"
           and r.get("period") == "R30"]
    bt.extend(add)
    a1["research_hypotheses"].append(u.account("IDVZ", "activity_30d", "IDVZ added Alphabet Inc over the last 30 trading days."))
    for a in a1["research_hypotheses"]:
        if a.get("fund_id") == "TXUE":
            a["text"] = str(a.get("text") or "") + " TXUE also opened Space Exploration Technologies Corp."
    return ctx


def walk(node, panel, out):
    p = node.attrs.get("data-fund-panel") or panel
    if node.tag == "button" and "data-sec" in node.attrs:
        out.append((p, node))
    for ch in getattr(node, "children", []):
        if hasattr(ch, "attrs"):
            walk(ch, p, out)


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}
    found = []
    walk(root, None, found)
    in_panel = [(f, b) for f, b in found if f]

    def has_section(b, fund):
        t = ids.get(b.attrs.get("popovertarget"))
        return t is not None and any(x.tag == "section" and x.attrs.get("data-fund") == render._fid(fund) for x in t.iter())

    missing = [(f, b.attrs.get("data-sec")) for f, b in in_panel if not has_section(b, f)]
    mine = {"buttons": len(in_panel), "with_section": len(in_panel) - len(missing), "missing": len(missing)}
    theirs = render.fund_section_census(html) if hasattr(render, "fund_section_census") else None
    print("census (check):", mine, "| render.fund_section_census:", theirs, "| missing sample:", missing[:6])
    v.check(mine["missing"] == 0 and mine["buttons"] > 0 and theirs == mine,
            f"(a) every in-panel data-sec button opens a modal with its fund's section ({mine['with_section']} of {mine['buttons']})")

    sp = [b for f, b in in_panel if f == "TXUE" and b.attrs.get("data-sec") == "SPCX_US_Equity"]
    print("SpaceX buttons in TXUE:", len(sp), "| with TXUE section:", sum(1 for b in sp if has_section(b, "TXUE")))
    v.check(bool(sp) and all(has_section(b, "TXUE") for b in sp), "(b) SpaceX (trend-only in TXUE) opens a modal with TXUE's section")

    alpha = [b.attrs.get("data-sec") for n in nodes if n.attrs.get("data-ai-fund") == "IDVZ" for b in n.iter()
             if b.tag == "button" and "data-sec" in b.attrs and "Alphabet" in u.text(b)]
    print("Alphabet in IDVZ AI text ->", alpha)
    v.check(bool(alpha) and set(alpha) == {"GOOGL_US_Equity"}, "(c) 'Alphabet Inc' in IDVZ's AI text links to GOOGL_US_Equity")

    ap = [b for n in nodes if n.attrs.get("data-component") == "rankings" and n.attrs.get("data-rank-fund") == "IDVZ"
          for b in n.iter() if b.tag == "button" and b.attrs.get("data-sec") == "AAPL_US_Equity"]
    if not ap:
        ap = [b for f, b in in_panel if f == "IDVZ" and b.attrs.get("data-sec") == "AAPL_US_Equity"]
    v.check(bool(ap) and all(has_section(b, "IDVZ") for b in ap), "(d) control: Apple in IDVZ's panel opens a modal with IDVZ's section")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
