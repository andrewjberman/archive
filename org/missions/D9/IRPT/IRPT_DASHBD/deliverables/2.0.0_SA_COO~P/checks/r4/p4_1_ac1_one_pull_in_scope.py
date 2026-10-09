"""DB4-1-AC1 -- the ONE Black Diamond pull Andrew's card 4 admits (record @0abef798f7): the five round-1 accounts, Opal's gap-free
segments, nothing else.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/BD_LIKEDAY_PULL_R4.json:
  {"word": "<the record path or hash>", "endpoint": "performancePeriod", "accounts_in_scope": [the five],
   "requests": [{"account": "<schwab>", "bd_account": "<bd id>", "ranges": [{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}],
                 "http_status": 200}],
   "vendor_calls": n, "unmapped": [{"account": "<schwab>", "reason": "..."}]}
and deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.json's "pairs".
Grades: accounts_in_scope is exactly the five round-1 accounts; every request's account is one of them and appears in at most ONE
request; vendor_calls == len(requests) and <= 5; every requested range is a pair (account, start, end) of the tie-out record; every
account of the five is either requested or unmapped-with-a-reason. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


FIVE = {_REAL("acct#89d0916a"), _REAL("acct#f08ffd13"), _REAL("acct#6b914f88"), _REAL("acct#ffa615d2"), _REAL("acct#d0cf6c92")}
W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/"


def fail(msg):
    print("FAIL: " + msg)
    print("DB4-1-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p, t = root / (W + "BD_LIKEDAY_PULL_R4.json"), root / (W + "TIEOUT_49F_BLACKDIAMOND_R4.json")
    if not p.is_file():
        fail("no pull record BD_LIKEDAY_PULL_R4.json")
    if not t.is_file():
        fail("no tie-out record TIEOUT_49F_BLACKDIAMOND_R4.json")
    rec, tie = json.loads(p.read_text(encoding="utf-8")), json.loads(t.read_text(encoding="utf-8"))
    if set(rec.get("accounts_in_scope") or []) != FIVE:
        fail("accounts_in_scope is not exactly the five round-1 accounts")
    if rec.get("endpoint") != "performancePeriod":
        fail("endpoint is not performancePeriod")
    reqs = rec.get("requests") or []
    seen = set()
    pairs = {(x.get("account"), x.get("start"), x.get("end")) for x in tie.get("pairs") or []}
    for r in reqs:
        a = r.get("account")
        if a not in FIVE:
            fail("a request names an account outside the five: %r" % a)
        if a in seen:
            fail("account %s is requested more than once" % a)
        seen.add(a)
        for rg in r.get("ranges") or []:
            if (a, rg.get("start"), rg.get("end")) not in pairs:
                fail("requested range %s %s..%s is not a pair of the tie-out record" % (a, rg.get("start"), rg.get("end")))
    if int(rec.get("vendor_calls", -1)) != len(reqs) or len(reqs) > 5:
        fail("vendor_calls %r against %d request(s) (cap 5)" % (rec.get("vendor_calls"), len(reqs)))
    unmapped = {u.get("account"): u.get("reason") for u in rec.get("unmapped") or []}
    for a in FIVE - seen:
        if not str(unmapped.get(a) or "").strip():
            fail("account %s is neither requested nor unmapped with a reason" % a)
    print("OK: %d request(s) = vendor_calls, %d unmapped with reasons, every range a tie-out pair" % (len(reqs), len(FIVE - seen)))
    print("DB4-1-AC1 PASS")


if __name__ == "__main__":
    main()
