# L8 drain end -- ADVI_COTBKF round 15

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~16:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 15 was cut as one issuance (@d6f1f583f0, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-14 analysis @47ea1968e7.
1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-o-1 near-match page from the served crosswalk | ~31 | @cb6c7d6cd5 | VALID: AC1 PASS, AC2 3 passed (served-vs-generator control) | `NEAR-MATCH-PAGE near_matches=22 served_equals_generator=True crosswalk_version=wv5z6zeRnWQrPGfO3UcmrxlIaz3ozzLZ entered=1 left=0 entered_accounts=acct#8179a706` |

**The page:** `deliverables/0.9.0_WK_ADVI_COTBKF~31/near_matches.{csv,md}` -- 22 entries; all 21 of round 4's kept; 0 left.

**The entering entry (the CTO's control, criterion 2), completed by the issuer from the served history:** the worker could not give
acct#8179a706's score before (the round-4 page lists only in-band accounts). The previous served crosswalk version, kept by bucket versioning,
gives it:

| crosswalk VersionId | status | score | reason_code |
|---|---|---|---|
| `fatOX6x0HfXRV_O7TKPNmuGBrL5wuoG1` (round 4, old signing rules) | NOT_MATCHED | (none -- not scored) | NO_CURRENT_ACCOUNT_HOLDS_POSITIONS |
| `wv5z6zeRnWQrPGfO3UcmrxlIaz3ozzLZ` (round 14, the one table) | NOT_MATCHED | 0.75 | AWAITING_PERSON |

Under the old rules its end positions rebuilt to nothing a current account held, so it was never scored; under the one table they rebuild
to positions a current account holds 0.75 of. It is listed for a person, never linked.

**For Andrew/Cottonwood:** the page to send is now this one (22), replacing round 4's (21) -- row D2-S25 is answered by it.

No rows. ARMED: 0. After this round the lane waits on MDPF_SECHIST's first announced price load (FWD-3 steps 2-4) or the laptop's
C-RESTRICTED apply (FWD-2 CRM half, FWD-4, FWD-7).
