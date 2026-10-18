# AMGT_RESAPP round 117 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: DRAFT, 2026-10-18 ~08:1xZ. NOT SENT. Sections 1 and 2 hold what is measured so far; every line marked `[TO FILL]` waits on the `bx-5` act (SC1, the order `AMGT_RESAPP.TO-AMGT-bx-5.*` @`f083288861`, queued behind another COO's deploy) and the issuer's reads after it (`round117_prep/checks/r117_post_act_reads.sh`). Nothing below the `[TO FILL]` markers is a claim.** Round 117 is the CTO's round-116 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round116.R1.md`, msg 7933, addendum `@7161fc38d4` correcting item 3), issued at `51cbf82b4f` under this seat's keys (decomposition s.126). `round-close-check --round 117` reads `orders=3 ... verdict=MAY-CLOSE` (before `bx-5`, which rides the REDEPLOY workstream). Push state of every commit named: LOCAL on box/dell1, unread.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bx-1` | the Summary reads the served recommendation (`last_stated_position`: text, fund and weight, one `Source:` line); no state sentence names a path, a key, an order id or a vendor error | complete | worker ~512, re-seated once (AMENDMENT 1: the served recommendation leads the Summary, before the thesis sentence; my spec's order was wrong); merged `74e37dade8` and `4613d6c0cb`; 21 tests; 8 of 23 state-sentence sites changed |
| `AMGT-bx-2` | a header money figure's currency by the PAGE'S rule: own code, `currency not stated`, or WITHHELD (the page's words, no amount) where the served basis is UNMEASURED | complete | worker ~513; merged `543dc225ef`; 12 tests; of 18 money-unit header figures 4 withheld, 3 second market-value lines deduped, 11 unchanged. The CTO's item-3 grade named USD for RIO LN; the served data carries no currency for those four figures and the page withholds them: reported, accepted (msg 7937) |
| `AMGT-bx-3` | the cleared `ai_fill` passages the page shows, each followed by `machine-drafted, cleared <date>`; uncleared never; a `Thesis pillars` section | complete | worker ~514, re-seated once (AMENDMENT 1: the management passages above the roster as the page draws them; no `no public profile` line above a passage); merged `3dd98e9a9d` and `64907494e1`; 10 tests |
| `AMGT-bx-4` | the issuer's reads | the issuer | instruments `r116_pack_money_vs_page.py` (the page's withheld rule) and `r116_pack_form_check.py` (path leaks, labels, the Thesis pillars heading), each run on the live packs as a base control (`MONEY NO 12/16`, `FORM NO 3/8`); the merged-tree reads below |
| `AMGT-bx-5` | the live pack | `[TO FILL]` | `0.7.0_AE_CloudOps~SC1` from release pin `9ab6d36305` (live pin `fe04d740bf` plus `render_pack.py`); never-widen pair: COO half `871379e429`, CTO half `2a3c57d709` |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` |

## 2. The issuer's real runs

- **The merged tree:** `lib/research/print/tests` plus `lib/research/api/tests` in the full tree read `9 failed, 1230 passed`: exactly the nine known failures, 40 new tests all passing. The hand merge of `bx-3` needed a second try: a first resolution of the append-only investigation channel kept both sides and the row gate refused the merged index (4 malformed blocks); the second resolution was HEAD plus the branch's appended rows.
- **The candidate** (this checkout's handler over the live pool, eight names, 200 on all sixteen requests, the `ai_fill` reader run as the live function runs it): `PACK FORM: YES (8 of 8 names)` with no line naming a path or an order id; `MONEY VS PAGE: YES (16 of 16 money lines)` with four lines withheld; labelled passages RIO LN 1 (the Simon Trott profile), ICT PM 3, GOOGL US 4, ICICIBC IN 3, BA US 1, KMB US 1, HD US and TSM US 0 (their served blocks carry no text).
- **The pool, read before the cut with a denominator** (the CTO's negative-control condition): 95 `ai_fill` documents, 475 blocks, 134 with text, ALL `CLEARED`: no live name holds an uncleared block. The live negative arm is HD US and TSM US (`[TO FILL]` after the act: 0 labels on the live packs); the uncleared arm is proven by the unit control `M4` only.
- **The live function after the act:** `[TO FILL]` config (CodeSha256, memory, timeout, environment), `[TO FILL]` PACK FORM, `[TO FILL]` MONEY VS PAGE, `[TO FILL]` print-route timing against the CTO's 20 s bar, `[TO FILL]` the three live PDFs in `round117/packs/`.

## 3. For your judgment

`[TO FILL after the act]` 1. FWD-5 at L9: three live packs (RIO LN, ICT PM, GOOGL US) for your re-read against the CTO's grade (the Summary reads the served recommendation, no path or order id, the page's currency rule, the labelled passages).

Known now, to state at the send: (a) for these three names no recommendation, thesis or risks have been DRAFTED (the Summary leads with the served position, then `No investment thesis has been written` and the risks sentence); (b) the machine-written passages are the cleared `ai_fill` text the page shows, labelled, and are not analyst prose; (c) RIO LN prints no market cap, net debt or enterprise value amount: the page withholds them (no currency is served, basis UNMEASURED), which the CTO accepted as the grade; (d) not covered: the `format=rich` export (it prints raw amounts for the withheld figures and served reasons verbatim: rows `AMGT_RESAPP-D1-W513-S1`, `W512-S4`), `EQY_FUND_CRNCY` served USD for RIO LN though no per-figure currency is (`W513-S2`); (e) the pre-commit risk reflex held on `render_pack.py` on each worker commit, citing a closed redeploy record: the redeploy's closure diff is `bx-5`'s.

**Process findings (seat errors named):** my order face told the workers to shorten the proof-instance file name, and `round-close-check` needs the full name (three renames repaired it); a stray backspace byte in a non-raw regex made my money check's withheld branch silently not fire until its base control exposed it; my candidate capture script forced an empty `ai_fill` hold directory so a first candidate read showed no passages; the two defects found by reading the merged output (the Summary order, the contradictory `no public profile` line) were not catchable by the workers' fixtures.

**Not verified by the issuer:** `[TO FILL]`.

## 4. Open and carried

- Round 118 (the CTO's analysis, after your slug and the FWD-5 grade): the rich export's withheld figures and served reasons; `EQY_FUND_CRNCY`; whatever your L9 read of the live packs surfaces.
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew); row `S57` (the fold-back verb) is the portal manager's.
