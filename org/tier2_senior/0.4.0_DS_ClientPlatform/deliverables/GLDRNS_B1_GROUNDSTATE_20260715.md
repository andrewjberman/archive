# OPAL_GLDRNS.B1 — Ground-state audit of the INF AoR chain (drive step 1, read-only)

**archetype:** VALIDATE
**agent:** 0.4.0_DS_ClientPlatform~B · **window:** 2026-07-15 19:30Z-20:0xZ · **TO:** OPAL_GLDRNS.B1 (GO 19:22:56Z)
**Method:** every claim below is grounded on a LIVE primitive or DEPLOYED bytes (downloaded AND imported), never
a record or self-report. Instrument named per claim. Zero writes to any estate surface; scratchpad only.

## A. HOLD INSTRUMENTS — all holding, all verified live

| Instrument | Read | Verdict |
|---|---|---|
| Chokepoint | `aws lambda get-function-configuration inf-gold-trigger` (live env): `INF_GOLD_DISPATCH_HOLD` SET, `INF_GOLD_DISPATCH_RELEASE` ABSENT | **HELD** (config-read; refusal-exercise scheduled with validation prep, per 0.6.2 briefing) |
| 3 gold EventBridge rules | `describe-rule` x3 | all **DISABLED** |
| Door 5 (collisions) | `head-object` x4: `build_assets_dim.py` gold `ee55f2c5…`/8,498B vs silver `7c0df7f0…`/9,244B; `_orion_api_silver_lib.py` gold `65baced6…`/21,132B vs silver `7cb5c6ce…`/28,694B | ETags DIFFER both pairs → **SHUT** |
| Door 6 sentinel | `head-object gold/meta/pipeline-complete.json`: `fbcddcbf…`/135B/2026-07-10T14:52:54Z | **UNTOUCHED** — exact manual baseline |
| Bronze feed | `s3 ls silver/transactions/`: newest 2026-07-10.parquet; bronze runner i-083ad9ae297f88e9f `stopped` (last boot attempt TODAY 13:30:53Z — the daily step-zero FATAL cycle continues) | dark, as held |
| Door 2 (ceiling) | today = Wed 07-15, txn 3 trading days behind ceiling 2 | TRUE alarm expected today; **fix stays SEALED** |

## B. THE AoR CHAIN — what is READY (deployed bytes, exercised where legal)

