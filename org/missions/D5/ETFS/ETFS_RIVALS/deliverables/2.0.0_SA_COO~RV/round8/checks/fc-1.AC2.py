"""RIV-fc-1 AC2 (FWD-21; Andrew-direct "anytime a stock/ticker is mentioned, it should be clickable to the modal"): the AI text
links a security that it names by the page's own display name, not only by its security key. Measured at the first fc-1 build
(57f7403405, the worker's report): AI prose is linked only where it writes a security key (`..._US_Equity`) or a casing variant
of a page name; a name written exactly as the page spells it ("Apple Inc") stays plain text.

Interface (prescribed): in the AI text (`data-ai-fund` cards and their dialogs), every occurrence of a display name the page
carries for a security (the `_NAMES` map, whole-word) is a `<button data-sec="<key>" popovertarget=...>` resolving to that
security's `data-sec-dialog`; the citation list (`.rf-cite`) keeps its keys as text; a word that is only part of a name
("Inc", "Apple" alone) is not linked.
Fixture: as fc-1.AC1, with the TXUE account text "TXUE added Apple Inc and trimmed Microsoft Corp; the Inc filings were late."
  - (a) "Apple Inc" and "Microsoft Corp" in the AI text are data-sec buttons resolving to AAPL_US_Equity and MSFT_US_Equity;
  - (b) control: the bare word "Inc" in "the Inc filings" is not inside a data-sec button.
FAIL at the first fc-1 build: (a) FAILS; (b) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

TEXT = "TXUE added Apple Inc and trimmed Microsoft Corp; the Inc filings were late."


def load_ac1():
    p =pathlib.Path(__file__).resolve().parent / "fc-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]  # the fixture only; never run AC1's own verdict
    mod = type(sys)("fc1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    from rivalfunds import render

    ac1 = load_ac1()
    ctx = ac1.fixture()
    for a in ctx["a1"]["research_hypotheses"]:
        a["text"] = TEXT
    root = u.parse(render.render_page(ctx))
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}
    cards = [n for n in nodes if "data-ai-fund" in n.attrs]
    linked = {}
    for card in cards:
        for b in card.iter():
            if b.tag == "button" and "data-sec" in b.attrs:
                t = ids.get(b.attrs.get("popovertarget"))
                if t is not None and t.attrs.get("data-sec-dialog") == b.attrs["data-sec"]:
                    linked.setdefault(u.text(b).strip(), b.attrs["data-sec"])
    print("AI cards:", len(cards), "| linked mentions:", linked)
    v.check(linked.get("Apple Inc") == "AAPL_US_Equity" and linked.get("Microsoft Corp") == "MSFT_US_Equity",
            "(a) 'Apple Inc' and 'Microsoft Corp' in the AI text open their security dialogs")
    v.check("Inc" not in linked, "(b) control: the bare word 'Inc' is not linked")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
