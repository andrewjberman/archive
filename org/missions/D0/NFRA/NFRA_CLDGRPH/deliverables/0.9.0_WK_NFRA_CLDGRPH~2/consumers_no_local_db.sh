#!/bin/bash
# D7-AC2, AS AMENDED @e27c871ccf -- DOES ANY ENUMERATED CONSUMER OPEN A LOCAL DATABASE IN CODE?
#
# THE POPULATION IS CLOSED AND WRITTEN DOWN, not swept. It is exactly the file list this task
# order names in <paths> (TO-CG-D-7 @565008157e, lines 218-253), because a corpus sweep answers a
# question about the CORPUS while this criterion asks a question about a NAMED SET. The two files
# the order names that no longer exist were DELETED with the seam they pinned in pass 2; they are
# printed by name and excluded from the denominator rather than dropped in silence, because a file
# that vanished and a file that passed are different findings.
#
# THE BAND IS THE WHOLE POINT. This criterion exists because its predecessor counted TEXT: the
# tombstone `_canonical.py` must NAME `CANONICAL_DB_PATH` in its docstring to say what it retired,
# `comp_aws_cli.py:2857` must name it in a comment to explain the old default, and the CG-8
# battery must hold `"kuzu.Database("` in string literals to assert those tokens are forbidden.
# None of those is a call. So the detector is an AST walk, not a regex: only an `ast.Call` whose
# callee is the ATTRIBUTE `kuzu.Database`, and only an `ast.Name`/`ast.Attribute` spelling
# `CANONICAL_DB_PATH`, count. Comments do not survive parsing at all and string constants are
# never inspected, so docstrings, forbidden-token tuples and planted mutant fixtures are excluded
# BY CONSTRUCTION rather than by a hand-kept skip list that would drift.
#
# TWO CONTROLS, BOTH REQUIRED, BECAUSE A ZERO HAS THREE CAUSES.
#   CONSUMER_PROBE_CONTROL -- a PLANTED opener, held in a temp string in this file and never in a
#     tracked one, carrying both signatures. It runs through the SAME detector in the SAME process
#     and must be CAUGHT. Without it, a detector that matched nothing (a typo'd node test, a walk
#     that never recursed) would print a perfect zero over 30 real files.
#   CONSUMER_PROBE_BAND_CONTROL -- the SAME two tokens planted in a docstring and a comment ONLY.
#     It must NOT be caught. Without it, "banding" is an unexercised claim: a detector that also
#     ignored real calls would satisfy the first control's opposite and still read clean.
# A file that fails to PARSE is BLOCKED (exit 2), never counted as clean -- an unparseable file
# yields zero AST nodes, which is a perfect score for the wrong reason.
#
# Exit: 0 = no consumer opens in CODE and both controls behaved; 1 = an opener was found, or a
# control misbehaved; 2 = BLOCKED (a named file could not be parsed).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

python - <<'PY'
import ast
import os
import sys

# --- the closed population, transcribed from TO-CG-D-7 <paths> ---------------------------------
DECLARED = [
    "infra/aws/globgrph/_canonical.py",
    "infra/aws/globgrph/projection_client.py",
    "infra/aws/globgrph/comp_detect.py",
    "infra/aws/globgrph/comp_cluster_cli.py",
    "infra/aws/globgrph/comp_debt.py",
    "infra/aws/globgrph/debtscan_canon_scorer.py",
    "infra/aws/globgrph/canon_motif_scorer.py",
    "infra/aws/globgrph/kuzu_cost_enrich.py",
    "infra/aws/globgrph/kuzu_ac_traversals.py",
    "infra/aws/globgrph/cse_emit_graphhead.py",
    "infra/aws/globgrph/c2c3_liveness_acceptance.py",
    "org/modules/graph/cli.py",
    "org/modules/graph/comp_blast_universe.py",
    "org/modules/graph/comp_trigger.py",
    "org/modules/graph/comp_system.py",
    "org/modules/graph/comp_marker_read.py",
    "org/modules/graph/comp_iam_live.py",
    "org/modules/graph/iam_cli.py",
    "org/modules/graph/cse_schema.py",
    "org/modules/graph/c2_canonical_compose.py",
    "org/modules/graph/comp_aws_cli.py",
    ".tools/comp-find",
    ".tools/tool_index.py",
    ".tools/safe_deploy_core.py",
    ".tools/tests/test_comp_find_battery.py",
    ".tools/tests/test_g2_disclosure_battery.py",
    ".tools/tests/test_comp_similar_battery.py",
    ".tools/tests/test_cg8_seam_retired_battery.py",   # the <paths> glob .tools/tests/test_cg8_*.py
    "org/modules/heatmap/ms_heat_index.py",
    "infra/aws/globgrph/tests/test_canonical_rebuild_liveness.py",
    "infra/aws/globgrph/tests/test_canonical_refresh_failure_signal.py",
    "infra/aws/globgrph/tests/test_comp_cluster_cli.py",
]
LOCAL_DB_NAME = "CANONICAL_DB_PATH"


