# The one resident release -- never-widen packet: st30 = the whole tree at pin 37210c771a, installed over st27

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11. **Operator:** `0.7.0_AE_CloudOps~YC2` (stood down; respawned on the apply order).
**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Ledger:** `irpt-resident-st30-20261011`, opened at the first host act.
**Rulings:** CTO msgs 4502, 4521, 4597, 4620. **Census:** `../r10/RELEASE_CENSUS_PART1_MECHANICAL_20261011.md` @8e5ae4a62c,
`../r10/RELEASE_CENSUS_PART2_SERVED_OR_INERT_20261011.md` @e9bf588450.

**SEVEN groups change what the resident does. This is not a four-change release.** One build, one pair, one restart.

**RESTATED 2026-10-11 on CTO msgs 4662, 4669, 4682.** The first version of this packet (blob `e6bec0e8cb`, @4387c36e01)
offered four after-reads as drivable by a seat. Three were not: st30's allow list for the Opal producer is Andrew's
sign-in only (`OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com",)`, the same as st27), so a request a seat submits
as `svc-irpt-analysis` takes the YCharts producer, which is vendor-facing. Section 2 now states each after-read as it
truly is. The tar, the pin and the three host scripts are UNCHANGED. Nothing is added to the allow list: PRD line 248,
"The list changes only on Andrew's word", and the CTO has carried that question to him.

## 1. The act

- **Pin:** `37210c771a`, scratch branch `rel-resident-r5`: box/dell2 @f6b74199a9 plus a cherry-pick of the 390 s half
  766a03a0f1. Tests at the pin: `ycharts/generate` 498 passed, 0 failed; `ycharts/research` 250 passed; the 5 release
  tests pass.
- **Build:** the whole tree at the one pin, no base pin and no member override; `--research`, `--opal-map`, 2 `--member`s
  (the classifier client, the logo). 294 members.
- **Gate:** `resident_package_gate.py` PASS against the running st27. G1 294 of 294; G2 292 of 292 (2 generated members
  not compared); G3 117 of 117 compile; G4 0 unserved; G5 added 25, removed 0, changed 61, identical 208.
  Gate note: in its whole-tree mode the gate compares the map member to a repo path that does not exist and fails on it.
  It was run in named-list mode with base pin = pin and an EMPTY list, which applies the recorded map source. The map
  member is byte-equal to st27's (`21a8f6d690bbd28c`).
- **Artifacts** (`C:/dev/irpt-release-st30/`, local only, NOT staged):
  - tar `37210c771a-st30.tar.gz`, sha256 `e5a6b6251b0e5e971cf73d785770965d4c2f407a6b4d79286508b50a853da241` (999,816 B);
  - `resident_host_install_37210c771a-st30.sh`, sha256 `dd85725806894839bd46fc66d990ba195f966862015a2983bb7bbbef0964b969`.
