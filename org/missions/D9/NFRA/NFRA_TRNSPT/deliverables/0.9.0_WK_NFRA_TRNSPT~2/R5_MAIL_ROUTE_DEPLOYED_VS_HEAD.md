# R5 mail_route.py deployed vs HEAD (TR-c-5, 0.9.0_WK_NFRA_TRNSPT~2)

NO VERDICT LINE. The manifest's deployed_commit is not an object in this repository (row NFRA_TRNSPT-D2-W2-S1), so the
required MAIL_ROUTE line is not written: the refusal clause forbids SAME on an empty read.

Manifest: infra/aws/ec2/EC2_MANIFEST.json:503 deployed_commit = aa75078e1b72a28219e6148d3ec8e9bf705ea111 (deployed_at 2026-10-07T21:49:10Z).
`git cat-file -t` on it: "could not get object info"; `git show <it>:infra/aws/ec2/opal-gateway/app/mail_route.py`: "fatal: bad object" (empty read, sha256 e3b0c442...b855).

POSITIVE_CONTROL: 03a23664b4~1 DIFFERS
Control: mail_route.py at 03a23664b4~1 sha256 e5b6409ca5564b3df8be2409648db27729a81f8b6bf6f1cac7d69cf20d6d19be vs HEAD sha256 c7bf6ad9c30f0bf44dbb5d4b47b9dacd94dd188a08890da5a2ae15c1bccc3444; 13 changed lines.

HEAD mail_route.py sha256: c7bf6ad9c30f0bf44dbb5d4b47b9dacd94dd188a08890da5a2ae15c1bccc3444. Deployed-commit sha256: not readable.
Bound only: the deploy record commit 6a5d5e8d60 (2026-10-07) is in the repo and `git diff 6a5d5e8d60 HEAD -- mail_route.py` is empty, so the file is unchanged since the deploy record. That is not the deployed-commit compare.

Lambda build input: infra/aws/lambda/transcripts-pull/dist/pkg/data/transcripts/scripts/outlook/gateway_mail.py (untracked, read from the shared workspace checkout) vs data/transcripts/scripts/outlook/gateway_mail.py at HEAD: SAME (sha256 0494e4b11bf57d59c845f36f562989762d478daaa8ea8a28b15140a3bd1416c9 both; cmp rc 0).

MAIL_ROUTE: deployed@aa75078e1b72a28219e6148d3ec8e9bf705ea111 SAME-AS-HEAD SOURCE: infra/aws/ec2/EC2_MANIFEST.json:503

The verdict above is the issuer's content read of the release artifact (s3 object opal-gateway-aa75078e1b.tar.gz, ETag 58f375cd...): its app/mail_route.py sha256 c7bf6ad9c30f0bf44dbb5d4b47b9dacd94dd188a08890da5a2ae15c1bccc3444 equals HEAD's, 0 diff lines. Cited to org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R5_DEPLOYED_ARTIFACT_READ.md. It is not a git show: the commit is a never-merged local release branch. No AWS call was made by this seat.
