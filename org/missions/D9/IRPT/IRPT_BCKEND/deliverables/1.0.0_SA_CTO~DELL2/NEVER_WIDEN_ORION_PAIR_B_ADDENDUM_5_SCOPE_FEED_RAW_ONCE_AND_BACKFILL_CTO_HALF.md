# CTO half -- Orion pair (b) ADDENDUM 5: the Scope feed writes the raw replies once per run, and the history backfill

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~14:1xZ.

**Addendum:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL.md`.
I re-measured it: blob `619dbf431bc578cf22bb59114f5e289d7f9c4c94`, equal at 5c163df336 and in the working tree; sha256
`a343d3da11a97704c6822cff71049a94b3d0693fef925d5a1ed46179f2671616`; 9,177 bytes. COO half: `~N2` msg 10704. Applier:
`0.7.0_AE_CloudOps~IB2`.

**SIGNED, with the conditions below.**

## Read at signing

- `data/inf/manual_api/pull_inflection_scope_account_returns.py` at HEAD is blob `b3bcc5e55afd`, sha256 `acfe390bda5a`,
  equal to section 1. IB-pn-5's merge `d281b8b32c` is in HEAD.
- `run_object_address` (`:463`) builds the run object's address with `lib/opal_naming` `address()` when the builder
  imports, and is content-addressed by sha256 (Rule 30). This is the shape I ruled at @2f780e14a6: raw replies once,
  unchanged, and day envelopes that carry the key and sha256.
- The measured N is 2,326 days from 2020-06-03, with 294 households (IB2 @c438e1f1a6), within the script's 4,000-day bound.

## Blast radius (section 5, accepted as read)

- **The apply:** one S3 code object, saved first; Branch B restores it. There is no dispatch change.
- **Every run after the apply:** one new key under the new `run=<pull_date>/` prefix, plus the existing `date=` keys.
- **The backfill:** one run object, 2,326 v2 envelopes and 2,326 silver objects, all new keys; existing days are skipped.
- **Served values changed: none.** No reader of the feed exists until the adapter is cut, and no window is named readable
  by this run.
- **Rollback:** the script by Branch B. Removing a written feed key is Andrew's act; nothing waits on it.

## The two proposals

1. **Confirmed:** the backfill waits for a clean first scheduled run of the new writer, read from the STEP LOG.
2. **Confirmed:** the apply and the backfill run outside the weekday 11:30Z to 14:15Z band, and never on Tuesday
   2026-10-20, which is the Inflection pair's day. They never run alongside another IB2 act.

## Conditions (in addition to sections 3 to 5)

1. **Memory is the risk this addendum leaves inferred.** The 294 full-window replies are about 337 MB of JSON, held parsed
   once. The backfill's run record prints peak memory against the host's limit. A failure is a STOP and a row, never a
   raised limit or a split run under this pair.
2. **The run object's address is printed from `address()` at the apply's smoke.** A fallback to the sidecar path, because
   the builder did not import on the runner, is printed as such. It is acceptable only if its partition and object name
   equal the builder's.
3. **The tolerance check** (at least 5 accounts, windows of 237 days or less, 0.5 bp) is printed per account with its
   window. A miss is a STOP before any window is named readable.
4. **Section 6 is noted:** the dispatch tolerating a failed pull step (row W404-S9) stays outside this pair.
