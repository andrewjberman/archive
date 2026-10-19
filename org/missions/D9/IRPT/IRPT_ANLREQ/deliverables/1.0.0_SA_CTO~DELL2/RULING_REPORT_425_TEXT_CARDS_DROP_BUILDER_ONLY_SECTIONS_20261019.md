# Ruling -- the report page shows 425 empty "text" cards: sections[] drops BUILDER_ONLY entries

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~13:4xZ. **Source:** Andrew-direct PROD smoke at 13:43Z, relayed by the laptop
`1.0.0_SA_CTO` through `0.0.0_AB_MSTR~DELL2` (msg 10692, bus 27628202). On the Analysis Request report page, Andrew saw 425
cards titled "text". Each read Method BUILDER_ONLY, Not available NOT_IN_THIS_VERSION, Unit unknown.

## Read at ruling

`infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py`:
- **`:531`** builds `sections` from EVERY run.json entry.
- **`:168-171`** (`_entry`): an element with no computed result gets `method` `BUILDER_ONLY` when the layout says it is
  builder-drawn, with status `NOT_AVAILABLE` and reason `NOT_IN_THIS_VERSION`.
- **`:174-189`** (`_section`): it emits the element as a section whose `section_type` is the layout kind (`text`).

So the static text that the PDF builder draws itself reaches `sections[]` and the page as empty cards. The portal renders
what it is given; there is no portal defect.

## RULING

1. `sections[]` excludes every entry whose `method` is `BUILDER_ONLY`. `run.json` keeps every entry, unchanged.
   Vendor-sourced elements that are `NOT_AVAILABLE` stay as cards, so a missing value still shows honestly.
2. **Owner:** `2.0.0_SA_COO~Y2`, ONE LOCAL cell now. Its acceptance, on the overview fixture:
   - 0 sections with method `BUILDER_ONLY`;
   - every `VALUE` section byte-equal to before;
   - the section count printed before and after.
3. **Release:** a resident release with its own never-widen pair; IB2 applies it after 14:15Z. It goes ahead of
   `TO-RUN-COMMENTARY-E2E-3`, or rides with it only if `~Y2` shows the two do not interact.
4. **ETA given to Andrew** (through the laptop CTO): clean new reports by ~17:00Z today. A report already produced keeps
   its sections until a new filing.

---

## ADDENDUM 1 (2026-10-19 ~15:3xZ) -- 425 was not reproduced on the overview map; the fix widens to NOT_IN_THIS_VERSION

**Answers:** `2.0.0_SA_COO~Y2` msg 10756.
- AR-y-404 is merged (3676d5836b); 2 and 48 tests pass.
- Offline, the fix drops 65 cards on the overview map. The comparison map has 223 builder-only elements, and the multi
  map has 280 of 424.
- Andrew's 425 cards are closest to the multi map (424 elements), but his variant is not read.

**RULING:**
1. `~Y2` reads the variant of Andrew's 13:43Z request from its own request item, the same read-only get-item as for
   REQ-d6231c013ae90519c67d18e9. The acceptance is re-run on THAT variant's map.
2. **The page shows no empty "not in this version" cards.** `sections[]` also drops entries whose reason is
   `NOT_IN_THIS_VERSION`. In their place, `disclosures[]` gains ONE line naming how many elements this version does not
   yet include. run.json keeps every entry.
3. Entries that are NOT_AVAILABLE for any other closed reason (`COVERAGE_BELOW_0.95`, `STALE_INPUT`, an input missing)
   stay as cards, because their reason is real information about the client's data.
4. The acceptance, on Andrew's variant's map:
   - 0 sections that are BUILDER_ONLY or `NOT_IN_THIS_VERSION`;
   - every VALUE section byte-equal;
   - the disclosure count equals the dropped count;
   - the section count printed before and after.
5. This rides the same r34l release (TO-AR-y-406) as one more mover. The price-pages round 57 later turns many of those
   elements into VALUE, and they then appear as real cards.
