import collections
import json
import sys
g = json.load(open(sys.argv[1], 'rb'))
root = sys.argv[2].replace('\\', '/')
cl = json.load(open(sys.argv[3], 'rb'))
mods = {k.replace('\\', '/'): v for k, v in g['modules'].items()}
def n(s):
    return s.replace('\\', '/')

ENTRY = root + '/' + cl['entry']
closure = set(cl['closure_files'])
for f in ['src/pages/InvestorReporting/render/analysis/AnalysisDocument.tsx', 'src/pages/InvestorReporting/render/PrintEntry.tsx',
          'src/pages/InvestorReporting/export/resolveBundle.ts']:
    print('POSITIVE', f, f in closure)
for f in ['src/pages/InvestorReporting/tabs/holdings/HoldingsTab.tsx', 'src/pages/InvestorReporting/tabs/analysis/OwnedRequestHistory.tsx',
          'src/pages/InvestorReporting/index.tsx']:
    print('NEGATIVE', f, 'in_build_graph=' + str((root + '/' + f) in mods), 'in_closure=' + str(f in closure))
# shortest import path from the entry to each changed-in-closure file
def bfs(entry):
    parent = {entry: None}
    queue = collections.deque([entry])
    while queue:
        cur = queue.popleft()
        for imp in mods[cur]['s'] + mods[cur]['d']:
            dest = n(imp)
            if dest in mods and dest not in parent:
                parent[dest] = cur
                queue.append(dest)
    return parent


prev = bfs(ENTRY)
for f in cl['changed_in_module_closure']:
    p, m = [], root + '/' + f
    while m:
        p.append(m[len(root) + 1:])
        m = prev[m]
    print('PATH', ' <- '.join(p[::-1]))
