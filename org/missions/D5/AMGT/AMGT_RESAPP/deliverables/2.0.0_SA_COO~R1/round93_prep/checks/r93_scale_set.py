"""AMGT_RESAPP round-93 PREP -- D1-S22: a point set whose figures are stated on different scales is held as a SET.

  PYTHONPATH=<repo root> python r93_scale_set.py            (no network, no AWS: synthetic excerpts)

`analyze._apply_point_verification` keeps a driver point when its value's digits sit inside the block that carries its own period label. It
never asks what scale the figure is stated on. Measured on the live SAP object (round 92): 2024 = 18,078 and 2023 = 13,745 are stated "million",
2025 = 21.05 is stated "billion": one series, one axis, units a factor of 1,000 apart. The rule: after verification, when the KEPT points'
figures carry more than one stated scale word (thousand, million, billion, trillion; whole word, within 12 characters after the figure's span),
the whole kept set is HELD, never a part of it. A point whose figure states no scale word (a table cell) has no scale and is not counted.

    M1 the SAP-shaped excerpt: 2024 and 2023 in millions, 2025 in billions: all three points are held, none kept, and the held reason names
       both scales.
    M2 control: the same two periods in millions only (2024 = 18,078, 2023 = 13,745): both kept.
    M3 control: figures with no scale word (a table row): all kept.
    M4 control: two points both stated in billions: both kept (one scale is not a mix).
    M5 control: ONE path: a single point stated in billions beside a bare table figure: both kept (a bare figure is not a second scale).
Verdict: R93 SCALE SET: YES|NO (exit 0|1). At the base (2026-10-11) M1 FAILs (all three are kept), M2-M5 PASS.
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
TABLE = "Year ended December 31,\n2023\nBacklog\n13745\n2024\nBacklog\n18078\n"
BILLIONS = ("Cloud backlog was EUR 18.08 billion in 2024. Cloud backlog was EUR 21.05 billion in 2025, up from the year before.")
MIXED_BARE = ("Cloud backlog was EUR 21.05 billion in 2025. Year ended December 31,\n2023\nBacklog\n13745\n")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def run(text, points):
    kept, held = analyze._apply_point_verification([dict(p) for p in points], text, [], anchor=0)
    return {k["period"]: k for k in kept}, {h["period"]: h for h in held}


def main():
    results = []
    kept, held = run(SAP, [{"period": "2025", "value": 21.05}, {"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}])
    reasons = " | ".join(str(h.get("reason")) for h in held.values()).lower()
    named = "million" in reasons and "billion" in reasons
    results.append(say(not kept and sorted(held) == ["2023", "2024", "2025"] and named,
                       "M1 the SAP-shaped excerpt: the whole set is held and the reason names both scales",
                       "kept %s, held %s, reasons name both scales: %s" % (sorted(kept), sorted(held), named)))
    kept, held = run(MILLIONS, [{"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}])
    results.append(say(sorted(kept) == ["2023", "2024"], "M2 control: two points both stated in millions are kept", "kept %s" % sorted(kept)))
    kept, held = run(TABLE, [{"period": "2024", "value": 18078}, {"period": "2023", "value": 13745}])
    results.append(say(sorted(kept) == ["2023", "2024"], "M3 control: figures with no scale word are kept", "kept %s" % sorted(kept)))
    kept, held = run(BILLIONS, [{"period": "2025", "value": 21.05}, {"period": "2024", "value": 18.08}])
    results.append(say(sorted(kept) == ["2024", "2025"], "M4 control: two points both stated in billions are kept", "kept %s" % sorted(kept)))
    kept, held = run(MIXED_BARE, [{"period": "2025", "value": 21.05}, {"period": "2023", "value": 13745}])
    results.append(say(sorted(kept) == ["2023", "2025"], "M5 control: a bare figure beside a billions figure is not a second scale", "kept %s" % sorted(kept)))
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R93 SCALE SET: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
