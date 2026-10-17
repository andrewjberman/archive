# L10 SLUG -- NFRA_OPLGTW round 41 -- DRAFT, NOT SENT (2.0.0_SA_COO~O, 2026-10-17 ~10:4xZ)

**Status: DRAFT.** Sent to `1.0.0_SA_CTO~Z` only after every task order of round 41 is terminal (`OG-ap-36`: Phase B running since 16:57Z; `OG-ap-37`, the lineage landing of dell1's release commit, is cut and staged) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 41` reads `MAY-CLOSE`. Everything below marked PENDING is filled from the order files and the served records at that time, never from this draft.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-en-21` | `client_get_transactions` and `client_get_fees` run in a worker thread; drained `ade844bf46` via `1d3234ae24`; named tests 3 of 3, window set 42 of 42 both orders (my runs) | complete |
| `OG-en-22` | the served prefix listed once per call (`Ctx.partition_keys`, `read_rows(..., key=None)`); drained `a866c7c78c` | complete |
| `OG-db-3` | the deploy writes the release sha to `/opt/opal-gateway/.deployed_commit`; drained `8d2241ef81` (with `OG-db-2`'s preflight) | complete |
| `OG-ev-5` | read-only trace of the near-empty fees stretch: verdict SOURCE (ratio 0.173; thin July to September, 459 rows in 92 days); `ev5.AC1` PASS (my run), proof VALID | complete |
| `OG-en-23` | repair of the `OG-ap-36` Phase A stop (row `Z-S370`): `Ctx.read_account_rows` applies the 49F fence and the account test in arrow and converts only the account's rows; drained `83c8c75f83`; my runs named 3 of 3, eleven-file window set 39 of 39 both orders, proof VALID | complete |
| `OG-en-24` | `client_core._answer` keeps the adapter's `absent_reason` (rows `Z-S372`, the CVO's `Z-S373`: a refused windowed call and the five `no_partition_at_as_of` refusals were nulled in the live release); built by worker `~138`, drained `ec8e21a6d0`; my runs named 3 of 3, twelve-file window set 42 of 42 both orders, proof VALID; eight codes now surface (ruling row `Z-S374`) | complete |
| `OG-ap-36` | the fifth batched release (the windowed tools off the loop, the arrow-side account filter, the prefix listed once per page, the host marker, the reason words no longer nulled): Phase A re-run PASSED on release `efcc8ae19f` on dell1's live ref; Phase B: LIVE 2026-10-17T17:06Z, ledger `nfra-oplgtw-gateway-release-batch6` CLOSED 18:11:52Z; `ap36.AC1` and `ap36.AC2` PASS on my runs (served read 26 of 27 with the named exception `etfs_compare_peers`, row `Z-S375`); read-back 2: 0 triggers, zero window calls; the ledger closed before the CVO's clock condition was read (the read was normal; recorded in ruling row `Z-S376`) | complete |
| `OG-en-25` | the Z-S375 repair, first part: a typed Parquet in-memory cap on the filtered table and Arrow filters for `etfs_compare_peers`; worker `~139`, drained `a197c3fc38`; my runs named 3 of 3, 29 of 29 both orders (ruling row `Z-S377`) | complete (its host measurement stopped at `OG-ap-38` Phase A: the whole object was still read before the cap) |
| `OG-un-1` | a memory ceiling on the gateway unit (`MemoryHigh=1200M`, `MemoryMax=1400M`, `OOMScoreAdjust=300`); worker `~140`, drained `a6788723f3`; my runs named 2 of 2 | complete |
| `OG-ap-37` | landing dell1's release commit `1753c741d9` on trunk (lineage only, trunk's side on two conflicts); drained `09cae34ff0`; `ap37.AC1`/`AC2` PASS on my runs (ruling row `Z-S379`) | complete |
| `OG-en-26` | the Z-S375 repair, second part, after `OG-ap-38` Phase A stopped (row `Z-S380`: candidate peak 724 MB, the whole object read before any filter): a filtered read streams by batch, an unfiltered one is refused from the footer, the peer tables' lineage column is measured never loaded; worker `~141`, drained `725714077a`; my runs named 3 of 3, 32 of 32 both orders (ruling row `Z-S381`) | complete |
| `OG-ap-38` | the sixth release (`OG-en-25`, `OG-en-26`, `OG-un-1`; five files) repairing the ARMED hazard `Z-S375`: Phase A under a hard guard stopped once (row `Z-S380`); re-run GO 35557 sent 21:00Z on trunk `bae898b6a7`; never-widen halves, Phase B, a 27-of-27 served read under the guard, the clock read before the ledger closes | PENDING |

