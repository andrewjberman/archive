# AMGT_RESAPP round 102 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-13 ~16:5xZ. Four orders, all complete: `AMGT-bi-1` (a build: the overlay prints one log line per phase), `AMGT-bi-2` (its apply: `opal-amgt-scoped-api`
`j+j1k5r7IY1ZCh9NijT8GSLaqEL3FhamwT8V3tYofCk=` -> `bKCGUhXppwg1WJxnI/SunRQ/paJXq9m1qOGqHTp2kdc=`, no served byte moved, and the first request after it read by phase), `AMGT-bi-3` (a read: the weekday
steady state driven on the live function) and `AMGT-bi-4` (the portal suite's six red tests: a DEV candidate built, then WITHDRAWN before landing and the row ROUTED).** Round 102 implements the
CTO~DELL1 round-101 analysis `ledger/ROUND_ANALYSIS.round101.md` section 3 (msg 4864); decomposition s.110; issuance @30eabaab86. Amendments (the issuer's own orders, no gate limb graded them: they
are modifications): `bi-4` AMENDMENT 1 @d6463fb75c (the CTO's contract ruling, later moot), `bi-3` AMENDMENT 1 @1400223c57 (a second run), `bi-2` ADDENDUM 1 to its pair @0389729ee5 (the twelfth member) and the
`<proof_genre>` line @089668ee09. `round-close-check.py --round 102` is read after your grades: judgment criteria in two orders (`bi-3` AC3, `bi-4` AC4).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-bi-1` | `_phase_call` and fourteen `AMGT_PHASE route=overlay` lines in `read_security_overlay` and the handler's overlay leaf; log lines only | complete, merged @6ecb5bc567 | worker ~401 @b19294e267; `scoped_amgt.py` `9f72b58aa87e` -> `02627c18a0ea` (+32 -9); issuer re-run 14 of 14 |
| `AMGT-bi-2` | the apply from merged pin `6ecb5bc567`, twelve members by blob (five packaged); the first request after it driven alone | complete, SERVED: applied 2026-10-13T16:15:54Z (LastModified 16:17:06Z) by `0.7.0_AE_CloudOps~RA1`, commit 3a14a2a55d, ledger CLOSED 11 of 11 | pair `ledger/NEVER_WIDEN_ROUND102_PHASE_LOG_REDEPLOY_{COO,CTO}_HALF.md` (COO @97304bbc62, CTO msg 4919 and ADDENDUM 1 msg 4929) |
| `AMGT-bi-3` | the weekday steady state: `/freshness` from the snapshot, warm overlays, bytes | complete, workers ~402 (two seats), merged @b5d90e2193 | two runs, kept; the first read NO on the issuer's design defects |
| `AMGT-bi-4` | NFRA_GATSCP D1-S18: the portal suite's six red tests | complete as a READING at DEV 0a06280a; the candidate (portal `c26e0c68`) WITHDRAWN, nothing landed or pushed; the row ROUTED by the CTO (msg 4925) | worker ~403, merged (outer) @8375ebc797 |
| `AMGT-bi-5` | ss-7 / pp-4 on the DEMQUE answer; the EXPIRED criterion | CARRIED, no order | `AMGT_RESAPP-S14-CRNCY-SCANNER-US-SLICE1` queued at site Z, finish 2026-10-14 |

## 2. The issuer's ONE REAL RUN at close

- **bi-2 (SERVED, WORLD): re-run by the issuer on the live function, after RA1's reads, alone** (RA1 released the hold at 16:29Z; my readers ran 16:30Z to 16:37Z). Deployed censuses `r97_sector_serve_census.py`
  (6 of 6), `r95_classification_census.py` (6 of 6) and `r94_name_census.py` all YES; `r89_deployed_close.sh --want amgt-corpus-dossier/15` YES. `r98_thesis_fullbody_compare.py --after local` from a detached
  worktree at the pin (the live function against the pin's own handler, 95 names, all 200): **0 paths under `team_sheet`, 7 generation clocks, 18 `float_repr` (the measuring checkout's python 3.14; the same
  18 as rounds 98 to 101), 0 other**: `R98 THESIS FULLBODY: YES`. RA1's compare: replay 527 requests, status moved 0, 36 clock paths, 0 over 20 s (max 3.54 s); `ay4_compare` 95/95, 95/95, growth 0, build 1/1;
  **the naming replay on the BUILT zip (the CTO's condition): 35 requests, 78 builder calls, 16 distinct, 0 differ.**
- **The first request, re-read by me from its own log stream** (`r102_phase_table.py --request-id 4737aa2a-fb3f-4092-84d8-42cfabfc8a8a`, `R102 PHASE TABLE: YES`): `ASML_NA_Equity` overlay, 200, handler **20,565.94 ms**,
  Init 744.11 ms (cold by construction: the first request on a new package). Fourteen phases once each; the eleven inner phases sum to 20,323 ms against `read_security_overlay` 20,338 ms (0.07 percent); the
  outer three to 20,563 ms against 20,565.94 ms (0.014 percent).
- **bi-3: verified against the function's own REPORT lines** (15:11 to 15:14Z: 20,531.5, 206.0, 839.9, 799.9 ms; Init 666.07 ms on the first) and the issuer's dry-run at 14:21Z.
- **bi-1: re-run on the worker's tree** (14 of 14); **bi-4: the seven test files 23 pass 0 fail on the withdrawn candidate; typecheck rc 0; eslint rc 0** (a measurement at a stale base, section 3.4).

## 3. WHAT THE READINGS SAY (the attribution this round was cut for)

1. **The cold first overlay request is 20.0 to 24.0 s and 91 percent of it is ONE phase, `feed`.** On `bKCGUhXp..`, request 4737aa2a (ms): `feed` **18,796**; `peers` 714; `model_block` 239; `identity` 223; `axis_reads` 182;
   `input_provenance` 126; `research_coverage` 90; `posture` 68; `top_band` 59; `provenance` 47; `check_face` 2; `description` 0; `serialize` 2; Init 744 outside the handler. Inside `feed`, the module's existing
   `AMGT_SEGMENT gold_article_security_mention=17951` is the gold table read (a second read of the same table in the same request: 49 ms). **Code:** `read_feed` calls
   `_timeline_snapshot_rows("article_security_mention")` (`scoped_amgt.py:5657`) which loads the table for ALL securities and filters by `security_key` in Python. Lambda's Init (0.56 to 0.74 s) and every
   other phase together are about 1.7 s. **No remedy was cut: the CTO's rule (round-100 ADDENDUM 2(b)) was attribution first.**
2. **The 20 s is the first overlay on a container, not the container's first request** (`bi-3`, run 1: `/freshness` met a new container at 0.27 s with an Init, and the next overlay on THAT container read 20.08 s with
   no Init). A warm overlay after the 60 s hold reads **0.75 to 0.91 s** (eight requests, three runs and RA1's) and `/freshness` **0.21 to 0.27 s** from the snapshot. The CTO's "about 1.3 s" is the box's figure; Lambda's is lower.
3. **The snapshot and the recompute differ on two metadata keys (`denominators`, `reads`) 2.4 to 2.7 hours after the write with the 302 rows equal**: inputs landed after 12:30Z. Equality is read near the write,
   or with those two keys named.
4. **The portal suite (D1-S18) at the cut and today are different readings.** At local DEV 0a06280a: 462 files, 1,419 tests, 1,386 pass, 6 fail (three undisputed repairs and three wire-drift tests on one contract
   decision). The local DEV was **34 commits behind origin**; at origin DEV f6ef1d25 the suite reads 471 files, 1,466 tests, 1,435 pass, 4 fail, five of the six already repaired by IRPT_BCKEND's landings
   (IB-pr-495, -500, -504, -506). The three reds that remain are ROUTED to dell2 (IRPT_ANLREQ, IRPT_BCKEND, DSGN_IRPTV1) by the CTO.

## 4. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **I measured the portal suite on a local `portal` DEV that was 34 commits behind origin and built a candidate on it.** Cost: a worker (two seats, about 35 minutes), a contract ruling from the CTO, a
   regenerate-and-relax edit of a test, and an approval to land that had to be withdrawn. Nothing was landed because I re-measured at origin DEV before asking anyone to push; the CTO's words: "good catch measuring at
   origin DEV". **The control:** `git ls-remote origin DEV` against `git rev-parse DEV` before any portal measurement, and the base printed in the order.
2. **`bi-3`'s criteria assumed a container that stays the same and inputs that do not move** (and the claim "a warm overlay after the hold reads about 1.3 s" had no container condition). The first run read NO on both and
   filed two ARMED rows; the reading was richer than the criteria (the first overlay per container). Cost: an amendment and a second seat (about 12 minutes). **The control:** a driven-request criterion names the
   container condition it needs, and a metadata equality is read near the write.
3. **`r102_phase_table.py` read NO on its first live use**: its controls were saved lines files, and a live `print` line carries no request id, so the id query returned START, END and REPORT only. Caught on the
   first real request (before RA1's AC3), fixed @50566b47c1. **The control:** an instrument that reads a remote store is dry-run once against the live store, not only against a control file.
4. **The admission table diffed only `scopes.json` and `systems.json` among the registry files**, and the merged pin was not a one-member pin: RA1 STOPPED at the build on a twelfth member (`exemptions.json`, the
   Inflection fence row), nothing landed. Cost: one STOP round-trip (about 20 minutes) and an addendum to the pair. The CTO had named eleven because I did; the build's own diff is the authority. The
   instrument now diffs every registry file. **A one-member pin exists only in the window right after a merge; `bi-1`'s merge landed after ten other seats' changes, and I did not measure the pin's members before
   choosing to cut the apply as a separate order.**
5. **The `bi-2` order lacked `<proof_genre>DEPLOY</proof_genre>`** (round 101's `bh-2` had it; I cut `bi-2` from a template that did not). RA1's instance read INVALID on that one line. Fixed @089668ee09.
6. **The substitution I proposed for the CTO's close** ("a first request on a new package, cold by construction, for 15 quiet minutes") held, and its cost was zero; it is recorded because it changed the close's text.

## 5. JUDGMENT for L9

`bi-3` AC3 (the steady-state reading states only what its numbers show, with the weekday limitation named) and `bi-4` AC4 (the table and its decision, as a reading at DEV 0a06280a with the supersession in the
status). For your own re-run, read-only: `r102_phase_table.py --request-id 4737aa2a-fb3f-4092-84d8-42cfabfc8a8a` (a Logs Insights read), `r102_steady_state_live.py` (it invokes the live function: announce it).

## 6. Rows filed this round

Worker ~402: `AMGT_RESAPP-D1-W402-S1` (ARMED observation: dismissed by the issuer, the premise holds on a container that has served an overlay), `S2` (INERT, resolved by the amendment), `S3` (ARMED observation:
dismissed as INERT, metadata keys move with inputs after the write). Worker ~403: `AMGT_RESAPP-D1-W403-S1` (INERT: the nested portal worktree has no committer identity; carried to `0.0.0_AB_MSTR~DELL1`).
RA1: `AMGT_RESAPP-D1-S27` (the twelfth member: STOP at the build, resolved by the CTO's admission and the pair's addendum). Issuer: none. **For your adjudication:** the two ARMED rows of worker ~402.

## 7. For the next round (the CTO's analysis; the ENRICHMENT LIST's inputs)

1. **The remedy for the `feed` phase** (the CTO's call; nothing was cut here). Candidates the evidence supports, none built: read only the subject's rows (a partition or predicate on `security_key`, or the column
   subset the feed uses) instead of the whole `article_security_mention` table; keep the per-container reuse that already makes the second read 49 ms; the same table read appears under the timeline route. Close:
   a first request on a new package, driven alone, `feed` under a stated bound, the phases summing within 5 percent (`r102_first_cold_request.py` and `r102_phase_table.py` are the instruments).
2. **`peers` (714 ms)** is the next phase by size and is two orders below `feed`; no cell proposed until `feed` moves.
3. **The weekend close of `bh-2`** (the issuer's read): Saturday 2026-10-17 from 12:35Z, three DELIBERATE warm overlay requests more than 60 s apart, Lambda against Lambda (the weekday figure is now 0.75 to 0.91 s).
4. **Instruments**: `r94_admission_table.py` now diffs every registry file; an issuance's pin member count is printed in the pair before the cut.
5. **Carried:** `AMGT_RESAPP-S14-CRNCY-SCANNER-US-SLICE1` (50 cells, queued at site Z, finish 2026-10-14; the pull draws when the Terminal sign-in is back: Andrew's act; the full 1,038-cell request is filed and
   undrawn); the portal PROD promote call `dell1-20261011T033643Z-e7f2` (Andrew); FWD-16 and the model API key (Andrew); the CSL AU sector vintage (CTO call); `D1-W381-S1` (`0.0.0_AB_MSTR~DELL1`); the EXPIRED-rule
   criterion for the first `packs/<key>/status.json` reader (none exists); D1-S18's three reds (dell2, via MSTR).
