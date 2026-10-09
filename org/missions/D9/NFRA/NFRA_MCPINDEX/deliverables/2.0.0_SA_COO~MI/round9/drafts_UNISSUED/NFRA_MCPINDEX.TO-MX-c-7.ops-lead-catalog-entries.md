# NFRA_MCPINDEX task order -- `MX-c-7` -- the catalog's one writer adds the operations lead's six needs (E-30..E-35), two from the readers' census and four GAP, unowned

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md</decomp_doc>
<owned_cells>MX-c-7</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_NFRA_MCPINDEX~30</issued_to>
<issued_by>2.0.0_SA_COO~MI</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule.
comp-iam: DECLARED-NOT-APPLICABLE -- catalog source files and the regenerated catalog only; no role, grant or tool change.
comp-adversary: DECLARED-NOT-APPLICABLE -- the MX-c-6 pattern; the battery dry-run is the control (c7.AC1 0 of 6, c7.AC2 0 of 8 at base).
EGRESS CLASS, declared: NONE.
</preflight>

## 1. THE CELL -- `MX-c-7` (round 9; PRD v0.8 @0eff9e0e6d FWD-19, contract 4; decomposition section ROUND 9)

**Start only when MX-o-1 (your own previous order) AND MX-o-2 (worker ~31) are complete and drained.** Merge `CLOUD`
into your branch first. Both censuses are then at
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~30/census_trade_rec.json` and
`.../0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json`. A SERVED reader's tool name is the `TOOL` constant in
`infra/aws/ec2/opal-gateway/app/integrations/ops_trade_rec/integration.py` (or `ops_billing/`).

**What the user sees at the base.** The catalog's `needs:` list holds E-1..E-29, Alyssa's needs. None of the
operations lead's six items is there, so discover answers each with NOT_CATALOGUED.

**The act.** Add six need source files, `workflows/atom_decomposition/catalog_entries/need_E-30.yaml` ..
`need_E-35.yaml`, in the exact shape of the existing `need_E-*.yaml` files. Then regenerate
`infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` through the ONE emitter (`emit_catalog_v02.py`, C1):

| id | need | status / tool / owner |
|---|---|---|
| E-30 | trade reconciliation: Opal's trade status against the custodian's | census SERVED: `SERVED`, the reader's `TOOL`, its owner. Census GAP: `GAP`, tool null, owner = the census owner |
| E-31 | billing: AUM, fee rate, fee and paid status per account and period | the same rule from the billing census |
| E-32 | post model update rec | `GAP`, tool null, owner `unowned` |
| E-33 | high cash account alert FA | `GAP`, tool null, owner `unowned` |
| E-34 | assets transfer alert FA | `GAP`, tool null, owner `unowned` |
| E-35 | restricted account alert FA | `GAP`, tool null, owner `unowned` |

- Every entry is `op_class: read`. None retires one of Alyssa's C1-C8 / W1-W6, so each carries a `retires_none` reason
  naming the operations lead.
- E-33..E-35 are under the standing alert moratorium (contract 4): catalogued, never built.
- Each entry's `example_questions` carries the operations lead's own phrasing, so discover's own-text rule reaches it
  first: "trade reconciliation" and "did the custodian settle our trades" (E-30); "billing" and "which households have
  unpaid fees" (E-31); the item names for E-32..E-35.
- **Emitter input (row Z-W29-S1, ruled Z-S86):** run the emitter with `--census-dir` pointing at YOUR WORKTREE's own
  tracked census, never the main tree. The regenerated catalog then differs from base only in `needs:` and the
  built-by stamp. Print that diff summary in your report.

## 2. BOUNDS

1. You change `workflows/atom_decomposition/catalog_entries/need_E-3[0-5].yaml`, the regenerated `DATA_CATALOG.yaml`
   and `workflows/atom_decomposition/tests/` only. No discover code: if a phrasing does not route first with words
   alone, that is a BLOCKING row naming the ask and the first match, never a code edit.
2. No tool, grant, route or `.env` change. No deploy (MX-r-10). No push.
3. REFUSE a criterion you cannot meet as written, and report it with its measurement.

## 3. SURFACES

<paths>
workflows/atom_decomposition/catalog_entries/
workflows/atom_decomposition/tests/
infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml
org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~30/**
org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

Rows go to `org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md`:
- id `NFRA_MCPINDEX-Z-W30-S<k>`; re-read the file for the next free k at commit time;
- fabric `site-z`;
- `disarm_owner` `2.0.0_SA_COO~MI`;
- `surfaced_at` written as a full UTC timestamp, never a placeholder.

## 4. PROOF OF SPEC (literal; run from your worktree root)

<proof_of_spec>
  <expected_criteria>AC1,AC2</expected_criteria>
  <criterion id="AC1" cell_refs="MX-c-7" judgment="false"><invocation>bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round9/checks/c7.AC1.sh; echo "exit=$?"</invocation><expect>ops lead entries present 6 of 6; earlier entries kept 29 of 29; duplicates 0; violations 0 -- RESULT: PASS -- exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="MX-c-7" judgment="false"><invocation>bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round9/checks/c7.AC2.sh; echo "exit=$?"</invocation><expect>ops lead asks routed 8 of 8 on the first try -- RESULT: PASS -- exit=0</expect></criterion>
  <instance_path>org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~30/NFRA_MCPINDEX.TO-MX-c-7.ops-lead-catalog-entries.proof_of_spec.json</instance_path>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Write the proof instance at the `<instance_path>`, then flip `<status>` to complete and commit the instance,
deliverables and flip together. Report once, naming each entry's status and tool, the catalog diff summary, and each
ask's first match. After this order the issuer continues you with MX-r-10's PHASE A.

<!-- ===================== RECORD FACE ===================== -->

**ISSUER NOTES (2.0.0_SA_COO~MI).** Round 9 join of the two reader chains, worker ~30 after MX-o-1. STAGED UNISSUED
2026-10-09 ~10:2xZ (1.0.0_SA_CTO~Z @ff362e8444). Battery dry-run at base 1dd356991a (`round9/checks/`):
- c7.AC1 FAIL as expected: 0 of 6 present, 29 of 29 kept, 12 violations.
- c7.AC2 FAIL as expected: 0 of 8, all NOT_CATALOGUED.

<status>issued</status>
<round>9</round>
<fabric>site-z</fabric>
<risk>WORLD</risk>
<worker_class>worker</worker_class>
