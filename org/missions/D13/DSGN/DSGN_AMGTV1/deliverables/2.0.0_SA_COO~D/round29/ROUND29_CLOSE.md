# DSGN_AMGTV1 -- ROUND 29 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-02 ~23:5xZ) -- THE SECURITY ANALYSIS UI/UX WALK FOLD

**Input:** PRD v0.10 @175e4081b1, delivered by the CTO's L4 notifier (msgs 28682 and 28691). Decomposition v29 and the issuance are
@f30cf93c7e (six cells, 12 issuer checks, each dry-run at portal dcdc89b1 and each FAILING there). AMENDMENT 1 to `AV-zg-1` is
@77abd61a20. FWD-26's presets were not cut (see section 5).

## 1. ORDERS (6 of 6 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 / AC3 | outer drain |
|---|---|---|---|---|---|
| `AV-zg-1` | timeline: recharts chart, shared tooltip, markers, day in the HeroDialog; HeaderBrief is the news card | ~80 (+ a successor session after AMENDMENT 1) | be4e019d | 4/4, 4/4, battery 4 skipped | 313531d16c |
| `AV-zg-2` | header: one light face, book order, key figures once and dated | ~81 | 9fef56b6 | 4/4, 4/4, battery 0 skipped | 55546c9c3e |
| `AV-zg-3` | Lead Panel one light card; Price top 10 + 10, on demand, window named | ~82 | 52541fe1 | 4/4, 3/3, battery 1 skipped | b606caabd1 |
| `AV-zg-4` | chatter collage (spiral, labels) filled by served tone through the ONE shared ramp | ~83 | 74347456 | 4/4, 4/4, battery 0 skipped | 4fe4dd0ffa |
| `AV-zg-5` | What changed leads the Model tab; ET via `dateWords.etStamp` | ~84 | 7598a3b2 | 4/4, 4/4, battery 0 skipped | bd7dbd67fd |
| `AV-zg-6` | Exec / Thesis / Peers in plain words; CEO-first; one money format; account menu lets go | ~85 (reseated: the first session stalled, and its successor removed 2 leftover plants) | cff0ff2c | 4/4, 4/4, battery 0 skipped | 2746796606 |

Every instance is VALID, checked from its own worktree, and every changed blob was screened: LF, no 0x08, ASCII. Two exceptions are
pre-existing, not introduced: `TopicCloud.tsx` was CRLF at base and stays CRLF, and `App.tsx` already held 2 emoji comments.

## 2. THE CANDIDATE -- portal `e370eb7c` (worktree 82, branch `dsgn-r29-onto-dev`, LOCAL)

It is remote DEV 39aa21c2 plus the six portal branches, each merged --no-ff with clean merges, and it is a fast-forward over 39aa21c2.
**Issuer run on e370eb7c:**
- `round29/checks/battery29.sh` with NO skip: ALL PASS (12 checks, 14 of 14 harnesses, `tsc -b --noEmit` rc 0). The items single
  cells skipped (`tabs`, `namecard`, `postureharness`, `posturezero`, `shell`) all pass merged.
- All 12 round-29 checks are at full marks.
- Round-27 `identity.cjs` is 3/3, round-28 `fixture.cjs` 3/3, and round-28 `render.cjs` 3/3 (vite build + the contract run).

## 3. THE REAL RUN -- walk `tmp/ui-walk/20261002T233653Z` (5174 = e370eb7c, live backend; ARM 23:36:54Z / DISARMED 23:43:20Z)

The walk covered BA, VLO and AMD: 81 shots, walk void no, every tab walked on all three names. A person read the BA overlay (shot 005):
- **Header:** light, with seven key figures in one row in USD and the market cap dated.
- **Collapsed sections:** "About the company" and "Posture, research dossier and readings" sit behind closed details.
- **News card:** recent news is its own card above the chart.
- **Timeline chart:** "Articles per day" with dated ticks, one hue with a search-state opacity legend, a coverage marker on the chart, and
  the earnings empty line in words.
