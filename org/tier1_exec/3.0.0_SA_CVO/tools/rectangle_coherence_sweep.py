# -*- coding: utf-8 -*-
"""rectangle_coherence_sweep -- the instrument whose ABSENCE cost me the W4a plant.

WHY THIS EXISTS, mechanism first.

On OPAL_ANALYST.W4a I missed a planted cell: sscn.02/consumer_set said "Fires on page
load" while its structural twin sscn.03/consumer_set said "TAB-GATED. Does NOT fire on
page load." Two entities on ONE mechanism (the same conditional render) cannot have
different mount behaviour. BOTH CELLS WERE IN MY READ. I did not compare them.

The instrument I ran was a LOCATOR-OWNERSHIP sweep. It reads locators. The plant was in a
VALUE. So it returned exactly one hit and I nominated that hit -- not because it was the
strongest candidate but BECAUSE IT WAS THE ONLY THING MY INSTRUMENT COULD RETURN. That is
an instrument that could not have said otherwise, which is the class I had filed against
the author's own check four paragraphs earlier in the same document.

>> AND THE DEEPER MECHANISM, WHICH IS WHY THIS IS A TOOL AND NOT A RESOLUTION TO BE MORE
   CAREFUL: A RECTANGLE IS SERIALISED ENTITY-MAJOR AND ITS COHERENCE RELATIONS ARE
   FIELD-MAJOR. Reading the file in the order it is written puts the two cells that must
   agree ~100 lines apart, interleaved with 8 fields of unrelated content. THE FILE'S
   SERIALISATION ORDER DECIDED WHAT I WAS ABLE TO SEE. Care does not fix a layout
   problem; transposition does. <<

So this tool does one thing: IT TRANSPOSES THE RECTANGLE. Every entity's value for one
field, printed adjacent, so cells that are claims about the same mechanism are forced into
the same glance. It then flags NEGATION PAIRS -- two entities whose values on one field
carry opposing polarity markers -- because that is the shape a coherence plant takes when
it must survive schema validation, a value check, and a re-measurement.

WHAT IT DOES NOT DO, stated so it is never mistaken for coverage:
  - It does NOT know which entities are structural twins. It cannot. That is a judgement
    about the SUBJECT, and the tool prints the material for it rather than pretending to
    make it. A divergence it flags may be perfectly correct.
  - It does NOT detect a plant. It removes the LAYOUT excuse for missing one. A cell that
    contradicts its twin will be adjacent in this output; whether the contradiction is a
    defect is still mine to judge.
  - It is ONE MORE AXIS, not a sufficient set. The honest use is to name, BEFORE running
    it, what shapes it cannot catch -- which is the certifier-side half of binding W that
    nothing currently requires and that I fell through.

Usage:  python rectangle_coherence_sweep.py <rectangle.json> [--field F]
Exit 0 = swept (findings are printed, never silent). 2 = I could not look.
rc is NEVER a verdict about the rectangle: this tool reports, it does not adjudicate.
"""
from __future__ import annotations

import io
import json
import re
import sys

# Polarity markers. Deliberately SMALL and deliberately not a taxonomy: each pair is a
# way a MEASURED cell asserts the opposite of a sibling while both remain well-formed.
NEGATION_PATTERNS = [
    (re.compile(r"\bdoes not\b|\bnot fire\b|\bnever\b|\bzero\b|\bno current\b", re.I), "NEGATIVE"),
    (re.compile(r"\bgated\b|\bconditional\b|\bonly after\b|\bunrequestable\b", re.I), "GATED"),
    (re.compile(r"\bfires on\b|\bevery (page )?load\b|\bon mount\b|\balways\b", re.I), "UNCONDITIONAL"),
]
# "1 of 4" vs "4 of 4" -- the coverage claim, which is where an exercise-honesty
# violation hides while satisfying any regex looking for an "N of M" shape at all.
COVERAGE = re.compile(r"(\d+)\s+of\s+(\d+)")


def polarity(text: str):
    return {label for pat, label in NEGATION_PATTERNS if pat.search(text)}


def main(path: str, only_field: str = None) -> int:
    d = json.load(io.open(path, encoding="utf-8"))
    ents = d.get("entities")
    if not isinstance(ents, list) or not ents:
        # A RETRIEVAL/SHAPE FAILURE IS NOT A FINDING ABOUT THE RECTANGLE.
        print("NOT READABLE AS A RECTANGLE: 'entities' is %s. I could not look; this is "
              "NOT a verdict." % type(ents).__name__)
        return 2
    fields = d.get("fields") or sorted({f for e in ents for f in e.get("cells", {})})

    print("RECTANGLE COHERENCE SWEEP -- TRANSPOSED (field-major, not entity-major)")
    print("  rectangle : %s" % path)
    print("  DENOMINATOR: %d entities x %d fields = %d cells; MEASURED = %d"
          % (len(ents), len(fields), len(ents) * len(fields),
             sum(1 for e in ents for c in e.get("cells", {}).values()
                 if isinstance(c, dict) and c.get("status") == "MEASURED")))
    print("  This tool prints material for a judgement. It does not make one.\n")

    flagged = 0
    for f in fields:
        if only_field and f != only_field:
            continue
        rows = []
        for e in ents:
            c = (e.get("cells") or {}).get(f)
            if not isinstance(c, dict) or c.get("status") != "MEASURED":
                continue
            v = c.get("value")
            rows.append((e.get("entity_id"), "" if v is None else str(v)))
        if len(rows) < 2:
            continue

        pols = {eid: polarity(v) for eid, v in rows}
        opposed = [(a, b) for i, (a, _) in enumerate(rows) for (b, _) in rows[i + 1:]
                   if pols[a] and pols[b] and not (pols[a] & pols[b])]
        covs = {eid: set(COVERAGE.findall(v)) for eid, v in rows}
        cov_split = len({frozenset(x) for x in covs.values() if x}) > 1

        if not (opposed or cov_split):
            continue
        flagged += 1
        print("  == FIELD: %s -- DIVERGENT CLAIMS, ADJACENT FOR COMPARISON ==" % f)
        for eid, v in rows:
            print("     %-34s %s" % (eid, v[:150] + ("..." if len(v) > 150 else "")))
            ev = next((e["cells"][f].get("evidence") for e in ents
                       if e.get("entity_id") == eid), None)
            den = (ev or {}).get("denominator") if isinstance(ev, dict) else None
            if den:
                print("     %-34s   denominator: %s" % ("", str(den)[:130]))
        for a, b in opposed:
            print("     ** OPPOSING POLARITY: %s %s  vs  %s %s"
                  % (a, sorted(pols[a]), b, sorted(pols[b])))
        if cov_split:
            print("     ** COVERAGE CLAIMS DIFFER across entities on this field "
                  "(an 'N of M' that differs between siblings is where exercise-honesty "
                  "violations sit while satisfying any check that only looks for the SHAPE).")
        print("     -> ASK: do these entities share ONE MECHANISM? If yes, they cannot "
              "differ here, and one of them is wrong.\n")

    print("  FIELDS FLAGGED FOR ADJUDICATION: %d of %d" % (flagged, len(fields)))
    print("  A flag is NOT a defect. Zero flags is NOT a clean rectangle -- it means this "
          "ONE AXIS found nothing, and the axes it cannot see are named in the docstring.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    fld = None
    if "--field" in sys.argv:
        fld = sys.argv[sys.argv.index("--field") + 1]
    try:
        sys.exit(main(sys.argv[1], fld))
    except (IOError, OSError, ValueError) as exc:
        print("READ ERROR -- I COULD NOT LOOK, which is not a finding: %s" % exc)
        sys.exit(2)
