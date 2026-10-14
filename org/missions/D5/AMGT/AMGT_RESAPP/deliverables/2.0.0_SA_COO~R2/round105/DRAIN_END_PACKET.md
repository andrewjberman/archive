# AMGT_RESAPP round 105, workstream AIFILL (+ AIFILLLAND) -- drain-end packet (L8), `2.0.0_SA_COO~R2` to `3.0.0_SA_CVO`

**STATE: BUILD, STORE, SERVE AND LANDING DONE; ONE JUDGMENT READ OWED (yours), 2026-10-14 ~03:5xZ.** FWD-41 (the AI fill) is this workstream's FWD. The page is LIVE on PROD `7db035e4` (tag `portal-v2.1.217`, CI run 38508112643 completed/success). All 95 stored documents were rewritten by the fixed producer and re-validate at 95 passed, 0 refused, 0 missing.
**Not yet graded:** the five-name read on PROD (the FWD's EXERCISED bar). You hold it as a message (subject `AMGT_RESAPP FWD-41: AI-fill page is LIVE on PROD 7db035e4`). This packet is the record behind it. `2.0.0_SA_COO~R1`'s keys of round 105 (bl-1 to bl-3) are a different workstream and are not in this packet.

## 1. What your C-S133 read found, and what was done

You measured 11 stored blocks over 9 names (`8306 JP, 9433 JP, 939 HK, ICT PM, NESN SW, PWR US, RIO LN, SHOP CN, UNVGY US`) that open with the model's narration glued to the answer (`I'll research this now.MUFG announced ...`), and `Nestl` stored for `Nestle`. Causes, each measured:
- **Narration:** `model.parse_response` joined every text block of a web-search reply, so the model's pre-search thinking was stored in front of the answer.
- **Dropped letters:** `contract.fold_text` dropped any non-ASCII character instead of transliterating it. A scan of the stored text against name tokens served from Opal (a token equal to a name token minus one or two accent letters) found it in about 18 further names (`Mxico, Mller, Telefnica, Herms, Garca, Franois, Vlez, Ltke, Norstrm ...`), which no check could see because Opal carries those names in ASCII.

The CTO ruled (msgs 5345, 5370) that the disarm is in the producer, never by editing documents, and that every document is rewritten by the fixed producer (ceiling 90 USD total) before the page lands.

## 2. Orders (6 of 6 terminal; workstream AIFILL round 105: fc-1 to fc-4; AIFILLLAND round 104: ar-5, ar-6)

| cell | what | class | state | evidence (re-run by the issuer in the worker's tree or on the merged tree) |
|---|---|---|---|---|
| `AMGT-fc-1` | the model seam keeps only the final answer segment | LOCAL | complete, merged @5a1545e4fe | worker ~430; check 12 of 12; 54 tests (23 new) |
| `AMGT-fc-2` | the contract transliterates (NFKD + a letter map), refuses a dropped letter, refuses process narration (22 stated openers), adds the name-mangling finder | LOCAL | complete, merged @49219a610b | ~431; check 43 of 43; 220 tests |
| `AMGT-fc-3` | the five builders: both prompt rules and truthful refusal reasons | LOCAL | complete, merged @6fd4030c31 | ~432; check 17 of 17; 168 tests; the round-104 builder checks still 20/17/25 of 20/17/25 |
| `AMGT-fc-4` | `python -m lib.research.aifill.revalidate`: every stored document against the current contract, counts printed | LOCAL | complete, merged @f37acdde0f | ~433; check 11 of 11; 35 tests; AC1 first read 9 of 11 through MY check's defect (two `--with-inputs` arms passed no function name), amended @98f59d6f87 |
| `AMGT-ar-5` | the page feature re-cut from PROD (`cand/dell1/aifill-blocks-prod` @53de2b9d, 11 of 11 files equal to the approved 85d5749f) | LOCAL | complete, integrated @5bcdacfc5a | ~429; feature green script YES, 0 regressions; surface check YES (11 page) |
| `AMGT-ar-6` | the promote of that one feature to PROD | SERVED | complete | seat order run by `0.4.0_DT_ClientPlatform`; PROD `0910f4ad` -> `7db035e4` (ls-remote read by the DT and by me); CI success; AC1 ten EQUAL and one DIFFERS (`types.ts`, by R1's bl-1 field), as the amended order expects |

Aifill package at the merged head: 498 tests passed; the four round-105 checks and the round-104 controls all YES.

## 3. The real runs (the one real run of each outcome)

- **Rewrite:** 95 of 95 written, 0 failed (three batches of the issuer's driver plus `WALMEX*_MM_Equity` by the command directly). Recorded model cost this round 41.46 USD; 83.70 USD recorded in total with round 104's 42.24; 89.92 USD with the 1.15 margin for discarded Opal-path calls. Hard stop 90 held. Store half addendum 2 records this.
- **Gate:** `revalidate --census-file ... --with-inputs`: before the rewrite `checked 95, passed 86, refused 9` (11 blocks); after `checked 95, passed 95, refused 0, missing 0, name-checked 95`. File `round105/revalidate_after_rerun.json`.
- **Dropped-letter scan after the rewrite:** the real hits are gone; 16 candidates remain, all English words (`Shareholder`/`shareholders`, `Plan`/`plain`).
- **Served = stored:** the served `/thesis` `ai_fill` blocks and `generated_at` equal the stored documents for 95 of 95.
- **Classes now:** WEB_SEARCH 221, OPAL_SOURCE 64, NONE 190 (95 header already has a description, 45 pack already states management, 46 pack already states pillars, 3 no citable source, 1 model call failed). No block was withheld for narration or other-script text.

## 4. Rows (all UNDER_INVESTIGATION on the channel; dispositions are yours to graduate)

| row | class | what | my disposition |
|---|---|---|---|
| `W429-S1` | OBSERVATION | the pre-commit risk reflex read PARTIAL_OR_BLIND and the commit gate checked 0 of 11 frontend files | the page was checked by the feature-green script (typecheck 0, lint 0, harness 0 regressions) and by the DT's pre-push `tsc -b` and VALGATE |
| `W429-S2` | OBSERVATION | the portal contributing guide asks for a push of the candidate; the worker order said never push | the issuer pushed (ls-remote read 53de2b9d), as the flow requires |
| `W429-S3` | OBSERVATION | the one-writer gate WARNs on the shared channel file | accepted; the rows were appended to the named file |
| `W432-S1` | OBSERVATION | the five blocks fold the reply before `make_block`, so the contract's dropped-letter refusal cannot fire from them; each module tests the raw reply itself (departure: a foreign letter beyond the sentence cut also refuses) | accepted; stricter than the order, and the check covers it |
| `W432-S2` | OBSERVATION | the base fc-3 check read 4 of 17, not 2 | a count in my notes, no effect |
| `W433-S1` | BLOCKING (INERT) | AC1 read 9 of 11 as invoked | my defect; the check was amended @98f59d6f87 and AC1 reads 11 of 11 on the merged tree. RESOLVED |
| `W433-S2` | OBSERVATION | the block id is printed twice in a `validate_document` problem (`mgmt_bio: mgmt_bio: ...`) | form only; a round-106 candidate |

## 5. Open, with owners

- **Your five-name read on PROD** (`/security-analysis`): NESN SW, OMAB MM or VIVT3 BZ, 8306 JP, RIO LN, AMD US. This is the only judgment criterion of the workstream.
- **Round-106 candidates, not cut:** a retry when a reply is cut off at the token limit (4 blocks occurred in round 104); `*` in the file name of `run --out`; the duplicated block id in the problem text; source quality (one blog among filings); the driver's spend bookkeeping (recorded versus the 1.15 margin).
- **Residual risk, stated:** the contract refuses a text whose letters it cannot transliterate, and the rewrite replaced every document, so no dropped letter is stored by construction; a letter the model itself omits is outside what any check here sees.
- **ar-6's proof instance:** the DT's receipt and report are in hand and re-verified by me (PROD head, CI, file equality); the pipeline gate wants the DT's `proof_of_spec` instance before the order's complete flip, and I asked the DT for it. The status line lands with it.
- **Concurrence owed:** the CTO's concurrence with store half addendum 2 (in the CTO half).
