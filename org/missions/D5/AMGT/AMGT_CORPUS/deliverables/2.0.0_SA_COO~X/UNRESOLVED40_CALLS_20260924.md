# The 40 identity-unresolved folders -- what their own documents say, and this seat's CALL per folder (2026-09-24 ~17:1xZ)

Andrew-direct ~16:5xZ: *"2 just go look right now and make a call, if unsure look at some of the docs and try to find a
ticker."* (record `org/tier1_exec/2.0.0_SA_COO~X/deliverables/ANDREW_DIRECT_20260924_165xZ_LOOK_AT_THE_40_AND_MAKE_A_CALL.md`).
CTO R-77 named the measurement. READ-ONLY: `unresolved40_name_census.py` (this dir) listed the folders through
`library.census`, opened every docx/pdf/xlsx "rb" through `extract.extract`, and searched for ticker forms; its raw pass is
`UNRESOLVED40_NAME_CENSUS_20260924T170319Z.json` (denominator: the 40 non-RESOLVED records of the research-backlog scan
vintage `20260924T145816Z`; 93 folders). This file is the seat's READ of that evidence plus the calls. Nothing is registered,
no vendor was called, no store was written; the calls are a MEASURED TABLE for the round-3 cut.

**One artifact corrected by eye:** the raw pass reported `KPN NA` as the document ticker for six folders. Every one of those
hits sits in the team's FactSet ONE PAGER TEMPLATE peer block (`KPN NA Equity / VOD LN / BT/A LN / ORA FP ...`, with `AAPL US`
as the template's placeholder identifier), not in the subject's own line. The subject's line in those same files reads
`Ticker: <ROOT>-<CC>` in FactSet form, which is what the calls below use. The template artifact is itself a finding: any
ticker search over these workbooks must exclude the peer block and the `AAPL US` placeholder.

## Totals (40 of 40 called; 0 NONE)

| tier | count | meaning |
|---|---|---|
| DOC | 12 | a document in the folder states the ticker itself (FactSet `Ticker:` line, `(Ticker: ...)` label, `NYSE:`/`NASDAQ:` form, or a `[ROOT CC]` note header) |
| FOLDER+LISTING | 9 | the folder name carries the ticker but no exchange code, and no document states one; the primary listing is this seat's call |
| FOLDER-PAIR | 19 | the folder name carries `ROOT CC` and no document states a ticker; the call is the folder's own pair, exchange code normalised to Bloomberg's (GB->LN, NL->NA, CA->CN) |

