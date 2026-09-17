"""RB-s-10 census: every empty / loading / error / no-permission rendering idiom in portal/src/**/*.tsx,
BEFORE (a portal commit, read from git objects) and AFTER (the worktree), with the file denominator printed.

A TEXT-LEVEL census: it counts idioms in source, never rendered states. Its denominator certifies the
sweep (every .tsx under src/), not that the pattern list is complete -- the categories are listed so a
reader can see what was and was not looked for.

usage: python rb-s-10_census.py <portal-worktree> <before-commit> <out.json>
"""
import json
import pathlib
import re
import subprocess
import sys

CATS = {
    # the RB10-AC2 criterion's own four patterns, case-sensitive, verbatim
    'ac2_raw_state_strings': [r'No .{0,30} available', r'No .{0,30} data', r'Unable to load', r'Failed to load'],
    # EMPTY: a quoted or JSX-text sentence opening "No <word>" (ad-hoc or designed alike)
    'empty_sentence_no_x': [r'''(?:['"`>]\s*)No [A-Za-z]'''],
    # ERROR idioms the contract retires: red ink / red tint blocks (C12 "never a red block", C5.8)
    'error_red_ink_or_tint': [r'text-red-(?:300|400|500)', r'bg-red-500/(?:5|10|20)', r'text-danger\b'],
    'error_could_not_load_text': [r'[Cc]ould not load', r"[Cc]ouldn't load"],
    # LOADING idioms the contract retires on a panel (a spinner over a blank panel)
    'loading_spinner_component': [r'<LoadingInline\b', r'<LoadingSpinner\b', r'<LoadingModal\b', r'<LoadingOverlay\b'],
    'loading_animate_spin': [r'animate-spin'],
    'loading_text': [r'Loading\.\.\.', 'Loading…'],
    # NO-PERMISSION idioms
    'no_permission_text': [r'(?i)no access|not authori[sz]ed|permission denied|do not have (?:access|permission)'],
    # the designed states and their adapters
    'designed_PanelEmpty': [r'<PanelEmpty\b'],
    'designed_PanelLoading': [r'<PanelLoading\b'],
    'designed_PanelError': [r'<PanelError\b'],
    'designed_PanelNoPermission': [r'<PanelNoPermission\b'],
    'adapter_ErrorMessage': [r'<ErrorMessage\b'],
    'adapter_EmptyState': [r'<EmptyState\b'],
    'adapter_LoadingContent_or_Container': [r'<LoadingContent\b', r'<LoadingContainer\b'],
}


def count(texts):
    res = {}
    for cat, pats in CATS.items():
        hits, files = 0, 0
        for _, t in texts:
            n = sum(len(re.findall(p, t)) for p in pats)
            hits += n
            files += 1 if n else 0
        res[cat] = {'hits': hits, 'files_with_hits': files}
    return res


def before_texts(portal, commit):
    names = subprocess.run(['git', '-C', portal, 'ls-tree', '-r', '--name-only', commit, 'src'],
                           capture_output=True, text=True, check=True).stdout.split('\n')
    names = [n for n in names if n.endswith('.tsx')]
    out = []
    for n in names:
        b = subprocess.run(['git', '-C', portal, 'show', f'{commit}:{n}'], capture_output=True, check=True).stdout
        out.append((n, b.decode('utf-8', errors='replace')))
    return out


def after_texts(portal):
    root = pathlib.Path(portal)
    return [(str(q.relative_to(root)).replace('\\', '/'), q.read_text(encoding='utf-8', errors='replace'))
            for q in (root / 'src').rglob('*.tsx')]


def main():
    portal, commit, out = sys.argv[1], sys.argv[2], sys.argv[3]
    b, a = before_texts(portal, commit), after_texts(portal)
    doc = {
        'instrument': 'rb-s-10_census.py (text-level idiom census over portal/src/**/*.tsx)',
        'before': {'vintage': commit, 'tsx_files': len(b), 'categories': count(b)},
        'after': {'vintage': 'worktree', 'tsx_files': len(a), 'categories': count(a)},
        'patterns': CATS,
    }
    pathlib.Path(out).write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
    print(f"DENOMINATOR: before {len(b)} .tsx files @ {commit}; after {len(a)} .tsx files @ worktree")
    print(f"{'category':40s} {'before':>14s} {'after':>14s}")
    for cat in CATS:
        x, y = doc['before']['categories'][cat], doc['after']['categories'][cat]
        print(f"{cat:40s} {x['hits']:>5d} in {x['files_with_hits']:>3d}f {y['hits']:>5d} in {y['files_with_hits']:>3d}f")


if __name__ == '__main__':
    main()
