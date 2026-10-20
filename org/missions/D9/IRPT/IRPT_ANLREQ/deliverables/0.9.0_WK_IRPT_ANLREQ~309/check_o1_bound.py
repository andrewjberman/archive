"""O1 bound check for IRPT_ANLREQ TO-AR-y-415 (stdlib only, read-only, ASCII).

Proves that the committed change of this worktree, outside org/, is exactly the two owner
functions of the guard class in served.py, one added class, the one new test file, and the one
pinned test file that the amendment grants (three paths).

Method: take the merge base of HEAD and box/dell2 (the branch point), list the changed paths,
keep the ones not under org/, then compare ast.dump of every top-level definition and every
method of the guard class (the class that defines _create_owner and _advisor_owner) at the
branch point and at HEAD.

Output: O1-BOUND-OK functions=2 classes=1 files=2 (rc 0), or O1-BOUND-BAD <what> (rc 1),
or O1-BOUND-ERROR <what> (rc 2) when git cannot be read.
"""
import ast
import collections
import os
import subprocess

SERVED = "infra/aws/lambda/investor-reporting/_authz/served.py"
TEST_FILE = "infra/aws/lambda/investor-reporting/_authz/tests/test_create_owner_on_behalf.py"
PINNED_FILE = "infra/aws/lambda/investor-reporting/_authz/tests/test_served_on_behalf_create.py"
EXPECTED_PATHS = sorted([SERVED, TEST_FILE, PINNED_FILE])
CHANGED_METHODS = frozenset(["_create_owner", "_advisor_owner"])
ADDED_CLASSES = frozenset(["AdvisorUnprovisioned"])
ALLOWED_IMPORT = "from prospect import ProspectOwnershipRefused"
HERE = os.path.dirname(os.path.abspath(__file__))


class BoundBad(Exception):
    """A structural mismatch: the printed reason follows O1-BOUND-BAD."""


class BoundError(Exception):
    """git could not be read: the printed reason follows O1-BOUND-ERROR."""


def git(args):
    proc = subprocess.run(["git"] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=HERE)
    if proc.returncode != 0:
        raise BoundError("git %s rc=%d %s" % (" ".join(args), proc.returncode, proc.stderr.strip()))
    return proc.stdout


def is_def(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))


def dump(node):
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def method_names(class_node):
    return set(n.name for n in class_node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))


def split_module(source):
    tree = ast.parse(source)
    defs = {}
    stmts = collections.Counter()
    for node in tree.body:
        if is_def(node):
            if node.name in defs:
                raise BoundBad("duplicate top-level definition %s" % node.name)
            defs[node.name] = node
        else:
            stmts[dump(node)] += 1
    return defs, stmts


def class_parts(class_node):
    header = [dump(x) for x in list(class_node.decorator_list) + list(class_node.bases)
              + list(class_node.keywords)]
    methods = {}
    attributes = []
    for item in class_node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if item.name in methods:
                raise BoundBad("duplicate method %s" % item.name)
            methods[item.name] = dump(item)
        else:
            attributes.append(dump(item))
    return header, methods, attributes


def compare(base_source, head_source):
    base_defs, base_stmts = split_module(base_source)
    head_defs, head_stmts = split_module(head_source)
    guards = sorted(name for name, node in base_defs.items()
                    if isinstance(node, ast.ClassDef) and CHANGED_METHODS <= method_names(node))
    if len(guards) != 1:
        raise BoundBad("guard class not unique at the branch point: %s" % guards)
    guard = guards[0]
    if guard not in head_defs or not isinstance(head_defs[guard], ast.ClassDef):
        raise BoundBad("guard class %s missing at HEAD" % guard)

    base_other = dict((n, dump(v)) for n, v in base_defs.items() if n != guard)
    head_other = dict((n, dump(v)) for n, v in head_defs.items() if n != guard)
    moved = sorted(n for n in base_other if n in head_other and base_other[n] != head_other[n])
    removed = sorted(n for n in base_other if n not in head_other)
    added = sorted(n for n in head_other if n not in base_other)
    if moved or removed:
        raise BoundBad("top-level definitions changed %s removed %s" % (moved, removed))
    if set(added) != ADDED_CLASSES or not all(isinstance(head_defs[n], ast.ClassDef) for n in added):
        raise BoundBad("top-level definitions added %s, want exactly the class %s"
                       % (added, sorted(ADDED_CLASSES)))

    base_header, base_methods, base_attrs = class_parts(base_defs[guard])
    head_header, head_methods, head_attrs = class_parts(head_defs[guard])
    if base_header != head_header:
        raise BoundBad("guard class header changed")
    if base_attrs != head_attrs:
        raise BoundBad("guard class attributes changed")
    if set(base_methods) != set(head_methods):
        raise BoundBad("guard class method set changed: added %s removed %s"
                       % (sorted(set(head_methods) - set(base_methods)),
                          sorted(set(base_methods) - set(head_methods))))
    changed = sorted(n for n in base_methods if base_methods[n] != head_methods[n])
    if set(changed) != CHANGED_METHODS:
        raise BoundBad("guard class methods changed %s, want exactly %s"
                       % (changed, sorted(CHANGED_METHODS)))

    gone = base_stmts - head_stmts
    new = head_stmts - base_stmts
    if gone:
        raise BoundBad("top-level statements removed: %d" % sum(gone.values()))
    allowed_import = dump(ast.parse(ALLOWED_IMPORT).body[0])
    if any(key != allowed_import for key in new) or sum(new.values()) > 1:
        raise BoundBad("top-level statements added beyond the one prospect import: %d"
                       % sum(new.values()))
    return len(changed), len(added)


def main():
    try:
        base = git(["merge-base", "HEAD", "box/dell2"]).strip()
        names = [p for p in git(["diff", "--name-only", base, "HEAD"]).splitlines() if p.strip()]
        kept = sorted(p for p in names if not p.startswith("org/"))
        if kept != EXPECTED_PATHS:
            raise BoundBad("paths outside org/ are %s, want %s" % (kept, EXPECTED_PATHS))
        if git(["ls-tree", base, "--", TEST_FILE]).strip():
            raise BoundBad("the test file already existed at the branch point")
        base_source = git(["show", "%s:%s" % (base, SERVED)])
        head_source = git(["show", "HEAD:%s" % SERVED])
        functions, classes = compare(base_source, head_source)
    except BoundBad as exc:
        print("O1-BOUND-BAD %s" % exc)
        return 1
    except BoundError as exc:
        print("O1-BOUND-ERROR %s" % exc)
        return 2
    print("O1-BOUND-OK functions=%d classes=%d files=%d" % (functions, classes, len(kept)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
