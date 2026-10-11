"""AMGT_CORPUS round 48, CRPS-ax-7 leg p (the /14 restatement of aw-4) / CRPS-ax-1 -- compare the LIVE /thesis payloads captured BEFORE and AFTER the redeploy that
carries /14, against the stored /14 dossiers. READ-ONLY (two local JSON files and S3 GETs). Issuer's file.

  PYTHONPATH=. python ax7_compare.py <pre.json> <post.json>

Per name, one line:
  team_sheet_equals_stored14   the post payload's `model.team_sheet` equals the stored /14 `team_sheet` field, every key (read_dossier at /13)
  others_equal                 every other captured field equals its pre-act read: `fiscal_year_figures`, `fiscal_years`, `header_figures`, `check_face`,
                               `model_status`, `posture`, `dossier_fields` and every `model` key but `team_sheet`
  bytes pre -> post            the response size, and growth = post - pre against that name's own team_sheet delta (its serialised team_sheet bytes post - pre)
Bound (the CTO's, msg 4101, replacing the withdrawn 1 MB ceiling): growth may not exceed the name's team_sheet delta, and the maximum response stays
under 6,291,456 bytes (the synchronous Lambda limit) with the margin printed; exceeding either is Branch C.
Totals: names; equal counts; the max response and its margin; names whose growth exceeds their delta. Branch A needs team_sheet_equals_stored14 on every
name that wrote, others_equal on every name (a Bloomberg vintage stamp or a value that moved with a daily pull is printed WHOLE, never hidden), growth
within delta on every name, and the max under 6 MB.
Prints `ax7 compare build <b>/1`.
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store

LIMIT = 6291456  # the synchronous Lambda response limit; the CTO's 1 MB ceiling was withdrawn (msg 4101)
OTHER_TOP = ("fiscal_year_figures", "fiscal_years", "header_figures", "check_face", "model_status", "posture", "dossier_fields")


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _stored14(key, client):
    cur = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = "amgt-corpus-dossier/14"
    try:
        doc = dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = cur
    if doc.get("method_version") != "amgt-corpus-dossier/14":
        return None
    return (doc.get("fields") or {}).get("team_sheet")


def main(argv):
    pre = json.load(open(argv[0], encoding="utf-8"))
    post = json.load(open(argv[1], encoding="utf-8"))
    print("pre function %s" % json.dumps(pre.get("function"), sort_keys=True))
    print("post function %s" % json.dumps(post.get("function"), sort_keys=True))
    client = store._default_client()
    names = sorted(post["keys"])
    ts_eq = oth_eq = n = 0
    biggest = (0, None)
    over = 0
    grew = 0
    for key in names:
        n += 1
        a, b = pre["keys"].get(key), post["keys"][key]
        if a is None:
            print("NO-PRE %s" % key)
            continue
        stored = _stored14(key, client)
        pt = (b.get("model") or {}).get("team_sheet")
        e1 = stored is not None and _canon(pt) == _canon(stored)
        diffs = []
        for k in OTHER_TOP:
            if _canon(a.get(k)) != _canon(b.get(k)):
                diffs.append(k)
        ma, mb = a.get("model") or {}, b.get("model") or {}
        for k in sorted(set(ma) | set(mb)):
            if k == "team_sheet":
                continue
            if _canon(ma.get(k)) != _canon(mb.get(k)):
                diffs.append("model." + k)
        e2 = not diffs
        ts_eq += int(e1)
        oth_eq += int(e2)
        pb, qb = a.get("response_bytes", 0), b.get("response_bytes", 0)
        if qb > biggest[0]:
            biggest = (qb, key)
        tsa, tsb = a.get("team_sheet_bytes"), b.get("team_sheet_bytes")
        delta = (tsb - tsa) if (isinstance(tsa, int) and isinstance(tsb, int)) else None
        growth = qb - pb
        exceeds = delta is None or growth > delta
        grew += int(exceeds)
        over += int(qb > LIMIT)
        print("ax7 %s status %s team_sheet_equals_stored14 %s others_equal %s%s bytes %d -> %d growth %d team_sheet_delta %s within %s class %s" % (
            key, b.get("status"), int(e1), int(e2), (" DIFF[" + ",".join(diffs) + "]") if diffs else "", pb, qb, growth, delta,
            int(not exceeds), (pt or {}).get("class") if isinstance(pt, dict) else None))
    print("ax7 names %d team_sheet_equals_stored14 %d/%d others_equal %d/%d max_response_bytes %d (%s) margin_to_6MB %d over_6MB %d growth_exceeds_delta %d" % (
        n, ts_eq, n, oth_eq, n, biggest[0], biggest[1], LIMIT - biggest[0], over, grew))
    build = int(n == len(names) and ts_eq == n and oth_eq == n and over == 0 and grew == 0)
    print("ax7 compare build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
