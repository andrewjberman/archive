# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-518: Opal Ultra Short-Term in the served comparison catalogue

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~22:2xZ. **Bound to:** packet `deliverables/0.9.0_WK_IRPT_BCKEND~367/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-518.md`,
sha256 `7439728602c6b63b19e727ffacced7c57cb513c0abbd676febd1c778e4f7cd99` (this seat's `sha256sum`, equal to the COO half's), and the COO half
`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_518_CATALOGUE_FUNCTION_COO_HALF.md` @d06ee1f0fc.

## Signed

- **The act:** `irpt-ycharts-generate` moves from live `hpNfkhLt...` to built `xP47NQDn...`. 2 of 104 members change.
- **The served change:** the catalogue lists five Opal models in canonical order (Ultra Short-Term, Short-Term, Intermediate-Term,
  Long-Term, Ultra Long-Term), the new one keyed `opal_ultra_short_term` in the OPAL namespace with no YCharts id.
- **The visible change, signed on Andrew's word:** the four existing models REORDER for every firm (Long-Term goes from first to
  fourth). Andrew asked for exactly this on 2026-10-13: "they should be arranged in canonical order", and "we're missing the Opal
  Ultra Short-Term".
- **Unchanged:** permission (3 firms, 3 principal classes); no figure moves; no route, IAM, schedule or cache surface.

## Conditions

1. **One change at a time on this function.** It is also the target of IB-pr-456 and of IRPT_ANLREQ's consolidated FWD-1 release
   (r19.3 resident and Lambda legs). Whichever applies second re-censuses against the then-live bytes and carries a fresh packet sha256.
   No two applies overlap in one window.
2. **The digest gate:** rebuild to `c4fe3b35...` or ABORT. Plan 0/1/0. Use `safe-apply`. Rollback to the live version re-read at step 3.
3. **The after-read:** the served catalogue returns the five labels in canonical order for one permitted firm. The Analysis Request
   form on DEV lists Ultra Short-Term. The admission refusal of an altered entry is shown.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** at packet sha256 `7439728602c6...`.

-- 1.0.0_SA_CTO~DELL2
