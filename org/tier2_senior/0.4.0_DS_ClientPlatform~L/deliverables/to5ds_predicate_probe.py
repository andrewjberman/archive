"""TO-5-DS AC4 + AC5 evidence -- the membership predicate, exercised.

SHAPE-INDEPENDENT BY CONSTRUCTION: this measures WHICH ROWS ARE MEMBERS. It takes no
position on how the artifact is serialised, which is still with 1.0.0_SA_CTO~Z /
3.0.0_SA_CVO~Z at the time of writing.

AC4 as AMENDED by 1.0.0_SA_CTO~Z (msg 11202) is THREE rows, not one:
    REAL,      MUST REJECT   Core | Satellite 98            the `Opal` token limb
    SYNTHETIC, MUST REJECT   Opal Satellite 50 + 15% cash   the trailing-anchor limb
    SYNTHETIC, MUST ADMIT    Opal Satellite 55              proves the path DERIVES
The third is load-bearing and no real row can supply it: the nine members pass under BOTH
the derived predicate and the declared list it replaces, so only an ADMIT the list does
not contain separates the two implementations.

PER-LIMB ablation reproduces CTO's measurement rather than quoting it.
"""
import json
import re
import sys

ROSTER = ("C:/Users/OPALBL~1/AppData/Local/Temp/claude/"
          "C--Users-Opal-Bloomberg-Desktop-ajb-workspace/"
          "9380252a-7dd3-410d-9afa-14091d235dbd/scratchpad/f3ctl/roster.json")
REGISTRY = "data/assets/scripts/gold"

CANONICAL = re.compile(r"^Opal Satellite (\d+)$")

# The ablations. Each drops exactly ONE limb of the canonical form.
ABLATIONS = {
    "SHIPPED  ^Opal Satellite N$": re.compile(r"^Opal Satellite (\d+)$"),
    "drop token Opal": re.compile(r"satellite", re.I),
    "drop leading anchor": re.compile(r"Opal Satellite (\d+)$"),
    "drop trailing anchor": re.compile(r"^Opal Satellite (\d+)"),
}


def names(rows):
    return [r.get("name") for r in rows if isinstance(r.get("name"), str)]


def main():
    doc = json.load(open(ROSTER, encoding="utf-8"))
    rows = doc["pagedResults"]
    ns = names(rows)

    print("=" * 74)
    print("ROSTER, self-certifying envelope (not inferred):")
    print("  pageCount=%s totalResultCount=%s len(pagedResults)=%s  rows with a name=%d"
          % (doc["pageCount"], doc["totalResultCount"], len(rows), len(ns)))
    print("=" * 74)

    # ---- AC5: the derivation -------------------------------------------
    members = sorted(n for n in ns if CANONICAL.match(n))
    print("\nAC5  DERIVED MEMBERS -- %d of %d" % (len(members), len(rows)))
    for m in members:
        print("      %s" % m)

    sys.path.insert(0, REGISTRY)
    import satellites_registry as SR
    declared = sorted(SR.MEMBER_NAMES)
    print("\n  declared (SATELLITE_MEMBERS) : %d" % len(declared))
    print("  derived == declared          : %s" % (members == declared))
    print("  derived not declared         : %s" % sorted(set(members) - set(declared)))
    print("  declared not derived         : %s" % sorted(set(declared) - set(members)))

    print("\n  AC5 EXCLUSION SPOT-CHECKS (named in the TO):")
    for probe in ("Opal Ultra Short Term",):
        on_roster = probe in ns
        admitted = bool(CANONICAL.match(probe))
        print("      %-26s on roster=%-5s admitted=%-5s  <- roster membership is NOT "
              "satellite membership" % (probe, on_roster, admitted))
    blends = sorted(n for n in ns if n.lower().startswith("core |")
                    or ("sat" in n.lower() and not CANONICAL.match(n)))
    print("      rows containing 'sat' or 'Core |' that are NOT admitted: %d" % len(blends))
    for b in blends:
        print("          REJECTED  %s" % b)

    # ---- AC4: the three rows -------------------------------------------
    print("\n" + "=" * 74)
    print("AC4  THE THREE ROWS (amended). REAL pair + two synthetics.")
    print("=" * 74)
    cases = [
        ("REAL      MUST REJECT", "Core | Satellite 98", False),
        ("SYNTHETIC MUST REJECT", "Opal Satellite 50 + 15% cash", False),
        ("SYNTHETIC MUST ADMIT ", "Opal Satellite 55", True),
    ]
    ac4_ok = True
    for label, name, want in cases:
        got = bool(CANONICAL.match(name))
        ok = got == want
        ac4_ok &= ok
        on_roster = name in ns
        print("  %s  %-30s admitted=%-5s want=%-5s %s   (in roster: %s)"
              % (label, name, got, want, "OK" if ok else "FAIL", on_roster))

    print("\n  Why the third row cannot come from the corpus: the declared list contains")
    print("  %d names and 'Opal Satellite 55' is not one of them (%s). A HARDCODED LIST"
          % (len(declared), "Opal Satellite 55" in declared))
    print("  REJECTS it; the DERIVED predicate ADMITS it. That is the only separator.")

    # ---- per-limb ablation, reproducing rather than quoting -------------
    print("\n" + "=" * 74)
    print("PER-LIMB ABLATION -- extra admits vs the shipped form (65-row roster)")
    print("=" * 74)
    base = set(n for n in ns if ABLATIONS["SHIPPED  ^Opal Satellite N$"].match(n))
    for label, rx in ABLATIONS.items():
        got = set(n for n in ns if rx.match(n) or (rx.flags & re.I and rx.search(n)))
        extra = sorted(got - base)
        print("  %-30s admits %2d   EXTRA %+d" % (label, len(got), len(extra)))
        for e in extra[:6]:
            print("        + %s" % e)
    print("\n  The two anchors measure +0 on this corpus -- NO REAL ROW TESTS THEM.")
    print("  That is why AC4's synthetic REJECT is required and is not a shortcut.")

    print("\n" + "=" * 74)
    print("AC4: %s     AC5: derived %d of %d, matches declared: %s"
          % ("PASS" if ac4_ok else "FAIL", len(members), len(rows), members == declared))
    print("=" * 74)
    return 0 if (ac4_ok and members == declared) else 1


if __name__ == "__main__":
    sys.exit(main())
