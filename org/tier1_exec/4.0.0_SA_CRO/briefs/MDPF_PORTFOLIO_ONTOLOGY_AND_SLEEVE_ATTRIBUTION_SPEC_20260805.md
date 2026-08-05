# MDPF Portfolio Ontology and Sleeve Attribution Specification

**Author:** 4.0.0_SA_CRO (Chief Research Officer)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0005 -- registered in RECON_REGISTER.md
**Date:** 2026-08-05
**Status:** PROPOSAL FOR ANDREW REVIEW -- research/design specification; no build, dispatch,
deployment, or served-output change is authorized by this document.
**Consumes:** `docs/architecture/MDPF_GLOBAL_PRD.md`,
`docs/references/MDPF_GLOBAL_ANDREW_RECORDING_20260729.md`,
`docs/architecture/MDPF_3FIRMS_PRD.md`, and the current MDPF model crosswalk.
**Proposed canonical destination after ratification:** an amendment to `MDPF_GLOBAL` or a sibling
project registered by the owning exec lanes. This CRO copy is the authored source proposal.
**Target schema ID:** `portfolio_classification_v1`.

**2026-08-05 Andrew/Yang working-session amendment:** establishes the five-category portfolio
classification and the Primary/Custom Model distinction described in sections 0-2. This amendment
supersedes this document's earlier recommendation to retire **Custom Model** as a canonical term.

---

## 0. Executive decision

The proposed MDPF_GLOBAL four-segment taxonomy -- ETF Models, SMA Strategies, Custom Models, and
Non-Model -- puts objects from different levels of abstraction into one mutually exclusive dollar
partition. It therefore cannot represent the portfolio structures it is intended to describe.

A Tax Strategy account is the discriminating example. Its high-level category is `strategy` and its
drilldown is `tax`. It also has a reusable Strategy Definition, a distinct client implementation, and
client-level sleeve/lot attribution. Those ontology facts do not make `SMA` a category, and none of
the account's holdings may be attributed to a Model.

**This specification now separates two compatible layers:**

1. a mutually exclusive high-level portfolio classification: **Models, Strategy, Alternative,
   Client, and Insurance**; and
2. an attribution ontology and independent axes:

- stable, reusable **Models**;
- reusable **Strategies**;
- client-specific **Mandates / Strategy Instances**;
- effective-dated client-level **Sleeves**;
- leaf **Holdings / Tax Lots**;
- independent `selection_origin`, `advisory_scope`, and `fee_basis` classifications.

**SMA is not a category in this framework. Every account in the classified population is inherently
an SMA, so `SMA` describes the common account structure and provides no discriminatory value.** A
Strategy account is therefore classified as `strategy`, not `sma`.

### 0.1 Version authority and v0 supersession

In this document, **v0** means the original four-segment design recorded in
`docs/architecture/MDPF_GLOBAL_PRD.md`: ETF Models, SMA Strategies, Custom Models, and the Non-Model
residual. That source document called its proposed axis `segment_v1`; the present working-session
feedback materially changes both its vocabulary and its schema.

The following precedence is binding for this proposal:

1. Andrew's current feedback, including the Andrew/Yang working-session direction, governs the
   target ontology and schema.
2. This specification is the normative successor contract for that direction.
3. The original MDPF_GLOBAL PRD and recording remain provenance for v0 and current-state discovery;
   their four-segment definitions are not co-canonical target requirements.
4. The old `segment_v1` identifier is retired for the successor design and must not be reused with
   new semantics. The revised contract emits `schema_id = portfolio_classification_v1`.

Historical v0 text is retained or referenced only when explicitly labeled **v0**, **legacy**,
**existing**, or **compatibility**. An unlabeled requirement anywhere in this specification is a
current requirement. Section 8 contains the binding field-by-field supersession map.

The existing per-firm A4 rule remains unchanged unless Andrew separately changes it:

```text
non_model(firm, date) = total_aua(firm, date) - model_aum(firm, date)
```

The v0 `segment_v1` four-term subtraction is retired from the target contract. If a legacy
compatibility view is ever reproduced, it must retain an explicit deprecated-v0 label and cannot be
presented as the successor five-category classification.

---

## 1. Canonical high-level portfolio classification

The five high-level categories are:

```text
models | strategy | alternative | client | insurance
```

The display labels are **Models**, **Strategy**, **Alternative**, **Client**, and **Insurance**.
`SMA` must not be emitted as a sixth category because every account in scope is already an SMA.

| Category | Qualifier | Drilldown | Binding meaning |
|---|---|---|---|
| `models` | `primary` or `custom` | registered Opal `model_id` | Branded Opal model exposure. The qualifier is required. |
| `strategy` | none | `divz`, `idvz`, `pfoe`, `muni`, or `tax` | Account dedicated entirely to one Opal Strategy and focused on individual securities. Model membership is prohibited. |
| `alternative` | `private_equity`, `private_credit`, `hedge_fund`, or `real_asset` | registered alternative product/manager such as `aqr` | Alternative exposure classified by both product identity and alternative type. Initially, `aqr` is qualified as `hedge_fund`. |
| `client` | none | none | Unforked catch-all for client assets that do not belong to Models, Strategy, Alternative, or Insurance. |
| `insurance` | none | none | Insurance exposure. No qualifier or drilldown is defined at this time. |

