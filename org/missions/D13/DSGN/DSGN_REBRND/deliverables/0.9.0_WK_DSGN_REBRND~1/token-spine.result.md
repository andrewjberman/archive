# DSGN_REBRND.TO-RB-s-1 -- result (0.9.0_WK_DSGN_REBRND~1)

**Cell `RB-s-1`: the token spine -- ONE writer, the measured values, two disjoint colour families.**
Six criteria: five mechanical, all PASS by output; one (`RB1-AC6`) is judgment and is RECORDED with no
verdict for `3.0.0_SA_CVO` at L9.

- Portal commit **e830352e9693ab7fa2ad79f7aeaace8ae4a1e01d** -- LOCAL on branch `wk-dsgn_rebrnd-1` of the
  PORTAL repo (6 files, +392 / -105, `tailwind.config.js` deleted). Never pushed.
- Workspace commit **8c0b1af6571c14826947298edfd44a71997c18e5** (the surprise channel, opened fresh + 4
  rows) -- LOCAL on the same branch name in the WORKSPACE repo, committed before this proof.
- Proof of spec: `DSGN_REBRND.TO-RB-s-1.token-spine.proof_of_spec.json`, `proof-of-spec-check.py`
  **rc=0 (VALID)**.

---

## WHAT WAS BUILT

| Path (portal repo) | What it is |
|---|---|
| `design/brands/opal-capital.json` | the sole writer: navy/accent hex corrected to the FIXED brand values, canvas/darkField/mutedTint palette entries added, `semantic.background.default/inverse` repointed, new `status` (brand-derived) and `data` (preserved chroma) top-level families |
| `design/themes/opal-capital.css` | hand-updated generated theme: new `--palette-canvas/-darkField/-mutedTint` + corrected `--palette-navy/-indigo` (each with a hex comment), new `--status-*` (4) and `--data-*` (23) blocks; pre-existing Semantic block otherwise untouched |
| `design/tokens/brand-schema.ts` | `StatusPalette`/`DataPalette` types, `BrandDefinition.status?`/`.data?` |
| `design/tokens/brand-resolver.ts` | `generateStatusAndDataCSSVariables()`, additive, verified by direct execution, not wired into the file-writing pass |
| `src/index.css` | all 22 literal colour custom properties relocated to `var()` onto the generated theme; `--chart-1..5` de-aliased from status onto `--data-chart-*` |
| `tailwind.config.js` | deleted (confirmed dead: no `@config`, 0 live source references) |

### Three decisions worth reading

1. **The four brief-CONTRACTS "never redefined" values are all now present**: navy `#163372`, accent
   `#5F3BE3` (both corrections to the existing `navy`/`indigo` palette keys, not renames -- every existing
   `semantic.*` reference that already pointed at them keeps pointing at them), dark field `#0A1733` (new
   `darkField` key, wired to `semantic.background.inverse`), and the fourth fixed value `#C4CBDB` (new
   `mutedTint` key) that the cell's own prose does not name but the PRD's CONTRACTS section does.
2. **`--chart-1..5` and the legacy sentiment/model/asset/perf mini-palettes are repointed onto `--data-*`,
   not left on `--success`/`--info`/etc.** Those four now carry NEW brand-derived values (R8), so leaving
   the data-visualization aliases on them would have silently recoloured the Fear & Greed gauge, the model
   legend and the asset-class/performance gradients -- exactly the "charts keep their colour" constraint
   this cell exists to protect. `portal/src/lib/modelPortfolioColors.ts` was not touched.
3. **The pre-existing `opal-capital.css` was not run back through its own generator.** It already diverges
   structurally from what `generate-themes.ts` produces (no canonical-navy tiers, no `--bg-*` aliases) --
   running it would have regressed a structure `index.css` depends on today. The new `--status-*`/`--data-*`
   values were instead computed by executing the (extended) resolver directly via `bun` against the live
   JSON and copied into the checked-in file verbatim, so they are INSTRUMENT-VERIFIED, not hand-derived.

---

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| RB1-AC1 | PASS-by-output | `rc=0` | 1 of 1 typecheck project, 0 diagnostics |
| RB1-AC2 | PASS-by-output | `LITERAL-COLOUR-DEFS: 0` / `VERDICT: ONE-WRITER` | 0 of 22 pre-existing literals remain (22 relocated) |
| RB1-AC3 | PASS-by-output | `exists=1` | 1 of 1 file deleted |
| RB1-AC4 | PASS-by-output | `MISSING: []` / `VERDICT: ALL-PRESENT` | 4 of 4 required hex substrings present (0 of 4 before) |
| RB1-AC5 | PASS-by-output | `STATUS-ALIASED-CHART-TOKENS: 0 []` / `VERDICT: DISJOINT` | 0 of 5 chart tokens alias status (5 of 5 did before) |
| RB1-AC6 | RECORDED (judgment) | see below -- NO VERDICT TAKEN | 11 of 11 `darkMode.palette` entries + 5 of 5 semantic categories read |

