# SMARTX_BD_EXACT_JOIN — spec + residual census + the U1 model-identity edge

**TO:** `D3_MODELOVERLAY.TO-D3.1` · **Author:** `0.4.0_DS_ClientPlatform` · **2026-08-19**
**Authority:** `D3_ACCOUNT_MODEL_OVERLAY_PRD.md` §4.1 + §6 item 1 @52a85baf08; taxonomy-owner
ruling `4.0.0_SA_CRO~A` ~20:45Z (adds D3.1-6).
**Machine-readable contract:** `data/_contracts/smartx_bd_join_disposition.yaml` (v1.0).

> **Every number here is MEASURED at this seat on 2026-08-19** against the live
> `fact_allocation_account_map` (as_of 2026-08-19) and `fact_acc` (as_of 2026-08-18), via
> `a06_dim_identity_crosswalk.build_crosswalk`. Denominators are printed beside every figure.

---

## 1. Purpose, and the bar

Drive the measured end-to-end join to **100%-CLASSIFIED**: every allocation row either joins or
carries an explained residual class. *Perfect = joined + explained-residual = denominator, zero
silent drops.* **That bar is met today** — see §3.

---

## 2. The measured coverage

| quantity | value | denominator |
|---|---|---|
| allocation map rows (post-dedup) | **7,305** | — |
| 49F `fact_acc` universe accounts | **7,316** | — |
| feed → map (key derivable) | **7,289** | 7,305 → 0.9978 |
| end-to-end (resolves to a 49F account) | **7,286** | 7,305 → 0.9974 |
| residual | **19** | 7,305 → 0.26% |
| distinct models on the U1 edge | **8** | — |

**REVERSE DIRECTION, measured because a join has two sides and the TO asks for accounts
*examined*, not only accounts that failed:** 5,741 of 7,316 universe accounts (78.47%) carry at
least one allocation; **1,575 (21.53%) carry none.** ⚠ **That is NOT prima facie a defect** — a
49F account with no SmartX allocation is the *expected* state for a non-model account. It is
reported here because it is the account-side coverage number, and it is deliberately **not** a
value on this spec's axis (§4, `NO_SMARTX_ALLOCATION`).

---

## 3. The residual, fully classified — 19 of 19, zero unexplained

| class | rows | distinct | share |
|---|---|---|---|
| `KEY_OUTSIDE_ACCOUNT_GRAMMAR` | 16 | 13 | 0.22% |
| `KEY_VALID_ACCOUNT_ABSENT` | 3 | 3 | 0.04% |
| `UNRESOLVED` | 0 | 0 | 0.00% |

**`KEY_OUTSIDE_ACCOUNT_GRAMMAR` — the keys are 9-digit, and the exclusion is structural.**
All 16 are 9-digit numerals — not empty, not malformed, not UUID-shaped. The universe is
**7,316 of 7,316** ten-character `00`-leading ids, i.e. *exclusively* zfilled 8-digit accounts,
with **zero** native 9- or 10-digit members.

> **RELAXED-JOIN CONTROL — I tested whether the `\d{8}` filter was manufacturing this residual,
> because that is the difference between "unresolvable" and "resolvable-but-in-the-residual":**
> zfilling the 13 distinct 9-digit values to 10 and testing membership yields **0 of 13** present.
> **POSITIVE CONTROL:** 50 of 50 known 8-digit keys *are* present, so the membership test
> discriminates. **NEGATIVE CONTROL:** synthetic `9999999999` absent. The filter is **not**
> manufacturing the residual — these keys genuinely cannot exist in this universe.

**`KEY_VALID_ACCOUNT_ABSENT` — well-formed keys, missing accounts, and 2 of 3 are *departures*.**
Specimens `0010299365`, `0099250989`, `0041879643`. Read across **532** `fact_acc` partitions
(2024-07-08 … 2026-08-18): **2 of the 3** (`0041879643`, `0099250989`) were present in the
2024-07-08 universe and are absent from every recent partition — **departed accounts still
carrying an OPEN SmartX allocation.** The third was present at neither end.

> That departed-vs-never-present split is recorded in the `evidence` field and **deliberately not
> as an enum value** — it is a *cause*, and putting cause on an outcome axis is the Rule 24(iii)
> break this spec exists to avoid.

---

## 4. The enum, and what was rejected

Full contract: **`data/_contracts/smartx_bd_join_disposition.yaml`**. Rule 24 declaration:

- **Intent (24-iii):** join-resolution **OUTCOME ONLY**. Not cause, not lifecycle, not custody,
  not attribute provenance.
- **Grain (24-ii):** one **allocation map row**, `(allocation_id × as_of)`.
- **MECE (24-i):** `7,286 + 16 + 3 + 0 = 7,305` — arithmetically exhaustive against the printed
  denominator, and the tests are structurally disjoint.

**PRD §4.1 proposed seven values. Four are rejected and two renamed — each on a measured basis,
not a style preference:**

