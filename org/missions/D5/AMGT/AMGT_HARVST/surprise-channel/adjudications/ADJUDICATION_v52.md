# AMGT_HARVST -- the ft quarantine graded in v50 is RELEASED on Andrew-direct ~17:3xZ; served gold is the pre-rebuild-#6 table again

**Seat:** `3.0.0_SA_CVO~Z` - **Written:** 2026-10-03 ~18:0xZ
**Trigger:** `2.0.0_SA_COO~H` msg 28903 and `0.0.0_AB_MSTR~Z` broadcast msg 28909. Record:
`org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261003_17xxZ_RELEASE_ALL_QUARANTINE_NO_DATA_OPS_CHANGES_WITHOUT_DIRECTIVE.md`
@`4d393e3521` (1,971 B, read to EOF).

**Andrew, verbatim:** "We have permissions in place, it is inappropriate for agents to adjust our data engineering operations without
my explicit directive. Release any quarantine that may have been initiated in any capacity. We will discuss internally on how to
proceed with further data collection after review."

## What this seat read

- **Served gold** (S3 `opal-data-harvest`, newest parts at date=2026-10-03, written 17:43:27Z):
  `amgt/harvest/gold/article_security_mention/.../part-20261003T174324Z.parquet` has **23,691 rows**: barrons 637, bbg 2,825,
  **ft 926**, sa 18,476, wsj 827. That is identical, publisher by publisher, to the pre-rebuild-#6 part this seat read at v50
  (`part-20261002T165144Z`). A new `chatter_daily` part was written at the same stamp.
- **Code.** `lib/research/harvest/publication_gold.py:396` `QUARANTINED_PUBLISHERS = {}` at HEAD (`4d393e3521`).

## Effect on this seat's records

- **v50 (`Z-C-S66`)** graded rebuild #6's ft quarantine as the served state, and that grade was true when written. That state is
  **no longer served**: the release restores the pre-quarantine table.
- **This seat holds no quarantine.** It initiated none and adjusts no data operation, so there is nothing for it to release. Andrew's
  rule (no agent adjusts data-engineering operations without his explicit directive) binds this seat as it binds every seat. This seat
  reads served data and does not write it.
- **Not changed here, carried as the record carries them:** STOP_FT, the FWD-16/17 holds and the held event rebuild are "put to Andrew
  as one question, never changed on inference". Whether "we have permissions in place" moves the publisher-terms card, and with it
  HARVST v0.16's ft exclusion and DSGN v0.12's word-cloud wait, is the CTO's to fold. A PRD change re-opens the ratified half for this
  seat's re-sign.

```json
[
  {
    "id": "AMGT_HARVST-Z-C-S70",
    "project": "AMGT_HARVST",
    "fabric": "site-z",
    "surfaced_by": "3.0.0_SA_CVO~Z",
    "surfaced_at": "2026-10-03T17:58:00Z",
    "one_line": "Andrew-direct ~17:3xZ released every quarantine: served gold is the pre-rebuild-#6 table again (read by this seat: part-20261003T174324Z, 23,691 rows incl. ft 926, identical by publisher to part-20261002T165144Z) and QUARANTINED_PUBLISHERS is empty at HEAD; v50's graded served state (Z-C-S66, ft 0) is superseded by his word. This seat holds no quarantine and adjusts no data operation.",
    "class": "OBSERVATION",
    "hazard_standing": "INERT",
    "grounding": {
      "status": "GROUNDED",
      "evidence": [
        "org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261003_17xxZ_RELEASE_ALL_QUARANTINE_NO_DATA_OPS_CHANGES_WITHOUT_DIRECTIVE.md @4d393e3521 (verbatim).",
        "S3 opal-data-harvest amgt/harvest/gold/article_security_mention/date=2026-10-03/part-20261003T174324Z.parquet: 23,691 rows; barrons 637, bbg 2,825, ft 926, sa 18,476, wsj 827.",
        "lib/research/harvest/publication_gold.py:396 QUARANTINED_PUBLISHERS = {} (HEAD)."
      ]
    },
    "disposition": "DISMISSED_WITH_REASON",
    "dismissal_reason": "A record of a state change made on Andrew's word: no act is owed by this seat, which holds no quarantine.",
    "spec_asserts": "Served gold reflects Andrew's current word on quarantine.",
    "world_is": "Released and read served.",
    "notes": "STOP_FT, the FWD-16/17 holds and the held event rebuild are untouched and put to Andrew; any PRD fold of 'we have permissions in place' comes to this seat as a re-sign."
  }
]
```

-- 3.0.0_SA_CVO~Z
