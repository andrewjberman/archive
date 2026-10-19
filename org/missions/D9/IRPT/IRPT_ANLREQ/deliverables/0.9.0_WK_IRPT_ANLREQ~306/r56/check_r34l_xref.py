"""Cross-reference check over a built resident tarball (READ ONLY: the tarball is read, nothing is built, uploaded, installed or run).

usage: python -I check_r34l_xref.py <irpt-resident-0485393f3a-r34l.tar.gz>

The producer ycharts/research/opal_producer.py and the layout ycharts/research/layout_overview.py are parsed with ast (no import,
no execution). The alias under which the producer imports layout_overview is found (import layout_overview as lo); every
<alias>.<NAME> the producer reads (load context) is collected; each NAME must be defined at module level in the layout member
(an assignment target, a def or a class).
Prints R34L-XREF-OK missing=0 names=<n> (rc 0) only when no NAME is missing; otherwise R34L-XREF-BAD <why> or
R34L-XREF-BAD missing=<k> <sorted names> (rc 1). ASCII only.
"""
import ast
import sys
import tarfile

PRODUCER = "ycharts/research/opal_producer.py"
LAYOUT = "ycharts/research/layout_overview.py"
LAYOUT_MODULE = "layout_overview"


def bad(why):
    print("R34L-XREF-BAD %s" % why)
    return 1


def read_member(tar, name):
    for mem in tar.getmembers():
        norm = mem.name[2:] if mem.name.startswith("./") else mem.name
        if norm == name and mem.isfile():
            return tar.extractfile(mem).read().decode("utf-8")
    return None


def layout_aliases(tree):
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == LAYOUT_MODULE:
                    found.add(alias.asname or alias.name)
    return found


def producer_reads(tree, aliases):
    found = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load)
                and isinstance(node.value, ast.Name) and node.value.id in aliases):
            found.add(node.attr)
    return found


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


def module_names(tree):
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                names |= target_names(tgt)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            names |= target_names(node.target)
    return names


def main(argv):
    if len(argv) != 1:
        print("usage: check_r34l_xref.py <irpt-resident-0485393f3a-r34l.tar.gz>")
        return 2
    try:
        with tarfile.open(argv[0], "r:gz") as tar:
            prod_src = read_member(tar, PRODUCER)
            lay_src = read_member(tar, LAYOUT)
    except (OSError, tarfile.TarError) as exc:
        return bad("tarball unreadable: %s" % exc)
    if prod_src is None:
        return bad("member %s absent" % PRODUCER)
    if lay_src is None:
        return bad("member %s absent" % LAYOUT)
    prod_tree = ast.parse(prod_src, PRODUCER)
    lay_tree = ast.parse(lay_src, LAYOUT)
    aliases = layout_aliases(prod_tree)
    if not aliases:
        return bad("%s does not import %s" % (PRODUCER, LAYOUT_MODULE))
    reads = producer_reads(prod_tree, aliases)
    defined = module_names(lay_tree)
    missing = sorted(reads - defined)
    if missing:
        print("R34L-XREF-BAD missing=%d %s" % (len(missing), " ".join(missing)))
        return 1
    print("R34L-XREF-OK missing=0 names=%d" % len(reads))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
