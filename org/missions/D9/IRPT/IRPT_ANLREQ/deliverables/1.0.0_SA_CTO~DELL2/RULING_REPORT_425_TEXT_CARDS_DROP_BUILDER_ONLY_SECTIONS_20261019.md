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
