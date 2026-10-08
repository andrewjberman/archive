#!/usr/bin/env python3
"""sort_holes -- BS5-AC1 of LGIC_BLANKFIX.TO-BF-s-5. Takes no argument; run from the worktree root.

Runs opal_naming_rootcheck.check_root (report-only, output captured) over EVERY root the root map covers, takes every HOLE
line, and gives each ONE class by a rule on the line's own text and type (the CLASSES table below, tested in order). A line
no rule takes is NEW: printed whole with a name for what it is (NEW_KINDS), and it is a finding.
Writes HOLES_SORTED_round5.txt and HOLES_FOR_RULING_round5.md beside this file. Builds nothing in lib/.
Python 3.9; ASCII only; no AWS, no network.
"""
import contextlib
import io
import json
import os
import re
import subprocess
import sys

MAP = "infra/logic/registry/root_map.json"
HERE = os.path.dirname(os.path.abspath(__file__))
SORTED_TXT = os.path.join(HERE, "HOLES_SORTED_round5.txt")
RULING_MD = os.path.join(HERE, "HOLES_FOR_RULING_round5.md")


def _in(*needles):
    return lambda typ, detail: all(n in detail for n in needles)


# class -> (label, why, the test on (type, detail)). Tested in this order; the first that holds takes the line.
CLASSES = (
    ("carded", "S1", "detail says it was skipped by a card that gives no correct name and does not say none is owed",
     _in("it was skipped by a card", "the card gives no correct name and does not say none is owed")),
    ("event_rule", "S3", "type EVENT_RULE and detail says the event rule's on-{event} token is not ruled",
     lambda typ, d: typ == "EVENT_RULE" and "event rule:" in d and "token is not ruled" in d),
    ("source_bucket", "S2", "type S3_BUCKET, detail says the root serves more than one firm and the bucket gives no firm",
     lambda typ, d: typ == "S3_BUCKET" and "this root serves more than one firm" in d),
    ("unknown_word", "S4", "detail says a first word is in no vocabulary (R1.f), is neither a source nor a tier (K1), or "
     "is an unresolved token (R1.c)",
     lambda typ, d: ("is in no vocabulary" in d or "is neither a source nor a tier" in d or "is an unresolved token" in d)),
)
ORDER = tuple(c[0] for c in CLASSES) + ("new",)

# What a NEW line is, named by a test on the line; the class stays NEW (no rule takes it).
NEW_KINDS = (
    ("a stored-file key whose firm place {scope} is open on a multi-firm root (a key, not a bucket; the root map entry "
     "gives no firm, the bucket where read names none or was not read)",
     lambda typ, d: typ == "S3Key" and "this root serves more than one firm" in d),
    ("a name that two resources are given (a collision between FIX targets)", _in("two resources cannot take one name")),
)


def classify(typ, detail):
    for name, _lab, _why, test in CLASSES:
        if test(typ, detail):
            return name, ""
    for what, test in NEW_KINDS:
        if test(typ, detail):
            return "new", what
    return "new", "a hole no rule here takes and no named kind covers: read the line"


def _ascii(s):
    return s.encode("ascii", "replace").decode("ascii")


def _setup():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, stdout=subprocess.PIPE, check=True)
    repo = out.stdout.decode("utf-8").strip()
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import opal_naming_rootcheck
    return opal_naming_rootcheck


LINE = re.compile(r"^HOLE (\S+) (.*?) -> (.*)  \[(.*)\]$")


def collect(rootcheck):
    with open(MAP, "rb") as fh:
        keys = sorted(json.loads(fh.read().decode("utf-8"))["roots"])
    holes, roots, problems = [], [], []
    for key in keys:
        lines, sink = [], []
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rootcheck.check_root(key, MAP, out=lines.append, report_only=True, sink=sink)
        except Exception as exc:  # a stopped root is counted, never dropped
            problems.append("%s: stopped: %s: %s" % (key, type(exc).__name__, exc))
            roots.append({"root": key, "own": 0, "read": 0})
            continue
        last = lines[-1] if lines else ""
        if not last.startswith("ROOTCHECK "):
            problems.append("%s: no ROOTCHECK last line (last printed: %r)" % (key, last))
            roots.append({"root": key, "own": 0, "read": 0})
            continue
        own = int(dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)["hole"])
        # the bucket the check read for each HOLE line, from the sink (item, answers, kind, detail)
        buckets = {}
        for ent in sink:
            if isinstance(ent, tuple) and ent[2] == "HOLE":
                row = (ent[1] or {}).get("key") or {}
                buckets[(ent[0]["type"], ent[0]["current"], ent[0]["where"])] = row.get("bucket") or ""
        n = 0
        for ln in lines[:-1]:
            if not ln.startswith("HOLE "):
                continue
            m = LINE.match(ln)
            if not m:
                problems.append("%s: a HOLE line the pattern cannot split: %s" % (key, ln))
                continue
            typ, name, detail, where = m.groups()
            bucket = buckets.get((typ, name, where), "")
            if not bucket:
                mb = re.search(r"bucket (opal-[A-Za-z0-9-]+) names no firm", detail)
                bucket = mb.group(1) if mb else ""
            cls, what = classify(typ, detail)
            holes.append({"root": key, "type": typ, "name": name, "detail": detail, "where": where, "bucket": bucket,
                          "cls": cls, "what": what, "line": ln})
            n += 1
        roots.append({"root": key, "own": own, "read": n})
    return holes, roots, problems


