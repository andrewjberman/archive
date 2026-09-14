# POSN_ASTTAX -- COMPLETION BRIEF, narrowed to the Positioning page

**Author:** 4.0.0_SA_CRO~Z (Chief Research Officer, site-Z lane)
**Home:** org/tier1_exec/4.0.0_SA_CRO~Z/
**For:** 1.0.0_SA_CTO~Z (L2/L4 owner), on Andrew's word of 2026-09-14 ~16:00Z and ~16:34Z
(records `deliverables/ANDREW_DIRECT_20260914_1600Z_...md` @d5f883ce90 and
`deliverables/ANDREW_DIRECT_20260914_1634Z_...md`)
**Status:** v0.2 -- pitched to Andrew at this seat's terminal ~16:5xZ; read by `1.0.0_SA_CTO~Z` from the tree at
v0.1 @ee4b7e5539 and carried into its close-out breakdown
`org/tier1_exec/1.0.0_SA_CTO/deliverables/POSN_ASTTAX_CLOSEOUT_BREAKDOWN_20260914_Z.md` @a35baa02ea, which is now
the cell-level authority (its s.3 eight cells supersede s.4 step 2 below). **v0.2 (2026-09-14 ~17:2xZ):** file
locations corrected on the CTO's measurement (msg 22836) -- `SelectionTab.tsx` and `holdings-shared.tsx` are
ATTRIBUTION files at pin `e85f6eb84f`, not Positioning; s.8 added with this seat's alignment notes on the breakdown.
**Not a recon engagement; no RCN id.** Everything below is measured on the LIVE plane at the vintages
stated, never from a document's description of it.

---

## 0. THE ONE-PARAGRAPH VERSION

The satellites do not hold GLD and VXX "outside the models" in Black Diamond's data. **Black Diamond's
copies of the five Opal models hold them; Yang's copies do not.** Every Opal Satellite in the rebalancer
is a pure blend of BD's models (0 securities at any satellite root, 13 of 13 sleeve references resolve to
the standalone BD model ids), and the portal builds satellites by blending YANG's models. So the gold and
the volatility overlay are lost at the sleeve, not at the satellite. The fix is to source the Satellites
toggle from Black Diamond's flattened holdings, coalesced by ticker, classified through ETFClassifier --
and to keep the Models toggle on Yang. The two must never be summed: they are two versions of one model,
and the satellite column takes the traded one. Everything else on this project (deploy, retag, seed
script, frontend) is already priced and is small.

## 1. WHAT IS TRUE, MEASURED 2026-09-14

**Source A -- Black Diamond rebalancer**, `s3://opal-data-assets/blackdiamond/cottonwood/bronze/
rebalancer_model_detail/2026-09-14/` (81 files, landed 06:00:54Z). Every `Opal Satellite N` is
`rebalanceModelType=Strategy` with `root components = 0` and `children[]` = BD model nodes. The
child nodes carry the SAME `id` as the standalone BD models (13 of 13). The standalone BD models
carry the overlay:

| BD model (= Positioning book) | GLD | VXX | CASH | leaves |
|---|---|---|---|---|
| Opal Short-Term (ST) | 8.34% | -- | 0.84% | 16 |
| Opal Intermediate-Term (INT) | 3.99% | 1.40% | 0.65% | 20 |
| Opal Conservative Growth (LT, ruled) | 2.11% | 1.87% | 0.96% | 16 |
| Opal Long-Term Aggressive (ULT) | -- | 1.87% | 1.05% | 16 |
| Opal Ultra Short-Term Income (UST) | -- | -- | 1.00% | 14 |

**Source B -- Yang's served models**, `s3://opal-data-portal-v2/json/positioning/positioning_data.json`
(`data_as_of 2026-09-11`, generated 2026-09-12T11:05Z): GLD in **0 of 5** books; VXX in LT 1.50% and
ULT 2.00% only; no CASH line in any book; ICSH in **5 of 5** Yang books and **0 of 5** BD models.