Three of the 40 collide with a key the pool ALREADY carries (CPA_US_Equity, UBER_US_Equity, and SLB's universe entry): the
folder IS that security, so the round-3 cell treats them as folder ASSOCIATION to the existing record (the resolve-by-folder /
ENRICH shape), never a second record.

## Amendment ~19:0xZ (before any worker read the table)

Read against the served pool: `BZLFY_US_Equity`, `UNVGY_US_Equity` and `QXO_US_Equity` are already MEASURED universe records with no
folder, and `SLB_US_Equity` is absent. So Bunzl's call becomes **BZLFY US** and UMG's **UNVGY US**, both ASSOCIATE (a folder
attached to the existing record; minting BNZL LN or UMG NA would give one company two identities), QXO becomes ASSOCIATE, and
Schlumberger becomes REGISTER. Totals now: 40 rows, 35 register, 5 associate (Copa, Uber, QXO, Bunzl, UMG). The JSON carries
the amendment. Shopify stays **SHOP CN** (the folder name and the team's research note agree; the FactSet template reads
SHOP-US; `2.0.0_SA_COO~Y` proposed SHOP US) -- a documented disagreement, raised with that lane.

## The calls

| folder | files | evidence read | CALL | tier | note |
|---|---|---|---|---|---|
| Adobe ADBE US | 1 | 1 docx, no ticker stated | ADBE US | FOLDER-PAIR | |
| Air Liquide AI FP | 0 | empty folder | AI FP | FOLDER-PAIR | identity callable; content none (never-prose: empty) |
| Alphabet GOOGL US | 1 | 1 docx, no ticker stated | GOOGL US | FOLDER-PAIR | |
| America Movil AXMB MM | 3 | earnings update `(Ticker: AMXB MM Equity)`; workbook `Identifier AMXB MM EQUITY ... AMERICA MOVIL-B` | AMXB MM | DOC | folder name is a transposition; the team's own two documents agree on AMXB |
| Bunzl BNZL GB | 1 | 1 docx, no ticker stated | BNZL LN | FOLDER-PAIR | GB -> LN |
| Cadence CDNS US | 1 | 1 docx, no ticker stated | CDNS US | FOLDER-PAIR | |
| Canadian National Railway CNR | 6 | research note `[CNR CN]`, `Ticker: CNR-CA`, peer table `CNR CN Equity CAN NATL RAILWAY` | CNR CN | DOC | |
| Celsius CELH | 2 | pitch docx `CELSIUS HOLDINGS, INC. (NASDAQ: CELH)` | CELH US | DOC | |
| Clorox CLX | 9 | research pack `CLOROX [CLX] ... Ticker: CLX-US`, peer table `CLX US Equity CLOROX CO` | CLX US | DOC | KPN hit was the template block |
| Copa CPA | 38 | research pack `COPA [CPA US] ... Ticker: CPA-US`; six press releases `Copa Holdings, S.A. (NYSE: CPA)` | CPA US | DOC | COLLIDES with existing CPA_US_Equity -> folder association |
| Eli Lilly LLY US | 1 | 1 docx, no ticker stated | LLY US | FOLDER-PAIR | |
| Global Payments GPN | 1 | 1 docx (company overview), no ticker stated | GPN US | FOLDER+LISTING | NYSE primary |
| HEICO Corporation HEI US | 1 | 1 docx, no ticker stated | HEI US | FOLDER-PAIR | |
| Idexx IDXX | 2 | 2 pdf earnings updates, no ticker stated | IDXX US | FOLDER+LISTING | NASDAQ primary |
| Intuitive Surgical ISRG US | 2 | 2 files, no ticker stated | ISRG US | FOLDER-PAIR | |
| MSCI Inc MSCI US | 1 | 1 docx, no ticker stated | MSCI US | FOLDER-PAIR | |
| Mastercard MA | 2 | 2 pdf earnings updates, no ticker stated | MA US | FOLDER+LISTING | NYSE primary |
| MercadoLibre MELI US | 2 | 2 files, no ticker stated | MELI US | FOLDER-PAIR | |
| Michelin ML FP | 10 | research pack `Michelin [ML-FR] ... Ticker: ML-FR`; ONE PAGER `Ticker: ML-FR` | ML FP | DOC | FactSet FR = Bloomberg FP; folder agrees |
| Mitsubishi UFJ Financial Group 8306 JP | 2 | ONE PAGER `Ticker: 8306-JP` | 8306 JP | DOC | |
| Monster MNST | 1 | 1 pdf earnings update, no ticker stated | MNST US | FOLDER+LISTING | NASDAQ primary |
| Netflix NFLX | 2 | 2 pdf earnings updates, no ticker stated | NFLX US | FOLDER+LISTING | NASDAQ primary |
| Nike NKE US | 1 | 1 docx, no ticker stated | NKE US | FOLDER-PAIR | |
| QXO | 1 | investor Q&A pdf, no ticker stated | QXO US | FOLDER+LISTING | NYSE primary |
| Quanta Services PWR | 1 | workbook `Quanta Services (NYSE: PWR) EPS & Backlog History` | PWR US | DOC | workbook-only folder (never-prose) but identity is stated |
| Schlumberger SLB | 3 | `Ticker: SLB US SLB LTD`, workbook `Identifier SLB US EQUITY` | SLB US | DOC | the universe carries an SLB entry UNRESOLVED (R-76) -> association, not a second record |
| ServiceNow NOW US | 2 | 2 files, no ticker stated | NOW US | FOLDER-PAIR | |
| Shopify SHOP CA | 5 | research pack `SHOPIFY [SHOP] ... Ticker: SHOP-CA`; ONE PAGER `Ticker: SHOP-US` | SHOP CN | DOC | CA -> CN (Toronto primary); dual-listed SHOP US noted |
| Spotify SPOT US | 2 | 2 files, no ticker stated | SPOT US | FOLDER-PAIR | |
| Sumitomo Mitsui Financial Group 8316 JP | 1 | 1 docx (management/board), no ticker stated | 8316 JP | FOLDER+LISTING | Tokyo primary; the folder pair `8316 JP` is numeric so the pair parser skipped it |
| Synopsys SNPS US | 1 | 1 docx, no ticker stated | SNPS US | FOLDER-PAIR | |
| Taiwan Semiconductor Manufacturing TSM US | 2 | 2 files, no ticker stated | TSM US | FOLDER-PAIR | the ADR; the folder's own choice |
| Tokyo Electron 8035 JP | 1 | 1 pdf, no ticker stated | 8035 JP | FOLDER+LISTING | numeric pair, as 8316 |
| Tokyo Marine 8766 JP | 3 | ONE PAGER `Ticker: 8766-JP` | 8766 JP | DOC | |
| Uber Technologies UBER US | 13 | earnings update `(Ticker: UBER US Equity)` | UBER US | DOC | COLLIDES with existing UBER_US_Equity -> folder association |
| UnitedHealth Group UNH US | 1 | 1 docx, no ticker stated | UNH US | FOLDER-PAIR | |
| Universal Music Group UMG NL | 2 | 2 files, no ticker stated | UMG NA | FOLDER-PAIR | NL -> NA |
| Visa V | 2 | 2 pdf earnings updates, no ticker stated | V US | FOLDER+LISTING | NYSE primary |
| Workday WDAY US | 3 | 3 files, no ticker stated | WDAY US | FOLDER-PAIR | |
| Zoetis ZTS US | 1 | 1 docx, no ticker stated | ZTS US | FOLDER-PAIR | |

## What this changes for round 3

- The 40 are no longer UNMEASURED: **40 of 40 carry a callable identity** on this table -- 12 stated by the folder's own
  documents, 28 by the folder's own name (9 with the listing supplied by this seat). Under Andrew's word above, the table is
  the evidence basis the round-3 induction cell consumes: one `add_security --batch` run over it (R-16 V2's word covered
  ONE call for each of the 60 unresolved names, ONCE; 20 were called today, these 40 have not been), with the three
  collisions routed to folder association instead of a call.
- Content stays what R-75 measured: 10 of these folders are workbook-only or empty and can never carry prose; identity
  resolution does not change that, and the census's never-prose list already names them.
- The template artifact (KPN/VOD/BT/ORA peer block, `AAPL US` placeholder) is a rule for any future document-ticker reader.
