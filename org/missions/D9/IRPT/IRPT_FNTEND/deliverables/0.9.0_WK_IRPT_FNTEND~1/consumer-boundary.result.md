# IRPT_FNTEND.TO-FE-s-25 -- the consumer boundary: a distinction the contract makes must survive arrival

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` (slot ~1)
**Branch:** `wk-irpt_fntend-4-1-fe-s-25` (workspace and portal), cut from CLOUD @`f3b42b1e0b` / DEV @`237a9027`
**Portal commit:** `abd470c7` -- LOCAL. Portal is frozen: no push, no gitlink bump.
**Order status:** **NOT flipped -- left `pending`.** Two mechanical criteria fail by output (`F25-AC6`,
and `F25-AC10` with it). A valid instance is not a met order.

---

## THE RESULT IN ONE PARAGRAPH

Nine of eleven mechanical criteria pass by output. `F25-AC12` is a judgment criterion and carries a
record with no verdict. **`F25-AC6` fails at 7 of 9**: QUEUED and RUNNING still render identically at the
panel, and each honest remedy needs a path this order's `<paths>` does not name. That is filed as BLOCKING
row `IRPT_FNTEND-W1-S49`. **`F25-AC10` fails as a consequence** (`11 pass / 1 fail`), because the fe-s-25
folder contains the arm that asserts AC6's true bar. I did not weaken that arm to turn the folder green.
Three of the four defects are fixed at the view. The fourth (`W1-S41`) is fixed as far as arrival: the view
now **carries** the producer's state but does not **render** it.

---

## WHAT A READER OF THE PAGE CAN NOW TELL APART -- one entry per row

Every "before" below is the production path at `237a9027`, where a status envelope reached the panel
through `envelopeFromAvailability(status.availability)`, whose source-age slot was `source_dates.as_of`.

### `W1-S43` -- ABSENT vs NULL (`F25-AC2`, `F25-AC3`)

| no-answer state | `business_date` ABSENT | `business_date: null` |
|---|---|---|
| QUEUED, RUNNING, UNAVAILABLE, FAILED -- **before** | `No source age yet` | `No source age yet` |
| QUEUED, RUNNING, UNAVAILABLE, FAILED -- **now** | `No source age yet` | `Source date malformed` |

**A reader can now tell a job that has no source date yet from a producer that broke the contract.**
Before, a null was indistinguishable from an absence, which is the collapse the schema's `$comment`
forbids. Now the null is named as the defect it is. The DOM key tells the two apart as well
(`no-source-age-yet` vs `malformed`).

The fix is to the grain, not just the string. `adaptStatusEnvelope` takes the three-way fact **on the
wire object** and carries it as `StatusEnvelope.sourceDate`, so a consumer holding only the view object can
still tell the two apart. fe-s-21 recorded that as impossible, and its disclosing arm still passes because
`sourceTimestamps.businessAsOf` is, correctly, null in both cases. The pattern is enforced as well as the
instance: a scan of `contracts/` and `state/` over **the 35 distinguished fields, found by subtracting from
the schemas' 309 declared properties**, finds **0** coalesces of the form `?? null` among **19**. The positive
control fires **2 of 2** on seeded coalesces. The negative control, a legal coalesce on the nullable
`as_of`, fires **0**.

### `W1-S42` -- the age reads the field the clause governs (`F25-AC4`, `F25-AC5`)

A READY envelope carrying the REQUIRED `business_date` and no `as_of`:
- **before:** `Source time unknown` -- the amendment's success case wearing its failure case's words.
- **now:** `Updated 2d ago`, DOM key `age`.

**A reader can now tell a conforming READY from one that lost its date.** READY with `business_date` absent
still reads `Source time unknown`, so the anomaly is still named. Field agreement is structural. The field
name is declared once (`GOVERNED_SOURCE_DATE` in `contracts/index.ts`), the adapter reads `.wire`, and
the age basis reads `.view`. The code of `state/status.ts` contains **0** occurrences of `as_of`. The
behavioural arm hands the two fields **different dates** (business `2026-09-11`, as_of `2026-09-05`), and on
all 5 answer-bearing states the panel says `Updated 2d ago` where an `as_of` reader would say `Updated 7d ago`.

### `W1-S41` -- two different nines (`F25-AC6` FAIL, `F25-AC7` PASS)

**A reader still cannot tell a queued job from a running one.** With every wire field except `state` held
constant, both render `Loading | No source age yet | <reason code>`. What changed is below the page: the
view `StatusEnvelope` now carries `producerState` verbatim, so the distinction is **no longer lost on
arrival**. What is missing is a renderer that reads it. Both planes are now printed with their own
denominators and the full mapping (AC7): producer 9, view 9, 8 view states reached, the view member
`RETRYABLE` reached by no producer state, and one collapse (QUEUED and RUNNING both onto LOADING).

Why AC6 was not forced green (full detail in row `W1-S49`):
- **A tenth view state** would redden `__tests__/fe-s-3/status.test.ts:31`
  (`expect(ENVELOPE_STATES).toHaveLength(9)`). fe-s-3 is not in `<paths>`, and no criterion here runs it,
  so the breakage would have been silent.
- **A rendered carrier** needs `tabs/StatusPanel.tsx`, which is not in `<paths>`.
- **Three workarounds inside the grant were refused** because each makes the page say something false:
  overwriting the producer's reason code, putting a job state in the source-age slot (which fe-s-21 pins to
  `No source age yet`), and mapping RUNNING onto RETRYABLE.
- **Disclosed, not graded:** giving each state its own reason code renders 9 of 9. That measures the
  fixture; the schema makes no per-state promise about the code.

### `W1-S26` -- the generator (`F25-AC8`, `F25-AC9`)

Not reader-facing. It is developer-facing, and that is where the defect lived. Regenerating
`StatusEnvelope` emits all **7 of 7** properties, and the committed wire file equals the render. **A developer
regenerating against a construct the generator cannot render now gets an error naming the coordinate**
(`UNRENDERABLE SCHEMA at Seeded.schema.json#/properties/unrenderable`), where before a legal-looking
`unknown` was emitted and could pass review. The negative controls hold: the live schema does not trip the
guard, and **all 22 live schemas regenerate byte-identically** with it in place. Importing the generator no
longer runs it. `generate()` now sits behind `import.meta.main`, so a test can grade `renderModule` without
rewriting `contracts/wire/`, and in particular without touching the three wire files the BOUNDS exclude.

