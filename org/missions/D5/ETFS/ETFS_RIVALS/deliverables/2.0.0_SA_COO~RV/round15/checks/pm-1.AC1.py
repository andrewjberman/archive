"""RIV-pm-1 AC1 (PRD v0.18 FWD-22, FWD-23): the month strip marks a first month the window only partly covers.

Interface (prescribed, from the cell):
  - `render._month_chart(mark, end=None, start=None)` and `render._month_words(mark, end=None, start=None)` take the trend
    row's `window_start` as `start` (an ISO string or a date). When `start` is given, its day of month is greater than 1 AND
    the strip's first cell is `start`'s calendar month, the FIRST cell carries the attribute `data-part` and no other cell
    does; `render.MONTH_CSS` holds a rule that shows it (the text `[data-part]`). `_month_words` marks the same month with
    " (part month)". With `start` absent, or on the 1st of a month, no cell carries `data-part`. Everything round 21 built
    stays: 13 cells for a 13-token mark with `data-m="Oct 25"` / `data-m="Oct 26"`, bare month labels otherwise.
  Two spellings are accepted where a worker could build either: the attribute as `data-part=1`, `data-part="1"` or the
  bare `data-part`; the words as "Jul (part month) bought" or "Jul bought (part month)" (the marker anywhere in that
  month's own `; `-separated item, and in no other item).
  The two call sites in render.py pass the row's `window_start`; this check reads the two functions only, not the call sites.

Fixture: marks typed here, no frame. END 2026-10-06. M13 (13 tokens, Oct 25 .. Oct 26); M4 `+ - 0 +` (Jul, Aug, Sep, Oct).
  - (a) M13 with start 2025-10-06: 13 cells labelled "Oct 25", Nov .. Sep, "Oct 26" with the classes of all 13 tokens; the
    first carries data-part, the other 12 do not;
  - (b) M4 with start 2026-07-08 (as a string and as a `datetime.date`): 4 cells Jul .. Oct, Jul carries data-part alone;
  - (c) M4 with start 2026-07-01 (the 1st): no cell carries data-part; a 2-token mark (Sep, Oct) with start 2026-07-08 (the
    first cell is not the start's month): none; and with no start: none;
  - (d) `_month_words` on the (b) case marks Jul, and only Jul, "(part month)"; on the (c) case (start on the 1st) the
    words do not hold "(part month)";
  - (e) `render.MONTH_CSS` holds `[data-part]`;
  - (f) pl-1.AC1, ml-1.AC1 and pd-2.AC1 still end `PASS 0 failures` (each run as its own process from the worktree root);
  - (g) control: called with (mark, end) only, the round-21 strip holds (13 cells, "Oct 25" .. "Oct 26", no data-part), a
    2-token mark draws Sep and Oct, and the words of M4 name Jul first with no "(part month)".
A function that does not accept `start` is read with inspect.signature and counts as a failed arm, never a traceback.
FAIL at base b1a4837abe: (a), (b), (c), (d), (e) FAIL (neither function takes `start`; no `[data-part]` rule); (f), (g) PASS."""
import datetime as dt
import inspect
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
END = "2026-10-06"
M13 = "+ - 0 . + - 0 . + - 0 . +"
M4 = "+ - 0 +"
CLS = {"+": "u", "-": "d", "0": "f", ".": "n"}
LABELS13 = ["Oct 25"] + MON[10:] + MON[:9] + ["Oct 26"]
LABELS4 = ["Jul", "Aug", "Sep", "Oct"]
PART = "(part month)"
EARLIER = ("pl-1.AC1", "ml-1.AC1", "pd-2.AC1")
NO_START = "the function takes no `start` parameter"


def cells(html: str):
    """[(class letter, label, carries data-part)] per cell; the label is the data-m value, quoted or not."""
    out = []
    for tag in re.findall(r"<i\b[^>]*>", html or ""):
        k = re.search(r'\bclass="?([a-z])"?', tag)
        m = re.search(r'\bdata-m=(?:"([^"]*)"|([A-Za-z]{3})\b)', tag)
        part = re.search(r"""\sdata-part(?:=(?:"1"|'1'|1))?(?=[\s>/])""", tag)
        out.append((k.group(1) if k else None, (m.group(1) or m.group(2)) if m else None, bool(part)))
    return out


def takes_start(fn) -> bool:
    try:
        ps = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False
    return "start" in ps or any(p.kind is inspect.Parameter.VAR_KEYWORD for p in ps.values())


