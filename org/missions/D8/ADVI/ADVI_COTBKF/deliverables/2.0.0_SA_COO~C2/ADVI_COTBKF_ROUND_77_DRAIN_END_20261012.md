# L8 drain end -- ADVI_COTBKF round 77: no reader was found serving a figure built from an AFFECTED close; 47 served holdings partitions do carry the store's close, on dates where it is not affected; all 15 failing funds hold an unadjusted close locally; two list entries merged into one defect

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-12 ~00:53Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB77by1-AC2, CB77by3-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-77 analysis @1101e06fcd (the hash read from the file's own history), and two rulings inside the
round: msg 6196 and msg 6213. **Issued:** @363c94c9cc, 4 cells; re-cut twice by MODIFICATION (@f3afa0b887, @e69224f87e).
**Nothing was fetched, served, applied or re-minted. Read-only calls were made against this project's firm's bucket and three
resources; every one is listed in section 5.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-by-1 | who reads the affected closes | ~143 | complete @9aeceaf6a7, drained | `CLOSE-READERS failing_funds=15 stores=2 funds_placed=15 readers=19 classed=19 serving=1 one_read=1 serving_from_an_affected_close=0 rows_filed=0 denominators=18` (serves_nothing 15, not_established 3, serves_a_value 1) |
| CB-by-2 | the 15 failing funds listed (direct-act) | ~144 | complete @edea4464f2, drained | `FAILING-FUNDS funds=15 listed=15 held_in_cache=15 held_in_fetch_folder=0 none_held=0 held_sum=15 held_series_passes=14 held_series_fails=0 held_series_too_few_trades=1` |
| CB-by-3 | the no-snapshot branch read (AMENDMENT 1), and the level error where served | ~145 | complete @ca72e263fe, drained | `NO-SNAPSHOT-BRANCH first_snapshot_date=2026-06-08 partitions_before_it=47 still_exist=True ... page_accepts_an_earlier_date=False request_made=False failing_funds_held_before=7 served_from_an_affected_close=False readers_not_established=3 rows_filed=0` and `LEVEL-ERROR census_serving_from_an_affected_close=0 served_readers_from_cell_1=0 sized=0 unsized=0 sum=0` |
| CB-by-4 | the correction list, two entries merged (direct-act; AMENDMENTS 1 and 2) | ~146 | complete @ea54306ecb, drained | `OPEN-CORRECTIONS-RECORD revisions=7 record_absent=0 merged=True old_ids_left=0 corrections=6 keys_complete=True merged_from=dividend-adjusted-fund-series,trade-day-valuation carried=True readers_key=True evidence_rows=43 unreconciled=40` |

No product code changed (records and no channel row this round), so the suite was not re-run: it stands at `1020 passed, 12 skipped`.

## 1. For L9: CB77by1-AC2 (the census of readers)

**The store.** All 15 failing funds are read from one store, the firm's silver canonical prices, by ticker. Its writer is not in the
live step list and its owner is not established (the projects that built it are closed).

**The census.** 18 sweeps, each with its denominator in the record (the widest: one term over 93,200 files; the portal by two
instruments, 2,049 and 2,069 files), and the tool's census verb run on four trees before a zero was read as an absence. **19 readers:
15 serve nothing, 3 not established, 1 serves a value** -- the cot holdings builder, which feeds the firm's advisor-intelligence page.
**No reader was found serving a figure from an affected close; no row was filed.**

**The one serving reader, read by the issuer in the code as well:** with a holdings snapshot present it prices each holding at the
custodian's market value over units (`B_00.canonical_holdings.py:163-173`) and returns (`:1116-1121`) BEFORE the price store is
loaded (`:1145`). So the census's "does not use the store's close" is true of its live branch only. That is what section 2 reads.

**For the grade:**
- What the census could not see, in its own words: deployed cot gold code as against the repository copy; consumers that fetch the
  firm's gold through an API without naming the store; exports; the live catalog.
- Its reading of `A_03.positions_cube` (live, reads the store) as serving nothing rests on nothing live reading its output.
- The relayed claim that no IRPT_BCKEND surface names the store holds by code; two IRPT_BCKEND analysis scripts do name it.
- A latent finding, the worker's: this project's own build output is minted as a table of 3,325 days with 0 readers; the first
  reader built on it would serve figures from these closes.
- Three comp-rail denials, each re-run in the form the rail printed.

## 2. For L9: CB77by3-AC2 (the no-snapshot branch, and the level error where served)

**Ruled into the round by the CTO (msg 6196) on this seat's question.** The first snapshot is 2026-06-08 (a complete listing of 87
snapshot keys). **47 holdings partitions dated 2026-04-22 to 2026-06-07 still exist and were built on the no-snapshot branch:** the one
partition read (2026-06-03) has 8,164 of 8,164 rows with source `bd`; all 47 were last written in one run on 2026-06-09. **They are
served:** the page takes no date, but its period series is built by live steps from every partition with no filter on source (the
issuer read `C_03.account_performance.py:199-226` itself: every key, the market value summed).

**And the close is not affected on those dates.** For the 15 funds the store's close over the unadjusted close across that window is
0.9845 to 1.0061, median 1.0000, over 480 fund-days, none below 0.98; one price read (FCNTX, 2026-06-03) gives 26.35 in the served
holdings, in the store and unadjusted. **So no served figure carries the three-quarters error.** The level error sized where served:
0 readers; an empty result, reported as one.