**What the portal shows today vs what BD holds** (registry `as_of 2026-09-14`, 9 books):

| satellite | legs | GLD portal | GLD BD | VXX portal | VXX BD |
|---|---|---|---|---|---|
| 15 | ST 100 | 0.00% | **8.34%** | 0.00% | 0.00% |
| 30 | ST 75 / INT 25 | 0.00% | **7.25%** | 0.00% | 0.35% |
| 40 | ST 50 / INT 50 | 0.00% | **6.17%** | 0.00% | 0.70% |
| 50 | INT 75 / ST 25 | 0.00% | **5.08%** | 0.00% | 1.05% |
| 60 | INT 100 | 0.00% | **3.99%** | 0.00% | 1.40% |
| 70 | LT 50 / INT 50 | 0.00% | **3.05%** | 0.75% | 1.64% |
| 80 | LT 100 | 0.00% | **2.11%** | 1.50% | 1.87% |
| 90 | ULT 100 | 0.00% | 0.00% | 2.00% | 1.87% |
| 98 | ULT 100 | 0.00% | 0.00% | 2.00% | 1.87% |

So the current satellites toggle is wrong on gold for 7 of 9 satellites and wrong on VXX for 6 of 9 --
in BOTH directions (90/98 overstate). The DT brief of 2026-09-11 ("VXX is already done") was true of
the models path and false of the satellites, because it measured the blend, not Black Diamond.

**Two premises corrected, stated so nobody re-derives them:**
1. *"GLD/VXX sit at the satellite level, outside the model constituents."* Not in the data plane. They
   sit INSIDE Black Diamond's model sleeves and identically in the standalone BD models. "Outside the
   model" is true only in the sense *outside Yang's version of the model*. Two objects, one name.
2. *"A ticker inside the model and outside it must be coalesced (summed)."* Within BD there is no such
   pair -- each sleeve carries one row per ticker, and a ticker in two sleeves (GLD in Sat 30: ST 6.26 +
   INT 1.00 = 7.25) sums by construction. Between BD and Yang the pair DOES exist (LT VXX: 1.87 vs 1.50)
   and it must NOT be summed -- summing double-counts. The satellite takes BD's number; Yang's is
   disclosed beside it.

**Beyond GLD/VXX, found in passing and NOT this project's:** the two versions differ materially
elsewhere -- ST BIV 19.0% (Yang) vs 11.2% (BD); INT BIV 8.4% vs 4.2%; ICSH present only in Yang; INT
SPYM is the known duplicate-row defect. A models-vs-rebalancer drift row is owed on the surprise channel
by this seat; it is a Yang/Andrew reconciliation question, not a POSN cell.

## 2. THE DESIGN -- four rules

**R1. The Satellites toggle is sourced from Black Diamond.** Per satellite: flatten `components[]`
across its sleeves, group by `metadata.symbol`, sum `absoluteAllocation`. That is the whole coalescing
rule, and it already handles the case BD does not exercise today (a security at the satellite root;
0 of 9 now) with no code change if it ever appears.

**R2. The Models toggle stays Yang's.** Models = the design; Satellites = as-traded. They will disagree
by exactly the overlay, and the artifact DISCLOSES it rather than hiding it: each coalesced row carries
`weight` (BD), `weight_models_blend` (what the Yang blend would have said) and `overlay = weight -
weight_models_blend`. A negative overlay (Yang holds more than BD, e.g. ULT VXX) is a drift flag, surfaced
and never clipped. **Never sum the two sources.**

**R3. Classification from ETFClassifier, the one place.** Each coalesced ticker gets `asset_class` /
`sub_asset_class` from the served DynamoDB table through the shared module. The satellite's five-class
allocation is computed from those labels times the coalesced weights. This is FWD-1 / FWD-2 / FWD-5
exercised on real satellites, and it is where the retag lands: Sat 15 renders Commodities 8.34% in its
own bucket. This is the outcome Andrew named as the reason the project exists.

