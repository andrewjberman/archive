# DRAFT -- NOT ISSUED. Target path at issuance: org/missions/D8/MDPF/MDPF_CANON/task-orders/MDPF_CANON.TO-CN-i-1.aua-trend-grouping.md
# Round 7 (FWD-9, PRD v2.12). The checks move from round7/draft/checks/ to round7/checks/ (same names) at issuance. Written by a fork of 2.0.0_SA_COO~D1, 2026-10-13 ~19:5xZ.
# THIS DRAFT CUTS "VARIANT A" -- the part of FWD-9 that is implementable under the CTO's rulings (msg 5071) with FIELD READS and no new served key.
# The Client Supervised / Unsupervised chips and the full ETF Strategies group are NOT in it: see ISSUER NOTES, FORKS 1-3. The issuer rules before this is cut.

# MDPF_CANON task order -- `CN-i-1` -- THE AUA TREND GROUPS ITS CUSTOM MODELS INTO ONE SERIES AND NAMES ITS ETF AND ALT BANDS IN THE TOTAL ASSETS COLOURS (FWD-9; PORTAL DEV CANDIDATE)

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_CANON/decompositions/MDPF_CANON_DECOMP.md</decomp_doc>
<owned_cells>CN-i-1</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_MDPF_CANON~18</issued_to>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no cron, alarm, monitor or cadence is added or changed; one page and one pure module.
comp-iam: DECLARED-NOT-APPLICABLE -- no AWS; the page reads series the served global object already carries.
comp-adversary: RUN by the issuer (2.0.0_SA_COO~D1) on DELL1 at the shared tree -- `r7_cn_i_1.py module` reads 0 of 1 (the module is absent), `page` 0 of 5 at base; the reference patch reads 6 of 6 and 5 of 5; three mutants (a null coalesced to 0; a hex literal beside a group label; a grouping that is not Global-gated) turn M2, P5 and P4 red; `data` reads 3 of 3 on the real served objects (a control: it grades the rule, not the page).
EGRESS CLASS, declared: NONE (the worker reads no AWS and writes none).
</preflight>

**Your worktree:** the spawn names it (outer branch `wk-MDPF_CANON-18`, cut from the issuance commit). The portal is a NESTED repository at
`<worktree>/portal`, provisioned on its own branch `wk-MDPF_CANON-18-portal` cut from portal `DEV` (the issuance names the ref) with `node_modules`
linked. Start every shell call with `cd` into the outer worktree path: a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base
checkout. All three existing files use CRLF line endings: keep them, and confirm with `git -C portal diff --stat` that the diff is a few dozen lines.

## 1. THE ACT -- `CN-i-1` (round 7)

THE REQUIREMENT (Andrew, 2026-10-13 ~18:4xZ, PRD v2.12 FWD-9). On Model Portfolios > AUA TREND ANALYSIS, Global view, the trend lists about 17 series.
He wants the custom models as ONE series, "Custom Models", in the colour the Total Assets card uses for Custom, and the ETF and ALT strategy bands named
and coloured as the Total Assets card names and colours them. The five canonical Opal models stay as their own series. The CTO ruled (msg 5071): group
IN THE COMPONENT, reusing the ONE Total Assets colour export; no back-cast, no interpolation, no new served key; "Custom Models" REPLACES the fold's
`other_models` series.

WHAT THE PAGE DOES TODAY (`portal/src/pages/ModelPortfolios.tsx`, anchors at HEAD; verify each before you edit):
- the Global series are built client-side from the served `by_model` (`:782-856`): every key whose `cohort_class !== 'sma'`, named by
  `getCanonicalModelName(display_name)`. After the fold (deployed 2026-10-13) the served global `by_model` holds the five core models and ONE
  `other_models` line (display name "Other Models") for the custom models, emitted only on dates two firms hold it; before the fold's first fire it
  still holds the individual custom lines. Both shapes must work.
- the 50/50 blends are rolled into their archetype models by `rollBlendsIntoArchetypeSeries` (`:171`, used in the `timeSeriesData` memo at `:854-857`).
  Leave that function and the Total Holdings / donut rollups alone.
- the mount list is `STACK_SERIES` (`:146-157`), a closed literal mounted in registration order; extras are appended before `non_model` by
  `trendStackSeries` (`:888-896`). The two additive bands are `sma_additive` (label 'Additive SMA sleeves') and `tax_additive` (label 'Tax-Managed SMA'),
  Global only, fed by `sma_additive_aua` and `tax_additive_aua` (CN-d-3; do not change how they are read).
