# cot fix-wave FIX LOG — OPAL_GLDRNS.C1 drive (0.4.0_DS_ClientPlatform~C, 2026-07-15)

Drive executed under OPAL_GLDRNS.C1 + Andrew-direct fix-wave GO ("Ok fix it now", ~21:1xZ,
recorded lane_c_fix_wave_go_record.md). The per-agent finding reports live in
`org/tier1_exec/1.0.0_SA_CTO/deliverables/cot_gold_bughunt_reports/` (CTO-authored, 07-07);
that folder's FIX_LOG scaffold is BASE_EXEC-laned, so the drive log lives HERE — CTO may fold
it in. Full triage (re-keyed to the REAL nightly, SSM doc `opal-cot-gold-run`):
`COT_GLDRNS_C1_TRIAGE.md`. All four fixes deployed via safe-deploy on push + independently
verified `comp-pipescript deployed` MATCH; the SCHEDULED 02:03Z nightly is the validation run.

## FIX-001 -- A_00: incremental snapshot-union corrodes established accounts (verify_09, CRITICAL, live+growing 13->38)
- **File:** `data/cot/scripts/gold/A_00.accounts_dimension.py` -- `build_accounts_dimension` / `_run_incremental`
- **Defect:** in incremental mode the snapshot union tested only the window's txn accounts, so the whole book re-entered as null-metadata rows and `merge_incremental` overwrote real name/tax_status/state fields nightly.
- **Fix:** `known_account_ids` (the existing dimension's ids) passed into the union test -- `_extra` now only genuinely-new accounts. (+2 preexisting lint clears for the gate.)
- **Commit:** `20c5f9c96`. **Acceptance (CTO):** tomorrow's dim shows corrupted-count FROZEN at 38, tax diversity on newly-updated accounts. **Repair of the existing 38 + book-wide 'taxable' stamp = the SEPARATE CTO-gated --full rebuild.**

## FIX-002 -- C_06: unguarded dead read of retired C_02's frozen artifact (verify_23, latent chain-abort fuse)
- **File:** `data/cot/scripts/gold/C_06.client_mix_timeseries.py` -- `load_static_tables`
- **Defect:** `cp_daily_total` computed and never consumed; producer C_02 retired 06-22; deleting the frozen artifact would abort this REQUIRED nightly step.
- **Fix:** read deleted (import + return + unpack cleaned). C_02's stale artifact is now safe to purge (easy-win 8, held for CTO).
- **Commit:** `293ab5fe6`.

## FIX-003 -- cot_silver_merge: key ID columns forced to string pre-object-loop (verify_17 root, hardening)
- **File:** `data/cot/scripts/silver/cot_silver_merge.py` -- `process_xlsx_to_parquet`
- **Defect:** the cot fork dropped the 49F producer's explicit ID cast; a numeric BD delivery would land int64 IDs in silver and silently miss every string-keyed join (the B_01 Gate-3 lots-wipe trigger).
- **Fix:** account_id/relationship_id/portfolio_id/account_number/contra_account_number cast (null-preserving, integral-float-safe). **Blast grounded live (CTO rider):** cot IDs are 'z'-prefixed strings today -> the cast is a NO-OP on current data, pure drift-hardening. transaction_id + asset_id EXCLUDED deliberately: int64 across existing history; a dtype fork breaks cross-partition dedup (int 845418533 != str '845418533') -- unify only at the consolidation-port history rewrite.
- **Commit:** `5930dd45d`.

## FIX-004 -- B_00: required-column guard on snapshot partitions (verify_04 + verify_07, both HIGH)
- **File:** `data/cot/scripts/gold/B_00.canonical_holdings.py` -- `_build_canonical_from_snapshot`
- **Defect:** absent `units` -> AttributeError chain-abort; absent `market_value` -> silent $0-AUA canonical; account_id/asset_name -> KeyError. Only `ticker` was guarded.
- **Fix:** presence check on all four; missing -> named RuntimeError citing the partition (loud, actionable). (+3 preexisting E702 clears.)
- **Commit:** `b0182ce05`.

## DESIGN ITEMS + NO-FIX

Carried in `COT_GLDRNS_C1_TRIAGE.md` §2 (easy wins 5-9, held at CTO gates), §3 (dormant
booby-trap register + trash list), §4 (port-time design items D1-D6). Refuted/diagnostic-tier
findings adjudicated per-script in the triage table (§6).

---

# DORMANCY FOLD + LANE CLOSE (Andrew-direct, 2026-07-16) -- THE LANE IS CLOSED

**Ruling (Andrew-direct to this lane, ~13:0xZ, on a two-form conflict I surfaced rather than
adjudicated):** **PARK IT -- the lane stays closed.** No code, no `--full` rebuild, no cot gold
push. Recorded here once so **nobody re-derives the decision.**

**Provenance of the conflict (both cite Andrew's SAME ~12:5xZ message; recorded, not resolved by me):**
- `1.0.0_SA_CTO` -> this lane, **12:57Z**: GO on three motions (tax fix -> one `--full` rebuild -> dormancy fold -> close).
- `2.0.0_SA_COO` record, **12:58Z** (`041ac9e57`, folded to MEMORY.md): *"DS~C deliberate close; Cottonwood dormant-where-data-absent w/ tax-fields exception PARKED-SPECIFIED."*
- Both agree the tax cell is a GENUINE EXCEPTION to dormancy; they differ ONLY on execute-now vs park.
  Latest-and-most-restrictive bound -> surfaced to Andrew -> **Andrew chose PARK.** CTO's 12:57Z GO is
  **SUPERSEDED**, not ignored.
- Andrew's dormancy premise, verbatim (via CTO 12:57Z): *"the issue with Cottonwood is that their data
  is just incomplete, there are a lot of missing fields, so a lot of this stuff if there is no
  information there just has to be dormant."*

## PARKED-SPECIFIED -- **NOT** "source-absent, dormant" (the one cell where the dormancy premise does NOT hold)

### P-001 -- A_00 tax derivation: flat 845/845 `taxable` book (**the data EXISTS**)
**DO NOT re-file this as source-absent.** Every other item below is dormant *because the source lacks
the field*; this one is dormant **only because Andrew parked it**. The distinction is the record's whole
value: filing it under the dormancy rationale would bury a live defect behind a reason that is
measurably false, and the next reader would close it wrongly.

- **Status:** PARKED-SPECIFIED, NOT PURSUED (Andrew 07-16). Specified fully here so revival costs a read, not a re-derivation.
- **Grounding: CTO's measurement, NOT mine** (his 02:22Z inbox message, his own instruments; this lane
  did **not** independently re-verify -- do that at revival before acting):
  - Source `silver/transactions/2026-07-16.parquet` carries RICH diversity:
    `tax_status` = Tax-Deferred 7,478 / Non-Taxable 2,816 / Taxable 2,132;
    `tax_status_1` = Taxable 10,563 / Not Available 1,223 / Other 564 / Tax-Exempt 76.
  - The dim nonetheless reads **845/845 flat `taxable`**, including the 3 self-healed accounts.
  - Therefore CTO **REFUTED** the sparse-source hypothesis by measuring the source: this is a live
    derivation defect, not incomplete data.
- **First suspects (CTO's, unverified by this lane):** `A_00.accounts_dimension.py` L502-504,
  `map(...).fillna('taxable')` running on `tax_status_1` -- (a) key/case mismatch between the map's keys
  and the source's actual values (`Taxable`/`Not Available`/`Tax-Exempt`/`Other`) would send EVERYTHING
  through the fillna default; (b) `tax_status_1` is the WEAKER column -- the source's `tax_status`
  (Tax-Deferred/Non-Taxable/Taxable) is the discriminating one, so the derivation's column CHOICE is
  itself in question.
- **Blast:** the empty/wrong tax panels in D_02 and the C_05/D2 tax-panel question both trace here.

### P-002 -- the ONE `--full` rebuild: **NOT RUN. Gate stays CLOSED.**
- FIX-001 is **verified working** (CTO 02:03Z read: 38 -> 35 corroded, **ZERO new**, strict subset
  proven by ID-set diff, 3 healed -- z0926771071 / z0926890141 / z0927135141). The corrosion machine is
  STOPPED; the rebuild was only ever the REPAIR of the pre-existing 38 + the flat tax book.
- CTO's own sequencing stands and is the reason this is safe to leave: a rebuild BEFORE the tax fix
  *"would restore names/states while baking 845/845 taxable into a fresh dimension through the same
  broken derivation."* Parked tax fix => the rebuild must NOT run. **Rebuilding now would bake the
  defect in.**
- **Standing hazard if revived:** cot gold **AUTO-DEPLOYS on push**; the rebuild is a served-content change.
- **A known-wrong frozen number is strictly safer than a fresh one built through a known-broken derivation.**

## DORMANT -- source-absent (one line each, per the ruling)

- **Item 6 -- office dim / OFC views empty** (`dim_advisor_office.csv`, B4): source-absent, dormant per Andrew 07-16. *(CTO GO'd 22:45Z as UPLOAD-else-DROP-with-tombstone; the GO landed AFTER this lane's 22:25Z close and was never executed -- superseded unexecuted.)*
- **Item 7 -- CLA wrong two-ways, FE-consumed** (D_01/B2): NOT source-absent -- a real defect; unpursued per Andrew 07-16, carried to the OPAL_CONSOLIDATION port. *(CTO GO'd 22:45Z as SUPPRESS-NOW-FIX-AT-PORT; landed after close, never executed -- superseded unexecuted. Still emitting today.)*
- **Item 8 -- resurrection booby-traps** (dead `C_00`/`C_02.py` on S3, `gold_dispatch.sh` wrong-firm wires): dormant per Andrew 07-16 -- **the path never runs; it is only lethal if someone runs it.** Register retained in TRIAGE §3.
- **Item 9 -- records hygiene** (`gold_pipeline_deps.yaml` stale key, `README_BUILD_SEQUENCE.md`, REGISTRY D-group row, `.py.legacy`): dormant per Andrew 07-16, port-time cleanup.
- **Item 5 -- C_05 de-chain/skip-clean** (SSM doc edit): ROUTED to `0.7.0_AE_CloudOps` (infra lane) per CTO 22:45Z -- **not this lane's to close**; dormant here.
- **Lots stack B_01/B_01b/B_02/B_03, C_07, C_08 + repair machinery** (verify_17/06/08/12/19/25): source-absent (no lots/fee feed from BD), dormant per Andrew 07-16 -- port-time design inputs D1/D4, NOT pre-port fixes.
- **C_01b/C_01c role_aua**: source-absent (role_aua empty, never ran), dormant per Andrew 07-16 -- D3.
- **A_02 fee_rate_history / A_01 advisor_assignments**: source-absent (no fee data; output absent), dormant per Andrew 07-16.
- **S_00 canonical_prices for cot**: inert (frozen 06-09; B_00 skips FIFO), dormant per Andrew 07-16 -- retire-candidate at port.

## WHAT REMAINS TRUE AT CLOSE
FIX-001..004 are **deployed, MATCH-verified, and validated by the scheduled 02:03Z nightly**
(CTO's independent read, not a self-report). The corrosion machine is stopped and 3 accounts
self-healed on the predicted path. Everything else above is **recorded, specified, and deliberately
not pursued.** Lane `0.4.0_DS_ClientPlatform~C` **CLOSED** per Andrew 07-16.
