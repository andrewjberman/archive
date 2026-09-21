# NEVER-WIDEN SIGN-OFF PACKET -- mdpf-gold-lambda Cottonwood auto-custom deploy (Phase A + Phase B), TWO LEGS

**For:** `4.0.0_SA_CRO` (the half the standing rule gives the COO, for THIS deploy) and `1.0.0_SA_CTO`.
**Prepared by:** `0.7.0_AE_CloudOps~V`, 2026-09-21 ~19:5xZ. **Nothing is applied by this packet.**
**Authority:** Andrew-direct ~18:3xZ at `0.0.0_AB_MSTR` (record @`0b46309ec2`): *"give it to CloudOps~V, they're
idle and can take this"* / *"~V Does work, CRO and CTO signs off"*. Follow-on ~19:45Z (record @`1ab93ec740`, via
MSTR 99200 / CTO 99209): *"Sign first, then push"* -- the sign-off covers LEG A (Lambda) AND LEG B (the EC2 runner's
S3 code sync). Source rulings: /open-calls ~17:58Z calls 1 + 2 (CTO record
`ANDREW_DIRECT_20260921_1758Z_OPEN_CALLS_THREE_RULINGS.md`). Phase A + Phase B ship together (CRO/CTO 99196).
**Method:** MINIMAL PIN over the running vintage (08-26 doctrine; CRO 99159). Not HEAD.

A half signs the BLAST RADIUS and the rollback per key, both branches -- never an intention.

---

## 0. THE TWO LEGS, EXACTLY

| leg | act | who performs it | what it writes |
|---|---|---|---|
| **A** | upload the pin-built zip; commit `MDPF_GOLD_COMMIT`; `safe-apply -target=aws_lambda_function.mdpf_gold` | `0.7.0_AE_CloudOps~V` | 1 S3 object version + 1 Lambda (code + one env var) + 1 repo literal |
| **B** | the CLOUD push; its safe-deploy pre-push hook syncs changed `data/*/scripts/*.py` to their S3 code prefixes | `0.0.0_AB_MSTR` pushes (shared-branch law), the hook syncs | the S3 keys in s.5, CLOUD HEAD's bytes |

No invoke on either leg. Acceptance = the 2026-09-22 13:30Z scheduled fire (s.7).

---

## 1. LEG A -- THE PIN AND ITS DELTA AGAINST THE RUNNING BUNDLE (CRO item 1)

**RUNNING, measured this turn (not taken from the brief):**
```
mdpf-gold-lambda  CodeSha256 evIYCXURor4V++Ci4HsgwE8zIPZva/BAL+ICaLJIiAE=  CodeSize 835,383
                  LastModified 2026-09-15T06:09:14Z  MDPF_GOLD_COMMIT 48b8671569b72efb4eca64ef41ded4de9c54e84c
artifact  s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip
          VersionId 9GsracvIPvfBMzF1dttMpew0TkQtt.qg  content-sha256 7af218097511a2be15fbe0a2e07b20c04f3320f66f6bf0402fe20268b2488801
live bundle re-downloaded (get-function Code.Location): sha256 == CodeSha256 == the S3 content-sha256; 23 members;
          in-zip BUILD_MANIFEST source_vintage.commit 48b8671569 -- so the declaration and the bytes agree today.
```

**BUILD PIN `74d7efe1449b47587cf0d8ca47e3a0f9824bf297`** (branch `hotfix/mdpf-cottonwood-autocustom-20260921-cto`,
ephemeral, not for merge) = the running pin `48b8671569` + 5 commits:

| pin commit | CLOUD commit | what |
|---|---|---|
| `a2f351db1b` | `58caa80b8a` | the stuck name as an INCOME residual (immediate unblock) |
| `f5821c0945` | `db6b9fc948` | `is_auto_custom()` general mechanism in the slice (retires the manual entry) |
| `4307f067e2` | `4ce72c343d` | same mechanism in the pair + the identity-gate fix (custom bucket in `assert_identities`) |
| `bc089b4309` | `e964b7fd9c` | `build_package.py` PACKAGE row: ship `mdpf_name_discovery.py` (s.2 says why it is load-bearing) |
| `74d7efe144` | `0d09727e53` | Phase B: Opal Fixed Income stops carrying its own by_model line (3 files) |

Git delta pin vs running: **5 files, +216 / -48.**

**THE BUILT ZIP:** `build_package.py --pin 74d7efe144...` -> **868,952 B, sha256
`9c6db39ae8ae7c9d21060dfbdc5bb451053fbca9564cd046f3df75090804d0cd`**, import-closure gate PASS (19 `.py`), in-zip
`source_vintage.commit` = `74d7efe144...`. This exact file is what uploads (`.scratch/mdpf_cot/built_ab.zip`); it is
not rebuilt between signing and upload.

