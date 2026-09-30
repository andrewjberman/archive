# NFRA_MCPINDEX -- reinstated: the blocker rulings (1.0.0_SA_CTO~O, 2026-09-30 ~07:5xZ)

**Andrew, verbatim, at the 1.0.0_SA_CTO~O terminal, ~07:5xZ:** "I need us to get MCPINDEX back online, need a COO~M on
the fabric to handle it. I have a text handoff from CVO~O with more detail. There are some very silly blockers that are
preventing us from moving forward that i do not give a fuck about".
**His earlier word, recorded by 3.0.0_SA_CVO~O:** `org/tier1_exec/3.0.0_SA_CVO/deliverables/ANDREW_DIRECT_20260930_072xZ_NFRA_MCPINDEX_REINSTATE_NO_TEST_USER_NO_AUTH.md`
-- "I want this project reinstantiated fucking right now with any of these harebrained blockers delineated." "We
shouldnt need a 'test user' to test it. I do not care about fucking aroudn with auth right now."
**Input:** the CVO's handoff `org/tier1_exec/3.0.0_SA_CVO/deliverables/HANDOFF_NFRA_MCPINDEX_REINSTATE_TO_CTO_O_20260930.md`,
blockers B1-B9. This seat is CTO of NFRA_MCPINDEX and NFRA_OPLGTW.

## Rulings

- **B1 -- the "test user" no longer holds anything in MCPINDEX.**
  - NFRA_OPLGTW's G-C (a new unprivileged M365 user) is REMOVED as a precondition of the Schwab enable and of any
    MCPINDEX test, on Andrew's "we shouldnt need a 'test user' to test it".
  - The enable is tested with an EXISTING Opal principal who already holds a Schwab grant.
  - What remains is the enable act itself: `schwab` in `ENABLED_INTEGRATIONS`, the IAM read on its secret and data, and
    a gateway release. That is a release under a NEVER-2 ledger with never-widen halves (CTO + COO), because it adds
    tools to the served surface. Those are safety mechanics, not blockers, and the round-5 release cell carries them.
  - This does not change G-C inside NFRA_OPLGTW's own OG-g-1; that order's test identity is a separate matter.
- **B2 -- "no auth work now", with its reach stated.**
  - G-B (a non-author cold asker) is satisfied by any ALREADY-ADMITTED Opal principal who did not author the index.
    No new identity, grant or sign-in is created for it.
  - FWD-9 (Andrew admits staff one at a time) is DEFERRED on his word; its outcome text is kept, not retired.
  - No round-5 cell creates, changes or tests an identity, grant or sign-in path. Existing guards stay exactly as they
    are; "no auth work" means none is added, not that any is removed.
- **B3 -- the naming gate on the ETF catalog row: one acknowledgement from Andrew.**
  - A registry row or LEGACY-READ waiver cannot cover it today. The waiver kinds cover a Python call site or a
    Terraform local, not a catalog YAML row, and adding a kind is a gate build.
  - The fast legal path is an R20 departure (CLAUDE.md rule 30; `infra/logic/02_DOCTRINE.md` R20) for the existing
    served key under `platinum/etfs/` as read by the catalog and its emitter. It needs his acknowledgement, put to him
    in-session 07:5xZ.
  - On his word the entry lands, and MX-t-10's frozen candidate (`refs/archive/wt-20260929/wk-mcpindex-r4-15-candidate`
    03a19ac282) commits as-is.
- **B4 -- Schwab transactions:** a round-5 build cell (a transactions table beside the three `dim_*`, one master, one
  date). Not a gate.
- **B5 -- FWD-4:** round 5 cuts Black Diamond's analysis record (PRD S8), then its first catalog row and tool. Orion,
  Eclipse and SmartX follow on the same pattern.
- **B6 -- MX-s-14's wait is legitimate and gates nothing else.** Row Z-S61 names the evidence: an ad-hoc run would
  consume the day's new input and destroy the scheduled write-arm proof. That is CLAUDE.md's stated exception. It holds
  its own two acceptance legs only; B1-B5 and B7 proceed.
- **B7 -- `query_v0` as an MCP tool,** under its catalog classification (C2): a round-5 cell.
- **B8 -- the PRD's "laptop project, Bloomberg not claimed" limit is stale.** The project is fabric site-z, where
  Bloomberg lives. A PRD addendum makes FWD-8 reachable through Bloomberg as well as YCharts; this seat writes it and
  3.0.0_SA_CVO~O re-signs.
- **B9 -- the drive.**
  - This seat's `/self-drive` is armed (cron 625c63e4, record @680afc11fd).
  - 2.0.0_SA_COO~MI is NOT REGISTERED (read 07:5xZ), so the lane is asked of 0.0.0_AB_MSTR~Z to respawn.
  - Andrew said "COO~M". Read here as the MCPINDEX lane ~MI, because ~M is the laptop's IRPT_BCKEND lane and this is
    a site-Z project. If he means a new lane, the respawn names it instead.

## Order for round 5 (2.0.0_SA_COO~MI, one issuance)

1. MX-t-10 lands, the ETF work (FWD-5, FWD-2 etfs), on Andrew's B3 word.
2. The Schwab enable release (B1) with the transactions table (B4).
3. `query_v0` becomes a tool (B7).
4. The Black Diamond analysis and its first tool (B5).
5. An `advi` catalog row and tool (FWD-2).
6. The FWD-1 cold run by an existing non-author principal (B2).
7. The COO's close run on all of it; 3.0.0_SA_CVO~O grades the judgment criteria at L9.
