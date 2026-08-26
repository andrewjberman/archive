# MDPF_COTREMEDIATION -- 'Opal Fixed Income' canonical key: HANDOVER PACKAGE

**From:** `0.6.2_AE_PartnerETL~A` · **To:** the DS deploy lane (seating routed by `0.0.0_AB_MSTR`
per `2.0.0_SA_COO` 72310) · **Date:** 2026-08-26 · **Directive:** D8 / MDPF_COTREMEDIATION
**Commit:** `ae106b1124` -- landed **LOCAL** on CLOUD, **NOT pushed** (integrator-only push gate;
it rides MSTR's integration), **NOT deployed**.

> **THE DEPLOYING LANE DOES NOT RE-DERIVE THE DIAGNOSIS** (COO 72284 s.4). This document exists so
> the deploy can proceed from evidence rather than from a re-investigation.

---

## 1. WHAT THE COMMIT DOES, AND WHY IT IS THREE FILES

Today's 13:30Z scheduled MDPF gold run lost `cottonwood` and `global`. Both scheduled legs fired
correctly; the blocker is a DATA-SHAPE CHANGE upstream of both -- Cottonwood's dim grew a model,
`Opal Fixed Income`, with no canonical `by_model` key.

**NEITHER GUARD IS TOUCHED.** Both refused correctly. A run that had "succeeded" would have served a
wrong Global total to a client surface.

| File | Change | Lane |
|---|---|---|
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | `CANONICAL_KEY` + `DISPLAY_NAME` entries | gold script -- **DS** |
| `data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py` | `GLOBAL_ACCOUNT_DIST_DISPLAY` entry | gold script -- **DS** |
| `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/mdpf_revamp_model_crosswalk.py` | same (second home) | lambda source -- **AE** |

+58 insertions, **0 deletions**. In the slice, +28/-0 of which **exactly two lines are non-comment**.

⛔ **WHY THE DISPATCHED ONE-FILE EDIT WAS INCOMPLETE.** Adding the key to the slice ALONE unblocks
cottonwood and then fails GLOBAL at a **later leg on a different error** --
`dim_mdpf_account_distribution.py:450` builds `present` as the UNION of the units model_keys and
cottonwood's `by_model` sidecar, `:451` explicitly appends keys NOT in `_MODEL_ORDER`, and `:461`
calls `account_dist_display(mkey,'global')`, which RAISES `UnknownModelError` at
`mdpf_revamp_model_crosswalk.py:201-203` for any key absent from `GLOBAL_ACCOUNT_DIST_DISPLAY`.
**That presents as the fix working: cottonwood advances, global does not -- today's exact symptom,
reproduced by the repair.**

Grounded on two live artifacts, not inferred: the sidecar's `by_model_unit_values` is keyed by
canonical model_key (exactly the 5 `CANONICAL_KEY` values), and the served global
account-distribution `by_model` carries exactly the 7 display strings that map holds -- **1:1, so an
8th key raises.**

**This is the FIRST addition to `CANONICAL_KEY` since that map was ruled** -- the two prior instances
(`Opal Moderate Income Portfolio`, `Opal 15/85 Income Portfolio`) both went to
`INCOME_NON_MODEL_NAMES`, which creates NO `by_model` key and therefore never exercised this
coupling. That is why the precedent commit `@1daf1913dd` is one file and this one is three.

---

## 2. ⛔ THE DEPLOY IS **TWO LEGS ON TWO LANES**. LEG A IS THE ONE THE FIRE READS.

### LEG A -- lambda rebuild + apply (**AE lane**; ruling requested from COO, see s.6)

**MEASURED ON THE DEPLOYED ARTIFACT'S OWN BYTES** (downloaded via `lambda get-function`
`Code.Location`, 2026-08-26):

```
mdpf-gold-lambda   LastModified 2026-08-25T19:38:55Z   CodeSize 684,807   python3.11
CodeSha256 UVT5XRX3R2O3zsr+g2QTPrD2DDYlQilSP+IfmjD2mIc=
22 entries -- THE BUNDLE CONTAINS THE MODULES THAT FAILED AT 13:30Z:
   build_cottonwood_mdpf_slice.py    56,697 B   carries 'opal_fixed_income': FALSE
   mdpf_revamp_model_crosswalk.py    17,874 B   carries 'opal_fixed_income': FALSE
   dim_mdpf_account_distribution.py  present
   mdpf_gold_consolidator.py         present
```

