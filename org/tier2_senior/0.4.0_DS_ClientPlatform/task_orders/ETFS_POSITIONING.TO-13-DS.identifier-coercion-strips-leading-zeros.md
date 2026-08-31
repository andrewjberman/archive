# TO ETFS_POSITIONING.TO-13-DS — STOP THE UPSTREAM COERCION STRIPPING LEADING ZEROS OFF CUSIPs

<id>ETFS_POSITIONING.TO-13-DS.identifier-coercion-strips-leading-zeros</id>
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md -- cells ETFS-a-1, ETFS-a-5, ETFS-d-1</decomp_ref>
⛔ **THE FIRST CUT OF THIS FACE CLAIMED "NO CELL CLAIMED -- NO HONEST CELL REFERENCE EXISTS" AND THAT WAS FALSE. Corrected by the issuer before the face landed; recorded because the reasoning was plausible and wrong.** I reasoned that a 2026-08-21 round-1 decomp could not cover a defect measured on 2026-08-29, copied the disclosure pattern from `ETFS_INGEST.TO-9-DS`, and never opened the decomp. **`safe-commit` refused the commit and its refusal text said the thing I needed to hear: *"If no decomp exists yet, that is a PIPELINE FAILURE TO SURFACE to COO/CTO, not a reason to cut the TO without one."* I had asserted the antecedent without checking it.**
⭐ **THE CELLS ARE REAL AND THEY ARE EXACT.** `ETFS-a-1` IS `silver/holdings/{date}.parquet` — *"the WEIGHTS, already ours"*, DS-class — **which is the very artifact carrying `cusip=2824100`.** `ETFS-a-5` is `bbg/{date}/`, the L1 landing prefix whose `history_topup` lost the ABT row. `ETFS-d-1` is the producer, *"BUILT against the bbg/{date}/ CONTRACT"* (DECOMP §3.1), which is what emits the served gold. **A cell names an OPERATIVE SURFACE, not a date — an eight-day-old decomp covers a defect found today whenever the defect lives on a surface it enumerated.** That is what I got wrong, and it is the general form.
⚠ **A DECOMP-REF ARMS ALIGNMENT ENFORCE in `proof-of-spec-check.py:24,161`. THAT IS CORRECT HERE AND IS WHY `ETFS_INGEST.TO-9-DS` IS NOT A PRECEDENT FOR THIS FACE:** that TO had genuinely no cell, so its element was absent by necessity and its enforcement would have been vacuous. **This face has three real cells, so enforcement is a feature.** ⛔ **NEVER fabricate `cell_refs` to satisfy the gate — that yields a VALID-READING INSTANCE THAT LIES. The remedy for a missing cell is to SURFACE the pipeline gap, never to invent a reference or to reach for the override.**

