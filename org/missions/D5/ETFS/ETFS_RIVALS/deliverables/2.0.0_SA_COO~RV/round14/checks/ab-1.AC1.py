"""RIV-ab-1 AC1 (row Z-S54; ROUND_ANALYSIS.round13.md ADDENDUM 1 @594d1be8f8 (C); Andrew-direct 2026-10-07 ~03:1xZ "not needed do
a and c"): the badge carries its claim -- "Grounded" only when the account's cited revision is the revision the page serves.

Measured on the served 2026-10-06 page: 22 of 26 accounts carry a figure that differs from the panel beside it (IDVZ: "Petrobras
... +0.47%" against the rankings' +0.93%), each under a green "Grounded"; the accounts cite holding_contribution revision
20261006T110357Z while the page serves 20261006T130556Z. The only disclosure is a small "Written against earlier tables" line.

Interface (prescribed): the PASS badge of an account is
  `<span class="rf-grounding-PASS" data-grade="PASS" data-build="served">Grounded</span>` when every revision its cited rows carry
  for a vintage table (holding_contribution, buying_trend) is a revision the page serves for that table, and
  `<span ... data-grade="PASS" data-build="earlier">Grounded on an earlier build</span>` otherwise -- the same element, the same
  place, the same weight. `render.grounding_census(html) -> {"served": n, "earlier": m}` counts the PASS badges by build (the
  publisher writes it into the manifest as `ai_grounding`). A FAIL badge is unchanged.
Fixture: round 8's fc-1 AC1 page; every holding_contribution row carries revision R_NEW; TXUE's account cites
holding_contribution TXUE|R30|AAPL_US_Equity at R_OLD; IDVZ's account cites IDVZ|R30|AAPL_US_Equity at R_NEW.
  - (a) TXUE's badge reads "Grounded on an earlier build" with data-build="earlier";
  - (b) IDVZ's badge reads exactly "Grounded" with data-build="served"; `render.grounding_census` reads {"served": 1, "earlier": 1};
  - (c) control: both accounts still carry a PASS badge and their text.
FAIL at base: (a), (b) FAIL (both read "Grounded", no data-build, no census); (c) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

R_OLD, R_NEW = "20261006T110357Z-9717671d0d45", "20261006T130556Z-bd0200b20c0a"


def fixture():
    import _ui7 as u
    ctx = c.load_fc1().fixture()
    a1 = ctx["a1"]
    for r in a1["holding_contribution"]:
        r["revision"] = R_NEW
    acc = [a for a in a1["research_hypotheses"] if a.get("fund_id") == "TXUE"]
    for a in acc:
        a["cited_rows"] = ('[{"table": "holding_contribution", "key": "TXUE|R30|AAPL_US_Equity", "revision": "%s", "value": 0.012}]'
                           % R_OLD)
    idvz = u.account("IDVZ", "activity_30d", "IDVZ held AAPL_US_Equity over the last 30 trading days.")
    idvz["cited_rows"] = ('[{"table": "holding_contribution", "key": "IDVZ|R30|AAPL_US_Equity", "revision": "%s", "value": 0.012}]'
                          % R_NEW)
    a1["research_hypotheses"] = acc + [idvz]
    return ctx


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)

    def badges(fund):
        out = []
        for card in (n for n in root.iter() if n.attrs.get("data-ai-fund") == fund):
            for n in card.iter():
                if n.attrs.get("data-grade") == "PASS" and n.tag == "span":
                    out.append((u.text(n).strip(), n.attrs.get("data-build")))
        return out

    tx, iv = badges("TXUE"), badges("IDVZ")
    print("TXUE badges:", tx, "| IDVZ badges:", iv)
    v.check(bool(tx) and all(b == ("Grounded on an earlier build", "earlier") for b in tx),
            "(a) an account citing an older revision reads 'Grounded on an earlier build'")
    census = render.grounding_census(html) if hasattr(render, "grounding_census") else None
    print("grounding_census:", census)
    v.check(bool(iv) and all(b == ("Grounded", "served") for b in iv) and census == {"served": 1, "earlier": 1},
            "(b) an account citing the served revision reads 'Grounded'; the census counts 1 served, 1 earlier")
    v.check(bool(tx) and bool(iv) and "IDVZ held" in html and "TXUE added" in html,
            "(c) control: both accounts keep a PASS badge and their text")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