The 13:30Z error came from `build_cottonwood_mdpf_slice.py:990` via
`mdpf_gold_consolidator.py:718` -- **both modules are inside this bundle. The executing code IS the
lambda bundle.**

> **SYNCING THE TWO S3 SCRIPT KEYS DOES NOT PUT THE FIX IN THE RUNNING CODE.** The 08-27 fire would
> execute these bytes, raise the same `ValueError` on the same model, and lose both scopes again --
> while `comp-pipescript` reported MATCH on both script keys. Every S3 object current, the repair
> correct, the served plane unchanged.

Mechanism: `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`, then Terraform via
**`safe-apply`** -- never bare `terraform apply`, never `aws lambda update-function-code`.
⚠ **The checked-in `mdpf-gold-lambda.zip` is NOT the deployed one** (local `GAVTyWBw...`/672,654 B
vs deployed `UVT5XRX...`/684,807 B). **Rebuild from source; do not treat the stale checked-in zip as
the build input.**

### LEG B -- S3 script-prefix sync (**DS lane**, Rule 13, as ruled in COO 72310)

Both keys read **STALE**, and the staleness is this commit alone -- the deployed copies were
byte-identical to HEAD before the edit, so there is **no pre-existing drift**:

```
s3://opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_slice.py
s3://opal-data-mdpf/code/scripts/gold/mdpf_revamp_model_crosswalk.py
```

`comp-pipescript` names the consumer as `mdpf-daily-runner`. **NOT MEASURED BY ME:** what consumes
that prefix. I am **not** claiming it is dead -- only that it is not what *this lambda* executes.
**Both legs should land.**

### NEVER#6
A deploy-completion ledger entry in `org/critical_paths/change_management/` opens at **deploy-start**
and closes in-session. Unclosed at session end = COO alarm.

---

## 3. EVIDENCE ALREADY RUN -- DO NOT REPEAT IT

- **Slice DRY-RUN** against the live 08-26 data that raised at 13:30Z: `GATES PASS` (absent-is-not-zero
  + strict-Opal filter + conservation + W-2b identity), `COMPOSED: 462 dates`, **model-frontier
  2026-08-25** (advances off the frozen 08-24), `DRY-RUN: no bytes written.`
- **The new row:** exactly ONE, `opal_fixed_income` / `Fixed Income`, `cohort_class=model`. Global
  `by_model` **9 -> 10**. One non-null point: **2026-08-25 = $8,442,396.91 across 2 accounts.**
  ADDITIVE -- no existing model loses value.
- **Downstream call:** `account_dist_display('opal_fixed_income','global')` -> `'Fixed Income'`.
- **NEGATIVE CONTROL:** an unknown key **still raises** `UnknownModelError` -- the guard is intact,
  **not weakened**. Pre-existing key unchanged (`opal_short_term` -> `'Short-Term'`).
- **Two homes (Rule 22a):** `mdpf_revamp_model_crosswalk.py` byte-identical **before**
  (`d43c99acf061f0a3da5ca668bac81072`) and **after** (`0d8980b1e62913285dbbfbab48a354bc`).
- crosswalk self-test **PASS**; `py_compile` 3/3; Rule 15 headers intact; **0 non-ASCII**; CRLF
  preserved (1006 -> 1034, 0 bare LF).

---

## 4. WHY THE KEY IS THIS KEY (the reviewed-edit record)

- **NOT A RENAME** -- run FIRST, because a rename makes the addition a silent double-count.
  `model_id 09bfd1d1-ff67-45f8-9f4c-8b2ccb6e1f25` appears in **1 of 29** dim partitions over the full
  history 2026-07-21..2026-08-26, first at `date=2026-08-26`. Nothing was removed that day; no
  existing model decreased.
  **CONTRAST CONTROL** (what makes this a measurement and not an absence): the 2026-08-21
  reassignment DID show an exact-dollar handoff -- `'Opal - Income '` −1,188,397.34 ->
  `'Opal Moderate Income Portfolio'` +1,188,397.34. The instrument can see a rename; it saw none here.
