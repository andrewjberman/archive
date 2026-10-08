# L8 drain end -- IRPT_DASHBD round 26 (workstream B, and workstream BD's first cell)

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~23:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @ebfb8e6736

Three task orders, all terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer on each branch and
after each drain). 0 JUDGMENT criteria. Nothing was applied and no S3 write was made by any worker. On: `1.0.0_SA_CTO~DELL2`'s round-25
analysis @3543da2f4d (E1, E2) and Andrew's per-use word for FWD-8's split BD pull (MSTR msg 1103, record @5ef6d33141).

## The orders

| order | ws | drain | criteria (issuer re-run) | result |
|---|---|---|---|---|
| DB-b-41 (E1 release prep; WORLD by path floor) | B | @f3500197db (efeb21df71, ef8637f37c) | DB26-1-AC1..AC3 PASS | Contracts name 19 of 19 built columns each, with `primary_key`; both lot contracts carry `basis_source` (3 members); 0 custodian table names typed in the producer, all 4 in `sources.json`; the handler emits returns, class and the three tables; role writes five prefixes. 20 accounts x 1 day: returns and class byte-identical before/after; 0 repeated keys (and 0 over a 24-day window). Expected plan `0 to add, 3 to change, 0 to destroy` (read from the diff; no terraform on this box). Packet covers the whole next apply of the root, the round-22 class release included |
| DB-b-42 (E2 criterion 2) | B | @a782e08f7a (bba117fdd8) | DB26-2-AC1 PASS | 190 of 190 served trading-day partitions read (2026-01-02..2026-10-05), 0 frames with a repeated index label: the frame carries a RangeIndex by construction. Verdict CANNOT; no code change |
| DB-b-44 (FWD-8 split pull plan) | BD | @35a0fc34d4 (80f080e624, f32897c7b6) | DB26-3-AC1, AC2 PASS | 2,299 requests over the record's 2,299 accounts, 4,598 ranges split at 2025-01-09, 0 unmapped, builder landing keys under `pull=split20261007`, 0 vendor calls; 11 offline tests; the runner refuses any wider plan |

Drain hygiene: commit-gate clean on the code files; the two test folders 154 passed; the split-pull tests 11 passed.

## Read before grading

- **The release is prepared and NOT applied, and the COO half is WITHHELD** (`NEVER_WIDEN_ACTIVITY_LOT_RELEASE_COO_HALF.md`, @ebfb8e6736),
  on two conditions, each a row:
  - **S31 on W23-S2 (ARMED -> gated):** the lots stage added about 35 s and about 764 MB on 20 accounts; the population is 7,597 against
    900 s / 2048 MB. The half is signed when one day at full population is measured inside both limits, or the stage is split so it is.
    This is an enrichment for round 27.
  - **S32 on W23-S6 (ARMED -> gated):** pin 0 re-pins `account_return_daily.py` to the round-25 `classify_and_sum` change, which DB-b-43
    has not tested on the served pandas 2.2.3. The half is signed when DB-b-43 passes on 2.2.3 with the returns table byte-identical.
  The CTO's E1 criterion (3) asked for the COO half signed; it is withheld for these two reasons, not refused.
- **W23-S1:** the role gains READ on the custodian's lot silver prefixes (derived from `lot_source`), beyond the order's literal text;
  named in the packet for the CTO half.
- **DB-b-43 (E2 criterion 1, pandas 2.2.3)** is not done: the laptop carries pandas 2.3.3 (MSTR msg 1136). The approved Python 3.12
  installer is on dell2 awaiting Andrew; the layer-pinned wheels are fetched separately by the laptop's 2.0.0_SA_COO~C.
- **FWD-8's live pull did not run.** On dell2 it aborted before any vendor call (0 calls, 0 mints, 0 landed): AccessDenied on
  `secretsmanager:GetSecretValue` for `blackdiamond/49f/session` for this box's user. No fence was widened. The same command is relayed to
  the laptop (MSTR msg 1142, pin on origin @eaae449ef2); its run record returns as a file. Abort record @e39ea3dcca.
- **Issuer defects this round, both recovered:** a drain's chained teardown deleted an unmerged branch after the merge lock refused (the
  branch was recreated from its commit and merged; nothing lost); the first live-run launch omitted the repo-root argument (refused at
  argument parsing; nothing called).

## Rows in the round

| row | class | standing |
|---|---|---|
| W23-S1 | OBSERVATION, INERT | lot silver read grant beyond the literal text -- for the CTO half |
| W23-S2 | OBSERVATION | gated by issuer row S31 (UNDER_INVESTIGATION) |
| W23-S3 | OBSERVATION, INERT | the producer gained `emit_day()` (it had no write path) |
| W23-S4 | OBSERVATION, INERT | sample list; realized table empty on the run day (a 24-day window covered it) |
| W23-S5 | OBSERVATION, INERT | no terraform on the box; plan counts from the diff |
| W23-S6 | OBSERVATION | gated by issuer row S32 (UNDER_INVESTIGATION) |

## What the round leaves

- The lots stage measured at population scale (S31), and DB-b-43 on pandas 2.2.3 (S32): then the COO half is signed.
- The split BD pull's run on the laptop, and the tie-out of its figures (FWD-8 branches A/B), cut when the pull lands.
- The class release (FWD-3) now rides this packet; its apply waits on the terraform kit and both halves.