def openers(source, label):
    """Every CODE-band local-DB open in `source`. Returns [(lineno, kind, text)].

    kind is 'kuzu.Database(' for a call on the kuzu attribute, or 'CANONICAL_DB_PATH' for a
    name/attribute reference. Raises SyntaxError up to the caller -- a parse failure is a BLOCK.
    """
    tree = ast.parse(source, filename=label)
    lines = source.splitlines()
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr == "Database" \
                    and isinstance(fn.value, ast.Name) and fn.value.id == "kuzu":
                found.append((node.lineno, "kuzu.Database("))
        elif isinstance(node, ast.Name) and node.id == LOCAL_DB_NAME:
            found.append((node.lineno, LOCAL_DB_NAME))
        elif isinstance(node, ast.Attribute) and node.attr == LOCAL_DB_NAME:
            found.append((node.lineno, LOCAL_DB_NAME))
    out = []
    for lineno, kind in sorted(set(found)):
        text = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
        out.append((lineno, kind, text))
    return out


# --- the population walk ------------------------------------------------------------------------
present, absent = [], []
for path in DECLARED:
    (present if os.path.isfile(path) else absent).append(path)

print("CONSUMER_POPULATION_DECLARED=%d  (the file list in TO-CG-D-7 <paths>)" % len(DECLARED))
for path in absent:
    print("  ABSENT (excluded from the denominator): %s" % path)
print("CONSUMER_POPULATION_ABSENT=%d" % len(absent))
print("CONSUMER_BAND_RULE=ast.Call on kuzu.Database / ast.Name|Attribute %s; comments and string"
      " constants (docstrings, forbidden-token tuples, mutant fixtures) never inspected"
      % LOCAL_DB_NAME)

hits_by_file = {}
for path in present:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
    except OSError as exc:
        print("BLOCKED: %s could not be read (%s)" % (path, exc))
        sys.exit(2)
    try:
        hits = openers(source, path)
    except SyntaxError as exc:
        print("BLOCKED: %s failed to PARSE (%s) -- an unparseable file yields zero AST nodes,"
              " which is a clean score for the wrong reason" % (path, exc))
        sys.exit(2)
    if hits:
        hits_by_file[path] = hits

for path in present:
    if path in hits_by_file:
        for lineno, kind, text in hits_by_file[path]:
            print("  OPENS  %s:%d  [%s]  %s" % (path, lineno, kind, text))

print("CONSUMERS_OPENING_LOCAL_DB=%d of %d" % (len(hits_by_file), len(present)))

# --- control 1: a planted opener MUST be caught --------------------------------------------------
PLANTED = (
    "import kuzu\n"
    "CANONICAL_DB_PATH = 'kuzu_nessie_db'\n"
    "def load():\n"
    "    db = kuzu.Database(CANONICAL_DB_PATH)\n"
    "    return kuzu.Connection(db)\n"
)
caught = openers(PLANTED, "<planted-opener>")
kinds = sorted({k for _, k, _ in caught})
if len(caught) < 2 or "kuzu.Database(" not in kinds or LOCAL_DB_NAME not in kinds:
    print("CONSUMER_PROBE_CONTROL=DEAD -- the planted opener yielded %r; the zero above measures a"
          " broken detector, not a clean population" % (caught,))
    sys.exit(1)
print("CONSUMER_PROBE_CONTROL=FIRED -- planted opener caught %d of 2 signature(s) %s at line(s) %s"
      " through the SAME detector, in-process, on a temp string (never a tracked file)"
      % (len(kinds), ",".join(kinds), ",".join(str(n) for n, _, _ in caught)))

# --- control 2: the SAME tokens in a docstring and a comment MUST NOT be caught -------------------
BANDED = (
    '"""Historic note: this module used kuzu.Database(CANONICAL_DB_PATH) before R7."""\n'
    "# db = kuzu.Database(CANONICAL_DB_PATH)  # retired, kept for the reader\n"
    "FORBIDDEN = ('kuzu.Database(', 'CANONICAL_DB_PATH')\n"
)
band_caught = openers(BANDED, "<planted-prose>")
if band_caught:
    print("CONSUMER_PROBE_BAND_CONTROL=DEAD -- prose-only tokens were counted as opens %r; the"
          " detector is a text match wearing an AST's clothes" % (band_caught,))
    sys.exit(1)
print("CONSUMER_PROBE_BAND_CONTROL=FIRED -- the same two tokens planted in a docstring, a comment"
      " and a string tuple scored 0, so the banding is exercised and not merely asserted")

sys.exit(1 if hits_by_file else 0)
PY
