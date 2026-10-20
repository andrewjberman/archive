# NEVER-WIDEN -- COO ADDENDUM 1 to the `HVST-co-7` pair: the image digest the run half is bound to

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-20 ~23:4xZ. **Binds:** the COO half `ledger/NEVER_WIDEN_CO7_GOLD_REBUILD_DELIBERATE_RUN_COO_HALF.md` (sha256 `f05b443bc4bfe87fca8a4d6a3889c1fe94788675b73ee491520601d17c3cd2a4`, `5c42df7141`) and the CTO half `ledger/NEVER_WIDEN_CO7_GOLD_REBUILD_DELIBERATE_RUN_CTO_HALF.md` (`d9bedbcbff`), condition 2: the digest is bound by an addendum at the stage it becomes known, countersigned by the CTO.

## WHAT THIS ADDENDUM BINDS

- **Image digest:** `sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74`, repository `amgt-gold-refresh-repo`, tag `git-9e26b79f7edf`, size 286233455 bytes (286.23 MB), pushed 2026-10-20 23:25Z by CodeBuild run `amgt-gold-refresh-build:73b870ef-9b06-4701-afa1-c775435020af` (SUCCEEDED, smoke step passed).
- **Two routes agree, and I read the second myself.** Route 1: the build log's `IMAGE_DIGEST=` line (line 336 of `co7_s2.out`). Route 2: `aws ecr describe-images --repository-name amgt-gold-refresh-repo` read by me at ~23:40Z: ONE image in the repository, the same digest, the same tag, the same size.
- **The source is the pinned source.** The build commit `9e26b79f7e` is `db8895e57f` plus the seat's ledger files only; the diff over the zip sources is 0 files (stated by the seat in `co7_s2.out`, line 1; evidence on the seat's branch `wk-co7-gold-apply` @9e858b8e81, LOCAL, path `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~SC1/round100/co7/co7_s2.out`).
- **The run half is applied with exactly this digest** (`-var gold_refresh_image_digest=sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74`); the task definition names the image by digest, never a tag. A different digest (a rebuild, a new tag) voids this addendum and needs a new one.

## WHAT I READ AND DO NOT CLAIM

- The ECR scan on push reports HIGH 12, MEDIUM 20, LOW 5, UNDEFINED 1 findings. The order lists a scan finding as printed, not a stop; I have not triaged them and this addendum does not say they are harmless. They are a base-image and requirements matter for a later cell.
- Task families pulling the repository: 0 today, 1 after stage 3 (`amgt-gold-refresh-task`), the number the order asked the seat to print.

## WHAT IT DOES NOT CHANGE

The property (the newest snapshot of each of the three tables), its N=2 writers and three `write_gold` calls, the three added objects, both branches, the per-key rollback (an S3 delete, Andrew's word, carded by the CTO), the task role's `PutObject` only under the three gold prefixes with no delete, the schedule DISABLED, the dry canary with no `--write`, and the one `--write` run (its date and as_of are ADDENDUM 2). Stage 3 applies the run half; it writes no gold object.

## VERDICT: SIGNED (COO addendum 1). Stage 3 starts on my message after the CTO's countersignature is on file.
