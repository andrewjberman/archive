# TO ETFS_INGEST.TO-9-AE — the APPLY leg: deploy the `etf-positioning-producer` package carrying `TO-6` **and** `TO-8`

<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — **NO NEW CELL.** This TO is the **APPLIED rung** of cells already claimed by `TO-6` (`INGEST-T3-6`, `INGEST-T5-1` data half) and `TO-8` (`INGEST-T4-1`). `DESIRED ≠ APPLIED ≠ EXERCISED` is one axis over one cell, not three cells.</decomp_ref>
<certification>Rides `TO-6`'s and `TO-8`'s existing certification (`3.0.0_SA_CVO~Z` @422bdb431b, bound to @fcdf042972). No cell is added, so no re-certification is sought.</certification>
<issued_to>`0.7.0_AE_CloudOps~P` — **letter amended from `~I` to `~P` 2026-08-28 ~01:3xZ**, accepting `0.0.0_AB_MSTR~Z`'s pre-cleared lane (11576: 1d 0 active TOs, 1pt no live process). The letter is cosmetic and a measured-clean pre-clearance beats a fresh name. ⛔ **BUT THE PROJECT IS `ETFS_INGEST`, NOT `ETFS_POSITIONING`, AND THE DISTINCTION IS LOAD-BEARING FOR RULE 27:** this TO discharges the APPLIED rung of `INGEST-T3-6` / `INGEST-T4-1` / `INGEST-T5-1`, and **a TO belongs to the project whose CELLS it discharges, never to the directory its `.tf` happens to live in.** `infra/aws/terraform/etfs-positioning/` is an implementation location. Reading it as `ETFS_POSITIONING` would collide this seat with `ETFS_POSITIONING.TO-2` (AE-class, ACTIVE) and fence it from the very cells it is being seated to apply.</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>⛔ **GATED: BOTH `ETFS_INGEST.TO-6` AND `ETFS_INGEST.TO-8` MUST HAVE LANDED FIRST.** Not one. See §2 — a deploy after `TO-6` alone ships the defect `TO-8` exists to prevent, in APPLIED form.</seating_trigger>
<placement>SITE Z (Rule 26) — the apply runs on the device that owns the work; D4 is SITEZ-placed until done.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:3xZ</issued>
<status>ACTIVE — gated on TO-6 + TO-8. Raised by `0.4.0_DS_ClientPlatform~Q` as a BLOCKING/ARMED surprise (msg 11527); **DISARMED same-turn by naming this owner. DISARMED ≠ REMEDIATED — the apply still has to happen.**</status>
<priority>P1 — ⚠ **CLOCK, MEASURED by `0.0.0_AB_MSTR~Z` 11576 rather than felt: the ~13:00Z fire is ~687 minutes (11.4h) out at cut time. That is a COMFORTABLE window, not a crunch, and it is stated so no seat skips a control against an urgency that is not real.** The ~13:00Z gold fire runs the DEPLOYED bytes. Without this apply, `TO-6`/`TO-8` are DESIRED and today's platinum does not carry the field. **A missed window costs a day, not the work** — it is never a reason to skip a control.</priority>
<authority>CLAUDE.md Rule 13 (infra / PROD triggers are the AE/DT lane — DS explicitly cannot own this) · NEVER#9 (`safe-apply`, never bare `terraform apply`; `aws lambda update-function-code` is BANNED — Terraform is the only Lambda deploy mechanism) · NEVER#2 (a confirmed deploy is never left half-landed; ledger opened at start, closed at completion).</authority>

---

## 1. WHY THIS TO EXISTS

`0.4.0_DS_ClientPlatform~Q` edits `data/etfs/scripts/gold/etf_positioning_gold.py`. **That file is a
MEMBER of a Lambda package**, confirmed at source:

```
infra/aws/lambda/etfs-pipeline/etf-positioning-producer/build_package.py
  :67-68   ("etf_positioning_gold.py",      "data/etfs/scripts/gold/etf_positioning_gold.py")
  :69-70   ("etf_positioning_publisher.py", "data/etfs/scripts/gold/etf_positioning_publisher.py")
infra/aws/terraform/etfs-positioning/producer-lambda.tf
  :215     handler = "etf_positioning_gold.lambda_handler"
```

⛔ **THE ~13:00Z FIRE RUNS THE DEPLOYED BYTES, NOT THE REPO EDIT.** A committed `TO-6` is **DESIRED**.
The DS lane cannot close that gap — Rule 13 — so the apply needed an owner and did not have one.

## 2. ⛔ THE SEQUENCING IS THE POINT OF THIS TO — ONE DEPLOY, AFTER BOTH

**Both files ship in ONE package.** Therefore:

```
deploy after TO-6 ALONE   gold row carries `industry_group` -> publisher HOLDING_KEYS DROPS it
                          -> platinum still lacks the field, but now the loss is APPLIED and green
deploy after TO-6 + TO-8  gold carries it, publisher passes it, platinum serves it
```

