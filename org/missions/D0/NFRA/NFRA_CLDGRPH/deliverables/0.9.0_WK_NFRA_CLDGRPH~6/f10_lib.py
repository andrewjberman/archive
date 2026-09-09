"""Shared measurement helpers for NFRA_CLDGRPH.TO-CG-F-10 (cell CG-s-30).

0.9.0_WK_NFRA_CLDGRPH~6. Every probe in this folder imports from here so the BEFORE census and
the AFTER acceptance runs measure with THE SAME instrument -- a before/after pair measured two
different ways is not a delta.

Nothing here writes to the shared plane. The three subcommands exercised are READ-ONLY
(classes, dual-managed, metrics --graph <fixture>); derive/snapshot/iceberg-commit are never run.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                    text=True, cwd=HERE).stdout.strip()

# ---- the four `when:` phrasings of comp-tools.yaml's comp-aws entry, verbatim at the cut ------
PHRASINGS = [
    "What AWS resources exist + how are they typed/connected?",
    "What's the drift / blast radius / unmanaged surface?",
    "Is any resource dual-managed across TF states?",
    "Cloud-shape snapshot + diff over time",
]
# the POSITIVE CONTROL: a phrasing that must still reach the served surface after the change.
CONTROL_PHRASING = "list all s3 buckets"
CONTROL_EXPECT = "comp-kuzu"

# ---- the read-only subcommands the preamble is exercised on ------------------------------------
FIXTURE = os.path.join(HERE, "f10_metrics_fixture.json")
SUBCOMMANDS = [
    ["classes"],
    ["dual-managed"],
    ["metrics", "--graph", FIXTURE],
]

BASELINE = os.path.join(HERE, "f10_baseline.json")

# ---- THE DECLARED PHRASE DOMAIN (TO-CG-F-10, "a laptop as a producer") -------------------------
# Declared by the issuer at the cut; each entry is (label, compiled regex). MECE over ONE axis:
# "agent-facing text that describes THIS LAPTOP running a write/producer path".
PHRASE_DOMAIN = [
    ("-> .comp-graph",                                r"->\s*\.comp-graph"),
    ("snapshot tarballs -> opal-...-globgrph",        r"snapshot tarballs\s*->\s*opal-\d+-globgrph"),
    ("--commit-to-nessie",                            r"--commit-to-nessie"),
    ("iceberg-commit",                                r"iceberg-commit"),
    ("writes the derive",                             r"writes the derive"),
    ("run comp-aws derive",                           r"run comp-aws derive"),
    ("full derive",                                   r"full derive"),
]
REGISTRY_FILES = [
    os.path.join(WS, "org", "modules", "graph", "comp-tools.yaml"),
    os.path.join(WS, "org", "modules", "graph", "comp-aws-agent-usage.yaml"),
]
# the agent-facing FIELD set censused (the scoped read); an UNSCOPED whole-file read runs beside it.
AGENT_FACING_FIELDS = ("command", "when", "cmd", "does", "use_when", "when_to_use",
                       "output", "cost", "usage_guide", "overlay_role", "key_facts",
                       "related_tools", "note", "name_note", "guardrails", "segment_scope",
                       "engine", "project", "source", "data_sources", "replaces", "freshness")


def sha256_of(b):
    return hashlib.sha256(b).hexdigest()


def git_bash():
    """ABSOLUTE Git-for-Windows bash.exe. NEVER bare 'bash': a python-spawned bare `bash` Windows-
    resolves to the System32 WSL stub, which returns rc=1 and 504 bytes of UTF-16LE on stdout --
    a false baseline that reads as three identical subcommand hashes. Measured here on the first
    before-census run; .tools/git_bash_resolver.py is the estate's resolver and is used first."""
    sys.path.insert(0, os.path.join(WS, ".tools"))
    try:
        from git_bash_resolver import git_bash as _gb
        b = _gb()
        if b:
            return b
    except Exception:
        pass
    for c in (r"C:\Program Files\Git\usr\bin\bash.exe",
              r"C:\Program Files (x86)\Git\usr\bin\bash.exe"):
        if os.path.exists(c):
            return c
    raise RuntimeError("Git Bash not resolved -- refusing to fall back to bare 'bash' (WSL stub)")


def run_wrapper(argv, env=None):
    """Run .tools/comp-aws through the WRAPPER (the entry an agent types). Returns
    (rc, stdout_bytes, stderr_text). Bounded."""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([git_bash(), os.path.join(WS, ".tools", "comp-aws")] + argv,
                       capture_output=True, cwd=WS, env=e, timeout=110)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


def run_cli(argv, env=None):
    """Run the CLI DIRECTLY (no wrapper) -- used to prove the one-print-per-invocation contract."""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable,
                        os.path.join(WS, "org", "modules", "graph", "comp_aws_cli.py")] + argv,
                       capture_output=True, cwd=WS, env=e, timeout=110)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


