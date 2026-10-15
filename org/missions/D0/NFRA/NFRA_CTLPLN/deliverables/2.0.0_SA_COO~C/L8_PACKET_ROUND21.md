# NFRA_CTLPLN round 21 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~18:2xZ)

All four round-21 orders are `complete` (issuance `57922ec762`, amendments `4d79c7c58c` and `9b2702a5a5`, decomposition `NFRA_CTLPLN_DECOMP.round21.md`; merges `be732b30a0`, `4e5affbf52`, `57f13ba60a`; flips `97db771d1e`, `7eae244033`, `4f93acb5f4`, `5ac8ec35ff`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 21` reads `verdict=MAY-CLOSE`, `orders=27 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL unless stated. Inputs for the analysis: `ROUND21_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge / seat | issuer re-run |
|---|---|---|---|
| `CT-ak-1` | 19, 15 | `be732b30a0` | `CHECK-DEVICE arms=6/6 ok=True`; `INTAKE-CHECK-TEST cases=57/57 skipped=0 ok=True`; `FETCH-DEVICE arms=8/8 ok=True` |
| `CT-ak-2` | hygiene | `4e5affbf52` | `HYGIENE-MAP tsx_classed=1 py_classed=1 ok=True` (main tree, fresh map); `HYGIENE-MAP SKIP map STALE age=100.0h`; `FABRIC-CENSUS ... unclassified=0 ok=True` |
| `CT-ak-4` | 5 | `57f13ba60a` | `FWD5-PRE ... differs=True others_differ=0 ok=True` (68 of 68 other top-level gold scripts equal S3); `AST-IDENTICAL ast_identical=True`; `PARSE-OK`; ruff clean |
| `CT-ak-3` | 5 (WORLD) | seat `0.7.0_AE_CloudOps~CT2`, close commit `35ac3c0dd0`, proof `4781da8f97` | `FWD5-POSITIVE versions=2 etag_equals_repo_md5=True` (issuer, 18:08Z); the audit log row below |

Every proof instance reads VALID on the committed state (`CT-ak-4`'s only after its merge: its branch was cut before the order's amendment, row `W118-S2`). Amendments by the issuer, each in its own commit: `CT-ak-3` re-pointed from the dead `0.7.0_AE_CloudOps~U7` (which holds an unrelated order) to a fresh lane `~CT2` with its paths cut, and the commits it could not make (lanes POD4 and TOOL_BATTERIES admit only a worker serial) moved to the new worker cell `CT-ak-4` (row `S9130`); `CT-ak-4`'s signed change became comment-only and `CTak4-AC2` became `--ast-identical`, because `diag_sleeve_fix.py` fails ruff at the previous commit and its line-2 string is not a module docstring (row `W118-S1`). GATE (viii) of `to-pipeline-gate` graded the modified orders and passed.

## 3. What each outcome now stands at (evidence, not a grade)

- **FWD-5, the positive arm (WORLD):** the one signed change (`diag_sleeve_fix.py`, comment-only, commit `461e3f64ee`, blob `8d6f273a9e`) deployed exactly one S3 key. `s3://opal-data-bd/code/gold/diag_sleeve_fix.py` holds 2 versions (new VersionId `ceImQVXASssU3IUCRXRjMkoA1XnifTf7`, written 2026-10-15T18:02:18Z) and its ETag equals the committed script's md5 `c204fd9be3bbfc43346a14b4c71051af`. `org/safe-deploy-bypass-audit.log`: two HELD-DEPLOY rows for the path (17:51:27Z, 17:53:05Z, `no-open-ledger-names-it`: the negative arm, for real, before the entry opened) and exactly one PINNED-DEPLOY row (18:01:57Z, slug `ctlpln-r21-fwd5-one-script-20261015`, pin `971327859b33`). The CloudOps seat reports 0 of 190 other `code/gold/` keys changed since the entry opened (the issuer's own count was refused by the comp rail and is not made). **The actor was `0.0.0_AB_MSTR`'s scheduled box-sync push, not the CloudOps seat:** LD-0367/0368 lets only the integrator push `box/laptop` (row `S9132`; it contradicts the CLAUDE.md "agents push at will" line, which is the CTO's to reconcile). The path was the `D1-S8` pinned-entry step: the script had already reached CLOUD by integrate, so it was in no box diff, which is the very case the `D1-S8` fix was cut for. The NEVER-2 entry was opened and closed by the seat (all 3 legs). The rollback VersionId `3.yZFEuxxfxUOEMd.NRY7bZucaDccGX.` was recorded and not used.
- **FWD-3:** `python .tools/crossbox-matrix.py` reads `pairs=12 with_file=12 acked=12`. The five pairs never before acknowledged by a manager (dell1->laptop, dell2->dell1, dell2->sitez, sitez->dell1, sitez->dell2) were each opened by the sending box's manager and acknowledged by the receiving manager through `0.0.0_AB_MSTR` (msgs 109456, 109457; `sitez->dell1` acknowledged at 17:01:07Z).
- **FWD-21:** site Z's manager quoted lines 19401-19404 of its spawn audit log verbatim into a committed record, `org/tier0_exec/0.0.0_AB_MSTR/deliverables/SITEZ_SPAWN_AUDIT_QUOTE_20261014_2332Z_RESPAWNS.md` @be4c42da12 on `origin/box/sitez` (four SPAWN lines at 23:32:26Z to 23:32:43Z by `0.0.0_AB_MSTR~Z`; 0 specific asks found). The issuer read the file (`git show origin/box/sitez:...`). The committed copy of the audit LOG itself ends 2026-10-09 (row `S9128`, owner `0.0.0_AB_MSTR`).
- **FWD-14 (the box's own record, as ruled in the CTO's record of Andrew's word):** event 1149 connections from the MacBook (`rc`, `100.98.173.75`): laptop 28 (latest 2026-10-15T02:49:50Z, read by the issuer), site Z 37 (earliest 2026-09-22T23:16:10Z, latest 2026-10-12T20:20:10Z), dell1 3 (2026-10-07T22:23:20Z to 2026-10-13T22:29:14Z), dell2 3 (2026-10-07T22:30:45Z to 2026-10-13T22:30:34Z). Not read: the Windows laptop to site Z, dell1, dell2 arm; the refused attempt from outside the tailnet. Andrew's session tonight (`c9a4`) stays open.
- **FWD-11:** Andrew restarted dell1 himself (call `7841` CLOSED). dell1's manager reports: last boot 2026-10-15T15:46:57Z, restart initiated 15:46:25Z, reason Other (Unplanned), by the `Test` account, event 6005 at 15:47:06Z; previous boot 2026-10-14T06:29:22Z (planned OS-upgrade restart); 14 seats registered LIVE by 17:1xZ. **Not measured:** which seats held which round at 15:46Z, and whether anything was left half-done (18 open deploy-ledger entries in the shared tree were not classified as interrupted or ordinary).
- **FWD-15, 16, 18, 19 (the package journey):** `polars` (a request naming no lane) is decided REFUSED (@8e78591d2b); dell1's CTO named lane `2.0.0_SA_COO~D1` (MDPF_CANON) and its question (the SMArtX sleeve day-over-day on `s3://opal-data-mdpf/mdpf/global/gold/aggregate_aua_timeseries/`); `duckdb==1.5.0` is filed (`REQ-20261015T171032Z-duckdb`) and APPROVED by the CTO (@ec54e27083) with a fetch approval for exactly one wheel (@29a69ec1c5); the CRO's co-decision is outstanding. dell1's interpreter tag is asked (call `XB-20261015T174945Z-6bd5`, not yet answered). Fetch records and the check step's fetch-shaped records carry the device. FWD-18: site Z refused one download (exit 3, route named) and so did the laptop.
- **FWD-24:** the laptop CTO answered OWED; site Z's CTO has not answered `e670`.

## 4. FWD state

`FWD-11`'s call `7841` is closed on Andrew's word; `FWD-9` PARKED; `FWD-14` call `c9a4` and `FWD-17` call `318f` open for Andrew; the clean-up call `715c` was executed by the CTO.

## 5. Rows this round minted

`W116-S1`, `S2`, `W117-S1`..`S4`, `W118-S1`, `S2`, the issuer's `S9128` and `S9129`, the CloudOps seat's `S9130` (BLOCKING), `S9131`, `S9132` (BLOCKING). Ruled by the issuer: `S9130` (amend and re-point, see section 2), `S9132` (the order's actor claim was wrong; see the first bullet of section 3), `W118-S1` (comment-only change), `W118-S2` (merge first, validate in the main tree), `W116-S1`/`S2` (the check verb's own record carries no device and the downloads reader reads only fetch records; not cut), `W113-S1` disarmed by `S9129`. `S9131` is moot for this deploy (the pinned path writes an audit row). Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`, `S9128` (MSTR), `W117-S2`/`S3` (the map's producer is not scheduled; owner `1.0.0_SA_CTO`).

## 6. Not measured here

The fetch, check, taildrop and install of the approved wheel and the lane's own run; the CRO co-decision on duckdb; site Z's FWD-24 answer; the Windows-laptop remote-desktop arm and the off-tailnet refusal of FWD-14; what was in flight across dell1's restart; the PRD FWD grade table, which the CVO's re-grade governs.