### 1.1 Models: `primary` and `custom`

Both Model classes are branded Opal Models. The qualifier describes production status and breadth of
use; it does not describe who owns the client relationship and it does not make a Custom Model
client-owned.

`model_class = primary` currently permits exactly:

```text
ultra_short_term
short_term
intermediate_term
long_term
ultra_long_term
```

These are the five branded, archetypal Opal ETF Models.

`model_class = custom` identifies branded Opal Models used for large clients in limited production
on an ad hoc basis. The initial named example is:

```text
fixed_income
```

**Custom is a lifecycle classification, not a separate entity type.** A Custom Model can later be
promoted to Primary without changing its stable `model_id`. `model_class` must therefore be
effective-dated so a promotion preserves historical truth: the model is `custom` before the
promotion date and `primary` on and after it. Promotion requires an explicit governed registry
change; it must never arise from usage-count inference.

### 1.2 Strategy

The Strategy drilldown currently permits exactly:

```text
divz | idvz | pfoe | muni | tax
```

Strategy has no qualifier. A Strategy account is designated entirely to one Opal Strategy, is
individual-security-focused, and does not hold or reference Models. In particular, a Tax Strategy
account may hold client-contributed tax lots, but those lots remain part of the `tax` Strategy
implementation rather than becoming Model exposure.

### 1.3 Alternative

Alternative uses two distinct facts:

- the drilldown identifies the product or manager, initially including `aqr`; and
- `alternative_class` qualifies the exposure as `private_equity`, `private_credit`, `hedge_fund`,
  or `real_asset`.

The initial mapping is `alternative_id = aqr` plus `alternative_class = hedge_fund`. Product identity
and class must not be concatenated into a display label or inferred from one another.

### 1.4 Client and Insurance

Client is intentionally unforked and has no qualifier or drilldown. It is the known catch-all after
the other four business classifications have been evaluated. Missing source evidence must still be
made visible through classification confidence/quality controls rather than silently asserted as a
high-confidence Client classification.

Insurance is also unforked at this time and has no qualifier or drilldown. Future subdivision is a
schema evolution, not something to anticipate with placeholder values now.

### 1.5 Why the ontology remains necessary

The high-level category answers a presentation and population-classification question. Mandates,
sleeves, holdings, origin, advisory scope, and fee basis answer different attribution and governance
questions. They therefore remain separate fields and entities rather than being encoded into the
five category labels.

The old residual remains dangerous. A missing model assignment, an unrecognized strategy, a known
client asset, an alternative, insurance, and a genuinely excluded asset must not all silently become
`non_model`. The five-category taxonomy replaces that semantic plug while explicit unknown/quality
controls expose incomplete evidence.

The replacement ontology must let Opal answer, independently:

1. **Model exposure:** which stable model building blocks back the dollars?
2. **Strategy exposure:** which reusable strategies govern the client implementations?
3. **Client construction:** which sleeves compose each client mandate?
4. **Selection origin:** who originated the selection?
5. **Advisory scope:** what is Opal's substantive relationship to the exposure?
6. **Fee basis:** is the exposure inside the governing fee arrangement, and how is that arrangement
   measured?

Every rollup must reconcile to a named denominator without requiring these axes to be collapsed into
one another.

---

## 2. Canonical entity definitions

### 2.1 Model

A **Model** is a stable, reusable, versioned investment building block with a defined target,
composition, or repeatable selection rule.

Models have two effective-dated lifecycle classes:

- **Primary Models** are the five broadly produced archetypal ETF Models:
  `ultra_short_term`, `short_term`, `intermediate_term`, `long_term`, and `ultra_long_term`.
- **Custom Models** are still branded Opal Models, but are used for large clients in limited
  production on an ad hoc basis. `fixed_income` is the initial example.

A model is not made Custom merely because a client implementation is bespoke. Primary/Custom is a
property of the registered Opal Model and its production lifecycle. A future promotion from Custom
to Primary changes the effective-dated classification, not the stable model identity.

Binding properties:

- stable identity (`model_id`) independent of display name;
- effective-dated `model_class = primary|custom`;
- explicit versions and effective dates;
- reusable across clients and strategies;
- target composition or rule contract;
- never inferred from a display label or ticker;
- a client-specific arrangement does not become a model merely because someone calls it one.

### 2.2 Strategy

A **Strategy** is a reusable Opal individual-security investment mandate, policy, or decision process
that can be applied to multiple clients. The current registry is `divz`, `idvz`, `pfoe`, `muni`, and
`tax`.

Tax is the primary client-specific example. Its stable part is the process -- tax-aware transitions,
restrictions, harvesting rules, gains budgets, and direct-security selection authority -- not a
single identical set of holdings shared by every client.

For this taxonomy, a Strategy account is entirely designated to one Strategy and cannot reference a
Model or Model Version. Strategy is the differentiating category; SMA is only the common account
structure shared by the full population.

### 2.3 Client mandate

A **Client Mandate** is the effective-dated statement of the advisory or management arrangement for a
client, household, or account population. It defines the governed perimeter within which strategies,
sleeves, advice, and fee arrangements apply.

