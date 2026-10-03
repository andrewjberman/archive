"""RIV-ui-5 AC1 (RFW-U11, DESIGN.md C14 details/summary): each "Inputs that did not arrive" list is grouped by reason
with a count and a fund breakdown, not one repeated sentence per item; the per-security list opens on demand.
INTERFACE: `render._census(ctx)`. Each (input kind, reason) group is ONE element carrying `data-reason-count="<n>"`; its
text states the reason and the per-fund counts; the per-security items stay inside a closed <details>.

Pure, offline fixture, the gold_input_census reason strings for 2026-10-01:
  price: 765 missing "no G4 row for 2026-10-01; the rankings price it ..." (TXUE 400, BASG 300, IDVZ 65), 5 missing "no
  G4 px_close for 2026-10-01; ..." (TXUE), 1000 arrived; gics: 765 missing "no G4 row for 2026-10-01; the sector is read
  ..." (same split), 1005 arrived; holdings: 13 arrived.
  - the group counts are exactly {765, 5, 765} (data-reason-count);
  - the census text states "no G4 row for 2026-10-01" at most twice (once per kind) and "no G4 px_close" at most once
    (today 1530 and 5 times);
  - each 765 group names TXUE, BASG and IDVZ with 400, 300 and 65;
  - control: the summary still reads "1000 of 1770" for prices, and a security item (TXUE-S0001) is reachable but not on
    the face."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

DAY = "2026-10-01"
PX = "the rankings price it from the fund's own reported valuation"
GX = "the sector is read from the fund's G1 report where present"
SPLIT = (("TXUE", 400), ("BASG", 300), ("IDVZ", 65))


def _rows():
    rows = [
        {"input_kind": "holdings", "subject": f"F{i:02d}", "fund_id": f"F{i:02d}", "status": "arrived", "reason": None}
        for i in range(13)
    ]
    for kind, why in (("price", PX), ("gics", GX)):
        for fund, n in SPLIT:
            rows += [
                {
                    "input_kind": kind,
                    "subject": f"{fund}-S{i:04d}",
                    "fund_id": fund,
                    "status": "missing",
                    "reason": f"no G4 row for {DAY}; {why}",
                }
                for i in range(1, n + 1)
            ]
        rows += [
            {"input_kind": kind, "subject": f"OK-S{i:04d}", "fund_id": "TXUE", "status": "arrived", "reason": None}
            for i in range(1000 if kind == "price" else 1005)
        ]
    rows += [
        {
            "input_kind": "price",
            "subject": f"TXUE-P{i}",
            "fund_id": "TXUE",
            "status": "missing",
            "reason": f"no G4 px_close for {DAY}; {PX}",
        }
        for i in range(5)
    ]
    return rows


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render._census({"day": "2026-10-02", "a1": {"input_census": _rows()}})
    root = u.parse(html)
    t, fc = u.text(root), u.face(root)
    groups = root.all("data-reason-count")
    counts = sorted(int(g.attrs["data-reason-count"]) if g.attrs["data-reason-count"].isdigit() else -1 for g in groups)
    print("census face:", fc[:400])
    print("reason groups:", counts)
    v.check(counts == [5, 765, 765], f"one group per (kind, reason) with its count (found {counts})")
    n_row, n_px = t.count(f"no G4 row for {DAY}"), t.count(f"no G4 px_close for {DAY}")
    v.check(n_row <= 2 and n_px <= 1, f"each reason is stated once per group, not per item ({n_row} and {n_px} times)")
    big = [u.text(g) for g in groups if g.attrs["data-reason-count"] == "765"]
    split_ok = len(big) == 2 and all(
        re.search(rf"\b{f}\b", g) and re.search(rf"\b{n}\b", g) for g in big for f, n in SPLIT
    )
    v.check(split_ok, "each 765 group carries its fund breakdown (TXUE 400, BASG 300, IDVZ 65)")
    v.check(
        "1000 of 1770" in t and "TXUE-S0001" in t and "TXUE-S0001" not in fc,
        "control: the summary counts stay, and the per-security list is reachable on demand only",
    )


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
