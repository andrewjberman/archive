"""RIV-au-1 AC1 (row Z-S47; ROUND_ANALYSIS.round10.md ADDENDUM 3 @8f1c1a9e6e as re-sequenced by ADDENDUM 4 @56de423b4d; Andrew-direct
2026-10-06 ~16:3xZ "Any mention of a security by ticker should be hyperlinked to the modal popup for that fund's engagement with
that security" and ~16:4xZ "1.) Pull audit off the page 2.) Get those linking schemas up and running 3.) Make an audit gateway
after 2.) is done"): the audit trail leaves the main page for its own document (NOT linked until the gateway route serves), and
BOTH documents link every security mention to a dialog in the same document.

Measured at the cut: the served 2026-10-06 page is 1,813,001 B with data-holding-dialogs="off" (0 links); its closed
`<details id="audit">` block is 1,119,671 B of it, so the with-dialogs render crosses render.DIALOG_SOFT_CAP (1,950,000 B).

Interface (prescribed):
  - `render.render_page(ctx)` returns the MAIN page: no `<details id="audit">`, no `id="trades"`, no `id="holdings"`, and NO
    link to `/rivalfunds/<day>/audit` yet (ADDENDUM 4: the link lands only after the route serves, never a 404);
  - `render.render_audit_page(ctx)` returns the AUDIT page: a whole document (`<!DOCTYPE html>` ... `</html>`) carrying the
    trades (`id="trades"`), holdings (`id="holdings"`) and status sections, one `<details class="trace"` per trade, and its OWN
    `data-sec-dialog` dialogs (from `_sec_dialogs`) for the securities it names; every `data-sec` button resolves to a
    `data-sec-dialog` element in the SAME document (popovertarget works within one document only).
Fixture: round 8's fc-1 AC1 page (IDVZ home, TXUE rival; Apple and Microsoft ranked; one TXUE trade in Apple).
  - (a) main page: no audit block, no trades or holdings section, exactly ONE link to /rivalfunds/<day>/audit (amended 2026-10-07
    after RIV-lk-1: the gateway route serves since release r23 @7d65a28db0, row Z-W2-S15);
  - (b) audit page: whole document; trades and holdings sections once each; trace panels == the context's trade count; Apple in
    the trade log is a data-sec button resolving to Apple's dialog in the audit document;
  - (c) control: on both documents every data-sec button resolves in-document and no data-sec-dialog key repeats; the main page
    still renders a rank panel per fund for R30, QTD and YTD with Apple linked in the rankings; neither carries `<script`.
FAIL at base: (a) and (b) FAIL; (c) PASSES on the main page (the audit page does not exist; the arm reads the main page only)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PERIODS = ("R30", "QTD", "YTD")


def _resolve_all(u, html):
    root = u.parse(html)
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}
    dialogs = [n for n in nodes if "data-sec-dialog" in n.attrs]
    buttons = [n for n in nodes if n.tag == "button" and "data-sec" in n.attrs]

    def resolves(b):
        t = ids.get(b.attrs.get("popovertarget"))
        return t is not None and t.attrs.get("data-sec-dialog") == b.attrs.get("data-sec")

    keys = [d.attrs["data-sec-dialog"] for d in dialogs]
    ok = bool(buttons) and all(resolves(b) for b in buttons) and len(keys) == len(set(keys))
    return nodes, buttons, dialogs, resolves, ok


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    ctx = c.load_fc1().fixture()
    day = ctx["day"]
    n_trades = sum(f.get("n_trades", 0) for g in ctx["groups"] for f in g["funds"] if f.get("status") == "updated")
    main = render.render_page(ctx)
    link = f"/rivalfunds/{day}/audit"
    print("main bytes:", len(main.encode("utf-8")), "| audit block in main:", '<details id="audit"' in main,
          "| links to audit:", main.count(link))
    v.check('<details id="audit"' not in main and 'id="trades"' not in main and 'id="holdings"' not in main
            and main.count(link) == 1, f"(a) the main page carries no audit trail and exactly one {link} link (lk-1, after the route served)")

    audit = None
    if hasattr(render, "render_audit_page"):
        audit = render.render_audit_page(ctx)
    if audit is None:
        v.check(False, "(b) render.render_audit_page exists and returns the audit document")
    else:
        a_nodes, a_buttons, a_dialogs, a_res, _ = _resolve_all(u, audit)
        n_trace = audit.count('<details class="trace"')
        apple = any(b.attrs.get("data-sec") == "AAPL_US_Equity" and a_res(b)
                    for h in a_nodes if "data-trades" in h.attrs for b in h.iter() if b.tag == "button" and "data-sec" in b.attrs)
        print("audit bytes:", len(audit.encode("utf-8")), "| traces:", n_trace, "of", n_trades, "| buttons:", len(a_buttons),
              "| dialogs:", len(a_dialogs), "| Apple linked in trade log:", apple)
        v.check(audit.startswith("<!DOCTYPE html>") and audit.rstrip().endswith("</html>")
                and audit.count('id="trades"') == 1 and audit.count('id="holdings"') == 1 and n_trace == n_trades and apple,
                "(b) the audit page is whole, carries trades and holdings once, one trace per trade, Apple linked in the trade log")

    nodes, buttons, dialogs, res, ok_main = _resolve_all(u, main)
    panels = {(n.attrs.get("data-rank-fund"), n.attrs.get("data-rank-period")) for n in nodes if "data-rank-period" in n.attrs}
    apple_rank = any(b.attrs.get("data-sec") == "AAPL_US_Equity" and res(b) for h in nodes
                     if h.attrs.get("data-component") == "rankings" for b in h.iter() if b.tag == "button" and "data-sec" in b.attrs)
    ok_audit = True if audit is None else _resolve_all(u, audit)[4]
    no_script = "<script" not in main.lower() and (audit is None or "<script" not in audit.lower())
    print("main buttons:", len(buttons), "| main dialogs:", len(dialogs), "| Apple in rankings:", apple_rank)
    v.check(ok_main and ok_audit and no_script and apple_rank and all((f, p) in panels for f in ("IDVZ", "TXUE") for p in PERIODS),
            "(c) control: every data-sec button resolves in its own document, no key repeats, rank panels per fund, no script")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
