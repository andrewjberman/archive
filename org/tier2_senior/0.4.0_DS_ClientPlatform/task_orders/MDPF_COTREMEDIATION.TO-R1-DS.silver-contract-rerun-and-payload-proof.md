<task_order>
<id>MDPF_COTREMEDIATION.TO-R1-DS.silver-contract-rerun-and-payload-proof</id>
<project>MDPF_COTREMEDIATION</project>
<title>The silver contract, the three-partition re-run, and the payload proof (holds NEVER#6 completion)</title>
<issued_to>0.4.0_DS_ClientPlatform~M</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- CLOSED 2026-08-25 ~21:3xZ by 2.0.0_SA_COO (issuer). CLOSED ON PROOF + ARTIFACT, BOTH: the instance at instance_path carries 8 of 8 acceptance rows PASS, AND the outage this TO existed to remediate is resolved on the SERVED plane -- all four MDPF partners serving 2026-08-24, verified on the served payload by 0.4.0_DS_ClientPlatform~N (global as_of_last=2026-08-24 with _provenance.source_keys naming the 2026-08-24 gold partition; 49financial 12,310 leaf fields compared -> 1 differing, inflection 12,375 -> 1 differing, both _provenance.written_at). Deploy-completion ledger CLOSED @222fdf3042. Flagged by 1.0.0_SA_CTO (71345) as a record lagging reality: ACTIVE while its work was done. Prior status: active</status>
<priority>P0 -- LIVE CLIENT-FACING OUTAGE. Andrew-direct 2026-08-25 ~14:20Z: "That needs to get fixed immediately". cottonwood + global served at as_of_last=2026-08-19, FOUR TRADING DAYS behind, NEVER#1 discharged first.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/mdpf-cotremediation/20260825T161149Z/DECOMP.md</ref>
  <ref type="prd">docs/architecture/MDPF_COTREMEDIATION_PRD.md (v1.0)</ref>
  <ref type="directive">D8 -- Model Portfolios Pipeline Fortification</ref>
</references>
<objective>
Restore cottonwood and global MDPF served data to the correct T-1 frontier THROUGH THE REAL
PRODUCER CHAIN, and prove the restoration at the PAYLOAD layer -- never at the object layer.
Declare the two added columns as Rule-17 passthrough in the silver header contract, re-run the
THREE refused partitions, and carry every payload verification. 49financial and inflection move
ZERO BYTES. You hold the NEVER#6 completion obligation for the whole repair.
</objective>
</task_order>

# TASK ORDER — MDPF_COTREMEDIATION.TO-R1-DS · THE SILVER CONTRACT, THE RE-RUN, AND THE PAYLOAD PROOF

**to:** `0.4.0_DS_ClientPlatform~M` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~16:5xZ

## ⛔ UNCERTIFIED DECOMP — STATED BY THE ISSUER, AS THE PIPELINE REQUIRES

**The decomp this TO derives from is SOLO and UNCERTIFIED.** No fan-out cohort and no CVO were live
at authoring (roster: MSTR, CTO, CTO~X, COO). `3.0.0_SA_CVO` seated at 16:28Z **after** the decomp
landed; **the cert is owed and queued behind a sovereign-facing estate-report backlog, by CVO's own
sequencing.** Nothing about the cert gates your execution — CVO has said so explicitly.

**What this means for you:** execute on spec. **If a cell looks wrong, that is a SURPRISE-CHANNEL
item, not something to absorb** — one line to `3.0.0_SA_CVO`, cc me. **Do not write to
`org/surprise_channel/**` yourself; executing seats are barred from that tree.**

<decomp_ref>
workflows/atom_decomposition/runs/mdpf-cotremediation/20260825T161149Z/DECOMP.md — cells
COTR-inv-1, COTR-inv-2, COTR-inv-3, COTR-inv-4, COTR-inv-5, COTR-inv-6, COTR-inv-7, COTR-inv-8, COTR-inv-9,
COTR-a-1, COTR-a-2, COTR-a-3, COTR-a-4,
COTR-b-1, COTR-b-2, COTR-b-3, COTR-b-7,
COTR-d-1, COTR-d-2, COTR-d-3,
COTR-e-1, COTR-e-2, COTR-e-3,
COTR-f-1, COTR-f-2, COTR-f-3,
COTR-g-1, COTR-g-2, COTR-g-3
</decomp_ref>

<decomp_context>
⛔ **TEN OF THE DECOMP'S 39 CELLS ARE NOT YOURS. Named so the 29-vs-39 difference is VISIBLE rather than lost:**

- **`COTR-b-4`, `COTR-c-1..3` (4) — THE DEPLOY LEG, `0.5.0_AE_OpalETL~B`.** Re-vendor into the lambda
  dir, build, import-health probe, Terraform apply. **That lane is `CLOUD_OPS_OR_ETL` and you are not
  in it — a commit there will be REFUSED, fail-closed (`rollout_phase: 2`). Do not attempt it.**
- **`COTR-g-4` (1) — the NINE NON-TRADING DAYS in cot/global.** ⛔ **REAL DEFECT, ROUTED TO D8, AND
  EXPLICITLY BARRED FROM THIS REPAIR.** It predates the freeze, survives it, and your re-run will not
  touch it. **If you notice it, that is expected — do not fix it here.** Folding it in makes a P0 wait
  on a data-quality investigation.
- **`COTR-h-1`, `COTR-h-2` (2) — the process defect + the `VendorDriftError` misnomer.** Routed to D8;
  CVO has already GRADUATED both. **You cannot close them and they are not criteria against you.**
- **`COTR-i-1..3` (3) — boundary cells, non-criterion-bearing.**

**`COTR-b-3` and `COTR-b-7` are SHARED with the AE seat and appear in BOTH TOs. That is deliberate:
they ARE the handoff, and a shared cell is how an edge gets an owner on both sides.**
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json COTR1DS-AC1,COTR1DS-AC2,COTR1DS-AC3,COTR1DS-AC4,COTR1DS-AC5,COTR1DS-AC6,COTR1DS-AC7 ; check the rc. -->
  <criterion id="COTR1DS-AC1" cell_refs="COTR-a-1, COTR-a-2, COTR-a-3, COTR-d-3"/>
  <criterion id="COTR1DS-AC2" cell_refs="COTR-b-1, COTR-b-2, COTR-inv-2, COTR-inv-3"/>
  <criterion id="COTR1DS-AC3" cell_refs="COTR-d-1, COTR-d-2, COTR-inv-4, COTR-inv-6"/>
  <criterion id="COTR1DS-AC4" cell_refs="COTR-e-1, COTR-e-2, COTR-inv-1"/>
  <criterion id="COTR1DS-AC5" cell_refs="COTR-e-3, COTR-a-4, COTR-inv-5"/>
  <criterion id="COTR1DS-AC6" cell_refs="COTR-f-1, COTR-f-2, COTR-f-3, COTR-inv-7"/>
  <criterion id="COTR1DS-AC7" cell_refs="COTR-g-1, COTR-g-2, COTR-g-3"/>
  <criterion id="COTR1DS-AC8" cell_refs="COTR-b-3, COTR-b-7, COTR-inv-8, COTR-inv-9"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~M/deliverables/MDPF_COTREMEDIATION.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>COTR1DS-AC1,COTR1DS-AC2,COTR1DS-AC3,COTR1DS-AC4,COTR1DS-AC5,COTR1DS-AC6,COTR1DS-AC7,COTR1DS-AC8</expected_criteria>
  <alignment_denominators>cells in this TO: 29 (inv 9 - a 4 - b 4 - d 3 - e 3 - f 3 - g 3); criteria: 8; every
criterion carries >=1 cell_ref; all 29 cells reachable by >=1 criterion. Unmapped 0; untraceable 0. Decomp total
39; 10 excluded (4 to the AE lane, 3 routed to D8, 3 boundary non-criterion), each named in decomp_context.
COTR-b-3 and COTR-b-7 are SHARED with MDPF_COTREMEDIATION.TO-R1-AE by design.</alignment_denominators>
</proof_of_spec>

---

## ⛔ THE THING THAT WILL MISLEAD YOU, AND IT HAS ALREADY MISLED FOUR INSTRUMENTS

**THE SERVED OBJECTS ARE REWRITTEN EVERY DAY.** All four partners' keys were written within two
seconds of each other today, and have been every day through the entire outage. **The publisher runs,
emits, and succeeds. THE STALENESS IS INSIDE THE PAYLOAD.**

**There are THREE layers that read HEALTHY on frozen data, and each is CORRECT about what it measures:**

| layer | what it says | why it is blind |
|---|---|---|
| object `LastModified` / `s3 ls` age / `comp-freshness` | fresh, today | correct **about the FILE** |
| payload `_provenance.written_at` | fresh, today | **advances daily at FIXED WIDTH** — a payload field that is still not the data |
| byte size | unchanged, stable | 08-21 and 08-25 versions are **size-identical and byte-different** |

⛔ **A seat told "read the payload, not the object" reaches for `written_at` and is EXACTLY AS BLIND as
the mtime readers were.** Measured at decomp time. **Key on `_provenance.source_keys` and `as_of_last`.**

**`COTR-f-1`: THE DISCRIMINATOR ALREADY EXISTS — DO NOT BUILD AN INSTRUMENT.** `source_keys` names the
exact gold partition the payload was built from, and on the frozen partners it has read
`.../aggregate-aua-timeseries/2026-08-19.json` for **five consecutive daily republishes**. The whole
check is *that date vs `expected_last_trading_day`*. Build-ladder rung 2.

---

## YOUR LEG, IN ORDER

### 1 — THE CONTRACT (`COTR-b-1`, `COTR-b-2`)

Edit `data/assets/scripts/silver/mirror_schemas.py`, the `("blackdiamond", "holdings")` dict at
`:457-477` (19 declared columns). **Add `Account Supervised` and `Holding Supervised` as Rule-17
passthrough, WITH DELIBERATE DTYPES.**

⛔ **ORDER IS PART OF THE CONTRACT. APPENDING BOTH WILL STILL FAIL.** `assert_declared_header`
(`mirror_conversion.py:263-270`) compares **the exact tuple, order included** — *"positional formats
earn a positional check."* Reported observed positions: `Account Supervised` at **index 8** (before
`AssetID`), `Holding Supervised` at **index 20** (last).

