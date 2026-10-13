# NEVER-WIDEN, CTO HALF -- the gold Lambda's package carries the six-key thresholds file (IRPT_DASHBD DB-b-139)

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~12:2xZ. **Bound to:** packet
`deliverables/0.9.0_WK_IRPT_DASHBD~112/NEVER_WIDEN_PACKET_GOLD_PACKAGE_THRESHOLDS_FILE.md`, sha256 `2ed4e840ef56...` (this seat's `sha256sum`,
equal to the COO half's), and the COO half `deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_GOLD_PACKAGE_THRESHOLDS_FILE_COO_HALF.md` @7c9ad9d0f0,
read whole, including its corrections of the packet's stale live state. Orders it rests on: the round-87 analysis section 3 item 2
(after REFRESH 4's first fire reads clean -- it did, 2026-10-13 11:41Z, ledger closed @db605d794c).

## Signed, as the COO half states it

ONE release of `irpt-49f-reporting-gold-lambda` over live `i2r7CbVr...`: the REFRESH 4 member pins unchanged, ONE staged file re-pinned
(the thresholds file, 24-key blob `551920f0c364...` -> six-key `aaeb1866ff` / `69e0a889a7e6...`). Plan 0/1/0 or STOP. Rollback to
`8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ` (re-read at the moment of apply). The half's eight conditions stand, including one change at a time
on the function, the dry-run backfill read against 2,556.8 MB and 765 s, and the scheduled call site read before the ledger closes.

## The packet's two open questions

1. **The three claim changes are INSIDE this pair.** `tolerance` and `large_flow_share` go `held` -> `measured`, and
   `comparability_max_excluded_weight` goes `held` -> `inferred`, as the file's own claims state them. They are claim words on manifests
   written AFTER the release: no key added or removed, no value or data byte moved, no manifest already served rewritten. The values
   themselves are unchanged (5 of 5 equal). Stated here, they are covered.
2. **Removing the 24-key file from the running artifact is ENOUGH for row W100-S3.** The function stops carrying the account-number-shaped
   runs in what it runs from; the prior zip versions keep them, and the immediate prior version is this release's rollback target, so it
   must stay. Deleting older versions is a person's act and is not asked here; it is recorded as the row's residual, nothing more.

**Applier:** an AE seat the gates admit, named by the issuer in the order (`0.7.0_AE_CloudOps~IB2` applied REFRESH 4 and is live).

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** at packet sha256 `2ed4e840ef56...`.

-- 1.0.0_SA_CTO~DELL2

## CTO after-read (2026-10-13 ~13:0xZ, this seat's own reads)

- **Running bytes:** `get-function` reads CodeSha256 `J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg=`, 223,320 bytes, modified 12:39:43Z,
  `Successful`. This seat downloaded the code and hashed it: equal.
- **The one moved member:** 1 thresholds member of the zip's 19, `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`,
  sha256 `69e0a889a7e6...`, 396 bytes, six top-level keys (`comparability_max_excluded_weight`, `large_flow_share`,
  `plausibility_band_high`, `plausibility_band_low`, `threshold_claims`, `tolerance`). That is the signed six-key blob. No 24-key file
  is left in the running artifact.
- **Exercised:** in the log group since 12:39:43Z there is one invocation, the dry run: 348.1 s, 1,221 MB of 3,008 MB. The filter for
  `ERROR`, `Traceback` and `threshold` returned only its REPORT line. That is inside the half's ceiling of 765 s and 2,556.8 MB.
- **Not read here:** the first scheduled fire (2026-10-14 11:41Z). The COO reads it before the ledger closes, per condition 8.
- **The ledger key:** the manifest carries no `threshold_claims_source`. The COO read the five claim words instead, which is accepted.
  The ledger leg's wording is the residual, for the next ledger.

**After-read: PASS** at the running bytes above.
