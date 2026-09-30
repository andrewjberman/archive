"""AMGT_RESAPP round 53, AMGT-ac-1 AC1 -- FWD-30's grader reads the DISPLAYED figure, never a hover tooltip's text (CTO round-52 ruling 2).
On a REAL rendered page (ASML_NA_Equity, captured from the DEPLOYED function by the grader's own capture, rendered by the grader's own
`render_page_html` against the portal tree), the grader's `page_facts_from_html` reads the header figures' VALUES three times:
  (0) as rendered;
  (a) PLANT: every hover tooltip's full-precision text and its `data-full-value` replaced by 999.999 -- the read must be IDENTICAL to (0);
  (b) CONTROL: the visible PX_LAST figure (the `tabular-nums` span inside `<li data-card-figure-mnemonic="PX_LAST">`, the element
      the grader reads HEADER values from) replaced by 999.999 -- the read of PX_LAST must CHANGE.
At the cut (the grader reading the cell's whole text) the plant changes the read, so (a) fails.
usage: python <this> --cache <dir outside the repo>   (from the repo root; read-only Invokes)"""
import argparse
import importlib.util
import json
import re
import sys

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"
KEY = "ASML_NA_Equity"


def header_values(m, html):
    vals = (m.page_facts_from_html(html).get("VALUES") or {})
    return {k: v for k, v in vals.items() if isinstance(k, tuple) and k[0] == "HEADER"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    _d, fx = m.captured(a.cache, KEY, m.load_capture_lib())
    html = m.render_page_html(fx)
    base = header_values(m, html)
    planted = re.sub(r'data-full-value="[^"]*"', 'data-full-value="999.999"', html)
    planted = re.sub(r'(<div data-data-tooltip="[^"]*">)[^<|]*', r"\g<1>999.999 ", planted)
    # the grader reads HEADER values from `<li data-card-figure-mnemonic=...>`; its visible figure is the `tabular-nums` span
    control = re.sub(r'(data-card-figure-mnemonic="PX_LAST"[^>]*>(?:(?!</li>).)*?<span class="tabular-nums[^"]*">)([^<]*)',
                     r"\g<1>EUR 999.999", html, count=1, flags=re.S)
    plant_read, control_read = header_values(m, planted), header_values(m, control)
    px = ("HEADER", "PX_LAST")
    print("header value facts read: %d; PX_LAST as rendered: %s" % (len(base), json.dumps(base.get(px))[:120]))
    same = json.dumps(sorted(map(str, plant_read.items()))) == json.dumps(sorted(map(str, base.items())))
    print("(a) tooltip plant: read unchanged: %s" % same)
    moved = json.dumps(control_read.get(px)) != json.dumps(base.get(px))
    print("(b) visible-figure control: PX_LAST read changed: %s (%s)" % (moved, json.dumps(control_read.get(px))[:120]))
    ok = bool(base) and same and moved
    print("THE GRADER READS THE DISPLAYED FIGURE, NOT THE TOOLTIP: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