⛔ **CONFIRM POSITIONS BY READING ROW 1 OF THE ACTUAL XLSX. Do not take my arithmetic, the CTO's, or
this TO's.** The bronze files are on disk. **This is the single most likely wasted cycle on the job.**

⛔ **DTYPE: READ THE ACTUAL VALUES before declaring. Do not assume string.**

### 2 — THE HANDOFF (`COTR-b-3`, `COTR-b-7`) — SHARED, AND IT IS WHAT BROKE LAST TIME

`mirror_schemas.py` lives in **TWO independently-editable homes**. `BUILD_MANIFEST.json` settles the
direction: *"repo files are the source of truth; fix there and rebuild, never edit a zip."* **You edit
the SOURCE home. `0.5.0_AE_OpalETL~B` re-vendors it.**

**Send them the OBSERVED trigger — your actual commit hash, READ AFTER the commit returns, never a
projected one or a promise.**

⛔ **THE EDGE CLOSES ON A MEASUREMENT, NOT A REPORT.** After both legs land:
`md5sum data/assets/scripts/silver/mirror_schemas.py infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_schemas.py`
**Identical = discharged. Different = not, whatever either of you reports.** *(Pre-repair baseline:
both `85fc671e92ba56491419713c93845b15`.)*

> **This cell exists because on 2026-08-20 the bronze leg reported `QA export PASS 21 cols` — TRUE for
> that leg — and no step told the silver contract. The edge had no owner, so nobody failed to
> discharge it.**

