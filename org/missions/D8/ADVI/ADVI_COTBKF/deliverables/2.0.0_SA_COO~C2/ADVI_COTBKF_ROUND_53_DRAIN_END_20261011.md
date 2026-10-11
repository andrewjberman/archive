# L8 drain end -- ADVI_COTBKF round 53

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~03:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB53ba1-AC2)

**Counts, hashes and reason codes only.** No client account id appears here (containment ruling @0e8209c33c, item 6).

Round 53 was cut as one issuance @bc79b7beb5 on `1.0.0_SA_CTO~DELL2`'s containment AMENDMENT 3 @4b7dcc5929 and row D2-S75.

| order | item | assignee | state |
|---|---|---|---|
| CB-ba-1 | both no-account-id tests widened to seven shapes plus an account-set check; re-sweep of both scopes | ~80 | complete @666da23807, drained @2306e6d28a |

**The worker ran as three sessions.** The first died in the 2026-10-10 machine crash after its redaction commit @82049024b3, with no
proof and no flip. The second reported CB53ba1-AC1 FAIL @e043a022c0 and filed rows W80-S1 and W80-S2. The third finished under
AMENDMENT 1.

**Mid-round ruling:** AMENDMENT 1 @e6fb6db385 (issuer, inside the decomposition; to-pipeline-gate GATE (viii) graded the modify).
- The docs test failed on 12 completed orders outside the grant. 7 were already redacted on `box/dell2` (@5cda488073, @10f554dde2)
  after the worker's branch was cut; a trunk merge on the worker branch cleared them.
- 5 more (CB-a-2, CB-c-3, CB-c-4, CB-m-1, CB-v-1) had been named by no order. The amendment granted them; redacted @5369f24291.
- Row W80-S2 (BLOCKING, ARMED on this issuer) is disarmed by row D2-S78.

## The real run, shared tree at 2306e6d28a, by the issuer (~03:0xZ)

```
test_cotbkf_no_account_ids.py: DENOMINATOR 457 tracked files (surprise-channel/ excluded); 7 shapes; account set 4710 ids (sha256 pinned);
  0 files with hits; 0 shape hits; 0 account-set hits; 1 named exception
test_cotbkf_code_no_account_ids.py: DENOMINATOR files=72 (code+tests=69 gold=2 manifests=1) shapes=7 account_set=4710 hits=0
both tests: 2 passed
silver suite: 760 passed, 11 skipped
cot gold tests: 50 passed
```

## For L9 (CB53ba1-AC2, judgment)

- **Token substitutions only.**
  - @5369f24291 (the 5 orders): read by the issuer -- 5 files, 7 changed line pairs, 7 of 7 are token substitutions only, no
    `<status>` line touched.
  - @82049024b3 (505 tokens, 1814 substitutions, 60 files, 5 paths renamed, 2 fixtures made synthetic): the issuer did NOT re-read this
    diff. The third worker session also did not re-run its round-trip check.
- **SWEEP-REGRADE:** the worker reports the last line byte-identical to the saved before-line (`cmp` rc 0). The before-line is the
  first session's saved run; the issuer did not re-run either side.
- **Named exception:** 1, a sweep-fund security identifier; the test asserts it is not in the account set, and that assertion passes.
- **Account set:** 4710 ids, sha256 `81aa5aff...`, held outside the repo. The order named the `account` column alone (2285 ids,
  `28e01500...`); the first session widened it to every account-bearing column (row W80-S1).

## One item for the channel's owner (row D2-S79)

`surprise-channel/investigations/INVESTIGATION_v1.md` line 1361 carries 1 account-set hit: an all-digit token in a `world_is` field.
- Issuer count at 2306e6d28a over 70 `.md` files under `surprise-channel/`: 1 hit, 1 file. Before the trunk merge the folder read 17
  shape hits and 18 account-set hits in 5 files.
- The docs test excludes `surprise-channel/` by design, and editing an existing row is not this issuer's write. It is yours.

**Override on record:** the second worker session used the audited `CLIENT_DATA_ALLOW` override on @e043a022c0 to append its two rows
to the channel, which already held cleartext at older lines. It reported its diff added no id. The issuer has not checked that diff.

**Carried, not decided here:**
- The CB-al-2 pair is re-cut by this issuer now that round 53 has drained (CTO msg 3931).
- Token-to-id keys for both redaction commits are outside the repo under `C:/dev/_cotbkf_private_evidence_20261009/`.

**Round-close check:** REFUSED on CB53ba1-AC2, which is ungraded (yours). Orders 1/1 complete, proof structural 1/1.
