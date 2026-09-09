#!/bin/bash
# E1-AC3 -- DO THE HELP TEXTS AND CODE SITES STILL NAME THE RETIRED LOCAL SURFACE?
#
# THE POPULATION IS CLOSED AND WRITTEN DOWN: exactly the eight SURFACED carriers TO-CG-E-1's
# E1-AC3 names. A corpus sweep answers a question about the corpus; this criterion asks a question
# about a NAMED SET, so the set is transcribed and any member that vanished is printed by name
# rather than dropped -- a file that disappeared and a file that passed are different findings.
#
# THE BAND IS THE WHOLE POINT, AND IT IS ENFORCED TWO DIFFERENT WAYS BECAUSE THE SET IS MIXED:
#   PYTHON carriers  -- ast.walk over ast.Constant STRING values only. Comments do not survive
#     parsing at all, and every DOCSTRING (module, class, function) is located by position and
#     excluded by construction, not by a hand-kept skip list that would drift. A comparison against
#     a string literal (`x == "kuzu_nessie_db"`) is an ast.Constant too, so comparisons are covered
#     by the same walk rather than by a second, differently-blind pass.
#   SHELL carriers   -- .tools/comp-describe and .tools/comp-cluster are bash, and an AST walk
#     cannot parse them. They are banded BY LINE: a line whose first non-blank character is `#` is
#     COMMENT and is excluded, on the SAME rule the Python limb applies to docstrings; every other
#     line is CODE and counted. The rule is printed above the count so a reader can see what the
#     denominator does and does not contain.
#
# THE EXCLUSION THE CRITERION MANDATES: a string inside a DECLARED RETIRED-ALIAS record is a
# RECORD, not an instruction, and is printed as RETIRED-RECORD and never counted. "Declared" means
# the enclosing dict key is a name in graph-call-manifest.yaml's own `retired_aliases:` closed set
# -- read from the manifest at run time, never a literal list in this script, so the exemption
# cannot outlive the declaration it depends on.
#
# THE TOKENS: `kuzu_nessie_db`, `ENGINE-INTERNALLY`, `--mode auto|inc|full` (and a bare `--mode`),
# `--db-path`. The first two name the retired local store and the engine-internal refresh it did;
# the last two are flags the thin client REFUSES (measured at this cut:
# `kuzu_cli.py: error: unrecognized arguments: --mode`).
#
# TWO CONTROLS, BOTH REQUIRED, BECAUSE A ZERO HAS TWO OPPOSITE CAUSES:
#   HELP_PROBE_CONTROL -- a PLANTED help string carrying the retired surface, held in a temp string
#     in this script and never in a tracked file, fed through the SAME detector in the SAME
#     process. It must be CAUGHT. Without it a detector that matched nothing prints a perfect zero.
#   HELP_BAND_CONTROL  -- the SAME tokens planted in a DOCSTRING, a COMMENT and a shell comment
#     line. They must NOT be caught. Without it "banding" is an unexercised claim, and a detector
#     that ignored real strings too would satisfy the first control and still read clean.
#
# A file that fails to parse is BLOCKED (exit 2), never counted clean: an unparseable file yields
# zero AST nodes, which is a perfect score for the wrong reason.
#
# Exit: 0 = no carrier names the retired surface outside a declared record, both controls behaved;
#       1 = a carrier does, or a control misbehaved; 2 = BLOCKED (a named file is unreadable /
#       unparseable, or the manifest's retired_aliases could not be read).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

python - <<'PY'
import ast
import os
import re
import sys

try:
    import yaml
except ImportError as exc:
    print("BLOCKED: PyYAML unavailable (%s) -- the retired-alias exemption is read from the"
          " manifest, not hardcoded here" % exc)
    sys.exit(2)

DECLARED = [
    ".tools/tool_index.py",
    "org/modules/graph/comp_aws_cli.py",
    "org/modules/graph/debtscan/comp_similar.py",
    ".tools/comp-which",
    ".tools/comp-describe",
    ".tools/comp-cluster",
    ".tools/comp-find",
    ".tools/gen_tool_classification.py",
]
SHELL = {".tools/comp-describe", ".tools/comp-cluster"}
TOKENS = re.compile(r"kuzu_nessie_db|ENGINE-INTERNALLY|--mode\s+(?:auto|inc|full)|--mode\b|--db-path\b")

try:
    with open("org/modules/graph/graph-call-manifest.yaml", encoding="utf-8") as fh:
        RETIRED_NAMES = set((yaml.safe_load(fh).get("retired_aliases") or {}).keys())
except (OSError, yaml.YAMLError) as exc:
    print("BLOCKED: the retired_aliases declaration could not be read (%s)" % exc)
    sys.exit(2)