The final household-vs-client-vs-account authority grain is an open implementation decision (D-1),
but the data model must support one mandate spanning multiple accounts.

### 2.4 Strategy instance / portfolio implementation

A **Strategy Instance** is a strategy as applied to a particular client mandate. It carries the
client-specific restrictions, objectives, tax facts, effective dates, and sleeve composition.

Every Tax Strategy client therefore has a distinct strategy instance even though the instances
reference the same `strategy_id = tax`.

**Custom Model** is a valid canonical Model classification, but it must not be used as a synonym for
the client-specific Strategy Instance. A Custom Model is Opal-branded, stable, versioned, and in
limited production; a Strategy Instance is the client-specific application of a reusable Strategy.

### 2.5 Sleeve

A **Sleeve** is an effective-dated, client-level attribution container within a mandate or strategy
instance. It answers why a portion of the client's assets is present and what governs it.

A sleeve may:

- reference a `model_version_id`;
- contain direct holdings selected under a strategy;
- contain client-originated holdings that Opal advises upon;
- contain assets governed by an external manager;
- carry cash or another exposure not yet backed by a registered model; or
- be explicitly `unknown` while required evidence is missing.

Sleeves are the canonical aggregation grain. Models and strategies are references on sleeves; they do
not replace them.

The category contract constrains those references: a sleeve under a `strategy` account cannot carry
`model_id` or `model_version_id`. A Model reference is permitted only in the `models` category.

### 2.6 Holding and tax lot

A **Holding** is the actual security exposure. A **Tax Lot** is the minimum leaf when origin, tax
history, or sleeve attribution differs within one security position.

Security-level classification alone is insufficient. A client may bring legacy shares of a security
and later acquire the same security through an Opal-selected strategy. The two sets have the same
ticker but different origin, tax history, and potentially different sleeve attribution.

The target design therefore supports lot-level assignment. A position-level implementation is
permitted only where a measured source census proves that no required fact differs below position
grain.

---

## 3. Independent classification axes

### 3.1 `selection_origin`

Canonical values:

```text
opal | client | external_manager | unknown
```

| Value | Definition |
|---|---|
| `opal` | The investment choice originated from an Opal model, strategy, recommendation, or discretionary decision. |
| `client` | The client originated or retained the choice. This includes legacy positions, RSUs, and client-directed securities. |
| `external_manager` | A third-party manager originated and governs the selection. |
| `unknown` | Evidence is absent or insufficient. Unknown is a first-class data state, never coerced to client or external manager. |

`selection_origin` records provenance of the investment choice. It does not by itself state whether
Opal advises, excludes, or charges fees on that exposure.

### 3.2 `advisory_scope`

Canonical values:

```text
advised | excluded | null
```

| Value | Definition |
|---|---|
| `advised` | The exposure is substantively within Opal's advisory perimeter. This value does not attempt to subdivide discretionary and non-discretionary implementation authority. |
| `excluded` | The exposure is visible to Opal but explicitly outside the substantive advisory perimeter. |
| `null` | The governing relationship cannot be established from available evidence. Display/reporting label: **Unknown**. |

`unknown` is a semantic/reporting state, not a persisted string value for this column. The stored
unknown/missing representation is `null`. Null counts and value must still be surfaced explicitly in
quality reporting.

The axes are deliberately independent. Valid combinations include:

| Example | `selection_origin` | `advisory_scope` |
|---|---|---|
| Opal model exposure inside the advisory perimeter | `opal` | `advised` |
| Opal recommendation implemented by the client | `opal` | `advised` |
| Client-retained RSUs advised around by Opal | `client` | `advised` |
| Third-party manager inside Opal's advisory perimeter | `external_manager` | `advised` |
| Visible assets outside the engagement | any known value | `excluded` |
| Missing advisory-scope evidence | any independently known origin | `null` |

### 3.3 `fee_basis`: governed commercial inclusion plus calculation method

Fee basis is an independent axis. It is **not** an intrinsic property of a Model or Strategy. The same
model or strategy can be subject to different fee arrangements for different clients, accounts, or
effective periods.

The canonical fee-basis object contains:

```text
fee_basis_status:
  included | excluded | null

fee_basis_method:
  market_value | average_daily_balance | period_end_value |
  not_asset_based | null

fee_arrangement_id:
  reference to the governing effective-dated commercial agreement
```

Definitions:

| Field/value | Definition |
|---|---|
| `included` | The exposure is within the economic scope of the governing fee arrangement. |
| `excluded` | The agreement explicitly excludes the exposure from its economic scope. |
| `null` | No reliable agreement or rule establishes inclusion. Display/reporting label: **Unknown**. |
| `market_value` | Fee basis is derived from contemporaneous market value. |
| `average_daily_balance` | Fee basis is derived from an average of daily eligible values. |
| `period_end_value` | Fee basis is derived from a named period-end eligible value. |
| `not_asset_based` | The exposure is commercially covered, but the fee is not calculated from asset value. |

For `not_asset_based`, covered sleeves may remain `fee_basis_status = included`, while
`fee_basis_value` is `null`. This preserves the distinction between commercial inclusion and a
numeric asset-based calculation. `null` is not zero.

