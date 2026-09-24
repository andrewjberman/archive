# AMGT_CORPUS round 3 -- never-widen pair, the FWD-12 DERIVE (the Model block with the 22 added mnemonics, 89 keys)

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`, in its own lane
(`ledger/`). The derive does not run until both are signed at these bytes. It is leg L3 of the open change-management entry
`amgt-corpus-fwd12-model-block-pull-20260924` (@`9361723c96`), whose L1 (pull) and L2 (raw verify) are closed.

## COO HALF -- `2.0.0_SA_COO~X`

**Where it stands.** The pull ran once under Andrew's per-use word (@`16ee7f6373`, FWD-12's figures for the 22) and R-21:
30 of 30 batches rc 0, 89 of 89 keys landed raw (refdata + histdata + bestdata each, read back on S3, the two slash keys under
their sanitised partitions); `evidence/fwd12_pull_20260924T213558Z.log`. Raw bronze is write-once and served by nothing. The
DERIVE is what reaches a screen, so it takes this pair.

### THE ACT

`model_block_pull.py derive --securities <k1> <k2> <k3>` over the same 89 keys (`FWD12_PULL_KEYS_20260924.json`), 30
invocations of at most 3, stopping at the first non-zero rc. Each derive reads the raw bytes BACK from S3 (never the pull's
memory), joins fiscal years, and lands one object.

### BLAST RADIUS -- what the act MAY touch, and the rollback for each

1. **Per key, ONE new object** `derived/model_block/<safe key>/<UTC stamp>/model_block.json`, `s3_put_if_absent` (a fresh
   stamp, never an overwrite). **This is a served move:** the newest object per key is read by FOUR readers --
   `lib/research/api/scoped_amgt.py` (`read_model_block`, the served API behind the Model tab), `lib/research/print/
   render_pack.py` (print packs), `lib/research/peers/universe.py` and `lib/research/scores/run_scores.py`.
   Before-state, measured (`evidence/fwd12_derive_before_20260924.json`): **31 of 89 keys already serve a block** (newest
   stamps 2026-09-19 .. 2026-09-22) and **58 serve none**. So 31 served blocks are REPLACED as newest (the 46 existing fields
   re-derived from today's raw, plus the 22) and 58 go from absent to present.
   **Rollback:** for the 31, copy each key's prior newest block forward under a newer stamp (no delete; the prior keys are
   in the before file). For the 58, the only rollback is removing the new object, **an S3 delete, which needs Andrew's
   confirmation** -- so a bad derive on those 58 is disclosed, not silently reversible, and this half says so.
2. **The unit map** (`build_unit_map.FIELD_MAP_PATH`, a repo file beside the producer): additive entries for a security the
   map does not yet carry, never overwriting a MEASURED entry. Committed by this seat after the run, or reverted.
3. **Seeking Alpha fallback** for a FY1-FY3 `BEST_` cell Bloomberg left empty (`sa_forecast_fallback.py`): GET requests
   only, raw landed write-once at `seeking-alpha/harvest/bronze/{symbol,metrics}/security_key=<safe>/<stamp>.json`; a
   REHARVEST or transport failure STOPS the fallback for that security (no sign-in, no retry). Authority: authorized by name
   for exactly this path (Andrew-direct "Yes use SA thats fine", PRD `C-SA-VENDOR-WORD`, cited in the module docstring) and
   R-21 (scripted producer).
NOT in the write set: `derived/model_block_fye/` (a separate writer, `derive_fye_fixed.py`); any crosswalk, dossier or
backlog key; any delete.

### WRITER CENSUS -- N = 2 writers of the named prefix, PRINTED

`comp-find 'derived/model_block' integrations lib infra/aws/lambda --band SURFACED` (27 hits, 5,726 files; SURFACED 17, read in
full) plus the producer's own key composition (`model_block_pull.py:1318`, `f"derived/{ENGINE}/{sec_key}/..."`, which the
literal census cannot see): the writers are **`model_block_pull.stage_derive`** called by (a) THIS act's `cmd_derive` and
(b) **`integrations/bloomberg/research/pull_consumer.py:99`**, the terminal box's pull drain, which imports the same
function unmodified. ONE rule, TWO callers. `derive_fye_fixed.py` writes `derived/model_block_fye/`, a different prefix the
served reader explicitly excludes (`scoped_amgt.py:150`). If (b) runs during this act, it lands its own newer stamp by the
same rule; the reader picks the newest either way, so the two cannot produce a mixed object.

### EXPECTED OUTCOME -- read from the producer's own rule, BOTH branches

Per `stage_derive` (`model_block_pull.py:1116-1326`): every figure carries `{value, unit, sign, basis, vintage, source}`;
the latest CLOSED fiscal year is named and an unclosed group goes to `unresolved`; forecasts FY1-FY3 come from the
`BEST_FPERIOD_OVERRIDE` rows, and a set whose period dates are not annually spaced is REFUSED whole for that stamp rather than
served. So:
- **a key derives:** one new block, the 22 present as figures or as `unresolved` records naming why (a refused mnemonic, an
  empty cell SA could not fill). Nothing is invented.
- **a key raises:** no new object for that key; the prior block (the 31) or nothing (the 58) keeps serving; the batch stops
  at its non-zero rc and the rest are NOT run until read.
Read-back recorded per key: derived key, figures present of the 22, unresolved count, SA fallback used or not.

**Discriminator after the run:** for each of the 89, the newest `derived/model_block/<key>/` object is this run's stamp
(or the key is named as raised); for a sample of 3 (one of the 31, two of the 58), `scoped_amgt.read_model_block(key)`
returns this run's block with the 22 fields present or unresolved-with-reason.

Signed: `2.0.0_SA_COO~X`, 2026-09-24 21:5xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Owed, in the CTO's own lane (`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).
