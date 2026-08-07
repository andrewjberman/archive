# MDPF remediation register R-9 … R-12 — CONSUMER CENSUS

**`0.8.0_AE_CloudComp` · 2026-08-07 · TO `MDPF_REMED.W2-1` @e745552a63 · project `MDPF_CANPLAT`**
Register (PRD): `docs/architecture/MDPF_REMEDIATION_REGISTER.md` @e5e932caf6 §2c
**Measurement vintage: 2026-08-07T20:1x–20:4xZ.** Served artifacts read at `data-as-of 2026-08-05`.
**NOTHING WAS MOVED, RENAMED OR RETIRED. This document is evidence; the decisions are not mine.**

---

## §0 — THE FOUR ROWS, ANSWERED

| row | measured verdict | authorizes |
|---|---|---|
| **R-9** `last_updated` | **ZERO rendering consumers** (1 hit / 288 portal component files — and it is a comment saying *do not use it*). One **disabled** reader, one **live passthrough** in the served response shape. | a move — **but the passthrough is a contract change**, see §1 |
| **R-10** `inflection_non_model_aua` | **ZERO portal-source consumers** (0 SURFACED / 1,260 files, **positive-controlled**). Three **internal instrument** readers. | a decision — cost is internal gates, §2 |
| **R-11** five global-only fields | **ALREADY CLOSED — by ADOPTION, on 2026-08-05, two days before the register became the PRD.** | closing the row; nothing to retire |
| **R-12** pair-model blindness | **CONFIRMED AND MEASURED: 14 pairs served, 12 generated, 8 keys invisible by construction.** Two unrecognised artifact types, both LIVE. | a fix — §4 |

⚠ **THE ASYMMETRY GOVERNING THIS WHOLE DOCUMENT:** a PRESENCE verdict needs one hit; an ABSENCE
verdict authorizes retiring a client-facing field and needs exhaustiveness nobody fully has. Every
absence below carries its denominator and its blind spots (§5). Where I could not close a surface I
say **UNMEASURED**, not zero.

---

## §1 — R-9: `last_updated` (process clock in the business payload, all 4 scopes, `aum-metrics`)

**Confirmed present** at top-level in the served artifact, all scopes (`2026-08-05.json`, 9 top-level
keys: `_provenance, by_model, dates, last_updated, meta, non_model_assets_detail, period, scope,
total`). Written at `dim_mdpf_aum_metrics.py:439` and `:553` as `datetime.now(timezone.utc)` — a
**process** clock, exactly as the row says.

### The consumer census

| # | site | what it does | live? |
|---|---|---|---|
| 1 | `portal/src/contexts/DataSourceContext.tsx:104-106` | fetches `/aum/metrics`, reads `data.last_updated` | **NO — `enabled: false`** at `:110` |
| 2 | `portal/src/api/endpoints/aum.ts:395` | `last_updated: metricsData.last_updated` — **passes it into the response object** | **YES — live contract** |
| 3 | `portal/src/api/endpoints/aum.ts:125`, `:579` | type declarations (`last_updated?: string`) | type-only |
| 4 | `portal/src/pages/ModelPortfolios.tsx:567` | a comment: use `as_of_last`, **NOT** `metricsData.last_updated` | **negative reference** |

**Denominators.** `comp-find "last_updated" data/mdpf portal` → **77 hits / 1,317 files**
(DEF 2 · SURFACED 17 · CONFIG 17 · TEST 7 · DOC 34).
`comp-find "last_updated" portal/src/pages portal/src/components` → **1 hit / 288 files**, and that
one hit is #4 above.

### The finding that matters more than the count

**Andrew already ruled this field misleading for display.** `ModelPortfolios.tsx:563-572` records the
MDPF_CADENCE FE-label fix (**Andrew-sovereign 2026-06-08**): the page was deliberately switched to
stamp `as_of_last` because *"the process timestamp misleads (renders 'today') when the spine has
advanced but MDPF hasn't re-sampled."* **R-9 is asking whether to relocate a field whose display use
was already ruled against on exactly the grounds R-9 states.** That is not a new judgement call; it is
the same one, one layer down.