As with `advisory_scope`, the fee-basis unknown state is stored as `null`, not the literal string
`unknown`. A null `fee_basis_status` means inclusion cannot be established. A null
`fee_basis_method` means the calculation method cannot be established or does not yet apply; those
are separately observable facts.

The following are separate facts and must not be collapsed:

- the exposure is within an advisory relationship (`advisory_scope`);
- the exposure is economically within a fee arrangement (`fee_basis_status`);
- the fee is calculated from asset value (`fee_basis_method`);
- an actual invoice or fee amount was produced (billing outcome, outside this specification).

---

## 4. Fee-basis qualification level and precedence

### 4.1 Authority and materialization

The authoritative source is an effective-dated **Fee Arrangement** at the client or household billing
relationship. It supplies the commercial agreement, method, schedule reference, and default inclusion
rule.

Applicability is then resolved through:

```text
client / household fee arrangement
  -> mandate or account applicability
      -> optional sleeve override
          -> materialized fee_basis on each sleeve / lot attribution
```

The canonical precedence is:

```text
explicit sleeve override
  > mandate/account-specific rule
  > fee-arrangement default
  > null (displayed as Unknown)
```

Every override carries an effective range, source, reason, and authorizing record. Absence of a rule
is `null` (displayed as Unknown), never automatically `included` or `excluded`.

### 4.2 Policy selectors, not legacy labels

The existing MDPF `fee_scope: full|model` labels are implementation selectors, not durable ontology
values. They should be translated into explicit fee-policy predicates during migration rather than
copied into the new axis.

Illustrative selectors include:

```text
include where advisory_scope = advised
exclude where advisory_scope = excluded
include where strategy_id = tax
include where model_version_id is present
include explicit sleeve_ids
exclude explicit sleeve_ids
```

The current 49F `full` and Inflection/Cottonwood `model` practices require source-grounded translation
before any selector is ratified. Their names are not enough to prove which assets the agreements
actually include.

### 4.3 What fee basis does not cover

This specification does not define fee rates, breakpoints, household tiering, minimum fees, billing
frequency, invoice production, waivers, or revenue recognition. Those belong to a billing contract.
The ontology provides the eligible exposure and the policy/provenance needed by that contract.

---

## 5. Conceptual data contract

This is a logical contract, not a physical-table mandate. The build lane may choose physical names
after source and consumer census, but it must preserve these entities and relationships.

### 5.1 Reference entities

| Entity | Required identity / purpose |
|---|---|
| Model Definition | stable `model_id`, canonical name, owner, status |
| Model Version | `model_version_id`, effective range, target/rule contract, parent `model_id` |
| Model Classification History | `model_id`, `model_class = primary|custom`, effective range, decision authority |
| Strategy Definition | stable `strategy_id`, reusable mandate/process, status |
| Alternative Definition | stable `alternative_id`, canonical name, status |
| Portfolio Category Assignment | classified unit, `asset_category`, category-specific references, effective range, source |
| Client Mandate | `mandate_id`, client/household/account perimeter, effective range |
| Strategy Instance | `strategy_instance_id`, `strategy_id`, `mandate_id`, client-specific constraints |
| Sleeve | `sleeve_id`, mandate/instance, category-constrained optional model/alternative reference, effective range |
| Fee Arrangement | `fee_arrangement_id`, commercial scope, method, effective range, source |
| Fee Rule | rule/override selector, precedence, effective range, provenance |

The business discussion currently describes category assignment in account terms. The physical
assignment grain must preserve that account classification and may carry a more granular drilldown
on sleeves/lots when a non-Strategy account legitimately contains multiple registered products.
Strategy exclusivity is not provisional: if an account is `strategy`, the entire account is assigned
to exactly one `strategy_id` and no lower-grain record may carry a Model reference.

### 5.2 Normative classification schema

The successor contract is identified by:

```text
schema_id = portfolio_classification_v1
```

Its classification fields are:

```text
asset_category:
  models | strategy | alternative | client | insurance

model_class:
  primary | custom | null

model_id / model_version_id:
  registered identifiers | null

strategy_id:
  divz | idvz | pfoe | muni | tax | null

alternative_id:
  registered identifier, initially including aqr | null

alternative_class:
  private_equity | private_credit | hedge_fund | real_asset | null

selection_origin:
  opal | client | external_manager | unknown

advisory_scope:
  advised | excluded | null

fee_basis_status:
  included | excluded | null

fee_basis_method:
  market_value | average_daily_balance | period_end_value |
  not_asset_based | null
```

The string `unknown` remains valid only for `selection_origin`. For `advisory_scope`,
`fee_basis_status`, and `fee_basis_method`, the unknown/missing representation is SQL/JSON null and
may display as **Unknown**.

Category-specific nullability is binding:

| `asset_category` | Required | Must be null |
|---|---|---|
| `models` | `model_class`, `model_id`; version where applicable | `strategy_id`, `alternative_id`, `alternative_class` |
| `strategy` | exactly one `strategy_id` | `model_class`, `model_id`, `model_version_id`, `alternative_id`, `alternative_class` |
| `alternative` | `alternative_id`, `alternative_class` | `model_class`, `model_id`, `model_version_id`, `strategy_id` |
| `client` | no qualifier or drilldown | all Model, Strategy, and Alternative fields |
| `insurance` | no qualifier or drilldown | all Model, Strategy, and Alternative fields |

