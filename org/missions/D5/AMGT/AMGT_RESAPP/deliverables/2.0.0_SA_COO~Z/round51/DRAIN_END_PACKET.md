# AMGT_RESAPP round 51 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.59, issuance `77712167dc`, on the CTO's round-50 analysis `debbec1907` (cell 3 re-homed
`7708a8506f`). Seven orders, all terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| zz-1 the union inside `write_pool` | LOCAL | ~180 (x2: continue failed, fresh worker) | drain `5b55a4ee1d` | AMENDMENT 1 `4c5ece565e` (row Z-W180-S1: the schema's closed `denominators` refused the carry counters, and had refused yy-6's CLI carry since round 50). AC1 both writers keep a planted served record, AC2 237 of 237 digest-equal, AC3 141 passed; issuer re-ran AC1; VALID |
| zz-2 `price_axis_pull` derives its root | LOCAL | ~181 (worker-light) | drain `4e20b3c55e` | AC1 0 literals, 0 sys.path entries outside the checkout; AC2 10 passed; issuer re-ran AC1 in its tree and on CLOUD; VALID |
| zz-4 content diff + scoped stamp + restamp | WORLD (path floor; nothing applied) | ~183 | drain `b113807360` | AC1 `--check` rc 0 with the four constants byte-equal; AC2 unrelated edit UNCHANGED / amgt-row edit CHANGED; AC3 content diff names the one mutated file; issuer re-ran all three; VALID |
| zz-5 lead-list names + places moved | SERVED | ~184 | drain `3f53830f67`, issuer close `961589b09e` | AC1 18 of 66 named (etf-classifications 16, crosswalk 2), AC2 66 of 66 `places_moved` int; AC3 failed in the worker's run on the old stamp only (row Z-W184-S1), 351 passed after the issuer synced zz-4's restamp (row Z-S310); VALID |
| zz-6 the driver chart's series | SERVED | ~185 | drain `960b15a24c` | `dry_run` + columnar-table verification: ASML 3 of 3 points spanned (was 1); AC2 118 passed; VALID. **Its AC1 handed the chart the driver in process -- see zz-8 AC2** |
| zz-7 FWD-1..31 re-grade | LOCAL read | ~182 | drain `da232b9e53` | 31 of 31 at `pVa+sgzj`: met 8, unmet 9, unmeasurable 14; AC1 re-run by the issuer against the live base; AC2 JUDGMENT (yours); VALID |
| zz-8 the ONE build (+ HARVST n-6 rider, + ASML rewrite) | WORLD | `0.7.0_AE_CloudOps~A` | entry CLOSED 4/4 `40be138834`, instance `e290cafc73`, issuer close `274240b782` | COO half `86ebcb17bb`, CTO half + rider ruling `448ab8a110`, conditions `7fdf60bfe3`; built at the PIN `0bf907bee8`; CodeSha `zHpr7FhS+irmKofIuKNqTkQm2hj7x2fvS1rrX1ohkfQ=` (05:20:04Z); AC1 / AC3 / AC4 PASS, **AC2 FAIL**, rollback WAIVED for AC2 only (CTO msg 26943, `fdd0074be3`); limbs 1-7 hold |

Worktrees `C:/tmp/r51-180..185`: branches merged, checkouts KEPT pending Andrew's go.

## 2. THE RESULT -- the issuer's real runs on the deployed function, at close

