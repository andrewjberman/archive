# AMGT_RESAPP round 61 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-02 ~09:3xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.69. **Issuance:** `f234d5aa12` (drained `63e78fe4f7`). **Input:** `1.0.0_SA_CTO~Z`'s
DSGN_AMGTV1 round-21 analysis `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/ROUND_ANALYSIS.round21.md` @`e14de1769c`, section 3B, amended
@`b74c090804` (B4) and @`2b1e921054` (B5).

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `ak-1` B1 a company name on every price bar and bubble | LOCAL | issuer | landed | `f234d5aa12`; suite green; `b1_names.py` local YES, `--mutant` FAIL |
| `ak-2` B1's code-only redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete: LIVE 07:45:38Z | proof `b8481055c0`; CodeSha256 `UnSqZgCD...` -> `E+FAZF0f...`; CONTENT-DIFF 350/347/CHANGED 3 (2 signed + rider `aa2b5a42ff`); plan 0/1/0; entry CLOSED; pair COO `f234d5aa12` / CTO `02d032ee67`; closed `36b180b3fe` |
| `ak-3` B2 plain served reasons + B5 the CEO search basis | LOCAL | `0.9.0_WK_AMGT_RESAPP~201` | complete | `042ee0f7a8`, AMENDMENT 1 `25ac521b3d` (the peers producer `csc.py`), AMENDMENT 2 `48661ef1f5`/`78b7325369`; drained `5eb2a8c593`, `067df94e74`; shared tree AC1 544 passed; closed `0b0c5eec8a` |
| `ak-4` B3 the M-1 officer parse | LOCAL | `0.9.0_WK_AMGT_RESAPP~202` | complete | `c58ef63415`, drained `a846f71d22`; AC1 481 passed, AC2 YES; no parser change was owed (rk-46 already correct); closed `a1226bd474` |
| `ak-5` B4 a missing score in words | LOCAL | `0.9.0_WK_AMGT_RESAPP~203` | complete | `3b7c56774e`, drained `7672553ecc`; AC1 392 passed, AC2 YES; `plain_claim` on the drafter's write path, no model call; closed `a1226bd474` |
| `ak-6` (A) B2/B3/B4 stored-field rewrite | WORLD | `0.7.0_AE_CloudOps~A` | complete | proof `4d12c64f00`; 251/251 keys, 1,188/1,188 fields; pair COO `fa9c914db9` / CTO `af95b2f1c0`; accepted `9115f4594b`; AMENDMENT 1 removed the redeploy (0 of 350 packaged members changed) |
| `ak-6` (C) B5 stored-field rewrite | WORLD | `0.7.0_AE_CloudOps~A` | complete | proof `83158f6267`; 7/7 keys; pair COO `0b0c5eec8a` (correction `7bbf273c19`) / CTO `b49f4d2db3` (re-signed `bbbda2e848`); entry CLOSED |

## The real run on the DEPLOYED function (issuer, independent; moving fields, never an HTTP status)

- **B1** (07:5xZ): TRENDING/PRICE and BREAKOUT/PRICE serve 0 of 94 unnamed (base 24).
  - The 24 now carry Bloomberg names from the model-block header (SSE PLC ... HERMES INTERNATIONAL); 0 of 70 already-named rows moved.
  - Chatter: 0 of 95 by ticker (base 25).
  - Round 60's overlay-equals-row holds (AC2).
- **B2/B3/B4** (08:5xZ): `ak6_verify.py` CLEAN -- 1188/1188 planned fields, 251/251 objects unchanged outside them, 251/251 moved.
  - Deployed /thesis + /peers for BA and VLO: b2 0 of 26 code-shaped (base 11); b3 VLO officers full names and titles, 0 aged roles (CFO
    "Harminder S. "Homer" Bhullar" recovered), BA 12; b4 0 of 12 posture claims with a status token (base 2).
- **B5** (09:2xZ): `ak6_verify.py` CLEAN on 7/7, with VLO's act-(A) fields intact under the masked comparison. `ak6c_reading.py`: all 7
  reading states unchanged; `urls_returned` unchanged on 6, and SAP_GY None -> 10, the named exception. b5 deployed: 0 of 2 bases say
  "SERP" or "contract's search" (base 2 of 2).
- **Final regression on the deployed function after the last write:** b1, b2, b3, b4 and b5 all YES (`final_regression_*.out`,
  `ak6c_issuer_read_*.out`).

## For the CVO's L8 read

1. **B1's name source (issuer ruling R1).** The 24 unnamed rows entered from the one-pager universe and were never registered, so no
   crosswalk identity block names them. Each already served Bloomberg `NAME` in its overlay's `header_figures`. The serve-time chain
   takes that before the ticker fallback, with no registration and no vendor call.
2. **B4 without a model call (R2).** The posture claims are model-drafted and stored. Regenerating them is an Anthropic call (reserved).
   The drafter's prompt and pack now state a missing score in words, and the stored claims were rewritten through a deterministic
   `plain_claim`.
3. **B2's census (R3)** is the analysis's two strings (the Lusha skip reason, the peers absent reasons), not every `*reason` key. 273 of
   395 such keys are technical records the page never prints.
4. **The peers reasons were stored, not served at the cut.** ak-3 AMENDMENT 1 granted `lib/research/peers/` so the producer writes the
   words. ak-6 rewrote 234 peers objects.
5. **ak-3 AC2's plan form goes stale after ak-6's write, by design.** It was graded with the plan before the write and without it after
   (row Z-S335).
6. **Act (C) condition 4 carried one named exception**, measured before the GO and re-signed @`bbbda2e848`. SAP_GY `urls_returned` goes
   None -> 10, the true count, now parseable from the producer's sentence. Every reading state is unchanged.
7. **Not deployed by this round:** ak-3's one-line `scoped_amgt.ceo_profile_reading` prefix (a new failure sentence); no stored object
   is a failure case. It rides the next scoped-API redeploy.

8. The executor flagged the act-(C) pre capture as taken before act (A). It was taken after act (A): commit `7bbf273c19` at 05:04 -0400,
   which is 09:04Z, and act (A) wrote at 08:3x-08:4xZ. The 05:02Z the executor read is local time. Its own re-capture between the acts
   found 0 differences anyway.

## Rows

- `Z-S333`: the seating lint counts `withdrawn` as open and truncates worker serials (INERT; disarm `1.0.0_SA_CTO~Z`).
- `Z-S334` (AE~A): the ak-2 worktree premise was measured false (0 packaged files drifted), DISMISSED_WITH_REASON.
- `Z-W201-S1..S4`, `Z-W202-S1/S2`, `Z-W203-S1`: worker rows. The portal-fixture AC1 errors and the stale-by-design C0 are disarmed by
  `Z-S335`, and W201-S1 is answered by AMENDMENT 1.
- Carried past Friday, unchanged: `Z-S332` (an unknown key's overlay answers 200).
