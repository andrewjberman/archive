"""AMGT_RESAPP round 50, AMGT-yy-1 AC1 / AC2 -- the CVO's two VALUE plants are the falsifiers (CTO round-49 ruling 1).

On AMD_US_Equity, captured live through sweep.py's own `captured`, rendered with `render_page_html`:
  unplanted:    compare_facts(page_facts_from_html(html), rich_facts(rich, fixture)) -> verdict OK
  --side page:  the FIRST `data-model-cell` in the `data-model-row="IS_EPS"` row gets the text 999.99 -> NOT_OK naming FIGURES
  --side export: the first figure value on the export's IS_EPS line gets 999.99 -> NOT_OK naming FIGURES
usage: python <this> --side page|export   (from the repo root; reads the deployed function read-only)"""
import argparse
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"
KEY = "AMD_US_Equity"
PLANT = "999.99"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--side", choices=("page", "export"), required=True)
    a = ap.parse_args()
    sys.path.insert(0, ".")
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    with tempfile.TemporaryDirectory() as tmp:
        return graded(a, sw, *sw.captured(str(Path(tmp) / "cache"), KEY, sw.load_capture_lib()))


def graded(a, sw, d, fx):
    # every read of the fixture happens while the capture's temp directory still exists (rich_facts reads it lazily)
    html = sw.render_page_html(fx)
    rich = open(next(iter(sorted((Path(d) / "served").glob("*.rich.md")))), encoding="utf-8").read()
    base = sw.compare_facts(sw.page_facts_from_html(html), sw.rich_facts(rich, fx)) or {}
    if a.side == "page":
        row = re.search(r'<tr[^>]*data-model-row="IS_EPS".*?</tr>', html, re.S)
        cell = re.search(r'(<td[^>]*data-model-cell="[^"]*"[^>]*>)([^<]*)(<)', row.group(0)) if row else None
        if not cell:
            print("no IS_EPS data-model-cell on the page of %s" % KEY)
            print("THE %s VALUE PLANT FAILS THE GRADE: NO" % a.side.upper())
            return 1
        start = row.start() + cell.start(2)
        was = cell.group(2)
        html2 = html[:start] + PLANT + html[start + len(was):]
        got = sw.compare_facts(sw.page_facts_from_html(html2), sw.rich_facts(rich, fx)) or {}
    else:
        line = next((ln for ln in rich.splitlines() if "| IS_EPS |" in ln), None)
        num = re.search(r"^\s*(-?[0-9][0-9,]*\.?[0-9]*)\s", line.split("|", 3)[3]) if line else None
        if not num:
            print("no IS_EPS figure value on the export line of %s" % KEY)
            print("THE %s VALUE PLANT FAILS THE GRADE: NO" % a.side.upper())
            return 1
        was = num.group(1)
        head, tail = line.split("|", 3)[:3], line.split("|", 3)[3]
        new_line = "|".join(head) + "|" + tail.replace(was, PLANT, 1)
        got = sw.compare_facts(sw.page_facts_from_html(html), sw.rich_facts(rich.replace(line, new_line, 1), fx)) or {}
    print("%s: unplanted verdict %r reason %r" % (KEY, base.get("verdict"), base.get("reason")))
    print("%s plant %r -> %s: verdict %r reason %r" % (a.side, was, PLANT, got.get("verdict"), got.get("reason")))
    ok = base.get("verdict") == "OK" and got.get("verdict") == "NOT_OK" and "FIGURES" in str(got.get("reason") or "")
    print("THE %s VALUE PLANT FAILS THE GRADE: %s" % (a.side.upper(), "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
