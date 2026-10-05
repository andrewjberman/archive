"""AMGT-au-6 AC2 -- the nine Lead Panel bodies AFTER the change equal the `before/` bodies, ignoring `generated_at`.

Run from the repo root with PYTHONPATH=<repo root>. Calls the local handler for each of the nine reads (capture9.READS),
loads the matching `before/<name>.json`, drops every `generated_at` key at any depth from both sides, compares the parsed
values, and prints one line per read and `EQUAL n of 9`. Exit 0 only on 9 of 9. Each fresh body is also written to `after/`.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture9  # noqa: E402


def strip(node):
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items() if k != "generated_at"}
    if isinstance(node, list):
        return [strip(v) for v in node]
    return node


def first_diff(a, b, path="$"):
    if type(a) is not type(b):
        return "%s: type %s vs %s" % (path, type(a).__name__, type(b).__name__)
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return "%s.%s: present on one side only" % (path, k)
            d = first_diff(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "%s: length %d vs %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    return None if a == b else "%s: %r vs %r" % (path, a, b)


def main():
    equal = 0
    os.makedirs(os.path.join(HERE, "after"), exist_ok=True)
    for path, q in capture9.READS:
        name = capture9.name(path, q)
        status, body = capture9.get(path, q)
        with open(
            os.path.join(HERE, "after", name), "w", encoding="utf-8", newline="\n"
        ) as f:
            json.dump(body, f, indent=1, sort_keys=True)
        with open(os.path.join(HERE, "before", name), encoding="utf-8") as f:
            before = json.load(f)
        diff = first_diff(strip(before), strip(body))
        ok = status == 200 and diff is None
        equal += 1 if ok else 0
        print(
            "%s %s status=%s rows=%s%s"
            % (
                "EQ " if ok else "DIFF",
                name,
                status,
                len(body.get("rows") or []),
                "" if ok else " first diff " + str(diff),
            )
        )
    print("EQUAL %d of %d" % (equal, len(capture9.READS)))
    return 0 if equal == len(capture9.READS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
