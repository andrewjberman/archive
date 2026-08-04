# SPEC — Cottonwood into the Global account-distribution.json (Andrew-direct 2026-08-04 ~17:5xZ)

**Author:** 0.2.0_DS_PortfolioAnalytics · 2026-08-04 18:2xZ
**Authority:** Andrew-direct (verbatim record: `ANDREW_DIRECT_20260804_GLOBAL_ACCT_DIST_COTTONWOOD_GAP.md`, committed) — "spec the fix to get Cottonwood incorporated in there."
**Coordination:** DE (0.4.0_DE, per Andrew's word) · 0.4.0_DS (GRF carry seam, COO 181124Z) · CTO head-starts 180742Z.

## 1. THE FINDING — the fix already exists; it was never deployed

**The gap is NOT in the feed and NOT in the code. It is a Rule-13 deploy leg that never ran, 12 days old.**

| plane | state | evidence |
|---|---|---|
| Feed (daily) | COMPLETE — cottonwood account-grain units emitted daily by the pair producer as a sidecar | `s3://opal-data-assets/gold/mdpf_revamp/cottonwood/account_units.json` (`build_cottonwood_mdpf_pair.py:504`); refreshed TODAY 17:41Z (round 4) with the corrected residual classification |
| Repo code | 3-FIRM FOLD PRESENT since **2026-07-23** | `dim_mdpf_account_distribution.py` — sidecar read `:304-322` (fail-closed for global), fold `:338-348` (both grains), in-band `meta.cottonwood_fold` marker `:379-392`. Commits `fa491f9b61` (fold, exercised 7863/$1.672B at landing) + `34e38a8e55` (W-6 marker), author 0.4.0_DS |
| Deployed code | **STALE — 2026-07-21 vintage, PRE-fold** | `s3://opal-data-mdpf/code/scripts/gold/dim_mdpf_account_distribution.py` LastModified 2026-07-21 17:42:42Z; **zero** occurrences of "cottonwood" (full-file grep of the pulled object); comp-pipescript `deployed` = STALE |
| Staged artifact | 2-firm — emitted daily by the stale builder (dispatch 6b `:489-492` runs it every cycle) | `gold/mdpf_revamp/global/account_distribution.json` written today 17:41:49Z, no fold marker |
| Served artifact | 2-firm | `platinum/mdpf/global/account-distribution.json` period=2026-08-04: account_count **7632**, no `cottonwood_fold` marker, "cottonwood" absent from the whole body |

So every daily cycle since 07-23 staged and served the 2-firm bell while the repo carried the 3-firm fix. The accrual and publisher are faithful couriers of a stale producer — same class as the trio script's `MISSING_ON_S3` (flagged to CTO this morning) and the EMIT-1 wiring gap: **the estate's parity instrument (comp-pipescript deployed) sees it in one call; nothing runs that call on a schedule.**

## 2. THE DYNAMICS (how 49F / INF work, where cottonwood folds — the reference pattern Andrew asked for)

One builder, `dim_mdpf_account_distribution.py`, per-firm unit extraction then shared stats:

- **49financial** (`_units_49financial` `:212`): monolith silver facts → per-account funded units (>= $1K floor), SMAs excluded, core-model keying via crosswalk.
- **inflection** (`_units_inflection` `:246`): same monolith silver, Opal-model keying, blends included.
- **global** (`_units_global` `:290`): the CROSS-FIRM UNION of 49F + INF unit frames — then (post-07-23 code) **cottonwood joins from the SIDECAR** (`:338-348`), not from the monolith: the pair producer is the ONE computation of cottonwood account-grain units (relationship-grain already collapsed, ties to the dim to the penny), read as an artifact to avoid a cross-tree runtime import.
- **Both grains, deliberately** (the CTO head-start #2 treatment, already encoded): **distinct full-value accounts** feed the TOTAL bell curve / container metrics (an account counted once at its full value), while **blend-split values** feed `by_model` (a blended account contributes to each underlying model row). This is exactly the LD-0330 count-axis law: by_model counts are NOT summable to the firm population (~1.51x overcount if summed) — the artifact's `meta.count_axis_note` states it, and the total-vs-by_model split is why cottonwood can enter both without double-counting the bell.
- Downstream is already scope-agnostic: accrual DECLARES `account-distribution` for ALL scopes (`build_portal_gold_accrual.py` DECLARED_TYPES), publisher derives its publish set from the listing. **No accrual/publisher/portal change is needed.** DE's reader consumes the served shape as-is; the fold only ADDS units and the in-band marker.

## 3. THE FIX (three steps, ~one hour end-to-end, zero new code)

1. **Deploy repo HEAD** `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` → `s3://opal-data-mdpf/code/scripts/gold/` (Rule 13, DS lane = mine). comp-pipescript `deployed` must read MATCH.
2. **Re-emit global** (`--firm global --upload`) ad-hoc for the same-day heal, with the next scheduled 6b cycle as the production evidence (NEVER#4 discipline: the ad-hoc is QA/heal; the schedule is the proof). Per-firm scopes are byte-unaffected (`:341` comment — fold is global-only).
3. **Accrual + publisher** bridge as normal (AE's publisher leg per the standing one-invoker grant).

**Exercised TODAY (pre-spec validation, dry-run on live data):** global build with the fold = funded **7925** / active 7974 / total $1,694,070,546 / by_model 7 — vs served 2-firm 7632. Delta ≈ +293 ≈ cottonwood's 295 dim accounts (net of the funded floor). Fail-closed sidecar read passed on today's corrected sidecar.

**Acceptance (machine-checkable):**
- served `platinum/mdpf/global/account-distribution.json` carries `meta.cottonwood_fold` (the in-band 3-firm marker — W-6's point: a byte-grep for "cottonwood" on values alone read FALSE on a genuinely 3-firm bell) with plausible `folded_accounts`/`folded_dollars`;
- `total.account_count` moves ~7632 → ~7925 (exact printed in the deploy ledger);
- per-firm 49F/INF artifacts byte-stable on frozen inputs;
- DE render check: Global bell curve/container metrics reflect the fold (their Phase-3-style verify);
- next SCHEDULED cycle reproduces it (per-stage read).

**SERVED-VALUE MOVEMENT, declared:** count/mean/median/percentiles/histogram ALL move (deliberately — that is the ask). Andrew's word is the sovereign basis; CTO+COO GO on this spec = the never-widen sign-off. No serve-bucket move, no monitors, no new artifacts.

## 4. SEAM — GRF carry (0.4.0_DS), composed not raced

COO 181124Z: 0.4.0_DS's GRF roll-forward scoping (Andrew ~1715Z T+2 ruling) covers account-COUNT CARRY semantics in this SAME artifact. Composition (COO's natural order, adopted): **INCLUSION first (this spec), then CARRY applies to the included cottonwood leg on its lagged dates** (cottonwood value-dates lag T+2-class; on a day the sidecar's vintage trails, the carry semantics govern what the fold shows rather than the fold dropping the leg). Their spec cites this one and vice versa; conflicts route through CTO.

## 5. RIDERS (observed during grounding, not this spec's scope)

- **F5 crosswalk WARN** (pre-existing, fires in today's build): `eclipse_id=31 '90/10 Opal Intermediate/Ultra Short Term'` candidate-NEW-Opal model excluded, folded to non_model — crosswalk review owed (routed with this spec's report; owner = crosswalk lane).
- **Deploy-parity class:** this is the 3rd committed-vs-deployed gap surfaced today at this seat (trio MISSING_ON_S3, EMIT-1 wiring, this). A scheduled `comp-pipescript deployed` sweep would have caught all three; noting for CTO's routing as a GATE candidate, NOT building any monitor (moratorium).
