<task_order>
<id>MDPF_COTREMEDIATION.TO-R1-AE.vendor-build-and-deploy-the-silver-contract</id>
<project>MDPF_COTREMEDIATION</project>
<title>Vendor, build, deploy the silver contract and prove the deployed bytes</title>
<issued_to>0.5.0_AE_OpalETL~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>active</status>
<priority>P0 -- LIVE CLIENT-FACING OUTAGE. Andrew-direct 2026-08-25 ~14:20Z: "That needs to get fixed immediately". cottonwood + global served at as_of_last=2026-08-19, FOUR TRADING DAYS behind.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/mdpf-cotremediation/20260825T161149Z/DECOMP.md</ref>
  <ref type="prd">docs/architecture/MDPF_COTREMEDIATION_PRD.md (v1.0)</ref>
  <ref type="directive">D8 -- Model Portfolios Pipeline Fortification</ref>
</references>
<objective>
Carry the silver header-contract change from its SOURCE home into the deployed Lambda: re-vendor,
build, import-health probe, Terraform apply, and verify the DEPLOYED PACKAGE BYTES carry both new
column names. You own the infra half of a two-seat repair whose handoff edge is the thing that
broke. Rule 26: you built it, you apply it, on this device.
</objective>
</task_order>

# TASK ORDER — MDPF_COTREMEDIATION.TO-R1-AE · VENDOR, BUILD, DEPLOY, AND PROVE THE BYTES

**to:** `0.5.0_AE_OpalETL~B` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~16:5xZ

## ⛔ UNCERTIFIED DECOMP — STATED BY THE ISSUER, AS THE PIPELINE REQUIRES

The decomp this TO derives from is **SOLO and UNCERTIFIED** — no fan-out cohort and no CVO were live
at authoring. `3.0.0_SA_CVO` seated at 16:28Z; **the cert is owed and queued behind a sovereign-facing
backlog by CVO's own sequencing, and does not gate your execution.** If a cell looks wrong, that is a
**surprise-channel item** — one line to `3.0.0_SA_CVO`, cc me. **Do not write to
`org/surprise_channel/**` yourself; executing seats are barred from that tree.**

<decomp_ref>
workflows/atom_decomposition/runs/mdpf-cotremediation/20260825T161149Z/DECOMP.md — cells
COTR-inv-1, COTR-inv-2, COTR-inv-3, COTR-inv-4, COTR-inv-5, COTR-inv-6, COTR-inv-7, COTR-inv-8, COTR-inv-9,
COTR-b-3, COTR-b-3a, COTR-b-4,
COTR-c-1, COTR-c-2, COTR-c-3
</decomp_ref>

<decomp_context>
⛔ **TWENTY-FOUR OF THE DECOMP'S 39 CELLS ARE NOT YOURS. Named so the 15-vs-39 difference is VISIBLE:**

- **`COTR-a-1..4`, `COTR-b-1`, `COTR-b-2`, `COTR-d-1..3`, `COTR-e-1..3`, `COTR-f-1..3`, `COTR-g-1..3` (18)
  — `0.4.0_DS_ClientPlatform~M`.** The causal record, the contract edit, the three-partition re-run, and
  ALL payload verification. **They hold the NEVER#6 completion obligation for the whole repair.**
- **`COTR-g-4`, `COTR-h-1`, `COTR-h-2` (3) — routed OUT to D8.** The nine non-trading days, the process
  defect, the `VendorDriftError` misnomer. **CVO has GRADUATED all three. Not criteria against you.**
- **`COTR-i-1..3` (3) — boundary cells, non-criterion-bearing.**

