"""V8-AC9 -- DURABILITY: a routine re-seed CANNOT undo the retag, proved on the arm
that can fail.

WHAT THIS RUNS. TO-V3-1's guarded seeder
(data/black_diamond/scripts/classification/seed_canonical_securities.py) on its
UPLOAD ARM -- seed(upload=True, sync_yang=True) -- against a SCRATCH copy of the
POST-RETAG table built from V8-AC6's read (r1_after.json). The DRY-RUN arm was
refused at the cut and is refused here too: its conflict list is [] before any
comparison (`if upload else []` at :295), so 0 PRESERVED is the only value that arm
can emit -- an instrument with no failing branch (row W21-S1).

THE LIVE TABLE IS NEVER OPENED. boto3 is replaced in sys.modules before any seeder
byte executes: boto3.client() raises, boto3.resource('dynamodb').Table(name) returns
an in-process dict and prints the name it intercepted. The machinery is round 4's,
re-used unmodified through slot ~21's harness (v3_mutant_control_re.py), whose own
module-level assertion pins the machinery at sha256 ae72cab7dfbeb62f.

THE SUBJECT IS RESOLVED BY CONTENT, NOT BY FILENAME -- and it has to be. This
worktree is a SPARSE CONE (13 directories; `data/` is not one of them), so the
seeder's path carries the sparse bit and does not exist on disk; the harness's
applied_bytes() reads the working tree and cannot see it. The bytes are therefore
taken from the object store at HEAD and pinned by BLOB HASH:
  HEAD:...seed_canonical_securities.py    = 803721e2c15464ed4ba054a02aba2311d5506164
  8cad052620~1:...  (round 4's subject)   = fbbc7165d33198789d3a7788a557ed3f5ce75614
The two differ, and 8cad052620 is 'POSN_ASTTAX TO-V3-1 (AT5-s-3): APPLY round 4's
preserve-don't-clobber guard', so the bytes under test are PROVABLY the guarded ones
and not the pre-patch ones. That is a stronger resolution than reading a filename,
not a weaker one. Surfaced as row POSN_ASTTAX-Z-W19-S14.

THE POSITIVE CONTROL, so a refusal is not mistaken for a broken import: the same
harness is run a second time against a PRE-RETAG scratch table (r1_before.json). The
guard must NOT refuse there on the asset_class field -- the seeder's own two-value
vocabulary agrees with the pre-retag rows on the members it carries -- which is what
makes the post-retag refusal a measurement of the RETAG rather than of the guard's
mere existence.

Usage: python .../v8_ac9_guard_vs_retag.py
Exit: 0 = the upload arm REFUSES rc=1 on the post-retag table with a [PRESERVED] line
for every member whose seeder value disagrees; 1 otherwise.
"""
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'org/missions/D4/POSN/POSN_ASTTAX/deliverables')
HARNESS = os.path.join(HERE, '0.9.0_WK_POSN_ASTTAX~21/v3_mutant_control_re.py')
AFTER = os.path.join(HERE, '0.9.0_WK_POSN_ASTTAX~19/r1_after.json')
BEFORE = os.path.join(HERE, '0.9.0_WK_POSN_ASTTAX~19/r1_before.json')
SUBJECT = 'data/black_diamond/scripts/classification/seed_canonical_securities.py'
HEAD_BLOB = '803721e2c15464ed4ba054a02aba2311d5506164'
PRE_PATCH_BLOB = 'fbbc7165d33198789d3a7788a557ed3f5ce75614'

THIRTEEN = ['DBC', 'GLD', 'GSG', 'IAU', 'SLV', 'USO', 'PDBC',
            'VXX', 'VIXY', 'UVXY', 'QBER', 'JEPI', 'VNQ']


def load_rows(path):
    with open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    rows = {}
    for item in doc['Items']:
        rows[item.get('ticker', {}).get('S')] = {
            k: v.get('S') for k, v in item.items() if 'S' in v}
    return doc, rows


