<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-R4</id>
<title>Closure row 4 — THE EXERCISE. Sever one channel, confirm the other two still publish. The PRD says NOTHING ELSE PROVES IT. You have it because no contract author may verify their own independence claim.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. Row 4 is the acceptance of the entire independence premise.</workstream>
<issued_to>3.0.0_SA_CVO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:30Z</issued_at>
<status>complete -- verdict NOT-EXERCISABLE-YET delivered 2026-07-24T1752Z @b7291513cd (on origin/CLOUD), deliverable org/tier1_exec/3.0.0_SA_CVO/deliverables/MDPF_CHANNEL_INDEPENDENCE_CI-R4_CVO_VERDICT_20260724.md. Reached on independent grounding and a DIFFERENT basis than the one given (leg 2, the Actions billing-block-as-reason, refuted); 13th item filed as an amendment to CTO's gate. Status flipped 2026-07-28 at CVO startup -- the verdict landed 4 days ago and this cell still read `pending`, which is the stale-record-with-authority class, not a re-open.</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD `docs/architecture/MDPF_CHANNEL_INDEPENDENCE_PRD.md` @eaa8433547 §3a row 4. Placement proposed by COO, **APPROVED by CTO 171936Z.**</authorization>

<references>
  <ref type="prd">PRD §2.1 (channels are the unit), §2.2 (the three event contracts), §3a row 4</ref>
  <ref type="sovereign">Andrew ~1648Z: *"If we get locked out of Black Diamond for some reason and Cottonwood freezes, it is not fair nor appropriate for 49 Financial and Inflection to have their MDPF data freeze. We need to design so that each channel is its own unit and can proceed independently."*</ref>
</references>

<scope>
**ROW 4: "No cross-partner gate exists ANYWHERE between vendor and served artifact."**
**Verified by — and the PRD is emphatic — THE EXERCISE: sever one channel, confirm the other two still
publish. NOTHING ELSE PROVES IT.**

>> **WHY YOU, AND NOT A CONTRACT BUILDER.** Row 4 is the acceptance of the whole premise. `0.6.2~C` builds
   C1/C2; `0.7.0` builds C3. **If a contract author severs a channel and confirms their own contracts held,
   the highest-stakes assertion in the document is verified by the person who wrote it.**
   Today produced three separate instances of a builder's own instrument failing to see the thing it was
   built to see — a recovery predicate that silently skipped the case it was hunting, a census matcher blind
   to ~90% of its own defect, and a check that printed a verdict its two states could not distinguish.
   **Every one was caught by someone other than the author, or by the author only after the arithmetic
   refused to close.** You are the someone else.

**THE EXERCISE HAS ONE SHAPE AND ONE TRAP:**

⚠⚠ **SEVER A CHANNEL THAT IS CURRENTLY HEALTHY.** This is the criterion's own easiest-pass and it would
produce a clean, confident, worthless PASS:
- **COTTONWOOD is NOT a valid subject.** Its count feed is permanently absent (Andrew ~1456Z: cannot get
  backfill counts), its vendor is D+2 by design, and `allocations`+`unrealized` have had no new data since
  07-17. **Severing a channel that was not publishing proves nothing about whether severing one WOULD stop
  the others.**
- Sever **49F** or **INFLECTION** — a channel that is *currently producing* — and confirm the other two
  still publish. **The severed channel must have been demonstrably alive at the moment you severed it**;
  state how you established that.

**AND THE INVERSE CONTROL, WHICH IS WHAT MAKES IT AN EXERCISE RATHER THAN AN OBSERVATION:** show that the
severed channel's own output DID stop. If nothing changes anywhere, you have not severed anything and the
"other two still publish" reading is vacuous. **Both limbs, or the result is undetermined.**
</scope>

<explicitly_out_of_scope>
- **Building or fixing any contract.** You verify; you do not repair. If the exercise fails, that is a
  finding for CTO's gate, not work for you.
- Rows 1/2 (`0.6.2~C`), 3/10 (`0.7.0`), 9 (`0.7.0~A`), 7/8 (`0.7.0~B`), 5/6/11/12 (`0.4.0_DS~A`).
- **Do not sever anything in a way that requires a deploy.** See the constraint below.
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **THE PRIMARY TRAP:** sever cottonwood, observe 49F and INF publishing, report PASS. **A channel that was
  already not publishing cannot demonstrate independence.**
- *Easiest pass 2:* sever a channel and observe the others' ARTIFACTS still EXIST. **Existence is not
  publication** — an artifact that was already there when you started proves nothing. Establish that the
  others **published AFTER** the severance, with a timestamp that discriminates.
- *Easiest pass 3:* run the exercise while the chain is not dispatching anyway. **The MDPF chain is
  event-driven with no schedule of its own and did not rebuild today.** If nothing was going to publish
  regardless, the exercise is unexercised — **and that is a legitimate verdict, not a failure to try.**
- *Easiest pass 4:* accept a builder's report that their contract held. **The whole reason this row is yours
  is that a builder's confirmation of their own contract is not independent evidence.**
**MISSING THIRD STATE:** the verdict is `INDEPENDENT | CROSS-GATE-FOUND | NOT-EXERCISABLE-YET`. The third is
real and expected today — the contracts are being BUILT and cannot be LANDED (below). **An unexercisable row
reported as PASS is the failure this whole PRD exists to prevent.**
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠ **GitHub Actions is BILLING-BLOCKED ORG-WIDE.** `lambda-deploy.yml` / `ec2-deploy.yml` refused at dispatch;
Rule 1 makes Terraform the only Lambda mechanism. **C1/C2/C3 CAN BE BUILT AND VERIFIED BUT NOT LANDED.**
**So row 4 is very likely NOT-EXERCISABLE-YET until billing clears and the contracts land.** That is expected
and it is the honest verdict. **Do not construct a proxy exercise against the current architecture and let it
read as row 4** — the current architecture is the one with the cross-partner gate; exercising it would
measure the defect, not the fix.
If you can define the exercise now so it is ready to run the moment the contracts land, that is the most
useful thing available today.
</constraint_deploy_blocked>

<acceptance_criteria>
1. **A verdict from `INDEPENDENT | CROSS-GATE-FOUND | NOT-EXERCISABLE-YET`**, with the state that produced it.
2. If exercised: **the severed channel named, with evidence it was HEALTHY at severance**; the other two
   shown to have **published AFTER** severance (not merely to exist); and **the severed channel's own output
   shown to have STOPPED**.
3. If not yet exercisable: **the exercise DEFINED and ready to run** — which channel, how severed, how
   reversed, what discriminates a pass from a vacuous one.
4. Denominators and explicit-Z throughout. Pin any coverage claim to a BUILD, not a cardinality — **your own
   finding: two builds both reporting 429 covered different date sets.**
</acceptance_criteria>

<deliverables>
  - Verdict + evidence at `org/tier1_exec/3.0.0_SA_CVO/`, **pinning the commit-ish you verified** (RAVC 3a).
  - To CTO (he gates closure) + COO. **Commit; do NOT push — COO is push operator (Andrew ~1600Z).**
</deliverables>

<notes>
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE** — not absorbed silently, not parked
into a successor project.
Your constitutional independence applies: this verdict is not COO's or CTO's to overturn, and a REWORK from
you is a better outcome than a fast GREEN.
</notes>
</task_order>
