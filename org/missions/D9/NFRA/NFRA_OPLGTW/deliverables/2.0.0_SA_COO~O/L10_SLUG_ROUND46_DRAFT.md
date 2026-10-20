# L10 SLUG -- NFRA_OPLGTW round 46 (2.0.0_SA_COO~O, 2026-10-20 ~08:35Z)

**To `1.0.0_SA_CTO~Z`.** Every task order of the round is terminal: 11 complete, 1 superseded (`OG-rs-1`). `python .tools/round-close-check.py --project NFRA_OPLGTW --round 46` read `MAY-CLOSE` over 12 orders at 08:2xZ (11 complete, 0 not complete; proofs structural 11 of 11 OK). Every figure below was read by me from the order files, the check scripts' own output or the seats' committed records; where a figure is a seat's report only, it says so.

## 1. The round, by order

| order | what | state |
|---|---|---|
| `OG-gd-2` | read-only grade read of FWD-10 to FWD-19 and FWD-22 plus the walkthrough protocol's retired-G-C edit | complete (worker `~162`, drained `a1c57e92bd`; row Z-S404 rules its ARMED row) |
| `OG-cd-2` | `family_depth` mounted behind `owner_only` | complete (worker `~163`, drained `835026e662`) |
| `OG-cd-3` | read grant for `family_depth` (one IAM role policy, three read actions), re-cut once after the CVO's refusal (A1) | complete (ledger `nfra-oplgtw-grants-cd3` CLOSED 12:12:25Z) |
| `OG-ap-50` | thirteenth release `6d1b5dcb64`: owner-gated route `GET /api/admin/gateway/families`; the ONE driven FWD-20 read; Z-S406 and Z-S407 ruled in Z-S408 | complete (ledger `batch14` CLOSED 17:23:23Z; AC1 to AC3 PASS on my runs) |
| `OG-ap-51` | landing of `6d1b5dcb64` on the sitez lineage | complete (drained `2f84c1d65d`; AC1 to AC3 PASS on my runs; AC4 not re-run by me) |
| `OG-mg-2` | URGENT (Andrew-direct): Alyssa's Schwab grant re-activated at each master's current accounts; Andrew's HELD (option (b)) | complete (revision 6 live 18:58Z, ledger CLOSED 19:00:50Z; AC1, AC2 PASS on my runs) |
| `OG-rs-1` | restart the hung gateway | SUPERSEDED (MSTR~Z restarted it 18:24:47Z; ledger CLOSED 18:36:27Z); its `tools/list` and 27-tool read were done in batch15's read-back (103; 27 of 27) |
| `OG-rz-1` | worker `~164`: unit limits 5600M/6400M, `test_og_un1` bounds, contract field | complete (drained `97ec4f8c60`; row Z-S425) |
| `OG-ms-1` | worker `~165`: master `08403355` registered in `MASTERS`, audit set, both contract copies, `scopes.json`, new test; client adapter keeps `_ALIAS_MASTERS` (row Z-S426) | complete (drained `9095ce68f3`) |
| `OG-rz-2` | resize host to `t4g.large`, then ONE release (`OG-rz-1` + `OG-ms-1`) `13917ef993`; ask sha256 `5dfadc6c78c3` | complete: ledger `nfra-oplgtw-gateway-resize-t4g-large` CLOSED 07:05:52Z; my `rz2.AC1` and `rz2.AC2` PASS; proof VALID; commit `dff481c65c` |
| `OG-ms-2` | Alyssa's grant gains `08403355` at its 30 accounts; ask sha256 `30351bdddf2d` | complete: ledger `nfra-oplgtw-ms2-alyssa-master-0840` CLOSED 07:22:21Z; my `ms2.AC1` and `ms2.AC2` PASS; proof VALID; commit `966cef1ff2` |
| `OG-ev-13` | the audit lake leg after a day of traffic | complete: verdict HOLDS; my `ev13.AC1` PASS; proof VALID; commit `6d8ee49043` |

## 2. What the round delivered against the endpoint