**`COTR-b-3` and `COTR-b-3a` are SHARED with the DS TO and appear in BOTH. That is deliberate — they ARE
the handoff, and a shared cell is how an edge gets an owner on both sides.**
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json COTR1AE-AC1,COTR1AE-AC2,COTR1AE-AC3,COTR1AE-AC4 ; check the rc. -->
  <criterion id="COTR1AE-AC1" cell_refs="COTR-b-3, COTR-b-3a, COTR-inv-8"/>
  <criterion id="COTR1AE-AC2" cell_refs="COTR-b-4, COTR-inv-2, COTR-inv-3"/>
  <criterion id="COTR1AE-AC3" cell_refs="COTR-c-1, COTR-c-2"/>
  <criterion id="COTR1AE-AC4" cell_refs="COTR-c-3, COTR-inv-9"/>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL~B/deliverables/MDPF_COTREMEDIATION.TO-R1-AE_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COTR1AE-AC1,COTR1AE-AC2,COTR1AE-AC3,COTR1AE-AC4</expected_criteria>
  <alignment_denominators>cells in this TO: 15 (inv 9 - b 3 - c 3); criteria: 4; every criterion carries >=1
cell_ref; all 15 cells reachable by >=1 criterion. Unmapped 0; untraceable 0. Decomp total 39; 24 excluded
(18 to the DS lane, 3 routed to D8, 3 boundary non-criterion), each named in decomp_context. COTR-b-3 and
COTR-b-3a are SHARED with MDPF_COTREMEDIATION.TO-R1-DS by design.</alignment_denominators>
</proof_of_spec>

---

## ⛔ THE ONE INSTRUCTION MOST LIKELY TO BE GOT WRONG: **DO NOT EDIT THE SOURCE MAP**

**`infra/aws/lambda/ci/lambda-source-map.json` REQUIRES NO EDIT FOR THIS CHANGE.** CTO ruling 70759,
adopted into the decomp.

`mirror_schemas.py` is **already in the entry's `files` array** (`lambda-source-map.json:2583`). This
repair changes that file's **CONTENTS** — it adds no file, moves no directory, and changes no
`runtime`/`memory`/`tf_file`/`artifact_s3_key` cell. **Nothing in the entry becomes false, so Rule 4
requires no edit.** Rule 4's own warning is the confirming half: *the map pairs a Lambda with its repo
dir and does NOT compare deployed bytes to built-from bytes* — **a map that does not model bytes cannot
need editing because bytes changed.**

⛔ **A needless commit there is a commit on a fail-closed `YANG_PIPELINE_DEPLOY` lane during a live
outage. Don't.**

⚠ **THE FALSIFIER IS YOURS TO WATCH.** If at execution **any** cell in that entry actually goes stale,
**that falsifies the ruling — STOP and re-route to `1.0.0_SA_CTO`.** Do not quietly edit it on your lane
either; CTO wants the measurement back.

*(Disclosure: the decomp briefly said both things — the lane row struck while `COTR-c-1` still required
the update. CTO caught it and both copies are now reconciled. If you find a third stale copy, that is a
finding and I want it.)*

---

## YOUR LEG, IN ORDER

### 1 — THE HANDOFF IN (`COTR-b-3`) — WAIT FOR AN OBSERVED TRIGGER

`mirror_schemas.py` lives in **TWO independently-editable homes**, currently byte-identical
(`85fc671e92ba56491419713c93845b15` both, measured at decomp time). `BUILD_MANIFEST.json` settles
direction: *"repo files are the source of truth; fix there and rebuild, never edit a zip."*

**`data/assets/scripts/silver/mirror_schemas.py` is SOURCE. Your lambda-dir copy is VENDORED FROM IT.**

⛔ **Start on `~M`'s ACTUAL COMMIT HASH, read after their commit returns — never a projected time, a
promise, or "they said they were about to."** That is the OBSERVED-completion trigger and it is a cell.

### 2 — VENDOR AND BUILD (`COTR-b-4`) — AND THE LATENT TRAP IN THIS PACKAGE FAMILY

Re-vendor per `BUILD_MANIFEST.json`. ⛔ **`mirror_conversion.py` is vendored FLAT into FOUR packages**
(`silver-{blackdiamond,eclipse,etf,orion}`). Your schema change is keyed `("blackdiamond","holdings")`
and `holdings/` exists **only** under `blackdiamond/cottonwood/`, so only cottonwood *can* be affected —
**state that structurally, not empirically.**

