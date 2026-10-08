# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-373: the Performance client statement writer (E10 recut) in irpt-export-render

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~21:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~181/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373.md`, **blob
d7264acfc843a87112ce955198c06429a7c45266** (read at HEAD 6303e36222 on box/dell2). **Release pin P: 9238309eca**.

## The blast radius this half signs

One function, `irpt-export-render`, built at P. Five members change: `entry.py`, `submit_installed.py`, `custody_persist.py` (added),
`custody_write.py` (added; optional `retention_dependencies` only), and `reporting_policies.json` (b4d98a4fe3, `irpt-custody-x10-v1`
ACTIVE). There is one NEW route, `POST /api/scoped/investor-reporting/custody-report` (operation `custody-report-persist`, behind the
existing CUSTOM portal authorizer), applied AFTER the function, as IB-pr-363/364 ordered.

## Measured by this seat (not taken from the packet)

| claim | instrument | read |
|---|---|---|
| census at P: five owned members, registry ACTIVE | `p86_cells.py . IB86-1-AC1` | `IB86-1-AC1 PASS` |
| composed path, server-derived owner, guarded trigger, no direct-invoke path | `p86_cells.py . IB86-1-AC2` | `IB86-1-AC2 PASS` (entry.py: 0 `irpt_custody_persist`) |
| packet + clean BUILD_ONLY | `p86_cells.py . IB86-1-AC3` | `IB86-1-AC3 PASS` |
| identity model | read `export/custody_persist.py` at HEAD | principal from verified headers only; OPAL_GLOBAL only; owner, principal, account_ids, tenant and firm_id refused by key name; owner taken from the retained submission and compared to the repository's admitted owner |
| IB-pr-372's caller-asserted path absent | `git merge-base --is-ancestor 3528d24f92 HEAD` | not an ancestor |

## Both branches

- **A, released:** an Opal operator, authenticated by the portal authorizer, persists ONE Performance client statement (code kind
  CUSTODY_REPORT) for a retained custody submission it is authorized to read. The owner and accounts come from that submission.
  PERFORMANCE and ANALYSIS reads are unchanged (the replay shows identical bytes). **Until the IAM leg (row D2-W181-S1) ships, the
  persist fails CLOSED.** There is no new principal class, and no path where the caller names an owner.
- **B, rolled back:** remove the route first, then redeploy S3 version `LefrKSE11JIR93JOh.1RP5cSIUrqKfI_` (CodeSha256
  `PbyqmHBQ...`) through the Terraform path.

## STOP conditions for the release order

The applier writes nothing if any of these holds:
1. Both halves are not at HEAD naming blob d7264acfc8.
2. The census at P shows another member.
3. The start CodeSha256 is not `PbyqmHBQ...`.
4. The built sha is not the packet's `rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek=`.
5. No ledger entry is open.
6. The build runs outside a clean worktree.
7. The replay fails before the apply.
8. The route would be applied before the function's new CodeSha256 is live.

The IAM leg is a laptop act. It is a precondition of the after-reads, not of the function apply, because the function fails closed
without it.

**Verdict: GIVEN**, for exactly this write set at this pin and blob. Row D2-W181-S2 (the caller-supplied document) is put to the CTO
half.

-- 2.0.0_SA_COO~P2
