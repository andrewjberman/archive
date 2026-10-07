"""RIV-ml-1 AC1 (PRD v0.18 FWD-23; row ETFS_RIVALS-Z-S58): the month-by-month buying strip labels each cell with the month it
is, counted back from the trend row's window end, and shows the window's last 12 months.

Interface (prescribed, from the cell): `render._month_chart(mark, end=None)` and `render._month_words(mark, end=None)`. `mark`
is the trend row's `trend_mark` (month tokens, oldest first, the last token being the month of the row's window end); `end`
is that row's `window_end` (ISO string or date). With `end`: the LAST token is `end`'s month, each earlier token one month
before; at most the last 12 tokens are drawn; every cell carries its month as `data-m=<Jan..Dec>`. With `end` None (a row
that carries none): the tokens are labelled from January, as before. `render.MONTH_CSS` prints the label from the cell
(`attr(data-m)`), no longer from the cell's position.
  - (a) a 13-token mark with end 2026-10-06 draws 12 cells labelled Nov, Dec, Jan .. Oct, with the classes of tokens 2..13
    (the newest month is kept, the oldest dropped);
  - (b) a 2-token mark "- +" with end 2026-10-06 draws 2 cells labelled Sep (sold) and Oct (bought);
  - (c) a 10-token mark with no end draws 10 cells labelled Jan .. Oct;
  - (d) MONTH_CSS holds `attr(data-m)` and no rule that names a month by cell position;
  - (e) `_month_words("- . +", "2026-10-06")` == "Aug sold; Oct bought", and on the 13-token mark it names 12 months at most
    and ends at Oct;
  - (f) pd-2.AC1, pd-2.AC2 and md-1.AC2 still end `PASS 0 failures` (each run as its own process from the worktree root);
  - (g) control: with no end, `_month_words("- . +")` == "Jan sold; Mar bought" and `_month_chart("- . +")` draws 3 cells.
FAIL at base 5be2c73b12: (a), (b), (c), (d), (e) FAIL (no `end` parameter, no data-m, labels by position); (f), (g) PASS."""
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
CLS = {"+": "u", "-": "d", "0": "f", ".": "n"}
EARLIER = ("pd-2.AC1", "pd-2.AC2", "md-1.AC2")


def cells(html: str):
    """[(class letter, data-m | None)] for each cell of the first month strip in `html`."""
    out = []
    for tag in re.findall(r"<i\b[^>]*>", html or ""):
        k = re.search(r'\bclass="?([a-z])"?', tag)
        m = re.search(r'\bdata-m="?([A-Za-z]{3})"?', tag)
        out.append((k.group(1) if k else None, m.group(1) if m else None))
    return out


def call(fn, *a):
    try:
        return fn(*a), None
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        return None, f"{type(e).__name__}: {e}"


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    h13, e13 = call(render._month_chart, M13, END)
    got13 = cells(h13 or "")
    toks = M13.split()
    want13 = [(CLS[t], m) for t, m in zip(toks, MON[9:] + MON[:9] + MON[9:10])]
    print("13 tokens, end", END, "->", e13 or got13)
    v.check(got13 == want13, "(a) a 13-token mark draws its last 12 months labelled Nov, Dec, Jan .. Oct with the classes of tokens 2..13")

    h2, e2 = call(render._month_chart, "- +", END)
    print("2 tokens, end", END, "->", e2 or cells(h2 or ""))
    v.check(cells(h2 or "") == [("d", "Sep"), ("u", "Oct")], "(b) a 2-token mark draws Sep (sold) and Oct (bought)")

    m10 = "+ - 0 + - 0 + - 0 +"
    h10, e10 = call(render._month_chart, m10)
    print("10 tokens, no end ->", e10 or cells(h10 or ""))
    v.check(cells(h10 or "") == [(CLS[t], m) for t, m in zip(m10.split(), MON[:10])],
            "(c) a 10-token mark with no end draws Jan .. Oct, each cell carrying its label")

    css = getattr(render, "MONTH_CSS", "") or ""
    positional = re.findall(r'nth-child\(\d+\)::before\{content:"[A-Za-z]{3}"\}', css)
    print("MONTH_CSS chars:", len(css), "| attr(data-m):", "attr(data-m)" in css, "| positional month rules:", len(positional))
    v.check("attr(data-m)" in css and not positional, "(d) the stylesheet prints the label from the cell, not from its position")

    w3, ew3 = call(render._month_words, "- . +", END)
    w13, ew13 = call(render._month_words, M13, END)
    print("_month_words('- . +', end):", ew3 or repr(w3), "| 13-token words:", ew13 or repr(w13))
    named = re.findall(r"\b(" + "|".join(MON) + r")\b", w13 or "")
    v.check(w3 == "Aug sold; Oct bought" and 0 < len(named) <= 13 and named[-1] == "Oct" and len(set(named)) == len(named) - 1,
            "(e) the hover words name the same months: 'Aug sold; Oct bought'; a 13-token mark names 12 at most and ends at Oct")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(f) pd-2.AC1, pd-2.AC2 and md-1.AC2 still end PASS 0 failures")

    wl, _ = call(render._month_words, "- . +")
    hl, _ = call(render._month_chart, "- . +")
    print("legacy words:", repr(wl), "| legacy cells:", [k for k, _ in cells(hl or "")])
    v.check(wl == "Jan sold; Mar bought" and [k for k, _ in cells(hl or "")] == ["d", "n", "u"],
            "(g) control: with no end the words read 'Jan sold; Mar bought' and the strip draws 3 cells")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
