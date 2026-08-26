# D3_MODELOVERLAY -- THE ADVISOR-LEVEL UPSTREAM-UNBLOCK SPEC

**archetype:** DIAGNOSE

**Author:** `0.4.0_DS_ClientPlatform~S` · **2026-08-26 ~14:0xZ**
**Authority:** `2.0.0_SA_COO` 72176 section 2 (re-cut approved as written; "until it lands, this
message IS your authority"), shaped by `3.0.0_SA_CVO` 72187 section 4 -- cut as the UPSTREAM-UNBLOCK
SPEC, never as "build the advisor level."

**Scope:** the ARMED residual `D3_MODELOVERLAY-S2` ONLY. Surfaces (a) and (b) of
`D3_MODELOVERLAY.TO-R1-DS` are DISCHARGED (`fbf3ce7a44`, 2026-08-25) and CVO-CERTIFIED 6/6
(`CERT_D3_MODELOVERLAY_TO_R1_DS_20260825.md`). Nothing here rebuilds them.

---

## 0. THE ONE-LINE ANSWER

**The advisor level is not buildable because BD dimension 436 (Primary Portfolio Group) is not in
template 390224's dimension selection, and the selection is BLACK DIAMOND-SIDE STATE that this
estate's puller replays verbatim and never authors.** The remedy is a template amendment at Black
Diamond. **A mechanism to perform that amendment from this estate EXISTS and is proven** (the cot
G4 precedent), but it is a vendor API write and therefore Andrew's call, not an exec act.

---

## 1. WHAT WAS ALREADY ESTABLISHED, AND WHAT I DID NOT RE-DERIVE

`1.0.0_SA_CTO`'s `FINDING_20260825_BD_DIM_436_ONE_VENDOR_FIELD_BLOCKS_TWO_DIRECTIVES.md` established
the ABSENCE and its blast radius (D3 advisor level + ADVI_INSURE advisor spine leg, two lanes inside
twenty minutes). **I did not re-run its measurement and I do not restate it as mine.** Its positive
control ("portfolio" = 8 columns while "primary" = 0) is sound and settles that the zero is a true
absence rather than a dead matcher.

**What that finding did NOT settle, and what this spec adds:** its conclusion that the gap is
"fixable only vendor-side (add dim 436, re-pull)" and "fixable by no code in this estate" is sourced
from `bd49f_dim_portfolio_group.py:26-29` -- **our runner's comment about the vendor's template.**
That is the artifact-describes-itself shape: the code under investigation is also the witness. The
comment may be right (it is, on the substance) but ABSENCE and OWNER-OF-THE-REMEDY are two different
claims, and a positive control on the first does not carry the second.

**This spec grounds the remedy-owner claim on instruments that are not the runner.**

---

## 2. THE DISCRIMINATOR, RUN ON TWO INSTRUMENTS NEITHER RECORD USED

The question that decides the owner: **does this estate CHOOSE the dimension selection, or replay
one BD holds?** Three outcomes, three different owners.

### 2.1 Instrument A -- the puller's run-body construction (source, not comment)

`infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py`, `_run_template()`
at `:259-286` @HEAD:

```
:262  fetched, _ = _request("GET", "/datamining/request/v1/template/%d" % tid, token=token)
:263  full = fetched.get("template", fetched)
      ... mutates ONLY: startDate/endDate re-stamp (:265-276)
      ... setdefault(None) on 5 fields (:277-279)
      ... pop() of 3 fields (:280)
:281  out, _ = _request("POST", "/datamining/request/v1/run", ... body={"template": full, ...})
```

**MEASURED: the function never reads, writes, or constructs `parentDimensionLevels`,
`childDimensionLevels`, `levels`, or any `dimensions[].isSelected`.** It GETs BD's persisted body,
adjusts dates and a fixed field set, and POSTs it back. `_selected_dim_floor()` at `:235-256` READS
the selection to compute a column floor -- **a reader, never a writer.**

**Verdict on A: the selection is vendor-side state. The estate is a faithful replayer.** This is
`1.0.0_SA_CTO`'s conclusion, now carried by the puller rather than by the runner's self-description.

### 2.2 Instrument B -- the landed enriched template body (vendor bytes, not our prose)

This closes the one estate-side workaround that instrument A leaves visibly open: **if BD's enriched
GET returned the full dimension CATALOG with per-dimension `isSelected` flags, we could flip 436's
bit in the POSTed run body without touching BD's persisted template at all.**

Read: `s3://opal-data-assets/blackdiamond/49f/_ops/probe/20260714T171101_template_390224.json`
(37,055 B, landed 2026-07-14).

**Provenance of those bytes, checked before trusting them** -- `lambda_function.py:513-517`:
`_land(t_key, t_body)` writes the **raw response body of `GET /datamining/request/v1/template/{tid}`
unmodified.** No normalization, no filtering. So this file IS the enriched GET, not an echo of
something we sent.

Measured census over all three envelopes:

| envelope | level | dims | isSelected=true |
|---|---|---|---|
| `parentDimensionLevels` | Relationship | 7 | 7 |
| `parentDimensionLevels` | **Portfolio Group** | **2** | **2** |
| `childDimensionLevels` | Portfolio | 26 | 26 |
| `childDimensionLevels` | Account | 70 | 70 |
| | **TOTAL** | **105** | **105** |

```
dimension id 436 occurrences ......... 0
dimension name containing "primary" .. 0
```

**THE DECISIVE FACT: 105 of 105 enumerated dimensions are `isSelected=true`. THERE IS NO UNSELECTED
POOL.** BD's enriched GET for this template returns the SELECTION, not the CATALOG.

**Therefore dim 436 is not present-and-deselected -- it is absent from the body entirely, and there
is no bit to flip.** The client-side-override workaround is not merely unwise; it is **not
expressible**. A remedy must ADD a dimension object to a level's `dimensions[]` array.

**CORROBORATION, independent of me:** `Portfolio Group` = 2 dims here matches the runner's own
sidecar census ("Portfolio Group": 2) and its export-column measurement ("columns containing
'group': 2 -- Portfolio Group, Portfolio Group Market Value"). Three instruments, one number,
two of them not mine.

### 2.3 VINTAGE -- stated because a line citation without one is not a citation

The probe body is **2026-07-14**, 43 days before this read. It is the newest landed enriched body;
the `pull` mode GETs a fresh body every run but **lands the EXPORT, not the template body**, so no
newer enriched body exists in the estate. The claim "436 is not selected" is therefore MEASURED at
2026-07-14 and **CORROBORATED at 2026-08-18** by the runner's census over that day's landed export
(0 columns containing "primary" across all 92). **I did not call the BD API to refresh it -- that is
a vendor call and is not mine to make.**

---

## 3. THE REMEDY MECHANISM -- AND WHY ONE SENTENCE OF THE CTO FINDING NEEDS AMENDING

`1.0.0_SA_CTO`'s finding says the gap is **"fixable by no code in this estate and by neither lane."**
On the substance (neither DS lane can fix it, and no workaround should be built) that is right and
it binds. **As literally worded it is too strong, and the counter-example is in this repo:**

`org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/COT_SUPERVISED/g4_amend_holdings_template.py`
amended a persisted BD template (226355) from this estate on **2026-08-20**, EXERCISED:

```
POST /v1/template/ with a real templateId  -> MINTS A CLONE (not an update). Doc defect, routed.
PUT  /v1/template/{id}                     -> HTTP 405.
PUT  /v1/template/  (id in the BODY)       -> 200, UPDATES IN PLACE.
```

Measured delta, pre-image vs post-image, both saved beside that script:

| level | dims before | dims after | added |
|---|---|---|---|
| Account | 2 | 3 | id `33` "Account Supervised" |
| Holding | 11 | 12 | id `45` "Holding Supervised" |
| Portfolio | 1 | 1 | -- |
| Relationship | 1 | 1 | -- |

**So a BD persisted-template dimension amendment is a KNOWN, EXERCISED, ROLLBACK-EQUIPPED procedure
in this estate.** It saves a pre-image before any write, verifies by fresh-GET diff, and rolls back
by re-POSTing the pre-image.

**This does not make the change an exec act.** It is a **write to a partner system** -- vendor
egress, which CLAUDE.md reserves to Andrew's explicit per-use word, and availability of the wire is
not authorization. What it changes is **the SHAPE of the ask**: not "ask Black Diamond support to
reconfigure a template," but **"authorize one BD API amendment we already have tooling and a rollback
for."** Those are very different asks with very different lead times, and the RESERVED card at Andrew
currently reads as the first.

---

## 4. THE RESIDUAL UNKNOWN -- NAMED, NOT PAPERED OVER

**Nothing in this estate can currently confirm that dim 436 is ADDABLE to template 390224's
`Portfolio Group` level.** The reason is exactly the finding in 2.2: the enriched GET returns the
selection, not the catalog, so **no landed artifact enumerates what dimensions BD OFFERS on that
level of that query type.**

The cot G4 precedent does not settle it either -- it is a different query type (qt1 flat `levels`)
and a different firm tree, and cot is a completely separate firm pipeline from bd (never mirror).

**Two ways to close it, both requiring a vendor read that is not mine to make:**
1. The BD UI -- open template 390224, inspect the Portfolio Group level's available dimensions.
2. A catalog API read (the datamining dimension/level catalog endpoint for queryType 6), landed to
   `_ops/probe/` the same way the template bodies were.

**Until one of those runs, "add dim 436 to 390224" is a WELL-FORMED ASK WHOSE FEASIBILITY IS
UNVERIFIED.** I am not asserting it will work. I am asserting precisely what blocks it and what the
next measurement is.

---

## 5. ACCEPTANCE, ONCE THE UPSTREAM CHANGE LANDS

Written now so the unblock has a defined finish rather than a re-investigation.

| # | acceptance | instrument |
|---|---|---|
| U1 | A fresh enriched GET of 390224 lands under `_ops/probe/` and its `Portfolio Group` level enumerates a dimension whose id is `436`, `isSelected=true`. Census printed with its denominator. | landed vendor bytes |
| U2 | The next scheduled `pull` export carries a column matching `primary` -- **positive control: the "portfolio" matcher still returns 8**, so a zero is discrimination, not a dead matcher. | landed export, not a self-report |
| U3 | `bd49f_dim_portfolio_group.py` emits `is_primary` non-null for > 0 of the bridge rows, and `is_primary_status` stops reading `ABSENT-UPSTREAM`. **Denominator printed both ways** (non-null / total). | producer output |
| U4 | The advisor rollup is built ONLY on `is_primary`, and the account-double-count control is EXERCISED: with 90.6% of accounts in 2+ portfolio groups (mean 4.86, max 13), an advisor sum without the partition key overstates by ~5x. **The control must FAIL on the pre-fix data and PASS on the post-fix data** -- an arm that cannot fail is not a control. | exercised, both arms |
| U5 | `D3_MODELOVERLAY-S2` disarms via its NAMED owner, and AC6's four-level contract reads 4 of 4. **DISARMED is not REMEDIATED** -- both states recorded. | surprise channel |

---

## 6. WHAT MUST NOT HAPPEN, AND WHY IT IS THE EXPENSIVE HALF

**DO NOT BUILD THE ADVISOR LEVEL ON A SUBSTITUTE PARTITION KEY.** `1.0.0_SA_CTO`'s ruling binds and
I am not going near it. The mechanism, restated because it is the reason this residual is safe today:

> 5,579 of 6,155 accounts (**90.6%**) sit in 2+ portfolio groups -- mean **4.86**, max **13**. An
> advisor sum without `is_primary` counts each account roughly five times.

**That produces a NUMBER, not an error** -- the $10.2B-vs-$1B shape. **The absent level is the SAFE
state; a built one would be the incident.** Every candidate workaround (bare advisor name, "- Local
Ops" suffix parsing, division inference) is our reading of vendor intent presented as vendor fact,
which is what the runner already refuses at `:31`, and a name-string join across a 160,091-row dim is
a silent-collision generator.

**An honest missing leg beats a leg that is right most of the time.**

**Also preserved:** both dims publish their own limitation in a status field
(`is_primary_status`, `partition_key_status`). That behaviour is why two lanes diagnosed this in
minutes instead of at a reconciliation. **Preserve it; never route around it.** A bare NULL would
have been indistinguishable from a load failure, a schema drift, or a genuine all-false -- the null
plus its reason is a fact, the null alone is a question.

---

## 7. WHAT I RECOMMEND, FOR THE RECORD-HOLDERS TO RULE ON

1. **To `1.0.0_SA_CTO`:** amend the finding's "fixable by no code in this estate" clause to name the
   G4 mechanism. The finding's OPERATIONAL conclusion is unchanged -- still a vendor write, still
   Andrew's -- but the RESERVED card at Andrew currently understates what we can execute once he
   says yes, and that changes how he reads the cost.
2. **To `2.0.0_SA_COO`:** the new TO's acceptance should be section 5, not "the advisor level
   exists." Per `3.0.0_SA_CVO` 72187 section 4, the latter is unsatisfiable by construction and
   would sit open looking like a stalled lane rather than a blocked one.
3. **Sequencing:** close section 4's residual unknown (a catalog read) BEFORE the ask reaches
   Andrew, so he is asked to authorize a change already known to be possible rather than one we
   hope is.

---

## 8. COMPILER TOOLS

| tool | invocation | result |
|---|---|---|
| `comp-find` | `'390224'` | 224 hits / 26,734 scanned; DEF band named the puller + both silver producers |
| `comp-find` | `'is_primary_status'` | 4 hits / 26,734 -- 1 SURFACED (source), 3 DOC. Narrow and discriminating |
| `comp-find` | `'parentDimensionLevels'` | 22 hits / 26,734 -- surfaced the cot G4 amendment precedent, which is the section-3 finding and was not reachable from the D3 thread |
| `comp-find --name` | `'*template*39022*'` | measured 0 / 28,700 -- no repo-local template body; forced the S3 read rather than a stale copy |
| `comp-pipescript deployed` | `b04_account_model_membership.py` | **rc=2 REFUSED** -- `--pipeline` required, and the script is not under `data/*/scripts/`. It lives at `data/assets/scripts/gold/runners_49f/`. Recorded as an OBSERVATION, not chased |
| `aws s3 cp` (rail-checked) | probe template body | 37,055 B; the section-2.2 census |

**What failed:** `comp-pipescript deployed b04_...` refused twice -- once for the missing
`--pipeline`, once because `runners_49f` is not in the `bd` tree's 30 script ids. **The refusals are
correct behaviour** (a typo must never read as "clear to run"), but I could not resolve the tree for
this script from the tool's own output. **One line to `3.0.0_SA_CVO` as an OBSERVATION; not chased.**

**Gap found:** a declared upstream limitation is discoverable per-project and **nothing aggregates it
across directives** -- `1.0.0_SA_CTO` named this and it is still true. One vendor field blocks two
directives; it took two lanes colliding to see it.

---

## 9. STATE OF THIS DELIVERABLE

**PUSH STATE: landed LOCAL, rides integration.** `0.0.0_AB_MSTR` holds 170 commits mid-publish under
the integrator-only push gate (COO 72167 binding 3), so this is not on `origin/CLOUD` at authorship.

**Nothing in this spec was executed against a vendor system. No BD API call was made. No producer was
written, deployed, or invoked. No TO status field was touched. The MDPF path was not approached.**

-- `0.4.0_DS_ClientPlatform~S`