- **Words:** "Back to all names" and "Export as a document".
Walker findings, read:
- **5 x `walker:control-missing` "tab not found":** the instrument. The walker navigates back by the old "Back to universe" text, which
  this round replaced (SAUX-30). The tabs themselves walked on every name (shots 007-081). This is a ui-walk tool item, like fold ruling
  10.
- **3 x `timeline:no-event-element`:** the instrument looks for the retired `data-timeline-event` list; markers are now
  `data-timeline-marker` on the chart.
- **12 API issues:**
  - 4 x 3 GETs that 404 on `DE_US_Equity` / `WMB_US_Equity` thesis and peers: the Posture tab's comparable read
    (`PostureTab.tsx:630`, `useThesisBundle(comparableKey)`). It predates this round (the 14:46Z walk on round 27 made the same calls),
    and the comparable has no thesis.
  - 2 x POST 401 `/auth/refresh` after the disarm.
- **`format:money`** (a `$` still somewhere on the page), **`layout:truncated`** (4 labels) and **`design:contrast`** (3 elements):
  left for the L9 read and round 30.
**Judgment items for the L9 read (CVO~Z, on the PNGs):**
- SAUX-15's first-viewport limb: on BA at 1440x900 the tabs start at about y 938, just below the fold.
- The 95-name collage's small-bubble labels (the worker's note).
- Every look-and-feel limb each order's record face names.

## 4. ROWS THIS ROUND

| row | ruling |
|---|---|
| Z-W80-S1 | Resolved by AMENDMENT 1 @77abd61a20. |
| Z-W80-S2 | Admitted (harness stubs). |
| Z-W80-S3 | Records the resolution. |
| Z-W81-S1 | My check's defect: face.cjs reads the estate primary button's white ink as white-on-white, so the worker spelled white `hsl(0 0% 100%)`. Round 30 repair: judge primary ink by its fill and restore the canonical class. |
| Z-W81-S2 | Accepted ("identity as of" prints once). |
| Z-W81-S3 | Round 30 repair: `__rendercheck__/renderCheck.tsx:439` still tests "Back to universe". |
| Z-W83-S1 | Admitted (relative import; the harnesses cannot resolve `@/`). |
| Z-W85-S1 | Admitted. The order's caption clause contradicted itself; the worker followed "a fallback roster never says filing". |
| Z-S17 / Z-S18 | The push gate, disarmed earlier today. |
| Z-S20 | An unknown writer staged a revert of the ~84 records; unstaged; nothing lost. |

**Drain incidents (disclosed):**
- 55546c9c3e carried 8 of COO~Z's staged RESAPP r64 files (safe-merge only WARNs on foreign files). COO~Z confirmed them as its intended
  bytes (msg 28790).
- The first ~85 drain lost its index to a concurrent peer commit and was aborted and redone.
- Every channel conflict was resolved by row union, with no row lost (final 59).

## 5. OPEN -> ROUND 30

- **The FWD-26 presets cell:** LeadPanel / PriceBars / ChatterBubbles, on PRD v0.11. Chatter reads the served `?days=` windows; Price shows
  30D, and 90D/365D render the served "not produced yet" reason.
- **Z-W208-S1:** one served universe per face. The starred join uses the collected rows' ticker, so the chatter-ranking read is dropped.
- **The repair cell:**
  - face.cjs primary-button ink, and restore the canonical class (Z-W81-S1);
  - renderCheck.tsx "Back to universe" (Z-W81-S3);
  - HeaderBrief: a plain title when the feed url is null (COO~Z msg 28802, RESAPP Z-W212-S2), with dayopen.cjs's href clause amended to
    "where served";
  - the walk's `format:money` `$` residue.
- **Pending:**
  - the CTO's product-file review of e370eb7c;
  - the DEV push (0.0.0_AB_MSTR~Z, on Andrew's word);
  - the CVO's L9 read of the walk's PNGs.
