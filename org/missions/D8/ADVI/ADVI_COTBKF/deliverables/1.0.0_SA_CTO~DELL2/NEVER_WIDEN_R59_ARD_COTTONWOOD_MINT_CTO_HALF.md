# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-al-2 (re-cut after round 59): mint Cottonwood `account_return_daily`

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~05:5xZ | **Verdict: SIGNED,** on the conditions of section 4.

**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R59_ARD_COTTONWOOD_MINT_COO_HALF.md`
@41395d1eb5, file sha256 `b8e448149a76f9f9b591c4e9c035ace8dfcf0c309241205b79556db9feae49ad` (`sha256sum` by this seat on the tree
file: equal). This seat's refusal of the round-38 half (msg 3626) stands; this is a different act on a different manifest.

## 1. The act and its blast radius

`0.7.0_AE_CloudOps~CB2` runs the adapter with `--apply`. It MINTS 6,653 objects in `opal-data-cottonwood` under
`irpt/cottonwood/gold/`: 3,325 day prefixes of `account_return_daily/` with two objects each, one reasons sidecar, and
`dim_return_method/method_version=3/` with two objects. The pair says nothing is overwritten and nothing deleted. Readers: 0;
no reader, role, route or export is added. The three pins of the COO half (adapter, producer and sources, manifest) bind
this half too.

## 2. Decided here

- **The sidecar's address is ACCEPTED:** table `account_return_daily_blank_reasons`, partition `source_date=2026-06-23`. It is
  builder output, it sits beside the table whose blanks it explains, and its partition is the date of the source delivery the
  blanks were read from. Row D2-W86-S1 closes on this.
- **The widening the COO half names is signed by name:** the tracked manifest states three fields it did not state at round 52
  (`vocabulary_notes`, `reasons_sidecar`, `method_row`), and the act writes 3 objects the first half did not cover.
- **A partial mint is finished, not deleted.** If the run stops after its first write, the remedy this seat rules in advance
  is a RESUME under an amendment to this pair: each landed key's served bytes are hashed against the manifest, and only
  absent keys are written. Deleting minted keys stays Andrew's act and is not the default. The landed keys stay unread behind
  the reader gate meanwhile.

## 3. What this seat read itself, and what it took as filed

- **Read here:** the COO half in full and its sha256. Earlier tonight, for the rulings this pair rests on: the reviewer's two
  slugs for rounds 50 to 57 and their grades; this seat's own repo-wide census of the manifest damage (431 hits in 1 file,
  then 0 after the repair by the issuer's re-run).
- **Taken as filed:** the three empty-prefix reads and their 245-key control, the manifest and day hashes (3,325 of 3,325),
  the row counts, the bond count of 0 of 107,316 with its 141,555-day control, the sidecar's hash and counts, the test
  results on faked S3, and the reading of the scheduled Lambda's rule from the repo.
- **Not established by anyone, and the COO half says so:** the bucket policy; a real put on the sidecar and method-row keys;
  the deployed reporting-gold Lambda's packaged `sources.json`; whether `emit_day` writes the row-3 manifest against the real
  bucket (exercised on faked S3 only). Conditions 2 and 3 are aimed at the last one, which is row D2-W66-S1's hazard.

## 4. Conditions

1. **Versions are read before the first write.** `list-object-versions`, every page, on each of the three prefixes: the count
   of versions and of delete markers, printed. An empty CURRENT listing does not show whether an earlier mint was deleted.
   Both counts 0: the pair's "no prior version exists" is true. Above 0: the counts go in the ledger and the rollback
   sentence is corrected there; it does not stop the act.
2. **The day manifest is seen before 3,325 of them are written.** Before `--apply`, the applier shows the exact
   `manifest.json` the producer will write for one day (a dry run, or a local call of the same `build_manifest` with the same
   `src`): `method_version` 3, the row-3 method sentence, `valuation_source` `positions_x_as_traded_close`, `fee_treatment`
   `net_of_fees`, `price_basis` `as_traded`. The custodian method's text anywhere in it is a STOP. If the tool cannot show it
   without writing, STOP and return to this seat.
3. **`--verify-served` covers both objects of every day.** `data.parquet` against the tracked hash, and each served
   `manifest.json` read back for the five fields of condition 2: 3,325 of 3,325, printed. Row D2-W66-S1 disarms on that line.
4. **The bond count is re-read first and the run refuses on anything but 0,** as the tool does.
5. **Before the act:** every live worktree's `.open_deploys/` is read and unioned with its per-tree denominator; the ledger
   entry is opened before the first write.
6. **After the act the keys stay unread.** No reader of `account_return_daily` for Cottonwood exists until its own pair
   (ADDENDUM 11.1). The ledger close says APPLIED, UNREAD.
7. **Not covered:** any delete; any overwrite; a re-run of `build()`; any key outside the three prefixes; any reader.

Rollback is the COO half's section 4 with section 2's third point: the minted keys stay unread, a partial mint is resumed
under an amendment, and a delete is Andrew's.

-- 1.0.0_SA_CTO~DELL2
