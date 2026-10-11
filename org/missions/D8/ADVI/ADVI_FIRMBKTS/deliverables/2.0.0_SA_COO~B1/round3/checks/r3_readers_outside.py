"""r3_readers_outside.py -- the CTO's act-2 precondition (ADDENDUM 5 / CTO half): ONE census of S3 data calls that read
(or list, delete) a key under one of the 11 served legacy prefixes, over every .py file of data/ and infra/aws/lambda that
is NOT one of the 14 writers or the 8 lib modules r3_reads.py already grades.

Per S3 data call (same call set as r3_reads.py) the key's static prefix is resolved through module constants, s3_layout
names, f-string prefixes and one-return key builders:
  SERVED      the prefix starts with (or is a proper prefix of) a served legacy prefix
  NOT-SERVED  resolved, outside every served prefix
  UNRESOLVED  the key is dynamic and could not be resolved statically (a count, never a silent pass)
Output is per file: SERVED / UNRESOLVED counts and the SERVED call lines (file:line, method), with the denominator
(files scanned, files with at least one S3 data call, call sites). It classes nothing as producer, QA or router: that is a
reading of each SERVED file, in the amendment.

  python r3_readers_outside.py [--root CHECKOUT] [--scope data/black_diamond infra/aws/lambda]
"""
import argparse
import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_reads as r  # noqa: E402

BD_TOKENS = ('opal-data-bd', 'BD_S3_BUCKET', 's3_layout', 'lib.config', 'from lib import')
SKIP_DIRS = {'tests', '__pycache__', 'node_modules', '.git', '.scratch'}


def all_py(root, scopes):
    out = []
    for sc in scopes:
        base = os.path.join(root, sc)
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for fn in fns:
                if fn.endswith('.py'):
                    out.append(os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, '/'))
    return sorted(out)


def classify(root, rel, served, shared):
    with open(os.path.join(root, rel), encoding='utf-8', errors='replace') as fh:
        src = fh.read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    local = dict(shared)
    here = os.path.dirname(rel)
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            cand = os.path.join(here, n.module.replace('.', '/') + '.py').replace(os.sep, '/')
            if os.path.exists(os.path.join(root, cand)):
                vals = r.module_values(root, cand)
                for alias in n.names:
                    if alias.name in vals:
                        local[alias.asname or alias.name] = vals[alias.name]
    env = r.Env(tree, local)
    rows = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in r.METHODS):
            continue
        m = n.func.attr
        if m == 'load' and not isinstance(n.func.value, ast.Call):
            continue
        keys = []
        if m == 'copy_object':
            _, sk = r.copy_source_parts(n)
            keys += [x for x in (sk, r.arg(n, 'Key')) if x is not None]
        else:
            for kw in r.KEYWORDS:
                k = r.arg(n, kw)
                if k is not None:
                    keys.append(k)
            if m in ('download_file', 'download_fileobj') and len(n.args) >= 2:
                keys.append(n.args[1])
        if not keys:
            continue
        pf = [env.prefix(k) for k in keys]
        if any(p and any(p.startswith(s) or s.startswith(p) for s in served) for p in pf):
            st = 'SERVED'
        elif all(p is not None and p != '' for p in pf):
            st = 'NOT-SERVED'
        else:
            st = 'UNRESOLVED'
        rows.append((n.lineno, m, st))
    # one hop of inter-procedural reads: a local helper whose S3 call keys on one of its parameters is itself a read
    # site at every call; the call's argument is resolved the same way.
    helpers = {}
    for f in [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]:
        params = [a_.arg for a_ in f.args.args]
        for n in ast.walk(f):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in r.METHODS):
                continue
            ks = [r.arg(n, kw_) for kw_ in r.KEYWORDS]
            if n.func.attr in ('download_file', 'download_fileobj') and len(n.args) >= 2:
                ks.append(n.args[1])
            for k in ks:
                if k is None:
                    continue
                for nm in ast.walk(k):
                    if isinstance(nm, ast.Name) and nm.id in params:
                        helpers.setdefault(f.name, set()).add(params.index(nm.id))
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in helpers:
            for idx in sorted(helpers[n.func.id]):
                node = n.args[idx] if len(n.args) > idx else None
                if node is None:
                    continue
                p = env.prefix(node)
                if p and any(p.startswith(s) or s.startswith(p) for s in served):
                    st = 'SERVED'
                elif p:
                    st = 'NOT-SERVED'
                else:
                    st = 'UNRESOLVED'
                rows.append((n.lineno, 'via ' + n.func.id, st))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--scope', nargs='+', default=['data/black_diamond', 'infra/aws/lambda'])
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    served = r.served_prefixes(root)
    shared = {}
    for mod in ('s3_layout', 'config'):
        shared.update(r.module_values(root, '%s/lib/%s.py' % (r.GOLD, mod)))
    graded = set(r.writer_files(root))
    graded.update(r.lib_files(root, sorted(graded)))
    files = [f for f in all_py(root, a.scope) if f not in graded]
    tot = {'SERVED': 0, 'NOT-SERVED': 0, 'UNRESOLVED': 0}
    withcalls = 0
    served_files = []
    unparsed = 0
    bdfiles, unresolved_bd = [], []
    bdtot = {'SERVED': 0, 'NOT-SERVED': 0, 'UNRESOLVED': 0}
    for rel in files:
        rows = classify(root, rel, served, shared)
        if rows is None:
            unparsed += 1
            continue
        if not rows:
            continue
        withcalls += 1
        c = {'SERVED': 0, 'NOT-SERVED': 0, 'UNRESOLVED': 0}
        for _, _, st in rows:
            c[st] += 1
            tot[st] += 1
        with open(os.path.join(root, rel), encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        bd = any(tok in text for tok in BD_TOKENS)
        if bd:
            bdfiles.append(rel)
            for k in c:
                bdtot[k] += c[k]
        if c['SERVED']:
            served_files.append((rel, c, [(ln, m) for ln, m, st in rows if st == 'SERVED']))
        elif bd and c['UNRESOLVED']:
            unresolved_bd.append((rel, c['UNRESOLVED']))
    print('  scope: %s; python files scanned=%d (graded elsewhere: %d excluded, unparsable=%d); files with an S3 data call=%d'
          % (', '.join(a.scope), len(files), len(graded), unparsed, withcalls))
    print('  call sites SERVED=%d NOT-SERVED=%d UNRESOLVED=%d in %d file(s) with a SERVED call'
          % (tot['SERVED'], tot['NOT-SERVED'], tot['UNRESOLVED'], len(served_files)))
    for rel, c, ls in served_files:
        print('    %s  SERVED=%d UNRESOLVED=%d  lines: %s'
              % (rel, c['SERVED'], c['UNRESOLVED'], ', '.join('%d:%s' % x for x in ls[:12])))
    print('  files that name the BD bucket or its layout (tokens: %s): %d; their call sites SERVED=%d NOT-SERVED=%d UNRESOLVED=%d'
          % (', '.join(BD_TOKENS), len(bdfiles), bdtot['SERVED'], bdtot['NOT-SERVED'], bdtot['UNRESOLVED']))
    print('  BD-named files with UNRESOLVED calls (dynamic key; each needs a reading): %d' % len(unresolved_bd))
    for rel, n in unresolved_bd:
        print('    %s  UNRESOLVED=%d' % (rel, n))
    print('ROUND 3 OUTSIDE READERS: %d file(s) read a served prefix' % len(served_files))
    return 0


if __name__ == '__main__':
    sys.exit(main())
