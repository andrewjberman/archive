# Security Analysis (AMGT_RESAPP) -- DESIGN_SPEC.md

**Owner:** `0.9.0_WK_AMGT_RESAPP~1` (AMGT-s-5, THE PRINT RENDERER cell)
**Status:** Pending approval (gate -- no `.tsx` files written until approved; the F10 precedent's
own gate, `portal/src/pages/SecurityScanner/DESIGN_SPEC.md`, states the identical rule)
**Project:** AMGT_RESAPP, directive D5 Alternative Research
**Precedent followed:** `portal/src/pages/SecurityScanner/DESIGN_SPEC.md` (F10; read from a
sibling checkout at commit `30ca034bbaa4b9d2864d3acce826e3c2fa59be0a` -- see the surprise row
this deliverable cites for why this worktree's own gitlink could not be read directly; the file's
560-line count matches the task order's own citation exactly, giving confidence the content is
the same one F10 describes)
**Date:** 2026-09-10

---

## 1. Design Principle

Security Analysis follows the F10 (SecurityScanner) precedent's own discipline: reuse the
estate's shared layout primitives (`PageHeaderCleanBadge`, `TabNavigation`/`useTabNavigation`,
`Panel`/`PanelHeader`/`PanelContent`, `ErrorBoundary`) and write new components ONLY where no
shared equivalent exists. Every deviation from a shared pattern is documented in this file with a
reason, exactly as F10 requires of itself (F10 section 1).

**Canvas law binds unchanged** (`portal/CLAUDE.md`, read at the same vintage as the F10 file
above): the page canvas is light silver: dark text only, directly on the canvas. The white-text
idiom (`text-white/N`, ghost fills) is legal ONLY inside a dark container (`Panel
variant="chart"/"mixed"`, `PanelHeader`, `DarkCard`, `NestedCard`, `SectionCard`) -- every panel
section below composes inside one of those containers, never loose on the canvas. This is stated
once, here, rather than repeated per surface section.

**Every displayed number on this page carries its vintage** (the estate's general rule, restated
by every wire cell's own section below): a value with no "as of" timestamp beside it is never
rendered as if current. This is the single cross-cutting rule every S1-S15 section below assumes
without re-deriving it.

---

## 2. Header Panel

Analogous to F10's `ScannerHeaderPanel` (sticky, between the page title and the tab bar). Shows,
for the security currently open:

- **Ticker** and **company name** -- from AMGT-s-1's landed `model_block.json` (`security`
  field) via AMGT-s-12's identity layer for resolution when the page is reached by a route other
  than a direct Bloomberg ticker.
