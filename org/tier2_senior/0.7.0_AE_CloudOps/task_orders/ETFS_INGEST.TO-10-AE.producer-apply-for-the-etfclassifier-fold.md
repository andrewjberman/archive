# TO ETFS_INGEST.TO-10-AE — APPLY THE PRODUCER PACKAGE CARRYING THE ETFCLASSIFIER FOLD

<task_order id="ETFS_INGEST.TO-10-AE" project="ETFS_INGEST">
<id>ETFS_INGEST.TO-10-AE.producer-apply-for-the-etfclassifier-fold</id>
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — **NO NEW CELL.** This TO is the **APPLIED rung** of `INGEST-T3-6` and `INGEST-T5-1`, the same cells `ETFS_INGEST.TO-9-AE` served for the TO-6/TO-8 change. <owned_cells>INGEST-T3-6, INGEST-T5-1</owned_cells></decomp_ref>
<issued_to>`0.7.0_AE_CloudOps~M`</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T18:3xZ</issued>
<status>complete -- SELF-MARKED by the assignee per org/XXX.md, 2026-08-29T13:2xZ, by `0.7.0_AE_CloudOps~M` on `2.0.0_SA_COO~Z`'s re-address. AC1-AC4 ALL PASS; proof-of-spec instance reads VALID, violations=0, WITH coverage checked against the TO's own declared expected set (expected=4 carried=4 matched=4) and a negative control that FIRES on a planted fifth id -- so the coverage limb is a live instrument here, not a silent pass. AC1/AC2/AC4 were filed 2026-08-28 by `0.7.0_AE_CloudOps~I` and are NOT re-opened. THIS SEAT SCORED AC3 ONLY, on the event the face was waiting for: the 2026-08-29T13:00Z scheduled fire, which the producer's own log declares `run_class=scheduled` (RequestId 497b6400-2342-485d-9936-4a67aa35b60a). The no-ad-hoc bar is discharged BY MEASUREMENT, not by restraint -- 0 invocations between the 2026-08-28T18:49:14Z apply and the fire, 1 invocation on 08-29, over a 14-of-14 unpaginated log-stream census. On the served plane (s3://opal-data-portal-v2/platinum/etfs/positioning_data.json, VersionId bpgnYq4ir2yrM5cnWgJ35DzmnqalquU5, sha256 80c128dcf08b3855... == the sha256 the publisher logged at build time): 7 of 7 label completions over 59 of 189 rows, `inferred-from-truncation` on 59 of 59 changed rows, `observed` retained on 121 of 121 unchanged equity rows, and 0 values remaining at Bloomberg's 30-char cap against 6 pre-fire. AC4 additionally RE-SCORED on the real served before/after pair (the stronger instrument, unavailable to the earlier lane): 189/189 rows, 0 gaining or losing the key, 0 losing a value. **A NOTE FOR THE NEXT READER, because the issuer's located evidence reads as a negative and is not one:** the "6 values at exactly 30 chars, max length 30" measured at re-address is the GOLD parquet, and gold is CORRECT to carry the capped strings -- the decode is publisher-side at platinum-write time (`etf_positioning_publisher.py` `_industry_group`, read at the applied pin b066be7a92). Two planes, one artifact name. Nothing here stamps ETFS_INGEST or D4 closed. Push is the integrator's act and is NOT taken.</status>
</task_order>

<proof_of_spec>
  <criterion id="INGEST-TO10-AC1" cell_refs="INGEST-T3-6"/>
  <criterion id="INGEST-TO10-AC2" cell_refs="INGEST-T3-6, INGEST-T5-1"/>
  <criterion id="INGEST-TO10-AC3" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO10-AC4" cell_refs="INGEST-T3-6"/>
  <expected_criteria>INGEST-TO10-AC1,INGEST-TO10-AC2,INGEST-TO10-AC3,INGEST-TO10-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_INGEST.TO-10-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4, firm-tokened `INGEST-TO10-ACn`. Cells: 2, both pre-existing — this is an APPLIED rung, no new cell. **AC3 is EVENT-GATED on the next scheduled fire and cannot close on the first filing**; a 3-of-4 instance is the expected first state, not a failure.</alignment_denominators>
</proof_of_spec>

## WHY THIS EXISTS — MEASURED, NOT INFERRED

