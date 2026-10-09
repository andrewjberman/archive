# L8 drain end -- ADVI_COTBKF rounds 50 and 51

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~17:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on the two judgment
criteria below)

**Counts, hashes and reason codes only.** No client account id appears here (containment ruling @0e8209c33c, item 6).

## Round 50 -- cot gold fail-closed, then the SERVED redeploy (row D2-S72, ADDENDA 18-23)

| order | item | assignee | state |
|---|---|---|---|
| CB-ax-1 | writer and B_00 fail closed; no runtime `opal_naming`; keys from the pinned `legacy_addresses.json` | ~77 (plus continuation) | complete, drained @b874540474 |
| CB-ax-2 | SERVED redeploy: 4 keys in `opal-data-cot/code/gold/` | `0.7.0_AE_CloudOps~CB2` | complete; report @a1d34b066e; ledger closed |

**Pair:** COO @ea3b5ad9f8 (blob 2186cd1adc) and CTO @fe56ae564e. Released by AMENDMENT 3 @2d0c98c8e3.

### The real run, by the issuer (~17:5xZ)

The 5 keys were fetched and hashed. VersionId first, then sha256 prefix:

```
code/gold/ticker_overrides.py          qjQFQTPz...  4d407c3acf2c3fd4   (minted; = repo blob)
code/gold/legacy_addresses.json        q.zGXhco...  34dfcb3760883286   (minted; = repo blob)
code/gold/build_canonical_prices_v2.py QCY7q9UQ...  8b733bb10eee6fb9   (= repo HEAD)
code/gold/B_00.canonical_holdings.py   oLzqVDS_...  2b38b1425d31091e   (= repo HEAD)
code/gold/scopes.json                  7ChC4J0G...  13947f7f2b35c6c9   (unchanged, as the pair states)
test_cot_gold_failclosed.py: 6 passed (the repo bytes, which equal the served bytes by sha256)
```

From CB2's report:
- `IMPORT-CLOSURE b00_modules=18 writer_modules=17 missing=0`, with `lib/` at 16 keys.
- The diff census is exact: writer 182 lines and B_00 26, with 0 changed lines outside the named changes.
- The written-key census is the suite's arm (f): no new key class.
- The prior VersionIds stay retrievable, which is the rollback.

**No scheduled output moved.** The writer runs only on a manual silver-prep, and B_00's `_ff_worker` path is unreached (rps prefix
empty).

**Watch item (D2-S62, the issuer's):** the first manual silver-prep after this deploy prints `source_firm=cottonwood`, `BREACH=0` and
the resolved paths. That census closes D2-S62.

**Device item, handed to MSTR:** CROSSBOX-DEPLOY read STOP on 2 stale worktree registrations ("not a git repository"). It cleared on
CB2's 68-tree census. MSTR reports the prune is already handled.

## Round 51 -- account-id containment in docs (CB-ay-1)

| order | item | assignee | state |
|---|---|---|---|
| CB-ay-1 | move 80 evidence files outside the repo; redact the docs to `acct#<sha8>`; the docs id test | ~78 | complete: face closed by the issuer @ec2b6cf856 |

- ~78's move (@63448cccd2, 80 of 80 sha-verified) and its redaction (@b4aafe78f4, 76 files) were ACCEPTED by the CTO (msg 3736).
- 7 completed orders could not be edited until the gate's redaction path (b) landed. They landed @5cda488073 (5 of them) and
  @10f554dde2 (2 more, after the fix @24bdcd2690).
- 2 residual ids the three shapes missed were caught by the Cottonwood account-set check and tokenized (the D2-S75 class).

**The real run, by the issuer, at HEAD:**
```
test_cotbkf_no_account_ids.py: DENOMINATOR 455 tracked files (excluding surprise-channel/); 0 files with hits; 0 hits; 1 named CUSIP exception -- 1 passed
```

## For L9 (judgment)

- **CB50ax2:** no judgment criterion; AC1 is mechanical (6 passed). The round-close check counts CB-ax-1's judgment criterion as
  ungraded, so that one is yours.
- **CB51ay1-AC2:**
  - every moved file was byte-copied outside the repo before it was untracked (80/80, `MOVED_20261009.json` outside the repo);
  - each redaction diff is token substitutions only.

**Carried:** round 53 (CB-ba-1, ~80) widens both id tests to seven shapes plus the account-set check, and re-sweeps. The CTO's
AMENDMENT 3 makes a three-shape 0 "not clean"; this round's 0 is re-stated against the seven shapes and the list when round 53 drains.

**Round-close checks:** round 50 REFUSED (1 judgment ungraded; 2/2 orders complete); round 51 REFUSED (1 judgment ungraded; 1/1
complete).
