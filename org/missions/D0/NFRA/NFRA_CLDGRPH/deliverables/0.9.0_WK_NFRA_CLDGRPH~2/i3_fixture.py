#!/usr/bin/env python3
"""i3_fixture -- shared harness for TO-CG-I-3 (CG-s-42).

GRAIN. This harness does NOT transcribe the producer's drop. It loads
`infra/aws/globgrph/derive_stitch.py` AS A MODULE and calls the producer's OWN
`drop_prior_cycle_edges` / `SOLE_WRITTEN_EDGE_TYPES`, so the behaviour graded is the
behaviour that ships. A harness transcribed from the implementation scores its blind
spot as a pass; loading the real module is what avoids that.

ENVIRONMENT. Local worktree only. `load_producer` execs the module source, which imports
boto3 but calls NOTHING: `load_aws_layer` is the only S3 reader in the file and no arm
here invokes it. No AWS call, no publish, no task run.

TREE. Every consumer prints the worktree, branch and HEAD it ran in, and the BASELINE arm
resolves the pre-remedy bytes BY CONTENT (a marker string absent from the baseline and
present in the worktree) with a positive control on the retrieval -- never by asking
whether a commit is an ancestor. A hash test answers "did this commit land", not "is the
fix present".
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE
while WS.name and not (WS / ".git").exists():
    WS = WS.parent

PRODUCER_REL = "infra/aws/globgrph/derive_stitch.py"
PRODUCER_ABS = WS / "infra" / "aws" / "globgrph" / "derive_stitch.py"
GLOBGRPH_DIR = str(PRODUCER_ABS.parent)

# The commit this worker started from: the producer BEFORE this order touched it.
BASELINE_PIN = "4ff4abd9a4d6d2f60fd74fef32ce64158c6bd34b"
# The marker CG-s-42 writes into the producer. Absent in the baseline BY CONSTRUCTION.
REMEDY_MARKER = "SOLE_WRITTEN_EDGE_TYPES"

EXTS = (".py", ".json", ".jsonl", ".yaml", ".yml", ".patch")
SIZE_CAP = 4_000_000

# Files that MENTION an edge type in an emission shape but are not estate producers.
# Each is excluded BY NAME so the exclusion can be argued with (rule 24: write the
# enumeration as the denominator MINUS what you exclude, never as a forward list).
NON_PRODUCER_PREFIXES = (
    "org/missions/",                    # mission harnesses, fixtures and captures
    "org/tier1_exec/",                  # seat deliverables
    "org/tier2_senior/",                # seat deliverables
    "org/modules/graph/tsgraph_spike/",  # a P0 spike; its out/ payload is never served
    "infra/aws/globgrph/tests/",        # tests
    ".tools/tool_index.py",             # an index that DESCRIBES edge types
    "org/modules/graph/cse_schema.py",  # the vocabulary map (reader)
    "org/modules/graph/comp_coverage_check.py",   # the roll-up resolver (reader)
)


def git(*args: str) -> str:
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"          # git show <ref>:<slashed path>
    p = subprocess.run(["git", "-C", str(WS), *args], capture_output=True, env=env)
    if p.returncode != 0:
        raise RuntimeError("ERROR: git %s rc=%d %s"
                           % (args, p.returncode, p.stderr.decode("utf-8", "replace")[:400]))
    return p.stdout.decode("utf-8", "replace")


def tree_facts() -> dict:
    return {
        "worktree": str(WS).replace("\\", "/"),
        "tree_kind": "WORKTREE" if (WS / ".git").is_file() else "MAIN",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        "head": git("rev-parse", "HEAD").strip(),
        "baseline_pin": BASELINE_PIN,
    }


def baseline_source() -> str:
    src = git("show", "%s:%s" % (BASELINE_PIN, PRODUCER_REL))
    # POSITIVE CONTROL on the retrieval: a mangled/empty git show returns clean-empty.
    if len(src) < 10000 or "def build_stitched_graph" not in src:
        raise RuntimeError("ERROR: baseline source retrieval failed (len=%d)" % len(src))
    return src


def current_source() -> str:
    return PRODUCER_ABS.read_text(encoding="utf-8")


def load_producer(src: str, name: str):
    """Exec the producer source as a module. __file__ points at the REAL path so the
    producer's own `_WS = parents[3]` resolves to the workspace root."""
    if GLOBGRPH_DIR not in sys.path:
        sys.path.insert(0, GLOBGRPH_DIR)
    if str(WS) not in sys.path:
        sys.path.insert(0, str(WS))
    mod = types.ModuleType(name)
    mod.__file__ = str(PRODUCER_ABS)
    mod.__name__ = name
    sys.modules[name] = mod
    exec(compile(src, str(PRODUCER_ABS), "exec"), mod.__dict__)
    return mod