### 3 — THE RE-RUN (`COTR-d-1..3`)

⛔ **THREE PARTITIONS: `date=2026-08-20`, `date=2026-08-21`, `date=2026-08-24`. NOT five days.**
**2026-08-22 and 08-23 are Sat/Sun — the vendor emitted nothing and none is owed.** **Name the weekend
in your report** so nobody downstream reads two absent partitions as a defect.

⛔ **`COTR-d-3`: A CLEAN RE-RUN DOES NOT ESTABLISH CAUSE.** It establishes the producer works when run
today. **AC1 is discharged by the source record, never by your re-run.** You have already stated you
will not cite it as AC1/AC5 evidence — that is exactly right and it is now a criterion.

### 4 — DOWNSTREAM AND THE PROOF (`COTR-e-1..3`, `COTR-f-1..3`)

Propagate through the real chain (`mdpf_gold_consolidator.py:92,:860`, `build_mdpf_spine.py:56`,
`dim_mdpf_aggregate_aua_timeseries.py:1915`). ⛔ **Cottonwood MDPF code is in `data/mdpf/scripts/gold/`
with everyone else's. `data/cot/scripts/gold/` is Cottonwood's *ADVI* pipeline — a different PRODUCT.
Asserted once as evidence and corrected by Andrew; do not re-derive it.**

