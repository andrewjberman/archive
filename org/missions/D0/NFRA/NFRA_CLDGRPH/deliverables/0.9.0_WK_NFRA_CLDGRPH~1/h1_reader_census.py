#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-1 / CG-s-36 -- H1-AC1: THE READER CENSUS WITH THE REPOSITORY AS ITS
DENOMINATOR, AND THE MANIFEST BESIDE IT RATHER THAN INSTEAD OF IT.

WHY THIS SCRIPT EXISTS AND WHY IT IS NOT g2_reader_census.py:
Round 7 ran the CTO's condition 1 exactly as written. That condition named
`org/modules/graph/graph-call-manifest.yaml` as the denominator, and over that denominator
MANIFEST_TOOLS_TOUCHING_STORED_IN = 0 of 78 -- an honest zero for that domain, with the
resolution arm present and passing (78 of 78 names resolved to a file). The unscoped sweep of
the same repository found consumers the manifest never declared. A MANIFEST IS A DECLARATION
OF CONSUMERS, NOT A CENSUS OF THEM, and the whole finding is the DELTA between the two
numbers. So this script prints BOTH, and the delta, and refuses to let either stand alone.

FOUR THINGS EVERY NUMBER BELOW CARRIES (spine v3.8 cut discipline, plus this round's TREE):
  TREE         which CHECKOUT the instrument scanned, with a positive control that can only
               fire in this worktree. A comp-rail denominator from a linked worktree is
               inadmissible without it: before the caller-tree fix, the rail scanned the MAIN
               tree from a worktree and returned a well-formed zero with a real denominator,
               and nothing in the output said which tree it read.
  COVERAGE     the population swept and its denominator, WITH what the denominator excludes.
  GRAIN        one OCCURRENCE (file + line), rolled up to one FILE per consumer row.
  ENVIRONMENT  where the comparison values came from -- named inline at each number.

THE ENUMERATION IS A SUBTRACTION, NEVER A FORWARD LIST (Rule 24(i)): the consumer set is
written as THE PRINTED REPOSITORY DENOMINATOR MINUS each named exclusion, each exclusion
counted on its own line. A forward list covers what its author had in mind and omits silently.

CONTROLS:
  TREE POSITIVE   h1_tree_control.marker exists ONLY on branch wk-cldgrph-8-1. Two independent
                  instruments must both find it: the native git enumeration this script uses,
                  and the comp-rail (`comp-find`) as a second instrument on a second corpus
                  definition. Either missing it => TREE_POSITIVE_CONTROL is NOT fired.
  CLASSIFIER      one planted line per class -- READ / WRITE / FIXTURE / PROSE -- through the
                  same classifier the census uses. 4 of 4 or the census is not admissible.
  SUBSTRING TRAP  STORED_INLINE_POLICIES must NOT be counted. A bare substring search returns
                  hundreds of hits in this repository, most of them that token. The word
                  boundary is the difference between a census and a number.

READ ONLY. No producer run, no AWS call, no write outside this file's own stdout.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
DELIV = "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/"
TERM = "STORED_IN"
BOUNDED = re.compile(r"STORED_IN(?![A-Za-z0-9_])")
MANIFEST = "org/modules/graph/graph-call-manifest.yaml"
CONTROL = DELIV + "h1_tree_control.marker"
CONTROL_TOKEN = "H1_TREE_CONTROL_MARKER_WK_CLDGRPH_8_1"

# The EPHEMERAL FLOOR this denominator excludes, printed rather than assumed.
FLOOR = ("__pycache__/", ".scratch/", ".git/")
PROSE_SUFFIX = (".md", ".txt", ".log", ".jsonl", ".marker")
FIXTURE_PAT = re.compile(r"(^|[/_])tests?[/_.]|(^|[/_])test_|_test\.|fixture", re.I)
WRITE_PAT = re.compile(r'"edge_type"\s*:\s*"STORED_IN"|,\s*"STORED_IN"\s*\)|'
                       r"'edge_type'\s*:\s*'STORED_IN'|"
                       r'\(\s*[A-Za-z_0-9\[\]"\']+\s*,\s*"STORED_IN"\s*,')
READ_PAT = re.compile(r'[=!]=\s*["\']STORED_IN["\']|["\']STORED_IN["\']\s*[,}\])]|'
                      r'in\s+.*["\']STORED_IN["\']|edge_type\s*=\s*["\']STORED_IN["\']|'
                      r'frozenset|STITCH_EDGE_TYPES|["\']STORED_IN["\']')


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, cwd=str(ROOT))
    return out.stdout


