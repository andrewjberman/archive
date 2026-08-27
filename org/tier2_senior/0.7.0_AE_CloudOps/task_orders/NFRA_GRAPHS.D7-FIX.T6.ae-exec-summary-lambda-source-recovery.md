<to_id>NFRA_GRAPHS.D7-FIX.T6</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T6 — exec_summary_generator Lambda source recovery (.py absent from repo, only __pycache__ present)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (D7-FIX.T4 DS surface flag, ~170000Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_GRAPHS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<priority>low — nightly Lambda is running (exec_summary.json being produced); source absence is a hygiene/maintenance gap, not production breakage</priority>

<scope>
D7-FIX.T4 DS investigation surfaced: `infra/aws/lambda/exec-summary-generator/exec_summary/` contains only `__pycache__` (compiled .pyc) — no `.py` source files present in the working tree. The exec_summary_generator Lambda is a production nightly batch artifact producer writing `platinum/advisors/{id}/exec_summary.json` (consumed by portal advisor-intelligence.ts, confirmed at :1352 "nightly batch artifact").

Without the .py source in the repo:
- Code changes to exec_summary logic require locating the source outside normal repo workflow
- Terraform deployment (Rule 1: TF is the only Lambda deployment mechanism) cannot update the Lambda code from the repo
- Source-level review (comp-pipescript, ds-commit-gate, owned-paths) is structurally impossible

Investigation steps:
1. `aws lambda get-function --function-name exec_summary_generator` — download the current deployment package; extract and recover the .py source
2. Determine source-absence root cause: .gitignored? Deployed directly to AWS without committing? Never added to repo? Check git log for infra/aws/lambda/exec-summary-generator/ history
3. Add recovered .py source to `infra/aws/lambda/exec-summary-generator/exec_summary/` + commit
4. Verify Terraform `.tf` resource points to the recoverable source (source_code_hash / filename configured correctly); if not, fix the resource block
5. Run `python -m py_compile` + `ruff check --target-version py39` on recovered source (Rule 14)

Acceptance:
- `infra/aws/lambda/exec-summary-generator/exec_summary/*.py` present and committed
- Terraform wired to deploy from repo source
- `python -m py_compile` clean on recovered source
- RAVC2 to COO with root-cause note (how did source go missing?)

Companion: T5 item-2 (Lambda producer ingestion into comp-platinum graph) depends on knowing this Lambda is real and in-repo — coordinate with T5.
</scope>
