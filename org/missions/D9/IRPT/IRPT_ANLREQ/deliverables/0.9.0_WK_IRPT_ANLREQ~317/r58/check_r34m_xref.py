"""Cross-reference check over the three movers of a built resident tarball (READ ONLY: the tarball is read, nothing is built, uploaded, installed or run).

usage: python -I check_r34m_xref.py <irpt-resident-0485393f3a-r34m.tar.gz>

Movers: reports/resident_installed.py, ycharts/generate/resident_worker.py, ycharts/research/opal_packager.py. Each is parsed with ast
(no import, no execution). For every `import X` / `import X as Y` and `from X import a, b` whose X resolves to ANOTHER member of the tarball
(the dotted path as <path>.py or <path>/__init__.py, a suffix match, or a unique basename match; relative imports resolve from the mover's
package), the check collects every <Y>.<NAME> the mover reads (load context) and every imported a, b. A `from X import a` where X.a is itself a
member is a submodule import and is not a name. Each NAME must be bound at module level in that sibling (assignment, annotated or augmented
assignment, def, class, for target, or an import binding; module-level if, try and with bodies are included). A sibling that star-imports
defines nothing this check can see, so a name it would supply counts as missing.
Prints R34M-XREF-OK missing=0 names=<n> (rc 0) only when no NAME is missing; otherwise R34M-XREF-BAD missing=<k> <sorted names> (rc 1),
followed by one detail line per missing name. ASCII only.
"""
import ast
import posixpath
import sys
import tarfile

MOVERS = [
    "reports/resident_installed.py",
    "ycharts/generate/resident_worker.py",
    "ycharts/research/opal_packager.py",
]


def bad(why):
    print("R34M-XREF-BAD %s" % why)
    return 1


def load_members(path):
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for mem in tar.getmembers():
            if not mem.isfile():
                continue
            norm = mem.name[2:] if mem.name.startswith("./") else mem.name
            if norm.endswith(".py"):
                out[norm] = tar.extractfile(mem).read().decode("utf-8")
    return out


def resolve(dotted, members):
    """Return the member path a dotted module name denotes, or None."""
    base = dotted.replace(".", "/")
    for cand in (base + ".py", base + "/__init__.py"):
        if cand in members:
            return cand
    suffix = [p for p in sorted(members) if p.endswith("/" + base + ".py")]
    if suffix:
        return suffix[0]
    if "." in dotted:
        # a dotted stdlib or third-party name (urllib.parse) never resolves by its last component alone
        return None
    same = sorted(p for p in members if p.split("/")[-1] == dotted + ".py")
    if len(same) == 1:
        return same[0]
    return None


def resolve_from(mover, level, module, members):
    """Resolve an ImportFrom module (absolute, or relative to the mover's package)."""
    if level == 0:
        return resolve(module, members) if module else None
    pkg = posixpath.dirname(mover).split("/") if posixpath.dirname(mover) else []
    if level - 1 > len(pkg):
        return None
    if level - 1:
        pkg = pkg[: len(pkg) - (level - 1)]
    parts = pkg + ([module] if module else [])
    return resolve(".".join(p for p in parts if p), members) if parts else None


def flatten(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        head = flatten(node.value)
        return head + "." + node.attr if head else None
    return None


def target_names(tgt):
    if isinstance(tgt, ast.Name):
        return {tgt.id}
    if isinstance(tgt, (ast.Tuple, ast.List)):
        out = set()
        for elt in tgt.elts:
            out |= target_names(elt)
        return out
    if isinstance(tgt, ast.Starred):
        return target_names(tgt.value)
    return set()


def module_names(body):
    names = set()
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                names |= target_names(tgt)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            names |= target_names(node.target)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            names |= target_names(node.target) | module_names(node.body) | module_names(node.orelse)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars is not None:
                    names |= target_names(item.optional_vars)
            names |= module_names(node.body)
        elif isinstance(node, ast.If):
            names |= module_names(node.body) | module_names(node.orelse)
        elif isinstance(node, ast.Try):
            names |= module_names(node.body) | module_names(node.orelse) | module_names(node.finalbody)
            for handler in node.handlers:
                if handler.name:
                    names.add(handler.name)
                names |= module_names(handler.body)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    names.add(alias.asname or alias.name)
    return names


def mover_uses(mover, tree, members):
    """Return {(sibling, NAME)} for every sibling attribute read and every from-import name of this mover."""
    prefix_map = {}
    uses = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                sib = resolve(alias.name, members)
                if sib and sib != mover:
                    prefix_map[alias.asname or alias.name] = sib
        elif isinstance(node, ast.ImportFrom):
            sib = resolve_from(mover, node.level, node.module, members)
            if sib is None or sib == mover:
                continue
            for alias in node.names:
                if alias.name == "*" or is_submodule(sib, alias.name, members):
                    continue
                uses.add((sib, alias.name))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            head = flatten(node.value)
            if head in prefix_map:
                uses.add((prefix_map[head], node.attr))
    return uses


def is_submodule(sib, name, members):
    """True when `from X import name` names the submodule of package X (X resolved to a package __init__.py)."""
    if not sib.endswith("/__init__.py"):
        return False
    pkg = posixpath.dirname(sib)
    return (pkg + "/" + name + ".py") in members or (pkg + "/" + name + "/__init__.py") in members


def main(argv):
    if len(argv) != 1:
        print("usage: check_r34m_xref.py <irpt-resident-0485393f3a-r34m.tar.gz>")
        return 2
    try:
        members = load_members(argv[0])
    except (OSError, tarfile.TarError, UnicodeDecodeError) as exc:
        return bad("tarball unreadable: %s" % exc)
    uses = {}
    for mover in MOVERS:
        if mover not in members:
            return bad("mover %s absent" % mover)
        tree = ast.parse(members[mover], mover)
        for sib, name in mover_uses(mover, tree, members):
            uses.setdefault((sib, name), set()).add(mover)
    defined = {}
    missing = []
    checked = uses
    for (sib, name), movers in sorted(checked.items()):
        if sib not in defined:
            defined[sib] = module_names(ast.parse(members[sib], sib).body)
        if name not in defined[sib]:
            missing.append((sib, name, sorted(movers)))
    if missing:
        names = sorted(set(name for _sib, name, _m in missing))
        print("R34M-XREF-BAD missing=%d %s" % (len(names), " ".join(names)))
        for sib, name, movers in missing:
            print("  %s is not bound at module level in %s (read by %s)" % (name, sib, ", ".join(movers)))
        return 1
    print("R34M-XREF-OK missing=0 names=%d" % len(checked))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
