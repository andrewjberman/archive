# INF advisor-of-record go-live -- NEVER#2 never-widen co-sign package (P8)

**`2.0.0_SA_COO`, 2026-07-12.** *The P8 co-sign deliverable for the AoR go-live (LD-0277), pre-built while the
round-4 fold review (wcckzqqdu) runs so P8 does not wait on the COO side. Runbook: `docs/briefs/advisor-of-record-go-live-runbook-20260712.md`.
Sign-off chain: **base CTO principal (`1.0.0_SA_CTO`) + COO (`2.0.0_SA_COO`) + Andrew final GO** -- do NOT proceed
on 3-of-4. **NUMBERS ARE FILLED FROM THE FINAL REPRODUCTION (P1/P5 on the REAL loader), NOT the runbook target**
(Rule 22a: ground the co-sign on the exercised reproduction, never the aspirational number).*

---

## THE NEVER-WIDEN ARGUMENT -- why this is a RE-ATTRIBUTION, not a widen

NEVER#2 governs MOVING/WIDENING served output. This change **re-keys advisor attribution WITHIN a conserved firm
cohort** -- it does not add served AUA or widen the served surface beyond the firm. The co-sign rests on:

1. **FIRM-TOTAL DELTA = 0.** Served firm AUA before == after (target $202.3M) and 871 accounts unchanged. The change
   moves AUA BETWEEN advisor labels; the firm sum is invariant. *A re-attribution under a conserved firm total is
   not a widen.*
2. **No NEW served AUA.** Noel Soderblom surfacing as a new advisor is EXISTING firm AUA re-keyed to a new advisor
   label (seeded from Orion advisor-of-record), NOT new dollars entering the served surface.
3. **No stranding.** Blank-AoR accounts keep the servicing-rep key (fallback); the 34 blank-udf7ADVISOROF accounts
   stay servicing; the 164 movers re-key within-firm. Every account still lands on exactly one advisor.

**CO-SIGN EVIDENCE -- VERIFIED by `3.0.0_SA_CVO~B` (gate 2, V1) 2026-07-12T1923Z, from CVO~B's OWN independent
re-derivation (own canonicalization + servicing maps + mover logic, never calling DS's build; live silver av2
2026-07-12 + live roster; oracle sym-diff=0 on BOTH servicing bases). These are the numbers the co-sign carries
(Rule 22a -- verified, not the runbook target):**
- firm served AUA before = **$202.32M** ; after = **$202.32M** ; **DELTA = 0, conserved EXACTLY**.
- account count before = after = **871** (CVO~B applied to the SERVED account_team 871).
- per-advisor (post-fold, transparent): peter **$135.24M** / joe **$29.19M** / patrick **$24.13M** /
  **noel NEW $12.42M** / IWM **$1.34M** (residual). All within <0.05M of target; each a within-firm re-attribution
  from the pre-fold servicing number, summing to 0 firm-wide.
- **INERT-STATE VERIFIED LIVE (the BEFORE / firebreak proof):** served TODAY is PRE-FOLD -- peter **$160.61M**,
  noel **$0.00** (not yet an advisor). So the co-signed move is peter -$25.37M / noel +$12.42M (NEW) etc., firm flat.
- `|fold| == 164` (CVO~B: 164 movers / 837 explicit / 0 dropped).

**HONEST SCOPE LINE the co-sign MUST carry (CVO~B O2):** "loader+fold EXERCISED on production schema + live data;
the deployed SILVER JOIN is VERIFIED-BY-MIMIC (the gate's mimic == `convert_orion_api_to_silver.py:574-581`,
semantically confirmed) and is FIRST EXERCISED on the go-live nightly -- the sentinel holds the advisor_key column
out of deployed silver until then." NOT a blocker; a truthful scope qualification so the co-sign does not overclaim
the deployed join is exercised pre-go-live. (The post-activation served-verify, gate-2 V-served, closes it.)

