# PHASE 0 — the `infra/` limb of the two-firm enumeration

> ## ⛔ BINDING ON `0.7.0_AE_CloudOps` — APPLY GATE ON DS'S AUDIT-WIRING DIFF. READ BEFORE ANY R1 APPLY.
>
> **I WILL NOT LAND DS'S AUDIT-WIRING DIFF AS PREPARED.** (`0.4.0_DS` @`c138e7f58`; STOP block on the diff
> itself @`930d85108`.)
>
> **THREE CONDITIONS, ALL REQUIRED, AS ONE STEP — NEVER THE DIFF FIRST AND THE FIX AFTER:**
> 1. the diff, **plus**
> 2. **derive the marker's `count_axis_source_audit` keys from the world, not the two literals**, and carry
>    `unaudited_firms` as a first-class marker field where **non-empty = cycle NOT clean** regardless of every
>    mapped leg being green, **plus**
> 3. **CONTROL 5 — stage a synthetic THIRD firm prefix under `gold/mdpf_revamp/`, run the stage, assert the
>    marker NAMES it.** **If the marker still reads green and two-firm, the wiring is SELF-CERTIFYING and
>    DOES NOT LAND.**
>
> **DS's controls 1-4 are NOT sufficient** — control 4 ("absent is not clean") only fires for a firm already
> in the dict, so **all four pass green on a cycle missing an entire firm.**
>
> **VINTAGE:** the diff header's `CTO: APPROVED AS WRITTEN 134926Z` is **TRUE, never retracted, and predates
> the §7f finding by ~3 hours** — DS marked it SUPERSEDED IN PART rather than deleting it. **An approval is
> valid as of what was known when it was given.**
>
> **WHY THIS BLOCK EXISTS, recorded against myself:** I told DS *"a message is not a carrier"* and then left
> this entire gate **in a message**, while committing only the doctrine half (@`5bcd9bec5` — gate language: 0
> occurrences; positive control: 3). **DS verified my carrier instead of trusting it and caught it.** The
> insight half feels like the finding, so it gets written down; **the operational half feels like a decision
> you will obviously remember — and that is the half that dies at a reset.** Same class as R1, committed
> within an hour of the R1-R12 sweep landing.

**Author:** `0.7.0_AE_CloudOps` 2026-07-22 ~1537Z · **Phase 0 owner:** `0.4.0_DE_ClientPlatform`
**Why me:** DE's coverage line names **`infra/` dispatch + IAM as NOT COVERED**, and that is my domain.
**Authority:** carve-out 3 — *"read-only MDPF ANALYSIS continues, especially Phase 0 — enumerating is not
initiating, and it is the input the advisory needs."* **Read-only. Nothing changed, nothing applied.**

---

## COVERAGE — stated first, per R6/R10

| | |
|---|---|
| **COVERED** | the `infra/` tree, token-search on `{49financial, inflection, cottonwood}` via `comp-grep`, **plus a full read of the MDPF dispatch Stage-6 block** (`mdpf-daily-dispatch.sh:425-549`) |
| **NOT COVERED — and this is the important half** | **encodings that name NO firm** — a hardcoded arity, a count literal, a 2-element slice — **are INVISIBLE to a token search.** I caught `keys_staged: 7` only because I read the file, not because the search found it. **Everything outside the block I read is unenumerated for that class.** |
| **NOT COVERED (other limbs, not mine)** | publisher/promote path · `dim_mdpf_account_distribution.py` / `dim_mdpf_aum_{metrics,timeseries}.py` (they live in `data/`, not `infra/`) · FE per-firm path (`portal/`) · IAM (see below, partial) |

> **The token axis is the wrong axis for the sharpest member of this class.** A two-firm assumption written
> as `7` names no firm and survives every grep for a firm name. **Treat this limb as covering the NAMED
> encodings in `infra/` and only the block I actually read for the unnamed ones.**

---

## FINDING 1 — the completion marker's anti-omission guard is ITSELF firm-hardcoded

`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:508-539`

`_audit()` (`:508-517`) was written **specifically** so a missing audit cannot read as clean:

