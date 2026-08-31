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

# Allocation carries envelope fields the other leaves do not, and the RENDERER READS ALL
# FOUR EXTRAS: residue_states_declared classifies residue rows (never a frontend literal),
# basis_line is quoted verbatim, period_keyed explains why the picker does not move these
# numbers, allocation_as_of dates the cut. Dropping any of them would force the component
# to invent the fact instead.
ALLOCATION_ENVELOPE_FIELDS = ENVELOPE_FIELDS + [
    'allocation_as_of', 'basis_line', 'period_keyed',
    'residue_states_declared', 'residue_states_present', 'classes',
]


def load(level):
    p = os.path.join(EMISSIONS, 'perfrp_performance_%s.json' % level)
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def load_gainloss(level):
    p = os.path.join(EMISSIONS, 'perfrp_gainloss_%s.json' % level)
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def load_book():
    p = os.path.join(EMISSIONS, 'perfrp_book_advisor.json')
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def load_allocation(level):
    p = os.path.join(EMISSIONS, 'perfrp_allocation_%s.json' % level)
    with open(p, encoding='utf-8') as fh:
        return p, json.load(fh)


def pick_allocation_rows(leaf, n):
    """Pick n entries, PREFERRING ones that carry a declared RESIDUE class.

    ⛔ THIS IS THE SAME RULE AS THE STATE-SPANNING PICK ABOVE, APPLIED TO ALLOCATION'S
    OWN DISPOSITION AXIS. Allocation has no figure_state; its dispositions live in the
    CLASS dimension, where an unclassifiable dollar is emitted as a named residue class.
    Residue reaches only 117 of 3,834 relationship entries (3.1%) and 170 of 6,179
    account entries (2.8%) -- measured -- so a first-N pick would almost certainly draw
    three tidy canonical classes and score a render that never exercised the residue
    branch as a pass. That is the one-branch-render trap this builder already refuses
    for figure_state, and it would be no less a false pass here.

    Residue-carrying rows come FIRST; canonical-only rows backfill so the count is met
    even if the emission ever stops emitting residue.
    """
    declared = set(leaf.get('residue_states_declared') or [])
    with_residue, without = [], []
    for e in leaf.get('entries') or []:
        names = {c.get('asset_class') for c in (e.get('classes') or [])}
        (with_residue if (names & declared) else without).append(e)
    return (with_residue + without)[:n], len(with_residue)


def pseudonymise_row(row, i):
    """Replace the client-identifying fields of one client_table row, keeping every FIGURE.

    Deliberately NOT a hash of the real name: a stable hash is a pseudonym that still
    distinguishes real clients, and anything that survives as a per-client identifier is a
    re-identification handle once joined against another artifact. An index is not.
    """
    new = dict(row)
    label = 'Fixture Household %s' % chr(ord('A') + (i % 26))
    new['relationship'] = label
    new['client'] = label
    new['relationship_id'] = 'FIXTURE_REL_%d' % (i + 1)
    return new


