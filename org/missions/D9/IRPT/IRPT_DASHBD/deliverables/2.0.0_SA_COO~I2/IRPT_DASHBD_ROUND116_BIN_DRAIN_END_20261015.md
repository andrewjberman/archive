# IRPT_DASHBD round 116 (the CTO's B-IN analysis, msg 7978), workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~03:5xZ)

**One order, drained; nothing served moved, nothing written to AWS, no vendor call, no secret read, nothing deployed; paths, line numbers, short code quotes and words only.** Issued @5f9b191126 (merged @38707eebf2). Drained: `DB-i-4` (~304, @26fd29c5d2). On the landed tree `DBI116-1-AC1` PASSES and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 116` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## What the cell found (the ruling's question: does Orion expose an account-level return)

**YES, in code the estate already holds, and it is not the pull that feeds the silver.**

- **Endpoint:** `POST https://api.cloud.orionadvisor.com/api/v1/Reporting/Scope`, built by the investor-reporting performance adapter (`infra/aws/lambda/investor-reporting/performance/`: `orion_adapter.py`, `orion_selected.py`, `orion_live.py`, `tenants.py`). Of the 13 distinct Orion paths in the 85 files of the two pools, only the performance directory carries it.
- **Grain (measured in the daily fixture's key structure):** a household-entity scope with an `Account` grouping. The response returns one period return per account plus a daily breakdown series (one point per end date, compact, not cumulative). **The code sends it only for a household that holds exactly one account in the mapping snapshot, and refuses a response unless it holds exactly one Account group with that id.** The fixture shows the vendor can return two Account groups and one Household group in one response; whether the code's one-account limit is a vendor limit or a choice is not shown in the repo.
- **Fields:** `performance`, `factor`, `startDate`, `endDate`, `feeAmount`.
- **Gross or net: UNDETERMINED.** The request sends `calcGrossOfFees` as false, a name that reads net of fees, but the adapter records `fee_basis` UNKNOWN: the response has a per-day `feeAmount` and no stated basis for the return. The gross-or-net fact decides whether Opal's fee treatment can be tied out, and the repo cannot settle it.
- **Credential: REACHES by code only, not proven.** The transport loads the Secrets Manager secret `orion/jwt/current` and sends it as `Authorization: Session`; the Inflection pull reads the same estate token from an S3 copy. The code does not show the two stores hold one value at call time, and no call was made, so Orion's acceptance of the token on Scope is unproven.
- **Who calls it today:** only the declared route `GET /api/scoped/investor-reporting/performance/{accountSetId}` (`docs/contracts/investor-reporting/v1/routes.json`, status DECLARED). No schedule in the files read invokes it, and deployment was not measured (no AWS call).
- **The silver pull does not call Scope.** `inf-performance-daily` (EventBridge cron 13:40 UTC per its Lambda) calls the Envision `ExcelReports` endpoints: a per-account period return over ONE requested date range, not a daily series. Its header says it has been stale since 2026-04-28; whether it is stale live was not measured (row `W304-S2`). Since it already returns a per-account period return from Orion, it is a candidate source the CTO may weigh against adding the Scope feed.

## What this seat read for itself

I re-ran the criterion in the worker's tree (PASS), re-validated the proof instance with the worktree's own checker (VALID), merged through `safe-merge.sh` (row gate clean) and scanned the record and the proof for identifier-length digit runs: none. The checker recomputes the endpoint inventory (13 paths, 85 files) and opens every cited evidence line (24 of 24) to find the quote on it. I did not run the account-mapping code or open a fixture value. **Not a grade.**

## Issuer errors this round

None found in this round. (Rounds 114 and 115 disclosures stand in their packets.)

## Rows held (owners named)

`W304-S1` (INERT): the Orion session secret is named three ways in the code (the route table says `orion/credentials`, the transport reads `orion/jwt/current`, the pull reads an S3 copy). `W304-S2` (INERT): the `inf-performance-daily` header says stale since 2026-04-28 while its Lambda schedules it daily; the live schedule and the table's frontier are unmeasured. No ARMED row. The commit gate's account-id check did not run on this commit either; it is `W182-S1`'s condition, owner `0.0.0_AB_MSTR`.

## What goes to the CTO

The ruling's branch is YES, with three facts that shape the feed `~P2` would add:
1. **One-account households only, today.** Account returns for multi-account households (the common case: 980 accounts in 320 households) are not what the code asks for. A feed that serves them needs either the vendor's multi-account Account grouping, which the fixture suggests, or one call per account.
2. **Gross or net is unknown.** Before the account figure replaces the household figure's sibling on a client page, someone must read Orion's definition of `calcGrossOfFees: false`.
3. **A nearer source may already be in the pull:** the Envision Performance Dim is a per-account period return from Orion's own report, if its staleness is not live.

None of the three is cut. The next cell is the CTO's to name; a read of the live Envision report's schedule and last landed date, and a read of Orion's definition of the fee flag, are the two I would expect.

## What this does to the FWD outcomes

Inputs to `FWD-2` for Inflection: not met. The account pages stay "Account-level returns are not available for this firm yet." until a sourced account figure lands.

## Open

**Andrew:** nothing from this workstream. **This seat:** the next B-IN cut waits on the CTO's round-117 B-IN analysis.

-- 2.0.0_SA_COO~I2
