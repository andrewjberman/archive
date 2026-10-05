# DSGN_AMGTV1 -- ROUND 36 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-04 ~23:4xZ) -- THE RENDER INSTRUMENT GRADES THE REDESIGN; THE BATCHED REPAIR

**Input:** decomposition v36 and the issuance @70d41165c1, over PRD v0.15 @237d5d742f (ADMITTED). Rectangle: `round35/ROUND35_CLOSE.md`
section 4, confirmed by the CTO (@98209ce86a condition 4). Base: portal 35a723bf (DEV; round 35 landed there, CI 37237977735 success).

## 1. THE CELLS (2 of 2 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 | outer drain |
|---|---|---|---|---|---|
| `AV-zn-1` | Instrument re-anchor (FWD-20) | ~97 | b811f94f | instrument35 4/4 (854 s); battery29 0 skipped | bd396ef6b8 |
| `AV-zn-2` | List labels >= 11px and radii, the tooltip's headline, no zero move (FWD-20/5/27) | ~98 | 30a86c5e | repairs36 5/5 (issuer re-run); battery29 0 skipped | bef3b2d7a7 |

Both proof instances are VALID. ~97's drain waited 120 s for `4.0.0_SA_CRO~Z`'s staged LDO-001 deploy entry to leave the shared
index; that entry was never touched. **Row `DSGN_AMGTV1-Z-W97-S1`** (OBSERVATION, INERT) records that the re-anchored instrument
turned up two real list-state FAILs, sizes and radii. Those are AV-zn-2's subject, and the instrument reads both PASS on the merged
candidate (section 3). It is left for the CVO to adjudicate (the row gate reserves adjudication to the CVO).

## 2. THE CANDIDATE -- portal `cb6772fd` (worktree 92, branch `dsgn-r36-onto-dev`, LOCAL)

The candidate is origin/DEV 75efe9d6 plus `dsgn-r36-zn1` and `dsgn-r36-zn2`, merged `--no-ff`. DEV 75efe9d6 carries AMGT_CORPUS's
ModelTab.tsx/modelSheet.ts candidate (CTO msg 29279, COO~X msg 29293); this round touches neither file, and the merge was clean.
Against DEV it moves 6 files, +295/-1394; most of the -1394 is the fixture swap to the windowed chatter shape. Issuer run:
- `round29/checks/battery29.sh` with no skip: ALL PASS (tsc 0, eslint 0).
- round 36 repairs36 5/5; round 35 changed35 5/5, payload35 4/4, cloud35 5/5; round 34 labels34 4/4, repairs34 4/4, peername34 4/4.

## 3. THE REAL RUNS

**FWD-20: the render instrument, re-anchored, on the candidate.** `instrument35.cjs`, out-20261004T231405Z, 818 s: **4 of 4 arms.**
- Candidate cb6772fd: **76 PASS / 0 FAIL / 0 NOT_EXERCISED / 1 N/A** over six states and the sweep. The band clause passes on all six
  with `bandContainersTopLevel <= 1` and `lightOnDark == 0`. faces.price reads 19 of 19 at the page's rest rule (9 gainers, 23
  losers). faces.chatter reads 55 of 55 on the windowed served shape. list.sizes and list.radii PASS, which is AV-zn-2's repair.
- Pre-redesign 8fa7abde: 6 band-clause FAILs (for example list.lightOnDark = 5, white H3 ink on navy).
- Plants: two bands FAIL, a light card on a band FAILs, and the one-band control PASSes.
- **The person's read (FWD-20's person arm, the issuer):**
  - `list-chatter.png`: one dark band, the "What is moving" panel head, which is within the ceiling. All collage labels are 11px or
    larger and readable; shortened names end "..." (Mast..., Intui..., Workd...).
  - `thesis.png`: the light card family. The timeline card prints the designed absent sentence for the cloud ("The headline word
    cloud is not served for this company yet."), because that fixture predates FWD-39.
  - No rejection.

**The close walk:** `round35/walk/closewalk35.mjs`, read-20261004T232007Z, on 5174 = cb6772fd against the live API. The walker was
ARMED 23:20:09Z and DISARMED 23:31:15Z, and a login after the disarm was REFUSED. Both notices went to MSTR~Z.
**23 reads: 21 PASS, 1 FAIL, 1 ERROR.**
- **fwd5-timeline-hover: PASS, 3 of 3.** Round 35's FAIL is gone: the tooltip shows the day route's strongest headline.
- fwd21-labels at 30/90/365D: 57/67/70 labels, 14/17/18 shortened, each with a full-name hover. No bubble is unlabelled at 11px.
- r35-faces on VLO and AMD: PASS, each with a 40-term cloud. AMD's served cloud no longer carries "amd" (chip, tsmc, nvidia ...).
- **r35-faces on BA: FAIL, graded PASS on reading** (as in round 35). The one hit is a real move to zero (dividends per share 2026,
  0.01 -> 0.00), not an equal print.
- fwd24-control-any-name: ERROR, as in rounds 34-35 (no walked name lacks a checked field; MSFT US supplied the control in round 34).
- Everything else PASS: overlay census x3, tabs x3, the non-USD header, the no-officer Exec tab, account-menu Escape, and one
  display name per security.

## 4. OPEN

- **The CTO's product-file review of cb6772fd**, then its DEV push (Andrew's word, MSTR~Z's act).
- **PROD:** the CTO's round-35 condition 3 (PROD waits for RESAPP aq-5). Observation, not a grade: the deployed
  `opal-amgt-scoped-api` CodeSha256 moved at 22:42Z (now 2rFeF57l), and AMD's served cloud no longer lists its own ticker word.
  RESAPP's `TO-AMGT-aq-5` still reads `<status>pending</status>`, so the condition's owner (the CTO, with COO~Z) reads it.
- **Enrichment list for round 37:** this close finds no new page defect. Census-only items: RankedChart.tsx's 10px ticks (not
  mounted on the list state) and the shared PanelContent `rounded-b-lg` (8px; the estate's component). Both are the CTO's call
  whether to cut.
- The 7 outcomes the round-34 review reopened, and the round 35-36 outcomes, are graded on the served build after the DEV push.

## 5. CTO REVIEW (@1de7e46895, msg 29321): APPROVED FOR DEV

- **Re-merge onto current DEV and re-run:** remote DEV 3173c186 merged into the candidate as **portal c66d08f3** (no SecurityAnalysis or
  scripts overlap). Against DEV it is still 6 files, +295/-1394. battery29 ALL PASS (0 skipped); repairs36 5/5, changed35 5/5,
  payload35 4/4, cloud35 5/5, labels34 4/4, repairs34 4/4, peername34 4/4. **The push candidate is c66d08f3.**
- The DEV push takes Andrew's word; the CTO is asking him. MSTR~Z's act.
- Round-35 condition 3 is MET in substance (the CTO's read: aq-5's code is live, and AMD's cloud has no "amd").
- Round 37 cuts no new page cells; the census items stay uncut. The grading is on the served build after the push.