**R4. Characteristics.** Per-ticker fee / yield / duration / beta / returns are carried from Yang's
`current_holdings` for any ticker a Yang book holds (VXX and the ETFs -- the established precedent in
`satelliteAdapter.ts`), and are NULL for tickers no Yang book holds (GLD, CASH) until the Bloomberg daily
pull carries them. Null renders today (VXX's yield/duration already do). Adding GLD and VXX to
`etf_daily_pull.py FUNDS` is the Bloomberg lane's two-string change (DT step 0) and is time-sensitive:
those fields have no backfill.

## 3. WHERE IT LIVES -- extend, never add (build ladder)

| layer | today | change |
|---|---|---|
| producer | `cot-satellites-registry-producer` (daily, reads the same bronze partition, writes `s3://opal-data-cot/platinum/satellites/registry.json`) | emit a sibling key in the same prefix on the same schedule, `holdings.json`: `{as_of, source, claim, satellites: {code: [{ticker, weight, sleeves:[{book, weight}], weight_models_blend, overlay, asset_class, sub_asset_class}]}}`. ETFClassifier read from a lambda is established (`_shared/etf_classifications_dynamodb.py`). |
| route | `@/api/endpoints/satelliteRegistry` over the scoped satellites route (ETFS_SATELLITES TO-7/TO-8) | the new key rides the same route family; no new route class, no new bucket (cot stays in cot -- CLAUDE.md NEVER cross-firm) |
| portal | `satelliteAdapter.ts` union-blends Yang holdings (B) and blends book measures (A) | (B) is replaced by the served coalesced holdings; the allocation block becomes five-class from served labels; (A) stays for measures where per-ticker characteristics are missing. `HoldingsTab` and `PositioningSummary` render the satellite column through the same five-class order and colour fix every mode needs (both bind colour through `src/lib/chartColors.ts`); `SelectionTab` is an Attribution file and gets only a one-line no-regression guard. |
| untouched | Yang's PKL, the models generator's holdings, the Models toggle, the ETFs toggle, the registry producer's membership predicate | -- |

No shadow pipeline, no parallel artifact, no monitor. One producer, one artifact family, one adapter.

## 4. THE COMPLETION PLAN -- Positioning page only, in order

| # | step | owner | state today |
|---|---|---|---|
| 0a | Relaunch `2.0.0_SA_COO~Z` and `3.0.0_SA_CVO~Z`; `1.0.0_SA_CTO~Z` lifts the CVO stop | Andrew / CTO | both down post-reboot |
| 0b | CVO adjudicates round 4 (packet handed 2026-09-13T07:54Z, 25 rows); COO marks `TO-S2-1`/`TO-S3-1` **superseded** by `TO-T6-1`/`TO-T7-1` (their own headers say so); round-4 slug | CVO / COO | 4 carried orders block the L10 refuser |
| 0c | Round-4 analysis + **PRD v0.7 addendum**: (i) this design as constraint `C-SATELLITE-SOURCE` and a fourth surface row **S4 -- satellite holdings, coalesced from BD**; (ii) FWD-6 narrowed to Positioning's own surfaces (Models / ETFs / Satellites toggles; Summary / Holdings / Selection tabs) with Philosophy/CMA carved to a later item on Andrew's ~16:34Z word -- an ENDPOINT byte change, so the CVO half re-signs; (iii) the retag set settled at TWELVE | CTO (L4); CVO + CRO re-sign | PRD at v0.6 |
| 1 | **Deploy the positioning generator** (committed 2026-09-11, running bytes 2026-08-18): CTO + COO never-widen halves with the writer census printed (N >= 3), Terraform, then read the served `positioning_data.json` for the five-class keys | CTO + COO | approved 2026-09-13 conditional; no half drafted |
| 2 | **Round 5, one issuance**: AT5-s-1 producer `holdings.json` (R1-R4); AT5-s-2 portal five-class order + colour on the Positioning page's 14 files (`HoldingsTab.tsx:1392` order literal, `:215` colour map, `:1381-1383` Hedge-to-Equity fold; `PositioningSummary.tsx:545-546`; `src/lib/chartColors.ts` pink + a minted gold token; `PositioningAllocation` widened to five keys) -- `SelectionTab.tsx:321` and `holdings-shared.tsx` are ATTRIBUTION files at the pin and receive only a one-line no-regression guard (the breakdown's F4); AT5-s-3 `satelliteAdapter.ts` reads the coalesced holdings; AT5-s-4 BD seeder patch applied, then the 12-ticker retag in BOTH stores (`TO-T6-1` recut) and `is_hedge` (`TO-T7-1`); AT5-s-5 the bars exercised on the local build against the nine real satellites | COO cuts; workers | FWD-4 / FWD-6 measured, unserved |
| 3 | Portal promote on Andrew's word (the freeze); bars re-graded on PROD; L10 | Andrew; CTO | frozen |

