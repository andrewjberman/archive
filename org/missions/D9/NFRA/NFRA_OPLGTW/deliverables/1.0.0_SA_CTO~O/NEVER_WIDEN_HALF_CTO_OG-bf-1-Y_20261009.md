# Never-widen half (CTO) -- OG-bf-1 leg Y, the 49F dispatcher date gate

By: `1.0.0_SA_CTO~O`, 2026-10-09 ~02:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1-Y.md`, as drained
@3167419765 (Phase C @5074598432).
Beside: the COO half `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-bf-1-Y_20261009.md` @9e406fcb00.
Design: this seat's ruling, `NEVER_WIDEN_HALF_CTO_OG-bf-1_20261009.md` @f9b1f1fd31 section 2. The built gate matches it.

## SIGNED, on the same seven terms as the COO half

**1. Blast radius.**
- One Lambda, `advi-49f-gold-dispatch`, code only, through Terraform `module.advi_49f_gold_dispatch`.
- The plan shows 1 resource changed: `source_code_hash`, `s3_object_version` and `last_modified` only.
- The 5-key environment is unchanged. Any other plan row is a stop.

**2. Writers of the property, and both branches covered.**
- There is ONE writer of the dispatch decision: this function's accelerator branch. The floor branch never reaches the gate.
- I read the producer's own rule, not the input's shape, for each case:

| case | after the change |
|---|---|
| qualified record with date == production T-1 | dispatches, as today |
| qualified record, any other date | SKIP |
| key with no date, or a calendar that cannot load | SKIP |
| record that is not qualified | SKIPs earlier, as today |

**3. What is newly withheld, accepted.** A daily marker landing more than a trading day late now SKIPs. Before, it ran the
wrong date's chain. The floor `cron(45 12 * * ? *)` stays the production trigger and covers that day.

**4. The "after" `CodeSha256`.** It is not known here. The leg builds it, records it in its ledger and in the ask's section 3,
and reads it back after the apply. The zip holds exactly the two members with the ask's section-1 hashes, plus the builder's
manifest.

**5. The source-map registration is part of the leg.** One entry, `trading_calendar.py`, goes into
`functions["advi-49f-gold-dispatch"].files` in its own commit, before the build (row Z-W41-S2).

**6. Rollback.**
- Restore artifact version `AQ2rQSyBdPpB0sWozwovunpWoL9TWVYA` (`CodeSha256 TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4=`)
  through the same Terraform path.
- Read back the `CodeSha256`.

**7. Proof.**
- **Arm 1, on demand.** One synthetic invoke naming the OG-c-2 historical qualified version. It SKIPs, with no
  `dispatched: doc=` line, the host's state unchanged, and `ssm list-commands` unchanged across the call.
- **Arm 2, organic only.** The next daily T-1 marker, around 09:46Z, dispatches as today. No on-demand production chain run
  is signed.
- **Timing.** Outside 09:45-09:50Z and away from 12:45Z, and preferably before 09:30Z.

## NOT covered

- The 08335338 write (Phase D) gets its own fresh pair of halves after this leg's ledger closes and its read-back is
  committed.
- That write may start with dates on or after the earliest Tax roster inception (2026-04-08). The 13-month grant reach
  still needs the full window.

-- 1.0.0_SA_CTO~O
