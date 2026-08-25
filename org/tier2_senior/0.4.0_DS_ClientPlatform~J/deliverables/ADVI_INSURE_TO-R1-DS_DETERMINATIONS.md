# ADVI_INSURE.TO-R1-DS — DETERMINATIONS (AC2 design · AC4 · AC6)

**seat:** `0.4.0_DS_ClientPlatform~J` · **2026-08-25** · **issuer:** `2.0.0_SA_COO`
**decomp:** `workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY.**

> **READ THE LAYER BEFORE READING THE VERDICT.** Everything here is **DESIGN / SOURCE** layer.
> **No claim in this file is an APPLIED claim about an insurance artifact, because no insurance
> artifact exists** — 0 insurance-bearing keys over **480,954** fully-walked keys across four
> named trees, positive control `allocation` = 416. Committing is not executing, and designing
> is not either.

---

## AC2 — the gold table, DESIGN-COMPLETE / APPLIED-GATED

**Table:** `{49F-gold-bucket}/gold/advi/insurance/insurance_nav_current/date={D}/`
**Grain:** one row per (`bd_account_id`, `as_of_date`). Additive; a new row only when
`as_of_date` advances; a value change on a **closed** `as_of_date` is a **CONFLICT — refuse
loudly, never rewrite.**

**Own subtree, deliberately not under `canonical/`.** `canonical/` is the asset-management
contract and the agentic-query root; an enumerator over `canonical/*` would blend **by
adjacency** exactly what `INS-inv-1` forbids. **Never-blend holds by construction only when the
tables do not share a prefix** — anywhere else it holds by discipline, and discipline is not a
control.

### The spine, measured leg by leg (`date=2026-08-24`)

| leg | mechanism | measured |
|---|---|---|
| BD-native → Opal `account_id` | JD2 `dim_advisor_fee_role` carries **both** `bd_account_id` (e.g. `z0817426091`) and `account_id` (10-char zero-padded) | 5,337 distinct each · **ID JOIN EXISTS** |
| `account_id` → `relationship_id` | `dim_relationship` (7,357 rows / 14 cols) | **7,356 of 7,382 = 99.65%**; **26 unassigned** · **ID JOIN EXISTS** |
| firm | constant on this tree | carried, not derived |
| **advisor** | — | ⛔ **`NOT-DERIVABLE-UPSTREAM`** |

⛔ **THE ADVISOR LEG IS DECLARED ABSENT PER COO RULING 70462.** Measured: **0 of 95 columns**
across `dim_account` (37) + `dim_relationship` (14) + JD2 (44) match an advisor-identifier
shape. Every advisor handle is a name string, in two mutually unparseable formats —
`'ANDERSON  ROY CLAYTO'` (UPPER, LAST-FIRST, double-spaced, 20-char truncated, **9 distinct
over 7,202 rows**) versus `'Campbell Huber'` (Title Case, First Last, 141 distinct). **Nine
distinct values cannot carry 141 implementors**, so the first is very likely not an advisor
field at all — *stated as a read, not asserted as a fact; I did not confirm it.*

The row therefore carries `advisor_basis = 'NOT-DERIVABLE-UPSTREAM'` **with the reason
recorded**, and **no name-string join is performed.** A name match across a 160,091-row dim is
a silent-collision generator — it returns a plausible number instead of an error. **An honestly
missing leg beats a leg that is right most of the time.** The issuer independently re-ran this
census over a deliberately wider net and the finding survived.

Unresolvable rows take `spine_class = 'unassigned'` and are **NEVER dropped**; a dropped row
silently shrinks the denominator of every figure above it.

### ⚠ The untestable premise, recorded rather than buried

JD2's `roles_source` and `fee_source` are both the single value `bd-49f-allocation_390224` —
**the asset-management allocation feed.** Insurance accounts arrive from a *different* BD
endpoint. **So the insurance cohort's overlap with JD2's 5,337 accounts may be low or zero, in
which case `unassigned` is the DEFAULT rather than the edge case**, and the spine aggregation
that AC2, `INS-inv-3` and the Books rollup all rest on would resolve for almost nobody.

⛔ **Nobody can measure this today** — the cohort does not exist. It is an **untestable premise
of the design**, not a defect. **Cheapest disarm, and the moment is about to pass:** one line in
`INS-a-1`'s oracle — *print how many exported `bd_account_id` appear in JD2 at `is_current`,
with the denominator* — answers it before any gold code is written. Filed to CVO as an
OBSERVATION; the disarm act belongs to the surface-(a) lane, not to this seat.

---

## AC3 — forbidden-field census

Predicate: `insurance_forbidden_field_census.py` (in this folder). **Exercised, rc=0.**

```
CONTROL neg (clean schema, must be 0):  0 -> OK
CONTROL pos (3 planted, must be >=3):   3 -> OK
DESIGNED SCHEMA: 14 columns scanned, 0 violations, CLEAN
```

**Both control arms are reachable from different truths** — the negative arm returns clean on a
good schema, the positive arm returns dirty on a planted one, and the module **refuses to report
a verdict at all** unless both hold. A census nobody has seen fail proves nothing.

Word-boundary token matching, never substrings: this estate has a measured case where a
case-insensitive substring search returned 19 hits that were **all** a longer unrelated word.
Every hit is printed for reading, because a count nobody reads is a count of the pattern's
accidents.

**BEFORE baseline for `INS-inv-1`:** `AC3_AM_BYTE_IDENTITY_BASELINE_BEFORE.json`, committed
`4d40f0d1c8` — 12 served objects, **sha256 over the full GET body, not ETag** (a multipart ETag
is not a content hash; 0 of 12 are multipart today and the method does not depend on that
holding). `last_modified` + `etag` recorded per key so the AFTER can **discriminate "the
publisher re-ran" from "insurance moved an AM figure."** Only the second falsifies the design.

⚠ **Declared honestly:** `timeseries_chart.json` and `timeseries_chart_full.json` are
**byte-identical** (same sha256, 7,260,521 B) though the emitter documents them as a divergent
pair. **The benign explanation — the series' full domain is inside the truncation window, making
truncation a correct no-op — is at least as likely as a defect, and I am not calling it one.**
Consequence for my own instrument: the AFTER comparison has **at most 11 independent figures,
not 12**, and I will quote that denominator rather than 12.

---

## AC4 — platinum: one json, one producer, and a MINT

**Key:** `opal-data-portal-v2/platinum/advi/49financial/insurance_nav.json`, emitted as an
`EMITTERS` entry in `d_publisher_port.py`.

**ONE PRODUCER PER SERVED KEY — by construction, not by promise.** Source-read:
`d_publisher_port.py:61-62` pins `SERVE_BUCKET` / `SERVE_ROOT`; `:466` builds every write as
`f"{SERVE_ROOT}/{row['leaf']}"`; `:530-533` **refuses unknown keys** against the `EMITTERS`
registry. The writer cannot address a key outside its own serve root, so a second producer for
this leaf is not something to avoid — it is **unreachable through this path.**

*The estate's live counter-example is why this matters: two emitters writing one served key with
disagreeing cache headers, resolved only by write order.*

### ⛔ NEVER#3 DETERMINATION — stated positively so nobody re-derives it under pressure

**This MINTS a served key. It does not move one.** Measured this session: `platinum/advi/49financial/`
holds **12 keys**, fully walked, **none insurance-bearing**.

> **A MINT NEEDS NO NEVER-WIDEN SIGN-OFF. MOVING OR REPOINTING AN EXISTING SERVED KEY DOES.**
> **No sign-off is owed here, and I am not manufacturing one** — an agent-invented approval step
> is invisible to the person it delays.

**What WOULD attach NEVER#3, named so the boundary is not blurred later:** repointing any of
those 12 existing keys, changing a route that serves them, or relocating the insurance leaf once
published. None is in this TO.

---

## AC6 — the moratoria and the categorical exclusions

| prohibition | this TO's compliance | basis |
|---|---|---|
| no alarm / SNS / SES / monitor / freshness-checker | **NONE built, none proposed.** `INS-c-3`'s cadence work is a **printed census from observed `as_of_date` history — nothing standing** | standing moratorium |
| no shadow path / parallel emitter / standing comparator | **NONE.** One landing prefix, one gold table, one platinum leaf, one producer | build correctly once and port |
| Advisor tab + Distribution tab OUT, categorically | **No cell of mine touches either.** My 14 cells are inv/b/c/d/f — the frontend plane (e) is excluded to another lane entirely | `INS-inv-3`, `INS-g-3` |

⛔ **The freshness distinction that keeps this from becoming a monitor:** `INS-c-3` measures each
account's **statement cycle** from its own observed `as_of_date` advances — monthly, quarterly, or
unknown — and **serves `as_of_date` as a field.** It does not compare that date to wall-clock, it
does not hold a threshold, and it raises nothing. **The consumer sees the statement date and
judges; the pipeline does not judge for it.** This plane is explicitly **NOT `T-1`** — a
statement-cycle asset is not a trading-calendar asset, and treating it as one would manufacture a
false outage every single day between statements.

---

## STATUS AT THIS WRITING

| criterion | layer | status |
|---|---|---|
| AC1 landing | APPLIED | ⛔ **UNCOMPUTABLE-BY-DEPENDENCY** — `INS-a-1..3`, surface (a), excluded to the ETL lane. 0 source bytes exist |
| AC2 gold table | DESIGN / APPLIED | **DESIGN-COMPLETE** · APPLIED-GATED behind AC1 |
| AC3 forbidden fields + baseline | EXERCISED | **DESIGN-CLEAN, controls held, rc=0** · BEFORE baseline captured and committed |
| AC4 platinum + NEVER#3 | APPLIED | **DETERMINED** (mint, one producer by construction) · emission APPLIED-GATED behind AC2 |
| AC5 pattern record | SOURCE | **DELIVERED** — `ADVI_INSURE_PATTERN_RECORD.md`, 0 cot prefixes with a firing positive control, all four required items named |
| AC6 moratoria + exclusions | SOURCE | **SATISFIED** |

**Nothing here is blocked overall. One criterion and one spine leg are** — and both are declared
with the dependency named, not absorbed and not quietly descoped.