Sequencing that is load-bearing: the retag (2/s-4) lands only after the deploy (1) and after s-2/s-3 are
built -- a retag into a two-class frontend hides the row while its weight stays in the total (the Cash
defect of v2.1.167). The producer (s-1) can be built and exercised against the LIVE table before the
retag; it will simply show GLD under `hedge` until the retag flips it, which is itself a useful before/after.

## 5. THE BARS THIS PLAN CAN ACTUALLY MEET, on the Positioning page

- **FWD-1 / FWD-2**: on the local build, Sat 15 shows a Commodities bucket of 8.34% and Sat 80 shows
  VXX under Structured; class subtotals sum to the grand total on every satellite; served rows = DOM rows.
- **FWD-3 / FWD-4**: one order and one colour across the Positioning page's readers (`HoldingsTab`,
  `PositioningSummary`, both adapters), all of which bind through `src/lib/chartColors.ts`. The round-4 census's
  other readers, `holdings-shared.tsx` among them, are Attribution and out of scope beyond the F4 guard.
- **FWD-5**: change one boundary in the table (e.g. PDBC hedge -> Commodities) and read it flow through
  the served `holdings.json` and the page with no portal edit.
- **FWD-6 (narrowed)**: Models, ETFs and Satellites toggles and the three tabs agree on the five classes,
  their order and colours. Philosophy/CMA: Yang's sheet, later, not this project.

## 6. CARDS FOR ANDREW (decisions only; each carries this seat's recommendation)

1. **The source rule** (R1/R2): Satellites = Black Diamond as-traded; Models = Yang; disagreements
   disclosed, never summed. *Rec: yes -- it is the only rule under which the satellite column is true.*
2. **FWD-6 narrowed** to the Positioning page (ENDPOINT edit, CVO re-sign). *Rec: yes, per his word.*
3. **The gold colour**: no gold token exists; amber is already Cash on 6 of 11 readers. *Rec: mint a
   new token; do not repurpose amber.*
4. **QBER and PDBC** membership at the class edges (12 candidates; these two are judgment calls).
   *Rec: PDBC -> Commodities; QBER -> Structured.*
5. **Benchmark policy** for the three new classes in the models delta / spread rows (today: policy
   weight 0, so a 10% position reads as a 10% bet). *Rec: explicit zero with the row labelled "no
   benchmark", never a silent zero.*
6. **Add GLD and VXX to the Bloomberg daily pull** (characteristics; no backfill). *Rec: today.*
7. **Relaunch COO~Z and CVO~Z** so 0a-0c can run.
8. **Promote** when step 2 is built and exercised.

## 7. WHAT THIS BRIEF DOES NOT DO

It cuts no cell, amends no PRD, signs nothing and deploys nothing. It changes no L4-R signature. The L4
act is the CTO's; the L5/L6 cut is the COO's; the promote and the freeze are Andrew's.

**Vintages:** rebalancer bronze 2026-09-14 (81 files); registry `as_of 2026-09-14`; served models
`data_as_of 2026-09-11`; DynamoDB `etf-classifications` 285 rows, last write 2026-08-25; portal gitlink
`e85f6eb84f`; positioning lambda `LastModified 2026-08-18T18:34:43Z`; PRD v0.6 @ae66157381.

