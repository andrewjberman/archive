# Base Terraform plans of the three lambda-source-map roots (read-only), run by 2.0.0_SA_COO~C at 2026-10-16T16:30:19Z on the laptop at HEAD ca239c0486
# command per root: TF_DATA_DIR=<scratch> terraform -chdir=<root> init -input=false; terraform -chdir=<root> plan -input=false -lock=false -no-color -detailed-exitcode (never an apply; no state lock taken)
# purpose: the merge check of CT-ca-1 is the after-plan on the cell's branch IDENTICAL to this base plan (a root with a standing change at the base is not 'zero').

## account-return-daily (finished)
64:  # module.irpt_account_return_daily.aws_lambda_function.this will be updated in-place
82:Plan: 0 to add, 1 to change, 0 to destroy.
88:== account-return-daily plan rc=2 2026-10-16T16:26:28Z

## reporting-gold-iso (finished)
58:No changes. Your infrastructure matches the configuration.
plan rc=0 (16:30:35Z)

## reporting-publish-iso (finished)
58:No changes. Your infrastructure matches the configuration.
plan rc=0 (16:31:48Z)

## Reading
Two roots are clean at the base (rc 0, No changes); `account-return-daily` carries one standing in-place update on `module.irpt_account_return_daily.aws_lambda_function.this` (rc 2). The after-plan on `CT-ca-1`'s branch must read: gold-iso rc 0 No changes, publish-iso rc 0 No changes, account-return-daily the SAME one in-place update with the same changed attributes (the full base text is kept in the issuer's scratch and re-run at the merge).