> *"ABSENT IS NOT CLEAN -- if the file is missing the marker says the audit DID NOT RUN, it does not omit
> the field (an omitted field reads as 'fine')."*

**But the dict it feeds has hardcoded firm keys** (`:536-539`):
```python
"count_axis_source_audit": {
    "inflection":  _audit("inflection"),
    "49financial": _audit("49financial"),
}
```

**So for a third firm the field is not `audit_did_not_run` — the firm is ABSENT FROM THE DICT ENTIRELY.**
The guard delivers exactly the failure it was built to prevent, for any firm it does not name.

> **A guard that enumerates its subjects cannot protect a subject it does not enumerate.** The
> absence-is-not-clean property holds **per named firm**, never **per firm**. Cottonwood joins and the
> marker reports two verdicts for a three-firm cycle, with nothing anywhere saying a verdict is missing.

**This is the R6 principle** (*"the unreached are NOT clean"*) **defeated by a hardcoded key list** — same
shape as my own census finding, one layer down.

---

## FINDING 2 — `keys_staged` is a hardcoded literal, and the marker is what the co-sign reads

`:526` `"keys_staged": 7` · `:434-435` the comment deriving it: aggregate ×3 + account_distribution ×3 +
non_model ×1 = **7**. With Cottonwood the true count is **9** (aggregate ×4 + distribution ×4 + non_model ×1).

**Both halves have to move together, and nothing couples them:**
- loops extended, literal not → marker asserts **7** while **9** landed
- literal changed, loops not → marker asserts **9** while **7** landed

**This is not cosmetic. `gold/mdpf_revamp/meta/cycle-complete.json` is the artifact the parity streak and the
co-sign read.** A marker misreporting its own coverage is a **false completion record** — the same class as
the count-axis defect found *inside* the co-signed frozen-9 this morning.

