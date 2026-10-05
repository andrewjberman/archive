# AMGT_RESAPP round 70 -- `AMGT-at-6` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-05 ~08:0xZ

**The act (TWO legs, in this order):** for `opal-amgt-scoped-api`:
1. **Grant leg.**
   - Add the prefix `issuer-site/harvest/silver/filing_source/` to `local.scoped_amgt_pool_prefixes`.
   - Then ONE `safe-apply` targeted at `aws_iam_role_policy.scoped_amgt_api_grants`.
   - Then `round70/checks/r70_grant_at6.sh` reads YES.
2. **Code leg.** ONE artifact at build commit `e041c86791`, or a descendant whose CONTENT-DIFF against the DEPLOYED build equals the
   list below. Then ONE code-only `safe-apply`. `memory_size` stays 1769.

- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-at-6.the-code-redeploy.md`, with AMENDMENT 1 (`<proof_genre>DEPLOY</proof_genre>`).
- It carries at-4 @a882634ed9, at-1 @238ef99a85, at-3 @7f04bf1aca and at-2 @e041c86791.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `OcKZF34X9liuVKg9ZnpaqBcbSxwcDl6JlW+PlxWyF4k=` (round 69 as-2) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `WlTp7CvQs4zkxFnYmwhDPB8cITLFF.Ve` (as-2's upload, 2026-10-05T04:39:45Z) |
| role policy `opal-amgt-scoped-api-grants` | the pool prefixes WITHOUT `issuer-site/harvest/silver/filing_source/` |
| simulate GetObject / ListBucket(prefix) on that prefix | implicitDeny / implicitDeny; the controls on `sec/harvest/silver/filing_source/` read allowed |
| open NEVER-2 entries on this function | none |

## THE FILE LIST (`--build-only` at `e041c86791`, from a detached checkout)

The build read cold-start FATAL [] and request-time break []. It is 253,913,029 B against the 262,144,000 B ceiling (96.9%,
8,230,971 B spare). pyarrow is in the package. Against the DEPLOYED `OcKZF34X...`:
`CONTENT-DIFF SUMMARY: files 363, IDENTICAL 354, CHANGED 2, ADDED 7, REMOVED 0`.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | at-1..at-4 | the header's seven figures or a reason (c30); `management.chain_tried` + reason (c31); member `price_currency` or a reason (c32); day-route `origin`, own first (c33) |
| `lib/research/harvest/store.py` | CHANGED | HARVST HVST-at-4 @46f165ea6e | NONE through this function: `silver_append` is a writer this function never calls (CTO msg 29511) |
| `lib/research/harvest/bloomberg.py`, `lib/research/harvest/filings.py` | ADDED | at-2's import closure | the chain's stored-source readers |
| `lib/research/management/__init__.py`, `bloomberg_fallback.py`, `exec_roster_chain.py`, `roster.py` | ADDED | at-2 | the F3 chain at request time |
| `lib/research/peers/price_currency.py` | ADDED | at-3 | the member currency join |

Any other changed file at build time is a STOP.

**New S3 read paths (round-67 ruling 4), simulated at the cut:**
- allowed: `sec/harvest/silver/filing_source/`, `amgt/harvest/state/filing_attempt/`, `bloomberg/harvest/bronze/exec_officers/` and
  `derived/model_block/`;
- denied: `issuer-site/harvest/silver/filing_source/`, which the grant leg adds.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| grant `safe-apply` (targeted) | `opal-amgt-scoped-api-grants`: GetObject on `opal-data-harvest/issuer-site/harvest/silver/filing_source/*` and that prefix in the ListBucket condition; read only, on a bucket the role already reads | a targeted `safe-apply` with the entry removed |
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `WlTp7CvQs4zkxFnYmwhDPB8cITLFF.Ve` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `OcKZF34X...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed `OcKZF34X`, ~06:3xZ) | after (local at `e041c86791`, ~07:5xZ) |
|---|---|---|
| r70 grant (AC4) | NO (implicitDeny x2) | YES (read after the grant leg) |
| r70 c30 | NO: 43 of 95 headers | YES: 95 of 95 |
| r70 c31 | NO: 84 of 95 | YES: 11 served, 84 `chain_tried` + reason (0 new officers; row Z-W227-S1 lists the Bloomberg pull for Andrew) |
| r70 c32 | NO: 676 of 676 members | YES: 4 with a currency, 672 with a reason (row Z-W228-S1) |
| r70 c33 | NO: 8 of 8 rows | YES: every row `external` (no own publisher declared) |
| r69 c29, r68 c27/c28, r67 c23-c26, r64 c14 | YES | YES |
| r64 c15 (amended), /peers latency | YES; /peers ~0.2 s | read on deployed; /peers now reads one model block per member |

**Failure branch:** any of the following is a ROLLBACK of the code leg, per the table:
- c30-c33 not YES;
- any other check moves;
- c15 over 5 s;
- a non-200 on a covered key's overlay, thesis, peers, timeline, ledger or collected/chatter;
- ZZZZ_US_Equity not 404.

**A STOP, not a rollback:** a /peers latency over 5 s. Report it with the segment times.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a memory change;
- any IAM change other than the one prefix;
- a store write or an S3 delete;
- a vendor call (row Z-W227-S1's Bloomberg pull is Andrew's act, not this one);
- a route or gateway change;
- a data-engineering operation.