<issued_to>`0.4.0_DS_ClientPlatform~Y`</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-29T12:4xZ</issued>
<status>active -- ⛔ **THE BARE TOKEN `active` NOW LEADS THIS FIELD.** It opened with `⛔`, which `to-check.py:191` splits to that symbol, matches no state set, and falls through to `return "ACTIVE"` at :202 -- **[ACTIVE] BY DEFAULT, NOT BY DECLARATION.** Corrected 2026-08-29 ~17:4xZ by `2.0.0_SA_COO~Z` (issuer) off a 55-face census. The state is unchanged and correct: live work gated on tonight's 22:00Z `etfs-netassets-daily` fire, re-verified ENABLED at `cron(0 22 * * ? *)` with a negative control. ⛔ **DO NOT CARRY `TO-14-AE`'s "AC1 + AC2 PASS" ONTO THIS FACE. THE TWO FACES NUMBER THEIR CRITERIA IDENTICALLY AND THE CLAIMS ARE DIFFERENT.** Flagged by `0.4.0_DS_ClientPlatform~Y`, who measured both limbs rather than reading either face. `POS-TO14-AC1/AC2` are about THE APPLY LANDING -- deployed via safe-apply, deployed bytes carry the repair -- and they PASS. `POS-TO13-AC1..AC4` are about THE SERVED ARTIFACT CARRYING THE REPAIRED IDENTIFIER and they are ALL FOUR STILL UNCOMPUTABLE. **A reader taking "AC1 + AC2 PASS" across the two faces closes THIS TO on evidence that does not touch it.** ***** WHY AC1 CANNOT BE SCORED YET, MEASURED 2026-08-29 ~15:1xZ: the deploy landed at 14:17:24Z (CodeSha256 6RFz1jbz... -> rznYiHb5PiktdT/V7Ayls0djByQdvuJ9nQeVQsIS2gI=) but THE NEWEST silver/holdings PARTITION IS STILL 2026-08-28.parquet, WRITTEN 2026-08-28T22:00:16Z -- WHICH PREDATES THE DEPLOY. `silver/holdings/{next}.parquet` DOES NOT EXIST YET, so AC1 -- whose own text says SCORE BY READING THE ROW, NOT THE WRITER'S LOG -- has no row to read. AC2's "still carry non-null returns AFTER THE CHANGE" limb likewise has no post-change artifact. ***** THE FIRST PARTITION THAT CAN SCORE AC1 IS TONIGHT'S 22:00Z `etfs-netassets-daily` FIRE (silver/holdings/2026-08-29.parquet). AC3/AC4 ride further out -- see the trading-calendar note below: the gold producer refuses weekend silver, so AC4 cannot close before 2026-09-01T13:00Z. ***** ⭐ **EXPECT BLOCK FOR THE 22:00Z FIRE -- WRITTEN 2026-08-29 ~18:2xZ BY `0.4.0_DS_ClientPlatform~Y`, BEFORE THE ARTIFACT EXISTS. EVERY VALUE BELOW IS A PREDICTION, NOT AN OBSERVATION.** Placed on the FACE at `2.0.0_SA_COO~Z`'s ask (msg 16899) so AC1/AC2 can be scored by ANY seat after 22:00Z **without this session surviving and without reading anyone's session log** -- a session is not a scheduled resource. ⛔ **NOTHING HERE IS PRE-SCORED.** Its evidential value comes from being fixed BEFORE the partition exists: expected values written in advance cannot have been fitted to the artifact. **OPEN:** `s3://opal-data-etfs/silver/holdings/2026-08-29.parquet`. ⭐ **CHECK COLUMN PRESENCE FIRST, BEFORE ANY VALUE -- IT IS THE STRONGEST AND CHEAPEST DISCRIMINATOR:** the partition MUST carry two NEW columns, `cusip_as_delivered` and `cusip_basis`. **If either is ABSENT, the repaired code did NOT write this partition** -- that is a deploy/trigger problem, not a data problem, and it is diagnosable without reading a single identifier. **THE ROW (`fund_ticker=DIVZ`, `holding_ticker=ABT`):** `cusip` = **`002824100`** (nine chars), `cusip_as_delivered` = **`2824100`** (the vendor's bytes, preserved), `cusip_basis` = **`zero-pad-restored`**, `id_kind` = **`cusip`** (it reads `unclassified` in every partition through 08-28). **THE TWO CONTROLS THAT MUST SURVIVE UNCHANGED -- AC2 EXISTS FOR THEM:** `IDVZ/ICT` `cusip`=`6455819` and `IDVZ/MER` `cusip`=`B247XZ6`, **both still 7-char, both `cusip_basis`=`as-delivered`, both `id_kind`=`unclassified`.** A partition where either moved has broken AC2 and the fix must be reverted, not tuned. **THE 8-CHAR BUCKET SHOULD VANISH ENTIRELY:** `AEP 25537101`, `AIG 26874784`, `ATO 49560105`, `BP 55622104` all become 9-char (`0`+value) with `cusip_basis`=`zero-pad-restored`. **LENGTH HISTOGRAM, if the partition is still 187 rows:** `{7:3, 8:4, 9:177, 10:2, 12:1}` -> **`{7:2, 9:182, 10:2, 12:1}`** -- the 7-bucket drops 3->2, **the 8-bucket drops to ZERO**, 9 gains 5. `cusip_basis` distribution: **5 `zero-pad-restored`, 182 `as-delivered`.** ⚠ **WHAT MAY LEGITIMATELY VARY, SO A RE-SCORER DOES NOT FALSE-ALARM: the ROW COUNT.** 187 is today's; holdings change and the counts above scale with it. **Score the BUCKET SHAPE and the NAMED ROWS, never the totals.** ⚠ **AND 2026-08-29 IS A SATURDAY** -- the sheet may carry Friday's holdings, or may not advance at all. That affects WHICH day's positions appear; it does NOT affect the identifier repair, which is applied at parse to whatever rows arrive. ⚠ **ONE BENIGN OUTCOME THAT MUST NOT BE READ AS FAILURE: if the VENDOR fixes their sheet**, ABT arrives as `002824100` already and `cusip_basis` reads **`as-delivered`** rather than `zero-pad-restored`. **AC1 is still SATISFIED** -- it requires a 9-char stored cusip, not a particular repair path -- and `cusip_as_delivered` would then read `002824100` too, which is the tell. ⛔ **WHAT WOULD BE A REAL FAILURE:** ABT still 7-char; ICT or MER moved; the new columns absent; or any `cusip_basis` value outside {`as-delivered`, `zero-pad-restored`}. ⛔ **AC3/AC4 ARE NOT SCORABLE FROM THIS PARTITION AT ALL** -- they need `gold/holding/date={d}/holding.parquet` from a SCHEDULED gold fire, which the trading calendar puts at 2026-09-01T13:00Z. **Do not score them off silver.** ***** ⭐ **EXPECT BLOCK FOR AC3/AC4 -- THE GOLD LEG. WRITTEN 2026-08-29 ~18:3xZ BY `0.4.0_DS_ClientPlatform~Y`, ALSO BEFORE THE ARTIFACT EXISTS; EVERY VALUE IS A PREDICTION.** Added for the same reason as the silver block and MORE so: AC3/AC4 ride 2026-09-01, three days out, and no session survives that. **OPEN:** `s3://opal-data-etfs/gold/holding/date=2026-08-31/holding.parquet`. ⛔ **WHY 08-31 AND NOT 08-29 OR 09-01 -- THE MECHANISM, READ AT SOURCE, BECAUSE THE OBVIOUS ANSWER IS WRONG:** `etf_positioning_gold.py resolve_as_of` does **NOT** key the partition on the calendar frontier. It selects **the newest silver/holdings partition THAT IS A TRADING DAY**, and its own comment says why: *"The upstream netassets producer fires on a FLAT DAILY cron (0 22 * * ? *), so it writes SATURDAY AND SUNDAY partitions that re-stamp Friday's closing data. Selecting one as the as-of would key a trading-day artifact to a non-trading day."* **So tonight's `silver/holdings/2026-08-29.parquet` (Saturday) is REFUSED as an as-of, gold stays pinned at 2026-08-28, and it cannot advance until MONDAY 2026-08-31's 22:00Z silver lands.** The 2026-09-01T13:00Z gold fire then selects `as_of=2026-08-31`. ⚠ **`tcal.expected_last_trading_day(2026-09-01T13:00Z)` returns `2026-09-01`, and that number is NOT the partition name** -- the function is DATE-ONLY (`_to_date(now)` discards the time) and feeds the `behind` staleness metric, not the key. **A seat reading the frontier and expecting `date=2026-09-01/` will look in a prefix that does not exist.** **AC3 -- THE ROW:** `ticker=ABT`, `book=DIVZ` carries **8 of 8 NON-NULL** return windows (`return_1D, return_WTD, return_MTD, return_1M, return_QTD, return_1Q, return_YTD, return_1Y`). It reads **0 of 8** in every gold partition through 08-27. **AC3 -- THE POPULATION, AND SCORE IT BY NAME NOT BY COUNT:** the 0-of-8 set must be exactly **FIVE NAMED ROWS -- `CASH`x4 (DIVZ, IDVZ, PFDE, PFOE) plus `2602335D` (TPG Inc)** -- i.e. today's six minus ABT. ⛔ **DO NOT SCORE "five of 189".** 189 is the 08-27 row count and 08-28 silver already carries 187; **the total moves with the holdings and a checker pinned to it false-alarms on an ordinary composition change.** Print the day's observed total BESIDE the count; compare the NAMED SET, never the denominator. ⛔ **`2602335D` MUST REMAIN NULL** -- a zero-weight CVR with a numeric Bloomberg ticker and no `PX_LAST`, explicitly out of scope per AC3. **A run that also "fixes" it has gone outside this TO.** **AC4 -- THE FIRE MUST BE SCHEDULED:** name it by DATE (2026-09-01T13:00Z, `etf-positioning-producer-daily`). An ad-hoc QA run is legitimate for testing and **is not the acceptance**; the feeding silver row carries `run_class` (`scheduled` | `replay-from-bronze`) and that is the field which distinguishes them. ⚠ **WHAT MAY LEGITIMATELY VARY:** the total row count, and WHICH day's holdings the vendor sheet carried over the weekend. **Neither affects whether ABT's returns resolved.** ⛔ **WHAT WOULD BE A REAL FAILURE:** ABT still 0-of-8; the 0-of-8 set containing any row outside the five named; `2602335D` non-null; or the partition produced by an ad-hoc rather than the scheduled fire. ***** ⭐ **POST-FIRE ADDENDUM, WRITTEN 2026-08-29 ~22:1xZ AFTER AC1 PASSED -- TWO FALSE-ANOMALY TRAPS ON THE DATE FIELDS THAT THE PRE-FIRE BLOCKS DID NOT NAME.** Added because a Monday re-scorer meets both and neither is a defect. **(1) THE CONTENT IS FORWARD-DATED AND THAT IS DESIGN, NOT DRIFT.** Measured on `silver/holdings/2026-08-29.parquet`: `run_date=2026-08-29` but `date=2026-08-31` and `data_as_of=2026-08-31`, **uniform 187/187**. `infra/aws/terraform/etfs-netassets/netassets-lambda.tf:200` states the intent verbatim -- the lambda *"Runs EVERY day, not weekdays-only -- deliberately... Pathfinder uses a T+1 effective-dating convention: ON A WEEKEND RUN THE HOLDINGS FILE IS STAMPED WITH THE NEXT BUSINESS DAY. The row records what the issuer served and stamps its vintage; it does not pretend a weekend produced new data."* ⛔ **AND THE OBVIOUS REMEDY IS ALREADY RETRACTED AT CTO LEVEL -- THE SAME COMMENT SAYS SO:** *"A `data_as_of <= run_date` GUARD HERE WOULD BLOCK THE PATHFINDER CHANNEL EVERY WEEKEND -- CTO PROPOSED AND THEN RETRACTED EXACTLY THAT. DO NOT ADD IT."* **A seat filing this as an anomaly would have its natural fix silently kill a vendor channel every Saturday and Sunday.** **(2) ⛔ THE GOLD PRODUCER JUDGES THE PARTITION *KEY*, NOT THE CONTENT DATE -- AND THE TWO DISAGREE BY DESIGN THIS WEEKEND.** `silver/holdings/2026-08-29.parquet` CONTAINS `date=2026-08-31`, a trading day. **That does NOT make gold advance.** `resolve_as_of` lists silver PARTITIONS and refuses one whose KEY is a non-trading day; the key here is `2026-08-29`, a Saturday. **So a seat reasoning "the content says 08-31, so the gold fire can use it" reaches the wrong conclusion from a true reading.** Confirmed post-fire: `gold/holding` newest is still `date=2026-08-28` (written 2026-08-29T13:01:22Z) **after** tonight's silver landed. The gold leg still waits on MONDAY 2026-08-31's silver partition, exactly as the AC3/AC4 block above says. ⭐ **AND ONE AC4-RELEVANT FACT THE BLOCKS DID NOT CLAIM: the artifact ASSERTS ITS OWN RUN CLASS.** `run_class='scheduled'` on **187 of 187** rows -- a per-row field, strictly stronger than inferring "scheduled" from the 22:00:14-17Z landing band. **Score AC4 on that column, not on a timestamp.** ***** ⛔⛔ **AND THE MOST IMPORTANT THING FOR THE 09-01 SCORER: THERE IS A SECOND WAY ABT CAN READ NULL IN GOLD, AND IT IS NOT THIS TO'S BUSINESS.** Surfaced by `0.7.0_AE_CloudOps~N`, **verified at source here rather than relayed.** `etf_positioning_gold.py:354` sets `SILVER_AS_OF_COLUMN = "data_as_of"` -- so the producer ALSO reads the as-of from ROW CONTENT for per-fund resolution, and `:626-640` shows what happens when a fund has no rows at the global selection key: it steps back to that fund's own most recent partition, and a fund with rows in NO candidate partition *"render[s] as labelled shells with a NULL date"*. >> **SO A NULL RETURN WINDOW HAS TWO CAUSES: NULL-BECAUSE-UNREPAIRED (this TO's defect) and NULL-BECAUSE-SHELL (a per-fund as-of resolution failure, nothing to do with identifiers).** << ⭐ **BUT THEY ARE DISTINGUISHABLE IN ONE READ, AND THE DISCRIMINATOR IS THE GRAIN: THE SHELL PATH IS PER-FUND, NOT PER-HOLDING.** `:626-640` iterates fund CODES, so a shell nulls the WHOLE BOOK: ```  ABT null AND its DIVZ siblings carry returns   -> NOT a shell. The IDENTIFIER path. THIS TO's business.  ABT null AND the WHOLE OF DIVZ is null, date NULL -> SHELL. A per-fund as-of failure. NOT this TO.``` **Check the fund before the holding.** ⛔ **AND DO NOT SCORE A FAIL WITHOUT THAT CHECK** -- misattributing a shell to the identifier repair would reopen a closed defect and send a seat back into `bbg_security` for a fault that lives in as-of resolution. ⚠ **ONE MORE COINCIDENCE TRAP ON THE SAME DATE, and it is the shape that has recurred all evening:** `2026-08-31` appears tonight for **THREE INDEPENDENT REASONS** -- (a) tonight's `data_as_of`, via Pathfinder's T+1 weekend forward-dating; (b) AC3/AC4's target partition, being the first repaired TRADING-DAY silver KEY; (c) simply the next trading day after this weekend. **A scorer who reads (a) and concludes (b) has confirmed NOTHING, and the agreement will feel like corroboration.** The gold selection is by KEY (`_list_silver_partitions` derives the date from the filename stem; `:323` and `:543` -- *"as_of is a SELECTION KEY and is NEVER a provenance stamp"*), so **only Monday's silver KEY 08-31 can produce `gold/holding/date=2026-08-31/` -- tonight's content stamp cannot, however much it matches.** ***** AND THE ISSUER CONTRIBUTED TO THIS RISK: `2.0.0_SA_COO~Z` wrote BOTH faces and used the bare shorthand "AC1 + AC2 PASS" about TO-14-AE in its own reports. The criterion IDs are distinct (`POS-TO13-` vs `POS-TO14-`) and the SHORTHAND is not. **Quote the full criterion id or the face name; never the bare AC number across two faces of one project.** code-complete -- ⛔ **THE BARE STATE TOKEN LEADS THIS FIELD AND CARRIES NO MARKDOWN: `to-check.py:189-202` splits on the first whitespace/hyphen and a leading `**` yields `**code-complete`, which falls through to the ACTIVE default. Measured the hard way on `ETFS_INGEST.TO-9-DS` today.** **CODE COMPLETE 2026-08-29 ~13:3xZ at `353c4b5a00`; proof-of-spec instance VALID (rc=0, violations=0, alignment forward 4/4 and 3/3, backward 3/3) at `406ca98415`; comp-system discharged in-session at `1d7d5706ee`. ALL THREE LOCAL** -- `git branch -r --contains 353c4b5a00` returns EMPTY and origin/SITEZ is `e998abbfa6`. ⛔ **ALL FOUR ACs ARE FILED UNCOMPUTABLE AND THAT IS THE HONEST SHAPE, NOT A SHORTFALL.** AC1 says IN ITS OWN TEXT "score by reading the row, not the writer's log" and the executor exercised the writer's logic -- which IS the writer's log. AC2's "still resolve" limb is measured at the query plane and a PASS would let the unmeasured limb inherit the verdict. AC3 and AC4 need a SCHEDULED fire after the fix lands and there is no date to name. **Four PASS rows would have read as a completed TO; this TO's own proof_of_spec comment warns that a placeholder row passes the checker.** ⛔⛔ **AND SECTION 5'S PREMISE IS WRONG -- THE ISSUER'S ERROR, CORRECTED HERE RATHER THAN IN THE BODY WHERE `to-check` WOULD NOT RENDER IT.** Section 5 says "fix the numeric coercion ... BEFORE it reaches silver/holdings". **THERE IS NO COERCION OF OURS TO FIX.** Measured on the raw vendor bytes (`s3://opal-data-assets/trueshares/DIVZ/bronze/holdings/20260828/divz_holdings.csv`, written byte-for-byte BEFORE any parse): bronze ALREADY carries `2824100`, and both parsers in the producing Lambda read that column as text and only `.strip()` it. **THE COERCION IS THE TRUESHARES GOOGLE SHEET exporting an unformatted identifier cell as a NUMBER.** Section 5's CONCLUSION survives intact -- repair at source is still the only sound fix -- but "source" is OUR SILVER BOUNDARY, not a coercion site of ours. ⭐ Finding the bronze at all required the APPLIED state: the module's DEFAULTS say `BRONZE_BUCKET=S3_BUCKET` / `GRAMMAR=legacy`, the DEPLOYED environment says `opal-data-assets` / `monolith`. **Reading the code would have sent the executor to a prefix that returns nothing** -- a clean zero from the wrong place. ⛔ **THE DEPLOY IS BLOCKED ON A LANE, NOT ON EFFORT, AND THE ISSUER HAS MADE THE STAFFING CALL: `ETFS_POSITIONING.TO-14-AE` IS CUT FOR THE APPLY**, mirroring the `ETFS_INGEST.TO-9-DS` / `TO-10-AE` split this project already uses. Lambda code deploy is Terraform-only (CLAUDE.md NEVER) and infra is DT/AE (Rule 13). `0.4.0_DS_ClientPlatform~Y` correctly declined to pick a seat rather than doing the issuer's staffing. ⚠ **THE FIX DOES NOT SHIP ALONE AND THE DEPLOYER MUST KNOW IT: the deployed function is ALREADY BEHIND the repo INDEPENDENTLY of this change** -- deployed `lambda_function.py` 69,897 B, CodeSha256 `6RFz1jbzLMXXoWOmEkjIe3JoEZAf7EaHpQ4CsZXzuK8=`, LastModified 2026-08-25T00:09:54Z, against 72,296 B in the repo BEFORE this edit. The pending delta is the **Z-S31 `RunDateFabricationGuard`** from a `1.0.0_SA_CTO~Z` ruling, authored by ANOTHER SEAT and unrelated to identifiers. **A DEPLOY OF THIS FIX CARRIES IT.** Divergence confirmed REAL, not the CRLF false-divergence class: CR count 0 in BOTH files. ✅ **RESIDUAL, RECORDED IN THE FUNCTION'S OWN DOCSTRING SO IT IS NOT REDISCOVERED:** this repairs the UNAMBIGUOUS cases and DOES NOT CLOSE THE CLASS -- ~1 in 10 future doubly-stripped CUSIPs will be SEDOL-valid, be refused repair, and silently retain the ABT failure. Safe direction; better everywhere, worse nowhere. `/sedol/2824100` remains UNEXERCISED and no vendor call was made. -- ORIGINAL STATUS BELOW, PRESERVED -- **PENDING — CUT WITH THE DEFECT FULLY CHARACTERIZED AND ONE LINK DELIBERATELY UNEXERCISED.** The finding, the mechanism, the blast radius and both rival explanations are all MEASURED and recorded in `org/projects/ETFS_POSITIONING.json` `blocking` (the NAMED PRIMARY CARRIER; commits `9ebcd31a3a`, `6bac9a3680`, `dc57db85c5`, `0d5f5a8e2e`). ⛔ **WHAT IS NOT MEASURED AND MUST NOT BE MEASURED BY THIS FACE: `/sedol/2824100` has NOT been run against Bloomberg. That is a VENDOR CALL and needs Andrew's explicit per-use word, which nobody has asked for and which this TO does NOT request — the scheduled pull exercises it for free.** So "the sedol query returns nothing for ABT" is **STRONGLY EVIDENCED AND UNEXERCISED**, and is deliberately NOT called a root cause under Rule 22. ⚠ **A SEAT PICKING THIS UP MUST NOT UPGRADE THAT LANGUAGE WITHOUT EITHER THE SOVEREIGN WORD OR A SCHEDULED-RUN OBSERVATION.**</status>
<priority>P2 — a real served defect on a real position, bounded to one holding by enumeration, and not urgent enough to spend a vendor call on. **It is wrong-valued, not wrong-looking** (contrast `ETFS_INGEST.TO-9-DS`), which is why it is not P3; it is one row of 187, which is why it is not P1.</priority>

