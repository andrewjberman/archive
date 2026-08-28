"""EXECUTOR-SIDE acceptance check for D1_CATVIEWS chain step 3 (CTO ruling 14212).

WHAT THIS IS FOR. Step 3 is `mdpf_refresh.py gold` (floor -> accrual -> publisher).
That tool prints its own VERIFY block, and 1.0.0_SA_CTO~Z has RULED that citing its
PASS as evidence the SMA figure landed is itself a defect: `mdpf_refresh.py:104-105`
reads ONE artifact type (`aggregate-aua-timeseries`), hardcoded, and `:279-283`
scores only `as_of` recency and write recency. It never opens a value and it cannot
see `category-views` at all. It passes HONESTLY while answering a different question.

So this reads the thing the deliverable is actually about: the SERVED
`category-views` BODIES.

  ACCEPTANCE (14212)          platinum/mdpf/{scope}/category-views.json, BODY, per scope
    global / 49financial      nodes.SMA.aum == 22,794,766.25  AND absent_reason ABSENT
    cottonwood / inflection   nodes.SMA.aum == 0.00           AND absent_reason PRESENT
  CONSERVATION, global        Client.aum + SMA.aum == 290,426,813.47 -- PRINTED AS A
                              CONTROL, NOT SCORED. 14212 called this "the one that
                              matters ... cannot pass by accident"; MEASURED, IT PASSES
                              RIGHT NOW ON THE UN-RELANDED PLANE (290,426,813.47 + 0.00)
                              with nothing done. The fix REALLOCATES between two
                              siblings, so a criterion on their SUM is invariant across
                              the exact change it exists to accept. Kept because a
                              WRONG-AMOUNT fix still fails it -- a conservation guard on
                              a non-degenerate value, which is what 2.0.0_SA_COO~Z ruled
                              the identical PRD AC4 to be (14091/14097).
  L2 MEMBERS, global          members carry `aum`. Scored as a FLOOR (>=8 non-null) over
                              a WIDE sweep of every L2 member (15 at global). 14212's
                              "8 of 9" is a NARROWER set -- two denominators over one
                              world, not the same claim, and not reported as agreeing.

WHAT DISCRIMINATES, THEREFORE: the per-scope SMA.aum and absent_reason reads, which are
OPPOSITE in direction across the two scope groups (dollars must APPEAR at global/49f and
must STAY ZERO WITH ITS EXPLANATION at cottonwood/inflection). A one-sided "did SMA
appear" sweep would score a global-only bug as success.

THREE DEFECTS BANKED FROM 3.0.0_SA_CVO~Z's OWN RATIFIER (14182 s3), folded in here
rather than rediscovered:
  1. UNREADABLE IS ITS OWN STATE. A failed retrieval is INDETERMINATE (rc=2), never a
     FAIL and never a PASS. CVO's first build counted retrieval failures as refusals,
     and its negative control then "passed" while the instrument had never read a
     single object -- it would have refused identically after a perfect reland.
  2. POSITIVE EXPECTATIONS, NOT BLACKLISTS. Every assertion states what MUST be true.
  3. PATHS ARE MEASURED, NOT REASONED BY ANALOGY. bucket/prefix/key shape are read off
     the publisher at source (SERVE_BUCKET/SERVE_ROOT, `serve_key` at :282), because
     guessing platinum layout by analogy from gold is the exact cross-plane analogy
     that has already produced two wrong answers tonight.

NOT A RATIFIER, AND NOT THE PRIMARY CARRIER. 3.0.0_SA_CVO~Z's `ratify_sma_live.py`
@97239e14c4 IS the acceptance instrument for the four ruled rows: it asserts them
exactly, over BOTH planes and all four scopes, and is proven to refuse the current plane
(PASS 12 / FAIL 12, 24 assertions). It was armed before this file existed (14220).

>> SO THE FOUR RULED SMA ROWS HERE ARE DELIBERATELY REDUNDANT AND THE CVO INSTRUMENT IS
   NAMED PRIMARY. Two durable checks of one obligation drift from minute one, and the
   drift is invisible while they agree. If this file and the ratifier ever disagree on
   those rows, THE RATIFIER IS RIGHT and this file is stale. <<

WHAT THIS ADDS THAT THE RATIFIER DOES NOT COVER -- the only reason it exists:
  - the L2 MEMBER `aum` leg (the D-1 half, reclassified DATA-not-RENDER on 2026-08-28).
  - conservation demoted to an UNSCORED control, with the measurement that demotes it.
Both are OFFERED FOR ABSORPTION into the ratifier. If 3.0.0_SA_CVO~Z takes them, this
file should be DELETED rather than kept in sync -- one carrier, not two.

Usage:  python verify_step3_served_category_views.py [--json]
Exit:   0 all assertions PASS · 1 at least one FAIL · 2 INDETERMINATE (unreadable)
"""
from __future__ import annotations

