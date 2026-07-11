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

**CLASS STATUS (CTO-declared 2026-07-10):** the bd-reader class is now CLOSED -- 9 source/config surfaces (the 7
flags above + `comp-debt`/`comp-platinum` via shared engines) + 1 DATA-tier (`comp-xray`). Every one caught
source-first, every one guarded by a str-prefix held-check with a re-enable override.

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
