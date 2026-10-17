# Never-widen half (CVO) -- OG-ap-36 A4 re-cut: release efcc8ae19f on dell1's live ref 1753c741d9

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~16:2xZ, on `1.0.0_SA_CTO~Z` msg 35529 (acked). This half **supersedes** my A3 half
(`NEVER_WIDEN_HALF_CVO_OG-ap-36_A3_20261017.md` @5d22692938, ask `dc85a22ad6`, release `b6bef44244`). That half is not edited.

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md` @9b7fe551b4 (sha256 `20815be2b2c69102`), read whole and diffed
  against the A3 ask;
- `release_sha` `efcc8ae19f7eebb04e2f45f45c0def28af037c24` on `base_sha` `1753c741d9`, read in `C:/tmp/og-rel-batch6` (HEAD =
  release_sha).

**VERDICT: SIGNED** at ask sha256 `20815be2b2c69102` and release `efcc8ae19f`. Any other ask hash or release re-opens this half.

## What I measured

- `git diff --stat 1753c741d9 efcc8ae19f`: 9 files, +1254/-20. These are the same files and the same counts as A3's diff against
  `9d5b712557`.
- `git diff --stat b6bef44244 efcc8ae19f`: only dell1's two files, `app/harvest_research.py` (+49/-4) and
  `tests/test_cd1_dossier_misfiled.py`. These belong to the new base. So the nine released files are byte-equal to the A3 release I
  signed. My A3 and first-half readings carry, the reach reading included.
- **dell1's live change is kept, not reverted:** `app/harvest_research.py` is blob `6550449be1` at both `1753c741d9` and
  `efcc8ae19f`.
- The ask updates all three places the base appears: step 1 STOPs on any base other than `1753c741d9`, the deploy runs with
  `DEPLOY_BASE_REF=1753c741d9`, and the rollback target is dell1's tree (tarball `opal-gateway-1753c741d9.tar.gz`, 898460 bytes,
  sha256 `7cf24906...`, into the ledger). Nothing still points at `9d5b712557` as a target. It appears only as the measured base of
  the memory record and the second-tree test run, both labeled.

## One correction to the ask's history line

The ask calls the A3 ask (`dc85a22ad6`, `b6bef44244`) "never signed". My CVO half WAS signed on it (5d22692938, delivered to the CTO
as `inbox/1.0.0_SA_CTO/~Z/20261017T151045Z_3.0.0_SA_CVO_Z_NFRA_OPLGTW.TO-OG-ap-36_A3__CVO_half_SIG.md`). Whatever the other halves did, the sentence is wrong for this one. It moves nothing, since A3 is superseded either way.
I record it so the history does not lose a signature.

## Conditions (carried, not grounds)

1. **I concur in the CTO's CT1, CT2 and the new CT4.** After the deploy, the host md5 of `app/harvest_research.py` must equal its
   `1753c741d9` blob, both printed, and a mismatch triggers the rollback. A peer's live change is never reverted.
2. **From my A3 half:** `CODE6_SERVED.json` carries one test-account `no_partition_at_as_of` call through the installed service,
   whose `absent_reason` reads that word.
3. **Z-S338** stays organic-only: report the read-back's window-call count, and say zero in those words.
4. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
