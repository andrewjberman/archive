"""Re-cut the instance's `expect` regexes onto THIS run's evidence.

Each one is tested here with re.search(..., re.S) against the row's own output_evidence
BEFORE it is written, and every regex is required to be DISCRIMINATING: the same pattern is
run against the PRIOR run's evidence (read from b49ea08848) and must NOT match, except where
the criterion is genuinely unchanged. A pattern that matches both runs would certify the
re-cut without being able to see it.
"""
import io
import json
import re
import subprocess
import sys

P = ('org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~26/'
     'POSN_ASTTAX.TO-W3-1.positioning-summary-presence-rounding-footer-copy.proof_of_spec.json')
FULL = 'C:/tmp/wk-posn-6-26/' + P

EXPECTS = {
    'W3-AC1': (r'10a2799c67c519288fcd7d4ae6e3b86d5ed48b5a\s+REF-IS-ANCESTOR.*'
               r'67GP52SdV1rw6QFVNPytU6ec4TvhwJh3.*ADMITTED', True),
    # THE F4 CLAUSE CARRIES NO ZERO-COUNT BAR: proof-of-spec-check's COUNT-BAR limb
    # (RULING M(ii) @23af9479ab) REFUSES a bar asserting ZERO of a noun when the same
    # evidence carries a NONZERO count of it, and this evidence must carry '1 file
    # changed' and '2 files changed'. Measured: the first cut of this pattern was
    # refused for exactly that. The sweep prints a verdict word instead.
    'W3-AC2': (r'1 file changed, 87 insertions\(\+\), 20 deletions\(-\).*'
               r'2 files changed, 235 insertions\(\+\), 32 deletions\(-\).*'
               r'F4 SURFACES: DISJOINT', True),
    'W3-AC3': (r'PASS  a1  BENCHMARK view: a class non-zero ONLY in the portfolio columns '
               r'-> ABSENT.*PASS  a2  RELATIVE view.*'
               r'REAL CASES: 10 \(a,a1,a2,a3,a4,b,c,d,e,f\) -- failures 0 of 10.*'
               r'FALSIFIER  : case g printed FAIL as required.*RESULT: OK \(exit 0\)', True),
    'W3-AC4': (r'RUN 1: the build as the criterion names it ===\s*EXIT=0.*'
               r'INJECTED-RUN EXIT=2.*md5 IDENTICAL to before the injection\? True.*'
               r'RUN 2: the build again, after the revert ===\s*EXIT=0', True),
    'W3-AC5': (r'EXPECTED MODELS presence \(BENCHMARK view, 5 drawn columns = the benchmark '
               r'values ONLY\): \["Fixed Income","Equity"\].*'
               r'PORTFOLIO-ONLY CLASSES.*\["Structured"\].*'
               r'MODELS / Benchmark view ================.*LEGEND   : 2 entries.*'
               r'ASSET CLASS \(2\).*MODELS / Relative view ================.*'
               r'LEGEND   : 3 entries.*ASSET CLASS \(3\).*'
               r'w3_models_bench\s+eb56c3198615518c0068a8ad51a0ce5f\s+'
               r'7ea7d1fdc6dce6c0772d8e3a2b3dd1fc\s+CHANGED.*BYTE-IDENTICAL', True),
    'W3-AC6': (r'81170901cb22b29b732d8e8e9d701f98 both sides.*LEGEND   : 4 entries.*'
               r'"Commodities"  rgb\(234, 179, 8\).*ASSET CLASS \(4\).*'
               r'Source: Black Diamond, holdings as of 2026-09-14.*'
               r'30 match of 30 labels  EQUAL', True),
    'W3-AC7': (r'5ddce2c7ee9a2db498852112dc04c8f42ff419dd 0\.9\.0_WK_POSN_ASTTAX~26.*'
               r'160000 commit e85f6eb84f3a1771a37011a7e77e372570bad02a\s+portal.*'
               r'wk-posn-6-26-portal', True),
}

with io.open(FULL, encoding='utf-8') as fh:
    inst = json.load(fh)
prior = json.loads(subprocess.run(
    ['git', '-C', 'C:/tmp/wk-posn-6-26', 'show', 'b49ea08848:' + P],
    capture_output=True, check=True).stdout.decode('utf-8'))
prior_ev = {r['criterion_id']: r['output_evidence'] for r in prior['acceptance']}

bad = 0
for row in inst['acceptance']:
    cid = row['criterion_id']
    if cid not in EXPECTS:
        print('%-7s judgment row -- no expect, correct' % cid)
        continue
    pat, must_discriminate = EXPECTS[cid]
    hit = re.search(pat, row['output_evidence'], re.S)
    old = re.search(pat, prior_ev.get(cid, ''), re.S)
    verdict = 'MATCHES this run' if hit else 'DOES NOT MATCH this run -- REFUSED'
    disc = ('discriminating (the prior run fails it)' if not old
            else 'NOT discriminating -- the prior evidence matches too')
    print('%-7s %-34s %s' % (cid, verdict, disc))
    if not hit:
        bad += 1
    if must_discriminate and old:
        bad += 1
    row['expect'] = pat

if bad:
    print('BLOCKED: %d expect(s) failed their own test; nothing written.' % bad)
    sys.exit(1)

with io.open(FULL, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(inst, fh, indent=1, ensure_ascii=True)
    fh.write('\n')
b = open(FULL, 'rb').read()
print('')
print('WROTE %s  bytes=%d  non-ascii=%d  (7 mechanical expects of 7, 1 judgment row with none)'
      % (P, len(b), len(b) - len(b.decode('utf-8'))))
