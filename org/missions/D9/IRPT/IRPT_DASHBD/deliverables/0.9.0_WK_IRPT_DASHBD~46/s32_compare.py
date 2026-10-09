"""TO-DB-b-69 (S32): compares two s32_classify.py outputs (kit vs tested) exactly. Prints a JSON summary (counts and numbers only).

Usage: python <this file> <kit.json> <tested.json>
A difference is any key present on one side only, or any value that is not exactly equal (floats compared with ==, no tolerance).
Accounts in a difference are named by a 1-based ordinal in the sorted key list of that day and field, never by id.
"""
import json
import sys
from pathlib import Path


def walk(a, b, path, out, ordinal):
    if isinstance(a, dict) and isinstance(b, dict):
        keys = sorted(set(a) | set(b))
        for i, k in enumerate(keys, 1):
            label = "acct#%d" % i if ordinal else str(k)
            if k not in a or k not in b:
                out.append({"where": path + [label], "kit": a.get(k, "<absent>"), "tested": b.get(k, "<absent>")})
            else:
                walk(a[k], b[k], path + [label], out, ordinal and False)
    elif a != b:
        out.append({"where": path, "kit": a, "tested": b})


def main(kit, tested):
    k = json.loads(Path(kit).read_text(encoding="utf-8"))
    t = json.loads(Path(tested).read_text(encoding="utf-8"))
    diffs, counts = [], {}
    for day in sorted(set(k["days"]) | set(t["days"])):
        for field in ("flow", "income", "unvalued", "cash_unknown"):
            a, b = k["days"][day][field], t["days"][day][field]
            walk(a, b, [day, field], diffs, True)
            counts["%s/%s" % (day, field)] = len(a)
        for field in ("partition_absent", "census"):
            walk(k["days"][day][field], t["days"][day][field], [day, field], diffs, False)
    summary = {"n_accounts": [k["n_accounts"], t["n_accounts"]], "per_day_field_account_counts": counts,
               "equal": not diffs, "n_differences": len(diffs), "differences": diffs[:200],
               "runtime_kit": k["runtime"], "runtime_tested": t["runtime"]}
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:3])
