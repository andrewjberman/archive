# Wave-3 spec-cell DRAFTS — M1 (C_02) + M6 (C_03), for CTO sign-off

**Author:** 0.4.0_DS_ClientPlatform~A | 2026-07-15 ~23:5xZ | **Status:** DRAFT — CTO's pen finalizes.
**Purpose:** the Wave-3 freeze was released conditional on the M-resolutions folding into their
owning spec text before each port begins (CTO 211544Z, M6 added 222722Z). These drafts fold the
two cells my lane surfaced, exactly as ruled, so the folds cost CTO a review not a composition.
M4/M5 one-line riders included. (M2 -> C_08 and M3 -> the office cell are Wave-4 and not drafted here.)

## M1 -> the C_02.client_performance spec (SERVED FIRM-AUA AUTHORITY)

> **The served firm-AUA number.** The portal-headline firm AUA is C_02's computed firm total
> (SUM of relationship `total_aua` at the partition asof), and C_02 is its sole authority once
> the legacy certification layer retires. The emit is GATED, not patched:
> 1. **C_04 gate:** the emit consults the C_04 flag state for the same asof; a flag-rate breach
>    beyond the run's declared threshold HOLDS the emit loud (names the flagged accounts) —
>    C_04 itself never writes into data (flags-never-patches law).
> 2. **The degenerate floor (the legacy law's new home, semantics carried verbatim):** the
>    served firm total must be > 0. On a <=0 computed total the emit REFUSES LOUD; vintages do
>    not advance. There is NO hold-last-good fallback — that mechanism retires WITH the cert
>    layer it patched (pre-declared divergence D5; the legacy `DEGENERATE_CERT_MODE`
>    hold/gold machinery, D_00:246-280, is superseded by refuse-loud).
> 3. Cross-contract invariant (already in the plan): SUM(C_01 account rows) == C_02 relationship
>    rows, row-for-row, every partition.
> Ruling anchors: CTO 211544Z ("C_02-computed total, GATED by C_04 flags, emit-time <=0 assert...
> carry the old floor's threshold semantics verbatim").

## M6 -> the C_03.nna spec (THE DAILY-ATOMIC EMISSION)

> **C_03 emits TWO first-class tables; the windowed derives from the atomic, never the reverse.**
> 1. **`nna_atomic` — grain (date, account_id)** — the hard input of D_00b's daily series, D_00f's
>    window summation, D_01/D_02/D_04: columns `daily_inflow`, `daily_outflow`, `nna_txn`
>    (= inflow - outflow), the sb-code decomposition (`nna_cash`, `nna_in_kind`,
>    `in_kind_unvalued_count` — flagged, never zero-buried), `relationship_id`, and a row-quality
>    flag (the `nna_clean` successor; A QUALITY FLAG, NEVER AN AGGREGATION FILTER — the pinned
>    served semantic, A1 sec-7).
>    **Incrementality: INCREMENTAL by construction** — key (date), unit of work = one
>    dim_transaction partition (+ that day's dim_position for in-kind valuation).
> 2. **`nna_windowed`** — the seed G6 shape (period_start, period_end, account_id), a pure
>    projection/rollup of `nna_atomic` over window bounds.
> Evidence anchor: dry-fit F1 (DRYFIT_REPORT sec-3: the seed estate carries NO daily-atomic flow
> table; windowed-only starves the daily chart series). Ruling anchor: CTO 222722Z ("the C_03
> spec MUST carry the daily-atomic NNA emission as a first-class cell BEFORE its port begins").

## Riders (one line each, as ruled 211544Z)

- **M4:** the canonical-prices builder is PROMOTED to a named C-group unit (own dictionary rows,
  casebook entry rides its Wave-3 port); `pct_priced` on C_01/C_02 derives from its coverage.
- **M5:** A_01 spec note — `hh_seen` carrier verified at the G6 port (C_03 carries or A_01
  derives; one-line check, non-gating).

-- drafts end; CTO edits stand as the record --
