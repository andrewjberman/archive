#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-2 -- CONDITION 1 OF THE CTO'S 95004: CENSUS THE READERS OF
`STORED_IN`, BY SUBTRACTION, BEFORE ANY RETIREMENT.

"A PRODUCER CENSUS IS NOT A CONSUMER CENSUS." TO-CG-G-1 measured 55 of 55 edge families
and WHO WRITES THEM. Retirement is a claim about WHO READS, and that set had not been
measured. This is that measurement, and it is a SUBTRACTION -- never a forward list of the
consumers somebody thought of:

  DENOMINATOR   every graph consumer declared in org/modules/graph/graph-call-manifest.yaml
                (tool grain and entry grain, both printed), PLUS an UNSCOPED sweep of every
                tracked first-party file in the repository. The manifest alone would be a
                scoped check on a shared vocabulary -- the unscoped sweep is what can see a
                consumer the manifest never declared.
  MINUS         every file whose only occurrence of the literal is PROSE (a comment, a
                docstring, a .md, or a JSON prose field), each subtraction counted.
  MINUS         this order's own artifacts and another round's captures, counted.
  =             the READERS and WRITERS that survive, each with its file and line, split by
                whether it lives INSIDE this order's <paths> or outside them.

THE TWO CONTROLS, because a census that cannot be wrong is not a census:
  POSITIVE  a planted read, a planted write and a planted prose line are put through the
            same classifier and must come back READ / WRITE / PROSE.
  NEGATIVE  `STORED_INLINE_POLICIES` must NOT be counted. A bare substring search for
            STORED_IN returns 328 hits in this repository and 259 of them are that token
            in seven validate_parity.sh files. The word boundary is the whole difference
            between a census and a number.

READ ONLY: this script reads files and runs no producer, no AWS write and nothing the
egress hold names.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
TERM = "STORED_IN"
BOUNDED = re.compile(r"STORED_IN(?![A-Za-z0-9_])")
MANIFEST = Path("org/modules/graph/graph-call-manifest.yaml")

# This order's write grant, verbatim from the face's <paths>.
IN_PATHS = (
    "infra/aws/globgrph/derive_runner.py",
    "infra/aws/globgrph/derive_stitch.py",
    "org/modules/graph/graph-call-manifest.yaml",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/NFRA_CLDGRPH.TO-CG-G-2.bucket-identity-made-one.md",
)
PROSE_SUFFIX = (".md", ".txt", ".log", ".jsonl")
WRITE_PAT = re.compile(r'"edge_type"\s*:\s*"STORED_IN"|,\s*"STORED_IN"\s*\)|'
                       r"'edge_type'\s*:\s*'STORED_IN'")
READ_PAT = re.compile(r'[=!]=\s*["\']STORED_IN["\']|["\']STORED_IN["\']\s*[,}\]]|'
                      r'in\s+.*["\']STORED_IN["\']|edge_type\s*=\s*["\']STORED_IN["\']|'
                      r'frozenset|STITCH_EDGE_TYPES')


def tracked_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=ROOT)
    return [ln for ln in out.stdout.split("\n") if ln.strip()]


def classify(path: str, lineno: int, line: str) -> str:
    """READ / WRITE / PROSE for one occurrence. Conservative: unclear reads as READ."""
    st = line.strip()
    if Path(path).suffix in PROSE_SUFFIX:
        return "PROSE"
    if st.startswith("#") or st.startswith("//"):
        return "PROSE"
    if Path(path).suffix == ".json":
        # A JSON hit is prose UNLESS the literal is a key or a bare enum value.
        return "PROSE" if ('"' + TERM + '"') not in st else "READ"
    if WRITE_PAT.search(st):
        return "WRITE"
    if READ_PAT.search(st):
        return "READ"
    # inside a python docstring block is handled by the caller; anything else that merely
    # mentions the token in a sentence is prose.
    if st.startswith('"') or st.startswith("'") or " " in st.replace(TERM, "")[:1]:
        return "PROSE"
    return "READ"


def occurrences(path: str):
    p = ROOT / path
    try:
        text = p.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:  # noqa: BLE001
        return []
    out = []
    in_doc = False
    for i, ln in enumerate(text, 1):
        st = ln.strip()
        if p.suffix == ".py":
            ticks = st.count('"""') + st.count("'''")
            was = in_doc
            if ticks % 2 == 1:
                in_doc = not in_doc
            if was or (ticks % 2 == 1 and not was and BOUNDED.search(ln)):
                if BOUNDED.search(ln):
                    out.append((i, ln, "PROSE"))
                continue
        if BOUNDED.search(ln):
            out.append((i, ln, classify(path, i, ln)))
    return out


