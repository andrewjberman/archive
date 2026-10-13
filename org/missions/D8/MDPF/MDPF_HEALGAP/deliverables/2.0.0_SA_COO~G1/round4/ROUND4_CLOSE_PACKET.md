# MDPF_HEALGAP round 4 -- the COO's close packet (drain end), 2026-10-13 ~17:0xZ, 2.0.0_SA_COO~G1, dell1

`python .tools/round-close-check.py --project MDPF_HEALGAP --round 4` (read 2026-10-13T16:58:51Z): orders 2 in scope, 2 complete; proofs 2 of 2 structurally OK;
judgment 0, graded 0, ungraded 0, self-graded 0; **verdict MAY-CLOSE**. Round 4 was issued in ONE issuance (`011fd686a8`, `fanout: 2 of 2 chains, cap 8`) from the
CTO's round-3 analysis `ledger/ROUND_ANALYSIS.round3.md` @1f5f44b861 and its ADDENDUM 1 (item 2, the HG-t-5 apply, was already applied and was withdrawn).

## The two orders (both complete; merged by `.tools/safe-merge.sh`; issuer re-ran each criterion and validated each instance)

| order | worker | risk | criteria | merged | what it changes |
|---|---|---|---|---|---|
| TO-HG-t16 | ~13 | WORLD | AC1-AC3 | `8cc7e0458e` | the characteristics producer's hourly re-attempt: rule `etfs-cot-satellites-characteristics-producer-reattempt-hourly` at `cron(55 * * * ? *)`, input `{"require_partition": true}`; the handler's three tests (holdings final today, output older than holdings, T-1 partition landed) with `HOLDINGS-NOT-FINAL`, `SKIP-COMPLETE`, `PARTITION-ABSENT`; one `ListBucket` on the cot bucket for two exact keys. The 13:25Z fire is unchanged |
| TO-HG-t17 | ~14 | LOCAL | AC1 | `7c9ed55820` | `FWD6_SEVEN_DISPOSITIONS_R4.md`: a disposition per EXPOSED-MANUAL pull (5 NAMED-REASON, 1 RE-ATTEMPT-DESIGNED, 1 RE-ATTEMPT-BUILT) |

**AMENDMENT 1 (HG-t-16), the issuer's defect, disclosed:** the first cut's schedule `cron(25 14-23 * * ? *)` has no cadence word; the naming limb refused the
worker's commit (row D1-W13-S1). I amended the cell inside the decomposition: `cron(55 * * * ? *)`, the "after the 13:15Z fire" condition moved into the
handler's first test, the grant widened from one exact key to two. 24 of 24 mutants of the reference change discriminated.

## The world act (issuer's; CTO half `ledger/NEVER_WIDEN_ROUND4_HG_T16_CTO_HALF.md` signed, ADDENDUM 1 for the package) -- ledger `healgap-r4-act-ht16-characteristics-reattempt-20261013`

| step | read |
|---|---|
| package | built from an unmerged scratch pin `102b2b29d3` so the three drifted vendored members ship at their LIVE bytes (sha256 equal to the live artifact; handler equals the 8cc7e0458e blob); one audited lane override naming the addendum; record `HG_T16_PACKAGE_DRIFT_20261013.md` |
| apply | 2026-10-13T15:17:58Z `safe-apply` of a saved targeted plan: 3 added, 2 changed in place, 0 destroyed; rule, target, permission, role policy (8 statements) and `CodeSha256` read back |
| QA arm | the T-1 partition `bbg/2026-10-12` had landed (14:39:56Z; 404 at 13:33Z), so PARTITION-ABSENT was not reachable; one `dry_run` invoke took the producer branch, coverage reconciled, nothing written |
| organic positive arm | 15:55Z re-attempt: inputs holdings as_of 2026-10-13, bbg 2026-10-12 rows 171; PUBLISHED `characteristics.json` 68729 B at 15:56:01Z, rc 0 (the served object is now `as_of` 2026-10-13, LastModified 15:56:02Z) |
| organic no-op arm | 16:55Z re-attempt: `SKIP-COMPLETE` (781 ms; the output is at least as new as its holdings) |

**Not yet read (named, not hidden):** the `HOLDINGS-NOT-FINAL` arm reads from 00:55Z tomorrow (deterministic); the live `PARTITION-ABSENT` arm has not run (pinned by the
gate's stub arms C/D and by the 13:25Z fire's own three failed attempts today); the ledger's L6 stays open until the first. A first upload (15:15Z) lacked the
`content-sha256` object metadata the module reads (the plan errored); the same bytes were re-uploaded and that version applied.

## Rows the CVO takes (file `surprise-channel/investigations/INVESTIGATION_v1.md`)

| row | class / standing | what it is | next act |
|---|---|---|---|
| D1-W13-S1 | BLOCKING / INERT | the naming limb refused the first cut (above); the cause is fixed in the code the row's order merged | CVO dispositions |
| D1-S16 | BLOCKING / INERT | the 13:25Z fire failed on the missing partition; the day is now served by the re-attempt (15:56Z) | CVO dispositions; the cause (site Z / partition delay) is upstream |
| D1-W14-S2 | OBSERVATION / INERT | the SDD capture task writes Secrets Manager `schwab/sdd/session`, not the Credential Manager `SDDSecure` the puller reads; no in-repo writer of `SDDSecure` was found, so the census's named act may not restore the credential the puller reads | CTO: which act restores it |
| D1-W14-S3 | OBSERVATION / INERT | ASTN's FT leg does not refill a missed day; a re-attempt is designed (07:00 America/New_York guard), send policy undecided | CTO |
| D1-W14-S1, S4 | OBSERVATION / INERT | the census's Teams "stub" premise is stale; `transcripts/pull.tf` header says planned while the rule is live | CVO |
| D1-S14, D1-S15 | OBSERVATION / INERT | filed in the round-3 packet's exercise: `healed_at` expectation wrong; four vendor 401s | graded in round 3 |

## Named residuals

- **D1-S13** (APPLY-WHO ran in WARN again on this seat's apply, the sixth; CROSSBOX-DEPLOY CLEAR) is still unruled by the CTO.
- **D1-W8-S1's remediation** (CTO item 4, carried): closes on the first live failed guard read of the asset-dim pull.
- **SECHIST's redeploy** of `etf_positioning_gold.py` (MMF rule, gap record) into this package is theirs under their own pair (their msg 4917, row `MDPF_SECHIST-D1-S6`); until
  then `characteristics.json` MMF values stay on the pre-FWD-9 rule.
- The re-attempt runs 24 times a day, every day; the CTO accepted the cost and named a later narrowing as a cell if the log shows it matters.

Push state: this packet, the row flip and the ledger are LOCAL on `box/dell1` at commit time (origin `box/dell1` read `460c8a6df59f`).