def build_text(holes, roots, problems):
    out = []
    for h in holes:
        out.append("HOLE-SORT %s | %s | %s" % (h["root"], h["cls"], h["line"]))
    out.append("")
    out.append("CLASS TESTS (first that holds takes the line):")
    for name, lab, why, _t in CLASSES:
        out.append("  %-13s (%s) %s" % (name, lab, why))
    out.append("  %-13s (--) any hole no test above takes; printed whole below and named" % "new")
    out.append("")
    out.append("CLASS BY ROOT (every mapped root; own = the root's own hole= count):")
    out.append("  %-28s %6s %10s %13s %12s %4s %6s | own" % ("root", "carded", "event_rule", "source_bucket", "unknown_word",
                                                              "new", "total"))
    tot = dict((c, 0) for c in ORDER)
    for r in roots:
        mine = [h for h in holes if h["root"] == r["root"]]
        cnt = dict((c, sum(1 for h in mine if h["cls"] == c)) for c in ORDER)
        for c in ORDER:
            tot[c] += cnt[c]
        out.append("  %-28s %6d %10d %13d %12d %4d %6d | %d" % (
            r["root"], cnt["carded"], cnt["event_rule"], cnt["source_bucket"], cnt["unknown_word"], cnt["new"],
            len(mine), r["own"]))
    out.append("  %-28s %6d %10d %13d %12d %4d %6d | %d" % (
        "ALL", tot["carded"], tot["event_rule"], tot["source_bucket"], tot["unknown_word"], tot["new"], len(holes),
        sum(r["own"] for r in roots)))
    news = [h for h in holes if h["cls"] == "new"]
    out.append("")
    out.append("NEW LINES (%d), whole, and what each is:" % len(news))
    for h in news:
        out.append("NEW %s || %s" % (h["root"], h["line"]))
        out.append("    is: %s" % h["what"])
    for p in problems:
        out.append("FAIL: " + p)
    n = len(holes)
    ok = (not problems and sum(tot.values()) == n and n == sum(r["own"] for r in roots)
          and all(r["own"] == r["read"] for r in roots))
    out.append("HOLES-SORTED ok=%s roots=%d holes=%d carded=%d source_bucket=%d event_rule=%d unknown_word=%d new=%d" % (
        ok, len(roots), n, tot["carded"], tot["source_bucket"], tot["event_rule"], tot["unknown_word"], tot["new"]))
    return "\n".join(_ascii(x) for x in out) + "\n", ok


def _missing(h):
    d = h["detail"]
    if "it was skipped by a card" in d:
        return "skipped by a card; the card gives no correct name and does not say none is owed"
    i = d.find("partial form")
    if i >= 0:
        return d[i:]
    return d


ASK = {
    "carded": "S1 -- for each name: its whole correct name, or that none is owed, with the reason.",
    "source_bucket": "S2 -- for each bucket: how a bucket owned by a data source (no firm in its name) is written on a "
                     "root that serves several firms.",
    "event_rule": "S3 -- for each rule: the token for a rule fired by an event (the form asks for a cadence; an event rule "
                  "has none).",
    "unknown_word": "S4 -- for each name: is it a real stored path or group (then it needs a ruling) or a pattern in the "
                    "code (then it is printed as a pattern)?",
    "new": "NEW -- the class is not among S1 to S4: for each name, which of the four routes serves it, or a new ruling "
           "form is needed. The lines say the firm place {scope} is open on a multi-firm root.",
}
TITLE = {"carded": "carded (S1)", "source_bucket": "source-owned bucket on a multi-firm root (S2)",
         "event_rule": "event-fired rule with no ruled token (S3)", "unknown_word": "first word no vocabulary holds (S4)",
         "new": "NEW: no class of S1 to S4 takes the line"}


def build_md(holes):
    o = ["# Holes for ruling -- round 5 (LGIC_BLANKFIX, BF-s-5)", "",
         "Source: `sort_holes.py`, run over every root of `infra/logic/registry/root_map.json`; the lines are in "
         "`HOLES_SORTED_round5.txt`. One row per DISTINCT (type, name); `lines` is how many hole lines that name closes. "
         "Bucket is the one the check read, `-` where it read none. This file states facts and asks; it proposes no name.",
         ""]
    counts = {}
    for cls in ORDER:
        mine = [h for h in holes if h["cls"] == cls]
        groups = {}
        for h in mine:
            groups.setdefault((h["type"], h["name"]), []).append(h)
        counts[cls] = len(groups)
        o.append("## %s: %d lines, %d distinct names" % (TITLE[cls], len(mine), len(groups)))
        o.append("")
        o.append("Ask: " + ASK[cls])
        o.append("")
        o.append("| type | name | root | where | bucket read | what the line says is missing | lines |")
        o.append("|---|---|---|---|---|---|---|")
        for (typ, name), hs in sorted(groups.items()):
            roots = sorted(set(h["root"] for h in hs))
            wheres = sorted(set(h["where"] for h in hs))
            bks = sorted(set(h["bucket"] for h in hs if h["bucket"]))
            miss = []
            for h in hs:
                m = _missing(h)
                if m not in miss:
                    miss.append(m)
            o.append("| %s | `%s` | %s | %s | %s | %s | %d |" % (
                typ, name, ", ".join(roots), "; ".join(wheres), ", ".join(bks) or "-",
                " // ".join(miss).replace("|", "/"), len(hs)))
        o.append("")
    return _ascii("\n".join(o)), counts


def main():
    rootcheck = _setup()
    holes, roots, problems = collect(rootcheck)
    text, ok = build_text(holes, roots, problems)
    md, counts = build_md(holes)
    with open(SORTED_TXT, "wb") as fh:
        fh.write(text.encode("ascii"))
    with open(RULING_MD, "wb") as fh:
        fh.write((md + "\n").encode("ascii"))
    sys.stdout.write(text)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
