"""CE-p-4 shared carrier: the authority census, the question set, and the comp-which invoker.

ONE definition of every string the BEFORE capture and the AC1 battery both use, so the
regression comparison is between two runs of the SAME question list rather than two
hand-typed lists that agree by luck.

THE AUTHORITY (measured 2026-09-09, see the census below): this estate registers gold-script
ids IN THE FILESYSTEM, not in a registry file. `org/modules/graph/pipeline_cli.py`
:203 `_discover_script_trees` ("re-derive the script-tree universe from the FILESYSTEM at
call time -- NOT a frozen list", the roster-to-predicate move) and :3016 `_resolve_gold_script`
(globs `data/inf/scripts/gold/` then `data/black_diamond/scripts/gold/`) are the estate's own
resolvers, and both read directories. `comp-find 'GOLD_ID' .tools --all` returns 2 hits, BOTH
in `.tools/comp-which` -- the pattern has no other consumer, so there is no second authority
to reconcile against.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
COMP_WHICH = os.path.join(WS, ".tools", "comp-which")
SPILL_DIR = os.path.join(WS, ".comp-graph", "which")

# comp-which's own subject pattern, copied VERBATIM from .tools/comp-which:1279 so the census
# enumerates exactly the id-space the router claims to recognise.
GOLD_ID = re.compile(r"(?<![\w])(INF_)?[A-DIS]_-?\d{1,2}[a-z]?(?![\w])")

# The three gold-script homes the estate's own resolvers read. Declared here so the census
# prints WHICH directories it consulted; discovered by walking data/*/scripts/*/ (30 layer
# directories scanned, 3 carry GOLD_ID-shaped stems).
AUTHORITY_DIRS = (
    "data/black_diamond/scripts/gold",
    "data/cot/scripts/gold",
    "data/inf/scripts/gold",
)

# ---- the regression set -------------------------------------------------------------------
# The four `when:` phrasings F-10 measured, copied VERBATIM from
# org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~6/f10_lib.py:23-28
# (the set C-S46 graded: "comp-aws rows 0 of 78 ranked in each of four spilled rank files").
PHRASINGS = [
    "What AWS resources exist + how are they typed/connected?",
    "What's the drift / blast radius / unmanaged surface?",
    "Is any resource dual-managed across TF states?",
    "Cloud-shape snapshot + diff over time",
]

# ---- the three subject probes -------------------------------------------------------------
# PLANTED NON-EXISTENT: INF_D_99 -- verified absent from all three authority dirs.
PLANTED_Q = "what does INF_D_99 write to s3"
PLANTED_ID = "INF_D_99"

# NEGATIVE CONTROL: INF_D_02 is real (data/inf/scripts/gold/INF_D_02...py); INF_D_20 is the
# same id with the two digits transposed and is absent from all three dirs.
MISSPELLED_Q = "what does INF_D_20 write to s3"
MISSPELLED_ID = "INF_D_20"
MISSPELLED_NEAREST = "INF_D_02"

# POSITIVE CONTROL WITH A SUBJECT: the same question shape carrying a REAL id. The four
# regression phrasings carry no gold id at all, so they cannot exercise a resolved subject --
# this question does. (See row NFRA_COMPEFFICACY-W1-S1.)
REAL_Q = "what does INF_D_02 write to s3"
REAL_ID = "INF_D_02"


def authority_census():
    """Return (per_dir, all_ids). per_dir = [(reldir, sorted_ids)] for each authority dir."""
    per_dir = []
    all_ids = set()
    for rel in AUTHORITY_DIRS:
        d = os.path.join(WS, *rel.split("/"))
        ids = []
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if not name.endswith(".py") or name.startswith("__"):
                    continue
                stem = name.split(".")[0]
                if GOLD_ID.fullmatch(stem):
                    ids.append(stem)
        ids = sorted(set(ids))
        per_dir.append((rel, ids))
        all_ids.update(ids)
    return per_dir, sorted(all_ids)


def comp_which(q, extra=None):
    """Run the ESTATE'S OWN CLI in a fresh process. Returns (rc, combined_text, spill_text).

    The spill file is PID-keyed (.tools/comp-which:1875), so it is read back by locating the
    file whose mtime is newest under .comp-graph/which after the call -- the child's pid is not
    knowable from here, and reading the newest file is safe because each call is serialised.
    """
    argv = [sys.executable, COMP_WHICH] + list(extra or []) + [q]
    before = _spill_snapshot()
    r = subprocess.run(argv, cwd=WS, capture_output=True, text=True, timeout=110)
    text = (r.stdout or "") + (r.stderr or "")
    spill = _newest_spill(before, q)
    return r.returncode, text, spill


def _spill_snapshot():
    out = {}
    if os.path.isdir(SPILL_DIR):
        for n in os.listdir(SPILL_DIR):
            p = os.path.join(SPILL_DIR, n)
            try:
                out[n] = os.path.getmtime(p)
            except OSError:
                pass
    return out


def _newest_spill(before, q):
    """The spill file written (or rewritten) by the call just made, or '' if none.

    TWO conditions, both required -- mtime alone is not enough. A stale file from an earlier
    question can win a coarse mtime comparison and would then be read as THIS question's
    ranked list, which is a wrong-object error one step before every comparison in this
    battery. So the file must ALSO carry this question on its `question:` line.
    """
    if not os.path.isdir(SPILL_DIR):
        return ""
    want = "question: " + "'" + q.replace("'", "''") + "'"
    best, best_m = "", -1.0
    for n in os.listdir(SPILL_DIR):
        p = os.path.join(SPILL_DIR, n)
        try:
            m = os.path.getmtime(p)
        except OSError:
            continue
        if n in before and m <= before[n]:
            continue  # untouched by this call
        try:
            with open(p, "r", encoding="utf-8") as fh:
                body = fh.read()
        except OSError:
            continue
        if want not in body:
            continue
        if m > best_m:
            best, best_m = body, m
    return best


def ranked_rows(spill_text):
    """THE RANKED LIST, isolated from the spill file's header.

    This is the object the order calls 'the ranked list' and requires BYTE-EQUAL across the
    change. It is separated from the header deliberately: the header is where the new
    `subject_resolved` / `authority_consulted` keys land, so comparing whole files would
    compare the FIX against itself and could never pass. Rows are rank/tool/score/vetted/
    call/does -- the routing decision itself.
    """
    if not spill_text:
        return ""
    lines = spill_text.splitlines(True)
    out = []
    started = False
    for ln in lines:
        if not started:
            if ln.rstrip("\r\n") == "tools:":
                started = True
            continue
        out.append(ln)
    return "".join(out)


def terminal_routes(text):
    """The route lines a seat actually READS, with the two non-deterministic lines dropped.

    DROPPED, and why each is not part of the ranked list: any line carrying `WITHIN BUDGET`
    or `BUDGET REACHED` (Rule T prints the seconds this run spent -- a wall-clock reading, it
    differs run to run on an unchanged tool), and the spill PATH line (`Not it?  ALL N tools`)
    because the filename is `rank-<pid>.yaml` and the pid differs per invocation. The rank
    COUNT inside that line is preserved separately by ranked_rows().
    """
    keep = []
    for ln in text.splitlines():
        if "WITHIN BUDGET" in ln or "BUDGET REACHED" in ln:
            continue
        if ln.lstrip().startswith("Not it?  ALL "):
            keep.append(re.sub(r"\.comp-graph/which/rank-\d+\.yaml", "<spill>", ln))
            continue
        keep.append(ln)
    return "\n".join(keep) + "\n"


def rank_row_count(spill_text):
    return len(re.findall(r"(?m)^  - rank: \d+$", spill_text or ""))
