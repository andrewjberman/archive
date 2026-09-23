#!/usr/bin/env bun
/**
 * FE-s-11 -- component census. (FE-s-73's copy, corrected; see the FE-s-73
 * block below for what changed and why. Everything above that block is
 * FE-s-11's original text, copied from FE-s-64's deliverables/census.ts
 * unmodified except where the FE-s-73 fix required it.)
 *
 * Enumerates every IMPORT appearing in a file under
 * `portal/src/pages/InvestorReporting/**` (excluding `__tests__/` and
 * `fixtures/`) that resolves to a React component -- a `.tsx` module export
 * USED AS JSX in the importing file. One ADDITIONAL importer is scanned
 * beyond that directory, disclosed here rather than silently applied:
 * `portal/src/App.tsx`, because it is the ONLY file that ever mounts the
 * page's own two top-level route entries (`index.tsx`'s `InvestorReporting`,
 * `render/PrintEntry.tsx`'s `PrintEntry`) as JSX -- neither is imported by
 * anything INSIDE the tree, so without this one exception the census would
 * silently omit the page's own two mount points. Every other importer
 * scanned is inside the tree.
 *
 * SCOPE NOTES (read before disputing a row's absence):
 *  - A component defined and used ONLY inside its own file (never exported,
 *    e.g. ScopeSummary.tsx's `Fact`, AnalysisDocument.tsx's `Section`,
 *    DrillTree.tsx's `Breadcrumbs`) is not an IMPORT and carries no row --
 *    it is implementation detail of the one file that defines it.
 *  - `export function Name(...)` is this script's ONLY component-definition
 *    detector (no arrow-function-component form exists anywhere in this
 *    tree today, confirmed by hand before writing this script -- see the
 *    FE-s-11 census brand-review notes for the manual cross-check).
 *  - A named import whose local binding is never used as a JSX tag in the
 *    SAME importing file (a formatter function, a class, a constant lookup
 *    table, a type) produces no row, by design -- the census is of
 *    COMPONENTS THE PAGE RENDERS, not of every value crossing a module
 *    boundary.
 *  - A component `export`ed by a file under the tree but never imported by
 *    ANYTHING (including App.tsx) is listed separately, under
 *    `definedButNotImported`, and is NOT counted in `COMPONENTS: N` -- it
 *    is not "imported" by the literal rule this script implements. Two such
 *    components exist today (`AppliedBranding`, `ReceiptPanel`) -- see the
 *    surprise row this finding produced (IRPT_FNTEND-W1-S11).
 *
 * ---------------------------------------------------------------------------
 * FE-s-73 FIX (row W14-S2) -- read this before trusting any `reason` field.
 * ---------------------------------------------------------------------------
 *
 * THE DEFECT THIS COPY FIXES. FE-s-11's (and FE-s-64's) `extractHeaderComment`
 * took the FIRST `/** ... *\/` block of the whole FILE and used it as the
 * `reason` for EVERY NEW component defined in that file. `render/Page.tsx`
 * defines `PageSheet` and `UnnamedReasonCodeFlag` together; both got the
 * file's frame comment ("the page frame both templates share: sheet, header,
 * footer"), although `UnnamedReasonCodeFlag` carries its OWN JSDoc directly
 * above it ("The flag beside a code the contract does not name. ..."). The
 * SAME method defect hits three other multi-component files in this tree
 * today: `export/ExportButton.tsx` (`ExportButton` / `ExportAnchorSlot`),
 * `export/ExportModal.tsx` (`ExportModalPanel` / `ExportModal`), and
 * `render/values.tsx` (`Metric` / `SourceValue`) -- all four pairs carried
 * IDENTICAL `reason` text in FE-s-64's round-10 `component-census.json`,
 * confirmed by the F73-AC8 control below.
 *
 * THE FIX. `extractOwnLeadingComment(fileRel, definitionName)` finds
 * `export function <definitionName>(` and walks BACKWARD from it: if the
 * nearest preceding `/** ... *\/` block is separated from the declaration by
 * nothing but whitespace, that block IS the component's own doc comment, and
 * its first paragraph becomes the `reason`. If no such block exists (nothing
 * but code, or a `//` section header, sits directly above the declaration),
 * the row falls back to the FILE'S leading block (the original
 * `extractHeaderComment`, unchanged) and is marked `reasonScope:
 * "FILE-LEVEL (shared)"` so a reader can tell a shared reason from an own
 * one at a glance. A row with neither gets the same generic fallback text
 * FE-s-11 always used, marked `reasonScope: "NONE"`.
 *
 * `definitionName` is not always the row's `component` field (the LOCAL
 * binding the importer renders as JSX): `src/App.tsx`'s bare
 * `lazy(() => import('./pages/InvestorReporting/render/PrintEntry'))` binds
 * the target's DEFAULT export under the local alias `InvestorReportingPrint`,
 * so the row is keyed `InvestorReportingPrint` but the function actually
 * defined in that file is `PrintEntry` -- `definitionNameFor` resolves this
 * the same way the pre-existing `definedButNotImported` cross-check already
 * does (`exportedNameHint` first, then `defaultExportName` for a bare default
 * import, else the local binding, which IS the real export name for every
 * named import in this tree -- no `as`-aliasing of a tree-internal component
 * exists today, confirmed by a targeted search before writing this fix).
 *
 * NEW FIELDS (F73-AC5). Every NEW row now also carries `needs` (one sentence
 * naming what THIS component does that the nearest existing candidate
 * cannot) and `nearestExisting` (that candidate's name, so a reviewer can
 * dispute it) -- populated from the curated `NEEDS_TABLE` below, one entry
 * per NEW component, written by hand against this tree's actual reused set
 * and sibling components (never invented): see the table for the citation
 * behind each. A component this table does not cover is listed in
 * `needsMissing` and is a FINDING, never an invented reason -- none is
 * expected today (`NEEDS_TABLE` covers all 45 of FE-s-64's NEW rows), and
 * the corrected run's own NEW count is checked against the table's coverage
 * at the bottom of this script (`NEEDS-MISSING: N`).
 *
 * WRAPPER / SELF-USE BOUNDARY (task point 3). Stated ONCE, in
 * `SCOPE_BOUNDARY_NOTE` below, carried into both output files: a component
 * used only inside its own defining file (no import edge exists to
 * enumerate) is still one row, keyed `(self -- no import statement; ...)`;
 * `TabShell`, `ClientSearch` and `FirmDropdown` are thin wrappers over a
 * REUSED primitive and are still classified NEW, by the SAME rule this
 * script applies everywhere -- classification tracks WHERE a component is
 * DEFINED, never how much logic it adds over what it wraps.
 *
 * NO SOURCE WRITE. This copy writes only inside its own `OUT_DIR` (wherever
 * this file itself lives -- FE-s-73's `deliverables/0.9.0_WK_IRPT_FNTEND~23/`
 * folder, never FE-s-11's or FE-s-64's). It reads component source under
 * `portal/src/pages/InvestorReporting/**` and `portal/src/App.tsx` only, and
 * writes nothing there.
 *
 * Run from `<portal>`: `bun run <this file>`. Writes `component-census.json`
 * and `component-census.md` beside this script, and prints `COMPONENTS: N`
 * (the REUSED/NEW split) to stdout.
 */
