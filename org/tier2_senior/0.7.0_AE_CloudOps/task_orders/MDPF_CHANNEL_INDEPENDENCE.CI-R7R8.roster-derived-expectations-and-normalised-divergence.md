<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-R7R8</id>
<title>Closure rows 7 + 8 — the ROSTER as the one source of expected-ness (partners AND cadences, no literals), and NORMALISED divergence. Acceptance for row 7 is the PARTNER-#4 TEST.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. Rows 1–12 true = MDPF CLOSES.</workstream>
<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:34Z</issued_at>
<status>complete</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD @eaa8433547 §2.6 / §2.5, §3a rows 7 + 8. Fresh lane. Row 8 placed here by COO, **approved by CTO 171936Z** — expected cadence comes from the roster, and splitting them would put one lane's acceptance inside another's deliverable.</authorization>

<references>
  <ref type="prd">PRD §2.6 (the roster is the one source of expected-ness), §2.5 (divergence — normalised, never raw), §3a rows 7 + 8</ref>
  <ref type="sovereign">Andrew ~1500Z: *"there will always be scenarios of varying N of partner firms with holdings counts as new partners are onboarded. From here on out there should be 3 (until a new partner comes in making it 4 and so on), but we can't get 3 in the past because we didnt have COttonwood at that time. So rules/error flags need to take that into account."*</ref>
  <ref type="sovereign">Andrew ~1648Z: *"Our job as the developers are to watch for expanding divergence between partner channels, more than 1 Day. That is the signal someone is falling behind, but we do not hold the rest."*</ref>
</references>

<scope>
**ROW 7 — expected partners AND CADENCES are ROSTER-DERIVED. No literals.**
*Verified by:* **THE PARTNER-#4 TEST — onboarding a partner is a ROSTER ROW AND NOTHING ELSE.** No code edit,
no constant bump, no threshold re-derivation. **If onboarding requires touching composition logic, the design
has failed and CTO refuses it at gate.**

>> **THE ROSTER MUST BE PER-QUANTITY AND PER-EFFECTIVE-DATE, AND TODAY PROVED WHY BOTH HALVES MATTER.**
   Three eras exist for Cottonwood alone:
   ```
   pre-2026-05-28   expected COUNT {49F, INF}              not a partner yet
   05-28 .. 07-21   expected COUNT {49F, INF}              VALUE-only era — value(3) vs count(2) is CORRECT
   2026-07-22 on    expected COUNT {49F, INF, COTTONWOOD}  a missing cottonwood count MUST now flag
   ```
   **CTO wrote `COUNT effective-from: NEVER` for Cottonwood and Andrew corrected it within minutes.** Had
   NEVER shipped, Cottonwood would have been **permanently excused from the count expectation** — so on the
   day its feed broke, **nothing would flag it, and the rule would look correct forever because the alarm
   simply never fires.** *A guard nothing invokes is not a guard.* **The un-backfillable window is a BOUNDED
   HISTORICAL FACT recorded in the roster, NOT a permanent exemption — those two must not be representable
   the same way.**

**ROW 8 — divergence is NORMALISED per §2.5; a healthy estate reads 0/0/0.**
*Verified by:* run it against **today's live state**; **any non-zero must name a real lag.**
Andrew's signal is *"expanding divergence... more than 1 Day"* — **and we do not hold the rest.** Divergence
is a WATCH, never a GATE. It must not become a cross-partner blocker; that would reintroduce row 4's defect
through the monitoring layer.
**NORMALISED, NEVER RAW:** Cottonwood is D+2 by vendor design. A raw day-count would flag it permanently and
correctly-by-arithmetic — and a permanently-red signal is one nobody reads.

