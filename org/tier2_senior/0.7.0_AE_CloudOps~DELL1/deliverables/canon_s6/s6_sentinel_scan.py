"""Union of org/critical_paths/.open_deploys/ across every live worktree (git ls-tree HEAD), plus the shared working tree; prints the
per-tree denominator and every OPEN-ish sentinel naming the gold lambda or the code/scripts/gold prefix."""
from __future__ import annotations

import re
import subprocess

wts = [ln[9:] for ln in subprocess.run(['git', 'worktree', 'list', '--porcelain'], capture_output=True, text=True).stdout.splitlines() if ln.startswith('worktree ')]
names: dict = {}
per_tree = []
for w in wts:
    r = subprocess.run(['git', '-C', w, 'ls-tree', '-r', '--name-only', 'HEAD', 'org/critical_paths/.open_deploys/'], capture_output=True, text=True)
    fl = [n for n in r.stdout.split() if n.endswith('.json')]
    per_tree.append(len(fl))
    for n in fl:
        names.setdefault(n, w)
print('worktrees', len(wts), 'per-tree json counts min/max', min(per_tree), max(per_tree), 'union files', len(names))
pat = re.compile(r'mdpf-gold-lambda|code/scripts/gold|opal-assets-daily-emitter|MDPF_GOLD_COMMIT')
hits = []
for n, w in sorted(names.items()):
    b = subprocess.run(['git', '-C', w, 'show', 'HEAD:' + n], capture_output=True).stdout.decode('utf-8', 'replace')
    st = re.search(r'"status"\s*:\s*"([^"]*)"', b)
    if pat.search(b):
        hits.append((n.split('/')[-1], st.group(1) if st else '?', w))
print('sentinels naming the gold lambda / code prefix / emitter:', len(hits))
for h in hits:
    print('  ', h)
