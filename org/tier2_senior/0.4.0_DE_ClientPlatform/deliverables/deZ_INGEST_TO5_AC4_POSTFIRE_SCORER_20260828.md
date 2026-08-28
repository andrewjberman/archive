# INGEST-TO5-AC4 — POST-FIRE SCORER + BASELINE

**Author:** `0.4.0_DE_ClientPlatform~Z` · 2026-08-28 ~04:1xZ
**Why this file exists:** no session live tonight reaches the ~13:00Z fire. Per `3.0.0_SA_CVO~Z`
(12638 s.5) **a carrier bound by DISCIPLINE fails and a carrier bound by NEED survives** — the
2026-08-25 watch file was walked past by three seats because someone had to *remember* to query it.
**This is a SCORER, not a reminder.** Whoever scores `INGEST-TO5-AC4` has to produce a render; this is
the method, the baseline it is scored against, and the traps that already cost time. It is useless to
ignore and unavoidable to use.

---

## 1. THE CRITERION, VERBATIM

> `INGEST-TO5-AC4` — **Condition (ii): BOTH vocabularies rendered SIDE BY SIDE on the DEV build** —
> `GICS_INDUSTRY_GROUP_NAME` beside the Bloomberg `HB_INDUSTRY_SECTOR_ALLOCATION` labels, **for him to
> point at.** NOT a swap. **Screenshot is the deliverable.**

Currently faced **KNOWN-UNREACHABLE** ("the field is not pulled"). ⛔ **THAT GROUND HAS EXPIRED** — the
field is pulled (`@ebce987b42`), gold and publisher carry it, and the served artifact gets it at the
fire. Re-facing to GATED-ON-EVENT is `2.0.0_SA_COO~Z`'s (ruled 12598/12613).

## 2. PRECONDITION — VERIFY BY CONTENT, NOT BY CLOCK

The fire having *run* is not the field having *landed*. Check the served bytes:

```bash
.tools/aws s3api get-object --bucket opal-data-portal-v2 \
  --key json/positioning/positioning_data.json "C:/<abs-win-path>/pos.json"
```
⚠ **The object is GZIPPED at rest** (`ContentEncoding: gzip`) — a naive JSON parse dies on byte `0x8b`.
`gzip.decompress(open(p,'rb').read())`.
⚠ **The aws shim rejects a POSIX destination** — pass a Windows path or it errors having written nothing.

Score it, **with the negative control**:
```
industry_group present on holding rows      -> required
industry_group_basis present                -> required (CTO 11831; and see s.5)
NEG CONTROL: a key that must NOT exist      -> must read absent, or the test cannot say NO
DENOMINATOR: rows carrying it / total rows  -- print both
```
**If the field is absent, AC4 is still not reachable and the correct act is to say so — not to render.**

## 3. THE RENDER

```bash
cd portal && <bun> run dev --port 5175          # ONE server only — see s.4
node scripts/ui-smoke.mjs positioning <out.png> --port 5175 --fixtures <served-bytes.json>
```
**Use the SERVED BYTES from s.2 as the fixture.**

> ⛔ **DO NOT USE `deZ_ETFS_INGEST_T5_SYNTHETIC_24value_fixture_20260824.json`.** It sits in
> THIS SAME FOLDER, it renders a beautiful passing page, and IT PROVES NOTHING ABOUT THE SERVED
> PLANE — it was built on 2026-08-24 to test LABEL GEOMETRY against invented values. A render
> against it produces a **FALSE PASS on the one criterion this file exists to prove.** If the
> fixture you are holding did not come out of s.2's `get-object` this minute, STOP.

Using the served bytes is what makes this a REAL measurement rather than a synthetic one: the
renderer is exercised against the actual served artifact.

⛔ **AND THE BOUND THAT MUST TRAVEL WITH THE RESULT:** this proves **renderer × real served data**. It
does **NOT** exercise the auth/CloudFront path, so it is *not* an end-to-end served render. The
credentialed route needs a real bearer (the stub passes the route guard while the edge 401s the data).
**Do not report AC4 as "verified on the served plane" without saying which of the two you did.**

## 4. BASELINE — WHAT "NO CHANGE" LOOKS LIKE, so absence is distinguishable from breakage

Rendered 2026-08-28 pre-fire, portal `@09f9078b`, fixture-driven:
- Sub-Asset cells show **the sector only** (`Information Technology`, `Financials`, `Energy`, …).
- **No second line, no placeholder** on any row. The absent case is silent BY DESIGN.
- Non-equity rows (`SHY`, `FXFXX`) render sector alone and are **expected** to stay that way —
  `industry_group_basis: not-applicable-non-equity`.

>> **SO A POST-FIRE RENDER THAT LOOKS LIKE THIS BASELINE MEANS THE FIELD DID NOT ARRIVE — NOT THAT THE
   RENDER IS BROKEN.** That is the whole point of recording it. Confirm against s.2 before concluding.

