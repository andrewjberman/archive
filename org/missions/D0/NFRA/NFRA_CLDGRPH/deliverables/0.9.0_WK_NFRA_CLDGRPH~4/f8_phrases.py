"""F8-AC1 -- the dead-engine phrase census BY SOURCE over the regenerated carriers + the checker.

NFRA_CLDGRPH.TO-CG-F-8 / cell CG-s-28, 0.9.0_WK_NFRA_CLDGRPH~4.

WHY BY SOURCE. Three of the four scanned files are GENERATED. A raw hit count over a generated
file answers the wrong question: it cannot say WHICH upstream literal put the string there, and
this order owns exactly one of the two upstreams. So every hit is attributed:

  generator            -- the string is a literal in .tools/gen_tool_classification.py (REFRESH);
                          THIS ORDER'S surface, must read 0.
  manifest-entry:<id>  -- the string is a field of an entry in graph-call-manifest.yaml, which
                          .tools/tool_index.py embeds VERBATIM as MANIFEST_DOC. The manifest is
                          OUTSIDE this order's <paths> (it is E-1's / CG-s-17's surface), so this
                          count is expected NON-ZERO and is carried by a surprise row, not edited.
  other:<file:line>    -- neither; a hit nobody in this census owns. Printed loud.
  CHECKER              -- org/modules/graph/manifest_check_cli.py, an ordinary source file.

THE PHRASE LITERALS ARE BUILT FROM FRAGMENTS ON PURPOSE: this probe lives in the repo corpus, and
a probe that carries the retired phrase verbatim adds a hit to every future census of it.

CONTROL (a detector that cannot return non-zero on a positive is a constant): the whole scan is
re-run against a TEMPORARY copy of the tree in which the phrase is planted BACK into the generator
literal AND into a generated carrier. GENERATOR_SOURCED_HITS must go non-zero there or the zero
above is worthless. Nothing under the repo is written.
"""
import os
import re
import shutil
import sys
import tempfile

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..', '..', '..', '..', '..', '..'))

GEN_REL = os.path.join('.tools', 'gen_tool_classification.py')
MANIFEST_REL = os.path.join('org', 'modules', 'graph', 'graph-call-manifest.yaml')
CHECKER_REL = os.path.join('org', 'modules', 'graph', 'manifest_check_cli.py')
CARRIERS_REL = [
    os.path.join('.tools', 'tool_index.py'),
    os.path.join('.tools', 'TOOL_CLASSIFICATION.yaml'),
    os.path.join('org', 'modules', 'graph', 'TOOL_MASTER.yaml'),
]

# fragment-built -- see module docstring
_A = 'auto-refresh' + ' on HEAD-advance'
_B = 'auto-refreshes' + ' on HEAD-advance'
_C = 'canonical persisted' + ' Kuzu DB'
PHRASES = [_A, _B, _C]


def read(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def hits(text):
    """(line_no, phrase, line_text) for every phrase occurrence. A line with two phrases counts
    twice -- the unit is the OCCURRENCE, not the line."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for p in PHRASES:
            for _ in range(line.count(p)):
                out.append((n, p, line.strip()))
    return out


def manifest_phrase_owners(manifest_path):
    """entry id -> set(phrases) for every entry of graph-call-manifest.yaml that carries one.

    Walks the parsed doc and attributes each string to the NEAREST ENCLOSING dict that has an
    'id' key -- the manifest's entry grain."""
    doc = yaml.safe_load(read(manifest_path)) or {}
    owners = {}

    def walk(node, owner):
        if isinstance(node, dict):
            own = str(node['id']) if isinstance(node.get('id'), str) else owner
            for v in node.values():
                walk(v, own)
        elif isinstance(node, list):
            for v in node:
                walk(v, owner)
        elif isinstance(node, str):
            for p in PHRASES:
                if p in node:
                    owners.setdefault(owner or '(no enclosing id)', set()).add(p)

    walk(doc, None)
    return owners


def manifest_doc_region(index_text):
    """(start_line, end_line) of tool_index.py's MANIFEST_DOC literal, or None.

    tool_index.py is emitted as: TOOLS = ..., MANIFEST_DOC = ..., LEDGER_DOC = ...  -- so the
    region is bounded by the two assignment lines."""
    start = end = None
    for n, line in enumerate(index_text.splitlines(), 1):
        if re.match(r'^MANIFEST_DOC\s*=', line):
            start = n
        elif start is not None and re.match(r'^[A-Z_]+\s*=', line) and end is None:
            end = n - 1
    if start is None:
        return None
    return (start, end if end is not None else len(index_text.splitlines()))


def scan(root):
    gen_text = read(os.path.join(root, GEN_REL))
    manifest_path = os.path.join(root, MANIFEST_REL)
    owners = manifest_phrase_owners(manifest_path)
    gen_phrases = {p for p in PHRASES if p in gen_text}

    rows = []
    for rel in CARRIERS_REL:
        path = os.path.join(root, rel)
        text = read(path)
        region = manifest_doc_region(text) if rel.endswith('tool_index.py') else None
        for (n, p, line) in hits(text):
            src = None
            if region and region[0] <= n <= region[1]:
                for eid, ps in sorted(owners.items()):
                    if p in ps:
                        src = 'manifest-entry:%s' % eid
                        break
            if src is None and p in gen_phrases:
                src = 'generator'
            if src is None:
                for eid, ps in sorted(owners.items()):
                    if p in ps:
                        src = 'manifest-entry:%s' % eid
                        break
            if src is None:
                src = 'other:%s:%d' % (rel.replace(os.sep, '/'), n)
            rows.append({'file': rel.replace(os.sep, '/'), 'line': n, 'phrase': p,
                         'source': src, 'text': line[:150]})

    checker_rows = []
    ctext = read(os.path.join(root, CHECKER_REL))
    for (n, p, line) in hits(ctext):
        checker_rows.append({'file': CHECKER_REL.replace(os.sep, '/'), 'line': n, 'phrase': p,
                             'source': 'CHECKER', 'text': line[:150]})
    return rows, checker_rows, owners


def control(tmproot):
    """Positive control: plant the phrase back into the generator literal AND a generated carrier
    inside a COPY of the tree, then re-run the same scan function."""
    for rel in [GEN_REL, MANIFEST_REL, CHECKER_REL] + CARRIERS_REL:
        dst = os.path.join(tmproot, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, rel), dst)

    gp = os.path.join(tmproot, GEN_REL)
    with open(gp, 'a', encoding='utf-8') as fh:
        fh.write("\n_F8_CONTROL_PLANT = '%s'  # planted by f8_phrases.py control\n" % _A)

    cp = os.path.join(tmproot, '.tools', 'TOOL_CLASSIFICATION.yaml')
    with open(cp, 'a', encoding='utf-8') as fh:
        fh.write('\n_f8_control_plant:\n  refresh_mechanism: %s\n' % _A)

    rows, checker_rows, _ = scan(tmproot)
    planted = [r for r in rows if r['source'] == 'generator']
    return planted