**GUARDS -- EXERCISED-VERIFIED by CVO~B (gate 2, V2):** own fresh-process poisoned/fake-boto3 probes (independent of
DS's tests): OFF = ZERO S3 I/O; RAISE bites on all 5 (no-raw-column / all-null-raw / populated-but-0-movers /
GROSS-over-fold [A3, tripped CVO~B's own first fixture] / no-rep-name); positive control loads clean (not reject-all);
the 2 neg-controls (swap + 165th mover) BOTH caught = non-placebo. S1-allowlist-no-mint + INF_D_10-over-286 covered
in the suites (20/20 + 21/21); CVO~B doing an independent S1-no-mint spot-exercise before final determination (belt+braces, COO-requested).

## WHAT THE CO-SIGN AUTHORIZES -- the DYNAMIC mechanism + its guards, NOT a frozen 164

Per CTO~B's ruling from Andrew's DAILY directive: the never-widen sign-off is for the **DYNAMIC self-maintaining
daily mechanism** (the fold tracks Orion `udf7ADVISOROF` daily among the SIGNED allowlist group
peter/joe/patrick/noel/IWM within data-quality + anomaly guards), **not a one-time frozen 164**. So the co-sign must
verify the GUARDS that bound the dynamic behavior, not just today's snapshot:

| guard | what it prevents | co-sign check (EXERCISED, not just present) |
|---|---|---|
| **S1 allowlist** | a NEW advisor auto-surfacing on daily drift | a not-allowlisted advisor in the roster does NOT mint a card -> reviewed-add only |
| **`\|fold\|==164` runtime upper-bound + gross-over-fold RAISE** | daily drift silently re-attributing beyond the signed set | over-fold on the daily path RAISES, does not serve |
| **marker-checked accounts_v2 load** | deriving off a silent-null / stale partition (THE firebreak) | stale+last-good -> carry-forward + LOUD ChainStepDegraded; stale+NO-last-good -> FAIL LOUD, never serve pre-fold |
| **load-once-per-process, source-invariant** | cross-producer basis drift | every producer's first apply() loads the SAME marker-checked partition |
| **INF_D_10 conformance guard** | served surfaces disagreeing with the SSOT | non-vacuous over the 286 live SSOT households, prints OK on SERVED |

**I co-sign only on these guards EXERCISED on the final clean build (P1/P5/P6 GREEN through the REAL loader), not
config-read.** A guard that is present but never bitten is not a guard (Rule 22a).

## TRANSPARENCY FLAG -- MUST be stated plainly to Andrew at final GO

**One household flips today: hh286.** Its sole explicit-AoR account (Noel, **$0 AUA**) headlines over 4 blank-AoR
Peter accounts (~$79k). This is faithful to Andrew's "advisor-of-record ALWAYS wins regardless of AUA" override --
but **a $0-AUA account driving a household-headline flip is the one counter-intuitive consequence**, and it goes to
Andrew explicitly in the final-GO ask, not buried. TRUE multi-AoR-owner households = 0, so the AUA/lexical tie-break
never fires on live data (defensive-only). Keil/DeMuth excluded (Andrew).

## THE GATE

**Updated go-live gate chain (Andrew added a DEDICATED verification lane 2026-07-12):**
`(1) CTO~B /code-review CLEAN (w83xbuei1 + CHANGE-2)` -> `(2) 3.0.0_SA_CVO~B independent VERIFICATION` ->
`(3) never-widen co-sign (base CTO principal + COO + Andrew)` -> `(4) Andrew final GO`.

- **THE CO-SIGN RESTS ON CVO~B's INDEPENDENT VERIFICATION (gate 2), not on my read or a self-report.** This session
  produced FOUR false-greens (P5 synthetic-frame blind spot; tautological reproduction-gate checks; the rate-limit
  vacuous pass; the mis-scoped review) -- all verification-instrument failures. A never-widen co-sign resting on my
  own read would be the fifth. CVO~B independently grounds: the P1/P5 reproduction on the REAL loader (|fold|==164,
  firm-conserved on LIVE data), the 5 guards EXERCISED (not config-read), and the POST-ACTIVATION served-verify.
- **Sign-off chain:** base CTO principal + COO + Andrew final GO. Banked BEFORE the DS release commit. NOT 3-of-4.
- **DRIFT-ROBUSTNESS is a CO-SIGN REQUIREMENT (round-5, CTO~B /code-review 2026-07-12):** the co-sign authorizes a
  DYNAMIC DAILY mechanism, so "correct on today's data" is NOT sufficient -- the fold must be robust on a FUTURE
  DRIFT day. The round-4 fold was correct-today (CVO V1/V2/V3) but the /code-review found it silently WIDENS on
  drift: **F1** (a bad-pull/silver-drift night -> servicing-reps don't resolve -> ~150 movers silently kept-on-servicing,
  Noel loses ~$12M, only a log line = NEVER#2 SILENT WIDEN -- CONFIRMED-BY-EXERCISE, CVO~B null-servicing probe:
  120/200 null-servicing explicit accts silently kept, fold=40, no raise); **F2** (household/account grain desync);
  **F4** (thin/partial roster FALSE-RAISES -> whole INF nightly crashes). A fold right-today that silently-widens-on-drift
  is EXACTLY what NEVER#2 forbids. So the co-sign is WITHHELD until round-5 fixes the unified guard model + CVO
  re-verifies the fix INCLUDING these drift classes (the null-servicing-at-scale probe re-run). Correct-today is
  necessary, not sufficient.
  **STATUS 2026-07-12T1958Z: DRIFT-ROBUSTNESS MET (round-5 `4818dfa5f`, CVO~B gate-2 re-verified by EXERCISE).** F1
  CLOSED: the null-servicing ceiling RAISES `[NULL-SERVICING-CEILING]` at 60% (needle-matched) -> a systemic bad
  pull now REFUSES to serve. F2 CLOSED: null-servicing folds to AoR in BOTH maps at 4% (grains agree). Ceiling
  BRACKETED (fires 9.1%, quiet 4.0%, threshold 5%); RULE-2 armed BOTH directions (gross-over + thin-under); full
  battery green; 164+$+firm-$202.32M re-reproduced LIVE by CVO's own derivation (RULE-1 no-ops today: zero
  null-servicing accounts, so today's fold + the co-sign numbers are UNCHANGED; the guard is for the drift day).
  Co-sign basis now COMPLETE: correct-today (V1/V2/V3) AND robust-on-drift (round-5). Waits only on gate (1) CTO~B
  /code-review CLEAN on `4818dfa5f` (`w0cf5gz8z`, running ~40min) + CHANGE-2 (fold-review + CVO-verify).
- **My (COO) due-diligence before I co-sign:** (1) CVO~B's independent verification is IN + PASSED -- the reproduction
  + guards grounded on the real loader/live AND the DRIFT-ROBUSTNESS classes (F1/F2/F4) re-verified on the round-5
  fix (gate 2, drift-inclusive); (2) I confirm the FINAL firm-conservation DELTA=0 from CVO~B's VERIFIED reproduced
  numbers (Rule 22a -- not the runbook target, not the synthetic path); (3) the served-verify plan is real + the
  rollback rehearsed. I withhold my co-sign until CVO~B's drift-inclusive verification is in.
- Then: the ONE atomic go-live (ledger open -> DS release commit with SERVE-RELEASE-ACK, base CTO gates -> DT FE
  promote -> served-verify on the next scheduled nightly -> ledger close).

**Attribution:** package authored by `2.0.0_SA_COO` (go-live driver, Andrew-direct via CTO~B); mechanism/guard
design + the DYNAMIC-not-frozen ruling by `1.0.0_SA_CTO~B`; fold by `0.4.0_DS_ClientPlatform`; numbers to be
grounded from the final reproduction.