### ⚠ THE COST, AND IT IS NOT "NOTHING BREAKS"

Consumer #1 degrades **silently, in the wrong direction**:

```ts
const timestamp = data.last_updated || data.generated_at || new Date().toISOString()
```

If `last_updated` moves to `_provenance`, this does **not** error — it falls through to
`generated_at`, and failing that to **the client's own current time**. A stale "as of" would render
as **now**. It is `enabled: false` today, so nothing renders it *today* — but a future re-enable
inherits a silent wrong-timestamp path. **Consumer #2 is the real contract**: `aum.ts:395` puts the
field in the response object every caller of `getAUMMetrics()` receives, so the move is a
**served-shape change with an external surface**, which is precisely why the row says it needs
Andrew's word.

**RECOMMENDATION (evidence, not a decision).** The move is **safe on the rendering surface** and
**already aligned with a standing Andrew ruling**. Sequence it as: fix the `||` fallback chain at
`DataSourceContext.tsx:106` to fail loud rather than default to `new Date()` **before** the field
moves — otherwise the one consumer that could notice is the one guaranteed not to.
**Who decides: Andrew** (served-shape change). **Who executes: DE** (portal reader) then DS (emitter).

---

## §2 — R-10: `inflection_non_model_aua` (firm-named field at global scope)