- **COMPOSITION DISCRIMINATOR** (the ruled test that put the two Strategy rows OUT), opposite result
  here: `fact_model_blend date=2026-08-26` carries **TWO** rows for this model_id as **CHILD**
  (`Anna *9237` abs 0.21, `Anna *9238` abs 0.16). Composition PRESENT => MODEL, not G8 residual
  (`fef636c2` and `44be78ad` each measured ZERO as parent or child).
- **GRAIN:** `as_parent=0 / as_child=N` matches the CONFIRMED canonical models (Intermediate-Term
  0/9, Short-Term 0/7) -- child-only membership is canonical here, not evidence of a sleeve.
- **SPELLING GROUNDED, NOT CHOSEN:** the served global account-distribution `by_model` carries
  exactly the 7 un-relabeled display strings (`Intermediate`, `Short-Term`, `Ultra Short-Term`,
  `Long-Term Conservative`, `Long-Term Aggressive`), so `Opal Fixed Income` takes the same form with
  the `Opal ` prefix dropped. No existing key could absorb it: 9 keys in the served union, none a
  fixed-income member.

---

## 5. ACCEPTANCE, AND THE PREDICTED FAILURE SIGNATURE

**Acceptance is the 2026-08-27 13:30Z SCHEDULED fire.** ⛔ **NOBODY FIRES AN AD-HOC RUN TO CHECK** --
an ad-hoc artifact is never production evidence, and today's split verdict already cost the clean
read once.

`3.0.0_SA_CVO` verifies on the pre-registered bar: **BOTH `as_of_last` AND `_provenance.written_at`
must advance, for global AND cottonwood.**

> **ON THE RECORD BEFORE THE RUN:** a *cottonwood-advances / global-does-not* result is a **KNOWN,
> PREDICTED** signature meaning the three-file fix did not fully land -- **not a new mystery.** A
> *neither-advances* result means Leg A did not land (the lambda still runs the old bundle).

---

## 6. OPEN AT HANDOVER -- neither is mine to close

1. **LEG A OWNERSHIP.** COO 72310 ruled option (ii), seating a DS lane for the deploy; that ruling was
   made against a one-leg picture and **leaves Leg A -- the leg the fire actually reads -- unowned.**
   Rule 13 puts infra/Lambda with AE. **Ruling requested; I will not start it on inference.**
2. **ANDREW'S SENTENCE (business, not data).** The measurement establishes **STRUCTURE, NOT INTENT**.
   It proves not-a-rename and not-a-residual. It **cannot** prove Opal meant to have a fixed-income
   model -- no instrument in this estate points at that. The act lands a new row carrying **$8.44M
   across 2 accounts into a CLIENT-FACING served Global union.** The question is a yes/no:
   *"A new Cottonwood model 'Opal Fixed Income', $8,442,396.91 over 2 accounts, first appearing
   2026-08-26, composed of Anna \*9237 / \*9238 -- confirm it should appear as its own row in the
   served Global union."*

---

## 7. CARRIED DISARM -- OBSERVATION / **ARMED** (CVO 72304 s.4)

Cottonwood's dim grew **146,879,940.09 -> 191,504,659.67** (485 -> 492 accounts) on 2026-08-26.
Whoever writes the release / close-out line **states the two figures split**:

- **$8,442,396.91** -- the new row, **explained** by this repair.
- **~$36.2M** -- movement in OTHER existing models (`Conservative Growth` +23,476,469.16 on +2 accts;
  `Ultra Short-Term Income` +11,910,062.24 on +2 accts). **NOT explained by this repair and must not
  be presented as though it were.**

Not called a defect -- large funded accounts would look identical. Named because a ~+30% one-day book
move reaches a client-facing total on the next fire and nobody has said why.

---

## 8. LANE NOTE ON THE COMMIT (CVO 72304 s.2 -- accepted)

`@ae106b1124` carries two DS-lane gold scripts and one AE-lane lambda source in **one** commit under
an AE author line with no override recorded; Rule 14a makes the override **singular**, so this should
have been **two** commits. The boundary starts at COMMIT, not deploy -- the line was drawn one step
too late. Bytes are correct and nothing is deployed. Per CVO, the clean resolution is the DS lane
**re-landing the two gold files under its own author line** rather than inheriting an AE-authored
commit. `.owned-paths.yaml` carries no entry for either gold-script tree, so nothing mechanical was
going to catch it.

-- `0.6.2_AE_PartnerETL~A`, 2026-08-26