No v0 segment key (`etf_models`, `sma_strategies`, `custom_models`, or `non_model`) is valid in this
schema. No target payload may use `axis = segment_v1`.

### 5.3 Leaf attribution fact

At minimum:

```text
as_of_date
schema_id                    portfolio_classification_v1
client_id
household_id                 nullable until household canon is settled
account_id
mandate_id
strategy_instance_id         nullable
sleeve_id
asset_category               models|strategy|alternative|client|insurance
model_class                  primary|custom; required only for Models
model_id                     nullable
model_version_id             nullable
strategy_id                  nullable; one of divz|idvz|pfoe|muni|tax
alternative_id               nullable; initial registered value includes aqr
alternative_class            private_equity|private_credit|hedge_fund|real_asset; Alternative only
security_id
tax_lot_id                   nullable only when position grain is proven sufficient
attribution_weight
market_value
selection_origin
advisory_scope
fee_basis_status
fee_basis_method
fee_arrangement_id
fee_basis_value              null for not_asset_based or unknown/missing method
classification_confidence
source_system
source_vintage
written_at
```

### 5.4 Derived daily sleeve fact

The daily aggregation groups the leaf fact by sleeve and preserves all three axes. It does not infer
one axis from another. A model-backed sleeve may be client-originated; an advised sleeve may be
fee-included, fee-excluded, or unknown/null.

It also preserves `asset_category` and the applicable category-specific drilldown. Qualifier fields
that do not apply are null, not populated with `none`, `other`, or a duplicated category label.

---

## 6. Binding invariants and failure behavior

1. **One dollar, one leaf attribution.** A lot or position belongs to exactly one sleeve per date, or
   carries explicit fractional weights that sum to exactly 1.0.
2. **Exactly five business categories.** `asset_category` is one of
   `models|strategy|alternative|client|insurance`. `sma` is never a category value.
3. **Models are typed and promotable.** A Models record has exactly one effective-dated
   `model_class = primary|custom` and a registered `model_id`. Promotion changes the classification
   history without changing `model_id`.
4. **Strategy is exclusive and unqualified.** A Strategy account has exactly one registered
   `strategy_id`, no category qualifier, and null `model_id`/`model_version_id` at every lower grain.
5. **Alternative separates identity from class.** Alternative requires a registered
   `alternative_id` and one permitted `alternative_class`; `aqr` maps to `hedge_fund` initially.
6. **Client and Insurance are unforked.** Neither category has a qualifier or drilldown.
7. **Axes never substitute for one another.** Category, selection origin, advisory scope, and fee
   basis are independent facts.
8. **IDs, not labels.** Model, strategy, and alternative membership bind to stable IDs and, where
   applicable, versions.
9. **Effective dating is mandatory.** Category assignments, Model classifications, mandates, fee
   arrangements, and overrides all carry start/end vintages.
10. **Unknown goes loud.** Missing category evidence, selection, null advisory scope, null fee-basis
    status, or sleeve attribution is emitted with counts and value. It never silently becomes a
    high-confidence Client record or another business category.
11. **No semantic residual plug.** `non_model` may survive as a compatibility calculation, but it is
    not a canonical business classification.
12. **Cross-axis reconciliation.** Every rollup over the same perimeter and date reconciles to the
    same denominator and the five-category rollup is mutually exclusive.
13. **Null is not zero.** Missing classification or non-asset-based fee methods produce `null` where
    a numeric basis cannot be computed.
14. **No current MDPF widening by inference.** The A4 per-firm two-term residual and current served
    views remain unchanged until an explicit migration is ratified and exercised.
15. **Residual checks are controls.** `unattributed_value` and `unknown_value` are failure outputs,
    not segments to make a chart sum.

---

## 7. Worked examples

### 7.1 Tax Strategy account

```text
Account structure: SMA (common to all accounts; not a category)
asset_category = strategy
strategy_id = tax
Client implementation: Client A Tax Strategy, effective 2026-01-01

Sleeve A: tax-managed direct securities
  selection_origin = opal
  advisory_scope = advised
  model_id = null
  model_version_id = null

Sleeve B: client-contributed legacy low-basis securities governed by the Tax Strategy
  selection_origin = client
  advisory_scope = advised
  model_id = null
  model_version_id = null
```

Both sleeves reference the same `strategy_instance_id` and remain inside the `strategy` category.
No Intermediate, Cash, or other Model sleeve is permitted inside this account. Whether a sleeve is
fee-included comes from the client's fee arrangement, not from the Strategy category.

### 7.2 Primary and Custom Model lifecycle

```text
asset_category = models
model_id = fixed_income
model_class = custom
```

`fixed_income` is a branded Opal Model in limited, ad hoc production for large clients. If Opal later
promotes it, the same `model_id` remains in force and a new effective-dated classification begins:

```text
model_id = fixed_income
model_class = primary
```

Historical records before the promotion date continue to resolve to `custom`.

### 7.3 Client category with RSUs

The client's concentrated employer stock can be assigned `asset_category = client` without being
called Non-Model or Custom Model.

- The category has no qualifier or drilldown.
- The exposure has `selection_origin = client`.
- If Opal advises around the position, it is `advisory_scope = advised`.
- If the agreement excludes it from fees, `fee_basis_status = excluded`.

