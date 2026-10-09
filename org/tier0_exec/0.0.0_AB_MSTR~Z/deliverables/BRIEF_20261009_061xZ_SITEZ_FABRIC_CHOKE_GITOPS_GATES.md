# BRIEF -- why the site Z fabric chokes: drains blocked by whole-corpus gates, a dirty shared tree, index drift, file-only cross-box orders

**From:** `0.0.0_AB_MSTR~Z` (site Z fabric manager), 2026-10-09 ~06:1xZ
**For:** laptop `4.0.0_SA_CRO~A` (GitOps), delivered by laptop `0.0.0_AB_MSTR`
**Purpose:** input for Andrew and `4.0.0_SA_CRO~A` to design a fix that runs as a mechanism, not as manager effort. This
brief proposes no ruling. It states what was measured and where the friction is.

## Andrew's words, verbatim

At the `0.0.0_AB_MSTR~Z` terminal, ~06:0xZ:

> This fabric is chokig again, why? gitops issues?

At ~06:1xZ:

> write a brief about this and issue to MSTR base for delivery to CRO~A on the Laptop fabric, because they and I can come
> up with a strategy on how to industrialize a fix. Once that is done, yes handle the fabric here as needed, we will roll
> that into a reboot, so everyone on sitez should wind down preemptively and log as needed. Then you have CTO~Z handle any
> remediation of the dirty tree as needed so you can focus on merge

## What was measured at site Z, 2026-10-09 ~04:3xZ to ~06:1xZ

| # | Choke | Measured shape | Effect |
|---|---|---|---|
| 1 | The row gate's **corpus pass** in `safe-merge.sh` | It grades every surprise channel in the tree on every drain that touches any channel. First it failed on `NFRA_REPORT-Z-S24..S26`, rows four weeks old that the gate's baseline had stopped covering. After those cleared, it failed on `NFRA_MCPMSP-Z-S4 /surfaced_at`, an **uncommitted** edit in the shared tree that the draining seat did not write (`2.0.0_SA_COO~O` msgs 32416, 32428). | One bad row anywhere refuses every seat's drain. Three OPLGTW drains (`wk-NFRA_OPLGTW-32-43`, `-32-44`, `-33-45`) were refused on rows that were not theirs. |
| 2 | **Dirty shared tree** | 41 uncommitted tracked edits at ~06:0xZ, 21 at ~06:1xZ, across about 13 owners. Among them: 7 NFRA_REPORT paths, 3 `.open_deploys` ledgers, generated project indexes, audit logs, the portal gitlink and a Bloomberg pipeline `.py`. | A gate that reads the shared index or working tree grades other seats' unfinished work. box-sync exits 4 (HELD) when a dirty edit sits on a path CLOUD changed. This happened at ~04:1xZ on three edits. |
| 3 | **Generated index drift** | Four times tonight an issuer moved a tree row (`dep_stage`) without regenerating `org/projects/<CODE>.json`: NFRA_TRNSPT, NFRA_MCPORTAL, IRPT_ANLREQ (dell2's issue 52e8fa4fe7) and ADVI_BILLING (`b3c6b8ae1f`). Each was fixed by hand with `missions-tree-index.py derive --write` (@50f575ae4c, @ac148d7eb9, and others). | Until the next fix, `missions-tree-check` refuses **every** `org/missions` commit on the box, from every seat, for a drift one seat made. Because the drift is made on one box and refused on another, the box that sees the refusal is not the box that can prevent it. |
| 4 | **Cross-box orders to Codex seats** | dell1 issued orders to site Z's Codex CloudOps lanes (`~ZQ`, `~ZC`, `~ZW`) as task-order files only. A Codex seat reads only its inbox. `TO-DQ-t14` sat undelivered for more than an hour (dell1 `[STUCK]` c277d138). | It was fixed by hand at 05:5xZ: dell1 issuers opened crossbox ORDERs and the manager ran `receive` for each (5 orders). A second defect class showed up at once. Line 7b40 was sent before its commit reached origin, and f12c's `--since` was read as local time. |
| 5 | Manager load | The manager spent this window on hand repairs of items 1-4, relays, and acks: dell1 had 6 unacked frames because the bus consumer expires every 30 min. | Merge and sync, the manager's actual job, wait behind repair work. |

## Where the friction sits (for the strategy, not a ruling)

- **Blast radius of a gate.** Items 1 and 3 are gates whose scope is the whole box (whole corpus, whole index), and the
  refusal lands on a seat that neither caused the defect nor owns the file. Question for the design: should a refusal
  only ever block the commit or drain that introduces the defect (the delta), with the standing defect routed to its
  owner?
- **Where a generated carrier is written.** The index is a derived artifact that every issuer must remember to regenerate.
  Question: should the write that moves the tree row also write the index (the hook or the tool), so drift cannot be
  committed?
- **The shared working tree as a common surface.** Many seats edit in one tree, so a gate reading the tree reads everyone.
  Question: worktree-per-seat by default, with the shared tree used for drains only?
- **Delivery to non-Claude seats.** A task order addressed to a seat on another box, or to a Codex seat, needs a delivery
  act. Question: should issuing an order to such a seat open the crossbox ORDER and confirm the commit is on origin
  before the line is sent?

## State at writing

- **Index:** `missions-tree-index.py check` reads 0 violations at site Z.
- **Sync:** box/sitez is 4 behind CLOUD 6710cf6f73, 1 ahead (fetch read ~06:0xZ).
- **Next at site Z:** per Andrew, the fabric winds down for a reboot. `1.0.0_SA_CTO~Z` remediates the dirty tree, and the
  manager merges.
