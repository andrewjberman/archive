# bd-hold-lift resumption checklist -- the 6 re-enable mechanisms the guarded bd-readers need flipped when the sovereign hold lifts

**`2.0.0_SA_COO`, 2026-07-10.** *Authored in the COO lane per CTO GO (`000829Z`); `1.0.0_SA_CTO` owns/tracks the
bd-hold lifecycle (this pairs with the bd-cron-under-hold decision Andrew + CTO track). **UPDATE 2026-07-11: the
CONSOLIDATION IS COMPLETE (CVO~B, C1->C8, CTO-gated). One signal now lifts everything -- see THE ONE-FLIP below;
the per-tool flags are retained only as back-compat overrides.***

---

## THE ONE-FLIP (post-consolidation, 2026-07-11) -- THE resumption instruction

**When Andrew lifts the sovereign bd hold: `set COMP_INCLUDE_HELD=1` (+ verify).** That ONE env var re-enables ALL
14 in-repo guarded bd-readers at once, via the shared `sovereign_held.include_held()` predicate
(`org/modules/graph/sovereign_held.py`, `f2ead7904` -- no underscore: a public 15-tool API). **Polarity:**
`COMP_INCLUDE_HELD=="1"` -> read held; unset / anything-else -> held (skip). The 14: comp-validate, comp-dispatch,
comp-recognizers (code+config), freshness_manifest_gen, comp-iam, comp-constants, comp-secrets, comp-pipescript
(deployed + io), comp-incrparity, + the trace-graph indexer / extract_pipeline / extract_s3 / platinum (via the
shared predicate).

**ONE TEMPORARY EXCEPTION:** `freeze_monitor` (comp-xray, the deployed lambda in `infra/aws/compdiff`) is
`0.7.0_AE_CloudOps~C`'s lane and not yet migrated -- until their C-x lands it honors **`COMP_XRAY_INCLUDE_HELD=1`**
separately. So for now the lift is: **`COMP_INCLUDE_HELD=1` (14 in-repo tools) + `COMP_XRAY_INCLUDE_HELD=1`
(freeze_monitor).** CVO~B pings when C-x lands; then this exception drops and it is truly one flip.

**Drift-guarded:** `test_sovereign_held_no_drift.py` (`7854a9977`) FAILS CI if any tool re-introduces a local
held-marker copy -- the single-source-of-truth cannot silently erode.

**VERIFY after the flip** (resumption is not "set it and trust"): exercise one guarded reader per tier against bd and
confirm it now READS, not loud-skips (e.g. `comp-freshness chain bd` returns a real freshness verdict, not the
held-skip note).

---

## THE LATENT GAP (why the consolidation exists -- historical)

As the NFRA_TOOLPASS sweep guarded the bd-reader-class tools one-by-one, **each grew its OWN re-enable
mechanism** so a normal agent invocation loud-SKIPS bd under the sovereign hold, while a pipeline/opt-in
invocation can still read bd. That is correct *under the hold*. **But it becomes a trap the moment the hold
lifts:** if bd work resumes and these flags are NOT flipped, the bd tooling **silently loud-skips bd** -- bd
deploy-verify, IAM-scan, freshness-gate, dedup, consumers-scan all quietly no-op on bd, looking healthy while
covering nothing. There are **6 heterogeneous mechanisms** (2 CLI flags + 4 env vars, 3 name-shapes) -- no single
switch, so lifting the hold correctly requires remembering all 6.

## LEGACY PER-TOOL OVERRIDE FLAGS (back-compat -- the ONE-FLIP above supersedes these; `include_held()` still honors each)

*Pre-consolidation, each guard had its own flag. Post-consolidation these STILL work (per-tool override for a single
tool without lifting the whole hold), but the resumption default is the one-flip `COMP_INCLUDE_HELD=1`. Kept for
reference + single-tool override.*

