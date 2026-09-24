"""Commit census: classify every non-merge commit on the current branch in a window by the paths it touches.

Usage: python census.py <since> <until> <out_json>
Classes per path (first match wins):
  PRODUCT   -- application/pipeline/infra code: code extension, outside org/, docs/, .tools/, .claude/, rcg/
  TOOLING   -- process tooling code: code extension under .tools/, .claude/, org/mcp/, org/modules/
  GOV_TO    -- task orders (any */task_orders/*)
  GOV_SURP  -- surprise channel / adjudication / remediation files
  GOV_LOG   -- session logs (*/logs/*)
  GOV_MSG   -- inbox / message archive / audit logs / telemetry (org/mcp non-code, *.log, *.jsonl under org/)
  GOV_REC   -- every other org/ path (records, deliverables, ledgers, PRD sign-offs, project.json, registers)
  DOCS      -- docs/ (PRDs, doctrine, architecture)
  LAW       -- CLAUDE.md, org/XXX.md, AGENTS.md
  DATA      -- data/config files outside org/ (json/yaml/csv/md outside the above)
  OTHER
"""
import json
import re
import subprocess
import sys
from collections import Counter

CODE_EXT = {'.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.sh', '.ps1', '.tf', '.sql', '.go', '.rs',
            '.css', '.html', '.vue', '.psm1', '.bat', '.cmd', '.hcl'}


def ext(p):
    m = re.search(r'(\.[A-Za-z0-9]+)$', p)
    return m.group(1).lower() if m else ''


def classify(p):
    pl = p.lower()
    e = ext(p)
    if p in ('CLAUDE.md', 'org/XXX.md', 'AGENTS.md') or p.endswith('/CLAUDE.md'):
        return 'LAW'
    if '/task_orders/' in pl:
        return 'GOV_TO'
    if 'surprise-channel/' in pl or 'surprise_channel/' in pl or '/adjudications/' in pl or 'remediation' in pl.split('/')[-1].lower():
        return 'GOV_SURP'
    if pl.startswith(('.tools/', '.claude/', 'org/mcp/', 'org/modules/')) and e in CODE_EXT:
        return 'TOOLING'
    if pl.startswith(('.claude/',)):
        return 'TOOLING_DOC'  # skills text, settings
    if '/logs/' in pl and pl.startswith('org/'):
        return 'GOV_LOG'
    if pl.startswith('org/mcp/') or (pl.startswith('org/') and (e in ('.log', '.jsonl'))):
        return 'GOV_MSG'
    if pl.startswith('org/') or pl.startswith('rcg/'):
        return 'GOV_REC'
    if pl.startswith('docs/'):
        return 'DOCS'
    if pl.startswith('.tools/'):
        return 'TOOLING_DOC'
    if e in CODE_EXT:
        return 'PRODUCT'
    if p == 'portal':
        return 'PORTAL_PTR'
    return 'DATA'


def main():
    since, until, out = sys.argv[1], sys.argv[2], sys.argv[3]
    fmt = '%x1e%H%x1f%an%x1f%cI%x1f%s'
    raw = subprocess.run(['git', 'log', '--no-merges', '--numstat', f'--since={since}', f'--until={until}',
                          f'--format={fmt}'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if raw.returncode != 0:
        print('git log rc', raw.returncode, raw.stderr[:500])
        sys.exit(1)
    merges = subprocess.run(['git', 'log', '--merges', f'--since={since}', f'--until={until}', '--format=%H'],
                            capture_output=True, text=True).stdout.split()
    commits = []
    for block in raw.stdout.split('\x1e')[1:]:
        lines = block.strip('\n').split('\n')
        h, an, t, s = lines[0].split('\x1f', 3)
        files = []
        for ln in lines[1:]:
            if not ln.strip():
                continue
            parts = ln.split('\t')
            if len(parts) < 3:
                continue
            a, d, path = parts[0], parts[1], parts[2]
            if ' => ' in path:
                path = re.sub(r'\{[^}]*? => ([^}]*)\}', r'\1', path).replace('//', '/')
                if ' => ' in path:
                    path = path.split(' => ')[1]
            a = int(a) if a.isdigit() else 0
            d = int(d) if d.isdigit() else 0
            files.append((path, a, d, classify(path)))
        commits.append({'h': h[:10], 'author': an, 't': t, 's': s, 'files': files})
    json.dump({'since': since, 'until': until, 'merges': len(merges), 'commits': commits}, open(out, 'w'))

    n = len(commits)
    cls_commits = Counter()
    cls_lines = Counter()
    primary = Counter()
    for c in commits:
        seen = set(f[3] for f in c['files'])
        for k in seen:
            cls_commits[k] += 1
        for f in c['files']:
            cls_lines[f[3]] += f[1] + f[2]
        if 'PRODUCT' in seen:
            primary['touches PRODUCT code'] += 1
        elif 'TOOLING' in seen:
            primary['touches TOOLING code (no product)'] += 1
        elif seen and seen <= {'GOV_TO', 'GOV_SURP', 'GOV_LOG', 'GOV_MSG', 'GOV_REC', 'LAW'}:
            primary['governance-only'] += 1
        elif seen and seen <= {'DOCS', 'GOV_TO', 'GOV_SURP', 'GOV_LOG', 'GOV_MSG', 'GOV_REC', 'LAW', 'TOOLING_DOC'}:
            primary['docs/governance/skill-text only'] += 1
        else:
            primary['data/other (no code)'] += 1
    print(f'WINDOW {since} .. {until}: {n} non-merge commits, {len(merges)} merge commits')
    print('\nPRIMARY (each commit counted once):')
    for k, v in primary.most_common():
        print(f'  {k:40s} {v:6d}  {100*v/max(n,1):5.1f}%')
    print('\nCOMMITS TOUCHING CLASS (a commit may touch several):')
    for k, v in cls_commits.most_common():
        print(f'  {k:12s} {v:6d}  {100*v/max(n,1):5.1f}%')
    tot = sum(cls_lines.values())
    print(f'\nLINES CHANGED (added+deleted) BY CLASS, total {tot}:')
    for k, v in cls_lines.most_common():
        print(f'  {k:12s} {v:9d}  {100*v/max(tot,1):5.1f}%')


if __name__ == '__main__':
    main()
