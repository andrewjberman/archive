# DSGN_REBRND.TO-RB-s-2 -- result (0.9.0_WK_DSGN_REBRND~1)

**Cell `RB-s-2`: typography -- Lato self-hosted, tabular numerals, the mono census to zero.**
Six criteria: **five mechanical, all PASS by output**; one (`RB2-AC6`) judgment, RECORDED with no
verdict for `3.0.0_SA_CVO` at L9. `<status>` flipped to `complete`.

This is the second pass at this order. The first left `RB2-AC4` FAIL and the status `pending`,
because the Lato binaries could not be obtained without unauthorized external egress. The issuer
then found the faces already on this box, staged them into the worktree, and amended `RB2-AC4`
onto a form that actually discriminates. Nothing was fetched.

- Portal commit **748384e4641dbcea998e652f04ae29e21d112ae0** -- the shipped faces + the `@font-face`
  repoint (4 files, +60 / -42). LOCAL on `wk-dsgn_rebrnd-1c`. Never pushed.
- Workspace commit **d4eefbe04e74e16568b9a86c7f59059d77dc6a76** -- channel row `W1-S8`.
- Earlier, merged in from the previous pass: portal **15c2cb7f** (the 266 monospace removals, the
  Inter/Google-Fonts removal, and the `RB-s-1` CSS-parse-break fix).
- Proof of spec: `DSGN_REBRND.TO-RB-s-2.typography-lato.proof_of_spec.json`,
  `proof-of-spec-check.py` run from inside `<WS>` with the worktree's own copy: **rc=0 (VALID)**.

---

## WHAT SHIPPED, WITH ITS HASHES

| file | served as | the face IS | sha256 |
|---|---|---|---|
| `portal/public/fonts/lato-regular-400.woff2` | `font-weight: 400` | Lato Regular, usWeightClass **400** | `08c7108aa1b1b718e1910cbd38976108193d814c354c1cc5a46dee0cacf786ac` |
| `portal/public/fonts/lato-semibold-600.woff2` | `font-weight: 700` | Lato SemiBold, usWeightClass **600** | `0f8199f77a24bd3e91d999ebc24e221609220efdcbd5898bfbb75d968a422594` |
| `portal/public/fonts/OFL.txt` | -- | SIL OFL 1.1, Reserved Font Name "Lato" | (unchanged from the previous pass) |

Converted **locally** (fontTools 4.63.0 + brotli; no network request, and none is authorized) from
the three `.ttf` faces staged into the worktree:

| source `.ttf` | family / subfamily (from its OWN `name` table) | `OS/2.usWeightClass` | sha256 | shipped? |
|---|---|---|---|---|
| `Lato-Regular.ttf` | Lato / Regular | 400 | `d636e4683231f931eda222d588e944d082bfd3bdba02f928bee461c0f185b251` | yes, as the 400 |
| `Lato-SemiBold.ttf` | Lato / SemiBold | 600 | `71b8b7decbe75a881ed267be539d402bd1e9420b799658aada4e0d1bd5af803c` | yes, as the 700 |
| `Lato-Light.ttf` | Lato / Light | 300 | `cf2a774503baf418d584f49967bd160e1e03f087c13b25602f28024ec7788f08` | **no** -- see below |

Identity was read from each face's own `name` table and `OS/2.usWeightClass`, **never from its
filename**, both before and after conversion; family, subfamily, weight class and glyph count
(3023) are unchanged by the conversion and `fsType` is 0 (no embedding restriction).

**`Lato-Light.ttf` is deliberately not shipped.** The cell restricts the product to two weights
("restricting to two forces SIZE and WHITESPACE to carry hierarchy"), so no `@font-face` rule
references a 300 face and shipping it would serve a weight the design has ruled out. Its hash is
recorded here and in the fonts README so the decision is visible, not silent.

---

## THE BOLD IS A SEMIBOLD

A real Lato Bold is not on this box — the three staged faces are 300/400/600, read from their own
weight classes — and fetching one is not authorized. `font-weight: 700` therefore maps onto the 600
SemiBold, so **every bold figure and heading in the product is ~100 weight units lighter than the
measured site's bold.** Filed as `DSGN_REBRND-W1-S8`; carried to Andrew by the issuer.

The substitution is stated in three places that cannot drift apart: the **filename** says `600`, the
**`@font-face` rule** says it is served as `700`, and **`portal/public/fonts/README.md`** says both.
When a real Bold arrives it is one file drop plus one rule repoint.

