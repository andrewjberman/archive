#!/usr/bin/env python3
"""check_all_roots_round5 -- BS9-AC1 of LGIC_BLANKFIX.TO-BF-s-9. Takes no argument; run from the worktree root.

Re-runs `python lib/opal_naming_rootcheck.py all --map MAP`, compares it with ALL_ROOTS_round5.txt (the whole output, and
the last line), and checks the saved run: hole=0 and stopped=0; mapped + unmapped == roots_total; each root's saved run
(all_roots_round5/<root>.txt) equals the root's live run, its counts sum to its items; no FIX line carries a brace the
root check's own stray_braces does not admit (a per-firm {scope}, or the open places a key ruling's fills explains); no two
different current names of one type share a FIX target. Python 3.9; ASCII only; reads only; no AWS, no network.
"""
import os
import subprocess
import sys

MAP = "infra/logic/registry/root_map.json"
HERE = os.path.dirname(os.path.abspath(__file__))
KINDS = ("RIGHT", "FIX", "NOT-ASKED", "PATTERN", "CARDED", "REFUSED", "HOLE")


def _repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, stdout=subprocess.PIPE, check=True)
    return out.stdout.decode("utf-8").strip()


def _read(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8").splitlines()


def _fields(line):
    return dict(p.split("=", 1) for p in line.split()[1:] if "=" in p)


def _root_lines(lines):
    """The mapped roots' section lines of an `all` output, key -> line: ROOTCHECK and COMPLETED/STOPPED in one line."""
    out = {}
    for ln in lines:
        if ln.startswith("ROOT ") and " | " in ln:
            out[ln[5:].split(" | ", 1)[0]] = ln
    return out


def _repeat_diffs(live, saved):
    """The repeat over the MAPPED roots only: each saved mapped root's line against the live line of the same root (a saved
    root absent from the live run is a difference; a live root absent from the saved file is ADDED, not compared), and the
    ALL-ROOTS last lines field by field over the fields both carry (a field one line carries is listed, not a difference).
    UNMAPPED lines are not compared. Returns (differences, added roots, one-sided fields)."""
    diffs, lr, sr = [], _root_lines(live), _root_lines(saved)
    for key in sorted(sr):
        if key not in lr:
            diffs.append("%s: a saved mapped root is absent from the live run" % key)
        elif lr[key] != sr[key]:
            diffs.append("%s: the root line differs: live %s | saved %s" % (key, lr[key], sr[key]))
    added = sorted(k for k in lr if k not in sr)
    fl = _fields(live[-1]) if live else {}
    fs = _fields(saved[-1]) if saved else {}
    for k in sorted(set(fl) & set(fs)):
        if fl[k] != fs[k]:
            diffs.append("ALL-ROOTS field %s differs: live %s, saved %s" % (k, fl[k], fs[k]))
    one = ["%s (live only)" % k for k in sorted(set(fl) - set(fs))] + ["%s (saved only)" % k for k in sorted(set(fs) - set(fl))]
    return diffs, added, one


def main():
    repo = _repo_root()
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import json
    import opal_naming_rootcheck as rc
    bad = []
    proc = subprocess.run([sys.executable, "lib/opal_naming_rootcheck.py", "all", "--map", MAP],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    live = proc.stdout.decode("utf-8").splitlines()
    saved = _read(os.path.join(HERE, "ALL_ROOTS_round5.txt"))
    last_saved = saved[-1] if saved else ""
    if proc.returncode != 0:
        bad.append("the all command exited %d" % proc.returncode)
    diffs, added, one_sided = _repeat_diffs(live, saved)
    repeat = "identical" if not diffs else "DIFFERS"
    for d in diffs:
        bad.append(d)
    for r in added:
        print("ADDED " + r)
    for fld in one_sided:
        print("ONE-LINE-FIELD " + fld)
    f = _fields(last_saved)
    if not last_saved.startswith("ALL-ROOTS ok=True "):
        bad.append("the saved last line is not ALL-ROOTS ok=True: %r" % (last_saved,))
    hole, stopped = f.get("hole"), f.get("stopped")
    if hole != "0":
        bad.append("hole is %s, not 0" % hole)
    if stopped != "0":
        bad.append("stopped is %s, not 0" % stopped)
    total, mapped, unmapped = int(f.get("roots_total", -1)), int(f.get("mapped", -1)), int(f.get("unmapped", -1))
    if mapped + unmapped != total:
        bad.append("mapped %d + unmapped %d != roots_total %d" % (mapped, unmapped, total))
    with open(MAP, "rb") as fh:
        keys = sorted(json.loads(fh.read().decode("utf-8"))["roots"])
    keys = [k for k in keys if k not in added]  # an ADDED root has no saved run: listed above, not compared
    if len(keys) != mapped:
        bad.append("the map holds %d roots the saved run covers, the last line says mapped=%d" % (len(keys), mapped))
    items_all, braces_ok, fix_n = 0, 0, 0
    for key in keys:
        name = key.replace("/", "__") + ".txt"
        lines = _read(os.path.join(HERE, "all_roots_round5", name))
        live_lines, sink = [], []
        rc.check_root(rc._TF_PREFIX + key, MAP, out=live_lines.append, report_only=True, sink=sink)
        if live_lines != lines:
            bad.append("%s: the saved run differs from the live run" % key)
        last = lines[-1] if lines else ""
        if not last.startswith("ROOTCHECK ok=True "):
            bad.append("%s: the saved last line is not ROOTCHECK ok=True: %r" % (key, last))
        fl = _fields(last)
        items = int(fl.get("items", "-1"))
        body = lines[:-1]
        count = dict((k, 0) for k in KINDS)
        for ln in body:
            kind = ln.split(" ", 1)[0]
            if kind in count:
                count[kind] += 1
            else:
                bad.append("%s: a line of no kind: %s" % (key, ln))
        if sum(count.values()) != items:
            bad.append("%s: the counts sum to %d, the last line says items=%d" % (key, sum(count.values()), items))
        if count["HOLE"] != 0 or fl.get("hole") != "0":
            bad.append("%s: hole is not 0" % key)
        items_all += items
        rows = sink[1:]
        if len(rows) != len(body):
            bad.append("%s: %d rows for %d saved lines" % (key, len(rows), len(body)))
            continue
        targets = {}
        for (it, ans, kind, detail), ln in zip(rows, body):
            if kind != "FIX" or not ln.startswith("FIX "):
                continue
            fix_n += 1
            kr = ans.get("key_ruling")
            if rc.stray_braces(detail, rc._is_per_firm(kr), rc.admitted_places(kr)):
                bad.append("%s: a FIX line carries a brace not admitted: %s" % (key, ln))
            else:
                braces_ok += 1
            targets.setdefault((it["type"], detail), set()).add(it["current"])
        for (typ, tgt), names in sorted(targets.items()):
            if len(names) > 1:
                bad.append("%s: two current names of %s share the FIX target %s: %s" % (key, typ, tgt, sorted(names)))
    if str(items_all) != f.get("items"):
        bad.append("the roots' items sum to %d, the last line says items=%s" % (items_all, f.get("items")))
    for b in bad:
        print("FAIL: " + b)
    print("ALL-ROOTS-R5 ok=%s mapped=%d unmapped=%d items=%d hole=%s stopped=%s repeat=%s" % (
        not bad, mapped, unmapped, items_all, hole, stopped, repeat))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
