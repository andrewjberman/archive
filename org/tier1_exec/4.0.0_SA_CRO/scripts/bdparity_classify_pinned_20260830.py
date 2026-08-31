"""ADVI_BDPARITY BP1-4 -- apply the CRO word (EXACT 0.5 bp, TIGHT 10 bp) to the 20-cell table AS PINNED
@cd7966658a (parsed from the committed markdown via git show, never re-run), and print the exact sub-window
identity: Dlog = ln(1+ours) - ln(1+BD) is additive over concatenated windows on BOTH sides, so
Dlog(YTD) - Dlog(QTD) = Dlog(Jan-1..Jun-30) exactly, hole or no hole (the hole sits inside QTD on both sides).
4.0.0_SA_CRO, 2026-08-30. Target-specific: the pinned commit + markdown path + column order.
"""
import argparse
import math
import re
import subprocess

MD = ("org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/"
      "ADVI_BDPARITY_BP1-2_PROBE_TABLE_20260830.md")
DASH = "\u2014"  # the table renders an absent value as an em dash


def classify(delta, exact_bp, n_bp):
    a = abs(delta) * 1e4
    if a <= exact_bp:
        return "EXACT"
    if a <= n_bp:
        return "TIGHT"
    return "LARGE"


def parse(pin):
    txt = subprocess.run(["git", "show", "%s:%s" % (pin, MD)], capture_output=True,
                         text=True, encoding="utf-8", check=True).stdout
    rows = []
    for line in txt.splitlines():
        if not re.match(r"\|\s*\d{10}\s*\|\s*(QTD|YTD|1Y|SI)\s*\|", line):
            continue
        cells = [c.strip().strip("*") for c in line.split("|")[1:-1]]
        acct, per, req, _ret, _match, outcome, ours, bd, delta = cells[:9]
        rows.append(dict(acct=acct, per=per, req=req, outcome=outcome,
                         ours=None if ours == DASH else float(ours), bd=float(bd),
                         delta=None if delta == DASH else float(delta)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", default="cd7966658a")
    ap.add_argument("--exact-bp", type=float, default=0.5)
    ap.add_argument("--n-bp", type=float, default=10.0)
    a = ap.parse_args()
    rows = parse(a.pin)
    print("parsed %d cells from the pinned table @%s" % (len(rows), a.pin))
    print("\n=== CLASS per COMPUTED cell (EXACT<=%.1fbp, TIGHT<=%.0fbp, else LARGE), delta = ours - BD, SIGNED ==="
          % (a.exact_bp, a.n_bp))
    counts = {"EXACT": 0, "TIGHT": 0, "LARGE": 0}
    classified = 0
    byacct = {}
    for r in rows:
        if r["outcome"] == "COMPUTED" and r["delta"] is not None:
            c = classify(r["delta"], a.exact_bp, a.n_bp)
            counts[c] += 1
            classified += 1
            dl = math.log1p(r["ours"]) - math.log1p(r["bd"])
            byacct.setdefault(r["acct"], {})[r["per"]] = dl
            print("  %s %-3s %-16s delta=%+9.1f bp  Dlog=%+9.1f bp  -> %s"
                  % (r["acct"], r["per"], r["req"], r["delta"] * 1e4, dl * 1e4, c))
        else:
            print("  %s %-3s %-16s %s (an OUTCOME; not classified)" % (r["acct"], r["per"], r["req"], r["outcome"]))
    computed = sum(1 for r in rows if r["outcome"] == "COMPUTED")
    print("DENOMINATOR: classified %d of COMPUTED %d of %d cells; classes %s" % (classified, computed, len(rows), counts))
    print("\n=== SUB-WINDOW ISOLATION (exact in log space; hole-free windows fall out of the table itself) ===")
    for acct, d in byacct.items():
        if "YTD" in d and "QTD" in d:
            if abs(d["YTD"] - d["QTD"]) > 1e-12:
                sub = d["YTD"] - d["QTD"]
                print("  %s  Dlog[Jan-1..Jun-30] = Dlog(YTD)-Dlog(QTD) = %+8.1f bp -> %s"
                      % (acct, sub * 1e4, classify(math.expm1(sub), a.exact_bp, a.n_bp)))
            else:
                print("  %s  YTD == QTD window (lived period shorter than the calendar window): nothing to isolate" % acct)
        if "1Y" in d and "YTD" in d and abs(d["1Y"] - d["YTD"]) > 1e-12:
            sub = d["1Y"] - d["YTD"]
            print("  %s  Dlog[1Y-open..12-31]  = Dlog(1Y)-Dlog(YTD)  = %+8.1f bp -> %s   (carries the 1Y open-boundary term pre-BP1-6)"
                  % (acct, sub * 1e4, classify(math.expm1(sub), a.exact_bp, a.n_bp)))


if __name__ == "__main__":
    main()
