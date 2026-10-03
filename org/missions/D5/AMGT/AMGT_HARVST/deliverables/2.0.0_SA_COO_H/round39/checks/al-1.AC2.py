"""HVST-al-1 AC2 (issuer, LOCAL, no network): a Dow Jones listing that answers HTTP 200 with 0 parseable hits is told
apart from a genuine "no articles" (row Z-W91-S10; round-38 analysis enrichment item 1).

Drives the REAL `publishers.DowJones.discover` for wsj AND barrons through a stub session (no network). PASS requires:
- `publishers.LISTING_EMPTY_200 == "listing_empty_200"`;
- a 200 response whose body parses to 0 hits returns [] AND sets `listing_empty_200` True on the instance;
- a 403 response does NOT set the flag (status-gated, never body-only);
- the flag is reset on the next call (a later 403 after an empty 200 reads False).
"""
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)


class Resp:
    def __init__(self, status, text):
        self.status_code, self.text = status, text

    def json(self):
        raise ValueError("not json")


class Session:
    def __init__(self, responses):
        self.responses = list(responses)

    def get(self, url, params=None, headers=None, **kw):
        return self.responses.pop(0)


EMPTY = "<html><head><title>Search</title></head><body><main>No results</main></body></html>"


def main():
    failures = []
    try:
        from lib.opal_data_harvest import publishers as p
    except Exception as exc:
        print("IMPORT FAILED: %s" % exc)
        print("AC2 RESULT: FAIL (1 failure(s))")
        return 1
    if getattr(p, "LISTING_EMPTY_200", None) != "listing_empty_200":
        failures.append("publishers.LISTING_EMPTY_200 is %r" % getattr(p, "LISTING_EMPTY_200", None))
    sec = {"company": "Example Co"}
    for pub in ("wsj", "barrons"):
        dj = p.DowJones(pub, Session([Resp(200, EMPTY), Resp(403, EMPTY)]))
        urls = dj.discover(sec)
        flag1 = getattr(dj, "listing_empty_200", None)
        urls2 = dj.discover(sec)
        flag2 = getattr(dj, "listing_empty_200", None)
        print("%s: 200-empty -> urls %r flag %r; then 403 -> urls %r flag %r" % (pub, urls, flag1, urls2, flag2))
        if urls != []:
            failures.append("%s: 200-empty returned %r" % (pub, urls))
        if flag1 is not True:
            failures.append("%s: 200-empty flag is %r, not True" % (pub, flag1))
        if flag2 is not False:
            failures.append("%s: a 403 after an empty 200 reads flag %r, not False" % (pub, flag2))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