---

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| RB2-AC1 | PASS-by-output | `rc=0` | 1 of 1 project, 0 diagnostics |
| RB2-AC2 | PASS-by-output | `FONT-MONO: 0 in 263 tsx files` / `VERDICT: CLEARED` | 0 of 221 pre-existing occurrences remain |
| RB2-AC3 | PASS-by-output | `GOOGLE-FONTS: 0 INTER-REFS: 0` / `VERDICT: SELF-HOSTED` | 2 of 2 substrings absent; 2 of 2 font requests same-origin |
| RB2-AC4 | PASS-by-output | `FACES: [...400.woff2, ...600.woff2]` + both hashes + `LICENCE: ['OFL.txt']` / `VERDICT: SELF-HOSTED-ON-BOX` | 2 of 2 declared faces, 1 of 1 licence, 4 of 4 directory entries accounted for |
| RB2-AC5 | PASS-by-output | `CANVAS: rgb(195, 202, 218)`, real page TEXT, `rc=0` | 1 of 1 route captured, non-blank |
| RB2-AC6 | RECORDED (judgment) | see below -- NO VERDICT TAKEN | 6 of 6 sampled figures compute Lato + tabular-nums |

### RB2-AC6 -- recorded, not graded

**The firm typeface is now actually applied, measured rather than eyeballed** (three independent
instruments):

- **Network:** the page fetched exactly two fonts, both same-origin —
  `200 lato-semibold-600.woff2 | 200 lato-regular-400.woff2`. Zero external font requests.
- **FontFaceSet:** `document.fonts` holds `Lato 400 normal status=loaded` and
  `Lato 700 normal status=loaded`.
- **Computed style, on real figures:** the RSI axis numerals `0 / 30 / 50 / 70 / 100` (SVG `tspan`)
  and the Fear & Greed value `50` (SVG `text`) each compute `font-family: Lato` with
  `font-variant-numeric: tabular-nums`, at weights 400 and 700. No element resolves to a monospace
  stack.

**A check I ran and then rejected, stated so nobody re-derives it:**
`document.fonts.check('400 16px Lato')` returns `true` — but so does
`document.fonts.check('400 16px NoSuchFaceXYZ')`, which I ran as a negative control.
`FontFaceSet.check()` reports whether the text can be rendered with *any* fallback, so it is not
evidence of the named family. It is not cited above. (Same failure shape as `W1-S6`: a green that
cannot go red.)

**Alignment, honestly.** No capture of `/market` exists from before the font work, so no pixel diff
of numeral alignment is offered. What *is* observable between the fallback render and this one: two
panel titles (`GLOBAL RSI`, `U.S. REGIME`) now wrap to two lines under Lato's metrics where they
were single-line under Segoe UI — no clipping, no overlap, nothing unreadable, but a real reflow the
grader should see stated rather than discover. Numeral columns are unchanged in structure:
`tabular-nums` is still the single global token and every removal in this cell was font-family-only.

---

## CONTROLS

**Mutants — and one of them changed what I was willing to claim.**

| # | control | expected | observed |
|---|---|---|---|
| 1 | run the amended `RB2-AC4` form against the tree before the faces were copied in | reports no faces | `FACES: []` / `NO-FACES-OR-NO-LICENCE` — the amended criterion discriminates where its predecessor could not |
| 2 | request an absent face (`/fonts/lato-700.woff2`) from the dev server | distinguishable from a present one | **it also returned HTTP 200** — Vite falls back to `index.html` (826 bytes, `text/html`). Status code alone proves nothing. |
| 3 | `document.fonts.check()` on a nonexistent family | must be `false` | **returned `true`** — instrument discarded, not cited |

Because of (2), the served-artifact claim rests on content-type `font/woff2`, the `wOF2` signature
in the first four bytes, and the **served bytes hashing identical to the shipped bytes** — not on
the status code.

**Determinism.** The four command criteria: identical output across two runs each. The woff2
conversion, however, **is not byte-deterministic**, and since a sha256 is recorded as identifying
evidence that had to be resolved rather than left as an unknown: two conversions of the same `.ttf`
differ, and a table-level comparison shows **exactly one of 17 tables differs** — `head`, in
`head.modified` (a save timestamp one second apart) and its derived `checkSumAdjustment`.
`head.created` and every glyph, metric, cmap and name table are byte-identical. **The font is
reproducible; the container bytes are not.** The recorded hashes identify the bytes shipped and
served (verified equal), not a re-derivable build. Noted in the fonts README so a future
re-derivation does not read as tampering.

---

## SURPRISES

- **DSGN_REBRND-W1-S8** (OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~D`) — the bold weight is a
  SemiBold; carried to Andrew by the issuer. Supersedes the BLOCKING half of `W1-S5`.
- Carried from the previous pass, unedited (append-only): **W1-S5** (the binaries, now shipped),
  **W1-S6** (the old `RB2-AC4` could not discriminate — since amended by the issuer), **W1-S7** (the
  `RB-s-1` CSS parse break, fixed).

`[surprise-row-gate]`: `1 new row(s) of 14 total checked (13 pre-existing, NOT re-graded)`.

## WHAT THIS CELL DID NOT DO

Ship a 300 face or a real 700 Bold (reasons above); fetch anything over the network; touch
`.ir-mono`/`print.css` (different grain); add letter-spacing; touch any file outside `<paths>`;
push, merge or rebase. Full list with reasons in `declared_exclusions` of the proof instance.