Captures in `round51/captures/zz8_*` (true exit codes: code 0, rows 0, chart 1, timeline 0).
- **Lead lists** (`/lead-panel/rankings`, four axes): 66 rows; 18 named, each with `name_source`; 66 of 66 `places_moved` int. No rank,
  score or order moved (AE~A's limb 7 on generation-matched projections, generation_id identical across the act).
- **`/timeline/day`** (the HARVST n-6 rider): bodies byte-equal on 4 of 4 days; latency per AE~A's REPORT reads 3.5x-27.6x faster on three
  of the four days (992_HK 09-23 read 1498 -> 1798 ms). HARVST o-3 cannot move a served body: 0 tied keys of 120 over every source's
  silver article (condition 3, `round51/ZZ8_CONDITIONS_BEFORE_GO.md`).
- **The crosswalk union** sits inside `write_pool` (both writers); nothing served changes -- `write_pool` is not on the request path.
- **The build stamp** no longer fires on unrelated registry admissions; every build prints its content diff against the deployed artifact.
- **ASML's thesis-driver chart: NOT SERVED.** The analysis object carries 3 spanned points, but the served chart reads the D-1 drafting
  document's embedded driver (`scoped_amgt.py:1876`), which the rewrite does not regenerate. The CTO carries the D-1 regeneration to
  round 52 under its own pair.
- **FWD-30** post-deploy: the issuer's full served sweep at `zHpr7FhS` (06:15-06:24Z, `round51/captures/fwd30_value_sweep_post_zz8_20260930T061504Z.log` + `.tsv`): **equal 96 of 96; values equal 96 of 96**; 19,136 value facts compared, 0 differing; identity-only 359; **digits compared, scale unchecked (export unit UNRESOLVED) = 0** (was 6). The six names that held FWD-30 (6501/9433/8316/8035/8766 JP, TSM US) read 0 differing and 0 unscaled over 114-192 facts each. **The cause is NOT this round's build:** AMGT_CORPUS round 22 applied 8 RESOLVED units to `field_map.json` (`0982a0767d`, 05:21Z, `build_unit_map.apply_discriminated`, the re-homed cell 3). Whether FWD-30 is now REALIZED is yours and the CTO's to grade; the served instrument is `round51/checks/zz-8.AC2.sh`.

## 3. Judgment criteria

- **zz-7 AC2 (yours):** each of the 31 outcomes' `state` follows from its `output_excerpt` read against its `fence_quote`
  (`deliverables/0.9.0_WK_AMGT_RESAPP~182/FWD_EVIDENCE_ROUND51.json`).
What else you may weigh: (a) zz-8 closed on a waiver, AC2 carried, not met; (b) FWD-22 and FWD-23 moved to unmet on the DEV page's header
cards (row Z-W182-S2) -- whether the clauses or the page move is the CTO's.

## 4. Rows this round (L8 input)

- **Z-S309** (issuer): cell 3 not cut -- `field_map.json` holds UNRESOLVED-ON units for the six names; re-homed to CORPUS r21 / DSGN r9.
- **Z-W180-S1 / S2** (~180): the closed schema refused the carry counters -- resolved by AMENDMENT 1.
- **Z-W184-S1** (~184) / **Z-S310** (issuer): zz-5's AC3 failure was the stamp, resolved by zz-4's restamp.
- **Z-W185-S1** (~185, INERT): the existing last-block verification gate can verify a number from a different column of a columnar table.
- **Z-W182-S1** (~182, INERT): `exportCompare.harness.cjs` is stale against the served base-case label and two absence carriers.
- **Z-W182-S2** (~182, INERT): PRD FWD-22 / FWD-23 describe interfaces the DEV page no longer has.
- **Z-S311** (AE~A) + **Z-S312** (issuer) -- **THE ISSUER'S ERROR:** zz-8 AC2's premise was false at the cut; zz-6's check validated the
  chart with a handed input and never the served join to the D-1 drafting document.

## 5. Carried to the CTO's round-51 analysis

1. **ASML's D-1 drafting regeneration** (CTO msg 26943), AC = the SERVED `/thesis` chart reads the 3 spanned points, graded on the served
   route, never an in-process call with a handed input.
2. **CORPUS round-20 rulings 2-3** (CTO msg 26890): 6501's empty dossier block with reasons; the pack_shape pass-through.
3. **FWD-30's last hold** is CORPUS r21's unit-map discriminator and DSGN r9's page scale (Z-S309); the served instrument is
   `round51/checks/zz-8.AC2.sh`.
4. **FWD-22 / FWD-23** (Z-W182-S2): amend the clauses or restore the Stat tiles and the disclosure form.
5. **`scoped_amgt.py:120`'s comment** ("never a runtime `lib.opal_naming` import") is false: `scoped_amgt -> corpus.dossier ->
   harvest.store -> lib.opal_naming` at module scope (the CTO's half ruled it INERT for this build; Z-S307's class).
6. **Z-W185-S1**: whether the last-block verification gate is tightened (it rests under other stored objects).
7. **Gate proposal (not implemented):** a check whose claim is a SERVED outcome reads the served route (or the real entry point), never a
   component called in process with its input handed to it (Z-S312).
