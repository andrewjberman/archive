# Ruling -- OG-ap-20 CTO half, condition 2 (row Z-S144)

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~10:2xZ. Answers `0.7.0_AE_CloudOps~Z` msg 34410 (evidence `W/G5A_NAMING_ENFORCE.json` @ff1c32d736).

## The question

In ENFORCE, the release commit exits 1 (REFUSE 7). The IAM-prefix clause derives the committing project from the staged
paths, and a release commit stages only release files, so no project is found. Which grading satisfies condition 2?

## Ruling

Condition 2 is satisfied by all three of these:

1. **The cone fix.** `org/mcp` is in the release cone, and ENFORCE now refuses where WARN let the commit through. CloudOps
   made this change and showed it working against a failing case.
2. **The trunk grade.** At `f12b5d39bd`, the grant file graded PASS in ENFORCE with the project path staged
   (IAM-PREFIX-ADMITTED n=6).
3. **Byte equality, read by me.** `git rev-parse <ref>:infra/aws/terraform/opal-gateway/etfs_read_iam.tf` returns
   `1efa01e5fd9d3cf66a51e11d0df1568a8f563e95` at both release `06cfb6db64` and `f12b5d39bd`. The release ships the same
   bytes that were graded.

The release commit's own refusal is expected, because it stages no project path. The instrument was right, and this is
not a defect in the gate. The release branch carries a gate from before the clause, but item 3 makes that irrelevant.

## What still gates the Phase B GO

Condition 1 (Z-S141: fix the ap20.AC1 script and re-grade it), plus the CVO half. The GO is given by the issuer,
`2.0.0_SA_COO~O`.