def main():
    rows, checker_rows, owners = scan(ROOT)
    total = len(rows) + len(checker_rows)

    print('PHRASE CENSUS BY SOURCE -- NFRA_CLDGRPH CG-s-28 (F8-AC1)')
    print('  root            : %s' % ROOT)
    print('  phrases         : %d (fragment-built; see the module docstring)' % len(PHRASES))
    print('  files scanned   : %d = 3 regenerated carrier(s) + 1 checker' % (len(CARRIERS_REL) + 1))
    for rel in CARRIERS_REL + [CHECKER_REL]:
        print('      %s' % rel.replace(os.sep, '/'))
    print('  manifest entries carrying a phrase (the OUT-OF-GRANT upstream): %d' % len(owners))
    for eid, ps in sorted(owners.items()):
        print('      %s -- %s' % (eid, ', '.join(sorted(ps))))
    print('')
    print('  HITS (%d):' % total)
    for r in rows + checker_rows:
        print('      %s:%d  source=%s' % (r['file'], r['line'], r['source']))
        print('        | %s' % r['text'])
    if total == 0:
        print('      (none)')
    print('')

    gen_hits = [r for r in rows if r['source'] == 'generator']
    man_hits = [r for r in rows if r['source'].startswith('manifest-entry:')]
    oth_hits = [r for r in rows if r['source'].startswith('other:')]

    print('GENERATOR_SOURCED_HITS=%d of %d hits' % (len(gen_hits), total))
    print('CHECKER_HITS=%d' % len(checker_rows))
    if man_hits:
        ids = sorted({r['source'] for r in man_hits})
        carried = 'row NFRA_CLDGRPH-W4-S1 -- ' + ' + '.join(ids)
    else:
        carried = 'NONE'
    print('MANIFEST_SOURCED_HITS=%d (%s)' % (len(man_hits), carried))
    print('OTHER_SOURCED_HITS=%d%s' % (len(oth_hits),
                                       '' if not oth_hits else ' -- ' + ', '.join(
                                           r['source'] for r in oth_hits)))

    tmproot = tempfile.mkdtemp(prefix='f8_phrase_control_')
    try:
        planted = control(tmproot)
    finally:
        shutil.rmtree(tmproot, ignore_errors=True)
    fired = len(planted) >= 1
    print('PHRASE_PROBE_CONTROL=%s -- phrase planted into a COPY of gen_tool_classification.py '
          'AND of TOOL_CLASSIFICATION.yaml; GENERATOR_SOURCED_HITS there = %d (>=1 required). '
          'The 0 above is a measurement, not a constant.'
          % ('FIRED' if fired else 'DID-NOT-FIRE', len(planted)))

    rc = 0 if (not gen_hits and not checker_rows and not oth_hits and fired) else 1
    print('RC=%d' % rc)
    return rc


if __name__ == '__main__':
    sys.exit(main())
