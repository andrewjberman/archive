"""AST words-only comparison of two status.py files: one CORRECTION_WORDS key may be added."""
import ast
import hashlib
import sys


def target_name(stmt):
    if isinstance(stmt, ast.Assign) and stmt.targets and isinstance(stmt.targets[0], ast.Name):
        return stmt.targets[0].id
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
        return stmt.target.id
    return None


def literal_dict(mod, name):
    for stmt in mod.body:
        if target_name(stmt) == name and isinstance(stmt.value, ast.Dict):
            return ast.literal_eval(stmt.value)
    return None


def main(argv):
    live_p, rel_p = argv[1], argv[2]
    live_src = open(live_p, "rb").read()
    rel_src = open(rel_p, "rb").read()
    print("live_bytes", len(live_src), "live_sha256", hashlib.sha256(live_src).hexdigest())
    print("rel_bytes", len(rel_src), "rel_sha256", hashlib.sha256(rel_src).hexdigest())
    la = ast.parse(live_src.decode("utf-8"))
    ra = ast.parse(rel_src.decode("utf-8"))
    print("top_level_statements", len(la.body), "and", len(ra.body))
    diff_idx = []
    for i, (a, b) in enumerate(zip(la.body, ra.body)):
        if ast.dump(a) != ast.dump(b):
            diff_idx.append(i)
    print("differing_statement_indices", diff_idx)
    for i in diff_idx:
        print("idx", i, "target", target_name(la.body[i]), target_name(ra.body[i]))
    left = literal_dict(la, "CORRECTION_WORDS")
    right = literal_dict(ra, "CORRECTION_WORDS")
    print("keys_live", len(left), "keys_release", len(right))
    added = sorted(set(right) - set(left))
    removed = sorted(set(left) - set(right))
    changed = sorted(k for k in set(left) & set(right) if left[k] != right[k])
    print("added_keys", added)
    print("removed_keys", removed)
    print("changed_values_shared_keys", changed)
    other = [i for i in diff_idx if target_name(la.body[i]) != "CORRECTION_WORDS"]
    print("other_statements_differing", other)
    verdict = (
        diff_idx == [18]
        and target_name(la.body[18]) == "CORRECTION_WORDS"
        and added == ["SHARES_PRICE_SOURCE_NOT_COMPOSED"]
        and not removed
        and not changed
        and not other
    )
    print("WORDS_ONLY_ONE_KEY_ADDED", verdict)
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
