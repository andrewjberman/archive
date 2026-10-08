#!/usr/bin/env python3
"""sort_unmapped_roots -- BF-u-1: sort the unmapped Terraform roots by whether they declare a stored name.

Run from the repository root:  python <this file>

The unmapped roots are taken from the check's own `all` command (lib/opal_naming_rootcheck.py all --map
infra/logic/registry/root_map.json): the `UNMAPPED <root> names=N` lines and the `ALL-ROOTS ... roots_total= mapped=
unmapped=` line. No second list of roots is kept. Each root's names are read from lib/opal_naming_scope.root_items (the
enumeration the `all` command counts) and counted by type.

THE RULE (one class per root, the first test that applies):
  names-zero      the scope gives the root no name at all (the census's reading, NOT a verdict: the ruling file decides).
  no-stored-name  it has names and none of them is a STORED name. A stored name is one of the types STORED_TYPES:
                  S3_BUCKET (a bucket), S3Key (a stored-file key), DYNAMODB_TABLE (a table), EVENT_RULE (a rule).
  to-map          anything else (at least one stored name).

Writes UNMAPPED_ROOTS_round6.txt beside this script. Last line: UNMAPPED-SORTED ok=... (see main). Python 3.9; ASCII only.
"""
import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
for _ in range(7):
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, "lib"))
import opal_naming_scope  # noqa: E402

MAP = "infra/logic/registry/root_map.json"
STORED_TYPES = ("S3_BUCKET", "S3Key", "DYNAMODB_TABLE", "EVENT_RULE")
OUT_TXT = os.path.join(HERE, "UNMAPPED_ROOTS_round6.txt")
RULING = os.path.join(HERE, "MAP_ENTRIES_FOR_RULING_round6.md")


def run_all():
    p = subprocess.run([sys.executable, os.path.join("lib", "opal_naming_rootcheck.py"), "all", "--map", MAP],
                       cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    return p.returncode, p.stdout.decode("utf-8", "replace").splitlines()


def classify(by_type):
    if not by_type:
        return "names-zero"
    if not any(t in STORED_TYPES for t in by_type):
        return "no-stored-name"
    return "to-map"


def main():
    rc, lines = run_all()
    roots = [m.group(1) for m in (re.match(r"UNMAPPED (\S+) names=(\S+)$", ln) for ln in lines) if m]
    counts = dict((m.group(1), m.group(2)) for m in (re.match(r"UNMAPPED (\S+) names=(\S+)$", ln) for ln in lines) if m)
    last = [ln for ln in lines if ln.startswith("ALL-ROOTS ")]
    fields = dict(p.split("=", 1) for p in last[-1].split()[1:] if "=" in p) if last else {}
    total, mapped, unmapped = (int(fields.get(k, "-1")) for k in ("roots_total", "mapped", "unmapped"))
    rows = []
    for r in roots:
        items = opal_naming_scope.root_items(r, os.path.join(REPO, MAP))[0]
        by = collections.Counter(i["type"] for i in items)
        cls = classify(by)
        rows.append((cls, r, len(items), by, counts[r]))
    order = {"to-map": 0, "no-stored-name": 1, "names-zero": 2}
    rows.sort(key=lambda x: (order[x[0]], -x[2], x[1]))
    out = []
    for cls, r, n, by, cnt in rows:
        out.append("%-14s %s names=%d | %s" % (cls, r, n, ", ".join("%s=%d" % kv for kv in sorted(by.items())) or "-"))
    cc = collections.Counter(x[0] for x in rows)
    out.append("")
    out.append("CLASS COUNTS (rule: names-zero = no name; no-stored-name = names, none of %s; to-map = the rest)"
               % "/".join(STORED_TYPES))
    for c in ("names-zero", "no-stored-name", "to-map"):
        out.append("  %-14s %d" % (c, cc[c]))
    out.append("  %-14s %d" % ("sum", sum(cc.values())))
    with open(OUT_TXT, "w", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))
    sections, decl = -1, -1
    if os.path.isfile(RULING):
        with open(RULING, "rb") as fh:
            txt = fh.read().decode("utf-8")
        sections = len(re.findall(r"^### ", txt, re.M))
        decl = len(re.findall(r"^verdict: DECLARES-NAMES", txt, re.M))
    counts_match = all(str(x[2]) == x[4] for x in rows)
    ok = (rc == 0 and sum(cc.values()) == unmapped == len(roots) and mapped + unmapped == total
          and sections == unmapped and counts_match)
    print("UNMAPPED-SORTED ok=%s roots_total=%d mapped=%d unmapped=%d names_zero=%d no_stored_name=%d to_map=%d "
          "sections=%d declares_names=%d" % (ok, total, mapped, unmapped, cc["names-zero"], cc["no-stored-name"],
                                             cc["to-map"], sections, decl))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
