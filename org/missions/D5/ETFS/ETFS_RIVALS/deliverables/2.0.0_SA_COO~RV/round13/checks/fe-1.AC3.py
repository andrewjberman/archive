"""RIV-fe-1 AC3 (AMENDMENT 1; CTO half NEVER_WIDEN_ROUND13_FE1_DEPLOY_CTO_HALF.md @2f44b42430, "The 2 Alphabet mentions", case 1):
a name in fund F's AI text links to the listing F holds, even when another listing's rows carry that name as a variant.

Measured on the served 2026-10-06 page (batch rv-publish-1006r13, after fe-1): WCMG's activity_30d account reads "The biggest
losses were Alphabet Inc at -0.37%" and cites `WCMG|R30|GOOGL_US_Equity`; WCMG holds GOOGL_US_Equity (page name "Alphabet Inc")
and no GOOG row. The page renders that mention as a button to GOOG_US_Equity reading "Alphabet Inc-Cl C" (2 mentions), whose modal
has no WCMG section -- the 2 of the 10 `fund_sections` misses that are not Nebius. Cause read in `render._collect_aliases`: a row
carries a casing variant of "Alphabet Inc" for GOOG, so the alias "alphabet inc" maps to GOOG's page name, and the second loop's
`setdefault` keeps it over GOOGL's own page name; the text is rewritten before the fund-aware rule (fe-1) sees it.

Interface (prescribed): inside fund F's panel, a name (or alias) that resolves to several keys' names links to the key F holds or
traded, and reads that key's page name; the account's cited key breaks any remaining tie (round 9 RIV-ln-1). A page name of the
key F holds is never rewritten to another security's name.
Fixture: round 8's fc-1 AC1 page; IDVZ ranks GOOGL_US_Equity "Alphabet Inc"; TXUE ranks GOOG_US_Equity "Alphabet Inc-Cl C" and one
of its rows names GOOG "ALPHABET INC"; IDVZ's account reads "IDVZ's biggest loss was Alphabet Inc at -0.37%." citing
IDVZ|R30|GOOGL_US_Equity; TXUE's account reads "TXUE trimmed Alphabet Inc-Cl C."
  - (a) the mention in IDVZ's AI text is a button to GOOGL_US_Equity reading "Alphabet Inc" (never "Alphabet Inc-Cl C");
  - (b) every data-sec button in IDVZ's panel opens a modal with IDVZ's section (missing 0 for IDVZ);
  - (c) control: "Alphabet Inc-Cl C" in TXUE's AI text links GOOG_US_Equity.
FAIL at base (CLOUD 98de9868ce): (a), (b) FAIL; (c) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def fixture():
    import _ui7 as u
    ctx = c.load_fc1().fixture()
    a1 = ctx["a1"]
    hc = a1["holding_contribution"]
    extra, variant_done = [], False
    for r in hc:
        if r.get("axis") == "security" and r.get("bucket") == "MSFT_US_Equity":
            if r["fund_id"] == "IDVZ":
                extra.append(dict(r, bucket="GOOGL_US_Equity", security_name="Alphabet Inc"))
            else:
                name = "Alphabet Inc-Cl C" if variant_done else "ALPHABET INC"
                variant_done = True
                extra.append(dict(r, bucket="GOOG_US_Equity", security_name=name))
    hc.extend(extra)
    acc = [a for a in a1["research_hypotheses"] if a.get("fund_id") != "IDVZ"]
    for a in acc:
        if a.get("fund_id") == "TXUE":
            a["text"] = "TXUE trimmed Alphabet Inc-Cl C."
    idvz = u.account("IDVZ", "activity_30d", "IDVZ's biggest loss was Alphabet Inc at -0.37%.")
    idvz["cited_rows"] = '[{"table": "holding_contribution", "key": "IDVZ|R30|GOOGL_US_Equity", "value": -0.0037}]'
    a1["research_hypotheses"] = acc + [idvz]
    return ctx


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}

    def ai_buttons(fund):
        return [(b.attrs.get("data-sec"), u.text(b).strip()) for n in nodes if n.attrs.get("data-ai-fund") == fund
                for b in n.iter() if b.tag == "button" and "data-sec" in b.attrs and "Alphabet" in u.text(b)]

    got = ai_buttons("IDVZ")
    print("Alphabet in IDVZ AI text ->", got)
    v.check(bool(got) and all(k == "GOOGL_US_Equity" and t == "Alphabet Inc" for k, t in got),
            "(a) 'Alphabet Inc' in IDVZ's AI text links GOOGL_US_Equity and reads 'Alphabet Inc'")

    def panel_buttons(node, panel, out):
        p = node.attrs.get("data-fund-panel") or panel
        if node.tag == "button" and "data-sec" in node.attrs and p:
            out.append((p, node))
        for ch in getattr(node, "children", []):
            if hasattr(ch, "attrs"):
                panel_buttons(ch, p, out)

    found = []
    panel_buttons(root, None, found)

    def has_section(b, fund):
        t = ids.get(b.attrs.get("popovertarget"))
        return t is not None and any(x.tag == "section" and x.attrs.get("data-fund") == render._fid(fund) for x in t.iter())

    miss = [b.attrs.get("data-sec") for f, b in found if f == "IDVZ" and not has_section(b, "IDVZ")]
    n_idvz = sum(1 for f, _ in found if f == "IDVZ")
    print("IDVZ panel buttons:", n_idvz, "| without IDVZ's section:", miss)
    v.check(n_idvz > 0 and not miss, f"(b) every button in IDVZ's panel opens a modal with IDVZ's section ({n_idvz - len(miss)} of {n_idvz})")

    tx = ai_buttons("TXUE")
    print("Alphabet in TXUE AI text ->", tx)
    v.check(bool(tx) and all(k == "GOOG_US_Equity" for k, _ in tx), "(c) control: 'Alphabet Inc-Cl C' in TXUE's AI text links GOOG_US_Equity")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