import argparse
import json
import sys

import boto3

# Read off the publisher at source, never assumed:
#   lambda_function.py  SERVE_BUCKET = opal-data-portal-v2 · SERVE_ROOT = platinum/mdpf
#   :282  serve_key = f"{SERVE_ROOT}/{scope}/{atype}.json"   <- NO as_of IN THE KEY.
# Platinum is a MUTABLE latest-style key (3.0.0_SA_CVO~Z 14182): a stale object sits at
# the SAME key as a fresh one, so the key proves nothing about vintage. Everything below
# is read from the BODY.
SERVE_BUCKET = "opal-data-portal-v2"
SERVE_ROOT = "platinum/mdpf"
ARTIFACT = "category-views"

SMA_EXPECTED = 22794766.25
CLIENT_PRE_FIX_TOTAL = 290426813.47      # global Client.aum BEFORE the extraction
CENT = 0.005                             # half a cent; raw values are always printed

# MECE over the declared scope set: every scope is in exactly one bucket, and the two
# buckets have OPPOSITE expectations -- which is what makes this discriminating rather
# than a one-sided "did SMA appear" sweep.
SMA_BEARING = ("global", "49financial")   # SMA dollars present, absent_reason GONE
SMA_TRUE_ZERO = ("cottonwood", "inflection")  # genuinely 0.00, absent_reason PRESENT

_s3 = boto3.client("s3", region_name="us-east-1")


def _get_body(scope: str):
    key = f"{SERVE_ROOT}/{scope}/{ARTIFACT}.json"
    try:
        raw = _s3.get_object(Bucket=SERVE_BUCKET, Key=key)["Body"].read()
        return json.loads(raw), key, None
    except Exception as exc:  # noqa: BLE001 -- INDETERMINATE, never a verdict
        return None, key, f"{type(exc).__name__}: {exc}"


def _node(doc: dict, name: str) -> dict:
    return ((doc or {}).get("nodes") or {}).get(name) or {}


def _eq(actual, expected) -> bool:
    return isinstance(actual, (int, float)) and abs(float(actual) - expected) < CENT


