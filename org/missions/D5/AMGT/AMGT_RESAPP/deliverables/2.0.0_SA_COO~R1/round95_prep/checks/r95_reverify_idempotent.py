"""AMGT_RESAPP round-95 PREP -- the verifier locates a point by its `stated_value` (row D1-S24, CTO round-94 analysis item 1).

  PYTHONPATH=<repo root> python r95_reverify_idempotent.py        (no network, no AWS: the stored object and its source are in-memory fixtures)

Round 94's `AMGT-ff-3` stores a rescaled point as `value` = the shown figure on the unit's scale (13.745) with `stated_value` (13745), `stated_scale` ('million') and
`rescaled_to` ('billion') beside it. `analyze.reverify_stored_thesis_driver` builds its raw claim from each stored point's `value` only, so the passage never prints
13.745 as a whole number and a SECOND verification of an already rescaled object keeps 1 of 3 points (SAP's object, row D1-S24). The rule: a stored point (in `points`
AND in `held_uncited`) is located by its `stated_value` when it carries one, else by its `value`; nothing else changes.

    I1 the object a fresh run stored (the SAP-shaped excerpt, unit 'EUR billions and % growth at constant currencies', three rescaled points) re-verifies to the SAME
       three points: same periods, same `value`, `stated_value`, `stated_scale`, `rescaled_to`, and none held.
    I2 a second re-verification of that result is byte-equal to the first (idempotent over its own output), and both keep the three.
    I3 a stored point whose figure no excerpt prints (2022 = 99999) beside the three is HELD with a reason, and the three are kept (the negative arm still holds).
    I4 an object whose three points sit in `held_uncited` WITH their `stated_value` is re-derived: the three are kept (the held list is reconsidered by its stated figure).
    I5 control: an unrescaled single-scale object (two million-stated figures, unit text 'EUR billions') re-verifies to the same two points with no rescale field, and
       a second run is byte-equal.
    I6 control: a raw object a fresh run held whole (the SAP excerpt, NO unit text) re-verifies to the same three held points and none kept.
Verdict: R95 REVERIFY IDEMPOTENT: YES|NO (exit 0|1). At the base (2026-10-11): I1, I2, I3, I4 FAIL; I5, I6 PASS.
"""
import copy
import json
import sys

from lib.research.filings import analyze
from lib.research.harvest import filings as hf
from lib.research.harvest import store as hstore

SAP = ("The current cloud backlog increased EUR 2.97 billion, or 16%, to EUR 21.05 billion in 2025 (2024: EUR 18.08 billion). "
       "Our total cloud backlog increased 22% from EUR 63.29 billion in 2024 to EUR 77.29 billion in 2025. "
       + "Operating commentary continues. " * 40 +
       "The current cloud backlog increased EUR 4,333 million, or 32%, to EUR 18,078 million in 2024 (2023: EUR 13,745 million). "
       "Our total cloud backlog increased 43% from EUR 44.25 billion in 2023 to EUR 63.29 billion in 2024.")
MILLIONS = ("The current cloud backlog increased EUR 4,333 million, or 32%, to EUR 18,078 million in 2024 (2023: EUR 13,745 million). "
            "Revenue for 2023 was reported in the segment note.")
