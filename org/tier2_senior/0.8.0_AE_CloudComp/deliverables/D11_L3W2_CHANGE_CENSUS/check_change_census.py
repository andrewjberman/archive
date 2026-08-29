#!/usr/bin/env python3
"""THE CONSUMING HALF of L4-C02's change census -- the mechanism, not a description of one.

L4-C02 (boundary declarations @9c1a45ad28) requires, for EVERY input in the fusion's
population, either at least TWO OBSERVED CHANGES or an explicit FROZEN declaration. This
script is what a consumer RUNS, and it REFUSES rather than defaulting:

  exit 0  every input carries >=2 observed changes, or an explicit frozen declaration
  exit 2  an input is short of the rule (changed <2 and not declared frozen) -> WINDOW NOT
          YET SUFFICIENT; N may not be re-derived as if it were
  exit 3  the required field is ABSENT on an input, or the census itself is missing a
          required field -> the record is REFUSED. An absent field is NEVER read as
          "no change"; that is the silent-pass this declaration exists to stop.

"The field is expected" is not a mechanism. Run this, read the exit code.

Usage: python check_change_census.py <census.json> [--explain]
"""
import io
import json
import sys

REQUIRED_TOP = ['schema_version', 'declaration', 'population_denominator', 'observation',
                'inputs', 'classification']
REQUIRED_PER_INPUT = ['name', 'paths', 'pin', 'observed_changes', 'frozen_declaration']


def main(argv):
    if len(argv) < 2:
        print("usage: check_change_census.py <census.json> [--explain]")
        return 64
    explain = '--explain' in argv
    try:
        c = json.load(io.open(argv[1], encoding='utf-8'))
    except Exception as e:
        print("REFUSED (exit 3): census unreadable -- %r" % (e,))
        return 3

    missing_top = [k for k in REQUIRED_TOP if k not in c]
    if missing_top:
        print("REFUSED (exit 3): census is missing required field(s): %s" % missing_top)
        return 3

    inputs = c['inputs']
    den = c['population_denominator']
    if den != len(inputs):
        print("REFUSED (exit 3): population_denominator %r does not equal the number of "
              "inputs listed (%d) -- a denominator that does not count its own population "
              "is a frame error" % (den, len(inputs)))
        return 3

    absent, short, ok, frozen = [], [], [], []
    for i in inputs:
        miss = [k for k in REQUIRED_PER_INPUT if k not in i]
        if miss:
            absent.append((i.get('name', '<unnamed>'), miss))
            continue
        if i['frozen_declaration']:
            frozen.append(i['name'])
        elif not isinstance(i['observed_changes'], int):
            absent.append((i['name'], ['observed_changes not an integer']))
        elif i['observed_changes'] >= 2:
            ok.append(i['name'])
        else:
            short.append((i['name'], i['observed_changes']))

    print("change-census check | population denominator %d" % den)
    print("  >=2 observed changes : %d of %d" % (len(ok), den))
    print("  frozen declared      : %d of %d" % (len(frozen), den))
    print("  SHORT (<2, no frozen): %d of %d %s" % (len(short), den, short if short else ''))
    print("  FIELD ABSENT         : %d of %d %s" % (len(absent), den, absent if absent else ''))

    if absent:
        print("REFUSED (exit 3): a required field is ABSENT on %d input(s). An absent field is "
              "NOT 'no change' -- the record is refused and the run's persistence claims are "
              "not credited." % len(absent))
        return 3
    if short:
        print("REFUSED (exit 2): %d input(s) carry fewer than two observed changes and no "
              "FROZEN declaration. The window is NOT yet sufficient for them; N may not be "
              "re-derived as though it were, and a persistence rate measured over this window "
              "would measure that nothing happened." % len(short))
        if explain:
            for n, v in short:
                print("     %-26s observed_changes=%d -- needs a second observed change or an "
                      "explicit frozen_declaration" % (n, v))
        return 2
    print("OK (exit 0): every input satisfies L4-C02 -- >=2 observed changes or an explicit "
          "frozen declaration.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