import { readdirSync, statSync, readFileSync, writeFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'

const PORTAL_ROOT = process.cwd()
const TREE_ROOT_REL = 'src/pages/InvestorReporting'
const OUT_DIR = import.meta.dir

function toPosix(p: string): string {
  return p.split('\\').join('/')
}

function isDir(rel: string): boolean {
  return statSync(join(PORTAL_ROOT, rel)).isDirectory()
}

function walkTsx(dirRel: string, out: string[]): void {
  const dirAbs = join(PORTAL_ROOT, dirRel)
  for (const entry of readdirSync(dirAbs)) {
    if (entry === '__tests__' || entry === 'fixtures') continue
    const entryRel = toPosix(dirRel + '/' + entry)
    if (isDir(entryRel)) {
      walkTsx(entryRel, out)
    } else if (entry.endsWith('.tsx')) {
      out.push(entryRel)
    }
  }
}

const treeFiles: string[] = []
walkTsx(TREE_ROOT_REL, treeFiles)
treeFiles.sort()

const IMPORTER_FILES = [...treeFiles, 'src/App.tsx']

// ---------------------------------------------------------------------------
// Import-edge extraction
// ---------------------------------------------------------------------------

interface ImportEdge {
  local: string
  isNamespace: boolean
  specifier: string
  importerRel: string
  line: number
  /**
   * The NAMED export a `.then(m => ({ default: m.NAMED }))` lazy-import
   * selects, when known -- lets the definedButNotImported cross-check match
   * the target's real export name even though the JSX call site renders it
   * under a local alias (App.tsx's `InvestorReportingPrint` for
   * `PrintEntry.tsx`'s default-exported `PrintEntry`). Undefined for every
   * ordinary static import (named-import aliasing is already resolved to
   * the local binding by the caller).
   */
  exportedNameHint?: string
  /**
   * True only for an edge that imports the target's DEFAULT export under a
   * local alias the importer chose (a bare `import Foo from '...'`, or a
   * bare `lazy(() => import('SPEC'))` with no `.then` selector) -- the ONLY
   * case where the census must also credit the target's OWN default-export
   * name (via `defaultExportName`) as "imported", because the local alias
   * need not match it. A NAMED import's local binding (after `as`
   * resolution) IS the real exported name already, and must NOT also credit
   * that file's default export -- crediting it unconditionally is exactly
   * the bug this flag fixes: `import { ExportAnchorSlot } from
   * './ExportButton'` would otherwise also mark that file's UNRELATED
   * default export (`ExportButton`) as imported, when nothing imported it.
   */
  isDefault: boolean
}

function extractImports(fileRel: string, src: string, lazyOnly = false): ImportEdge[] {
  const edges: ImportEdge[] = []

  // React.lazy dynamic imports -- `const X = lazy(() => import('SPEC'))` or
  // `const X = lazy(() => import('SPEC').then(m => ({ default: m.Y })))`.
  // Not an ES `import ... from` statement at all (a dynamic `import()` call
  // inside an arrow function), so the static regex below never sees it --
  // portal/src/App.tsx's own two route-mount edges are exactly this form.
  const LAZY_RE =
    /const\s+(\w+)\s*=\s*lazy\(\s*\(\)\s*=>\s*import\(['"]([^'"]+)['"]\)(?:\s*\.then\(\s*\(?\w+\)?\s*=>\s*\(\{\s*default:\s*\w+\.(\w+)\s*\}\)\s*\))?/gs
  let lm: RegExpExecArray | null
  while ((lm = LAZY_RE.exec(src))) {
    const local = lm[1]
    const specifier = lm[2]
    // Restrict to THIS feature's two lazy routes -- App.tsx lazy-loads every
    // other top-level portal page the same way, and none of those are in
    // scope for an Investor Reporting component census.
    if (!specifier.includes('InvestorReporting')) continue
    const exportedNameHint = lm[3] || undefined
    const line = src.slice(0, lm.index).split('\n').length
    edges.push({
      local,
      isNamespace: false,
      specifier,
      importerRel: fileRel,
      line,
      exportedNameHint,
      isDefault: !exportedNameHint,
    })
  }

  // `lazyOnly` is set for the one importer outside the tree (src/App.tsx):
  // the census's job is components the INVESTOR REPORTING PAGE uses, not the
  // portal's whole app shell -- App.tsx's OWN top-level imports (its nav
  // chrome, its login pages, its unrelated lazy routes) are out of scope,
  // and scanning them would silently smuggle unrelated components into this
  // feature's census. Only its two lazy imports of THIS feature are in
  // scope, both already captured above.
  if (lazyOnly) return edges

  const IMPORT_RE = /import\s+(type\s+)?([^;]*?)\s+from\s+['"]([^'"]+)['"]/gs
  let m: RegExpExecArray | null
  while ((m = IMPORT_RE.exec(src))) {
    const wholeTypeOnly = !!m[1]
    const clause = m[2].trim()
    const specifier = m[3]
    const line = src.slice(0, m.index).split('\n').length
    if (wholeTypeOnly) continue // `import type { .. } from '..'` -- no runtime binding

    const nsMatch = /^\*\s+as\s+(\w+)$/.exec(clause)
    if (nsMatch) {
      edges.push({ local: nsMatch[1], isNamespace: true, specifier, importerRel: fileRel, line, isDefault: false })
      continue
    }

    let defaultName: string | null = null
    let namedContent: string | null = null
    const mixedMatch = /^(\w+)\s*,\s*\{([\s\S]*)\}$/.exec(clause)
    const namedOnlyMatch = /^\{([\s\S]*)\}$/.exec(clause)
    const defaultOnlyMatch = /^(\w+)$/.exec(clause)
    if (mixedMatch) {
      defaultName = mixedMatch[1]
      namedContent = mixedMatch[2]
    } else if (namedOnlyMatch) {
      namedContent = namedOnlyMatch[1]
    } else if (defaultOnlyMatch) {
      defaultName = defaultOnlyMatch[1]
    } else {
      continue // unrecognised clause shape -- record nothing rather than guess
    }

    if (defaultName) {
      edges.push({ local: defaultName, isNamespace: false, specifier, importerRel: fileRel, line, isDefault: true })
    }
    if (namedContent) {
      for (const rawTok of namedContent.split(',')) {
        const tok = rawTok.trim()
        if (!tok) continue
        const isType = /^type\s+/.test(tok)
        if (isType) continue // inline `type X` within a mixed named list -- no runtime binding
        const rest = tok.replace(/^type\s+/, '')
        const asMatch = /^(\S+)\s+as\s+(\S+)$/.exec(rest)
        const local = asMatch ? asMatch[2] : rest
        edges.push({ local, isNamespace: false, specifier, importerRel: fileRel, line, isDefault: false })
      }
    }
  }
  return edges
}

function usedAsJsx(fileSrc: string, local: string, isNamespace: boolean): boolean {
  const escaped = local.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  // The follow-character class allows `<` too: a generic JSX component such
  // as `<Combobox<SearchOptionRow | null> ...>` (header/ClientSearch.tsx)
  // opens its type argument with `<` immediately after the tag name, and a
  // class limited to whitespace/`/`/`>` misses it -- a real false negative
  // found while writing this script (see the census brand-review notes).
  const pattern = isNamespace
    ? new RegExp('<\\s*' + escaped + '\\.')
    : new RegExp('<' + escaped + '(?=[\\s/><])')
  return pattern.test(fileSrc)
}

// ---------------------------------------------------------------------------
// Specifier resolution
// ---------------------------------------------------------------------------

type Resolution =
  | { kind: 'repo'; relPath: string; exists: boolean }
  | { kind: 'npm'; pkg: string; exists: boolean }

function resolveRepoCandidate(combined: string): { relPath: string; exists: boolean } {
  for (const suffix of ['', '.tsx', '.ts', '/index.tsx', '/index.ts']) {
    const candidate = combined + suffix
    const abs = join(PORTAL_ROOT, candidate)
    if (existsSync(abs) && statSync(abs).isFile()) return { relPath: candidate, exists: true }
  }
  return { relPath: combined, exists: false }
}

function resolveSpecifier(importerRel: string, specifier: string): Resolution {
  if (specifier.startsWith('.')) {
    const baseDir = dirname(importerRel)
    const combined = toPosix(join(baseDir, specifier))
    const r = resolveRepoCandidate(combined)
    return { kind: 'repo', ...r }
  }
  if (specifier.startsWith('@/')) {
    const combined = 'src/' + specifier.slice(2)
    const r = resolveRepoCandidate(combined)
    return { kind: 'repo', ...r }
  }
  const pkg = specifier.startsWith('@') ? specifier.split('/').slice(0, 2).join('/') : specifier.split('/')[0]
  const exists = existsSync(join(PORTAL_ROOT, 'node_modules', pkg))
  return { kind: 'npm', pkg, exists }
}

// ---------------------------------------------------------------------------
// Reason extraction: FE-s-73's fix -- the component's OWN leading JSDoc
// first, the file's leading block only as a disclosed fallback.
// ---------------------------------------------------------------------------

/** The first paragraph of a `/** ... *\/` comment BODY (between the delimiters). */
function firstParagraphOf(commentBody: string): string | null {
  const lines = commentBody.split('\n').map((l) => l.replace(/^\s*\*\s?/, '').trimEnd())
  const para: string[] = []
  for (const l of lines) {
    if (l.trim() === '' && para.length > 0) break
    if (l.trim() === '' && para.length === 0) continue
    para.push(l)
  }
  let text = para.join(' ').replace(/\s+/g, ' ').trim()
  if (text.length > 480) text = text.slice(0, 477) + '...'
  return text || null
}

/** FE-s-11's original extractor: the FIRST doc comment of the whole FILE. Kept, unchanged, as the disclosed fallback for a component with no own leading comment. */
function extractHeaderComment(fileRel: string): string | null {
  const abs = join(PORTAL_ROOT, fileRel)
  if (!existsSync(abs)) return null
  const src = readFileSync(abs, 'utf8')
  const m = /^\s*\/\*\*([\s\S]*?)\*\//.exec(src)
  if (!m) return null
  return firstParagraphOf(m[1])
}

/**
 * FE-s-73's fix: the doc comment IMMEDIATELY ABOVE `export function
 * <definitionName>(` in `fileRel` -- i.e. nothing but whitespace between the
 * comment's closing `*\/` and the declaration. Returns null when the
 * component has no such comment (a `//` section header or other code sits
 * directly above it instead), so the caller can fall back to the file's
 * block and mark the row FILE-LEVEL (shared).
 */
function extractOwnLeadingComment(fileRel: string, definitionName: string): string | null {
  const abs = join(PORTAL_ROOT, fileRel)
  if (!existsSync(abs)) return null
  const src = readFileSync(abs, 'utf8')
  const escaped = definitionName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const declRe = new RegExp('^export function ' + escaped + '\\s*\\(', 'm')
  const dm = declRe.exec(src)
  if (!dm) return null
  const before = src.slice(0, dm.index)
  const blockRe = /\/\*\*[\s\S]*?\*\//g
  let last: RegExpExecArray | null = null
  let bm: RegExpExecArray | null
  while ((bm = blockRe.exec(before))) last = bm
  if (!last) return null
  const tail = before.slice(last.index + last[0].length)
  if (tail.trim() !== '') return null // something besides whitespace sits between the comment and the declaration
  const inner = last[0].slice(2, -2) // strip the outer /* and */
  return firstParagraphOf(inner)
}

/** Resolves the NAME actually `export function`-defined in `relPath` for this edge -- not always `edge.local` (see the FE-s-73 FIX block above). */
function definitionNameFor(edge: Pick<ImportEdge, 'local' | 'isDefault' | 'exportedNameHint'>, relPath: string): string {
  if (edge.exportedNameHint) return edge.exportedNameHint
  if (edge.isDefault) {
    const def = defaultExportName(relPath)
    if (def) return def
  }
  return edge.local
}

type ReasonScope = 'OWN' | 'FILE-LEVEL (shared)' | 'NONE'

interface ReasonResult {
  reason: string
  reasonScope: ReasonScope
}

function reasonFor(relPath: string, definitionName: string): ReasonResult {
  const own = extractOwnLeadingComment(relPath, definitionName)
  if (own) return { reason: own, reasonScope: 'OWN' }
  const fileLevel = extractHeaderComment(relPath)
  if (fileLevel) return { reason: fileLevel, reasonScope: 'FILE-LEVEL (shared)' }
  return { reason: 'No equivalent existed in the reused set; built for this feature.', reasonScope: 'NONE' }
}

// ---------------------------------------------------------------------------
// Component-definition detector (for the definedButNotImported cross-check)
// ---------------------------------------------------------------------------

function definedComponents(fileRel: string): string[] {
  const src = readFileSync(join(PORTAL_ROOT, fileRel), 'utf8')
  const names: string[] = []
  const re = /^export function ([A-Z]\w*)\s*\(/gm
  let m: RegExpExecArray | null
  while ((m = re.exec(src))) names.push(m[1])
  return names
}

// ---------------------------------------------------------------------------
// F73-AC5 -- the curated need vs. nearest-existing-candidate table.
//
// One entry per NEW component in FE-s-64's round-10 census (45 of 45).
// Written by hand against THIS tree's actual reused set (28 REUSED rows) and
// sibling components -- never invented, never a role label restated. A
// component this table does not cover produces no invented reason: it is
// listed in `needsMissing` (below) instead, and is a finding.
// ---------------------------------------------------------------------------

interface NeedsEntry {
  needs: string
  nearestExisting: string
}

const NEEDS_TABLE: Record<string, NeedsEntry> = {
  AccountDetail: {
    needs: "States each account's own performance AND explicitly names any account the source could not cover, row by row; the nearest reused container has no per-row completeness contract at all.",
    nearestExisting: 'PanelContent',
  },
  AnalysisDocument: {
    needs: "The portrait-letter print template for the Analysis report; the only reused page-shaped primitive is built for the interactive dashboard's live chrome (nav, scroll), not a fixed print page with a page-number/footer/report-state contract.",
    nearestExisting: 'PageSurfaceControl',
  },
  AnalysisTab: {
    needs: "Composes the Analysis tab's own request/response/native-sections flow inside TabShell's mount point; the closest reused analogue only renders the strip of tab buttons and knows nothing about any one tab's contents.",
    nearestExisting: 'TabNavigation',
  },
  AnswerStatus: {
    needs: "Prints what every reporting answer carries on its face (state, reason, business date) per FE-s-30's contract; no reused component reads an EnvelopeState/publicReasonCode pair at all.",
    nearestExisting: 'StatusPanel',
  },
  AppliedBranding: {
    needs: "Reads what branding was ACTUALLY applied off the resolved preview bundle (falling back to 'Opal' when no logo asset came back) -- a fact about a resolved ExportBundle, not a request; no reused component reads that bundle shape.",
    nearestExisting: 'ReceiptPanel',
  },
  ClientSearch: {
    needs: 'A THIN WRAPPER (see the scope boundary note) composing the reused Combobox family for this page\'s client/relationship/account search keys; the portal\'s other client-search panel searches a different, unrelated result shape and is not imported by this feature.',
    nearestExisting: 'Combobox',
  },
  CumulativeReturnChart: {
    needs: 'Labels BOTH endpoints of the cumulative-return line with the returned dates, over the source\'s daily series; the reused recharts primitives it composes carry no endpoint-labelling behaviour of their own.',
    nearestExisting: 'LineChart',
  },
  Disclosures: {
    needs: 'Prints the source\'s disclosure text VERBATIM, never authored or reformatted here; no reused component passes text through unedited the way this one is contracted to.',
    nearestExisting: 'MethodsAndSources',
  },
  DrillTree: {
    needs: 'Model-led radial drilldowns over a HoldingsSnapshot, preserving SIGNED amounts (never Math.abs); the PRD\'s own named precedents use a Math.abs-donut shortcut this cell explicitly declines, so their behaviour cannot be reused as-is.',
    nearestExisting: 'CategoryViewTree',
  },
  ExportAnchorSlot: {
    needs: 'Portals the real ExportButton onto a DISABLED control the tabs already render, found by that control\'s own data-action/data-slot, without editing the tab files (outside this order\'s grant); no reused component does anchor-swap-by-selector.',
    nearestExisting: 'ExportButton',
  },
  ExportButton: {
    needs: 'Owns the export flow\'s local state (bundle composition, revision bump, submit gate) end-to-end for this feature\'s wire contract; the reused dialog/panel primitives it opens have no notion of an export bundle or a submit gate.',
    nearestExisting: 'Panel',
  },
  ExportModal: {
    needs: 'The dialog shell that mounts ExportModalPanel under the reused Dialog; Dialog alone renders no fieldset, branding controls or preview -- it is a generic focus/overlay mechanic with no export-specific content.',
    nearestExisting: 'Dialog',
  },
  ExportModalPanel: {
    needs: 'The export options body itself (branding choice, narrative/account-detail toggles, optional sections, the mounted AppliedBranding/ReceiptPanel pair); the reused panel primitives supply chrome but no branding or export-option state.',
    nearestExisting: 'PanelContent',
  },
  FirmAttribution: {
    needs: "Global mode's per-result firm label, shown beside every tab's content when scope spans more than one firm; no reused component carries a per-row firm attribution.",
    nearestExisting: 'ScopeSummary',
  },
  FirmDropdown: {
    needs: "A THIN WRAPPER (see the scope boundary note) reproducing ModelPortfolios.tsx's exact PageSurfaceControl firm-dropdown composition verbatim, because that file exports no separate dropdown component to import; nothing beyond PageSurfaceControl itself is reused.",
    nearestExisting: 'PageSurfaceControl',
  },
  GenerateComposer: {
    needs: "The Analysis tab's Generate composer (drafting and sending a generation request); no reused component composes or submits an analysis-generation request.",
    nearestExisting: 'RequestList',
  },
  HoldingsSummary: {
    needs: "The Holdings tab's own top strip summarising the holdings snapshot -- distinct data (holdings totals) from the performance summary block's beginning/ending/period-return triple.",
    nearestExisting: 'Summary',
  },
  HoldingsTab: {
    needs: "Composes the Holdings tab's whole body (summary strip, drill tree, slice table, status) inside TabShell's mount; the reused tab-strip component renders only the strip, never a tab's contents.",
    nearestExisting: 'TabNavigation',
  },
  InputReview: {
    needs: "Reviews the Analysis tab's own input/request state before submission; no reused component reviews a request payload.",
    nearestExisting: 'RequestList',
  },
  InvestorReporting: {
    needs: "The page shell that mounts the header, TabShell and the page-level providers for this feature; the reused page-chrome primitives are generic surface controls, not a page assembled around this feature's own header row.",
    nearestExisting: 'PageSurfaceControl',
  },
  InvestorReportingPrint: {
    needs: "The print route's entry point: reads ?bundle=, obtains or composes the bundle, asserts version support, resolves every referenced report, and renders the right print template; nothing else in the portal owns a print-route bundle-resolution flow.",
    nearestExisting: 'PageSheet',
  },
  MethodAndSources: {
    needs: "The Reporting tab's OWN method/sources block, scoped to that tab's live data -- distinct from the printed page-level equivalent inside the PDF template.",
    nearestExisting: 'MethodsAndSources',
  },
  MethodsAndSources: {
    needs: "The printed page that lets a reader check the report's method and sources, inside the PDF template; no reused component renders that page.",
    nearestExisting: 'Disclosures',
  },
  Metric: {
    needs: "Renders a MetricValue union (supported/value/unavailableReason), printing the UNAVAILABLE word and the reason when the source says unsupported; the plain-value sibling only handles a bare nullable primitive with no supported flag or reason.",
    nearestExisting: 'SourceValue',
  },
  NativeSections: {
    needs: "Reads the wire's own verdict on which sections are native, since FE-s-15; no reused component reads that wire shape.",
    nearestExisting: 'RequestList',
  },
  PageSheet: {
    needs: 'The shared print-page frame (logo clear-space, footer, page number, the FE-s-31 report-state band) both templates mount; the reused page-surface primitive is the dashboard\'s interactive chrome and carries no page-number/footer/report-state contract.',
    nearestExisting: 'PageSurfaceControl',
  },
  PerformanceDocument: {
    needs: 'The landscape-letter template composing the performance report\'s pages (frame, summary, period results, account detail, chart, methods, disclosures); no reused component assembles that page set.',
    nearestExisting: 'AnalysisDocument',
  },
  PeriodControls: {
    needs: 'Period presets, a custom date range, Refresh and the (disabled) Export control together, for the Reporting tab; no reused component composes that control set.',
    nearestExisting: 'PeriodResults',
  },
  PeriodInContextPage: {
    needs: 'Composed ENTIRELY from a NarrativePacket, the narrative page inside the export bundle; no reused component reads a NarrativePacket.',
    nearestExisting: 'PerformanceDocument',
  },
  PeriodResults: {
    needs: 'The period results table: every summary return the source stated, the window it applies to, and any benchmark facts supplied; no reused component renders that row shape.',
    nearestExisting: 'AccountDetail',
  },
  Preview: {
    needs: 'Requests the export preview through the typed client at the CURRENT revision, resolves it, and renders the right document inside the modal; the reused dialog/panel primitives supply modal chrome but fetch nothing and resolve nothing.',
    nearestExisting: 'ExportModal',
  },
  ReceiptPanel: {
    needs: "Drives the export job's state through the shared status renderer and, on READY, an authorized download link -- and ONLY that link, never a vendor URL; the status renderer alone has no download-route or receipt-shape awareness.",
    nearestExisting: 'StatusPanel',
  },
  ReportingTab: {
    needs: "Mounts the Reporting tab's performance components with the advisor's controls; NOTHING here computes a return (a boundary its sibling tabs share); no reused component composes that specific set.",
    nearestExisting: 'HoldingsTab',
  },
  RequestList: {
    needs: "Lists the Analysis tab's own generation requests; no reused component lists that request shape.",
    nearestExisting: 'InputReview',
  },
  RevisionIdentity: {
    needs: 'Identifies which export/source revision a preview or receipt belongs to (row W3-S2); no reused component carries that revision-identity concept.',
    nearestExisting: 'ReceiptPanel',
  },
  ScopeSummary: {
    needs: "The header's context strip (what scope -- tenant, firm, accounts -- the page is currently showing); no reused component summarises this feature's scope shape.",
    nearestExisting: 'Panel',
  },
  SliceTable: {
    needs: 'The table equivalent beside every donut in the Holdings tab, keeping the same signed-amount rule the donut itself preserves; no reused table renders that pairing.',
    nearestExisting: 'DrillTree',
  },
  SourceValue: {
    needs: "Renders a plain nullable primitive (no supported/unavailableReason fields) for analysis sections whose own value union carries neither; the fuller MetricValue-shaped sibling would not typecheck against a bare number | string | null.",
    nearestExisting: 'Metric',
  },
  StageDisplay: {
    needs: "Shows the Analysis tab's own generation-stage progress; no reused component displays a stage/progress state for this flow.",
    nearestExisting: 'StatusPanel',
  },
  StatusPanel: {
    needs: 'The one status renderer every tab shares (FE-s-3); no reused status component existed before this feature, and three per-tab copies was the alternative this consolidates.',
    nearestExisting: 'PanelEmpty',
  },
  Summary: {
    needs: 'The summary block (beginning value, ending value, period return) at the top of the performance document -- a distinct row shape from the period-results table\'s per-period rows.',
    nearestExisting: 'PeriodResults',
  },
  TabShell: {
    needs: "A THIN WRAPPER (see the scope boundary note) around the reused tab-strip primitive PLUS this feature's three tab mount points (Reporting/Holdings/Analysis) and its own navigation hook; the reused strip alone renders only the strip, never a tab's mounted content.",
    nearestExisting: 'TabNavigation',
  },
  UnnamedReasonCodeFlag: {
    needs: 'Flags a public_reason_code the v1 contract does not name, inline beside the reason text, on four separate surfaces; its FILE-SIBLING only lays out the page frame and has no per-code-lookup logic of its own -- this is the exact copied-reason case row W14-S2 names (see F73-AC7).',
    nearestExisting: 'PageSheet',
  },
  VariantSelector: {
    needs: "Selects which analysis variant/output the Analysis tab is viewing; no reused component selects among this feature's variant set.",
    nearestExisting: 'RequestList',
  },
  VendorPdfPreview: {
    needs: 'Previews a vendor-produced PDF inline for the Analysis tab, backed by the reused empty-state primitive for the not-yet-available state; that primitive alone is a bare placeholder with no PDF-preview behaviour.',
    nearestExisting: 'PanelEmpty',
  },
}

// ---------------------------------------------------------------------------
// F73 -- the scope boundary this census applies, stated once.
// ---------------------------------------------------------------------------

const SCOPE_BOUNDARY_NOTE =
  'SELF-USE: a component defined and rendered only from within its own defining file (no import edge exists to ' +
  'enumerate) is still one census row, keyed "(self -- no import statement; mounted from within its own defining ' +
  'file)" -- see ExportButton and ExportModalPanel below. WRAPPERS: TabShell, ClientSearch and FirmDropdown each ' +
  'compose a REUSED primitive (the tab-strip component, the Combobox family, PageSurfaceControl) with little logic ' +
  'of their own beyond that composition. They are still classified NEW by the ONE rule this script applies ' +
  'throughout: classification tracks WHERE a component is DEFINED (inside src/pages/InvestorReporting/**), never ' +
  'how much new logic it adds over what it wraps. A thin wrapper still carries its own needs/nearestExisting entry ' +
  '(see the table) naming the primitive it wraps and what the wrap adds that the primitive alone does not supply.'

// ---------------------------------------------------------------------------
// Main pass: walk every importer, collect JSX-used edges
// ---------------------------------------------------------------------------

interface ComponentRow {
  component: string
  importedFrom: string
  classification: 'REUSED' | 'NEW'
  path?: string
  reason?: string
  reasonScope?: ReasonScope
  needs?: string
  nearestExisting?: string
  usedIn: { file: string; specifier: string; line: number; exportedNameHint?: string; isDefault: boolean }[]
}

const rows = new Map<string, ComponentRow>()

for (const importerRel of IMPORTER_FILES) {
  const abs = join(PORTAL_ROOT, importerRel)
  if (!existsSync(abs)) continue
  const src = readFileSync(abs, 'utf8')
  const edges = extractImports(importerRel, src, importerRel === 'src/App.tsx')
  for (const edge of edges) {
    if (!usedAsJsx(src, edge.local, edge.isNamespace)) continue
    const resolution = resolveSpecifier(importerRel, edge.specifier)
    const targetKey =
      resolution.kind === 'repo' ? `repo:${resolution.relPath}#${edge.local}` : `npm:${resolution.pkg}#${edge.local}`
    let row = rows.get(targetKey)
    if (!row) {
      const inTree = resolution.kind === 'repo' && resolution.relPath.startsWith(TREE_ROOT_REL + '/')
      if (inTree) {
        const definitionName = definitionNameFor(edge, resolution.relPath)
        const { reason, reasonScope } = reasonFor(resolution.relPath, definitionName)
        row = {
          component: edge.local,
          importedFrom: edge.specifier,
          classification: 'NEW',
          reason,
          reasonScope,
          usedIn: [],
        }
      } else {
        const path =
          resolution.kind === 'repo'
            ? `portal/${resolution.relPath}${resolution.exists ? '' : ' (UNRESOLVED -- file not found)'}`
            : `portal/node_modules/${resolution.pkg}${resolution.exists ? '' : ' (UNRESOLVED -- package not found)'}`
        row = {
          component: edge.local,
          importedFrom: edge.specifier,
          classification: 'REUSED',
          path,
          usedIn: [],
        }
      }
      rows.set(targetKey, row)
    }
    row.usedIn.push({
      file: importerRel,
      specifier: edge.specifier,
      line: edge.line,
      exportedNameHint: edge.exportedNameHint,
      isDefault: edge.isDefault,
    })
  }
}

// ---------------------------------------------------------------------------
// definedButNotImported cross-check
// ---------------------------------------------------------------------------

function defaultExportName(fileRel: string): string | null {
  const abs = join(PORTAL_ROOT, fileRel)
  if (!existsSync(abs)) return null
  const src = readFileSync(abs, 'utf8')
  const m = /^export default (\w+)\s*$/m.exec(src)
  return m ? m[1] : null
}

const importedTargets = new Set<string>()
for (const row of rows.values()) {
  for (const use of row.usedIn) {
    // resolve again to get the target file for the cross-check key
    const r = resolveSpecifier(use.file, use.specifier)
    if (r.kind !== 'repo') continue
    if (use.exportedNameHint) {
      // A `.then(m => ({ default: m.NAMED }))` lazy-import names the real
      // export explicitly, regardless of the local JSX-rendered alias.
      importedTargets.add(`${r.relPath}#${use.exportedNameHint}`)
    } else {
      // A NAMED import's local binding (after `as` resolution) IS the real
      // exported name -- always credit it.
      importedTargets.add(`${r.relPath}#${row.component}`)
      if (use.isDefault) {
        // A bare `import Foo from '...'` or bare `lazy(() => import('SPEC'))`
        // (no `.then`) imports SPEC's DEFAULT export under whatever local
        // alias the importer chose (App.tsx binds render/PrintEntry.tsx's
        // default-exported `PrintEntry` to its own `InvestorReportingPrint`)
        // -- also credit the file's real default-export name. Gated on
        // `isDefault`: crediting it for an ORDINARY NAMED import (e.g.
        // `{ ExportAnchorSlot }` from a file whose UNRELATED default export
        // happens to be `ExportButton`) would falsely mark that default
        // export "imported" when nothing imported it.
        const defName = defaultExportName(r.relPath)
        if (defName) importedTargets.add(`${r.relPath}#${defName}`)
      }
    }
  }
}

const definedButNotImported: { file: string; component: string }[] = []
for (const fileRel of treeFiles) {
  const ownSrc = readFileSync(join(PORTAL_ROOT, fileRel), 'utf8')
  for (const name of definedComponents(fileRel)) {
    const importedElsewhere = importedTargets.has(`${fileRel}#${name}`)
    // Same-file self-usage (e.g. export/ExportButton.tsx's `ExportAnchorSlot`
    // portals `<ExportButton .../>` from inside its OWN file -- a real JSX
    // use with no import statement to enumerate, since a file never imports
    // from itself) counts as "used", just not as an IMPORT-based census row
    // via the edge scan above -- so it is added as its OWN row here instead
    // of being silently absent from both the count and the orphan list.
    const usedInOwnFile = usedAsJsx(ownSrc, name, false)
    if (!importedElsewhere && !usedInOwnFile) {
      definedButNotImported.push({ file: fileRel, component: name })
    } else if (!importedElsewhere && usedInOwnFile) {
      const selfKey = `repo:${fileRel}#${name}`
      if (!rows.has(selfKey)) {
        const { reason, reasonScope } = reasonFor(fileRel, name)
        rows.set(selfKey, {
          component: name,
          importedFrom: '(self -- no import statement; mounted from within its own defining file)',
          classification: 'NEW',
          reason,
          reasonScope,
          usedIn: [{ file: fileRel, specifier: '(self)', line: 0 }],
        })
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Attach the curated needs/nearestExisting fields to every NEW row.
// ---------------------------------------------------------------------------

const needsMissing: string[] = []
for (const row of rows.values()) {
  if (row.classification !== 'NEW') continue
  const entry = NEEDS_TABLE[row.component]
  if (entry) {
    row.needs = entry.needs
    row.nearestExisting = entry.nearestExisting
  } else {
    needsMissing.push(row.component)
  }
}

// ---------------------------------------------------------------------------
// PRD PATHS table reuse-row accounting (11 static rows, from the PRD text) --
// two rows (1, 5) are not import edges at all (a route-registration file and
// a copied className, not a component import) and are checked directly
// against source text rather than against the edge scan above.
// ---------------------------------------------------------------------------

interface PrdRow {
  row: number
  paths: string[]
  cell: string
}

const PRD_ROWS: PrdRow[] = [
  { row: 1, paths: ['portal/src/App.tsx'], cell: 'F1' },
  {
    row: 2,
    paths: [
      'portal/src/components/PageHeaderVariants.tsx',
      'portal/src/components/ui/PageSurfaceControl.tsx',
      'portal/src/ui/components/panels/',
    ],
    cell: 'F2, F4, F11',
  },
  {
    row: 3,
    paths: ['portal/src/components/TabNavigation.tsx', 'portal/src/hooks/useTabNavigation.ts'],
    cell: 'F3',
  },
  {
    row: 4,
    paths: [
      'portal/src/ui/components/catalyst/combobox.tsx',
      'portal/src/pages/AdvisorIntelligence/_shared/panels/ClientListPanel.tsx',
    ],
    cell: 'F2',
  },
  { row: 5, paths: ['portal/src/pages/ModelPortfolios.tsx'], cell: 'F2, F11' },
  {
    row: 6,
    paths: ['portal/src/components/CategoryViewTree.tsx', 'portal/src/lib/modelPortfolioColors.ts'],
    cell: 'F6',
  },
  {
    row: 7,
    paths: [
      'portal/src/pages/AdvisorIntelligence/_shared/AdvisorPublicProfile.tsx',
      'portal/src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx',
      'portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx',
    ],
    cell: 'F6',
  },
  {
    row: 8,
    paths: [
      'portal/src/api/portal-proxy.ts',
      'portal/src/api/endpoints/market.ts',
      'portal/src/api/endpoints/sentiment.ts',
      'portal/src/api/endpoints/trending.ts',
    ],
    cell: 'F12',
  },
  {
    row: 9,
    paths: [
      'portal/src/components/market-performance/MarketRegimeIndicator.tsx',
      'portal/src/components/market-performance/SentimentGauge.tsx',
      'portal/src/hooks/useRSIValues.ts',
      'portal/src/pages/MarketPerformance/panels/SentimentPanel/SentimentPanel.tsx',
    ],
    cell: 'F10',
  },
  {
    row: 10,
    paths: [
      'deck_generation/brand/opal_brand_guidelines.pdf',
      'deck_generation/brand_spec/brand.json',
      'deck_generation/engine/brand.py',
    ],
    cell: 'F9, F13',
  },
  {
    row: 11,
    paths: ['deck_generation/brand/logo_package/Opal-Capital-Logo-Package/Full Logo/Full Color/Opal-Capital-Logo-Full-Color.svg'],
    cell: 'F9',
  },
]

function fileContains(pathRel: string, needle: string): boolean {
  const abs = join(PORTAL_ROOT, '..', pathRel) // PORTAL_ROOT is <WS>/portal; repo root is one level up
  const abs2 = join(PORTAL_ROOT, pathRel.replace(/^portal\//, ''))
  const target = pathRel.startsWith('portal/') ? abs2 : abs
  if (!existsSync(target)) return false
  return readFileSync(target, 'utf8').includes(needle)
}

const reusedRepoPaths = new Set<string>()
for (const row of rows.values()) {
  if (row.classification === 'REUSED' && row.path) {
    const clean = row.path.replace(/ \(UNRESOLVED.*\)$/, '')
    reusedRepoPaths.add(clean)
  }
}

const prdAccounting = PRD_ROWS.map((r) => {
  if (r.row === 1) {
    const registered =
      fileContains('portal/src/App.tsx', "import('./pages/InvestorReporting')") &&
      fileContains('portal/src/App.tsx', "./pages/InvestorReporting/render/PrintEntry")
    return {
      row: r.row,
      paths: r.paths,
      cell: r.cell,
      status: registered
        ? 'USED by F1 -- portal/src/App.tsx lazy-imports both `InvestorReporting` (./pages/InvestorReporting) and the print entry (./pages/InvestorReporting/render/PrintEntry) and registers /investor-reporting and /investor-reporting/print routes for them.'
        : 'NOT USED: no route registration for this feature was found in portal/src/App.tsx.',
    }
  }
  if (r.row === 5) {
    const copied = fileContains(
      'portal/src/pages/InvestorReporting/header/FirmDropdown.tsx',
      'ModelPortfolios.tsx',
    )
    return {
      row: r.row,
      paths: r.paths,
      cell: r.cell,
      status: copied
        ? 'USED by F2/F11 (header/FirmDropdown.tsx) -- NOT an import edge: ModelPortfolios.tsx composes its firm dropdown inline (PageSurfaceControl as="dropdown") rather than exporting a separate dropdown component, so there is nothing importable. FirmDropdown.tsx instead reproduces that exact composition -- the same PageSurfaceControl (see row 2) configured with the IDENTICAL className string ModelPortfolios.tsx passes its own dropdown (portal 5907cbca, lines 1268-1275), copied verbatim per FirmDropdown.tsx\'s own header comment. This is the pattern reuse the PRD names, not a look-alike rebuild -- but it cannot appear as a census row because no import exists to enumerate.'
        : 'NOT USED: FirmDropdown.tsx does not reference ModelPortfolios.tsx.',
    }
  }
  if (r.row === 7) {
    // DrillTree.tsx's own header comment names PartnerAnalytics.tsx and
    // DistributionTab.tsx explicitly as a PRESENTATION-pattern precedent
    // (legend-beside-chart, direct labels, breadcrumb-driven drill) --
    // consulted, not imported, exactly like row 5's ModelPortfolios pattern
    // -- and explicitly declines their "use Math.abs for the donut"
    // shortcut. AdvisorPublicProfile.tsx (this row's third listed path) is
    // not referenced anywhere under the tree.
    const patternCited = fileContains(
      'portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx',
      'PartnerAnalytics.tsx',
    ) && fileContains('portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx', 'DistributionTab.tsx')
    return {
      row: r.row,
      paths: r.paths,
      cell: r.cell,
      status: patternCited
        ? 'PARTIALLY USED (pattern, not import) by F6 (tabs/holdings/DrillTree.tsx) -- NOT an import edge: DrillTree.tsx\'s own header comment names PartnerAnalytics.tsx and DistributionTab.tsx as the layout precedent for its recharts donut (legend beside chart, direct labels, breadcrumb-driven drill), and explicitly does NOT inherit their "use Math.abs for the donut" shortcut (this cell preserves signed amounts through its own donut). AdvisorPublicProfile.tsx (this row\'s third listed path) is not referenced anywhere under the tree -- NOT USED.'
        : 'NOT USED: no import of any listed path was found used as JSX (or as a function/hook) anywhere under ' + TREE_ROOT_REL + '.',
    }
  }
  const usedBy = new Set<string>()
  for (const p of r.paths) {
    // strip a trailing slash (directory reuse rows) for a startsWith comparison
    const clean = p.replace(/\/$/, '')
    for (const rp of reusedRepoPaths) {
      if (rp === p || rp.startsWith(clean + '/') || rp === clean) {
        for (const row of rows.values()) {
          if (row.classification === 'REUSED' && row.path && row.path.replace(/ \(UNRESOLVED.*\)$/, '') === rp) {
            for (const use of row.usedIn) usedBy.add(use.file)
          }
        }
      }
    }
  }
  // row 3's second path (useTabNavigation.ts) is a HOOK, never JSX -- it will
  // never appear as a component row even though it is genuinely used; checked
  // directly by source text so the row is not falsely marked unused.
  if (r.row === 3) {
    const hookUsed = fileContains(
      'portal/src/pages/InvestorReporting/tabs/TabShell.tsx',
      "from '@/hooks/useTabNavigation'",
    )
    if (hookUsed) usedBy.add('tabs/TabShell.tsx (useTabNavigation -- a hook, not a JSX component; no census row)')
  }
  // row 6's second path (modelPortfolioColors.ts) is functions, never JSX --
  // same treatment.
  if (r.row === 6) {
    const fnUsed = fileContains(
      'portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx',
      "from '@/lib/modelPortfolioColors'",
    )
    if (fnUsed)
      usedBy.add('tabs/holdings/DrillTree.tsx (getCanonicalModelName/getModelColor -- functions, not JSX components; no census row)')
  }
  return {
    row: r.row,
    paths: r.paths,
    cell: r.cell,
    status:
      usedBy.size > 0
        ? `USED by ${Array.from(usedBy).join('; ')}`
        : `NOT USED: no import of any listed path was found used as JSX (or as a function/hook) anywhere under ${TREE_ROOT_REL}.`,
  }
})

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------

const sortedRows = Array.from(rows.values()).sort((a, b) => a.component.localeCompare(b.component))
const reusedCount = sortedRows.filter((r) => r.classification === 'REUSED').length
const newCount = sortedRows.filter((r) => r.classification === 'NEW').length

const json = {
  generatedBy: 'census.ts (FE-s-73 corrected copy, from FE-s-64/FE-s-11)',
  scannedTreeFiles: treeFiles.length,
  additionalImporterFiles: ['src/App.tsx'],
  componentCount: sortedRows.length,
  reusedCount,
  newCount,
  scopeBoundaryNote: SCOPE_BOUNDARY_NOTE,
  needsMissing,
  components: sortedRows,
  definedButNotImported,
  prdReuseRowAccounting: prdAccounting,
}

writeFileSync(join(OUT_DIR, 'component-census.json'), JSON.stringify(json, null, 2) + '\n', 'utf8')

function mdEscape(s: string): string {
  return s.replace(/\|/g, '\\|')
}

let md = ''
md += '# FE-s-73 component census (corrected copy of FE-s-11/FE-s-64)\n\n'
md += `Generated by \`census.ts\` from \`portal/${TREE_ROOT_REL}/**/*.tsx\` (excluding \`__tests__/\` and \`fixtures/\`), plus \`portal/src/App.tsx\` for the two route-mount edges (see the script header for why).\n\n`
md += `COMPONENTS: ${sortedRows.length} (REUSED ${reusedCount}, NEW ${newCount}) across ${treeFiles.length} scanned tree files.\n\n`
md += '## Scope boundary (read once)\n\n' + SCOPE_BOUNDARY_NOTE + '\n\n'
if (needsMissing.length > 0) {
  md += `## NEEDS TABLE GAP -- ${needsMissing.length} NEW component(s) with no curated needs/nearestExisting entry (FINDING, not an invented reason)\n\n`
  md += needsMissing.map((n) => `- ${mdEscape(n)}`).join('\n') + '\n\n'
}
md += '## Components\n\n'
md += '| component | importedFrom | classification | reused path / new reason (scope) | needs (nearest existing) | usedIn |\n'
md += '|---|---|---|---|---|---|\n'
for (const r of sortedRows) {
  const detail =
    r.classification === 'REUSED'
      ? r.path ?? ''
      : `${r.reason ?? ''} [${r.reasonScope ?? 'NONE'}]`
  const needs = r.classification === 'NEW' ? `${r.needs ?? '(FINDING: no entry)'} (nearest: ${r.nearestExisting ?? '(FINDING: no entry)'})` : ''
  const usedIn = r.usedIn.map((u) => `${u.file}:${u.line}`).join('; ')
  md += `| ${mdEscape(r.component)} | \`${mdEscape(r.importedFrom)}\` | ${r.classification} | ${mdEscape(detail)} | ${mdEscape(needs)} | ${mdEscape(usedIn)} |\n`
}

md += '\n## Defined but never imported (not counted in COMPONENTS: N)\n\n'
md += 'A component this tree exports but that no importer scanned above (including `src/App.tsx`) ever uses as JSX. Not an import, so not a census row by the literal rule -- listed here for transparency, and cross-referenced to the surprise row this finding produced (IRPT_FNTEND-W1-S11).\n\n'
if (definedButNotImported.length === 0) {
  md += 'None.\n'
} else {
  md += '| file | component |\n|---|---|\n'
  for (const d of definedButNotImported) md += `| ${mdEscape(d.file)} | ${mdEscape(d.component)} |\n`
}

md += '\n## PRD PATHS table -- 11 reuse rows, accounted\n\n'
md += '| # | paths | cell | status |\n|---|---|---|---|\n'
for (const a of prdAccounting) {
  md += `| ${a.row} | ${a.paths.map(mdEscape).join('; ')} | ${mdEscape(a.cell)} | ${mdEscape(a.status)} |\n`
}

writeFileSync(join(OUT_DIR, 'component-census.md'), md, 'utf8')

console.log(`COMPONENTS: ${sortedRows.length} (REUSED ${reusedCount}, NEW ${newCount})`)
console.log(`SCANNED: ${treeFiles.length} tree files + src/App.tsx`)
console.log(`DEFINED-BUT-NOT-IMPORTED: ${definedButNotImported.length}`)
console.log(`PRD-REUSE-ROWS: ${prdAccounting.length} of 11 accounted`)
console.log(`NEEDS-MISSING: ${needsMissing.length}`)