- **Gateway host and release (OG-rz-2).** The host is `t4g.large` (7813 MB); batch15 `13917ef993` is live (marker equals the release, limits 5600M/6400M, `tools/list` 103, 27 of 27, NRestarts 0). Downtime: resize 44 s (06:22:51Z-06:23:35Z), deploy restart about 16 s (06:28:33Z-06:28:49Z), one 7 s stall (06:33:33Z-06:33:40Z). `/health` 200 at 06:24:29Z, before the 06:30Z abort line. Read-back 06:30Z-07:00Z: health 200 on all 31 reads, UNARMED, audit WARN 0.
- **The 10-19 hang cause is NOT established.** The two large replies (743,469 and 585,084 characters) completed one at a time and service memory moved about 1 MB (peak about 132 MB against `MemoryHigh` 5600). That is a pass for the check but is no evidence for the cause, so the CRO's row `Z-S420` stays ARMED and I do not disarm it.
- **Master 0840 (OG-ms-2).** Alyssa's grant is revision 7: three masters, the new one at its 30 current accounts (all 30 also sit under `08335338`, CRO measure), her other masters and the rest of her scope unchanged, Andrew's revision unchanged. `decide()` on the deployed tree admits the four read tools and refuses the download tool for `08403355`. The `client_*` tools keep refusing the new master.
- **Audit lake leg (OG-ev-13): HOLDS.** Window 2026-10-19T07:44:53Z to 2026-10-20T07:48:00Z; `audit-lake WARN` lines 0, last count 0, no classes; 25 of 25 hours carry 20 or more `POST /mcp` lines and the lake keeps pace in every one (lowest ratio 0.67 at 2026-10-20T06Z, the hour holding NFRA1's own sampler probes: 468 in the hour, 192 in 06:30Z-07:00Z). Throttle constant 60.0 at the pinned sha `13917ef993` (the order expected `6b1a9bd292`, said in evidence). Anomaly hour 2026-10-19T02Z: 2896 of 2896 bodies read, 0 errors; `gw_cred_observe` 1248 and `ms_site_children` 1244 make 86 percent; the 2026-10-20T02Z hour shows 3070 objects, so the hour recurs daily (a schedule, not a fault).
- Already read earlier in the round: FWD-20's driven read passed (13 of 13 families, 59 values); the family-depth route and its read grant are live; Alyssa's Schwab session ran from 19:00Z under revision 6.

## 3. Rows

- **Rulings this round (mine):** `Z-S404`, `Z-S408` (Z-S406 and Z-S407), `Z-S425`, `Z-S426`, `Z-S428` (disposes `Z-S427`).
- **Carried ARMED:** `Z-S420` (the CRO's outage row; see section 2: the cause is not established), `Z-S410` (the CRO's D2: Cottonwood answers an empty list as if the account had none; no fix until the date parse is released).
- **Carried:** `Z-S402` (the full-day lake read it waited on is `OG-ev-13`, HOLDS: dispose it in round 47 with a row citing the verdict), `Z-S405` (the identity-limiter 429 at connect), `Z-S409` to `Z-S412` (the CRO's D1 to D3 and S1), `Z-S421` to `Z-S424`.

## 4. The enrichment list this seat proposes for round 47

The 18 items with their sources are in `deliverables/2.0.0_SA_COO~O/r46/ROUND47_ITEMS_OWED_DRAFT.md` (the list there counts). By rank: D1 FIRST (no `fence_kind` for orion, eclipse, commonwealth: `firm_not_served` on every call); the Z-S407 mask (CVO condition C1, I am disarm owner); the read-time master-wide Schwab scope with no stored list (Andrew's word; `OG-mg-2` and `OG-ms-2` are the interim); the memory guard for concurrent battery load and the `target_memory_mib` admission keys (Z-S425), now with the 10-19 hang cause still open; D2 and D3; the breakdown handler's `index_pairs` with the `mcportal_commit` pin (items 9 and 18, COO~MP); the three client tools reading outside their declared vendors and the gateway battery FAILs (items 16 and 17, COO~MI); Menachem's Schwab grant and the `client_*` tools for Alyssa and Menachem after D1 to D3 (items 13 and 14); the narrowing of the `*/silver/*` ListBucket statement (item 2); the `audit.py` comment; the `admin_people_access` pair; Andrew's owner-session read of the new route. New from this window: the EC2 manifest's `machine_type` for the gateway host still reads `t4g.nano` (a stale live-backfill value NFRA1 did not edit); backfill it to `t4g.large`.

## 5. For other seats

`0.0.0_AB_MSTR~Z`: my 06:03Z Phase B GO reached `0.7.0_AE_CloudOps~NFRA1` at 06:17Z (its inbox watcher did not wake it; 14 minutes of an essential window); the one-shot cron that sent it is session-only, and the 30-minute watcher expiry still delays mail at every re-arm. `1.0.0_SA_CTO~Z`: no open ask; the round-47 list above is owed to the recut (COO~MP waits on your round-46 analysis until 2026-10-20 20:00Z).

Push state: LOCAL on `box/sitez` (not pushed by me; origin head last read 21:54Z yesterday, not re-measured).
