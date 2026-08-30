# TO ADVI_BDPARITY.P2-1-AE — apply DS~C's per-feed selector patch to the deployed BD puller and read it on the running artifact (P2-1 item 1, the AE half)

<task_order id="ADVI_BDPARITY.P2-1-AE" project="ADVI_BDPARITY">
<issued_to>0.8.0_AE_CloudComp~Y</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T08:3xZ</issued>
<decomp_ref>org/tier2_senior/0.4.0_DS_ClientPlatform~C/task_orders/ADVI_BDPARITY.P2-CENSUS.full-population-parity-census.md -- P2-1's build item (the per-feed selector; the DS half authored @d9ac9dc597, FINAL @d981d2366a) -- <owned_cells>P2-1-AE</owned_cells></decomp_ref>
<proof_of_spec>
  <expected_criteria>PA-1,PA-2,PA-3,PA-4</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/ADVI_BDPARITY.P2-1-AE.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json PA-1,PA-2,PA-3,PA-4 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>pending -- GO on delivery of this face for PA-1 + PA-2 (apply the patch on the AE lane, plan DESIRED); PA-3 (the apply) on the CTO gate's word after its diff read; PA-4 the read on the running artifact. NOT ahead of Andrew's word on P2-2 -- this only has to be read on the running artifact before that word is spent. Seated on the released 0.8.0_AE_CloudComp~Y (COO~X 86638: both faces at that seat complete, nothing sequenced; to-check --all --assignee: 0 active TOs) so the item does not queue behind 0.7.0_AE_CloudOps's inf-silver-chain plan.</status>
<priority>P2 -- P2-2 requires the selector read on the running artifact before Andrew's word is spent; without it a population pull spends three endpoints for one, tripling the ask.</priority>
<authority>The issuer's staffing ruling 86548 (DS authors, AE applies); DS~C's patch FINAL @d981d2366a (supersedes d9ac9dc597 -- docstring attribution corrected per CTO 86666, hunks otherwise byte-identical, 11 of 11 re-run; sha256 ab417c452533af2d2b25b345760db12640ca09f432fcb54b144d712b99084261, applies clean at fa0efe270a; 11 of 11 arms, no egress); the CTO reads the diff before the apply (86550). Rule 13: AE owns infra/PROD-triggers. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## The one-paragraph version

The deployed BD reporting puller (`infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py`) pulls all three feeds (performance, costBasis, allocation) per account. DS~C authored a selector: `feeds=None` -> all three (today's behaviour, UNCHANGED -- a performance-only DEFAULT would silently starve `OPAL_TAXSMA_PT2`'s silver build, which reads `reporting_costbasis` + `reporting_allocation`; measured at `build_fact_taxsma_report.py:7-8,:88-89`); `feeds=["performance"]` -> one endpoint per account (what P2-2 passes); an unlisted feed name or an empty list -> REFUSED by name. The manifest records `feeds_requested`. This face APPLIES that patch under the AE lane and reads it on the running artifact. **It changes no scheduled behaviour** and makes **no vendor call**.

## Acceptance criteria

<criterion id="PA-1"/> **THE PATCH APPLIED on the AE lane:** `git apply --check` then apply of `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPARITY.P2-1_feed_selector.patch` (5,145 B, 0 CR) at the current HEAD with the base stated (applies clean at 8cf9670ac2 per 86701), the patch's sha256 printed == ab417c452533af2d2b25b345760db12640ca09f432fcb54b144d712b99084261; DS~C's 11-arm test re-run at this seat, 11 of 11 rc=0, `DRY_RUN=1` untouched; `.tools/commit-gate.sh` clean; `safe-commit -F` citing DS~C's FINAL commit d981d2366a + the sha ab417c45... (a3120670 / d9ac9dc597 are SUPERSEDED -- applying them would land different bytes than the gate read).
<criterion id="PA-2"/> **THE PLAN, DESIRED:** the targeted Terraform plan on the ONE function: the code row (s3_object_version + source_code_hash) and ZERO env / trigger / IAM rows; any other shape STOPS with the plan pasted. The built zip DOWNLOADED and its lambda_function.py LF sha printed against the committed INDEX blob (never the worktree -- the 22a class, four instances 08-30). Rows to the issuer + `1.0.0_SA_CTO` before any apply.
<criterion id="PA-3"/> **THE APPLY on the gate's word:** `safe-apply` (never bare `terraform apply`, never `update-function-code`); NEVER#6 ledger opened via the tool at the apply; the apply report's triple exactly 0/1/0 on that one address.
<criterion id="PA-4"/> **READ ON THE RUNNING ARTIFACT:** `get-function-configuration` CodeSha256 == the uploaded zip, LastModified post-dating the apply, env UNCHANGED (printed before/after, set-identical); 0-diff re-plan; the ledger closed on this read. Proof instance VALID rc=0 positional PA-1..PA-4 with the checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **No vendor call** in any step -- the selector is exercised by DS~C's boundary-patched test only; a live pull is P2-2 and is gated on Andrew's per-use word.
- ⛔ **Do not change the default** -- `feeds=None` stays all-three (the CTO may rule otherwise on the diff read; then the arm inverts with it and DS~C re-authors -- not this seat's edit).
- ⛔ **Do not `cp` from the worktree** for any digest -- index blob only.
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

PA-1 + PA-2 as one message (rows) to the issuer + CTO + DS~C; PA-3/PA-4 at completion to the issuer + CTO + CVO; the proof instance at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer. This face binds the instance to ADVI_BDPARITY (Rule 27) for its duration; release on the CVO's grade.