⛔ **`COTR-e-3` / `COTR-inv-5` — AC4 IS AN INVARIANT: `49financial` and `inflection` MOVE ZERO BYTES.**
Baseline banked pre-repair at `AC4_BASELINE_SHA256.txt` with its normalisation stated (raw S3 bytes).
**Any movement is a defect and STOPS the work. It is not reconciled after the fact.**

**`COTR-f-2`: exercise the frontier read on BOTH arms.** Both fixtures already exist — the failing arm
is any pre-repair version (versioning is ENABLED; cottonwood `U07eSmo2rr5kesv2JTXjxe6JD6c0yvAw` @
08-21), the passing arm is today's `49financial`. **An instrument only ever run against the state it
was built for has never been tested.**

### 5 — THE SIGNATURES (`COTR-g-1..3`)

⛔ **L1 and L2 DO NOT REPRODUCE on the served payload** (cottonwood `nulls = 0 of 458`, clean ascending;
global's tail clean consecutive, zero repeats). **They are RELOCATED, NOT REFUTED.** Someone saw a
null-filled array *somewhere* — gold object, `D_05`, a per-model series, another field. **Find which
artifact carries it, or produce a controlled absence over an enumerated set.**
**NOBODY IS TO RECORD L1 AS IMAGINARY.** CVO has filed it `UNDER_INVESTIGATION` and an open item blocks
the zero-graduation round — **do not let it read as closed.**

**`COTR-g-3`:** cot and global `dates` arrays are **identical** (`cot.dates == global.dates` → True).
Strong shared-cause evidence — **not a proof. AC3 asks for a proof, not a correlation.**

---

## WHAT WOULD FALSIFY THE WHOLE THING

**`COTR-inv-5`.** A single byte of movement on `49financial` or `inflection` means the remedy reaches
partners it must not. **That is a DESIGN error, not an implementation slip. Report and STOP.**

**`COTR-g-1`.** If the frontier restores and the null-fill is never explained, **this project is NOT
done however good the served payload looks.** AC5 unmet; the producing condition is still armed.

## COMPLETION

⛔ **YOU HOLD `COTR-inv-9` / NEVER#6 FOR THE WHOLE REPAIR.** Open a deploy-completion ledger entry in
`org/critical_paths/change_management/` at deploy-start; close it at completion. **A begun deploy
finishes in-session or rolls back loud.** **Your completion is NOT discharged on your commit landing —
it is discharged when the DEPLOYED PACKAGE BYTES carry the declaration (`COTR-c-2`, AE's leg, your
obligation to confirm).**

**Report to `2.0.0_SA_COO` with evidence. Surprises: one line to `3.0.0_SA_CVO`, cc me.**
