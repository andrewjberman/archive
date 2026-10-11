"""r3_reads.py -- FB-f-9 phase A3 census (CTO ADDENDUM 5): every S3 data call in the 14 platinum writers and in the gold
lib modules they import is ROUTED through the platinum seam, NOT-SERVED by a static key prefix, or EXEMPT with a printed
reason. The arm passes only when UNROUTED = 0.

A site is an ast.Call whose method is one of READ/LIST/DELETE/WRITE below (get_object, head_object, list_objects_v2,
list_objects, paginate, delete_object, delete_objects, download_file, download_fileobj, copy_object, put_object,
upload_file, upload_fileobj, load). Per site:
  ROUTED       its Bucket argument is bound from a seam call (platinum_destination / platinum_source / platinum_list_target),
               directly or through a tuple unpack, or the call sits inside a function that unpacks a seam call and passes the
               unpacked bucket
  NOT-SERVED   its Key/Prefix resolves statically (module constants, s3_layout names, f-string prefixes, a key builder's
               return) to a string that starts with NO served legacy prefix of lib/platinum_dest_view.py
  EXEMPT       the call's line (or the line above) carries `# seam: exempt <reason>`
  UNROUTED     anything else

  python r3_reads.py [--root CHECKOUT] [--list]
Plain ASCII; prints counts and file:line, never a key value.
"""
import argparse
import ast
import json
import os
import re
import sys

GOLD = 'data/black_diamond/scripts/gold'
CENSUS = 'org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/0.9.0_WK_ADVI_FIRMBKTS~16/PRODUCER_CENSUS.json'
SEAM = {'platinum_destination', 'platinum_source', 'platinum_list_target'}
METHODS = {'get_object', 'head_object', 'list_objects_v2', 'list_objects', 'paginate', 'delete_object', 'delete_objects',
           'download_file', 'download_fileobj', 'copy_object', 'put_object', 'upload_file', 'upload_fileobj', 'load'}
KEYWORDS = ('Key', 'Prefix')


def root_of(a):
    return os.path.abspath(a.root)


def served_prefixes(root):
    ns = {}
    with open(os.path.join(root, GOLD, 'lib', 'platinum_dest_view.py'), encoding='utf-8') as fh:
        exec(compile(fh.read(), 'view', 'exec'), ns)  # a generated, assignment-only module
    return sorted({row[0] for row in ns['PLATINUM_CLASSES']})


class Env:
    """Static string evaluation over module-level constants and key-builder returns."""

    def __init__(self, tree, imported):
        self.consts, self.funcs, self.imported = {}, {}, imported
        for n in tree.body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                self.consts[n.targets[0].id] = n.value
            elif isinstance(n, ast.FunctionDef):
                self.funcs[n.name] = n

    def prefix(self, node, depth=0):
        """Static leading text of a string expression, or None when it cannot be known."""
        if depth > 6 or node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):
            out = ''
            for v in node.values:
                if isinstance(v, ast.Constant):
                    out += v.value
                else:
                    sub = self.prefix(v.value, depth + 1) if isinstance(v, ast.FormattedValue) else None
                    if sub is None:
                        return out or None
                    out += sub
            return out
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self.prefix(node.left, depth + 1)
            right = self.prefix(node.right, depth + 1)
            if left is None:
                return None
            return left + (right or '') if right is not None else left
        if isinstance(node, ast.Name):
            if node.id in self.consts:
                return self.prefix(self.consts[node.id], depth + 1)
            if node.id in self.imported:
                return self.imported[node.id]
            return None
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            f = self.funcs.get(node.func.id)
            if f is None and node.func.id in self.imported:
                return self.imported[node.func.id]
            if f is not None:
                rets = [r.value for r in ast.walk(f) if isinstance(r, ast.Return) and r.value is not None]
                if len(rets) == 1:
                    return self.prefix(rets[0], depth + 1)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ('format',):
            return self.prefix(node.func.value, depth + 1)
        return None


def module_values(root, rel):
    """Names defined in a lib module that evaluate to a static string prefix (constants and key-builder returns)."""
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as fh:
        tree = ast.parse(fh.read())
    env = Env(tree, {})
    out = {}
    for name, node in env.consts.items():
        v = env.prefix(node)
        if v is not None:
            out[name] = v
    for name, f in env.funcs.items():
        rets = [r.value for r in ast.walk(f) if isinstance(r, ast.Return) and r.value is not None]
        if len(rets) == 1:
            v = env.prefix(rets[0])
            if v is not None:
                out[name] = v
    return out


def seam_names(tree):
    """Names bound from a seam call (single name, or each element of a tuple unpack), plus subscripts of one."""
    names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
            f = n.value.func
            fid = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            if fid in SEAM:
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        names.add(t.id)
                    elif isinstance(t, ast.Tuple):
                        names.update(e.id for e in t.elts if isinstance(e, ast.Name))
    return names


def is_seam_expr(node, names):
    if isinstance(node, ast.Name):
        return node.id in names
    if isinstance(node, ast.Subscript):
        return is_seam_expr(node.value, names)
    if isinstance(node, ast.Call):
        f = node.func
        fid = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
        return fid in SEAM
    return False


def arg(call, name, pos=None):
    for k in call.keywords:
        if k.arg == name:
            return k.value
    if pos is not None and len(call.args) > pos:
        return call.args[pos]
    return None


