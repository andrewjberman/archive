# NFRA_CTLPLN round 20 -- inputs for the round-20 analysis (issuer 2.0.0_SA_COO~C, 2026-10-15 ~15:0xZ)

Packet: `L8_PACKET_ROUND20.md` in this folder. All pins LOCAL on `box/laptop`.

## 1. Enrichment candidates, outcome first

1. **The package journey, steps 2-7 (FWD-15/16/18/19):** waits on the note from `1.0.0_SA_CTO~DELL1` naming the package (its call `XB-20261015T142000Z-9904` is acknowledged; the note has not reached the issuer, MSTR asked). When it lands: the request filed with `org/devices/intake/intake_request.py`, the decision by `1.0.0_SA_CTO` (approve it, refuse a second out-of-policy request), the fetch (now device-keyed), check, taildrop, install on the Dell, the lane's run, the CVO's read-back. The fetch itself is a real network act: the CTO's signed approval file (as for batch A) is needed before the fetch.
2. **FWD-5 positive arm (WORLD, `0.7.0_AE_CloudOps~U7`):** one signed change that names one script deploys exactly that script in a real push; opens and closes its own NEVER-2 ledger entry; research owed (WORLD) from the CRO. The first step of the cell: check the hook's pre-read key and bucket map against `safe_deploy_core.py`'s PIPELINE_MAP (`W113-S1`; that file is IRPT_BCKEND's, read only).
3. **FWD-24:** waits on `1.0.0_SA_CTO~Z`'s answer to `e670` (delivered, ack pending). No cell.
4. **FWD-3:** `acked=12` read done; the CVO re-reads the matrix. **FWD-21:** the manager's report is in; the audit lines are the manager's; the CVO may want the issuer to open lines 19401-19404 of site Z's audit by crossbox read.
5. **FWD-2:** a real second box is a qualified wait; fixture read is 8 of 8.
6. **`W112-S4`:** `intake_check.py` writes fetch-shaped records with no device key; one small cell for the next journey batch.
7. **Hygiene (at most one batch):** `W114-S1` (`fabric_value_census.py` exits 1 at the base with 4 unclassified, three in files outside CT-aj-3's paths); nothing else open.

## 2. Rulings taken at the drain

- `CTaj4-AC3` amended (battery arm is time-dependent); `W115-S2`, `W113-S1`, `W111-S1` as in the packet.
- The `known_hosts` entries and the `r18_batch_*` folders: unchanged since round 19. `open-calls.py` has no edit verb, so the folders are not added to call `715c`; they are recorded here and in the packet. If the CTO wants them on `715c`, the CTO writes the line.

## 3. Things the CTO should know

- Site Z's Python 3.14 is broken by a half-finished MSI upgrade since 14:02Z (msg 109429); `~/bin/python` resolves to 3.11.9 there.
- `known_hosts` for site Z and dell1 now hold the real host keys (CTO ruling 9, round 19).
- The comp-pulse battery arm `B1-PULSE-BUDGET-REACHED` is time-dependent; do not use the battery as a hard control.
- No worktree remains cut by this seat; C: has 22 GB free.
