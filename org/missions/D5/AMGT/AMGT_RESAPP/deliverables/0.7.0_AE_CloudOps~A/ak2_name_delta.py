"""AMGT-ak-2 -- the CTO half's condition 2: the previously-unnamed keys' post-act
`display_name` and `name_source` printed BESIDE their pre-act values.

AC1's C1/C3 assert a population property (0 unnamed of 94). They never show the per-key
move, and the round-61 `pre` file holds only a sha, so the pre-act labels had to be
captured separately before the apply (ak2_name_census.py --label pre). This joins the two
censuses on the keys that were unnamed-or-ticker-labelled at the base.

  --pre <json> --post <json>
"""
from __future__ import annotations

import argparse
import json

CONTROL = "RMS_FP_Equity"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre", required=True)
    ap.add_argument("--post", required=True)
    a = ap.parse_args()
    pre = json.load(open(a.pre, encoding="utf-8"))
    post = json.load(open(a.post, encoding="utf-8"))

    print("CodeSha256 %s -> %s" % (pre["CodeSha256"], post["CodeSha256"]))
    print("LastModified %s -> %s" % (pre["LastModified"], post["LastModified"]))
    rc = 0

    for kind in ("trending/price", "breakout/price"):
        was = [k for k, _n, _w in pre["rankings"][kind]["unnamed"]]
        print()
        print("=== %s -- the %d keys the base left unnamed or ticker-labelled ==="
              % (kind, len(was)))
        print("    %-18s %-34s %-34s %s" % ("key", "PRE display_name", "POST display_name", "POST name_source"))
        still = []
        for k in sorted(was):
            p = pre["rankings"][kind]["rows"].get(k) or {}
            q = post["rankings"][kind]["rows"].get(k) or {}
            print("    %-18s %-34r %-34r %r" % (k, p.get("display_name"), q.get("display_name"), q.get("name_source")))
            if not q.get("name") or str(q.get("name", "")).strip().upper() == str(q.get("ticker") or "").strip().split(" ")[0].upper():
                still.append(k)
        print("    MOVED: %d of %d; STILL UNNAMED-OR-TICKER: %d %s"
              % (len(was) - len(still), len(was), len(still), still))
        if still:
            rc = 1

    print()
    was_c = [k for k, _d in pre["chatter"]["ticker_named"]]
    print("=== chatter -- the %d rows the base labelled by ticker ===" % len(was_c))
    print("    %-18s %-34s %-34s %s" % ("key", "PRE display_name", "POST display_name", "POST name_source"))
    still_c = []
    for k in sorted(was_c):
        p = pre["chatter"]["rows"].get(k) or {}
        q = post["chatter"]["rows"].get(k) or {}
        print("    %-18s %-34r %-34r %r" % (k, p.get("display_name"), q.get("display_name"), q.get("name_source")))
        if q.get("name_source") == "ticker" or not q.get("display_name"):
            still_c.append(k)
    print("    MOVED: %d of %d; STILL TICKER-NAMED: %d %s"
          % (len(was_c) - len(still_c), len(was_c), len(still_c), still_c))
    if still_c:
        rc = 1

    print()
    print("=== POSITIVE CONTROL %s ===" % CONTROL)
    pr = pre["rankings"]["trending/price"]["rows"].get(CONTROL) or {}
    po = post["rankings"]["trending/price"]["rows"].get(CONTROL) or {}
    print("    ranked name        %r -> %r" % (pr.get("name"), po.get("name")))
    print("    ranked name_source %r -> %r" % (pr.get("name_source"), po.get("name_source")))
    print("    overlay            %r -> %r" % (pre["overlay"][CONTROL]["overlay_display_name"],
                                               post["overlay"][CONTROL]["overlay_display_name"]))

    print()
    print("=== NEGATIVE CONTROL -- rows already named at the base must not move ===")
    moved = []
    for kind in ("trending/price", "breakout/price"):
        was = set(k for k, _n, _w in pre["rankings"][kind]["unnamed"])
        for k, p in (pre["rankings"][kind]["rows"] or {}).items():
            if k in was:
                continue
            q = post["rankings"][kind]["rows"].get(k) or {}
            if p.get("display_name") != q.get("display_name") or p.get("name_source") != q.get("name_source"):
                moved.append((kind, k, p.get("display_name"), q.get("display_name"),
                              p.get("name_source"), q.get("name_source")))
    print("    already-named rows whose name or source CHANGED: %d" % len(moved))
    for m in moved[:12]:
        print("      %s %s %r->%r src %r->%r" % m)
    if moved:
        rc = 1

    print()
    print("CONDITION 2 VERDICT: %s" % ("PASS -- every previously unnamed key now carries a company "
                                       "name and no already-named row moved" if rc == 0 else
                                       "FAIL -- see the rows above"))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
