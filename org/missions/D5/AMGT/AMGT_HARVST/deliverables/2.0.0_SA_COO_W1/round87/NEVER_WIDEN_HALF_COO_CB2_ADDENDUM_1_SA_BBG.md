# NEVER-WIDEN -- COO HALF, ADDENDUM 1: `sa` and `bbg` join the dell1 harvest runner (`HVST-cb-7`, round 87, workstream RUNNER-REGISTER)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-15 ~20:2xZ. **Extends:** the COO half `NEVER_WIDEN_HALF_COO_CB2_DELL1_RUNNER.md` @5271f99a66 (sha256 `167561c1...d50b`), whose "does not cover" and the CTO half's CANNOT both name `bbg`, `sa`, `ft`: "they join by a re-registration under their own addendum, each after its local proof". **Pairs with:** a CTO addendum 1 (owed).
**Authority:** Andrew-direct 2026-10-15 ~16:3xZ ("including Seeking Alpha + Bloomberg as well"); CTO addenda 3 and 4.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, AFTER `HVST-cb-2`'s +15 minute reads are TRUE: at a cycle boundary by the runner's own stop file (no kill), re-register the one task from the SAME pin and state with `-Publishers wsj,barrons,sa,bbg` (the `-Plan` read first), the same flags, start once, with the same reads at +3 and +15 minutes and the same rollback. Nothing else changes.

## THE NEW THINGS THIS ADDS (named)

- **Two more publishers' production rows change writer from site Z to dell1:** `sa` and `bbg`. Site Z's task is Disabled (formal read-back, `ledger/SITE_Z_RETIRE_READBACK_20261015.md`); site Z's `sa` wrote until about 18:25Z (its own record corrects the "stored 0 since 14:02Z" premise), so the S3 LastModified read of `HVST-cb-2` 1.c applies to the `sa` and `bbg` prefixes too and must be made again at this act.
- **`sa` is held by a PERSON's sign-in, not a script.** Its profile `browser-profiles/sa` was signed in by Andrew at 20:1xZ; `verification.ACCOUNT_CHECKS` has no `sa`, so `--refresh-once` cannot renew it, and the bundle refresh that exists writes a store the tab never reads. When the session expires, every `sa` job ends `sign_in_refused` (class `expired`) and the cycle stops `sa`'s leg: **a recorded finding, not a repair; Andrew signs in again** (the script `sa_profile_login.py` pattern). The runner never signs `sa` in, and never reaches the Kimi-VL authenticator or the Google credential.
- **`bbg` runs on a Secrets session captured 2026-09-11** and met a Press and Hold challenge in 1 of 3 local jobs; the in-profile solve (`verification.solve`) handles it. Its sign-in path is Google OAuth for `google/andrew-goldengate/credentials`, which the driver's `--refresh-once` NEVER reaches (`REFRESH_PUBLISHERS` is `wsj`, `barrons` only: HVST-bz-12); a `bbg` refusal as expired is recorded, never refreshed. A challenge in a MINIMISED window is unmeasured (1 `TargetClosedError`, 1 success with the minimise off, 1 success with no challenge).
- **Order inside a pass** (`cycle_runner.PUBLISHERS`): `bbg`, `wsj`, `barrons`, `sa`; a stop status ends THAT publisher's cycle at its first refused pair and the runner goes on to the next publisher (as read at site Z in round 85: "the runner keeps cycling, each publisher stops at its first refused pair").

## BLAST RADIUS

- **Writers of the property N = 1 per publisher** once site Z is Disabled and the S3 read shows no site Z write after 19:04:24Z (C-b of the first half, repeated for these two prefixes).
- **What it touches in the world:** vendor requests to `seekingalpha.com` and `bloomberg.com`; S3 writes of bronze and silver for those two publishers; minimised Chrome windows on dell1's desktop; NO sign-in by the runner for either publisher.
- **Not touched:** `ft`, the Google credential, the Kimi key, the portal, gold, any firm bucket.
- **Served output moved:** yes, the `sa` and `bbg` rows that feed `AMGT_RESAPP`'s Chatter axis and news.

## BOTH BRANCHES

- **Branch D:** each of `sa` and `bbg` ends a leg with accepted > 0 and the E2 line (`s3_get_count`, `s3_get_bytes`) in its cycle record; the issuer reports it as `HVST-cb-6` does for `wsj` and `barrons`.
- **Branch F (a refusal as expired for `sa` or `bbg`, or `bot_check`/`TargetClosedError` at a challenge):** NO sign-in by any hand but a person for `sa`; one row (publisher, class, job id) and the question returns to the issuer; the task stays registered and the other publishers' legs go on.

## CONDITIONS

- **C-a1.** The first half's conditions hold again at this act (pin ancestry, both halves and this addendum SIGNED, site Z's Disabled read-back on file, the S3 read repeated for `sa` and `bbg`).
- **C-b1.** `HVST-cb-2`'s +15 minute reads are written and TRUE, and no `REFRESH ... FAILED` or double refusal is on file.
- **C-c1.** The `sa` profile still reads signed in: the `sa` account check (`auth_check`, 200) is read just before the re-registration; if it reads logged out, `sa` is left out of the list and Andrew is asked.

## ROLLBACK

Re-register from the same pin with `-Publishers wsj,barrons` (the first half's list), same flags, start once; or the first half's stop-file and `Disable-ScheduledTask` rollback. Rows written for `sa` or `bbg` are append-only and stay; the watermark follows the writer.

## WHAT THIS ADDENDUM DOES NOT COVER

- `ft`; any sign-in made by the runner for `sa` or `bbg`; the Google credential; the Kimi key; an in-profile sign-in for `sa` (a candidate cell for a later round); a headless transport.

## VERDICT: SIGNED (COO). Not started until the CTO addendum 1 is on file and C-b1 reads true.
