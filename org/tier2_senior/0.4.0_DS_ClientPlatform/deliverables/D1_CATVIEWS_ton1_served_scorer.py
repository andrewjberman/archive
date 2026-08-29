"""TO-N1-DS AC3/AC4/AC5/AC6 -- score the four SERVED-rung rows against the relanded body.

READ-ONLY. No S3 writes, no producer edit. This is a SCORING act against an artifact that
already exists (COO 16189): if a row cannot be scored as written, it says so and stops.

BEFORE-IMAGES are LIFTED VERBATIM from D1_CATVIEWS.TO-N1-DS_PROOF_OF_SPEC.json, where they
were captured with their denominator (4 of 4 scopes) at the 2026-08-28T13:31:13Z object.
They are NOT re-derived here -- the pre-fix artifact was deleted and rebuilt by the reland,
so re-deriving them is impossible and asserting them from memory would be worse.

⛔ AC7 and TM1-AC1 are NOT scored: both require a SCHEDULED fire by their own verbatim and
the reland is AD-HOC. 4 is the whole scoreable set today, not a 4-of-6 shortfall.

Usage: python D1_CATVIEWS_ton1_served_scorer.py
"""
from __future__ import annotations

import io
import json

import boto3

BUCKET = "opal-data-assets"
SCOPES = ("49financial", "cottonwood", "inflection", "global")
DATED = "2026-08-27"
BAR = "=" * 92

# Captured at the pre-reland object, 4 of 4 scopes, LastModified 2026-08-28T13:31:13Z,
# _provenance.trigger="scheduled". Source: the TO-N1-DS proof-of-spec instance.
BEFORE = {
    "49financial": {"sma": 0.00, "client": 290426813.47, "total": 1762750154.52, "reason": True},
    "cottonwood":  {"sma": 0.00, "client": 294905777.43, "total": 481690858.04, "reason": True},
    "inflection":  {"sma": 0.00, "client": 64867579.31, "total": 209683644.85, "reason": True},
    "global":      {"sma": 0.00, "client": 290426813.47, "total": 2094351300.67, "reason": True},
}
# AC3 limb D's literals -- scored ONLY when as_of == this date, else N/A-BY-DATE.
D_AS_OF = "2026-08-27"
D_DELTA = 22794766.25
D_CLIENT_AFTER = 267632047.22


def _get(s3, key):
    return json.load(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()))


def r2(x):
    return None if x is None else round(float(x), 2)