⛔ **A deploy after `TO-6` alone ships the exact green-build-invisible-loss failure `TO-8` was cut to
prevent — except APPLIED, and therefore harder to see.** ⚠ **If both cannot land before ~13:00Z, THE
DEPLOY WAITS.** A missed window costs one day; a half-deployed package costs a wrong served artifact
and a debugging session that starts in the wrong place.

## 3. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `TO9-AC1` | **BOTH PRECONDITIONS MEASURED BEFORE THE APPLY.** `TO-6` and `TO-8` both landed — cite each by `file:line @ <commit-ish>`, and show the built package's **BUILD INPUT** carries both changes. ⛔ **Diff the deployed bytes against the BUILD INPUT (source map / manifest), NEVER by filename** — running-bytes-older-than-built passes every naive check. | `INGEST-T3-6` `INGEST-T4-1` | |
| `TO9-AC2` | **APPLIED via `safe-apply`, code-only.** ⛔ **NEVER bare `terraform apply`. NEVER `aws lambda update-function-code`.** Show the plan is scoped to what you intend: state added/changed/destroyed, and **name what the plan says is UNCHANGED** as a did-not-move control. | `INGEST-T3-6` | |
| `TO9-AC3` | **READ BACK FROM THE LIVE PLANE, not the plan.** `CodeSha256` **moved** (it must, this is a code deploy) and matches the built artifact. ⚠ **This is the inverse of the control `0.7.0_AE_CloudOps~Z` used on its config-only change** — there `CodeSha256` had to be IDENTICAL; here it must MOVE. **State which you expect BEFORE you read it.** | `INGEST-T3-6` | |
| `TO9-AC4` | **LEDGER.** Entry opened in `org/critical_paths/change_management/` at apply start, closed at completion. ⛔ **A confirmed deploy is NEVER left half-landed** — finish in-session or roll back and escalate loud. | `INGEST-T4-1` | |
| `TO9-AC5` | ⛔ **DO NOT ASSERT THE SERVED OUTCOME FROM THE DEPLOY.** The apply discharges APPLIED, never EXERCISED. Whether the ~13:00Z artifact carries the field is a **separate, later** measurement against the served `positioning_data.json`, and it belongs to `TO-8` `AC2`. **Report the deploy; do not report condition (ii).** | `INGEST-T5-1` | |

## 4. WHAT IS **NOT** YOURS

- ⛔ **The producer and publisher source.** `0.4.0_DS_ClientPlatform~Q`'s lane (`TO-6`/`TO-8`). **Do not
  edit `data/**` to make an apply succeed** — if the build input is wrong, report it back; a
  cross-lane repair is the SoD violation Rule 13 exists to prevent.
- ⛔ **The `mdpf` pipeline.** ⚠ **A DIFFERENT LAMBDA (`mdpf-gold-lambda`) AND A DIFFERENT PIPELINE.**
  The 13:30Z mdpf hold and this 13:00Z etfs deploy **do not collide** — stated because two 13:xxZ
  constraints on one box invite a false conflict. **Still: no ad-hoc `mdpf` gold run before 13:30Z.**
- ⛔ **`ETFS_SATELLITES` AC6** — `0.7.0_AE_CloudOps~S`'s, a different project. **Rule 27.**
- ⛔ **The `ETFS_POSITIONING` PROD promote** — Andrew's word, not an AE act.

## 5. REPORTING

Deliverable + proof instance in this lane's `deliverables/`, via `.tools/safe-commit.sh --author
"0.7.0_AE_CloudOps~P <0.7.0_AE_CloudOps~P@opal.agent>" -F <msgfile>` (message file written by a
**non-shell** writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt** —
silent receipt and silent completion are both RAVC violations.

<proof_of_spec>
  <criterion id="TO9-AC1" cell_refs="INGEST-T3-6,INGEST-T4-1"/>
  <criterion id="TO9-AC2" cell_refs="INGEST-T3-6"/>
  <criterion id="TO9-AC3" cell_refs="INGEST-T3-6"/>
  <criterion id="TO9-AC4" cell_refs="INGEST-T4-1"/>
  <criterion id="TO9-AC5" cell_refs="INGEST-T5-1"/>
  <expected_criteria>TO9-AC1,TO9-AC2,TO9-AC3,TO9-AC4,TO9-AC5</expected_criteria>
  <alignment_denominators>cells declared: 3 (INGEST-T3-6, INGEST-T4-1, INGEST-T5-1); criteria: 5. FORWARD — 5 of 5 criteria carry >=1 cell_ref. BACKWARD — 3 of 3 declared cells reachable (INGEST-T3-6 from AC1/AC2/AC3, INGEST-T4-1 from AC1/AC4, INGEST-T5-1 from AC5). Unmapped 0; untraceable 0. NOTE: this TO adds NO cell — it is the APPLIED rung of cells already claimed by TO-6 and TO-8. AC5 exists specifically to STOP this TO claiming the EXERCISED rung of INGEST-T5-1, which remains TO-8's.</alignment_denominators>
</proof_of_spec>
