"""GS-f-5 AC1 (row D1-S7; ruling R6): the read-only census of the seven commit-path gates that read the working tree or grade
beyond the act. Checks the report's shape and its denominators, not its conclusions (those are the CTO's to read).

Report: org/missions/D0/NFRA/NFRA_GATSCP/deliverables/0.9.0_WK_NFRA_GATSCP~12/GATE_CENSUS_round3.md, one table with a row per
gate and the columns `gate | reads | beyond the act | false refusals 7d | audited overrides 7d | log read`, and a line
`CENSUS window=<from>..<to> logs=<n> lines_read=<n>`.
Arm 1: all seven gates have a row (commit_gate_runner, to-pipeline-gate, to-decomp-ref-lint, owned-paths-check,
  mstr-ledger-check, pipescript-suite-check, manifest_check).
Arm 2: every row's two 7-day columns are integers (0 included) and its `log read` names a path or `none: <reason>`.
Arm 3: the CENSUS line is present with integer denominators.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT, finish  # noqa: E402

REPORT = os.path.join(ROOT, "org/missions/D0/NFRA/NFRA_GATSCP/deliverables/0.9.0_WK_NFRA_GATSCP~12/GATE_CENSUS_round3.md")
GATES = ["commit_gate_runner", "to-pipeline-gate", "to-decomp-ref-lint", "owned-paths-check", "mstr-ledger-check",
         "pipescript-suite-check", "manifest_check"]
text = open(REPORT, encoding="utf-8").read() if os.path.exists(REPORT) else ""
rows = {}
for ln in text.splitlines():
    cells = [c.strip() for c in ln.strip().strip("|").split("|")] if ln.strip().startswith("|") else []
    if len(cells) >= 6:
        for g in GATES:
            if g in cells[0]:
                rows[g] = cells
present = all(g in rows for g in GATES)
ints = present and all(re.fullmatch(r"\d+", rows[g][3]) and re.fullmatch(r"\d+", rows[g][4]) for g in GATES)
logs = present and all(rows[g][5] and ("/" in rows[g][5] or rows[g][5].lower().startswith("none:")) for g in GATES)
census = re.search(r"(?m)^CENSUS window=\S+\.\.\S+ logs=\d+ lines_read=\d+", text)
arms = [
    ("seven-gate-rows", present, "report=%s rows=%s" % (os.path.exists(REPORT), sorted(rows))),
    ("integer-7d-columns-and-log", bool(ints and logs), "ints=%s logs=%s" % (bool(ints), bool(logs))),
    ("census-denominators", bool(census), "line=%s" % (census.group(0) if census else None)),
]
sys.exit(finish("GS-F5-CENSUS", arms))
