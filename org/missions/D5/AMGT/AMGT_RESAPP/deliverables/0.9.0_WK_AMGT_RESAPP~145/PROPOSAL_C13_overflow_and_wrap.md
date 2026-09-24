PROPOSAL C13 -- overflow, truncation and wrap
AMGT-rm-6, worker 0.9.0_WK_AMGT_RESAPP~145, round 38

STATUS: DRAFT INPUT for 1.0.0_SA_CTO~Z's L4-R ratification. Not applied to portal/DESIGN.md by this
cell (Bound 2). portal at c7b022a1, contract-check instrument at rm-1's re-key (b51330c5, merged
before this cell). Origin: ADJUDICATION_v47 s.2.4 (`org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel
/adjudications/ADJUDICATION_v47.md:100-115`, row AMGT_RESAPP-Z-C-S414) -- a real render defect (the
Lead Panel provenance caption clipped mid-word) that `3.0.0_SA_CVO~Z` could NOT reject on because
`DESIGN.md` carried no clause on overflow, truncation, clipping, ellipsis or wrap (measured 0 hits
across the file for all six terms at that vintage). Round-37 analysis item 6 (amended @18d29a99c7)
routes the CONTENT to the CTO and the INPUT -- this document -- to this cell.

===========================================================================================
1. MEASURED CASES -- THE LIVE PAGE, ALL SIX STATES, BOTH SCOPES
===========================================================================================

Instrument: `portal/scripts/ui-contract-check.mjs --port 5185 --scope main|body --out <dir>`, which
runs `ui-measure.mjs`'s `clippedTextBlocks` classifier (leaf text-bearing elements whose own content
overflows their own clientWidth under `overflow:hidden|clip` or `text-overflow:ellipsis`, read off
the LEAF element itself -- see the classifier's own comment at ui-measure.mjs:149-157) against the six
SecurityAnalysis states (list, thesis, exec, peers, model, posture).

RESULT: 0 clipped blocks on every state, in both scopes, in both runs.

  DENOMINATOR: 24 of 24 measurement JSON files read clippedTextBlocks=0, clippedTextSamples=[]
    - clipped-main/{list,thesis,exec,peers,model,posture}.json       -- scope=main -- 0 each
    - clipped-main/{list,thesis,exec,peers,model,posture}-body.json  -- scope=body -- 0 each
    - clipped-body/{list,thesis,exec,peers,model,posture}.json       -- scope=body -- 0 each (re-run)
    - clipped-body/{list,thesis,exec,peers,model,posture}-body.json  -- scope=main -- 0 each (re-run)
  (the two invocations are redundant by construction -- each always measures BOTH scopes internally
  and prints both tables -- so this is TWO independent runs of the same six-state sweep, not two
  different populations; both agree, 0 in every cell.)

WHY: rm-1's own re-keyed clippedTextBlocks detector is merged, AND rm-5 merged before this cell
(portal DEV 9bcbc290, drained by 2.0.0_SA_COO~Z, worker 0.9.0_WK_AMGT_RESAPP~144) -- the exact
provenance caption ADJUDICATION_v47 s.2.4 flagged is the one rm-5 fixed. So the live measurement is
attributed: NO CASE ATTRIBUTABLE, reason = the one known live instance was remediated by a merged
predecessor cell before this cell ran. Per issuer note 1, this is the EXPECTED outcome and is stated
as such rather than treated as a null result.

===========================================================================================
2. THE HISTORICAL CASE, REPRODUCED FROM HISTORY (never by worktree mutation -- git-show reads only,
   plus the two written artifacts the issuer named)
===========================================================================================

