"""RIV-ln-1 AC1 (CVO C-S35, fc-1 J1 NOT MET on the AI text): a display name that several KEY FORMS of one security carry opens
that security's dialog. Measured on the served 10-05 page (batch rv-publish-1005r8b): 395 AI-text mentions of 43 securities
that have a modal are plain text; in the page's own render context 428 of 860 display names are carried by more than one key
(e.g. 'Enel SpA' <- 29265W207, ENEL_IM_Equity, 'ENEL IM Equity'), and `render._render_page` keeps a name in `_NAME_KEYS` only
when exactly one key carries it (render.py:1769), so every such name renders as plain words; 'E.On Se' (one key) links.

Interface (prescribed): a page name whose keys include exactly ONE key with a dialog on the page links to that key; a name two
dialog-bearing securities share links to the key the account's citation list names, else stays plain with both identifiers in
its title. A name one key carries links as today.
Fixture (offline): round 8's fc-1.AC1 page (IDVZ home, TXUE rival; Apple and Microsoft held and ranked), with the page's name map
also carrying 'Apple Inc' for the key forms 'AAPL US Equity' and '037833100' (as the served map carries three forms per name),
and TXUE's account text "TXUE added Apple Inc and trimmed Microsoft Corp.":
  - (a) 'Apple Inc' in the AI text is a data-sec button resolving to the AAPL_US_Equity dialog;
  - (b) control: 'Microsoft Corp' (one key) is a data-sec button resolving to the MSFT_US_Equity dialog.
FAIL at base: (a) FAILS (the name has three keys and is dropped); (b) PASSES."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parents[1] / "round8" / "checks"))
import _common as c  # noqa: E402

TEXT = "TXUE added Apple Inc and trimmed Microsoft Corp."


def load_fc1():
    p = HERE.parents[1] / "round8" / "checks" / "fc-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]  # the fixture only; never run fc-1's own verdict
    mod = type(sys)("fc1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    import _ui7 as u

    from rivalfunds import render

    ctx = load_fc1().fixture()
    for a in ctx["a1"]["research_hypotheses"]:
        a["text"] = TEXT
    orig = render._collect_names

    def names(cx):
        out = dict(orig(cx))
        out.setdefault("AAPL US Equity", out.get("AAPL_US_Equity", "Apple Inc"))
        out.setdefault("037833100", out.get("AAPL_US_Equity", "Apple Inc"))
        return out

    render._collect_names = names
    try:
        root = u.parse(render.render_page(ctx))
    finally:
        render._collect_names = orig
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}
    linked = {}
    for card in (n for n in nodes if "data-ai-fund" in n.attrs):
        for b in card.iter():
            if b.tag == "button" and "data-sec" in b.attrs:
                t = ids.get(b.attrs.get("popovertarget"))
                if t is not None and t.attrs.get("data-sec-dialog") == b.attrs["data-sec"]:
                    linked.setdefault(u.text(b).strip(), b.attrs["data-sec"])
    print("AI-text links:", linked)
    v.check(linked.get("Apple Inc") == "AAPL_US_Equity", "(a) 'Apple Inc', carried by three key forms, opens the AAPL_US_Equity dialog")
    v.check(linked.get("Microsoft Corp") == "MSFT_US_Equity", "(b) control: 'Microsoft Corp' (one key) opens its dialog")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
