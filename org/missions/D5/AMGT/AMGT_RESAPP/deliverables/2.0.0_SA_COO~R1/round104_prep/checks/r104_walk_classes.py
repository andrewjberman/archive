"""AMGT_RESAPP round-104 PREP -- a ui-walk's findings BY CLASS (the inventory a worker's prose is never a substitute for; round 103's packet missed four format:money hits because this was not read).

  python r104_walk_classes.py <walk.txt> [<walk2.txt> ...] [--max-money N]
  python r104_walk_classes.py --selftest

Each walk text file is the walker's own stdout; its `OUT <folder>` line names the output folder whose `findings.json` is read. Prints, per walk, every finding class with its count and, for
the classes `format:money`, `raw-code` and `unconnected-field` (the FWD-40 (a) classes), the observed text. Verdict: `R104 MONEY FORMAT: YES|NO (format:money <n> in <k> walk(s))`
(YES when the count is at most --max-money, default 0); exit 0|1. A walk text with no OUT line or an unreadable findings file is NO, never a silent zero.
"""
import collections
import json
import os
import re
import sys

FWD40 = ("format:money", "raw-code", "unconnected-field")


def findings_of(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"\bOUT\s+(\S.*?)\s*$", text, re.M)
    if not m:
        return None, "no OUT line in %s" % path
    folder = m.group(1).strip().replace("\\", "/")
    f = os.path.join(folder, "findings.json")
    try:
        d = json.load(open(f, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, "findings.json unreadable (%s)" % exc
    return (d if isinstance(d, list) else d.get("findings", [])), f


def classes(items):
    c = collections.Counter(it.get("check") for it in items)
    seen = {}
    for it in items:
        if it.get("check") in FWD40:
            seen.setdefault(it["check"], []).append((it.get("observed") or "")[:110])
    return c, seen


def selftest():
    import tempfile

    arms = []
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "out"))
        json.dump([{"check": "format:money", "observed": "money written as USD 1,234 and $1,234 on one page"}, {"check": "layout:clipped", "observed": "x"}],
                  open(os.path.join(d, "out", "findings.json"), "w"))
        open(os.path.join(d, "w.txt"), "w").write("20:00:00 OUT %s\nSUMMARY: 2 unique\n" % os.path.join(d, "out"))
        items, _ = findings_of(os.path.join(d, "w.txt"))
        c, seen = classes(items)
        arms.append(c["format:money"] == 1 and "format:money" in seen)
        open(os.path.join(d, "none.txt"), "w").write("no out line here\n")
        arms.append(findings_of(os.path.join(d, "none.txt"))[0] is None)
        json.dump([{"check": "layout:clipped"}], open(os.path.join(d, "out", "findings.json"), "w"))
        items, _ = findings_of(os.path.join(d, "w.txt"))
        arms.append(classes(items)[0]["format:money"] == 0)
    for i, ok in enumerate(arms, 1):
        print("   %s A%d" % ("PASS" if ok else "FAIL", i))
    print("R104 WALK CLASSES ARMS: %s" % ("YES" if all(arms) else "NO"))
    return 0 if all(arms) else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    limit = int(argv[argv.index("--max-money") + 1]) if "--max-money" in argv else 0
    files = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--max-money")]
    money, bad = 0, 0
    for path in files:
        items, where = findings_of(path)
        if items is None:
            print("WALK %s: UNREADABLE (%s)" % (path, where))
            bad += 1
            continue
        c, seen = classes(items)
        print("WALK %s (%s): %s" % (os.path.basename(path), where, ", ".join("%s x%d" % (k, v) for k, v in sorted(c.items(), key=lambda kv: str(kv[0])))))
        for k, v in seen.items():
            for text in v[:5]:
                print("   %s: %s" % (k, text))
        money += c["format:money"]
    ok = not bad and bool(files) and money <= limit
    print("R104 MONEY FORMAT: %s (format:money %d in %d walk(s)%s)" % ("YES" if ok else "NO", money, len(files), ", %d unreadable" % bad if bad else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
