# TO ETFS_POSITIONING.TO-14-AE — APPLY THE IDENTIFIER-REPAIR PACKAGE (and it does NOT ship alone)

<id>ETFS_POSITIONING.TO-14-AE.identifier-repair-apply</id>
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md -- cells ETFS-a-1, ETFS-d-1</decomp_ref>
⚠ **APPLIED RUNG, NO NEW CELL.** `ETFS-a-1` IS `silver/holdings/{date}.parquet` — the artifact whose `cusip` the repair writes; `ETFS-d-1` is the producer. Same two surfaces `ETFS_POSITIONING.TO-13-DS` cites; this face changes the DEPLOYED STATE of them, not the cell set.
<issued_to>`0.7.0_AE_CloudOps~N`</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-29T13:4xZ</issued>
<status>active -- APPLIED 2026-08-29T14:17:24Z BY `0.7.0_AE_CloudOps~N`. **`POS-TO14-AC1` + `POS-TO14-AC2` + `POS-TO14-AC3` PASS -- 3 of 4.** `POS-TO14-AC4` alone remains UNCOMPUTABLE-BY-CONSTRUCTION and rides ONE named later run. ⭐ **AC3 SCORED ON THE SCHEDULED 22:00Z FIRE, 2026-08-29** -- `silver/holdings/2026-08-29.parquet`, 30,356 B, LastModified `2026-08-29T22:00:16Z`, ETag `e42b0a703b9b3377957318423e6df3a0`, inside the 22:00:14-17Z band seen on 8 of 8 prior days. **NO ad-hoc run was fired at any point.** Scored by an instrument written and certified 5-of-5 in BOTH directions BEFORE the artifact existed (its refuse path fired on REAL pre-repair data; its vendor-fix fixture passed). **ABT: `002824100`, `id_kind` moved `unclassified` -> `cusip`, `cusip_as_delivered '2824100'`, `cusip_basis 'zero-pad-restored'` -- OUR repair fired, distinguished from a vendor fix rather than assumed. ICT `6455819` and MER `B247XZ6` UNCHANGED and `as-delivered` -- the AC2 controls hold.** Basis split 182/5; histogram `{7:2, 9:182, 10:2, 12:1}` with the 8-char bucket VANISHED; per-fund 4-of-4 exact (DIVZ 4/1, IDVZ 1/0, PFDE 0, PFOE 0). Row total **187, PRINTED not matched**. ⛔ **FIRM TOKENS, NOT BARE AC NUMBERS -- `0.4.0_DS_ClientPlatform~Y` (16802) caught the collision: `ETFS_POSITIONING.TO-13-DS` HAS ITS OWN `AC1`-`AC4` AND THEY ARE DIFFERENT CLAIMS** (this face's are about the APPLY landing; TO-13-DS's are about the SERVED artifact carrying the repaired identifier). **A reader carrying a bare "AC1 + AC2 PASS" across the two faces closes TO-13-DS on evidence that does not touch it.** TO-13-DS's ACs remain UNCOMPUTABLE: measured, the newest silver partition is still `2026-08-28.parquet` at 22:00:16Z, which PREDATES this 14:17:24Z deploy, so there is no post-change row to read until tonight's fire. Instance VALID, violations=0, at `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-14-AE_PROOF_OF_SPEC.json`. Live `CodeSha256 rznYiHb5PiktdT/V7Ayls0djByQdvuJ9nQeVQsIS2gI=` (was `6RFz1jbz...`); the deployed `lambda_function.py` member is byte-identical to `353c4b5a00`/HEAD, and **the Z-S31 `RunDateFabricationGuard` IS present in the deployed bytes** -- the section-2 co-passenger landed and is reported, not discovered. The section-2 STOP TEST is DISCHARGED: the plan was `0 to add, 1 to change, 0 to destroy`, code attributes only, so no third seat's work was pending. ⛔ **THE TRADING CALENDAR MOVES AC4 THREE DAYS PAST THE NAIVE READING, AND A SEAT SCORING IT EARLY WILL MIS-READ A CORRECT PIPELINE AS A FAILED DEPLOY.** The gold producer REFUSES weekend silver (`etf_positioning_gold.py:501-509`; confirmed on both planes -- gold has no `date=2026-08-22/23` while silver does), so tonight's SATURDAY silver is skipped forever. **AC3 closes on the 22:00Z fire TONIGHT (`silver/holdings/2026-08-29.parquet`); AC4 cannot close until 2026-09-01T13:00Z on `gold/holding/date=2026-08-31/holding.parquet`.** Monday's own 13:00Z fire re-emits `date=2026-08-28` from PRE-REPAIR silver and that is CORRECT, not a regression. Deploy ledger OPEN at `.open_deploys/etfs-positioning-to14-identifier-repair-apply.json` (L1-L3 closed; L4/L5 are those two fires). ⛔ **SCORING IS SEAT-INDEPENDENT AND THE MARGIN IS 7.18h -- BOTH LEGS CARRY FULL EXPECT BLOCKS IN THAT SENTINEL'S `proof_required`, WRITTEN AS PREDICTIONS BEFORE THE ARTIFACTS EXIST.** Window EXPIRES `2026-09-01T20:10:56Z`; L5's EARLIEST scorable moment is `2026-09-01T13:00Z`. **That 7.18h is THE ENTIRE SLACK on the last leg and it falls across a weekend-to-Monday transition** -- if Monday's 13:00Z gold fire slips, or fires and nobody scores it within seven hours, this entry breaches the no-half-deploys window, and the breach would read as negligence rather than as a schedule that was always this tight. **Nothing is late; 73.2h remained when this was written (`2.0.0_SA_COO~Z` 16981, margin re-derived at this seat).** ⛔ **TWO TRAPS A RE-SCORER WILL OTHERWISE HIT: (a) `cusip_basis == 'zero-pad-restored'` IS NOT THE AC3 PASS CONDITION** -- a TrueShares upstream fix delivers `002824100` already, `cusip_basis` correctly reads `as-delivered`, and the criterion is still satisfied; the discriminator is `cusip_as_delivered` (`2824100` = our repair, `002824100` = vendor's). **(b) AC4 SCORES NAMED ROWS, NEVER THE TOTAL** -- the 0-of-8 set must be exactly {four CASH, `2602335D`} whatever the row count is; `189` is 08-28's inherited count (issuer-annotated `a3c8b63260`: PRINT the denominator, never MATCH it) and the 2026-08-28 partition measures 187 -- THERE IS NO 08-29 SILVER UNTIL TONIGHT'S FIRE, and an earlier line of mine wrongly said there was. ORIGINAL ISSUANCE CONTEXT FOLLOWS -- CUT ON A STAFFING CALL HANDED UP BY THE BUILDER. `0.4.0_DS_ClientPlatform~Y` finished `TO-13-DS` code-complete at `353c4b5a00` with ALL FOUR ACs filed UNCOMPUTABLE, because every one of them names an artifact that needs a Terraform deploy DS cannot perform. **They explicitly declined to pick a lane themselves — "picking a seat would be doing `2.0.0_SA_COO~Z`'s staffing" — and handed it up. This face is that call landing.** Lambda code deploy is Terraform-only (CLAUDE.md NEVER) and infra is DT/AE (Rule 13). ⛔ **NOT GATED ON ANYTHING. The code is committed and the instance is VALID; this is the apply leg.**</status>
<priority>P2 — the same priority as the defect it ships. One real priced holding (ABT, 2.36% of DIVZ) carries all eight return windows null on the served plane, reproduced across two consecutive scheduled fires.</priority>

<authority>
No sovereign word. Cut by `2.0.0_SA_COO~Z` under the **D1+D4 scoped `/drive` arm** (Andrew-direct
2026-08-28 ~02:3xZ). **This mirrors the split this project already uses** —
`ETFS_INGEST.TO-9-DS` (code, DS) / `ETFS_INGEST.TO-10-AE` (apply, AE), both closed today.
</authority>

## 1. WHAT TO APPLY

`353c4b5a00` — a repair at `holdings_rows_to_parquet`, the single choke point where `cusip` and
`id_kind` are both written. Two independent checksums, **SEDOL-refuses BEFORE CUSIP-repairs**:

```
  ABT  2824100  -> 002824100 passes CUSIP mod-10 . NOT a valid SEDOL  -> REPAIRED
  ICT  6455819  -> no padding passes CUSIP mod-10 . VALID SEDOL       -> untouched
  MER  B247XZ6  -> no padding passes CUSIP mod-10 . VALID SEDOL       -> untouched
```

Rule 17 is satisfied without destroying anything: the delivered value is carried forward verbatim in
a new `cusip_as_delivered`, and `cusip_basis` `{as-delivered | zero-pad-restored}` is the claim field
a consumer can reject on. **Bronze is untouched.**

## 2. ⛔ THE FIX DOES NOT SHIP ALONE — READ THIS BEFORE PLANNING

**The deployed function is ALREADY BEHIND the repo INDEPENDENTLY of this change**, measured by
`0.4.0_DS_ClientPlatform~Y`:

```
  deployed  lambda_function.py  69,897 B
            CodeSha256 6RFz1jbzLMXXoWOmEkjIe3JoEZAf7EaHpQ4CsZXzuK8=
            LastModified 2026-08-25T00:09:54Z
  repo      72,296 B  BEFORE the TO-13-DS edit
```

**The pending delta is the Z-S31 `RunDateFabricationGuard`, from a `1.0.0_SA_CTO~Z` ruling, authored
by ANOTHER SEAT and unrelated to identifiers. A DEPLOY OF THIS FIX CARRIES IT.**

⭐ **Divergence confirmed REAL, not the CRLF false-divergence class: CR count 0 in BOTH files.** That
check was run because a raw byte-compare reads DIVERGENT after a perfect round-trip when line endings
differ; it does not here.

⚠ **THIS IS NAMED, NOT GATED.** The guard is committed to the repo by an authorized seat under a CTO
ruling, and shipping repo state is what a deploy IS. **`1.0.0_SA_CTO~Z` is copied so the ruling's
author knows it lands; nobody needs to grant permission for a normal apply, and no seat should invent
a hold here.** If the plan shows anything BEYOND those two changes, stop and surface it — that would
mean a third seat's work is also pending and the radius is wider than measured.

## 3. ACCEPTANCE CRITERIA

**AC1 `POS-TO14-AC1` — DEPLOYED VIA `safe-apply`, LEDGER OPENED AND CLOSED.** Never bare `terraform
apply`; never `aws lambda update-function-code`. Plan reviewed BEFORE apply; added/changed/destroyed
recorded. Ledger entry in `org/critical_paths/change_management/` opened at start and closed at
completion. ⛔ **A `plan` 0-diff is not evidence for AC2.**

**AC2 `POS-TO14-AC2` — THE DEPLOYED BYTES CARRY THE REPAIR.** Diff deployed bytes against the BUILD
INPUT (source-map / manifest), **never by filename** (Rule 22a). Record the new `CodeSha256` and show
it differs from `6RFz1jbz…`. **Name the Z-S31 guard as also present** — the radius must be reported,
not discovered later.

**AC3 `POS-TO14-AC3` — EXERCISED ON A SCHEDULED FIRE, NAMED BY DATE.** An ad-hoc QA run is legitimate
for testing and is **NOT** the acceptance. ⛔ **DO NOT SCORE AGAINST A WEEKEND FIRE WITHOUT RESOLVING
THE TRADING CALENDAR.** Today is Saturday 2026-08-29. This producer is CALENDAR-anchored
(`etf_positioning_gold.py:497`, `:1672`, `tcal.expected_last_trading_day`) and **did advance today** —
so `AFTER == BEFORE` here would be the DEFECT, not the expected weekend outcome. **That is the
opposite of the MDPF content-derived rule; do not carry the MDPF result across the boundary.**

**AC4 `POS-TO14-AC4` — ABT CARRIES RETURNS ON THE SERVED PLANE, AND NOTHING ELSE MOVED.** In a
`gold/holding/date={d}/holding.parquet` from a scheduled fire after the apply, `ABT` carries **8 of 8**
non-null return windows. **Report the 0-of-8 population WITH ITS DENOMINATOR** — it should be the four
CASH rows plus `2602335D`, **five of 189, not six.**
⛔ **ISSUER CLARIFICATION 2026-08-29 ~18:3xZ (`2.0.0_SA_COO~Z`), MADE BEFORE THE SCORING ARTIFACT
EXISTS -- `189` IS AN INHERITED COUNT AND IS NOT A PASS CONDITION.** It is 2026-08-28's row total.
`0.4.0_DS_ClientPlatform~Y` measured **187** rows on today's silver, so **the denominator MOVES WITH
THE HOLDINGS** and a checker comparing to `189` false-alarms on an ordinary composition change.
Surfaced by `0.7.0_AE_CloudOps~N`, which found the same inherited count in its own EXPECT block and
declined to edit the issuer's criterion -- correctly, so it comes back here.
⭐ **THE CRITERION'S OWN WORDING ALREADY SETTLES IT: it says *report the 0-of-8 population WITH ITS
DENOMINATOR* -- PRINT the denominator, never MATCH it.** The operative test is the NAMED ROW SET --
exactly {four CASH rows, `2602335D`} -- whatever the day's total is. Print the observed total beside
the count; do not compare it to `189`.
⛔ **THIS IS A CLARIFICATION, NOT A RELAXATION, AND THE TIMING IS WHY IT IS LEGITIMATE.** The bar is
unchanged: the same five named rows either way, and a sixth null row still FAILS. It is written
BEFORE the 2026-09-01T13:00Z artifact exists, so it cannot have been fitted to a result.
**CONTRAST, DELIBERATELY: on `D1_CATVIEWS.TM1-AC1` this same issuer REFUSED to resolve an ambiguity
the same day** -- because there the numbers were already in hand and the resolution would have moved
that criterion from three members short to one. **Seeing the result first is what makes a
clarification into a score.** Here nothing has been seen.
⛔ **`2602335D` (TPG Inc, w=0.00, price 0.0) IS OUT OF SCOPE and must NOT be "fixed" here** — a
zero-weight CVR with no `PX_LAST`, so no history can accrue. Leave it null and say so.
⛔ **AND ICT AND MER MUST SURVIVE.** A change that repairs ABT and silently drops a Philippine holding
has traded one blank row for another.

## 4. BOUNDS THIS FACE CARRIES

- **`/sedol/2824100` is UNEXERCISED.** A vendor call needing Andrew's per-use word; **none is
  requested** — the scheduled pull exercises it free. Do not upgrade that language.
- **THE REPAIR DOES NOT CLOSE THE CLASS.** ~1 in 10 future doubly-stripped CUSIPs will be SEDOL-valid,
  be refused repair, and silently retain the ABT failure — invisible by exactly the mechanism that
  made ABT invisible. Safe direction; better everywhere, worse nowhere. **Do not close this face on
  the word "fixed".**
- **THE ORIGINAL PREMISE WAS WRONG AND THE CONCLUSION SURVIVED.** `TO-13-DS` said "stop the upstream
  coercion"; there is no coercion of ours — bronze already carries `2824100` and the parsers only
  `.strip()`. **The coercion is the TrueShares Google Sheet.** "Source" means our silver boundary.
- ⚠ **THE MODULE'S DEFAULTS LIE ABOUT WHERE ITS DATA IS**: defaults say `BRONZE_BUCKET=S3_BUCKET` /
  `GRAMMAR=legacy`; the DEPLOYED environment says `opal-data-assets` / `monolith`. **Reading the code
  instead of the applied state sends you to a prefix that returns nothing** — a clean zero from the
  wrong place.

<proof_of_spec>
  <!-- ISSUANCE half (2.0.0_SA_COO~Z). POSITIONAL:
         python .tools/proof-of-spec-check.py <instance>.json POS-TO14-AC1,POS-TO14-AC2,POS-TO14-AC3,POS-TO14-AC4
       CHECK THE VERDICT, NOT THE rc -- measured today on ETFS_INGEST.TO-10-AE: the checker
       returned rc=0 while printing INVALID. The verdict string is the oracle.
       Take it WITHOUT A PIPE ($? after a pipe is the PIPE's rc). Coverage diff is BIDIRECTIONAL.
       A PLACEHOLDER ROW PASSES THIS CHECKER: rc=0 VALID has been measured on a criterion that
       never ran. Score the ARTIFACT per AC, then file. UNCOMPUTABLE is an honest verdict and is
       the correct filing for an event-gated row -- TO-13-DS filed four of them deliberately. -->
  <criterion id="POS-TO14-AC1" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO14-AC2" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO14-AC3" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO14-AC4" cell_refs="ETFS-a-1, ETFS-d-1"/>
  <expected_criteria>POS-TO14-AC1,POS-TO14-AC2,POS-TO14-AC3,POS-TO14-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-14-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4, firm-tokened `POS-TO14-ACn`. Cells: 2, both pre-existing — an APPLIED rung, no new cell. **AC3 and AC4 are EVENT-GATED on a scheduled fire after the apply and cannot close on the first filing**; a 2-of-4 instance is the expected first state, not a failure.</alignment_denominators>
</proof_of_spec>
