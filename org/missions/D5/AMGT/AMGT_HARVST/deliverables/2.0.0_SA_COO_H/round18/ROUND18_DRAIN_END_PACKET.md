# AMGT_HARVST ROUND 18 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~19:5xZ

**Issuance:** `4d86812a13` (one chain, `g-1` -> `g-2`, over `ROUND_ANALYSIS.round17.md` @`c296f4ba12`; decomp
section 30). **L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** SERVED (`g-2` moved three served gold tables under a signed
never-widen pair). **Crash note:** the round was interrupted by the 11:34 ET site-Z crash. `g-1`'s uncommitted work was
salvaged (`refs/archive/wt-20260929/wk-AMGT_HARVST-45-wip` @`a4374c7043`) and re-graded by a resumed worker; nothing
was re-authored.

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | deliver | drained | instance |
|---|---|---|---|---|
| `HVST-g-1` the alias rule (exact-case tickers, whole-brand list, two-limb parent-brand refusal) | LOCAL | `0c591ac7a4` | `a802677065` | VALID rc=0 |
| `HVST-g-2` rebuild mention, daily and event on the rule | SERVED | `8538e74110` | `8c02ff0b12` | VALID rc=0 |

- **Suite:** the trunk reads **194 of 194** (base 177; +17 alias-rule tests).
- **The pair:** COO half `round18/NEVER_WIDEN_HALF_COO_G2.md` @`294e28bcbe`; CTO half
  `ledger/NEVER_WIDEN_ROUND18_G2_CTO_HALF.md` @`9a25d2d5d3`.

## 2. WHAT MOVED ON THE SERVED PLANE (`g-2` AC1/AC2 PASS; issuer's independent diff agrees)

| table | before (newest) | after (newest) | rows |
|---|---|---|---|
| article_security_mention | `part-20260929T112204Z` `b8118b05...` | `part-20260929T192610Z` `831c5669...` | 275 -> 304 |
| chatter_daily | `part-20260929T112222Z` `06025a62...` | `part-20260929T192649Z` `7bce5e68...` | 51,952 -> 51,952 |
| chatter_event | `part-20260929T092439Z` `c146a325...` | `part-20260929T192706Z` `c146a325...` | 8 -> 8 (identical bytes) |

**Daily:**
- 4,286 cells moved, over exactly the 50 securities the pair names, 0 of them outside it.
- FDX did not move, and there were 0 extension rows.
- The per-column counts equal the COO half's section 4.2 table, read by this seat from S3 directly.

**Events:** kept 8, moved 0, gone 0, new 0.

**Prior parts:** 18 of 18 have their ETags unchanged.

## 3. THE ONE REAL RUN (`round18/close_run_round18.py` -> `.out.txt`): CLOSE RUN OK

The run invoked the deployed `opal-amgt-scoped-api` `/timeline` for ASML_NA, DELL, BA and FDX: all four returned HTTP
200, with series equal to the newest landed daily on 272 of 272 days each (0 field mismatches), and events equal to the
newest landed events. ASML_NA now serves **74 PARTIAL** days (07-15 onward), which were DENIED before (row `Z-W45-S2`;
148 cells across its two listings).

**Row `Z-S41` (OBSERVATION, INERT):**
- The scoped API was redeployed by AMGT_RESAPP ww-1 at 19:18:58Z (`lg6NJ2JL...`). That was between the two halves'
  reader read and the puts.
- The close run above is the read of that combined state, and it is correct.

## 4. FOR L9 -- JUDGMENT CRITERIA, PRESENTED AND NOT GRADED

1. **`g-1` AC4, "is the added hit the company?"** `deliverables/0.9.0_WK_AMGT_HARVST~45/ac4_output.txt`: 179 of 244
   added hits across 52 form blocks, seed 20260929. This grades the rule on its own output, as the round-17 analysis
   asks. The exact-case short tickers (`HD`, `KO`, `BA`, `MU`, `NOW`, `COST`) are the adversary. The control mutant
   shows that case-insensitive matching would have admitted 100 lower-case hits (NOW 63, COST 30, FIX 5, DECK 2); the
   rule admits 0.
2. **`g-2` AC4, on the SERVED rows.** `deliverables/0.9.0_WK_AMGT_HARVST~45/g2_ac4_output.txt`: 0 new or moved events
   of 8. It presents the 11 new or newly tier-A/B mention rows (of 146 tier-A/B served) in 7 form groups, each with its
   headline and the words around the match. **Is each one the company?**

Rows this round: `Z-W45-S1..S4` (worker, all INERT) and `Z-S41` (issuer, INERT). None ARMED, none BLOCKING.