1. **Change-3 EXERCISED, second consecutive scheduled row.** `accounts_v2/snapshot_date=2026-07-15/data.parquet`
   (ETag `3be9c3a2…`, 80,152B, 13:22:51Z — the nightly's own product, NEVER#4 honored): 874 rows/46 cols,
   `advisor_of_record_raw` non-null **837/874** (positive control `rep_id` present). Fold readiness via the
   library's own `build_advisor_of_record_fold` (env-activated scratch diagnostic, read-only):
   **fold_map=164 / explicit=837 — byte-stable with the banked 07-14 measurement**
   (noel 64, joe 64, patrick 22, peter 14). All 6 raw values known incl. both `_IWM` variants; zero unexpected.
2. **Deployed INF_C_01 == repo** (md5 `4dd6e769…` both). Time-lock **WIRED on the runner's bytes**:
   `lock_and_stamp` CALLED and RE-BOUND at `:873` (AST; positive control `apply_resolution_fold` call `:549`).
   BOTH guards wired: residual `:901` + coverage continuity (imports `:105-112`, exercised `:899-911`).
3. **Deployed gold lib (19 files) imports clean** — `inflection_rep_scope, aor_resolution, advisor_timelock,
   nna_coverage_guard, advisor_of_record_conformance, roster_usability, skip_gate, partition_provenance` all
   IMPORT OK from the downloaded deployed bytes. The "guard that cannot load" class: closed.
4. **Deployed lib == repo byte-identical** on every AoR file except `advisor_of_record_conformance.py`, whose
   whole diff is the 2-line DEPLOY-SERVE-HELD sentinel comment (repo-only). Functionally identical.
5. **AoR SSOT exists** (`gold/dimensions/aor_resolution.parquet` + `aor_ledger_state.parquet`, 07-13 15:11Z,
   fold-OFF vintage; ledger events present). Stamped rows: none possible — gold/canonical last written 07-10,
   before the lock wiring ever reached the runner; last chain completion 07-10.
6. **Served spine grounded** (`platinum/firm/advisor_nna_canonical.json`, generated 07-10T14:49:57Z,
   `data_as_of` 2026-07-09): phantom `inflection_unmapped_rep` **$52,604.80 still served**; MAX-window
   sum(advisors) == firm == **$133,107,667.64 to the cent**; per-advisor values tie the hold-doc's split exactly
   (peter 104,647,053.28 = observe 104,318,087.60 + 328,965.68 etc.). Noel ABSENT from the served spine.
   `platinum/advisors/` prefixes: iwm/joe/patrick/peter/unknown — no noel_soderblom yet (FE pair waits on this).

## C. THE GAPS — what stands between here and FOLD→VERIFY→LOCK (the drive's work list)

**G1 (HEADLINE, my lane, next action): the DEPLOYED dispatch has ZERO AoR wiring.**
`code/gold/orion-gold-dispatch.sh` deployed = 92,862B, 2026-07-08T19:31:26Z, md5 `5bf875c9…`;
repo = 109,903B @ `ff6b2ff87` (07-13), md5 `3aef4ae7…`. Marker counts deployed→repo:
`INF_AOR_ASOF` 0→14, `INF_AOR_SRC_ETAG` 0→10, `INF_AOR_FOLD_ACTIVE` 0→3, `aor_resolver` 0→4
(positive control `sync_scripts` 10/11 — the reads are sound). ALL of round-8.2 (resolver presence-gating,
the (source_digest, fold_mode, code_digest) pin, the switch de-multiplex) is REPO-ONLY. Consequence: deployed
INF_C_01 is fail-closed on the pin env — a release run under the deployed dispatch aborts at pin-unset.
**Deploying the repo dispatch is a hard chain prerequisite.** Safety: deploying ≠ running (chokepoint refuses
every dispatch); the new dispatch calls `sync_scripts()` at run_chain entry (`:892`) so the step-zero collision
FATAL is preserved byte-for-byte in behavior; not frozen-3; not serve-held; pre-flight = sibling-prefix
basename check before cp.

**G2: the GO-flip mechanism is NOT BUILT.** The trigger injects env into the SSM command by the
PERF-ceiling export pattern (`lambda_function.py:452-462`); it carries no `INF_AOR_FOLD_ACTIVE` forward, and
the live trigger env has no AoR var (correct today = dark). For "the flip at Andrew's GO is one motion"
(acceptance), the trigger needs the same export-forward for `INF_AOR_FOLD_ACTIVE` + a TF env var — infra/aws +
TF motion → **MCP 0.7.0 first** (B1 amendment 8d42d6903), exercised DARK (var unset → empty export → OFF).

**G3: change-2 (household AoR-wins) code is DEPLOYED byte-identical already** (`inflection_rep_scope.py`
deployed==repo, CHANGE-2 signal at `:207/:592/:643`); what it still needs is PROCEDURAL: the sentinel says
"pending CTO~B clean-review + NEVER#2 sign-off" — CTO~B is down; needs **live-CTO routing**. 15 repo files
carry DEPLOY-SERVE-HELD sentinels pending the same arch-gate.

**G4: the silver rescue** (`convert_transactions_to_silver.py`, code/silver only, no collision) is FROZEN-3 by
the two-axis rule — it turns the residual guard GREEN while the fold is a no-op, i.e. the stamp-order trap's
live trigger. It deploys ONLY inside the gated release run (fold+rescue same run). Flag to CTO at that moment.

**G5: Door 5 de-collide** = 0.7.0's open (reversible, revert pre-staged, Andrew by-name, CTO+COO co-sign,
chokepoint still held). Not mine. The 0.6.2 brief (@53a0db73a) confirms the collision diff is a pure AoR
annotation; the silver copy is the newer/load-bearing one.

**G6: CVO~B re-spawn** for the V4 re-take (gate-2's re-take, constitutionally independent) — route via
CTO→MSTR when the validation battery is staged (drive step 4).

**G7: the sovereign-worded gates** — INF hold-lift (Andrew BY NAME) + Andrew's GO + never-widen co-sign
(CTO+COO) — queued at their in-order moments; my job is that everything behind each is green first.

## D. SEQUENCE OF RECORD for the release (stamp-order absolute; no step reordered)

```
1. deploy repo dispatch -> code/gold/          (G1, mine, deploy!=run, NOW)
2. build + dark-exercise the GO-flip injection (G2, trigger+TF, MCP 0.7.0 first)
3. change-2 / serve-held arch-gate review      (G3, live CTO)
4. validation battery staged + CVO~B re-spawn  (G6, via CTO->MSTR)
5. GATED: silver rescue deploy + Door-5 de-collide (G4+G5, 0.7.0 opens, co-signed, revert pre-staged)
6. Andrew: hold-lift BY NAME + GO; never-widen co-sign        (G7)
7. ONE run, chokepoint re-armed same session: bronze -> silver(rescued) -> resolver(FOLD ON, pinned)
   -> INF_C_01: FOLD -> pre-stamp verify (preview on the producer's own path; pre-registered delta:
   firm total UNCHANGED $133,107,667.64; phantom GONE; joe DOWN ~$2.1M / peter UP ~$1.6M /
   patrick UP ~$1.03M incl. $52,604.80) -> only then LOCK/STAMP
8. CVO~B V4 re-take on the SERVED artifact; portal: noel platinum surfaces appear; Andrew SEES it.
```

## Compiler Tools

comp-grep (fold builder locate, CHANGE-2 census, DEPLOY-SERVE-HELD census — 3 runs, all with denominators
printed); comp-glob (dispatch repo locate); comp-pipescript deployed sweep RUNNING at report time (background;
result appended to the session log when it lands). Raw-aws inspections carried inline `# rail-checked:`
markers (chokepoint env var + ETag reads are the hold doc's own mandated live instruments; comp-aws models
DESIRED only).