def docstring_nodes(tree):
    """Every ast.Constant that IS a docstring, by position -- module, class, function, async."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", None) or []
            if body and isinstance(body[0], ast.Expr) \
                    and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                out.add(id(body[0].value))
    return out


def record_nodes(tree):
    """Every ast.Constant reachable from a dict VALUE whose KEY is a DECLARED retired name."""
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and isinstance(key.value, str) \
                    and key.value in RETIRED_NAMES:
                for sub in ast.walk(value):
                    if isinstance(sub, ast.Constant):
                        out.add(id(sub))
    return out


def scan_python(source, label):
    """[(lineno, band, text)] for CODE-band string constants naming a retired token.

    band is 'CODE' (counted) or 'RETIRED-RECORD' (printed, never counted). Raises SyntaxError to
    the caller -- a parse failure is a BLOCK, not a clean score.
    """
    tree = ast.parse(source, filename=label)
    skip = docstring_nodes(tree)
    records = record_nodes(tree)
    hits = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if id(node) in skip:
            continue
        if not TOKENS.search(node.value):
            continue
        band = "RETIRED-RECORD" if id(node) in records else "CODE"
        text = node.value.strip().replace("\n", " ")
        hits.append((node.lineno, band, text[:150]))
    return hits


def scan_shell(source, label):
    """[(lineno, band, text)] for a bash carrier. Band by line: leading `#` is COMMENT."""
    hits = []
    for i, raw in enumerate(source.splitlines(), start=1):
        if not TOKENS.search(raw):
            continue
        band = "COMMENT" if raw.lstrip().startswith("#") else "CODE"
        hits.append((i, band, raw.strip()[:150]))
    return hits


print("HELP_POPULATION_DECLARED=%d  (the SURFACED carriers TO-CG-E-1 E1-AC3 names)" % len(DECLARED))
print("HELP_TOKEN_SET=kuzu_nessie_db | ENGINE-INTERNALLY | --mode [auto|inc|full] | --db-path")
print("HELP_BAND_RULE=python -> ast.Constant STRING values only, module/class/function DOCSTRINGS"
      " excluded by position, comments never parsed; shell -> a leading `#` line is COMMENT and"
      " excluded, every other line is CODE")
print("HELP_RECORD_EXEMPTION=a string under a dict key naming one of the %d DECLARED retired"
      " aliases (%s) is printed RETIRED-RECORD and never counted"
      % (len(RETIRED_NAMES), ", ".join(sorted(RETIRED_NAMES))))

present, absent = [], []
for path in DECLARED:
    (present if os.path.isfile(path) else absent).append(path)
for path in absent:
    print("  ABSENT (excluded from the denominator): %s" % path)
print("HELP_POPULATION_ABSENT=%d" % len(absent))

dirty = {}
records_seen = 0
for path in present:
    try:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    except OSError as exc:
        print("BLOCKED: %s could not be read (%s)" % (path, exc))
        sys.exit(2)
    if path in SHELL:
        hits = scan_shell(source, path)
    else:
        try:
            hits = scan_python(source, path)
        except SyntaxError as exc:
            print("BLOCKED: %s failed to PARSE (%s) -- zero AST nodes is a clean score for the"
                  " wrong reason" % (path, exc))
            sys.exit(2)
    counted = [h for h in hits if h[1] == "CODE"]
    for lineno, band, text in hits:
        if band != "CODE":
            records_seen += 1
            print("  %-14s %s:%d  %s" % (band, path, lineno, text))
    if counted:
        dirty[path] = counted
        for lineno, band, text in counted[:12]:
            print("  NAMES RETIRED  %s:%d  %s" % (path, lineno, text))
        if len(counted) > 12:
            print("  NAMES RETIRED  %s: ... %d more counted hit(s) in this file"
                  % (path, len(counted) - 12))

print("HELP_EXCLUDED_AS_RECORD_OR_PROSE=%d" % records_seen)
print("HELP_COUNTED_HITS_TOTAL=%d" % sum(len(v) for v in dirty.values()))
print("HELP_ROUTES_BACK=%d of %d" % (len(dirty), len(present)))

# --- control 1: a planted help string MUST be caught -----------------------------------------------
PLANTED_PY = (
    "HELP = {\n"
    "    'comp-kuzu': {\n"
    "        'freshness': 'DEFAULT surface (no --db-path) = canonical Nessie kuzu_nessie_db;'\n"
    "                     ' auto-refreshes ENGINE-INTERNALLY on HEAD-advance',\n"
    "    },\n"
    "}\n"
    "def use():\n"
    "    return HELP['comp-kuzu']['freshness'] == 'kuzu_nessie_db'\n"
)
caught = [h for h in scan_python(PLANTED_PY, "<planted-help>") if h[1] == "CODE"]
if len(caught) < 2:
    print("HELP_PROBE_CONTROL=DEAD -- the planted help string yielded %r (want a help value AND a"
          " comparison literal); the zero above measures a broken detector" % (caught,))
    sys.exit(1)
print("HELP_PROBE_CONTROL=FIRED -- a PLANTED help string and a PLANTED comparison literal, held"
      " only in this script and fed through the SAME detector in-process, were caught: %d CODE-band"
      " hit(s) at line(s) %s" % (len(caught), ",".join(str(h[0]) for h in caught)))

# --- control 2: the same tokens in a docstring / comment MUST NOT be caught -------------------------
BANDED_PY = (
    '"""Historic: the default surface was kuzu_nessie_db and it auto-refreshed ENGINE-INTERNALLY."""\n'
    "# comp-kuzu --mode inc --db-path PATH   # retired, kept for the reader\n"
    "def f():\n"
    '    """This function once documented --mode full over kuzu_nessie_db."""\n'
    "    return 1\n"
)
BANDED_SH = (
    "#!/bin/bash\n"
    "#        comp-cluster --db-path PATH ... # query a frozen-vintage DB\n"
    "# comp-kuzu --mode inc refresh hint\n"
    "exit 0\n"
)
band_py = [h for h in scan_python(BANDED_PY, "<planted-prose>") if h[1] == "CODE"]
band_sh = [h for h in scan_shell(BANDED_SH, "<planted-prose-sh>") if h[1] == "CODE"]
if band_py or band_sh:
    print("HELP_BAND_CONTROL=DEAD -- prose-only tokens were counted (python %r, shell %r); the"
          " detector is a text match wearing an AST's clothes" % (band_py, band_sh))
    sys.exit(1)
print("HELP_BAND_CONTROL=FIRED -- the same tokens planted in a module docstring, a function"
      " docstring, a python comment and two shell comment lines scored 0 CODE-band hits in both"
      " limbs, so the banding is exercised and not merely asserted")

sys.exit(1 if dirty else 0)
PY
