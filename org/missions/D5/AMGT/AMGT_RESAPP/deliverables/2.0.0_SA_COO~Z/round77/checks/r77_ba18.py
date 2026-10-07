"""AMGT_RESAPP round 77 -- AMGT-ba-18 (the export chart line mirrors the page). Issuer checks.

  python r77_ba18.py --crit AC1|AC2 [--where local]

AC1 (build)   lib.research.print.render_pack._thesis_driver_chart_markdown: where the thesis is UNDRAFTED the page
              renders no chart element, so the export prints NO chart line.
AC2 (control) where the thesis IS drafted the export still prints the one absence line, in the same words, and prints
              nothing when the chart is served. PASSES at the base.

Pure: the function is called on fixture bundles; no read, no PDF is built.
"""
import argparse
import sys

OK = []


def clause(label, ok, detail=""):
    OK.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


ABSENT_CHART = {"status": "ABSENT", "reason": "no stored series matches the thesis driver", "probed": 12}
DRIVER = {"series": "commercial aircraft deliveries"}


def bundle(drafting_status, chart=None, read_completed=True):
    return {"drafting_status": drafting_status, "drafting_reason": None, "drafting_read_completed": read_completed,
            "drafted_sections": [], "thesis_driver": dict(DRIVER), "thesis_driver_chart": dict(chart or ABSENT_CHART)}


def ac1():
    from lib.research.print import render_pack

    f = render_pack._thesis_driver_chart_markdown
    for status in ("ABSENT", "INVALID", None):
        out = f(bundle(status))
        clause("C1 an undrafted thesis (drafting_status %r) prints no chart line" % (status,), list(out or []) == [],
               "got %r" % (out,))
    clause("C2 no bundle at all prints no chart line", list(f(None) or []) == [], "got %r" % (f(None),))


def ac2():
    from lib.research.print import render_pack

    f = render_pack._thesis_driver_chart_markdown
    out = f(bundle("SERVED"))
    clause("C1 a drafted thesis with no chart prints the one absence line, naming the driver",
           list(out or []) == ['The chart: ABSENT -- the thesis driver is "commercial aircraft deliveries"'],
           "got %r" % (out,))
    served = f(bundle("SERVED", chart={"status": "SERVED", "points": [1, 2, 3]}))
    clause("C2 a drafted thesis whose chart is served prints no absence line", list(served or []) == [],
           "got %r" % (served,))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    {"AC1": ac1, "AC2": ac2}[a.crit]()
    ok = bool(OK) and all(OK)
    print("R77 BA18 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