- **Scripts** (this folder, derived from st29's): `pre_read.sh` (P1), `install_st30.sh` (D2 + V1),
  `remove_st30_to_st27.sh` (X1 + V2).

## 2. What changes, by project, and how each is read after the install

| # | change | project | state after the install | what exercises it |
|---|---|---|---|---|
| S1 | reason fix and page sentence | IRPT_YCDGEN | APPLIED, UNEXERCISED | Only the one listed sign-in reaches the Opal producer. It waits on Andrew's word about `svc-irpt-analysis`, carried to him by the CTO, or on his own sitting. Then: the section census on that report, 0 sections stating `INPUT_MISSING:held_<group>` for a no-rule or no-row cause |
| S2 | ticket reference admitted, named on the READY receipt | IRPT_ANLREQ release 4; TCKT_VNEXT's thread | APPLIED, UNEXERCISED until TCKT_VNEXT's fourth run | That run, under TCKT_VNEXT's own pair, on the YCharts producer path. Reaching READY exercises the admission and the receipt (`resident_worker.py` line 434 to `mark_ready`). A run ending ATTENTION exercises the admission only. The criterion on that run: `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/apply1_cells.py . REL4-READ5` expecting `REL4-READ5 PASS`. A refusal is also TCKT_VNEXT's answer: the `ticket_id` schema was not the cause of the dead letters |
| S3 | read-back release 390 s | IRPT_BCKEND | APPLIED, UNEXERCISED | V1 prints the packaged constant. Exercised only if the fourth run's read-back pends |
| S4 | research policy row names 3 firms (digest `6e3286a3d962` to `aebe35b9a054`) | IRPT_YCDGEN round 7 | READ by a seat in the batch window | The status read of the one retained research report (49financial, 2026-10-09T12:00:29Z). It reads (expected), or it stays refused: then the digest on the record was not st29's; a row, no rollback. 0 artifacts exist under the old digest |
| S5 | one WARN journal line per READY, no message | IRPT_ANLREQ AR-g-21 | APPLIED, UNEXERCISED until a READY | The fourth run's READY: the journal shows `ANALYSIS_READY_QUEUE_UNSET` for its request and 0 send failures. A send or a send failure means the variable is set: X1 at once |
| S6 | refusals carry a reason class | IRPT_BCKEND | APPLIED, UNEXERCISED | none short of a failing job; the suites at the pin |
| S7 | optional schema members | IRPT_ANLREQ | APPLIED, UNEXERCISED | the first report persisted after the install validates against v2 |

**So the install itself is followed by ONE seat-driven after-read (S4) and V1.** Everything else is stated as
unexercised until the act named beside it.

Inert until a binding this release does NOT carry: the packager poll and the I3 send (no `commentary_ready_queue_url`, no
`analysis_ready_queue_url`; V1 prints both counts), service subjects, custody reports. No commentary queue binding. I3 is
not before the attach release.

## 3. Blast radius

Host `i-0167fd745ad906a66`: one new root `/opt/irpt-resident/37210c771a-st30`, the ExecStart, the receipt, ONE restart.
The capture library and its wrapper are byte-equal to st27's (`857d90b81960d69a`, `55ddb8f7947cba7c`), so the installer's
library step rewrites the same bytes. No IAM, data, Lambda, queue or portal change. The svc profile is not touched.

Writers counted. "Which firms a research write may retain": 1, the packaged registry row. "Whether I3 sends": 2 -- the
bindings (`analysis_ready_queue_url`, absent) and the unit's own environment, which this release does not write. The
second is why P1 is a STOP.

## 4. Order, STOP and rollback

1. **U2 stage** the tar and the install script; read both sha256 back from the staged copies.
2. **P1 pre-read** (read only). **STOP:** `P1 STOP-READ PASS` is required: the unit Environment, the running process and
   the unit files all show 0 for `IRPT_ANALYSIS_READY_QUEUE_URL`. On FAIL nothing is installed.
3. **D2 + V1 install.** The installer refuses unless `irpt-generation` reads 0/0, and rolls back itself on a failed start.
4. **After-read S4** in ONE served-read window, with the three reads already listed for it (one dead letter read with
   no delete; TCKT_VNEXT run 3's request id and state; the status re-read of REQ-5e4149d2). No generation is submitted
   by this seat in that window or any other.
5. **Rollback (X1 + V2):** `remove_st30_to_st27.sh` restores the st27 receipt and root. The st27 root stays on the host.
   Rollback package: `e606008994-st27.tar.gz`, sha256
   `20916261074c356ab31497b338a6957e3d72cb252b8a3f54432db98610da39e4`.

Rollback is run on: a failed V1, any I3 send or send failure, or a resident that stops polling. A failed read of S4, or
of S2 on TCKT_VNEXT's run, is a finding and a row, not a rollback, unless the CTO rules otherwise on the read.

No dead letter is redriven. Nothing goes to Bloomberg. One CVO packet per project follows the install.

## 5. Not established

Nothing here was exercised on the host. The st27 comparison is against the running root's BUILD INPUT, not a listing of
the host's bytes; P1 prints the running root and its worker hash. The digest on the retained record is unread (S4). The
three host scripts pass `bash -n` and have not run.

## COO HALF

**COO half SIGNED on the RESTATED packet** -- `2.0.0_SA_COO~G2`, at pin `37210c771a` and the unchanged tar, on the gate
result, the census parts 1 and 2, the seven changes with their after-install states as section 2 now states them, and
P1 as a STOP. My signature on the first version is withdrawn with that version.

## CTO HALF

(owed on this blob; the half @42972d0ea5 was signed against blob `e6bec0e8cb` and the CTO ruled it does not cover an
install, msg 4662)