def subject_bytes():
    """BY CONTENT: the blob at HEAD, pinned by hash, never by filename."""
    sha = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD:' + SUBJECT]).decode().strip()
    raw = subprocess.check_output(['git', 'show', 'HEAD:' + SUBJECT])
    if sha != HEAD_BLOB:
        print('BLOCKED: HEAD blob %s is not the pinned subject %s' % (sha, HEAD_BLOB))
        sys.exit(1)
    if sha == PRE_PATCH_BLOB:
        print('BLOCKED: the subject IS the pre-patch blob -- the guard is absent')
        sys.exit(1)
    return raw.decode('utf-8'), sha


def main():
    print('=' * 100)
    print('V8-AC9 -- THE GUARD BETWEEN A ROUTINE RE-SEED AND THE RETAG')
    print('=' * 100)

    spec = importlib.util.spec_from_file_location('v3harness', HARNESS)
    v3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v3)          # asserts the round-4 machinery sha256
    ac1 = v3.ac1
    print('  harness        : %s' % HARNESS)
    print('  machinery      : %s (sha256 %s asserted at import)'
          % (v3.MACHINERY, v3.MACHINERY_SHA256))
    print('  scratch tables : %r (yang) and %r (bd) -- in-process dicts'
          % (ac1.YANG_TABLE, ac1.BD_TABLE))

    src, sha = subject_bytes()
    print('  subject        : %s' % SUBJECT)
    print('                   blob %s, %d bytes, resolved BY CONTENT from HEAD'
          % (sha, len(src.encode('utf-8'))))
    print('                   pre-patch blob for comparison: %s (DIFFERS: %s)'
          % (PRE_PATCH_BLOB, sha != PRE_PATCH_BLOB))
    print('  sparse cone    : %s does not exist on disk (git ls-files -t reports S)'
          % SUBJECT)

    adoc, after = load_rows(AFTER)
    bdoc, before = load_rows(BEFORE)
    print('  post-retag read: r1_after.json, Count %s == ScannedCount %s'
          % (adoc.get('Count'), adoc.get('ScannedCount')))
    print('')

    # ---- which members of the thirteen does the seeder actually carry? -----
    secs = ac1.canonical_securities(src)
    by_ticker = {s['ticker']: s for s in secs}
    carried = [t for t in THIRTEEN if t in by_ticker]
    print('DENOMINATOR -- the seeder carries %d securities; of the thirteen it carries '
          '%d: %s' % (len(secs), len(carried), ','.join(carried)))
    print('the remaining %d of 13 are absent from the seeder and CANNOT be reverted by '
          'it: %s' % (13 - len(carried),
                      ','.join(t for t in THIRTEEN if t not in by_ticker)))
    print('')
    print("THE SEEDER'S OWN VALUE vs THE RETAGGED TABLE, per carried member")
    print('  %-6s %-16s %-16s %-16s %s'
          % ('ticker', 'seeder says', 'table NOW says', 'table BEFORE said', 'disagrees'))
    disagree = []
    for t in carried:
        sv = by_ticker[t]['asset_class']
        tv = after[t]['asset_class']
        bv = before[t]['asset_class']
        d = sv != tv
        if d:
            disagree.append(t)
        print('  %-6s %-16s %-16s %-16s %s' % (t, sv, tv, bv, 'YES' if d else 'no'))
    print('  members whose seeder value DISAGREES with the retagged table: %d of %d'
          % (len(disagree), len(carried)))
    print('')

    def builder(rows, label):
        # THE DOMAIN IS THE CLAIM'S POPULATION, NOT THE HARNESS'S.
        # Round 4's ac1.RETAG names four tickers; this criterion's population is THE
        # THIRTEEN. Building the scratch store over ac1.RETAG silently drops JEPI --
        # the seeder carries it, so with no row in the store the seeder MINTS it and
        # the guard has nothing to preserve, i.e. the one member the round-5 PRD added
        # would have gone ungraded with every arm reading green. The store is
        # therefore built over THIRTEEN intersected with the seeder's own securities,
        # which is a superset of ac1.RETAG's members.
        def build(by_t, mint_probe):
            store = {}
            for ticker in THIRTEEN:
                if ticker not in by_t or ticker not in rows or ticker == mint_probe:
                    continue
                live = rows[ticker]
                sec = by_t[ticker]
                store[ticker] = {
                    'ticker': ticker,
                    'asset_class': live.get('asset_class'),
                    'sub_asset_class': live.get('sub_asset_class'),
                    'name': sec['name'],
                    'management_style': live.get('management_style', 'passive'),
                    'sector': live.get('sector', 'Broad'),
                    'last_updated': live.get('last_updated', '2026-09-14T00:00:00Z'),
                    'updated_by': live.get('updated_by', 'posn-asttax-retag'),
                }
            assert mint_probe not in store
            return store
        build.__doc__ = label
        return build

    results = {}
    for label, rows in (('POST-RETAG (r1_after.json) -- the arm under test', after),
                        ('PRE-RETAG (r1_before.json) -- the positive control', before)):
        r = v3.run(src, 'V8-AC9 upload arm, scratch table built from %s' % label,
                   store_builder=builder(rows, label))
        results[label] = r
        print('=' * 100)
        print('ARM: %s' % label)
        print('=' * 100)
        for ln in r['intercepts']:
            print('  ' + ln)
        print('  rc = %r   raised = %s' % (r['rc'], r['err'] or 'none'))
        print('  scratch get_item (pre-read) count: %d   update_item count: %d   '
              'minted: %d' % (r['yang_reads'], r['yang_writes'], r['yang_minted']))
        print('  MINT CONTROL: %r %s' % (r['mint_probe'],
              'MINTED -- the seeder IS writing' if r['minted']
              else 'NOT MINTED -- a refusal here says nothing'))
        print('  %-6s %-16s %-16s %-16s %s'
              % ('ticker', 'scratch BEFORE', 'scratch AFTER', 'seeder would set',
                 'verdict'))
        for t in r['present']:
            b = r['before'][t]['asset_class']
            a = r['after'][t]['asset_class']
            print('  %-6s %-16s %-16s %-16s %s'
                  % (t, b, a, by_ticker[t]['asset_class'],
                     'SURVIVED' if a == b else 'CLOBBERED'))
        print('  SURVIVED %d of %d | CLOBBERED %d'
              % (len(r['survived']), len(r['present']), len(r['clobbered'])))
        for ln in r['refused_lines']:
            print('  ' + ln)
        print('  [PRESERVED] lines: %d' % len(r['preserved_lines']))
        for ln in r['preserved_lines']:
            print('    ' + ln)
        print('')

    post = results['POST-RETAG (r1_after.json) -- the arm under test']
    pre = results['PRE-RETAG (r1_before.json) -- the positive control']

    print('=' * 100)
    print('V8-AC9 VERDICT')
    print('=' * 100)
    pres_tickers = set()
    for ln in post['preserved_lines']:
        for t in carried:
            if (' %s ' % t) in ln or ('%s:' % t) in ln or ("'%s'" % t) in ln:
                pres_tickers.add(t)
    covered = sorted(set(disagree) & pres_tickers)
    print('  upload arm on the POST-RETAG table : rc=%r, %d [PRESERVED] line(s), '
          'CLOBBERED %d of %d' % (post['rc'], len(post['preserved_lines']),
                                  len(post['clobbered']), len(post['present'])))
    print('  positive control, PRE-RETAG table  : rc=%r, %d [PRESERVED] line(s), '
          'CLOBBERED %d of %d' % (pre['rc'], len(pre['preserved_lines']),
                                  len(pre['clobbered']), len(pre['present'])))
    print('  the two arms DIFFER                : %s'
          % (post['rc'] != pre['rc'] or
             len(post['preserved_lines']) != len(pre['preserved_lines'])))
    print('  members that disagree with the retagged table: %d (%s)'
          % (len(disagree), ','.join(disagree)))
    print('  of those, named in a [PRESERVED] line        : %d (%s)'
          % (len(covered), ','.join(covered)))
    print('  get_item count > 0                          : %s (%d)'
          % (post['yang_reads'] > 0, post['yang_reads']))

    ok = (post['rc'] == 1 and post['yang_reads'] > 0
          and len(post['clobbered']) == 0
          and len(covered) == len(disagree) and disagree)
    print('')
    print('  RESULT: %s' % ('PASS -- the guard PROVABLY stands between a routine '
                            're-seed and the retag' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
