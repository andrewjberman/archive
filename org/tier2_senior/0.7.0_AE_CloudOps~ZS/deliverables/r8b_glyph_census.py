"""R8b evidence census (read-only). For every retained pull log, list each VERIFY block's username glyph-run count, expected range,
password-dot count, OCR SIMILARITY (never the OCR text) and the VERIFY verdict. Prints a denominator. No screenshot is opened."""
from __future__ import annotations

import glob
import os
import re
from collections import Counter

LOGDIR = r"C:\Users\Opal Bloomberg\opal_bbg_logs"
files = sorted(glob.glob(os.path.join(LOGDIR, "*.log")))
files.append(r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace\org\tier2_senior\0.7.0_AE_CloudOps~ZS\deliverables\z6_r3_exercise.log")
rx_runs = re.compile(r"username glyph-runs: (\d+) \(expect (\d+)\.\.(\d+) for len (\d+)")
rx_dots = re.compile(r"password dots: (\d+) \(expect (\d+)\)")
rx_sim = re.compile(r"username OCR \(observation only\): .* similarity (\d+)%\s*$")
rx_ver = re.compile(r"VERIFY: (PASS|FAIL)(.*)$")
rx_loc = re.compile(r"locator: (username field FOUND|MISS)")
rows = []
for f in files:
    try:
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        continue
    cur = {}
    last_dots = "-"
    for ln in lines:
        m = rx_dots.search(ln)
        if m:
            last_dots = "%s/%s" % (m.group(1), m.group(2))
        m = rx_runs.search(ln)
        if m:
            cur = {"log": os.path.basename(f), "runs": int(m.group(1)), "lo": int(m.group(2)), "hi": int(m.group(3)), "len": int(m.group(4)), "dots": last_dots}
            continue
        if not cur:
            continue
        m = rx_sim.search(ln)
        if m:
            cur["sim"] = int(m.group(1))
        m = rx_ver.search(ln)
        if m:
            cur["verdict"] = m.group(1)
            cur["why"] = m.group(2).strip()[:60]
            rows.append(cur)
            cur = {}
print("logs scanned: %d ; VERIFY blocks with a glyph-run line: %d" % (len(files), len(rows)))
print("%-30s %5s %-7s %-5s %4s %-5s %s" % ("log", "runs", "range", "dots", "sim", "res", "why"))
for r in rows:
    print("%-30s %5d %d..%d  %-5s %4s %-5s %s" % (r["log"][:30], r["runs"], r["lo"], r["hi"], r.get("dots", "-"), r.get("sim", "-"), r.get("verdict", "-"), r.get("why", "")))
c = Counter((r["runs"], r.get("verdict")) for r in rows)
print("distribution (runs, verdict) -> n:", dict(sorted(c.items())))
