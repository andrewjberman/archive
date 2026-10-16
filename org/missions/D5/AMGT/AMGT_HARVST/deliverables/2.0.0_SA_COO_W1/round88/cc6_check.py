"""HVST-cc-6 shape check (issuer file, read-only for the worker).

Usage: python cc6_check.py <triage.json> [<population.json>]

The triage file is a JSON list of rows {id, verdict, reason, read, new_owner}. The population is the issuer's
cc6_population.json (the 32 OPEN remediation rows). It prints one summary line and exits 0 only when every
population id appears exactly once, every verdict is in the enum, every reason is at least 40 characters,
a "met" row names the read that meets it (path or command, at least 12 characters), and a "re-owned" row names a
new_owner that looks like an agent serial and a next_act of at least 20 characters. It does NOT judge whether a verdict is right: the CVO reads that.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERDICTS = ("met", "re-owned", "dismissed")
SERIAL = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+_[A-Za-z]+_[A-Za-z0-9]+(~[A-Za-z0-9]+)?$")


def main(argv):
    if not argv:
        print("TRIAGE FAIL usage: cc6_check.py <triage.json> [<population.json>]")
        return 2
    triage_path = Path(argv[0])
    pop_path = Path(argv[1]) if len(argv) > 1 else HERE / "cc6_population.json"
    if not triage_path.is_file():
        print("TRIAGE FAIL no triage file at %s" % triage_path)
        return 1
    pop = [p["id"] for p in json.loads(pop_path.read_text(encoding="utf-8"))["population"]]
    rows = json.loads(triage_path.read_text(encoding="utf-8"))
    problems = []
    seen = {}
    for r in rows:
        rid = r.get("id")
        seen[rid] = seen.get(rid, 0) + 1
        if r.get("verdict") not in VERDICTS:
            problems.append("%s verdict %r" % (rid, r.get("verdict")))
        if len(str(r.get("reason", "")).strip()) < 40:
            problems.append("%s reason under 40 characters" % rid)
        if r.get("verdict") == "met" and len(str(r.get("read", "")).strip()) < 12:
            problems.append("%s met without a read" % rid)
        if r.get("verdict") == "re-owned" and not SERIAL.match(str(r.get("new_owner", ""))):
            problems.append("%s re-owned without a serial in new_owner" % rid)
        if r.get("verdict") == "re-owned" and len(str(r.get("next_act", "")).strip()) < 20:
            problems.append("%s re-owned without a next_act" % rid)
    missing = [i for i in pop if i not in seen]
    extra = [i for i in seen if i not in pop]
    dup = [i for i, n in seen.items() if n > 1]
    problems += ["missing %s" % i for i in missing] + ["extra %s" % i for i in extra] + ["duplicate %s" % i for i in dup]
    counts = {v: sum(1 for r in rows if r.get("verdict") == v) for v in VERDICTS}
    if problems:
        print("TRIAGE FAIL rows=%d population=%d problems=%d first=%s" % (len(rows), len(pop), len(problems), problems[0]))
        return 1
    print("TRIAGE OK rows=%d population=%d met=%d reowned=%d dismissed=%d" % (
        len(rows), len(pop), counts["met"], counts["re-owned"], counts["dismissed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
