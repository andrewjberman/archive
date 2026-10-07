#!/usr/bin/env python3
"""check_second_root -- BR6-AC1 of LGIC_BLANKFIX.TO-BF-r-6. Takes no argument; run from the worktree root.

Re-runs `python lib/opal_naming_rootcheck.py ROOT --map MAP --report-only`, compares it with the saved trace, and checks the
run against the scope's own count. Python 3.9; ASCII only. Reads only; writes nothing.
"""
import os
import subprocess
import sys

ROOT = "infra/aws/terraform/investor-reporting/directory"
MAP = "infra/logic/registry/root_map.json"
HERE = os.path.dirname(os.path.abspath(__file__))
SAVED = os.path.join(HERE, "SECOND_ROOT_TRACE_round3.txt")
KINDS = ("RIGHT", "FIX", "NOT-ASKED", "PATTERN", "CARDED", "REFUSED", "HOLE")


def _repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, stdout=subprocess.PIPE, check=True)
    return out.stdout.decode("utf-8").strip()


def main():
    repo = _repo_root()
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import opal_naming_scope
    bad = []
    proc = subprocess.run([sys.executable, "lib/opal_naming_rootcheck.py", ROOT, "--map", MAP, "--report-only"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    text = proc.stdout.decode("utf-8")
    lines = text.splitlines()
    with open(SAVED, "rb") as fh:
        saved = fh.read().decode("utf-8")
    differs = 0 if text.splitlines() == saved.splitlines() else 1
    if differs:
        bad.append("the re-run differs from the saved trace")
    if proc.returncode != 0:
        bad.append("the run exited %d" % proc.returncode)
    last = lines[-1] if lines else ""
    if not last.startswith("ROOTCHECK ok=True "):
        bad.append("the last line does not read ROOTCHECK ok=True: %r" % (last,))
    body = lines[:-1]
    count = dict((k, 0) for k in KINDS)
    for ln in body:
        kind = ln.split(" ", 1)[0]
        if kind in count:
            count[kind] += 1
        else:
            bad.append("a line of no kind: " + ln)
    fields = dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)
    items = int(fields.get("items", "-1"))
    if sum(count.values()) != items:
        bad.append("the counts sum to %d, the last line says items=%d" % (sum(count.values()), items))
    scope_n = len(opal_naming_scope.root_items(ROOT, MAP)[0])
    if items != scope_n:
        bad.append("items=%d but len(root_items(root, map)[0]) = %d" % (items, scope_n))
    for ln in body:
        if ln.startswith("FIX ") and "{" in ln:
            bad.append("a FIX line carries a brace: " + ln)
    targets = {}
    for ln in body:
        if ln.startswith("FIX "):
            head, rest = ln.split(" -> ", 1)
            parts = head.split(" ")
            typ, cur = parts[1], parts[2]
            tgt = rest.rsplit("  [", 1)[0]
            targets.setdefault((typ, tgt), set()).add(cur)
    for (typ, tgt), names in sorted(targets.items()):
        if len(names) > 1:
            bad.append("two current names of %s share the FIX target %s: %s" % (typ, tgt, sorted(names)))
    for k in KINDS:
        print("%s %d" % (k, count[k]))
    for b in bad:
        print("FAIL: " + b)
    print("SECOND-ROOT ok=%s root=%s items=%d hole=%d differs=%d" % (not bad, ROOT, items, count["HOLE"], differs))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
