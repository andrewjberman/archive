# TO NFRA_GLOBGRPH.TO-USERS-DELPROT -- make DESIRED match APPLIED on the served users table: declare `deletion_protection_enabled = true` on `aws_dynamodb_table.opal_users_v2` in the shared-infra module (live: true; the declaration lacks the attribute, so every unscoped plan would null it) -- never an apply of the null; acceptance = the UNSCOPED re-plan of shared-infra at 0 add / 0 change / 0 destroy once this and TO-MSHEAT-EXPIRY have both landed, and the live table still reading deletion protection true

# pipeline-override: a ONE-ACT change-management order on a project whose register reads COMPLETE (NFRA_GLOBGRPH: no ENDPOINT section, no atom decomposition) -- the spec and the acceptance are 1.0.0_SA_CTO's GATE RULING 93765 act (b) on the worker's STOP (row NFRA_GLOBGRPH-S1 @3d2daa3ffa); the carrier of record is that row and this seat's own deploy-ledger entry; audited here as the sibling of TO-MSHEAT-EXPIRY's override line.

<task_order>
<id>NFRA_GLOBGRPH.TO-USERS-DELPROT.declare-deletion-protection</id>
<to_id>NFRA_GLOBGRPH.TO-USERS-DELPROT</to_id>
<project>NFRA_GLOBGRPH</project>
<issued_to>0.8.0_AE_CloudComp~K</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-09-03</issued_date>
<status>pending -- GO paired at cut (2.0.0_SA_COO, /drive v2 tick 4, 16:1xZ). Authority: 1.0.0_SA_CTO 93765 act (b), verbatim: "2.0.0_SA_COO cuts a SECOND order under the NFRA_GLOBGRPH row to the same owner class: declare deletion_protection_enabled = true on aws_dynamodb_table.opal_users_v2 in the shared-infra module so DESIRED matches APPLIED (never an apply of the null); acceptance = the unscoped re-plan of shared-infra reading 0 add / 0 change / 0 destroy after (a) and (b) both land, and the live table still reading deletion protection true. Its own ledger entry, its own proof instance. The order in which (a) and (b) land does not matter; each has its own unscoped read." Sequenced with the same seat's TO-MSHEAT-EXPIRY (amended @4fa04d9c1f): either first; each with its own unscoped read.</status>
<priority>P1 -- a served users table whose declaration would strip its delete guard on any unscoped apply; every apply of shared-infra until this lands carries that passenger</priority>
<endpoint>docs/architecture/NFRA_GLOBGRPH_PRD.md (2026-06-08; context only -- this order changes no spec); the endpoint is the drift row NFRA_GLOBGRPH-S1 @3d2daa3ffa closed by DESIRED == APPLIED on one attribute</endpoint>
<tier>2</tier>
</task_order>

**Directive:** none on the register (NFRA_GLOBGRPH is a COMPLETE flat project; this is change management on its infra) · **Fabric:** laptop (where `safe-apply` and the shared-infra state live) · **The carrier of record:** row NFRA_GLOBGRPH-S1 @3d2daa3ffa (0.8.0_AE_CloudComp~K, 15:5xZ) + the ledger entry this order opens.

## THE FACT (from the worker's STOP, read by the gate)

The SAVED UNSCOPED plan of `infra/aws/terraform/shared-infra` read **0 add / 2 change / 0 destroy**: the ms-heat lifecycle rule AND `aws_dynamodb_table.opal_users_v2` `deletion_protection_enabled` **true -> null**, while the live table reads **true**. The declaration at `infra/aws/terraform/shared-infra/dynamo.tf:15` carries no `deletion_protection_enabled` attribute (compare `dynamo-market-data-import.tf:67`, which declares it `true`). Terraform therefore plans to null it on every unscoped apply -- a served users table losing its delete guard as a passenger of any other change. 0.8.0_AE_CloudComp~K refused the 0/2/0 apply against an exact 0/1/0 gate, ran nothing, and filed the row: the spine's L7 shape to the letter (1.0.0_SA_CTO 93765).

## DELIVERABLE -- in this order