- **Bloomberg session-state indicator** -- REQUIRED to be visible (this cell's task text: "PART V
  says the session's state must be VISIBLE to the user"). A three-state badge, plain text is
  sufficient at this cut (color/icon is a later `.tsx` decision, not fixed here):
  - `BLOOMBERG: CONNECTED` -- the box-side pull that feeds this page's data last ran with
    `dapi_check.py` reporting `DAPI: UP` (AMGT-s-1's own pre-pull check).
  - `BLOOMBERG: SIGNED OUT` -- the last recorded pull attempt found the terminal signed out
    (`integrations/bloomberg/READ_HERE.md` section 1's most common failure). The page still
    shows whatever data was last successfully landed, dated with ITS OWN vintage -- a signed-out
    terminal does not blank the page, it only means no FRESHER pull has landed since the dated
    vintage shown (C-MARK-NOT-DEGRADE: a stale connection is a stated fact, not a blank).
  - `BLOOMBERG: UNKNOWN` -- no health check has ever been recorded for this security (never
    rendered as `CONNECTED` by default; an unknown state is its own state, not assumed-good).
- **"as of" vintage for the header block itself** -- the timestamp on the header figures
  (`CUR_MKT_CAP`, `PX_LAST`, etc.), per AMGT-s-3's provenance fragment for the `scope: "header"`
  figures.

---

## 3. Tabs / Page Shell

One page, tab bar below the header panel (mirrors F10's shell composition order: page header ->
sticky header panel -> tab bar -> tab content). Proposed tabs, each corresponding to one or more
manifest surfaces (grouping is this section's own call; the surfaces themselves are S1-S15
below, and every one of them appears SOMEWHERE on the page, per section 4):

| Tab | Surfaces shown |
|---|---|
| Model | S1 (figures), S3 (provenance beside them), S10 (check-face verdicts), S11's effect (qualification outcomes, not the rules themselves) |
| Coverage | S4 (news/IR coverage reader), S13 (social feed) |
| Peers | S8 (peer set) |
| Drafting | S9 (generated prose sections) |
| Freshness & Lists | S7 (coverage-freshness view), S14 (input ledger), S15 (list-health panel, per its own section below) |
| Print | S5's own print path (section "Print Path," below) |

S2 (on-demand pull) and S6 (version store), S12 (identity layer) do not get their own tab --
S2 is a page-level AFFORDANCE (a ticker box that can appear on any tab), and S6/S12 are backend
engines with no direct tab of their own; sections S2, S6 and S12 below say exactly what a reader
sees for each, never inventing a tab that does not correspond to a manifest row's own claim.

---

## 4. ONE SECTION PER SURFACE, S1 through S15

### S1 -- The Model Block

**What the page shows:** the figures AMGT-s-1 landed (`model_block_<security_key>.json`) --
header scalars in the Header Panel (section 2) and fiscal-year line items in the Model tab, one
row per fiscal year, one column per mapped mnemonic. Every figure renders with its provenance
fragment (S3) beside it and its check-face verdict (S10) as the figure's visual state.

**UNRESOLVED / FAILED / HELD BACK:**
- A field AMGT-s-1's field map could not resolve a unit for on this security (recorded as the
  `SEE field_map.json ...` placeholder in the figure's `unit`) renders via S10's REFUSE state:
  `[REFUSED: <reason>]` in place of the value -- never the raw number with an unlabelled unit.
- A security AMGT-s-1 has not yet pulled (not one of the covered names landed so far) shows a
  page-level "not yet pulled" state for the whole Model tab, not a partially-empty table.
- "Fetching now" does not apply to S1 directly -- the box-side pull is not triggered by opening
  this page (it is AMGT-s-2's surface, below, that is triggered by a page action).

### S2 -- The On-Demand Pull

**Status at this cut:** design-only (decomposition: "OPEN (design)"); no worker face nor artifact
has landed for this cell as of this document. This section is written from the PRD's own manifest
row (S2: "a name outside coverage, by ticker... the page states it is fetching now;
`C-VENDOR-EGRESS`") and the decomposition's own note ("FIRST deliverable: THE SEAM DESIGN...
SECOND: the build on the approved design") -- it states the REQUIRED BEHAVIOUR this page must
show, not a schema AMGT-s-2 has not yet minted (inventing one here would be exactly what this
cell's own bound forbids: "a missing [SPEC_SECTION] is noted as a gap in the spec, never
invented").

**What the page shows:** an affordance (a ticker input, placement TBD by the eventual `.tsx`) that
lets a reader request a name outside the covered set. On submit:
- **"fetching now"** -- a visible in-progress state (AMGT-s-2's own status object, once it exists,
  is what this state reads from) for as long as the box-side pull is running. This is the ONE
  state this cell's own task text calls out by name for S2 specifically.
- **FAILED** -- if the seam (browser -> AWS -> the loopback-only box) cannot be crossed (no route
  exists today, per the decomposition's own plane note: "the estate has no precedent" for this
  seam), the page states that plainly rather than spinning forever or silently doing nothing.
- **HELD BACK** -- until AMGT-s-2's seam design is itself approved and built, this entire
  affordance is either absent from the page or visibly disabled with a stated reason ("on-demand
  lookup: design pending approval") -- never a control that looks live but does nothing.

### S3 -- The Provenance Face

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~1/SPEC_SECTION_provenance.md`
(this same worker, cell AMGT-s-3):*

**What backs this section:** `lib/research/provenance/schema.json` is the data contract every
figure on the page must satisfy before it is eligible to render at all: `source`,
`basis.mnemonic`, `basis.definition`, `vintage`, `unit`, `sign` all present and non-empty.
`lib/research/provenance/validate.py` is how a consumer checks a landed `model_block.json` against
that contract before trusting it. `lib/research/provenance/render_print.py` is the reference
implementation of the print-path text below.

**Beside every figure, always:** the **value** and its **unit** (in the unit the record actually
states for THAT figure on THAT security -- never a page-wide default); the **basis** (the vendor
mnemonic and Bloomberg's own definition of it, never a paraphrase and never another vendor's
normalization reconstructed to look like it); the **vintage** (when this figure was derived); the
**source** (which vendor/instrument answered).

**Reference text** (`render_print.render_figure_line()`, verbatim): value, unit, mnemonic,
definition, "as of" vintage, source, bullet-separated -- see
`provenance_render_<security_key>.md` in this same deliverables folder for the exact rendering.

**On hover:** the full line above is the tooltip content for every figure -- never a shortened
version.

**In the printed pack:** the same line, printed beside (not instead of) the number, grouped by
header scalars first, then by fiscal year.

**When a unit could not be resolved -- MARK, NEVER DEGRADE:** the literal marker
`[UNRESOLVED UNIT]` in the unit's place -- never a blank, never a silently-dropped row. Measured
example: `BA US Equity`'s `IS_DIV_PER_SHR` carries this marker on all ten fiscal years (Boeing's
dividend suspension put a zero in the field map's sampled year); `SAP GY Equity` and
`BABA US Equity` carry a real resolved unit for the identical mnemonic.

### S4 -- The Coverage Reader (non-SA sources)

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~3/SPEC_SECTION_coverage.md`
(`0.9.0_WK_AMGT_RESAPP~3`, cell AMGT-s-4):*

**What AMGT-s-4 hands the page:** per security, one `coverage_items_<security_key>.json` --
ranked items (recency desc, then mentions desc), each carrying `admitted: PASS|REFUSE|PROVISIONAL`
and a `rule_reason`, plus an `identity_dropped` list for items whose source's identity key was
UNRESOLVED.

**Rendering rule for `admitted` -- say the state, never hide it:**
- `PASS` -- rendered plainly, full weight in the list.
- `PROVISIONAL` -- rendered, with a visible marker carrying `rule_reason` on hover/expand --
  never hidden and never rendered identically to `PASS`. This is the honest majority state today
  (AMGT-s-11's item rule is `held_back`, no threshold yet).
- `REFUSE` -- NOT rendered in the main list (optionally an "excluded" affordance so the count is
  auditable) -- never silently dropped from the underlying JSON.

**The three source classes today:** `publication` (fixtures only, no live SERP word yet);
`ir` (zero items today -- `ir_domain` UNRESOLVED for every one of the 89 names); `sa` (zero keys
today -- AMGT-s-b4's one attempt failed at the proxy's TLS layer, an infrastructure fact, not a
code fault). Each class's honest empty/absent state is stated plainly, per the section's own
text, rather than an empty list a reader cannot distinguish from "nothing was ever written."

**The unscoped pass:** `reader.check_no_shared_item_sets()` REFUSES the whole run if any two
securities carry an identical attached item set (the F6 shape, moved to this layer). A stale or
missing `coverage_items_<key>.json` renders as "coverage not available this cycle," never a
silent fallback to a previous run.

*(Row S4 also carries `AMGT-s-b4`, THE SEEKING ALPHA BACKEND: at this cut, released from its
Andrew-hold but its one live attempt failed at the proxy's TLS handshake -- see S4's own `sa`
class above. `AMGT-s-b4` is not scheduled or served in production per `C-SA-VENDOR-WORD`; the
page's SA-class coverage items read "no Seeking Alpha content landed yet" until that changes.)*

### S5 -- The Print Renderer (this cell)

**What the page shows:** a "Print" action (placement TBD by the eventual `.tsx`) that, when
activated, requests the server-side PDF this cell's second deliverable produces
(`lib/research/print/render_pack.py`) and previews it in a modal -- the MODAL ITSELF is `.tsx` and
is HELD on this spec's approval (C-DESIGN-SPEC-FIRST). The PDF generation is buildable now and is
this cell's own artifact (`pack_<security_key>.pdf`, this deliverables folder).

**UNRESOLVED / FAILED / HELD BACK:** the print action is disabled (with a stated reason, "print:
design pending approval") until this spec is approved; once approved and the modal exists, a PDF
render failure states so in the modal rather than showing a blank preview.

**"Fetching now":** the modal shows a generating/loading state while the server-side render runs
(the same discipline as S2's fetching-now state, applied to a render instead of a vendor pull).

See "Print Path" (section 5, below this surface list) for the artifact's own structure.

### S6 -- The Version Store

**What the page shows:** nothing directly -- `opal-data-research` is backend infrastructure (an
S3 bucket), not a UI surface. Every number this page renders that originated in S1's pull reached
the page BY WAY of this store (raw landed before derived, STORE_CONTRACT.md's own grammar), but
the store's own keys/prefixes are never exposed to a reader. This is a stated absence with a
reason, not an oversight: S6's claim ("snapshots ACCUMULATE, never overwrite; raw before derived")
is a correctness property of the PIPELINE, and the page's job is to show its OUTPUT (S1's figures,
their vintage) rather than its mechanism.

### S7 -- The Coverage-Freshness View

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~7/SPEC_SECTION_freshness.md`
(`0.9.0_WK_AMGT_RESAPP~7`, cell AMGT-s-7):*

**One place, one list:** every row of `coverage_freshness.json["rows"]` renders as ONE list, in
ONE place -- not a per-name detail view, not a tab, not a folder tree.

**Sort order: stale-first.** Sorts by `last_refreshed` ascending with `"NEVER"` at the TOP.

**`NEVER` is a state on the list, never its own row and never a blank** -- same columns, same
list, same sort participation; the word `NEVER` (or "never refreshed") appears in the date column
exactly where a date would otherwise appear.

**The rot signal sits beside the list, not apart from it** -- one of three honest states in the
SAME column (an actual signal, "no rot entry for this name at this vintage," or "no rot signal at
this vintage"); none is an error to the reader.

**Per-input clocks** (`bloomberg`, `seekingalpha`, `serp` at this vintage) are a secondary,
expandable detail, not the headline list.

**`security_key` may be absent** -- the row still appears, with every clock reading `NEVER`.

**Generation is on demand, never a running process** -- `generated_at` is the one page-wide
freshness-of-the-view timestamp; `G-20` (the alerting moratorium) means nothing here schedules
itself.

### S8 -- The Peer Set

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~4/SPEC_SECTION_peers.md`
(`0.9.0_WK_AMGT_RESAPP~4`, cell AMGT-s-8):*

**What the panel shows:** one `peer_set` record per security, exactly three possible `basis`
values, never a bare list with no basis attached:
- `basis: "analyst"` -- an analyst-entered set, badged "analyst-entered."
- `basis: "derived"` -- the engine's own comparability test (same classification field, market
  cap 0.2x-5x band), badged "derived," with the exact `test` string on hover/expand.
- `basis: "absent"` -- **no table.** The `reason` string renders verbatim in ordinary body text.

**Why every panel reads `absent` today:** a `derived` set additionally needs a candidate universe
(other covered names classified by the same field) -- classifying the research universe is itself
an unspent quota decision (F2). All three securities AMGT-s-1 has landed read `absent`, with the
reason naming that quota decision by name.

**The measured defect this bar answers:** 48 of 54 one-pager workbooks in the research corpus
carry a stale, unmodified telecom peer set (F6) -- the corpus is never a source of truth for this
panel; neither the engine nor its shared-defect guard opens a workbook.

**Every record carries `vintage`**, including an `absent` reading.

### S9 -- The Drafting Face

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~3/SPEC_SECTION_drafting.md`
(`0.9.0_WK_AMGT_RESAPP~3`, cell AMGT-s-9):*

**Three rendering consequences of FWD-9's bar:** every machine sentence is visually distinct from
firm-authored text AT A GLANCE (no hover/click required to discover it); the evidence sits BESIDE
the sentence, not behind a separate link; the page must INVITE EDITING (an edit affordance on
every machine sentence, not just theoretically available).

**Five sections always present, in order:** company description, investment thesis, risks, CEO
bio, recommendation. **An empty `sentences` array is a real, honest state** -- a visibly
empty/placeholder limb an analyst can fill by hand, never a missing block that looks like a
rendering bug.

**The marking, concretely:** `generated: true` -> a persistent visual marker on every machine
sentence, never on firm text; `evidence` -> rendered adjacent (an id that does not resolve is a
page defect, never a silent blank); `quoted_spans` -> a quotation treatment distinguishing lifted
text from connective prose; `verbatim_check` -> NEVER shown to the reader as a value (its only
visible effect: a REFUSEd sentence never appears at all).

**What is NOT resolved yet:** `company_description`, `ceo_bio` and `recommendation` render EMPTY
today for every security (no figure or coverage evidence resolves for them yet) -- shown as
"not drafted yet, add your own," identical in shape to the machine-sentence editor but starting
blank.

### S10 -- The Check Face

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~8/SPEC_SECTION_checkface.md`
(`0.9.0_WK_AMGT_RESAPP~8`, cell AMGT-s-10):*

**Three states, at a glance, none of them a blank/zero/absent row:**
- `PASS` -- the value, plain.
- `REFUSE` -- `[REFUSED: <reason>]` REPLACING the value -- looks deliberately BROKEN (FWD-10's
  bar: a failed check is VISIBLE as failed, not merely logged).
- `PROVISIONAL` -- the value WITH `[PROVISIONAL]` beside it -- looks normal but flagged, a
  DIFFERENT visual marker than REFUSE so the two never read the same at a glance.

**Measured, on the three real blocks AMGT-s-1 landed:** SAP GY Equity 203/203 PASS, 0 REFUSE, 0
PROVISIONAL; BA US Equity 179 figures, 169 PASS, 10 REFUSE (all `IS_DIV_PER_SHR`, the unresolved-
unit case S1/S3 also name), 0 PROVISIONAL; BABA US Equity 196 figures, 93 PASS, 0 REFUSE, 103
PROVISIONAL (all carrying a `currency_caveat` -- the reconciliation gap this project's own field
map recorded).

**The value is never lost:** a REFUSE's underlying value stays in `check_face.json` beside the
verdict and reason -- the page exposes it on hover/expand, never as the headline figure.

### S11 -- The Qualification Rules

**What the page shows:** no dedicated tab -- these are BACKEND RULES (one per class: a figure, a
peer, an identity, a news/social item, a source, a generated sentence), and the page shows their
EFFECT, not the rules themselves. Concretely: S10 (a figure's PASS/REFUSE/PROVISIONAL badge) is
the figure-rule's effect; S4/S13's `admitted` field is the item-rule's effect; S9's
`verbatim_check`-gated visibility is the sentence-rule's effect; S8's `basis` field is the
peer-rule's effect. `rule_reason` (wherever it appears above) is this surface's OWN CONTENT,
surfaced inline rather than in a separate "rules" page.

**UNRESOLVED / HELD BACK:** a rule that is `held_back` (no threshold, no distribution yet -- e.g.
the social item rule per S13, below) means every item it governs renders PROVISIONAL, never a
confident PASS, until the rule's own cell produces the distribution its threshold is drawn from.

### S12 -- The Identity Layer

**What the page shows:** no dedicated tab -- this is the ROOT that resolves which Bloomberg
ticker, SA symbol, IR domain and social account correspond to one company. Its effect surfaces in
the Header Panel (S2's ticker/company resolution) and everywhere a cross-reference between two
sources is drawn (S4's `identity_dropped`, S13's account-official badge).

**UNRESOLVED:** an identity key that is `UNRESOLVED` (today: `sa_symbol` INFERRED-at-best for US
names only, `ir_domain` and `social_account` UNRESOLVED for all 89 covered names) means the page
never shows that cross-reference as if confirmed -- two sources are never shown together until
resolved; where they cannot be, the page SAYS SO (the identity layer's own `render_together()`
rule, mechanically: it REFUSES to render an UNRESOLVED dependency alongside a resolved one).

### S13 -- The Social Feed

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~6/SPEC_SECTION_social.md`
(`0.9.0_WK_AMGT_RESAPP~6`, cell AMGT-s-13):*

**What the panel shows:** a "Social Discussion" panel, one per security, listing admitted
`social_items` -- platform, handle, the account's official status (`MEASURED`/`INFERRED`/
`UNRESOLVED`) as a small badge, post text, timestamp, link, and the item rule's verdict badge
(`PASS` green / `PROVISIONAL` amber / `REFUSE` never rendered as a row).

**The disclosure line's placement:** `source_line` renders as a single small-print line directly
under the panel header, above the first item row -- not a footnote, not collapsed behind a
tooltip. At this account: *"general-social plus finance-adjacent; the cashtag-native venue
(StockTwits) carries 0 datasets on this account."*

**C-RULE-MUST-EXIST -- held back:** the item rule is `held_back` at this cut (no threshold, no
distribution -- the measurement that would produce one has not been triggered, G-24). Until then,
every admitted item carries `admitted: PROVISIONAL`, never a hard `PASS`, and the panel's held
state reads: *"Social discussion measurement not yet triggered ... No feed is shown until
Andrew's per-use word arrives and the first measurement runs."*

### S14 -- The Input Ledger

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~7/SPEC_SECTION_ledger.md`
(`0.9.0_WK_AMGT_RESAPP~7`, cell AMGT-s-14):*

**One row per class, three columns, always six rows:** `market_data`, `filings`, `news`,
`social`, `web`, `sa` -- never fewer, never a row that only appears once something has run.
Columns: source, last run, outcome.

**THREE states per row, not two:** **NOT WIRED** (`stage is None` -- today: `filings`, `news`,
`social`, `web` -- no button, the row says "not wired yet"); **WIRED, NEVER RUN** (the re-run
control IS present; last-run/outcome read "never run"); **WIRED, HAS RUN** (an entry exists; the
re-run control is present and enabled).

**One re-run control per row, and it calls exactly one class** -- FWD-12's own bar rules out a
"refresh all" control explicitly: *"A single button that refreshes everything under one
timestamp does not count."* Pressing one row's control changes ONLY that row's two remaining
columns; every other row stays byte-for-byte the same.

**Deliberately not built:** no schedule, alarm or automatic re-run of any class (`G-20`).

### S15 -- The List Register

*Folded in verbatim from `deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/SPEC_SECTION_lists.md`
(`0.9.0_WK_AMGT_RESAPP~5`, cell AMGT-s-15):*

**Where: inside S7's coverage-freshness view, not a new tab.** The two owned lists
(`publishers`, `social_accounts`) are not per-name data, so a small "List health" panel renders
above or beside S7's per-name table, from `rot_signal.json` on every page load (a normal GET of a
static/generated artifact -- never a poll or subscription).

**One row per owned list**, each showing: the owner (today, literally
`"UNASSIGNED -- Andrew names the owner (C-NO-CONTACT: not Adam's team directly)"`, never a
placeholder name, never blank -- `C-LIST-OWNER`); `entries_stale of entries_total stale (>N
days)` plus, for publishers, `unresolvable_count`; `computed_at` (the rot check's own vintage).

**Never a live check:** no button that triggers a fetch, no auto-refresh timer, no alert state
(a coloured badge on an already-open page is not an alarm; `G-20` still binds).

---

## 5. Print Path

Adam's artifact (this cell's second deliverable). `lib/research/print/render_pack.py` assembles,
for one security, a PDF reproducing the template's four blocks (F1: pasted Excel model block /
RECOMMENDATION + COMPANY DESCRIPTION / THESIS | RISKS / bio), from:

1. AMGT-s-1's landed `model_block_<security_key>.json` (the figures, for the model block);
2. AMGT-s-3's provenance fragment (`render_print.render_figure_line()`), so every figure in the
   PDF carries its basis/vintage/source exactly as the page would show it (S3, above);
3. **placeholders** for every section no drafting/coverage/bio engine has filled yet (today, all
   of them -- S9's own section says company_description/ceo_bio/recommendation render empty),
   each placeholder MARKED as machine-empty (`[MACHINE-EMPTY: <what belongs here>]`) -- never a
   blank page that looks finished, and never invented prose.

The PDF is server-side and buildable NOW (no `.tsx`, no portal write). The MODAL that previews it
inside the page is `.tsx` and is HELD on this spec's approval, per C-DESIGN-SPEC-FIRST -- see
S5, above.

**The template is a floor, not the pack:** reproducing the four blocks is the skeleton; the
analyst-specific sections (thesis, risks, recommendation, bio) are the actual value this project
drafts toward, and a render that stops at the skeleton has not reached FWD-5's bar on its own --
FWD-5's EXERCISED bar ("Adam has actually forwarded one") is Adam's to clear, not this cell's.

---

## 6. Approval

This design is not approved by anyone on this project's execution chain -- the approval is not
this cell's to give and not its issuer's.

Approved by: _______________________ on _______________________