**For the grade:**
- **7 of the 15 funds were matched as held** on the date read (by asset name through a local bridge: the partition's ticker column is
  empty); 3 have a name and no row that day; 5 have no name in the bridge. "Held on any such date" is between 7 and 15.
- **46 of the 47 early partitions were not opened;** the branch that built them is read from one partition's rows and from the
  listing's last-written times for the rest.
- **The store read is a local copy of 2026-10-08,** not the store as it stood when the partitions were written.
- The CTO's sentence on why this holds, for the record: an adjusted series sits near the traded price close to the present and falls
  away going back; those partitions are right today, and a REBUILD of them from a later copy of the store would not be. Nothing in
  the tree prevents such a rebuild; the list carries that as unreconciled, for the CTO.
- The level by fund, as a proportion (served close over unadjusted close): medians from 0.5647 to 0.9179; 12 of 15 funds have a
  2026 median of 1.0.
- In this project's minted, UNREAD table (labelled not served): 259,357 account-days in 407 accounts hold one of the 15 funds at a
  value; the funds' share of the account's valued total has a median of 0.2276 and exceeds 25 percent on 43.1 percent of them.
- AWS reads made by the worker: two listings and one object, this firm, read-only. Two comp-rail denials; it switched to the native
  tools.

## 3. The 15 failing funds (direct-act)

All 15 hold an unadjusted close in the local cache, 2020-06-29 to 2026-10-08, covering every held trading day of the build; none
needed the round-74 fetch. Against the price paid: 14 pass under round 76's rule, 0 fail, 1 too few (VGHAX). Nine reproduce the price
paid on every trade unit; five pass partly through the rule's allowances (plain within-1-percent shares: VEIRX 0.79, PCBIX 0.98,
SGIIX 0.91, PRILX 0.62, AGTHX 0.70). 8 are validated by reinvestment, 7 unreadable by it.

## 4. The three readers the census left not established -- read by the ISSUER, on the CTO's ruling (msg 6213)

Record: `deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_77_THREE_READERS_READ.json` @e69224f87e. Made by this seat and not by a cell:
the gate takes one issuance per round, a re-cut must modify an existing order, and the one cell these reads fit was terminal.
- **The tax panels:** the view object is absent (a 404, with a positive control: the same call on a key that exists returns it) and
  the holdings-lots prefix holds 0 keys. Serves nothing built from the store.
- **The holdings-performance channel:** both live schedules are ENABLED and name two other sources; nothing scheduled fires it for
  this firm. A manual invocation is not excluded by a schedule read.
- **The performance route:** the adapter is Active and carries a tenant for this firm, a vendor pass-through that does not name the
  store (0 hits in its folder of 155 files). **CARRIED, needs a window:** whether a portal page opens that route for this firm's
  logins; what its data-plane prefix holds was not opened.
The second schedule belongs to another firm's channel: its state and the source key in its input were read; none of its data.
**This record is the issuer's own and is not graded by a criterion of the round.**

## 5. How the round was amended, and every remote read

- **Two re-cuts, both by MODIFICATION.** A first attempt to add a fifth order for the no-snapshot read was REFUSED by
  `to-pipeline-gate` ("ONE ISSUER PER ROUND is keyed to the ROUND ... A re-cut into the first issuance MODIFIES its orders and adds
  no file ... this limb reads no override"). Not overridden; the refused files were put back. The read was folded into CB-by-3
  (one mechanical criterion added, its judgment clause extended) and CB-by-4 was made to carry the new records. Each modification
  was graded by GATE (viii), as the gate printed.
- **Two workers stopped by the issuer** before any commit, each because its order was amended under it: CB-by-3's first (eight
  minutes in) and CB-by-4's first (one minute in). Both branches held 0 commits; each cell was re-run on the amended face.
- **Remote reads, all read-only, this firm:** by ~143, none beyond the graph (its one read came from code); by ~145, a listing of
  the snapshot prefix, a listing of the holdings prefix, one object; by the issuer, head-object twice, one listing of one prefix,
  get-schedule twice, get-function-configuration once.

## 6. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 7, six entries)

`dividend-adjusted-fund-series` and `trade-day-valuation` are ONE entry, `adjusted-close-used-as-price`, `state` `OPEN`. The worker's
own check: both former extents carried whole under `holdings` and `trade_days`; evidence 23 + 14 + 6 new = 43; unreconciled 12 + 8 +
6 new = 26, no exact duplicate; `LOSSLESS extents=True evidence=True unreconciled=True`. The issuer ran the record's line and did
not re-verify the merge row by row. Floor 19 and ceiling `NOT_MEASURED` stand. 40 unreconciled items in all. No PRD addendum past
v0.7 exists.

## Where this leaves the project

- **Served:** no figure built from an affected close was found, by a census with its limits and two ruled reads. One reader is
  carried (a portal page binding, needing a window).
- **Latent:** the served holdings before 2026-06-08 are right only as written; and this project's minted table, unread, holds the
  15 funds at the affected close on 259,357 account-days.
- **In hand for a correction:** an unadjusted close for all 15 failing funds, 14 of which reproduce the price paid.
- **Not decided here, the CTO's:** the fund-basis addendum, now that what is served is read; whether the 47 early partitions are
  protected from a rebuild; whether the carried reader gets its window; the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the two judgment criteria are graded.
