"""AC11 second clause -- NO DOUBLE COUNT EXPRESSIBLE -- discharged, plus the size bound.

TWO RULINGS, ONE RUN, and they were made an hour apart for different reasons.

1. CHILD IDS, COO @5142c6a711. 0.4.0_DE_ClientPlatform~D found that their own AC11
   clause was undischargeable by anyone, including them: the relationship leaf carried
   a child COUNT and not child IDS, and -- their sentence, which is the whole finding --
   "A DOUBLE-COUNT PAIRED WITH AN OMISSION YIELDS THE SAME 7,335." Necessary, not
   sufficient. 0.7.0_AE_CloudOps~G reproduced the limb at their own seat before
   endorsing it, and recorded that it falsified a sentence of their own rather than
   merely filling a gap they had left.
   With `account_ids` on each entry the partition becomes CHECKABLE at the render
   boundary, which is section 2 below.

2. THE SIZE BOUND, COO's map-form ruling, connected to this change by AE~G at 69136:
   "an additive field is exactly the kind of change that does not feel like it triggers
   a size bound." The bound requires the emitted object size per family MEASURED AND
   PRINTED before it is wired, with a breach returning to COO rather than being
   adjudicated here. Section 3. I measure the delta rather than argue about it -- AE~G
   called the growth "materially larger" and gave the baseline (1,320,577 B) precisely
   so the decision would carry a number instead of an adjective.

WHY THE PARTITION CHECK SURVIVES A 100% NULL CENSUS. Every window_return on the live
frontier is NOT_COMPUTED. AE~G's own correction is the reason this still works:
A COUNT IS NOT A RETURN, and neither is an ID -- value-blindness does not imply
structure-blindness. This check reads MEMBERSHIP, so the null values are irrelevant to
it.

WHAT COVERAGE AND DISJOINTNESS CATCH, SEPARATELY -- they are two failures, not one:
  UNION == account leaf key set   catches an OMISSION (an account in no relationship)
                                   and a PHANTOM (an id belonging to no account)
  PAIRWISE DISJOINT               catches a DOUBLE-COUNT (one account under two parents)
A sum of counts passes both of these while failing either, which is exactly DE~D's point.

EVIDENCE VINTAGE: live 49F plane read 2026-08-25; subject modules at the committing ref.
"""
from __future__ import annotations

import copy
import json
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import perfrp_emit_core as core  # noqa: E402  the SUBJECT -- imported, never re-typed

ASOF = "2026-08-21"
FAMILIES_WITH_LEVELS = ("perfrp_performance", "perfrp_activity", "perfrp_allocation")


