"""PRF-a-5 + PRF-b-6 EXERCISE (ADVI_PERFRP TO-R1-DS, AC6) -- book membership tie-out.

AC6: the Book view's relationship set == the set d07's leaderboard publishes for that
advisor+window.

This is a TIE-OUT AGAINST A LIVE SERVED ARTIFACT, not against a fixture. The
leaderboard is the thing an advisor already sees; if my book disagrees with it, one
of the two surfaces is lying to the same person about the same book.

THE AS-OF TRAP, HANDLED EXPLICITLY: leaderboard.json carries data_as_of = 2026-08-20
while today's jd2 frontier is 2026-08-21. Comparing my 08-21 book against their 08-20
publication would manufacture differences that are pure vintage skew and read as a
tie-out failure. The exercise reads jd2 AT THE LEADERBOARD'S OWN as_of, taken from the
artifact rather than assumed.

EVIDENCE VINTAGE: live plane read 2026-08-25; citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import io
import json
import sys

import boto3
import pyarrow.parquet as pq

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from perfrp_book import (  # noqa: E402  IMPORTED, never copied
    EXCLUDED_ROLE_COLUMNS,
    ROLE_BREAKDOWN_SEMANTICS,
    ROLES,
    book_membership,
    role_sum_would_be,
)

ASSETS = "opal-data-assets"
SERVE_BUCKET = "opal-data-portal-v2"
LEADERBOARD = "platinum/advi/49financial/leaderboard.json"
JD2 = "blackdiamond/49f/silver/dim_advisor_fee_role/"

PASSED = 0
FAILED = 0


def check(label, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
    else:
        FAILED += 1
    print("  [%s] %-54s %s" % ("PASS" if ok else "FAIL", label, detail))


def main() -> int:
    s3 = boto3.client("s3")
    lb = json.loads(s3.get_object(Bucket=SERVE_BUCKET, Key=LEADERBOARD)["Body"].read())
    asof = lb["data_as_of"]

    print("PRF-a-5 + PRF-b-6 EXERCISE -- ADVI_PERFRP TO-R1-DS (AC6)")
    print("=" * 100)
    print("served artifact : s3://%s/%s" % (SERVE_BUCKET, LEADERBOARD))
    print("  generated_at  : %s" % lb["generated_at"])
    print("  data_as_of    : %s   <- jd2 is read AT THIS DATE, taken from the artifact" % asof)
    print("  semantics     : %s" % lb.get("role_breakdown_semantics"))

    key = "%sdate=%s/data.parquet" % (JD2, asof)
    jd2 = pq.read_table(io.BytesIO(
        s3.get_object(Bucket=ASSETS, Key=key)["Body"].read())).to_pandas()
    cur = jd2[jd2["is_current"].astype(bool)]
    rows = cur.to_dict("records")
    print("  jd2 source    : s3://%s/%s" % (ASSETS, key))
    print("  jd2 rows %d, is_current %d, distinct accounts %d"
          % (len(jd2), len(cur), cur["account_id"].nunique()))

    print("\nAC6.0 -- the contract term is REPRODUCED, not coined")
    check("module semantics == the served artifact's own declaration",
          ROLE_BREAKDOWN_SEMANTICS == lb.get("role_breakdown_semantics"),
          ROLE_BREAKDOWN_SEMANTICS)

    print("\nAC6.1 -- `manager` exclusion VERIFIED, not inherited from d07's docstring")
    for col in EXCLUDED_ROLE_COLUMNS:
        vals = set(jd2[col].fillna("").astype(str))
        check("%s has exactly one value across ALL %d rows" % (col, len(jd2)),
              len(vals) == 1 and vals == {"Unassigned"}, "values=%s" % sorted(vals))

    book = book_membership(rows)
    entries = lb["windows"]["MAX"]["entries"]
    lbmap = {e["name"]: e for e in entries}

    print("\nAC6.2 -- THE TIE-OUT: my book set vs the LIVE leaderboard")
    print("  my advisors %d | leaderboard entries %d" % (len(book), len(entries)))
    only_mine = sorted(set(book) - set(lbmap))
    only_lb = sorted(set(lbmap) - set(book))
    check("advisor SETS are identical (not merely equal in count)",
          not only_mine and not only_lb,
          "mine-only=%d lb-only=%d" % (len(only_mine), len(only_lb)))

    match = 0
    diffs = []
    for name, e in lbmap.items():
        mine, theirs = len(book.get(name, ())), e.get("account_count")
        if mine == theirs:
            match += 1
        else:
            diffs.append((name, mine, theirs))
    check("per-advisor account_count ties for EVERY advisor",
          not diffs, "%d/%d match" % (match, len(lbmap)))
    for n, m, t in diffs[:5]:
        print("      DIFF %-26s mine=%s leaderboard=%s" % (n, m, t))

    print("\nAC6.3 -- NON-ADDITIVITY IS REAL AND MEASURED (R-p5), not asserted")
    print("        an advisor holding two roles on one account must count ONCE.")
    shown = 0
    worst = (None, 0, 0)
    for name in sorted(book, key=lambda a: -len(book[a]))[:6]:
        deduped = len(book[name])
        additive = role_sum_would_be(rows, name)
        if additive > deduped and shown < 4:
            print("        %-24s tagged-book=%-6d additive-sum=%-6d  overstates by %d (%.1f%%)"
                  % (name, deduped, additive, additive - deduped,
                     100.0 * (additive - deduped) / deduped))
            shown += 1
        if additive - deduped > worst[2] - worst[1]:
            worst = (name, deduped, additive)
    check("the additive rollup OVERSTATES at least one real book",
          worst[0] is not None and worst[2] > worst[1],
          "worst: %s %d -> %d" % worst if worst[0] else "none found")
    check("and the tagged-book count is the one that ties to the served surface",
          len(book.get(worst[0], ())) == lbmap[worst[0]]["account_count"] if worst[0] else False,
          "%s: book=%d leaderboard=%d" % (worst[0], len(book.get(worst[0], ())),
                                          lbmap[worst[0]]["account_count"]) if worst[0] else "")

    print("\nAC6.4 -- the four KPIs are present on the served surface to roll up against")
    e0 = entries[0]
    for kpi in ("total_aua", "nna", "client_count", "account_count"):
        check("leaderboard carries %s" % kpi, kpi in e0, str(e0.get(kpi))[:28])

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d checks, %d PASS, %d FAIL | advisors %d | roles %d"
          % (PASSED + FAILED, PASSED, FAILED, len(book), len(ROLES)))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
