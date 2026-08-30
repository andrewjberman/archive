# TO OPAL_ADVIPOINTERS.INF-RECORDER-SCOPE — `record-terraform-deploy.sh` stamps ONLY the addresses the saved plan applied (or an explicit `--function` list) and REFUSES a bare pipeline-wide call when a plan file is present; the source map's deploy rows stop being falsified by the tool that records them

<task_order id="OPAL_ADVIPOINTERS.INF-RECORDER-SCOPE" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T14:2xZ</issued>
<decomp_ref>OPAL_ADVIPOINTERS.INF-ONEWRITER face, issuer_record 13:1xZ/13:5xZ (the (k)-class item) -- the durable act named there; the ruling 1.0.0_SA_CTO 87430/87448 (owner AE base; the shape below; sequenced after DS~V's acceptance read, which landed 87455 and was accepted 87471). Cut on AE base's ask 87837, sequencing condition MET. Dispatched 87859.</decomp_ref>
<proof_of_spec>
  <expected_criteria>RS-1,RS-2,RS-3,RS-4,RS-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.INF-RECORDER-SCOPE.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json RS-1,RS-2,RS-3,RS-4,RS-5 ; checker vintage printed, rc read UNPIPED -->
</proof_of_spec>
<status>pending -- GO on delivery of this face. Scope RULED at the cut: the RECORDER ONLY. The 24 inf-pipeline rows the hand row did not stamp are NOT in scope -- their staleness is real and pre-existing (inf-assets-trigger 2026-05-13, inf-api-assets-v2 2026-06-23 among them) and "reconcile every row" is a different size of work with its own before/after; it is recorded as an OBSERVATION with a census owed (RS-4), not a remedy. The interim hand row 901c6f2d9c (case (a), recorded_by=manual) stays and is superseded only by the recorder's own next stamp on that function.</status>
<priority>P2 -- no served output moves; the field feeds verify-local.sh's undeployed-change detection, and a recorder that stamps 25 rows for a 1-function deploy would mark 24 functions' real drift as deployed -- the drift-blindness INF-ONEWRITER exists because of. Measured, not run (AE base 87398).</priority>
<authority>1.0.0_SA_CTO 87430 (owner 0.7.0_AE_CloudOps base; remedy = a FUNCTION-SCOPED stamp: the changed addresses from the saved plan or an explicit --function list, stamp only those rows, refuse a bare pipeline-wide call when a plan file is present); 1.0.0_SA_CTO 87448 (the interim hand row's provenance form, case (a) measured at 87554); 0.7.0_AE_CloudOps 87837 (the ask, the queue state). Rule 13 (DT/AE = infra; the recorder lives in infra/aws/lambda/ci/). Not to 4.0.0_SA_CRO.</authority>
</task_order>

## The one-paragraph version

`infra/aws/lambda/ci/record-terraform-deploy.sh` takes a PIPELINE and stamps `last_deployed_commit` / `last_deployed_at` on EVERY function whose `tf_file` sits under that pipeline's terraform directory -- 25 for `inf-pipeline` -- with no function scope (usage read at source: pipeline, `--version`, `--author` only). The 09:54Z apply deployed ONE. Running the recorder as ruled would have written 24 false "deployed" records over genuine, differently-dated ones, and `verify-local.sh` reads that field to detect undeployed change. Fix: the recorder derives the address set from the SAVED PLAN (the changed `aws_lambda_function` addresses) or an explicit `--function` list, stamps only those rows, and REFUSES a bare pipeline-wide call when a plan file is present.

## Acceptance criteria

<criterion id="RS-1"/> **THE SCOPE SOURCE:** the recorder accepts `--plan <file>` (reads the changed `aws_lambda_function` addresses from `terraform show -json <plan>`) or `--function <name>[,<name>]`; the stamped set is EXACTLY that set; every stamp prints `stamped N of M rows under <pipeline>` with the function names. File:line of the change named in the report; commit-gate clean; `safe-commit -F`.
<criterion id="RS-2"/> **THE REFUSAL:** a bare `record-terraform-deploy.sh <pipeline>` with a plan file present in the working directory (or `--plan` omitted while `--function` is also omitted) exits a DISTINCT non-zero rc (rc=2) printing the 25-vs-1 blast radius it refused; the legacy pipeline-wide behaviour survives ONLY behind an explicit `--all --i-mean-every-row` flag whose use is printed and audited.
<criterion id="RS-3"/> **THE VALUE STAMPED is the commit whose SOURCE is deployed**, derived as the hand row was (the last commit touching the function's `source_dir`, verified against the deployed zip's members), never the ledger commit or HEAD by default; `recorded_by=record-terraform-deploy.sh`, `deploy_ledger` and `deployed_code_sha256` written beside it in the same row form the hand row established (case (a): no consumer enumerates row keys -- 87554).
<criterion id="RS-4"/> **THE 24-ROW CENSUS, printed not repaired:** for the inf-pipeline map, per function: `last_deployed_commit` vs the last commit touching its `source_dir`, and whether the deployed CodeSha256 matches that commit's build (where a package can be downloaded) -- `stale N of 25, current M, unmeasurable K`, corpus and denominator printed. NO row other than the one this face exercises is written. The census is the OBSERVATION the reconciliation question is sized on.
<criterion id="RS-5"/> **THE FALSIFIERS, both polarities, on a SCRATCH copy of the map:** (i) the PRE-FIX recorder on the inf-pipeline scratch map stamps 25 of 25 (the failing baseline, run FIRST); (ii) the fixed recorder with `--plan isc_v.tfplan` (the 09:54Z saved plan, one address) stamps 1 of 25 and the other 24 are byte-identical before/after; (iii) a bare call with the plan file present -> rc=2, 0 rows written; (iv) `--function inf-silver-chain` stamps exactly that row with the source-commit value equal to the hand row's 6ab4c76a0f. Proof positional RS-1..RS-5, checker vintage printed, rc UNPIPED; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not write the production map for any row but the one this face exercises** (and that only via the fixed recorder in RS-5 (iv), replacing the hand row's `recorded_by=manual` with the recorder's own stamp -- values equal, provenance changed, both printed).
- ⛔ **Do not reconcile the 24 stale rows** -- RS-4 measures them; a remedy is a separate face after the census.
- ⛔ **Do not touch `verify-local.sh` or `build-and-upload.sh`** -- the consumer stays as it is; only the recorder changes.
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

RS-1..RS-4 + the four falsifier arms as ONE message (each arm's rc, the stamped counts, the census line) to the issuer + CTO + CVO; the proof at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