### 7.4 Alternative

```text
asset_category = alternative
alternative_id = aqr
alternative_class = hedge_fund
```

The manager/product drilldown and Alternative qualifier remain separate governed facts.

### 7.5 Insurance

```text
asset_category = insurance
```

No qualifier or drilldown field is populated.

### 7.6 External manager

An account supervised by another investment manager but incorporated into Opal's advice is:

```text
selection_origin = external_manager
advisory_scope = advised
```

Fee status remains independent and may be `included`, `excluded`, or `null` (Unknown).

### 7.7 Fixed-fee relationship

Assets within the commercial engagement may carry:

```text
fee_basis_status = included
fee_basis_method = not_asset_based
fee_basis_value = null
```

The absence of a numeric asset basis does not erase the relationship or fabricate a zero-dollar fee
base.

---

## 8. Binding v0 and interim-schema supersession map

### 8.1 Original MDPF_GLOBAL v0 taxonomy

| v0 concept / field | `portfolio_classification_v1` disposition | Migration rule |
|---|---|---|
| `etf_models` | `asset_category = models`, `model_class = primary` | Map only through the registered IDs for `ultra_short_term`, `short_term`, `intermediate_term`, `long_term`, and `ultra_long_term`. |
| `sma_strategies` | `asset_category = strategy` | Drop the nondiscriminating SMA label and resolve the account to exactly one of `divz|idvz|pfoe|muni|tax`. Model fields must be null. |
| v0 `custom_models` meaning “client-specific mix” | **No direct mapping to new Custom Models** | Reclassify the underlying account/sleeves from evidence across all five current categories. Never cast v0 `custom_models` to `model_class = custom`. |
| current `model_class = custom` | New concept under `asset_category = models` | Populate only from the branded Opal Model registry; initial example `fixed_income`. |
| `non_model` residual | No target business category | Resolve known assets to Strategy, Alternative, Client, or Insurance. Emit unresolved evidence through quality/null controls; do not load the residual as Client. |
| `axis = segment_v1` | Retired identifier | Do not reuse. Emit `schema_id = portfolio_classification_v1`. |
| v0 four-entry `segments` object | Retired payload shape | Emit governed classification rows/leaf facts using section 5.2; aggregate the five current categories only after leaf classification. |
| v0 four-term residual equation | Retired target logic | No new category is calculated by subtraction. Unattributed value is a control failure, not a segment. |
| A4 per-firm two-term `non_model` residual | Existing served compatibility calculation | Leave unchanged until separately ruled and migrated; it does not populate current `asset_category`. |

The phrase **Custom Model is a breaking semantic rename** between v0 and the current contract. In v0
it described a client-specific arrangement; now it describes a branded, stable Opal Model in limited
production. Automated name-based migration is prohibited.

### 8.2 Interim CRO-schema changes from Andrew's feedback

| Superseded interim rule | Current binding rule |
|---|---|
| `SMA` as a peer category | Prohibited; all accounts are inherently SMAs. Use the five current categories. |
| Strategy may contain Model-backed sleeves | Prohibited; a Strategy account is individual-security-focused and all Model fields are null. |
| `Custom Model` should be retired | Reversed; Custom is a valid branded Opal Model class. |
| `advisory_scope = managed` | Map to `advisory_scope = advised`; `managed` is not a valid target value. |
| `advisory_scope = unknown` | Store null and display Unknown. |
| `fee_basis_status = unknown` | Store null and display Unknown. |
| `fee_basis_method = unknown` | Store null and display Unknown when a display label is required. |

Migration must reject, count, and report every invalid enum, prohibited cross-category reference, and
unresolved v0 Custom/Non-Model record. It must never coerce those failures into a current category.

The successor five-category presentation must be derived from governed assignments and declare its
classification grain and denominator. A Strategy account cannot also contribute Model exposure, and
SMA must not appear as a peer category because it applies to the entire account population.

No frontend work is authorized here. Any future user-facing taxonomy requires its own product and
design review after the backend ontology is proven.

---

## 9. Current evidence and declared gaps

### 9.1 Grounded facts

- The five archetypal models already map one-to-one through stable `model_id` values.
- The current crosswalk contains five served model entries and two served SMA entries.
- Those two SMA entries are currently folded into the per-firm `non_model` residual.
- The inspected MDPF backend currently has no served Primary/Custom Model classification. The
  Andrew/Yang working-session direction establishes that distinction as a required design, with
  `fixed_income` as the initial Custom Model example.
- The proposed `segment_v1` contract is documentation-only: an exact-identifier scan across five
  repo roots (`org`, `data`, `portal`, `infra`, `docs`) found its contract identifiers only in the
  MDPF_GLOBAL PRD and project/registry records, with no producer or served schema.

### 9.2 Gaps that require discovery

1. The authoritative client/household/account mandate perimeter.
2. The source of record and effective dates for the five-category assignment.
3. Strategy-to-client assignment and effective dates across firms, including the complete mapping
   to `divz|idvz|pfoe|muni|tax`.
4. The registered Custom Model roster beyond the initial `fixed_income` example and the authority
   that approves Custom-to-Primary promotion.
