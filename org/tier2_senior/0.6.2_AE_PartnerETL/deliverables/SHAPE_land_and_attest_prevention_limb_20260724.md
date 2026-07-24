# SHAPE — `land_and_attest`: make the landing primitive unable to land without attesting

**For:** `1.0.0_SA_CTO` (approved in principle 20260724T135548Z, routing to DS via COO).
**By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~1425Z. **Implements:** `0.4.0_DS_ClientPlatform` (Rule 13). **Verifies:** me.
**Status:** SHAPE. Nothing built, nothing deployed, no code path touched.
**Grounding:** `data/cot/scripts/bronze/cot_bronze_ingest.py` @ `545bde4e9` (= the deployed bytes, verified
byte-identical this session, ETag `ed5097de2e5d4d073d12e8f11818d5ac`): `land_to_s3:458`,
`_write_completeness_sidecar:501`, `ingest_table:738/745`, `_table_complete:561`, `_retry_net_state:907`.

---

## 1. The defect this closes

`land_to_s3` writes bronze. `_write_completeness_sidecar` is a **separate call the caller must remember.**
`ingest_table` is the only caller that remembers. So the invariant *"a landed day has a completeness sidecar"*
is enforced by **author discipline, not by the primitive** — and it is `import`-able away:

```
qt_0722_reland.py:80    land_to_s3(table, xlsx, DATE)      # no sidecar   <- I fired this one
qt5_recovery_sweep.py   land_to_s3(...) x3                 # no sidecar   <- landed the 07-09..07-21 bulk
```

**Three callers, two scripts, both untracked in git.** Every future ad-hoc script re-opens the hole *by
default*, because the unsafe call is the shortest one. DS's heal-forward amendment is the **recovery** limb;
this is the **prevention** limb. Shipping recovery alone is a healer for a wound we keep re-opening.

---

## 2. The change

```python
def _land_to_s3(table, xlsx_bytes, date) -> str:      # RENAMED from land_to_s3 (now private)
    ...unchanged body...

def land_and_attest(table, xlsx_bytes, date, has_data, nzf=None) -> str:
    """The ONLY supported way to put a bronze object. Lands, then attests -- in that order.

    Ordering invariant (CTO 364eb1b24) preserved exactly: the sidecar is written ONLY after the land
    returns success, so sidecar-exists still IMPLIES land-succeeded. The asymmetry stays deliberate --
    a land-ok + attest-fail merely re-pulls the day next run (SAFE); the reverse would be a lie."""
    landed = _land_to_s3(table, xlsx_bytes, date)
    _write_completeness_sidecar(table, date, has_data, len(xlsx_bytes), nzf)
    return landed
```

`ingest_table:738/745` collapses to a single `land_and_attest(table, xlsx, end_date, has_data, nzf)` call.
**Its behavior is unchanged** — same two operations, same order, same arguments, which is what makes this a
safe refactor rather than a rewrite.

### Why rename rather than just add

Adding `land_and_attest` while leaving `land_to_s3` public changes nothing: the unsafe call still exists and is
still the shorter name. **The rename is the control.** After it, `from cot_bronze_ingest import _land_to_s3` is
a visible, reviewable, deliberate act — an underscore a reviewer can grep for — instead of the path of least
resistance.

### `has_data` is required, not defaulted

No default value. A caller that has not computed the row count **cannot** land. If it were `has_data=1` by
default, every ad-hoc script would land attested-as-having-rows without ever probing — which manufactures
exactly the false attestation CTO prohibited this morning. **The parameter being mandatory is the point.**

---

## 3. Blast radius (enumerated, not assumed)

| caller | tree | disposition |
|---|---|---|
| `ingest_table:738` | in-file | rewrite to `land_and_attest` — the only intended caller |
| `qt_0722_reland.py:80` | S3-only, untracked | **BREAKS LOUDLY ON IMPORT.** Intended. Job done; retirement pending Andrew. |
| `qt5_recovery_sweep.py` ×3 | S3-only, untracked | **BREAKS LOUDLY ON IMPORT.** Intended. Same. |
| `tests/test_empty_stub_and_asof_lag.py:264`, `tests/test_retry_net.py:118,137` | repo | `mock.patch.object(bz, "land_to_s3", ...)` → repoint to the new names. **Must be updated in the same commit or the suite passes against a function nothing calls** — the same failure mode DS already hit and fixed once today. |

**This is the deletion question dissolving.** Once the rename lands, both bypass scripts fail immediately on
import — a one-off whose job is done and which now cannot run is **inert**. Retirement becomes calm
housekeeping at Andrew's convenience rather than an ask riding a fix. *(Deleting S3 objects remains a
human-confirmation action; nothing here deletes anything.)*

### Cross-tree constraint — READ BEFORE TOUCHING

`cot_bronze_ingest.py` is a **guarded single source deployed to BOTH firm trees** (`opal-data-cot` and
`opal-data-bd`; runtime separation via `_assert_firm_separation`, ledger `20260625T1547Z` L2). The bd copy is
currently **15 days stale** (`fa9fd5a9652e7c7aea60776ed469c773`, 56,885 B, 2026-07-09) versus cot's 72,808 B.
**CTO has RULED: HOLD bd, do NOT sync**, divergence recorded at the point of action, `0.6.0` informed directly.
So this change is cot-deploy-only — and that is now a **decision**, not an accident of drift.

---

## 4. Acceptance

1. `ingest_table` on a table with rows → object lands **and** a `basis="land_time_measured"` sidecar appears.
   Byte-compare the sidecar against one written by the pre-change code: **identical fields**. Behavior unchanged.
2. `ingest_table` on a 0-row snapshot → still rejected pre-write at `:712`; **no object, no sidecar** (the
   reject path never reaches the primitive).
3. **`land_to_s3` is gone from the module namespace** — `hasattr(m, "land_to_s3") is False`. This is the whole
   control; assert it directly.
4. **MUTANT (mandatory):** re-add a public `land_to_s3 = _land_to_s3` alias → test 3 must FAIL. Without this,
   test 3 could pass because the module failed to import at all.
5. **Attest-failure asymmetry preserved:** force `_write_completeness_sidecar` to raise → the object is still
   landed and the day re-pulls next run (no exception escaping to abort the whole table sweep). Proves the
   safe direction of the asymmetry survived the refactor.
6. Full bronze suite green **with the mocks repointed** — and confirm the repointed tests actually exercise the
   new path (a mock on a name nothing calls is a test that cannot fail).

**Verified as DEPLOYED, not as committed:** download the served object, import it, assert (3). A green suite
describes a file; the deploy is about a runtime.

---

## 5. What this does NOT do

- **Does not touch bronze data.** No re-write, no delete, no backfill (CLAUDE.md 17a).
- **Does not change `_table_complete` / `_retry_net_state`** — DS shipped those today and they are verified.
- **Does not sync the bd tree** (CTO ruling above).
- **Does not delete the bypass scripts** — it makes them inert, which is a different and reversible thing.