### RB1-AC6 -- recorded, not graded

`darkMode` carries its own complete palette (11 colours, none shared with light) and its own complete
5-category semantic map, unchanged by this cell -- the light-mode fixes (canvas/darkField repointing)
touch only the light `semantic.background` branch. The description field still reads "Light mode by
default with toggleable dark mode." The selection MECHANISM already exists as code
(`design/tokens/theme-loader.tsx`'s `ThemeProvider`/`ThemeSwitcher`, a `.light-mode`-class + localStorage
toggle) but is not mounted in `src/App.tsx`/`src/main.tsx` (confirmed by grep: 0 hits outside
`design/tokens/` itself) -- mounting it is plumbing this cell's `<paths>` does not fully reach (`App.tsx`
is not granted) and no criterion asks for it. `index.html`'s static `data-theme="opal-capital"` is what
makes the generated CSS live at all. Not resolved by this cell, filed as surprise `DSGN_REBRND-W1-S3`:
the checked-in `opal-capital.css`'s own Semantic block does not yet reflect a light/dark split at all
(pre-existing, R3's structure to collapse) -- the split this AC asks about is complete in the JSON, not
yet in the generated CSS artifact.

---

## CONTROLS

**Mutants -- two, one per mechanically-graded regex family, each on a BYTE COPY in `.scratch/`, never on
the tracked file.**

| # | mutation | expected | observed |
|---|---|---|---|
| 1 | restored `--chart-1: var(--primary); --chart-2: var(--success);` (the pre-fix shape) | AC5 flips to ALIASED | `STATUS-ALIASED-CHART-TOKENS: 2 ['primary', 'success']` / `VERDICT: ALIASED` |
| 2 | restored `--success: 162 79% 46%;` (the pre-fix literal) | AC2 flips to MULTI-WRITER | `LITERAL-COLOUR-DEFS: 1` / `VERDICT: MULTI-WRITER` |

Both checks re-run against the real, unmutated, committed files immediately after: DISJOINT / ONE-WRITER
again. `git -C portal status --porcelain -- src/index.css` printed nothing throughout (clean against
`e830352e`).

**Determinism.** RB1-AC1/AC2/AC4/AC5 each run three times across the session (pre-edit baseline,
post-edit, post-commit) with no source change between the last two runs: identical output every time
(`rc=0`; `0`/`ONE-WRITER`; `ALL-PRESENT`; `0`/`DISJOINT`).

---

## SURPRISES

- **DSGN_REBRND-W1-S1** (OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~D`) -- the project's
  surprise-channel tree did not exist at all; this worker created it. A sibling worker slot whose
  worktree branched before this commit could independently create the same new file; the drain
  reconciles by union of rows, not by picking a side.
- **DSGN_REBRND-W1-S2** (OBSERVATION, INERT) -- `RB1-AC2`'s prose asserts 60+ literal colour defs at
  issuance; measured 22. Not acceptance-bearing (the printed value is the VERDICT string).
- **DSGN_REBRND-W1-S3** (OBSERVATION, INERT) -- `opal-capital.css` is hand-tuned, not byte-generated;
  two light-mode `semantic.background` slots (`muted`, `contentPanel`) still cross-reference
  `darkMode.palette` in the JSON, and the CSS's Semantic block does not yet reflect this cell's
  canvas/darkField repointing. Relevant to R3.
- **DSGN_REBRND-W1-S4** (OBSERVATION, INERT) -- the legacy `--model-*` CSS mini-palette (relocated,
  values preserved) disagrees with `modelPortfolioColors.ts` for the same named models; `--model-*` has
  no live consumer in `portal/src` today (grep-confirmed), so the disagreement is not currently visible.

All four rows are new appends to a channel this worker opened; `[surprise-row-gate]` confirmed
`4 new row(s) of 4 total checked (0 pre-existing, NOT re-graded)` and all four carry their step-7 fields.

## WHAT THIS CELL DID NOT DO

Restyle any component; touch `index.css:52`/`:132` or the canonical-navy nesting (R3's); build the radii/
shadow/`color-scheme` tokens the cell's prose mentions but no criterion tests; reconcile the two
model-colour systems or build R4's ramps; run `generate-themes.ts`'s file-writing pass; push, merge or
rebase. Full list with reasons in `declared_exclusions` of the proof instance.
