# 0.4.0_DS_ClientPlatform — PRE-REBOOT HANDOFF (2026-08-12 ~15:45Z)

**Trigger:** ANDREW-DIRECT ~1520Z via MSTR 154135Z — *"We need to reboot this device so make sure
that everyone finishes their work."* Finish what is finishable, start nothing new, PERSIST
EVERYTHING, report DONE.

⛔ **A REBOOT KILLS EVERY SESSION. NOTHING BELOW RE-ARMS ITSELF.**

## ⛔ CLOCKED PAST THE REBOOT — THE ONLY ITEMS THAT REQUIRE A SUCCESSOR ACT

### 1. bd mix served-read → owed to 3.0.0_SA_CVO — ⛔ WATCHER DIES, DOES NOT RE-ARM
- **Obligation:** send CVO the served bd mix read the moment the bd chain publishes.
  **UNGRADED** — CVO authored the two-leg pin **@70a4d4421a** and grades it themselves.
- **Watch target:** `s3://opal-data-bd/platinum/firm/mix_summary.json`
- **Baseline at reboot:** LastModified **2026-08-12T05:18:40Z**, 8,623 B. **Any LATER vintage is
  the fire condition.**
- **Why it matters:** my classifier heal deployed **14:49Z** (@bd2a8f854a), so the served artifact
  PREDATES it. Per CVO that is **PRECONDITION-ABSENT, not a FAIL** — and **V35 INVERTS the
  grading**, so a reader who grades the pre-publish artifact will wrongly score the heal as failing.
- **CVO's pin, carried so the successor does not re-derive it:**
  - baseline: fixed_income **335,568,824.39** · equity **1,425,031,320.52** · alternatives **17,939,245.90**
  - **LEG A (VINTAGE-INVARIANT, decides):** the five named securities (BNP PARIBAS 0%, BARCLAYS
    BANK PLC 0%/9%, GLADSTONE CAP, RIO TINTO FIN) must classify `fixed_income` and appear in NO
    unclassified bucket. Class does not move with prices, so this holds on any vintage.
  - **LEG B (CONDITIONAL):** ONLY if `data_as_of` is UNCHANGED (2026-08-06) does fixed_income rise
    by exactly **+$2,428,594.60** to **337,997,418.99**. **If the vintage ADVANCED, magnitude is
    confounded by market movement and LEG A alone decides.**
- A watcher script exists at the session scratchpad path but **the scratchpad does not survive
  either** — re-create it or head-object manually.

### 2. Nothing else of mine is clocked
No armed deploy, no scheduled tick, no open ledger. **CPR-4 step 4 TICKED and is CLOSED** (serve
fired 14:58:55Z). The 15:06Z-armed CPR-5 leg-B sits with **0.7.0_AE_CloudOps**, not with me.

## ⛔ OPEN DEFECT FILED THIS WINDOW — LIVE, NOT FIXED
`DEFECT_INF_ADVISOR_FEE_SPLIT_IS_FEE_EARNING_DROPPED_20260812.md` (same directory).
INF advisor summary serves `fee_earning_aua = $0.00` with the entire book as non-fee, beside
`avg_fee_bps_earned = 114.5`. **Mechanism source-confirmed AND input-confirmed; ROOT CAUSE NOT
ESTABLISHED; reachability UNDETERMINED and not claimed.** Surfaced by 4.0.0_SA_CRO~A, COO copied.
**Do not fix before the root cause — see the file's "NEXT ACTS", which explicitly forbids
back-filling the column.**

## LANDED THIS WINDOW (all committed and pushed)
| what | commit |
|---|---|
| P3 scope-hole ledger CLOSED (copy 10/10 + produce 3/3) | **@4c1219fc34** |
| `b01` swallow → FATAL + `a03`/`a04` name their destination + ledger amend | **@0205eef992** |
| Session log 1435-1535Z | **@6bdbf0d05c** |
| Classifier heal (both files) + V35 band, deployed 14:49Z | **@bd2a8f854a** |
| P3 re-point / ledger (earlier window) | **@aa72ab5bc5** / **@e99231aeda** |

## STATE A SUCCESSOR NEEDS
- **CPR-4 step 4 COMPLETE.** Serve 14:58:55Z carried both fields; `unreconciled_aua` 0.0
  discriminated on two independent grains (dollars close to $0.0000; accounts 725+74=799 = full
  universe) plus `radial_12m_meta` as a third axis. CVO holds the delta-cert. ⚠ **CVO ruled the
  mutant I offered must NOT be built** — the field is a FRAMING check, not an attribution check
  (`round(float(total_aua) - holdings_total, 2)`), so that mutant would read 0.00 and look like a
  hardcode. Attribution is enforced by `identity_gap`, fail-closed.
- **P4 is HELD** on a never-widen determination held by **CTO + COO** on DS~B's LEG A (35 advisors
  newly exposed, 4 dropped, client labels regressing to hashes). **Not mine to release.**
- **P4 EXIT CONDITION LIVE:** the old root `s3://opal-data-assets/schwab/08335338/gold/` must be
  decommissioned at P4; **P4 may not close while it exists.** Nothing was deleted this window.
- **The three produced dims** (`dim_security`, `dim_boundary`, `dim_calendar`, all
  `date=2026-08-11`) sit at `portal/gold/advi/49financial/dimensions/`. **Correct LOCATION,
  pre-production PROVENANCE — separable facts (CTO).** Production-criterion clause (i) UNMET, so
  **P4 must not close on these artifacts.**
- **`dim_identity_crosswalk`: NEVER-LAUNCHED, not superseded** — zero consumers repo-wide
  (`comp-find`: HEAD=7 is two implementations and nothing else), live input, built to spec row
  A_06. Leave it; name it consumer-less. A crosswalk-shaped hole exists at HOUSEHOLD grain
  (`d04:12`) and A_06 is ALLOCATION grain — **different grains, so it is not the answer to it.**

## OWED BUT NOT SENT AT REBOOT
- **1.0.0_SA_CTO** — the five-field OPAL_ADVIPOINTERS PRD lane report (requested 153926Z).
  **Sent this window if time allowed; if absent from CTO's inbox, this file plus the session log
  `logs/2026-08-12/step4_tick_and_p3_scopehole_1435-1535Z.md` carry the same content.**
