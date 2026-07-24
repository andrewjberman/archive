<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-R5R6R11R12</id>
<title>Closure rows 5, 6, 11, 12 — the firm-axis poison, carry-forward with labelled basis+as-of, the frontier-stamp staleness check, and the exempt_absorbed label collision. ALL FOUR ARE YOUR OWN MEASUREMENTS.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. When rows 1–12 are true, MDPF CLOSES.</workstream>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:20Z</issued_at>
<status>staged</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD `docs/architecture/MDPF_CHANNEL_INDEPENDENCE_PRD.md` @eaa8433547. Fleet narrowed by Andrew; you are one of two Tier-2 lanes KEPT, on CTO's argument that your operational judgement on these rows does not transfer in writing.</authorization>

<addendum id="roster-consumption-interface" added="2026-07-24T17:25Z" authority="CTO 172159Z, relayed by MSTR 172410Z — added BEFORE this TO's GO">
>> **YOU ALSO OWN THE GOLD-SCRIPT CONSUMPTION OF THE ROSTER. This is an INTERFACE with the roster lane, not
   a new row and not a fourth spawn.**

```
ROSTER LANE (CloudOps)  ->  the roster ARTIFACT + its SCHEMA + the divergence computation off it (rows 7, 8)
YOU (DS lane)           ->  the GOLD-SCRIPT CONSUMPTION: reading expected-vs-present FROM THE ROSTER
                            instead of literals — which is rows 5/6 territory anyway
```

**WHY THE SPLIT EXISTS, AND IT IS NOT BUREAUCRACY:** `dim_mdpf_aggregate_aua_timeseries.py` lives under
`data/mdpf/scripts/gold/`. **CLAUDE.md Rule 13 gives DS the full commit→QA-deploy cycle for
`data/*/scripts/{gold,silver,bronze}/*.py`, and it is enforced atomically by safe-deploy's PRE-PUSH hook.**
So a CloudOps lane told to "make composition roster-derived" would build the whole thing correctly, **hit the
hook at PUSH, and be blocked at the very end — under a P0 clock.** That is exactly the moment someone reaches
for `--force` or an audited bypass, and it would be a self-inflicted wound caused by the TO's shape rather
than by anyone's judgement.

**PRACTICALLY:** the roster lane hands you a schema and an artifact; **you make the gold script read
expected-vs-present from it and remove the literals.** Agree the schema with them *before* either side
builds against it — a schema agreed after the fact is two lanes discovering they measured different objects,
which happened twice today.
**NO HARDCODED FIRM NAMES, NO HARDCODED N, NO HARDCODED DATES** in the consumption path. The acceptance is
the partner-#4 test: onboarding a partner is a roster row and nothing else.
</addendum>

<references>
  <ref type="prd">MDPF_CHANNEL_INDEPENDENCE_PRD.md §2.4 (carry-forward), §3a rows 5/6/11/12</ref>
  <ref type="input">**YOUR OWN WORK — POINT AT IT, DO NOT RE-DERIVE IT:** GC-W1 @b078877020 (the `:1656` firm-axis poison; the 40-null attribution), GC-W2a @694175f91 (the frontier-stamp hole generator; the exempt_absorbed 20-enumerated/18-fallback split), GC-W2b @4d0831382 (the served-count definition, EXACT on four quantities; the as-of skew)</ref>
</references>

<scope>
**THESE FOUR ROWS ARE LITERALLY YOUR MEASUREMENTS.** You found the firm-axis poison, the frontier-stamp
generator, the label collision and the as-of skew. **Do not re-derive any of them** — cite your own commits.
The work here is turning four measured defects into four true statements.

**ROW 5 — the `:1656` firm-axis poison is GONE.** One firm's absence must not null the Global cell.
*Verified by:* a MUTANT — remove one firm's cell, Global still composes **and is labelled**.
Your W-1 established this fires on all 40 nulls and that the PRD's original model-cell rule never fired at all.

**ROW 6 — Global carries forward PER FEATURE, and every carried value is LABELLED with basis + as-of.**
*Verified by:* artifact inspection **plus the render showing held ≠ measured**.
⚠ **W-7 IS FOLDED IN HERE AND GRADED CORRECTNESS, NOT HYGIENE** — 18 non-trading rows on a declared
trading-day axis, and the 447-vs-429 confusion that **already put two wrong numbers in a live Andrew-facing
brief**. Fix it inside this row.

