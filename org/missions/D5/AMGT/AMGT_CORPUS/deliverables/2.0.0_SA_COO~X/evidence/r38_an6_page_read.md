# AMGT_CORPUS round 38 CRPS-an-6 -- FWD-20's currency limb read on the page, after an-2 (2026-10-06 03:35-03:41Z)

## The walk

| | |
|---|---|
| walk | `/ui-walk` signed in, `tmp/ui-walk/20261006T033542Z/` (gitignored: the shots carry client data) |
| build | local dev :5174 at portal DEV `7d1ea524` (`bun run dev:live`, live deployed backend) |
| route | `/security-analysis` |
| names | TSM US (TWD reporting, USD quote), SAP GY (EUR), BA US (USD, the positive control) |
| result | 92 shots, 0 guard aborts, walk void no |
| walker slot | MSTR~Z msg 29881; ARM 03:35Z; DISARMED 03:41:20Z (walk password REFUSED 401) |
| served data | read after an-2's re-derive (ledger `amgt-corpus-r38-an2` CLOSED @`d1b66b2562`) |

## Model tab, financial summary (shots 012, 041, 074)

| name | table header | every money row names its currency | share-count rows | forecast columns |
|---|---|---|---|---|
| TSM US | "Figures in TWD" | yes, e.g. "EPS (per share, TWD)", "EBITDA (millions, TWD)", "Total assets (millions, TWD)", "Short and long-term debt (millions, TWD)" | none served (listed under "No figures served for: ... Diluted shares ...") | 2026E-2027E visible; 2028E clipped at the card edge |
| SAP GY | (EUR) | yes, every money row "(..., EUR)", e.g. "Goodwill (millions, EUR)", "Free cash flow per share (per share, EUR)" | "Diluted shares (millions of shares)": **no currency** | 2026E-2028E all visible |
| BA US (control) | "Figures in USD" | yes, every money row "(..., USD)" | "Diluted shares (millions of shares)" and "Shares outstanding, as reported (millions of shares)": **no currency** | 2026E-2028E all visible |

**Result: on all three names, every money row in the financial summary names its currency.** The two count rows the page shows
carry none. That is CRPS-an-1's fix, served by an-2, on the page.

## One row outside the financial summary

**Where:** the "What changed" panel above the table, which compares Bloomberg versions. On TSM US, its "Enterprise value" row reads
"unit not resolved -- raw figure 71,993,494.73 / 75,714,013.45 / currency not stated".

**What it shows:** the row states its own reason. It is not a silent blank.

**Compared with the other names:** on BA US the same row reads "USD 187B / USD 185B".

**Assessment:** TSM's enterprise value is unresolved on a mixed-currency name (an ADR quoted in USD, reporting in TWD). It is laid
here against FWD-20's "every money row names its currency" for the CVO to grade.
