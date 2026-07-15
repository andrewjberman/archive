# OPAL_GLDRNS.B1 — Serve-held AoR bundle manifest (staged for CTO arch-gate review, ~22:3xZ slot)

**archetype:** SCRIBE
**agent:** 0.4.0_DS_ClientPlatform~B · 2026-07-15 ~21:1xZ · feeds: G3 review (CTO accepted-slot 20:54:34Z msg)
**DENOMINATOR:** comp-pipescript deployed sweep (inf-gold tree, run ~20:15Z this session): 33 tracked gold
scripts compared; 21 MATCH · 8 STALE · 2 MISSING_ON_S3 · (2 basenames frozen-3, out of bundle by law).
Bundle = the 10 non-MATCH files below + 1 lib parity note. All carry the DEPLOY-SERVE-HELD sentinel.
**Scope of the review being requested:** DEPLOY-WITH-CHOKEPOINT-HELD only (CTO 20:54:34Z: never-widen
co-sign on SERVING stays at its own gate). Deploy != run: chokepoint verified HELD this session.

## The 10 files

| # | script | deployed vintage (md5-8) | repo (md5-8 @ commit) | diff lines | what changed since the deployed vintage |
|---|---|---|---|---|---|
| 1 | INF_A_0.aor_resolver.py | **MISSING_ON_S3** | @ 345c85daa (07-12) | n/a | THE RESOLVER — writes the AoR SSOT + ledger; presence-gated chain entry (dispatch reads resolver-absent today). Chain CANNOT fold without it. |
| 2 | INF_D_11.aor_attribution_drift.py | **MISSING_ON_S3** | @ 1a107c20b (07-12) | n/a | the attribution-drift detector (AOR-DRIFT-ALERT token, exit-0 advisory). |
| 3 | INF_A_00.accounts_dimension.py | 07-11 22:49Z (31df1725) | 49a81251 @ 8ca92d80c | 117 | 5581c0de1 consumer-migration + **8ca92d80c F2/F9: pin AND assert source digest in both full-attach consumers** (closes the silent-row-loss class). |
| 4 | INF_A_01.advisor_assignments.py | 07-13 02:50Z (b1e54a38) | 966bc4e6 @ 8ca92d80c | 66 | **8ca92d80c F2/F9** (deploy predates the commit by 3.5h — TZ artifact resolved: 02:50Z deploy vs 06:29Z commit). |
| 5 | INF_C_02.client_performance.py | 07-12 01:12Z (afec8593) | da93670f @ dbd10d7aa | 1,082 | 5581c0de1 + fc0a85362 (F4/F7/F8 fail-closed-on-unobservable) + **dbd10d7aa C_07-class sweep**. |
| 6 | INF_C_07.advisor_attribution.py | 07-12 01:39Z (8db12678) | 7c33f187 @ dbd10d7aa | 947 | 223a71982 CHANGE-3c wiring + 5581c0de1 + **dbd10d7aa: DELETES the override that silently UN-FOLDED AoR on the served view** (the gate-2 retraction defect). THE single most load-bearing file in the bundle. |
| 7 | INF_D_00c.portal_leaderboard.py | 07-11 22:49Z (59c85362) | dfd73226 @ 5581c0de1 | 8 | 5581c0de1 consumer migration (fold census 10->1; views inherit the canonical resolution). |
| 8 | INF_D_00d.cumulative_chart.py | 07-12 01:12Z (0f52d670) | 94c149e3 @ dbd10d7aa | 26 | 5581c0de1 + fc0a85362 + dbd10d7aa (as #5, small surface). |
| 9 | INF_D_00f.advisor_nna_canonical.py | 07-11 22:49Z (822df65b) | a3029cf2 @ 5581c0de1 | 8 | 5581c0de1 consumer migration. |
| 10 | INF_D_02b.top_holdings.py | 07-10 23:37Z (d1eb9268) | 38066955 @ 5581c0de1 | 746 | 5581c0de1 (oldest vintage in the bundle; pre-dates the whole round-8 consumer migration). |
| + | lib/advisor_of_record_conformance.py | deployed lacks the 2-line sentinel comment (only diff) | 6ac1f9b9 dep / f25e882c repo | 2 | parity-only redeploy with the bundle (functionally identical today). |

## Refactor-census note (persistence duty, Andrew DIRECTIVE 8): the Group-D/platinum surfaces touched

| script | output keys (grounded where marked) | portal consumer |
|---|---|---|
| INF_D_00f | `platinum/firm/advisor_nna_canonical.json` + `platinum/advisors/{advisor_key}/nna_clients.json` (GROUNDED live this session: read + tied to the cent) | the served per-advisor NNA spine — the surface the FE AoR allowlist pair (73ee2705+b005545e, portal-v2.1.136) waits on; noel_soderblom prefix appears only post-fold |
| INF_D_00c | portal leaderboard artifact (record-known, not re-grounded this pass) | leaderboard view |
| INF_D_00d | cumulative NNA chart artifact (record-known) | cumulative chart |
| INF_D_02b | top-holdings artifact (record-known) | holdings view |
| INF_D_11 | AOR-DRIFT advisory log/token (no served artifact) | none (operator instrument) |

## Deploy plan on clearance (what I execute, in order)

1. `.tools/deploy-import-lint.py` over the bundle (the 5-file-atomic lesson: aor_resolution hard-depends
   on advisor_timelock; NOBODY DEPLOYS A SUBSET — this bundle + already-deployed libs are mutually consistent
   at repo HEAD, which is what the lint asserts).
2. `aws s3 cp` all 11 files (10 scripts + 1 lib) to `code/gold/` (+ `code/gold/lib/`) — single session, no
   subset. AMEND-51 pre-flight per basename (none of the 11 exists in manual_api/silver/bronze — verified
   pattern from G1; re-run per-file at deploy time).
3. DOWNLOAD-AND-IMPORT verify every file (md5 == repo == origin/CLOUD; import the libs; AST marker checks on
   the load-bearing calls: C_07 zero advisor_key writes, A_00/A_01 digest assert present, D_00f fold call).
4. Re-verify Door-5 ETags + chokepoint UNCHANGED post-deploy (the G1 pattern).
5. Report evidence to CTO same-session; chain stays held; nothing serves until the gated release.

**NOT in this bundle by law:** the frozen-3 (`build_assets_dim.py`, `_orion_api_silver_lib.py`,
`convert_transactions_to_silver.py`) — unfreeze only as in-order chain steps with the hold-lift, CTO-flagged
at that moment. Door 5/6 untouched.