| tool | legacy override | shape | re-enables (what silently skips bd without it) |
|---|---|---|---|
| `comp-dups` | `--allow-held` | CLI flag | the estate dedup/dead-confirm scan over bd source |
| `comp-constants` | `--allow-held-scan` | CLI flag | the firm-constant drift scan over bd source (`check --file <bd>`, bare `check`) |
| `comp-freshness` | `COMP_FRESHNESS_PIPELINE=1` | env var | the bd `chain bd` freshness gate reading `gold_freshness_config.yaml` (the $130M-overshoot protection) |
| `comp-iam` | `COMP_IAM_INCLUDE_HELD=1` | env var | the bd gold + EC2-manifest service-source IAM scan |
| `comp-pipescript` | `COMP_PIPESCRIPT_INCLUDE_HELD=1` | env var | the bd `deployed` verify (md5 vs opal-data-bd) + the all-trees firm-separated deploy-verify sweep's bd leg (Rule 13, DS) |
| `comp-secrets` | `COMP_SECRETS_INCLUDE_HELD=1` | env var | the `consumers` git-grep over bd source for a secret name/arn |
| `comp-validate` | `COMP_VALIDATE_INCLUDE_HELD=1` | env var | the bd `gold_validate_config.yaml` read (alias map, `--list`, every non-INF validation) + the bd validators-dir stat/dispatch |
| `comp-dispatch` | `COMP_DISPATCH_INCLUDE_HELD=1` | env var | reads bd `gold_dispatch.sh` (C0-#1, `c56421407`) |
| `comp_recognizers` | `COMP_RECOGNIZERS_INCLUDE_HELD=1` | env var | code+config recognizers read bd `gold_freshness_config.yaml` + `gold_dispatch.sh`/`s3_layout`/`A_00`/`A_01` (C0-#4/#5, `5f893de0d`) |
| `comp-incrparity` (CLI) | `COMP_INCRPARITY_INCLUDE_HELD=1` | env var | the comp-tool incrparity CLI reads s3 `opal-data-bd` (C0-#7, `54c1b9ab5`) |

**No new var (C0):** `freshness_manifest_gen` (C0-#2, `c2b306806`) reuses **`COMP_FRESHNESS_PIPELINE`** (its sibling
comp-freshness's flag now covers both). `extract_pipeline:994` -> `comp-pipescript io` (C0-#3, `f51ee8323`) uses a
bare `_held_path_hit` -- a C1 note threads `include_held` so `io` honors `COMP_PIPESCRIPT_INCLUDE_HELD` like `deployed`
(comp-pipescript is now fully guarded, deployed+io, not half).

**Inheriting via shared engines (no own flag -- covered by the above):** `comp-debt` (its DUPLICATES signal rides
`dup_scan` -> `--allow-held`); `comp-platinum` + any future caller ride the shared `_held_path_hit` chokepoint.

**DATA-tier member (separate mechanism):** `comp-xray` / freeze-monitor (`04de28c0b`) reads a held bd DATA bucket,
not source -- its re-enable is a **deployed-cron env-flag** (0.7.0_AE_CloudOps~C's leg), distinct from the tool-side
flags above. When the hold lifts, its cron-flag flips too. Confirm the exact var with 0.7.0~C's freeze-monitor deploy.

**CLASS STATUS: CLOSED -- census-verified 2026-07-11 (C0 exit).** The alphabetical pass's "final tool =
comp-validate = closed" was PREMATURE; `3.0.0_SA_CVO~B`'s independent source-only CENSUS found 6 more unguarded
readers, they were GUARDED in the C0 phase, and the census now confirms closure. **DENOMINATOR (CTO-confirmed):**
28 bd-referencing tool sources / 16 content-readers / **15 GUARDED** / 1 designed-bd OUT-of-scope (`incrparity_core`,
pure library no CLI) / **0 UNGUARDED**. (The lesson stands: a source-first CENSUS is the ground truth of closure,
not the alphabetical pass's "final tool" -- the census caught 6 gaps the tool-by-tool pass had declared away.)

CENSUS-FOUND READERS -- NOW GUARDED in C0 (CVO~B, each fixture mutation-proven, CTO-gated):
1. `comp_dispatch.py` -- open+read bd `gold_dispatch.sh` (SOURCE-CONFIRMED).
2. `extract_pipeline._extract_column_gaps:994` -> `comp-pipescript io` -- `deployed` is guarded, **`io` is NOT** (SOURCE-CONFIRMED gap).
3. `comp_recognizers_config.py` -- bd `gold_freshness_config.yaml`.
4. `comp_recognizers_code.py` -- bd `gold_dispatch.sh` / `s3_layout` / `A_00` / `A_01`.
5. `.tools/freshness_manifest_gen.py` -- bd `gold_freshness_config.yaml` (comp-freshness guards its sibling; this does NOT).
6. `incrparity_core.py` -- s3 `opal-data-bd` (CAVEAT: a designed-bd parity ENGINE, likely OUT of scope -- CTO scope call B).

CENSUS ALSO CONFIRMED the known-guarded readers intact + found 4 MORE already-guarded (comp_constants, dup_scan,
extract_iam, comp-freshness) -- the guarded set is solid and larger than tracked; the gap is precisely these 6.

**SO for the flag enumeration:** the pre-C1 set is now COMPLETE (census-verified) -- the 7 core tool-flags above +
the 3 C0 override vars (`COMP_DISPATCH`/`COMP_RECOGNIZERS`/`COMP_INCRPARITY`_INCLUDE_HELD) + the shared-engine
inheritance (comp-debt/comp-platinum) + the two no-new-var C0 cases (freshness_manifest_gen reuses
`COMP_FRESHNESS_PIPELINE`; comp-pipescript `io` rides `COMP_PIPESCRIPT_INCLUDE_HELD` post-C1). **C1**
(`_sovereign_held.py`, gated to CTO) collapses ALL of them into ONE `COMP_INCLUDE_HELD` signal. **FINAL POLARITY
(CVO~B-confirmed): `COMP_INCLUDE_HELD=1` LIFTS the hold** -- one flip re-enables every guarded bd-reader. Once
C1-C7 land, this checklist becomes "set `COMP_INCLUDE_HELD=1` + verify", and the per-tool flags become back-compat
legacy vars the shared predicate still honors.

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
