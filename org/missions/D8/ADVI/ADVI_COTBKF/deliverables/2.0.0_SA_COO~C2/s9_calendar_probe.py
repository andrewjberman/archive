"""S9 diagnostic (2.0.0_SA_COO~C2): re-run commonwealth_account_links with NYSE holidays 2014-2023
computed from the published rules, added to lib/trading_calendar's fallback set, then compare to the
laptop's committed account_links_r4.csv. Scratch only; changes no repo file."""
import datetime as dt
import runpy
import sys

ROOT = sys.argv[1]
OUT = sys.argv[2]
sys.path.insert(0, ROOT + "/lib")
import trading_calendar as tc  # noqa: E402


def easter(y):
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    wk = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * wk) // 451
    mo, da = divmod(h + wk - 7 * m + 114, 31)
    return dt.date(y, mo, da + 1)


def nth_weekday(y, mo, wd, n):
    d = dt.date(y, mo, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_weekday(y, mo, wd):
    d = dt.date(y, mo + 1, 1) - dt.timedelta(days=1) if mo < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def observed(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def nyse(y):
    s = set()
    nyd = dt.date(y, 1, 1)
    if nyd.weekday() == 6:
        s.add(nyd + dt.timedelta(days=1))
    elif nyd.weekday() != 5:  # NYSE does not observe a Saturday New Year on the prior Friday
        s.add(nyd)
    s.add(nth_weekday(y, 1, 0, 3))   # MLK
    s.add(nth_weekday(y, 2, 0, 3))   # Washington
    s.add(easter(y) - dt.timedelta(days=2))  # Good Friday
    s.add(last_weekday(y, 5, 0))     # Memorial
    if y >= 2022:
        s.add(observed(dt.date(y, 6, 19)))
    s.add(observed(dt.date(y, 7, 4)))
    s.add(nth_weekday(y, 9, 0, 1))   # Labor
    s.add(nth_weekday(y, 11, 3, 4))  # Thanksgiving
    s.add(observed(dt.date(y, 12, 25)))
    if y == 2018:
        s.add(dt.date(2018, 12, 5))  # national day of mourning
    return s


extra = {d.isoformat() for y in range(2010, 2024) for d in nyse(y)}
tc.NYSE_HOLIDAYS_FALLBACK = frozenset(set(tc.NYSE_HOLIDAYS_FALLBACK) | extra)
tc._NYSE_HOLIDAYS_FALLBACK = tc.NYSE_HOLIDAYS_FALLBACK
print("probe: fallback extended by %d pre-2024 holidays" % len(extra))
sys.argv = ["commonwealth_account_links.py", "--out", OUT]
runpy.run_path(ROOT + "/data/assets/scripts/silver/commonwealth_account_links.py", run_name="__main__")
