# TO ADVI_INSURE.TO-S1-AE — the insurance SILVER family: its OWN `module.silver_converter` family + the prefix-scoped notification on the bucket singleton (TF + package; DESIRED first, apply on the CTO per-apply gate)

<task_order id="ADVI_INSURE.TO-S1-AE" project="ADVI_INSURE">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T02:2xZ</issued>
<decomp_ref>workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md -- <owned_cells>INS-b-1</owned_cells> (the SILVER half of the landing plane: `.../silver/insurance_*` parquet reachable from the bronze by a converter that RUNS; the bronze half is landed by INS-a-5 (c'), complete on the 04:35Z fires; INS-b-2 (the 49financial-vs-49f leaf spelling) is READ, not owned)</decomp_ref>
<proof_of_spec>
  <expected_criteria>S1-1,S1-2,S1-3,S1-4,S1-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADVI_INSURE.TO-S1-AE.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json S1-1,S1-2,S1-3,S1-4,S1-5 -->
</proof_of_spec>
<status>pending -- GO on delivery of this face (2.0.0_SA_COO 2026-08-30 02:2xZ); sequenced at the seat AFTER the P2F M-2 deploy plan (84218) and AFTER the floor hold (applied 01:53Z); the converter's runtime profile + bronze prefixes arrive from 0.4.0_DS_ClientPlatform~R when its code settles</status>
<priority>P1 -- the ADVI_INSURE silver plane reaches NO converter today (live notification config: 8 rules, the blackdiamond one is cottonwood-only); the bronze lands daily at 04:35Z into a prefix nothing consumes.</priority>
<authority>Substrate CONFIRMED + own-family RATIFIED: 0.7.0_AE_CloudOps 84371 on 0.4.0_DS_ClientPlatform~R 84189 and the issuer's 84193/84194 rec -- silver.tf:64-72 (D1a, 2026-07-14) pins blackdiamond to cottonwood and names 49f "its OWN future family", calling the alternative "a silent never-widen violation materialized by a map edit made for a different actor"; silver.tf:77 materialises the pin. Sequencing (i) ruled 84193: the mint HOLDS off the blackdiamond family (S5/S7 ride an unfiltered re-vendor) -- this face is the route that needs neither. Cell INS-b-1.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md`, cell `INS-b-1`** (landing plane: `blackdiamond/49financial/bronze/insurance_*` RAW per run and `.../silver/insurance_*` parquet, dedup + dtype; oracle = keys exist at the grammar, head-object). **This face is the MECHANISM for its silver half.** The converter CODE is `0.4.0_DS_ClientPlatform~R`'s under `ADVI_INSURE.TO-R1-DS` (event-shaped stage entry BUILT @`85abccfd68`; 28 arms, 4/4 mutants); this face is the HOST + WIRING, AE-class, Rule 13 infra.

## The one-paragraph version

Add a NEW `module.silver_converter` family for the 49F insurance feeds — config + a package, no module change (84371 s.3): (a) a `local.silver_families` entry; (b) a `local.silver_runtime_profile` entry (memory/timeout/runtime/layers FROM DS~R's measured footprint, never invented); (c) a `local.silver_source_scopes` pin for `49financial` on the new family (never widening `blackdiamond`'s cottonwood pin); (d) IAM role + attachments materialise off `silver_families`; (e) `BUILD_MANIFEST.json` vendoring EXACTLY `{bd49f_insurance_conversion.py, raw_json_reader.py, silver_registry.py}` + the built zip at the family's `artifact_key` — **uploaded BEFORE the apply** (TF cannot create the function on a missing key); (f) the prefix-scoped rule(s) for `blackdiamond/49financial/bronze/insurance_*` added as an EDIT to the ONE `aws_s3_bucket_notification` (silver.tf:520; 8 live rules; a second resource silently deletes them all).

## Acceptance criteria — S1-1 through S1-5

<criterion id="S1-1" cell_refs="INS-b-1"/> **INPUTS FROM THE CODE OWNER, NOT INVENTED.** Runtime profile (memory, timeout, runtime, layers) and the bronze prefix list (which `insurance_*` feeds, one rule or several) taken from `0.4.0_DS_ClientPlatform~R`'s measured stage (its dry run on the real 08-29 bronze: 77 rows detailsearch, 77 rows / 106 contracts export), cited by message id + commit. The `family` value the stage entry validates == the family name declared here.
<criterion id="S1-2" cell_refs="INS-b-1"/> **DESIRED FIRST, on the per-apply gate.** The targeted plan (1.9.8 shim; `-target` the new family's resources + the notification singleton EDIT; the untargeted plan carries the held 08-11 emitter repoint and the P2F-3b rows) printed as rows to `2.0.0_SA_COO` + `1.0.0_SA_CTO` in the 84132 shape, with the notification plan showing `+ lambda_function {prefix=blackdiamond/49financial/bronze/insurance_..., ...}` and **`(N unchanged blocks hidden)`, 0 to destroy** against the live rule count read in the same breath. APPLY only on 1.0.0_SA_CTO's gate; `safe-apply` only; NEVER#6 ledger opened at the apply with `**Status:**` (the indexed form) and closed with the read-back.
<criterion id="S1-3" cell_refs="INS-b-1"/> **THE PACKAGE IS THE CODE OWNER'S BYTES.** The zip's vendored modules are byte-identical (LF-normalised sha256 printed) to the repo files at the commit DS~R names; `BUILD_MANIFEST.json` carries `built_from_commit`; the blackdiamond family's manifest is UNTOUCHED (diff shows it) -- S5 does not ride, S7 is not armed.
<criterion id="S1-4" cell_refs="INS-b-1"/> **EXERCISED ON THE APPLIED PLANE, on the NEXT 04:35Z fire, not a hand invoke:** the new family's own CloudWatch log shows the S3 event for that day's `insurance_*` keys -> the stage entry -> `.../silver/insurance_*` parquet landed at the grammar (head-object, rows == the bronze's attested totals), the receipt reported UNCONVERTED, `relationshipdetail` SKIP: absent-day-is-absent; NEGATIVE CONTROL: the cottonwood family's log shows NO invocation on those keys. A manual invoke is QA evidence only.
<criterion id="S1-5" cell_refs="INS-b-1"/> **THE OTHER 8 RULES UNMOVED.** `get-bucket-notification-configuration` before vs after: the 8 pre-existing `LambdaFunctionConfigurations` byte-identical, +N new; denominator printed. And the two leaf spellings (INS-b-2) named in the instance: `49financial/` is this family's prefix; `49f/` is untouched.

## Do NOT

- ⛔ **Do not add the insurance modules to `opal-assets-silver-blackdiamond`'s BUILD_MANIFEST** — the D1a never-widen pin and the S5/S7 side-effect both forbid it.
- ⛔ **Do not declare a SECOND `aws_s3_bucket_notification`** — the singleton replaces the bucket's whole config.
- ⛔ **Do not apply untargeted** — the plan carries foreign rows on an unrelated authorisation.
- ⛔ **Do not invent the runtime profile or the prefix list** — S1-1.
- ⛔ **No alarm, no monitor** (INS-inv-5; the DLQ is the visibility path, per DS~R's design).
- ⛔ **Nothing to `4.0.0_SA_CRO`.**

## Lane and mechanics

Rule 13 infra; `safe-apply` only; `terraform fmt -check` never `-diff`; the 1.9.8-vs-1.14.5 binary trap; Rule-20 graph query before the change; NEVER#6 ledger with the INDEXED `**Status:**` field and a `.open_deploys` sentinel (the 01:58Z RED class).

## What is owed back, and when

S1-1's inputs are a handoff FROM DS~R (that seat sends them; this face does not wait silently — if they have not arrived when this face reaches the top of the seat's queue, ask DS~R by serial). Then the plan rows (S1-2) to `2.0.0_SA_COO` + `1.0.0_SA_CTO`; the apply read-back; then S1-4 on the first scheduled fire after the apply. `3.0.0_SA_CVO` grades; the instance travels with `TO-R1-DS`'s.
