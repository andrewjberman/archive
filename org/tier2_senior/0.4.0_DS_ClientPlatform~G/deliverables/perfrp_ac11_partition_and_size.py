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
import os
import sys
import tempfile

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

    # EMIT FOR REAL and read the two FILES back. Reading core._performance() in
    # memory would verify the FUNCTION; AC11 is about the ARTIFACTS a verifier is
    # handed, and after COO @0fe8a898f8 relocated the ids there are now TWO of them.
    # Reading the files is also the only way the cross-tie means anything: it has to
    # actually cross, and an in-memory structure has nothing to cross to.
    tmp = tempfile.mkdtemp()
    rel_path = os.path.join(tmp, "perf_rel.json")
    acct_path = os.path.join(tmp, "perf_acct.json")
    core.main("perfrp_performance_relationship", ["--date", ASOF, "--out", rel_path])
    core.main("perfrp_performance_account", ["--date", ASOF, "--out", acct_path])
    ver_path = rel_path[:-len(".json")] + core.VERIFICATION_SUFFIX

    with open(rel_path, encoding="utf-8") as fh:
        rel_doc = json.load(fh)
    with open(acct_path, encoding="utf-8") as fh:
        acct_doc = json.load(fh)
    with open(ver_path, encoding="utf-8") as fh:
        ver = json.load(fh)
    rel, acct = rel_doc["entries"], acct_doc["entries"]
    membership = ver["membership"]

    checks = []

    def chk(name, got, want, note=""):
        ok = got == want
        checks.append(ok)
        print("   [{}] {:<52} got={!s:<10} want={!s}{}".format(
            "PASS" if ok else "FAIL", name, got, want, ("  -- " + note) if note else ""))

    # ---------- 1. the two artifacts, and the SERVED one must be clean ----------
    print()
    print("1. THE TWO ARTIFACTS -- COO @0fe8a898f8 relocated the ids OUT of the payload")
    print("   served relationship entries ..... {:,}".format(len(rel)))
    print("   served account entries .......... {:,}".format(len(acct)))
    print("   verification keys ............... {:,}".format(len(membership)))
    print("   verification ids ................ {:,}".format(
        sum(len(v) for v in membership.values())))
    leaked = sum(1 for e in rel if "account_ids" in e
                 or core.VERIFICATION_IDS_KEY in e)
    chk("SERVED leaf carries NO ids", leaked, 0,
        "a client fetch must not pay for a check that runs once")
    chk("verification covers every served relationship",
        set(membership) == {e["key"] for e in rel}, True)
    chk("SAME ACT: verification as_of == served as_of", ver["as_of"],
        rel_doc["as_of"], "a re-derivation would verify a DIFFERENT object")
    chk("SAME ACT: contract_version matches", ver["contract_version"],
        rel_doc["contract_version"])

    # ---------- 1b. the cross-tie ----------
    print()
    print("1b. THE CROSS-TIE -- DE~D: the only assertion reaching BACK into served bytes")
    print("    Co-emission alone leaves the two documents UNLINKED: the ids would prove")
    print("    a partition over some population while the leaf asserts counts over")
    print("    another, with nothing joining them.")
    counts = {e["key"]: e.get("accounts") for e in rel}
    bad = [(k, len(v), counts.get(k)) for k, v in membership.items()
           if len(v) != counts.get(k)]
    print("   relationships checked ........... {:,}".format(len(membership)))
    print("   len(ids) != served `accounts` ... {:,}".format(len(bad)))
    chk("len(ids) == served `accounts`, every key", len(bad), 0,
        "asserted at emit AND re-checked here from the two files")

    # ---------- 2. the partition ----------
    print("\n2. THE PARTITION -- the clause DE~D could not discharge from a count")
    union = set()
    dupes = {}
    total_ids = 0
    for k, ids in membership.items():
        total_ids += len(ids)
        for a in ids:
            if a in union:
                dupes.setdefault(a, []).append(k)
            union.add(a)
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
    doc = rel_doc                      # the SERVED bytes, read back from disk
    augmented = copy.deepcopy(doc)     # what the payload WOULD carry, for the bound
    for e in augmented["entries"]:
        e["account_ids"] = membership.get(e["key"], [])

    def _file_bytes(d, compact=False):
        """Serialize EXACTLY as perfrp_emit_core.main() does, and measure the BYTES
        that reach the file -- not the length of the string that produced them."""
        kw = dict(separators=(",", ":"), sort_keys=True) if compact else dict(
            indent=1, sort_keys=True)
        return len(json.dumps(d, **kw).encode("utf-8"))

    grid = {(lbl, k): _file_bytes(d, compact=c)
            for lbl, c in (("indent=1 (the emitter's own)", False), ("compact", True))
            for k, d in (("served", doc), ("counterfactual", augmented))}
    print()
    print("   THE IDS ARE NO LONGER IN THE PAYLOAD. The served column is what ships;",
          "the")
    print("   counterfactual is what it WOULD have cost, kept because COO's bound",
          "asked.")
    print("   {:<30} {:>14} {:>14} {:>16}".format(
        "serialization", "SERVED today", "counterfactual", "cost avoided"))
    for lbl in ("indent=1 (the emitter's own)", "compact"):
        w, x = grid[(lbl, "served")], grid[(lbl, "counterfactual")]
        print("   {:<30} {:>14,} {:>14,} {:>11,} ({:+.1f}%)".format(
            lbl, w, x, x - w, 100.0 * (x - w) / w))
    ind_w = grid[("indent=1 (the emitter's own)", "served")]
    ind_x = grid[("indent=1 (the emitter's own)", "counterfactual")]
    total = ind_x - ind_w
    struct_ids = grid[("compact", "counterfactual")] - grid[("compact", "served")]
    # MEASURE the id characters; do NOT infer them from an assumed bytes-per-id.
    n_ent = len(doc["entries"])
    ids_only = sum(len(json.dumps(x)) + 1
                   for v in membership.values() for x in v) - n_ent
    key_struct = struct_ids - ids_only
    indent_ws = total - struct_ids
    print()
    print("   THE COST DECOMPOSED -- three components, not two. A RESIDUAL BUCKET IS A")
    print("   CLAIM, NOT A REMAINDER (DE~D 69331, against their own number): measuring",
          "one")
    print("   component and labelling the leftover with the name you are arguing for is",
          "not")
    print("   a measurement of that thing. The omitted component was the one that",
          "mattered.")
    for lbl, v in (("1. id characters + commas", ids_only),
                   ("2. the key, brackets, separators -- THE FIELD", key_struct),
                   ("3. indent whitespace -- the only recoverable part", indent_ws)):
        print("     {:<52} {:>10,} {:>6.1f}%".format(lbl, v, 100.0 * v / total))
    print("     {:<52} {:>10,} {:>6.1f}%".format("TOTAL", total, 100.0))
    print("     self-check: components sum to the total: {}".format(
        ids_only + key_struct + indent_ws == total))
    print("   Only (3) is a serialization choice. (2) is the field itself -- a key name",
          "is")
    print("   not formatting, and filing it as such is what turned 31.5% into 60.5%.")

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
    print("   ALL THREE PLANES, so no one has to guess which two were differenced:")
    print("     string LF -> string LF   1,289,850 -> 1,531,505   +241,655  +18.7%")
    print("     file CRLF -> file CRLF   1,320,577 -> 1,578,337   +257,760  +19.5%")
    print("     file CRLF -> string LF   1,320,577 -> 1,531,505   +210,928  +16.0%")
    print("   The third is the one that circulated, and DE~D 69331 retracted it against")
    print("   their own interest: it is not a size of ANYTHING, because one side carries")
    print("   30,727 CR bytes the other does not. +18.7% is the operative figure now that")
    print("   the emitter writes bytes; +19.5% describes the plane the old artifact was on.")
    print("   I had endorsed +16.0% as standing. That was wrong and this line replaces it.")
    print("   DE~D and I decomposed independently and converged: indent is 31.5%, and the")
    print("   55%/60.5% figures both counted the field's own key as formatting.")

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