```
  etf-positioning-producer   deployed LastModified   2026-08-28T02:43:57Z
  the ETFClassifier fold     committed               b0e1f33471, ~18:3xZ
```
**A package deployed at 02:43:57Z cannot contain an 18:3xZ commit.** So the running bytes do not
carry the GICS decode, and **tomorrow's ~13:00Z fire would serve the OLD truncated labels** while
every source-side artifact says the fix shipped.
⚠ **THIS IS THE SAME SHAPE AS THE D1 GOLD-LAMBDA FINDING EARLIER TODAY** — committing is not
executing, and a source read cannot answer a question about the deployed plane.
`0.4.0_DS_ClientPlatform~Q` named this in its completion report (*"Needs an AE apply of the producer
package, THEN a scheduled fire"*) and correctly did not take it: it is not that lane's.

## NEVER-LAW, RIDING EVERY CRITERION

- **`safe-apply` ONLY.** Bare `terraform apply` is a NEVER.
- **Terraform ONLY.** `aws lambda update-function-code` is a NEVER.
- **Ledger entry OPENS AT START, CLOSES AT COMPLETION** (NEVER#6).
  ⚠ `0.4.0_DS_ClientPlatform~Q` hit a real trap here today: **it chained a close-edit and its commit
  with `;` instead of `&&`, the edit aborted, and the commit published the PRE-EDIT state and
  reported success.** Use `&&`.
- **NEVER#1 IS ALREADY SATISFIED — DO NOT RE-RAISE IT.** Both halves given (`1.0.0_SA_CTO~Z` +
  `2.0.0_SA_COO~Z`) against a measured radius of **59 of 189 rows, 7 labels, display text only**.
  Grouping, rollups and joins key on the 4-digit code and do not move.

## ACCEPTANCE CRITERIA

**AC1 `INGEST-TO10-AC1` — THE DEPLOYED BYTES CARRY THE DECODE.**
Pull the deployed package, extract the classifier module, and show the decode is present. **Prefer
`cmp` against the source at the applied commit** — byte-identity against the BUILD INPUT is Rule 22a's
actual ask and needs no pattern. If you use a grep instead, **carry a POSITIVE CONTROL**, and be aware
that today an arm asserting a string must be ABSENT was unsatisfiable because the fix documented the
defect it removed. ⛔ **A changed `CodeSha256` or an advanced `LastModified` is NOT acceptance** — both
are true of any deploy, including one built from the wrong input.

**AC2 `INGEST-TO10-AC2` — DEPLOYED VIA `safe-apply`, LEDGER OPENED AND CLOSED.**
Plan reviewed before apply; added/changed/destroyed recorded. A `plan` 0-diff is not evidence for AC1.

**AC3 `INGEST-TO10-AC3` — EXERCISED: the first SCHEDULED fire after the apply.**
⚠ **EVENT-GATED — CANNOT CLOSE TODAY.** The producer fires ~13:00Z. On the first scheduled fire after
this apply, the served artifact must show the 7 completed labels, with `industry_group_basis` reading
`inferred-from-truncation` on the changed rows and `observed` retained on rows the decode returned
unchanged.
⛔ **NO AD-HOC RUN TO BEAT THE CLOCK** — it would destroy the discriminator the scheduled run exists to
produce, and an ad-hoc artifact is never production evidence.
⚠ **THE 59-OF-189 FIGURE IS A PREDICTION FROM SIMULATION, NOT A SERVED MEASUREMENT.**
`0.4.0_DS_ClientPlatform~Q` recorded it that way deliberately. **The fire is what says it happened** —
score what the artifact does, do not grade it against the prediction.

**AC4 `INGEST-TO10-AC4` — NO REGRESSION.**
`industry_group` key present on the same row count before and after; **0 rows lose a value; 0 rows
gain or lose the key.** The pre-state to compare against is in that seat's completion report.

## BARRED / REPORTING

⛔ Nothing here stamps `ETFS_INGEST` or D4 closed — Andrew ruled "D4 is done" a READ, not a close order.
⛔ **Andrew ordered the naming-detail traffic STOPPED at 18:24Z.** This TO is the DELIVERY of a decided
thing, not further adjudication of it. **Do not re-open the member, the completions, or the radius.**
RAVC to `2.0.0_SA_COO~Z`, **once**. Push is the integrator's act. Off-task findings: one line to the
surprise channel, and keep working.


## SEATING -- RE-ADDRESSED 2026-08-29 ~13:0xZ TO `0.7.0_AE_CloudOps~M`

⛔ **THE PRIOR LANE WAS DEAD AND THE FACE SAID SO; THE EVENT IT WAITED ON HAS NOW HAPPENED, SO THE
SEAT IS CORRECT NOW AND WOULD HAVE BEEN PREMATURE BEFORE.** The face's own plan was *"at ~13:0xZ,
seat a FRESH lane of this class and re-address this face"*. This is that act, by `2.0.0_SA_COO~Z`
(issuer; COO spawn/seat authority per Andrew 2026-08-28 15:32Z).

```
  1pt process truth   9 claude.exe live -- 0.7.0_AE_CloudOps~M proc=0
                      POSITIVE CONTROL 0.4.0_DS_ClientPlatform~Y (seated 12:5xZ) proc=1 -> not blind
  1b  marker scan     0 hit(s)   (same control: ~Y = 1 hit)
  1c  concurrency     8 of 16 spawn-marker windows
  1d  encumbrance     0 open TOs . 0 project/mission owner rows . channel hits are `surfaced_by`
                      ONLY -- AUTHORSHIP, NOT OWNERSHIP, and only ownership is an obligation
  1d-ii artifact      the proof-of-spec INSTANCE is PRESENT and its event-gated criteria were
                      UNSCORABLE until this fire. NOT a stale face over finished work.
```

⚠ **`<issued_to>` NOW CARRIES THE SERIAL AND NOTHING ELSE.** `to-check` renders the FIRST
serial-shaped token in that field, so prose containing serials makes a face render against the wrong
seat. The prior field's text is preserved in git history; the seating narrative lives here.


## POST-FIRE EVIDENCE, MEASURED BY THE ISSUER 2026-08-29 ~13:0xZ -- LOCATED, NOT ADJUDICATED

The **Saturday 2026-08-29 13:00Z** `etf-positioning-producer-daily` fire RAN AND ADVANCED THE
FRONTIER. This face's event gate is DISCHARGED: there is now a post-fire served artifact to score.

```
  gold/holding/date=2026-08-28/holding.parquet   45,630 B   LastModified 2026-08-29T13:01:22Z
  gold/_manifests/2026-08-28/0f277195f2d7.json    3,068 B   same stamp -- THE RUN COMPLETED
  189 rows . 169 distinct ticker . 183 rows at 8-of-8 return windows . 6 rows at 0-of-8
```

⛔ **AND THE WEEKEND PREDICTION IN THIS FACE'S OWN HISTORY WAS WRONG FOR THIS PIPELINE — READ THIS
BEFORE SCORING.** An earlier amendment warned that *"a correct Saturday run may write NOTHING because
the trading-day frontier has not moved"* and that **`AFTER == BEFORE` is the expected weekend
outcome**. That is the **MDPF** mechanism — a CONTENT-derived `as_of` (`derive_as_of()`,
`mdpf_gold_consolidator.py:1106`). **ETF positioning is CALENDAR-anchored**:
`etf_positioning_gold.py:497` and `:1672` use `tcal.expected_last_trading_day(now)`, which for
Saturday 2026-08-29 is **2026-08-28** — and `bbg/2026-08-28/` existed as input. **So it advanced, as
predicted before the fire.** `3.0.0_SA_CVO~Z` fenced their MDPF frontier result at exactly this
pipeline boundary (msg 16732) before anyone carried it across. **AFTER == BEFORE WOULD HAVE BEEN THE
DEFECT HERE, NOT THE EXPECTED OUTCOME.**

⚠ **THE MEASUREMENTS BELOW ARE EVIDENCE LOCATED FOR THE SEAT, NOT A VERDICT ON ANY CRITERION. THE
ISSUER HAS NOT READ THIS FACE'S AC TEXT IN FULL AND IS NOT SCORING IT.** In particular Andrew
narrowed the delivered scope at 2026-08-28 18:24Z, VERBATIM: *"the subsector name is not that
important, as long as it is properly managed within ETFClassifier, it is done."* **Whether a served
30-char string is in or out of the accepted scope is the executor's reading, not the issuer's.**

```
  industry_group in the POST-FIRE artifact: 23 distinct values over 180 non-null of 189 rows
  SIX sit at EXACTLY 30 chars (Bloomberg's cap), max len over all values = 30:
    'Commercial & Professional Serv'   'Consumer Discretionary Distrib'
    'Health Care Equipment & Servic'   'Pharmaceuticals, Biotechnology'
    'Semiconductors & Semiconductor'   'Technology Hardware & Equipmen'
```

⭐ **AND AN UNRELATED FINDING IN THE SAME ARTIFACT, ROUTED ELSEWHERE — DO NOT CHASE IT FROM THIS
FACE.** `ABT` (Abbott, DIVZ) carries **0 of 8** return windows in BOTH the 08-27 and the 08-28
partition, so the defect is **REPRODUCED ACROSS TWO CONSECUTIVE SCHEDULED FIRES** rather than a
one-day glitch. Its weight moved **2.36 -> 2.33** between them, which is the discriminator: **the
book row refreshes daily and only the RETURN SERIES has no source.** That is
`ETFS_POSITIONING.TO-13-DS`, seated on `0.4.0_DS_ClientPlatform~Y`, and it is NOT this face's work.
