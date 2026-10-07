# L8 drain end -- IRPT_DASHBD round 22, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~13:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @c4c454a03b

The one order of the round is terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer before
the drain). 0 JUDGMENT criteria. Risk WORLD by the gate's floor (the paths name infrastructure), but this cell APPLIED NOTHING: no
terraform, no Lambda update, no S3 write. The worktree and branches were removed. On: `1.0.0_SA_CTO~DELL2`'s round-21 analysis
@214a0ef324 (W18-S2 ruled: release as is with the unclassified share shown) and its correction msg 463 (classes from the etf-classifications
TABLE, not the module).

## The order

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-34 (prepare the account_class_daily release) | @d48052d79b (worker ~19: 7517444629, 81c3ac9d25; amendment 1 @e765698322; bae1e8bd8b, 1a9f68b833) | DB22-1-AC1..AC3 PASS | returns DELTA=0: sha256 11453fc7... on both sides, the before side on the base handler AND base sources.json (2026-10-05, 20 accounts, 19 rows); 18 measured account-days sum within 1.6e-16; unclassified share 0.072% of the sample's class market value; role writes 2 prefixes, GetItem on etf-classifications only, no Delete; packet carries 7 of 7 sections |

What landed in source: the class producer reads the `etf-classifications` table (one GetItem per ticker through the shared client); the
reporting-gold handler also emits `account_class_daily` and catches the class table up from its own newest landed day (at most 10 days a
fire, never past the newest returns day); `sources.json` carries the trade-leg tokens; the role gains the class prefix and GetItem; the
contract names the table as its source. Drain hygiene: commit-gate clean; 96 tests passed across both test folders; the served producer
`account_return_daily.py` and `infra/aws/lambda/ci/lambda-source-map.json` show a 0-line diff.

## Read before grading

- **The table fixes the gap the module would have frozen.** On the round-21 sample (61 accounts, 2026-10-05) the unclassified share is
  0.153% reading the table against 1.804% reading the module; 9 of 78 holdings are absent from the table against 45 under the module.
  The ~16% of W18-S2 was every account on 2026-10-01, so this sample neither confirms nor refutes it (row W19-S5). MDPF_SECCLASS SC-e-49 is
  still landing single stocks and money-market funds; the table is re-run on 2.0.0_SA_COO~M1's landing notice.
- **The apply is NOT done and has three preconditions, all in the packet**
  (`deliverables/0.9.0_WK_IRPT_DASHBD~19/NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`): (1) the source map's three `staged_from`
  entries pinned to d48052d79b with their sha256, set by the deploying lane (row W19-S2, ruled a release act); (2) the dell2 terraform kit;
  (3) both never-widen halves signed (the CTO half on ask, per the analysis).
- **W19-S1 (open, INERT):** the shared client returns None on a DynamoDB error, so the producer reads through the client's table handle
  and refuses the day on an error instead of calling it unclassified.

## Rows in the round

| row | class | standing |
|---|---|---|
| W19-S1 | OBSERVATION, INERT | open: the client's None-on-error, worked around in the producer |
| W19-S2 | BLOCKING, INERT | resolved by S29 (@c4c454a03b): an apply precondition in the packet |
| W19-S3 | OBSERVATION, INERT | resolved by S29: the class-prefix read grant is now used by the catch-up |
| W19-S4 | OBSERVATION, ARMED | DISARMED by S29: the catch-up retries a skipped day; nothing was ever deployed |
| W19-S5 | OBSERVATION, INERT | open: the share figures and the scope of the ~16% |
| W19-S6 | OBSERVATION, INERT | DISMISSED (the worker's record of the catch-up) |
| W18-S1 | OBSERVATION, INERT | resolved by S29: the trade-leg tokens are in `sources.json` |
| S29 | OBSERVATION, INERT | the issuer's `adjudicates` row |

OPEN 2, ARMED 0 (comp-surprise after S29).

## What the round leaves

- The apply of the release, the first fire and the after-read (the CTO's criteria 2 and 3), under the three preconditions above.
- The page's unclassified-share line beside the class breakdown (FWD-3's view), a workstream F item. Its face carries the bun rule
  106215/106221 verbatim.
- FWD-8 stays HELD on Andrew's per-use word for the split BD pull.
- The live thread trace (FWD-1 hop 5) was not re-run; its last exercised run stays 2026-10-02 (STATUS~D).
