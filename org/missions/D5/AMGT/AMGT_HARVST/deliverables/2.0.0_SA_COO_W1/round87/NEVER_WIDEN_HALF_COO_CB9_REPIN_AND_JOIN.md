# NEVER-WIDEN -- COO HALF, ADDENDUM 2: one re-registration of the dell1 harvest runner -- re-pin to a head carrying `HVST-cb-8`, delete the seeded session copies, and `sa` and `bbg` join (`HVST-cb-9` + `HVST-cb-7`, round 87, workstream RUNNER-REREGISTER)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-15 ~20:5xZ. **Extends:** the COO half `NEVER_WIDEN_HALF_COO_CB2_DELL1_RUNNER.md` @5271f99a66 and its addendum 1 `NEVER_WIDEN_HALF_COO_CB2_ADDENDUM_1_SA_BBG.md` (sha256 `0f811a062934a228436461b93ac1cdd8b405dc82ed82709806f6b4abf3ecc165`, CTO addendum `ledger/NEVER_WIDEN_ROUND87_CB2_CTO_HALF_ADDENDUM_1_SA_BBG.md` @4e7a011829), and the CTO's bound on the seeded copies (msg 6216). The erratum applies throughout: the bucket is `opal-data-harvest`. **Pairs with:** a CTO addendum 2 (owed).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, AFTER the first complete cycle of BOTH `wsj` and `barrons` has ended (so the first productive cycle's record, with its E2 line, exists first): at a stop-file boundary (never a kill), re-register the ONE task from a NEW locked pin `Q` (the head of `box/dell1` at the act, carrying `a879d12881`, the cb-8 merge) with `-Publishers wsj,barrons,sa,bbg`, the same state dir, runtime root, flags (`-Windowless -RefreshOnce`) and stop file, `-Plan` read first, start once, the same reads at +3 and +15 minutes, the same rollback. Then DELETE the two seeded `.dpapi` copies in `<runtime>\secrets\` (the CTO's bound: they exist only until cb-8 reaches the runner), and read the first pass for a `wsj` job whose run record carries `token_source` `browser_profile`.

## WHAT THIS ADDS (named)

- **The runner's code changes under it:** `TokenFirstSessions.get()` returns a profile-store envelope (no refresh, no stored bundle) for a publisher whose contract is tab, `seed_from_bundle` false and that has an account check (`wsj`, `barrons`). That is what makes deleting the seed safe; it is graded by the cb-8 tests (AC1 9 passed, AC2 144 passed) and by the first pass's run records, NOT by a real job before this act (the production runner holds the profiles, and a second Chrome on a profile in use would collide with it).
- **`sa` and `bbg` start writing** (addendum 1, unchanged): two more publishers' production rows change writer from site Z to dell1; `sa` rides a person's sign-in (its expiry is a finding, never a repair), `bbg` rides the 2026-09-11 Secrets session and is never refreshed; CTO conditions C-i (done: `ledger/CTO_CONDITION_C-i_BLOOMBERG_READ_HERE_20261015.md` @576cfb1e47), C-j (two `bbg` legs ending `bot_check` or `TargetClosedError` drop `bbg` by re-registration, finding to the CTO), C-k (the S3 read repeated for the `sa` and `bbg` prefixes, no site Z write after 19:04:24Z).
- **The runner stops once more** (a stop-file boundary), losing at most the one in-flight pair, re-queued from the same state dir.

## BLAST RADIUS

- **Writers of the property N = 1 per publisher**, as before. The task registration is written by `install-cycle-schedule.ps1` and by nothing else on dell1.
- **What it touches in the world:** the same vendor requests and S3 writes as the first half, now for four publishers; the deletion of two files that are copies of encrypted local sessions (DPAPI, user `Test`, never printed or moved).
- **Not touched:** `ft`; the Google credential; the Kimi key; the portal; gold; any firm bucket; the main tree's code.
- **Served output moved:** `sa` and `bbg` rows change writer (as addendum 1); `wsj` and `barrons` do not change writer.

## BOTH BRANCHES

- **Branch D (the first pass after the re-pin runs, the wsj job's `token_source` reads `browser_profile`):** the seed is gone, the runner no longer needs any saved bundle, and the first productive cycle per publisher is reported (`HVST-cb-6`).
- **Branch F (a `wsj` or `barrons` job after the re-pin ends `sign_in_refused` with `token_source` None, or any job fails that passed at the seeded pin):** restore the two copies from the main tree's `secrets\` (a copy within one box and one user), re-register from the PREVIOUS pin with the previous publisher list, file one row, and tell the issuer. The previous pin stays locked until `HVST-cb-6` is closed.
- **Branch X (an account stop rule fires):** as the first half: no second attempt by any hand; one row.

## CONDITIONS

- **C-a2.** All of the first half's and addendum 1's conditions hold again at this act (pin ancestry including `a879d12881`, halves SIGNED at their pins, site Z's Disabled read-back, the S3 read for ALL FOUR prefixes with none written after 19:04:24Z by site Z, `sa` profile still reads signed in).
- **C-b2.** At least one `wsj` cycle record and one `barrons` cycle record exist under the CURRENT pin with `s3_get_count` and `s3_get_bytes` (CTO C-h); if the cycles have not ended when the executor reads, the act does not start.
- **C-c2.** The seeded copies are deleted ONLY after the first job of the new pass has read `token_source` `browser_profile` for `wsj`; if it has not, the copies stay and Branch F applies.

## ROLLBACK

As the first half and addendum 1; plus the copy restore of Branch F. Rows written by `sa` and `bbg` are append-only and stay; the watermark follows the writer.

## WHAT THIS ADDENDUM DOES NOT COVER

- `ft`; any sign-in made by the runner for `sa` or `bbg`; the Google credential; the Kimi key; an in-profile sign-in for `sa`; a challenge repair on a profile-store publisher outside the runner (rows `AMGT_HARVST-D1-W145-S1`, `-S2`, residual named in `D1-S21`).

## VERDICT: SIGNED (COO). Not started until the CTO addendum 2 is on file and C-a2 and C-b2 read true.
