"""HVST-ac-3 AC2 (issuer check, read-only): the two in-window bbg articles reach the PAGE for 992_HK.

Read through the route's own handlers (`scoped_amgt._serve_timeline`, in-process at the checked-out code, reading the served S3
gold and silver). PASS requires:
- the `/timeline` series for 992_HK carries `bbg` in `publishers_found_codes` on 2026-08-13 and 2026-09-01, with
  `articles_total` at least 1 on each;
- the `/timeline/day` route for each of those days lists the bbg story-id article with a non-empty headline and its
  `mention_count`;
- for the co-mentioned expected rows (AAPL, C, MU on 2026-08-13), the series row carries `bbg` in `publishers_found_codes`.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ac3_common as c  # noqa: E402

from lib.research.api import scoped_amgt  # noqa: E402



def serve(sec, day=None):
    resp = scoped_amgt._serve_timeline(sec, day, {})
    body = resp.get("body")
    return resp.get("statusCode"), (json.loads(body) if isinstance(body, str) else (body or {}))


def main():
    failures = []
    expected = sorted(c.expected_rows())
    series_cache = {}
    for sec, day in expected:
        if sec not in series_cache:
            status, body = serve(sec)
            series_cache[sec] = {str(r.get("date"))[:10]: r for r in body.get("series") or []}
            print("series %s: status %s, %d days" % (sec, status, len(series_cache[sec])))
        row = series_cache[sec].get(day) or {}
        found = row.get("publishers_found_codes") or []
        print("  %s %s: articles_total %s, found %s, covered %s"
              % (sec, day, row.get("articles_total"), found, row.get("publishers_covered_codes")))
        if "bbg" not in found:
            failures.append("%s %s: bbg not in publishers_found_codes on the series" % (sec, day))
        if sec == c.LENOVO:
            if not (row.get("articles_total") or 0) >= 1:
                failures.append("%s %s: articles_total < 1" % (sec, day))
            status, body = serve(sec, day)
            bbg = [a for a in body.get("articles") or [] if str(a.get("article_key", "")).startswith("bbg:")]
            ok = [a for a in bbg if (a.get("headline") or "").strip() and a.get("mention_count")]
            print("  day route %s %s: status %s, bbg articles %d, with headline + mention_count %d"
                  % (sec, day, status, len(bbg), len(ok)))
            if status != 200 or not ok:
                failures.append("%s %s: the day route lists no bbg article with a headline and mention_count" % (sec, day))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
