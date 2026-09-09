#!/bin/bash
# D7-AC2, AS AMENDED @e27c871ccf AND NARROWED FOR PASS 4 -- DOES ANY ENUMERATED CONSUMER OPEN THE
# RETIRED CANONICAL LOCAL DATABASE IN CODE?
#
# THE POPULATION IS CLOSED AND WRITTEN DOWN, not swept. It is exactly the file list this task
# order names in <paths>, because a corpus sweep answers a question about the CORPUS while this
# criterion asks a question about a NAMED SET. Files the order names that no longer exist are
# printed by name and excluded from the denominator rather than dropped in silence, because a file
# that vanished and a file that passed are different findings. THREE are absent at pass 4: the two
# seam tests deleted with the seam in pass 2, and kuzu_cost_enrich.py, deleted in pass 4 on the
# CTO's ruling 94466 @1266d65641 (a WRITER against the retired store, with no repoint target).
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
# THE PASS-4 NARROWING, AND ITS RULE. CG-s-8 retires FOUR surfaces and every one of them is
# `kuzu_nessie_db` or its seam. A `kuzu.Database(` call on a DIFFERENT local store is therefore
# outside this cell -- the same split 1.0.0_SA_CTO ruled at 94456 for the scratch loaders: in
# FWD-7's TERRITORY, not in CG-s-8's PATHS. So each opener is RESOLVED to the store it names and
# only CANONICAL openers are counted. An out-of-cell opener is PRINTED as DECLARED-OUT-OF-CELL
# with the store it opens, never silently dropped. The one live instance is `comp_debt.py:215`
# (`kuzu_stitch_db`, the second reachability surface), which the issuer PLACED as a manifest row.
#
# RESOLUTION IS FAIL-CLOSED, WHICH IS THE ONLY WAY A NARROWING IS HONEST. The resolver walks the
# opener's first argument through that file's own bindings (module and function assignments, `for`
# targets over literal tuples, argparse defaults, `os.path.join` segments) and collects every
# reachable STRING LITERAL. If any names the canonical store -> CANONICAL, counted. If none does
# but some other store-shaped literal is reachable -> DECLARED-OUT-OF-CELL, named. IF NO STORE
# LITERAL IS REACHABLE AT ALL -> COUNTED AS CANONICAL, because an opener whose target cannot be
# read is exactly the case a narrowing must not be allowed to swallow.
#
# THREE CONTROLS, ALL REQUIRED, BECAUSE A ZERO HAS FOUR CAUSES.
#   CONSUMER_PROBE_CONTROL -- a PLANTED opener, held in a temp string in this file and never in a
#     tracked one, carrying both signatures. It runs through the SAME detector in the SAME process
#     and must be CAUGHT. Without it, a detector that matched nothing (a typo'd node test, a walk
#     that never recursed) would print a perfect zero over 29 real files.
#   CONSUMER_PROBE_BAND_CONTROL -- the SAME two tokens planted in a docstring and a comment ONLY.
#     It must NOT be caught. Without it, "banding" is an unexercised claim: a detector that also
#     ignored real calls would satisfy the first control's opposite and still read clean.
#   CONSUMER_NARROWING_CONTROL -- the NARROWING itself, exercised in BOTH directions: a planted
#     stitch-store opener must classify OUT-OF-CELL, and a planted opener whose argument cannot be
#     resolved must still COUNT. Without it the fail-closed rule is a promise, and a scope filter
#     that quietly matched everything would read as a clean population.
# A file that fails to PARSE is BLOCKED (exit 2), never counted as clean -- an unparseable file
# yields zero AST nodes, which is a perfect score for the wrong reason.
#
# Exit: 0 = no consumer opens the canonical store in CODE and all controls behaved; 1 = an opener
# was found, or a control misbehaved; 2 = BLOCKED (a named file could not be parsed).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

python - <<'PY'
import ast
import os
import re
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
CANONICAL_STORE = "kuzu_nessie_db"
STORE_SHAPE = re.compile("^kuzu[a-z0-9_]*db$")
MAX_DEPTH = 6


