"""Compare the served chatter body at days 30/90/365 against the snapshots taken before the edit.
Prints EQUAL n of 3; a body that differs while its vintage/as_of also differs is DRIFT (a snapshot landed)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture  # noqa: E402


def main():
    equal = 0
    for d in (30, 90, 365):
        with open(os.path.join(HERE, "before", "chatter_{0}.json".format(d)), encoding="utf-8") as f:
            before = json.load(f)
        after = capture.body(d)
        if after == before:
            equal += 1
            print("days {0}: EQUAL ({1} rows)".format(d, len(after.get("rows") or [])))
            continue
        moved = after.get("vintage") != before.get("vintage") or after.get("as_of") != before.get("as_of")
        diff = [k for k in sorted(set(before) | set(after)) if before.get(k) != after.get(k)]
        print("days {0}: {1} keys differing: {2}".format(d, "DRIFT (a snapshot landed)" if moved else "DIFFERENT", diff))
        br = {r["security_key"]: r for r in before.get("rows") or []}
        n = 0
        for r in after.get("rows") or []:
            b = br.get(r["security_key"])
            if b != r:
                n += 1
                if n <= 3:
                    print("   row", r["security_key"], [k for k in sorted(set(b or {}) | set(r)) if (b or {}).get(k) != r.get(k)])
        print("   rows differing:", n)
    print("EQUAL {0} of 3".format(equal))
    return 0 if equal == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
