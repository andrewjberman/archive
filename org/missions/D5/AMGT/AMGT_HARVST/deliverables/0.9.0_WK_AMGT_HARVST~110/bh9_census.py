"""HVST-bh-9 (round 63): what the bare-name fallback loses when it matches the company string in its STORED CASE only.

READ-ONLY (S3 GET through the served iterator, no put). Reads the r60 list file and every latest silver article.

AFTER  = `pg._security_mentions` as it stands in this worktree.
BEFORE = the matcher with the fallback case-insensitive again -- THE MUTANT OF PLANT (vi): each empty-alias security is
         handed to the same function with `aliases = [company]` (which is exactly what `aliases or [company]` made of an
         empty list before bh-9). To show that the mutant IS the old code, the base commit's `publication_gold.py`
         (BASE_COMMIT, read with `git show`) is also run on the empty-alias securities and must return the same
         `mention_count` on every article (line `MUTANT EQUALS BASE MODULE`).
SECURITIES WITH ALIASES CHANGED compares the base module with this one on every security that has aliases, over every
article, on the full result dict (all fields `_security_mentions` returns).

Run from the repo root of the worktree:  PYTHONPATH=. python -u <this file>
"""
import json
import os
import subprocess
import sys
import types

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
LIST_FILE = os.path.join(HERE, "..", "2.0.0_SA_COO_H", "round60", "securities.universe.r60.json")
BASE_COMMIT = "7e75953bf3"
CONTEXT = 120
TRUE_PAIRS = ("sa:4473686", "sa:4441205")


def _load_base_module():
    src = subprocess.run(["git", "show", "%s:lib/research/harvest/publication_gold.py" % BASE_COMMIT],
                         cwd=REPO, check=True, capture_output=True).stdout.decode("utf-8")
    mod = types.ModuleType("publication_gold_base")
    mod.__file__ = os.path.join(REPO, "lib", "research", "harvest", "publication_gold.py")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def _asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def _spans(text, company, field):
    """Every span of the company string (case-insensitive, word-bounded) in one text, with 120 chars each side."""
    out = []
    pattern = pg._span_pattern([company])
    if pattern is None or not text:
        return out
    for m in pattern.finditer(text):
        out.append({"where": field, "text": m.group(0),
                    "case": "stored case" if m.group(0) == company else "other case",
                    "context": text[max(0, m.start() - CONTEXT):m.end() + CONTEXT]})
    return out


def main():
    with open(LIST_FILE, encoding="utf-8") as fh:
        securities = json.load(fh)
    S = len(securities)
    empties = [s for s in securities if not s.get("aliases")]
    aliased = [s for s in securities if s.get("aliases")]
    E = len(empties)
    base = _load_base_module()
    mutants = []
    for s in empties:
        m = dict(s)
        m["aliases"] = [s["company"]]
        mutants.append(m)

    stats = {s["security_key"]: {"before": 0, "after": 0, "removed": 0} for s in empties}
    removed = []
    mutant_vs_base_diff = 0
    aliased_changed = set()
    n = 0
    for row in pg._iter_latest_articles():
        n += 1
        if n % 1000 == 0:
            print("progress: %d articles read" % n, flush=True)
        for s, m in zip(empties, mutants):
            before = pg._security_mentions(row, m)["mention_count"]
            if before != base._security_mentions(row, s)["mention_count"]:
                mutant_vs_base_diff += 1
            after = pg._security_mentions(row, s)["mention_count"]
            st = stats[s["security_key"]]
            st["before"] += 1 if before >= 1 else 0
            st["after"] += 1 if after >= 1 else 0
            if before >= 1 and after < 1:
                st["removed"] += 1
                spans = _spans(row.get("title") or "", s["company"], "title")
                for i, block in enumerate(row.get("text_blocks") or []):
                    spans += _spans(block, s["company"], "block %d" % i)
                removed.append({"security_key": s["security_key"], "company": s["company"],
                                "article_key": row.get("article_key"), "title": row.get("title"), "spans": spans})
        for s in aliased:
            if s["security_key"] in aliased_changed:
                continue
            if pg._security_mentions(row, s) != base._security_mentions(row, s):
                aliased_changed.add(s["security_key"])

    lines = []
    lines.append("DENOMINATOR: securities %d, with an empty alias list %d, silver articles %d" % (S, E, n))
    for s in empties:
        st = stats[s["security_key"]]
        lines.append("%s company=%s: pairs before %d after %d removed %d"
                     % (s["security_key"], s["company"], st["before"], st["after"], st["removed"]))
    removed.sort(key=lambda p: (p["security_key"], p["article_key"]))
    lines.append("REMOVED PAIRS: %d" % len(removed))
    for p in removed:
        lines.append("  %s | %s | %s" % (p["security_key"], p["article_key"], _asc(p["title"])))
        if not p["spans"]:
            lines.append("      (no span of the company string in any case)")
        for sp in p["spans"]:
            lines.append("      [%s] `%s` (%s): ...%s..." % (
                sp["where"], _asc(sp["text"]), sp["case"],
                _asc(sp["context"].replace("\n", " ").replace("\r", " "))))
    gone = {p["article_key"] for p in removed}
    lines.append("TRUE PAIRS LOST BY NAME: " + ", ".join(
        "%s %s" % (k, "removed" if k in gone else "still present") for k in TRUE_PAIRS))
    lines.append("MUTANT EQUALS BASE MODULE (%s): differing (article, security) counts %d"
                 % (BASE_COMMIT, mutant_vs_base_diff))
    lines.append("SECURITIES WITH ALIASES CHANGED: %d of %d" % (len(aliased_changed), S - E))

    fail = []
    if n <= 0:
        fail.append("N == 0")
    if E <= 0:
        fail.append("E == 0")
    stored = [p for p in removed if any(sp["case"] == "stored case" for sp in p["spans"])]
    if stored:
        fail.append("%d removed pair(s) have a stored-case span: %s"
                    % (len(stored), [(p["security_key"], p["article_key"]) for p in stored][:5]))
    nokia = [s for s in empties if s["company"].lower() == "nokia"]
    if not nokia:
        fail.append("no Nokia among the empty-alias securities")
    for s in nokia:
        if stats[s["security_key"]]["removed"] != 0:
            fail.append("Nokia removed %d" % stats[s["security_key"]]["removed"])
    for k in TRUE_PAIRS:
        if k not in gone:
            fail.append("true pair %s is not removed" % k)
    if aliased_changed:
        fail.append("SECURITIES WITH ALIASES CHANGED is %d" % len(aliased_changed))
    if mutant_vs_base_diff:
        fail.append("the mutant differs from the base module on %d counts" % mutant_vs_base_diff)
    lines.append("CENSUS OK" if not fail else "CENSUS FAIL: " + "; ".join(fail))

    out = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "bh9_census.out"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
