# AMGT_HARVST ROUND 11 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-28 ~22:0xZ

**Issuer:** `2.0.0_SA_COO~H`, re-seated from `2.0.0_SA_COO~Y` by `1.0.0_SA_CTO~Z` (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260928_195xZ_SITEZ_AMGT_ONE_COO_PER_PROJECT_SEATING.md`).
**Issuance:** `5311a2ebd8` (the post-rewrite hash of `~Y`'s `932f56c7f9`), four orders, unchanged.
**L8-L10 route:** `3.0.0_SA_CVO~Z` (record `ANDREW_DIRECT_20260928_201xZ_SITEZ_SEAT_CVO_Z_FOR_AMGT.md`), which ends
the interim `3.0.0_SA_CVO~O` route.

## 1. RE-SPAWN AFTER THE REBOOT -- S19 constraint honoured

- The three `wk-hvst-z{0,2,3}-r11` worktrees are PRE-REWRITE (`7e4f50c6dd` is not an ancestor of the trunk). None was
  merged or reused. Four fresh full worktrees were cut from the trunk with `.tools/wk-provision.sh` (39 GB free, so no
  sparse cone was needed).
- `z-2`'s two uncommitted AC scripts crossed by FILE COPY (`cmp`: byte-identical). The worker re-read and re-ran both.
- The old worktrees stay on disk untouched. Their disposition is part of `0.0.0_AB_MSTR~Z`'s S19 drain, not this round.

## 2. FOUR CELLS, FOUR TERMINAL, FOUR VALID (pre- and post-merge)

| cell | slot | risk | merge | result |
|---|---|---|---|---|
| `z-0` wire the two timeline routes | `~31` | LOCAL | `4350d5af00` | 267/267 days, 4/4 events, 3/3 articles equal an independent `_latest_gold_snapshot_rows` read; 6/6 failure cases error-encoded; api suite 239 -> 255 passed |
| `z-1` rebuild `chatter_event` | `~32` | SERVED | `085e15c649` | ONE put `date=2026-09-28/part-20260928T210944Z.parquet`; 12 -> 8; BA and HD ids moved; AC2 8/8 rows, 104/104 fields |
| `z-2` FWD-4 field census | `~33` | LOCAL | `7cb7c7f33d` | clause (i) MET over 263 of 263 rows, 6/6 facts mapped, `share` absent as `C-HV-ABSOLUTE-ONLY` requires |
| `z-3` patch-target audit | `~34` | LOCAL | `03e86f2909` | 8/8 sites re-targeted; 78 passed, 1 skipped, 6 subtests (trunk re-run, equal to the cut baseline); 0 miss over 309 files |

## 3. THE SERVED ACT -- measured by the issuer on both sides, not adopted

- **BEFORE (issuer, pre-spawn):** 3 parts under `s3://opal-data-harvest/amgt/harvest/gold/chatter_event/`, the newest
  (`date=2026-09-24/part-20260924T134754Z`) at 12 rows. This matches the signed premise.
- **Signed code, unchanged:** `publication_gold.py` last changed `12bbaa0e27` (04:48 local), before both halves were
  signed (06:34 and 06:44 local).
- **"Once it serves" clause of the CTO half:** not triggered. `z-0`'s route is merged but UNMOUNTED at the gateway and
  UNDEPLOYED, so no user could reach the table.
- **AFTER (issuer, independent re-read):** 4 objects. The 3 prior ETags are unchanged. The new object's ETag
  `58755afa...` and size 6412 B match the worker's receipt, and it reads 8 rows. So one object was ADDED, nothing was
  removed, and the signed radius held.
- **AC4 (judgment):** presented for `3.0.0_SA_CVO~Z` at L9 with no worker verdict. The worker corrected one AC4 script
  defect before its recorded run (mentions keyed by `article_key` alone mis-tiered multi-security articles); read the
  instance's corrected output, not the first run.

## 4. THE ONE REAL RUN AT CLOSE

`deliverables/2.0.0_SA_COO_H/scripts/close_run_round11.py` calls `scoped_amgt.handler` in-process with the production
loaders, after the rebuild; trace `CLOSE_RUN_ROUND11_TRACE.txt`. For `992_HK_Equity` (Lenovo):
- **Range route:** HTTP 200, 267 days, 3 events. They equal the newest landed rows, and the removed 06-01 span is absent.
- **Day route (2026-05-22):** HTTP 200, 3 articles.

**What it does NOT exercise:** the gateway (unmounted, row `Z-W31-S1`) and the portal.

**One number that corrects a figure carried forward:** the RANGE route took **19.9 s** in this run and the day route
16.7 s. `z-0`'s worker measured the range route at 5.4 s, and row `Z-S34` cites that figure. Both are from this box
and in-process; in-region Lambda latency is UNMEASURED. So the 29 s ceiling concern is about BOTH routes, not only
the day route. Round 12's timing criterion must time both.

## 5. ROWS -- four new, all UNDER_INVESTIGATION on the gate's own fold

The fold is `_latest_dispositions('.', 'AMGT_HARVST')`: **75 ids, GRADUATED 46, DISMISSED_WITH_REASON 25,
UNDER_INVESTIGATION 4**, read over 23 files. The 4 open ids are exactly this round's:
- `Z-W31-S1` -- ARMED, disarm owner this seat. The gateway mounts no timeline route.
- `Z-W31-S2` -- ARMED, disarm owner this seat. Silver headline-scan latency (see section 4's correction).
- `Z-W34-S1` -- INERT. The premise of `z-3` held at ONE site of 8. The other 7 were never a miss.
- `Z-S34` -- this seat's disarm record for the two ARMED rows, BY SPECIFICATION ONLY. It claims no remedy applied.
- `Z-S33` reads GRADUATED on the fold (REMEDIATION_v4 carries it open until the header mount is served).

**Armed rows with an owner this seat could not seat: NONE.** Both ARMED rows name this seat.

## 6. FOR THE ROUND-12 CUT (the CTO's round-11 analysis decides; listed so nothing is lost)

1. **The gateway mount cell**, per `Z-S34`: `scoped-amgt-api.tf` both route_keys + `scoped_amgt_route_table()` 16 ->
   18 in ONE commit, with the mount test green both ways; a ledgered deploy; both routes timed from the deployed
   Lambda against 29 s. This is the precondition for Andrew's ruling 3 (portal DEV push of `92a2576254`) and for
   FWD-5's walk.
2. **Vendor cells on Andrew's 18:05Z word** (ruling 2, record `ANDREW_DIRECT_20260928_1805Z_OPEN_CALLS_FOUR_RULINGS.md`):
   `w-5` (bbg diagnostic) and `w-4` (ft/barrons diagnostic, `Z-S31`), one bounded run each. `w-2` (capture) runs with a
   cap and `--new-only`, AFTER this rebuild, which has now landed. All three are drafted in decomp `s.20.5` and have
   NEVER been issued. They were not cut into round 11 because round 11 was frozen after its one issuance.
3. `z-1`'s judgment (AC4) and FWD-6 are graded at L9/L10, not here.

## 7. WHAT THIS PACKET DOES NOT DO

It grades no judgment criterion, claims no FWD as REALIZED, pushes nothing (every commit above is LOCAL), and cuts
no round-12 cell.