5. The Alternative registry beyond `aqr` and the evidence for each Alternative qualifier.
6. Sleeve definitions and whether any source already carries stable sleeve identifiers.
7. Position-vs-lot attribution requirements, especially for Tax Strategy and legacy holdings.
8. Selection-origin evidence for retained, recommended, and externally managed assets.
9. Advisory-scope evidence and the system of record for `advised`, `excluded`, and null/Unknown.
10. Fee agreements, inclusion rules, methods, overrides, and effective dates.
11. Translation of legacy `full|model` fee scopes into evidence-backed selectors.
12. Whether an Opal Cash Model and other building-block models already exist operationally but are
    absent from the current MDPF crosswalk, and whether they qualify as Primary or Custom.

No vendor API call or other vendor egress was performed for this specification. Any future vendor
egress requires Andrew's explicit per-use authorization.

---

## 10. Opportunity: the Opal Portfolio Blueprint / Sleeve Attribution Ledger

The ontology points to a product-data opportunity larger than a taxonomy amendment: an effective-
dated system of record that answers, for every dollar:

> Under which client mandate and strategy does this exposure sit, which stable model or selection
> process produced it, who originated it, what is Opal's advisory role, and is it inside the fee
> arrangement?

Working name: **Opal Portfolio Blueprint**, implemented through a **Sleeve Attribution Ledger**.

Capabilities unlocked:

- mutually exclusive Models, Strategy, Alternative, Client, and Insurance reporting;
- correct Tax Strategy and client-asset representation without an SMA bucket;
- strategy-level and sleeve-level AUA/performance attribution;
- Primary-versus-Custom Model adoption, promotion, and penetration analysis;
- Alternative exposure analysis by both product and class;
- transition, drift, rebalancing, and concentrated-position analysis;
- separation of Opal-selected assets from client/external-originated advised wealth;
- fee-basis AUM derived from client agreements instead of firm-wide hardcoded labels;
- explicit unknown/unattributed exposure instead of the silent non-model plug;
- historical portfolio-construction lineage through effective-dated assignments.

---

## 11. Research and implementation workstreams

These are proposed workstreams and suggested capabilities, not lane dispatches.

### P0 -- Ontology ratification

- Ratify the definitions and canonical values in sections 2-4.
- Decide the remaining D-items in section 12.
- Select the canonical project relationship: MDPF_GLOBAL amendment or sibling project.

**Suggested capability:** CRO + Andrew/product and investment-operating SMEs; CTO reviews architecture.

### P1 -- Representative-client discovery

Build a labeled sample spanning, at minimum:

- each of the five high-level categories;
- Tax Strategy clients with legacy lots and no Model references;
- all five Primary Model drilldowns;
- `fixed_income` and any other Custom Models in limited production;
- `aqr` classified as `hedge_fund`;
- clients with RSUs or concentrated personal securities;
- externally managed assets inside Opal advice;
- all three current MDPF firms.

For every sample, draw the mandate -> strategy instance -> sleeve -> holding/lot graph and label all
three axes from evidence. Print the sample denominator and every unclassified dollar.

**Suggested capability:** CRO research + DS + investment/operations SME.

### P2 -- Source and authority census

Trace the required facts through SmartX, Eclipse/Orion, Black Diamond Rebalancer, Schwab 0824, Tax
Strategy operational data (including any legacy Tax SMA labels), CRM/advisory records, alternative
records, insurance records, and fee/billing agreements. Identify which source asserts each fact and
whether it carries effective dates.

**Acceptance:** source/field/authority/coverage table; no endpoint-name schema inference; uncaptured
bodies marked; vendor egress separately authorized.

### P3 -- Fee-arrangement contract

- Identify the commercial authority source.
- Model household/client/account applicability and sleeve overrides.
- Translate legacy `full|model` scopes against actual agreements.
- Exercise asset-based, fixed-fee, excluded-sleeve, and missing-agreement cases.

### P4 -- Gold ontology and ledger prototype

- Build reference registries for Models, Model Classification History, Strategies, and Alternatives.
- Build effective-dated five-category assignments and enforce category-specific nullability.
- Build effective-dated Mandate, Strategy Instance, and Sleeve identities.
- Emit the leaf attribution fact and daily sleeve fact.
- Preserve source vintage, confidence, and unknown states.

### P5 -- Verification and reconciliation

- One-dollar-one-leaf control.
- Cross-axis reconciliation to the same named AUA denominator.
- Historical effective-date tests.
- Custom-to-Primary promotion test that preserves `model_id` and historical Model class.
- Strategy exclusivity test: inject a Model reference into a Strategy account and require failure.
- Alternative test: `aqr` resolves independently to the `hedge_fund` qualifier.
- Synthetic unknown model, strategy, and sleeve plus null advisory scope and fee arrangement; every
  one must go loud.
- Tax-lot discriminating test where one security contains client-originated and Opal-originated lots.
- Fixed-fee test: included relationship, `not_asset_based`, null numeric basis.

### P6 -- Compatibility and migration

- Derive existing MDPF views from the new substrate without changing numbers.
- Compare the old `non_model` residual to the newly explained sleeve categories.
- Produce the five-category successor presentation only after contract ratification and parity tests.
- Retire compatibility fields only behind consumer census, parity proof, and never-widen gates.

