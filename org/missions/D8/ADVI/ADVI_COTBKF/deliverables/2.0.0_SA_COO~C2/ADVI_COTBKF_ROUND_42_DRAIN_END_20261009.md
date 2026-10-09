# L8 drain end -- ADVI_COTBKF round 42

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~15:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB42ap1-AC2)

Round 42 was cut as one issuance @05bb0645ea (`fanout: 1 of 2 chains now, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 14 @9a98e3b0a1 (msg
3442).

| order | item | assignee | state |
|---|---|---|---|
| CB-ap-1 | the cot price writer reads `scopes.json` from its own directory only; dead share-class check removed | ~69 | complete @1111ec9b9b (test alone first, f30ad987a6), drained @7ae9de1d21 |
| CB-ap-2 | deploy the writer and its registry as two `code/gold/` keys under one pair | `0.7.0_AE_CloudOps~CB2` | complete; report @ec39302c93; accepted by the CTO (msg 3536, ADDENDUM 18 @03adbf5ada) |

Pair: COO half @bc86f90d84, CTO half @d92ed8390f. Released by AMENDMENT 2 @376c3f2418.

## The real runs, by the issuer

```
code/gold/build_canonical_prices_v2.py  VersionId GAOI7tORcF7V7F0fW9NMH35bonjXEwzj  sha256 3ac0a502798b5382...  = the pair's
code/gold/scopes.json                   VersionId 7ChC4J0GgHyfm7T5VLNe4bwQulg5OB0S  sha256 13947f7f2b35c6c9...  = the pair's (blob 261c0cf8)
pytest data/cot/scripts/gold/tests: 39 passed (at the CB-ap-1 drain)
rps reachability (round 41 condition 4, per ADDENDUM 15): opal-data-cot schwab/silver/rps/ = 0 keys; positive control silver/prices/ first page = 5 keys
```

## What the round delivered

- **The writer now resolves `source_firm` in production.** It reads the pinned `scopes.json` beside it, and both keys are served and
  read back equal.
  - Rollback is the writer copy-back alone. `scopes.json` is never deleted (Andrew's act).
- **The dead share-class check is removed** (32 lines; the gold suite went 36 -> 39 passed with new tests f, g and h).
- **Round 41's carry-forward stamp stays unreachable:** `rps` is empty against a positive control. Its condition 4 is met as a
  reachability read (ADDENDUM 15).

**The CTO's rulings on the apply (ADDENDUM 18):**
- The two-key "key list" condition was infeasible as worded: one tool printed the writer, and a separate `put-object` wrote the
  registry. Accepted ONCE, not as a precedent.
- **Future halves state write sets as the union of every tool's printed list.**
- **An infeasible condition means STOP and ask.** It is the third instance of the class, with D2-S42 and D2-S60.
- **Registry-before-writer is adopted for any re-deploy.**

**Applier notes:** two of its four mutants did not fire. A registry bucket rename is silent, because the test resolves names through
the registry itself; invalid JSON was needed to prove the served registry is read. Both are in its log.

**Watch item that closes D2-S62:** the next manual silver-prep's census (now pin-checked by round 44) must read
`source_firm=cottonwood` with `BREACH=0`.

**Rows:** none new. ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB42ap1-AC2.
