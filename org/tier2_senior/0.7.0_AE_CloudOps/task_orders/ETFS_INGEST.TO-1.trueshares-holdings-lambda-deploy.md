# TO ETFS_INGEST.TO-1 — deploy the TrueShares holdings call site (`INGEST-T0-3`): a TF-only deploy of code that already exists

<task_order id="ETFS_INGEST.TO-1" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md — cells `INGEST-T0-3` (the TrueShares source), `INGEST-T1-3` (the bronze holdings feed it writes), `INGEST-INV-1` (deployed bytes == the source they are built from)</decomp_ref>
<certification>⛔ **UNCERTIFIED DECOMP.** The stage-3 run is authored and NOT yet certified — `3.0.0_SA_CVO~Z` (certifier of record) is seated as of 19:57Z and has not signed. Stated on this TO's face per DIRECTIVE_EXECUTION_PIPELINE.md Stage-3. **The decomp is also a REDUCED-COHORT run: one independent perspective (the author's). Read its cells accordingly.** This TO is cut ahead of certification deliberately, because the cell it discharges has a real clock (below) — a disclosed trade, not an oversight.</certification>
<issued_to>AE-class (Lambda / Terraform / deploy). Seated: `0.7.0_AE_CloudOps~Z` (live pid 5024, spawned 20:06Z ahead of this TO).</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED. No dependency, no queue — this is the first cut of round 1 and nothing is sequenced ahead of it.</seating_trigger>
<placement>**SITE Z** (Rule 26 — the apply runs on the device that owns the work; D4 is SITEZ until the project is done, Andrew-direct 2026-08-24). `terraform` v1.15.8 resolves on PATH here — **resolve the binary, do not assume `.tools/terraform.exe`, which does not exist on this box.**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T20:1xZ</issued>
<status>pending</status>
<priority>P1 — the cheapest cell in the decomp and the only one with a clock.</priority>
<authority>Andrew-direct 2026-08-24 ~19:5xZ (stage-3 GO) + ~20:0xZ (*"all recs approved, proceed"* → **C4 RULED: the `etfs-netassets-daily` Lambda is the TrueShares vehicle**; record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260824_ALL_RECS_APPROVED_C2_C3_C4_C5.md`). PRD `docs/architecture/ETFS_INGEST_PRD.md` §3 F2, §4 T0/T1, §8. CLAUDE.md Rule 1 (Terraform is the only Lambda deploy mechanism), Rule 4 (source map), Rule 5 (size deliberately), Rule 22a (verify on the right layer), NEVER#4 (`safe-apply`, never bare), NEVER#6 (a begun deploy finishes in-session or rolls back loud).</authority>
</task_order>

## WHAT THIS IS — one sentence

**The code you are deploying already exists at HEAD and is not the code that is running.** There is
**zero new code** in this task order. Your deliverable is a Terraform apply, a verification that the
running bytes changed, and a proof that the path actually executes.

## THE MEASURED STATE — re-derived at the COO seat 2026-08-24 ~19:5xZ, with controls

**Do not cite these figures. Re-derive them yourself before you apply — that is `INGEST-TO1-AC1`, and
it is first for a reason.** They are printed so you know what a correct re-derivation looks like, and
so a disagreement is visible immediately.

| | DEPLOYED (package downloaded from `Code.Location`) | HEAD / working tree |
|---|---|---|
| `lambda_function.py` | **1083 lines, 49,995 B, sha256 `f306aa237e3e…`** | **1126 lines, 51,885 B, sha256 `e6f9fe5391da…`** |
| `fetch_trueshares_holdings` | **1** — its `def` at `:420`, **no call site** | **3** — `def :431`, comment `:532`, **CALL `:552`** |
| `TS_HOLDINGS_ENABLED` | 2 (both on `:381`, one line) | 6 (5 lines; the guard is `:550`, the `SKIP:` else at `:559`) |
| positive control `fetch_filepoint` | **3** | **4** |
| negative control `zzz_no_such_token_9999` | **0** | **0** |
| package members | 2 — `lambda_function.py`, `landing_guard.py` | source dir carries both (source map `files`) |
| **line endings** | ⛔ `lambda_function.py` **CRLF (1083 pairs)** · `landing_guard.py` **LF** | **both LF, 0 CRLF** |

> ⚠ **LINE-COUNT CONVENTION, so nobody re-measures and thinks they found drift:** the deployed member
> **ends with a newline**, so `wc -l` / newline-count = **1083**; a "newline + 1" convention reads
> **1084**. Both figures are in circulation and neither changes anything. *(This is the same
> trailing-newline hazard that corrupted the F8 row counts earlier today — DECOMP §1.1 — firing in the
> opposite direction. Whenever a count is off by exactly one, check the final byte first.)*

## ⛔ Z-S4 — THE PREMISE ORACLE WAS WRONG AND IS CORRECTED HERE. READ THIS BEFORE YOU COMPARE ANYTHING.

**A raw byte comparison of the deployed package against the repo RETURNS DIVERGENT AFTER A COMPLETELY
CORRECT DEPLOY.** Found by `3.0.0_SA_CVO~Z` (msg 4865), corrected by `1.0.0_SA_CTO~Z` (msg 4874),
**and re-derived independently at the COO seat before being written into this TO:**

| scan over the **6** commits that have ever touched `lambda_function.py` | matches |
|---|---|
| **RAW** byte compare vs the deployed member | **0 of 6** |
| **CRLF-NORMALIZED** compare vs the deployed member | **1 of 6 → `541a393798`** (DS, 2026-08-19T20:16:38-04:00, *"D4c Phase A … DISABLED by default"*) |

Positive control (a blob vs itself) **PASSES**; negative control (bogus ref) returns
**`fatal: invalid object name` at rc=128, stderr NOT discarded**. So the controls work — **and the raw
scan's clean, well-controlled ZERO supports the conclusion "the running code was built from a tree
state that was never committed," which is a Rule-2 provenance ACCUSATION, and it is FALSE.**

⛔ **THE CONTROL THAT MAKES IT AIRTIGHT, AND WHY IT IS SO CONVINCING: `landing_guard.py` in the SAME
package is LF and matches the repo RAW (measured: 5,998 B both sides, identical sha).** So this is not
the packaging step normalizing everything — it is edit-time CRLF on a Windows box, affecting one
member. **A verifier sees ONE member drifted and ONE clean, which is exactly what a genuine partial
drift looks like.**

**THE DISARM — three parts, and the third is the one that protects the next verifier rather than you:**
1. **Compare CRLF-NORMALIZED, PER MEMBER.** Never a raw sha of the package or of a member.
2. **Compare against the commit ACTUALLY DEPLOYED (`541a393798`), not only HEAD.** Against HEAD the
   normalized compare *also* differs — correctly, because HEAD has the call site and the deployed
   bytes do not. Both comparisons are needed and they answer different questions.
3. **After your deploy, STATE whether the new package is CRLF.** If your build runs on this Windows
   box it probably is. **That is not a defect in your deploy — it is a fact the next verifier needs.**

**`comp-closure` will return `equivalence=UNMEASURED` for this function** for an unrelated reason —
`landing_guard.py` exists at **three byte-identical homes** across three firm trees, so the tool
correctly refuses an equivalence it cannot resolve. **That UNMEASURED is NOT evidence against your
deploy.** (Latent, filed to the channel separately; **not something to fix inside this project.**)

**Live config:** `LastModified 2026-08-20T01:18:32Z` · `CodeSha256 tHeVS53pKxV4hX9UXciJsigvO8t5v10T3CmN2VwQURI=`
· runtime `python3.11` · **1024 MB / 300 s** (already sized — Rule 5 needs no change, confirm it)
· env **`TS_HOLDINGS_ENABLED=1`**, `BRONZE_BUCKET=opal-data-assets`, `ETFS_BUCKET=opal-data-etfs`.
**Trigger:** `cron(0 22 * * ? *)` **ENABLED, FIRED 7× in window** (`comp-trigger`, denominator 136
events-rules + 18 schedules).

> ⛔ **THE DEFECT, STATED PRECISELY: an env var is applied and TRUE for a code path the running package
> does not contain.** Every 22:00Z fire since 2026-08-20 has been a **silent green no-op** for DIVZ and
> IDVZ — and the deployed code **cannot even print the `SKIP:` line**, because the else-branch that
> prints it exists only at HEAD. **This is CLAUDE.md Rule 22a's exact specimen: DESIRED passes, APPLIED
> passes, the scheduled run is GREEN, and all three are true of the wrong bytes.**

> ⛔ **`INGEST-INV-2`, so you do not trust the wrong instrument: the source map's
> `artifact_sha256` for this function is `tHeVS53pKxV4hX…` — EXACTLY the live `CodeSha256`. The map is
> TRUE and it is telling you nothing about code currency.** Do not read a matching source-map hash as
> evidence the deployment is current. Rule 4 says this in its own words; this function is the live proof.

## THE CLOCK — and it is explicitly NOT a licence

The next scheduled fire is **22:00Z tonight**. If it passes on the old bytes it is a **fifth
consecutive lost day** from a **capture-forward source with no backfill** (PRD §2: the derived layer
and the issuer sheets are current-day; an uncaptured day is gone permanently).

> ⛔ **DO NOT COMPRESS A VERIFICATION TO BEAT IT.** `0.0.0_AB_MSTR~Z` put this plainly and the issuer
> adopts it verbatim as part of this TO: ***"If that chain does not close before 22:00Z, THE RIGHT
> OUTCOME IS A FIFTH LOST DAY AND A CORRECT DEPLOY, not a fast one."*** A sixth day costs exactly what
> the fifth did; a wrong deploy on the estate's live issuer-ingest Lambda costs more. **If you cannot
> complete AC1–AC3 properly before 22:00Z, deploy after it.**

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO1-AC1`** | ⛔ **RE-DERIVE BEFORE YOU APPLY, ON THE CORRECTED ORACLE (Z-S4).** Fresh `get-function` → download `Code.Location` → **per member, CRLF-normalize, then compare against (i) `541a393798`** — expect `lambda_function.py` **EQUAL** — **and (ii) HEAD `@4e5800fde0`** — expect **DIFFERENT**, with the call site `:550-559` **ABSENT** deployed and **PRESENT** at HEAD. Report the token census with **positive control `fetch_filepoint` = 3 deployed / 4 HEAD** (⚠ **not 3/3 — an earlier message said 3 in both copies and that is wrong on the HEAD side**) and **negative control `zzz_no_such_token_9999` = 0 both sides**. **A RAW compare here reads DIVERGENT on a perfect deploy — see Z-S4 above.** If your numbers disagree with this TO, **STOP and surface to COO~Z** — do not proceed on either set. | `INGEST-T0-3`, `INGEST-INV-1` | **CODE (Rule 22a)** — the deployed artifact's bytes |
| **`INGEST-TO1-AC2`** | **Terraform only, via `.tools/safe-apply.sh` (NEVER#4 — never bare, and never `aws lambda update-function-code`).** Record: `plan` → `apply` → **re-plan `-detailed-exitcode` rc=0 (0-diff), measured not eyeballed**. **Source map updated** (`infra/aws/lambda/ci/lambda-source-map.json`, Rule 4) — **THREE fields, not one:** `artifact_sha256` = the NEW deployed `CodeSha256`, **and `last_deployed_commit` / `last_deployed_at`, which are STALE TODAY: they read `e45606d461` / `2026-07-15T23:35:40Z` while the measured truth is `541a393798` / `2026-08-20T01:18:32Z`.** ⛔ **The stale field is the one an AE reads to answer "what is running?"; the field that would have caught it (`artifact_sha256`) is current — which is exactly why nothing caught this.** **Confirm memory/timeout stay 1024 MB / 300 s** (Rule 5 — already deliberate; a confirmation, not a change). Tag per Deployment Rule 6. | `INGEST-T0-3`, `INGEST-INV-2` | **DESIRED + APPLIED** |
| **`INGEST-TO1-AC3`** | ⛔ **POST-APPLY: DEPLOYED == BUILT-FROM, PROVEN, NOT ASSUMED — AND NORMALIZED PER MEMBER.** Download the package **again** and show: (a) `lambda_function.py`, **CRLF-normalized**, **== the applied commit's blob** — resolved **through the source map's `files` list (the build input), NEVER by filename guess**; (b) the same for **`landing_guard.py`** (TWO members — a one-member check is a half-check, **and it is the member whose LF-cleanliness is the discriminating control**); (c) `fetch_trueshares_holdings` now **≥3** with the **call site present**; (d) ⛔ **STATE WHETHER THE NEW PACKAGE IS CRLF** — if your build runs on this Windows box it likely is, that is **not a defect**, and saying so is what stops the next verifier re-discovering Z-S4. **This is `INGEST-INV-1`, the invariant this whole project exists because of.** | `INGEST-INV-1`, `INGEST-T0-3` | **CODE** |
| **`INGEST-TO1-AC4`** | ⛔ **EXERCISED, ON THE SCHEDULED FIRE.** After the next **`cron(0 22)` scheduled** run: (a) `s3://opal-data-assets/trueshares/DIVZ/bronze/holdings/{d8}/` and the IDVZ twin are **non-empty** (both read **0 objects** today — that is the discriminating before-state); (b) `s3://opal-data-etfs/silver/holdings/{date}.parquet` **gains DIVZ and IDVZ rows** (today: PFDE 90 / PFOE 24 / **DIVZ 0 / IDVZ 0**, 114 rows total). **An ad-hoc QA invoke is PERMITTED to de-risk and its artifacts are NEVER the evidence here** (CLAUDE.md ad-hoc rule: production numbers come from the scheduled run). **Report which run you are reading and how you know** — a CloudWatch log stream tied to the scheduled invocation, not an inference from an object's existence. | `INGEST-T1-3`, `INGEST-T0-3` | **EXERCISED** |
| **`INGEST-TO1-AC5`** | ⛔ **NO ALARM, NO SNS TOPIC/SUBSCRIPTION, NO SES SEND, NO FRESHNESS CHECKER, NO MONITOR** (standing moratorium, Andrew-direct 2026-07-28). **AND NO SCOPE WIDENING:** do not edit `integrations/bloomberg/pipeline/etf_constituents_pull.py` (C4 ruled the Lambda is the vehicle; the site-Z script's leg 2 **READS** unified silver and never fetches), do not touch `data/**` (Rule 13 — DS's lane), do not "fix" `PATHFINDER_FUNDS` (scope asymmetry is a FIELD, not a defect), and **do not remove or relax any runtime refusal you meet**. Declare the diff you actually landed. | `INGEST-T0-3` | **SOURCE** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-trigger etfs-netassets-daily</run>
      <expect>events-rule ENABLED, schedule `cron(0 22 * * ? *)`, target ARN = the function, with the scan DENOMINATOR printed (136 events-rules + 18 schedules at issuance). Fired-evidence non-zero.</expect>
      <if_mismatch>STOP and surface to COO~Z. A disabled or re-pointed rule changes what AC4 can even mean.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service etfs-netassets-daily</run>
      <expect>The S3 operations against `opal-data-assets` (PutObject for the new `trueshares/{fund}/bronze/holdings/` prefix) and `opal-data-etfs` are visible. **Treat the output as a FLOOR, never a denominator.**</expect>
      <if_mismatch>⛔ **comp-iam models `(action)`, NEVER `(action, resource)` — a role holding `s3:PutObject` on ANY bucket reports GRANTED for every other.** The new bronze prefix is a NEW RESOURCE: verify on the live primitive — `aws iam simulate-principal-policy --policy-source-arn <role> --action-names s3:PutObject --resource-arns <ONE exact key>`, **ONE `--resource-arns` per call**, with the **positive control run as a SEPARATE INVOCATION**. Never use `simulate-principal-policy` to check whether an action NAME is real.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash .tools/commit-gate.sh (on any `.py` you touch — expected: none)</run>
      <expect>PASS. If you touched no `.py`, say so explicitly rather than leaving the row blank.</expect>
      <if_mismatch>STOP. Do not commit a non-compiling or ruff-failing file; `--force` does NOT bypass a gate FAILURE.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>terraform plan -detailed-exitcode (via safe-apply's re-plan), in the OWNING root `infra/aws/terraform/etfs-netassets/`</run>
      <expect>rc=0 — no changes. **Naming the root is load-bearing: running a plan in the wrong root is itself the defect** (round-1 `ETFS-e-4`).</expect>
      <if_mismatch>Do not close the ledger. Surface the residual diff to COO~Z with the plan output.</if_mismatch>
    </step>
    <step>
      <run>re-download the package and re-census (AC3)</run>
      <expect>member sha256 == source at the applied commit, for BOTH members; `fetch_trueshares_holdings` >= 3.</expect>
      <if_mismatch>⛔ The apply reported success and the bytes did not move. That is the F2 class recurring — STOP, surface, roll back per NEVER#6.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). INVOCATION IS POSITIONAL — there is NO --expected-criteria flag; the
       flagged form exits rc=2 and the fallback people reach for (dropping the id argument) returns a
       clean rc=0 that validated COVERAGE NOTHING.
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO1-AC1,INGEST-TO1-AC2,INGEST-TO1-AC3,INGEST-TO1-AC4,INGEST-TO1-AC5
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING — the usage banner contains the vocabulary of BOTH
       verdicts ("Exit 0 = VALID"), so a grep for a success string passes on a call that validated
       nothing. And take the rc WITHOUT A PIPE: `| tail` gives you tail's rc.
       The coverage diff is BIDIRECTIONAL — an expected id with no row refuses the whole instance. -->
  <criterion id="INGEST-TO1-AC1" cell_refs="INGEST-T0-3, INGEST-INV-1"/>
  <criterion id="INGEST-TO1-AC2" cell_refs="INGEST-T0-3, INGEST-INV-2"/>
  <criterion id="INGEST-TO1-AC3" cell_refs="INGEST-INV-1, INGEST-T0-3"/>
  <criterion id="INGEST-TO1-AC4" cell_refs="INGEST-T1-3, INGEST-T0-3"/>
  <criterion id="INGEST-TO1-AC5" cell_refs="INGEST-T0-3"/>
  <expected_criteria>INGEST-TO1-AC1,INGEST-TO1-AC2,INGEST-TO1-AC3,INGEST-TO1-AC4,INGEST-TO1-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_INGEST.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run these at pickup, before anything else (spec-at-pickup currency)

| premise | the one-line read that falsifies it |
|---|---|
| the deployed code lacks the call site | download the package; `fetch_trueshares_holdings` count **< 3** |
| HEAD carries the call site | `grep -n "fetch_trueshares_holdings" infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py` → **3 hits incl. `:552`** |
| the working tree == HEAD for that file | `git diff HEAD -- <file>` → **0 lines** |
| the flag is applied and TRUE | `aws lambda get-function-configuration --function-name etfs-netassets-daily` → `TS_HOLDINGS_ENABLED=1` |
| the bronze holdings prefix is empty | `aws s3 ls s3://opal-data-assets/trueshares/DIVZ/bronze/holdings/ --recursive \| wc -l` → **0** |
| the trigger is live | `comp-trigger etfs-netassets-daily` → ENABLED + `cron(0 22 * * ? *)` |

## Standing constraints

- **NEVER#6 — a begun deploy FINISHES in-session or rolls back loud.** Open a deploy-completion ledger
  entry in `org/critical_paths/change_management/` **at deploy-start**, close it at completion.
  **Unclosed at session end = COO alarm.** If you decide to deploy after 22:00Z, do not open the ledger
  until you start.
- **Never rebase on a shared branch. Commit to your own lane; do NOT push** — push is the integrator's
  (LD-0367). **Report your commit as "landed LOCAL @hash, rides integration", never a bare "landed".**
- **Read the number, then write the sentence** — never compose a report of a completed act in the same
  tool call as the command that produces it.
- **`aws s3 ls` renders LOCAL time with no marker; `s3api`/boto3 render UTC.** Any timestamp you quote
  names its plane.
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), fabric coordinate
  `-Z-S{n}`. **OBSERVATION never interrupts** (one line to CVO~Z, keep working); **BLOCKING** routes
  same-turn to me, cc CVO~Z; **anything ARMED needs a named disarm owner same-turn**;
  **DISARMED ≠ REMEDIATED.** Mid-round the spec is **FROZEN** — route, do not adjudicate.
- **Status moves with the act, by you, in the same turn.** The proof-of-spec instance and the status
  flip are one atomic delivery.

## What this cell closes

Discharging this TO **disarms and remediates `Z-S-A` in one act** (the PRD's own surprise item), fills
the DIVZ/IDVZ books **by construction with zero further code** (`INGEST-T3-2` / `ETFS-TO1-AC3`), and
makes `INGEST-T3-3`'s same-day tie-out **measurable for the first time** — today it is structurally
unmeasurable, because the only issuer row counts in the estate are a 2026-07-31 snapshot being
differenced against an 2026-08-21 Bloomberg count (DECOMP §1.2).