def copy_source_parts(call):
    cs = arg(call, 'CopySource')
    if isinstance(cs, ast.Dict):
        d = {}
        for k, v in zip(cs.keys, cs.values):
            if isinstance(k, ast.Constant):
                d[k.value] = v
        return d.get('Bucket'), d.get('Key')
    return None, None


def sites(root, rel, served, shared, siblings=False):
    with open(os.path.join(root, rel), encoding='utf-8') as fh:
        src = fh.read()
    lines = src.splitlines()
    tree = ast.parse(src)
    imported = dict(shared)
    if siblings:  # --files mode: a Lambda's constants live in a sibling module (config.py)
        here = os.path.dirname(rel)
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                cand = os.path.join(here, n.module.replace('.', '/') + '.py').replace(os.sep, '/')
                if os.path.exists(os.path.join(root, cand)):
                    vals = module_values(root, cand)
                    for alias in n.names:
                        if alias.name in vals:
                            imported[alias.asname or alias.name] = vals[alias.name]
    env = Env(tree, imported)
    names = seam_names(tree)
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in METHODS):
            continue
        m = n.func.attr
        if m == 'load' and not (isinstance(n.func.value, ast.Call)):
            continue
        keys, buckets = [], []
        if m == 'copy_object':
            sb, sk = copy_source_parts(n)
            buckets += [x for x in (sb, arg(n, 'Bucket')) if x is not None]
            keys += [x for x in (sk, arg(n, 'Key')) if x is not None]
        else:
            b = arg(n, 'Bucket', 0 if m.startswith(('download', 'upload')) is False else None)
            if b is not None:
                buckets.append(b)
            for kw in KEYWORDS:
                k = arg(n, kw)
                if k is not None:
                    keys.append(k)
            if m in ('download_file', 'download_fileobj', 'upload_file', 'upload_fileobj') and len(n.args) >= 2:
                buckets.append(n.args[0] if m.startswith('download') else n.args[1])
                keys.append(n.args[1] if m.startswith('download') else n.args[2] if len(n.args) > 2 else n.args[1])
        line = n.lineno
        ctx = (lines[line - 1] if line - 1 < len(lines) else '') + ' ' + (lines[line - 2] if line >= 2 else '')
        em = re.search(r'#\s*seam:\s*exempt\s+(\S.*)', ctx)
        status = 'UNROUTED'
        why = ''
        if buckets and all(is_seam_expr(b, names) for b in buckets):
            status = 'ROUTED'
        elif em:
            status, why = 'EXEMPT', em.group(1).strip()[:80]
        else:
            pf = [env.prefix(k) for k in keys]
            if keys and all(p is not None and p != '' and not any(p.startswith(s) or s.startswith(p) for s in served)
                            for p in pf):
                status = 'NOT-SERVED'
        out.append((rel, line, m, status, why))
    return out


def writer_files(root):
    with open(os.path.join(root, CENSUS), encoding='utf-8') as fh:
        cen = json.load(fh)
    return sorted({w['script'] for c in cen['classes'] for w in c['writers']})


def lib_files(root, scripts):
    """gold lib modules imported by the scripts (from lib.<m> import ... / import lib.<m>)."""
    mods = set()
    for rel in scripts:
        with open(os.path.join(root, rel), encoding='utf-8') as fh:
            tree = ast.parse(fh.read())
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith('lib.'):
                mods.add(n.module.split('.')[1])
            elif isinstance(n, ast.ImportFrom) and n.module == 'lib':
                mods.update(a.name for a in n.names)
    out = []
    for m in sorted(mods):
        rel = '%s/lib/%s.py' % (GOLD, m)
        if os.path.exists(os.path.join(root, rel)) and m not in ('platinum_dest', 'platinum_dest_view', 'config', 's3_layout'):
            out.append(rel)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--files', nargs='+', default=None,
                    help='grade exactly these files (repo-relative) instead of the 14 writers and their libs')
    a = ap.parse_args()
    root = root_of(a)
    served = served_prefixes(root)
    shared = {}
    for mod in ('s3_layout', 'config'):
        shared.update(module_values(root, '%s/lib/%s.py' % (GOLD, mod)))
    if a.files:
        scripts, libs = list(a.files), []
    else:
        scripts = writer_files(root)
        libs = lib_files(root, scripts)
    allsites = []
    for rel in scripts + libs:
        allsites += sites(root, rel, served, shared, siblings=bool(a.files))
    cnt = {}
    for s in allsites:
        cnt[s[3]] = cnt.get(s[3], 0) + 1
    print('  files: %d %s + %d lib modules they import; served legacy prefixes: %d'
          % (len(scripts), 'named files' if a.files else 'writer scripts', len(libs), len(served)))
    print('  S3 data call sites=%d ROUTED=%d NOT-SERVED=%d EXEMPT=%d UNROUTED=%d'
          % (len(allsites), cnt.get('ROUTED', 0), cnt.get('NOT-SERVED', 0), cnt.get('EXEMPT', 0), cnt.get('UNROUTED', 0)))
    if a.list or cnt.get('UNROUTED', 0) or cnt.get('EXEMPT', 0):
        for rel, line, m, status, why in allsites:
            if status in ('UNROUTED', 'EXEMPT') or a.list:
                print('    %-10s %s:%d %s%s' % (status, os.path.basename(rel), line, m, (' -- ' + why) if why else ''))
    ok = cnt.get('UNROUTED', 0) == 0 and len(allsites) > 0
    print('ROUND 3 READ CENSUS: %s' % ('ALL SITES ROUTED, NOT-SERVED OR EXEMPT' if ok else 'UNROUTED SITES REMAIN'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