- colours: `getModelColor(label)` (`src/lib/modelPortfolioColors.ts`) at the legend (`:1146`, `:1157`, `:1160`), the bars (`:2003`) and the areas
  (`:2239`). The Total Assets card colours its buckets by NAME from `L1_COLOR` in `src/components/CategoryViewTree.tsx:87-95`
  (`Custom` fuchsia500, `ETF Strategies` cyan400, `ALT Strategies` green400); `L1_COLOR` and `l1ColorOf` (`:96`) are module-private today.

THE EDIT, three files:

### 1a. `portal/src/components/CategoryViewTree.tsx` -- export the palette, change nothing else

At `:87` `const L1_COLOR` becomes `export const L1_COLOR`; at `:96` `const l1ColorOf` becomes `export const l1ColorOf`. No logic, no value, no other line
moves. The page imports `l1ColorOf` from here; it must NOT copy the table.

### 1b. NEW `portal/src/lib/trendGrouping.ts` -- a pure module, imports nothing

```ts
export interface TrendPoint { period: string; aum: number | null; pointClass?: string }
export const CUSTOM_MODELS_LABEL = 'Custom Models'
export function groupCustomModelsSeries(
  byModel: Record<string, TrendPoint[]>,
  canonical: ReadonlySet<string>,
): Record<string, TrendPoint[]>
```

Behaviour, exactly: keys in `canonical` pass through UNCHANGED (the same array object); every other key is a member; when there are no members the result is
the canonical keys only (no group key is invented); otherwise the result also holds ONE key `'Custom Models'` whose points are, per `period` (first-seen
order), the sum of the members' `aum` rounded to cents, `null` only where EVERY member is null at that period (absent is not zero; a null member adds
nothing); `pointClass` is `interpolated_estimate` if any member carries it, else the first defined member value. The input is never mutated. The member
series do not appear in the result. Comment the module with the FWD-9 reference and the field-read law (it sums served series; it never composes an
artifact total).

### 1c. `portal/src/pages/ModelPortfolios.tsx`

1. Imports: change `import { CategoryViewTree } from '@/components/CategoryViewTree'` to also import `l1ColorOf`, and add
   `import { groupCustomModelsSeries } from '@/lib/trendGrouping'`.
2. Above `keyForModel` (`:136`) add `const TREND_GROUP_L1: Record<string, string> = { 'Custom Models': 'Custom', 'ETF Strategies': 'ETF Strategies',
   'ALT Strategies': 'ALT Strategies' }` and `const trendColorOf = (label: string): string | undefined => (label in TREND_GROUP_L1 ? l1ColorOf(TREND_GROUP_L1[label]) : undefined)`.
   These are the ONLY colour lines for the three labels: no hex literal and no `PALETTE.*` pick beside any of them.
3. `STACK_SERIES`: insert `{ key: 'custom_models', label: 'Custom Models' }` immediately BEFORE the `non_model` entry; change the two band labels to
   `'ETF Strategies'` (key `sma_additive`) and `'ALT Strategies'` (key `tax_additive`). Keys do not change (they are recharts dataKeys).
   `keyForModel('Custom Models')` resolves through the fallback to `m_custom_models`: add `'Custom Models': 'custom_models'` to `MODEL_KEY` so the
   series data lands on the mounted key.
4. The `timeSeriesData` memo (`:854-857`): after the blend roll, when `effectiveFirmId === 'global'`, pass the rolled `by_model` through
   `groupCustomModelsSeries(rolled, new Set(['Ultra-Short Term','Short Term','Intermediate Term','Long Term','Ultra-Long Term']))`; every other scope is
   left exactly as it is. Add `effectiveFirmId` to the memo's dependency list.
5. Colours: at the legend's model entries (`:1146-1150`) use `trendColorOf(modelName) ?? modelColor?.primary ?? PALETTE.blue400`; at the two band
   legend entries (`:1157`, `:1160`) relabel to `'ETF Strategies'` / `'ALT Strategies'` and use `trendColorOf(<label>) ?? PALETTE.gray300`; at the
   bars (`:2003`) and the areas (`:2239`) prefer `trendColorOf(s.label)` over `getModelColor(s.label)?.primary`.
6. Leave alone: the tooltip (it derives rows from the payload and anchors on the artifact total), `rollBlendsIntoArchetypeSeries`, the donut and the
   Total Holdings rollup, every per-firm path, the `plottedKeys` whole-day-gap filter, `src/lib/modelPortfolioColors.ts` and its tests.

### 1d. the existing colour test