⛔ **RUN AN IMPORT-HEALTH PROBE AFTER THE BUILD. THIS IS NOT OPTIONAL AND THE MANIFEST SAYS WHY.** Its
own `vendor_closure_note` records a latent vendor-closure break in this exact family: a module missing
from the vendor list is **invisible until somebody rebuilds**, and the rebuilder inherits a break they
did not write. `stream_parquet.py` did exactly this once — the build reported a VERIFIED upload (size +
sha256 match) and `CodeSha256` changed on the live function; **both true, both about a FILE, neither
about a RUNTIME**, and the zip could not import at all. *The manifest also records `eclipse` as still
carrying the same latent break — not yours to fix, but do not be surprised by it.*

### 3 — DEPLOY (`COTR-c-1`) AND PROVE THE BYTES (`COTR-c-2`)

**Terraform only** (Rule 1). **`.tools/safe-apply.sh`, never bare** (NEVER#4). **Rule 26: you apply, on
this device.** Plan → 0-diff apply → tag.

⛔ **`COTR-c-2` IS THE CELL THAT CATCHES WHAT EVERY OTHER PROBE MISSES. A plan 0-diff,
`get-function-configuration`, and a green run ALL PASS ON STALE CODE.** Rule 22a is explicit: a function
whose running bytes are older than its built-from bytes passes DESIRED, APPLIED, and EXERCISED.

**Download the deployed package and read the member. Both column names must be present in the deployed
bytes.** Resolve through the **build input**, never by filename — the repo holds two copies of this file
and a filename-resolved check reports drift where there is none *and reads clean where two copies have
silently diverged*.

### 4 — CLOSE THE EDGE (`COTR-b-3a`) — ON A MEASUREMENT, NOT A REPORT

After both legs land:
```
md5sum data/assets/scripts/silver/mirror_schemas.py \
       infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_schemas.py
```
**IDENTICAL = the handoff is discharged. DIFFERENT = it is not, regardless of what either of you
reports.**

> ⛔ **This cell exists because of exactly what happened on 2026-08-20.** The bronze leg reported
> `QA export PASS 21 cols` — **TRUE for its own leg** — and no step told the silver contract. **The edge
> had no owner, so nobody failed to discharge it.** You and `~M` now both own it, and it closes on a
> comparison neither of you can satisfy by self-report.

### 5 — LEDGER (`COTR-c-3`, `COTR-inv-9`)

**Open a deploy-completion ledger entry in `org/critical_paths/change_management/` at deploy-start;
close it at completion.** NEVER#6: **a begun deploy finishes in-session or rolls back loud to COO.** A
stranded leg is RED-ALERT material, not a follow-up. *(`~M` holds the completion obligation for the
repair as a whole; the deploy leg's ledger is yours.)*

---

## INVARIANTS THAT BIND YOU

⛔ **`COTR-inv-3` — THE GUARD IS CORRECT AND YOU DO NOT WEAKEN IT.** `assert_declared_header` detected a
real shape change and refused rather than silently absorbing two columns — **exactly what Rule 17 asks
of silver.** **No act of yours may make it permissive.** If the deploy fails because the contract is
still wrong, that is the guard working; route it back to `~M`, do not loosen the check.

⛔ **`COTR-inv-5` — `49financial` and `inflection` MOVE ZERO BYTES.** Baseline banked at
`AC4_BASELINE_SHA256.txt`. Any movement STOPS the work.

⛔ **`COTR-inv-7` — NO alarm, SNS, SES, monitor, or freshness-checker.** Standing moratorium. Nothing in
your leg needs one.

⛔ **`COTR-inv-8` — NO shadow path, NO parallel emitter, NO standing comparator.** Build correctly and
port. An ad-hoc run is a QA instrument and **never production evidence.**

**Report to `2.0.0_SA_COO` with evidence. Coordinate the edge directly with `0.4.0_DS_ClientPlatform~M`.**
