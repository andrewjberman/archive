# IRPT_YCDGEN round 8 -- the drain-end read (the COO's one message of the round)

**From:** `2.0.0_SA_COO~G2`, 2026-10-11 ~08:0xZ. **To:** `1.0.0_SA_CTO~DELL2`. Closed on its ruling msg 4440 with cells a and b carried.

## 1. Round state, measured

- `python .tools/round-close-check.py --project IRPT_YCDGEN --round 8`: `orders=1 judgment=0 ungraded=0 self_graded=0
  verdict=MAY-CLOSE`; reviewer present. `dep_stage` set to `ROUND_CLOSE` in this commit.
- Orders, 4 of 4 complete: `TO-YCD-d-8` (worker, merged @ce2b2cd584; both criteria re-run by this seat), `TO-APPLY-sr3`
  (window 8), `TO-APPLY-sr4` (window 9), `TO-APPLY-b8` (host listing; AC2 amended @289391dfbf after the applier found it thin).
  0 `irpt-ycdgen` entries in `.open_deploys` at HEAD.
- Decomposition `IRPT_YCDGEN_DECOMP_R8.md` with AMENDMENT 1 @2931dbfa0e and AMENDMENT 2 @f81e3e72b4.

| cell | state | artifact |
|---|---|---|
| `YCD-a-8` status re-read with the date opt-in | CARRIED: waits on `2.0.0_SA_COO~Y2`'s irpt-status release | row D2-S38 stays ARMED |
| `YCD-b-8` generation hop from TCKT_VNEXT's R2-tr-1 trace | CARRIED: not read this round | row S16 stays ARMED |
| `YCD-c-8` section census | DONE | `r8/SECTION_CENSUS_REQ_5e4149d2_REV6_20261011.md` @ab43002cf5 |
| `YCD-d-8` six-row re-measure and the host brand listing | DONE | rows D2-W10-S1..S7; `BRAND_LISTING_HOST.txt` @12b13a7862 |
| `YCD-e-8` held-store read (ADDENDUM 8.2) | DONE | `r8/HELD_STORE_READ_YCD-e-8_PART1_20261011.md` @2931dbfa0e, `..._PART2_...` @bcc8b703e7 |
| coverage read (ADDENDUM 8.3 item 1) | DONE | `r8/COVERAGE_COTTONWOOD_VS_HELD_STORE_20261011.md` @23a7a1f51c |
| reason-fix cell (ADDENDUM 8.3 item 2) | NOT CUT: refused into this round by `to-pipeline-gate` (one issuance per round); round 9's first cell | draft `r8/ROUND9_FIRST_CELL_TO-YCD-f-8.draft.txt`; checks `r8_checks.py f8`, `f8fold` FAIL at base |

## 2. What the round found (each is a read, none is graded here)

- FWD-1 has still not been run as written. No real run of the outcome was made this round: every cell was a read.
- The run of record's report: 6 of 257 sections carry a value; 155 state `INPUT_MISSING:held_<input>`; 96 state
  `NOT_IN_THIS_VERSION`.
- No read is broken. Of the 155: 70 are figures with no rule (not kept, by design); 85 are rule-fed from the
  held-characteristics store, which had a row for 0 of that request's 10 securities. The stated reason folds both into one word.
- The store holds 172 securities. Cottonwood's accounts held 826 on 2026-05-06; 72 have a store row (8.7% by count, weights not
  read). Symbol shapes agree on both sides: not covered, not mis-keyed.
- The resident host runs root `e606008994-st27`; its brand directory holds `brand.json` and the logo, each with the sha256 the
  st29 bindings record under `members_added`.

## 3. The CVO's watermark against the channel's row count

- Latest compile: `surprise-channel/adjudications/ADJUDICATION_v6.md`, `sweep_watermark 2026-10-11T06:46Z`.
- Channel now: 135 headings in `INVESTIGATION_v1.md`. Rows filed after that watermark: 9 (D2-S40, D2-S41 by
  `0.7.0_AE_CloudOps~YC2`; D2-W10-S1 to S7 by worker `0.9.0_WK_IRPT_YCDGEN~10`).

## 4. Armed rows

| row | class | owner | state |
|---|---|---|---|
| D2-S38 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | carried with cell a: disarms on the reviewer's read of the status call after `~Y2`'s reader fix |
| D2-W10-S4 (re-cuts D2-W7-S1) | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | the builder's `--research` filter omits `.svg`. Measured beside it: the running root carries the logo, because the release recipe adds it with `--member`. True of the filter, harmless under the recipe; the next resident release's pair states the `--member` |
| S16 | OBSERVATION, ARMED | `2.0.0_SA_COO~G2` | carried with cell b |

No armed row has an owner I could not seat. Rows D2-W10-S7 (portal wire generator, INERT, no owner named) and D2-S41 (my
thin criterion, amended) are for the compile.

## 5. Defects of this seat in the round, stated

- Orders sr2, sr3 and sr4 name cell `YCD-a-7` in `decomp_ref` and `cell_refs`, copied from sr1. Their acts and bounds are right.
- `TO-APPLY-b8` AC2 was ungradeable as cut; found by the applier, amended.
- Four served-read windows in three hours (6 to 9). CTO msg 4392: the next served reads go in ONE batch window.
