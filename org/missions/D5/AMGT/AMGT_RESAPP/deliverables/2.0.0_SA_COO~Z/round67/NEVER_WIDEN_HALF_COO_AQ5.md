# AMGT_RESAPP round 67 -- `AMGT-aq-5` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-04 ~20:3xZ

**The act (TWO legs, in this order):** for `opal-amgt-scoped-api`:
1. **Grant leg.** Add ONE IAM statement (below) to `scoped_amgt_api_grants`, then a `safe-apply` targeted at that role policy.
2. **Code leg.** Build and upload ONE artifact at build commit `d8bafe6896`, or a descendant whose CONTENT-DIFF equals the list below.
   Then ONE code-only `safe-apply`. `memory_size` stays 1769.

- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-aq-5.the-code-redeploy.md` (AMENDMENT 1).
- It carries the four drains of round 67:
  - aq-1 `fa22ce3149`: FWD-39 list repair;
  - aq-3 `e5ea575b16`: FWD-38 (d) /ledger provenance;
  - aq-2 `aac5a586d1`: FWD-36 tone from chatter_window;
  - aq-4 `d8bafe6896`: Z-S86, a covered name with no model block.
- **Why a grant leg (row `AMGT_RESAPP-Z-S345`).** aq-4 reads the Security Scanner S&P 500 universe file at request time.
  - The role cannot read that file today: `simulate-principal-policy` returns implicitDeny, against a positive control of allowed on `opal-data-harvest`.
  - The bucket policy grants only CloudFront.
  - So the code alone would answer 502 for DE_US_Equity, and for every unknown `_US_Equity` key that answers 404 today.
  - The grant goes first so that no request ever runs the new code without it.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `FcVBPafwzuPI0RMFjOJJfYN/KeZe3YYns9uqTSOlalU=` (ap-4, LastModified 2026-10-03T23:49:22Z) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `Pj6GLEdKjRnDFwBjZzOSR2gYAsQPHilG` (ap-4's upload, 2026-10-03T23:41:45Z) |
| role policy `opal-amgt-scoped-api-grants` | as declared at `d8bafe6896` (5 statements; S3 read only on the `opal-data-harvest` pool prefixes) |

## THE GRANT (exact; nothing wider)

```hcl
{
  Sid      = "ReadTheScannerSp500UniverseForCoveredNoBlock"
  Effect   = "Allow"
  Action   = ["s3:GetObject"]
  Resource = ["arn:aws:s3:::opal-data-portal-v2/json/security_scanner/latest/universes/sp500/universe_data.json"]
}
```

The grant is ONE object ARN. It has no prefix wildcard, no ListBucket and no other universe id. The literal ARN follows this
file's own `etf-classifications` precedent: the bucket is declared in another root. The cross-firm gate does not list
`opal-data-portal-v2` (`.tools/ds-precommit-check.py:69-72`).

## THE FILE LIST (`--build-only` at `d8bafe6896`, from a detached checkout)

Build results:
- cold-start FATAL [] and request-time break [];
- 356 entries;
- 253,753,630 B against the 262,144,000 B ceiling (96.8%, 8,390,370 B spare).

Against `FcVBPafw...`: `CONTENT-DIFF SUMMARY: files 356, IDENTICAL 350, CHANGED 5, ADDED 1, REMOVED 0`.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | aq-1, aq-3, aq-4 | word cloud excludes the own-ticker root, short and long name words and the measured boilerplate; an inverted window serves its reason (c23). /ledger classes are sourced or reasoned (c25). DE thesis and peers answer 200 with a reason (c26) |
| `lib/research/api/monthly_chatter.py` | CHANGED | aq-2 | chatter tone and voters come from the latest chatter_window part; 0 voters reads "no clear tone" (c24) |
| `lib/research/api/rolling_windows.py` | CHANGED | aq-2 | the old tone reason line goes (c24) |
| `lib/research/coverage/covered_no_block.py` | ADDED | aq-4 | the declared covered-without-block universe (c26) |
| `infra/logic/registry/reporting_policies.json` | CHANGED | `c6c3c0b674` (IRPT_YCDGEN, additive policy row) | NONE through this function |
| `infra/logic/registry/systems.json` | CHANGED | `4201d79857` (NFRA_SPRINTWIN, additive systems row) | NONE through this function |

**Why the two registry files have no served effect here:**
- Both diffs are additive rows (+20 and +9 lines).
- The function loads the registry through `lib.opal_naming`, and `import lib.opal_naming` succeeds at the pin.
- At the pin, locally:
  - every round-64 to round-66 regression read is YES (r64 c9-c14, r65 c17, r66 c18/c19/c22);
  - c23, c25 and c26 are YES;
  - the api suite reads 535 passed on the merged tree.

Any other changed file at build time is a STOP.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| grant `safe-apply` (targeted) | `opal-amgt-scoped-api-grants`: +1 statement, exactly as above | `safe-apply` with the statement removed (the policy at `d8bafe6896`) |
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `Pj6GLEdKjRnDFwBjZzOSR2gYAsQPHilG` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `FcVBPafw...` |

If the code leg rolls back, the grant may stay or go. It is read-only on one public-data object, and the rollback
restores the 404 behaviour either way.

## EXPECTED OUTCOME -- both branches

| check | base (deployed FcVBPafw) | after (local at `d8bafe6896`, ~20:2xZ) |
|---|---|---|
| grant | implicitDeny on the scanner key | allowed (`simulate-principal-policy`, read before the code leg) |
| r67 c23 | NO: 15 own-ticker/short-name offenders, 69 extended-list payloads, inverted window | YES: 190 payloads, 128 non-empty, 0 offenders |
| r67 c24 | NO: 74/95 mismatches per window | **NO by ONE clause only:** mismatches 0, old-reason 0, no-table-row 21 per window (the producer gap, row `AMGT_RESAPP-Z-W220-S1`) |
| r67 c25 | NO: 4 of 6 classes unsourced on BA, AMD, VLO | YES: 9 of 9 clauses |
| r67 c26 | NO: DE 404 on thesis and peers | YES: DE 200 with the reason on both; ZZZZ_US_Equity 404 |
| r64 c9-c14; r65 c17; r66 c18/c19/c22 | YES | YES |
| r64 c15 (cold, day route) | YES at ap-4 (3 of 3 cold) | read on deployed |

**Failure branch:** any of the following is a ROLLBACK of the code leg, per the table:
- c23, c25 or c26 is not YES;
- c24 shows a mismatch or an old reason, or its no-table-row count differs from a local read run beside it;
- any regression read moves;
- c15 reads over 5 s;
- a non-200 on a covered key's overlay, thesis, peers, timeline or collected/chatter;
- a 502 on any key, which means the grant did not take.

## WHAT THIS HALF DOES NOT COVER

Any of the following is a STOP:
- a memory change;
- a store write or an S3 delete;
- a vendor call;
- any IAM change other than the one statement above;
- a route or gateway change;
- a data-engineering operation;
- a grant leg that plans anything beyond the one role policy.
