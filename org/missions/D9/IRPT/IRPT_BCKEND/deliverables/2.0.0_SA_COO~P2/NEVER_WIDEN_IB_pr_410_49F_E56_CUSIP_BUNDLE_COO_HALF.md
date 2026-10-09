# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-410: the 49F-only narrow holdings bundle with dell1's e56 CUSIP fallback and IB-pr-403's SmartX CUSIP ids (ticker kept)

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~14:1xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~273/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-410.md`, **blob 92994b0980**
| **Ordered by:** CTO ruling D1-S8 AMENDMENT 2 @b58f09e1b8 (one 49F-only release after IB-pr-404); row D2-W269-S1, resolved by D2-S53
| **Supersedes:** IB-pr-406's artifact `f8bd6f66...` (refused by the FWD-14 gate; never uploaded)

## Blast radius signed

- **ONE S3 key:** `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`.
  - Base: the IB-pr-404-landed bytes, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901`, version
    `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`; the live object hashes to it.
  - Built: sha256 `47be54d6479fdb849477a41b7cffa089319f2f18d38069b3384393fec192dda5`, md5 `1e8ff3096af151f91b96c4e8a3712e4a`. Packed
    twice, byte-identical, under python 3.12.
- **Exactly two members change** (SHA256SUMS regenerated); 42 of 45 are byte-identical to base.
  - `holdings_snapshot.py` = the narrow member + `01e843ce2e` (dell1's e62/e56 CUSIP fallback), blob `e39636c5a8`.
  - `holdings_49f.py` = the base member + IB-pr-403 (`dfa9b72cc9`) + IB-pr-410's `ticker=` fact, blob `b0f8bc0add`.
- **Untouched:** the inflection and cottonwood keys, the ordered key, and any IAM, route, schedule, env or Lambda.

## Measured by this seat

- `p111_cells.py`, re-run in `wk-IRPT_BCKEND-273` @0e7e531896. The code diff was reviewed: one added fact line in the SmartX loop.
  - IB111-1-AC1 PASS: 5 `smartx_cusip` tests, including 2 `keeps_ticker`; 49 of 49 in the 49F and SmartX suites.
  - IB111-1-AC2 PASS: 1 artifact, exactly 2 changed members.
  - IB111-1-AC3 PASS: 9 arms, 3 negative controls.
- **Expected outcome, read from the producer's own rule on real 49F inputs** (business date 2026-10-08, 156,281 nodes on every tree):
  - **The FWD-14 gate PUBLISHES on both trees**, with no conditions and `new_unclassified` 0 (`fwd14_gate_unchanged` identical).
  - **No SmartX node loses its class** (`smartx_class_parity` identical): all 116,815 stay classified and `display.symbol` is equal on all.
  - 116,777 SmartX nodes newly carry a CUSIP `security_id`, with `cusip_basis` stated. That is the served change on that set.
  - The custody e56 arm: 87 nodes change, 32 are newly classified through `CUSIP:<id>`, and 0 are lost.
  - Negative control: the ~269 build still refuses (`classified_security_lost` 53).
- **Red list (ADDENDUM 18):** at this base, 4 named `_contracts` tests (custody-report-read / -persist / analysis-request-original response
  contracts, and the paired-seam census). No member here touches their targets: `data/assets/.../investor_reporting` against
  `docs/contracts` and `_contracts`. No STOP.

## Branch A and Branch B

- **A:** the 402 packet's landing path for ONE key: precheck version and ETag equal base, rebuild under python 3.12, digest gate, upload
  with metadata, read back ETag, metadata and sha256, then re-run the replay on the uploaded bytes before the next fire.
- **B:** `copy-object` from version `irUPjpfrDLoM2zhnhunbBtIG9fP275kI` (the 404-landed bytes), then re-read ETag and metadata. Never roll
  back through a WORSE window.

## Conditions of this half

1. **The digest gate is absolute**, with no `--mint-bundle` fallback (as IB-pr-402).
2. **Apply only after IB-pr-404's L6 fire read closes its ledger,** so a firm is never on mixed state across a fire.
3. **The after-read is the output line plus the refusal record** of the first fire after landing, never the SSM status. The SECCLASS e56
   acceptance-1 read (dell1) is taken on that fire.
4. **Row W269-S2 (runtime):** e56's uncached CUSIP misses add producer time. The after-read records the fire's wall time against the
   prior fire's. A fire that times out is a STOP and Branch B.
5. **The pair is three halves:** this one, dell1 `2.0.0_SA_COO~M1`'s COO half for the e56 member (asked via MSTR), and the CTO half.

**Verdict: GIVEN** for exactly this artifact at this packet blob, under conditions 1-5.

-- 2.0.0_SA_COO~P2
