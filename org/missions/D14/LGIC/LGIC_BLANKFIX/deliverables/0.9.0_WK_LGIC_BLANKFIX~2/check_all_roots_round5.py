#!/usr/bin/env python3
"""check_all_roots_round5 -- BS9-AC1 of LGIC_BLANKFIX.TO-BF-s-9. Takes no argument; run from the worktree root.

Re-runs `python lib/opal_naming_rootcheck.py all --map MAP`, compares it with ALL_ROOTS_round5.txt (the whole output, and
the last line), and checks the saved run: hole=0 and stopped=0; mapped + unmapped == roots_total; each root's saved run
(all_roots_round5/<root>.txt) holds in the root's live run (BF-v-6: compared by NAME and VERDICT -- a name is (type, current,
file), its verdict is (kind, text after "->"); the line number in [file:line] is not compared, a repeated name is a multiset;
a live name the saved run lacks is ADDED-NAME and is not a difference, a saved name absent live, or present with another kind
or answer, is a difference printed whole both ways; a line kind only the live run carries, as UNCOUNTED, is listed, not
compared), its counts sum to its items; no FIX line carries a brace the
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


def _name(line):
    """A name line -> (kind, type, current, file, answer), or None when the line is not `KIND type current -> detail  [file:line]`."""
    kind = line.split(" ", 1)[0]
    if kind not in KINDS or " -> " not in line or not line.rstrip().endswith("]") or "  [" not in line:
        return None
    head, tail = line.split(" -> ", 1)
    detail, _, where = tail.rpartition("  [")
    parts = head.split(" ", 2)
    if len(parts) < 3:
        return None
    return kind, parts[1], parts[2], where[:-1].rsplit(":", 1)[0], detail.strip()


def _name_diffs(live_lines, saved_lines):
    """Compare one root's live run with its saved run by name and verdict. Returns (differences, ADDED-NAME lines, live-only kinds)."""
    names = {}
    for tag, lines in (("saved", saved_lines), ("live", live_lines)):
        for ln in lines:
            n = _name(ln)
            if n is not None:
                names.setdefault(n[1:4], {"saved": [], "live": []})[tag].append((n[0], n[4], ln))
    diffs, added = [], []
    for key in sorted(names):
        sv, lv = list(names[key]["saved"]), list(names[key]["live"])
        for item in list(sv):
            m = [x for x in lv if x[:2] == item[:2]]
            if m:
                sv.remove(item)
                lv.remove(m[0])
        if not sv and not lv:
            continue
        if not names[key]["saved"]:
            added.extend(x[2] for x in lv)
            continue
        while sv and lv:
            a, b = sv.pop(0), lv.pop(0)
            diffs.append("the same name changed: saved %s | live %s" % (a[2], b[2]))
        for a in sv:
            diffs.append("a saved name is absent from the live run: %s" % a[2])
        added.extend(x[2] for x in lv)
    return diffs, added


def _repeat_diffs(live, saved):
    """The repeat over the MAPPED roots only: each saved mapped root against the live run -- present, and its COMPLETED/STOPPED
    status the same (its counts and its names are compared by name in the per-root pass; a count moves when a name is added).
    A live root absent from the saved file is ADDED, not compared. The ALL-ROOTS last lines are compared on roots_total and
    stopped only: the other fields are sums over the roots, which move when a root or a name is added, and are listed. A line
    kind the live run carries and the saved one does not (UNCOUNTED, NOTHING-TO-NAME) is listed with its count, not compared.
    UNMAPPED lines are not compared. Returns (differences, added roots, one-sided fields, live-only kinds)."""
    diffs, lr, sr = [], _root_lines(live), _root_lines(saved)
    for key in sorted(sr):
        if key not in lr:
            diffs.append("%s: a saved mapped root is absent from the live run" % key)
        elif lr[key].rsplit(" | ", 1)[-1] != sr[key].rsplit(" | ", 1)[-1]:
            diffs.append("%s: the root status differs: live %s | saved %s" % (key, lr[key], sr[key]))
    added = sorted(k for k in lr if k not in sr)
    fl = _fields(live[-1]) if live else {}
    fs = _fields(saved[-1]) if saved else {}
    moved = []
    for k in sorted(set(fl) & set(fs)):
        if fl[k] != fs[k]:
            if k in ("roots_total", "stopped"):
                diffs.append("ALL-ROOTS field %s differs: live %s, saved %s" % (k, fl[k], fs[k]))
            else:
                moved.append("%s live %s saved %s (sum over roots)" % (k, fl[k], fs[k]))
    one = ["%s (live only)" % k for k in sorted(set(fl) - set(fs))] + ["%s (saved only)" % k for k in sorted(set(fs) - set(fl))]
    kinds_saved = set(ln.split(" ", 1)[0] for ln in saved)
    counts = {}
    for ln in live:
        k = ln.split(" ", 1)[0]
        if k not in kinds_saved:
            counts[k] = counts.get(k, 0) + 1
    kinds = ["UNLISTED-KIND %s lines=%d" % (k, counts[k]) for k in sorted(counts)]
    return diffs, added, one + ["FIELD-MOVED " + m for m in moved], kinds


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
    diffs, added, one_sided, live_kinds = _repeat_diffs(live, saved)
    repeat = "identical" if not diffs else "DIFFERS"
    for d in diffs:
        bad.append(d)
    for r in added:
        print("ADDED " + r)
    for fld in one_sided:
        print(("" if fld.startswith("FIELD-MOVED") else "ONE-LINE-FIELD ") + fld)
    for k in live_kinds:
        print(k)
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
    saved_roots = set(_root_lines(saved))
    keys = [k for k in keys if k in saved_roots]  # a root with no saved run (ADDED, or NOTHING-TO-NAME) is not compared
    if len(keys) != mapped:
        bad.append("the map holds %d roots the saved run covers, the last line says mapped=%d" % (len(keys), mapped))
    items_all, braces_ok, fix_n = 0, 0, 0
    for key in keys:
        name = key.replace("/", "__") + ".txt"
        lines = _read(os.path.join(HERE, "all_roots_round5", name))
        live_lines, sink = [], []
        rc.check_root(rc._TF_PREFIX + key, MAP, out=live_lines.append, report_only=True, sink=sink)
        nd, nadded = _name_diffs(live_lines, lines)
        for d in nd:
            bad.append("%s: %s" % (key, d))
        for a in nadded:
            print("ADDED-NAME %s: %s" % (key, a))
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
        rows, live_body = sink[1:], live_lines[:-1]
        if len(rows) != len(live_body):
            bad.append("%s: %d rows for %d live lines" % (key, len(rows), len(live_body)))
            continue
        # the brace and target checks run on the saved names as the live run answers them; an ADDED name is not graded here
        pool = {}
        for ln in body:
            n = _name(ln)
            if n is not None:
                pool[n] = pool.get(n, 0) + 1
        targets = {}
        for (it, ans, kind, detail), ln in zip(rows, live_body):
            n = _name(ln)
            if n is None or pool.get(n, 0) < 1:
                continue
            pool[n] -= 1
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
