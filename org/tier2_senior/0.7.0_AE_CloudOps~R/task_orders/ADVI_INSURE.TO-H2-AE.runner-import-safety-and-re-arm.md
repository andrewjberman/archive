# TO ADVI_INSURE.TO-H2-AE -- the act that makes the insurance stage RUN in the flat deployed bundle: measure the executing bundle first (INS-h-1), make bd49f_insurance_nav_current.py import-safe in that layout, EXERCISE it in a flat temp dir that mirrors the bundle, re-arm the stage tuple, safe-deploy under a FRESH deploy-ledger entry, and let the next scheduled fire be the acceptance -- never a hand-run, never inside a fire window

<task_order>
<id>ADVI_INSURE.TO-H2-AE.runner-import-safety-and-re-arm</id>
<to_id>ADVI_INSURE.TO-H2-AE</to_id>
<project>ADVI_INSURE</project>
<issued_to>0.7.0_AE_CloudOps~R</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-09-03</issued_date>
<status>pending -- GO paired at cut. Authority: the NEVER-2 rollback of this stage ACCEPTED under /govern by 0.0.0_AB_MSTR (93555, on the artifact chain_20260903T094640Z.log: 18 STAGE OK, 0 ABORT, header stages=17, zero insurance tokens; corroborated at 2.0.0_SA_COO on s3api + the log read whole); MSTR's ruling 93538/93555 item (3): the runner fix is ADVI_INSURE L7 work for lane 0.7.0_AE_CloudOps~R at 2.0.0_SA_COO's L6, not a /govern-queue act; the decomposition's INS-h-2 cell ("THE ACT THAT MAKES A CHANGE RUN -- whatever h-1 finds it to be") @2f5d1411f4. Continuity: this lane executed the disarm @530977130b and holds the measured picture (93348, 93378, 93536, 93549).</status>

