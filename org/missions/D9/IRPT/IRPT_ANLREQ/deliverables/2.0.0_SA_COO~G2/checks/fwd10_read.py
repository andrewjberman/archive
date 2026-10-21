"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the issuer's page-by-page read of FWD-10's comparison section, the model side.
READ ONLY. Run from the repository root with a python that can import pypdf (not `-I`).

    python fwd10_read.py --pdf <saved Multi-Comp PDF> --codes ST,LT [--series <model_portfolio_timeseries.json>] [--start YYYY-MM-DD --end YYYY-MM-DD] [--dump]

It (1) finds the pages of the PDF that carry the comparison section (the labels `Comparison: common window|cumulative return|periodic total
returns|risk|asset allocation`), (2) prints the closed facts it can read there (the window dates, the names), (3) recomputes, from the live
model return series with this file's own arithmetic (never the code under test), each model's periodic total returns over the common
window and prints which of them appear in the page text. The portfolio side (priced holdings) and the risk table need the priced paths and
the benchmark: they are read by eye against the same pages and by a second script once the PDF exists. Prints counts and numbers only; a
number that is not on the page is reported NOT-ON-PAGE, never silently dropped. ASCII output.
"""
import argparse
import calendar
import datetime
import re
import subprocess
import sys

LABELS = ["Comparison: common window", "Comparison: cumulative return", "Comparison: periodic total returns", "Comparison: risk",
          "Comparison: asset allocation"]
KEYS = ["1m", "3m", "ytd", "1y", "3y", "5y", "10y"]


def day_of(ms):
    return datetime.datetime.fromtimestamp(ms / 1000.0, datetime.timezone.utc).strftime("%Y-%m-%d")


def shift(day, months_back):
    y, m, d = int(day[:4]), int(day[5:7]), int(day[8:10])
    total = y * 12 + (m - 1) - months_back
    y2, m2 = total // 12, total % 12 + 1
    return "%04d-%02d-%02d" % (y2, m2, min(d, calendar.monthrange(y2, m2)[1]))


def as_of(series, day):
    got = [v for d, v in series if d <= day]
    return got[-1] if got else None


def rebase_cut(series, start, end):
    base = as_of(series, start)
    return [(d, v / base * 100.0) for d, v in series if start <= d <= end]


def total_return(path, key):
    end = path[-1][0]
    target = "%d-12-31" % (int(end[:4]) - 1) if key == "ytd" else shift(end, int(key[:-1]) * (12 if key.endswith("y") else 1))
    if path[0][0] > target:
        return None
    return (path[-1][1] / as_of(path, target) - 1.0) * 100.0


def load_series(path):
    if path:
        raw = open(path, "rb").read()
    else:
        out = subprocess.run([".tools/aws", "s3api", "get-object", "--bucket", "opal-data-portal-v2", "--key",
                              "json/benchmarks/model_portfolio_timeseries.json", "/dev/stdout"], capture_output=True)
        raw = out.stdout
    sys.path.insert(0, "infra/aws/lambda/investor-reporting/ycharts/research")
    import model_source
    got = model_source.read_series(lambda key: raw)
    return {code: [(day_of(ms), lv) for ms, lv in rows] for code, rows in got["series"].items()}, got["as_of"]


def pdf_pages(path):
    import pypdf
    reader = pypdf.PdfReader(path)
    return [(p.extract_text() or "") for p in reader.pages]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--codes", required=True)
    ap.add_argument("--series")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--dump", action="store_true")
    a = ap.parse_args()
    pages = pdf_pages(a.pdf)
    squashed = [re.sub(r"\s+", " ", t) for t in pages]
    # the extractor splits letters ("O verview"); match labels on text with spaces removed
    nospace = [re.sub(r"\s+", "", t) for t in pages]
    found = {}
    for lab in LABELS:
        key = re.sub(r"\s+", "", lab)
        found[lab] = [i + 1 for i, t in enumerate(nospace) if key in t]
    print("PAGES %d" % len(pages))
    for lab in LABELS:
        print("LABEL %-38s pages %s" % (lab, found[lab] or "NONE"))
    section_pages = sorted({p for v in found.values() for p in v})
    if a.dump:
        for p in section_pages:
            print("=== page %d" % p)
            print(squashed[p - 1].encode("ascii", "replace").decode()[:3000])
    text = " ".join(squashed[p - 1] for p in section_pages)
    start, end = a.start, a.end
    if not (start and end):
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
        dates = sorted(set(dates))
        print("DATES on the section pages: %s" % dates[:8])
        if len(dates) >= 2 and not (start and end):
            start, end = dates[0], dates[-1]
            print("WINDOW taken from the first and last date on the section pages: %s .. %s (pass --start/--end to override)" % (start, end))
    series, as_of_date = load_series(a.series)
    print("MODEL SERIES as_of %s codes %s" % (as_of_date, sorted(series)))
    flat = re.sub(r"\s+", "", text)
    for code in a.codes.split(","):
        code = code.strip()
        path = rebase_cut(series[code], start, end)
        print("MODEL %s: window %s .. %s, %d points, first level %.4f last level %.4f" % (code, path[0][0], path[-1][0], len(path), path[0][1], path[-1][1]))
        for k in KEYS:
            v = total_return(path, k)
            if v is None:
                print("  %-4s n/a (period longer than the window)" % k)
                continue
            shown = ["%.2f" % v, "%.1f" % v]
            hit = any(s in flat or s.replace("-", "−") in flat for s in shown)
            print("  %-4s %9.4f %%   on page: %s" % (k, v, "YES" if hit else "NOT-ON-PAGE"))
    print("DONE (model side only; the portfolio rows, the risk table and the allocation are read against the pages by eye)")


if __name__ == "__main__":
    main()
