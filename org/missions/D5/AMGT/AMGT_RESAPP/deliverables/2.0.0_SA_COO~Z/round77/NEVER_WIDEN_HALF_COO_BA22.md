# AMGT_RESAPP round 77 -- `AMGT-ba-22` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~09:4xZ

**The act:** the Bloomberg EXECUTIVE OFFICERS research pull, an ISSUER ACT (decomposition s.85b, no order file), run by this
seat at site Z with `integrations/bloomberg/research/research_pulls.py run officers --confirm-calls <M>`: one name at a time, ONE
`reference_data([name], ["NAME", "COMPANY_EXEC_OFFICERS"])` call per name. It runs AFTER ba-21 has finished (one pull at a time,
decomposition s.85d) and after the day's 07:00 America/New_York vehicle has COMPLETED.

**THIS ACT MOVES SERVED OUTPUT, unlike ba-21.** The stored Bloomberg officer list has a live reader. That is the point of the
pull, and it is why this half is written separately.

## Authority

Andrew-direct 2026-10-06 ~21:1xZ, "all recs approved", ruling 1
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261006_211xZ_ALL_RECS_APPROVED_CTOZ_OPEN_CALLS_FOUR_CARDS.md:12-15`):
"executive officers for 84 names (row Z-W227-S1)", after the firm's 7:00 AM ET pull, one at a time.

**The same difference as ba-21, surfaced and not adjudicated here.** The record names 84 names. The plan, read at 09:3xZ with no
Bloomberg call, reads **86 names, 86 calls** (`probed True`). The population is computed: covered names whose officer chain
reports its Bloomberg leg as `needs_new_pull`. The CTO half says whether its ba-21 ruling (the plan's count on the day, with a
bound) carries to this pull and at what bound.

## The producer's own rule, read at signing (what a landed object does)

`lib/research/management/exec_roster_chain.py`, tried at REQUEST time by `scoped_amgt._with_exec_roster_chain`
(`lib/research/api/scoped_amgt.py:4443-4534`) for a name whose stored management object serves no officers. Three legs in order;
the first that yields officers is served:
1. the stored company filing's officer section;
2. the research notes' management section (yields no list today, by its own docstring);
3. the Bloomberg officer list ALREADY stored (`_bloomberg_leg`, `:181-233`), newest object for the name.

For a name in the plan, legs 1 and 2 yield nothing and leg 3 reads "no Bloomberg officer list is stored for this name ...
which this page does not make" (`needs_new_pull`). So the page serves NO officers for it today, with that reason.

**After an object lands for a name, on the next request, with no deploy:**
- **A. the list parses with one or more officers** (`STATUS_OK`): the management block serves those officers with
  `roster_source: BLOOMBERG_FALLBACK`, `roster_status: UNRESOLVED-SOURCE`, role from the Bloomberg title (or
  "Officer (Bloomberg, no title returned)"), and NO role start, tenure or pool comparison. It carries the label "officers from
  Bloomberg's officer list; no filing roster could be read ...". The name leaves the plan's population.
- **B. the list is empty** (`STATUS_EMPTY`): still no officers; the reason becomes "Bloomberg's stored officer list is empty for
  this name". The name leaves the plan's population (a stored object exists).
- **C. the object cannot be used** (any other status): still no officers; the reason becomes "Bloomberg's stored officer list
  could not be used for this name".
- **D. the call fails or returns no row:** nothing lands; the page is unchanged for that name; it stays in the population.

No branch changes a name outside the plan: a name whose filing leg serves officers never reaches leg 3.

## What the act may touch (the blast radius)

- **Vendor:** at most M `reference_data` calls, M = the plan's count on the day (86 at signing), one row each.
- **Store, new keys only:** `s3://opal-data-harvest/bloomberg/harvest/bronze/exec_officers/security_key=<KEY>/<stamp>.json`
  (`store.address_of` output through `bronze_write`), a conditional put that never overwrites.
- **Served:** the management block of up to M covered names, by the rule above. No other section, no score, no stored
  management object: the chain "writes nothing" (its docstring) and the M-1 objects are not rewritten.
- **Not touched:** no Lambda, route, table, schedule or page code. The Bloomberg budget ledger is not written by this driver.

## The base, read at signing

| object | value |
|---|---|
| plan | names 86, calls 86, `calls_per_name` 1, `probed True` (both fields already served and parsed by `bloomberg_fallback.pull_exec_officers`) |
| `exec_officers` bronze today | 7 objects (the CTO's read in its ba-21 half, 09:2xZ); this seat's own read for AMD: 0 objects |
| bucket `opal-data-harvest` versioning | Enabled |
| per-name before state | every name in the plan has 0 stored objects by the plan's own rule; the name list is committed before the run (below) |

## Writers counted (NEVER-1)

`bloomberg/harvest/bronze/exec_officers/`: **N = 2 callers of ONE rule.** `bloomberg_fallback.pull_exec_officers(...,
write_raw=True)` (`:226`, reached from `enrich.py:646`) and `research_pulls.bronze_writer`; both land through
`hbloom.bronze_write("exec_officers", ...)` with the same envelope (`research_pulls._body` states it copies the fallback's). The
request-time chain calls the fallback with `write_raw=False` and writes nothing. The served management block for a plan name:
**N = 1 rule**, the chain above.

## Rollback per key

- **A landed object cannot be withdrawn without an S3 delete.** The reader takes the NEWEST object for a name, the put never
  overwrites, and there is no "absent" object to write over it. Removing a served Bloomberg list therefore means deleting that
  key's object (the bucket is versioned, so a delete is a marker and the bytes stay). That is an S3 delete: the round carries
  `no_s3_deletes: true` and CLAUDE.md reserves it to Andrew's confirmation. This half does NOT pre-authorize one.
- What stands in for rollback: the served list is labelled as Bloomberg's and as lacking role start and tenure, and a filing
  roster, when one is later read for the name, wins at leg 1 without any removal.
- A wrong PARSE (branch A serving a malformed list) is a code repair in `bloomberg_fallback`, not a store change.

## Conditions this seat sets on itself

1. **The name list first.** The plan's M names are committed to `round77/` before `run officers --confirm-calls M`.
2. **A five-name first slice, read before the rest.** `run officers --names <the first five of the plan> --confirm-calls 5`; then
   one covered name of the five is read through the handler in-process (the chain's `served.leg` and the officer count) and
   printed in the act record. Expected: leg `bloomberg`, one or more officers, or branch B's reason. If a slice name serves a list
   that is visibly not officers, the remaining names do NOT run and it comes back to the CTO.
3. **The vehicle completed today** (the ba-21 half's C1 applies here as written), and not during the 07:30 ET check.
4. CAPACITY stops the sequence; failed names are listed and NOT re-run under this half.

## Acceptance, read after the run

`plan officers` re-run: its count falls by the number of names that landed (branches A, B and C all leave the population). The
act record prints, per branch, how many of the M names landed A, B, C or D.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~09:4xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`, including the 84 against 86 call and whether
the no-delete rollback is acceptable for a served list.
