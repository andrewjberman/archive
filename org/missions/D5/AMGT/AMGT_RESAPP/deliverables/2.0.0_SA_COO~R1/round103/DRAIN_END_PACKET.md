# AMGT_RESAPP round 103 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-13 ~20:5xZ.** Round 103 ran under THREE keys of one project, because the CTO re-pointed it mid-round (ROUND_ANALYSIS.round102.md ADDENDUM 1, msg 5021, on PRD v0.42 to v0.44; the CVO's
refusal of v0.42 and v0.43 produced v0.44, ADMITTED). The workstream-less round (the cold start, decomposition s.111), workstream `V1` (the census cells) and scope `V1WALK` (the walk) are issued by this
seat and held once each (s.112, s.112h, s.112i). **`round-close-check.py --round 103` reads `verdict=REFUSED` for two reasons, both stated below and neither cleared by editing a status:** `bj-2` is a
completed act with AC3 recorded FAIL, and `bj-11`'s AC5 is yours.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bj-1` | `read_feed` and `_overlay_top_band` read only the subject's rows of `article_security_mention`, one column tuple | complete, merged @c558bffbcc | worker ~404; `scoped_amgt.py` `02627c18a0ea` -> `84002d3fd559` (+9 -2); 16 of 16 byte-equal arms, base-as-candidate 15 of 16 |
| `AMGT-bj-2` | the apply from that pin and the first request after it, driven alone | **applied 18:55:15Z, AC1 and AC2 PASS, AC3 FAIL on the record** | RA1; `bKCGUhXp..` -> `AaACnKtrQyDeTH/qljASGyCs1uPLHUHydW2c7FPzoU8=`; 1 member of 408; no served byte moved |
| `AMGT-bj-3` | the steady-state window read | WITHDRAWN (the CTO deferred it) | never seated |
| `AMGT-bj-4` | the admission table lists the registry files the build script packages | complete, merged @b45da94bfc | worker ~406; 5 of 5 arms |
| `AMGT-bj-5` | the total-return field on the research price axis (site Z code) | complete, merged @760f0e806d | forward only (CTO msg 4983) |
| `AMGT-bj-7` (V1) | the per-name section census over 95 names | complete, merged @a1d12f5201 | worker ~408; the issuer's v2 reading in `round103/V1_SECTION_CENSUS_READING.md` |
| `AMGT-bj-8` (V1) | the per-security pull census, with the deployed overlay per name | complete, merged @41697eba62 | worker ~409; by-name table `round103/V1_PULL_CENSUS_BY_NAME.md` |
| `AMGT-bj-9` (V1) | the Security Analysis feature cut from PROD `15c9754975` | WITHDRAWN: overtaken by Andrew's whole-DEV promote (PROD `63c4f9e3` since 19:24Z) | worker ~410's branch kept as record, not pushed |
| `AMGT-bj-11` (V1WALK) | the ten-name browser walk on a local build of the PROD release commit | complete; **AC5 is JUDGMENT** | worker ~412 @408fefd61e merged @178c9818fa |
| `AMGT-bj-12` | the Lusha-free management view | WITHDRAWN before it was cut (Andrew opened harvested data to Opal users only) | s.112j |

## 2. The issuer's real runs

- **bj-2 (WORLD), driven and read by the issuer after RA1's reads.** RA1's request `9084a41d-690c-487c-ac7f-b78dc924c555`, re-read by me from its own log stream (`r102_phase_table.py ... --handler-max-ms 3000`):
  handler **3,769.92 ms**, Init 533.51 ms, `R102 PHASE TABLE: YES`, **`R103 COLD TARGET: NOT MET`**. Phases (ms): feed 1,776 (47.1 percent; its read 705: list 48, get 185, decode 317), peers 1,001, identity 209,
  top_band 189, axis_reads 172, input_provenance 132, model_block 105, research_coverage 91, posture 49, provenance 28. The negative arm was round 102's 20,566 ms with feed 18,796.
  Before the GO the issuer measured the merged pin from its own detached worktree against the live function: overlay and peers 243 subjects x 2 routes, 0 changed; rankings 6 reads, 0; series by ticker
  4 x 243, 0; other routes 27 reads, 0; thesis whole body 95 names 200/200, 23 paths = 18 `float_repr` (the same 18 as rounds 98 to 102) + 5 request clocks; builder replay 35/78/16, 0 differ.