**Recommendation (a change, therefore NOT made under the hold — DE/DS/CTO's call):** derive `keys_staged`
and `segments` from the same firm list the loops iterate, so the marker cannot disagree with what was staged.
**A count that is asserted rather than derived is a claim, not a measurement.**

---

## FINDING 3 — the staging loops are two-firm literals

`:459` and `:472` — `for firm in 49financial inflection global`.
Cottonwood's `aggregate_aua_timeseries` and `account_distribution` keys are **never staged**, and `:462`'s
`MISSING` guard fires only for firms already in the list. **A firm absent from the loop produces no error —
it produces nothing at all**, which the marker then reports as a clean 7-key cycle (Finding 2).

`:487` / `:495` — the audit legs are per-firm literals with the deliberate CTO-approved asymmetry
(`inflection || return 1` / `49financial || true`). **There is no Cottonwood leg.** *(The asymmetry itself is
correct and must not be collapsed — flagging only that the list is closed at two.)*

---

## FINDING 4 — an argparse whitelist that HARD-REJECTS a third firm

`infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/compute_per_firm_account_distribution.py:362`
```python
ap.add_argument("--firm", choices=["49financial", "inflection", "all"], ...)
```
`--firm cottonwood` **exits 2 at argument parsing** — it cannot reach the code. Per its own docstring
(`:19`) this writes `json/mdpf/{firm}/account-distribution.json`, i.e. the **legacy served path** — the same
`json/mdpf/**` prefix Deliverable 2's deny protects.

**REACHABILITY NOT ESTABLISHED BY THIS LIMB.** I found it in source; I did **not** determine whether the
nightly invokes it or whether `dim_mdpf_account_distribution.py` has superseded it. **Two producers write
per-firm distribution and I have not established which one serves** — that question belongs with DE/DS and
is flagged, not answered. *A hardcoded choices-list in a producer nobody invokes is a different severity
from one on the serving path, and I have not distinguished them.*

---

## IAM — ARN-AXIS SWEEP RUN (DE GO 154107Z). **FINDING 5 IS A HARD BLOCKER ON PHASE 1a.**

### FINDING 5 — the MDPF revamp producer's role CANNOT READ Cottonwood silver

`infra/aws/terraform/mdpf-pipeline/iam.tf:243-252`, Sid `AssetsRevampSilverRead`, grants `s3:GetObject` on
**exactly five** ARNs:
```
opal-data-assets/smartx/platform/silver/*
opal-data-assets/schwab/08242234/silver/*
opal-data-assets/eclipse/inflection/silver/*
opal-data-assets/orion/inflection/silver/*
opal-data-assets/gold/mdpf_revamp/*
```
**`blackdiamond/cottonwood/silver/*` is not among them** — and Cottonwood silver demonstrably EXISTS there
(12 `fact_*` tables: `fact_holdings`, `fact_allocations`, `fact_model_definition`, `fact_transactions`, …
the WS-5 converter output).

**GROUNDED ON ALL THREE LIMBS (Rule 22a):**

| limb | instrument | result |
|---|---|---|
| `desired` | TF source at HEAD | 5 ARNs, no Cottonwood |
| `applied` | live `aws iam get-role-policy --role-name mdpf-daily-runner-ec2-role --policy-name mdpf-runner-scoped` | **same 5 ARNs, no Cottonwood** — desired and applied AGREE, so this is **not drift, it is an unbuilt dependency** |
| `exercised` | `simulate-principal-policy`, **one `--resource-arns` per call** | `blackdiamond/cottonwood/silver/...` → **`implicitDeny`** |
| control | **SEPARATE invocation** (never batched — 2+ ARNs poisons the held ones) | `eclipse/inflection/silver/...` → **`allowed`** |

**The control discriminates**, so the `implicitDeny` is a real deny and not a blanket refusal.

**CONSEQUENCE:** Phase 1a re-homes Cottonwood as `build_cottonwood_artifact()` **inside the shared producer**,
which runs on `mdpf-daily-runner-ec2-role`. **On its first read of Cottonwood silver it AccessDenies at
runtime.** `AssetsRevampListScoped` (`:271-279`) carries the same closed prefix-condition list, so partition
discovery (`_latest_date` / `_read_partition` paginators) fails the same way. **Both need the Cottonwood
prefix before 1a can run green.** Not built under the hold — recorded, owner CTO.

### WHY NEITHER SWEEP AXIS WOULD HAVE FOUND THIS — a THIRD axis is needed

- **firm-token axis:** `main.tf:56-61` declares `bd_bucket` / `inf_bucket` and **no `cot_bucket`.** Those name
  **buckets, not firms.** Invisible.
- **unnamed-arity axis** (DE's second sweep): there is **no `2` anywhere here** — five ARNs covering two firms.
  A `== 2` / `[0]`/`[1]` / concat-pair search finds nothing. **Also invisible.**

> **The two-firm encoding here is an ABSENCE, and AN ABSENCE HAS NO TOKEN. You cannot grep for what is not
> there.** Every pattern search — on firm names, on arities, on anything — enumerates what IS present. This
> class is only visible by taking an enumerated grant/config and **comparing it against the population it is
> supposed to cover.**

**THIRD AXIS, recommended to DE for the census:** *completeness-of-enumeration* — for each place the estate
lists its subjects (IAM resource lists, prefix conditions, event-pattern filters, `choices=[...]`, config
maps), diff that list against the real population. **It is a set-difference check, not a pattern match**, and
it is the only axis that can see a missing member.

### FINDING 6 — the PUBLISHER fails SILENTLY and GREEN, and good IAM is *why*

*(Closes a cell DE's census names OUT OF REACH: publisher/promote. **My limb is the IAM face + the publish
map, NOT the producer logic.**)*

**IAM verdict: CLEAN on the firm axis — a genuine pass.** `mdpf_portal_publisher.tf:29-30` grants
wildcard prefixes (`gold/mdpf_revamp/*` read → `json/mdpf/*` + `json/portfolios/*` write), conditioned
ListBucket on the same. **No firm is enumerated anywhere in the grant.** A third firm needs no IAM change.

**And that is exactly the problem.** `lambda_function.py:37-47` — `PUBLISH_MAP` is a **hardcoded 9-entry
dict** over `global` / `49financial` / `inflection` / `portfolios`. **Cottonwood has no entry.**

```python
:100  results = [_publish_one(s3, seg, name, pk) for (seg, name), pk in PUBLISH_MAP.items()]
:102  all_present = len(missing) == 0
:106  "total": len(PUBLISH_MAP)
```

**The publisher iterates its own map.** A firm absent from the map is never attempted, never lands in
`results`, never lands in `missing` — so it cannot raise `all_present`. **The success denominator IS the
configuration.**

> **`all_present` is a claim about the MAP, not about the CYCLE. The publisher cannot report missing a firm
> it was never told to look for.**

**At S5/cutover, with Cottonwood staged, the publisher returns `published 9/9, all_present=True` — and
Cottonwood is simply never served.** Note `_publish_one` has a careful `missing_source` soft-fail path for a
mapped key whose source is absent; **that care does not reach an unmapped firm, which never enters the loop.**

**THE CONTRAST WITH FINDING 5 IS THE POINT:**

| | Phase 1a (Finding 5) | Phase 4 publisher (Finding 6) |
|---|---|---|
| IAM | enumerated prefixes → **blocks** | wildcard prefixes → **permits** |
| failure | **LOUD** — AccessDenied at runtime | **SILENT** — green, `all_present=True` |
| when found | first run | possibly never |

**The publisher's IAM is better-written than the runner's — correctly wildcard-scoped, least-privilege — and
that is precisely what removes the loud failure.** The runner's narrower grant accidentally functions as a
completeness check the publisher's cannot. **Tightening IAM does not catch a forgotten subject; enumerating
it does, and only by accident.**

---

## THE PATTERN — three instances, one class, all found in one sweep

Findings 1, 2 and 6 are **not three bugs. They are one defect class:**

> ### **A COMPLETENESS SIGNAL WHOSE DENOMINATOR IS ITS OWN CONFIGURATION.**

| # | signal | denominator | reports on a 3-firm cycle |
|---|---|---|---|
| 1 | `count_axis_source_audit` | hardcoded firm keys | two verdicts, third firm absent — **not** `audit_did_not_run` |
| 2 | `keys_staged: 7` | a literal | `7` |
| 6 | `all_present` | `len(PUBLISH_MAP)` | `9/9 = True` |
| 7 | `stale_partners` / `all_fresh` | `partners = {"49financial": …}` | `[]` / `True` — **and the SKIP never fires** |
| 8 | freshness cohort check | `EXPECTED_COHORTS` (15-tuple) | all-fresh — Cottonwood **not expected, so never missing** |

**Finding 7 is the one that escalates the class from reporting to safety:** 1, 2 and 6 mis-state what
happened; **7 changes what happens.** A firm outside the protected set does not merely go unreported — **it
goes unprotected**, and the roll-forward guard that exists to stop WS-E fabricating a residual simply does
not apply to it.

**Every one reports GREEN while a third firm is missing.** Each was written carefully — Finding 1's helper
exists *specifically* to prevent silent omission — and each is defeated the same way: **the guard's subject
list and the world's subject list are different objects, and nothing compares them.**

**This is why the completeness-of-enumeration axis is not a nicety.** A green signal derived from a
hardcoded list is not evidence of coverage; **it is evidence that the list was iterated.**

---

## FINDING 7 — the convergence gate. **A MISSING GUARD, not a missing report.** *(worst of the class)*

`infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:520-536`

```python
:520  partners = {"49financial": bd}   # inflection is the spine/DRIVER, not a skippable partner
:521  stale_partners = [p for p, v in partners.items() if not v["fresh"]]
:535  "all_fresh": bool(inf["fresh"] and bd["fresh"]),
```

**`partners` is a SINGLE-ENTRY dict.** Cottonwood is **neither** the spine (inflection is) **nor** a listed
partner — so **its freshness is never evaluated at all.** It therefore can never appear in `stale_partners`,
so the dispatch's `MDPF_STALE_PARTNERS` never names it, so **its feeders are never skipped when it is stale.**

**WHY THIS IS CATEGORICALLY WORSE THAN FINDINGS 1, 2 AND 6.** Those omit a firm from a **report**. This omits
a firm from a **safety mechanism**. The per-partner gate exists *specifically* so a stale partner's feeders
are skipped — the code says why (`:518-519`): *"WS-E never runs on a stale minuend, so it cannot fabricate a
residual (roll the BLOCK, never re-derive a field)."*

> **The fabrication this design prevents for 49financial is UNPREVENTED for Cottonwood — not because the
> protection was refused, but because the protected set is a one-element literal.**

**And `:535` `all_fresh` is a two-firm conjunction** (`inf AND bd`), so on a three-firm cycle it reports
**`all_fresh: True` with Cottonwood stale.** A fourth instance of the class, on the gate's own verdict field.

**ALIAS DISAMBIGUATION (per DE's caution — resolved by ROLE, not token):** `bd` at `:520`/`:531`/`:535` is the
**49financial freshness result object**, NOT the `CUSTODY_SOURCE` enum (`bd|schwab`, `:532`, `:404-411`),
which is a different variable in the same scope. **Two distinct meanings of `bd` in one function; I read the
role, not the string.**

---

---

## FINDING 8 — `EXPECTED_COHORTS`: the denominator is literally named *expected*

`infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py:99-130`

A hardcoded 15-entry tuple: **4 ETF + 1 inflection + 10 `49financial`. No Cottonwood cohort.**

> **The instrument asks "are all EXPECTED cohorts fresh?" where *expected* is a literal. A cohort absent
> from `EXPECTED_COHORTS` is not expected — and therefore can never be missing.** The class again, with the
> denominator wearing its own name.

**SEVERITY IS LOWER THAN 5/6/7, AND I AM NOT RECOMMENDING A FIX.** Apply Andrew's ~1425Z test — *does it PAGE
someone, or does it STOP something?* **This one pages.** It is a freshness monitor, not a gate, so it falls
under the **07-17 alert suspension**: the enumeration gap is a **census fact**, not a work item. **Recording
it as a two-firm encoding; explicitly NOT proposing to build against it while the suspension stands.**
*(Contrast Finding 7, which STOPS things and is therefore in scope.)*

---

---

## FINDING 9 — the trigger's IAM enumerates two firm sources (and would fail LOUD)

`iam.tf:390-426` — `InfSentinelRead` (`inf_bucket` sentinel) + `BdSilverGateRead` / `BdSilverGateList`
(`bd_bucket` `silver/allocations`, `silver/fees`, `schwab/silver/rps`). **No Cottonwood source.**

**Coupled to Finding 7 and they MUST move together:** extending `partners` to include Cottonwood without
adding the grant makes the gate AccessDeny on the new partner's freshness read.

**CREDIT WHERE IT IS DUE — this one is well-built.** `lambda_function.py:344-348` classifies the failure
explicitly: **404 → `ROLL_SOURCE_ABSENT` ("a DATA condition, expected"); 403 → `ROLL_SOURCE_UNREADABLE`
("the INSTRUMENT is broken (missing IAM grant). A CONFIG fault")**. **This code already distinguishes "the
thing is missing" from "I cannot see the thing."** That is the discrimination the publisher lacks entirely.

## FINDING 10 — freshness-checker IAM: **CLEAN on the firm axis**

`iam.tf:493-525` reads the **served** aggregate partitions (`platinum/mdpf/aggregate_aua/*`) by wildcard.
**No firm enumerated; a third firm needs no IAM change.** The enumeration is in the code (Finding 8).

---

## THE 2×2 — you can PREDICT the failure mode from the IAM shape

| | IAM **enumerates** firm prefixes | IAM **wildcards** the prefix |
|---|---|---|
| **fails** | **LOUD** — AccessDenied on first run | **SILENT + GREEN** |
| instances | runner (**F5**), trigger (**F9**) | publisher (**F6**), freshness-checker (**F8/F10**) |
| detectability | found immediately | possibly never |

> **The narrow grant is accidentally a completeness check; the wildcard grant is correctly least-privilege
> and detects nothing. Where IAM is firm-agnostic, the enumeration hides in CODE and fails silently — so
> THE BETTER-WRITTEN THE IAM, THE MORE THE CODE'S SUBJECT LIST NEEDS ITS OWN CONTROL.**

**Operational use:** for any remaining component, **read its IAM shape first** — a wildcard grant predicts a
silent code-level enumeration and tells you where to look. **Both publisher and freshness-checker split
exactly this way (IAM clean / code two-firm), found independently.**

---

## §7f NEEDS A SECOND CLAUSE — **OUTSIDE-THE-CONFIG IS NECESSARY, NOT SUFFICIENT**

**Source: `0.4.0_DS_ClientPlatform` @`c138e7f58`, found against their own diff. The insight is theirs; I am
connecting it to the doctrine because §7f came from my findings and is now incomplete.**

§7f as landed: *a coverage fraction is only evidence if its denominator comes from OUTSIDE the instrument's
own configuration.* **DS's audit script satisfies that and is still blind.**

`mdpf_revamp_count_source_audit.py:102-109` `unaudited_firms()` set-differences the **live S3 staging prefix**
against `AUDITED_FIRMS` — a real set-difference, genuinely outside the config, **and it was landed
@`6785ce65a` BEFORE the doctrine was written.** But DS states the residual precisely:

> the denominator is derived from the staging prefix — **outside the config, yet still DOWNSTREAM of the
> producer being audited.** It catches *landed-but-unaudited*; it **cannot** catch *never-landed-at-all*.
> A firm that never emits has no prefix, the set-difference is empty, and the audit reads clean.

> ### **A DENOMINATOR DERIVED FROM A PROCESS'S OWN OUTPUT CAN ONLY ENUMERATE SUBJECTS THAT PRODUCED OUTPUT.
> ### THE DENOMINATOR MUST BE *UPSTREAM* OF THE PROCESS BEING MEASURED — AN AUTHORITATIVE REGISTRY — NOT
> ### MERELY OUTSIDE ITS CONFIG.**

**This is "an absence has no token" one layer up**, and it is the same failure my own census had: I enumerated
what the estate *contains*. **Observed state is a better denominator than a literal and still not evidence of
completeness.**

**ONE REGISTRY CLOSES BOTH.** DS's residual and R13's publisher need the *same* fix — an authoritative firm
list consumed as the denominator. **`PUBLISH_MAP` should not be hand-extended for Cottonwood and the marker
should not grow a second list**; both should read one registry. **Recommended to CTO as a single item, not
two.** *(Two hand-maintained lists is how they drift; one registry is why R13 and DS's residual are one
problem.)*

### Sweep — what this limb does NOT cover
`mdpf-pipeline` root (runner, trigger, freshness roles) + publisher role + trigger gate logic + cohort list.
**Not swept:** `bd-pipeline`/`cot-pipeline` cross-grants, Lambda@Edge. **OPEN, not clean.**

### INSTRUMENT NOTE — a false ABSENT I nearly published
`aws s3api list-objects-v2 --delimiter "/" --query 'CommonPrefixes[].Prefix' --output text` returned `None`
for `blackdiamond/cottonwood/` — **and returned 134 `None`s at the bucket root, where prefixes certainly
exist.** The positive control is what caught it; `aws s3 ls` on the same bucket returned all 12 prefixes
correctly. **Mechanism UNDETERMINED** (a lone `"/"` delimiter arg is a plausible MSYS-mangling target, not
established). **Had I not run the root control I would have reported "Cottonwood silver does not exist" —
the exact inverse of the true finding.**

---

## WHAT THIS MEANS FOR THE DATE

Phase 0 is *"the only unbounded item ... nothing else is unbounded."* This limb closes the **named** `infra/`
dispatch encodings — **6 sites in 2 files** — and leaves two named gaps: the **unnamed-arity class**
(`keys_staged: 7` is one confirmed instance; the population is unmeasured) and the **IAM ARN axis**.

**The unnamed-arity class is the one that should worry the estimate**, because it is invisible to the search
everyone will naturally run, and Finding 2 shows one member of it sitting directly on the co-sign's evidence
artifact.
