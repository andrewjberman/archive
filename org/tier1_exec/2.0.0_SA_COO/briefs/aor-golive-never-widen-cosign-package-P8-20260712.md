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

**CO-SIGN EVIDENCE (grounded, filled at go-live from the FINAL reproduction):**
- firm served AUA before = `<FILL>` ; after = `<FILL>` ; **DELTA = 0** (must be exact, grounded on the reproduced numbers).
- account count before = after = 871.
- per-advisor re-attribution (transparent): peter `<FILL ~135.24M>` / joe `<FILL ~29.19M>` / patrick `<FILL ~24.13M>`
  / **noel NEW `<FILL ~12.42M>`** / IWM `<FILL ~1.34M>`. Each delta from the pre-fold servicing number, summing to 0 firm-wide.
- `|fold| == 164` on the final build (the signed mover count).

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
- **My (COO) due-diligence before I co-sign:** (1) CVO~B's independent verification is IN + PASSED (the reproduction
  + guards grounded on the real loader/live -- gate 2); (2) I confirm the FINAL firm-conservation DELTA=0 from
  CVO~B's VERIFIED reproduced numbers (Rule 22a -- not the runbook target, not the synthetic path); (3) the
  served-verify plan is real + the rollback rehearsed. I withhold my co-sign until CVO~B's verification is in.
- Then: the ONE atomic go-live (ledger open -> DS release commit with SERVE-RELEASE-ACK, base CTO gates -> DT FE
  promote -> served-verify on the next scheduled nightly -> ledger close).

**Attribution:** package authored by `2.0.0_SA_COO` (go-live driver, Andrew-direct via CTO~B); mechanism/guard
design + the DYNAMIC-not-frozen ruling by `1.0.0_SA_CTO~B`; fold by `0.4.0_DS_ClientPlatform`; numbers to be
grounded from the final reproduction.