**MEMBER-BY-MEMBER vs the RUNNING bundle:** 24 vs 23 members.
- **ADDED 1:** `mdpf_name_discovery.py` (22,033 B, blob `e93d7eaeac`, identical at the running pin and at CLOUD HEAD;
  imports stdlib only). **INTENDED, not inert:** the slice imports `matches_word_boundary` from it at module scope.
  Its call closure (`matches_word_boundary -> _boundary_pattern, normalise`) opens no file, so the adjacent
  `mdpf_name_discovery_declared.json` (NOT packaged) is never read on this path.
- **REMOVED 0.**
- **CHANGED 5:** `BUILD_MANIFEST.json` (+15/-10); `build_cottonwood_mdpf_slice.py` (+128/-8); `build_cottonwood_mdpf_pair.py`
  (+46/-6); `dim_mdpf_aggregate_aua_timeseries.py` (+13/-5); `mdpf_revamp_model_crosswalk.py` (+19/-29).
- **UNCHANGED 18, byte-identical.** Config hashes (roster, bindings, registry) identical.

**PROVENANCE OF EACH CHANGED MEMBER (zip bytes compared to git objects):**
- slice == CLOUD `0d09727e53` blob `127bad164b` (== CLOUD HEAD); pair == `4ce72c343d` blob `4a9a649e60` (== HEAD);
  crosswalk == `0d09727e53` blob `30a1ac7249` (== HEAD).
- **timeseries is a NOVEL blob `2e3832829b` = the running pin's own file (`70374ee65d`) + EXACTLY Phase B's hunk**
  (`GLOBAL_MODEL_KEYS` 10 -> 9, `opal_fixed_income` dropped, comments). CLOUD's copy (`34c1752129`) additionally carries
  ~275 lines of MDPF_TAXSMA tax-overlay work that this pin does NOT carry and does not ship. The CTO's exercise ran on
  CLOUD's copy; THIS pin's copy is exercised in s.2.
- `opal_fixed_income` across all 24 members: 0 live-code string literals, 11 comment/docstring mentions (AST read).

**FALLBACK, if a half signs Phase A only:** pin `bc089b4309`, zip 867,224 B sha256 `0acbd2a5ed775da8...` (built,
diffed: ADDED `mdpf_name_discovery.py`, CHANGED slice/pair/manifest, 20 unchanged). Phase B's three files are coupled
(slice + timeseries + crosswalk), so it ships all three or none.

---

## 2. LEG A -- VERIFICATION AT REST (every claim here was exercised, and each has a control)

1. **The import-closure gate is BLIND to this defect -- its PASS is not evidence here.** The PRE-FIX builder (blob
   `1ce68e2bc8`, no PACKAGE row) at the pre-fix tip `4307f067e2` ALSO printed `OK: import-closure` and wrote a zip with no
   `mdpf_name_discovery.py`. The import sits in `try: ... except ImportError:` whose fallback inserts
   `../../../mdpf/scripts/gold`, a path absent in a flat zip. The gate treats the guarded import as optional. **So the
   PACKAGE row is the only thing between this deploy and a zip that fails every Cottonwood run.** (Flagged to the CTO
   as a gate gap; not fixed here.)
2. **Discriminating import test** (each zip extracted OUTSIDE the repo, `python -I`, cwd only):
   pre-fix-builder zip -> `build_cottonwood_mdpf_slice` / `_pair`: **`ModuleNotFoundError: mdpf_name_discovery`**;
   THIS zip -> consolidator, slice, pair, timeseries, crosswalk, account_distribution: **IMPORT-OK**; live zip -> OK.
3. **Crosswalk `_self_test()` from the zip: PASS** (10 models: 7 served, 5 core, 2 sma, 2 blend -- unchanged).
   `GLOBAL_MODEL_KEYS` = 9, `opal_fixed_income` absent. `is_auto_custom`: stuck name TRUE, `Opal Fixed Income` TRUE
   (Phase B), non-Opal name FALSE.
4. **QA DRY-RUNS FROM THIS ZIP AGAINST LIVE INPUTS -- no bytes written** (both CLIs default to DRY-RUN):
   - slice: *"GATES PASS (absent-is-not-zero + strict-Opal filter + conservation + W-2b identity)"*; source vintage
     2026-09-18; model_aua 176,034,872.82; custody 480,290,362.43; non_model 304,255,489.61.
   - pair (assignment 2026-09-21 x value 2026-09-18): *"IDENTITIES PASS: (i) decomposed==dim to the penny, (ii)
     model+non_model==firm, (iii) bridge complete, count-axis parity"*; `|decomposed - dim|` = 0 cents; by_model = the
     5 primary keys; model 176,034,872.82 (== the slice, to the cent).