def call(fn, mark, end, **kw):
    """(value, error words). A `start` the function cannot take is a failed arm, said in words."""
    if fn is None:
        return None, "the function is not in render"
    if "start" in kw and not takes_start(fn):
        return None, NO_START
    try:
        return fn(mark, end, **kw), None
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        return None, f"{type(e).__name__}: {e}"


def parts(got) -> list:
    return [i for i, x in enumerate(got) if x[2]]


def part_items(words) -> list:
    """Indexes of the `; `-separated items of the hover words that hold the part-month marker."""
    return [i for i, item in enumerate(str(words or "").split("; ")) if PART in item]


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    chart, words = getattr(render, "_month_chart", None), getattr(render, "_month_words", None)
    print("_month_chart takes start:", chart is not None and takes_start(chart),
          "| _month_words takes start:", words is not None and takes_start(words))

    h13, e13 = call(chart, M13, END, start="2025-10-06")
    got13 = cells(h13 or "")
    print("13 tokens, start 2025-10-06 ->", e13 or got13)
    v.check([(k, lab) for k, lab, _p in got13] == [(CLS[t], lab) for t, lab in zip(M13.split(), LABELS13)] and parts(got13) == [0],
            "(a) a 13-token mark starting 2025-10-06 draws 13 cells 'Oct 25' .. 'Oct 26'; the first carries data-part, the other 12 do not")

    h4, e4 = call(chart, M4, END, start="2026-07-08")
    h4d, e4d = call(chart, M4, END, start=dt.date(2026, 7, 8))
    got4, got4d = cells(h4 or ""), cells(h4d or "")
    print("4 tokens, start '2026-07-08' ->", e4 or got4)
    print("4 tokens, start date(2026, 7, 8) ->", e4d or got4d)
    want4 = [(CLS[t], lab, i == 0) for i, (t, lab) in enumerate(zip(M4.split(), LABELS4))]
    v.check(got4 == want4 and got4d == want4,
            "(b) a 4-token mark starting 2026-07-08 (string or date) draws Jul .. Oct and Jul alone carries data-part")

    h1, e1 = call(chart, M4, END, start="2026-07-01")
    h2s, e2s = call(chart, "- +", END, start="2026-07-08")
    h0, e0 = call(chart, M4, END)
    got1, got2s, got0 = cells(h1 or ""), cells(h2s or ""), cells(h0 or "")
    print("4 tokens, start 2026-07-01 ->", e1 or got1)
    print("2 tokens (Sep, Oct), start 2026-07-08 ->", e2s or got2s)
    print("4 tokens, no start ->", e0 or got0)
    v.check(len(got1) == 4 and parts(got1) == [] and len(got2s) == 2 and parts(got2s) == [] and len(got0) == 4 and parts(got0) == [],
            "(c) no cell carries data-part when the start is the 1st, when the first cell is not the start's month, or with no start")

    wb, ewb = call(words, M4, END, start="2026-07-08")
    wc, ewc = call(words, M4, END, start="2026-07-01")
    print("words, start 2026-07-08:", ewb or repr(wb))
    print("words, start 2026-07-01:", ewc or repr(wc))
    v.check(isinstance(wb, str) and wb.startswith("Jul ") and part_items(wb) == [0]
            and isinstance(wc, str) and wc.startswith("Jul ") and PART not in wc,
            "(d) the hover words mark Jul, and only Jul, '(part month)' for a start of 2026-07-08, and no month for a start on the 1st")

    css = getattr(render, "MONTH_CSS", "") or ""
    print("MONTH_CSS chars:", len(css), "| holds [data-part]:", "[data-part]" in css)
    v.check("[data-part]" in css, "(e) MONTH_CSS holds a [data-part] rule")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1700)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(f) pl-1.AC1, ml-1.AC1 and pd-2.AC1 still end PASS 0 failures")

    c13, ec13 = call(chart, M13, END)
    c2, _ = call(chart, "- +", END)
    w0, ew0 = call(words, M4, END)
    base13 = cells(c13 or "")
    print("control, 13 tokens (mark, end) ->", ec13 or [(k, lab) for k, lab, _p in base13], "| data-part cells:", parts(base13))
    print("control, 2 tokens ->", cells(c2 or ""), "| words of the 4-token mark:", ew0 or repr(w0))
    v.check(base13 == [(CLS[t], lab, False) for t, lab in zip(M13.split(), LABELS13)]
            and cells(c2 or "") == [("d", "Sep", False), ("u", "Oct", False)]
            and isinstance(w0, str) and w0.startswith("Jul ") and w0.count("; ") == 3 and PART not in w0,
            "(g) control: with (mark, end) only the round-21 strip holds (13 cells, 'Oct 25' .. 'Oct 26'), a 2-token mark draws "
            "Sep and Oct, and the words name Jul first")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