**ROW 11 — the frontier stamp cannot silently overwrite the newest point with a stale roster** (CVO's P2).
*Verified by:* a publish-time check — staged `account_dist` `as_of` vs coverage end.
Your GC-W2b measured the mechanism: `_latest_date()` resolves roster and valuation partitions
**independently**, so the stamped value's as-of is *"whenever account_distribution last ran"*, not the axis
date it lands on. **You tested and REJECTED the T-1-by-design reading** (DEFN(07-22)=7,038 vs served 7,026 =
DEFN(07-21)). Two clocks, unbounded skew, no convention.

**ROW 12 — the `exempt_absorbed` label collision is resolved AT THE PRODUCER, *or* the label is not rendered
as a reason.** You measured 20 ENUMERATED (`:1723`) + 18 FALLBACK (`:1729-1731`) under one byte-identical
label with **no read-time discriminator**, found by two independent searches with their spaces named.
>> **BOTH BRANCHES ARE LEGITIMATE — the PRD says "split it or do not render it."** CTO has already ruled the
   render side (DE renders the declaration and must not present `exempt_absorbed` as a *reason*). **So the
   not-render branch is ALREADY SATISFIED and this row may already be true.** Your job is to say which, with
   evidence — not to prefer the harder branch because it looks more thorough.
</scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **Row 5.** *Easiest pass:* mutate a firm that is ALREADY absent on the test date. Global would still
  compose and prove nothing. **Mutate a firm that is PRESENT and healthy on that date.**
- **Row 6.** *Easiest pass:* label carried values and stop. **The row requires the RENDER to show held ≠
  measured** — coordinate with whoever owns the FE side rather than declaring the producer half sufficient.
- **Row 11.** *Easiest pass:* add the as-of comparison and never exercise it. **A guard nothing invokes is
  not a guard** — construct the stale-stamp case and show the check fires.
- **Row 12.** *Easiest pass:* declare it satisfied by CTO's render ruling without checking that the ruling
  actually reached the code. **Verify the render does not present it as a reason**, then say the row is true.
- **ACROSS ALL FOUR:** *Easiest pass:* cite your own prior commits as evidence that a row is now TRUE. Your
  commits establish the DEFECTS. **They cannot establish the FIXES.** Do not let a citation of your own
  measurement stand in for an exercise of the repair.
**MISSING THIRD STATE:** each row is `true | not-yet-true | TRUE-BUT-UNEXERCISED`. The third is the one that
must never be reported as the first.
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠ **GitHub Actions is BILLING-BLOCKED ORG-WIDE.** `lambda-deploy.yml` and `ec2-deploy.yml` are REFUSED AT
DISPATCH, and CLAUDE.md Rule 1 makes Terraform the only Lambda mechanism.
**BUILD AND VERIFY. DO NOT LAND.** If a row needs a deploy to become true, take it to the gate and STOP.
**Do NOT improvise a path around CI** — not a manual deploy, not a direct push, not a re-run loop. Only
Andrew can clear it. If billing clears mid-flight, landing resumes; do not re-plan for it.
</constraint_deploy_blocked>

<compiler_tools_mandate>
  <before_write>`comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py` — column gaps + portal consumers.</before_write>
  <before_commit>`.tools/commit-gate.sh` per Rule 14; `comp-validate` before signalling; `comp-surface-check` BY HAND on any SEV1 surface — and note it BLOCKS on the portal side (CLAUDE.md Rule 20, corrected today).</before_commit>
  <after_commit>Session log with `## Compiler Tools` populated; `org/compiler-tools-log.md` line in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **Per row: a verdict from `true | not-yet-true | TRUE-BUT-UNEXERCISED`**, each with the exercise that
   produced it — not the measurement that found the defect.
2. **Row 5:** mutant on a PRESENT firm, Global composes and is labelled.
3. **Row 6:** carried values labelled with basis + as-of, W-7's axis defect fixed, denominators stated.
4. **Row 11:** the stale-stamp case constructed and the check shown FIRING.
5. **Row 12:** which branch, with evidence the branch actually holds in code.
6. Explicit-Z; denominators printed; NEVER#4 (no ad-hoc gold run).
</acceptance_criteria>

<deliverables>
  - Report at `org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/`, written for CVO.
  - To CTO (he gates closure) + COO. **Commit; do NOT push — COO is push operator (Andrew ~1600Z).**
</deliverables>

<notes>
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE.** It is not absorbed silently and not
parked into a successor project. If one of these four rows turns out to require something outside the twelve,
that is an amendment, not a quiet expansion.
</notes>
</task_order>