5. **NEGATIVE CONTROL -- the production failure reproduced:** the same slice dry-run from the LIVE bundle ->
   `ValueError: no canonical by_model key for Cottonwood model ' Opal Moderate Income Portfolio (Tax Efficient)'`.
   The only difference between (4) and (5) is the bundle.
6. **Name census**, Cottonwood gold `dim_model_portfolio`, last 15 partitions (to `date=2026-09-21`): 10 distinct
   `is_opal` names -- 5 CANONICAL, 2 DECLARED RESIDUAL, 3 AUTO-CUSTOM (`' Opal Moderate Income Portfolio (Tax
   Efficient)'`, `'Opal Fixed Income'`, `'Opal Income Portfolio - Gillham'` -- a second new name the old code would also
   have crashed on), **0 would-raise.**

---

## 3. LEG A -- KEYS THE ACT TOUCHES, AND THE ROLLBACK PER KEY (CRO item 2)

| key | change | rollback |
|---|---|---|
| `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` (versioning ENABLED) | one new version, content-sha256 = `9c6db39a...` | the prior version `9GsracvIPvfBMzF1dttMpew0TkQtt.qg` (== running CodeSha256, confirmed by re-download) restored as latest |
| Lambda `mdpf-gold-lambda` code | CodeSha256 -> b64 of `9c6db39a...`, CodeSize 868,952 | `safe-apply` with the artifact restored and the literal reverted; read back CodeSha256 `evIYCXUR...`, CodeSize 835,383. Never `update-function-code` |
| Lambda env `MDPF_GOLD_COMMIT` | `48b8671569...` -> `74d7efe1449b47587cf0d8ca47e3a0f9824bf297` (set from the pin BUILT WITH, confirmed against the zip's in-zip manifest) | revert to `48b8671569b72efb4eca64ef41ded4de9c54e84c` |
| `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf` literal | one line, CLOUD commit | revert the commit |

**The apply's own blast radius, read before it runs:** the root's untargeted plan (this turn, 19:37Z) shows **no
resource changes**. Its only drift is OUTPUT `mdpf_route_bindings_sha256` (pre-existing; the 09-15 deploy also left it
untargeted). After the upload + literal, the targeted plan must show EXACTLY `aws_lambda_function.mdpf_gold` update
(`s3_object_version`, `source_code_hash`, `environment.MDPF_GOLD_COMMIT`), 0 add, 0 destroy -- or the apply does not run.

**Keys the NEXT SCHEDULED FIRE may touch (the fire, not this act):** the consolidator's existing families,
`s3://opal-data-assets/portal/gold/mdpf/{49financial,inflection,cottonwood,global}/{type}/{date}.json` +
`_manifests/{date}/{run}.json`. Today's fire wrote 49financial/inflection only; cottonwood and global were last written
2026-09-16 (newest keys `.../2026-09-15.json`). Downstream, the egress publisher (its own 12:15 ET schedule) projects
CHANGED gold bodies to `s3://opal-data-portal-v2/platinum/mdpf/{scope}/{type}.json` (D5: unchanged body = no rewrite).
**Rollback per served key:** both buckets are versioned (ENABLED, measured). Gold keys are dated. A bad date is
superseded by the next good fire after a code rollback, or restored by version. The platinum keys revert on the next
publish from reverted gold, or restore by version.

---

## 4. EXPECTED OUTCOMES, READ FROM THE PRODUCER'S OWN RULE, BOTH BRANCHES -- AND WRITER COUNTS (CRO item 3)

**The rule (read at the pin, not predicted from the input):**
- `build_slice`: keep `is_opal` rows; CUSTOM = declared residual OR `is_auto_custom` (NOT canonical AND word-boundary
  "Opal"); everything else goes to `canonical_key()`, which **still raises** on an unknown name.
- `assert_identities` (pair): `SystemExit(1)`, nothing written, unless decomposed == dim (2 cents), model + non_model ==
  firm, bridge complete, count parity -- the custom bucket now counted on both axes (`4ce72c343d`).
- consolidator I-1 leg pins: a cottonwood refusal skips global.

**BRANCH 1 -- today's data shape (0 would-raise names, s.2 item 6):** cottonwood slice + pair build and pass (s.2 item 4);
cottonwood's gold is written at the data frontier 2026-09-18; global is built from 49financial + inflection + cottonwood
with **by_model = 9 keys: no `opal_fixed_income` line**. Fixed Income's dollars sit in cottonwood non_model / Other AUA
and in `custom_residual_detail` (named, `auto_classified: true`). **THAT IS A SERVED-SHAPE CHANGE ON GLOBAL**, the one
Andrew approved in call 2.
**BRANCH 2 -- a new `is_opal` name that is neither canonical nor word-boundary "Opal", or any other guard:**
`canonical_key()` raises or the identity gate exits -> cottonwood refused, global skipped, 49financial + inflection
written. That is today's state; the deploy makes no branch worse than the running code.
**This half does not predict which branch the fire takes -- the fire does.**

**WRITER COUNTS of the served properties named above** (instrument: `comp-find 'portal/gold/mdpf' --files --all`, 2,075
hits across 171,367 files scanned, 16 code files; write verbs counted in all 16; every write site READ):
- `opal-data-assets/portal/gold/mdpf/{cottonwood,global}/**` -- **N = 3**, 3 rules read:
  (1) `mdpf_gold_consolidator.py` -- THIS Lambda, scheduled 13:30Z, writes per date (the rule above);
  (2) `dim_mdpf_aum_metrics.py::_put` -- standalone CLI, `aum-metrics` type only, ad hoc; not changed by this deploy;
  (3) `build_portal_gold_accrual.py` -- the accrual bridge, own schedule, **R5 no-clobber: never overwrites an existing
  key** (`--allow-overwrite` off), so it cannot overwrite a date the consolidator writes.
- `opal-data-portal-v2/platinum/mdpf/**` -- **N = 1**: the egress publisher (D5 no-rewrite on an unchanged body).
- NOT the served tree, named so it is not confused with it: the EC2 runner's WS-A writes
  `opal-data-assets/gold/mdpf_revamp/_aggregate_aua/`.
- The census counts repo code. Console and CLI writes are not enumerable; they are banned (NEVER-9), and a ban is not a census.

---

## 5. LEG B -- THE EC2 RUNNER'S S3 CODE SYNC (Andrew: "Sign first, then push")

**The consumer:** `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:122-125` --
`aws s3 sync s3://opal-data-mdpf/code/scripts/ $SCRIPTS_DIR/ --delete` on every run, no pin, no import gate. Instance
`i-02448edb624a7a7cf`, launched 2026-09-21 13:40:22Z (runs daily ~12:52Z, then stops).

**LEG B's write set -- computed with safe-deploy's OWN functions** (`safe_deploy_core._changed_paths` rule +
`file_to_s3_target`), over the pending range `origin/CLOUD d32d3ad8b8..HEAD 0965835083` at **19:52:45Z**:
185 files changed, **6** `data/*/scripts/*.py`:

| S3 key (versioning ENABLED) | current S3 (blob) | after push (CLOUD HEAD) | delta | rollback VersionId |
|---|---|---|---|---|
| `opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_slice.py` | `e41b6c8b2f` (= running pin) | `127bad164b` | == LEG A's slice bytes (reviewed) | `9sQ6pQNRf8Zk9u86uusDXsYsmrmLAjkk` |
| `opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_pair.py` | `ffca06c843` (= running pin) | `4a9a649e60` | == LEG A's pair bytes (reviewed) | `b59tDxx.A03FHyDFB8_MD6H_cc2q4n73` |
| `opal-data-mdpf/code/scripts/gold/mdpf_revamp_model_crosswalk.py` | `5323ee8a41` (= running pin) | `30a1ac7249` | == LEG A's crosswalk bytes (reviewed) | `NA2MepxPsfQ0_rbaS3X0.Haa8NOV8UJ9` |
| `opal-data-mdpf/code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | **`3e1423e4a1` = CLOUD `5e8ba0e1d4` (MDPF_TAXSMA W2-S1), synced 2026-09-21T08:55:37Z** | `34c1752129` | **EXACTLY Phase B's hunk** (`0d09727e53^` == S3 today) | `syiCAA6n7.C9SSVDvJiQ1MLiPGn7ITJQ` |
| `opal-data-inf/code/gold/lib/tests/test_nna_coverage_guard.py` | `0cb44fa036` | HEAD | ANOTHER SEAT's test file riding the same push; NOT this deploy | `Lfw1C7oeuVMbMJmQWWVHoofOoXd3GK.u` |
| `opal-data-inf/code/gold/lib/nna_coverage_guard.py` | == HEAD | == HEAD | NO-OP | -- |

**THE CORRECTION THAT MATTERS FOR THE CTO's 99211:** the MDPF_TAXSMA overlay in the timeseries file is **ALREADY on
LEG B's path** -- S3 holds `5e8ba0e1d4`'s bytes since 08:55Z today. A raw push does not ship it; it ships Phase B's hunk
on top of it. The CTO's option (a), a scoped sync of the PIN's timeseries bytes, would REMOVE the TAXSMA work from the
EC2 path. That is a rollback of another project's deployed code, which this packet does not recommend.

**What the EC2 consumer DOES with it, read from the dispatch:** the Cottonwood pair/slice run only inside Stage 6 (`:547-556`,
both `--upload`), AFTER `build_mdpf_spine.py --firm all` (`:504`). Today's run log
(`telemetry/mdpf-daily-runner/logs/mdpf_daily_20260921_125229.log`): Stage 6 fails at IMPORT in 1 s --
`build_mdpf_spine.py:51 -> dim_mdpf_aggregate_aua_timeseries.py:75 -> taxsma_assets.py:95: ModuleNotFoundError: No
module named 'lib.opal_naming'` -- *"NON-FATAL build-alongside; legacy chain + serving UNAFFECTED; no marker written"*.
**So with LEG B, the EC2 outcome is UNCHANGED until that TAXSMA import is fixed** (it fails before any Cottonwood code).
If it is fixed, Stage 6 would run the reviewed Cottonwood code (which passes, s.2) and write only its build-alongside keys.
The legacy stages that serve do not reach any of the 4 files: **0 of the 7** `run_step` scripts the dispatch runs import
any of the 4 or any of their 8 intermediate importers (consolidator, spine, aum_metrics, account_distribution,
category_registry, revamp_trio, count_source_audit, eclipse_vintage_reconstruction) -- import census at the source, one
level of transitivity.
**The CTO's 99211 (TAXSMA would ship via LEG B) is RETRACTED by its author @`0962ba51c5` (msg 99219)** after a third
instrument agreed: served-vs-HEAD for that file is exactly Phase B's 18 lines.

**LEG B's range is PERISHABLE:** it is whatever is unpushed at push time. The push step re-derives this table
(same functions, printed) immediately before the push. A new script in the range is outside this signature.

---

## 6. CHANGE MANAGEMENT AND ACCEPTANCE (CRO item 4)

- **Ledger opened at deploy start** (before the upload), `org/critical_paths/change_management/`, legs:
  L1 S3 upload (read back version + content-sha256 + re-download hash); L2 `MDPF_GOLD_COMMIT` literal commit; L3 targeted
  plan (exact set, s.3) + `safe-apply`; L4 post-apply proof on the RUNNING plane: CodeSha256 == b64(`9c6db39a...`),
  CodeSize 868,952, `MDPF_GOLD_COMMIT` == pin, re-downloaded in-zip `source_vintage` == pin, AND a control that reads
  FALSE today: `mdpf_name_discovery.py` a bundle member / `is_auto_custom` in the slice -> FALSE pre, TRUE post;
  L5 LEG B: re-derive the s.5 table immediately before the push, then read back each synced key's blob == HEAD.
- **Acceptance:** the **2026-09-22 13:30Z** scheduled fire (`mdpf-scheduled-floor`, ENABLED, `cron(30 13 * * ? *)` UTC):
  run manifest + cottonwood and global `as_of_last` / `_provenance.written_at` advance on the served plane. **Never an
  ad-hoc invoke** (08-26 ledger :66-69): time of day is the discriminator. The ledger closes the DEPLOY; acceptance is a
  separate read.

---

## 7. WHAT THIS PACKET DOES NOT COVER

1. The other seat's `test_nna_coverage_guard.py` on `opal-data-inf` (s.5). It rides the push but is not this deploy's.
2. `opal-assets-daily-emitter`: the vendored crosswalk was committed @`650df7371e` (byte-identical to canonical, behaviour-neutral:
   the emitter reads only `CORE_MODEL_KEYS` and the id maps). That Lambda is not redeployed.
3. A CLOUD-HEAD build of the Lambda. Not built; minimal pin.
4. The import-closure gate's blind spot (s.2 item 1) and the EC2 Stage 6 `lib.opal_naming` break (MDPF_TAXSMA): surfaced,
   neither fixed here.
5. Any acceptance claim. The deploy puts code in place; the 09-22 fire is the acceptance.

## 8. WHAT THE HALVES SIGN AGAINST

This file's committed blob (named in the commit that lands it) + LEG A zip sha256
`9c6db39ae8ae7c9d21060dfbdc5bb451053fbca9564cd046f3df75090804d0cd` @ pin `74d7efe144` (or the Phase-A fallback
`0acbd2a5ed775da8...` @ `bc089b4309`, if a half says so) + LEG B's s.5 table as re-derived at push time.
