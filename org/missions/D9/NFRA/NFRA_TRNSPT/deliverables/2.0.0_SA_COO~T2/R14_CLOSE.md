# NFRA_TRNSPT round 14 -- close record: keep-driving, the FREE options (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `f506a07c1a` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R14.md`; Andrew-direct keep-driving ON, MSTR msg 2144). Calls queued on
dell2's open-calls list by the `/next-calls --drive` tick: the Kimi standing word for live operation (an Andrew act) and row D2-S7 (household).

| cell | merge | criteria |
|---|---|---|
| TR-l-14 the commentary Lambda (DESIRED, NOT APPLIED) | `d153aeaba0` | `R14-L14-OK 5 passed`; `R14-L14N-OK rows=4 all equal name()` |
| TR-h-14 H2 holdings categories | `1587d53a4c` | `R14-H14-OK 8 passed` |
| TR-x-14 the Apple exception list (two seats) | `113047fc82` | `R14-X14-OK 3 passed`; allowlist suites 33 passed |

Drain on the merged tree: transcripts tests (commentary, securities, wipe, research, slicer, outlook, mail, completeness) 189 passed, 0 failed;
`commit-gate.sh` clean on the 3 changed modules; `round-close-check --round 14`: MAY-CLOSE.

## What exists now

- **`outlook-global-commentary-draft-lambda`** as code (`commentary/lambda_handler.py`: entry -> drafter -> ticket client, stopping at
  `no_vendor_word` with no model call and no ticket while `KIMI_STANDING_WORD_REF` is empty) and as DESIRED Terraform (`infra/aws/terraform/
  transcripts/commentary.tf`: log group, DLQ, role, policy, attachment, KMS grant, function; no event source mapping; NOT APPLIED). Names:
  `outlook-global-commentary-draft-{lambda,role,policy,queue}` (builder). Not applied until CALL 1 (Andrew's standing Kimi word) and the `irpt`
  key decrypt leg (a key another box uses; the laptop, before-rule).
- **H2 holdings categories:** derived with largest-remainder rounding when a normalized input carries a category -- but it does not (row
  **D2-W2-S3**, BLOCKING: v1 position rows are `security_id` + `analysis_dollars`). The real source of a category is the canonical per-security
  table (DynamoDB `etf-classifications`, `asset_class` by ticker), a next-round cell.
- **The exception list v1:** Apple (AAPL; PFDE holding evidence as of 2026-10-07); "Apple" survives as an issuer and is wiped in a name context
  ("Mr. Apple", "Apple Smith"). CVO review of the entry: requested. The stored 29 objects do not carry it until a re-fold and re-write (served,
  laptop write).

## Rows

D2-W2-S3 (BLOCKING, above); D2-W3-S3 (the two stale assertions, fixed under amendment 1, `2a2915b702`).
