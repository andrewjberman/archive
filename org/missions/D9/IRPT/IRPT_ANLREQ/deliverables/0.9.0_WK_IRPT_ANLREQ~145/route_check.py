"""AR339-y-AC2 -- route check for the irpt-status release zip (TO-AR-y-339, worker 0.9.0_WK_IRPT_ANLREQ~145).

Extracts the staged zip and the downloaded live zip into scratch directories outside the repository, then prints
ROUTE-OK only when the staged package carries the merged commentary-pdf route, the signer family, and an unchanged
analysis-request-pdf route against the live package. Otherwise ROUTE-BAD <why> and exit 1.
"""
import json
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REC_PATH = os.path.join(HERE, "r41", "IRPT_STATUS_R31_BUILD.json")
SCRATCH = "C:/dev/irpt-release-r31/scratch"
ROUTE = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf"
OP = "analysis-request-commentary-pdf"
PDF_ROUTE = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/pdf"
FAMILY = "YCHARTS_OPAL_REPORT"


def bad(why):
    print("ROUTE-BAD " + why)
    sys.exit(1)


def extract(zpath, dest):
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(dest)
    return dest


def read(root, name):
    with open(os.path.join(root, name), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    rec = json.load(open(REC_PATH, encoding="utf-8"))
    zpath = rec.get("artifact", {}).get("path")
    if not zpath or not os.path.isfile(zpath):
        bad("no staged zip to extract (artifact.path=%r)" % zpath)
    live = rec["live_read"]["download_path"]
    if not os.path.isfile(live):
        bad("downloaded live zip missing: " + live)
    staged_root = extract(zpath, os.path.join(SCRATCH, "route_staged"))
    live_root = extract(live, os.path.join(SCRATCH, "route_live"))

    route_pat = re.compile(re.escape('"%s": "%s"' % (ROUTE, OP)))
    entry = read(staged_root, "entry.py")
    status = read(staged_root, "status_installed.py")
    pdf_link = read(staged_root, "pdf_link.py")
    live_pdf_link = read(live_root, "pdf_link.py")

    # 1. the route maps to the operation in entry.py and in status_installed.py
    if not route_pat.search(entry):
        bad("entry.py of the staged package does not declare %s -> %s" % (ROUTE, OP))
    if not route_pat.search(status):
        bad("status_installed.py of the staged package does not carry the route key %s" % ROUTE)

    # 2. the signer FAMILIES: present in the staged pdf_link.py, absent from the live one
    fam_line = re.compile(r"^FAMILIES\s*=.*$", re.M)
    m = fam_line.search(pdf_link)
    if not m or FAMILY not in m.group(0):
        bad("staged pdf_link.py FAMILIES does not contain " + FAMILY)
    lm = fam_line.search(live_pdf_link)
    if not lm or FAMILY in lm.group(0):
        bad("live pdf_link.py FAMILIES already contains " + FAMILY + " (the grant is not new)")

    # 3. the analysis-request-pdf route is unchanged against the live package (entry.py and status_installed.py)
    for name in ("entry.py", "status_installed.py"):
        new_lines = sorted(x.strip() for x in read(staged_root, name).splitlines() if PDF_ROUTE in x)
        old_lines = sorted(x.strip() for x in read(live_root, name).splitlines() if PDF_ROUTE in x)
        if new_lines != old_lines:
            bad("the analysis-request-pdf route differs in %s (staged %d lines, live %d)"
                % (name, len(new_lines), len(old_lines)))

    # 4. the count of route tables carrying the commentary route across the staged package
    n = 0
    for name in os.listdir(staged_root):
        if name.endswith(".py"):
            n += len(route_pat.findall(read(staged_root, name)))
    if n == 0:
        bad("no table carries the commentary route")

    print("ROUTE-OK commentary-pdf declared in %d tables, signer family present" % n)


if __name__ == "__main__":
    main()
