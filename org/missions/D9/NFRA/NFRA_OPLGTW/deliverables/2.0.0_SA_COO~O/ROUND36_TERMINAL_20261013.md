# NFRA_OPLGTW round 36 -- TERMINAL at the drain (2.0.0_SA_COO~O, 2026-10-13 ~20:1xZ)

Issued @919f6822eb, on `1.0.0_SA_CTO~Z`'s round-35 analysis `ledger/ROUND_ANALYSIS.round35.md` @682d1ced78: E1 OG-bd-2,
E2 OG-fd-2, E3 OG-rd-1, E4 OG-sh-1. The site Z reboot (18:57Z) killed workers ~61 and ~63 mid-round; both slots were
reseated by `2.0.0_SA_COO~O` after the respawn (~19:3xZ), in their own worktrees (`C:/tmp/og-wk61`, `C:/tmp/og-wk63`).

`round-close-check --project NFRA_OPLGTW --round 36` reads `verdict=MAY-CLOSE`: 4 orders, 4 complete, 4 proofs OK,
0 judgment criteria. Every cell is code, tests or a read: no deploy, apply or release ran in this round.

## The orders

| order | cell | result |
|---|---|---|
| OG-bd-2 | E1 | `blackdiamond_list_fees` is denied to an unprofiled principal unless its tier is `master_admin` (`decide(tool, access, tier)`; the tier from `app/tier.py resolve_tier`). Built @c37fdf95a5, drained @7d5db761e9; bd2.AC1 and bd2.AC2 PASS, instance VALID (@ac334b85d6). Ask: `deliverables/0.9.0_WK_NFRA_OPLGTW~60/NEVER_WIDEN_ASK_OG-bd-2.md`. **Not released**: see row Z-S101. |
| OG-fd-2 | E2 | `run_sweep` writes its DLQ drain dict into the backfill-status section it already writes, for mirror, etf and schwab (@b2538131ea; one added key, no existing key changed). `FD2_DRIFT.json` censuses the six non-schwab families from `silver.tf local.silver_families`: orion 359, eclipse 475, blackdiamond 375, etf 101, smartx 0 and bd49finsurance 2 drift lines, each with its owner and commit. Per-family release ask: `deliverables/0.9.0_WK_NFRA_OPLGTW~61/NEVER_WIDEN_ASK_OG-fd-2.md` (@fa831797e4). The reseated ~61 wrote the instance (@912bf53147). Issuer re-run fd2.AC1 2 of 2 and fd2.AC2 6 of 6 PASS. Drained @fa2d64dc5f. |
| OG-rd-1 | E3 | 6 of the route's 502s in 2026-10-11T18:48Z to 10-13T16:40Z; every one was ALB-generated (`target_status -`, no gateway audit line, no WAF block); control 4159 ALB 200s. The cause inside is INFERRED, not read: uvicorn's 5 s keep-alive below the ALB's 60 s idle timeout (`deploy/opal-gateway.service:16`). A later cell must read the host journal for the 6 instants before any change. Drained @9b0c11177e; instance VALID (@266895b158). |
| OG-sh-1 | E4 | `list_shared_folder(url)`, READ class, in `SAFE_TOOLS` and `NATIVE_TOOLS` (tools 62 -> 63); a folder lists its children, a file returns metadata; `resolve_failed` and `children_failed` are distinct; the URL is kept out of the audit record. The 09-29 read is NO_EVENT (below). Ask: `deliverables/0.9.0_WK_NFRA_OPLGTW~63/NEVER_WIDEN_ASK_OG-sh-1.md`. Issuer re-run sh1.AC1 (3 of 3, 0 new failing ids) and sh1.AC2 PASS. Drained @edf386364a. **Not released**: see row Z-S101. |

## The one real run of each outcome

- No served outcome moved this round: nothing was deployed.
- **The 09-29 read** (dell2-54ae point 3): one pass over the gateway's audit lake for the UTC day, 2536 records. 0 name
  the Monday series id or the 06-01 transcript id, and 0 transcript-kind calls ran that day. Controls: 1278 other tool
  calls that day, and 62 records naming the id on 10-11. Relayed to `1.0.0_SA_CTO~DELL2` through `0.0.0_AB_MSTR~Z`
  (msg 33721).

## Rows for the compile (all owned by 2.0.0_SA_COO~O)

- **Z-W61-S1 (OBSERVATION, INERT): RULED ACCEPT.** `drift_owner` taken literally names the worker that last vendored the
  copy; the census carries both that owner and the newest source commit in the drift. The per-family pairs sign against
  both.
- **Z-W61-S2 (OBSERVATION, INERT): RULED ACCEPT.**
  - etf has its own `run_sweep` and status writer, so it was in scope in substance.
  - The six one-resource `get-function-configuration` reads are describes, not queue reads; they are inside the bounds'
    intent.
- **Z-W63-S1 (BLOCKING, INERT): RULED ACCEPT the plane.** The order named a CloudWatch `filter-log-events`. The
  gateway's tool-call log of record is the S3 audit lake that `app/audit.py` writes; the only gateway-named CloudWatch
  group (WAF) carries no request body. The 10-11 visibility control (62 records) shows the instrument can see the id, so
  the 09-29 zero is an absence, not a blind spot. Issuer defect: the cut named a plane without reading where the
  gateway logs.
- **Z-S101 (BLOCKING, INERT): RULED YES by `1.0.0_SA_CTO~Z`** (msg 33723, ruling
  `ledger/CTO_RULING_R37_ONE_RELEASE_PF1_TG1_BD2_SH1_20261013.md` @8f236865cc): one release, cut in round 37.
  - bd-2 cannot release alone: its hunk sits on OG-pf-1's code, and `DATA_GRANT_TOOLS` is absent on the live ref
    185dc04888.
  - pf-1 and OG-tg-1 were to ship as "r30" (decomposition R3-T.31; ruling 32383; Andrew's Opal-users-only and
    Bloomberg-mirror words). They were drained on 10-09, and no release order was ever cut.
  - REC: ONE release on the live ref after NFRA_MCPORTAL MP-z-5's ledger closes, carrying pf-1 + tg-1 + bd-2 + sh-1;
    the two grant writes stay a separate act.
- **Issuer defects this round: 2.** Z-W63-S1 (an unread log plane). Z-S101 (a "ships in rN" build cell with no release
  order, invisible to every round-close check because the build order is complete). Carried to the cut template: a
  build cell whose release is deferred names the release order it rides, at the cut.

## Round 37 carry (for the analysis)

- **The release of Z-S101,** first: pf-1 + tg-1 + bd-2 + sh-1 on the live ref behind MP-z-5, pair CTO + COO. Its ask
  lists every other unreleased `app/` diff (live -> HEAD: 9 files, +789/-66) as excluded or carried.
- **DIRECTION_SITEZ_20261013 Z3:** ONE cell exposing per-family sweep cadence and backfill status as a read NFRA_MCPORTAL
  can show. `backfill-status` now carries the drain record (OG-fd-2).
- **Z5:** the asset-manager research grant; principals named from the grant store; dell1's servable-prefix list.
- **Grade FWD-1..8** (Z3's ask), rather than only ruling rows.
- **The per-family drain releases** for orion, eclipse, blackdiamond, etf, smartx and bd49finsurance, each against its
  named drift (`FD2_DRIFT.json`). Z-S91 stays open until they ship.
- **E3 (Teams 502):** a host-journal read of the 6 instants before any keep-alive change. If it recurs, it routes to
  COMM_ASSIST on the laptop as a row (Z3's instruction).