def pick_book_row(entries):
    """The advisor row that exercises the MOST tile states, not the first row.

    All four tiles carry a headline on nearly every advisor, so 'first row' would render
    four COMPUTED tiles and never reach the not-computed branch -- the same one-branch
    trap the performance selection avoids. Rank by DISTINCT figure_state count."""
    best, best_key = None, (-1, -1)
    for e in entries:
        tiles = e.get('tiles') or {}
        if not any(t.get('headline') for t in tiles.values()):
            continue
        states = {f.get('figure_state')
                  for t in tiles.values() for f in t.values() if isinstance(f, dict)}
        # PRIMARY: distinct tile states (the branch coverage this exists for).
        # TIE-BREAK: client_table size -- with the ruled columns now emitted, a one-row
        # table renders the header and proves almost nothing about the ROWS. The tie-break
        # is secondary on purpose: coverage of the state vocabulary still outranks a
        # prettier table.
        key = (len(states), len(e.get('client_table') or []))
        if key > best_key:
            best, best_key = e, key
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
    # ⛔ PII GATE -- THE ONLY PLACE REAL CLIENT NAMES COULD ENTER THE PORTAL REPO.
    # b-6's client_table re-emission carries `relationship` = a REAL display label (person,
    # trust or entity); 3,362 distinct values in the leaf, measured. The FIGURES stay real
    # because the fixture exists to prove they render; the NAMES are replaced. This is not a
    # nicety: the fixture is committed to the portal repo, which is a different exposure from
    # the pipeline tree the leaf lives in, and a name is not recoverable once pushed.
    bound['client_table'] = [
        pseudonymise_row(r, i) for i, r in enumerate(bound.get('client_table') or [])
    ]
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

    # ---- PRF-b-4, gain/loss, BOTH grains. The first emission carried bare numbers and this
    # lane refused to bind them; the re-emission @c118a8e4d7 carries {value, figure_state,
    # reason} on every figure, so the card's figures bind now. The bare-figure count is
    # RE-COUNTED here rather than trusted, and the builder REFUSES if any figure is bare --
    # the fixture must not be the thing that reintroduces an unclaimed value.
    gl_reports = []
    for lvl, keys in (('relationship', [REL_KEY]), ('account', ACCT_KEYS)):
        gl_path, gl = load_gainloss(lvl)
        bare = sum(
            1 for e in gl['entries'] for v in e.values()
            if isinstance(v, dict) and 'figure_state' not in v)
        if bare:
            sys.exit('ABORT: %s carries %d bare figure(s) -- refusing to bind' % (gl_path, bare))
        rows = gl['entries'][:len(keys)]
        gl_env = {k: gl[k] for k in ENVELOPE_FIELDS if k in gl}
        gl_env['entries'] = [rebind(r, k) for k, r in zip(keys, rows)]
        gl_env['_fixture_provenance'] = {
            'source_file': os.path.relpath(gl_path, ROOT).replace(os.sep, '/'),
            'real': 'every producer field including figure_state and reason on every figure',
            'fixture': 'the join key only; each row names its _source_key',
            'bare_figures': '0 of %d rows carry a bare figure (re-counted at build time)' % len(gl['entries']),
            'not_a_data_oracle': 'render instrument only.',
        }
        merged['perfrp/perfrp_gainloss_%s.json' % lvl] = gl_env
        gl_reports.append((gl_path, gl, rows, keys))

    # ---- PRF-b-3, allocation, BOTH grains. -----------------------------------------
    # ⛔ WHY THIS BINDS WHILE THE FIRST b-4 EMISSION DID NOT, THOUGH BOTH LACK
    # figure_state: allocation's disposition axis is the CLASS dimension, not a per-figure
    # state. An unclassifiable dollar is emitted as a NAMED RESIDUE CLASS carrying its real
    # market value, so nothing is left unstated for the consumer to invent. The guard below
    # is what makes that claim checkable instead of asserted.
    alloc_reports = []
    for lvl, keys in (('relationship', [REL_KEY]), ('account', ACCT_KEYS)):
        alloc_path, alloc = load_allocation(lvl)
        rows, residue_pop = pick_allocation_rows(alloc, len(keys))
        if len(rows) < len(keys):
            sys.exit('ABORT: %s has %d entries, need %d' % (alloc_path, len(rows), len(keys)))
        # THE CLOSURE GUARD, the structural sibling of the bare-figure refusal above.
        # The renderer presents these shares as a complete split; if the producer ever
        # stops closing the distribution, the fixture must REFUSE rather than ship a
        # split that silently totals less than 100%.
        for r in rows:
            s = sum(c.get('allocation_of_level') or 0 for c in (r.get('classes') or []))
            if abs(s - 1.0) > 0.0005:
                sys.exit('ABORT: %s row %s allocation_of_level sums to %.6f, not 1.0 -- '
                         'refusing to bind an unclosed distribution' % (alloc_path, r.get('key'), s))
        alloc_env = {k: alloc[k] for k in ALLOCATION_ENVELOPE_FIELDS if k in alloc}
        alloc_env['entries'] = [rebind(r, k) for k, r in zip(keys, rows)]
        alloc_env['_fixture_provenance'] = {
            'source_file': os.path.relpath(alloc_path, ROOT).replace(os.sep, '/'),
            'real': ('every class row -- asset_class, market_value, allocation_of_total, '
                     'allocation_of_level -- plus the leaf basis_line and residue vocabulary'),
            'fixture': 'the join key only; each row names its _source_key',
            'row_selection': (
                'RESIDUE-SPANNING, not first-N: %d of %d entries in this emission carry a '
                'declared residue class, so a first-N pick would very likely have rendered '
                'only canonical classes and never exercised the residue branch'
                % (residue_pop, len(alloc.get('entries') or []))),
            'closure_checked': 'allocation_of_level sums to 1.0 +/-0.0005 on every bound row',
            'no_figure_state_is_correct_here': (
                'allocation carries no per-figure state BY SHAPE; its dispositions are the '
                'declared residue classes. These values must NOT be rendered through '
                'PerfrpFigureCell.'),
            'not_a_data_oracle': 'render instrument only.',
        }
        merged['perfrp/perfrp_allocation_%s.json' % lvl] = alloc_env
        alloc_reports.append((alloc_path, alloc, rows, keys, residue_pop))

    globals()['_ALLOC_REPORT'] = alloc_reports
    globals()['_BOOK_REPORT'] = (book_path, advisor_row, book)
    globals()['_GL_REPORT'] = gl_reports

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
    print('   perfrp/perfrp_gainloss_relationship.json')
    print('   perfrp/perfrp_gainloss_account.json')
    print('   perfrp/perfrp_allocation_relationship.json')
    print('   perfrp/perfrp_allocation_account.json')
    print()
    for ap, al, rows, keys, residue_pop in globals()['_ALLOC_REPORT']:
        print('ALLOCATION %s -- entries %d, as_of %s, residue-carrying %d (%.1f%%)' % (
            ap.split(os.sep)[-1], len(al['entries']), al.get('allocation_as_of'),
            residue_pop, 100.0 * residue_pop / max(1, len(al['entries']))))
        declared = set(al.get('residue_states_declared') or [])
        for k, r in zip(keys, rows):
            cls = r.get('classes') or []
            res = [c['asset_class'] for c in cls if c.get('asset_class') in declared]
            tot = sum(c.get('allocation_of_level') or 0 for c in cls)
            print('   %-16s <- %-24s classes=%d sum_of_level=%.6f residue=%s' % (
                k, r['key'], len(cls), tot, ', '.join(res) if res else 'none'))
    print()
    for glp, gll, rows, keys in globals()['_GL_REPORT']:
        figs = sum(1 for e in gll['entries'] for v in e.values() if isinstance(v, dict))
        print('GAINLOSS %s -- entries %d, figures %d, bare 0, as_of %s' % (
            glp.split(os.sep)[-1], len(gll['entries']), figs, gll.get('as_of')))
        for k, r in zip(keys, rows):
            tgl = (r.get('total_gain_loss') or {})
            print('   %-16s <- %-24s total_gain_loss=%s (%s)' % (
                k, r['key'], tgl.get('value'), tgl.get('figure_state')))
    ct = bound.get('client_table') or []
    print()
    print('CLIENT TABLE (b-6) -- %d row(s) bound, ALL display labels PSEUDONYMISED' % len(ct))
    for r in ct[:3]:
        print('   %-22s status=%-9s ending_mv=%s' % (
            r.get('relationship'), r.get('status'),
            (r.get('ending_market_value') or {}).get('value')))


if __name__ == '__main__':
    main()
