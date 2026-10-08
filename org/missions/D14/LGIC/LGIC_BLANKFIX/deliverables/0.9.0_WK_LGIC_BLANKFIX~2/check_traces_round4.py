#!/usr/bin/env python3
"""check_traces_round4 -- BQ5-AC1 of LGIC_BLANKFIX.TO-BF-q-5. Takes no argument; run from the worktree root.

Re-runs `python lib/opal_naming_rootcheck.py ROOT --map MAP --report-only` for both roots, compares each with its saved
trace line for line, and checks each live output. Python 3.9; ASCII only. Reads only; writes nothing.
"""
import os
import subprocess
import sys

MAP = "infra/logic/registry/root_map.json"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = (
    ("infra/aws/terraform/bd-pipeline", "THREAD_TRACE_round4_bd-pipeline.txt"),
    ("infra/aws/terraform/investor-reporting/directory", "SECOND_ROOT_TRACE_round4.txt"),
)
KINDS = ("RIGHT", "FIX", "NOT-ASKED", "PATTERN", "CARDED", "REFUSED", "HOLE")
FILL = "{scope} is filled per firm"  # the phrase a per-firm FIX line carries (AMENDMENT 1)


def _repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, stdout=subprocess.PIPE, check=True)
    return out.stdout.decode("utf-8").strip()


def check_root(root, saved_name, opal_naming_scope):
    bad = []
    proc = subprocess.run([sys.executable, "lib/opal_naming_rootcheck.py", root, "--map", MAP, "--report-only"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    lines = proc.stdout.decode("utf-8").splitlines()
    with open(os.path.join(HERE, saved_name), "rb") as fh:
        saved = fh.read().decode("utf-8").splitlines()
    differs = 0 if lines == saved else 1
    if differs:
        bad.append("%s: the re-run differs from the saved trace %s" % (root, saved_name))
    if proc.returncode != 0:
        bad.append("%s: the run exited %d" % (root, proc.returncode))
    last = lines[-1] if lines else ""
    if not last.startswith("ROOTCHECK ok=True "):
        bad.append("%s: the last line does not read ROOTCHECK ok=True: %r" % (root, last))
    fields = dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)
    items = int(fields.get("items", "-1"))
    body = lines[:-1]
    count = dict((k, 0) for k in KINDS)
    for ln in body:
        kind = ln.split(" ", 1)[0]
        if kind in count:
            count[kind] += 1
        else:
            bad.append("%s: a line of no kind: %s" % (root, ln))
    if count["HOLE"] != 0 or fields.get("hole") != "0":
        bad.append("%s: hole is not 0 (lines=%d, last line hole=%s)" % (root, count["HOLE"], fields.get("hole")))
    if count["REFUSED"] != 0 or fields.get("refused") != "0":
        bad.append("%s: refused is not 0 (lines=%d, last line refused=%s)" % (root, count["REFUSED"], fields.get("refused")))
    if sum(count.values()) != items:
        bad.append("%s: the counts sum to %d, the last line says items=%d" % (root, sum(count.values()), items))
    scope_n = len(opal_naming_scope.root_items(root, MAP)[0])
    if items != scope_n:
        bad.append("%s: items=%d but len(root_items(root, map)[0]) = %d" % (root, items, scope_n))
    per_firm = 0
    for ln in body:
        has_scope = "{scope}" in ln
        if ln.startswith("FIX "):
            if "{" in ln.replace("{scope}", "") or "}" in ln.replace("{scope}", ""):
                bad.append("%s: a FIX line carries a brace other than {scope}: %s" % (root, ln))
            elif has_scope and FILL in ln:
                per_firm += 1
            elif has_scope:
                bad.append("%s: a FIX line carries {scope} without naming the per-firm fill: %s" % (root, ln))
        elif has_scope:
            bad.append("%s: {scope} on a line that is not a FIX line: %s" % (root, ln))
        if ln.startswith("NOT-ASKED ") and "rename" not in ln:
            bad.append("%s: a NOT-ASKED line without 'rename': %s" % (root, ln))
    targets = {}
    for ln in body:
        if ln.startswith("FIX ") and " -> " in ln:
            head, rest = ln.split(" -> ", 1)
            parts = head.split(" ")
            targets.setdefault((parts[1], rest.rsplit("  [", 1)[0]), set()).add(parts[2])
    for (typ, tgt), names in sorted(targets.items()):
        if len(names) > 1:
            bad.append("%s: two current names of %s share the FIX target %s: %s" % (root, typ, tgt, sorted(names)))
    print("ROOT %s items=%d right=%d fix=%d not_asked=%d pattern=%d carded=%d refused=%d hole=%d per_firm=%d differs=%d" % (
        root, items, count["RIGHT"], count["FIX"], count["NOT-ASKED"], count["PATTERN"], count["CARDED"],
        count["REFUSED"], count["HOLE"], per_firm, differs))
    return bad, items, count["HOLE"], count["REFUSED"], differs


def main():
    repo = _repo_root()
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import opal_naming_scope
    bad, items, hole, refused, differs = [], 0, 0, 0, 0
    for root, saved in ROOTS:
        b, i, h, r, d = check_root(root, saved, opal_naming_scope)
        bad += b
        items += i
        hole += h
        refused += r
        differs += d
    for b in bad:
        print("FAIL: " + b)
    print("TRACES-R4 ok=%s roots=%d items=%d hole=%d refused=%d differs=%d" % (not bad, len(ROOTS), items, hole, refused, differs))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
