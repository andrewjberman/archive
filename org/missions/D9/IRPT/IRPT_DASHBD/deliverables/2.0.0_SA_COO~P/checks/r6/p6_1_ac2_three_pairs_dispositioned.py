"""DB6-1-AC2 -- CTO batches 181/182: the three like-day pairs beyond 0.35 pp each carry a stated reason; the defect among them (S22)
is fixed and re-measured; no vendor call.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R6.json:
  {"tolerance": 0.0035, "vendor_calls": 0,
   "pairs": [{"account", "start", "end", "abs_diff_r4", "abs_diff_now", "reason", "defect": bool, "fixed": bool}]}
Grades: tolerance == 0.0035; vendor_calls == 0; the pairs are exactly the three of batch 182 (acct#89d0916a 2026-06-25, acct#ffa615d2
2026-08-21, acct#89d0916a 2026-04-09); every pair has a non-empty reason and a numeric abs_diff_now; the acct#89d0916a 2026-06-25 pair
has defect true and fixed true; any pair with defect true has fixed true. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R6.json"
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


THREE = {(_REAL("acct#89d0916a"), "2026-06-25"), (_REAL("acct#ffa615d2"), "2026-08-21"), (_REAL("acct#89d0916a"), "2026-04-09")}


def fail(msg):
    print("FAIL: " + msg)
    print("DB6-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / REC
    if not p.is_file():
        fail("no record at %s" % REC)
    r = json.loads(p.read_text(encoding="utf-8"))
    if r.get("tolerance") != 0.0035:
        fail("tolerance is %r, not 0.0035" % r.get("tolerance"))
    if r.get("vendor_calls") != 0:
        fail("vendor_calls is %r, not 0" % r.get("vendor_calls"))
    pairs = r.get("pairs") or []
    got = {(x.get("account"), x.get("start")) for x in pairs}
    if got != THREE or len(pairs) != 3:
        fail("the pairs are %s, not the three of batch 182" % sorted(got))
    for x in pairs:
        if not str(x.get("reason") or "").strip():
            fail("%s %s has no reason" % (x["account"], x["start"]))
        try:
            float(x.get("abs_diff_now"))
        except (TypeError, ValueError):
            fail("%s %s has no numeric abs_diff_now" % (x["account"], x["start"]))
        if x.get("defect") is True and x.get("fixed") is not True:
            fail("%s %s is a defect not fixed" % (x["account"], x["start"]))
        if (x["account"], x["start"]) == (_REAL("acct#89d0916a"), "2026-06-25") and not (x.get("defect") is True and x.get("fixed") is True):
            fail("the S22 pair is not recorded as a fixed defect")
    print("OK: 3 of 3 pairs dispositioned; S22 fixed, abs_diff now %s; 0 vendor calls"
          % [x["abs_diff_now"] for x in pairs if (x["account"], x["start"]) == (_REAL("acct#89d0916a"), "2026-06-25")][0])
    print("DB6-1-AC2 PASS")


if __name__ == "__main__":
    main()
