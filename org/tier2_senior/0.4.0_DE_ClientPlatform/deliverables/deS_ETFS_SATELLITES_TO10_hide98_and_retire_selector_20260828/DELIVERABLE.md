# ETFS_SATELLITES.TO-10-DE -- Andrew's smoke feedback

**Seat:** `0.4.0_DE_ClientPlatform~S` · **Issuer:** `2.0.0_SA_COO~Z` · **Certifies:** `3.0.0_SA_CVO~Z`
**Cells:** `SAT-d-1` · `SAT-b-5` · `SAT-c-2` · `SAT-c-3` · `SAT-d-2`
**Portal commit:** `5a4349a5` on `DEV` (3 files, +196/-51) · TO read at `31d7d685d2`, amended `543a487dec` (AC8/AC9) and `8c863d5f22` (AC3)

**8 of 9 met. `T10DE-AC3` is NOT SCOREABLE** -- pending Andrew's acceptance viewport, ruled by the
issuer as their own criterion defect rather than a failure of the work.

---

## 1. WHAT ANDREW ASKED FOR, AND WHAT HE WITHDREW

He smoke-tested the Satellites view on a localhost build and it **passed** -- *"looks very good, its
basically done only a couple points id add"* -- then **superseded his own first point** minutes later:
hiding `Satellite 98` removes the ninth column, so the scroll he had asked for is *"no need for
arrows"*. This TO is the surviving points.

## 2. ACCEPTANCE CRITERIA

### `T10DE-AC1` -- 98 hidden, AT THE RENDER LAYER · **MET**

`SATELLITES_HIDDEN_FROM_DISPLAY` is declared **in the page component** and applied between the served
registry and the adapter. Eight books render.

⛔ **It lives there precisely so it cannot be mistaken for a membership edit.** `SAT-b-5` makes the
direction of the tempting mistake concrete: **`Opal Satellite 98` has ELEVEN accounts and `90` has
ZERO**, so "same characteristics, drop one" is true of the DISPLAY and false of the DATA -- solving it
in membership would have deleted the populated book and kept the empty one.

### `T10DE-AC2` -- still tracked · **MET, BY RE-READ AFTER THE EDIT**

```
s3://opal-data-cot/platinum/satellites/registry.json   (read AFTER the change)
books served 9 · as_of 2026-08-27 · 0 of 9 fail the sum check
"Opal Satellite 98" still present: TRUE
sha256 0989650ab6a7541d...  UNCHANGED
```

Banked verbatim as `registry_served_AFTER_the_change.json`. **The criterion asks about the state after
the change; citing the earlier measurement would have answered a different question.**

### `T10DE-AC3` -- the width · ⛔ **NOT SCOREABLE**

```
1440px   8 columns CLIP -- the 8th column and its labels are cut
1600px   all 8 labels present; the 8th bar's VALUE labels still clip ("8.1", "91.9")
1920px   FITS CLEAN -- 8 columns, all labels, no scrollbar, no arrows
```

**Whether eight columns "fit" is a function of viewport width, and the criterion named none.** The
issuer has ruled this their own defect and amended it; the acceptance viewport is with Andrew.

⛔ **I did not close it by adding a scroll.** He withdrew the scroll explicitly, and building it anyway
would substitute a lane's judgement for his ruling on a page he had just approved. **His own viewport
width is unknown, so it cannot be checked against the screenshot he sent.**

### `T10DE-AC4` / `AC5` -- no selector, commented not deleted · **MET**

Internal viewers land on cottonwood with **no selector and no extra click**. The dropdown and **every
dependency it needs** carry a `TO-10-DE AC5` marker: both imports, `awaitingFirmSelection`, the query's
`enabled` clause, and the `firm-unselected` member across type, copy and style. `satelliteSelectableFirms()`
and `satelliteFirmLabel()` remain **exported and derived from `MODE_FIRM_ALLOWLIST`**, so re-enabling is
uncomment-only and a second entitled firm makes the selector correct again.

⚠ **The default is DERIVED, not a literal** -- `selectableFirms[0] ?? COTTONWOOD_FIRM_ID`. A firm added
to the allowlist moves it rather than being silently ignored by a hard-coded `'cottonwood'`.

### `T10DE-AC6` -- the discrimination survives · **MET, BY HASH**

```
populated  dbfeb0c1e701c6ee     empty  e02b1764dfb1fd5b
failed     92225d65f302069f  \  intended collision, unchanged from TO-8-DE
as_of null 92225d65f302069f  /
```

⭐ **The `empty` and `failed` hashes returned EXACTLY to their `TO-8-DE` values.** Removing the selector
restored the pre-`TO-9-DE` render for those states byte-for-byte -- **a did-not-move control that fell
out of the measurement rather than being constructed.**

### `T10DE-AC7` -- rendered · **MET**

Six read screenshots: four states at 1440, plus 1600 and 1920 for AC3. Canvas law holds; the header
carries only the mode pills.

### `T10DE-AC8` / `AC9` -- the gradient · **MET**

Orange -> yellow -> green -> blue -> red, **left to right, orange on `Satellite 15`**, eight distinct
colours across the displayed set.

⛔ **Direction was NOT derived from the Duration column.** It falls left-to-right (2.89 ... 1.81), which
reads as "shortest is rightmost" and inverts the gradient. Andrew's own reason: equity weight rises
rightward and **equity has no duration**, so the blended average falls because the fixed-income sleeve
shrinks. The falling number is a misnomer.

⭐ **AND THE FIX IS GATED SO MODELS AND ETFS ARE BYTE-UNCHANGED -- proven arithmetically, not asserted:**

```
models      n=5   ramp == old cycling   IDENTICAL
etfs        n=4   ramp == old cycling   IDENTICAL
satellites  n=8   8 DISTINCT colours    (old cycling gave 5 of 8 -- it REPEATED)
```

**Interpolating unconditionally would have silently recoloured ETF mode**, because 4 books against 5
stops is exactly the case where indexing and interpolation disagree. **Index while the palette can give
every book its own stop; interpolate only once it cannot.** That is the case `AC9` names, and nothing
else moves.

## 3. INSTRUMENT CHANGE, DISCLOSED

`ui-smoke.mjs` gains `--width <px>`, default **1440 unchanged** so every existing capture stays
byte-comparable. **A criterion of the form "N columns fit" is ABOUT the viewport; an instrument pinned
to one width reports that width's clipping as a property of the page.** AC3's answer is only expressible
because the instrument can vary the thing the criterion is about.

## 4. GATES

```
tsc -b --noEmit   rc=0        eslint  rc=0        non-ASCII added lines  0
```

⚠ **One eslint WARNING stands and is deliberately not suppressed:** `setSelectedFirmId` is unused
because only the commented selector calls it. Renaming it `_setSelectedFirmId` would silence it **and
break the uncomment-only property `AC5` requires**. The warning is the cheaper of the two and is better
visible than hidden.

## 5. NOT DONE, NOT MINE

- **AC3's remedy** -- pending Andrew's acceptance viewport. ⛔ Issuer-ruled: no narrower-viewport fix on
  this lane's own judgement; his named alternative was shrinking text/bars, and the scroll is the thing
  he withdrew.
- **The router, the registry, the producer, `SATELLITE_MEMBERS`** -- untouched, and AC2 exhibits it.
- **The PROD promote** -- DT lane, held at Andrew's word.