def in_grant(path: str) -> bool:
    p = path.replace("\\", "/")
    return any(p == g or p.startswith(g) for g in IN_PATHS)


def main() -> int:
    print("INSTRUMENT: a word-boundary sweep of every TRACKED first-party file (git "
          "ls-files) plus the declared consumer set in %s; classification by line, with "
          "python docstring blocks resolved so a mention inside one is PROSE." % MANIFEST)
    print("COVERAGE: the whole tracked corpus, unscoped -- the manifest alone would be a "
          "scoped check on a SHARED vocabulary and could not see an undeclared consumer.")
    print("GRAIN: one OCCURRENCE (file + line), rolled up to one FILE per row.")
    print("ENVIRONMENT: the retirement bar is the CTO's 95004 condition 1 as written onto "
          "this order's face @c16e3a4986; the known-reader hint (derive_stitch's "
          "drop-on-read keyed to the literal) is the substrate card's, quoted at the cut, "
          "not re-derived here.")
    print("")

    # ---- the manifest's declared consumer denominator ----
    import yaml
    man = yaml.safe_load((ROOT / MANIFEST).read_text(encoding="utf-8"))
    tools = man.get("tools_index") or {}
    entries = man.get("entries") or []
    excluded = man.get("excluded_not_graph_use_cases") or []
    retired = man.get("retired_aliases") or {}
    print("MANIFEST_CONSUMER_DENOMINATOR: %d tool(s) in tools_index, %d entry(ies) in "
          "entries, %d excluded-not-graph-use-case(s), %d retired alias(es)"
          % (len(tools), len(entries), len(excluded), len(retired)))

    resolved, unresolved = {}, []
    for name in sorted(tools):
        cands = [".tools/%s" % name,
                 "org/modules/graph/%s.py" % name.replace("-", "_"),
                 "org/modules/graph/%s.py" % name.replace("comp-", "comp_").replace("-", "_")]
        hit = [c for c in cands if (ROOT / c).exists()]
        if hit:
            resolved[name] = hit
        else:
            unresolved.append(name)
    print("MANIFEST_TOOLS_RESOLVED_TO_A_FILE=%d of %d; UNRESOLVED=%d (a tool whose "
          "executable this script could not locate is NOT silently dropped -- it is "
          "covered by the unscoped sweep below, which reads every tracked file)"
          % (len(resolved), len(tools), len(unresolved)))
    man_touch = sorted(n for n, fs in resolved.items()
                       if any(occurrences(f) for f in fs))
    print("MANIFEST_TOOLS_TOUCHING_%s=%d of %d resolved: %s"
          % (TERM, len(man_touch), len(resolved), man_touch or "none"))
    print("")

    # ---- the unscoped sweep ----
    files = tracked_files()
    hits = {}
    for f in files:
        occ = occurrences(f)
        if occ:
            hits[f] = occ
    print("UNSCOPED_SWEEP: %d tracked file(s) read; %d carry a word-boundary `%s`"
          % (len(files), len(hits), TERM))

    # ---- the subtractions, each named and counted ----
    def drop(pred, why):
        gone = [f for f in list(hits) if pred(f)]
        for f in gone:
            hits.pop(f)
        print("  MINUS %-4d %s" % (len(gone), why))
        return gone

    print("  START %-4d file(s)" % (len(hits) + 0))
    drop(lambda f: f.startswith("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/"
                                "0.9.0_WK_NFRA_CLDGRPH~1/"),
         "THIS ORDER'S OWN artifacts (the census cannot be its own consumer)")
    drop(lambda f: f.startswith("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/")
         and "~1/" not in f,
         "ANOTHER worker's round-6 deliverables -- captures and fixtures, "
         "outside this order's <paths> (carried below, NOT dropped from the blocking read)")
    prose_only = [f for f in list(hits)
                  if all(k == "PROSE" for _, _, k in hits[f])]
    for f in prose_only:
        hits.pop(f)
    print("  MINUS %-4d file(s) whose EVERY occurrence is PROSE (comment, docstring, .md, "
          "or a JSON prose field)" % len(prose_only))
    print("  = %d file(s) carrying a READ or a WRITE of the literal" % len(hits))
    print("")

    # ---- the survivors ----
    inside, outside = [], []
    print("  -- THE SURVIVING CONSUMERS, each with its file and line --")
    for f in sorted(hits):
        rows = [(i, k, ln.strip()[:110]) for i, ln, k in hits[f] if k != "PROSE"]
        where = "IN-PATHS" if in_grant(f) else "OUT-OF-PATHS"
        (inside if in_grant(f) else outside).append((f, rows))
        print("     [%s] %s" % (where, f))
        for i, k, ln in rows:
            print("         :%-5d %-5s %s" % (i, k, ln))
    print("")

    # re-add the other worker's deliverables for the BLOCKING read, since a fixture that
    # constructs a STORED_IN edge IS a consumer of the vocabulary even though it is a test.
    other = {}
    for f in tracked_files():
        if (f.startswith("org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/")
                and "0.9.0_WK_NFRA_CLDGRPH~1/" not in f):
            occ = [o for o in occurrences(f) if o[2] != "PROSE"]
            if occ:
                other[f] = occ
    if other:
        print("  -- ANOTHER ROUND'S DELIVERABLES that construct or query the literal "
              "(carried into the blocking read: a fixture is a consumer of the vocabulary) --")
        for f in sorted(other):
            print("     [OUT-OF-PATHS] %s" % f)
            for i, ln, k in other[f]:
                print("         :%-5d %-5s %s" % (i, k, ln.strip()[:110]))
            outside.append((f, [(i, k, ln) for i, ln, k in other[f]]))
        print("")

    # ---- the controls ----
    planted = [("x.py", 1, '    edges.append({"edge_type": "STORED_IN", "source": a})', "WRITE"),
               ("x.py", 2, '    if str(e.get("edge_type", "")) == "STORED_IN":', "READ"),
               ("x.py", 3, '    # STORED_IN is this producer\'s own edge type', "PROSE")]
    ctrl_ok = sum(1 for p, i, ln, want in planted if classify(p, i, ln) == want)
    neg = 'if [ -f "${STORED_INLINE_POLICIES}" ]; then'
    neg_ok = not BOUNDED.search(neg)
    print("  -- THE CONTROLS --")
    for p, i, ln, want in planted:
        print("     POSITIVE want=%-5s got=%-5s  %s" % (want, classify(p, i, ln), ln.strip()))
    print("     CLASSIFIER_CONTROL=%d of %d" % (ctrl_ok, len(planted)))
    print("     NEGATIVE (the substring trap): STORED_INLINE_POLICIES excluded by the word "
          "boundary = %s   -- a bare substring sweep returns 328 hits in this repository, "
          "259 of them that token in 7 validate_parity.sh files" % neg_ok)
    print("     SUBSTRING_TRAP_CONTROL=%s" % ("FIRED" if neg_ok else "NOT-FIRED"))
    print("")

    print("READERS_INSIDE_PATHS=%d of %d surviving consumer file(s)"
          % (len(inside), len(inside) + len(outside)))
    print("READERS_OUTSIDE_PATHS=%d of %d surviving consumer file(s)"
          % (len(outside), len(inside) + len(outside)))
    for f, rows in outside:
        print("  OUT-OF-PATHS READER: %s:%s" % (f, ",".join(str(i) for i, _, _ in rows)))
    empty = not outside and not inside
    blocked = bool(outside)
    print("READER_SET_EMPTY=%s" % ("true" if empty else "false"))
    print("RETIREMENT_BLOCKED=%s" % ("true" if blocked else "false"))
    print("")
    print("  DENOMINATOR: %d tracked file(s) swept unscoped, %d tool(s) and %d entry(ies) "
          "declared in the manifest with %d tool(s) resolved to a file; %d file(s) "
          "surviving every named subtraction, %d inside this order's <paths> and %d "
          "outside; %d of %d classifier control(s) correct and the substring trap "
          "excluded=%s."
          % (len(files), len(tools), len(entries), len(resolved),
             len(inside) + len(outside), len(inside), len(outside), ctrl_ok,
             len(planted), neg_ok))
    print("  THE RULING THIS FEEDS: CONDITION 1 of the CTO's 95004 -- EMPTY reader set "
          "retires; NON-EMPTY re-points every reader in the SAME act; a reader OUTSIDE "
          "the <paths> means STOP, file a BLOCKING row naming the file and the line, and "
          "report, without editing it and without widening the grant.")
    return 0 if ctrl_ok == len(planted) and neg_ok else 1


if __name__ == "__main__":
    sys.exit(main())