---

## 12. Open decisions

| ID | Decision | Recommendation | Blocks |
|---|---|---|---|
| D-1 | Canonical mandate authority grain: household, client, account, or layered? | Layered: household/client mandate with explicit account applicability. | Physical schema |
| D-2 | Is lot-level attribution mandatory everywhere? | Support it canonically; permit position grain only when a discriminating source census proves sufficiency. | P4 |
| D-3 | Canonical meaning of “Custom Model.” | **Resolved by Andrew/Yang:** a branded Opal Model used for large clients in limited, ad hoc production; not a client-specific implementation. | Registry/migration |
| D-4 | Is Opal Cash already a stable model or a proposed one? | Require a versioned target/rule contract before registering it as a Model. | Model roster |
| D-5 | Authoritative source for advisory scope. | Determine in P2; do not infer solely from vendor model assignment. | P4 |
| D-6 | Authoritative source and precedence for fee arrangements. | Commercial agreement first; account/mandate rules and explicit sleeve overrides below it. | P3/P4 |
| D-7 | Full set of fee-basis methods. | Begin with the five values in section 3.3; extend only from observed agreements. | P3 |
| D-8 | What does current `full|model` mean contractually for each firm? | Re-derive from actual agreements and billed basis; labels alone are insufficient. | Migration |
| D-9 | Project placement. | Register a sibling Portfolio Blueprint project if P1 proves a durable cross-product ledger; otherwise amend MDPF_GLOBAL. | Build registration |
| D-10 | Exact physical grain for category/drilldown assignment when a non-Strategy account contains multiple products. | Preserve the account category and allow governed sleeve/lot drilldown; validate against real representative accounts in P1. Strategy remains account-exclusive regardless. | Physical schema |
| D-11 | Authority and criteria for promoting a Custom Model to Primary. | Effective-dated registry decision with named approver; retain the stable `model_id`. | Model governance |

---

## 13. Acceptance bar

The specification is implemented only when:

1. Every target record emits `schema_id = portfolio_classification_v1` and exactly one of
   `models|strategy|alternative|client|insurance`; `sma` and all four v0 segment keys are rejected as
   category values.
2. Models, Model Classification History, Strategies, Alternatives, Mandates, Strategy Instances,
   Sleeves, and Holdings/Lots exist as distinct effective-dated entities.
3. Every Models record resolves to `primary|custom`; Primary initially contains exactly the five
   archetypal IDs and Custom includes `fixed_income`.
4. A Custom-to-Primary promotion preserves `model_id`, changes only the effective-dated class, and
   reproduces correct historical classification on both sides of the effective date.
5. Strategy accepts only `divz|idvz|pfoe|muni|tax`, has no qualifier, and rejects every Model
   reference throughout the account.
6. Alternative preserves separate product and class fields; `aqr` resolves to `hedge_fund`.
7. Client and Insurance emit neither qualifier nor drilldown.
8. Every in-perimeter dollar resolves to exactly one sleeve attribution or an explicit loud unknown.
9. `selection_origin` emits only `opal|client|external_manager|unknown`.
10. `advisory_scope` emits only `advised|excluded|null`, with null displayed as Unknown.
11. `fee_basis_status` emits only `included|excluded|null`, with null displayed as Unknown; fee basis
   resolves through an effective-dated arrangement and separately emits method, authority, and
   numeric basis where applicable.
12. Fixed-fee relationships remain commercially included with `not_asset_based` and no fabricated
   numeric basis.
13. Category, strategy, model, origin, advisory, and fee rollups each reconcile to a named denominator
   without double-counting within the rollup.
14. The Tax Strategy discriminating example is represented as `strategy/tax`, with no Model
   references and no SMA category.
15. Client-retained RSUs and personal securities appear as known client-originated advised sleeves,
   not as an anonymous non-model plug.
16. Synthetic unknowns are exercised and visible by count and value.
17. Existing per-firm MDPF numbers remain unchanged until a separately ratified migration.
18. No served-output movement occurs without CTO/COO never-widen governance.
19. Migration tests reject v0 `custom_models` to new Custom Model casts, `managed` advisory scope,
    literal `unknown` advisory/fee states, Strategy/Model overlap, and every reuse of
    `axis = segment_v1` in a target record.

---

## 14. Non-goals and authority boundary

- No frontend or visualization design.
- No fee-rate, tiering, invoicing, waiver, or revenue-recognition engine.
- No rebalancer or trading implementation.
- No vendor egress without Andrew's explicit per-use authorization.
- No deployment, build-lane staffing, task-order dispatch, or served-output movement by CRO.
- No silent modification of the CTO-owned MDPF_GLOBAL PRD. This document is the research/design
  proposal that its owner can consume after ratification.

---

## 15. Immediate recommendation

Do not implement the existing four-term `segment_v1` residual. Ratify the five-category contract and
then label representative real accounts across Models, Strategy, Alternative, Client, and Insurance.
The decisive early deliverable is a small, evidence-backed Sleeve Attribution Ledger that enforces
Strategy/Model exclusivity, represents a Tax Strategy account, tracks `fixed_income` as Custom,
records `aqr` as a hedge fund, preserves client RSUs, and handles a fixed-fee relationship without an
SMA category or residual plug.
