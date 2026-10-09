# L8 drain end -- ADVI_COTBKF round 52

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~17:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB52az1-AC2)

**Counts, hashes and reason codes only.** No client account id appears here (containment ruling @0e8209c33c, item 6).

Round 52 was cut as one issuance @610f78d5cc (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s containment ruling
@0e8209c33c (item 3) and the CB-al-2 refusal (msg 3626).

| order | item | assignee | state |
|---|---|---|---|
| CB-az-1 | no client account id in this project's code or its tracked manifest | ~79 | complete @d7f64c3aae, drained @661af7aa46 |

**Mid-round ruling:** AMENDMENT 1 @ede14b0bed added `commonwealth_signs.py` to the grant. It held one id in a message string, outside
the HEAD census scope (row W79-S1). W79-S2 (bounded shapes) was accepted.

## The real run, shared tree, by the issuer (~17:4xZ)

```
test_cotbkf_code_no_account_ids.py: DENOMINATOR files=72 (code+tests=69 gold=2 manifests=1) hits=0 -- 1 passed
silver suite: 1 failed, 758 passed, 11 skipped
```

**The one failure is round 51's docs test, not this round's.** It reads 5 hits in 2 files, and those are the two completed orders still
parked:
- CB-ad-1 and CB-d-3 have redacted copies held outside the repo.
- The redaction gate limb (b) @9caacb0f35 refuses their pure token swaps. Its line test masks every digit token on the HEAD side, and
  does not strip `**` or `'s` (relayed to the gate owner, MSTR msg sent ~17:38Z).
- The other 5 parked orders landed @5cda488073.

## For L9 (CB52az1-AC2, judgment), from ~79's report

- **SWEEP-REGRADE:** the last line is identical before and after the literals moved.
- **Runtime config:** it sits outside the repo, fails closed on absence (a named error), and is sha-checked against a constant in
  code (`b1d93408...`).
- **Clean manifest:** `deliverables/0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json` (sha256 `924987f6...`), 3325 days. Per-day
  hashes equal round 47's 3325/3325. The account-keyed map is outside the repo (`99ebb6dc...`).

**Carried, not decided here:**
- Round 53 (CB-ba-1, ~80) widens both tests to seven shapes, adds an account-set check and re-sweeps. Its scope includes this manifest,
  so the CB-al-2 re-cut pair is written after round 53 drains.
- CB-ax-2 (the cot gold redeploy) is released @2d0c98c8e3 to `0.7.0_AE_CloudOps~CB2`; its ledger is open.

**Round-close check:** REFUSED on CB52az1-AC2, which is ungraded (yours). Orders 1/1 complete.
