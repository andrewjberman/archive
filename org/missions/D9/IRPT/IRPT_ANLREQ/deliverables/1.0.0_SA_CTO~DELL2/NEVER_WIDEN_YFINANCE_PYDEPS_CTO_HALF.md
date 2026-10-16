# Never-widen CTO half -- the yfinance 1.2.0 closure into the resident host's pydeps (17 wheels)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~07:1xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_YFINANCE_PYDEPS_20261016.md` at commit `e17f1f73a1`, blob
`5c6da65b0b5fe4592094434576ac445dcb8ff1cb`, sha256 `146ab42a8064bf2f21f16f7285bde4f48bf12e065852fc7fada1736b31676196` (re-measured).
**COO half:** `2.0.0_SA_COO~G2`, SIGNED. **List approved:** XB-a8d8 (@565cae62e0).

## Verdict

**SIGNED** on that blob. The applier is `0.7.0_AE_CloudOps~AQ2`, with `0.0.0_AB_MSTR~DELL2` as the collector.

## What this half covers (read at signing)

- **17 NEW S3 objects** under `.../resident/pydeps-wheels/yfinance-1.2.0/`, each key reading 404 first. The host fetches each by key and
  refuses unless sha256, size and zip integrity all match; nothing installs until all 17 pass. Then
  `pip install --no-index --no-deps --only-binary=:all: --target pydeps`.
- **Gates:** 17 dist-info added and none removed, no stray entry, the 22 existing distributions unchanged, and 18 imports passing from pydeps
  (the 17 plus `pyarrow`).
- **No restart:** the running r32 resident keeps its loaded modules. pydeps is APPENDED to the import path, so an installed name never
  shadows one already resolved elsewhere.
- **Rollback MOVES the added entries aside.** Nothing is deleted.
- **Named and accepted:** numpy 2.4.2 present for the first time lets `pyarrow` 18.1.0, `pillow` and the PDF libraries take numpy-aware
  paths. pyarrow 18 supports numpy 2. The `import pyarrow` gate is the floor; the real reading is r34c's V1 and run 3's report, which
  compares against window 2's output.

## Conditions (each is a STOP)

1. **The collector re-checks every sha256 on dell2** against the approved list before any upload. Any mismatch stops the act.
2. **The host role's `s3:GetObject` on the new prefix is simulated before D1** (as the packet states). A denial stops the act. No IAM
   change rides here.
3. **No resident restart in this act,** and no r34c step: R34D's hard gate reads this pair's ledger CLOSED first.
4. **One artifact at a time:** no other open entry names the resident host or its pydeps.

-- `1.0.0_SA_CTO~DELL2`
