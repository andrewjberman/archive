# Portal Page Project Codes

Canonical 4-character codes for every portal page and pipeline context.
Use these as the `{CODE}` when registering projects in `org/projects/`.

All codes are exactly 4 characters. No 1-3 char codes are issued to prevent
ambiguity as the project list grows.

---

## Pod 1 — MarketIntelligence

Responsible pod: `0.1.0_DE` / `0.1.0_DS` / `0.1.0_DT`

| Code | Page / Context | Portal Directory | RD Agent | Pipeline |
|------|---------------|-----------------|----------|----------|
| `MKPF` | MarketPerformance | `portal/src/pages/MarketPerformance/` | `0.1.1_RD_MarketPerformance` | yang-pipeline, market-overview |
| `CENG` | CausalityEngine (+ MarketUpdate) | `portal/src/pages/CausalityEngine/` | `0.1.2_RD_CausalityEngine` | causality, news-pipeline |
| `CMAS` | CapitalMarketAssumptions | `portal/src/pages/CapitalMarketAssumptions/` | `0.1.3_RD_CapitalMarketAssumptions` | yang-pipeline |
| `MKOV` | Market Overview pipeline | (lambda/pipeline context, no single portal page) | — | market-overview |

---

## Pod 2 — PortfolioAnalytics

Responsible pod: `0.2.0_DE` / `0.2.0_DS` / `0.2.0_DT`

| Code | Page | Portal Directory | RD Agent | Pipeline |
|------|------|-----------------|----------|----------|
| `POSN` | Positioning | `portal/src/pages/Positioning/` | `0.2.1_RD_Positioning` | yang-pipeline |
| `ATTR` | Attribution | `portal/src/pages/Attribution/` | `0.2.2_RD_Attribution` | yang-pipeline |
| `FCTL` | FactorTilts | `portal/src/pages/FactorTilts/` | `0.2.3_RD_FactorTilts` | yang-pipeline |
| `VALU` | Valuation | `portal/src/pages/Valuation/` | `0.2.4_RD_Valuation` | yang-pipeline |
| `MACR` | Macroeconomics | `portal/src/pages/Macroeconomics/` | `0.2.5_RD_Macroeconomics` | yang-pipeline |
| `CORR` | Correlation | `portal/src/pages/Correlation/` | `0.2.6_RD_Correlation` | yang-pipeline |

---

## Pod 3 — TradingOperations

Responsible pod: `0.3.0_DE` / `0.3.0_DS` / `0.3.0_DT`

| Code | Page | Portal Directory | RD Agent | Pipeline |
|------|------|-----------------|----------|----------|
| `PFMG` | PortfolioManagement | `portal/src/pages/PortfolioManagement/` | `0.3.1_RD_PortfolioManagement` | portfolio-management |
| `TRSB` | TradeSubmission | `portal/src/pages/TradeSubmission/` | `0.3.2_RD_TradeSubmission` | smartx-pipeline |
| `DRFR` | DataRefresh | `portal/src/pages/DataRefresh/` | `0.3.3_RD_DataRefresh` | (cross-pipeline) |

---

## Pod 4 — ClientPlatform

Responsible pod: `0.4.0_DE` / `0.4.0_DS` / `0.4.0_DT`

| Code | Page | Portal Directory | RD Agent | Pipeline |
|------|------|-----------------|----------|----------|
| `MDLP` | ModelPortfolios | `portal/src/pages/ModelPortfolios.tsx` | `0.4.1_RD_ModelPortfolios` | yang-pipeline |
| `ADVI` | AdvisorIntelligence | `portal/src/pages/AdvisorIntelligence/` | `0.4.2_RD_AdvisorIntelligence` | bd-pipeline |

---

## Cross-Pod / Infrastructure Codes

For projects that span pods or live purely in infrastructure with no single page owner.
Assign the DE/DS/DT of the primary pod, or the AE for pipeline-only projects.

| Code | Context | Primary Owner |
|------|---------|---------------|
| `YALP` | Yang pipeline (cross-pod) | `0.5.0_AE_OpalETL` |
| `BDPL` | BD pipeline | `0.6.0_AE_PartnerETL` |
| `NPPL` | News pipeline | `0.5.0_AE_OpalETL` |
| `SXPL` | SmartX pipeline | `0.6.0_AE_PartnerETL` |
| `SHIF` | Shared infrastructure | `0.7.0_AE_CloudOps` |

---

## Rules

1. All codes are exactly 4 characters — no exceptions.
2. Codes map 1:1 to a page or pipeline context. No code covers multiple pages
   unless those pages share one RD agent and one pod (e.g., CENG covers
   CausalityEngine + MarketUpdate because both are owned by 0.1.2_RD).
3. When a project spans multiple pages, pick the primary page's code OR use a
   cross-pod code and list all affected pages in the project JSON file.
4. New codes must be added here before use. Check this file before assigning
   a new project code.