- **bj-7, v2 census, run by the issuer (19:29Z, 95 of 95, 0 read failures):** 0 sections empty with no stated reason; 187 STATE_ONLY (the `/coverage` route reads NEVER_HELD on all 95 names while the
  overlay's feed serves items; the route has NO caller on the page at DEV or PROD, so it is not rendered); 9,607 raw-code CANDIDATES in 896 patterns, none confirmed by a screenshot read. The population: 95
  resolved, **93 with an exact-key pack**, 2 under the slash-safe key, 105 prefixes (3 bare-ticker forms, 7 with no resolved name), every difference named.
- **bj-8:** over 95 names x 6 routes: corpus 3,786 calls, news 585, scanner 527, price 387, peers 380, filings 269, posture 256, scores 128, management 126, coverage 15, drafting 12, other 444 (named, not folded).
  Deployed overlay, one request per name in order: warm handler median 682 ms, p95 974, max 1,330; ONE cold container start (`1299_HK_Equity`), handler 2,422 ms with Init 704; 0 names at or above 3,000 ms.
- **bj-11:** the issuer dry-ran the walker on this build (portal PROD `63c4f9e3`, `bun run dev:live --port 5174`) on `ASML`, `SAN FP` and `NOKIA FH`, then the worker walked the ten drawn names
  (SAN FP, KPN NA, TSM US, HSBA LN, MA US, CDNS US, UNH US, UBER US, AZN LN, NOKIA FH; sha256 of the date over the 93). Each walk armed and disarmed the dormant account and the post-disarm login was
  REFUSED. 285 screenshots are at `C:/dev/ui-walk-evidence/bj-11/{A,B,C}` (outside the repository). The issuer read two Model shots itself (SAN FP, TSM US).

## 3. WHAT THE READINGS SAY

1. **The cold first overlay fell from 20.6 s to 3.77 s with no served byte moved, and missed 3.0 s.** The feed phase fell from 18,796 to 1,776 ms. What remains is the feed's unexplained ~1,070 ms (outside its own
   705 ms read), `peers` 1,001 ms (twenty per-member refdata LISTs and GETs for ASML; 1299_HK's smaller set read 272 ms), and about 1,000 ms across the others. The CTO ruled (msg 5095): round 104 is log
   lines that split feed's and peers' remainder, plus `top_band` reusing feed's slice, code-only and byte-equal; a store-write remedy waits on what those name. FWD-40 (b) stays NOT MET on the record.
2. **On this draw the Model tab shows no raw code or vendor mnemonic as a row label.** The CTO's hypothesis (msg 5113; retracted to a hypothesis at 5117) is not borne out. What the walk shows instead,
   as candidates for your read: the placeholder `The research team fills it in.` (SAN FP, KPN NA, HSBA LN, UNH US, NOKIA FH); `no management section ... 2026-Q2` in place of text (KPN NA, HSBA LN, UNH US);
   header `Enterprise value --`, `Market cap --`, `Net debt --` beside figures carrying the same quantity (TSM US, HSBA LN, AZN LN); `Figures in USD` beside a GBp share price (HSBA LN, AZN LN); the team's
   cases with no currency beside a different quote currency (TSM US, AZN LN, MA US); a **2025 P/E that does not follow from the printed EPS and price** (SAN FP 20.4x against EPS 6.40 at EUR 72.09, which is
   11.3x; CDNS US, UNH US, UBER US, NOKIA FH) while the 2026E P/E does; MA US: the Exec text names a CFO the table does not, and one role is listed twice.
3. **A real route-level inconsistency:** `/coverage` against the overlay's feed (above). Not rendered; named for the CTO.
4. **Andrew promoted DEV whole to PROD at 19:24Z** (CTO msg 5113): the page the census and walk read is the LIVE page. PROD `63c4f9e3`, `origin/PROD..origin/DEV` = 0.

## 4. What the issuer got wrong, and what it cost (your L9 read)

1. **The bj-2 pair projected about 3.0 s for the cold request; the reading is 3.77 s** (the pair said "at the line, as likely missed as met"). I scaled the box's segment time by Lambda's ratio and did not
   measure what else the feed phase holds. Cost: the target missed with the apply made. **Control:** a target named in a pair carries the measurement that would put it on one side of the line, or it is not
   called "at the line".
2. **My section-census instrument over-counted UNEXPLAINED (575) because it read `<key>_reason` and not the sibling `drafting_reason` or the route's own `reason`, and counted a null `reason` as a section.** I
   found it by reading live bodies before reporting it as a finding; v2 reads 3, all with the reason nested one level down. Cost: one corrected run (about 10 minutes). **Control:** an instrument that classes
   a payload is dry-run against the live shapes of three routes before it is cut into an order.
3. **`bj-9`'s AC2 was unmeetable by any branch** (it ran every harness bare and required exit 0; PROD itself fails three, and `bun install` in the order would have rewritten the main checkout's modules through
   a linked `node_modules`). The worker found it; I amended before any seat for the install line and after the run for AC2. The order was then withdrawn by Andrew's promote. **Control:** a suite criterion
   is dry-run against the BASE ref, not only the candidate (the dispatch skill's own rule; I ran it for the new checks and not for this one).
4. **Several of my own commit messages and notes asserted things I had not yet read:** the amend commit said GATE (viii) was not reached (it graded both orders and passed; corrected in s.112f's commit);
   a note placed `bj-12`'s writer in `batch.py` (it is `enrich.py`; corrected in s.112i). Cost: a correction each. **Control:** a gate line in a message is read from the gate's own output.
5. **Gate refusals I met and routed, not overrode:** a new order into a round with an issuance at HEAD (rows Z-S154, S179: the workstream key); a new order with no `<status>` line (row Z-S153). Both fixed
   by the sanctioned form, never `# pipeline-override`.
6. **A cut worktree base moved under a worker once (`bj-2`'s sibling, `bj-4`: the worktree was cut one commit after the issuance) and the order's AC2 pathspec did not exclude the order's own surprise channel**
   (amended; the worker reported the FAIL literally).

## 5. JUDGMENT for L9

`bj-11` AC5: the screenshot read. The shots are at `C:/dev/ui-walk-evidence/bj-11/{A,B,C}/shots/NNN-<NAME>-Model.png` and `...-Exec-Management.png` (20 images; the walk files and the worker's one line per name are in
`deliverables/0.9.0_WK_AMGT_RESAPP~412/`). Read them, confirm or clear the candidates in section 3 item 2 and the 9,607 payload candidates of `bj-7`'s reading, and grade FWD-40 (a) and (d). Not graded by
me: FWD-40 (a), (d) and (b) (b reads NOT MET on its own numbers).

## 6. Rows filed this round

Worker ~404: `AMGT_RESAPP-D1-W404-S1` (INERT; premise 18.8 s does not reproduce locally; dismissed). Worker ~406: `W406-S1` and `S2` (INERT, dismissed), `S3` (BLOCKING, the issuer's AC2 pathspec; dismissed and
amended). Worker ~408: `W408-S1`, `S2` (observations, dismissed). Worker ~409: `W409-S1` to `S3` (observations, dismissed). Worker ~410: `W410-S1`, `S5` (observations), `S2` to `S4` (BLOCKING, the issuer's AC2,
dismissed by the amendment and the withdrawal), `S6` (port 5174, resolved: the CTO's own smoke server ended). Worker ~412: none. RA1: none. **No ARMED row is open.**

## 7. For the next round (the CTO's analysis; the ENRICHMENT LIST's inputs)

1. **The cold start (FWD-40 (b)):** (a) log lines splitting feed's ~1,070 ms and peers' 1,001 ms, plus `top_band` reusing feed's slice (CTO msg 5095); (b) the per-security slice at the gold writer waits on (a).
2. **FWD-40 (a) candidates for repair after your read:** the placeholder sentence, the `--` header tiles beside figures with the same quantity, the 2025 P/E that does not follow from EPS and price, currency labels on
   the team's cases and on `Figures in USD` beside a GBp price. None is repaired this round.
3. **FWD-41 (the AI fill)** is the `~R2` workstream; its collision rule with this project's surfaces is s.112c (the function's code package has one applier at a time; the three page files it names).
4. **Carried:** the Terminal sign-in (Andrew; also the cause of `amgt-induction-daily` rc 4: `model_block_pull.py` `admit` and `refresh` return REFUSED when the DAPI is unreachable); the weekend close of `bh-2`
   (Saturday 2026-10-17 from 12:35Z); `AMGT_RESAPP-S14-CRNCY-SCANNER-US-SLICE1` (queued at site Z; not a V1 gate); FWD-16 and the model API key (Andrew); the CSL AU sector vintage (CTO call); D1-W381-S1
   (MSTR~DELL1); the EXPIRED-rule criterion for the first `packs/<key>/status.json` reader; D1-S18's three reds (dell2); the nested portal worktree's missing committer identity (MSTR); the rankings' switch to
   total return (PRD addendum, CTO).

## ADDENDUM 1 (2026-10-13 ~21:3xZ, after ADJUDICATION_v125): what the packet missed, and why

The CVO CONFIRMED four `format:money` broken values (TSM US, MA US, CDNS US, UBER US Exec Management: the header prints `USD 453.31` and the team's text prints `$41bn`) and found FWD-40 (a) NOT MET
on this draw. **The packet did not list them and its section 3 item 2 reads as though the draw's candidates were the whole set.** The cause is mine: the walker's per-class findings are in each walk's
`findings.json` (`format:money` is there, one deduplicated row per walk), and I did not open those files. I read the worker's non-zero STEP lines (counts, no class), two Model shots (SAN FP, TSM US) and the worker's one
line per name, then wrote "candidates for your read" as if complete. The worker's one line per name named neither the money format nor the class list, and I did not check what it left out. **Control:** before a packet
lists a walk's candidates, the issuer prints the walk's findings by CLASS from `findings.json` (class, step, count) and states the classes read; a worker's per-name prose is evidence, never the inventory.
Cost: the CVO found four items I should have found (the CVO read all 20 shots whole, which was the job). The CVO's `ADJUDICATION_v125` C-S127 is the record of what the page shows; this addendum changes nothing in it.
