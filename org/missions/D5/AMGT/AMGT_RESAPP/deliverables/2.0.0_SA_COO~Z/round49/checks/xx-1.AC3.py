"""AMGT_RESAPP round 49, AMGT-xx-1 AC3 -- the POSITIVE CONTROL that the grade keys on the ATTRIBUTE, not the words (CTO round-48 s.4).

On one real served name (ASML_NA_Equity, captured live into a temp cache through sweep.py's own `captured`):
  html  = sweep.render_page_html(fixture_path)       -- the page, rendered from the served fixture, as HTML
  facts = sweep.page_facts_from_html(html)          -- dict of sets keyed FIGURES / CITES / ABSENCES / CASES
(a) WORDING PLANT: the visible text of the FIRST element carrying `data-model-refused` or `data-model-case-reason` is replaced
    with "PLANTED WORDING" -> page_facts_from_html MUST return facts EQUAL to the original (the grade does not move);
(b) DIFFERENCE CONTROL: that same element's attribute VALUE gains the suffix "-PLANTED" -> the facts MUST DIFFER.
usage: python <this>   (from the repo root; reads the deployed function read-only)"""
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"
KEY = "ASML_NA_Equity"
TAG = re.compile(r'<[a-zA-Z][^>]*\b(data-model-refused|data-model-case-reason)="([^"]*)"[^>]*>([^<]*)<')


def main():
    sys.path.insert(0, ".")
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    sweep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sweep)
    missing = [n for n in ("render_page_html", "page_facts_from_html", "captured", "load_capture_lib") if not hasattr(sweep, n)]
    if missing:
        print("sweep.py lacks %s" % ", ".join(missing))
        print("THE GRADE KEYS ON THE ATTRIBUTE, NOT THE WORDS: NO")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        _, fixture = sweep.captured(str(Path(tmp) / "cache"), KEY, sweep.load_capture_lib())
        html = sweep.render_page_html(fixture)
    m = TAG.search(html)
    if not m:
        print("no element carrying data-model-refused / data-model-case-reason in the rendered page of %s" % KEY)
        print("THE GRADE KEYS ON THE ATTRIBUTE, NOT THE WORDS: NO")
        return 1
    base = sweep.page_facts_from_html(html)
    worded = html[:m.start(3)] + "PLANTED WORDING" + html[m.end(3):]
    reattr = html[:m.start(2)] + m.group(2) + "-PLANTED" + html[m.end(2):]
    a = sweep.page_facts_from_html(worded)
    b = sweep.page_facts_from_html(reattr)
    sizes = {k: len(v) for k, v in base.items()}
    print("facts on %s: %s; planted element %s=%r text %r" % (KEY, sizes, m.group(1), m.group(2)[:60], m.group(3)[:60]))
    print("(a) wording plant -> facts %s" % ("EQUAL" if a == base else "MOVED"))
    print("(b) attribute plant -> facts %s" % ("DIFFER" if b != base else "EQUAL"))
    ok = a == base and b != base and sum(sizes.values()) > 0
    print("THE GRADE KEYS ON THE ATTRIBUTE, NOT THE WORDS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