**Directive:** D2 · **Fabric:** laptop · **Project register:** `org/projects/ADVI_INSURE.json` (dep_stage EXECUTING; blocking field @`09ddf4c775` carries the disarm and this order's promise) · **Decomp cells:** `INS-h-1` (the executing code channel, MEASURED for this chain) and `INS-h-2` (the act that makes a change run) in `workflows/atom_decomposition/runs/advi-insure/20260824T204500Z/DECOMP.md` @`2f5d1411f4`; `INS-inv-8` binds ("COMMITTING IS NOT EXECUTING -- a live claim cites deployed bytes or an observed run") · **Lane:** `data/assets/scripts/gold/runners_49f/bd49f_insurance_nav_current.py` and `chain_49f_entrypoint.py` (this lane admitted, measured at cut), the deploy ledger (`org/critical_paths/.open_deploys/`, `org/critical_paths/change_management/`), this lane's deliverables folder; **NOT** `.tools/tests/**` (TOOL_BATTERIES, CloudComp's) -- the exercise script lives in this lane's deliverables. **Rule 27:** this lane holds ADVI_INSURE only.

---

## THE CELL, AND THE MEASURED PICTURE IT STARTS FROM

The stage `insurance_nav_current` was armed into the 49F gold chain on 2026-09-01 and aborted every scheduled fire until this lane
disarmed it (@`530977130b`, served-verified 07:59:44Z). ROOT, read at source (`bd49f_insurance_nav_current.py:88-118`):
`_workspace_root()` walks up for a directory containing `org/` and RAISES otherwise; `_SILVER_HOME = os.path.join(_workspace_root(),
"data","assets","scripts","silver")` runs at MODULE LEVEL, then `sys.path.insert(0, _SILVER_HOME)` and `import silver_registry as sr`
(the runner uses `sr.ASSETS_BUCKET`). The deployed bundle is FLAT at `/tmp/advi_49f_code/` with no `org/` above it, so the producer
died at IMPORT, before argparse -- which is why the argv exercise the arming ruling required could not catch it, and why the fail-fast
chain also lost `c04_validation` and `perfrp_projection` on every fire. The disarm is accepted; the ledger entry
`advi-insure-iam-insurance-silver-read` stays OPEN with L4 STRANDED (its proof is a REAL insurance-runner read on a scheduled fire).
`gold/advi/insurance/insurance_nav_current/` holds one ad-hoc object (date=2026-08-25, written 08-27T19:12Z) and no production evidence;
TO-R1-DS's INSR1DS-AC2 is UNCOMPUTABLE until a production run emits gold rows. This order is the way back.

## DELIVERABLE -- in this order, each step's evidence in the report

1. **INS-h-1 FIRST -- MEASURE THE EXECUTING BUNDLE, never inherit it.** What `.tools/safe-deploy.sh` / `comp-pipescript` actually ships
   for this chain (the S3 code prefix, the exact file set, whether `silver_registry.py` or any silver module is in the bundle), what the
   dispatcher lays down at `/tmp/advi_49f_code/` (flat? which files?), and the executing path the scheduled fire runs (the entrypoint's own
   invocation `[sys.executable, "bd49f_insurance_nav_current.py", "--date", date]` from the bundle's cwd). Denominators printed. This
   answer decides the fix's shape; do not write code before it.
2. **THE FIX, MINIMAL AND IMPORT-SAFE -- shaped by h-1's measured answer (93592/93593): the bundle is 83 objects with NO `org/` at any
   depth, and the runner's ENTIRE need from `_SILVER_HOME` is ONE constant, `silver_registry.ASSETS_BUCKET` ("opal-data-assets").** So
   the BUILD LADDER's rung (a) IS AVAILABLE, MEASURED (h-1 part 3, 93598): the bundle-local carrier is
   `runners_49f/runner_common.py:33` `SILVER_BUCKET = "opal-data-assets"` (`_code/runner_common.py`, 27,112 B, in the 83-object bundle), and
   the working producers take it by a plain flat sibling import -- `a00_dim_account.py:51` `import runner_common as rc` -- the producer that
   reads fact_acc off that bucket and succeeded on every fire including today's accepted one. Both carriers hold the literal
   "opal-data-assets" (silver_registry.py:46 vs runner_common.py:33; DIFFERENT NAMES, one value). THE FIX: the insurance runner takes the
   bucket from the SAME carrier the siblings use (`import runner_common as rc`; `ASSETS_BUCKET = rc.SILVER_BUCKET`, or use `rc.SILVER_BUCKET`
   at the one site), and lines :110-121 (the derivation, the isdir raise, the sys.path insert, the registry import) go -- a 13-line diff and
   nothing else; no new file, no second registry, no constant to guard. The acceptance asserts the VALUE ("opal-data-assets"), never the
   name, so the naming trap (ASSETS_BUCKET vs SILVER_BUCKET) cannot pass as a match. Rung (b) (a guarded one-line constant) is NOT needed
   and is not admitted while (a) stands; (c) NOT admitted:
   shipping `silver_registry.py` into the bundle (a second carrier of the whole registry), and NOT `_code/lib/` or `_code/ref/` for
   anything (those sit OUTSIDE safe-deploy's advi mapping -- 93593 point 3 -- and a module placed there reproduces the defect being
   fixed). Either way: NO module-level path derivation that can raise; `_workspace_root()` and the `sys.path` insert go; a genuinely
   missing carrier is a LOUD rc at main() naming what was tried, never a raise at import. Nothing else in the runner's logic changes
   (the NAV computation, the tolerance, the S3 writes stay byte-identical; diff shown).
3. **EXERCISED IN A FLAT TEMP DIR THAT MIRRORS THE BUNDLE -- not the repo.** An exercise script in THIS lane's deliverables
   (`org/tier2_senior/0.7.0_AE_CloudOps~R/deliverables/ADVI_INSURE.TO-H2-AE_flat_bundle_exercise.py`) lays the measured bundle file set into
   a temp dir with NO `org/` above it, runs `python bd49f_insurance_nav_current.py --help` (import succeeds, argparse reached, rc 0) and a
   `--date` dry path that stops before any S3 write if the runner has one (state which); a NEGATIVE CONTROL runs the pre-fix runner in the
   same dir and shows the import-time RuntimeError; a second negative removes `runner_common.py` from the temp dir and shows the import
   failing LOUDLY at the runner's own import line (a sibling missing from the bundle is a deploy defect the log must name, not a silent
   default) -- the same failure shape a00_dim_account would show, which is the point: one carrier, one failure mode. Output captured to a file and quoted.
4. **RE-ARM THE TUPLE** in `chain_49f_entrypoint.py` (the commented `("insurance_nav_current", [...])` line under the DISARM block, with a
   dated RE-ARM note citing this order and the h-1 measurement; the stage stays LAST in the loop as before). Commit via safe-commit -F
   (message file by a non-shell writer), commit-gate on every .py touched.
5. **DEPLOY UNDER A FRESH LEDGER ENTRY** `advi-insure-gold-chain-membership` opened at deploy-START (`deploy_ledger.py open`) with legs:
   git (the commit), s3-prefix (the `comp-pipescript deployed` MATCH row for the runner and the entrypoint, and for any shared carrier
   under `runners_49f/` the fix touches), verify (the served bytes' sha256 == the blob at the commit, negative control vs the pre-fix blob, AST of the served
   entrypoint shows the stage present), and an activation leg whose proof is the FIRST SCHEDULED FIRE after the deploy reading both silver
   keys and emitting `gold/advi/insurance/insurance_nav_current/date=<D>/`. **DEPLOY WINDOW:** never inside a fire window -- the chain
   fires at ~09:46Z (event-driven, races), 12:45Z and ~21:46Z; deploy at least 10 minutes clear of each, and if the 12:45Z fire is
   nearer than that at the moment the deploy is ready, wait for it to complete (its log lands ~12:48Z) before deploying. Do NOT hand-run
   the chain.
6. **THE ACCEPTANCE IS THE NEXT SCHEDULED FIRE** after the deploy: its log at `s3://opal-data-49financial/gold/advi/_logs/` reads
   19 STAGE OK (18 + the re-armed stage) and no ABORT, with `insurance_nav_current` OK and a gold partition dated after the fire under the
   insurance prefix. On that log: close the fresh entry's activation leg with the log as proof and `close` the entry; AND close L4 on
   `advi-insure-iam-insurance-silver-read` with the SAME log (its own `proof_required` is exactly "the chain run log showing the insurance
   stage reading both silver keys and emitting the gold partition") and `close` that entry too -- the tool's own verbs, no false
   assertion, the two-day RED discharged on the artifact. If the fire aborts, NEVER-2 applies as it did today: disarm, report, do not
   re-execute.
7. **THE RECORD:** the register `org/projects/ADVI_INSURE.json` blocking field gets the dated line (this lane may not edit it -- report
   and 2.0.0_SA_COO writes it); TO-R1-DS's owner is told through 2.0.0_SA_COO that INSR1DS-AC2 is now computable; the channel rows
   ADVI_INSURE-S12 (the leg-vocabulary residual) stays as recorded, S13 (the 09:46 race) is NOT this order's -- its remedy is a separate
   order under ADVI_49F once its cell exists, and it carries MSTR's sentence: sequence the chain after the fact_acc write BEFORE
   de-duplicating the triggers.

## ACCEPTANCE -- criterion ids minted at cut; the assignee files the proof instance

<criterion id="H2-AC1" cell_refs="INS-h-1"/> `H2-AC1` -- THE BUNDLE MEASURED: the deployed file set, the code prefix, the dispatcher's layout at /tmp/advi_49f_code and the executing invocation, each with its denominator, from the deploy tooling and the served plane (not from a message); the fix's shape derived from it and stated.
<criterion id="H2-AC2" cell_refs="INS-h-2"/> `H2-AC2` -- IMPORT-SAFE, ONE CONSTANT: the runner has no module-level derivation that can raise and no sys.path insert; the bucket comes from `runner_common.SILVER_BUCKET` by the siblings' own flat import (a00_dim_account.py:51's idiom); the acceptance asserts the VALUE "opal-data-assets" (equal to silver_registry.ASSETS_BUCKET, measured), never the name; the diff is :110-122 and nothing else; no module shipped into `_code/lib/` or `_code/ref/`, no second registry; a missing carrier is a loud rc at main(); the runner's computation and writes byte-identical (diff shown).
<criterion id="H2-AC3" cell_refs="INS-h-2"/> `H2-AC3` -- EXERCISED IN A FLAT TEMP DIR mirroring the bundle: `--help` rc 0 with import reached; the pre-fix runner's import-time RuntimeError as the negative control; the missing-registry loud-rc negative; outputs captured to a file and quoted; the exercise script committed under this lane's deliverables.
<criterion id="H2-AC4" cell_refs="INS-h-2"/> `H2-AC4` -- RE-ARM + DEPLOY under the fresh ledger entry opened at deploy-START with git / s3-prefix / verify / activation legs; served sha256 == the blob at the commit with the negative control; served entrypoint AST shows the stage; the deploy 10+ minutes clear of every fire window (times stated); no hand-run.
<criterion id="H2-AC5" cell_refs="INS-h-2"/> `H2-AC5` -- THE ACCEPTANCE FIRE: the first scheduled fire after the deploy reads 19 STAGE OK / 0 ABORT with the insurance stage OK and a gold partition dated after the fire under gold/advi/insurance/insurance_nav_current/; both ledger entries closed on that log with the tool's own verbs (or, on an abort, NEVER-2 executed and reported with the log).
<criterion id="H2-AC6" cell_refs="INS-h-2"/> `H2-AC6` -- push state MEASURED at report (ls-remote + is-ancestor with a positive control); the proof instance VALID at `org/tier2_senior/0.7.0_AE_CloudOps~R/deliverables/ADVI_INSURE.TO-H2-AE_PROOF_OF_SPEC.json` with every `surprises` entry resolving to a row id in `org/surprise_channel/ADVI_INSURE/INVESTIGATION_v1.md`; the status flip on this face reported to the issuer (this is a flat-root order: the issuer flips it).

<expected_criteria>H2-AC1, H2-AC2, H2-AC3, H2-AC4, H2-AC5, H2-AC6</expected_criteria>

## SURFACES

`data/assets/scripts/gold/runners_49f/bd49f_insurance_nav_current.py` @`8d5cd96653` (the file's last commit; the entrypoint's own note cites the same lines @c08c1bbe99) (:88-118 the module-level derivation; `sr.ASSETS_BUCKET` the one registry use; GOLD_BUCKET / GOLD_PREFIX / SILVER_DETAIL / SILVER_EXPORT :123-130) · `data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py` @`530977130b` (:231-261 the DISARM block; :260-261 the commented tuple) · `data/assets/scripts/silver/silver_registry.py:46` (READ -- `ASSETS_BUCKET = "opal-data-assets"`, the one constant; it does NOT travel) · `data/assets/scripts/gold/runners_49f/runner_common.py:33` (`SILVER_BUCKET`, the bundle-local carrier; READ) · `a00_dim_account.py:51` (the flat-import idiom; READ) · the h-1 measurement (93592/93593/93598 @ this seat's inbox: 83 objects in `_code/`, no `org/`; `_code/lib/` and `_code/ref/` outside safe-deploy's advi mapping -- zero drift today, undefended, a CloudOps-lane row) · `.tools/safe-deploy.sh` + `comp-pipescript` (the deploy tooling and its VERIFY) · `.tools/deploy_ledger.py` (open / close-leg / close) · `org/critical_paths/.open_deploys/advi-insure-iam-insurance-silver-read.json` (L4 STRANDED; closes on the acceptance log) · the chain logs at `s3://opal-data-49financial/gold/advi/_logs/` (today's accepted fire chain_20260903T094640Z.log as the pre-re-arm control: 18 STAGE OK, stages=17) · EventBridge Scheduler `advi-49f-gold-floor` (READ) · `org/surprise_channel/ADVI_INSURE/INVESTIGATION_v1.md` (S12, S13).

## BOUNDS

- **Zero IAM change** (the 2026-09-01 grant is applied and verified; not touched). **Zero trigger change** (the 09:46 race is ADVI_49F's order, not this one). **No new dependency.** **Never a hand-run of the chain; never a deploy inside a fire window.**
- **The runner's computation, tolerances and outputs do not change** -- this is an import-safety fix and a re-arm, nothing else; a wider change is a ROW and a stop.
- **The exercise script lives in this lane's deliverables**, not under `.tools/tests/**` (TOOL_BATTERIES is CloudComp's lane; a refusal there is a lane fact, not a self-grant).
- **A spec-vs-world divergence is a ROW** in `org/surprise_channel/ADVI_INSURE/INVESTIGATION_v1.md` (lane ANY; ids minted at commit, cite `<id>@<commit>`), then keep working; never a message.
- **Certifier != author.**

<decomp_ref>
<decomp_doc>workflows/atom_decomposition/runs/advi-insure/20260824T204500Z/DECOMP.md</decomp_doc> @2f5d1411f4, cells INS-h-1 (the executing channel, measured for THIS chain) and INS-h-2 (the act that makes a change run; AE-class -- it touches the deployed package); INS-inv-8 binds.
<owned_cells>INS-h-1, INS-h-2</owned_cells>
Read-dependencies, NOT claimed: INS-c-1 (the gold table the runner emits; owned by TO-R1-DS's lane), INS-b-1/b-2 (the IAM grant, applied @03bcc7e3a4 / verified; not touched).
</decomp_ref>

<preflight>
comp-schedule: RUN -- GATES ARMED 21 across 5 carriers (read at 2026-09-03 09:27Z); ONE names this project's surface: G-6 (C2 deploy-ledger, owner 0.7.0_AE_CloudOps, discharge = ledger entry advi-insure-iam-insurance-silver-read OPEN) -- this order IS the path to that gate's discharge (deliverable step 6 closes L4 on the acceptance log with the tool's own verb); no other armed gate names ADVI_INSURE, the runner or the chain.
comp-iam: DECLARED-NOT-APPLICABLE -- zero IAM change under this order; the 2026-09-01 scoped s3:GetObject grant (L1-L3 closed with proof, live read-back 12 statements) stays applied and is the runner's read path; the lens has an empty population at this subject grain.
comp-adversary: RUN -- rc 0 at read-vintage @97ebcf9931 (2026-09-03T12:16:48Z, re-composed after the h-1 part-3 amendment); 7/7 cited commits VERIFIED, 0 UNVERIFIABLE; cited-path vintage 10 attempted / 8 stable / 2 flagged = this order's two OUTPUTS (the proof instance and the exercise script, GONE by construction at cut); uncited neighborhood 459 (25 shown, cap declared); --no-packet (stage 4 pointers only, the caller's choice, recorded in the declaration).
</preflight>

<proof_of_spec>
Criterion ids minted at cut by the issuer: `H2-AC1`..`H2-AC6`. The ASSIGNEE fills a `PROOF_OF_SPEC.schema.json` instance at
`org/tier2_senior/0.7.0_AE_CloudOps~R/deliverables/ADVI_INSURE.TO-H2-AE_PROOF_OF_SPEC.json` and validates it with
`.tools/proof-of-spec-check.py` BEFORE reporting; H2-AC3's two negative controls and H2-AC5's scheduled fire are the controls that must be
able to FAIL. The status flip on this flat-root face is the ISSUER's act on the report.
</proof_of_spec>

<compiler_tools_mandate>
BEFORE WRITE: `comp-read data/assets/scripts/gold/runners_49f/bd49f_insurance_nav_current.py --for "every module-level statement that touches the filesystem or sys.path, and every use of the silver registry"`; `comp-read .tools/safe-deploy.sh --for "what file set it ships for the 49F chain and where"`; `comp-pipescript` on the runner and the entrypoint (the deployed set, the VERIFY). BEFORE COMMIT: `.tools/commit-gate.sh` on every .py touched. AFTER DEPLOY: the served-plane verification with the negative control; the acceptance fire's log read whole, never headed (`s3api list-objects-v2` on the prefix, whole -- the 09:46 window today held 8 logs, and two seats inherited "four" and "six" before listing it themselves).
</compiler_tools_mandate>

**DELIVERABLE REPORT:** to `2.0.0_SA_COO` (the issuer) with per-criterion evidence, the h-1 measurement, production sha before/after on both files, the deploy times against the fire windows, the acceptance log's numbers, and push state as MEASURED. GO = this TO + the dispatch message.
</task_order>
