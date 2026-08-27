# TO ADVI_INSURE.TO-A1-AE — surface (a): the bd49f REST vehicle gains an INSURANCE leg, and the field→call map nobody has printed

<task_order id="ADVI_INSURE.TO-A1-AE" project="ADVI_INSURE">
<decomp_ref>workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md — cells INS-a-1, INS-a-2, INS-a-3</decomp_ref>
<decomp_context>These are the THREE cells `ADVI_INSURE.TO-R1-DS` explicitly EXCLUDED to this lane ("the bd49f REST vehicle gaining an insurance leg is `0.6.0_AE_PartnerETL` ground"). NOT in this TO: every INS-b/c/d/f cell (the DS lane's landing/gold/platinum planes, already at its ceiling waiting on you) and INS-e-1..5 (the DE frontend plane).</decomp_context>

<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` cert `@7397dfd83e`, re-certified after scope re-open by the alternate signer (self-certification break). If a surprise item returns DECOMP-INVALIDATING, the ISSUER re-derives — the executing seat does not adjudicate that.</certification>
<issued_to>`0.6.0_AE_PartnerETL` — brought online by Andrew 2026-08-25 ~22:0xZ. ONE PROJECT PER INSTANCE: this lane holds ADVI_INSURE surface (a) and nothing else this session.</issued_to>
<executor_class>AE-class (partner ETL vehicle).</executor_class>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-25T22:0xZ</issued>
<status>ACTIVE — AC2 startable immediately. ⛔ AC1/AC3 HELD on a sovereign vendor-egress call (see THE HOLD).</status>
<priority>P1 — this lane is the ONLY thing standing between `ADVI_INSURE.TO-R1-DS` and its remaining four acceptance criteria. That TO is COMPLETE to its ceiling and waiting on you.</priority>
<placement>LAPTOP (Rule 26).</placement>
<scope_guard>ONE PROJECT. Exactly the three cells above. Adjacent findings → ONE LINE to `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO`; no action, keep working.</scope_guard>
⛔ <distribution>**NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY** (ADVI_INSURE PRD s.3, Andrew ~16:1xZ). This binds you and binds every message you send about this work.</distribution>

<proof_of_spec>
  <!-- Positional, check the rc:
         python .tools/proof-of-spec-check.py <instance>.json INSA1AE-AC1,INSA1AE-AC2,INSA1AE-AC3
       CHECK THE RC (0 VALID / 1 INVALID / 2 usage). The 2-arg form returns rc=0 with COVERAGE
       UNCHECKED -- PASS THE IDS. Measured 2026-08-25: a bare run and a coverage gap are
       BYTE-IDENTICAL to anyone who runs it the easy way. -->
    <criterion id="INSA1AE-AC1" cell_refs="INS-a-1"/>
    <criterion id="INSA1AE-AC2" cell_refs="INS-a-2"/>
    <criterion id="INSA1AE-AC3" cell_refs="INS-a-3"/>
  <expected_criteria>INSA1AE-AC1,INSA1AE-AC2,INSA1AE-AC3</expected_criteria>
  <instance_path>org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/ADVI_INSURE.TO-A1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 3; cells: 3; every criterion carries exactly 1 cell_ref; unmapped cells 0; untraceable criteria 0. ⛔ EACH CRITERION IS SINGLE-CELL AND SINGLE-LAYER BY CONSTRUCTION — deliberate. A criterion bundling two grounding layers cannot take one status honestly, and scoring at the weakest layer hides a satisfied check (`INSR1DS-AC1`, ruled 2026-08-25 ~21:0xZ; candidate census at `org/tier1_exec/2.0.0_SA_COO/deliverables/TWO_LAYER_CRITERION_CANDIDATE_CENSUS_20260825T2135Z.md`).</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ THE HOLD — a sovereign call I am NOT making for you, and NOT assuming

**AC1 and AC3 require calling Black Diamond's insurance endpoints on the 49 Financial principal.**

- **Black Diamond is a NON-OPAL SERVICE.** CLAUDE.md: *"NEVER call an external vendor API without
  Andrew's explicit per-use word — availability in the toolset is NOT authorization."*
- ⛔ **AND THIS IS NOT COVERED BY THE EXISTING bd49f PIPELINE'S STANDING OPERATION.** The decomp
  measured it: **the 49F principal is UNEXERCISED against the insurance surface — every live 200 on
  that surface to date is Cottonwood's.** A new endpoint family on a principal that has never touched
  it is a new egress, not a continuation of a running one.

**I have raised this to Andrew. DO NOT CALL THE VENDOR UNTIL HIS WORD LANDS.** I will relay it
verbatim. If he declines or defers, AC1/AC3 become `UNCOMPUTABLE-BY-DEPENDENCY` with the dependency
named — that is a complete answer, not a failure.

**START ON AC2 NOW — it needs no vendor call** (see below). That is deliberate: this TO is sequenced
so the hold blocks a third of it, not all of it.

## Cells

- **`INS-a-1` — THE VEHICLE LEG.** The bd49f REST vehicle gains an insurance leg. Reuse
  `DATA_BDINSURANCE` s.4.1a (the resolved BD insurance application surface, HAR-2). **BOTH token
  authorities carried** — `/session/token` is a *separate authority* from the main BD bearer (I2).
  *Oracle: the vehicle leg exists, cited at a named ref.*

- **`INS-a-2` — THE FIELD→CALL MAP. ⛔ THIS IS THE ONE THE WHOLE PROJECT IS WAITING ON, AND IT NEEDS
  NO VENDOR CALL.** The bulk export path is `run → resultGuid → download` for the cohort;
  `accountdetailsearch` supplies per-account identity + characteristics + `currentEmv` + `asOfDate`.
  **NAME WHICH CALL SUPPLIES WHICH FIELD — DO NOT ASSUME ONE CALL COVERS BOTH.**
  *Oracle: the field→call map, PRINTED.*
  > **Why this is the unblocking act:** `0.4.0_DS_ClientPlatform~J` declined to build the gold
  > builder and gave this as the binding reason — *"`INS-a-2`'s own oracle, the field-to-call map
  > printed, is UNPRODUCED and in another lane. Nobody has answered which call supplies `currentEmv`
  > vs `insuranceCharacteristics`."* They also measured that the documented contract at
  > `docs/architecture/DATA_BDINSURANCE_PRD.md:139-141` **ends in a literal ellipsis** — a partial
  > enumeration presented as whole. **Do not inherit that ellipsis. Enumerate.**
  > The map can be derived from the HAR-2 record and the existing Cottonwood-side calls **without
  > touching the 49F principal.** Do that.

- **`INS-a-3` — ⛔ A REFUSAL NAMES THE SURFACE, NEVER THE ABSENCE.** A clean zero from one endpoint
  says NOTHING about the one beside it. Any empty or entitlement-refused result is reported
  **per-surface with its denominator**, never generalised to *"insurance data is unavailable."*
  *Oracle: per-surface result + denominator.*
  > This is the Bloomberg-class trap written into a BD cell on purpose. A vendor refusal is evidence
  > about **one surface's entitlement**, and it is routinely read as evidence about the data's
  > existence. Those are different claims and only one of them is measured.

## Acceptance criteria

| id | criterion | cell | layer |
|---|---|---|---|
| **INSA1AE-AC1** | The insurance leg EXISTS in the bd49f vehicle, cited at a NAMED REF (file:line @ commit-ish), with **both token authorities** carried and the `/session/token` authority shown to be distinct | `INS-a-1` | **APPLIED** |
| **INSA1AE-AC2** | The **field→call map is PRINTED** — every v1 field (`carrier`/`product`, `currentEmv`, `asOfDate`, the `insuranceCharacteristics` family) mapped to the exact call that supplies it, with the ones NOT supplied by any known call named as gaps. **Denominator printed. No ellipsis.** | `INS-a-2` | **SOURCE** |
| **INSA1AE-AC3** | Every empty / entitlement-refused result reported **per-surface with its denominator**; no generalisation across surfaces. If a surface refuses, that is a RESULT, not a failure | `INS-a-3` | **EXERCISED** |

## Standing constraints

- **Rule 17a — BRONZE IS RAW AND UNTOUCHED.** Whatever BD returns lands byte-for-byte. **A
  `.parquet` under `bronze/` is an architectural violation, not a format preference.** The DS lane
  already refused to satisfy a criterion that would have required breaking this; do not undo it.
- **The landing tree is `blackdiamond/49financial/`** — a **deliberate in-grammar MINT** (Rule 17b
  `{vendor}/{firm}/{medallion}`). `blackdiamond/49f/` is the **legacy alias** and **nothing under it
  moves**. `ADVI_STITCH` mints `*_legacy/` leaves in the same parent — **coordinate, do not collide**
  (`0.4.0_DS_ClientPlatform~Q` holds that lane).
- **Every apply through `.tools/safe-apply.sh`.** NEVER#6: a begun deploy FINISHES in-session or
  rolls back loud, with a ledger under `org/critical_paths/change_management/`.
- ⛔ **`safe-commit.sh` can refuse SILENTLY and leave your files STAGED** (three instances measured
  2026-08-25; one swept a law-file edit under a foreign author line). **`[msg-verify] committed
  <hash>` appears ON SUCCESS ONLY — present means it committed, absent means it did not.**
  Capture-then-read, never pipe-then-read: `> /tmp/sc.out 2>&1; echo "RC=$?"`. **`$?` after a pipe is
  the last stage's rc, not the script's.** Do not stage or commit `CLAUDE.md`.

## Surprise-channel posture — Andrew-direct 2026-08-25 ~20:24Z, VERBATIM

> *"agents are expected to adhere to surprise-channel logic, they proceed with the task unless the
> task is untenable. if you do atom_decomp properly as you are supposed to that shouldnt be an issue."*

**THE DEFAULT IS PROCEED.** The bar is **UNTENABLE** — the task cannot be executed as specified.
Not surprising, not questionable, not "a premise looks softer than stated."

```
OBSERVATION -> ONE LINE to 3.0.0_SA_CVO, cc me. KEEP WORKING. It NEVER interrupts.
BLOCKING    -> only if UNTENABLE. Same-turn to me (the issuer) for spec amendment.
ARMED       -> disarm SAME-TURN via a NAMED disarm owner. DISARMED != REMEDIATED.
```

⚠ **The vendor hold above is a SPEC CONSTRAINT, not a blocker — do not report BLOCKED on it.**
⛔ **DO NOT RE-DERIVE A PEER'S METHODOLOGY.** Re-derive a peer's claim about an **artifact** when it
is load-bearing. Not how they got there.

**CVO owns proof-of-spec and is a VERIFIER, NOT AN APPROVER** — never idle waiting on a cert you were
not held by. **Nothing routes through CTO**; if you think you need CTO, it comes to me and I decide.

---
## ⚖ D2 LOCK-IN RIDER — COO, 2026-08-27 (CVO 76086, additive; no clause above is altered)
The proof-of-spec instance is validated **BY RC** (never an output string), and the validator
invocation + its TRUE rc are recorded as evidence **IN the instance**. The GO for this TO pairs
only AFTER `3.0.0_SA_CVO` cert step-zero (cert-before-GO — this holds the GO, it does not hold a
seated agent mid-work; the never-idle clause above is untouched). The re-seat is the S5 word
@1d761ded1f (seat not in the live roster per CTO 76081).
