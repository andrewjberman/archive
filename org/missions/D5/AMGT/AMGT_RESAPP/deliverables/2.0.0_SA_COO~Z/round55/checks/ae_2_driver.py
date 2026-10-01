"""AMGT_RESAPP round 55, AMGT-ae-2 -- FWD-18 read ON THE PAGE: ASML's thesis-driver chart (CTO round-54 analysis item 2).
Captures ASML_NA_Equity and AMD_US_Equity from the DEPLOYED function with FWD-30's own capture (sweep.py `captured`), renders the
SecurityAnalysis page with its own `render_page_html` (the portal's ThesisDriverChart, react-dom/server), and reads the chart's
data attributes:
  ASML  data-driver-chart="SERVED", data-driver-chart-source="filing", data-driver-chart-points = the served chart's point count (>= 3)
  AMD   CONTROL -- a name whose chart is not served from a filing: no SERVED filing chart on its page.
usage: python <this> --cache <dir outside the repo>   (from the repo root; read-only Invokes)"""
import argparse
import importlib.util
import re
import sys

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"


def chart(m, cache, key):
    _d, fx = m.captured(cache, key, m.load_capture_lib())
    html = m.render_page_html(fx)
    status = re.findall(r'data-driver-chart="([A-Z]+)"', html)
    source = re.findall(r'data-driver-chart-source="([^"]*)"', html)
    points = [int(x) for x in re.findall(r'data-driver-chart-points="(\d+)"', html)]
    return status, source, points


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    s, src, pts = chart(m, a.cache, "ASML_NA_Equity")
    print("ASML page: chart %s source %s points %s" % (s, src, pts))
    cs, csrc, cpts = chart(m, a.cache, "AMD_US_Equity")
    print("AMD page (control): chart %s source %s points %s" % (cs, csrc, cpts))
    ok = s == ["SERVED"] and src == ["filing"] and pts and pts[0] >= 3 and not ("SERVED" in cs and "filing" in csrc)
    print("FWD-18: ASML'S DRIVER CHART IS SERVED FROM ITS FILING ON THE PAGE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
