"""RIV-lk-1 AC1 (ROUND_ANALYSIS.round10.md ADDENDUM 4 step 3 @56de423b4d; ROUND_ANALYSIS.round11.md ruling 3 @3ae96d6bc7): once the
gateway serves the audit route, the main page carries its ONE link to the day's audit page, and the AI accounts' citation lines
(grounding records with machine keys) move off the main page onto the audit page.

Measured on the served 10-06 page (CVO): the AI modals carry 148 machine keys in 89 citation lines ("Cited rows: holding_contribution
NBIS_US_Equity = ..."), plain text; the main page has no audit link (au-1, by design until the route serves).

Interface (prescribed):
  - `render.render_page(ctx)`: exactly one `<a href="/rivalfunds/<day>/audit">` with "one step away" wording; no AI modal on the
    main page carries a "Cited rows:" line (the grade line, full text, Observed/Inferred and the invalidation stay);
  - `render.render_audit_page(ctx)`: a section `id="citations"` with, per fund and account, its "Cited rows:" line (and the
    [web] reads line when present), each block carrying `data-cited-fund="<fund>"` and `data-ai-kind="<kind>"`.
Fixture: round 8's fc-1 AC1 page; TXUE's account cites [holding_contribution AAPL_US_Equity = 0.012].
  - (a) the main page has exactly one link to /rivalfunds/<day>/audit and no "Cited rows:" text;
  - (b) the audit page's citations section carries TXUE's activity_30d block with "AAPL_US_Equity";
  - (c) control: the main page still carries TXUE's AI dialog with its grade line ("Grounded") and full text.
FAIL at base: (a), (b) FAIL; (c) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    ctx = c.load_fc1().fixture()
    for a in ctx["a1"]["research_hypotheses"]:
        if a.get("fund_id") == "TXUE":
            a["cited_rows"] = '[{"table": "holding_contribution", "key": "AAPL_US_Equity", "value": 0.012}]'
    day = ctx["day"]
    main = render.render_page(ctx)
    link = f'href="/rivalfunds/{day}/audit"'
    print("main: links", main.count(link), "| 'Cited rows:'", main.count("Cited rows:"))
    v.check(main.count(link) == 1 and "Cited rows:" not in main,
            f"(a) the main page has one {link} link and no citation lines")
    audit = render.render_audit_page(ctx) if hasattr(render, "render_audit_page") else ""
    root = u.parse(audit) if audit else None
    blocks = [] if root is None else [n for n in root.iter() if n.attrs.get("data-cited-fund") == "TXUE"
                                       and n.attrs.get("data-ai-kind") == "activity_30d"]
    sec = [] if root is None else [n for n in root.iter() if n.attrs.get("id") == "citations"]
    print("audit: citations section", len(sec), "| TXUE activity_30d blocks", len(blocks),
          "| AAPL in block", any("AAPL_US_Equity" in u.text(b) for b in blocks))
    v.check(bool(sec) and bool(blocks) and any("AAPL_US_Equity" in u.text(b) for b in blocks),
            "(b) the audit page's citations section carries TXUE's activity_30d citation line")
    mroot = u.parse(main)
    dlg = [n for n in mroot.iter() if n.attrs.get("data-ai-dialog") == "activity_30d"
           and "TXUE" in u.text(n)]
    v.check(bool(dlg) and any("Grounded" in u.text(d) for d in dlg),
            "(c) control: TXUE's AI dialog stays on the main page with its grade line")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
