# Holes owned elsewhere -- round 10, cell BF-y-3 (0.9.0_WK_LGIC_BLANKFIX~2)

`check_held_entries_round10.py` reads the lines that begin `OWNED ` in this file and fails if one does not match a HOLE left on a
newly mapped root, or if a HOLE left on a newly mapped root has none. The seven entries of `MAP_ENTRIES_round10.json` open 48 HOLE lines
on the roots they map (shared-infra 14, astn-pipeline 19, mdpf-pipeline 9, etfs-reports 3, etfs-netassets 3; etfs-canon and harvest 0).
After the 41 rows of `REGISTRY_ROWS_round10.json` (19 key rulings, 21 name rulings, 1 event rule) are applied to a copy of the
registry, six HOLE lines remain (astn-pipeline 1, etfs-reports 1, mdpf-pipeline 1, shared-infra 3), each below with its owner. None is a
cadence-reader defect: the one cadence line (`mdpf-feeder-accelerator`) is filled by an event-rule row.

**Owner `1.0.0_SA_CTO` -- the key reader reads the wrong bucket (4 holes; a row is drafted for three of them, and the fourth is
answered by a row already in the registry).** `lib/opal_naming_keyfill.py` `bucket_of` returns the bucket a stored-file path
is used with. For these four paths it returns another bucket than the one the code uses, and `_ruling_of` drops a candidate row whose
bucket differs from the bucket the reader read ("a candidate must also agree on the bucket wherever the item's bucket is known"). So a
correct row never matches. What the CTO owes: `bucket_of` must read the bucket of (a) an `s3://<bucket>/<key>` URI constant and (b) a
bucket constant that does not begin `opal-data-` (`opal-313476888478-globgrph`, `opal-313476888478-lambda-artifacts`). Today it
reads "the file's only bucket literal" in the file: `opal-data-astn` and `opal-data-etfs` for the two `ec2/` paths, `opal-data-portal-v2` for the two globgrph paths. Once it reads
the true bucket, the drafted rows match with no further act by the registry owner. Row `LGIC_BLANKFIX-D1-W2-S4` records this.

**Owner `4.0.0_SA_CRO` -- two holes the registry owner alone can close.** (1) `mdpf-pipeline` `gold/meta/pipeline-complete.json`:
the registry already holds the row for it (bucket `opal-data-inf`, canonical `orion/inflection/state/gold-pipeline-complete.json`). The
mdpf-daily-trigger Lambda picks its bucket from an environment variable (`INF_BUCKET`), the reader finds five bucket candidates and
none for the key, so the row does not match. A second row for the same (bucket, key) is refused (unique per pair), so the one act is to
add `infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py` to that row's `declared_in`. (2) `shared-infra`
`restricted-prefix-get-put-list`, an inline policy: the grader raises "R1.f: 'restricted' is in no vocabulary". Which word the
registry takes for it (a vocabulary row, or a name-ruling row once the word is decided) is the registry owner's call; the policy sits
on the break-glass role of the firm buckets (`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:262`), a cross-firm break-glass
that this cell did not read to a system.

OWNED astn-pipeline || S3Key ec2/astn-wsjft/deploy.sh || 1.0.0_SA_CTO || bucket_of reads opal-data-astn (the file's only opal-data literal); the code's bucket is opal-313476888478-lambda-artifacts, in an s3:// URI constant (infra/aws/lambda/astn-wsjft-orchestrator/lambda_function.py:61); the none_owed row for (opal-313476888478-lambda-artifacts, ec2/astn-wsjft/deploy.sh) is drafted and is dropped on the bucket mismatch
OWNED etfs-reports || S3Key ec2/etfs-reports || 1.0.0_SA_CTO || bucket_of reads opal-data-etfs; the code's bucket is opal-313476888478-lambda-artifacts, in an s3:// URI constant (infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:53); the canonical row for (opal-313476888478-lambda-artifacts, ec2/etfs-reports) is drafted and is dropped on the bucket mismatch
OWNED shared-infra || S3Key contract_integrity/latest.json || 1.0.0_SA_CTO || bucket_of reads opal-data-portal-v2; the code's bucket is GLOBGRPH_BUCKET = opal-313476888478-globgrph, a constant bucket_of does not recognise (infra/aws/lambda/infrastructure_monitor/lambda_function.py:127); the canonical row for (opal-313476888478-globgrph, contract_integrity/latest.json) is drafted and is dropped on the bucket mismatch
OWNED shared-infra || S3Key warehouse/_branch_head.main.json || 1.0.0_SA_CTO || same reader defect (infra/aws/lambda/infrastructure_monitor/lambda_function.py:124): the registry's row for (opal-313476888478-globgrph, warehouse/_branch_head.main.json) is the only candidate for the key and matches whatever its declared_in once the bucket is read as globgrph
OWNED mdpf-pipeline || S3Key gold/meta/pipeline-complete.json || 4.0.0_SA_CRO || add infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py to declared_in of the existing row (opal-data-inf, gold/meta/pipeline-complete.json); the bucket is an environment variable here (infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:53)
OWNED shared-infra || IAM_POLICY restricted-prefix-get-put-list || 4.0.0_SA_CRO || a vocabulary decision for the word 'restricted' (R1.f), or a name-ruling row once the registry owner has decided it (infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:262)