def on_floor(p: str) -> bool:
    return any(seg in p for seg in FLOOR)


def classify(path: str, line: str) -> str:
    """READ / WRITE / FIXTURE / PROSE for ONE occurrence.

    ORDER IS THE MECHANISM: prose first (a mention is never a consumer), then FIXTURE by PATH
    (a test that constructs the edge IS a consumer of the vocabulary, but it is a different
    remedy from a producer), then WRITE, then READ. Unclear falls to READ -- conservative,
    because a missed reader is the error that breaks a retirement.
    """
    st = line.strip()
    suf = Path(path).suffix
    if suf in PROSE_SUFFIX:
        return "PROSE"
    if st.startswith("#") or st.startswith("//"):
        return "PROSE"
    if suf == ".json":
        # A JSON hit is a DATA VALUE only when the literal is a whole quoted token; the
        # literal inside a long narrative string (a `verified_by` paragraph, a row body)
        # is PROSE and must not enter the consumer set.
        if ('"' + TERM + '"') not in st:
            return "PROSE"
        return "FIXTURE" if FIXTURE_PAT.search(path) else "WRITE"
    if FIXTURE_PAT.search(path):
        return "FIXTURE"
    if WRITE_PAT.search(st):
        return "WRITE"
    if READ_PAT.search(st):
        return "READ"
    return "READ"


def occurrences(path: str):
    """Every word-boundary occurrence in one file, python docstring blocks resolved to PROSE."""
    p = ROOT / path
    try:
        text = p.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:  # noqa: BLE001
        return []
    out, in_doc = [], False
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
            out.append((i, ln, classify(path, ln)))
    return out


