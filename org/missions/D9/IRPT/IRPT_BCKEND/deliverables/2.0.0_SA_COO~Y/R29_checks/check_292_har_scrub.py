#!/usr/bin/env python3
"""IB-yr-292 AC2 -- the HAR scrub removes credential and cookie VALUES, proven by a planted value.

Builds a synthetic HAR in memory carrying a planted session value in four places (a request
`Cookie` header, a response `Set-Cookie` header, an `Authorization` header, and `cookies[].value`)
plus one harmless header, writes it to a temp file, runs `har_scrub.scrub(src, dst)` and reads back:
  * the planted value occurs 0 times in the scrubbed output (the scan is on the OUTPUT BYTES);
  * the census reports headers_scrubbed == 3 and cookies_scrubbed == 1 and residual_hits == 0;
  * the harmless header survives byte-for-byte;
  * NEGATIVE CONTROL: a HAR with no such headers scrubs to identical bytes with all counts 0.
PASS iff every line holds. Base run (CLOUD HEAD before the cut): FAIL -- har_scrub does not exist.
Issuer 2.0.0_SA_COO~Y, round 29. ASCII only.
"""
import json
import os
import sys
import tempfile

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R29_checks itself; the repo root is parents[8]
LIB = os.path.join(ROOT, "infra", "aws", "ec2", "investor-reporting-ycharts")
sys.path.insert(0, LIB)

PLANTED = "PLANTED-SESSION-VALUE-9f3c2a7e"


def har(with_secrets):
    req_headers = [{"name": "Accept", "value": "application/json"}]
    res_headers = [{"name": "Content-Type", "value": "application/json"}]
    cookies = []
    if with_secrets:
        req_headers.append({"name": "Cookie", "value": "ycsessionid=" + PLANTED + "; csrftoken=abc"})
        req_headers.append({"name": "Authorization", "value": "Bearer " + PLANTED})
        res_headers.append({"name": "Set-Cookie", "value": "ycsessionid=" + PLANTED + "; Path=/"})
        cookies.append({"name": "ycsessionid", "value": PLANTED})
    return {"log": {"version": "1.2", "entries": [{
        "request": {"method": "GET", "url": "https://ycharts.com/dashboard/", "headers": req_headers,
                    "cookies": list(cookies)},
        "response": {"status": 200, "headers": res_headers, "cookies": list(cookies),
                     "content": {"size": 0, "mimeType": "application/json"}}}]}}


def run(doc):
    import har_scrub  # noqa: E402  (the cell's module)
    d = tempfile.mkdtemp()
    src, dst = os.path.join(d, "raw.har"), os.path.join(d, "scrubbed.har")
    with open(src, "w", encoding="utf-8") as fh:
        json.dump(doc, fh)
    census = har_scrub.scrub(src, dst)
    with open(dst, "rb") as fh:
        out = fh.read()
    with open(src, "rb") as fh:
        raw = fh.read()
    return census, raw, out


def main():
    try:
        import har_scrub  # noqa: F401
    except ImportError as exc:
        print("FAIL: har_scrub not importable from %s (%s)" % (LIB, exc))
        return 1
    census, raw, out = run(har(True))
    hits = out.count(PLANTED.encode())
    print("planted value occurrences in OUTPUT:", hits, "| in INPUT:", raw.count(PLANTED.encode()))
    print("census:", json.dumps(census, sort_keys=True))
    kept = json.loads(out.decode("utf-8"))["log"]["entries"][0]["request"]["headers"][0]
    print("harmless header after scrub:", json.dumps(kept, sort_keys=True))
    ok = (hits == 0 and census.get("headers_scrubbed") == 3 and census.get("cookies_scrubbed") == 1
          and census.get("residual_hits") == 0
          and kept == {"name": "Accept", "value": "application/json"})
    census0, raw0, out0 = run(har(False))
    print("negative control census:", json.dumps(census0, sort_keys=True), "| bytes identical:", raw0 == out0)
    ok = ok and census0.get("headers_scrubbed") == 0 and census0.get("cookies_scrubbed") == 0 and raw0 == out0
    if ok:
        print("PASS: planted value absent from the scrubbed output on every path; harmless header kept; negative control byte-identical")
    else:
        print("FAIL: the scrub did not hold on every path (read the census lines above)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