1. **THE LEDGER FIRST:** `.tools/deploy_ledger.py open` a fresh entry `shared-infra-users-v2-deletion-protection` (owner `0.8.0_AE_CloudComp~K`, the target address `aws_dynamodb_table.opal_users_v2`, the one attribute, the reason citing NFRA_GLOBGRPH-S1 and 93765 act (b)); the entry's legs: L1 declaration commit, L2 the scoped plan reading the expected triple, L3 the apply (or the no-op) with its output file, L4 the unscoped re-plan + the live read.
2. **THE PRE-READ, live, BEFORE any act:** `aws dynamodb describe-table --table-name <the table's name from the declaration> --query 'Table.DeletionProtectionEnabled'` quoted with its UTC time. Expected `true`. If it reads anything else, STOP and report -- the premise of this order is the live true.
3. **THE DECLARATION:** add `deletion_protection_enabled = true` to `resource "aws_dynamodb_table" "opal_users_v2"` in `infra/aws/terraform/shared-infra/dynamo.tf` -- one line, placed as `dynamo-market-data-import.tf:67` places it; nothing else in the file changes. `terraform fmt -check` on the file; commit through `.tools/safe-commit.sh` under your author with a python-written `-F` message file (L1).
4. **THE PLAN, SCOPED, SAVED:** with the estate's Terraform (`.tools/terraform.exe -chdir=infra/aws/terraform/shared-infra`, the module cache's version -- never `init -reconfigure`), `plan -target=aws_dynamodb_table.opal_users_v2 -out=<file named in the ledger>`. EXPECTED TRIPLE: **0 add / 0 change / 0 destroy** -- the declaration now equals the live attribute, so Terraform has nothing to do on that address (if the plan instead reads a change on that address, STOP with the output pasted: the premise or the declaration is wrong, and nothing applies). The scoped plan's output captured to a FILE named in the ledger (L2).
5. **THE APPLY LEG:** on a 0/0/0 scoped plan, `safe-apply` of that saved plan is a NO-OP and is still run (so the ledger carries the apply output reading no changes) -- never a bare `terraform apply`, never an unscoped apply (TO-MSHEAT-EXPIRY's lifecycle change may still be pending in the same module). Output to a file (L3).
6. **THE ACCEPTANCE, TWO READS (AMENDED 16:3xZ on row NFRA_GLOBGRPH-S2 @28b9a1e4d6: the unscoped plan also carries NINE `aws_apigatewayv2_route` authorization drifts the module would strip -- they are a finding at 1.0.0_SA_CTO, never applied here; so the unscoped re-plan after this order reads the users-table line GONE and those nine untouched, disclosed whole with their addresses; UDP-AC5 reads with this):** (i) the UNSCOPED re-plan of shared-infra AFTER this order: if TO-MSHEAT-EXPIRY has already landed it reads exactly **0 add / 0 change / 0 destroy**; if not yet, it reads exactly **0 add / 1 change / 0 destroy** and that one change is the lifecycle rule and NOTHING else (the users-table line gone from the plan) -- state which case you are in and quote the plan's summary line and its address list; (ii) the live `describe-table` read AFTER, `DeletionProtectionEnabled: true`, quoted with its time. The ledger closes on both reads (L4). When both orders have landed, the FINAL unscoped re-plan at 0/0/0 is quoted on whichever order lands second -- and on this one's report if that is this one.
7. **THE REPORT** to `2.0.0_SA_COO`: the pre-read, the declaration commit, the scoped plan triple, the apply file, both acceptance reads, the ledger entry's path and state, push state MEASURED (LOCAL). The proof instance validated before the report. No message to any seat other than the issuer.

## ACCEPTANCE -- criterion ids minted at cut

<criterion id="UDP-AC1" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC1` -- THE PRE-READ: live `describe-table` `DeletionProtectionEnabled` quoted BEFORE any act, reading true (or the STOP on anything else).
<criterion id="UDP-AC2" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC2` -- THE DECLARATION: one attribute added to `aws_dynamodb_table.opal_users_v2` in `shared-infra/dynamo.tf`, `terraform fmt -check` clean, committed under the ledger entry opened FIRST.
<criterion id="UDP-AC3" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC3` -- THE SCOPED PLAN: `-target=aws_dynamodb_table.opal_users_v2`, saved to a file named in the ledger, reading exactly 0 add / 0 change / 0 destroy on that address (DESIRED == APPLIED); any change on that address is a STOP with the output pasted, no apply.
<criterion id="UDP-AC4" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC4` -- THE APPLY LEG: `safe-apply` of the saved plan (a no-op apply, still run and captured to a file); never bare, never unscoped.
<criterion id="UDP-AC5" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC5` -- THE ACCEPTANCE: the UNSCOPED re-plan of shared-infra AFTER reading 0/0/0 (both orders landed) or exactly 0/1/0 = the lifecycle rule only (this order first), quoted with its address list; the live `describe-table` AFTER reading true, quoted; the ledger entry CLOSED on those reads.
<criterion id="UDP-AC6" cell_refs="ROW-NFRA_GLOBGRPH-S1"/> `UDP-AC6` -- push state MEASURED at report; the proof instance VALID (`.tools/proof-of-spec-check.py`); the status flip on this flat-root face is the issuer's on the report; no `git push`.
<expected_criteria>UDP-AC1, UDP-AC2, UDP-AC3, UDP-AC4, UDP-AC5, UDP-AC6</expected_criteria>

## SURFACES

- `infra/aws/terraform/shared-infra/dynamo.tf` (:15 the resource; the one attribute added); `infra/aws/terraform/shared-infra/dynamo-market-data-import.tf:67` (the pattern, read only).
- The live table (describe-table, read only; the attribute is never written by hand -- Terraform's no-op apply is the only act).
- `org/critical_paths/.open_deploys/shared-infra-users-v2-deletion-protection.json` (yours to open first and close last); `org/surprise_channel/NFRA_GLOBGRPH/INVESTIGATION_v1.md` (append-only rows for anything odd; S1 stands as the finding and is the CVO's to disposition).

## BOUNDS

- **`safe-apply` only, on a SAVED SCOPED plan; never bare `terraform apply`; never an unscoped apply** (the sibling order's lifecycle change may be pending in the same module). A triple other than the expected one is a STOP with the output pasted, no retry, no override.
- **Two Terraform versions live on this box** (PATH v1.14.5 vs the module cache and safe-apply at `.tools/terraform.exe` v1.9.8): use `.tools/terraform.exe -chdir=...`; a PATH plan refuses "Backend configuration changed"; NEVER `init -reconfigure` the shared module.
- **Zero IAM change; no new monitor / alarm; nothing on any other resource.**
- **PUSH (standing law on this CODEX seat's face):** a shared branch (CLOUD / DEV / PROD / main / SITEZ) is pushed ONLY by `0.0.0_AB_MSTR` or `0.0.0_AB_MSTR~Z`, and only on Andrew's word while he is at the terminal; this seat COMMITS and states LOCAL; it NEVER runs `git push`.
- Certifier != author: 3.0.0_SA_CVO grades; the issuer flips the face.

<decomp_ref>
<decomp_doc>org/surprise_channel/NFRA_GLOBGRPH/INVESTIGATION_v1.md</decomp_doc> @3d2daa3ffa (row NFRA_GLOBGRPH-S1, the carrier of record for this act; NFRA_GLOBGRPH has no atom decomposition -- the pipeline-override line above says so and is audited), cell ROW-NFRA_GLOBGRPH-S1
<owned_cells>ROW-NFRA_GLOBGRPH-S1</owned_cells>
</decomp_ref>

<preflight>
comp-schedule: RUN -- GATES ARMED 23 across 5 carriers (read at 2026-09-03 15:40Z); none names NFRA_GLOBGRPH's users table; the HOLD entry 20260903T1120Z and ledger 45b641343d name the sibling order's lifecycle act, sequenced with this one by both faces.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM resource, policy or role is touched; the one attribute is a DynamoDB table property already true live.
comp-adversary: RUN -- rc 0 at read-vintage @3bf5a6ea0a (2026-09-03T16:19:11Z); 2/2 cited commits VERIFIED, 0 UNVERIFIABLE; cited-path vintage 7 attempted / 4 stable / 3 flagged (dynamo.tf GONE; shared-infra-users-v2-deletion-protection.json GONE; NFRA_GLOBGRPH.TO-USERS-DELPROT_PROOF_OF_SPEC.json GONE -- this order's own outputs, GONE by construction at cut); --no-packet (the caller's choice).
</preflight>

<proof_of_spec>
Criterion ids minted at cut by the issuer: `UDP-AC1`..`UDP-AC6`. The ASSIGNEE fills a `PROOF_OF_SPEC.schema.json` instance at
`org/tier2_senior/0.8.0_AE_CloudComp~K/deliverables/NFRA_GLOBGRPH.TO-USERS-DELPROT_PROOF_OF_SPEC.json` and validates it with
`.tools/proof-of-spec-check.py` BEFORE reporting; UDP-AC1 (the pre-read) and UDP-AC5 (the unscoped re-plan) are the controls that must be able to FAIL.
</proof_of_spec>

<compiler_tools_mandate>
BEFORE WRITE: `comp-read infra/aws/terraform/shared-infra/dynamo.tf --for "the opal_users_v2 resource: every attribute it declares, any lifecycle/ignore_changes block, and whether deletion protection appears anywhere"`; `comp-schedule` before the apply leg; `comp-adversary compose` on this order at read-vintage before step 3.
</compiler_tools_mandate>

DELIVERABLE REPORT: one message to 2.0.0_SA_COO with the seven items of step 7; the proof instance path above.
