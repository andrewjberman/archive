#!/usr/bin/env python3
"""Compare two sweep files (sweep_runner.py output) by (project, round, order, criterion). Usage:
python .scratch/sweep_compare.py <before> <after> <classified-out>. Prints the counts; writes every differing line."""
import re
import sys

HEAD = re.compile(r"^== (\S+) (\S+) round (\d+) rc=(\S+)$")
JUDG = re.compile(r"^  JUDGMENT (\S+) (\S+) -> (GRADED|UNGRADED|SELF) \((.*)\)$")
SRC = re.compile(r"^(adjudication|investigation) row (\S+) by (\S+)(?: \(verdict ([^)]*)\))?")


def parse(path):
    runs, judg, close = {}, {}, {}
    key = None
    rcs = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            ln = raw.rstrip("\n")
            m = HEAD.match(ln)
            if m:
                key = (m.group(2), int(m.group(3)))
                runs[key] = ln
                rcs[key] = m.group(4)
                continue
            if ln.startswith("SWEEP "):
                continue
            if key is None:
                continue
            j = JUDG.match(ln)
            if j:
                judg[(key[0], key[1], j.group(1), j.group(2))] = (j.group(3), j.group(4))
                continue
            if ln.startswith("ROUND-CLOSE "):
                close[key] = ln
    return runs, judg, close


def source_of(state, why):
    m = SRC.match(why)
    if m:
        return "%s row %s" % (m.group(1), m.group(2))
    return "-"


def main(argv):
    b_runs, b_j, b_c = parse(argv[1])
    a_runs, a_j, a_c = parse(argv[2])
    out = []
    cats = {}
    for k in sorted(set(b_j) | set(a_j)):
        b = b_j.get(k)
        a = a_j.get(k)
        if b == a:
            continue
        if b is None or a is None:
            cat = "ONLY-IN-BEFORE" if a is None else "ONLY-IN-AFTER"
        elif b[0] == "GRADED" and a[0] == "UNGRADED":
            cat = "GRADED->UNGRADED"
        elif b[0] == "GRADED" and a[0] == "GRADED":
            cat = "GRADED->GRADED source changed" if source_of(*b) != source_of(*a) else "GRADED->GRADED detail only"
        else:
            cat = "%s->%s" % (b[0], a[0])
        cats[cat] = cats.get(cat, 0) + 1
        out.append("%s | %s round %d | %s %s | %s | before: %s [%s] | after: %s [%s]" % (
            cat, k[0], k[1], k[2], k[3], "", b[0] if b else "-", source_of(*b) if b else "-",
            a[0] if a else "-", source_of(*a) if a else "-"))
        if b and a:
            out.append("    before why: %s" % b[1])
            out.append("    after  why: %s" % a[1])
    close_changes = []
    for k in sorted(set(b_c) | set(a_c)):
        if b_c.get(k) != a_c.get(k):
            close_changes.append(k)
            out.append("ROUND-CLOSE CHANGE %s round %d" % (k[0], k[1]))
            out.append("    before: %s" % b_c.get(k, "-"))
            out.append("    after : %s" % a_c.get(k, "-"))
    verdict_changes = 0
    for k in close_changes:
        bv = re.search(r"verdict=(\S+)", b_c.get(k, "")) or None
        av = re.search(r"verdict=(\S+)", a_c.get(k, "")) or None
        if (bv and bv.group(1)) != (av and av.group(1)):
            verdict_changes += 1
    summary = ["RUNS compared=%d before=%d after=%d (projects=%d)" % (
        len(set(b_runs) & set(a_runs)), len(b_runs), len(a_runs), len(set(k[0] for k in a_runs)))]
    summary.append("JUDGMENT keys before=%d after=%d; lines that DIFFER: %d" % (
        len(b_j), len(a_j), sum(cats.values())))
    for c in sorted(cats):
        summary.append("  %s: %d" % (c, cats[c]))
    summary.append("ROUND-CLOSE lines that DIFFER: %d; verdict changes: %d" % (len(close_changes), verdict_changes))
    with open(argv[3], "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(summary + [""] + out) + "\n")
    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