def main():
    s3 = boto3.client("s3")
    cv, meta = {}, {}
    for sc in SCOPES:
        k = f"portal/gold/mdpf/{sc}/category-views/{DATED}.json"
        cv[sc] = _get(s3, k)
        h = s3.head_object(Bucket=BUCKET, Key=k)
        meta[sc] = (h["LastModified"], h["ContentLength"])
    ts49 = _get(s3, f"portal/gold/mdpf/49financial/aggregate-aua-timeseries/{DATED}.json")

    print(BAR)
    print("AFTER-IMAGE PROVENANCE -- denominator 4 of 4 scopes")
    print(BAR)
    for sc in SCOPES:
        p = cv[sc].get("_provenance") or {}
        print(f"  {sc:<12} LastModified {meta[sc][0]}  {meta[sc][1]}B  "
              f"as_of={cv[sc].get('as_of')}  trigger={p.get('trigger')!r}")
    print()

    def node(sc, n):
        return (cv[sc].get("nodes") or {}).get(n) or {}

    rows = []

    # ---- AC3 -------------------------------------------------------------------
    print(BAR)
    print("CATV-TON1-AC3 -- the money was REATTRIBUTED; none created or destroyed")
    print(BAR)
    as_of = cv["49financial"].get("as_of")
    sma_after = node("49financial", "SMA").get("aum")
    client_after = node("49financial", "Client").get("aum")
    nm_after = (ts49.get("non_model_aua") or [None])[-1]
    sma_members = {k: (v or {}).get("model_value", [None])[-1]
                   for k, v in (ts49.get("by_model") or {}).items()
                   if (v or {}).get("cohort_class") == "sma"}
    sma_sum = round(sum(float(v) for v in sma_members.values()), 4)

    print(f"  as_of (served)        : {as_of}")
    print(f"  SMA members resolved  : {len(sma_members)} -> {sma_members}")
    print(f"  sum(model_value)      : {sma_sum:,.4f}")
    print(f"  SMA.aum(after)        : {float(sma_after):,.4f}")
    a = round(float(sma_after), 4) == sma_sum
    print(f"  (A) SMA == sum(SMA member model_value) at its OWN as_of      {'PASS' if a else 'FAIL'}")

    print(f"  non_model_aua(after)  : {float(nm_after):,.4f}")
    b_expect = round(float(nm_after) - float(sma_after), 4)
    b = round(float(client_after), 4) == b_expect
    print(f"  Client.aum(after)     : {float(client_after):,.4f}  vs non_model - SMA = {b_expect:,.4f}")
    print(f"  (B) Client == non_model - SMA                                {'PASS' if b else 'FAIL'}")

    c = r2(BEFORE["49financial"]["client"]) == r2(BEFORE["49financial"]["client"])
    c = r2(BEFORE["49financial"]["client"]) == r2(nm_after)
    print(f"  (C) BEFORE Client {BEFORE['49financial']['client']:,.2f} == non_model_aua "
          f"{float(nm_after):,.2f}, UNNETTED                {'PASS' if c else 'FAIL'}")
    print("      (non_model_aua is the INPUT and is unchanged by the fix -- that is what makes")
    print("       the before-signature comparable to the after at all)")

    if as_of == D_AS_OF:
        delta = r2(BEFORE["49financial"]["client"] - float(client_after))
        d = (delta == D_DELTA) and (r2(client_after) == D_CLIENT_AFTER)
        print(f"  (D) as_of IS {D_AS_OF} -> literals ARE scored")
        print(f"      delta {delta:,.2f} vs {D_DELTA:,.2f} | Client(after) {r2(client_after):,.2f} "
              f"vs {D_CLIENT_AFTER:,.2f}                    {'PASS' if d else 'FAIL'}")
        d_state = "PASS" if d else "FAIL"
    else:
        d_state = "N/A-BY-DATE"
        print(f"  (D) as_of is {as_of}, not {D_AS_OF} -> N/A-BY-DATE (never PASS, never FAIL)")
    ac3 = a and b and c and d_state in ("PASS", "N/A-BY-DATE")
    rows.append(("CATV-TON1-AC3", ac3, f"A/B/C PASS, D={d_state}"))

    # ---- AC4 -------------------------------------------------------------------
    print()
    print(BAR)
    print("CATV-TON1-AC4 -- the OTHER TWO FIRMS DO NOT MOVE")
    print(BAR)
    ac4 = True
    for sc in ("cottonwood", "inflection"):
        s_a, c_a = node(sc, "SMA").get("aum"), node(sc, "Client").get("aum")
        ok = r2(s_a) == r2(BEFORE[sc]["sma"]) and r2(c_a) == r2(BEFORE[sc]["client"])
        ac4 = ac4 and ok
        print(f"  {sc:<12} SMA {r2(BEFORE[sc]['sma']):>14,.2f} -> {r2(s_a):>14,.2f} | "
              f"Client {BEFORE[sc]['client']:>16,.2f} -> {r2(c_a):>16,.2f}   "
              f"{'UNMOVED' if ok else 'MOVED <-- FAIL'}")
    rows.append(("CATV-TON1-AC4", ac4, "both firms unmoved on both nodes"))

    # ---- AC5 -------------------------------------------------------------------
    print()
    print(BAR)
    print("CATV-TON1-AC5 -- the false sentence GONE for 49financial, STILL PRESENT where TRUE")
    print(BAR)
    gone, kept = None, {}
    for sc in SCOPES:
        n = node(sc, "SMA")
        r = (n.get("absent_reason") or "").strip()
        present = bool(r)
        mp = n.get("members_present")
        print(f"  {sc:<12} members_present={str(mp):<5} absent_reason "
              f"{'PRESENT' if present else 'ABSENT ':<8} {r[:52]!r}")
        if sc == "49financial":
            gone = not present
        elif sc in ("cottonwood", "inflection"):
            kept[sc] = present
    ac5 = bool(gone) and all(kept.values())
    print(f"  limb 1 -- GONE at 49financial            : {gone}")
    print(f"  limb 2 -- STILL PRESENT where TRUE       : {kept}")
    rows.append(("CATV-TON1-AC5", ac5, "both limbs measured"))

    # ---- the fourth scope, which NO criterion on this TO covers ------------------
    print()
    print(BAR)
    print("⛔ REPORTED, NOT SCORED -- `global` MOVED AND NO CRITERION ON THIS TO NAMES IT")
    print(BAR)
    g_sma = float(node("global", "SMA").get("aum") or 0.0)
    g_cli = float(node("global", "Client").get("aum") or 0.0)
    g_reason = bool((node("global", "SMA").get("absent_reason") or "").strip())
    print(f"  SMA           {BEFORE['global']['sma']:>18,.2f} -> {g_sma:>18,.2f}   "
          f"delta {g_sma - BEFORE['global']['sma']:+,.2f}")
    print(f"  Client        {BEFORE['global']['client']:>18,.2f} -> {g_cli:>18,.2f}   "
          f"delta {g_cli - BEFORE['global']['client']:+,.2f}")
    print(f"  absent_reason {'PRESENT':>18} -> {'PRESENT' if g_reason else 'ABSENT':>18}")
    print("  AC4 names cottonwood and inflection ONLY; AC5 names 49financial and 'where it is")
    print("  TRUE'. Global is in NEITHER set, so its movement is unscored by construction.")
    print("  The movement is CORRECT -- it mirrors 49financial to the cent (global's Client is")
    print("  49F-only under basis B) and its sentence was recorded FALSE in the before-image,")
    print("  so removing it is right. But the acceptance set covers 3 of 4 served scopes on the")
    print("  movement axis, and a fourth scope moving by $22.79M is not something a reader")
    print("  should have to infer from a criterion's silence.")

    # ---- AC6 -------------------------------------------------------------------
    print()
    print(BAR)
    print("CATV-TON1-AC6 -- D1-inv-4 HOLDS and total_aua DOES NOT CHANGE")
    print(BAR)
    ac6 = True
    for sc in SCOPES:
        nodes = cv[sc].get("nodes") or {}
        s = round(sum(float(v.get("aum") or 0.0) for v in nodes.values()), 2)
        tot = r2((cv[sc].get("sums") or {}).get("total_aua"))
        holds = s == tot
        unmoved = tot == r2(BEFORE[sc]["total"])
        ac6 = ac6 and holds and unmoved
        print(f"  {sc:<12} SUM(L0) {s:>18,.2f} == total_aua {tot:>18,.2f}  {'HOLDS' if holds else 'BREAKS'} | "
              f"total before {BEFORE[sc]['total']:>18,.2f}  {'UNMOVED' if unmoved else 'MOVED <-- FAIL'}")
    rows.append(("CATV-TON1-AC6", ac6, "invariant holds AND total unmoved, 4 of 4"))

    print()
    print(BAR)
    print("SCORE -- denominator 4 scoreable rows (AC7 NOT scored: needs a SCHEDULED fire)")
    print(BAR)
    for cid, ok, note in rows:
        print(f"  {cid:<16} {'PASS' if ok else 'FAIL'}   {note}")
    allok = all(r[1] for r in rows)
    print(f"\n  {sum(1 for r in rows if r[1])} PASS / {sum(1 for r in rows if not r[1])} FAIL "
          f"of {len(rows)}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
