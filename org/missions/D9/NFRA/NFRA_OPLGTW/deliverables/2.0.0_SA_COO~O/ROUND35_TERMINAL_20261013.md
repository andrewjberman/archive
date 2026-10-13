# NFRA_OPLGTW round 35 -- TERMINAL at the drain (2.0.0_SA_COO~O, 2026-10-13 ~13:3xZ)

Issued @91bde9b54c, on `1.0.0_SA_CTO~Z`'s round-34 analysis `ledger/ROUND_ANALYSIS.round34.md` @026a983b34:
- E1 OG-fd-1, E2 OG-ap-10 and E3 OG-tb-1.
- E4, the OG-bd-1 re-cut, was NOT cut: it is held on Andrew's BD admission answer (row Z-W57-S2).

Apply workstreams:
- APPLY-R35 OG-ap-11 @10448c5323;
- APPLY-R35-G OG-ap-12 @48ec516a04;
- APPLY-R35-T OG-ap-13 @e473fef6eb.

`round-close-check --project NFRA_OPLGTW --round 35` reads `verdict=MAY-CLOSE`, with 0 judgment criteria. Of 6 orders, 5
are complete and 1 is failed (OG-ap-11, rolled back; OG-ap-12 carries its fix).

## The orders

| order | cell | result |
|---|---|---|
| OG-fd-1 | E1 | Per-family DLQ drain in source and tests, for all six families: own messages are deleted and reported; foreign messages are returned (visibility 0); unattributed messages are never deleted. The ask was signed for schwab only (COO @824ec17c4d, CTO @aafc1640e8): packaged copies are build snapshots, and etf, blackdiamond, orion and eclipse each need a pair naming their drift's owner. Instance VALID; fd1.AC1 and fd1.AC2 issuer re-run PASS. |
| OG-ap-10 | E2 | The `.pptx` -> market_update gateway release is LIVE: release d9f2ebded9, B2 @d8f0b20b8a, ledger CLOSED 11:58:46Z; ap10.AC1 and ap10.AC2 issuer re-run PASS. NFRA_MCPORTAL MP-n-1 then re-cut on it; the live ref is now 185dc04888 over d9f2ebded9. |
| OG-tb-1 | E3 | 90-day census of `gateway/teams/bearer` readers: 186 events, 4 principals, and the dell group's verdict is NONE. Narrowing ask signed (COO @f9cb4c5dca, CTO @fa2892a777) and un-held by the laptop CTO's YES (sitez-ffaf). tb1.AC1 issuer re-run PASS. |
| OG-ap-11 | E1 apply (schwab) | **FAILED, rolled back.** The real 12:15Z sweep raised AccessDenied on `sqs:ChangeMessageVisibility`, because the preflight's comp-iam NOT-APPLICABLE was the issuer's defect (Z-S97). Rolled back 13:14:03Z under A2. |
| OG-ap-12 | Z-S97 fix | One action added to `opal-assets-silver-dlq-access` in place (v1 -> v2, 7 attachments kept); schwab is back on the OG-ap-11 build. Ledger CLOSED 23:44:23Z; ap12.AC1 issuer re-run PASS. AC2 on the real 2026-10-13 12:15Z sweep: one invocation, no retries; the eclipse synthetic survived; depth 2 -> 1. ap12.AC2 (A2, read from the queue) issuer re-run PASS. |
| OG-ap-13 | E3 apply | The dell group's read of the teams bearer is removed at the census source (@5e58a617e7, audited lane override under A1) and live: policy v5, `ReadPlatformKeys` 31 -> 30, dell1 simulate implicitDeny on the bearer and allowed on a kept ARN. Ledger CLOSED 00:58:47Z; ap13.AC1 and ap13.AC2 issuer re-run PASS. Receipt @c7d4d1f4f1, relayed to the laptop seats via 1.0.0_SA_CTO~Z. |

## The one real run of each served outcome

- **Gateway:** the `.pptx` market_update pair is served on the live gateway (`W~Z/AP10_SERVED.json`, 5 of 5);
  ap10.AC2 PASS.
- **schwab per-family drain:** the real scheduled sweep RequestId 37fe3466 ran clean; the foreign record survived and
  the own record drained (`W~Z/AP12_GRADE.json`).
- **Teams-bearer narrowing:** a live simulate as the dell1 user reads implicitDeny, with the kept-ARN control allowed.

## Rows for the compile (all owned by 2.0.0_SA_COO~O)

- **Z-S97 (BLOCKING):** OG-ap-11's drain could not complete without `sqs:ChangeMessageVisibility`. REMEDIATED by
  OG-ap-12: the grant is live and the drain ran clean on the real sweep.
- **Z-S98 (BLOCKING):** OG-ap-12 step 2's description edit forces replacement, which contradicts its own plan bar.
  RULED by A1 @d78be8e6c2: the edit is struck, and the applier kept the bytes. This is an issuer defect.
- **Z-S99 (BLOCKING):** the owned-paths lane `NFRA_CTLPLN_FAST_C` refused the applier on the census source. RULED by
  OG-ap-13 A1 @fed356e1cb: one audited override commit, under COO condition A(a) and the laptop CTO's consent.
- **Z-S100 (BLOCKING):** OG-ap-12 AC2's REPORT clause had no referent, since a scheduled sweep's drain report is a
  discarded return value. RULED by A2 @d86203d41d: AC2 reads the queue. This is an issuer defect. The persistence of the
  report is carried to round 36.
- **Z-S95 / Z-S96 (OBSERVATION):**
  - Z-S95: `/hx/teams/channels/.../messages` returned 502 on 2 of 285, not yet read;
  - Z-S96: OG-ap-10 step 2 named a release-tree test that cannot run there.
- **Z-W57-S2 (ARMED):** the BD admission call, held on Andrew.
- **Issuer defects this round: 4** (Z-S97 comp-iam, Z-S98 a ForceNew field, Z-S99 the write surface across lanes, Z-S100
  a report with no referent). One class, carried to the cut template: an APPLY order's preflight RUNS comp-iam on every
  API call the new code makes; its plan bar is checked against the provider's ForceNew fields; its `<paths>` are checked
  against the lane owner of every file; and every criterion names an artifact that exists for the real trigger.

## Round 36 carry (for the analysis)

- **First enrichment item (CTO msg 33619):** the gateway `list_shared_folder(url)` tool, Graph
  `/shares/u!<b64>/driveItem/children`. It folds row NFRA_TRNSPT-D2-S29 and unblocks NFRA_TRNSPT FWD-2's
  research_meeting. dell2's read: the MASTER token already holds Files.ReadWrite.All (`app/config.py:64`), and
  `read_teams_attachment`'s resolver (`tools.py:1206`) 404s on folder links.
- **Persist the sweep's DLQ report** for every family (Z-S100): `run_sweep` writes its dlq dict into backfill-status.
- **The per-family drain for etf, blackdiamond, orion and eclipse:** each needs a pair naming its drift's owner (Z-S91
  stays open until then). This is now OBSERVED, not predicted: the eclipse synthetic that survived schwab's sweep was
  deleted by the blackdiamond sweep at 12:45:52Z (old drain-all code). It was found by bracketing, since eclipse never
  ran (0 lines; 0.7.0_AE_CloudOps~Z msg 33628).
- **OG-bd-1's re-cut** on Andrew's answer (Z-W57-S2).
- **Z-S95 (502s) read; reinstall the SI2 puller.**
- **Parked on NFRA_CTLPLN (laptop):** `cloudops-dell-agent-platform-secrets-policy` is at 5 of 5 versions, so a prune
  is due before that root's next apply.
