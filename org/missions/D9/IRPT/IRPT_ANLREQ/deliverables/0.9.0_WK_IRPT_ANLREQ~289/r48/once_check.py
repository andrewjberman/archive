#!/usr/bin/env python3
"""AR389-y-AC3 -- each change appears once: export and import uniqueness for the two conflicted files.

For src/api/endpoints/tickets.ts and src/pages/TicketCenter/TicketCenter.tsx it extracts the top-level
export names and the import specifier names of the resolved file (the branch), and of origin/DEV and
origin/PROD. ONCE-OK only when no export name and no import name repeats in the resolved file, and the
union of the exports of origin/DEV and origin/PROD is a subset of the resolved file's exports.

CONTROL: a copy of each resolved file in which one export block is duplicated must be REJECTED by the
same test; the control prints CONTROL-FIRES only after that rejection is shown. A control that is not
rejected prints CONTROL-DID-NOT-FIRE and the checker exits 1.
"""
import collections
import os
import re
import subprocess
import sys

BR = 'cand/dell2/prod-into-dev-reconcile'
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['src/api/endpoints/tickets.ts', 'src/pages/TicketCenter/TicketCenter.tsx']

EXPORT_DECL = re.compile(
    r'^export\s+(?:default\s+)?(?:declare\s+)?(?:async\s+)?(?:abstract\s+)?'
    r'(?:function\*?|const|let|var|class|interface|type|enum)\s+([A-Za-z_$][\w$]*)', re.M)
EXPORT_LIST = re.compile(r'^export\s*\{([^}]*)\}', re.M | re.S)
IMPORT_BRACED = re.compile(r'^import\s+(?:type\s+)?\{([^}]*)\}\s*from\s', re.M | re.S)
IMPORT_DEFAULT = re.compile(r'^import\s+(?:type\s+)?([A-Za-z_$][\w$]*)\s*(?:,|from\s)', re.M)


def git_show(ref_path, cwd):
    p = subprocess.run(['git', 'show', ref_path], cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return p.returncode, p.stdout


def local_name(spec):
    spec = spec.strip()
    if not spec:
        return None
    spec = re.sub(r'^type\s+', '', spec)
    if ' as ' in spec:
        spec = spec.split(' as ')[-1].strip()
    return spec


def exports_of(text):
    names = [m.group(1) for m in EXPORT_DECL.finditer(text)]
    for m in EXPORT_LIST.finditer(text):
        for part in m.group(1).split(','):
            name = local_name(part)
            if name:
                names.append(name)
    return names


def imports_of(text):
    names = []
    for m in IMPORT_BRACED.finditer(text):
        for part in m.group(1).split(','):
            name = local_name(part)
            if name:
                names.append(name)
    for m in IMPORT_DEFAULT.finditer(text):
        names.append(m.group(1))
    return names


def judge(resolved, dev, prod):
    """Return (ok, reason). The test used for the real files and for the control."""
    ex = exports_of(resolved)
    im = imports_of(resolved)
    rep_e = sorted(n for n, c in collections.Counter(ex).items() if c > 1)
    rep_i = sorted(n for n, c in collections.Counter(im).items() if c > 1)
    if rep_e:
        return False, 'export repeated: %s' % ', '.join(rep_e[:5])
    if rep_i:
        return False, 'import repeated: %s' % ', '.join(rep_i[:5])
    missing = (set(exports_of(dev)) | set(exports_of(prod))) - set(ex)
    if missing:
        return False, 'export of DEV or PROD missing from the resolved file: %s' % ', '.join(sorted(missing)[:5])
    return True, 'none repeated; every export of origin/DEV and of origin/PROD present'


def duplicate_one_export(text):
    """Control mutant: append a second copy of the first top-level exported function or interface."""
    m = EXPORT_DECL.search(text)
    if not m:
        return None
    start = m.start()
    # the block runs to the next top-level export or the end of the file
    nxt = EXPORT_DECL.search(text, m.end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    return text + '\n' + block, m.group(1)


def main():
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE,
                          capture_output=True, text=True).stdout.strip()
    portal = os.path.join(root, 'portal')
    total_e = 0
    total_i = 0
    all_ok = True
    for f in FILES:
        rc_r, resolved = git_show(BR + ':' + f, portal)
        rc_d, dev = git_show('origin/DEV:' + f, portal)
        rc_p, prod = git_show('origin/PROD:' + f, portal)
        if rc_r or rc_d or rc_p:
            print('ONCE-BAD cannot read %s at the branch, DEV or PROD' % f)
            return 1
        ok, reason = judge(resolved, dev, prod)
        total_e += len(exports_of(resolved))
        total_i += len(imports_of(resolved))
        print('  %s: %d exports, %d imports, %s' % (f, len(exports_of(resolved)), len(imports_of(resolved)), reason))
        all_ok = all_ok and ok
    if not all_ok:
        print('ONCE-BAD a file repeats a name or lacks a DEV or PROD export (see the lines above)')
        return 1

    # the control: a duplicated export must be rejected, on each file
    for f in FILES:
        _, resolved = git_show(BR + ':' + f, portal)
        _, dev = git_show('origin/DEV:' + f, portal)
        _, prod = git_show('origin/PROD:' + f, portal)
        mutant = duplicate_one_export(resolved)
        if mutant is None:
            print('CONTROL-DID-NOT-FIRE no export to duplicate in %s' % f)
            return 1
        mut_text, dup_name = mutant
        ok, reason = judge(mut_text, dev, prod)
        if ok:
            print('CONTROL-DID-NOT-FIRE the duplicated export %s in %s was accepted' % (dup_name, f))
            return 1
        print('CONTROL-FIRES %s: duplicated export %s rejected (%s)' % (f, dup_name, reason))

    print('ONCE-OK %d exports %d imports, none repeated, every export of origin/DEV and of origin/PROD present'
          % (total_e, total_i))
    return 0


if __name__ == '__main__':
    sys.exit(main())