def main() -> int:
    print("INSTRUMENT: a word-boundary sweep of every file in the REPOSITORY corpus (git")
    print("  ls-files tracked UNION git ls-files --others --exclude-standard), classified per")
    print("  OCCURRENCE, with python docstring blocks resolved so a mention inside one is")
    print("  PROSE; the call manifest is read as ONE INPUT beside it, never as the domain.")
    print("COVERAGE: the whole repository corpus, UNSCOPED. EXCLUDED and printed below: the")
    print("  gitignored arm and a named ephemeral floor. The manifest-scoped arm is reported")
    print("  separately BECAUSE it is the scoped domain whose zero authorized a breaking")
    print("  retirement last round -- it is the comparison, not the denominator.")
    print("GRAIN: one OCCURRENCE (file + line), rolled up to one FILE per consumer row.")
    print("ENVIRONMENT: the comparison values are round 7's own numbers, cited where used:")
    print("  MANIFEST_TOOLS_TOUCHING_STORED_IN=0 of 78 and 5 consumers outside the manifest")
    print("  (rows NFRA_CLDGRPH-W1-S38 and -S110). This run re-measures both from scratch.")
    print("")

    # ---------------- TREE ----------------
    top = git("rev-parse", "--show-toplevel").strip()
    gdir = git("rev-parse", "--absolute-git-dir").strip()
    common = git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    is_wt = "worktrees" in gdir.replace("\\", "/")
    print("TREE_READ=%s" % ("WORKTREE" if is_wt else "MAIN"))
    print("  TOPLEVEL:   %s" % top)
    print("  GIT_DIR:    %s" % gdir)
    print("  COMMON_DIR: %s" % (common or "(unread)"))
    print("  BRANCH:     %s" % git("rev-parse", "--abbrev-ref", "HEAD").strip())
    print("  HEAD:       %s" % git("rev-parse", "HEAD").strip())

    tracked = [ln for ln in git("ls-files").split("\n") if ln.strip()]
    untracked = [ln for ln in git("ls-files", "--others", "--exclude-standard").split("\n")
                 if ln.strip()]
    ignored = [ln for ln in git("ls-files", "--others", "--ignored",
                                "--exclude-standard").split("\n") if ln.strip()]
    corpus = sorted({p for p in tracked + untracked if not on_floor(p)})
    floor_n = len([p for p in tracked + untracked if on_floor(p)])

    native_ctrl = CONTROL in corpus
    # SECOND INSTRUMENT, SECOND CORPUS DEFINITION: the comp-rail. This is what makes the tree
    # claim admissible rather than self-reported -- the rail resolves its own corpus root, and
    # before the caller-tree fix it resolved to the MAIN tree from here.
    rail_ctrl, rail_line = False, "(not run)"
    try:
        r = subprocess.run([sys.executable, ".tools/comp-find", CONTROL_TOKEN,
                            "org/missions/D0/NFRA/NFRA_CLDGRPH", "--files"],
                           capture_output=True, text=True, cwd=str(ROOT), timeout=60)
        rail_ctrl = CONTROL in r.stdout
        for ln in r.stdout.split("\n"):
            if "DENOMINATOR" in ln:
                rail_line = ln.strip()
    except Exception as exc:  # noqa: BLE001
        rail_line = "ERROR: %s" % exc
    print("  CONTROL_FILE:           %s  (exists ONLY on branch wk-cldgrph-8-1)" % CONTROL)
    print("  NATIVE_ENUMERATION_SEES_IT=%s" % ("yes" if native_ctrl else "NO"))
    print("  COMP_RAIL_SEES_IT=%s   rail: %s"
          % ("yes" if rail_ctrl else "NO", rail_line))
    fired = (native_ctrl and rail_ctrl) if is_wt else False
    print("TREE_POSITIVE_CONTROL=%s"
          % ("FIRED" if fired else ("N/A-MAIN-TREE" if not is_wt else "NOT-FIRED")))
    print("")

    # ---------------- THE TWO DENOMINATORS ----------------
    print("REPOSITORY_DENOMINATOR=%d file(s)" % len(corpus))
    print("  = %d tracked + %d untracked-not-ignored, MINUS %d on the named ephemeral floor %s"
          % (len(tracked), len(untracked), floor_n, list(FLOOR)))
    print("  WHAT THE DENOMINATOR EXCLUDES, counted rather than asserted -- because a")
    print("  denominator that does not say what it dropped is not a denominator:")
    floor_files = [p for p in tracked + untracked if on_floor(p)]
    by_seg = {s: len([p for p in floor_files if s in p]) for s in FLOOR}
    print("    ephemeral floor    %-5d file(s)  %s" % (floor_n, by_seg))
    print("    gitignored arm     %-5d file(s)  (never entered the union above)" % len(ignored))
    # THE FLOOR IS NOT ASSERTED SAFE, IT IS TESTED, AND THE TEST IS PER SEGMENT -- because
    # the two segments are excluded for DIFFERENT reasons and one shared verdict over both
    # would certify each by the other's argument.
    #   __pycache__/  a .pyc embeds its module's string constants, so it CAN carry the
    #                 literal; when it does it is a COMPILED COPY of a .py the census already
    #                 reads, so dropping it cannot lose a consumer.
    #   .scratch/     a worker's private scratch directory (standing law: scratch is
    #                 `<worktree>/.scratch/` only). Not a consumer surface at all: nothing
    #                 imports it, nothing runs it in production, and it is per-session.
    corpus_set = set(corpus)
    seg_hits = {s: 0 for s in FLOOR}
    pyc_hits, pyc_covered = 0, 0
    scratch_named = []
    for p in floor_files:
        try:
            b = (ROOT / p).read_bytes()
        except Exception:  # noqa: BLE001
            continue
        if TERM.encode() not in b:
            continue
        for s in FLOOR:
            if s in p:
                seg_hits[s] += 1
        if "__pycache__/" in p:
            pyc_hits += 1
            src = re.sub(r"__pycache__/(.+?)\.cpython-\d+\.pyc$", r"\1.py", p)
            if src in corpus_set:
                pyc_covered += 1
        if ".scratch/" in p:
            scratch_named.append(p)
    print("    FLOOR_EXCLUSION_TESTED, per segment (a shared verdict would certify each")
    print("    segment by the other segment's argument):")
    print("      __pycache__/ : %d of %d carry the literal; %d of those %d resolve to a SOURCE"
          % (seg_hits["__pycache__/"], by_seg["__pycache__/"], pyc_covered, pyc_hits))
    print("                     .py inside the denominator -> no consumer can be lost here.")
    print("      .scratch/    : %d of %d carry the literal, ALL NAMED: %s"
          % (seg_hits[".scratch/"], by_seg[".scratch/"], scratch_named or "none"))
    print("                     Worker scratch, per standing law -- a private per-session")
    print("                     working directory, not a consumer surface. Named rather than")
    print("                     counted so a reader can overrule the exclusion.")
    print("      .git/        : %d of %d." % (seg_hits[".git/"], by_seg[".git/"]))

    import yaml
    man = yaml.safe_load((ROOT / MANIFEST).read_text(encoding="utf-8"))
    tools = man.get("tools_index") or {}
    entries = man.get("entries") or []
    print("MANIFEST_DENOMINATOR=%d tool(s)" % len(tools))
    print("  the same file also carries %d entry(ies); this is the domain the CTO's condition 1"
          % len(entries))
    print("  named, and it is reported here as a COMPARISON, never as the census.")
    resolved, unresolved = {}, []
    for name in sorted(tools):
        cands = [".tools/%s" % name,
                 "org/modules/graph/%s.py" % name.replace("-", "_"),
                 "org/modules/graph/%s.py" % name.replace("comp-", "comp_").replace("-", "_")]
        hit = [c for c in cands if (ROOT / c).exists()]
        (resolved.setdefault(name, hit) if hit else unresolved.append(name))
    print("  MANIFEST_TOOLS_RESOLVED_TO_A_FILE=%d of %d; UNRESOLVED=%d -- an unresolved name is"
          % (len(resolved), len(tools), len(unresolved)))
    print("  NOT silently dropped: it is covered by the repository sweep, which reads every file.")
    print("")

    # ---------------- THE SUBTRACTION ----------------
    hits = {}
    for f in corpus:
        occ = occurrences(f)
        if occ:
            hits[f] = occ
    print("  THE ENUMERATION, WRITTEN AS A SUBTRACTION FROM THE PRINTED DENOMINATOR:")
    print("  START %-5d file(s) of %d carrying a word-boundary `%s`"
          % (len(hits), len(corpus), TERM))

    prose_only = [f for f in hits if all(k == "PROSE" for _, _, k in hits[f])]
    for f in prose_only:
        hits.pop(f)
    print("  MINUS %-5d file(s) whose EVERY occurrence is PROSE (a comment, a docstring, a .md,"
          % len(prose_only))
    print("        or the literal inside a narrative JSON string). A mention is not a consumer.")

    own = [f for f in hits if Path(f).name.startswith("h1_")]
    for f in own:
        hits.pop(f)
    print("  MINUS %-5d file(s) that are THIS CELL'S OWN artifacts (h1_*): a census cannot be"
          % len(own))
    print("        its own consumer. NOTHING ELSE IS SUBTRACTED -- in particular no prior")
    print("        round's deliverable and no test is dropped, because for a RETIREMENT")
    print("        question a fixture that constructs the edge IS a consumer of the vocabulary.")
    print("  = %-5d file(s) carrying a READ, WRITE or FIXTURE use of the literal" % len(hits))
    print("")

    grant = tuple(ln.strip() for ln in """
infra/aws/globgrph/derive_runner.py
infra/aws/globgrph/derive_stitch.py
org/modules/graph/graph-call-manifest.yaml
org/modules/graph/tsgraph_spike/load_scratch_kuzu.py
org/modules/graph/tsgraph_spike/out/ts_semantic_benchmark_slice.producer.json
org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/
org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f11_edges_resolve.sh
org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f11_test_unified.py
org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f4_test_stitch_ingest.py
org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md
org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/NFRA_CLDGRPH.TO-CG-H-1.stored-in-retirement-own-cell.md
""".strip().split("\n"))

    def in_grant(p: str) -> bool:
        return any(p == g or (g.endswith("/") and p.startswith(g)) for g in grant)

    print("  -- THE SURVIVING CONSUMERS, each with its file and line, and whether this order's")
    print("     <paths> grant reaches it (a consumer OUTSIDE the grant cannot be re-pointed in")
    print("     the same act, which is the RETIRE branch's one forbidden outcome) --")
    inside, outside = [], []
    for f in sorted(hits):
        rows = [(i, k, ln.strip()[:104]) for i, ln, k in hits[f] if k != "PROSE"]
        g = in_grant(f)
        (inside if g else outside).append(f)
        print("     [%s] %s" % ("IN-GRANT    " if g else "OUT-OF-GRANT", f))
        for i, k, ln in rows:
            print("         :%-5d %-8s %s" % (i, k, ln))
    print("")

    man_consumers = sorted(n for n, fs in resolved.items()
                           if any(o for f in fs for o in occurrences(f) if o[2] != "PROSE"))
    print("REPOSITORY_CONSUMERS=%d" % len(hits))
    print("  of the %d-file repository denominator; %d inside this order's <paths> and %d outside."
          % (len(corpus), len(inside), len(outside)))
    print("MANIFEST_CONSUMERS=%d" % len(man_consumers))
    print("  of the %d-tool manifest denominator (%d resolved to a file): %s"
          % (len(tools), len(resolved), man_consumers or "none"))
    print("DOMAIN_DELTA=%d" % (len(hits) - len(man_consumers)))
    print("  THE DELTA IS THE FINDING: the manifest-scoped domain sees %d consumer(s); the"
          % len(man_consumers))
    print("  repository holds %d. A census over the manifest returns EMPTY and AUTHORIZES the"
          % len(hits))
    print("  retirement -- and an empty set is the branch that gets ACTED ON rather than argued")
    print("  with. Round 7 measured this delta at 5 (row W1-S38); this run re-measures it at %d."
          % (len(hits) - len(man_consumers)))
    print("")

    # ---------------- CONTROLS ----------------
    planted = [
        ("derive_stitch.py", '        edges.append(_e(resolved, present_firm_buckets[own], "STORED_IN"))', "WRITE"),
        ("derive_runner.py", '        if str(e.get("edge_type", "")) == "STORED_IN":', "READ"),
        ("f4_test_stitch_ingest.py", '    {"edge_type": "STORED_IN", "source": "s3:gold/a", "target": "b"},', "FIXTURE"),
        ("derive_stitch.py", "    # STORED_IN is this producer's OWN edge type (nothing else writes one)", "PROSE"),
    ]
    print("  -- THE CONTROLS --")
    ok = 0
    for p, ln, want in planted:
        got = classify(p, ln)
        ok += (got == want)
        print("     PLANTED want=%-8s got=%-8s  %s" % (want, got, ln.strip()[:78]))
    print("CLASSIFIER_CONTROL=%d of %d" % (ok, len(planted)))
    neg = 'if [ -f "${STORED_INLINE_POLICIES}" ]; then'
    neg_ok = not BOUNDED.search(neg)
    print("     NEGATIVE (the substring trap): STORED_INLINE_POLICIES excluded by the word")
    print("     boundary = %s. SUBSTRING_TRAP_CONTROL=%s"
          % (neg_ok, "FIRED" if neg_ok else "NOT-FIRED"))
    print("")
    print("  DENOMINATOR RESTATED: %d repository file(s) swept (tracked %d + untracked %d, floor"
          % (len(corpus), len(tracked), len(untracked)))
    print("  %d excluded and named, gitignored %d excluded and counted); %d manifest tool(s) with"
          % (floor_n, len(ignored), len(tools)))
    print("  %d resolved; %d consumer(s) surviving every named subtraction, %d in-grant and %d"
          % (len(resolved), len(hits), len(inside), len(outside)))
    print("  out-of-grant; classifier %d of %d; tree=%s control=%s."
          % (ok, len(planted), "WORKTREE" if is_wt else "MAIN",
             "FIRED" if fired else "not-fired"))
    return 0 if (ok == len(planted) and neg_ok and (fired or not is_wt)) else 1


if __name__ == "__main__":
    sys.exit(main())
