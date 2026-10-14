"""AST proof that a file changed only by one added CORRECTION_WORDS entry.

Usage: python ast_words_only.py <before.py> <after.py> <new_key>
Exit 0 only when the after-module equals the before-module once the new key is removed from the
CORRECTION_WORDS dict literal, and the new key is present exactly once in the after-module.
"""
import ast
import sys


def table(tree):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "CORRECTION_WORDS" for t in node.targets):
            return node.value
    raise SystemExit("no CORRECTION_WORDS assignment")


def main(argv):
    before_path, after_path, key = argv[1], argv[2], argv[3]
    before = ast.parse(open(before_path, encoding="utf-8").read())
    after = ast.parse(open(after_path, encoding="utf-8").read())
    keys_before = [k.value for k in table(before).keys]
    keys_after = [k.value for k in table(after).keys]
    print("CORRECTION_WORDS keys before: %d, after: %d" % (len(keys_before), len(keys_after)))
    print("new key count in after: %d" % keys_after.count(key))
    added = [k for k in keys_after if k not in keys_before]
    print("keys added: %s; keys removed: %s" % (added, [k for k in keys_before if k not in keys_after]))
    t = table(after)
    idx = [i for i, k in enumerate(t.keys) if k.value == key]
    if len(idx) == 1:
        del t.keys[idx[0]]
        del t.values[idx[0]]
    same = ast.dump(before) == ast.dump(after)
    print("ast equal after removing the new key: %s" % same)
    ok = same and keys_after.count(key) == 1 and added == [key]
    print("AST-WORDS-ONLY-OK" if ok else "AST-WORDS-ONLY-FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
