#!/usr/bin/env python3
"""POSN_AGGFIX.TO-B2-1 (slot ~3) -- <PRIOR_LAYOUT_MAP_B2>: THE PRIOR LAYOUT, ELEMENT BY ELEMENT.

Reads the removal commit d53049a0's diff of src/pages/Positioning/tabs/HoldingsTab.tsx and the file at portal HEAD, and
prints every element the removal took out beside its restored counterpart at HEAD, with line numbers on both sides
(old = the file at d53049a0^, HEAD = the file at portal HEAD).

THE ELEMENT SET IS A SUBTRACTION, NOT A LIST: every line the removal deleted is assigned to exactly one of
  - a RESTORABLE element (the aggregate entry, the prepend, the default, the landing, the Model Breakdown group), or
  - a DEAD element (code that could not run: the client-side weighting, the AUM state and fetch, the two builders
    behind a period that is a constant 'Current'), or
  - a named NON-AGGREGATE class (comment/blank lines, the toggle-persistence lines the same commit changed, and the
    neighbouring group's corner class toggle),
and the count of lines assigned to nothing is printed; it must be 0 or this map is not the whole removal.

Then the four classes the order forbids (text-white, text-orange-300, bg-white/10, bg-orange-500/5) are counted in the
ADDED lines of `git diff edf85ce503 HEAD -- <file>` (the restored hunks), each as a whole class token -- beside a control:
the same counter over the lines d53049a0 removed from the Model Breakdown group, which must find them.

REVISION (attempt 2, recorded beside attempt 1 in b2_ac1_prior_layout_map.attempt1.txt): attempt 1 anchored E7 on the
first `selectedPortfolio === 'AGG' && (` line, which is the COLGROUP's (old :1169), so E7's span swallowed a comment
line and stopped before the header cell's own closing lines (old :1227-1228); and the neighbour's corner toggle line
(old :1229) had no named class. E7 is now anchored on its own `<th colSpan={5}` line, and N4 names the toggle line.

Usage (from the workspace root): python <this>     exit 0 only when RESTORED n of n, 0 unassigned, 0 forbidden, control > 0.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
PORTAL = os.path.join(ROOT, 'portal')
FILE = 'src/pages/Positioning/tabs/HoldingsTab.tsx'
REMOVAL = 'd53049a0'
BASE = 'edf85ce503'
FORBIDDEN = ['text-white', 'text-orange-300', 'bg-white/10', 'bg-orange-500/5']


def git(*args):
    r = subprocess.run(['git', '-C', PORTAL] + list(args), capture_output=True)
    if r.returncode != 0:
        sys.exit('BLOCKED: git ' + ' '.join(args) + ' rc=' + str(r.returncode) + ' ' + r.stderr.decode('utf-8', 'replace'))
    return r.stdout.decode('utf-8').replace('\r\n', '\n')


head_sha = git('rev-parse', 'HEAD').strip()
removal_sha = git('rev-parse', REMOVAL + '^{commit}').strip()
old_src = git('show', REMOVAL + '^:' + FILE).split('\n')
head_src = git('show', 'HEAD:' + FILE).split('\n')
dirty = git('status', '--porcelain', '--', 'src').strip()
print('PORTAL HEAD ' + head_sha + '  branch ' + git('rev-parse', '--abbrev-ref', 'HEAD').strip() +
      '  src working-tree changes: ' + (repr(dirty) if dirty else 'NONE'))
print('REMOVAL ' + REMOVAL + ' = ' + removal_sha + '  (old side = ' + REMOVAL + '^:' + FILE + ', ' + str(len(old_src)) +
      ' lines; HEAD side = HEAD:' + FILE + ', ' + str(len(head_src)) + ' lines)')


def diff_lines(spec_args):
    """[(sign, old_no, new_no, text)] for every removed ('-') and added ('+') line of a unified diff."""
    out = []
    o = n = 0
    for ln in git(*spec_args).split('\n'):
        m = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', ln)
        if m:
            o, n = int(m.group(1)), int(m.group(2))
            continue
        if ln.startswith('---') or ln.startswith('+++') or not o:
            continue
        if ln.startswith('-'):
            out.append(('-', o, None, ln[1:]))
            o += 1
        elif ln.startswith('+'):
            out.append(('+', None, n, ln[1:]))
            n += 1
        elif ln.startswith(' '):
            o += 1
            n += 1
    return out


removal = diff_lines(['show', '--format=', REMOVAL, '--', FILE])
removed = [(o, t) for s, o, _, t in removal if s == '-']


def find_all(src, pattern, start=0):
    rx = re.compile(pattern)
    return [i + 1 for i in range(start, len(src)) if rx.search(src[i])]


def span(src, start_pat, end_pat, nth=1, back=0):
    """1-based inclusive line span: the nth line matching start_pat (moved `back` lines up), through the first line
    at/after that match matching end_pat."""
    starts = find_all(src, start_pat)
    if len(starts) < nth:
        sys.exit('BLOCKED: old-side anchor not found (' + str(nth) + '): ' + start_pat)
    s = starts[nth - 1]
    ends = [e for e in find_all(src, end_pat, s - 1)]
    if not ends:
        sys.exit('BLOCKED: old-side end not found after :' + str(s) + ': ' + end_pat)
    return (s - back, ends[0])


# ---- THE ELEMENTS, BY OLD-SIDE SPAN -----------------------------------------------------------------------------
# (id, kind, what, old span, HEAD counterpart patterns)
MB_CMT = r"\{/\* Model Breakdown - only for AGG - NOW FIRST \*/\}"
CLOSE = r"^\s*\)\}$"
elements = [
    ('E1', 'RESTORABLE', "the AGG_PORTFOLIO entry",
     span(old_src, r"^const AGG_PORTFOLIO = ", r"^const AGG_PORTFOLIO = "),
     [r"^const AGG_PORTFOLIO = \{ id: AGGREGATE_BOOK, name: 'Aggregate', color: PALETTE\.opalIndigo \}"]),
    ('E2', 'RESTORABLE', "the prepend (portfoliosFor's aggregate parameter and return)",
     span(old_src, r"^const portfoliosFor = \(", r"^\}$"),
     [r"const aggregateOffered = books\.includes\(AGGREGATE_BOOK\)",
      r"const basePortfolios = aggregateOffered \? \[AGG_PORTFOLIO, \.\.\.namedPortfolios\] : namedPortfolios"]),
    ('E2b', 'RESTORABLE', "the prepend's call site (caps.aggregate passed to portfoliosFor)",
     span(old_src, r"const basePortfolios = portfoliosFor\(books, bookMode, caps\.aggregate\)", r"const basePortfolios = portfoliosFor"),
     [r"const namedPortfolios = portfoliosFor\(books\.filter\(\(b\) => b !== AGGREGATE_BOOK\), bookMode\)"]),
    ('E3', 'RESTORABLE', "the default (initial selection on the aggregate)",
     span(old_src, r"useState\(caps\.aggregate \? 'AGG' : ''\)", r"useState\(caps\.aggregate \? 'AGG' : ''\)"),
     [r"const selectionKey = `\$\{bookMode\}:\$\{statusKnown\}:\$\{aggregateOffered\}`",
      r"if \(!selectedPortfolio && books\.length > 0\) \{"]),
    ('E4', 'RESTORABLE', "the landing (defaultBook returns the aggregate)",
     span(old_src, r"if \(caps\.aggregate\) return 'AGG'", r"if \(caps\.aggregate\) return 'AGG'"),
     [r"if \(aggregateOffered && carriesRows\(AGGREGATE_BOOK\)\) return AGGREGATE_BOOK"]),
    ('E5', 'RESTORABLE', "the Model Breakdown header tint (HDR_ORANGE)",
     span(old_src, r"^const HDR_ORANGE = ", r"^const HDR_ORANGE = "),
     [r"^const HDR_ORANGE = 'rgba\(249, 115, 22, 0\.1\)'"]),
    ('E6', 'RESTORABLE', "the Model Breakdown group: its five <col> widths",
     span(old_src, r"\{/\* Model Breakdown \(5 columns\) - NOW FIRST \*/\}", CLOSE),
     [r"\{/\* Model Breakdown \(5 columns\) -- the Opal aggregate only, FIRST \*/\}", r"<col key=\{`mb-col-\$\{code\}`\} style=\{\{ width: '45px' \}\} />"]),
    ('E7', 'RESTORABLE', "the Model Breakdown group: its group header cell (colSpan 5)",
     span(old_src, r"<th colSpan=\{5\} ", CLOSE, back=1),
     [r"<th colSpan=\{MODEL_BREAKDOWN_CODES\.length\}", r"Model Breakdown - All of Opal</span>"]),
    ('E8', 'RESTORABLE', "the Model Breakdown group: its five column header cells UST ST INT LT ULT",
     span(old_src, r"\{/\* Model Breakdown - Orange \(only for AGG\) - NOW FIRST \*/\}", CLOSE),
     [r"<th key=\{`mb-th-\$\{code\}`\}"]),
    ('E9', 'RESTORABLE', "the Model Breakdown group: its five body cells (model_breakdown x 100 at one decimal, or '-')",
     span(old_src, MB_CMT, CLOSE, nth=1),
     [r"<td key=\{`mb-td-\$\{code\}`\}", r"breakdownCellText\(holding\.model_breakdown, code\)", r"return v \? \(v \* 100\)\.toFixed\(1\) : '-'"]),
    ('E10', 'RESTORABLE', "the Model Breakdown group: its five subtotal filler cells",
     span(old_src, MB_CMT, CLOSE, nth=2),
     [r"<td key=\{`mb-sub-\$\{code\}`\}"]),
    ('E11', 'RESTORABLE', "the Model Breakdown group: its five grand-total filler cells",
     span(old_src, MB_CMT, CLOSE, nth=3),
     [r"<td key=\{`mb-tot-\$\{code\}`\}"]),
    ('D1', 'DEAD', "aggregateWeighting (the client-side AUM weighting, its doc block)",
     (span(old_src, r"^ \* AGG aggregation weighting", r"^ \* AGG aggregation weighting")[0] - 1,
      span(old_src, r"^function aggregateWeighting\(", r"^\}$")[1]), []),
    ('D2', 'DEAD', "the aumByModel state",
     span(old_src, r"// AUM data for weighting AGG aggregation", r"const \[aumByModel, setAumByModel\]"), []),
    ('D3', 'DEAD', "the /api/general/portfolios/aum-metrics.json fetch (getAUMSummary)",
     span(old_src, r"// Fetch AUM data for weighting AGG aggregation", r"^  \}, \[\]\)$"), []),
    ('D4', 'DEAD', "the holdings AGG builder behind selectedPeriod !== 'Current' (selectedPeriod is a const 'Current')",
     span(old_src, r"// For AGG, aggregate holdings from all 5 portfolios weighted by AUM", r"^      return result$", nth=1), []),
    ('D5', 'DEAD', "the attribution AGG builder behind the same unreachable period branch",
     span(old_src, r"// For AGG, aggregate holdings from all 5 portfolios weighted by AUM", r"^      return result$", nth=2), []),
]

# The builders' closing brace sits one line after `return result`; carry it.
fixed = []
for e in elements:
    if e[0] in ('D4', 'D5'):
        fixed.append((e[0], e[1], e[2], (e[3][0], e[3][1] + 1), e[4]))
    else:
        fixed.append(e)
elements = fixed

# Overlap guard: no two element spans may share a line (attempt 1's defect).
for a in range(len(elements)):
    for b in range(a + 1, len(elements)):
        (s1, e1), (s2, e2) = elements[a][3], elements[b][3]
        if s1 <= e2 and s2 <= e1:
            sys.exit('BLOCKED: element spans overlap: %s :%d-%d and %s :%d-%d' % (elements[a][0], s1, e1, elements[b][0], s2, e2))

TOGGLE = r"selectedPortfolio === 'AGG' \? '' : 'rounded-tr-lg'"
NOT_AGG = [
    ('N1', "import lines the commit rewrote (getAUMSummary and getCanonicalModelName dropped with the dead code; HOLDINGS_VIEW_MODES added for persistence)",
     r"^import \{ (getPositioningData|displayModelName|resolveBooks)"),
    ('N2', "toggle persistence (viewMode useState -> usePersistentToggle; the selector onClick -> selectBook)",
     r"useState<'characteristics' \| 'performance'>|onClick=\{\(\) => setSelectedPortfolio\(portfolio\.id\)\}"),
    ('N3', "comment or blank lines (doc and inline comments the commit rewrote)",
     r"^\s*$|^\s*(//|/\*\*|\*|\{/\*)"),
    ('N4', "the NEIGHBOURING ETF CHARACTERISTICS group header's corner class toggle (not carried -- stated below)",
     TOGGLE),
]

assigned = {}
for eid, kind, what, (s, e), _ in elements:
    for o, _t in removed:
        if s <= o <= e and o not in assigned:
            assigned[o] = eid
for o, t in removed:
    if o in assigned:
        continue
    for nid, _what, pat in NOT_AGG:
        if re.search(pat, t):
            assigned[o] = nid
            break

print('')
print('DENOMINATOR: ' + REMOVAL + ' removed ' + str(len(removed)) + ' lines from ' + FILE)
counts = {}
for o, _t in removed:
    k = assigned.get(o, 'UNASSIGNED')
    counts[k] = counts.get(k, 0) + 1
for eid, kind, what, (s, e), _ in elements:
    print('  %-4s %-10s old :%d-%d  removed lines %d  %s' % (eid, kind, s, e, counts.get(eid, 0), what))
for nid, what, _ in NOT_AGG:
    print('  %-4s %-10s removed lines %d  %s' % (nid, 'NOT-AGG', counts.get(nid, 0), what))
unassigned = [(o, t) for o, t in removed if o not in assigned]
print('  UNASSIGNED removed lines: ' + str(len(unassigned)))
for o, t in unassigned:
    print('    old :' + str(o) + '  ' + t.strip())
print('  SUM: ' + ' + '.join('%s %d' % (k, counts[k]) for k in sorted(counts)) + ' = ' + str(sum(counts.values())) +
      ' of ' + str(len(removed)))
empty_elements = [e[0] for e in elements if counts.get(e[0], 0) == 0]
print('  elements whose span holds NO removed line (a span that missed): ' + (', '.join(empty_elements) if empty_elements else 'none'))

# ---- EACH ELEMENT BESIDE ITS COUNTERPART AT HEAD -----------------------------------------------------------------
print('')
print('ELEMENT BY ELEMENT (old = ' + REMOVAL + '^, HEAD = ' + head_sha[:10] + ')')
restorable = [e for e in elements if e[1] == 'RESTORABLE']
restored = 0
for eid, kind, what, (s, e), pats in elements:
    rem = [(o, t) for o, t in removed if assigned.get(o) == eid]
    print('')
    print('%s  %s  -- %s' % (eid, kind, what))
    shown = [x for x in rem if x[1].strip() and not re.match(r"^\s*(//|\*|/\*\*|\{/\*)", x[1])]
    for o, t in (shown if len(shown) <= 8 else shown[:4] + [(None, '... %d more code lines ...' % (len(shown) - 7))] + shown[-3:]):
        print('    REMOVED  ' + ('old :%-5s' % o if o else '         ') + ' ' + t.strip()[:150])
    if kind == 'DEAD':
        print('    NOT RESTORED -- dead code (the order: "were DEAD code and are NOT restored")')
        continue
    hits = []
    for p in pats:
        lines = find_all(head_src, p)
        hits.append((p, lines))
    ok = all(lines for _p, lines in hits)
    for p, lines in hits:
        if lines:
            for ln in lines[:3]:
                print('    HEAD     :%-5d  %s' % (ln, head_src[ln - 1].strip()[:150]))
        else:
            print('    HEAD     MISSING  /' + p + '/')
    print('    ' + ('RESTORED' if ok else 'NOT FOUND AT HEAD'))
    restored += 1 if ok else 0

# ORDER: the group is FIRST among the column groups in each of the four places it renders.
print('')
print('ORDER AT HEAD (the Model Breakdown line number before the first ETF Characteristics line of the same region):')
order_ok = 0
pairs = [
    ('colgroup', r"<col key=\{`mb-col-", r"\{/\* ETF Characteristics -- charColCount columns"),
    ('group header row', r"<th colSpan=\{MODEL_BREAKDOWN_CODES\.length\}", r"<th colSpan=\{charColCount\}"),
    ('column header row', r"<th key=\{`mb-th-", r"\{/\* ETF Characteristics - Green - NOW SECOND \*/\}"),
    ('body row', r"<td key=\{`mb-td-", r"\{/\* ETF Characteristics - NOW SECOND \*/\}"),
]
for name, mb, etf in pairs:
    a, b = find_all(head_src, mb), find_all(head_src, etf)
    good = bool(a and b and a[0] < b[0] and b[0] - a[0] < 15)
    order_ok += 1 if good else 0
    print('  %-18s Model Breakdown :%s  ETF Characteristics :%s  %s' % (name, a[:1], b[:1], 'FIRST' if good else 'NOT FIRST'))
codes_line = find_all(head_src, r"^const MODEL_BREAKDOWN_CODES = \['UST', 'ST', 'INT', 'LT', 'ULT'\] as const")
print('  column order: HEAD :%s  %s' % (codes_line[:1], head_src[codes_line[0] - 1].strip() if codes_line else 'MISSING'))

print('')
print('NOT CARRIED, stated (N4): the removed ETF CHARACTERISTICS group-header line carried a corner class toggle '
      '(`selectedPortfolio === \'AGG\' ? \'\' : \'rounded-tr-lg\'`, old :%s). It is a class on the NEIGHBOURING group, not a part '
      'of the Model Breakdown group: ETF CHARACTERISTICS is the rightmost group with or without the aggregate, so its top-right '
      'corner class stays as HEAD has it.' % find_all(old_src, TOGGLE)[:1])

print('')
print('RESTORED %d of %d (the elements that are not dead code: %s)' % (restored, len(restorable), ', '.join(e[0] for e in restorable)))

# ---- THE FORBIDDEN CLASSES --------------------------------------------------------------------------------------
def token_rx(t):
    return re.compile(r'(?<![A-Za-z0-9_:/-])' + re.escape(t) + r'(?![A-Za-z0-9_/.-])')


added = [(n, t) for s, _o, n, t in diff_lines(['diff', BASE, 'HEAD', '--', FILE]) if s == '+']
print('')
print('FORBIDDEN CLASSES in the restored hunks: the ' + str(len(added)) + ' added lines of `git diff ' + BASE + ' HEAD -- ' + FILE + '`')
total_forbidden = 0
for t in FORBIDDEN:
    c = sum(len(token_rx(t).findall(x)) for _n, x in added)
    total_forbidden += c
    print('  %-16s %d' % (t, c))
variants = sum(len(re.findall(r'(?<![A-Za-z0-9_:/-])text-white/\d+', x)) for _n, x in added)
print('  (beside them, text-white/<n> variants in the same lines: %d)' % variants)
print('  TOTAL %d' % total_forbidden)

mb_removed = [t for o, t in removed if assigned.get(o) in ('E6', 'E7', 'E8', 'E9', 'E10', 'E11')]
print('CONTROL -- the same counter over the ' + str(len(mb_removed)) + ' lines d53049a0 removed from the Model Breakdown group:')
control_total = 0
for t in FORBIDDEN:
    c = sum(len(token_rx(t).findall(x)) for x in mb_removed)
    control_total += c
    print('  %-16s %d' % (t, c))
print('  TOTAL %d (must be > 0: the counter can see the classes it is asked to count)' % control_total)

ok = (restored == len(restorable) and not unassigned and not empty_elements and total_forbidden == 0 and control_total > 0
      and order_ok == len(pairs) and not dirty)
print('')
print('VERDICT INPUTS: restored %d/%d, unassigned %d, empty spans %d, order FIRST %d/%d, forbidden %d, control %d, src clean %s -> %s'
      % (restored, len(restorable), len(unassigned), len(empty_elements), order_ok, len(pairs), total_forbidden, control_total,
         not dirty, 'MET' if ok else 'NOT MET'))
print('EXIT=' + ('0' if ok else '1'))
sys.exit(0 if ok else 1)
