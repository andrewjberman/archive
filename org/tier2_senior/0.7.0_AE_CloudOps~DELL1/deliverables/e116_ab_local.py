"""TO-SC-e116b control: run the BASE and the NEW E_18 locally in plan form (upload False: reads only, no table or S3 write) on the same
latest holdings file, and print only the summary-count lines. Run from the repo root with python -I.
  python -I e116_ab_local.py <base_file> <new_file>
"""
from __future__ import annotations

import contextlib
import io
import os
import re
import sys

GOLD = os.path.join(os.getcwd(), 'data', 'black_diamond', 'scripts', 'gold')
sys.path.insert(0, GOLD)
real = os.path.join(GOLD, 'E_18.detect_new_securities.py')
KEEP = re.compile(r'Loading holdings from|Already resolved|Held out by|Scheduled-classification candidates|Scheduled rows written|Truly unresolved')


def run(path: str) -> list:
    src = open(path, encoding='utf-8').read()
    ns = {'__file__': real, '__name__': 'e18_ab'}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, real, 'exec'), ns)
        ns['detect_new_securities'](upload=False)
    return [ln.strip() for ln in buf.getvalue().splitlines() if KEEP.search(ln)]


base, new = run(sys.argv[1]), run(sys.argv[2])
print('BASE:', *base, sep='\n  ')
print('NEW :', *new, sep='\n  ')
key = lambda r: [ln for ln in r if not ln.startswith('Held out') and 'held out' not in ln]  # noqa: E731
print('AB-COUNTS-EQUAL', key(base) == key(new))