**PASS looks like:** a second, recessive, wrapped line under the sector on equity rows, taking the
sector cell's own background (dark on pale ramp steps, light on deep ones).

## 5. TRAPS ALREADY PAID FOR

| trap | cost if rediscovered |
|---|---|
| **FIVE edit sites, not four.** `HoldingsTab.tsx` Current-period mapper is an ENUMERATED object literal, no spread — it silently swallowed the field between a populated payload and a correct renderer. Its sibling ~50 lines below DOES spread. | Reading the file twice missed it; one render found it. |
| **Column geometry.** Sub-Asset col is 165px FIXED; longest GICS industry group is 46 chars. Values >~34 chars OVERFLOW into Ticker unless the recessive span wraps. `whitespace-normal` is the shipped remedy (b); (a) widen / (c) truncate remain open to a CTO ruling and are one-property changes. | A shipped collision on a client-facing page. |
| **Two vite servers share one dep cache.** A junctioned `node_modules` brings `.vite` with it; a second server re-optimises under the first and produces a route-specific `useRef of null` crash that reads as a real defect. A *different* route rendering clean does NOT clear it. | Nearly reported a manufactured crash on a page named in a sovereign instruction. |
| **`--click "SATELLITES"` fails; the accessible name is `Satellites`.** The uppercase is CSS. | One wasted 30s timeout. |
| **`industry_group_basis` is RECEIVED and deliberately NOT DISPLAYED.** CTO 11831 s.2 + 12172/12205 NARROW: the prohibition was lifted, nothing new authorised. A basis-derived render distinction is a SCOPE call at `2.0.0_SA_COO~Z`, with a Rule 24 caveat (it groups a 5-value enum 2-and-3). | Building it unbidden widens a frozen TO. |

## 6. WHAT THIS FILE DOES NOT COVER

- The **second** gated act — the `D1_CATVIEWS` fixture re-derivation (`TO-P1-AE:239-240`, full sentence:
  *"re-derives the fixture against the served artifact once one exists, **and reports disagreement as a
  DE finding.** Nothing is owed to that lane by this TO."*). **DIFFERENT TRIGGER**: `TP1AE-AC1`
  satisfied, i.e. `category_views` observed on the served plane — and per that TO's own title the
  scheduled run does not yet emit it, so the gate is AE's re-cut landing, **not** a clock.
- `POS-TO7-AC4/AC5` (`ETFS_POSITIONING.TO-7`) — seated to this serial, undischarged, **not taken**:
  Rule 27, different project, seating is `2.0.0_SA_COO~Z`'s.
- Whether the ~13:00Z fire actually emits the field. **Unmeasured here by construction** — that is s.2.

---

## 7. WRONG-READING TABLE — what a LITERAL execution of each step produces when it is wrong

Added 2026-08-28 ~05:1xZ, amending this file against `3.0.0_SA_CVO~Z`'s corrected carrier rule
(@`ea464ce569`): **need-binding is NECESSARY AND NOT SUFFICIENT.** A discipline-bound carrier nobody
reads is inert and its bad steps cost nothing. **THIS FILE IS BUILT TO BE EXECUTED LITERALLY BY A COLD
READER** — which converts any insufficient step from a dormant defect into an executed one. So every
step now states what a wrong reading yields, WHICH VERDICT, and WHOSE LANE it routes to.

| step | the wrong reading | verdict it produces | routes to |
|---|---|---|---|
| **s.2** field ABSENT | "the render is broken" | FALSE FAIL against DE | ⛔ NOT DE. Absent means AC4 is **STILL UNREACHABLE**, not failed. Route to the PRODUCER chain — did the ~13:00Z fire run, and did gold/publisher carry the key. DS/AE lane. |
| **s.2** skipping the negative control | "the key is absent" off a broken retrieval | FALSE FAIL, unattributable | Nobody. A retrieval that cannot say NO has produced no evidence — re-run before routing anything. |
| **s.3** rendering a fixture you wrote | "AC4 discharged" | ⛔ **FALSE PASS** — the dangerous one | Nobody, and that is the point: it closes the criterion. See the block in s.3. |
| **s.3** fixture render reported as end-to-end | "verified on the served plane" | over-claim; auth/CloudFront path never exercised | Reporting error — catch before filing, not after. |
| **s.4** post-fire render MATCHES the baseline | "the render regressed" | FALSE FAIL against DE | ⛔ NOT DE. It means the FIELD DID NOT ARRIVE. Confirm via s.2, then route to the producer chain. |
| **s.4** line renders with WRONG VALUES | "the render is wrong" | mis-attributed | ⛔ NOT DE. The renderer prints what it is given. Wrong CONTENT is a gold/publisher question. DS lane. |

⛔ **THE ASYMMETRY THAT DECIDES WHICH ROW MATTERS MOST:** every FALSE FAIL above gets investigated and
is recoverable. **The s.3 FALSE PASS ends inquiry** — it closes AC4 with a screenshot that never
touched the served plane. That row is why this table exists.
