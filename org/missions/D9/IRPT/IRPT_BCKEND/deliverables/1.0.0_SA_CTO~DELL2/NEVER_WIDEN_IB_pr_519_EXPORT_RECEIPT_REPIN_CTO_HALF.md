# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-519: irpt-export-render re-pins its ExportReceipt schema

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~23:4xZ. **Bound to:** packet `deliverables/0.9.0_WK_IRPT_BCKEND~368/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-519.md`,
sha256 `7d78889847312b5517d1d85172a93c5f1f993de30760c8f83d60c92079a7b53b` (this seat's `sha256sum`, equal to the COO half's), and the COO half
`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_519_EXPORT_RECEIPT_REPIN_COO_HALF.md`, read.

## Signed

- **The act:** `irpt-export-render` moves from live `K74JEIjw...` to built `5/9LZBbT...`. The ONE staged schema row moves (pin `8d08ee54e4` to
  `e8005582a1`). The source-map row is committed with the release.
- **The served change:** the export's own status read stops refusing its own receipts ("Additional properties are not allowed" on
  `facts.covered_account_ids`). This is Andrew's smoke failure ("The export's status could not be read (UNEXPECTED)"), live on PROD.
- **Never refuse a receipt that exists today:** the store holds one receipt, it carries the field and is refused today; it becomes readable.
  Zero receipts lack the field. The apply re-reads this count, and a receipt lacking the field found at the apply is a STOP.
- **Unchanged:** no route, IAM, schedule or permission; no figure moves.

## Conditions: the COO half's five, as written

The gates at the artifact; the digest gate to `5/9LZBbT...` with plan 0/1/0 and `safe-apply`; the latent `served:1026` mismatch carried and
not repaired (it is unreachable from this function's operations, and it is the same on live and built); the red list intersected, not
crossed; Branch B and the ledger.

**The after-read is a person's:** one new export reaching a readable status, plus the existing receipt still readable. Andrew's next
export on the IR page is that read; until then the applier reads one receipt through the function's own status route.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** at packet sha256 `7d7888984731...`.

-- 1.0.0_SA_CTO~DELL2
