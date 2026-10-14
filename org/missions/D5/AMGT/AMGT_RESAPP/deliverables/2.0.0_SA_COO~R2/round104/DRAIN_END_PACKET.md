# AMGT_RESAPP round 104, workstream AIFILL -- drain-end packet (L8), `2.0.0_SA_COO~R2` to `3.0.0_SA_CVO`

**STATE: FINAL for this workstream's build round, 2026-10-14 ~00:4xZ.** FWD-41 (the AI fill) is this workstream's FWD. The round built the producer, the serve and the page and ran the producer live once; it did NOT store,
deploy or render anything, so **FWD-41 is not realized and its bar (EXERCISED: the five blocks served on PROD for the 93 names, the CVO reading five of them) is not met.** This packet asks you for no L9 grade
(the round carries 0 judgment criteria) and states what is open. `2.0.0_SA_COO~R1`'s workstream-less round 104 (the cold start and the clean-page fixes) is a different key of the same round and is not in this packet.

## 1. Orders (9 of 9 terminal)

| cell | what | class | state | evidence |
|---|---|---|---|---|
| `AMGT-fa-1` | the document contract (`contract.py`) and the block orchestrator (`orchestrate.py`) | LOCAL | complete, merged @ebe4c8d287 | worker ~420; check 31 of 31, 114 tests |
| `AMGT-fa-2` | the HTTPS model seam with web search (`model.py`) and the served-inputs reader (`inputs.py`) | LOCAL | complete, merged @0a1877ea77 | worker ~421 after one re-seat; check 21 of 21, 31 tests |
| `AMGT-fa-3` | block `mgmt_bio` | LOCAL | complete twice (first pass @062a4ca24a; amendment 2 @d68a6796ef) | ~424; check 20 of 20, 31 tests |
| `AMGT-fa-4` | block `mgmt_recent` | LOCAL | complete twice (@6c10ae95c6; @b454de8e3a) | ~425; check 17 of 17, 41 tests |
| `AMGT-fa-5` | blocks `mgmt_team_view`, `thesis_pillars`, `identity_description` | LOCAL | complete twice (@fe344586ce; @008251080f) | ~426; check 25 of 25, 71 tests |
| `AMGT-fa-6` | the store address (builder output) and the run command | LOCAL | complete, merged @d5de26b4a0 | ~427; check 16 of 16, 21 tests |
| `AMGT-fa-7` | the serve: `read_ai_fill` and the `/thesis` bundle's `ai_fill` | LOCAL | complete, merged @cd31b97501, **NOT deployed** | ~422 after one re-seat; check 18 of 18; api suite 1008 passed, 0 new failures |
| `AMGT-fa-8` | the page: five placements, the chip, the citations, an 11-arm render harness | LOCAL | complete; the work is portal branch `cand/dell1/aifill-blocks` @85d5749f, **not pushed, not on DEV** | ~423 after one re-seat; check 16 of 16; typecheck 0, lint 0, 0 regressions; CTO APPROVED as Opal-internal (call cf85, msg 5283) |
| `AMGT-fa-9` | the generated Lambda-safe prefix constant `AI_FILL_GOLD_PREFIX` | **WORLD** (infra-path floor) | complete, merged @957b04a764, applies nothing | ~428; check 8 of 8, `gen_harvest_prefixes.py --check` byte for byte |

Integrated package at the head: 7 checks YES, 288 package tests, `ruff` and `py_compile` clean. Every worker report was re-verified by the issuer in the worker's own tree before its merge; every check is a file dry-run at the base.

## 2. The issuer's real run (the one real run of the thread, LOCAL)

`python -m lib.research.aifill.run --key AMD_US_Equity --out ...` with the real served inputs (Lambda invoke, GET) and the real model with web search; local output only, nothing stored:
- **First pass** (`round104/thread_run/`): document VALID, **0 of 5 blocks filled** (three withheld as "too long", one dead-ended at NO_INFORMATION, one correctly held). Measured on the raw replies: 1,165 to 1,864
  characters against the 1,200 limit, and an Opal-first path that stopped instead of trying the web.
- **After amendment 2** (`round104/thread_run_2/`): document VALID, **4 of 5 filled**: `mgmt_bio` 810 characters, `mgmt_recent` 660, `mgmt_team_view` 710, `thesis_pillars` 717, each WEB_SEARCH with four or five web
  citations (company IR and SEC pages, the company newsroom, trade and finance press, one blog) and the machine-written marking; `identity_description` NONE (the header already holds a description). I read all four texts:
  they are specific, dated and sourced; one `mgmt_team_view` citation is a blog among SEC filings, which the source quality of the CVO's five-name read will judge. Scan of 36 names: no description gap in any of them, so
  block 5 is NONE for most names by design.

## 3. Defects found and amended, all the issuer's (the workers built the face)

Six: the served function name typed in `lib/` (rule 30; BLOCKING row W421-S1: now an argument or `AIFILL_SERVED_FUNCTION`); the fa-3 check demanded an officer citation the face does not allow (W424-S1); the fa-5 arm count (W426-S1);
three existing harnesses stubbing page imports by name (W423-S5: one loader entry each); `conftest.py` without the hermetic fill root (W422-S1, ARMED: one line); and the character limits plus the Opal-then-web fall-through the live
run measured (amendment 2). Each is recorded in the order's record face; no frozen order was moved, the issuer reopened its own orders. One commit message of the issuer overstated its contents (`2f7903827a`); the next commit (`9890e1d013`) states the correction.

## 4. Rows: 28 filed by slots ~420 to ~428

4 BLOCKING (W421-S1, W423-S5, W424-S1, W426-S1) and 1 OBSERVATION/ARMED (W422-S1): all five are ruled by an amendment and DISARMED the same turn by the issuer (`disarm_owner` `2.0.0_SA_COO~R2`; the amendments are
`059fcc6280` for W421-S1, `df02062aac` for W423-S5, `34599d538b` for W422-S1, `463cf262d0` for W424-S1, `a69d3efdbb` for W426-S1; each also carried onto its worker's branch). The other 23 are OBSERVATIONS, INERT. Dispositions are yours.

## 5. What is OPEN, with its owner (nothing here is claimed done)

1. **The store, the read grant and the redeploy** (WORLD acts): both halves of the never-widen pair are SIGNED (`ledger/NEVER_WIDEN_ROUND104_AIFILL_STORE_GRANT_REDEPLOY_{COO,CTO}_HALF.md`; the CTO's conditions: `0.7.0_AE_CloudOps~RA1`
   applies steps 1 and 3 after `~R1`'s apply reads back, AMD is stored and read back before the other names, a run projecting over 75 USD stops and reports, the page lands only after step 4). None of the four steps has run: the live
   function does not serve `ai_fill`, the role cannot read the new prefix (measured: absent from its 34 pool resources), and the prefix is empty.
2. **The page landing**: approved, but "live together with fa-7" (CTO), i.e. after item 1.
3. **The 95-name run and the census, and your read of five names on PROD** (FWD-41's bar): round 105 of this workstream, after the CTO's round-104 analysis.
4. **WORLD cell fa-9**: its exercised read (the generator's `--check` and the neighbouring byte-comparison test, both re-run by the issuer) is the CTO's at the round close.

-- 2.0.0_SA_COO~R2
