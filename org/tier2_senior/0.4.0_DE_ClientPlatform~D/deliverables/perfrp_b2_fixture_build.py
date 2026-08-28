#!/usr/bin/env python3
"""
ADVI_PERFRP.TO-R1-DE -- build the harness fixture that carries the PRF-b-2 QA leaf.

WHY THIS EXISTS AS A SCRIPT AND NOT A HAND-EDITED JSON: the fixture's figures are REAL
producer values lifted out of the b-2 emission, so the ONLY thing that makes them
auditable is a reproducible construction that prints WHICH leaf row each fixture row
came from. A hand-built fixture would be indistinguishable from invented numbers.

WHAT IS REAL AND WHAT IS A FIXTURE -- stated here because the distinction is the whole
integrity of the artifact:

  REAL, copied byte-for-byte from the emission:
      contract_version, as_of, si_label, periods, declared_absent_columns, window,
      and per row: figure_state, reason, window_return, accounts.

  FIXTURE, invented by this script:
      the JOIN KEY only. The emission's keys are salted hashes (rel_337c6494223d65);
      the render harness drills into FIXTURE_HH_C / FIXTURE_ACCT_*. Each fixture row
      therefore carries a REAL figure under a FIXTURE key, and `_source_key` on every
      row names the emission row it was taken from.

  >> NO FIGURE CLAIM ABOUT ANY NAMED CLIENT MAY EVER BE SOURCED FROM THIS FILE. It
     proves that the LEAF'S SHAPE AND STATE VOCABULARY RENDER; it does not prove
     anything about FIXTURE_HH_C, which is not a real relationship.

ROW SELECTION is deliberately state-spanning, not first-N: the render is only a real
exercise of PerfrpFigureCell if the fixture reaches its distinct branches (a value, a
partial-with-reason, and a not-computed label). First-N would very likely have given
four rows in one state and scored a one-branch render as a pass.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
EMISSIONS = os.path.join(
    ROOT, 'org', 'tier2_senior', '0.4.0_DS_ClientPlatform~V', 'deliverables', 'emissions')
DRILL_FIXTURE = os.path.join(
    ROOT, 'portal', '.frontend-dev', 'testing', 'perfrp_books_l3.json')
OUT = os.path.join(
    ROOT, 'portal', '.frontend-dev', 'testing', 'perfrp_b2_leaf_l3l4.json')

# The fixture keys the drill actually reaches, in the order the harness clicks them.
REL_KEY = 'FIXTURE_HH_C'
ACCT_KEYS = ['FIXTURE_ACCT_1', 'FIXTURE_ACCT_2']
ADVISOR_KEY = 'Fixture Advisor'

ENVELOPE_FIELDS = ['contract_version', 'as_of', 'family', 'level', 'si_label',
                   'periods', 'declared_absent_columns', 'window']


def load(level):
    p = os.path.join(EMISSIONS, 'perfrp_performance_%s.json' % level)
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def load_book():
    p = os.path.join(EMISSIONS, 'perfrp_book_advisor.json')
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def pick_book_row(entries):
    """The advisor row that exercises the MOST tile states, not the first row.

    All four tiles carry a headline on nearly every advisor, so 'first row' would render
    four COMPUTED tiles and never reach the not-computed branch -- the same one-branch
    trap the performance selection avoids. Rank by DISTINCT figure_state count."""
    best, best_n = None, -1
    for e in entries:
        tiles = e.get('tiles') or {}
        if not any(t.get('headline') for t in tiles.values()):
            continue
        states = {f.get('figure_state')
                  for t in tiles.values() for f in t.values() if isinstance(f, dict)}
        if len(states) > best_n:
            best, best_n = e, len(states)
    return best


def pick_by_state(entries, wanted_states):
    """One real row per wanted state, in order. Returns [(state, row)] and names any
    state the emission could not supply -- an absent state is REPORTED, never silently
    replaced with a row in a different state."""
    out, missing = [], []
    used = set()
    for st in wanted_states:
        row = next((e for e in entries
                    if e.get('figure_state') == st and e.get('key') not in used), None)
        if row is None:
            missing.append(st)
            continue
        used.add(row['key'])
        out.append((st, row))
    return out, missing


def rebind(row, fixture_key):
    """Copy a real row onto a fixture join key, keeping every producer field and
    recording the row it came from."""
    new = dict(row)
    new['_source_key'] = row['key']
    new['key'] = fixture_key
    return new


def build_leaf(level, bindings, src_path, leaf):
    env = {k: leaf[k] for k in ENVELOPE_FIELDS if k in leaf}
    env['entries'] = [rebind(row, key) for key, row in bindings]
    env['_fixture_provenance'] = {
        'source_file': os.path.relpath(src_path, ROOT).replace('\\', '/'),
        'source_figure_state_census': leaf.get('figure_state_census'),
        'real': 'every producer field, including figure_state / reason / window_return',
        'fixture': 'the join key only; each row names its _source_key',
        'not_a_data_oracle': (
            'render instrument. No figure claim about any named client may be '
            'sourced from this file.'),
    }
    return env


def main():
    rel_path, rel = load('relationship')
    acct_path, acct = load('account')

    # THE THREE PerfrpFigureCell BRANCHES, spread across the three slots the drill can
    # actually reach (1 relationship + 2 accounts). Chosen this way rather than by
    # convenience: two value-carrying states in the two account slots would leave the
    # NO-VALUE branch unrendered, and that is precisely the branch PRF-d-7 protects
    # ("never a 0 where the value is unknown") -- the one a regression would hit.
    #
    #   L3 relationship  COMPUTED_PARTIAL              value + its coverage reason
    #   L4 account 1     COMPUTED                      a bare value, no reason
    #   L4 account 2     NOT_COMPUTED_INPUTS_PRESENT   a LABEL, never a 0
    rel_pick, rel_missing = pick_by_state(
        rel['entries'], ['COMPUTED_PARTIAL', 'COMPUTED'])
    if not rel_pick:
        sys.exit('ABORT: no renderable relationship row in %s' % rel_path)
    rel_bindings = [(REL_KEY, rel_pick[0][1])]

    acct_pick, acct_missing = pick_by_state(
        acct['entries'],
        ['COMPUTED', 'NOT_COMPUTED_INPUTS_PRESENT'])
    if not acct_pick:
        sys.exit('ABORT: no renderable account row in %s' % acct_path)
    acct_bindings = list(zip(ACCT_KEYS, [r for _, r in acct_pick]))

    with open(DRILL_FIXTURE, encoding='utf-8') as fh:
        merged = json.load(fh)

    merged['_README'] = list(merged.get('_README', [])) + [
        '',
        'ADVI_PERFRP.TO-R1-DE ADDITION -- the PRF-b-2 QA leaf, consumed as a BUILD',
        'ARTIFACT under the build-only cap (no platinum key, no publisher grant, no',
        'serve). Built by org/tier2_senior/0.4.0_DE_ClientPlatform~D/deliverables/',
        'perfrp_b2_fixture_build.py -- re-run it rather than hand-editing.',
        'FIGURES ARE REAL PRODUCER VALUES; the JOIN KEY is the fixture. Every perfrp',
        'row carries _source_key naming the emission row it was taken from.',
        'The rows above this line remain synthetic, exactly as before.',
    ]
    merged['perfrp/perfrp_performance_relationship.json'] = build_leaf(
        'relationship', rel_bindings, rel_path, rel)
    merged['perfrp/perfrp_performance_account.json'] = build_leaf(
        'account', acct_bindings, acct_path, acct)

    # ---- PRF-b-6, the advisor book leaf (four ruled KPI tiles + the client table) ----
    # Its as_of is 2026-08-27 / QTD against b-2's 2024-11-07 / SI. THAT DIFFERENCE IS
    # CARRIED THROUGH DELIBERATELY AND NOT RECONCILED: the two leaves are floored by
    # different upstreams, and a fixture that quietly aligned them would hide exactly the
    # cross-leaf as-of mismatch a consumer needs to see.
    book_path, book = load_book()
    advisor_row = pick_book_row(book['entries'])
    if advisor_row is None:
        sys.exit('ABORT: no advisor row with a headline tile in %s' % book_path)
    book_env = {k: book[k] for k in ENVELOPE_FIELDS if k in book}
    bound = dict(advisor_row)
    bound['_source_key'] = advisor_row['key']
    bound['key'] = ADVISOR_KEY
    book_env['entries'] = [bound]
    book_env['_fixture_provenance'] = {
        'source_file': os.path.relpath(book_path, ROOT).replace('\\', '/'),
        'real': 'every tile figure, its figure_state and reason, and the client_table rows',
        'fixture': 'the advisor join key only; the row names its _source_key',
        'as_of_note': (
            'as_of %s / period %s -- DIFFERENT from the performance leaves by '
            'construction, not an error to align' % (
                book.get('as_of'), (book.get('window') or {}).get('period'))),
        'not_a_data_oracle': 'render instrument only.',
    }
    merged['perfrp/perfrp_book_advisor.json'] = book_env
    globals()['_BOOK_REPORT'] = (book_path, advisor_row, book)

    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(merged, fh, indent=2)
        fh.write('\n')

    print('WROTE', os.path.relpath(OUT, ROOT).replace('\\', '/'))
    print()
    print('RELATIONSHIP leaf %s -- entries %d' % (rel_path.split(os.sep)[-1], len(rel['entries'])))
    for key, row in rel_bindings:
        print('   %-16s <- %-24s state=%-28s value=%s' % (
            key, row['key'], row.get('figure_state'), row.get('window_return')))
    if rel_missing:
        print('   STATES NOT PRESENT in the relationship emission: %s' % ', '.join(rel_missing))
    print('ACCOUNT leaf %s -- entries %d' % (acct_path.split(os.sep)[-1], len(acct['entries'])))
    for key, row in acct_bindings:
        print('   %-16s <- %-24s state=%-28s value=%s' % (
            key, row['key'], row.get('figure_state'), row.get('window_return')))
    if acct_missing:
        print('   STATES NOT PRESENT in the account emission: %s' % ', '.join(acct_missing))
    print()
    bp, brow, bleaf = globals()['_BOOK_REPORT']
    states = {}
    for tname, t in (brow.get('tiles') or {}).items():
        for fname, f in t.items():
            if isinstance(f, dict):
                states.setdefault(f.get('figure_state'), 0)
                states[f.get('figure_state')] += 1
    print('BOOK leaf %s -- advisors %d, as_of %s, period %s' % (
        bp.split(os.sep)[-1], len(bleaf['entries']), bleaf.get('as_of'),
        (bleaf.get('window') or {}).get('period')))
    print('   %-16s <- %-24s tiles=%d client_table rows=%d' % (
        ADVISOR_KEY, brow['key'], len(brow.get('tiles') or {}),
        len(brow.get('client_table') or [])))
    print('   tile figure_state spread (the reason this row was picked): %s' % (
        ', '.join('%s=%d' % kv for kv in sorted(states.items()))))
    print()
    print('ROUTE KEYS ADDED (denominator %d total in file):' % (
        len([k for k in merged if not k.startswith('_')])))
    print('   perfrp/perfrp_performance_relationship.json')
    print('   perfrp/perfrp_performance_account.json')
    print('   perfrp/perfrp_book_advisor.json')


if __name__ == '__main__':
    main()
