"""RIV-pd-2 AC1 (PRD v0.18 FWD-23; Andrew-direct periods @82bb78106e, MTD @96d0ab2f4b): every switch on the page offers the last
30, 90 and 365 days and opens on 30; no QTD, YTD or MTD is displayed anywhere on the main page or the audit page.

Measured today: `render.PERIODS = ("R30","QTD","YTD")`, `PERIOD_LABEL = {"R30": "Last 30 trading days", "QTD": "Quarter to date",
"YTD": "Year to date"}`; on the round-8 fc-1 page the main page shows "Quarter to date" 13 times and "Year to date" 13 times, the
audit page 2 and 2 (its security dialogs).

Interface (prescribed, verbatim): `render.PERIODS = ("R30","R90","R365")`; `PERIOD_LABEL = {"R30": "Last 30 days", "R90": "Last 90
days", "R365": "Last 365 days"}`; the switch reads 30d, the dividing line, then 90d and 365d, and opens on R30. No element of the
rendered main page or audit page carries the visible text QTD, YTD, MTD, "Quarter to date", "Year to date" or "Month to date".
Rows of MTD / QTD / YTD in the context are ignored, not an error.
Fixture: round 8's fc-1 page (IDVZ home, TXUE rival, Apple and Microsoft); its holding_contribution and buying_trend rows are
given for R30, R90, R365 AND MTD, QTD, YTD. Visible text = element text with tags, <style> and <script> stripped (`_ui7.text`).
  - (a) `render.PERIODS == ("R30","R90","R365")` and `render.PERIOD_LABEL` is exactly the prescribed mapping;
  - (b) the visible text of the main page and of the audit page holds none of QTD, YTD, MTD (whole words), "Quarter to date",
        "Year to date", "Month to date" (any case);
  - (c) the period radios are rf-period-R30, rf-period-R90, rf-period-R365 in that order and only R30 is checked; every switch
        (each `.rf-segs` holding period labels) reads R30, the dividing line, R90, R365; each fund has a rank panel for exactly
        R30, R90 and R365;
  - (d) control: both pages render from a context carrying all six periods; the R30 radio exists and is checked; each fund's
        R30 rank panel names Apple Inc.
FAIL at base: (a), (b), (c) FAIL; (d) PASSES."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SIX = ("R30", "R90", "R365", "MTD", "QTD", "YTD")
WANT_PERIODS = ("R30", "R90", "R365")
WANT_LABEL = {"R30": "Last 30 days", "R90": "Last 90 days", "R365": "Last 365 days"}
BANNED = (r"\bQTD\b", r"\bYTD\b", r"\bMTD\b", r"(?i)quarter to date", r"(?i)year to date", r"(?i)month to date")


def fixture():
    """fc-1's page with every A1 row of its R30 block repeated for each of the six periods."""
    ctx = c.load_fc1().fixture()
    a1 = ctx["a1"]
    for table in ("holding_contribution", "buying_trend"):
        base = [r for r in a1[table] if r.get("period") == "R30"]
        a1[table] = [dict(r, period=p) for p in SIX for r in base]
    return ctx


def banned_hits(text):
    return {pat: len(re.findall(pat, text)) for pat in BANNED if re.search(pat, text)}


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    print("render.PERIODS:", render.PERIODS, "| PERIOD_LABEL:", render.PERIOD_LABEL)
    v.check(tuple(render.PERIODS) == WANT_PERIODS and dict(render.PERIOD_LABEL) == WANT_LABEL,
            "(a) PERIODS is (R30, R90, R365) and PERIOD_LABEL names the last 30 / 90 / 365 days")

    ctx = fixture()
    main, audit = render.render_page(ctx), render.render_audit_page(fixture())
    hits_main, hits_audit = banned_hits(u.text(main)), banned_hits(u.text(audit))
    print("visible banned text: main", hits_main, "| audit", hits_audit)
    v.check(not hits_main and not hits_audit, "(b) no QTD / YTD / MTD or its long name is visible on the main or the audit page")

    root = u.parse(main)
    nodes = list(root.iter())
    radios = [(n.attrs.get("id"), "checked" in n.attrs) for n in nodes if n.tag == "input" and n.attrs.get("name") == "rf-period"]
    switches = []
    for s in root.cls("rf-segs"):
        seq = [("|" if "data-period-divider" in ch.attrs else (ch.attrs.get("for") or "")[len("rf-period-"):])
               for ch in s.children if not isinstance(ch, str)
               and ("data-period-divider" in ch.attrs or (ch.attrs.get("for") or "").startswith("rf-period-"))]
        if seq:
            switches.append(seq)
    panels = {}
    for n in nodes:
        if "data-rank-period" in n.attrs:
            panels.setdefault(n.attrs.get("data-rank-fund"), set()).add(n.attrs["data-rank-period"])
    print("period radios (id, checked):", radios)
    print("switches:", len(switches), "| distinct orders:", sorted({tuple(s) for s in switches}), "| rank panels:", panels)
    v.check(radios == [("rf-period-R30", True), ("rf-period-R90", False), ("rf-period-R365", False)]
            and bool(switches) and all(s == ["R30", "|", "R90", "R365"] for s in switches)
            and all(panels.get(f) == set(WANT_PERIODS) for f in ("IDVZ", "TXUE")),
            "(c) every switch reads R30, the dividing line, R90, R365 and opens on R30; a rank panel per fund per period")

    r30 = [n for n in nodes if n.attrs.get("data-rank-period") == "R30"]
    apple = {n.attrs.get("data-rank-fund"): "Apple Inc" in u.text(n) for n in r30}
    print("R30 radio checked:", ("rf-period-R30", True) in radios, "| Apple Inc in the R30 rank panel:", apple,
          "| main bytes:", len(main), "| audit bytes:", len(audit))
    v.check(("rf-period-R30", True) in radios and apple.get("IDVZ") is True and apple.get("TXUE") is True and bool(audit),
            "(d) control: the page renders with six periods in the context, opens on R30 and shows the R30 rankings")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
