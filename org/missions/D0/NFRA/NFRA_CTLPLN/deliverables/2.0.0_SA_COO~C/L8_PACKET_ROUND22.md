# NFRA_CTLPLN round 22 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~21:0xZ)

Round 22 is terminal: three orders `complete`, one `withdrawn` (issuance `54e8947a06`; amendments `b9d7c9bd21` and `bbcec1c613`; decomposition `NFRA_CTLPLN_DECOMP.round22.md`; merges `3c3d04d4ec`, `0b35c0c854`, `8d757213ea`; flips `73bc62901f`, `c4cddddd88`, `b8b740bbcf`; withdrawal `1b7f7da1b7`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 22` reads `verdict=MAY-CLOSE`, `orders=27 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL unless stated. Inputs for the analysis: `ROUND22_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge | issuer re-run (main tree, after the merge) |
|---|---|---|---|
| `CT-al-1` | 15, 16, 18, 19 | `3c3d04d4ec` | `JOURNEY-FETCH wheels=1 file=duckdb-1.5.0-cp314-cp314-win_amd64.whl device=laptop sha256=11ae50aaeda2 requests=4 ok=True where=release`; `JOURNEY-CHECK checks_run=7 failed=0 check8=SIGNED released=True ok=True`; `JOURNEY-TAG recorded=cp314-cp314-win_amd64 wheel=cp314-cp314-win_amd64 ok=True` |
| `CT-al-4` | 15, 16, 18, 19 | `8d757213ea` | `JOURNEY-RELEASE released=1 check8=SIGNED ... ok=True`; `JOURNEY-PACK files=4 manifest_ok=True verify=INTAKE-VERIFY ... wheels=1 verified=1 checked=1 stray=0 ok=True`; `JOURNEY-TAILDROP files_sent=4 failed=0 target=dell1 ok=True` (record read only) |
| `CT-al-3` | hygiene | `0b35c0c854` | `HYGIENE-MAPAGE inside_time=True mtime_ignored=True rebuild_once=True ok=True`; `HYGIENE-SPARSE builds=0 reads_main_or_blind=True ok=True`; `FWD5-POSITIVE versions=2 etag_equals_repo_md5=True other_changed=0 audit_actor=0.0.0_AB_MSTR ok=True`; `COMP-PULSE BATTERY: 12/12 PASS` |
| `CT-al-2` | 3 | WITHDRAWN | the CTO withdrew its ruling (ROUND_ANALYSIS.round21.md ADDENDUM 1 @d9c20f887e): the managers CARRY a call, the named seat READS and acknowledges it, which `crossbox-call.py` already enforces; worker `~120` stopped, branch `wk-NFRA_CTLPLN-120` not merged |

Every proof instance reads VALID on the committed state. Issuer rulings made during the round, each in its own commit: `CT-al-2` first amended (the manager rule replaces the named-seat rule, two suites granted, `b9d7c9bd21`) and then withdrawn when the CTO withdrew the ruling; `CT-al-4` cut as an amendment (`bbcec1c613`) the tick the CTO signed check 8; the journey tests `--fetch` and `--check` of `CT-al-1` made state-aware (rows `W122-S4`, `W122-S5`) so that `CTal1-AC1` and `CTal1-AC2` still reproduce after the release (the moved wheel).

## 3. What each outcome now stands at (evidence, not a grade)

- **The package journey (FWD-15, 16, 18, 19):** the request `REQ-20261015T171032Z-duckdb` (duckdb==1.5.0, lane `2.0.0_SA_COO~D1`, MDPF_CANON, dell1) is APPROVED by the CTO with the CRO's co-decision; its no-lane sibling `REQ-20261015T163055Z-polars` is REFUSED. ONE wheel (the cp314 one, dell1's CTO's interpreter choice) was fetched through the checked route (4 requests to the index), checks 1-7 passed, the CTO signed check 8 accepting four named limits (check 3 compares to the laptop's installed copy, the compiled `.pyd` is named not compared, check 7 does not show the scanner inspected the file, no check rules out a taken-over maker account), the wheel was released, packed (4 files, local verify 1 of 1) and sent to dell1 by Taildrop at 2026-10-15T20:24:27Z to 20:24:28Z (exit 0 on each). **Delivery is not proven**: a Taildrop has no read receipt. The call `XB-20261015T204024Z-7bc4` to `1.0.0_SA_CTO~DELL1` (sent 20:42:23Z, not yet acknowledged) asks for `tailscale file get`, the SHA-256s, `verify`, `prove`, `install --target` and the lane's one read.
- **FWD-3:** the issuer read `org/devices/crossbox/` at ~20:3xZ: the newest file of each of the 12 directed pairs is ACKED, was carried (`sent.bus_message_id` present) and was acknowledged by the very serial its `to_serial` names, 12 of 12. That is the CTO's corrected reading, not the withdrawn manager-only one.
- **FWD-24:** both leads answered the same question (an IAM write on a production Lambda role): the laptop CTO OWED (msg 109405, `org/tier0/STAKES_MATRIX.md:79`); the site Z CTO OWED (carried by `0.0.0_AB_MSTR`, `org/tier1_exec/1.0.0_SA_CTO/deliverables/XB_e670_FWD24_RESEARCH_OWED_ANSWER_SITEZ_20261015.md` @284cba9fbf on `origin/box/sitez`, `research-owed.py --stakes S3` printing OWED, run on site Z under Python 3.11.9). The answers agree.
- **FWD-11:** dell1's manager (call `3a78`, acknowledged 19:59:43Z): 16 open ledger entries after the 15:46:25Z restart; 4 opened after it (ORDINARY); 11 opened before it with a last log at least 2.5 h earlier (ORDINARY by log); ONE candidate for INTERRUPTED, not confirmed: `irpt-holdings-per-firm-mint-ib549-20261015` (CloudOps~IB2, opened 15:18:14Z, 5 legs, L1 closed 15:22:01Z, 4 legs not closed; owner not live on the broker; class and loss NOT measured). All seats were re-seated by new processes (autolaunch 15:47:44Z); `2.0.0_SA_COO~D1` closed its session at 15:45Z. Interrupted entries: none confirmed.
- **FWD-14:** MacBook (`rc`) connections on the four boxes' own logs are as in the round-21 packet. The Windows-laptop arm is NOT on record: the laptop's outbound remote-desktop client log shows attempts to dell1 (2026-10-13 13:17Z, 13:18Z) and dell2 (2026-10-10 13:55Z, 2026-10-13 13:18Z), none to site Z, and no target's event 1149 list holds a connection from the laptop's address `100.96.167.100`. That arm needs a real session from the laptop (with the MacBook session tonight, `c9a4`).
- **Hygiene:** the danger map carries `built_utc`, the reflex refreshes it itself when old (one rebuild, 120 s limit, no scheduled task) and never builds in a sparse worktree; `comp-pulse diff` on a real file reads `REFLEX CLEAN` against 2703 danger nodes in 0.9 s; the FWD-5 read test reproduces `other_changed=0` after the ledger entry closed.

## 4. FWD state

`FWD-5` REALIZED (round 21); `FWD-9` PARKED; calls `c9a4` (FWD-14, tonight) and `318f` (FWD-17, when the duckdb record exists) open for Andrew; `7841` CLOSED.

## 5. Rows this round minted and the rulings on them

`W119-S1`; `W120-S1`, `S2` (restated and dismissed as moot in the issuer's `S9133`: a seat cannot carry a worker coordinate); `W121-S1`..`S6`; `W122-S1`..`S5`; the issuer's `S9133`. Rulings: `W119-S1` (the tool records check 8 as failed, not awaiting, when the signature file does not exist; the test maps it, and the CVO should know); `W121-S1` (a sparse worktree reads its own checked-out map, which is the committed map at that commit; accepted), `S2` closed by the merge, `S3`/`S4` (the same corpus builds to 2692, 2703 and 3491 edges by tree; the build guard has no portal check) carried to `1.0.0_SA_CTO` as the map's owner; `W122-S1` (the release needed the checks re-run with the CTO's signed file, decided by the tool); `W122-S2` (the release folder holds the tool-written `.delivery.txt` beside the wheel, so "exactly one file" means one wheel); `W122-S4`, `S5` resolved by the state-aware tests.

### The 33 owned remediation rows unmoved for 2 or more rounds (CTO ruling 9), by owner

The issuer's parse of `surface-channel/remediations/REMEDIATION_v1..v11.md` finds 36 rows still open (the CTO counts 33 by its own cut):

| owner | open rows |
|---|---|
| `2.0.0_SA_COO~C` (15) | W12-S1, Z-S3, W8-S7, S9101, S9103, S9105, D1-S8, D1-S10, W61-S1, S9121, W84-S1, W79-S2, S9120, W89-S3, W111-S1 |
| `1.0.0_SA_CTO` (10) | W31-S6, W39-S1, W14-S32, D2-S1, S27, W65-S2, W79-S1, W106-S5, W117-S2, W117-S3 |
| `2.0.0_SA_COO~R` (7) | W31-S3, W32-S5, W31-S4, W31-S5, W31-S12, S33, S34 |
| `0.0.0_AB_MSTR` (2) | S9119, S9128 |
| `2.0.0_SA_COO~T2` (1) / `1.0.0_SA_CTO~Z` (1) | W36-S2 / Z-S8 |

**The issuer's dispositions of its own 15 (stated here, as the CTO asks):**
- **RESOLVED:** `D1-S8` (the pinned-entry deploy ran for real: PINNED-DEPLOY 18:01:57Z), `W111-S1` (fetch records carry the device: `JOURNEY-FETCH ... device=laptop`), `W84-S1` (`.tools/spawn-agent.ps1:108` now reads `[A-Za-z0-9_]+` in the third segment, read at HEAD 2026-10-15), `W61-S1` (Andrew's elevated line is on record: the 2026-10-13T14:47Z receipt `org/devices/state/laptop/ssh_enable_20261013T144716146Z.json` shows the tailnet-only firewall rule `100.64.0.0/10` and `password_auth: no`).
- **DISMISSED as INERT, reason stated:** `S9105` (slot `~K9` no longer exists; every worker has been a numeric slot with an order issued to it for twelve rounds), `S9101` (AMENDMENT 9's step 4 is amended to the five roots that init, `seeking-alpha` named as a configuration defect of the root's module arguments; the root's owner fixes it at its next apply), `W79-S2` (`test_crossbox_call.py` reads 64 of 65 at the round-22 base; the one failing case is sparse-checkout-only, per worker `~120`'s measurement).
- **CARRIED with a named outcome and owner:** `S9121` (the merge verb dropping a null bus id; owner the issuer; the next hygiene batch reads it with `test_round13_batch.py`), `W8-S7` (the fence census writing its own baseline; owner the issuer; the next hygiene batch), `D1-S10` (the install verb's target option; closed by call `7bc4`'s `install --target` on dell1), `S9103` (the kit's install replacing a Dell mirror; owner the issuer; cut with the next Terraform pack sent to a Dell, none is due), `S9120` (six dell2 seat endings; owner `0.0.0_AB_MSTR~DELL2` reads, the CVO grades), `W89-S3` (ADVI_FIRMBKTS's, per the CTO), `W12-S1` and `Z-S3` (each function's next deploy; `Z-S3` before 2027-12-01).
- The other owners' rows are the owners' to disposition; the list above is the packet's record.

## 6. Not measured here

The arrival and install of the wheel on dell1 and the lane's read (call `7bc4`); whether `irpt-holdings-per-firm-mint-ib549` was interrupted by the restart and whether anything was lost; the Windows-laptop remote-desktop arm and the off-tailnet refusal of FWD-14; the CVO's own re-grade of the FWD table.
