# NFRA_MCPINDEX -- input map for Andrew-direct 2026-10-09 ~03:2xZ ("all of this should be indexed")

Prepared by `2.0.0_SA_COO~MI`, 2026-10-09 ~03:5xZ, for `1.0.0_SA_CTO~O`, the carrier of the re-cut. It is a fact base for
the CTO's addendum or round analysis. It cuts nothing, and rules nothing outside this lane's decomposition.

Andrew's record: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261009_032xZ_MCPINDEX_INDEX_ALYSSA_WORKFLOWS.md`
@5716c7a83d.

## The two named inputs (located and read 2026-10-09 ~03:4xZ through the gateway, read-only)

SharePoint site `Shared` (`opalinvest.sharepoint.com,9332c03f-2ad0-4b84-97fe-7bcd2c9cb90a,18b7f31c-c878-41ea-9b7e-0c103bcb5679`):

| doc | path | item id | modified | size |
|---|---|---|---|---|
| External Chrome Workflows Brief | `Shared Documents/Product-Alyssa/PRD-004_gateway-data-feeds/assets/External Chrome Workflows Brief.md` | `01L6LHKFXGQPFGLCCSAJCLT634BZ66GEBF` | 2026-10-08T16:01:15Z | 12,048 B |
| Schwab Data Needs Brief | `Shared Documents/Product-Alyssa/PRD-004_gateway-data-feeds/assets/Schwab Data Needs Brief.md` | `01L6LHKFT5G5BWB7CHBBFK7PZ544S2SNEO` | 2026-10-08T16:00:29Z | 12,873 B |

The same folder holds an intake note (`intake/2026-10-08_external-chrome-workflows-brief.md`, 798 B). Sibling folders
`PRD-003_cio-hunt` and `_handoff-andrew-2026-10-05/REPORT-SCRIPTS.md` were seen but NOT read.

## Map: each brief item -> the FWD that covers it today, or the gap

Owner key: **MX** = NFRA_MCPINDEX (this project, PRD v0.6). **OG** = NFRA_OPLGTW (PRD v2.1, `2.0.0_SA_COO~O`).
"Gap" = no FWD names it.

### External Chrome Workflows Brief (C1-C8)

| item | what Alyssa does in Chrome today | nearest FWD | state |
|---|---|---|---|
| C1 | YCharts reports: create portfolios, generate the Overview/Comparison/Multi-Comp PDF; ~30 households a month (P0) | MX FWD-8 (on-demand vendor reads; MX-h-3 put ycharts in the index) | PARTIAL. The brief says `ycharts_time_series` returns 403 and `ycharts_snapshot_metrics` returns 404 (UNVERIFIED here). Report generation is a WRITE into a shared seat; no FWD covers it. |
| C2 | opalinvest.dev reads: model performance by period, AUA by partner, attribution, account counts (P0) | MX FWD-2 (the portal's own number for any portal figure) | COVERED by FWD-2's intent. Named tool shapes in the brief: `opal_model_performance`, `opal_aua(basis)`, `opal_account_counts(basis)` with month-end history and a basis label. The month-end account-count HISTORY does not exist anywhere (brief W5): a gap in DATA, not in an index. |
| C3 | Schwab Advisor Center: Tax SMA quarter-end statements, realized and unrealized cost-basis exports (P0, highest risk) | OG FWD-10..14 | OWNED BY OG. Not MX work beyond FWD-3's Schwab question classes. |
| C4 | Outlook mail bulk move/delete/folder create (P1) | none; open-calls `sitez-20261008T174201Z-f241` ("gateway mail-move and Teams-send write tools?", fork NFRA_MCPINDEX) is CLOSED | Gap, and a WRITE class. The ruling on f241 should be read before any cut. |
| C5 | Teams send as Alyssa (P1) | same call f241 | Gap, WRITE class; same as C4. |
| C6 | SharePoint/mail-attachment download to a local folder (P1); `save_email_attachment_to_site` returns `write_class_denied` | none | Gap. |
| C7 | Threshold bar-directory headless fetch (P2, inferred, not observed live) | none | Gap; the brief recommends licensed data instead. |
| C8 | Local Playwright PDF render | n/a | Not a browser workflow (the brief says no change). |

### Schwab Data Needs Brief (W1-W6, P0-P2 asks)

| item | need | nearest FWD | state |
|---|---|---|---|
| W1 Tax SMA quarterly | master 0840-3355, crosswalk, lots, realized G/L, 13 months | OG FWD-10, -11, -12, -13, -14 | OWNED BY OG (PRD v2.0/v2.1). |
| W2 advisor account-review | one account's positions, balances, transactions, cost basis by account number | OG FWD-10 (find by account number) + FWD-11 | OWNED BY OG. |
| W3 held-away prospect statements | positions parsed from emailed PDFs; NOT in Opal masters | none | Gap. Out of gateway reach per the brief; the blocker is email-attachment intake (same as C6). |
| W4 transition / sell-down proposals | lot-level basis, 30-day history for wash sale | OG FWD-11 + FWD-12 | OWNED BY OG once lots exist. |
| W5 board AUM / account counts by partner, month-end series | custodian-side month-end series | MX FWD-2 (portal figures) + Schwab ask P2-12 | PARTIAL; the month-end account-count history is a data gap (see C2). |
| W6 model performance vs benchmark | returns by period | MX FWD-2 (`platinum/mdpf`), MX-t-9 (model benchmarks tool) | COVERED in intent; the brief still reads it in Chrome. Worth one live check that the existing tool answers her exact question shape. |
| P1-10 | GICS sector and coupon on `dim_asset` | none | Gap (sector for Tax SMA top-10 holdings / allocation). |
| P2-11 | a gateway Modified Dietz helper | none | Gap. |
| P2-13 | account metadata (registration, rep code, household, model, open date) | OG FWD-10 in part | PARTIAL. |

## What this says for NFRA_MCPINDEX, plainly

1. The INDEXING half Andrew named sits on FWD-1 (discover routes a question to the right tool) and FWD-2/FWD-8 (the
   tools exist). Every item above becomes a catalog row with its owner, tool and coverage state. The S8 per-property
   analysis is the PRD's own home for "what people actually ask". These two briefs are that analysis for Alyssa,
   already written.
2. The BUILD half splits three ways:
   - Schwab (C3, W1, W2, W4) is OG's and already in flight.
   - Portal reads (C2, W5, W6) are MX FWD-2 tools.
   - YCharts reports, mail/Teams writes and file download (C1, C4, C5, C6) are gaps; no FWD names them.
3. Questions for the CTO, not for this lane:
   - Do C1, C4, C5 and C6 enter NFRA_MCPINDEX, NFRA_OPLGTW or a new project?
   - The f241 ruling (write tools) already exists; what did it rule?

## Instrument notes

- Read through the gateway: `find_sharepoint_site` ("project" returned 0 sites; "shared" returned the `Shared` site),
  then `search_site_files` ("Claude Chrome") and `read_site_file` x2. Nothing was downloaded or written to SharePoint.
- The 403/404 on the ycharts tools and every "inferred" line are the brief's claims, NOT measured here.
