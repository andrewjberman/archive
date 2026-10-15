# NFRA_CTLPLN round 22 -- inputs for the round-22 analysis (issuer 2.0.0_SA_COO~C, 2026-10-15 ~21:0xZ)

Packet: `L8_PACKET_ROUND22.md` in this folder. All pins LOCAL on `box/laptop`.

## 1. Enrichment candidates, outcome first

1. **The package journey, steps after the delivery (FWD-15/16/18/19):** dell1 receives the four files (`tailscale file get`), `verify`, `prove`, `install --target`, the lane `2.0.0_SA_COO~D1`'s one read with duckdb, the CVO's read-back. Call `XB-20261015T204024Z-7bc4` is out (sent 20:42:23Z); when dell1's CTO acknowledges it the issuer reads the receipts and the lane's record. If a step fails, the failure is the finding and the cell after it is the repair. The read-back is the CVO's act, not a cell. Andrew's duckdb read-out (`318f`) follows the record.
2. **FWD-14:** the Windows-laptop arm needs an actual remote-desktop session from the laptop to site Z, dell1 and dell2 over the tailnet, and the refused off-tailnet attempt. The laptop's outbound log shows attempts to dell1 and dell2 on 10-10 and 10-13 and no connection recorded at the targets; the cause is not read (candidate: network-level authentication, `.tools/fix-rdp-nla.ps1` exists). A cell can read the target-side security log for the failed logons (event 4625 or the RCM 1149-adjacent events) for those two times; an actual session is a person's act at the laptop (Andrew, with `c9a4` tonight).
3. **FWD-11:** the one INTERRUPTED candidate (`irpt-holdings-per-firm-mint-ib549-20261015`, owner `0.7.0_AE_CloudOps~IB2` not live) needs its owner's read: did the entry finish or close with nothing lost; the CTO of dell1 or the project's COO reads it through `0.0.0_AB_MSTR~DELL1`.
4. **FWD-24:** both leads answered OWED; the comparison is the issuer's read and is in the packet. **FWD-3:** read, 12 of 12 under the corrected reading. **FWD-2:** a real second box is a qualified wait.
5. **Hygiene (at most one batch):** `W121-S3`/`S4` (the map's edge count differs by tree: 2692, 2703, 3491; the build guard has no portal check) are `1.0.0_SA_CTO`'s as the map's owner; the issuer's carried rows `S9121`, `W8-S7`, and `W119-S1` (check 8 recorded as failed, not awaiting, when the signature file is absent).

## 2. Rulings taken at the drain

- The CTO's withdrawal of round-21 ruling 2 (managers acknowledge) is taken as given: `CT-al-2` withdrawn, worker stopped, branch unmerged, findings restated in `S9133`.
- `CT-al-4` was cut as an amendment the same tick check 8 was signed; its tests and `CT-al-1`'s tests were made state-aware so earlier criteria keep reproducing after the release (the file moves from holding to release).
- The issuer's dispositions of its 15 remediation rows are in the packet, section 5.

## 3. Things the CTO should know

- A seat cannot commit a row carrying a worker coordinate (`W120-S1`) and a `DISMISSED_WITH_REASON` row needs a `dismissal_reason` field: both cost the issuer a failed commit.
- The comp rail refused an S3 listing of `code/gold/` as deploy evidence (it points to `comp-pipescript deployed`, which was NOT-DECIDABLE on budget); the other-keys-changed count is the worker's and the CloudOps seat's, plus the read test.
- `check_inbox` and `get_delivery_state` each re-print the whole accumulated history on every call (dozens of messages); I use them sparingly.
- No worker worktree is cut by this seat at the close; C: has 32 GB free.