Case A -- Lead Panel provenance caption, pre-rm-5 (portal DEV 1f1555d2, the commit rm-5's own da76356a
supersedes).

  STATE: list.  SCOPE: main (and body -- the Lead Panel sits inside <main> on every route).
  ATTRIBUTED TO: `portal/src/pages/SecurityAnalysis/components/LeadPanel.tsx` (footer content) via
  `portal/src/ui/components/panels/PanelFooter.tsx` (the shared frame).

  TEXT (ADJUDICATION_v47 s.2.4, measured against list.png at that vintage): the caption reads
  `... -- dated 2026-09-23 (requested 2026-09-24) -- t` and stops -- clipped MID-WORD, no ellipsis,
  no visual cue that more text exists.

  CONTAINER'S COMPUTED OVERFLOW / TEXT-OVERFLOW / WHITE-SPACE VALUES, read off the pre-rm-5 source at
  portal 1f1555d2 (`git -C portal show 1f1555d2:<path>`, a read, not a worktree mutation):
    - The leaf holding the text was `<span>{content}</span>` inside PanelFooter.tsx:112/116 --
      NO className at all on that span. No `truncate`, no `overflow-hidden`, no `text-overflow:
      ellipsis`, no `white-space: nowrap` anywhere in its own class list.
    - Its immediate parent (PanelFooter.tsx:106) carries `text-right flex-shrink-0` ONLY when
      `leftContent` is present (LeadPanel.tsx pre-rm-5 line 409 passes
      `leftContent={resolution ? <ResolutionNote .../> : undefined}` -- present whenever the ranking
      query returns a `resolution`, which the list state's own render did in the adjudicated capture).
    - The grandparent (PanelFooter.tsx:97-101) is `flex items-start justify-between gap-4` when
      `leftContent` is present -- an unconstrained flex row with NO `min-width: 0` on the
      `flex-shrink-0` item, so that item takes its max-content width (the browser's flexbox default:
      a flex item's `min-width` is `auto`, i.e. its content size, unless overridden) and is never
      allowed to wrap or shrink.
    - Neither the leaf, its parent, nor its grandparent carries `overflow:hidden|clip` or
      `text-overflow:ellipsis` ANYWHERE in this chain (confirmed by reading all three levels above).

  ATTRIBUTED MECHANISM: NOT a truncate/ellipsis CSS idiom. The overflowing flex item is pushed past
  its panel's edge by `flex-shrink-0` + the browser's implicit `min-width:auto` on a flex child, and
  is then VISUALLY cut by an ancestor's own `overflow` behaviour further up the tree (the panel frame
  / `<main>`'s own `overflow-x-hidden`, the same class of container-level clip `ui-measure.mjs`'s
  own docstring at :152-157 names and deliberately excludes from `clippedTextBlocks` because it is a
  layout device, not a text-clip signal, when read at the CONTAINER level -- but the panel-frame
  ancestor here is genuinely clipping page TEXT, not just measuring a container wider than its row).

  ⛔ INSTRUMENT GAP THIS CASE EXPOSES, FOR THE RECORD: `clippedTextBlocks` reads `overflow-x` /
  `overflow-y` / `text-overflow` off the LEAF element only (ui-measure.mjs:162-163, `const cs =
  getComputedStyle(el)` where `el` is the candidate leaf). A clip produced by flex-sizing on the leaf's
  OWN box plus a hidden-overflow ancestor never sets any of those three properties ON THE LEAF, so this
  exact historical case, reproduced with the pre-rm-5 source, would read `clips = false` and would NOT
  have been counted by the current detector even had it still been live. The detector proves absence of
  the SIGNALLED form (ellipsis/nowrap+hidden on the leaf itself); it does not prove absence of this
  UNSIGNALLED form. C13's grading clause (s.4 below) names this gap rather than overclaiming coverage.

  CORROBORATING ARTIFACT: `0.9.0_WK_AMGT_RESAPP~144`'s own proof-of-spec
  (`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~144/
  AMGT_RESAPP.TO-AMGT-rm-5.the-provenance-disclosure.proof_of_spec.json`, AC2 + `controls.mutant`):
  the fix moved the same string OFF `PanelFooter`'s `content` prop entirely and onto a purpose-built
  `SourceCaption` rendered through `leftContent`, with BOTH lines carrying `whitespace-normal
  break-words` and NEITHER carrying `truncate`/`whitespace-nowrap`/`overflow-hidden`
  (`leadPanelPattern.harness.cjs`'s `source_caption_wraps` check). The MUTANT CONTROL in that record is
  the direct falsifier for "this predicate is load-bearing": re-appending `truncate` to the caption's
  className flipped `source_caption_wraps` from true to false (`CHECKS-WRONG-WAY source_caption_wraps`)
  and nothing else moved; reverted, re-verified identical. That is the harness-level proof that wrap
  vs. clip on THIS element is mechanically distinguishable, which C13's own instrument-grading clause
  (s.4) leans on.

  RELATED, NOT THIS CASE: surprise row `AMGT_RESAPP-W144-S1` (filed by 0.9.0_WK_AMGT_RESAPP~144, still
  UNDER_INVESTIGATION, disarm_owner rm-2 / PanelFooter.tsx's owner) names `PanelFooter.tsx`'s
  `content`-side `flex-shrink-0` wrapper as the likely GENERAL mechanism (confirmed by this cell's own
  read above) for any FUTURE `PanelFooter` caller that still routes long text through the `content`
  (string-only) prop with `leftContent` present -- rm-5's fix routes AROUND it for the Lead Panel only,
  so the wrapper itself is unexercised and unfixed. C13 (s.4) is written to bind that future caller too.

===========================================================================================
3. ESTATE CENSUS -- WHAT THE PORTAL DOES TODAY (portal/src/**, all classes, denominators printed)
===========================================================================================

  truncate            : 97 hits across 59 files   (comp-find, corpus=all, 1016 files scanned)
  text-ellipsis        : 0 hits across 0 files     (MEASURED ZERO over 1016 scanned files;
                                                      the estate uses `truncate`'s implicit
                                                      `text-overflow:ellipsis`, never the bare
                                                      Tailwind `text-ellipsis` utility, as its
                                                      ellipsis idiom)
  whitespace-nowrap    : 64 hits across 35 files
  overflow-hidden      : 121 hits across 69 files  (dominant use: layout/clip-corners on containers,
                                                      modals and chart frames, not caption text --
                                                      confirmed by file list, e.g. `HeroGraphic.tsx`,
                                                      `*Modal.tsx`, chart wrappers)
  break-words          : 4 hits across 2 files     (BOTH inside this project's own rm-5 fix:
                                                      `LeadPanel.tsx` and its harness -- i.e. the
                                                      wrap-safe idiom this proposal generalizes is
                                                      currently a SecurityAnalysis-only pattern, not
                                                      yet an estate-wide one)
  line-clamp-*         : 4 hits across 3 files     (`ExecutiveSummary.tsx` x2, `designTokens.ts`
                                                      `linkTruncate` token, `MacroHeatmap.tsx`)

  Within `portal/src/pages/SecurityAnalysis/**` specifically (the six graded states' own tree, 66
  files scanned): 10 hits across 6 files carrying `truncate|whitespace-nowrap|overflow-hidden|
  line-clamp` --
    - `ProvenanceLine.tsx:61`            `truncate` on `figure.basis.mnemonic` (a short fixed-format
                                          code, e.g. an accounting mnemonic -- an IDENTIFIER, not a
                                          disclosure sentence)
    - `RankedList.tsx:246-247`           `truncate` on `row.ticker` and `formatMetric(row)` (ticker
                                          symbol and a formatted number -- both short, bounded tokens)
    - `ExecManagementTab.tsx:115`        `whitespace-nowrap` on a `<td>` (`officer.role_start`, a
                                          short date/dash value)
    - `ModelTab.tsx:282`                 `whitespace-nowrap` on a `<td>` (`row.label`, a short model
                                          row label)
    - `PostureTab.tsx:277`               `overflow-hidden` on a rounded card FRAME (a layout device --
                                          clips corners, not text)
    - `LeadPanel.tsx` / its harness      `break-words` -- the rm-5 fix itself (s.2 above)

  READING: the estate's EXISTING practice already draws the line this proposal names, informally and
  inconsistently: short, bounded IDENTIFIERS and table-cell VALUES are truncated/nowrapped (tickers,
  mnemonics, short labels, short dates) and none of the 24 measured cells shows any of them actually
  clipping content live; the one place a FACT-BEARING, variable-length DISCLOSURE sentence was routed
  through a truncate-capable frame (`PanelFooter`'s `content` prop) is the one place it clipped, and
  the fix was to stop truncating it, not to shorten it. C13 below states this distinction as a rule
  rather than leaving it as an accident of which components happen to carry which class.

===========================================================================================
4. DRAFT CLAUSE -- C13, IN DESIGN.MD'S OWN VOICE (register read off C10-C12; NOT applied to the file)
===========================================================================================

C13. **Overflow, truncation and wrap.**
- **A fact-bearing line never clips.** Any text that discloses a fact the viewer relies on --
  a provenance caption, a generation timestamp, a data-quality disclosure, an error message, a
  resolution note, anything a viewer would need the FULL text of to trust or act on the panel --
  renders with `whitespace-normal break-words` (or the platform's equivalent wrap-safe pairing) and
  carries no `truncate`, `whitespace-nowrap`, `overflow-hidden` or `text-overflow: ellipsis` on itself
  OR on any ancestor between it and its panel frame. Where the panel is too small for it, the PANEL
  grows or the line wraps to a second line -- the fact is never partially withheld. Exception: none --
  a disclosure that does not fit is a layout defect, not a truncation candidate.
- **A short, bounded identifier or value MAY be truncated with a visible ellipsis.** A ticker symbol,
  an accounting mnemonic, a short fixed-format code, or a table-cell value whose full form is available
  on hover/focus or by opening the row's own detail, may use `truncate` (or `line-clamp-N` for a
  multi-line card excerpt). The full text is reachable another way -- a `title` attribute, a tooltip,
  or the record's own detail view -- never simply gone. This is the estate's existing practice (C.3
  above: `ProvenanceLine.tsx`'s mnemonic, `RankedList.tsx`'s ticker and metric) and this clause ratifies
  it rather than changing it.
- **A table cell defaults to `whitespace-nowrap` for short, single-token values** (a date, a short
  label, a status word) so the column stays legible; a cell whose value is prose (a note, a reason, a
  description) wraps instead and the column is sized for it. Never `truncate` a table cell that carries
  a reason or a note -- that is a disclosure by C13's first bullet, not a value.
- **`overflow-hidden` on a FRAME (a rounded card, a chart canvas, a modal, `<main>` itself) is a layout
  device and is unrestricted by this clause** -- it clips corners and canvas bounds, never a leaf's own
  text content. Where a frame's `overflow-hidden` sits BETWEEN a fact-bearing leaf and the page edge
  (PanelFooter.tsx's `flex-shrink-0` content wrapper is the estate's one known instance, surprise row
  `AMGT_RESAPP-W144-S1`), the leaf's own wrap-safe classing (bullet 1) is what prevents the frame from
  ever clipping it -- the frame is not required to change, the leaf's sizing is.
- **What the instrument grades, and its known limit, stated so the limit is not silently inherited by a
  future reader:** `ui-contract-check.mjs`'s `clippedTextBlocks` (0 required on every graded state) is
  the SIGNALLED-clip detector -- a leaf carrying `overflow:hidden|clip` or `text-overflow:ellipsis` on
  ITSELF whose content overflows its own box. It is the correct instrument for bullet 2's permitted
  ellipsis idiom (which must be signalled to be legal under this clause) and does NOT by itself prove
  bullet 1's promise for an UNSIGNALLED clip produced by flex/box sizing plus an ancestor's
  `overflow-hidden` (s.2 of this proposal's history). A candidate whose panel changed and whose text is
  fact-bearing is read against a full-width render at the panel's own minimum width as well as graded
  by the instrument, until an ancestor-aware detector variant exists.

===========================================================================================
5. CLOSING TABLE -- MEASURED CASE -> WHAT C13 SAYS
===========================================================================================

  Case                                            | State(s) | Live?  | C13 rule that governs
  -------------------------------------------------|----------|--------|----------------------------------
  Lead Panel provenance caption, pre-rm-5          | list     | FIXED  | Bullet 1 (fact-bearing, never
  (mid-word clip, unsignalled -- s.2 above)        |          | (rm-5) | clips) -- rm-5's `SourceCaption`
                                                    |          |        | is the FIRST conforming instance
  Lead Panel provenance caption, post-rm-5         | all six  | 0      | Bullet 1 -- wraps, 0 clipped
  (current state, measured s.1)                    |          | clipped| blocks measured; sets the pattern
  `ProvenanceLine.tsx` mnemonic truncate           | thesis   | 0      | Bullet 2 (bounded identifier,
                                                    |          | clipped| ellipsis-eligible) -- conforms
  `RankedList.tsx` ticker / metric truncate        | list     | 0      | Bullet 2 -- conforms
                                                    |          | clipped|
  `ExecManagementTab.tsx` / `ModelTab.tsx`         | exec,    | 0      | Bullet 3 (table-cell nowrap for
  `<td>` whitespace-nowrap                         | model    | clipped| a short value) -- conforms
  `PostureTab.tsx` card frame overflow-hidden      | posture  | n/a    | Bullet 4 (frame device, not
                                                    |          | (not  | leaf text) -- conforms, no leaf
                                                    |          | text) | routed through it
  `PanelFooter.tsx` `flex-shrink-0` content wrapper| (any     | ARMED, | Bullet 4's exception clause +
  (surprise row AMGT_RESAPP-W144-S1)               | future   | unex-  | bullet 1 -- future caller must
                                                    | caller)  | ercised| wrap-safe its own leaf; disarm
                                                    |          |        | owner rm-2
  Detector's leaf-only scope vs. an ancestor-caused| n/a      | n/a    | Bullet 5 -- named as a stated
  unsignalled clip (this proposal's own finding)   |          |        | instrument limit, not silently
                                                    |          |        | inherited

-- 0.9.0_WK_AMGT_RESAPP~145
