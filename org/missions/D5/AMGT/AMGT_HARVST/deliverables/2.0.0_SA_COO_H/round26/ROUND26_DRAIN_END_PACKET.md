# AMGT_HARVST ROUND 26 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~07:5xZ

**Issuance:** `dd85531321`, four orders over `ROUND_ANALYSIS.round25.md` @`300ea99310` (decomp section 38 and its addendum).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.

**Class: SERVED / WORLD.** Two gold rebuilds ran under signed pairs, with no vendor egress this round.

**Round-25 ruling 1 applied to every WORLD half.** Each half names the command that reaches the put and the config defaults,
and gives a stub put-count. Both halves' stub dry runs captured exactly 1 put, and both writes matched them.

## 1. FOUR ORDERS, ALL TERMINAL

| order | class | drained | status | instance |
|---|---|---|---|---|
| `p-1` mention rebuild | WORLD, pair `5b407d86a1` / `c698bf6ad0` | `ab11e2c48a` | complete | VALID |
| `p-2` FWD-3's two rows | LOCAL | `2023d17e46` | complete | VALID |
| `p-3` part (a): `chatter_daily` rebuild (split per CTO ruling, msg 27005) | WORLD, pair `e7eb9100ea` / `f12ec1564a` | `c2b1a57ebd` | complete | VALID |
| `p-4` why ft/barrons refuse | LOCAL, no request | `81fd5632c2` | complete | VALID |

**Close run** (`round26/close_run_round26.py`, at trunk `0640ed5a0c`): **9 of 9 re-runs rc 0.** No tracked file was rewritten.

**`p-3` part (b)** (the span-bearing run) **is carried to round 27 as its first cell.** `to-pipeline-gate` refuses a second
round-26 issuance. Its COO half and checks are signed at `round26/NEVER_WIDEN_HALF_COO_P5.md` @`dadba8badd`.

## 2. WHAT MOVED ON THE SERVED PLANE (measured; the CTO grades)

| FWD | this round |
|---|---|
| **2 (and the ANDREW-DIRECT count)** | **`article_security_mention` rebuilt** (`part-20260930T062354Z`): 358 rows, **304 of 304 kept byte-identical**, 54 NEW (sa 6, wsj 48). `mention_count` is present on every row, and Lenovo goes from 32 to 43 pairs. **The deployed `/timeline/day`** for 992_HK on 2026-02-13 serves a NEW wsj article with `mention_count` 1 (`~66/p1_deployed_day_read.json`). **bbg adds 0:** `o-5`'s 11 bbg rows are empty in silver (row `Z-S44`, a repair before FWD-3 per the CTO's `p-1` half). |
| **3** | **Both owed rows are answered** (`p-2`). `bbg:NM5NLQ6K50XZ01` was rejected on purpose (`short_or_partial_body`) but counted as fetched; the run record now names every fetched key's outcome (stored / rejected / not stored). The wsj URL-vs-UUID split: the run record now carries `keys_stored_join`. 12 tests and 5 mutants; 207 passed. |
| **7** | **`chatter_daily` rebuilt** (`part-20260930T072527Z`): 52,143 rows, and the digest equals the signed digest. Lenovo is DENIED -> PARTIAL on 271 days (273 of 273 PARTIAL), from `o-5`'s bbg listing spans. 43 `articles_total` rows move (`p-1`'s pairs), and 191 rows were added for 09-30. **The deployed `/timeline` for 992_HK** serves all 273 days PARTIAL, `publishers_covered_codes` `[bbg, wsj]` (`round26/p3a_deployed_timeline_read.json`; the CTO's condition 3, run by the issuer because the dispatch omitted it). RESOLVED stays 0 of 191 by the guard's rule. **FWD-7's denominator** is ruled on CRO~Z's five conditions (msg 27011), and round 27 = eligibility census, then code, then the gold flip. |
| **1 / 9** | **Why ft and barrons refuse** (`p-4`, 0 network calls). **barrons:** the saved session was logged out; the reauth was followed by a DataDome 401, and `worker.py:393` refuses the contracted repair after a same-job reauth. B1 is a run on Andrew's word; B2 is one guard edit. **ft:** 403 with the request unchanged since the 09-15 200s. The cause cannot be separated because the 403 body is never kept. F1 keeps it; F2 (credential re-harvest) needs Andrew; F3 (an edge block) is outside R-21. |

## 3. ROWS THIS ROUND

- **Issuer row `Z-S44`** (bbg silver empty): UNDER_INVESTIGATION.
- **INERT:** `Z-W66-S1` (the day envelope reads DENIED beside served articles, the pre-rebuild daily), `Z-W67-S1`,
  `Z-W68-S1` (`<expect>` is read as a regex: literal parentheses never match), `Z-W69-S1` and `Z-W69-S3`.
- **`Z-W69-S2`** (ARMED: a logged-out barrons start always fails): disarmed, because no signed act includes barrons.

## 4. FOR ROUND 27 (the CTO's list; not cut here)

1. `p-3` part (b), the span-bearing run. Its half is signed; it gets re-measured at the cut.
2. FWD-7: the eligibility census, the code under CRO~Z's five conditions, and the gold flip under a pair.
3. Repair `Z-S44`, so bbg's as-received articles parse into silver.
4. barrons B2, the guard edit, and ft F1, keeping the 403 body. Each run is Andrew's word.

## 5. FOR L9

All criteria are mechanical. The FWD grades are the CTO's at L10.

**Disposable worktrees:** `wk-hvst-r26-66` to `-69`, plus the r24 and r25 sets. Branches are kept; removal waits on
Andrew's go.
