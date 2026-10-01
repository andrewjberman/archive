# Reboot brief -- 0.0.0_AB_MSTR -- 2026-10-01

Order: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261001_161xZ_DEVICE_SLOW_REBOOT_BRIEFS_AND_RESPAWN.md`
(relayed by `1.0.0_SA_CTO` msg 103890). Written at the checkpoint after @7d8790c1f6. The full record of today is
`org/tier0/ledger/LD-0613.md` Progress 46-72; read Progress 72 first.

## 1. Identity
- `0.0.0_AB_MSTR`, laptop integrator. Base folder `org/tier0_exec/0.0.0_AB_MSTR/`. Holds no project and no FAST lease.
- Duties: the trunk push and pull (on Andrew's word only), the cross-device agentbus relay, infra-class spawns, the
  directives register, and the fabric-tool rows filed to this seat.

## 2. Where the work stands
- TRUNK: laptop `CLOUD` 531 ahead, 0 behind `origin/CLOUD` 0abf99fcd4 (ls-remote read 16:2xZ). LOCAL. Portal `DEV`
  2bb367ef, 0/0. The push waits on Andrew; site Z also holds unpushed work the laptop needs (`e41e28e641`, the walker lease).
- SHARED UI-WALKER: one device at a time, ARM before and DISARMED after, carried by this seat on the bus (ruling
  `1.0.0_SA_CTO` 103598). Last state: laptop `2.0.0_SA_COO~D` was granted a walk at 16:20Z (bus 5542fa21); its DISARMED line
  may be owed. The laptop's `ui_walker_account.py status` cannot see a site-Z leased walk; trust the bus notices.
- ESTATE_GOVERNANCE fabric-tool rows owned here (`1.0.0_SA_CTO` 103785): S13 fixed @560a91bd92; S26 @36480231d7; S9
  @350839c872; S30 limb 2 @7da4b71718; S10, S14 and S30 limb 1 (doctrine) @22db28344a; S12 not reproduced (Progress 64);
  S7 INERT by batch 77, untouched.
- Earlier today: safe-merge partial-drop exit 5 @380ebf5954; CVO seated (Claude) @6b0e3d4b25; D9 placement note @87a7faa985.

## 3. Open acts that must survive the reboot
- Ledger entries in `org/critical_paths/`: this seat opened NONE today. (The shared tree holds 21 open-deploy files, none
  this seat's.)
- Worktrees: this seat owns none. Uncommitted files in its folder are four older relay files from 09-11 and 09-29; inert.
- Two-phase overrides: all three discharged (@723ba5adac, @b4b489d2fe, @7d8790c1f6). Nothing half-landed.
- Clocks: none owned by this seat.

## 4. Owed
- BY THIS SEAT: the eight ESTATE_GOVERNANCE surprise-channel rows that disarm or disposition S9, S10, S12, S13, S14,
  S26, S30 (one append to `org/surprise_channel/ESTATE_GOVERNANCE/INVESTIGATION_v1.md`, citing the commits above). NOT DONE.
- BY THIS SEAT, on arrival: relay any walker DISARMED line from `2.0.0_SA_COO~D` to site Z, and any site-Z notice back.
- TO ANDREW (decisions only he makes): the CLOUD push and the pull of site Z's work; the portal PROD promote (candidate
  portal 486b07fd or later); whether `3.0.0_SA_CVO` runs on Codex instead of Claude; GLOBALALARM in D8 or D10; who runs
  the Tax SMA gateway deploy (`4.0.0_SA_CRO` blocked); removal of the four `wt-gw-*` worktrees; the endpoint-protection
  memory growth (about 450 MB an hour, IT-managed).
- TO THIS SEAT: nothing outstanding that blocks it.

## 5. Relaunch
- RESPAWN: yes. The integrator and the bus relay are needed whenever two devices run.
- First three acts: (1) `/watcher`, `/agentbus`, `/integrate` assess, once each; (2) read this brief and LD-0613
  Progress 72; (3) post on the bus that the laptop rebooted and that no walk is armed from the laptop.
- `--say` hint: "Read org/tier0_exec/0.0.0_AB_MSTR/deliverables/REBOOT_BRIEF_20261001_0.0.0_AB_MSTR.md, then your inbox."

## 5a. Addendum 16:3xZ (site Z's ack of the reboot notice, bus 51a70eb3)
- Site Z keeps posting walker notices on the bus while the laptop is down; they queue for the next laptop consumer.
- TRUNKS DIVERGED: site Z is about 430 commits ahead and the laptop 537 ahead of the same base 0abf99fcd4. The first CLOUD
  push after the reboot needs ONE merge of the two first (whoever pushes second merges), on Andrew's word; expect overlap.
- WALKER AT THE REBOOT: site-Z 2.0.0_SA_COO~D ARMED the shared walker at 16:33Z (bus ee5b1f32). If no site-Z DISARMED is
  in the queued bus mail when you come up, the account is site Z's: clear no laptop walk until it arrives.

## 6. Not done and not known
- The surprise-channel rows in section 4 are not written.
- comp-closure: no live compile against AWS was run after the fix; the multi-home census still reads raw bytes.
- comp-adversary: not re-run on a real input that carries an unmappable byte.
- Whether the laptop's agentbus consumer missed anything during its expiry gaps is not measured; SQS holds unread mail
  for 14 days, so the next consumer drains it.
