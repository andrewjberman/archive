#!/usr/bin/env python
"""KEYFILL-DTX ADDENDUM -- discharge the LIVE delta prose on this lane's 4 affected cards.

WHAT IS LIVE, AND WHY IT IS MINE. The v2->v3 migrator wrote, on exactly four of this lane's cards:

    "v3 delta pass: key_expression ABSENT on this card (not yet declared by the carding lane);
     row basis lowered from measured to the floor."

That was TRUE when written. TO-KEYFILL-DTX then filled key_expression on all four, so the sentence
is now false about the tree it sits in -- an accurate reading whose vintage outlived it. The
undischarged sentence is the finding; the lowered scalar is the same event seen from a second field.

RETAIN, DO NOT STRIP (3.0.0_SA_CVO~X 213420Z: retention preferred for provenance). Stripping would
erase the record of WHY the floor was ever taken down, which is the one thing a later reader needs
to evaluate the restoration. The marker is appended in the SAME field, so the claim and its
discharge cannot be separated by a later reader looking at only one of them.

⛔ THE SCALAR IS NOT TOUCHED HERE. trust.key.basis edits are HELD at every lane (issuer 213704Z act
(1), 4.0.0_SA_CRO~X 214157Z) pending the confirmed floor predicate, and this seat's replay under
that predicate reports 4 of 18 rather than the 15 on the boundary sheet (79308). The structural diff
of this addendum is confined to /trust/key/evidence and nothing else.

THE WRITER IS PROVED BEFORE IT WRITES. `round_trip_proof()` reads every card and re-serialises it
UNCHANGED; if a single byte differs the run refuses. That is what makes the post-diff attributable
to this edit rather than to re-serialisation -- and it discriminates: measured on this set,
ensure_ascii=True round-trips 1 of 18 and sort_keys 0 of 18, while the writer used here is 18 of 18.
"""
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LANE = "0.4.0_DT_ClientPlatform~X"
MARKER = "DISCHARGED-KEYFILL-DTX"
LIVE_TOKEN = "key_expression ABSENT on this card"


def serialise(obj):
    """The ONE writer. Proved byte-identical on an unchanged round trip before any write."""
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def cards():
    out = []
    for f in sorted(glob.glob(os.path.join(
            ROOT, "org", "tier2_senior", "0.4.0_DT_ClientPlatform", "deliverables",
            "D11_CARDS_*", "*.json"))):
        with open(f, "rb") as fh:
            raw = fh.read()
        d = json.loads(raw.decode("utf-8"))
        if d.get("carded_by") == LANE:
            out.append((f, raw, d))
    return out


def round_trip_proof(rows):
    bad = [f for f, raw, d in rows if serialise(d).encode("utf-8") != raw]
    print("WRITER ROUND-TRIP PROOF: byte-identical %d of %d" % (len(rows) - len(bad), len(rows)))
    for f in bad[:5]:
        print("   NOT IDENTICAL %s" % os.path.basename(f))
    return not bad


def main():
    apply = "--apply" in sys.argv
    rows = cards()
    if not rows:
        print("FAIL: zero cards located -- an addendum over an empty set is vacuous")
        return 1
    if not round_trip_proof(rows):
        print("REFUSING: the writer is not byte-identical on an unchanged round trip, so any diff "
              "below would mix re-serialisation into the edit and could not be attributed to it.")
        return 1

    live, already, changed = [], 0, []
    for f, raw, d in rows:
        key = d.get("trust", {}).get("key", {})
        ev = key.get("evidence") or ""
        if LIVE_TOKEN not in ev:
            continue
        if MARKER in ev:
            already += 1
            continue
        live.append((f, raw, d, key, ev))

    print("LIVE delta sentences on this lane: %d of %d cards (already discharged: %d)"
          % (len(live), len(rows), already))

    for f, raw, d, key, ev in live:
        kb = (key.get("basis_by_field") or {}).get("key_expression")
        note = (" || %s 2026-08-28: the sentence above is DISCHARGED, retained for provenance. "
                "key_expression is no longer ABSENT on this card -- TO-KEYFILL-DTX declared it and "
                "recorded basis_by_field.key_expression=%s at commit 8de6cabc12, so the condition "
                "that justified lowering the row basis no longer holds. The scalar itself is NOT "
                "changed here: trust.key.basis edits are held at every lane pending the confirmed "
                "floor predicate (issuer 213704Z), under which this lane replays 4 of 18."
                % (MARKER, kb))
        key["evidence"] = ev + note
        post = serialise(d).encode("utf-8")
        changed.append((f, hashlib.sha256(raw).hexdigest(), hashlib.sha256(post).hexdigest()))
        if apply:
            with open(f, "wb") as fh:
                fh.write(post)

    print()
    print("PRE / POST digests, per card:")
    for f, a, b in changed:
        print("   %-10s %s -> %s" % (os.path.basename(f).split("__")[0][-9:], a[:16], b[:16]))
    print()
    print("CENSUS: lane cards %d | live discharged %d | already %d | untouched %d"
          % (len(rows), len(changed), already, len(rows) - len(changed) - already))
    print("STRUCTURAL DIFF confined to: /trust/key/evidence  (no scalar, no other field)")
    print("mode: %s" % ("APPLIED" if apply else "DRY RUN (pass --apply)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