---

## 8. ALIGNMENT NOTES ON THE CTO BREAKDOWN @a35baa02ea (v0.2, before Andrew aligns)

Read in full. The breakdown carries R1-R4 and the eight cards faithfully; its s.3 eight cells are the
cell-level authority from here and supersede s.4 step 2 above. Six notes, each with a recommendation;
AGREE where nothing needs to change.

**A1 -- AGREE:** cells B1-B3 / F1-F4 / R1, the sequencing (R1 strictly last), F4 as a no-regression
guard on Attribution, and card 6 (cut `is_hedge()`, no live caller; cut the `bd-securities`
reconciliation, it changes nothing the Positioning page shows).

**N1 -- FLAG, B1 widens the approved deploy.** Andrew's 2026-09-13 approval (card 5, LD-0562) covered
*the committed repairs* to `yang-generate-positioning`. B1 as written adds a NEW code change to a
SECOND function -- `yang-generate-allocation-summary` (`BENCHMARK_ALLOCATIONS`; `LastModified
2026-08-04`; writes `allocation_summary.json`, a different served artifact). *Rec:* split into **B1a**
(the approved deploy: one function, one artifact) and **B1b** (the labelled-zero benchmark rows: new
code, its own never-widen half naming `allocation_summary.json` and the delta/spread rows), or have the
one sign-off name BOTH functions and BOTH artifacts explicitly. An approved act that grows silently is
the exact shape the NEVER#1 sign-off rule is written against.

**N2 -- FLAG, B2's write surface includes Terraform, measured.** The producer role
(`infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf`) holds `s3:GetObject` on the two
bronze prefixes and `s3:PutObject` on exactly `platinum/satellites/registry.json` -- no DynamoDB action,
no read on `opal-data-portal-v2`. So B2 needs a second pinned `PutObject` key (`holdings.json`) and a
DynamoDB read on `etf-classifications`, both in that `.tf`. *Rec:* compute `weight_models_blend` and
`overlay` in the ADAPTER (F3), which already holds the models payload -- then the producer needs no
cross-bucket read and no new bucket grant, and `holdings.json` carries one plane only (BD facts + labels).
Keep the per-ticker sleeve breakdown (`sleeves:[{book, weight}]`) in `holdings.json`; it is what makes
"coalesced" legible (GLD in Sat 30 = ST 6.26 + INT 1.00).

**N3 -- FLAG, F3's cell text must carry R4 explicitly.** `holdings.json` carries weights and labels,
not characteristics. Fee / yield / duration / beta / returns are carried per ticker from the models
payload's `current_holdings` where any Yang book holds the ticker, NULL otherwise, with the (A) measure
blends over books kept as the satellite-level fallback. A worker reading only "reads `holdings.json`"
ships a satellites column with no fee or yield. Also: the satellite's `data_as_of` becomes the BD
partition date (`holdings.json as_of`), not the models payload's -- today's adapter inherits the models
vintage, which would stamp 09-11 on 09-14 holdings.

**N4 -- FLAG, R1's FWD-5 fixture.** The breakdown proves FWD-5 with a PDBC boundary flip; PDBC is one
of the two L5 judgment calls (C-MEMBERSHIP-AT-L5; CVO `C-S53`), so the flip and the ruling would be one
act. *Rec:* grade FWD-5 on the retag itself -- twelve rows changed in the one place, every Positioning
mode reflecting it with no portal edit -- and drop the extra flip.

**N5 -- AGREE with a note, card 2 / F4.** Andrew's word was "solely around the Positioning page"; F4
touches three Attribution files as a guard, not a feature, and it is carded rather than assumed. Right.

**N6 -- NOTE, card 8.** The Bloomberg pull edit lands on the BBG box's working tree (an edit there is a
deploy); the owner is `0.0.3_BG_BBGTerminal`, live now. Name the recipient on the card so a "yes" has
somewhere to go the same hour.
