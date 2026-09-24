import glob
import json
import os
import re
import sys

S = os.path.dirname(os.path.abspath(sys.argv[1])) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, 'census_all.json')))
cs = d['commits']
by_code = {}
for c in cs:
    codes = set(re.findall(r'\b([A-Z]{4}_[A-Z0-9]{3,16})\b', c['s']))
    for f in c['files']:
        m = re.match(r'org/missions/D\d+/[^/]+/([A-Z0-9_]+)/', f[0])
        if m:
            codes.add(m.group(1))
    for k in codes:
        by_code.setdefault(k, []).append(c)

out = []
for pj in glob.glob('org/missions/D*/*/*/project.json'):
    pj = pj.replace(os.sep, '/')
    try:
        j = json.load(open(pj, encoding='utf-8'))
    except Exception:
        continue
    code = pj.split('/')[4]
    base = pj.rsplit('project.json', 1)[0]
    st = j.get('dep_stage') or j.get('status')
    grades = glob.glob(base + 'ledger/COMPLETION_GRADES*.json')
    rounds = glob.glob(base + 'ledger/ROUND_ANALYSIS*')
    tos = glob.glob(base + 'task-orders/*.md')
    tob = sum(os.path.getsize(t) for t in tos)
    mine = by_code.get(code, [])
    if not mine:
        continue
    prod = [c for c in mine if any(f[3] == 'PRODUCT' for f in c['files'])]
    pl = sum(f[1] + f[2] for c in prod for f in c['files'] if f[3] == 'PRODUCT')
    first = min(c['t'] for c in mine)
    last = max(c['t'] for c in mine)
    lp = max((c['t'] for c in prod), default='-')
    out.append((code, str(st), len(mine), len(prod), pl, len(tos), tob // 1024, len(rounds), len(grades), first[:10], last[:10], lp[:10]))
out.sort(key=lambda r: -r[2])
print('code | stage | commits | prod commits | prod lines | TO files | TO KB | round analyses | grade files | first | last | last prod')
for r in out[:45]:
    print('  %-18s %-11s %5d %4d %6d %4d %5d %3d %3d %s %s %s' % r)
print('projects with commits since June:', len(out), ' with ZERO product commits:', sum(1 for r in out if r[3] == 0))
tot_c = sum(r[2] for r in out)
tot_p = sum(r[3] for r in out)
print('sum commits', tot_c, 'sum prod commits', tot_p)
