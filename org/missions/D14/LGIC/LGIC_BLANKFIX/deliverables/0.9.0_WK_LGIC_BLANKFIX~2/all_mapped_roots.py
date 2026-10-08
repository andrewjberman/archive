#!/usr/bin/env python3
"""all_mapped_roots -- BQ6-AC1 of LGIC_BLANKFIX.TO-BF-q-6. Takes no argument; run from the worktree root.

Runs opal_naming_rootcheck.check_root (report-only, output captured) over EVERY root the root map covers, in sorted order,
prints one line per root (root, its ROOTCHECK last line, COMPLETED or STOPPED), then the HOLE lines, then the totals line.
A root whose run raises or prints no ROOTCHECK last line is STOPPED with the reason; it is counted, never dropped.
Saves the per-root outputs under all_roots_round4/ and the table as ALL_MAPPED_ROOTS_round4.txt. The second run is a
fresh child process (--single) whose last line must equal the first run's. Python 3.9; ASCII only; no AWS, no network.
"""
import contextlib
import io
import json
import os
import subprocess
import sys

MAP = "infra/logic/registry/root_map.json"
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "all_roots_round4")
TABLE = os.path.join(HERE, "ALL_MAPPED_ROOTS_round4.txt")
KINDS = ("RIGHT", "FIX", "NOT-ASKED", "PATTERN", "CARDED", "REFUSED", "HOLE")
FIELDS = ("right", "fix", "not_asked", "pattern", "carded", "refused", "hole")


def _repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, stdout=subprocess.PIPE, check=True)
    return out.stdout.decode("utf-8").strip()


def _ascii(s):
    return s.encode("ascii", "replace").decode("ascii")


def run_all(rootcheck, scope):
    """Returns (rows, problems, lines_by_root). rows: dict per root, in sorted order."""
    with open(MAP, "rb") as fh:
        keys = sorted(json.loads(fh.read().decode("utf-8"))["roots"])
    rows, problems, outputs = [], [], {}
    for key in keys:
        lines, reason, fields = [], "", {}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rootcheck.check_root(key, MAP, out=lines.append, report_only=True)
        except Exception as exc:  # a stopped root is counted, never dropped
            reason = "%s: %s" % (type(exc).__name__, exc)
        last = lines[-1] if lines else ""
        if not reason and not last.startswith("ROOTCHECK "):
            reason = "no ROOTCHECK last line (last printed: %r)" % last
        row = {"root": key, "last": last, "stopped": bool(reason), "reason": reason}
        if not reason:
            fields = dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)
            body = lines[:-1]
            count = dict((k, 0) for k in KINDS)
            for ln in body:
                kind = ln.split(" ", 1)[0]
                if kind in count:
                    count[kind] += 1
                else:
                    problems.append("%s: a line of no kind: %s" % (key, ln))
            items = int(fields.get("items", "-1"))
            scope_n = len(scope.root_items("infra/aws/terraform/" + key, MAP)[0])
            if sum(count.values()) != items:
                problems.append("%s: the counts sum to %d, the last line says items=%d" % (key, sum(count.values()), items))
            if items != scope_n:
                problems.append("%s: items=%d but the scope's own count is %d" % (key, items, scope_n))
            row["items"] = items
            row["count"] = count
        rows.append(row)
        outputs[key] = lines
    return rows, problems, outputs


def totals_line(rows, problems):
    done = [r for r in rows if not r["stopped"]]
    stopped = len(rows) - len(done)
    tot = dict((k, sum(r["count"][k] for r in done)) for k in KINDS)
    items = sum(r["items"] for r in done)
    ok = (len(done) + stopped == len(rows)) and not problems
    return "ALL-ROOTS ok=%s roots=%d completed=%d stopped=%d items=%d %s" % (
        ok, len(rows), len(done), stopped, items,
        " ".join("%s=%d" % (f, tot[k]) for f, k in zip(FIELDS, KINDS)))


def _setup():
    repo = _repo_root()
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import opal_naming_rootcheck
    import opal_naming_scope
    return opal_naming_rootcheck, opal_naming_scope


def main():
    rootcheck, scope = _setup()
    rows, problems, outputs = run_all(rootcheck, scope)
    if "--single" in sys.argv:
        print(totals_line(rows, problems))
        return 0
    os.makedirs(OUTDIR, exist_ok=True)
    for key, lines in outputs.items():
        with open(os.path.join(OUTDIR, key.replace("/", "__") + ".txt"), "wb") as fh:
            fh.write(("\n".join(_ascii(x) for x in lines) + "\n").encode("ascii"))
    first = totals_line(rows, problems)
    proc = subprocess.run([sys.executable, os.path.abspath(__file__), "--single"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=110)
    second = proc.stdout.decode("utf-8").strip().splitlines()
    second = second[-1] if second else ""
    if proc.returncode == 0 and second == first:
        repeat = "repeat=identical"
    else:
        repeat = "repeat=DIFFERENT rc=%d first=[%s] second=[%s]" % (proc.returncode, first, second)
        problems.append(repeat)
        first = totals_line(rows, problems)
    out = []
    for r in rows:
        out.append("ROOT %s | %s | %s" % (r["root"], r["last"] or "-",
                                          ("STOPPED " + r["reason"]) if r["stopped"] else "COMPLETED"))
    for r in rows:
        if r["stopped"]:
            out.append("STOPPED %s: %s" % (r["root"], r["reason"]))
    for r in rows:
        for ln in outputs[r["root"]]:
            if ln.startswith("HOLE "):
                out.append("%s || %s" % (r["root"], ln))
    for p in problems:
        out.append("FAIL: " + p)
    out.append(repeat)
    out.append(first)
    text = "\n".join(_ascii(x) for x in out) + "\n"
    with open(TABLE, "wb") as fh:
        fh.write(text.encode("ascii"))
    sys.stdout.write(text)
    return 0 if " ok=True " in first else 1


if __name__ == "__main__":
    sys.exit(main())
