# TO ETFS_POSITIONING.TO-2 — the ETF SERVING plane: ROUTE decision, ARTIFACT CONTRACT, IAM

<task_order id="ETFS_POSITIONING.TO-2" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cells ETFS-e-1, ETFS-e-2, ETFS-e-3 (constrained by ETFS-a-8 / boundary (h))</decomp_ref>
<certification>⛔ **UNCERTIFIED DECOMP.** Cut before `3.0.0_SA_CVO` certified the stage-3 decomp, under Andrew's 19:3xZ priority word and CTO's explicit instruction to cut UNCERTIFIED-on-face rather than idle a seat. Permitted, disclosed by the issuer, never silent.</certification>
<issued_to>AE-class (serving / route / IAM). Seated: `0.7.0_AE_CloudOps` — seated 19:45Z, reading plane (e), reported at 65608.</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED NOW. Class dark mid-execution → spawn call routes to MSTR SAME-TURN.</seating_trigger>
<placement>LAPTOP (Rule 26).</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T19:55Z</issued>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_POSITIONING_TO1_TO2_TO3_TO5_CERTIFICATION_20260828.md` @`e3d86ad9d1`, verdict **CERTIFIED -- 7 PASS + 1 RETIRED-UNREACHABLE**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**</status>
<priority>P1 — SESSION PRIORITY (Andrew-direct 19:3xZ). ⛔ **This TO's Half 1 is the CRITICAL PATH JOIN: both DS (TO-1) and DE (TO-3) build against the contract you produce.** Ship Half 1 FIRST and ship it as a one-page contract — do not batch it behind IAM.</priority>
<authority>PRD s.11.4(e) + s.11.1 (Models mode byte-identical) + s.11.5. CLAUDE.md Rule 17b (serving is its own tier), Rule 22a (verification layer), NEVER#3 (never-widen on served output).</authority>
<proof_of_spec>
  <!-- ISSUANCE half (COO, at decomposition): the machine-readable criterion-id set.
       Ids are FIRM-TOKENED so they cannot collide across the three parallel ETFS lanes.
       CELL_REFS ARE THE POINT: 3.0.0_SA_CVO's bidirectional alignment check is a JOIN on
       these, not a prose read -- every criterion names the decomp cell it discharges, and
       every criterion-bearing cell is reachable from some criterion. A criterion arriving
       WITHOUT cell_refs is REFUSED, never retrofitted: a retrofitted derivation makes
       alignment LOOK satisfied while being FALSE, and CVO confirmed they would have
       computed exactly that as PASSING.
       COMPLETION half (assignee, from their OWN efforts): a schema-valid instance at the
       path below, validated BEFORE the status flip.
       INVOCATION IS POSITIONAL -- there is NO --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO2-AC1,ETFS-TO2-AC2,ETFS-TO2-AC3,ETFS-TO2-AC4,ETFS-TO2-AC5,ETFS-TO2-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING. The usage banner contains the vocabulary of
       BOTH verdicts ("Exit 0 = VALID"), so a caller grepping for success matches the banner
       of a call that validated NOTHING. rc=0 VALID / rc=1 INVALID / rc=2 usage. And the
       2-arg form (id set omitted) returns a clean rc=0 that says COVERAGE UNCHECKED -- pass
       the ids. -->
    <criterion id="ETFS-TO2-AC1" cell_refs="ETFS-e-1"/>
    <criterion id="ETFS-TO2-AC2" cell_refs="ETFS-e-2"/>
    <criterion id="ETFS-TO2-AC3" cell_refs="ETFS-e-2, ETFS-f-3"/>
    <criterion id="ETFS-TO2-AC4" cell_refs="ETFS-e-3, ETFS-e-4"/>
    <criterion id="ETFS-TO2-AC5" cell_refs="ETFS-e-1"/>
    <criterion id="ETFS-TO2-AC6" cell_refs="ETFS-a-8"/>
    <criterion id="ETFS-TO2-AC7" cell_refs="ETFS-e-4"/>
    <criterion id="ETFS-TO2-AC8" cell_refs="ETFS-e-5"/>
  <expected_criteria>ETFS-TO2-AC1,ETFS-TO2-AC2,ETFS-TO2-AC3,ETFS-TO2-AC4,ETFS-TO2-AC5,ETFS-TO2-AC6,ETFS-TO2-AC7,ETFS-TO2-AC8</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## ⛔ YOUR READ WAS CORRECT AND THIS TO NARROWS IT — you asked to be corrected if (e) were scoped differently

You asked (65608) whether the (e) scope matched your read. **It does. And the decomp REMOVES one of your three candidates before you spend a turn on it.**

### THE CONSTRAINT — `opal-data-etfs/platinum/` IS OUT

PRD s.11.4(e) framed the route as a decomp decision between `/api/general/positioning/*` and `opal-data-etfs/platinum/`. **The second is not a free choice.** Measured live this run:

`s3://opal-data-etfs/platinum/etf_ownership_dashboard.json` — **6,408 B, rewritten 2026-08-21T16:00:04Z (TODAY)**. Source-confirmed, not inferred: `infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/lambda_function.py:37` (`PLATINUM_KEY` default `"platinum/etf_ownership_dashboard.json"`) and `:81` (*"AE-owned production write"*).

**It fails on two independent grounds, either alone decisive:**
1. **It is ETFS_CANON's LIVE serving root** — and ETFS_CANON is PRD s.11.4(h), the declared **OUT OF SCOPE** sibling. Writing there puts round-1 inside a sibling's territory; moving/colliding with served output is **NEVER#3**.
2. **Rule 17b** — serving lives in `opal-data-portal-v2/platinum/`, not a data bucket's `platinum/`. *(That `opal-data-etfs/platinum/` is itself non-canonical is a PRE-EXISTING ETFS_CANON condition — **surfaced, NOT chased**. Rule 17b's ratified-direction clause: a non-conforming tree is not a violation and not a warrant to move anything. **Do not remediate it.**)*

**So Half 1 decides between TWO candidates, not three.**

## ⛔ COO RULING — THE ARTIFACT IS SEPARATE, NOT MERGED. Decided here so you and DE and DS do not each decide it differently.

DE measured (65652) that `getPositioningData` returns **`portfolios: Record<string, PositioningPortfolio>`** — **keyed by arbitrary string, not a closed enum** (`portal/src/api/portal-proxy.ts:1085`). So the existing artifact's *type* would permit ETF keys being added to `positioning_data.json`. **DE was right to surface it. I am ruling AGAINST taking it, and the reason binds your design:**

- **PRD s.11.1 makes "Models mode BYTE-IDENTICAL" a sovereign constraint.** Adding ETF keys to the artifact Models mode reads makes byte-identity a property maintained **by discipline**. A separate artifact makes it true **BY CONSTRUCTION**. ⛔ **CARE IS NOT A CONTROL. CARE IS WHAT YOU HAVE INSTEAD OF ONE.**
- **It would put TWO producers on ONE served key.** The estate's one-producer-per-served-key property (Rule 17b's amendment holds it *by construction*) would be broken deliberately, on a **live client-facing page**.
- **Blast radius:** a producer bug would degrade the **live Models** page, not just the new ETF mode.

**THE RULING: ETF positioning serves from its OWN artifact. `positioning_data.json` is NOT WRITTEN BY THIS PROJECT.** *(DE's corollary still stands and is TO-3's: the portal derives ORDER from its own lists, so the positional coupling is portal-internal and the artifact can neither break nor fix it.)*

## ⛔ SPEC-AT-PICKUP — first act, before any design

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | `/api/general/positioning/` already serves FOUR keys | `grep -n "api/general/positioning" portal/src/api/portal-proxy.ts` → `positioning_data.json`, `model.json`, `allocation_summary.json`, `holdings_attribution_data.json` |
| O-2 | ETFS_CANON's platinum artifact is LIVE | `aws s3 ls s3://opal-data-etfs/platinum/` → mtime today |
| O-3 | Whether an ETF path class exists on the portal-v2 distribution or is a **MINT** | `comp-routes behaviors` — **read its provenance header; it is DESIRED plane by its own header** |

## Half 1 — `ETFS-e-1` + `ETFS-e-2`: THE ROUTE + THE CONTRACT ⭐ SHIP THIS FIRST

**Decide the route** between the two surviving candidates, **with `comp-routes` evidence** (PRD s.11.4(e) requires it), and **publish the artifact CONTRACT as a one-pager**: key/prefix, the s.4 rectangle shape, the four book keys, how the two SHELLS are represented, and the freshness/as-of field.

**⭐ THE CONTRACT IS THE JOIN POINT OF THE WHOLE PROJECT.** DS builds the producer against it (TO-1) and DE builds the portal reader against it (TO-3), **in parallel, without waiting for the artifact to exist**. That parallelism is what makes "DONE RIGHT NOW" reachable. **Ship the contract as soon as it is decided — a paragraph and a JSON skeleton beats a polished document an hour later.**

**Carry this limitation into the contract (decomp L-3):** publish-layer S3 keys are the **~11% generative class** — only ~11% of in-scope key call sites NAME their key (1 of 112 in the publish/serving layer). **A token census will not find your consumers. Do not rest the contract on one.**

## Half 2 — `ETFS-e-3`: IAM

Reader/writer pair for the chosen prefix. **You stated this discipline unprompted at 65608 and it is recorded here so it binds the CELL, not the seat:**

- **`comp-iam` is a FLOOR, never a verdict** — it models `(action)`, never `(action, resource)`. A role holding `s3:GetObject` on ANY bucket reports `[GRANTED]` for a call to EVERY other. **Treat its operation list as a floor; SILENCE IS THE DEFECT, and never read it as a deletion warrant.**
- A **NEW prefix** is verified on the live primitive: `aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action> --resource-arns <ONE exact key>`.
- ⛔ **ONE `--resource-arns` PER CALL** — 2+ flips the held ones to `implicitDeny`.
- ⛔ **The positive control runs as a SEPARATE INVOCATION** — mode (1) silently disarms the very control you are leaning on. *A positive control is only a control if it runs in isolation from the target.*
- ⛔ **NEVER use `simulate-principal-policy` to check whether an action NAME is real** — a nonexistent action returns `implicitDeny`, **indistinguishable from a missing grant**, and sends you hunting a policy gap that does not exist. The discriminating oracle is `aws accessanalyzer validate-policy`.
- Pass `--context-entries` for any conditioned statement (no context → `implicitDeny`, byte-identical to a real deny).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO2-AC1** | Route DECIDED between the two surviving candidates, **with `comp-routes` evidence cited** and the provenance header read | `ETFS-e-1` | DESIRED + APPLIED |
| **ETFS-TO2-AC2** | ⭐ **CONTRACT PUBLISHED** — key/prefix, s.4 shape, four books, shell representation, as-of field. Sent to DS + DE the turn it exists | `ETFS-e-2` | DECLARATIVE |
| **ETFS-TO2-AC3** | Contract states **explicitly** that `positioning_data.json` is NOT written by this project and Models-mode bytes are untouched | `ETFS-e-2`, `ETFS-f-3` | DECLARATIVE |
| **ETFS-TO2-AC4** | IAM delta named: what is granted, what a NEW prefix needs — on the **live primitive**, ONE `--resource-arns` per call, positive control in a SEPARATE invocation | `ETFS-e-3` | APPLIED |
| **ETFS-TO2-AC5** | If a CF path class is a **MINT**, say so plainly (mint ≠ gap) | `ETFS-e-1` | APPLIED |
| **ETFS-TO2-AC6** | **NO write, move, or delete touches `opal-data-etfs/platinum/`** or any ETFS_CANON artifact | `ETFS-a-8` | APPLIED |

## Your two queued items — ordering CONFIRMED, neither dropped

You proposed ordering both behind the ETF read. **Confirmed, and your reasoning was right:** P4I-3 executes nothing either way (the flip it serves is held on both of Andrew's conditions), and the 04:00Z producer census blocks no one. **Both stay yours, neither is dropped, both are AFTER this TO.** No further ask needed from you on either.

## Surprise channel · Reporting

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts** (one line, keep working); **BLOCKING** routes same-turn to me, cc CVO; **ARMED** needs a named disarm owner same-turn, and DISARMED ≠ REMEDIATED. **Mid-round the spec is FROZEN.**
**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN.** Status is CELL-level — `ETFS-e-1`, `-e-2`, `-e-3` complete independently.
**EVERY REPORT OF A COMMIT STATES ITS PUSH STATE** — never bare "landed."
⛔ **Never compose a report of a completed act in the same tool call as the command that produces it.**

---

## ⛔ AMENDMENT A (issuer, 2026-08-21T20:0xZ) — YOUR READ ARRIVED FIRST. `ETFS-e-1` IS RULED: YOUR RECOMMENDATION, ADOPTED.

Your 65661 landed **before this TO reached you** and answered `ETFS-e-1` with live evidence and a
recommendation. **Leaving the decision open would make DS build a producer against an undecided target, so the
decomp owner ratifies rather than waits. Three lanes, one voice.**

### RULED: **`platinum/etfs/` on `opal-data-portal-v2`, mdpf-shaped.** Your recommendation, adopted as written.

**The deciding fact was YOURS and it is the counter-intuitive one — the NEVER#3 INVERSION:** landing under
`json/positioning/` is an **existing prefix with LIVE Models consumers**, so it is **MORE** never-widen-exposed,
not less. **The "free" option is the one that touches a live serve** — on Andrew's top-priority page. That
reframes the whole cost table, and I would not have had it without the live read.

Reinforcing, also yours: there **is no `/api/general/positioning/*` behavior** — Positioning rides the
catch-all to `/json/`, so "the existing family" is a **legacy tree**, not a canonical home. Plus Rule 17b's
amendment (publisher reads parquet, publisher is the only JSON producer) makes a `json/`-landing producer
perpetuate the shape 17b retires. Andrew's standing rule closes it: *do it correctly the first time and port
over.*

**`ETFS-TO2-AC1` IS THEREFORE DISCHARGED AT ISSUE.** Record it in your proof-of-spec with your 65661 evidence
— route decided, `comp-routes` evidence cited, provenance header read. **Do not re-litigate it; spend the turn
on the contract and the IAM.**

### `ETFS-e-3` IS NO LONGER DARK — it is a NAMED ACT

Add `arn:aws:s3:::opal-data-portal-v2/platinum/etfs/*` to `AllowCloudFrontOACPublicData` (the live three-statement
policy you read; `platinum/advi/*` needing its own statement is the confirming precedent). ⛔ **Without it CF
returns 403 AND the CF error rules MASK JSON errors as HTML — so it fails as a CONFUSING HTML 403, not a clean
one. That masking is exactly why `ETFS-TO2-AC4` must be EXERCISED, never config-read.**

**Your own note is adopted into the criteria:** superseded TO-D4d's `D4d-2 "EXERCISED FETCH"` had it right —
**an exercised fetch of the ETF path carries forward as the discharge of `ETFS-TO2-AC5`**, since you correctly
flagged that nothing in your read is EXERCISED (no ETF path exists to fetch yet).

### ⛔ AMENDMENT B — YOUR STALE-RECORD FIND IS CLASSED **ARMED**, AND YOU ARE THE DISARM OWNER

`infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf:46-48` — *"measured 2026-07-28: 2 statements"*. The
zero-Denys half stands; the **count and scope are 24 days stale**.

**Class OBSERVATION · standing ARMED · disarm owner `0.7.0_AE_CloudOps` (you measured it) · SAME-TURN.**
ARMED because **a seat inheriting that header concludes a new platinum prefix is CloudFront-readable — it is
not** — and the failure it produces is the masked HTML 403, which reads as a *routing* bug rather than a
*policy* gap and sends the next seat at the wrong layer.

**Disarm = correct the comment to the measured three-statement, prefix-scoped truth. One line, cheap, now.**
**DISARMED ≠ REMEDIATED** — two states, two clocks. File both to CVO.

*Note this is a comment correction inside a TF file, not a policy change — it does not touch the applied plane
and needs no apply.*

**Nothing else in this TO changes.** The separate-artifact ruling, the contract-first sequencing (still the
critical-path join), and your IAM method all stand as written.

---

## ⛔ AMENDMENT C (issuer, 2026-08-21T20:2xZ) — **OPTION (A) RULED.** The advi statement is restored to code **IN THE SAME EDIT** as the etfs ARN. One edit, one reviewable act, ONE apply.

**AE routed a BLOCKING × ARMED surprise (65720) rather than writing an off-spec fix on their own authority.
That is the protocol working exactly as designed** — mid-round the spec is frozen for the *executing* seat, and
the amendment is the *issuer's* act. **This is that amendment.**

### RULED: **(A).** TO-2 Half 2 now includes restoring `AllowAdvisorRouterOAIPlatinumAdvi` to `s3-portal-v2-import.tf`.

**Why (A) and not (B) — the reason is the resource's own semantics, not convenience:**

1. ⛔ **`aws_s3_bucket_policy` is FULL-REPLACE (`PutBucketPolicy`).** Option (B) means **TWO applies against one
   live bucket policy**, and every apply on a full-replace resource is another chance to write the wrong
   statement set. **On a live serving resource, fewer applies is the safer direction, not the more casual one.**
2. **Option (B) serializes Half 2 behind a second TO for no safety gain** — and the two edits touch the *same
   declaration block*, so splitting them creates a window in which the file is half-correct.
3. **The drift was discovered by, and is inseparable from, this cell.** Handing it to a different TO would
   separate the finding from the seat holding the live measurement.

### THIS WIDENS NOTHING, AND THE DISTINCTION IS LOAD-BEARING

**Restoring `AllowAdvisorRouterOAIPlatinumAdvi` to code is not a grant, not a widening, and not a new serve.**
The grant is **ALREADY LIVE**, **ALREADY CO-SIGNED** (COO's half is in the P4R-3 paper), and **already serving
traffic**. Codifying it **narrows the gap between code and reality** — it changes the *record*, not the
*permission*. ⛔ **The dangerous act here is NOT codifying it; the dangerous act is applying without it.**

**And to be explicit, because I will not manufacture one:** the apply freeze AE declared is a **HAZARD DISARM,
not an approval gate.** No seat needs anyone's permission to work; one specific destructive act is fenced until
its precondition is in code. That is a control, not a choke point.

### ACCEPTANCE — `ETFS-TO2-AC4` gains a second half, and `ETFS-TO2-AC7` is MINTED

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO2-AC4** *(extended)* | The etfs ARN is added **AND** `AllowAdvisorRouterOAIPlatinumAdvi` is restored, **in ONE edit, ONE `safe-apply`**. Post-apply re-plan **IN `shared-infra`** reads **0-diff** — and **state the root you ran it in**, since running it in the wrong root is the defect being remediated | `ETFS-e-3` | APPLIED |
| **ETFS-TO2-AC7** *(NEW)* | ⛔ **THE ADVI ROUTE STILL SERVES AFTER THE APPLY — proven by an EXERCISED FETCH through the auth path, not a policy read.** Plus a live `get-bucket-policy` showing **THREE** statements | `ETFS-e-3` | **EXERCISED** |

⛔ **`ETFS-TO2-AC7` IS THE WHOLE POINT AND IS NOT CEREMONY.** The failure mode is *"the apply silently removed a
live read grant."* **A policy read after the apply would show what we just wrote and tell us nothing about
whether ADVI still serves.** Only fetching the route exercises it. **And a 403 here would arrive dressed as
HTML by the CF error rules** — so the check must assert the **body/status of a successful fetch**, never merely
"a response came back."

**Sequence it so the blast radius is observable:** capture the exercised advi fetch **BEFORE** the apply as
well, so a post-apply failure is attributable to the apply rather than to a pre-existing condition.

### THE CLASS THIS BELONGS TO — recorded because it will recur, and it is not AE's carelessness

AE's own P4R-3 close was **rigorous**: live-primitive read-back of all three statements, mutation-tested router
controls, an exercised fetch, deployed bytes hashed. **Every control fired correctly and every one of them was
about the WRONG PLANE.** A grant applied **out-of-band** is **structurally invisible to a plan you never run**,
and the re-plan that read *"No changes"* was in a root that **does not own the bucket policy**.

**That is CLAUDE.md's designed-half verbatim: *no control inside the wrong plane can catch a wrong-plane
error.*** *(AE labelled the "which root" part an INFERENCE and it stays labelled — the measured facts are the
pending change and the absent TF resource; which root the prior re-plan ran in is reasoned, not read.)*

**The transferable rule, and it is worth more than this fix: A LIVE-PRIMITIVE GRANT WITHOUT A CORRESPONDING
TERRAFORM RESOURCE IS A DELETION SCHEDULED FOR WHENEVER SOMEONE NEXT APPLIES THAT ROOT.** It reads perfectly
healthy on every APPLIED-plane check — which is exactly why nobody finds it until the apply.

### PROCEED

Half 2 is **UNHELD** on my side the moment you read this. CTO holds the other never-widen half and I have told
them my reading; **that is theirs to raise, not a hold you wait on.** Your read-only queued items were the right
way to spend the wait.


---

## ⛔ AMENDMENT D (issuer, 2026-08-21T20:2xZ) — **AE'S EDGE-PIN CORRECTION ACCEPTED. `ETFS-TO2-AC4` WAS INSUFFICIENT AND, WORSE, MISLEADING. `ETFS-TO2-AC8` MINTED.**

AE self-corrected a load-bearing sentence (65735) **in the direction that would have shipped a silently
non-working route.** Accepted in full. **The correction lands on MY criterion, not only on their contract.**

### THE FINDING

`infra/aws/terraform/portal-auth/lambda-edge.tf:197` — `public_data_router` carries
`ignore_changes = [qualified_arn, source_code_hash]`. That file's own header `:36-37`: ***"Apply publishes a
NEW Lambda version and CloudFront KEEPS SERVING THE OLD ONE."***

**So adding the `/api/general/etfs/` branch and applying would have published a new version while the
distribution kept serving the old one — the ETF URL 404ing into the `json/` fallback, silently, with
everything green.**

### ⛔ WHY THIS BREAKS MY OWN `ETFS-TO2-AC4`, AND I AM CORRECTING IT RATHER THAN LAYERING ON IT

Amendment C's `ETFS-TO2-AC4` required a **0-diff re-plan in `shared-infra`**. Against the bucket-policy drift
that is the right instrument. **Against the edge pin it is the SYMPTOM, not the reassurance** — the pin's whole
behaviour is to produce a clean plan and a genuine 0-diff re-plan while the edge never moved.

**`lambda-edge.tf:39-47` states it outright: the pin passes EVERY RUNG OF RULE 22a AT ONCE — DESIRED (clean
plan AND genuine 0-diff re-plan), APPLIED (a new version really was published; `get-function-configuration` is
true), EXERCISED (the route runs GREEN — on the OLD code).** An acceptance criterion resting on 0-diff would
therefore have **certified a broken route with a true statement.**

### `ETFS-TO2-AC8` — MINTED (the instrument that actually discriminates)

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO2-AC8** | ⛔ **READ THE LIVE DISTRIBUTION'S LAMBDA ASSOCIATION ARN AFTER APPLY** and confirm its version equals the newly published `public-data-router` version. Per `lambda-edge.tf:42-43` this is ***"the ONLY instrument that catches it, and it is not a rung anyone runs by habit."*** **A 0-diff re-plan DOES NOT DISCHARGE THIS** | `ETFS-e-5` | **APPLIED (live distribution read)** |

**`ETFS-TO2-AC4` AMENDED:** the 0-diff re-plan remains required **for the bucket-policy drift (`ETFS-e-4`)**
and is **explicitly NOT evidence about the edge association.** State the root; state that AC8 carries the edge.

### THE MINT IS **THREE** EDITS, IN ONE COMMIT

1. `public-data-router` branch `/api/general/etfs/` → `/platinum/etfs/`
2. the bucket-policy ARN for `platinum/etfs/*` **+ the advi restore** (Amendment C)
3. **NEW:** drop `qualified_arn` from `public_data_router`'s `ignore_changes` at `lambda-edge.tf:197` —
   the remedy the file itself prescribes at `:54-58`, and the way `shared_advisor_router` was already fixed.

⛔ **DO NOT BUNDLE THE OTHER TWO PINS.** `auth-validator-edge:96` and `cache-control-injector:151` stay
untouched — AE is right, and `lambda-edge.tf:52` explicitly warns against exactly that bundling. **Zero current
drift on both; an unrelated fix riding a live-serving apply is how a clean change becomes an incident.**

### THE PART I WANT ON THE RECORD, BECAUSE IT IS NOT A SCOLDING

AE cited `comp-routes edge-versions` reporting `[OK] DYNAMIC` as proof the edge would move. **The file
documenting that the tool lies about precisely this was written TODAY, by AE's own lane, out of P4R-3** — and
`:44-47` says it in terms: *"`comp-routes edge-versions` does NOT catch it… DO NOT READ THAT [OK] AS EVIDENCE
AN EDGE MOVED."*

**This is not a tool defect and not carelessness. It is the estate's own hardest lesson: a documented blind
spot protects nobody who does not read the documentation for the surface they are standing on.** The
`[OK]`-reporting-backwards drift was already routed to CTO as declarative drift and **that routing is still
OPEN — AE's error is a live instance of the cost of leaving it open.** *An instrument that reports a pinned
function as `DYNAMIC [OK]` is not merely unhelpful; it asserts the opposite of the truth, which is the one
failure a careful reader cannot defend against.*

### UNCHANGED — DS AND DE KEEP BUILDING

Route decision, key, URL, shape, `holdings_status`, the vocabulary boundary, `ETFS-TO2-AC3`: **all unchanged.**
This corrects **HOW THE MINT LANDS**, not what is being built. **Nothing for DS or DE here.**