def check() -> "tuple[int, list, list, list]":
    rows, indeterminate, controls = [], [], []

    def rec(scope, name, ok, detail):
        rows.append({"scope": scope, "assertion": name,
                     "verdict": "PASS" if ok else "FAIL", "detail": detail})

    bodies = {}
    for scope in SMA_BEARING + SMA_TRUE_ZERO:
        doc, key, err = _get_body(scope)
        if err:
            indeterminate.append({"scope": scope, "key": key, "reason": err})
            continue
        bodies[scope] = doc

    for scope in SMA_BEARING:
        if scope not in bodies:
            continue
        sma = _node(bodies[scope], "SMA")
        aum, reason = sma.get("aum"), sma.get("absent_reason")
        rec(scope, "SMA.aum == 22,794,766.25", _eq(aum, SMA_EXPECTED), f"aum={aum!r}")
        rec(scope, "SMA.absent_reason ABSENT", reason in (None, ""),
            f"absent_reason={'ABSENT' if reason in (None, '') else repr(reason)[:70]}")

    for scope in SMA_TRUE_ZERO:
        if scope not in bodies:
            continue
        sma = _node(bodies[scope], "SMA")
        aum, reason = sma.get("aum"), sma.get("absent_reason")
        rec(scope, "SMA.aum == 0.00", _eq(aum, 0.0), f"aum={aum!r}")
        # A TRUE ZERO must SAY it is one. Andrew ruled SMAs are 49F-only; these scopes
        # carrying 0.00 WITHOUT the explanation would be indistinguishable from the
        # pre-fix unreachable-branch artifact this whole fix exists to remove.
        rec(scope, "SMA.absent_reason PRESENT", bool(reason),
            f"absent_reason={'PRESENT' if reason else 'MISSING'}")

    # CONSERVATION -- CONTROL ONLY, EXCLUDED FROM THE VERDICT. MEASURED 2026-08-28
    # 21:5xZ: it PASSES ON THE UN-RELANDED PLANE (290,426,813.47 + 0.00), with nothing
    # done. 14212 called it "the one that matters ... cannot pass by accident"; that is
    # falsified by running it. The fix only REALLOCATES between two siblings, so a
    # criterion on their SUM is INVARIANT across the exact change it exists to accept --
    # the identical defect 2.0.0_SA_COO~Z measured on PRD AC4 (14091/14097) and held a
    # TO over, reappearing one rung along.
    #
    # It is NOT worthless and it is NOT deleted: a WRONG-AMOUNT fix
    # (267,632,047.22 + 22,000,000.00) FAILS it. So it is exactly what COO ruled AC4 to
    # be -- a CONSERVATION GUARD on a non-degenerate value, paired with criteria that
    # actually discriminate started-from-finished. Those are the SMA.aum and
    # absent_reason reads above, which is where the verdict comes from.
    if "global" in bodies:
        c_aum = _node(bodies["global"], "Client").get("aum")
        s_aum = _node(bodies["global"], "SMA").get("aum")
        if isinstance(c_aum, (int, float)) and isinstance(s_aum, (int, float)):
            total = float(c_aum) + float(s_aum)
            controls.append({
                "scope": "global",
                "assertion": "CONSERVATION Client.aum + SMA.aum == 290,426,813.47",
                "verdict": "PASS" if abs(total - CLIENT_PRE_FIX_TOTAL) < CENT else "FAIL",
                "detail": f"{c_aum} + {s_aum} = {total:.2f} (expected "
                          f"{CLIENT_PRE_FIX_TOTAL:.2f}, delta "
                          f"{total - CLIENT_PRE_FIX_TOTAL:+.2f})"})
        else:
            controls.append({
                "scope": "global",
                "assertion": "CONSERVATION Client.aum + SMA.aum == 290,426,813.47",
                "verdict": "FAIL",
                "detail": f"non-numeric: Client.aum={c_aum!r} SMA.aum={s_aum!r}"})

    # L2 MEMBER DOLLARS (the D-1 half, reclassified DATA not RENDER tonight). Reported
    # with its DENOMINATOR: the claim is "8 of 9 carry aum", so print both halves.
    if "global" in bodies:
        members = []
        for node in (bodies["global"].get("nodes") or {}).values():
            for child in (node.get("children") or {}).values():
                members.extend(child.get("members") or [])
        with_aum = [m for m in members if m.get("aum") is not None]
        # DENOMINATOR NOTE: this sweeps EVERY L2 member under every node/child at
        # global and finds 15. 14212's "8 of 9" refers to a NARROWER set (one child's
        # members). Different denominators over one world -- so >=8 is a FLOOR on the
        # wide set, not a restatement of the 8-of-9 claim, and the two must not be
        # reported as if they agreed.
        rec("global", "L2 members carry aum (>=8 non-null, wide sweep)",
            len(with_aum) >= 8,
            f"{len(with_aum)} of {len(members)} L2 member(s) carry a non-null aum "
            f"(wide sweep; 14212's 8-of-9 is a narrower set)")

    fails = [r for r in rows if r["verdict"] == "FAIL"]
    if indeterminate:
        return 2, rows, indeterminate, controls
    return (1 if fails else 0), rows, indeterminate, controls


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rc, rows, indeterminate, controls = check()
    if args.json:
        print(json.dumps({"rc": rc, "rows": rows, "indeterminate": indeterminate,
                          "controls_not_scored": controls}, indent=2))
        return rc

    print(f"\n== STEP-3 ACCEPTANCE: served {ARTIFACT} BODIES "
          f"(s3://{SERVE_BUCKET}/{SERVE_ROOT}/*/{ARTIFACT}.json) ==")
    for r in rows:
        print(f"  [{r['verdict']}] {r['scope']:<12} {r['assertion']:<52} {r['detail']}")
    if indeterminate:
        print("\n  INDETERMINATE -- object(s) unreadable. This is NOT a FAIL and NOT a")
        print("  PASS: an instrument that never read the object cannot have a verdict.")
        for i in indeterminate:
            print(f"    {i['scope']:<12} {i['key']}  {i['reason']}")

    if controls:
        print("\n  CONTROLS -- PRINTED, NOT SCORED (they pass on the un-relanded plane):")
        for c in controls:
            print(f"  [{c['verdict']}] {c['scope']:<12} {c['assertion']:<52} {c['detail']}")

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    print(f"\n  SCORED {n_pass} PASS / {len(rows) - n_pass} FAIL over {len(rows)} "
          f"assertion(s); {len(indeterminate)} scope(s) INDETERMINATE")
    print(f"  VERDICT: {['ACCEPT', 'REFUSE', 'INDETERMINATE'][rc]}")
    print("  NOTE: this is the EXECUTOR's check. Ratification is 3.0.0_SA_CVO~Z's, on "
          "its own instrument.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
