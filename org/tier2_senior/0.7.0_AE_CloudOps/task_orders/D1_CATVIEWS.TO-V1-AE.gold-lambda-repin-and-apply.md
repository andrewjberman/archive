# TO D1_CATVIEWS.TO-V1-AE — THE GOLD-LAMBDA RE-PIN + TF APPLY, on Andrew's named ship lift

<task_order id="D1_CATVIEWS.TO-V1-AE" project="D1_CATVIEWS">
<id>D1_CATVIEWS.TO-V1-AE.gold-lambda-repin-and-apply</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — `D1-i-2` (**THE LAMBDA RE-PIN + TF APPLY**, AE-CLASS by the cell's own words, "NOT the DS lane's"), with `D1-inv-5` riding every criterion (**COMMITTING IS NOT EXECUTING, and `safe-deploy` to the code channel is not either**). **NO new cell** — this TO executes `D1-i-2` as written.</decomp_ref>
<issued_to>`0.7.0_AE_CloudOps~Z` — seated 2026-08-28T17:09:54Z by `2.0.0_SA_COO~Z` under @b3f9f207da. Rule 27: this lane already holds `D1_CATVIEWS.TO-P1-AE`, SAME project, so this is continuity and not a collision.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T17:1xZ</issued>
<status>pending -- CUT AND SEATED ON AN ANDREW-DIRECT SHIP LIFT. Nothing about this TO is gated on a further sovereign word; AC7 alone is event-gated on a scheduled fire.</status>
</task_order>

<proof_of_spec>
  <criterion id="CATV-TOV1-AC1"/>
  <criterion id="CATV-TOV1-AC2"/>
  <criterion id="CATV-TOV1-AC3"/>
  <criterion id="CATV-TOV1-AC4"/>
  <criterion id="CATV-TOV1-AC5"/>
  <criterion id="CATV-TOV1-AC6"/>
  <criterion id="CATV-TOV1-AC7"/>
  <expected_criteria>CATV-TOV1-AC1,CATV-TOV1-AC2,CATV-TOV1-AC3,CATV-TOV1-AC4,CATV-TOV1-AC5,CATV-TOV1-AC6,CATV-TOV1-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D1_CATVIEWS.TO-V1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 7, all FIRM-TOKENED (`CATV-TOV1-ACn`) at cut time — the id-tokening defect measured on `ETFS_INGEST.TO-8` is avoided by construction. Cells cited: `D1-i-2` (all seven) and `D1-inv-5` (AC3, AC7). **AC7 is EVENT-GATED on a scheduled fire and CANNOT close on the first filing** — file with AC7 OPEN and re-file after the fire; a 6-of-7 instance is the expected first state, not a failure.</alignment_denominators>
</proof_of_spec>

## THE AUTHORITY, AND IT IS THE WHOLE REASON THIS TO EXISTS

**Andrew-direct 2026-08-28 ~17:0xZ at the `2.0.0_SA_COO~Z` terminal, on a 3-card `/open-calls`,
VERBATIM: "all recs approved".** The approved REC for CALL 1 was **SHIP**. Record:
`org/tier1_exec/2.0.0_SA_COO/deliverables/cooZ_ANDREW_DIRECT_20260828_1705Z_SHIP_LIFT_BLOOMBERG_GRANT_D4_READ.md`
@`8d86c930cd`. **READ THAT RECORD BEFORE THE FIRST COMMAND** — it carries two bounds that ride this
work and are not discharged by it.

⛔ **THE NO-SHIP IS LIFTED BY NAME.** `build_package.py`'s interlock states its own release condition:
*"the lift is a named act by COO or Andrew, and no seat has made it."* Andrew has now made it. **You
are not working around the interlock; its condition is met.**

⛔ **TWO BOUNDS THAT CAME WITH THE APPROVAL:**
1. **The blocker sweep was declared NON-EXHAUSTIVE by its own author.** This is "the four known
   blockers are gone", **not** "D1_CATVIEWS is clear." He decided on stated incomplete information.
2. **This ship does NOT make the category-views artifact correct.** It repairs the 49financial SMA
   branch and the `Models` L2 `--` render. A separate defect on the **global** scope is untouched by
   it. **Do not report this deploy as "category-views is now correct."**

⛔ **BOUND 2 WAS RE-WRITTEN 2026-08-28 ~17:2xZ AND THE ORIGINAL WAS WRONG — READ THIS IF YOU READ THE
FACE BEFORE THEN.** It said the ship *"cannot move the global Client **understatement** of
$359,773,356.74 ... global aggregates Client over one firm of three."* **BOTH HALVES ARE RETRACTED**
(`1.0.0_SA_CTO~Z`, which originated the characterisation and then retracted its own). Measured on the
served object: `global.Client` carries `"predicate": "unavailable"` and
`"held_constituents": ["cottonwood"]`. **It never claimed to aggregate** — it declares itself HELD and
names its holder, exactly as `mdpf_gold_consolidator.py:143-160` specifies (`global` has no
`CLIENT_L1_RULE` entry because the three firms' rules differ IN KIND; `client_l1_split('global')`
raises deliberately; it unholds by itself when cottonwood clears). **THE HOLD IS WORKING AS DESIGNED.**
"Understated" implies the node purports to be a complete total; it does not, so the word was wrong
even though the arithmetic was real. The ACTUAL global defect is smaller and two-sided: a **renderer printing the headline
unconditionally** beneath a panel saying that figure is unavailable. ⛔ **A SECOND CORRECTION, 17:3xZ:**
this line briefly also said the `aum` was a residual that *"should be `null`"* — **RETRACTED at
source.** `mdpf_gold_consolidator.py:590/:669/:679` computes it from **global's OWN `non_model_aua`**;
the hold is on the L1 SPLIT (`:748`), not the L0 total. **The `aum` is the part that is RIGHT.**
Neither issue is touched by this deploy, so **the CONCLUSION stands and only the mechanism changed.**
>> **WHY THIS CORRECTION IS ON THE FACE AND NOT ONLY IN A MESSAGE: a message retraction does not
   reach a file.** This TO is the durable carrier an executor and a certifier read. Leaving the
   retracted mechanism here would have it re-derived from my own artifact after everyone had agreed
   it was false. A correction is only as complete as its last surviving carrier. <<

## NEVER-LAW, RIDING EVERY CRITERION

- **`safe-apply` ONLY.** Bare `terraform apply` is a NEVER (mechanically gated).
- **Terraform ONLY.** `aws lambda update-function-code` is a NEVER.
- **A deploy-completion ledger entry in `org/critical_paths/change_management/` OPENS AT START and
  CLOSES AT COMPLETION** (NEVER#6). A confirmed deploy is never left half-landed — finish in-session
  or roll back and escalate loud.
- **`infra/aws/lambda/**` is lane `CLOUD_OPS_OR_ETL`** — your lane. (`1.0.0_SA_CTO~Z` needed an
  audited override for this path at `51bf6208a5`; you do not.)

## THE PIN AND WHAT IT ACTUALLY SHIPS — measured by `1.0.0_SA_CTO~Z` (13511) BEFORE this brief

**THE PIN IS `70a0828226`, AND IT IS NOT A FREE CHOICE.**
`git merge-base --is-ancestor a5227cf161 70a0828226` → **rc=0**, so `70a0828226` (TO-N1-DS) already
CONTAINS `a5227cf161` (TO-M1-DS). **One pin carries both fixes.**
⛔ **THERE IS NO NARROWER OPTION.** A git pin resolves ANCESTRALLY — pinning at `70a0828226` takes
everything up to it. *"Just these two commits"* is not expressible as a pin; it would be a cherry-pick,
which Rule 22a then forces to be resolved by content, and which this file's own interlock warns
against. **The breadth below is INHERENT to the act Andrew approved, not a choice anyone is making badly.**

**DEPLOY EXPOSURE — `git diff --stat bf74d031c1 70a0828226` across the 17 package member paths
(`build_package.py:134-163`): 7 files, 2,521 insertions, 71 deletions.**

```
  mdpf_category_registry.py            1211 ++   <- the module COMING INTO EXISTENCE, not drift
  mdpf_gold_consolidator.py             484 +-
  build_cottonwood_mdpf_pair.py         332 +-
  dim_mdpf_aggregate_aua_timeseries.py  304 +-
  mdpf_aggregate_aua.py                 159 +-
  build_cottonwood_mdpf_slice.py         58 +-
  mdpf_revamp_model_crosswalk.py         44 +-
```

⭐ The **1,211** is `mdpf_category_registry.py` being BORN — it was created `@be05d938af` (2026-08-19),
**after** the current pin `bf74d031c1` (2026-08-10). At the current pin it does not exist, which is
exactly why a bare build refuses. **Shipping it is the POINT of the advance, not a side effect.**
>> **SO THE HONEST DRIFT FIGURE IS THE OTHER SIX: 1,381 lines across 6 modules that have moved in 18
   days and ride along with the two approved fixes. THAT is the number the ledger entry carries.** <<
⚠ **NOT ASSERTED: that any of those 1,381 lines is harmful.** Nobody has reviewed them and no defect
is implied. The point is narrower and it matters: *"the ship fixes the SMA branch and the L2 values"*
is TRUE AND INCOMPLETE as a description of what lands, and a ledger entry written that way would
understate the change it exists to record.
⛔ **THIS IS SIZING, NOT A GATE.** Andrew approved the ship and it proceeds. Do not read this section
as a reason to pause, narrow, or re-confirm.

## ACCEPTANCE CRITERIA

**AC1 `CATV-TOV1-AC1` — THE PIN CARRIES BOTH FIXES.** `cell_refs: D1-i-2`
Build from **`70a0828226`**. Confirm it carries the change at the SOURCE rung:
`git show 70a0828226:data/mdpf/scripts/gold/mdpf_gold_consolidator.py` → `_l0_of` occurrences **>= 3**,
with a **NEGATIVE CONTROL** against the old default `bf74d031c1`, which must read **0**. Without that
control a `>=3` is equally consistent with a broken matcher.
⚠ **A PRECISION, BECAUSE THIS TO'S FIRST DRAFT WAS LOOSE ABOUT IT AND COULD HAVE MISLED THIS SEAT:**
Rule 22a's *"resolve a pin by CONTENT, never by `merge-base --is-ancestor`"* governs **verifying that a
deployed artifact carries a change**. It does **not** forbid `is-ancestor` for **choosing which commit
to pin** — that is a different question about the commit graph, and it is the correct instrument for
it (it is how `1.0.0_SA_CTO~Z` established that one pin suffices). **Two questions, two instruments:
`is-ancestor` selects the pin; CONTENT verifies the artifact (AC3).**

**AC2 `CATV-TOV1-AC2` — DEPLOYED VIA TERRAFORM `safe-apply`.** `cell_refs: D1-i-2`
Plan reviewed before apply; the apply output records added/changed/destroyed. **A `plan` 0-diff is
NOT evidence for AC3** — the cell says so in its own words: *"not `plan 0-diff`, which is true and
silent about code currency."*

**AC3 `CATV-TOV1-AC3` — THE DEPLOYED BYTES CONTAIN THE CHANGE.** `cell_refs: D1-i-2, D1-inv-5`
⭐ **THIS IS THE CRITERION THE CELL EXISTS FOR**, and `1.0.0_SA_CTO~Z` wrote the predicate runnable
(13513) so it is executed rather than derived. **Run all four arms:**

```bash
# A. pull the DEPLOYED package and read the predicate out of it
URL=$(.tools/aws lambda get-function --function-name mdpf-gold-lambda --query 'Code.Location' --output text)
curl -s -o pkg.zip "$URL" && unzip -o -q pkg.zip mdpf_gold_consolidator.py

# B. ASSERTION -- the fix's own function is PRESENT in the running bytes
grep -c '_l0_of' mdpf_gold_consolidator.py                     # EXPECT >= 3   (pre-deploy: 0)
grep -n '_l0_of(member.view_path)' mdpf_gold_consolidator.py   # EXPECT 2 hits, Models and SMA

# C. ** STRUCK 2026-08-28 ~17:4xZ -- THIS ARM WAS UNSATISFIABLE BY ANY CORRECT BUILD. **
#    It read: grep -c 'member.view_path == "SMA"'  # EXPECT 0
#    The DEPLOYED file returns 1 -- and so does the FIXED SOURCE AT THE PIN. The string survives
#    at :547 in a COMMENT documenting the defect that was removed ("was :611 ... EXACT -- brittle").
#    A grep cannot tell code from a comment. DO NOT edit that comment to make this pass:
#    that is fabricating compliance. The arm never discriminated; it is struck, not failed.

# D. POSITIVE CONTROL -- makes B and C mean anything
git show 70a0828226:data/mdpf/scripts/gold/mdpf_gold_consolidator.py > <scratchpad>/fixed_src.py
grep -c '_l0_of' <scratchpad>/fixed_src.py                     # MUST return 3
```

```bash
# ⭐ E. THE PRIMARY CRITERION, and it is stronger than every grep arm combined:
cmp <extracted>/mdpf_gold_consolidator.py <(git show 70a0828226:data/mdpf/scripts/gold/mdpf_gold_consolidator.py)
#    -> IDENTICAL.  MEASURED 2026-08-28 ~17:4xZ by 2.0.0_SA_COO~Z: **IT IS IDENTICAL.**
```
⭐ **BYTE-IDENTITY AGAINST THE BUILD INPUT *IS* WHAT RULE 22a ASKS FOR** — deployed bytes diffed
against the build input, with no pattern standing between the question and the answer. **Score AC3 on
E.** B and D remain as supporting evidence; C is struck.

>> **D IS THE ARM THAT MAKES B MEAN ANYTHING.** Without it,
   "0 hits" at C is equally consistent with a repaired file and a mistyped grep. This estate produced
   four broken-accessor zeros in one day and every one looked like a clean pass. <<
⛔ **A CHANGED `CodeSha256` OR AN ADVANCED `LastModified` IS NOT ACCEPTANCE.** Both are true of ANY
deploy — including one built from the wrong pin, or one where the packager silently dropped a member.
Rule 22a's banked trap applies exactly here: **running-bytes-older-than-built passes every metadata
rung.** A moved sha tells you a package landed; it cannot tell you WHICH.
⚠ **PATH HAZARD, MEASURED TODAY:** do the extract and the read under **ONE path convention, using the
session scratchpad ABSOLUTE path**. MSYS `/tmp` and the literal `/tmp` that native Windows python
resolves to `C:\tmp` are DIFFERENT DIRECTORIES, and `C:\tmp` on this box already holds same-named,
same-shaped files from other actors — **a wrong read there does not fail, it SILENTLY CORROBORATES**
(`3.0.0_SA_CVO~Z` hit this at 13485 s.5).
⛔ `D1-inv-5`: never by filename, never from a commit hash, never from an S3 code-channel upload.

**AC4 `CATV-TOV1-AC4` — SOURCE-MAP ENTRY ADDED.** `cell_refs: D1-i-2` (Deployment Rule 4.)

**AC5 `CATV-TOV1-AC5` — LEDGER ENTRY OPENED AT START AND CLOSED AT COMPLETION, CARRYING THE REAL EXPOSURE.**
`cell_refs: D1-i-2` (NEVER#6.)
The entry must state what actually lands, not what was asked for: **7 files / 2,521 insertions / 71
deletions across the package member list, of which 1,211 is `mdpf_category_registry.py` coming into
existence and 1,381 lines across 6 modules is 18 days of ride-along drift.** An entry saying "ships
the SMA branch fix and the L2 values" is true and understates the change it exists to record.

**AC6 `CATV-TOV1-AC6` — THE LIFT IS RECORDED INSIDE `build_package.py`'s INTERLOCK TEXT.** `cell_refs: D1-i-2`
The interlock is the artifact a future reader opens to learn whether D1_CATVIEWS may ship. It
currently says no seat has made the lift. **That sentence is now false and must not be left standing.**
Record: the lift, its date, Andrew's verbatim, the record's path and commit — and **keep both bounds
above**, because an interlock that records only the permission invites the over-read it exists to
prevent. Comment-only; do not change the `--pin` default as a side effect of this edit (advancing the
default is a separate decision with its own reasoning — surface a rec, do not take it silently).

**AC7 `CATV-TOV1-AC7` — EXERCISED: THE FIRST SCHEDULED FIRE AFTER THE APPLY.** `cell_refs: D1-i-2, D1-inv-5`
⚠ **EVENT-GATED AND CANNOT CLOSE TODAY.**
⛔ **CLOCK CORRECTION, and the defect was the ISSUER'S — caught by `0.7.0_AE_CloudOps~Z` on receipt.**
This criterion first read *"the gold floor fires ~13:00/13:30Z"*, phrased as though that fire were
AHEAD. **It is not: this TO was cut at ~17:1xZ, so today's fire is ~4h PAST.** The acceptance event is
**THE NEXT SCHEDULED FIRE AFTER THE APPLY LANDS**, which is tomorrow's — and that is true regardless,
because AC7 is the SERVED rung and no apply had landed when today's fire ran.
>> **WHY THE CORRECTION IS WORTH A RE-COMMIT ANYWAY:** the act does not change, but a later reader —
   a certifier deciding whether a same-day close was ever available — would compute the wrong wait
   from the original phrasing and could score an OPEN AC7 as a slip. **A stale clock on a durable face
   misleads everyone downstream of it, not just the executor who caught it.** <<
**AC3 IS THE PACKAGE RUNG; AC7 IS THE SERVED RUNG, AND THEY ARE DIFFERENT CLAIMS.** Passing AC3
establishes that the running bytes carry the fix — it does NOT establish that the served artifact is
corrected. On the first scheduled fire after this apply, read
`platinum/mdpf/49financial/category-views.json` and show:

```
  SMA.aum      0.00             ->  22,794,766.25
  Client.aum   290,426,813.47   ->  267,632,047.22
  delta        EXACTLY -/+ 22,794,766.25
  POSITIVE CONTROL: cottonwood and inflection UNMOVED
```

and the false *"NO SMA category members ... A TRUE ZERO"* sentence gone while six SMA members remain
`served: true`. The cottonwood/inflection control is what separates "the fix landed" from "something
else moved the numbers."
⛔ **DO NOT FIRE AN AD-HOC GOLD RUN TO BEAT THE CLOCK.** It would destroy the discriminator the
scheduled run exists to produce — CLAUDE.md's ad-hoc-QA exception does NOT apply here.
**File the instance with AC7 OPEN and re-file after the fire.** Do not hold the whole TO for it.
⚠ **AND IT DOES NOT FIX GLOBAL.** After this lands, the `global` scope still carries its own separate
defect — an **ungated renderer headline** on a Client node the producer declared
`predicate: "unavailable"`, `held_constituents: ["cottonwood"]` — untouched by this deploy. Do
not report AC7 as "category-views is correct."
⚠ **DO NOT EXPECT THAT NODE'S `aum` TO BE NULL OR TO MOVE, AND DO NOT SCORE IT.** Read at source
17:3xZ (`mdpf_gold_consolidator.py:590/:669/:679`): the consolidator computes it correctly from
global's own `ts_doc`; the hold is on the L1 SPLIT (`:748`), not the total — which is why `children`
is `{}` while the figure stands. **The defect is UPSTREAM**: `3.0.0_SA_CVO~Z` measured that global's
`non_model_aua` equals 49financial's to the cent while `global.Models` correctly sums all three in
the SAME object. **This deploy does not touch it, and its value after the fire is not evidence of
anything. RECORD IT, UNSCORED.**
⛔ **DO NOT SCORE `global` AGAINST THE OLD FRAMING.** An earlier version of this face called that node
"understated by $359,773,356.74" and described it as aggregating over one firm of three. **RETRACTED —
see the correction under BOUND 2.** `global.Client` is HELD BY DESIGN and is not claiming to be a
total, so there is no "shortfall" to measure. **Record what the field does; do not grade it against a
number that was never its target.**
⚠ **CONTROL SET FOR THE POST-DEPLOY DIFF IS `cottonwood` + `inflection` ONLY** — read
`3.0.0_SA_CVO~Z`'s baseline README **at HEAD** (path
`org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoZ_D1_PREDEPLOY_BASELINE_20260828/`, vintage
`@4c4f245316`; the earlier `@bc9d11dd8e` carries a SUPERSEDED control set). Path is the locator,
hash is the vintage stamp.

## BARRED AT THIS LANE

⛔ This serial holds **five `disarm_owner` rows in `org/surprise_channel/ETFS_INGEST/`** — a D4
project, outside what you are seated on. **You are barred from acting on them** (Rule 27), and Andrew
has put remaining ETFS/D4 work into a direct channel with `3.0.0_SA_CVO~Z`. If one looks urgent, one
line to `2.0.0_SA_COO~Z`; do not act.
⛔ **D4 IS NOT CLOSED.** Andrew ruled "all signs are indicating to me that D4 is done" is a **READ, not
a close order**. Nothing here stamps it.

## REPORTING

RAVC to `2.0.0_SA_COO~Z`. **Every commit report states its PUSH STATE as a measured value** (on origin
@hash via ls-remote / LOCAL @hash / UNREAD) — push is the integrator's act, route to
`0.0.0_AB_MSTR~Z`. **Never compose the report of a completed act in the same tool call as the act** —
read the number, then write the sentence. Off-task findings go to the surprise channel one line and
**you keep working**.
