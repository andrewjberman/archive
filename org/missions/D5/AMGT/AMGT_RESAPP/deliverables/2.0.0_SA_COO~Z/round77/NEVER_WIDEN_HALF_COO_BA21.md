# AMGT_RESAPP round 77 -- `AMGT-ba-21` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~09:3xZ

**The act:** the Bloomberg SEGMENTS research pull, an ISSUER ACT (decomposition s.85b, no order file), run by this seat at site Z
with `integrations/bloomberg/research/research_pulls.py` (cell ba-25, drained). Two steps, in this order, both AFTER the
07:00 America/New_York vehicle of 2026-10-07 has run:

1. **The probe.** `run segments --probe "AMD US Equity"`: ONE `reference_data` call, four fields
   (`NAME`, `SEGMENT_NAME`, `SEGMENT_REVENUE`, `GEOGRAPHIC_SEGMENT_NAME`). Three of the four are UNPROBED
   (`research_pull_fields.json`, `probed: false`): the repository records no Bloomberg segment mnemonic.
2. **The pull**, only on branch A below: `run segments --confirm-calls <M>`, one name at a time, one call per name.

## Authority

Andrew-direct 2026-10-06 ~21:1xZ, "all recs approved", ruling 1
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261006_211xZ_ALL_RECS_APPROVED_CTOZ_OPEN_CALLS_FOUR_CARDS.md:12-15`):
three one-time Bloomberg research pulls, after the firm's 7:00 AM ET pull, one at a time. The record's scope line: three named
pulls, not a standing word for any other Bloomberg pull.

**ONE DIFFERENCE TO THE RECORD, surfaced and not adjudicated here.** The record names "business segments for 83 names". The
driver's plan, read at 09:2xZ with no Bloomberg call, reads **85 names, 85 calls**. The population is computed (covered names
whose stored segment breakdown serves no rows), so it moved by two since the card was written. The CTO half says whether the
pull runs at the plan's count on the day or is capped at 83.

## What the act may touch (the blast radius)

- **Vendor:** at most 1 + M `reference_data` calls on the Terminal's logged-in entitlement, M = the plan's count on the day
  (85 at signing). No historical request, no BQL, no sign-in: `health()` false stops TERMINAL_DOWN with no call.
- **Store, new keys only:** `s3://opal-data-harvest/bloomberg/harvest/bronze/segments/security_key=<KEY>/<stamp>.json`
  (the address is `store.address_of` output, printed for AMD at signing:
  `.../bronze/segments/security_key=AMD_US_Equity/<stamp>.json`). One object per name that returns a row.
- **Nothing served moves.** No reader of the `segments` bronze exists: the decomposition states the served reader is NOT cut
  because its shape depends on this probe (s.85b, "Not an AMGT_RESAPP order"). No Lambda, route, table, schedule or page changes.
- **The Bloomberg budget ledger is NOT written by this driver.** `bbg_budget` records the rival-funds collector and (after the
  SECHIST deploy) the ETF history backfill; `research_pulls.py` calls neither `check_backfill` nor `record`. These are
  reference-data calls of one row per name, not history rows. Stated so no reader assumes the ledger counts them.

## The base, read at signing (09:2xZ)

| object | value |
|---|---|
| existing `segments` bronze for AMD | 0 objects (`store.fetch_key_exists`) |
| existing `exec_officers` bronze for AMD (the control channel) | 0 objects |
| bucket `opal-data-harvest` versioning | Enabled |
| the write | `store.bronze_put`, a conditional put (`IfNoneMatch="*"`): a key is never overwritten |
| plan | names 85, calls 85, `calls_per_name` 1, `probed False`; AMD US Equity is name 12 of 85 |
| vehicle | `OPAL_BBGTML_daily_pull`, 07:00 America/New_York; not yet run today at signing |

## Writers counted (NEVER-1)

`bloomberg/harvest/bronze/segments/`: **N = 1 rule**, `lib.research.harvest.bloomberg.bronze_write("segments", ...)`, reached
from `research_pulls.bronze_writer` (its `BRONZE_REQUEST` map). `segments` entered `BRONZE_REQUESTS` in round 77 (ba-25, one tuple
entry). Read at signing: under `lib/research/harvest/` the quoted name appears once, in that tuple; 17 files repo-wide call
`bronze_write` or name a bronze request, and the other 15 were not opened one by one for a computed request name.

## Both branches

**The probe:**
- **A. One or more segment fields are served** (a row with segment content and no field exception on that field). The response is
  landed as received at the AMD key. The fields file is then edited to the served set with `probed: true`
  (`research_pull_fields.json`, the ba-25 surface) in its own commit, and step 2 runs with `--confirm-calls` equal to the plan.
- **B. No segment field is served** (`BAD_FLD` / field exceptions on all three, or NOT_APPLICABLE). The response is still landed
  as received (it is the evidence). Step 2 does NOT run. The field exceptions name the next mnemonics to try or the surface that
  refused (READ_HERE section 4: ask which surface refused). A second probe with different field names is a NEW call and comes
  back to the CTO first; it is not covered by this half.
- **Stops, no call spent or one call spent:** VEHICLE_NOT_RUN (exit 4, no call), TERMINAL_DOWN (exit 5, no call, no sign-in by
  this seat), CAPACITY (exit 3, the driver never calls again). Each is reported; none is retried the same hour.

**The pull (branch A only):**
- every name returns: M objects land; `pulled M failed 0`.
- some names fail (no row, or an `__error__`): they are listed `FAILED <name>: <reason>` and nothing lands for them; the run
  continues. Failed names are NOT re-run under this half.
- CAPACITY at any name: the sequence stops there; the names already landed stay; the rest wait for another day and a new word.

## Rollback per key

- A landed bronze object is evidence and is kept: bronze is write-once and the round carries `no_s3_deletes: true`. Because no
  reader exists, a wrong or empty object changes no served value. If a reader is later cut, it selects by content, never by
  presence.
- The fields-file edit (branch A) is one commit; its rollback is the revert of that commit.
- Vendor calls cannot be rolled back. That is why the probe is one name and the pull states its count first.

## After the act

FWD-1 on AMD is re-read (ba-24 marked it SEGMENT PULL NOT YET RUN) only once a served reader of this bronze exists, which is the
first item offered to the round-77 analysis. This act alone does not change that page.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~09:3xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`, including the 83 against 85 call.