**Present** in served `global/aggregate-aua-timeseries/2026-08-05.json`; it is the **only** top-level
global-only field remaining (§3). Enumerated in code as the ONE contract-ruled key-set exception —
`mdpf_gold_consolidator.py:106-112`, `R2_RULED_EXTRAS`, citing CONTRACT §B3 @a3106d585: *"ruled NOT
canonical … serves until Andrew rules retirement (NEVER#3)."*

### Census

- **Estate-wide:** `comp-find "inflection_non_model_aua"` → **360 hits / 24,893 files**
  (DEF 1 · SURFACED 22 · CONFIG 309 · TEST 1 · DOC 27).
- **Portal:** **248 hits / 1,260 files — ALL 248 in the CONFIG band, and every one under
  `portal/.runtmp/`** (scratch/runtime copies, not source). **SURFACED source hits: 0.**

> ✅ **POSITIVE CONTROL, run because a portal zero is what would authorize a deletion:**
> `comp-find "aggregate-aua-timeseries" portal` → **22 hits / 1,260 files with 8 SURFACED.**
> The portal-scoped search **does** find source when source exists. **R-10's zero is a MEASURED zero,
> not a broken search.**

### The real readers — all internal instruments, none client-facing

| reader | line | relationship |
|---|---|---|
| CVO layer-3 enterprise composition gate | `mdpf_revamp_cvo_layer3_enterprise_composition_gate.py:104,109` | **READS** it as the audit carrier; partial-row detection |
| DT parity check | `mdpf_parity_check.py:139,232,239,803,944-1032` | declares it `EXCLUDED_PARTNER_FIELD` / `_shape_extras.published_only` — **depends on its presence to exclude it** |
| `route_bindings.yaml` | `:117` (derived-audit note), `:119` (code-literal tie row) | reference rows — **pinned at `f999fb25f6`**, see §5 |
| gold emitters | `dim_mdpf_aggregate_aua_timeseries.py:2470`, `dim_mdpf_non_model_assets.py:171`, backfill `:667,:805` | **WRITE** it |

**RECOMMENDATION.** **Do not retire on this evidence — but the reason is not "a consumer might
exist."** It is that three internal instruments are *keyed on its presence*, including a parity check
that would have to be re-baselined and a CVO gate that reads it. The client-facing surface is clear
(0 portal source consumers, positive-controlled); **the cost is entirely internal and entirely
knowable.** If Andrew rules retirement, the ordered cost is: CVO gate → DT parity baseline →
`route_bindings` tie rows → `R2_RULED_EXTRAS` removal → emitters. **Who decides: Andrew**
(NEVER#3 + CONTRACT §B3 both reserve it). **This TO does not ask him.**

---

## §3 — R-11: the five global-only fields — **ALREADY CLOSED, BY ADOPTION, BEFORE THE REGISTER WAS ADOPTED**

The row is not enumerated anywhere in the register, so I derived the population from the served
artifacts across every available vintage.

| vintage | global keys | union-of-firms | **global-only** |
|---|---|---|---|
| 2026-07-27 | 19 | 15 | **6** |
| 2026-07-28 | 19 | 15 | **6** |
| 2026-07-29 | 19 | 15 | **6** |
| 2026-07-30 | 19 | 15 | **6** |
| 2026-08-03 | 19 | 15 | **6** |
| **2026-08-05** | **23** | **22** | **1** |

The 6 were: `account_count_total_raw`, `count_as_of`, `count_basis`, **`inflection_non_model_aua`**,
`opal_aggregate_aua`, `point_class`. Removing R-10's field — which the register correctly splits out
into its own row — leaves **exactly the five R-11 names.** The row's count is right.

**MECHANISM — adoption, not deletion.** Measured directly:

| vintage | global | inflection | 49financial | cottonwood |
|---|---|---|---|---|
| 2026-08-03 | **5/5** | 0/5 | 0/5 | 0/5 |
| 2026-08-05 | **5/5** | **5/5** | **5/5** | **5/5** |

The five did not go away — **the firm scopes gained them.** The shape is now uniform across all four
scopes, so the fields are canonical by the L-1 test the row invokes, and there is nothing left to
classify or retire.

**RECOMMENDATION: close R-11 as RESOLVED-BY-CONVERGENCE.** No consumer census is owed, because
"retire a global-only field" is moot for a field present at every scope. **Cost of closing: zero —
nothing moves.** ⚠ Worth one line in the register: **the row described a condition that ended
2026-08-05, and the register became the PRD on 2026-08-07** — it was stale on adoption. Not anyone's
error; the estate fixed itself in between. **Who decides: COO** (register hygiene).

---

## §4 — R-12: the pair-model blindness — **CONFIRMED, AND THE ROW NAMES THE WRONG MECHANISM**

### The model, read from source (not retyped)

`data/mdpf/scripts/gold/mdpf_gold_consolidator.py`:
- `:89` `SCOPES` = 4 — `49financial, inflection, cottonwood, global`
- `:91` `ARTIFACT_TYPES` = 3 — `aggregate-aua-timeseries, aum-metrics, account-distribution`
- `:968` `a4_expected = len(SCOPES) * len(ARTIFACT_TYPES)` → **12**
- `:999` completion log: `emitted / a4_expected`

### The actual key listing — `s3://opal-data-assets/portal/gold/mdpf/`

Full pagination, materialised, counted client-side (never `--query length()`):
**68 keys = 66 artifact + 2 manifest.**

| | |
|---|---|
| pairs the model GENERATES | **12** |
| pairs ACTUALLY SERVED | **14** |
| generated-but-absent | **0** |
| **UNRECOGNISED — invisible by construction** | **2 pairs / 8 keys** |

### The unrecognised keys, BY NAME

```
portal/gold/mdpf/cottonwood/account-units/2026-07-20.json      artifact-type 'account-units'
portal/gold/mdpf/cottonwood/account-units/2026-07-24.json          NOT in ARTIFACT_TYPES
portal/gold/mdpf/cottonwood/account-units/2026-07-31.json
portal/gold/mdpf/cottonwood/account-units/2026-08-03.json
portal/gold/mdpf/cottonwood/account-units/2026-08-05.json
portal/gold/mdpf/global/non-model-assets/2026-07-27.json       artifact-type 'non-model-assets'
portal/gold/mdpf/global/non-model-assets/2026-08-03.json           NOT in ARTIFACT_TYPES
portal/gold/mdpf/global/non-model-assets/2026-08-05.json
```

**Both are LIVE, not abandoned.** Newest key for each is **2026-08-05** — the same vintage as ten of
the twelve recognised pairs (two recognised pairs are fresher, at 08-06). Something writes these
every cycle and it is not this consolidator.

### ⚠ THE ROW'S CONCLUSION IS RIGHT AND ITS NAMED MECHANISM IS NOT

R-12 says the model *"normalises `_` and `-` variants to one type."* **No underscore normalisation is
involved in a single one of the 8 invisible keys** — `account-units` and `non-model-assets` are both
already hyphenated. I found no `_`→`-` normalisation in `data/mdpf` (measured zero over 57 files).

**The operative mechanism is different and worse: the model is GENERATIVE, never OBSERVATIONAL.** It
builds keys from a closed hand-written tuple and then compares *what it built* against *what it
intended to build* — `emitted` vs `a4_expected`, **both derived from `SCOPES × ARTIFACT_TYPES`.**
Nothing ever lists the A4 prefix. So the check reads a clean **12/12 green** while 8 live keys sit
outside its universe entirely. **Two instruments that share a derivation cannot cross-check each
other**, and an artifact type absent from the tuple is not "missed" — it is *unaskable*.

This matters for the fix: **"add `_`/`-` variant handling" would close nothing.** The closure is to
make the completeness check **observational** — list the prefix, compare against the model, and
surface unrecognised types by name.

*(Same shape as R-29, one row over: a correct conclusion carried on a wrong key. And the same shape
as my own NFRA_PYFIELD finding this morning — a normalisation hiding a population.)*

**RECOMMENDATION.** Replace the generated `a4_expected` with a listing-derived check that fails loud
on an unrecognised `(scope, artifact-type)`. **Cost: contained** — one function in
`mdpf_gold_consolidator.py`, no served shape touched, no field moved. **What breaks if left as-is:**
nothing today; the check simply cannot report on 8 live keys, and any future artifact type is
invisible on arrival. **Who decides: CTO** (it is a gate change). ⚠ **Do NOT let "fix R-12" become
"delete the two unrecognised types" — they are live at current vintage and their producer is
unidentified. Identifying that producer is the prerequisite and is NOT in this TO.**

---

## §5 — BLIND SPOTS (named, per the TO's absence rule)

| surface | status | why it matters |
|---|---|---|
| main repo (tracked) | **MEASURED** — denominators printed per query above | |
| **portal submodule** | **MEASURED** — searched explicitly and **positive-controlled** (§2) | the control is what makes R-10's zero usable |
| `portal/.runtmp/**` | **EXCLUDED, DECLARED** — 248 R-10 hits live here; scratch, not source | excluded deliberately, not silently dropped |
| **deployed-but-uncommitted code** | ⛔ **UNMEASURED** | a deployed portal bundle or Lambda could read a field no committed source mentions |
| **another device's tree (site Z)** | ⛔ **UNMEASURED** | out of reach from this device by construction |
| **external callers of `/aum/metrics`** | ⛔ **UNMEASURED** — and **R-9 is in that response shape** (`aum.ts:395`) | the one surface where R-9's absence verdict is weakest |
| `route_bindings.yaml` | **PINNED, not blind** — `f999fb25f6` | see below |

**`route_bindings.yaml` — collision honoured.** `0.4.0_DS_ClientPlatform` held the file under W1-1
during this census. I did not read it mid-edit and did not edit it. They answered **from the diff,
not recollection**: their hunks span only `:58-83` (the 49F `custody_leg` block) and **do not touch
`inflection_non_model_aua` or any leg pin**; the reference rows sit at `:117`/`:119`, outside every
hunk. They ran their own positive control so their zero-in-diff discriminates.
**Settled vintage `f999fb25f6`, and it is UNPUSHED** — resolving via `origin/CLOUD` shows the
superseded ddb-cohort row. ⚠ **DS also flagged that their commit adds one PROSE mention of
`aggregate-aua-timeseries` at `:62`** (a citation inside `authority:`, not a reference), which would
move a textual count by +1 for no real change. **My §2 count does not include it** — I counted
reference rows, not string occurrences.

---

## §6 — WHAT THIS DOCUMENT DID NOT DO

**Nothing moved.** No served field renamed, relocated or retired. No gold or silver script modified.
No alert, checker or monitor built. `route_bindings.yaml` untouched.
R-9 needs **Andrew's word**; R-10 needs a **canonical-or-not decision on this evidence**; R-12 needs
a **CTO gate ruling**; R-11 needs only a **register edit**. Producing the evidence and taking the
decision are different acts, and this was the first.
