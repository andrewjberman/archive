# OG-h-1 item A -- NOT LANDED: the naming gate refuses the renormalized DATA_CATALOG.yaml (row Z-W13-S5)

The edit was made and measured, then withheld from the commit. Nothing here is an override.

## The block that was written (to append to `/.gitattributes`)

```
# opal-gateway shipped text (row NFRA_OPLGTW-W2-S8): a deploy from a Windows worktree with core.autocrlf=true shipped
# 9 of 68 files as CRLF, each an extension with no eol rule. Scoped to the gateway tree only -- never a repo-wide glob.
infra/aws/ec2/opal-gateway/**/*.service text eol=lf
infra/aws/ec2/opal-gateway/**/*.txt text eol=lf
infra/aws/ec2/opal-gateway/**/*.yaml text eol=lf
infra/aws/ec2/opal-gateway/**/*.json text eol=lf
infra/aws/ec2/opal-gateway/**/*.md text eol=lf
infra/aws/ec2/opal-gateway/**/*.html text eol=lf
infra/aws/ec2/opal-gateway/**/*.jsonl text eol=lf
```

With it applied, `git ls-files infra/aws/ec2/opal-gateway | grep -E '\.(service|txt|yaml|json|md|html|jsonl)$' | git check-attr --stdin eol`
read `eol: lf` on 41 of 41, and `git add --renormalize infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` moved that file's index
entry from `i/crlf` to `i/lf` (1,404 lines changed, line endings only; it was the only `i/crlf` file of the 41).

## Why it did not land

`safe-commit.sh` aborted the commit ("BLOCKED -- the naming limb refused (LGIC_ENFORCE DEC-6, ENFORCE mode)") with 16 `NAMING REFUSE`
findings, all in `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` (lines 632, 637, 648, 661, 672, 684, 695, 707, 718, 730, 740,
752, 763, 775, 818, 1304). Each is an S3 key pattern already in the file (for example `platinum/mdpf/{scope}/aum-metrics.json`), reported as
"EXISTING and OUT-OF-PATTERN ... assigned to the live remediation MDPF_CANON: REFUSE unless the diff removes it". A line-ending renormalize
rewrites every line, so each of those lines reads as added. Renaming them is MDPF_CANON's remediation, not this cell's.

## Why `.gitattributes` alone was not landed

With the rule in `.gitattributes` and DATA_CATALOG.yaml still stored CRLF, `git status` reads that file as modified (` M`) in every worktree
until it is renormalized. Landing the rule alone would put a phantom modification on CLOUD's tracked tree. So both edits were held back and the
worktree's `.gitattributes` restored by hand to the committed bytes.

## What the issuer decides

Either the naming limb is cleared for this one line-ending-only diff by whoever owns that gate, or DATA_CATALOG.yaml's renormalization is
landed by a seat the gate admits. Then apply the block above and run `git add --renormalize` on that one path in one commit. The hazard
W2-S8 (a Gateway release from a Windows worktree ships CRLF text) stays ARMED until then. `hy.AC1` reads FAIL until then: 41 files, attr eol=lf
on all but 41, stored CRLF 1.