<authority>
No sovereign word. Cut by `2.0.0_SA_COO~Z` under the **D1+D4 scoped `/drive` arm** (Andrew-direct
2026-08-28 ~02:3xZ at the COO~Z terminal, VERBATIM: *"you just need to keep the fabric discipined
and proceed through D1 and D4 TO completion. No distractions, pure execution, if there are issues
they go to surprise-channel and CVO investigates."*).

⚠ **THIS IS AN ISSUE THAT WENT TO INVESTIGATION AND CAME BACK RESOLVED**, which is the arm working
as written: `3.0.0_SA_CVO~Z` and `0.4.0_DS_ClientPlatform~Z` characterized it across msgs 16710 /
16712 / 16715 / 16718 / 16721 / 16723 / 16726 / 16728 / 16744, **both correctly declined the remedy
under Rule 27**, and handed it to whoever holds `ETFS_POSITIONING`. This face is that hand-off
landing. **Neither of those lanes carries this further.**
</authority>

## 0. SEATING -- SEATED 2026-08-29 ~12:5xZ ON `0.4.0_DS_ClientPlatform~Y`

✅ **SEATED 2026-08-29 ~12:5xZ ON `0.4.0_DS_ClientPlatform~Y` by `2.0.0_SA_COO~Z`** (issuer; COO spawn/seat authority per Andrew 2026-08-28 15:32Z). **PRE-FLIGHT, ALL FIVE GATES, EACH WITH ITS DENOMINATOR OR CONTROL:**

```
  1pt process truth   8 claude.exe live, ALL ~Z base lanes -- no ~Y process
                      (and no ~Q, no ~I: independent corroboration that both are DEAD)
  1a  broker          ~Y reads NOT REGISTERED   (control: ~Z present in the same dump)
  1b  marker scan     0 hit(s) for ~Y           (POSITIVE CONTROL: ~Z = 1 hit, so not blind)
  1c  concurrency     7 of 16 spawn-marker windows
  1d  encumbrance     0 open TOs . 0 surprise_channel ownership rows . 0 project/mission
                      owner rows . 0 mentions anywhere in org/ outside inboxes
```

⭐ **1d WAS NOT A FORMALITY — IT REFUSED THE FIRST TWO CANDIDATES.** `~R` holds `ADVI_INSURE.TO-R1-DS` (PENDING, 4d) and `~S` holds one too: **both would have been Rule 27 collisions on a letter that is free on every process-plane instrument.** `~V` was clean on obligations but is NAMED IN AN OPEN CARD AT ANDREW (its `FACE_FLIP_CHECK_SPEC_20260826.md`), so it was passed over for conflation risk rather than for encumbrance — a weaker reason, recorded as such.

⚠ **THIS WORK IS FIRE-INDEPENDENT.** Unlike the two `ETFS_INGEST` faces it does **not** wait on the 13:00Z `etf-positioning-producer-daily` run — the defect is already measured and the fix is in code. It was seated ahead of them for exactly that reason.

⛔ **HISTORICAL, KEPT BECAUSE IT IS THE LESSON, NOT THE STATE — THE FIELD IS SERIAL-FREE WHEN UNSEATED, AND MINE WAS NOT.** The seating note originally lived inside `<issued_to>`; `to-check` renders the FIRST serial-shaped token it finds there, so the face rendered **`-> SA_COO~Z`** — the issuer, as executor. **A face that renders the COO as its own assignee is a lane violation on its face, and it is WORSE than one rendering `(unassigned)`**, because `(unassigned)` announces itself and a plausible-but-wrong serial does not. Same class as `ETFS_INGEST.TO-7` carrying an executor CLASS and no instance for three days while every other field looked complete. **Prose about seats goes in a SECTION; only the assignee goes in the field.**

⛔ **THE LANES THAT COULD NOT TAKE THIS, measured at seating time:**

```
  0.4.0_DS_ClientPlatform~Z   holds D1_CATVIEWS TO-M1-DS + TO-N1-DS      LIVE, encumbered
  0.7.0_AE_CloudOps~Z         holds D1_CATVIEWS TO-P1-AE                 LIVE, encumbered
  0.4.0_DS_ClientPlatform~Q   holds ETFS_INGEST.TO-9-DS                  DEAD (INFERRED), encumbered
  0.7.0_AE_CloudOps~I         holds ETFS_INGEST.TO-10-AE                 DEAD (INFERRED), encumbered
```

**One instance is one project, which is why a fresh lane was required rather than a reuse.** The two `ETFS_INGEST` faces are seated separately AFTER the 13:00Z fire, because their criteria need a post-fire artifact to score and seating them earlier would seat on a read that does not exist yet.

⛔ **AND THE FIELD IS SERIAL-FREE ON PURPOSE — THE FIRST VERSION OF IT WAS NOT, AND THAT WAS A
DEFECT THE ISSUER CAUGHT ON ITS OWN FACE.** The seating note originally lived inside `<issued_to>`;
`to-check` renders the FIRST serial-shaped token it finds there, so the face rendered
**`-> SA_COO~Z`** — the issuer, as executor. **A face that renders the COO as its own assignee is a
lane violation on its face, and it is WORSE than one rendering `(unassigned)`**, because
`(unassigned)` announces itself and a plausible-but-wrong serial does not. Same class as
`ETFS_INGEST.TO-7` carrying an executor CLASS and no instance for three days while every other field
looked complete. **Prose about seats goes in a SECTION; only the assignee goes in the field.**

## 1. THE DEFECT, ON THE SERVED PLANE

`gold/holding/date=2026-08-27/holding.parquet` — the newest gold partition (`gold/book/` and
`gold/holding/` both stop at 08-27), 45,692 bytes, size matched against `s3api` before read.

```
  189 rows . 169 distinct ticker . 31 columns
  NON-NULL WINDOW COUNT, DENOMINATOR 189 ROWS -- BIMODAL AND EMPTY BETWEEN:
     8 of 8 non-null : 183 rows
     0 of 8 non-null :   6 rows      NOTHING PARTIAL
```

**Every one of the six, enumerated — this IS the population, not a sample:**

```
  ABT       Abbott Laboratories       DIVZ  w=2.36   is_cash=False  price=114.1
  CASH      Cash & Cash Equivalents   DIVZ  w=0.23   is_cash=True
  CASH      Cash & Cash Equivalents   IDVZ  w=0.53   is_cash=True
  CASH      Cash & Cash Equivalents   PFDE  w=0.03   is_cash=True
  CASH      Cash & Cash Equivalents   PFOE  w=-0.02  is_cash=True
  2602335D  TPG Inc                   PFDE  w=0.00   is_cash=False  price=0.0
```

>> ⛔ **FOUR OF THE SIX ARE CASH AND ONE IS A ZERO-WEIGHT ZERO-PRICE PLACEHOLDER. ABT IS THE ONLY
REAL PRICED HOLDING IN THE ESTATE WITH ALL EIGHT RETURN WINDOWS NULL — 2.36% of DIVZ, priced 114.1.** <<

## 2. THE MECHANISM — MEASURED AT SOURCE, AND THE BUCKET IS STRUCTURALLY AMBIGUOUS

`silver/holdings/2026-08-28.parquet`, 187 rows: **ABT's stored `cusip` is `2824100` — SEVEN
characters. Abbott Laboratories' CUSIP is `002824100`. TWO leading zeros stripped by numeric
coercion upstream.**

`integrations/bloomberg/pipeline/etf_daily_pull.py:96-102` @`6bac9a3680` routes by LENGTH:

```
  len(c) == 9   ->  "/cusip/" + c
  len(c) == 8   ->  "/cusip/0" + c     # pads ONE zero -- "leading zero stripped upstream"
  len(c) == 7   ->  "/sedol/" + c      # <-- ABT LANDS HERE
```

**THE WHOLE 7-CHAR BUCKET, ENUMERATED, DENOMINATOR 187:**

```
  DIVZ  ABT  2824100   digits_only=True    a CUSIP MINUS TWO ZEROS. MIS-ROUTED.
  IDVZ  ICT  6455819   digits_only=True    a GENUINE SEDOL
  IDVZ  MER  B247XZ6   digits_only=False   a GENUINE SEDOL
```

>> ⛔⛔ **THE SAME 2026-08-25 SWITCH TO IDENTIFIER-QUERY ADDED ICT AND MER AND DROPPED ABT, OUT OF
ONE LENGTH BUCKET, BY ONE RULE.** ICT and MER are the function's OWN docstring examples, verified on
the live terminal 2026-08-25 (`/sedol/6455819` -> INTL CONTAINER TERM SVCS px 949; `/sedol/B247XZ6`
-> MANILA ELECTRIC px 479). **The change was RIGHT for two of the three and wrong for the third.** <<

⛔ **`isdigit()` DOES NOT SEPARATE THEM** — ABT `2824100` and ICT `6455819` are both all-digits.
**THERE IS NO PURELY LEXICAL FIX INSIDE THE 7-CHAR BUCKET.** The docstring already calls fixing the
coercion at source *"a separate, better fix"*; this measurement makes it the **only** sound one.

⭐ **AND THE PAD MECHANISM IS NOT BROKEN — the 8-char bucket is four rows and all four are correct:**
`AEP 25537101 . AIG 26874784 . ATO 49560105 . BP 55622104`, each a CUSIP minus ONE zero, each padded
right. **ABT is the SINGLE row in 187 where stripping went one digit further than the pad
anticipates.** Blast radius bounded BY ENUMERATION, not estimate.

## 3. THE DATA WAS CONSTANT; THE CODE MOVED

`silver/holdings/{date}.parquet` cusip LENGTH histogram, denominator per date:

```
  2026-08-21   114 rows   {9:111, 10:2, 12:1}              <- NO 7-char, NO 8-char rows
  2026-08-24   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-25   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-26   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-27   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-28   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
```

**IDENTICAL FROM 08-24 ONWARD. ABT's cusip was 7-char THE DAY IT FIRST APPEARED and was never
9-char — the coercion defect PREDATES the 08-25 change, which merely walked into it.**
**CORROBORATED ON A SECOND PLANE:** ABT HAD a `history_topup` row on 08-24 (return `0.0257`) with the
7-char cusip ALREADY stored. On 08-24 the fetch did not depend on that identifier; on 08-25 it did.

⛔ **BOTH BENIGN EXPLANATIONS ARE DEAD BY MEASUREMENT, and each was hunted deliberately:**
`0.4.0_DS_ClientPlatform~Z` killed *"it was sold"* (ABT present in `constituents_issuer_fill` on
08-24 AND 08-28); `3.0.0_SA_CVO~Z` killed *"it left and returned"* (present on all five dates
08-24..08-28, no interruption). **THE RETURN FETCH STOPPED THE DAY AFTER ABT ENTERED THE PORTFOLIO,
NOT WHEN IT LEFT.**

## 4. ⭐ AND THE CODE PREDICTED THIS EXACT SHAPE, ABOUT A DIFFERENT TICKER

`etf_daily_pull.py:150-153`, on FXFXX: *"Excluding it meant its history NEVER ADVANCED — it renders
returns today only because the FROZEN backfill happens to reach the current as-of, and **IT WOULD
HAVE GONE BLANK THE MOMENT THE FRONTIER MOVED PAST IT.**"*
>> **That is ABT's shape verbatim, written days before ABT exhibited it. The author reasoned the
CLASS correctly while fixing one instance, and the 7-char limb created a NEW INSTANCE OF THE SAME
CLASS IN THE SAME COMMIT.** Read that comment before designing the fix — it is the best statement of
the failure mode in the tree. <<

## 5. THE WORK

**Fix the numeric coercion that strips leading zeros from `cusip` BEFORE it reaches
`silver/holdings/`.** The identifier must arrive as a 9-character CUSIP string.

⛔ **DO NOT "FIX" THIS IN `bbg_security()` BY WIDENING THE LENGTH HEURISTIC.** §2 measures why: a
7-char all-digit value is genuinely ambiguous between a doubly-stripped CUSIP and a real SEDOL, and
ICT is a live counter-example sitting in the same partition. **A heuristic that rescues ABT breaks
ICT.** The `len==8` pad stays as it is — it is correct for all four of its cases and is not in scope
to remove.
⚠ **The 8-char pad becomes DEAD CODE if the coercion is fixed at source. LEAVE IT.** It is a
defence against the same class recurring from a different producer, and removing it is a separate
decision with its own evidence.

## 6. ACCEPTANCE CRITERIA

**AC1 — THE STORED IDENTIFIER IS REPAIRED AT SOURCE.** `silver/holdings/{next}.parquet` carries
`ABT` with a **9-character** `cusip` (`002824100`). Score by reading the row, not the writer's log.
**Print the length histogram with its denominator** — the whole-partition shape is the control, and
the 7-char bucket must drop from 3 rows to 2 (ICT and MER, which are correct and must SURVIVE).

**AC2 — ICT AND MER ARE NOT COLLATERAL DAMAGE.** Both still resolve and both still carry non-null
returns after the change. ⛔ **This criterion exists because the obvious fix breaks them**; a change
that repairs ABT and silently drops a Philippine holding has traded one blank row for another.

**AC3 — THE SERVED ARTIFACT CARRIES ABT'S RETURNS.** In a `gold/holding/date={d}/holding.parquet`
produced by a **SCHEDULED** fire after the fix lands, `ABT` carries **8 of 8** non-null return
windows. **Report the 0-of-8 population with its denominator**, which should then be the four CASH
rows plus `2602335D` — **five, not six.**
⚠ **`2602335D` (TPG Inc, w=0.00, price 0.0) IS NOT IN SCOPE and MUST NOT be "fixed" as part of this.**
It is a zero-weight CVR whose Bloomberg ticker is numeric; per the docstring's RBGLD note that class
has no `PX_LAST` so no history can accrue. **Leave it null and say so.**

**AC4 — THE FIX IS EXERCISED BY A SCHEDULED RUN, NOT AN AD-HOC ONE.** An ad-hoc QA run is legitimate
for testing (CLAUDE.md permits it) but **is not the acceptance**. Name the scheduled fire by DATE.

⚠ **DO NOT SCORE AC1-AC4 AGAINST A WEEKEND FIRE WITHOUT RESOLVING THE TRADING CALENDAR FIRST.**
Today is **Saturday 2026-08-29**. `etf_positioning_gold.py:497` and `:1672` anchor on
`tcal.expected_last_trading_day(now)`, which is a DIFFERENT mechanism from the MDPF content-derived
`derive_as_of()` — **do not carry an MDPF frontier result across that boundary** (`3.0.0_SA_CVO~Z`
fenced exactly this, msg 16732). AFTER == BEFORE on a non-advancing day is the EXPECTED outcome, not
a regression.

## 7. BOUNDS THIS FACE CARRIES RATHER THAN DROPS

- **`/sedol/2824100` is UNEXERCISED** (§`<status>`). Not a root cause under Rule 22.
- **20 of 171 backfill objects were read** for the depth/date-range work, size-rank selected, not a
  census. The two-run conclusion is **STRONG AND SHORT OF A CENSUS**.
- **One gold partition (08-27) was read.** Whether ABT was null in the 08-25/08-26 gold is INFERRED
  from the input timeline, not measured on the output.
- **`3.0.0_SA_CVO~Z`'s first probe printed ABT ABSENT ON EVERY DATE** — it selected the first
  `*tick*` column, which is `fund_ticker` (DIVZ/IDVZ), not `holding_ticker`. **A failed retrieval
  returning a VALUE.** What caught it was a histogram printed for an unrelated reason. **If a probe
  here says ABT is absent, suspect the column before the world.**
- **The `bbg/{date}/constituents/` prefix also holds `derived_*` and a `run_manifest.json`** — a
  whole-prefix sweep into a CSV reader dies on the manifest. The constituent rows are
  `constituents_issuer_fill` ONLY.


<proof_of_spec>
  <!-- ISSUANCE half (2.0.0_SA_COO~Z). POSITIONAL -- no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json POS-TO13-AC1,POS-TO13-AC2,POS-TO13-AC3,POS-TO13-AC4
       CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE (a pipe resets $?).
       Coverage diff is BIDIRECTIONAL -- an extra filed criterion fails as loudly as a missing one.
       ⛔ A PLACEHOLDER ROW PASSES THIS CHECKER: rc=0 VALID has been measured on a criterion that
       never ran. rc=0 means the CONTRACT is well-formed, NOT that the work happened. Score the
       ARTIFACT for each AC, then file.
       CELL MAPPING, and the surfaces are what the cells name:
         AC1/AC2 -> ETFS-a-1  the silver/holdings identifier itself
         AC3     -> ETFS-d-1  the producer emitting the served gold
         AC4     -> ETFS-d-1 + ETFS-a-5   the scheduled fire landing under bbg/{date}/
       ⚠ The cells name OPERATIVE SURFACES. The exact code location of the coercion is NOT fixed by
       this contract and is the executor's to determine -- section 5 bounds what must NOT change. -->
  <criterion id="POS-TO13-AC1" cell_refs="ETFS-a-1"/>
  <criterion id="POS-TO13-AC2" cell_refs="ETFS-a-1"/>
  <criterion id="POS-TO13-AC3" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO13-AC4" cell_refs="ETFS-d-1, ETFS-a-5"/>
  <expected_criteria>POS-TO13-AC1,POS-TO13-AC2,POS-TO13-AC3,POS-TO13-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-13-DS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>


## ⛔ COMPLETION LANGUAGE IS BOUNDED -- THE REPAIR CLOSES ~90% OF THE CLASS, NOT THE CLASS

**Added by the issuer 2026-08-29 ~13:2xZ, BEFORE the face can be closed, because the natural
completion sentence -- "the identifier-coercion defect is fixed" -- would be an over-claim and
nobody would notice.**

`0.4.0_DS_ClientPlatform~Y` built the gate with a SEDOL refusal ahead of the CUSIP repair and
exhibited five values that prove it necessary (`BBB0135 BBB0168 BBB0317 BBB0481 BBB0630` -- valid
SEDOLs whose zero-padding ALSO passes CUSIP mod-10, so a check-digit-only gate would silently
rewrite a real SEDOL into a CUSIP). `3.0.0_SA_CVO~Z` REPRODUCED that on an independently written
implementation of both checksums -- **not by running the gate, which would be repetition rather than
corroboration under Rule 22** -- and agreed 8 of 8.

⭐ **THE PRECEDENCE IS THE LOAD-BEARING PART, not the two checksums.** For ABT/ICT/MER the two
checksums are OPPOSITE-VALUED, so either alone would have sufficed TODAY. On the BBB rows they do
NOT disagree -- both say valid -- **so nothing but the ORDERING (SEDOL-valid REFUSES, ahead of
CUSIP-valid REPAIRING) saves them.** "It works on today's data" was the wrong safety argument and
was correctly not made.

```
  THE QUANTIFIED RESIDUAL (3.0.0_SA_CVO~Z):
    a doubly-stripped CUSIP is 7 all-digit chars; SEDOL validity turns on the 7th char matching
    a weighted sum of the first six, so a random such value is SEDOL-valid ~1 time in 10.
    Vowel exclusion does not help -- an all-digit value has no vowels to exclude.
  => ROUGHLY 1 IN 10 FUTURE DOUBLY-STRIPPED CUSIPS WILL BE SEDOL-VALID, BE REFUSED REPAIR, AND
     SILENTLY RETAIN THE ABT FAILURE -- invisible by EXACTLY the mechanism that made ABT invisible.
  ABT ITSELF IS NOT LUCKY: `2824100` is SEDOL-INVALID, so this instance is unambiguous.
```

✅ **THIS DOES NOT ARGUE AGAINST SHIPPING AND IS NOT A BLOCKER.** The refusal leaves such a value
exactly as today's code leaves it: **the fix is strictly better everywhere and worse nowhere.**
⛔ **IT ARGUES AGAINST ONE THING ONLY -- DESCRIBING THE REPAIR AS CLOSING THE CLASS.** When this face
is closed, the completion sentence must say it repairs the UNAMBIGUOUS cases and name the residual.
**A face that closes on "fixed" hands the next reader a solved problem that is ~90% solved.**

⚠ **AND THE POLICY IS A POLICY, NOT A FACT:** *"a value that is a well-formed SEDOL is never a
damaged CUSIP"* is a choice about which error to prefer, and it prefers the safe one. Say it that
way rather than as a property of identifiers.

⭐ **THE ONLY COMPLETE FIX REMAINS UPSTREAM COERCION -- WHICH IS WHAT SECTION 5 ALREADY SCOPES.** A
downstream repair operating on a value whose information is already destroyed can only ever be a
heuristic; RTX (`7.55E+105`, unreconstructible) is the destructive limit case and the ~10% is the
same loss in a milder form. **Nothing further to do now -- named so the residual is not rediscovered
later as a surprise.**