_RANK_RE = re.compile(r"ranked \+ described:\s+(\S+rank-\d+\.yaml)")


def comp_which(question):
    """Run comp-which and return (rc, stdout, rank_file_abs_path or None).
    The RANK FILE is the measurement surface -- never page 1 of stdout."""
    p = subprocess.run([sys.executable, os.path.join(WS, ".tools", "comp-which"), question],
                       capture_output=True, text=True, cwd=WS, timeout=110)
    m = _RANK_RE.search(p.stdout or "")
    path = os.path.join(WS, m.group(1).replace("/", os.sep)) if m else None
    return p.returncode, (p.stdout or ""), path


_TOOL_ROW = re.compile(r"^\s*-?\s*(?:rank:.*\n\s*)?tool:\s*(.+?)\s*$", re.M)


def rank_rows(path):
    """Every `tool:` row in a spilled ranking, in rank order. A row is a TOOL ID."""
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("tool:"):
            v = s[len("tool:"):].strip().strip("'\"")
            out.append(v)
    return out


def curated_tuple_census():
    """Count the CURATED VOCABULARY tuples in .tools/comp-which and how many name comp-aws in
    their CALL list, plus description strings that name it. The router ranks off this vocabulary
    (comp-which:293), so this is the population that matters -- denominator PRINTED."""
    path = os.path.join(WS, ".tools", "comp-which")
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    # a curated tuple opens with `    ([` at module level in the vocabulary block.
    total = 0
    naming = []
    in_tuple = False
    buf = []
    start = 0
    depth = 0
    for i, ln in enumerate(lines, 1):
        stripped = ln.rstrip("\n")
        code = stripped.split("#", 1)[0] if stripped.lstrip().startswith("#") else stripped
        if not in_tuple:
            if re.match(r"^\s{0,8}\(\[", stripped):
                in_tuple = True
                buf = [stripped]
                start = i
                depth = code.count("(") - code.count(")")
                if depth <= 0:
                    total += 1
                    in_tuple = False
                    if re.search(r'"comp-aws\b', "".join(buf)):
                        naming.append(start)
                continue
        else:
            buf.append(stripped)
            depth += code.count("(") - code.count(")")
            if depth <= 0:
                total += 1
                in_tuple = False
                if re.search(r'"comp-aws\b', "".join(buf)):
                    naming.append(start)
    # description strings OUTSIDE a tuple that name comp-aws (CODE band, not comments)
    desc = []
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("#"):
            continue
        if "comp-aws" in s:
            desc.append(i)
    return {"tuples_total": total, "tuples_naming_comp_aws": naming,
            "code_lines_naming_comp_aws": desc}


def phrase_census():
    """The declared domain over the two registry files: SCOPED (agent-facing fields) and the
    UNSCOPED whole-file read beside it (CLAUDE.md Rule 22: one unscoped read after a scoped pass)."""
    import yaml
    scoped = {label: 0 for label, _ in PHRASE_DOMAIN}
    unscoped = {label: 0 for label, _ in PHRASE_DOMAIN}
    detail = []
    loads = 0
    for path in REGISTRY_FILES:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        try:
            doc = yaml.safe_load(raw)
            loads += 1
        except Exception as exc:                                  # pragma: no cover
            detail.append("YAML-LOAD-FAILED %s: %s" % (path, exc))
            doc = None
        for label, rx in PHRASE_DOMAIN:
            n = len(re.findall(rx, raw))
            unscoped[label] += n
            if n:
                detail.append("UNSCOPED %s :: %s x%d" % (os.path.basename(path), label, n))
        if doc is not None:
            for field, value in _agent_facing_strings(doc):
                for label, rx in PHRASE_DOMAIN:
                    n = len(re.findall(rx, value))
                    scoped[label] += n
                    if n:
                        detail.append("SCOPED %s :: field %s :: %s x%d"
                                      % (os.path.basename(path), field, label, n))
    return {"scoped": scoped, "unscoped": unscoped, "detail": detail, "yaml_loads": loads}


def _agent_facing_strings(node, field=None, out=None):
    """Every scalar reachable under an AGENT-FACING key, at any depth."""
    if out is None:
        out = []
    if isinstance(node, dict):
        for k, v in node.items():
            key = str(k)
            _agent_facing_strings(v, key if key in AGENT_FACING_FIELDS else field, out)
    elif isinstance(node, list):
        for v in node:
            _agent_facing_strings(v, field, out)
    else:
        if field and node is not None:
            out.append((field, str(node)))
    return out


def comp_aws_keys_in_comp_tools():
    """DUPLICATE-KEY history at comp-tools.yaml:691-698 -- count `comp-aws:` keys at HEAD."""
    path = REGISTRY_FILES[0]
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    return sum(1 for ln in lines
               if re.match(r"^\s{0,4}comp-aws:\s*$", ln) and not ln.lstrip().startswith("#"))


def jdump(obj):
    return json.dumps(obj, indent=2, sort_keys=True, default=str)
