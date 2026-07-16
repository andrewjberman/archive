# Casebook ENTRY 5 DRAFT — B_00, for CTO fold + sign

**TO:** OPAL_GLDRNS.A4 L0 | **Author:** 0.4.0_DS_ClientPlatform~A | 2026-07-16 ~13:2xZ
**Status: DRAFT — awaiting CTO fold into `docs/architecture/OPAL_RUNNERS_CANONICAL_FORM_CASEBOOK.md`.**
**Why here:** the casebook is CTO-lane (owned-paths gate measured live this window: ANY_CTO on
docs/architecture/, my commit correctly blocked) — per the WAVE3_SPEC precedent the lane drafts
fold-ready text, CTO's fold costs a review not a composition. Text below is fold-ready verbatim,
house rubric (R1-R5); it replaces the casebook's current next-entries footer line with ENTRY 5 +
the new footer carried at the bottom of this draft.

---

## ENTRY 5 — B_00 (canonical holdings): DELETED OUTRIGHT — the ruled-unacceptable core

**Analyzed:** 2026-07-16 ~13:2xZ (OPAL_GLDRNS.A4 L0 — the plan's named first motion) · **full-source
read**, 1,355 lines @ repo `c44ff4917` (file last touched `04c733de5`, 2026-07-06) · co-authored
0.4.0_DS_ClientPlatform~A per §4.2 · `comp-pipescript io B_00` returns an EMPTY manifest (dynamic key
construction — the tool itself says "manual review required"; this entry is that review, the A1-contract
precedent). **The ruling this entry records (PRD §4.1.2, verbatim):** *"deriving security valuations by
replaying transactions is **ruled unacceptable as a means of valuing securities**. The canonical form
values from the custodian's own position/lot facts (RPS/ULN/RLD — monolith silver); transactions are the
EVENT layer (Group B), never the valuation source."*

### R1 — What the legacy layer ACTUALLY computes

Merges A_03's replay-derived `positions_cube` with Schwab RPS silver into
`gold/canonical/holdings/{date}.parquet` — a per-date full outer join on (account_id, asset_name)
classifying every position `bd / bd_stale / schwab / reconciled / schwab_override` (`:531-539`), Schwab
authoritative wherever it speaks (`:557-573`), `bd_stale` = a FIFO ghost the custodian denies, zeroed
(`:560,:571`, tolerance max($0.01, 0.1%) `:83-84,:515-518`). To hold that join together it maintains:
a CUSIP→asset_name bridge from two silver files (`:258-300`); a Schwab→BD account mapping built by
transaction fingerprinting, self-healed from unrealized zero-padding to ~98.6% (`:161-204`), then
FILTERED for the fingerprinter's own false positives by an AUA-ratio>5x heuristic (`:207-255`);
BFIX1 persistent-coverage sets (≥3 assets/14-day window) so bd_stale stops firing on structurally
uncovered accounts — PCRA/AQR/Fidelity-401k/Schwab-Trust-Bank, ~$6.6M/25 accts (`:421-469,:483-491`);
BFIX2 re-injection of accounts the reconcile itself silently dropped — "drop mechanisms not fully
traced" is the comment's own admission (`:703-723`); BFIX3 re-injection of all-stale alive accounts
(`:725-748`); ghost/phantom/closure exclusion stacks (`:303-321,:664-680,:1000-1013`, plus
`aua_overrides.json` + `lib/exclusions` in-tree); hardcoded `NAME_ALIASES` ETF renames (`:75-79`); a
par-pricing NAME-GREP (CASH/MONEY/MMKT/SWEEP/SHIELD/BUFFER/DELPHI → price=1.0, with a "CASH COWS"
carve-out `:592-599`); weekend/holiday FORWARD-FILL of the entire prior holdings file with hybrid
price carry (else sparse prices collapse firm AUA $1.6B→~$100M — the Easter scar, `:1228-1233`;
unchecked cube pass-through would inflate AUA ~$270M — `:1151-1156`); and a sealed-date watermark
with `--force-recent-days 14` because "BD restates recent data within ~14d" (`:124-154,:973-977`).
Runs nightly at the head of `CHAIN_CANONICAL` (`gold_dispatch.sh:84,:140`); bulk-loads ALL history
into memory (256-thread reads, fork/COW engineering, the 2026-04-22 128GB OOM incident `:1113-1120`).
**Direct consumers:** B_01 (reopen/topup evidence tiers `B_01:1140-1198`), B_02 (alive-gate + input
`B_02:5,:23,:27`), B_03 (t-1/t position pairs `B_03:16-17`), D_04 (absence diagnostic `D_04:2882-2896`).

### R2 — Which bad-data reality each patch compensated, and whether 0833 still has it

| legacy patch | the reality it compensated | does the 0833 spine have that reality? |
|---|---|---|
| the entire reconcile taxonomy (5 source classes, tolerance, bd_stale zeroing) | positions were DERIVED by A_03's replay, so derived-vs-custodian divergence had to be detected and patched row-by-row | **NO — dissolves whole.** fact_rps IS the custodian's daily position statement (Entry 3; monolith silver `fact_rps` live, listed this session). A read fact has no self-vs-custodian axis. The reconciliation INSTINCT survives as C_04's recon guard — FLAGS-NEVER-PATCHES, already live (first exercise 07-15) |
| CUSIP bridge + account fingerprint mapping + false-positive ratio guard | two vendor ID spaces (BD names/ids vs Schwab CUSIPs/account numbers) with no authoritative join | **NO** — single CRS id space; securities via fact_sec, accounts native. The one lawful bridge left in the estate is D1 `dim_account_xref` (0824↔0833 overlap), in-band unresolved, never a fingerprint |
| BFIX1 persistent-coverage predicate | RPS coverage flickered on accounts BD tracked but Schwab didn't custody | **STRUCTURALLY GONE** — the 0833 book IS the custodian's book. Off-Schwab assets are a NAMED BASIS BOUNDARY (recorded, never patched — the never-summed law's row) |
| BFIX2/BFIX3 re-injections | the reconcile's own untraced drop mechanisms | **GONE WITH THE LAYER** — patch-on-patch; nothing to re-inject when nothing is derived |
| ghost/phantom/alive exclusions + aua_overrides | the synthetic valuation base manufactured phantom rows (PRD §4.1 items 1+3) | **NO** — refuse-loud guards replace row surgery (ruling-26 class; Entry 1's guard grammar) |
| weekend forward-fill + hybrid price carry | cube emitted calendar days; prices dropped out; overlay positions passed unchecked | **NO** — RPS partitions exist exactly on statement days; **an absent day is ABSENT** (gold grammar, Entry 1); T-1 trading-day law makes the weekend a non-event, not a fill target |
| par-pricing name-grep + NAME_ALIASES | price coverage gaps + vendor name drift | **MOSTLY NO** — pricing becomes the promoted canonical-prices unit (M4/L3) with measured `pct_priced`; naming lives in dim_asset. Honest residue: genuinely par-valued instruments are a TYPED dictionary decision, not a string pattern |
| sealed watermark + force-recent-14d | BD restated history within ~14d | **CHANGED IN KIND** — CRS partitions are immutable daily statements; a re-delivery is a new vintage. Sealing collapses into idempotent per-date roll-forward (the seed orchestrator pattern the plan keeps) |

### R3 — The canonical-form replacement

**NONE — the layer is deleted, inheriting Entry 3's foundation directly:** positions are READ
(fact_rps daily statement + fact_rps_s2 balance/cash discovery + ULN/ULT/RLD lot detail — all live in
monolith silver), never derived, never reconciled against a synthetic twin. What survives is not the
script but three instincts, each re-homed: (1) custodian-vs-derived checking → **C_04 recon guard**,
flags-never-patches, thresholds explicit per row; (2) pricing + coverage → the **M4 canonical-prices
promotion** (L3: named unit, own dictionary rows, `pct_priced` derives from its coverage); (3)
sealed-immutability → **idempotent per-date partitions, absent-day-absent**. Holdings before the
2024-07-08 feed floor remain the pre-floor decision on Andrew's desk (Entry 1's named residue —
inherited, not new).

### R4 — The TRUE incremental key (and what forced the legacy full recompute)

The layer's honest unit of work is **(date)** — one statement partition per day, O(one day). The
legacy economics (whole-history bulk load, 128GB budget, fork/COW engineering, the c6i.16xlarge class)
were forced by (a) the replay upstream — rebuilding any day's state means re-scanning history
(Entry 3), and (b) reconcile-and-reseal over the full tree. **Forced by fundamentally bad design, not
by the problem** — Andrew's §2 diagnostic answered for the pathology centerpiece itself.

### R5 — Contract vs named 49F variance

**Group-B contract material (generalizes):** Group-B facts come from custodian statements —
transaction replay is never a valuation or position source (the §4.1.2 ruling, now casebook law);
reconciliation is a GUARD that flags, never a data path that patches; valuation = units × canonical
price with coverage MEASURED, never a name-pattern par list; absent day absent. **Named 49F variances
(do NOT generalize):** the 0824/0833 dual-master identity and its one lawful bridge (D1 xref, recorded
never resolved); the off-Schwab account classes as a basis boundary of the 0833 book.

---

*(Next entries: the C-family lands WITH each A4 port — C_00-core first; B_01/B_01b/B_02 lots vs
ULN/ULT/RLD ride their disposition legs; B_03 vs the windowed-gains cell.)*
