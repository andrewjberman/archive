# Never-widen CTO half -- resident r34t (typed ETF, per-model dates, left-out line, risk tables, C-SWAP model leg)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~11:2xZ.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34T_TYPED_ETF_MODEL_DATES_LEFT_OUT_LINE_RISK_TABLES_AND_SWAP_MODEL_20261021.md`
- git blob `cf84479159f8b1c26b30814ca254bc07be6c7106`, sha256 `3ed4edcaf8f10a2b576b78724f7d3d5f0ff1ac5084e4de0bbb020cd82c82cea3`, commit e75ce7268b.
- Package pin c17477bc32, tar sha256 35a4f044c2bc..., 325 members: 9 changed, 2 added, 0 removed.

## What was read here
- **Rulings carried:**
  - typed ETF and per-model dates (round 60 G analysis @e1ed2d1914);
  - the left-out line and page 21 (msg to G2, 10:00Z);
  - C-SWAP checks (msg to Y2, 10:17Z).
- **Typed ETF:** measured on the real door, then fixed. The ETF is priced through the holdings' existing tiers (estate, yfinance, then YCharts last), the same vendor path the holdings already use. There is no new vendor leg.
- **C-SWAP model leg:**
  - It calls Moonshot kimi-k3 at `api.moonshot.ai/v1/chat/completions`, with no tools and no web search, sending a symbol and a class only. No client figures are sent.
  - Below 0.80 it flags `low_confidence`. Every swap is named in the swap record.
  - The resident role already reads the estate Kimi key: simulated `allowed` by Y2 at 10:19Z, and re-read `allowed` here at 10:22Z.
  - The binding `opal_swap_model` is optional, and an invalid value refuses at install.
- **Unmoved:** IAM, queues, tables, schema, registry, run.json, lease, budget and tiers.

## Both branches
- **V2S OK:** r34t runs. Then, one at a time:
  - run 7M (Multi-Comp with a typed ETF): the per-model dates read live, and FWD-10's ETF leg goes to the CVO;
  - run 7N (Overview with ZQXWVK kept plus BREIT): the left-out line, page 21 and the swap leg read live.
- **Not OK:** roll back to r34s and report. No retry.

## Conditions on the apply
- **Not inside the weekday no-deploy band, 11:30Z to 14:15Z:** the install starts at or after 14:15Z.
- Nothing else open on IB2.
- The 7N read names each swap's class, its confidence, and any `low_confidence` flag. A swap applied silently is a STOP.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