class Bindings:
    """Every name -> expression binding this MODULE offers, read once per file.

    Deliberately flat and over-inclusive: a name assigned in two places contributes BOTH
    expressions, so the resolver sees every store an opener could be reached with. A union that is
    too wide can only ever COUNT an opener a narrower read would have excused; it can never excuse
    one -- which is the direction a narrowing is allowed to err in.
    """

    def __init__(self, tree):
        self.names = {}
        self.argparse_defaults = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    self._bind(tgt, node.value)
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                self._bind(node.target, node.value)
            elif isinstance(node, ast.For):
                self._bind_for(node)
            elif isinstance(node, ast.Call):
                self._bind_argparse(node)

    def _bind(self, target, value):
        if isinstance(target, ast.Name):
            self.names.setdefault(target.id, []).append(value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for i, elt in enumerate(target.elts):
                if isinstance(value, (ast.Tuple, ast.List)) and i < len(value.elts):
                    self._bind(elt, value.elts[i])
                else:
                    self._bind(elt, value)

    def _bind_for(self, node):
        """`for a, b in ((X, Y), (Z, W)):` binds a -> X,Z and b -> Y,W."""
        it = node.iter
        elements = it.elts if isinstance(it, (ast.Tuple, ast.List)) else [it]
        for element in elements:
            self._bind(node.target, element)

    def _bind_argparse(self, node):
        fn = node.func
        if not (isinstance(fn, ast.Attribute) and fn.attr == "add_argument"):
            return
        flag = None
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                flag = arg.value.lstrip("-").replace("-", "_")
        for kw in node.keywords:
            if kw.arg == "dest" and isinstance(kw.value, ast.Constant):
                flag = str(kw.value.value)
        for kw in node.keywords:
            if kw.arg == "default" and flag:
                self.argparse_defaults.setdefault(flag, []).append(kw.value)


def literals(expr, binds, depth=0, seen=None):
    """Every string literal reachable from `expr` through this file's own bindings."""
    if expr is None or depth > MAX_DEPTH:
        return set()
    seen = seen if seen is not None else set()
    out = set()
    if isinstance(expr, ast.Constant):
        if isinstance(expr.value, str):
            out.add(expr.value)
    elif isinstance(expr, ast.JoinedStr):
        for part in expr.values:
            out |= literals(part, binds, depth + 1, seen)
    elif isinstance(expr, ast.FormattedValue):
        out |= literals(expr.value, binds, depth + 1, seen)
    elif isinstance(expr, ast.Name):
        if expr.id == LOCAL_DB_NAME:
            out.add(CANONICAL_STORE)          # the retired constant IS the canonical store
        key = ("n", expr.id)
        if key not in seen:
            seen.add(key)
            for value in binds.names.get(expr.id, []):
                out |= literals(value, binds, depth + 1, seen)
    elif isinstance(expr, ast.Attribute):
        if expr.attr == LOCAL_DB_NAME:
            out.add(CANONICAL_STORE)
        key = ("a", expr.attr)
        if key not in seen:
            seen.add(key)
            for value in binds.argparse_defaults.get(expr.attr, []):
                out |= literals(value, binds, depth + 1, seen)
    elif isinstance(expr, ast.Call):
        for arg in expr.args:
            out |= literals(arg, binds, depth + 1, seen)
        for kw in expr.keywords:
            out |= literals(kw.value, binds, depth + 1, seen)
    elif isinstance(expr, (ast.Tuple, ast.List, ast.Set)):
        for elt in expr.elts:
            out |= literals(elt, binds, depth + 1, seen)
    elif isinstance(expr, ast.BinOp):
        out |= literals(expr.left, binds, depth + 1, seen)
        out |= literals(expr.right, binds, depth + 1, seen)
    elif isinstance(expr, ast.Subscript):
        out |= literals(expr.value, binds, depth + 1, seen)
    return out


def classify(expr, binds):
    """(scope, stores): CANONICAL / OUT-OF-CELL / UNRESOLVED-COUNTED. Fail-closed."""
    found = literals(expr, binds)
    stores = set()
    for lit in found:
        norm = lit.replace(chr(92), "/").rstrip("/")
        for token in (lit, os.path.basename(norm)):
            if CANONICAL_STORE in token:
                stores.add(CANONICAL_STORE)
            elif STORE_SHAPE.match(token):
                stores.add(token)
    if CANONICAL_STORE in stores:
        return ("CANONICAL", sorted(stores))
    if stores:
        return ("OUT-OF-CELL", sorted(stores))
    return ("UNRESOLVED-COUNTED", [])


def openers(source, label):
    """Every CODE-band local-DB open in `source`. Returns [(lineno, kind, text, scope, stores)].

    kind is 'kuzu.Database(' for a call on the kuzu attribute, or 'CANONICAL_DB_PATH' for a
    name/attribute reference. Raises SyntaxError up to the caller -- a parse failure is a BLOCK.
    """
    tree = ast.parse(source, filename=label)
    binds = Bindings(tree)
    lines = source.splitlines()
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr == "Database" \
                    and isinstance(fn.value, ast.Name) and fn.value.id == "kuzu":
                arg = node.args[0] if node.args else None
                found[(node.lineno, "kuzu.Database(")] = classify(arg, binds)
        elif isinstance(node, ast.Name) and node.id == LOCAL_DB_NAME:
            found[(node.lineno, LOCAL_DB_NAME)] = ("CANONICAL", [CANONICAL_STORE])
        elif isinstance(node, ast.Attribute) and node.attr == LOCAL_DB_NAME:
            found[(node.lineno, LOCAL_DB_NAME)] = ("CANONICAL", [CANONICAL_STORE])
    out = []
    for (lineno, kind) in sorted(found):
        scope, stores = found[(lineno, kind)]
        text = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
        out.append((lineno, kind, text, scope, list(stores)))
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
print("CONSUMER_PREDICATE_SCOPE=the CANONICAL store '%s' only (CG-s-8 retires that store and its"
      " seam; an opener on another local store is FWD-7 territory, not this cell -- the same split"
      " 1.0.0_SA_CTO ruled at 94456). Each opener is resolved to the store it names through its"
      " own file's bindings; an opener whose target cannot be resolved is COUNTED, never excused."
      % CANONICAL_STORE)

hits_by_file = {}
out_of_cell = []
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
    counted = [h for h in hits if h[3] != "OUT-OF-CELL"]
    for h in hits:
        if h[3] == "OUT-OF-CELL":
            out_of_cell.append((path, h))
    if counted:
        hits_by_file[path] = counted

for path, hit in out_of_cell:
    lineno, kind, text, scope, stores = hit
    print("  DECLARED-OUT-OF-CELL  %s:%d  [%s]  store=%s  %s"
          % (path, lineno, kind, ",".join(stores) or "unknown", text))
print("CONSUMERS_OPENING_OUT_OF_CELL_STORE=%d (printed above, excluded from the count by the"
      " narrowing, NOT dropped)" % len(out_of_cell))

for path in present:
    if path in hits_by_file:
        for lineno, kind, text, scope, stores in hits_by_file[path]:
            print("  OPENS  %s:%d  [%s]  scope=%s  store=%s  %s"
                  % (path, lineno, kind, scope, ",".join(stores) or "unresolved", text))

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
kinds = sorted({k for _, k, _, _, _ in caught})
scopes = sorted({s for _, _, _, s, _ in caught})
if len(caught) < 2 or "kuzu.Database(" not in kinds or LOCAL_DB_NAME not in kinds \
        or scopes != ["CANONICAL"]:
    print("CONSUMER_PROBE_CONTROL=DEAD -- the planted opener yielded %r; the zero above measures a"
          " broken detector, not a clean population" % (caught,))
    sys.exit(1)
print("CONSUMER_PROBE_CONTROL=FIRED -- planted opener caught %d of 2 signature(s) %s at line(s) %s"
      " through the SAME detector, in-process, on a temp string (never a tracked file), both"
      " classified %s"
      % (len(kinds), ",".join(kinds), ",".join(str(n) for n, _, _, _, _ in caught),
         ",".join(scopes)))

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

# --- control 3: the NARROWING, exercised in BOTH directions ---------------------------------------
NARROW_OUT = (
    "import os\n"
    "import kuzu\n"
    "HERE = os.path.dirname(os.path.abspath(__file__))\n"
    "STITCH = os.path.join(HERE, 'kuzu_stitch_db')\n"
    "def sweep():\n"
    "    for path, scope in ((None, 'a'), (STITCH, 'b')):\n"
    "        if path is not None:\n"
    "            return kuzu.Connection(kuzu.Database(path, read_only=True))\n"
    "    return None\n"
)
NARROW_UNRESOLVED = (
    "import kuzu\n"
    "def openit(p):\n"
    "    return kuzu.Database(p)\n"
)
out_hits = openers(NARROW_OUT, "<planted-out-of-cell>")
unres_hits = openers(NARROW_UNRESOLVED, "<planted-unresolved>")
out_ok = (len(out_hits) == 1 and out_hits[0][3] == "OUT-OF-CELL"
          and out_hits[0][4] == ["kuzu_stitch_db"])
unres_ok = len(unres_hits) == 1 and unres_hits[0][3] == "UNRESOLVED-COUNTED"
if not (out_ok and unres_ok):
    print("CONSUMER_NARROWING_CONTROL=DEAD -- out-of-cell planted %r (want exactly 1 OUT-OF-CELL on"
          " kuzu_stitch_db), unresolved planted %r (want exactly 1 UNRESOLVED-COUNTED); a scope"
          " filter that matches everything reads as a clean population" % (out_hits, unres_hits))
    sys.exit(1)
print("CONSUMER_NARROWING_CONTROL=FIRED -- a planted stitch-store opener resolved through a `for`"
      " target over a literal tuple classified OUT-OF-CELL (store=%s, line %d) and a planted opener"
      " on an unresolvable parameter classified %s (line %d), so the narrowing is exercised in BOTH"
      " directions and the fail-closed limb is not a promise"
      % (",".join(out_hits[0][4]), out_hits[0][0], unres_hits[0][3], unres_hits[0][0]))

sys.exit(1 if hits_by_file else 0)
PY
