"""AMGT_RESAPP round-94 PREP -- the rescale rule: a point set stated on different scales is SHOWN on the scale its series unit names, not held.

  PYTHONPATH=<repo root> python r94_rescale.py            (no network, no AWS: synthetic excerpts)

Round 93's `AMGT-ss-2` holds a kept point set whole when its figures are stated on more than one scale word (thousand, million, billion, trillion). SAP's
2023-2025 current cloud backlog (13,745 and 18,078 "million", 21.05 "billion") is held, and SAP's driver is empty. The series' own unit text says what
scale the chart is in ("EUR billions and % growth at constant currencies"); the scale words have fixed factors (a thousand, a million, a billion, a
trillion), so each figure can be shown on the unit's scale with its stated value kept beside it. The rule:

    `_apply_point_verification(points, excerpt_text, passage_map, anchor=0, unit_text=None)`: when the verified points carry MORE THAN ONE scale word and
    `unit_text` names EXACTLY ONE scale word (whole word, singular or plural, case-insensitive) that is one of the words the points carry, and EVERY
    verified point carries a scale word, each verified point's `value` becomes `stated value x factor(stated word) / factor(unit word)`, rounded to 9
    decimals, and the kept entry carries `stated_value`, `stated_scale` and `rescaled_to`. In every other mixed case the whole set is held (ss-2).

    R1 the SAP-shaped excerpt with the unit text 'EUR billions and % growth at constant currencies': all three points kept at 13.745, 18.078 and 21.05, each
       with its stated value and scale, and spans retained.
    R2 control: the same excerpt with no unit text is held whole, the reason naming both scales (ss-2's behaviour).
    R3 control: a unit text whose one scale word is NOT among the points' scales ('EUR thousands') holds the set whole.
    R4 control: a unit text naming two scale words ('EUR millions or billions') holds the set whole.
    R5 control: all points stated in millions, unit text 'EUR billions': unchanged (one stated scale is not a mix): values as stated, no rescale fields.
    R6 control: a bare table figure beside a billions figure with a unit text: unchanged from ss-2 (a bare figure is not a second scale; nothing is rescaled).
    R7 control: a mixed set with a bare figure among scale-worded ones is held whole even with a matching unit text.
Verdict: R94 RESCALE: YES|NO (exit 0|1). At the base (2026-10-11) the function takes no `unit_text` (the call falls back to no unit): R1 FAILs, R2-R7 PASS
(R3, R4 and R7 are held whole as ss-2 holds them; R5 and R6 are unchanged).
"""
import sys

from lib.research.filings import analyze

SAP = ("The current cloud backlog increased EUR 2.97 billion, or 16%, to EUR 21.05 billion in 2025 (2024: EUR 18.08 billion). "
       "Our total cloud backlog increased 22% from EUR 63.29 billion in 2024 to EUR 77.29 billion in 2025. "
       + "Operating commentary continues. " * 40 +
       "The current cloud backlog increased EUR 4,333 million, or 32%, to EUR 18,078 million in 2024 (2023: EUR 13,745 million). "
       "Our total cloud backlog increased 43% from EUR 44.25 billion in 2023 to EUR 63.29 billion in 2024.")
MILLIONS = ("The current cloud backlog increased EUR 4,333 million, or 32%, to EUR 18,078 million in 2024 (2023: EUR 13,745 million). "
            "Revenue for 2023 was reported in the segment note.")
BARE_MIX = "Cloud backlog was EUR 21.05 billion in 2025. Year ended December 31,\n2023\nBacklog\n13745\n"
THREE = [{"period": "2025", "value": 21.05}, {"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}]
UNIT = "EUR billions and % growth at constant currencies"


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def run(text, points, unit=None):
    try:
        kept, held = analyze._apply_point_verification([dict(p) for p in points], text, [], anchor=0, unit_text=unit)
    except TypeError:
        kept, held = analyze._apply_point_verification([dict(p) for p in points], text, [], anchor=0)
    return {k["period"]: k for k in kept}, {h["period"]: h for h in held}


def main():
    res = []
    kept, held = run(SAP, THREE, UNIT)
    want = {"2025": 21.05, "2024": 18.078, "2023": 13.745}
    got = {p: round(float(kept[p]["value"]), 6) for p in kept}
    fields = all(k.get("stated_scale") and k.get("stated_value") is not None and k.get("rescaled_to") == "billion" and k.get("span") for k in kept.values())
    res.append(say(got == want and fields and not held, "R1 the SAP-shaped set is shown on the unit's scale with its stated values kept",
                   "values %s, fields ok %s, held %s" % (got, fields, sorted(held))))
    kept, held = run(SAP, THREE, None)
    reasons = " | ".join(str(h.get("reason")) for h in held.values()).lower()
    res.append(say(not kept and sorted(held) == ["2023", "2024", "2025"] and "million" in reasons and "billion" in reasons,
                   "R2 control: no unit text holds the set whole, the reason naming both scales"))
    kept, held = run(SAP, THREE, "EUR thousands")
    res.append(say(not kept and len(held) == 3, "R3 control: a unit scale the points do not carry holds the set whole", "kept %s" % sorted(kept)))
    kept, held = run(SAP, THREE, "EUR millions or billions")
    res.append(say(not kept and len(held) == 3, "R4 control: a unit naming two scales holds the set whole", "kept %s" % sorted(kept)))
    kept, held = run(MILLIONS, [{"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}], UNIT)
    res.append(say(sorted(kept) == ["2023", "2024"] and kept["2024"]["value"] == 18078 and "rescaled_to" not in kept["2024"],
                   "R5 control: one stated scale is unchanged", "kept %s" % {p: kept[p]["value"] for p in kept}))
    kept, held = run(BARE_MIX, [{"period": "2025", "value": 21.05}, {"period": "2023", "value": 13745}], UNIT)
    res.append(say(sorted(kept) == ["2023", "2025"] and kept["2025"]["value"] == 21.05 and "rescaled_to" not in kept["2025"],
                   "R6 control: a bare figure beside one scale word is unchanged (not a mix)", "kept %s" % {p: kept[p]["value"] for p in kept}))
    mixed_bare = SAP + "\nYear ended December 31,\n2022\nBacklog\n9000\n"
    kept, held = run(mixed_bare, THREE + [{"period": "2022", "value": 9000}], UNIT)
    res.append(say(not kept and len(held) == 4, "R7 control: a bare figure inside a mixed set holds it whole", "kept %s" % sorted(kept)))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R94 RESCALE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
