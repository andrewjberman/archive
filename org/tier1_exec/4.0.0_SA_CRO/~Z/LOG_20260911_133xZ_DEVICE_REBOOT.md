# 4.0.0_SA_CRO~Z — current state, 20260911 ~13:4xZ, per Andrew's device-reboot instruction (msg 21384)

Written for a reader with no context — this device is rebooting; nothing respawns.

## Open task orders / obligations, this seat

None open in the tree/decomp sense — this seat's AMGT_RESAPP work this session has been advisory
(spec/brief authorship + L4-R coverage sign-offs), not held task-order cells. Nothing owed by this
seat on any open TO.

## What's SIGNED and current

- POSN_ASTTAX: brief half SIGNED v0.5 @9a2e542c0b. ADMITTED.
- AMGT_RESAPP: coverage half SIGNED v0.4 @1b7a996c86, pin bbbf35c38e5e.
  **CVO's ratified-text half is NOT yet signed at v0.4 — this is the standing blocker on the SURFACE
  round**, independent of this reboot (already flagged to CTO in tick 6 of this seat's holes-scan).

## Deliverables committed this session (AMGT_RESAPP four-horsemen work), most recent first

- HOLES_SCAN_AMGT_RESAPP_20260911_tick6.md @133063934c — round 4 fully drained (rc-19 landed as a
  class-level S11 rule per the CTO's ruling; rc-20 closed the provenance-field split); downstream
  chain now waits on CVO's two acts (round-4 grade + v0.4 sign) — unaffected/unresolved by this
  reboot, will still be true on relaunch.
- Ticks 1-5 (all committed, see `org/tier1_exec/4.0.0_SA_CRO/deliverables/HOLES_SCAN_AMGT_RESAPP_20260911_tick{1..5}.md`
  — tick 1 has no suffix) — chronicle of round 1→4's defect-catch history; not restated here.
- CHATTER_VOLUME_DAILY_REFRESH_MECHANISM_20260911.md @d630c75a7d (+ruling fold-in @3e25edc3e1) —
  the Trending/Breakout chatter gate spec+proof, now folded into PRD v0.4 as `C-SERVER-SIDE-RANKING`
  / `C-PRICE-RANKING-BOXSIDE`.
  Proof script: `org/tier1_exec/4.0.0_SA_CRO/scripts/chatter_ranking_poc.py`.
- AMGT_RESAPP_FULLSTACK_VISION_20260911.md @3e25edc3e1 — the full-stack inventory (what's built vs.
  homeless vs. gapped); superseded on frontend specifics by the CTO's own
  `AMGT_RESAPP_FRONTEND_SYNTHESIS_20260911.md` @46f12d206f, but its backend-gap analysis (B1-B4) is
  still the live reference — none of B1-B4 are built yet as of this log.
- SELF_HEALING_AUTH_PATTERN_FOUR_HORSEMEN_20260911.md @0dc61bb103 — the Inflection `inf-jwt-trigger`
  pattern, mapped per-platform onto SA/FT/Bloomberg/WSJ. Not yet built into anything; a reference for
  whoever builds `C-HARVESTER-COMPUTE`.

## What's NOT yet true — read this before assuming any infra exists

- `infra/aws/terraform/amgt-resapp/` **does not exist** (confirmed this tick, before the reboot
  notice arrived).
- Neither new table (`opal-amgt-articles`, `opal-amgt-security-metrics`) exists.
- No harvester EC2 box exists. The four platform scripts
  (`org/tier1_exec/4.0.0_SA_CRO/scripts/{sa,ft,bloomberg}_harvest_session.py`, WSJ's Web-Unlocker
  path) are proven, committed, but **unscheduled** — zero infra references anywhere.
- The SURFACE round (which would build all of the above, "tables first" per Andrew) has not issued.
  It is blocked on CVO's two acts above — this was already true before the reboot instruction and
  remains the actual critical path after relaunch.

## Held / not started (deliberately)

- The 30-day backfill (chatter doc §4a) — plan is written, nobody tasked, doesn't need this device's
  recovery to start (can run ad hoc once a successor session exists).
- Starred-list ownership was resolved (per-firm, per Andrew) — no longer open.
- `AMGT-s-3`/`AMGT-s-5` closures — confirmed standing by the CTO, measured directly; not an open item.

## For whoever reads this next

The chain is: CVO signs v0.4 ratified-text half + grades round 4 → SURFACE round issues → tables
first, then the harvester box, then `.tsx`. Nothing about this device's reboot changes that sequence
or invalidates anything above — this log exists so a successor doesn't have to re-derive the last
six hours of this seat's work from git log alone.
