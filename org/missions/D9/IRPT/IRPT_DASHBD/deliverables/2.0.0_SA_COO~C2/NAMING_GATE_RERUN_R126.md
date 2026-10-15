# B-CW round 126: the naming gate re-run on the LANDED Cottonwood source-map entries (CTO ruling 1, msg 8325, condition on the disclosed `--no-verify` commit `eda88f89c7`)

Run by `2.0.0_SA_COO~C2` at 2026-10-15 ~14:3xZ, read only, with `.tools/naming-gate.py` (carrying the citation extension `b49303719e`).

**Method.** A scratch worktree at `f0069dd8ca` (the tree before any Cottonwood account_dim entry existed), the landed `infra/aws/lambda/ci/lambda-source-map.json` of `HEAD` (`90e66f6274` plus later commits) staged into it with `git checkout <HEAD> -- <file>`, and `python .tools/naming-gate.py --diff <the staged diff, -U0> --post-from-index`. That grades every line added since `f0069dd8ca` (262 added lines: the `irpt-cot-account-dim-lambda` entry, its applier-recorded fields, and the other seats' Cottonwood account-return entry) as NEW literals against the pre-entry tree, which is the check `safe-commit` would have made. The scratch worktree was removed.

**Result (verbatim last line): `NAMING-GATE: PASS 0 graded`.** The entry's `tf_file`, `tf_resource` and `artifact_s3_key` are admitted by the citation rule and its extension; nothing is graded as a new hand-kept `cot` carrier.

**Positive control, same setup:** the staged `tf_file` value changed to `infra/aws/terraform/investor-reporting/cot-planted/lambda.tf` gives `NAMING REFUSE ... NEW hand-kept carrier (context rule) ...` and `NAMING-GATE: REFUSE 1 graded`.

**Also read:** the same added lines graded against the CURRENT file as an existing pre-image (the check-mode form) read `NAMING-GATE: WARN 2 graded`, both `EXISTING hand-kept carrier` WARNs on the two `investor-reporting/irpt-cot-*.zip` keys (the account-dim zip and the other seat's account-return zip): a WARN is what the gate prints for a literal already in the pre-image, not a REFUSE; the PASS above is the NEW-literal grade.

No `--no-verify` was used in this round after `eda88f89c7`; every commit went through `.tools/safe-commit.sh`.