def main() -> int:
    print("AC11 -- PARTITION (second clause) + EMITTED SIZE BOUND")
    print("child-IDs ruling COO @5142c6a711 (raised DE~D 69112, reproduced AE~G 69120);"
          " size bound connected by AE~G 69136")
    print("as-of %s" % ASOF)
    print("=" * 108)

    rel = core._performance(ASOF, "relationship")
    acct = core._performance(ASOF, "account")

    checks = []

    def chk(name, got, want, note=""):
        ok = got == want
        checks.append(ok)
        print("   [{}] {:<52} got={!s:<10} want={!s}{}".format(
            "PASS" if ok else "FAIL", name, got, want, ("  -- " + note) if note else ""))

    # ---------- 1. the field is actually there, and populated ----------
    print("\n1. THE FIELD ITSELF (an absent or empty field would make every check below vacuous)")
    have = [e for e in rel if e.get("account_ids")]
    print("   relationship entries ............ {:,}".format(len(rel)))
    print("   carrying a NON-EMPTY account_ids  {:,}".format(len(have)))
    print("   account entries ................. {:,}".format(len(acct)))
    chk("every relationship entry carries account_ids", len(have), len(rel),
        "None/empty would union to nothing and pass disjointness silently")

    # ---------- 2. the partition ----------
    print("\n2. THE PARTITION -- the clause DE~D could not discharge from a count")
    union = set()
    dupes = {}
    total_ids = 0
    for e in rel:
        ids = e.get("account_ids") or []
        total_ids += len(ids)
        for a in ids:
            if a in union:
                dupes.setdefault(a, []).append(e["key"])
            union.add(a)
    acct_keys = {e["key"] for e in acct}
    sum_counts = sum(int(e.get("accounts") or 0) for e in rel)

    print("   sum of child `accounts`   {:>10,}   <- the NECESSARY-not-sufficient limb".format(sum_counts))
    print("   ids actually emitted      {:>10,}".format(total_ids))
    print("   DISTINCT ids (the union)  {:>10,}".format(len(union)))
    print("   account leaf key count    {:>10,}".format(len(acct_keys)))
    missing = acct_keys - union
    phantom = union - acct_keys
    print("   in account leaf, in NO relationship  {:>6,}".format(len(missing)))
    print("   claimed by a relationship, NOT an account key {:>6,}".format(len(phantom)))
    print("   accounts appearing under 2+ relationships     {:>6,}".format(len(dupes)))

    chk("COVERAGE: union == account leaf key set", union == acct_keys, True,
        "catches an OMISSION or a PHANTOM id")
    chk("DISJOINT: no account under two relationships", len(dupes), 0,
        "catches a DOUBLE-COUNT; a sum of counts cannot")
    chk("ids emitted == distinct ids", total_ids, len(union),
        "restates disjointness from the other side")
    chk("sum of counts still ties (DE~D's original limb)", sum_counts, len(acct_keys),
        "the necessary limb, unchanged and still true")
    if dupes:
        for a, parents in list(dupes.items())[:5]:
            print("     DUPLICATE {} under {}".format(a, parents))

    # ---------- 3. the size bound ----------
    print()
    print("3. EMITTED SIZE (COO's map-form bound; a breach routes to COO, NOT decided here)")
    print("   EVERY number below is FILE BYTES as main() writes them. That distinction is")
    print("   the whole of section 4 and it is why the first version of this section was wrong.")
    doc = core.build("perfrp_performance_relationship", ASOF)
    stripped = copy.deepcopy(doc)
    for e in stripped["entries"]:
        e.pop("account_ids", None)

    def _file_bytes(d, compact=False):
        """Serialize EXACTLY as perfrp_emit_core.main() does, and measure the BYTES
        that reach the file -- not the length of the string that produced them."""
        kw = dict(separators=(",", ":"), sort_keys=True) if compact else dict(
            indent=1, sort_keys=True)
        return len(json.dumps(d, **kw).encode("utf-8"))

    grid = {(lbl, k): _file_bytes(d, compact=c)
            for lbl, c in (("indent=1 (the emitter's own)", False), ("compact", True))
            for k, d in (("without", stripped), ("with", doc))}
    print()
    print("   {:<30} {:>14} {:>14} {:>16}".format(
        "serialization", "without ids", "with ids", "cost of the field"))
    for lbl in ("indent=1 (the emitter's own)", "compact"):
        w, x = grid[(lbl, "without")], grid[(lbl, "with")]
        print("   {:<30} {:>14,} {:>14,} {:>11,} ({:+.1f}%)".format(lbl, w, x, x - w,
                                                                   100.0 * (x - w) / w))
    ind_w, ind_x = grid[("indent=1 (the emitter's own)", "without")], grid[
        ("indent=1 (the emitter's own)", "with")]
    content = grid[("compact", "with")] - grid[("compact", "without")]
    print("   ID CONTENT alone (the compact delta) {:>10,} B".format(content))
    print("   FORMAT share of the indent=1 delta   {:>10.0f}%".format(
        100.0 * (1 - content / float(ind_x - ind_w))))

    print()
    print("4. THE BASELINE DISAGREEMENT, RESOLVED -- and it was a defect, not a rounding")
    print("   DE~D 69179 and AE~G 69136 both baselined at 1,320,577 B. I measured 1,289,850.")
    print("   Both were right about different objects: 1,320,577 is the FILE, 1,289,850 is")
    print("   the STRING, and the gap is 30,727 -- EXACTLY the newline count, because")
    print("   Path.write_text applied universal-newline translation and wrote CRLF.")
    print("   THE SIZE WAS THE SYMPTOM. d_publisher_port hashes read_bytes() into")
    print("   body_sha256 and D5's unchanged-skip compares it to the served object, so")
    print("   the same payload emitted on Windows and on Linux HASHED DIFFERENTLY --")
    print("   the idempotency guard would report a real diff on every platform switch.")
    print("   Fixed in the same commit: main() now write_bytes(). Emitted CR bytes = 0.")
    print("   DE~D's HEADLINE was right for a reason neither of us had: they differenced")
    print("   the old FILE against the new STRING, and removing CRLF made the new string")
    print("   BE the new file. Their +210,928 B / +16.0% is the true served-bytes delta.")
    print("   Their 55%-is-indent SPLIT is the half that does not survive: measured")
    print("   like-for-like the format share is {:.0f}%, not 55%.".format(
        100.0 * (1 - content / float(ind_x - ind_w))))

    npass = sum(1 for c in checks if c)
    print("\n" + "=" * 108)
    print("DENOMINATOR: {}/{} checks PASS over {:,} relationship entries and {:,} account entries"
          .format(npass, len(checks), len(rel), len(acct)))
    print("AC11 clause 2 (NO DOUBLE COUNT EXPRESSIBLE): {}".format(
        "DISCHARGEABLE and DISCHARGED" if npass == len(checks) else "NOT DISCHARGED -- see FAILs"))
    print("STILL OWED, unchanged by this run: the wire-time re-run of the VALUE leg against")
    print("  real returns (AE~G 69085). This run reads MEMBERSHIP only.")
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