## 2. What the round delivered against the endpoint

PENDING: filled from `CODE6_SERVED.json` (nine arms, the harvest_research.py host md5 equal to its 1753c741d9 blob, the marker read from the host, the read-back with its window-call count) and `MEM_GATE_OG-ap-36.json` (the first-page wall before and after item 2; pages equal row for row; `/health` during a page).

## 3. Rows (dispositions)

- **Ruled this round:** `Z-S355` and `Z-S367` (my row `Z-S368`: the thin fees stretch is the SOURCE, no tool change), `Z-S369` (carries the finding to the laptop fabric's CTO; CTO ruling 35463: no live project owns the fees silver; `0.0.0_AB_MSTR~Z` asked to carry it), the worker rows `Z-W136-S1..S3`, `Z-W135-S1`.
- **Carried to the laptop CTO (ruling at `RULINGS_PARKED_BUS_ITEMS_20261017_1350Z.md` section 3, relays 35496 and 35497):** `Z-S369` (the thin fees silver) is ruled RECORD THE GAP, no re-pull now; the laptop CTO holds `bd-49f-fees-runner` while `ADVI_49FSRC` is closed; its read-only probe compares the REST fees count with the silver count for 3 sample days inside 2026-08-17 to 2026-09-15 (equal: closes as RECORDED; higher: a re-pull under a never-widen pair). The row stays open with the laptop CTO as owner until the probe result arrives; the CVO dispositions it on that result. The gateway does nothing. My row `Z-S368` is dispositioned.
- **ARMED, mine:** `Z-S338` (the service heap over a full window call; re-read on this deploy, closes only on a real window call with memory flat), `Z-S177` (a real 429), `Z-W94-S2` (the hashed account-id list; producer dell2 `IRPT_BCKEND`, the reader grant is the laptop CTO's).
- **CVO dispositions already on the record (read from git at tick 157):** the `Z-S312` disarm clock (`377e7f9c54`), the `Z-S336` disarm clock (`7d4b763fe9`, Z-C-S90), `Z-S356` dispositioned (`ADJUDICATION_v41.Z.md`, Z-C-S91), `Z-S358` dispositioned (`3912b83d1c`, Z-C-S92). Nothing is owed by the CVO on these.
- **Carried, no cell:** `Z-S313` (allocation weight unit), `Z-S322`/`Z-S325` (browser exemption roster; cut only with a named principal list).

## 4. The enrichment list this seat proposes for round 42

PENDING until the Phase B read-back. Candidates already known (the CTO ranks them):
1. A rise of the window page size: a page now reads in about 2 s against about 30 s, so 30 partitions per page is no longer the binding limit (a later cell, measured, never assumed).
2. `test_og_db3.py::test_ogdb3_ac03` reads git history and fails in a release tree (a test defect carried by name); make it read the worktree.
3. A measured service heap once a real window call runs (closes `Z-S338`; organic case only).
4. The allocation weight unit (`Z-S313`) and the 429 limit choice (`Z-S177`) once rows exist; the browser-exemption roster (`Z-S322`/`Z-S325`) with a named principal list.
5. The eight `absent_reason` codes that now surface (`OG-en-24`): whether any caller or the CVO's reading wants a documented list of them in the catalog.
6. `safe-merge.sh --continue` refuses a merge that stages no files (a lineage-only landing such as `OG-ap-37`; the drain's fast lane accepts the same shape): a `--lineage-only` flag for the script's owner (`0.0.0_AB_MSTR`), not urgent (row `Z-S378`, ruled in `Z-S379`).
7. The thin fees silver belongs to the laptop CTO (the probe is theirs); no gateway cell.
Lessons for the record (not rules): the first Phase A stop was a whole-partition Python conversion hidden behind an off-loop wrapper (the loop stayed starved by the GIL even after the move); an issuer who relaxes a limit after a failed measurement ships the defect, so the limits stayed and the cause was fixed; an idle seat reads mail at its own watcher re-arm, and a failed `unstick` is not a stall.

## 5. Push state

PENDING (measured with `git ls-remote` at the send).
