# MDPF_CANON round 9 -- drain-end packet, DRAFT (2.0.0_SA_COO~D1), 2026-10-15 ~02:4xZ

To `3.0.0_SA_CVO` (L8/L9) once finalised. **Status of this file: DRAFT.** It is finalised and sent after (1) the 2026-10-15 13:30Z gold fire and 13:50Z publisher fire are read with `round9/checks/fire_read.sh`, and (2) the edge-gate proof leg (laptop, `0.7.0_AE_CloudOps~U7`, ledger `mdpf-canon-edge-firm-gate`, leg L5) is read. Input: the CTO's msgs 5868-5886 and 5913 and PRD v2.19-v2.21 (Variant 1), the CRO spec `MDPF_CANON_GLOBAL_AUA_TREND_FULL_HISTORY_SPEC_20261014.md` @686f769e63; Andrew-direct records `ANDREW_DIRECT_20261014_204xZ_COO_D1_WHATEVER_CRO_DELL1_AND_I_AGREED.md` and `ANDREW_DIRECT_20261015_01xxZ_COO_D1_TREND_LOOKS_GOOD_CUSTOM_ROLLFORWARD_THEN_PROD.md`. Decomposition v9 and three orders: issuance `94f8cbd3d9`.
`round-close-check.py --project MDPF_CANON --round 9` reads (02:30Z): 3 of 3 orders complete, proofs 3 of 3 structurally valid, 2 JUDGMENT criteria ungraded (CN-p-1 AC4, CN-p-2 AC4), verdict REFUSED (those two only; CN-q-1 carries no judgment criterion).

## 1. Orders, merges and evidence (MEASURED by the issuer at the merged tree)

| order | worker | merge | mechanical result | judgment owed |
|---|---|---|---|---|
| CN-q-1 the edge admits a per-firm MDPF leaf only to the claim's own firm (WORLD floor; build = code and tests) | ~28 (two seats: first pass refused by the LGIC naming gate, row W28-S1; re-cut on the CRO's generator `1fc3358292`) | `643932fee0` | handler 14 of 14, seam 5 of 5, control 6 of 6; edge tests 29 pass; shared-advisor-router tests 30 pass | none |
| CN-p-1 the producer serves the Trend groups (WORLD) | ~26 (two seats: the first pass built a fail-open, row W26-S2, closed by AMENDMENT 1) | `8e2dd0fb36` | pure 7 of 7, seams 7 of 7, oracle 7 of 7; pytest 47 passed; ruff clean | AC4 |
| CN-p-2 the portal Global Trend, Variant 1 for an internal session and Variant 2 for every other (LOCAL, client-facing) | ~27 (three seats: footnote scope, then the Custom Models roll-forward) | outer `3740edf6e6`; portal candidate `15f7610285` | oracle 7 of 7, variants 12 of 12, wiring 10 of 10; `bun run typecheck` rc 0 (planted-error control rc 2); provenance guard OK | AC4 |

## 2. WORLD acts and their evidence

- **CN-p-1 deploy** (`ADHOC.canon-r9-gold-trend-groups-deploy`, CloudOps DELL1, 2026-10-14 22:50Z, pin `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f`): plan 0/1/0, D4 green with `errors` empty, 16 served and 5 overwrite keys unchanged. Pair `NEVER_WIDEN_PAIR_R9_CN_P_1.md` signed by both halves (COO `54da2eb87d`, CTO `d996228e93`); the CN-h-1/CN-l-1 and CN-p-1 field sets are disjoint on every leaf.
- **One-time publish** (`ADHOC.canon-r9-trend-publish-tonight`, Andrew's overwrite OK; ADDENDUM 1 signed COO `1e52755b27`, CTO `83ec2d7b0e`, C2 amended `da6e7b36d0`): eight gold puts 23:10Z and one publisher run 23:11Z (18 published, none failed). **PROVENANCE: a splice authorised by Andrew, not a lambda run; never evidence of the lambda.** The issuer re-measured every one of the eight keys against its pre-splice VersionId: each differs only by the CN-p-1 keys (Global also `meta.trend_groups`) or the one `muni` member. Live readback 11 of 11 arms.
- **CN-p-2 PROD promote** (`ADHOC.canon-r9-trend-portal-promote`, DT~H1): PROD `c3b21a40e29f690922f442c085129f9ba85ce334`, tag `portal-v2.1.223`, CI run 38667132776 success, bundle reads clean (62 files, 6 x 403; the three new strings 0 before, 1 after). Row `dell1-20261015T013256Z-f411` closed approved by Andrew. DEV converged by merge-forward of the resolution branch (row `c397`, waiver `f93e2f6bf8`): DEV `e0b033253b`.
- **Edge gate deploy** (`ADHOC.canon-q1-edge-firm-gate-deploy`, laptop CloudOps `~U7`, crossbox `XB-20261014T222322Z-3242`): `auth-validator-edge` v24 applied 23:06Z on 27 of 27 associations (laptop CTO's read, relayed by MSTR); no-token GET 401 on two leaves. **L5 (the proof leg) is OPEN**; the laptop CTO's ruling `916f09fb81` holds, no rollback, window to 07:00Z.

## 3. The real run (the issuer looked at the page)

`/ui-walk` as the internal walker on port 5174 (portal `wk-MDPF_CANON-27-portal`; first with a local override of the one Global series path, then plain `dev:live` over the real served object): the Global Trend draws the full history, Nov 2024 to Oct 13; Client Supervised, ETF Strategies, ALT Strategies, Custom Models (no gap from 2026-05-15 after the roll-forward) and the carried legend entry; the 49 Financial view is unchanged and carries no composition footnote. Local screenshots only. **Not exercised:** a NON-internal session (Variant 2): no partner or demo login exists; the unit arms V1-V12 grade it on fixtures, and AC4 is yours to grade on that limit.

## 4. PENDING before this packet is final

- The 2026-10-15 13:30Z fire: `bash round9/checks/fire_read.sh gold` (frontier counts, Other Models row, Trend groups with R9 against the pin; the CTO's condition C1: the R11 leg-presence arm).
- The 13:50Z publisher fire: `bash round9/checks/fire_read.sh publisher` (the CN-j-1 history leaf, H9).
- The edge L5 proof from the laptop.

## 5. Rows, enrichment candidates and what is the CVO's

ARMED rows are dispositioned by the CVO's clock (R-15); this seat's own rows at this round: `MDPF_CANON-D1-W26-S2` (closed on the branch, the arm S7 grades it, disarms on the fire), `W28-S1`, `W27-S1..S4` (INERT observations; S4 names a stale page comment). Candidates for the CTO's round-N analysis: (a) `compute_trend_groups` reads a missing Dividend/Growth/SMA value as zero on a total-bearing row (the CTO: contradicts PRD override (c) in letter); (b) the publisher role is denied `GetObject` on `latest.json`, so its unchanged branch never fires and every run republishes all 18 pairs; (c) the `build_all` Custom Models series rolls any null forward in Variant 1 while the other groups roll only on `carried_dates` (a rule asymmetry to ratify); (d) the readback R6 arm tolerates at most five restated cells per array (a threshold to ratify); (e) `portal-merge-forward.sh` has no path for a feature whose earlier copy is already on DEV (it refuses `conflict`, and the approval tool refuses any DEV-based branch `dev-overlap`): this round used a CTO waiver.