---

## THINGS THE L9 GRADER SHOULD WEIGH (`F25-AC12`, recorded, no verdict)

1. **The age of a status envelope now comes from `business_date` even when `as_of` is present.** That is
   what AC5 asks for, and it is a behaviour change. An `as_of` six days older than the business date no
   longer drives the string. The envelope still carries `as_of` on its own `sourceAsOf` member.
2. **`TabEnvelope.sourceAsOf` widened** to `Instant | SourceDateReading | null`. Every out-of-grant
   consumer (`StatusPanel.tsx`, `tabs/analysis/StageDisplay.tsx`, `tabs/analysis/VariantSelector.tsx`,
   `export/submit.ts`, `state/hooks.ts`, `state/selection.ts`) typechecks unchanged. They build their
   envelopes from an `Availability` instant, so their runtime behaviour is unchanged too. The member name
   now covers more than a timestamp.
3. **The whole suite is not a bar here** (ruling C), but it was read once for blast radius:
   `460 pass / 1 skip / 1 fail`, and on a second run 3 fail. The failures belong to
   `fe-s-19/mounted-from-wire.test.ts`, whose header declares a precondition of a vite dev server on port
   5181, which was not up; and `fe-s-18` F18-AC3, which declares its own failure in its name. Neither is in
   this cell's surface.
4. **No distinction was invented.** `Source date malformed` renders only for a null the wire actually
   sent. The age renders only from a date the wire actually sent. `producerState` is the producer's own
   token, carried and not rendered.

---

## ROWS

`IRPT_FNTEND-W1-S49` -- BLOCKING, INERT. F25-AC6 cannot reach 9 of 9 inside this grant.
