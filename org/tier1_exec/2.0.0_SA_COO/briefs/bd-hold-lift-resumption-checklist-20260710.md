# bd-hold-lift resumption checklist -- the 6 re-enable mechanisms the guarded bd-readers need flipped when the sovereign hold lifts

**`2.0.0_SA_COO`, 2026-07-10.** *Authored in the COO lane per CTO GO (`000829Z`); `1.0.0_SA_CTO` owns/tracks the
bd-hold lifecycle (this pairs with the bd-cron-under-hold decision Andrew + CTO track). Durable capture now; the
CONSOLIDATION to a single signal is post-sweep (see below).*

---

## THE LATENT GAP

As the NFRA_TOOLPASS sweep guarded the bd-reader-class tools one-by-one, **each grew its OWN re-enable
mechanism** so a normal agent invocation loud-SKIPS bd under the sovereign hold, while a pipeline/opt-in
invocation can still read bd. That is correct *under the hold*. **But it becomes a trap the moment the hold
lifts:** if bd work resumes and these flags are NOT flipped, the bd tooling **silently loud-skips bd** -- bd
deploy-verify, IAM-scan, freshness-gate, dedup, consumers-scan all quietly no-op on bd, looking healthy while
covering nothing. There are **6 heterogeneous mechanisms** (2 CLI flags + 4 env vars, 3 name-shapes) -- no single
switch, so lifting the hold correctly requires remembering all 6.

## THE CHECKLIST -- flip ALL of these when the sovereign bd hold lifts

| tool | mechanism | shape | re-enables (what silently skips bd without it) |
|---|---|---|---|
| `comp-dups` | `--allow-held` | CLI flag | the estate dedup/dead-confirm scan over bd source |
| `comp-constants` | `--allow-held-scan` | CLI flag | the firm-constant drift scan over bd source (`check --file <bd>`, bare `check`) |
| `comp-freshness` | `COMP_FRESHNESS_PIPELINE=1` | env var | the bd `chain bd` freshness gate reading `gold_freshness_config.yaml` (the $130M-overshoot protection) |
| `comp-iam` | `COMP_IAM_INCLUDE_HELD=1` | env var | the bd gold + EC2-manifest service-source IAM scan |
| `comp-pipescript` | `COMP_PIPESCRIPT_INCLUDE_HELD=1` | env var | the bd `deployed` verify (md5 vs opal-data-bd) + the all-trees firm-separated deploy-verify sweep's bd leg (Rule 13, DS) |
| `comp-secrets` | `COMP_SECRETS_INCLUDE_HELD=1` | env var | the `consumers` git-grep over bd source for a secret name/arn |
| `comp-validate` | `COMP_VALIDATE_INCLUDE_HELD=1` | env var | the bd `gold_validate_config.yaml` read (alias map, `--list`, every non-INF validation) + the bd validators-dir stat/dispatch (the 7th/FINAL source/config reader) |

**Inheriting via shared engines (no own flag -- covered by the above):** `comp-debt` (its DUPLICATES signal rides
`dup_scan` -> `--allow-held`); `comp-platinum` + any future caller ride the shared `_held_path_hit` chokepoint.

**DATA-tier member (separate mechanism):** `comp-xray` / freeze-monitor (`04de28c0b`) reads a held bd DATA bucket,
not source -- its re-enable is a **deployed-cron env-flag** (0.7.0_AE_CloudOps~C's leg), distinct from the tool-side
flags above. When the hold lifts, its cron-flag flips too. Confirm the exact var with 0.7.0~C's freeze-monitor deploy.

**CLASS STATUS: closure IN PROGRESS -- NOT closed (corrected 2026-07-11).** CTO *declared* the class closed at
comp-validate, but `3.0.0_SA_CVO~B`'s independent source-only CENSUS (`031046Z`) found **6 unguarded
bd-content-readers the alphabetical sweep MISSED** -- so the enumeration below is INCOMPLETE and MUST NOT be locked
as the consolidation TO's set until the C0 guard phase lands. (This is the verify-before-asserting-closed lesson on
the sweep's own closure claim: a source-first CENSUS is the ground truth, not the alphabetical pass's "final tool.")

CENSUS-FOUND UNGUARDED READERS (C0 guard-first queue; CVO~B escalated the scope calls to CTO `031001Z`):
1. `comp_dispatch.py` -- open+read bd `gold_dispatch.sh` (SOURCE-CONFIRMED).
2. `extract_pipeline._extract_column_gaps:994` -> `comp-pipescript io` -- `deployed` is guarded, **`io` is NOT** (SOURCE-CONFIRMED gap).
3. `comp_recognizers_config.py` -- bd `gold_freshness_config.yaml`.
4. `comp_recognizers_code.py` -- bd `gold_dispatch.sh` / `s3_layout` / `A_00` / `A_01`.
5. `.tools/freshness_manifest_gen.py` -- bd `gold_freshness_config.yaml` (comp-freshness guards its sibling; this does NOT).
6. `incrparity_core.py` -- s3 `opal-data-bd` (CAVEAT: a designed-bd parity ENGINE, likely OUT of scope -- CTO scope call B).

CENSUS ALSO CONFIRMED the known-guarded readers intact + found 4 MORE already-guarded (comp_constants, dup_scan,
extract_iam, comp-freshness) -- the guarded set is solid and larger than tracked; the gap is precisely these 6.

**SO for the flag enumeration:** the 7 tool-flags above are the CURRENTLY-guarded set; C0 will GROW it by the new
guards' override vars (~5 in-scope), then C1 collapses ALL of them into the single `COMP_INCLUDE_HELD` signal.
Do NOT finalize the per-flag list until C0 lands. The one-flip end-state is unchanged (`COMP_INCLUDE_HELD=1` lifts
everything); only the pre-consolidation count is still growing.

## THE CONSOLIDATION TARGET -- ONE flip, not seven+ (CTO is OPENING the post-sweep TO 2026-07-10; it KEYS ON this checklist)

The 6 mechanisms are heterogeneous (CLI vs env, three name-shapes) -- a resumption is exactly the kind of
"remember all N or a control silently no-ops" trap the whole sweep is about. **The right end state is a SINGLE
fabric-wide signal** -- one env var or a shared `bd-hold-lifted` marker every guard honors -- so lifting the hold
is ONE flip that every bd-reader inherits, not six remembered independently. This **pairs directly with the
held-marker consolidation TO** (`a7b38ae7c`: one shared held-path constant every guard imports) -- the same guards,
the same "single source of truth vs N mirrored copies" hazard, one on the *held-path list* and one on the
*re-enable signal*. Both are **post-sweep** (a simultaneous rewrite of ~7 security-critical guards mid-sweep is the
churn the sweep avoids); the per-guard mechanisms + drift-guard tests hold each safe individually until then.

## DISPOSITION

- **Now:** this checklist is the durable capture. When Andrew lifts the sovereign bd hold, all 6 must flip (or bd
  tooling silently under-covers). Belongs in the bd-hold lifecycle CTO tracks (alongside the bd-cron-under-hold
  decision).
- **Post-sweep TO (CTO-owned scoping):** consolidate the 6 into one fabric-wide `bd-hold-lifted` signal, co-scoped
  with the held-marker consolidation (`a7b38ae7c`).

**Attribution:** flag set enumerated + checklist authored by `2.0.0_SA_COO` (surfaced via the comp-pipescript +
comp-secrets closes, CVO~B); consolidation target CTO-noted (`000829Z`); lifecycle owned by `1.0.0_SA_CTO`.
