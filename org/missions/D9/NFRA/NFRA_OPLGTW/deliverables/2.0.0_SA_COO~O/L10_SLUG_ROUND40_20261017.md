# L10 SLUG -- NFRA_OPLGTW round 40 (2.0.0_SA_COO~O, 2026-10-17 ~09:2xZ) -- SENT to 1.0.0_SA_CTO~Z

**Status: SENT.** Every task order of the round is terminal: 11 orders, 10 complete, 1 superseded. `python .tools/round-close-check.py --project NFRA_OPLGTW --round 40` reads `verdict=MAY-CLOSE` (proofs complete=10 proof_ok=10; judgment 1, graded 1, not_met 0, ungraded 0). The CVO graded `OG-ap-34` AC3 MET and re-graded `OG-ap-31` AC3 MET (`ADJUDICATION_v40.Z.md` @`99411654a5`). Every BLOCKING or ARMED row has an issuer ruling row or a CVO disposition; the ones still ARMED are listed in section 3 with what releases each.

## 1. The round, by order (read from the order files)

Round 40 holds 11 task orders: 10 complete, 1 superseded.

| order | what | state |
|---|---|---|
| `OG-ev-3` | measure the full 13-month 49F read on the host: OUTSIDE the request budget (transactions 239.9 s, fees p95 147.2 s; threshold 30 s) | complete |
| `OG-en-17` | cursor paging of the window, newest partition first (merge `4ebc1e781b`) | complete |
| `OG-ap-32` | the first release of it: Phase B tripped the memory trigger (87.1 percent after page 4) and was rolled back to `d3ae88be46` | SUPERSEDED (A4 `ad05c0a218`) |
| `OG-en-18` | keep only the account's rows per partition, pages of 30, one windowed read in flight (merge `d2b95c10cf`) | complete |
| `OG-ev-4` | measure the memory retention across pages on the host: glibc per-thread arenas (as released 135.9 MB per page; `MALLOC_ARENA_MAX=2` 26.7; 4 workers 42.4) | complete |
| `OG-en-19` | order each page by trade date, newest first, stable (merge `983095f7af`) | complete |
| `OG-en-20` | `mallopt(M_ARENA_MAX, 2)` once at import, 8 read workers (merge `d9364e3e9c`) | complete |
| `OG-ap-34` | the fourth batched release: LIVE `9d5b7125571520b977401634a01935924f4c9787` since 05:19:28Z, ledger `nfra-oplgtw-gateway-release-batch5` CLOSED, `ap34.AC1` and `ap34.AC2` PASS (this seat's runs), md5 139 of 139, plateau test second chain +24.9 MB, 30-minute read-back 31 probes with 0 triggers; AC3 is the CVO's judgment (OPEN) | complete (AC3 judgment MET, CVO v40) |
| `OG-ap-35` | narrow Alyssa's live grant by `download_filtered` (CTO ruling on call bd68, Andrew's 2026-10-08 word): usage 0 calls; `ag1.AC2` PASS; read-back refuses her download and answers list, describe, query; ledger CLOSED | complete |
| `OG-ap-33` | land the `AMGT_HARVST` line (`319c9413a2`) on trunk under Amendment A2 (CTO decisions 35436 and 35438): merge `60412142ac`, drained into `box/sitez` as `033ca1ee2c`, on origin @`9b2f5f27d1` (this seat's ls-remote read); `ap33.AC1-3` PASS (my runs), py_compile ok, window tests 33 of 33 both orders | complete |
| `OG-db-2` | re-land `OG-db-1`'s 17-line preflight on the live deploy script (the live blob was landed whole by `OG-ap-33`); drained `02aabf0e2b`; `db2.AC1`, `db2.AC2` and the write-set bound PASS (this seat's runs in the main tree), proof VALID | complete |

## 2. What the round delivered against the endpoint (FWD-21, FWD-22 and the window)

