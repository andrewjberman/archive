# AMGT_RESAPP round 54 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.62, issuance `24a11743a1`, on the CTO's round-53 analysis `d379533291`. Four orders, all
terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| ad-1 the no-span census = the hold transform's dry-run | LOCAL | ~193 | drain `4852128779` | `drafting_build.hold_unspanned` + `--hold-unspanned` (dry-run, `--census-out`). Census: 179 no-span sentences in 12 stored D-1 documents, equal to an independent recount. 12 new tests; 146 passed. VALID |
| ad-2 the hold on the object | WORLD | `0.7.0_AE_CloudOps~A` (respawned 18:5xZ: the seat was dead) | entry CLOSED `bcada3e9ea`, issuer close `2e9c087db4` | Halves: COO `18ac256769`, CTO `04f779ac51`. Pin `4852128779`. AMENDMENT 1 `2de4b63291` (AC3: the posture pack, per the CTO's reader-census ruling). AMENDMENT 2 `9d5bd13f74` (see section 3). Act ~19:48Z: 12 of 12 documents rewritten, 179 held. No rollback |
| ad-3 one verified upload for every harvest build script | WORLD by the L6 floor (code only) | ~194 | drain `71f1cafcab` | `infra/aws/terraform/harvest/upload_verified.sh`, sourced by all four `build-and-upload*.sh`. No path conversion on the metadata; a read-back refuses a mismatch; `build-and-upload.sh` moved onto the `.tools/aws` shim. Disarms Z-S319 / Z-S321. VALID |
| ad-4 FWD-30's grader reads an UNRESOLVED figure's raw digits | LOCAL | ~195 | drain `a4685945b8` | `sweep.py`: "unit not resolved -- raw figure N" reads as N, and grades equal ONLY against an UNRESOLVED export unit. The issuer escaped two non-ASCII dashes (`18ac256769`). VALID |

Worktrees `C:/tmp/r54-193..195`: branches merged; checkouts KEPT pending Andrew's go.

## 2. THE RESULT -- the issuer's real runs, at close

- **The store** (ad-2 AC1, issuer re-read): 12 documents; 179 sentences moved to `held_no_span` in the pipeline's held shape.
  - 0 no-span sentences left in any section.
  - The 210 span-carrying sentences are byte-equal (text and spans, in order) to the pre-act bytes.
- **The served /thesis** (ad-2 AC2): 12 of 12 names.
  - Sentence text is unmoved, and `held_no_span_count` is unchanged.
  - `held_no_span_at_read` is 0; `held_no_span_on_object` equals the count; the basis is `READ_GATE_PLUS_OBJECT`.
- **The posture pack** (ad-2 AC3): it loses exactly the 179 sentences. The served `posture/v1` moves only when the posture batch next
  runs; no batch ran.
- **The upload helper** (ad-3): a sha starting with `/` reaches a native program intact; a mangled read-back is refused.
- **FWD-30, the full served sweep at close:** **equal 96 of 96 identified names, values 96 of 96, 32,468 value facts compared, 0 differ,
  cases 288 of 288, CAPTURE_FAILED 0, sweep exit 0** (`round54/captures/fwd30_close_sweep_served_20260930T205921Z.{log,tsv}`, the
  live research library read at 20:59Z). TSM is now equal (ad-4). **The library grew to 97 folders:** `Brookfield Corporation BN CA`
  does not resolve to an identity, so it is counted UNIDENTIFIED and not graded (1 of 97) -- see section 6.

## 3. For your L8 read: a criterion RE-SCOPED AFTER IT FAILED (ad-2 AC2, AMENDMENT 2)

The CTO (msg 27358) asks for this to be recorded as a re-scope after failure, graded on its planted negative.

- **What failed.** AC2 as cut compared every non-volatile top-level key of the /thesis body. It failed on VLO only. The one difference
  was the nested `model.generated_at`, 19:37Z -> 19:53Z. That field is `_now_iso()` at read (`scoped_amgt.py:3417`, the CTO's
  reading), and VLO's model block has not changed since 09:40Z.
- **What AMENDMENT 2 does.** It drops the read-time stamps at every depth.
- **Negative arms:**
  - the issuer's plant, a nested non-volatile key under `model`: FAILS, exit 1;
  - the executor's plant, VLO `px_last` 382.86 -> 383.86: FAILS, exit 1.
- **Owner.** This is the issuer's instrument defect, the fourth of the class in this span (Z-S311, the FWD-30 plants, ac-3 AC3, and
  this one).
- **Ruling 1 caught two other defects before the cut.** The positive arm was run on every check: ad_1_hold's first held-entry shape was
  refused by the deployed validator, and ad-3's harness first handed `/tmp` paths to a native stub. It did NOT catch this one, because
  the simulated served post-state was built from the saved pre bodies and so carried the SAME `generated_at`. **The simulation cannot
  vary a field the check forgot to exclude.**

## 4. Judgment criteria

None this round.

## 5. Rows this round (L8 input)

| row | source | standing | what it records |
|---|---|---|---|
| Z-S322 | AE~A | OBSERVATION, INERT | `deploy_ledger.py open` stages its files into the shared index, so two peer drains (3ac5a8666e COO~RV, f3980a84ab COO~H) absorbed the ad-2 entry under their author lines before the executor's safe-commit. The content is correct, but the author line and the lane check are lost. Candidate repair: `open` writes and leaves the files unstaged |

## 6. Carried to the CTO's round-54 analysis

1. **Z-S322:** `deploy_ledger.py` stages on the caller's behalf. It is a fabric tool outside RESAPP's decomposition, so the owner is
   yours to name. INFERRED, not measured: every tool that stages for its caller has the same shape.
2. **The next posture batch** runs on packs without the 179 sentences. Its `posture/v1` diff is to be read when it runs (CTO half
   section 4). The packs' `S:<section>:<n>` ids renumber within a section.
3. **FWD-30:** 96 of 96 identified names equal at close. TSM `CURR_ENTP_VAL` grades equal (both sides unresolved, digits equal); its
   UNIT is still unresolved upstream, which is CORPUS's to resolve. **New:** the research library gained `Brookfield Corporation BN CA`,
   which has no identity in the crosswalk -- FWD-30 covers 96 of 97 folders until that name is onboarded (a universe/CORPUS act, not a
   RESAPP cell).
4. **The instrument lesson** (section 3): a positive arm simulated from pre-act data cannot exercise a volatile field. The CVO proposal
   `PROPOSAL_POSITIVE_ARM_BEFORE_THE_CUT_20260930_Z.md` may want that clause.
5. **Parked (unchanged from round 53):** site Z's `test_seed_etf_constituents.py:201-203` must assert the conditional put once origin
   `9e4997d618` lands on site Z.
