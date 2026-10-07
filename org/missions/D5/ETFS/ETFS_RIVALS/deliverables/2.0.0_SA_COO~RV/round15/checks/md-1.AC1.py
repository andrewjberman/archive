"""RIV-md-1 AC1 (PRD v0.18 FWD-22; ADDENDUM F.7; Andrew-direct modal @ad78eef973): every fund section of a security dialog carries
a chart frame -- the fund, the security, a three-way range switch, a status line and the fund's trades in words -- in the HTML
itself, so the words are there with or without the script.

Measured today on the round-8 fc-1 page: 2 security dialogs, 4 `<section data-fund=...>` blocks, 0 elements with `data-chart-fund`;
each dialog carries `data-history=none` and reads "History not yet backfilled".

Interface (prescribed, verbatim): each `<section data-fund=...>` of a security dialog gains a chart frame `<div class=rf-chart
data-chart-fund="<FUND>" data-chart-key="<security_key>">` holding a three-way range switch (30d first, then 90d, 365d), a words
line (`data-chart-status`) and the fund's trade list in words (from the context's trades; present with or without the script).
`data-history=none` and HISTORY_NONE leave the dialog.
Fixture: round 8's fc-1 page: IDVZ (home) and TXUE (rival); Apple and Microsoft each in both funds' rankings; ONE trade in the
context, TXUE's add of Apple (window 2026-09-30 to 2026-10-01). Text is read with <style> and <script> stripped (`_ui7.text`).
  - (a) every fund section of every security dialog holds exactly one `div.rf-chart` whose `data-chart-fund` is the section's
        fund and whose `data-chart-key` is the dialog's security key (4 frames for 4 sections);
  - (b) every frame holds an element carrying `data-chart-status`, and its text names the ranges 30, 90, 365 in that order
        (the first mentions of "30d" / "90d" / "365d", or "30 days" / "90 days" / "365 days");
  - (c) TXUE's Apple frame says "Bought" (its one trade, in words); IDVZ's Apple frame says neither "Bought" nor "Sold";
  - (d) no dialog carries `data-history` and the page no longer reads "History not yet backfilled";
  - (e) control: the page has 2 security dialogs and 4 fund sections, and Apple's dialog has a TXUE section.
FAIL at base: (a), (b), (c), (d) FAIL; (e) PASSES.
Not graded here: the drawn curve, the markers and the hover behaviour need a browser -- a JUDGMENT criterion for the CVO."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

APPLE = "AAPL_US_Equity"
RANGE = re.compile(r"\b(30|90|365)\s?d(?:ays?)?\b")


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    html = render.render_page(c.load_fc1().fixture())
    root = u.parse(html)
    dialogs = [n for n in root.iter() if "data-sec-dialog" in n.attrs]
    sections, frames, bad = [], {}, []
    for d in dialogs:
        key = d.attrs["data-sec-dialog"]
        for s in (n for n in d.iter() if n.tag == "section" and "data-fund" in n.attrs):
            fund = s.attrs["data-fund"]
            sections.append((key, fund))
            got = [n for n in s.iter() if n.tag == "div" and "rf-chart" in (n.attrs.get("class") or "").split()]
            ok = len(got) == 1 and got[0].attrs.get("data-chart-fund") == fund and got[0].attrs.get("data-chart-key") == key
            if ok:
                frames[(key, fund)] = got[0]
            else:
                bad.append((key, fund, [(g.attrs.get("data-chart-fund"), g.attrs.get("data-chart-key")) for g in got]))
    print("dialogs:", len(dialogs), "| fund sections:", len(sections), "| sections with their chart frame:", len(frames))
    for b in bad:
        print("  NO FRAME:", b)
    v.check(bool(sections) and len(frames) == len(sections), "(a) every fund section of a security dialog holds its chart frame")

    switch = {}
    for k, f in frames.items():
        seen = []
        for m in RANGE.finditer(u.text(f)):
            if m.group(1) not in seen:
                seen.append(m.group(1))
        switch[k] = (seen, any("data-chart-status" in n.attrs for n in f.iter()))
    print("frame -> (ranges named in order, has data-chart-status):", switch)
    v.check(bool(frames) and len(frames) == len(sections) and all(s == (["30", "90", "365"], True) for s in switch.values()),
            "(b) every frame holds the status line and a range switch reading 30, 90, 365")

    tx = u.text(frames[(APPLE, "TXUE")]) if (APPLE, "TXUE") in frames else None
    iv = u.text(frames[(APPLE, "IDVZ")]) if (APPLE, "IDVZ") in frames else None
    print("TXUE Apple frame text:", tx)
    print("IDVZ Apple frame text:", iv)
    print("TXUE frame names the window end 2026-10-01:", bool(tx) and "2026-10-01" in tx, "(printed, not graded: the date's form is not prescribed)")
    v.check(tx is not None and iv is not None and "Bought" in tx and "Bought" not in iv and "Sold" not in iv,
            "(c) the fund's trades are in the frame in words; a fund with no trade in the security lists none")

    hist = [d.attrs["data-sec-dialog"] for d in dialogs if "data-history" in d.attrs]
    print("dialogs still carrying data-history:", hist, "| 'History not yet backfilled' in page:", "History not yet backfilled" in html)
    v.check(bool(dialogs) and not hist and "History not yet backfilled" not in html,
            "(d) data-history=none and the not-yet-backfilled words have left the dialog")

    v.check(len(dialogs) == 2 and len(sections) == 4 and (APPLE, "TXUE") in sections,
            "(e) control: 2 security dialogs, 4 fund sections, Apple's dialog has a TXUE section")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