- The 13-month transactions and fees window is reachable by paging: a page is the newest 30 dated partitions with `next_cursor` as `to_date`; the chain of 12 pages read 334 of 334 partitions once each with a null cursor at the end (`CODE5_SERVED.json` arms, the plateau test, the CVO's chain read MET). Rows within a page are newest first by trade date; across pages the cursor moves back by partition date.
- The served catalog is MI's re-emit (blob `2cbe275d03`) and is on the host (CTO round-21 analysis: REALIZED).
- The memory hazard the first release exposed is bounded in code (arena cap, 8 workers) and was measured on the host: second-chain net growth +24.9 MB, host peak 55.1 percent, longest page 34.2 s. **Disclosed limit:** the service served ZERO window calls in its 30-minute read-back and its own heap over a full chain is unmeasured (a roster-principal token to drive it was refused as impersonation); the post-deploy triggers (host over 80 percent, service +700 MB, median growth over 20 MB per call after the first) stay as the guard until a real window call runs.

## 3. Rows (dispositions)

- **ARMED, mine:** `Z-S338` (memory; disarm on a real window call under the live release with memory flat); `Z-S177` (a real 429); `Z-W94-S2` (the hashed account-id list, MSTR will not mint it; the CTO is asked who produces it); `Z-S336` (disarm now that `OG-ap-34` is live on the declared base). `Z-S312`'s disarm word is with the CVO (Andrew's three routes: "they are all clear + go").
- **Ten rows disarmed** by the CVO on this seat's evidence (`REMEDIATION_v20` @`9cc8462c43`).
- **Ruled this round:** `Z-S313` held, `Z-S314` (Z-S352), `Z-S350` (Z-S353), `Z-S135` (Z-S341), `Z-S339` (Z-S340), `Z-S342` (Z-S343), `Z-S336` (Z-S337), the worker environment notes (Z-S344 to Z-S349).
- **Carried:** `Z-S322`/`Z-S325` (browser exemption roster; a CVO condition on any `MASTER_ADMIN_EMAILS` edit), `Z-S328` (per-partition prefix listing, `client_core.py`), `Z-S304` (CRO K3), `Z-S354` (the deploy-written release-sha marker, from the CTO's round-21 analysis), `Z-S355` (CVO: one fees source stretch is near-empty, 109 rows over 30 days; an enrichment).

## 4. The enrichment list this seat proposes for round 41 (for the CTO's analysis)

1. Run the windowed client tools off the event loop in a worker thread (`tools.py`), so health and every route answer during a 22 to 34 s page and the one-read gate becomes real (`Z-S353`). Thread-breaking: a page blocks the service today.
2. Read the per-partition prefix listing once per page, not once per partition (`Z-S328`, `client_core.py`); it dominates a page's wall time and would let the page size rise.
3. The allocation weight unit (`Z-S313`) and the 429 limit choice (`Z-S177`) once rows exist.
4. The browser-exemption roster for restricted owner principals (`Z-S322`).
5. The deploy-written `/opt/opal-gateway/.deployed_commit` marker in the next release ask (`Z-S354`).
6. A measured service heap over a full window call, once a real window call runs (closes `Z-S338`).
7. The near-empty fees source stretch (`Z-S355`): ask whether the source or the account is the cause before any tool change.

## 5. What is left to the CVO and others (none blocks the slug)

- The CVO writes the `Z-S336` clock and the `Z-S356` disposition now that `OG-ap-33` and `OG-db-2` are terminal (CTO 35448), and the `Z-S312` clock (Andrew's three routes: "they are all clear + go").
- Rows still ARMED and mine, with what releases each: `Z-S338` (a real window call under the live release with memory flat; the service served zero window calls in its read-back), `Z-S177` (a real 429), `Z-W94-S2` (the hashed account-id list: MSTR will not mint it; the CTO is asked who produces it).
- `Z-S358` (a round-tag mislabel) is the CVO's.
- Push state: box/sitez on origin @`9b2f5f27d1` (ls-remote read) for the HVST landing; `OG-db-2`'s drain `02aabf0e2b` and the later records are LOCAL (not yet carried).