| proposed | disposition | measured reason |
|---|---|---|
| `NO_SMARTX_ALLOCATION` | **rejected — wrong grain (24-ii)** | A property of an *account*, not of an allocation row; there is no row to carry it. Measured separately: 1,575 / 7,316. Belongs on an account-side axis. |
| `CLOSED` | **rejected — mixes lifecycle with outcome (24-iii), and classifies nothing** | The map holds **zero** `close` rows (7,279 `open` + 26 `workingClose`). All 19 residuals are `open`; all 26 `workingClose` **joined**. No members, no mechanism to acquire members. |
| `OTHER_CUSTODIAN` | **rejected — a cause, not an outcome (24-iii), and it would be INFERRED** | Nothing in the data names a custodian. Asserting one is a hypothesis wearing a value's clothing. |
| `NON_8DIGIT_KEY` | **renamed** → `KEY_OUTSIDE_ACCOUNT_GRAMMAR` | Named the *test*, not the *outcome*; invites "pad it and retry", which the relaxed-join control shows finds nothing. |
| `NOT_IN_ACCOUNT_UNIVERSE` | **renamed** → `KEY_VALID_ACCOUNT_ABSENT` | Ambiguous — a 9-digit key is *also* "not in the universe". The new name pins the discriminating fact. |
| `JOINED`, `UNRESOLVED` | **retained** | `UNRESOLVED` is held at 0 deliberately: it is the collectively-exhaustive guarantee, and per §4.1's error case an `UNRESOLVED` count > 0 is a published number, never a dropped row. |

### 4.1 Stability frame (24-iv) — **the axis SPLITS, and that must be said out loud**

| value | moves under an account-universe refresh? |
|---|---|
| `KEY_VALID_ACCOUNT_ABSENT` | **YES** — coverage/vintage condition |
| `KEY_OUTSIDE_ACCOUNT_GRAMMAR` | **NO** — unreachable by any refresh |

No refresh of a universe composed entirely of zfilled 8-digit ids can *ever* admit a 9-digit key.
Its remedy is a **scope decision** (do these accounts belong to 49F; is a second custodian grammar
in play), a different act with a different owner.

> **Consequence, stated because a schema whose members need different remedies presents as one
> workstream and is several:** a plan that says *"refresh the account dimension and the residual
> clears"* covers **3 of 19** rows and **structurally cannot reach the other 16.**

---

## 5. U1 — the model-identity edge, **ANSWERED**

The PRD records U1 as *"NOT yet located"*. It is located, and it is complete.

**Table:** `smartx/platform/silver/fact_model_allocation_roster` — carries
`allocation_id → model_id / model_name` (+ `rmid`, advisor block, `value`, `status`, `opened_ts`).

**Source, with vintage** (a line citation without a vintage is not a citation):

- `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py:328-330` **@`3e4e1843505c2f531e2d6c7ccf53fe7e1deff55c`**
  — the edge itself: `"model_id": mdl.get("id")`, `"model_name": mdl.get("name")`,
  `"allocation_id": r.get("allocationId")`.
- `…/silver.py:342` — `model_allocation_roster_frame()`, *"dtype + dedup ONLY (Rule 17). Natural
  key: (allocation_id, run_date)"*.
- `…/silver.py:152` — `MODEL_ALLOCATION_ROSTER_TABLE_NAME`.
- `…/silver.py:361-367` — the conflicting-rows guard on `(allocation_id, run_date)`.

**Measured coverage of the edge (date=2026-08-19):**

| quantity | value |
|---|---|
| roster rows / distinct `allocation_id` | 9,783 / **9,783** (1:1, 0 duplicates in-partition) |
| crosswalk allocations **with** a model identity | **7,305 / 7,305 = 100.00%** |
| **joined** crosswalk allocations with a model identity | **7,286 / 7,286 = 100.00%** |
| roster allocations not in the crosswalk | 2,478 |
| distinct models | 8 |

> **U1 is not a gap — it is a complete edge.** §4.2's `account_model_membership` producer can be
> built on it today. The 2,478 roster-only allocations are explained by status: the roster carries
> 2,475 `close` + 26 `workingClose` + 7,282 `open`, while **the allocation map carries no `close`
> rows at all** — so the map is already filtered to non-closed allocations.

**⚠ Two homes, flagged not chased:** this file exists at
`infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py` **and**
`infra/aws/lambda/smartx_assets_pull/silver.py`, **byte-identical today** (md5
`c9d400dcdacce9411a8ddaa4dc48aa7e`). Latent Rule-22a shape: a filename-resolved check reads clean
right up until they diverge.

---

## 6. Bucket discipline

`08242234` = **MDPF / SmartX**; `08335338` = **ADVI / Black Diamond**. Full 8 digits throughout —
the 4-digit prefix is what makes the two confusable (`0824`/`0833` differ in 2 characters; the
full forms in 6).

---

## 7. Open items — routed, not silently held

1. **`SYSTEM_DEFINITIONS` registration (D3.1-6) is AUTHORED, NOT LANDED.**
   `infra/system/**` is `ANY_EXEC_OR_AE` in `.owned-paths.yaml`; DS is neither, and my only carve
   there is `06_current_state*`. The entry is drafted at
   `…/deliverables/SMARTX_BD_JOIN_DISPOSITION_SYSTEM_DEFINITIONS_ENTRY.yaml` and routed to CRO —
   who is both the taxonomy owner and the definitions lead under the ontology lock-down
   (Andrew-direct 2026-08-19 ~1852Z @1044c49f2e). **The `status:` value is the registry owner's to
   set: landing it IS the ratification, and it is not mine to self-assert.**
2. **The 16 `KEY_OUTSIDE_ACCOUNT_GRAMMAR` rows need a scope decision**, not a data fix. Owner
   unassigned. Question: are these 49F accounts at all, and is a second custodian grammar in play?
3. **The contract is `DRAFT-FOR-RATIFICATION`** — CTO gates cross-package contracts, and D6/TO-G
   is a declared reader. Not self-ratified.
4. **Account-side coverage axis** (the 1,575) is named but not designed here — it is a different
   grain and therefore a different axis.