**INTERFACE — `0.4.0_DS_ClientPlatform~A` OWNS THE GOLD-SCRIPT CONSUMPTION, NOT YOU.**
```
YOU     -> the roster ARTIFACT + its SCHEMA + the divergence computation off it
DS~A    -> the gold script reading expected-vs-present FROM the roster, replacing literals
```
**Reason, and it would have cost you the whole build:** `dim_mdpf_aggregate_aua_timeseries.py` lives under
`data/mdpf/scripts/gold/`, **Rule 13 makes that DS's lane, and it is enforced at the PRE-PUSH hook.** You
would have built it correctly and been blocked at the very end under a P0 clock.
**AGREE THE SCHEMA WITH DS~A IN WRITING BEFORE EITHER SIDE BUILDS AGAINST IT.**
</scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **Row 7's PRIMARY TRAP:** encode the three known partners and their known effective dates, and call it
  roster-derived. **The partner-#4 test is not "can I add a row" — it is "does adding ONLY a row suffice."**
  Actually run it: add a synthetic fourth partner and show composition, expectations and divergence all
  follow with **zero code changes**.
- *Easiest pass 2:* one effective-date per partner. **The roster must be PER-QUANTITY** — Cottonwood is
  expected for VALUE from 05-28 and for COUNT from ~07-22. A single date cannot express that and would
  recreate the NEVER defect in a different shape.
- **Row 8's trap:** normalise so aggressively that a real lag reads 0. **Construct a genuine lag and show the
  metric moves.** A metric that only ever reads 0/0/0 is indistinguishable from one that cannot fail.
- *Easiest pass 4:* let divergence block a publish. **It is a WATCH, not a GATE** — a divergence check that
  holds the other partners is row 4's defect wearing a monitoring costume.
**MISSING THIRD STATE:** a partner on a date is not `expected | not-expected`. It is
`expected | not-yet-onboarded | ONBOARDED-BUT-NOT-FOR-THIS-QUANTITY`. The third is exactly what the
NEVER correction was about.
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠ **GitHub Actions is BILLING-BLOCKED ORG-WIDE** — `lambda-deploy.yml` refused at dispatch; Rule 1 makes
Terraform the only Lambda mechanism. **BUILD AND VERIFY. DO NOT LAND.** **Do not improvise around CI.** Only
Andrew clears it.
</constraint_deploy_blocked>

<compiler_tools_mandate>
  <before_write>`comp-which` for routing; `comp-iam service <lambda>` for any new boto3 call — NECESSARY NOT SUFFICIENT, see Rule 22a for a new bucket/table/ARN.</before_write>
  <before_commit>`.tools/commit-gate.sh` (Rule 14).</before_commit>
  <after_commit>Session log with `## Compiler Tools`; `org/compiler-tools-log.md` in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **THE PARTNER-#4 TEST RUN, not asserted:** a synthetic fourth partner added as a roster row ONLY, and
   composition + expectations + divergence shown to follow with **zero code changes.**
2. **Roster is PER-QUANTITY and PER-EFFECTIVE-DATE**, with all three Cottonwood eras representable and the
   un-backfillable window recorded as a bounded fact rather than an exemption.
3. **Divergence normalised; today's live estate reads 0/0/0**, or any non-zero **names a real lag.**
4. **A constructed lag shown to MOVE the metric** — it must be able to fail.
5. **Schema agreed IN WRITING with `0.4.0_DS_ClientPlatform~A`** before either side builds against it.
6. Explicit-Z; denominators; **pin any coverage claim to a BUILD, not a cardinality** (CVO: two builds both
   reported 429 and covered different date sets).
</acceptance_criteria>

<deliverables>
  - The roster artifact + schema + divergence computation, and the partner-#4 test evidence.
  - To CTO (gate — he refuses row 7 if onboarding needs a code edit) + COO. **Commit; do NOT push — COO is
    push operator (Andrew ~1600Z).**
</deliverables>

<notes>
Register as `0.7.0_AE_CloudOps~B` — FULL suffixed serial. Base `0.7.0` and `~A` are LIVE on adjacent rows.
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE.**
</notes>
</task_order>
