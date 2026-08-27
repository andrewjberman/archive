<to_id>ADVI_NNAATTR.TO-1b</to_id>
<project>ADVI_NNAATTR</project>
<title>DS lint cleanup — C_07.advisor_attribution.py 6 PRE-EXISTING ruff violations (per-class, no --fix bundle)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>0.4.0_DS_ClientPlatform (self-authored; COO-nodded 195533Z under CTO Rule A / NFRA_COT_RULE15)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project ADVI_NNAATTR is complete; this TO was last touched 2026-06-17, predating the project close 2026-06-22. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>LOW — pure lint debt, no behavior change. SEQUENCED: execute ONLY AFTER tonight's nightly validates the TO-1 architect_no_infer change in isolation, so the SEV1-relevant C_07 change verifies on the served artifact WITHOUT a second concurrent C_07 edit in the same nightly.</priority>

<context>
TO-1 (commit 0bca5a46a) added the additive architect_no_infer column to C_07. The ds-commit-gate
surfaced 6 PRE-EXISTING ruff E/F violations on touch (the file predates the tightened gate; lines NOT
in the TO-1 edits). Accepted via CTO Rule A (isolate the intended change + gate-note; NEVER a --fix
bundle on a live SEV1-adjacent script — C_07 feeds account_team to 14 consumers). This TO cleans them
as a SEPARATE per-class pass.
</context>

<deliverable>
Manually clean (NOT `ruff --fix`) the 6 pre-existing violations in C_07.advisor_attribution.py:
- F401 (L67): `import sys` unused -> remove the import (confirmed no `sys.` usage in the file).
- E701 x4 (L210-213): the rollup_roles col-map `if role == 'x': col = 'y'` one-liners -> split each onto
  two lines (mechanical, zero semantic change).
- E712 (L338): `acct_dim['account_is_open'] == True` -> use `.eq(True)` (semantics-IDENTICAL to `== True`
  on a pandas mask; NOT the bare-truthiness form ruff suggests, which differs for non-bool/NaN). Verify
  account_is_open dtype before choosing; default to `.eq(True)` to preserve exact NaN-as-False behavior.
</deliverable>

<acceptance_criteria>
AC1: ds-commit-gate.sh passes clean on C_07 (0 ruff E/F/FA, py_compile, AST) — no bypass note needed.
AC2: NO behavior change — account_team output (incl architect_no_infer + the 14-consumer columns) byte-identical
     to the pre-cleanup nightly artifact (diff the served account_team.parquet pre/post on a column basis).
AC3: deploy via the standard DS cycle; verify on the SCHEDULED nightly (no ad-hoc run).
</acceptance_criteria>

<compiler_tools_mandate>
Before: comp-pipescript io C_07 (consumers unchanged). After commit: comp-pipescript deployed MATCH.
</compiler_tools_mandate>

<cross_domain_coordination>
C_07 account_team is read by 14 consumers (comp-blast). This TO changes NO output values (lint-only), so
cross-domain risk is nil — but AC2 (byte-identical account_team) is the structural guard. No coordination needed.
</cross_domain_coordination>
