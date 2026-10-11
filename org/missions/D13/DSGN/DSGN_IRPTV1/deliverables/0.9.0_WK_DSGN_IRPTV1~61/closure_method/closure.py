"""Compute the print route's import closure from the build's module graph (written by the one-off rollup plugin).
usage: python closure.py <build_graph.json> <portal_root> <out.json> <changed_files_json>"""
import json
import os
import sys

g = json.load(open(sys.argv[1], 'rb'))
root = os.path.normpath(sys.argv[2]).replace('\\', '/')
changed = json.load(open(sys.argv[4], 'rb'))
mods = {k.replace('\\', '/'): v for k, v in g['modules'].items()}
def norm(s):
    return s.replace('\\', '/')

for v in mods.values():
    v['s'] = [norm(x) for x in v['s']]
    v['d'] = [norm(x) for x in v['d']]

ENTRY = root + '/src/pages/InvestorReporting/render/PrintEntry.tsx'
assert ENTRY in mods, 'entry not in graph'


def reach(entry, dynamic=True):
    seen, stack = set(), [entry]
    while stack:
        m = stack.pop()
        if m in seen or m not in mods:
            continue
        seen.add(m)
        stack.extend(mods[m]['s'])
        if dynamic:
            stack.extend(mods[m]['d'])
    return seen


full = reach(ENTRY, True)
static = reach(ENTRY, False)


def src(s):
    return sorted(x[len(root) + 1:] for x in s if x.startswith(root + '/src/'))


full_src, static_src = src(full), src(static)

# chunk-graph cross-check: the PrintEntry chunk and every chunk reachable from it by import / dynamicImport
ch = g['chunks']
start = [n for n, c in ch.items() if ENTRY in [norm(m) for m in c['modules']] or (c['facade'] and norm(c['facade']) == ENTRY)]
seen, stack = set(), list(start)
while stack:
    n = stack.pop()
    if n in seen or n not in ch:
        continue
    seen.add(n)
    stack.extend(ch[n]['imports'] + ch[n]['dynamicImports'])
chunk_mods = set()
for n in seen:
    chunk_mods.update(norm(m) for m in ch[n]['modules'])
chunk_src = src(chunk_mods)

in_closure = [f for f in changed if f in set(full_src)]
in_chunks = [f for f in changed if f in set(chunk_src)]
out = {
    'entry': ENTRY[len(root) + 1:],
    'modules_in_build_graph': len(mods),
    'closure_files_static_and_dynamic': len(full_src),
    'closure_files_static_only': len(static_src),
    'entry_chunks': start,
    'chunks_reachable_from_entry_chunk': len(seen),
    'chunk_graph_source_modules': len(chunk_src),
    'changed_files': changed,
    'changed_in_module_closure': in_closure,
    'changed_in_chunk_graph': in_chunks,
    'closure_files': full_src,
}
json.dump(out, open(sys.argv[3], 'w'), indent=1)
print('modules in graph', len(mods))
print('entry', out['entry'])
print('closure static+dynamic', len(full_src), 'static only', len(static_src))
print('entry chunks', start, 'reachable chunks', len(seen), 'chunk-graph src modules', len(chunk_src))
print('changed in module closure:', in_closure)
print('changed in chunk graph   :', in_chunks)
for c in changed:
    print('  changed', c, 'in_graph' if (root + '/' + c) in mods else 'NOT in build graph')