`portal/src/pages/ModelPortfolios.taxsma-color.test.ts` pins `getModelColor` for 'Tax-Managed SMA' (vermilion500) and 'ETF Strategies' (#6366f1); those
resolve through `modelPortfolioColors.ts`, which you do not touch, so the test stays green unchanged. Run it once and say so. Do not edit it.

LAWS THAT BIND THIS EDIT. (i) FIELD READ: the group is a per-date sum of SERVED model lines, never an artifact total recomposed; the stack must still
add to `opal_aggregate_aua` (the issuer's `data` arm proves the rule does, 486 of 486 valued dates). (ii) Absent is not zero: a date with no member
value draws no 'Custom Models' point. (iii) Global only. (iv) No back-cast, no interpolation, no new key, no served-object change. (v) The provenance
read guard stays green (`node scripts/provenance-read-guard.mjs` in the portal prints `OK:`).

Stamp any surprise row's `surfaced_at` with `date -u +%FT%TZ`. Row id form `MDPF_CANON-D1-W18-S<k>`, `disarm_owner` `2.0.0_SA_COO~D1`. If a band's resolved
colour equals another series' colour, file an OBSERVATION row naming both hex values: do not edit the colour registry.

## 2. BOUNDS

1. Portal repository only, on branch `wk-MDPF_CANON-18-portal`; never push; never touch `DEV` or `PROD`; no merge.
2. Edit only the files in section 3 (plus your deliverables and the surprise channel). No token change, no new dependency, no new component.
3. No AWS call of any kind, no deploy, no store write. No `bun install` (the modules are linked). No browser launch.
4. **CLIENT DATA:** never print a client figure or an account id in your report, a row or a file; tests use synthetic numbers.
5. No non-ASCII character in any line you add. Use the Edit tool; keep CRLF in the two existing files.
6. If an item cannot be met inside your paths, file a row and stop on that criterion: the issuer rules it.

## 3. SURFACES

<paths>
portal/src/components/CategoryViewTree.tsx
portal/src/lib/trendGrouping.ts
portal/src/pages/ModelPortfolios.tsx
org/missions/D8/MDPF/MDPF_CANON/task-orders/MDPF_CANON.TO-CN-i-1.aua-trend-grouping.md
org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~18/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

Read-only: the whole repository, in particular `portal/CLAUDE.md`, `portal/DESIGN.md`, `portal/src/lib/modelPortfolioColors.ts` and the issuer's check
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_i_1.py` (never edit it; read its subcommands to see exactly what each
arm asserts).

## 4. PROOF OF SPEC (literal; timeout 120 per invocation)

<proof_of_spec>
  <criterion id="AC1" cell_refs="CN-i-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_i_1.py" module; echo "exit=$?"</invocation><expect>ROUND 7 GROUP-MODULE: 6 of 6 arms -- and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="CN-i-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_i_1.py" page; echo "exit=$?"</invocation><expect>ROUND 7 GROUP-PAGE: 5 of 5 arms -- and exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="CN-i-1"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_i_1.py" data; echo "exit=$?"</invocation><expect>ROUND 7 GROUP-DATA: 3 of 3 arms -- and exit=0</expect></criterion>
  <criterion id="AC4" cell_refs="CN-i-1" judgment="true"/>
</proof_of_spec>

AC4 is JUDGMENT, graded at the round-7 close (never self-graded): the issuer renders the Global AUA Trend headless (`/frontend-dev`, `scripts/ui-smoke.mjs`,
fixtures shaped like the folded served global object) and the CVO reads the screenshot against `DESIGN.md` -- one 'Custom Models' series in the Total
Assets Custom colour, the two bands named 'ETF Strategies' and 'ALT Strategies' in their Total Assets colours, the five canonical models unchanged,
no 'Other Models' entry, no Client chips (they are not in this cell), and on a sampled date the tooltip rows still add to the Total. You do not render.

## 5. WHEN YOU ARE DONE

1. Commit the three portal files INSIDE the nested repo: `git -C "<worktree>/portal" add -- src/components/CategoryViewTree.tsx src/lib/trendGrouping.ts
   src/pages/ModelPortfolios.tsx` then `git -C "<worktree>/portal" commit --author "0.9.0_WK_MDPF_CANON~18 <0.9.0_WK_MDPF_CANON~18@opal.agent>" -F <msgfile>`
   (message file written with the Write tool). If a portal hook refuses, file a row with its text and stop: do not bypass it.
2. Write the proof instance at
   `org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~18/MDPF_CANON.TO-CN-i-1.aua-trend-grouping.proof_of_spec.json`, AC4
   UNVERIFIABLE-BY-INSTRUMENT with status_reason "graded at the round-7 close". **Flip this order's `<status>` to `complete` in the SAME commit as the
   instance**, and only when AC1, AC2 and AC3 all pass.
3. Commit the OUTER files via `.tools/safe-commit.sh --author "0.9.0_WK_MDPF_CANON~18 <0.9.0_WK_MDPF_CANON~18@opal.agent>" -F <msgfile> -- <paths>` (outer
   paths only; do not stage `portal`). Run `python .tools/proof-of-spec-check.py <instance>` on the committed bytes and report its verdict line.

Report once: the portal branch and commit hash, the diff (one line per file), the output line of AC1-AC3, the outer commit hash, and any row.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** round 7, from the CTO's round-6 analysis (FWD-9 enters beside CN-h-1, msg 5067; ruling msg 5071). Design: `round7/FWD9_GROUPING_READ.md`
@1c9f519b6f. DRAIN CHECKS (the issuer's, not criteria): `bun run typecheck` and `node scripts/provenance-read-guard.mjs` in the portal worktree, once,
after the commit; the `ui-smoke` render for AC4. A portal candidate touching product files: it comes to `1.0.0_SA_CTO~DELL1` for review BEFORE any DEV
landing, with the render beside it; the PROD push of Model Portfolios is client-facing and is Andrew's card with the before/after, beside the FWD-3
`/portfolios` card. The `--portal-ref` the issuance names is portal `DEV` HEAD at the cut (the `fanout:` line carries `portal_ref:`).

**RISK CLASS:** `LOCAL` for this cell (portal/src is the LOCAL floor, GATE xii; the candidate lands on portal DEV only); client-facing at the PROD
push. `worker-light`: about 90 product lines over three files (one new, about 40), every anchor inlined.

**FORKS FOR THE ISSUER (measured; the ruling's premises do not all hold, so this draft cuts only what is implementable):**
1. **The Client chips cannot be drawn from "the 21 dated objects" by the component.** The portal serves ONE category-views object per scope
   (`platinum/mdpf/<scope>/category-views.json`, the latest; `platinum/mdpf/archive/` holds no category-views). The 21 dated objects (2026-08-27 ..
   2026-10-12) live only in `opal-data-assets/portal/gold/mdpf/global/category-views/`, which no portal route serves. Reading them needs a served
   history route (a new key or behaviour: the ruling's "no new served key for history"). Without it a component can draw the Client chips at the single
   served as-of only. `r7_cn_i_1.py data` prints FINDING F1.
2. **The stack identity forbids drawing ETF Strategies (the whole group) or the Client chips as extra stacked series.** Measured on 2026-10-09:
   Models 1,837,033,010.51 + SMA 50,467,055.53 + Client 285,224,615.28 = opal_aggregate_aua 2,172,724,681.31, but the Trend stack is
   model bars + Non-Model + the two additive bands, and `non_model_aua` 306,345,816.66 INCLUDES the carve-out SMA members (Dividend 17,103,256.79 +
   Growth 4,017,944.59) that the ETF Strategies group counts. Client = non_model_aua - carve-outs: a client-side subtraction (the 0340Z FIELD READ law
   forbids it) or a new producer series. So this draft names the two EXISTING additive bands (`sma_additive_aua` is the additive ETF sleeves only,
   PFDE today, 0.41M; `tax_additive_aua` is the ALT Tax-Managed SMA, 28.9M) with the Total Assets labels and colours, and leaves the carve-outs inside
   'Other AUA'. The label 'ETF Strategies' on 0.41M while the card says 21.6M is a naming risk: the issuer may prefer 'ETF Strategies (additive)'.
3. **Two Andrew rulings name the ALT colour differently.** Total Assets `L1_COLOR['ALT Strategies']` is green400 (2026-09-15); the Trend pins the
   Tax-Managed SMA to the alternatives vermilion500 (Andrew-direct 2026-10-01 ~19:4xZ, "we canonically use vermillion for alts",
   `modelPortfolioColors.ts:139-144`, pinned by `ModelPortfolios.taxsma-color.test.ts`). FWD-9 says the Total Assets colours, so this draft uses green400
   for the 'ALT Strategies' band; the vermilion pin keeps applying to the name 'Tax-Managed SMA' elsewhere. The CTO or Andrew rules if the Trend band
   should stay vermilion.
4. **"Each grouped series equals the sum of its members on three dates" after the fold:** the members are no longer served on folded dates;
   `other_models` IS the served sum of the removed lines on emitted dates (R5 of `r6_fold_readback.py`). The module arm proves the sum on synthetic
   periods; the `data` arm proves the stack on the real object. The Custom Models series has gaps wherever `other_models` is suppressed (2026-05-15 ..
   2026-09-09) and before 2026-05-15, by accepted ruling.
5. **No hover change is cut:** the tooltip derives its rows from the payload; the group name appears there because the series name is the label.

<status>pending</status>
<round>7</round>
<to_id>MDPF_CANON.TO-CN-i-1</to_id>
<slot>~18</slot>
<fabric>dell1</fabric>
<risk>LOCAL</risk>
<worker_class>worker-light</worker_class>