# --------------------------------------------------------------- the sole-writership check
def emitters(term: str) -> dict:
    """Every ESTATE file that constructs or declares an edge of `term`, with its counts.

    THE FALSIFIER FOR A REGISTRY MEMBER. It is a repository sweep, so it is bounded by
    what the repository holds (bound (2) of i3_writers.py) -- and it is RE-RUNNABLE, which
    is the whole point: sole-writership is a fact about today, not a property of the type.

    Returns {relpath: {"payload": n, "code": n}} for PRODUCER files only; the excluded
    non-producer members are returned separately by `emitters_full`.
    """
    prod, excluded = emitters_full(term)
    return prod


def emitters_full(term: str):
    pay = re.compile(r'"edge_type"\s*:\s*"%s"' % re.escape(term))
    code = re.compile(r'(?:append|_edge|emit|add_edge)\s*\([^\n]{0,120}["\']%s["\']'
                      % re.escape(term))
    tracked = [f for f in git("ls-files", "-z").split("\0") if f]
    prod, excluded = {}, {}
    read_n = skipped = 0
    for f in tracked:
        if not f.endswith(EXTS):
            continue
        ap = WS / f
        try:
            if ap.stat().st_size > SIZE_CAP:
                skipped += 1
                continue
            txt = ap.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        read_n += 1
        if term not in txt:
            continue
        pn, cn = len(pay.findall(txt)), len(code.findall(txt))
        if not (pn or cn):
            continue
        row = {"payload": pn, "code": cn}
        if f.startswith(NON_PRODUCER_PREFIXES):
            excluded[f] = row
        else:
            prod[f] = row
    prod["_denominator"] = {"tracked": len(tracked), "read": read_n, "skipped_over_cap": skipped}
    return prod, excluded


def sole_written_holds(term: str):
    """(holds, producer_files, excluded_files, denominator) -- exactly one producer emitter."""
    prod, excluded = emitters_full(term)
    denom = prod.pop("_denominator")
    return (len(prod) == 1), prod, excluded, denom


# --------------------------------------------------------------------------- edge fixtures
SOLE = "STORED_IN"          # licensed: this producer's own type
MULTI = "OWNED_BY"          # NOT licensed: graphuni-storage writes 232 of them
BYSTANDER = "READS"         # neither requested nor licensed -- must be untouched either way


def prior_cycle_snapshot() -> list:
    """The archived snapshot this producer reads back: its own prior output PLUS another
    producer's live edges, in the shape derive_runner archives them."""
    return [
        {"source": "s3:opal-data-bd/gold/a.json", "target": "arn:aws:s3:::opal-data-bd",
         "edge_type": SOLE, "layer": "inter"},
        {"source": "s3:opal-data-bd/gold/b.json", "target": "arn:aws:s3:::opal-data-bd",
         "edge_type": SOLE, "layer": "inter"},
        # graphuni-storage's shape, verbatim from
        # org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer.json
        {"source": "opal-data-inf/bronze/orion-api/*/assets.csv",
         "target": "arn:aws:s3:::opal-data-inf", "edge_type": MULTI,
         "layer": "aws", "level": "prefix"},
        {"source": "opal-data-bd/config/ticker_lookup.json",
         "target": "arn:aws:s3:::opal-data-bd", "edge_type": MULTI,
         "layer": "aws", "level": "object"},
        {"source": "arn:aws:lambda:us-east-1:313476888478:function:x",
         "target": "arn:aws:s3:::opal-data-bd", "edge_type": BYSTANDER, "layer": "aws"},
    ]


def count(edges, et) -> int:
    return sum(1 for e in edges if str(e.get("edge_type", "")) == et)