UNIT = "EUR billions and % growth at constant currencies"
THREE = [{"period": "2025", "value": 21.05}, {"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}]
KEY, ACC = "SAP_GY_Equity", "000000000026000001"


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


class _Body:
    def __init__(self, doc):
        self._doc = doc

    def read(self):
        return json.dumps(self._doc).encode("utf-8")


class _Client:
    """Just enough of the S3 client: the one analysis object `reverify_stored_thesis_driver` reads."""

    def __init__(self, doc):
        self._doc = doc

    def get_object(self, Bucket=None, Key=None):  # noqa: N803 -- boto3's own parameter names
        return {"Body": _Body(self._doc)}


def reverify(excerpt, driver):
    """`reverify_stored_thesis_driver` (dry run) over an in-memory stored object and source; returns the driver it would write."""
    doc = {"thesis_driver": copy.deepcopy(driver), "passage_map": [], "denominators": {"passages": 0}}
    saved = (hstore.silver_latest, hf.source_object_from_row)
    hstore.silver_latest = lambda vendor, table, keys, client=None: {(KEY, ACC): {"security_key": KEY, "accession": ACC}} if vendor == "sec" else {}
    hf.source_object_from_row = lambda row: {"excerpt": {"text": excerpt}}
    try:
        out, _key, _receipt = analyze.reverify_stored_thesis_driver(KEY, ACC, client=_Client(doc), dry_run=True)
    finally:
        hstore.silver_latest, hf.source_object_from_row = saved
    return out["thesis_driver"]


def fresh(excerpt, unit):
    """What a fresh run stores for the claimed points: the kept and held entries of `_apply_point_verification`."""
    kept, held = analyze._apply_point_verification([dict(p) for p in THREE], excerpt, [], anchor=0, unit_text=unit)
    return {"points": kept, "held_uncited": held, "unit": unit, "source_passage_id": None}


def by_period(entries):
    return {e["period"]: e for e in entries}


def main():
    res = []
    stored = fresh(SAP, UNIT)
    shown = {p["period"]: round(float(p["value"]), 6) for p in stored["points"]}
    if shown != {"2025": 21.05, "2024": 18.078, "2023": 13.745}:
        print("FAIL precondition: a fresh run does not store the rescaled SAP set (%s): ff-3 is not in this tree" % shown)
        print("R95 REVERIFY IDEMPOTENT: NO")
        return 1
    once = reverify(SAP, stored)
    k1 = by_period(once["points"])
    same = (sorted(k1) == ["2023", "2024", "2025"] and not once["held_uncited"]
            and all(json.dumps(k1[p], sort_keys=True) == json.dumps(by_period(stored["points"])[p], sort_keys=True) for p in k1))
    res.append(say(same, "I1 an already rescaled object re-verifies to the same three points",
                   "kept %s held %s" % (sorted(k1), sorted(h["period"] for h in once["held_uncited"]))))
    twice = reverify(SAP, once)
    res.append(say(len(once["points"]) == 3 and json.dumps(twice, sort_keys=True) == json.dumps(once, sort_keys=True),
                   "I2 a second re-verification is byte-equal to the first, and both keep three",
                   "kept %d then %d" % (len(once["points"]), len(twice["points"]))))
    extra = copy.deepcopy(stored)
    extra["points"].append({"period": "2022", "value": 99999})
    out = reverify(SAP, extra)
    kept, held = by_period(out["points"]), by_period(out["held_uncited"])
    res.append(say(sorted(kept) == ["2023", "2024", "2025"] and "2022" in held and held["2022"].get("reason"),
                   "I3 a figure no excerpt prints is held with a reason, the three are kept",
                   "kept %s held %s" % (sorted(kept), sorted(held))))
    heldobj = {"points": [], "held_uncited": copy.deepcopy(stored["points"]), "unit": UNIT, "source_passage_id": None}
    out = reverify(SAP, heldobj)
    res.append(say(sorted(by_period(out["points"])) == ["2023", "2024", "2025"] and not out["held_uncited"],
                   "I4 held points carrying their stated figure are reconsidered and kept",
                   "kept %s held %d" % (sorted(by_period(out["points"])), len(out["held_uncited"]))))
    two = [{"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}]
    base_kept, base_held = analyze._apply_point_verification([dict(p) for p in two], MILLIONS, [], anchor=0, unit_text="EUR billions")
    single = {"points": base_kept, "held_uncited": base_held, "unit": "EUR billions", "source_passage_id": None}
    o1 = reverify(MILLIONS, single)
    o2 = reverify(MILLIONS, o1)
    plain = all("rescaled_to" not in p for p in o1["points"])
    res.append(say(len(o1["points"]) == 2 and plain and json.dumps(o1, sort_keys=True) == json.dumps(o2, sort_keys=True)
                   and [p["value"] for p in o1["points"]] == [p["value"] for p in base_kept],
                   "I5 control: an unrescaled single-scale object re-verifies to the same points, idempotently",
                   "kept %d plain %s" % (len(o1["points"]), plain)))
    rawheld = fresh(SAP, None)
    o = reverify(SAP, rawheld)
    res.append(say(not o["points"] and sorted(h["period"] for h in o["held_uncited"]) == ["2023", "2024", "2025"],
                   "I6 control: a set a fresh run held whole (no unit text) is held again",
                   "kept %d held %s" % (len(o["points"]), sorted(h["period"] for h in o["held_uncited"]))))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R95 REVERIFY IDEMPOTENT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
