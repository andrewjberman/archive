INVESTIGATION THREAD: BD lot-level valuation reconciliation.

GOAL: Identify every systematic driver of the $68M net gap ($211M over / $143M under) between our gold holdings_lots market_value and BD silver allocations account_market_value, then design programmatic fixes.

ROLES:
- DS (0.4.0_DS_ClientPlatform) is the KNOWLEDGE SOURCE on lot reconstruction logic, pricing, and the FIFO algorithm in 03_build_holdings_lots.py. DS also owns 05c_validate_aua_vs_silver.py.
- AE (0.6.0_AE_PartnerETL) is the KNOWLEDGE SOURCE on the silver ingestion pipeline, S3 data layout, EC2 execution, and what BD actually sends in the daily feeds.
- DT (0.4.0_DT_ClientPlatform) is the KNOWLEDGE SOURCE on deployment state, Lambda configurations, and any Terraform-managed infrastructure involved in pricing or valuation.

DELIVERABLE: A ranked list of divergence root causes with proposed fixes, estimated impact per cause, and the data/code changes required. This will become the input for COO task order decomposition.

CRITICAL CONTEXT (from COO session 2026-03-23):

The COO ran a full reconciliation of the 2026-03-19 silver allocations ($1.593B, 6,415 accounts) against the 2026-03-20 gold holdings_lots (401,063 open lots across 7,791 accounts, limited to silver-overlapping accounts: $1.662B across 5,998 accounts).

NET GAP: +$68.2M (lot MV exceeds BD AUA by 4.3%)

But the NET understates the problem. The GROSS picture:
- 2,574 accounts where lot MV EXCEEDS BD AUA: +$211M total overshoot
- 3,778 accounts where lot MV is LESS than BD AUA: -$143M total undershoot
- These partially offset to the $68M net, but both directions need explanation.

WATERFALL DECOMPOSITION (COO analysis):

1. PHANTOM LOTS (+$74M, 271 accounts): Our lot MV is >2x BD's reported AUA. Worst case: z0819189891 has a single BNP Paribas lot at $20.8M but BD says the account is $1.9M. Account z0821392551 has $7.5M in ETFs but BD reports $3K. These are likely stale lots our FIFO thinks are open but BD has closed/transferred.

2. MISSING LOTS (-$27M, 146 accounts): BD reports AUA but we have $0 in lots. 30 are Bank accounts, 11 Savings, 7 'No Type Assigned', 5 Insurance. These are likely held-away or non-tradeable assets BD tracks at account level but doesn't include in the transaction feed.

3. INSURANCE/ANNUITY SHORTFALL (-$8M, 96 accounts): BD reports policy value but underlying sub-account holdings aren't fully visible in transactions. Opaque wrappers.

4. NON-INVESTMENT ACCOUNTS (+$2M, 103 accounts): Bank, Savings, CreditCard, Loans, Mortgage, TermLife. Noise.

5. NORMAL ACCOUNTS NET (+$11M, 5,534 accounts): Median divergence -0.4%, mean +0.9%. The net positive comes from a fat right tail:
   - 992 accounts overshoot by >20% (+$97M). Heavily IRA-concentrated (535 of 992). Top securities are standard ETFs (Pathfinder, IDVZ, VTV, IEFA, JEPI). Hypothesis: DRIP lots that our FIFO creates but BD nets into parent position.
   - 473 accounts undershoot by >20% (-$57M). Corporate accounts disproportionate (-$9.7M from 8 accounts). Hypothesis: advisory fee deductions or billings that reduce BD-reported AUA without appearing as exit transactions.

QUESTIONS FOR DS:
1. In 03_build_holdings_lots.py, how does the FIFO algorithm handle dividend reinvestment (DRIP) transactions? Does it create a new lot per reinvestment? Could this inflate lot count and MV relative to BD's position-level reporting?
2. What exit transaction types does the FIFO algorithm recognize? Is there a type for transfers-out, journal entries, or corporate actions (mergers, spinoffs) that would zero a position?
3. The 05c_validate_aua_vs_silver.py script exists — what does it currently check? Does it flag the per-account divergences we're seeing?
4. How are prices assigned to lots? Is current_price from a daily feed, or is it the last-known price from a transaction? Could stale pricing explain the overshoots on large accounts?

QUESTIONS FOR AE:
1. What does the daily BD allocation feed contain vs the transaction feed? Does the allocation feed have position-level detail or only account-level totals?
2. What is the S3 layout for silver allocations vs silver transactions? How far back do we have daily snapshots?
3. Are there known gaps in the transaction feed — transaction types BD sends that we ignore or don't parse?
4. For the 146 accounts with $0 lots: is it possible BD sends allocation data for accounts that have NO transaction history in our feed?

QUESTIONS FOR DT:
1. Are there any scheduled jobs or Lambda functions involved in pricing updates for the gold layer?
2. Is the silver-to-gold pipeline fully automated or does it require manual triggers?
3. What's the deployment state of the price override / scoped override system?

Self-unblock requirement: If you are uncertain about a data field, date range, output shape, or script behavior, use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.
