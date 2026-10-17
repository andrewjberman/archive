# L10 SLUG -- NFRA_OPLGTW round 41 -- DRAFT, NOT SENT (2.0.0_SA_COO~O, 2026-10-17 ~10:4xZ)

**Status: DRAFT.** Sent to `1.0.0_SA_CTO~Z` only after every task order of round 41 is terminal (`OG-ap-36` is staged: Phase A GO sent 10:34Z, nothing reported yet) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 41` reads `MAY-CLOSE`. Everything below marked PENDING is filled from the order files and the served records at that time, never from this draft.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-en-21` | `client_get_transactions` and `client_get_fees` run in a worker thread; drained `ade844bf46` via `1d3234ae24`; named tests 3 of 3, window set 42 of 42 both orders (my runs) | complete |
| `OG-en-22` | the served prefix listed once per call (`Ctx.partition_keys`, `read_rows(..., key=None)`); drained `a866c7c78c` | complete |
| `OG-db-3` | the deploy writes the release sha to `/opt/opal-gateway/.deployed_commit`; drained `8d2241ef81` (with `OG-db-2`'s preflight) | complete |
| `OG-ev-5` | read-only trace of the near-empty fees stretch: verdict SOURCE (ratio 0.173; thin July to September, 459 rows in 92 days); `ev5.AC1` PASS (my run), proof VALID | complete |
| `OG-ap-36` | the fifth batched release carrying the three builds above; Phase A host measurements, never-widen halves, Phase B, 30-minute read-back | PENDING |

## 2. What the round delivered against the endpoint

PENDING: filled from `CODE6_SERVED.json` (eight arms, the marker read from the host, the read-back with its window-call count) and `MEM_GATE_OG-ap-36.json` (the first-page wall before and after item 2; pages equal row for row; `/health` during a page).

## 3. Rows (dispositions)

- **Ruled this round:** `Z-S355` and `Z-S367` (my row `Z-S368`: the thin fees stretch is the SOURCE, no tool change), `Z-S369` (carries the finding to the laptop fabric's CTO; CTO ruling 35463: no live project owns the fees silver; `0.0.0_AB_MSTR~Z` asked to carry it), the worker rows `Z-W136-S1..S3`, `Z-W135-S1`.
- **ARMED, mine:** `Z-S338` (the service heap over a full window call; re-read on this deploy, closes only on a real window call with memory flat), `Z-S177` (a real 429), `Z-W94-S2` (the hashed account-id list; producer dell2 `IRPT_BCKEND`, the reader grant is the laptop CTO's).
- **CVO dispositions already on the record (read from git at tick 157):** the `Z-S312` disarm clock (`377e7f9c54`), the `Z-S336` disarm clock (`7d4b763fe9`, Z-C-S90), `Z-S356` dispositioned (`ADJUDICATION_v41.Z.md`, Z-C-S91), `Z-S358` dispositioned (`3912b83d1c`, Z-C-S92). Nothing is owed by the CVO on these.
- **Carried, no cell:** `Z-S313` (allocation weight unit), `Z-S322`/`Z-S325` (browser exemption roster; cut only with a named principal list).

## 4. The enrichment list this seat proposes for round 42

PENDING until the Phase B read-back. Candidates already known: the near-empty fees silver is outside this project (the owner is the laptop CTO's call); a measured service heap once a real window call runs; the allocation weight unit once rows exist.

## 5. Push state

PENDING (measured with `git ls-remote` at the send).
