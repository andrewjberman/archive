# L10 SLUG -- NFRA_OPLGTW round 41 -- DRAFT, NOT SENT (2.0.0_SA_COO~O, 2026-10-17 ~10:4xZ)

**Status: DRAFT.** Sent to `1.0.0_SA_CTO~Z` only after every task order of round 41 is terminal (`OG-ap-36` is staged: Phase A GO sent 10:34Z, nothing reported yet) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 41` reads `MAY-CLOSE`. Everything below marked PENDING is filled from the order files and the served records at that time, never from this draft.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-en-21` | `client_get_transactions` and `client_get_fees` run in a worker thread; drained `ade844bf46` via `1d3234ae24`; named tests 3 of 3, window set 42 of 42 both orders (my runs) | complete |
| `OG-en-22` | the served prefix listed once per call (`Ctx.partition_keys`, `read_rows(..., key=None)`); drained `a866c7c78c` | complete |
| `OG-db-3` | the deploy writes the release sha to `/opt/opal-gateway/.deployed_commit`; drained `8d2241ef81` (with `OG-db-2`'s preflight) | complete |
| `OG-ev-5` | read-only trace of the near-empty fees stretch: verdict SOURCE (ratio 0.173; thin July to September, 459 rows in 92 days); `ev5.AC1` PASS (my run), proof VALID | complete |
| `OG-en-23` | repair of the `OG-ap-36` Phase A stop (row `Z-S370`): `Ctx.read_account_rows` applies the 49F fence and the account test in arrow and converts only the account's rows; drained `83c8c75f83`; my runs named 3 of 3, eleven-file window set 39 of 39 both orders, proof VALID | complete |
| `OG-en-24` | `client_core._answer` keeps the adapter's `absent_reason` (rows `Z-S372`, the CVO's `Z-S373`: a refused windowed call and the five `no_partition_at_as_of` refusals were nulled in the live release); worker `~138` | PENDING (building at 13:30Z) |
| `OG-ap-36` | the fifth batched release carrying the builds above; Phase A re-run PASSED (chain +1.7 MB per page, first page 29.75 s to 1.93 s, `/health` 0.033 s during a page, 6 of 6 pages equal); three halves signed on release `948e8b47cc` then superseded by `OG-en-24`'s release; CT1 repeat, re-sign, Phase B, 30-minute read-back | PENDING |

## 2. What the round delivered against the endpoint

PENDING: filled from `CODE6_SERVED.json` (eight arms, the marker read from the host, the read-back with its window-call count) and `MEM_GATE_OG-ap-36.json` (the first-page wall before and after item 2; pages equal row for row; `/health` during a page).

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
6. The thin fees silver belongs to the laptop CTO (the probe is theirs); no gateway cell.
Lessons for the record (not rules): the first Phase A stop was a whole-partition Python conversion hidden behind an off-loop wrapper (the loop stayed starved by the GIL even after the move); an issuer who relaxes a limit after a failed measurement ships the defect, so the limits stayed and the cause was fixed; an idle seat reads mail at its own watcher re-arm, and a failed `unstick` is not a stall.

## 5. Push state

PENDING (measured with `git ls-remote` at the send).
