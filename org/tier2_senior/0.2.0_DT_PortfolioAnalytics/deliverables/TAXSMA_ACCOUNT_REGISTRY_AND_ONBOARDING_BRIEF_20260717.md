# Architecture Brief: Tax SMA Account Registry + Seamless Onboarding (`/tax-newacc`)

**For:** 1.0.0_SA_CTO -- to register a NEW PRD under the OPAL_TAXSMA macro (coupling OPAL_TAXSMA_PT2)
and write the TOs from the WS decomposition below (Andrew-direct: CTO writes the TOs, NOT via COO).
**From:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · **archetype:** SCRIBE (architecture)
**Origin:** Andrew-direct 2026-07-17 (verbatim intent captured below). Couples with OPAL_TAXSMA_PT2
(WS-1 producer @opal-assets-v0.27.0, WS-4 gateway IAM plan @CTO-gate-PASS).

## 1. The problem (Andrew-direct, verbatim intent)

> "surely there will be more [Tax SMA clients] ... we need a process whereby the accounts created
> for those new clients with the tax strategy are seamlessly added to this bucket when queried ...
> When a client account gets added to this bucket, that account is added to the daily bronze ETL and
> silver conversion ... as Alyssa works on onboarding ... she will need to get them added to that ETL.
> We need some kind of dedicated process ... maybe a new skill like /tax-newacc. She can run
> '/tax-newacc {new account number}' through the mcp connection ... with the iam scoped for this table
> ... it will do two things: one, that ad hoc call [run tax-pt2 on the spot]; the second, adding that
> account number to some kind of queue that writes that account to the list on the bronze etl for the
> table so from that point forward we get the daily data from that account added to the table in
> perpetuity."

**The defect this fixes:** WS-1's `discover_accounts()` is a stub; the first pull ran on a hardcoded
Chiles id. A hardcoded roster does not scale and is not operable by Alyssa. The account set must be a
**registry** that (a) drives the daily ETL and (b) is grown seamlessly at onboarding time.

## 2. The resolution principle (Andrew-direct, NON-NEGOTIABLE): EXACT ACCOUNT NUMBER, no fuzzy matching

> Andrew-direct 2026-07-17, verbatim: "this needs to all be done based on account number from Alyssa's
> docs not fuzzy matching or some bullshit."

The input is the **exact Schwab account number** Alyssa has in her onboarding docs. The account number
IS the key -- the resolver does an EXACT match on it, and NEVER a fuzzy name / last-4 / surname guess.
This eliminates the wrong-client risk entirely (a fuzzy match could pull the WRONG client's tax data;
an exact account-number match cannot). Grounding from the live probe that constrains HOW to do the exact
match:
- The sanctioned `portfolioreporting/api/accounts/Query/AccountDetailSearch` enumerates the 49F book with
  `internalId` + external `id` (= `z08` + internalId) + name + startDate, but the `accountNumber` it
  returns is **MASKED** (last-4). So the sanctioned surface cannot by itself CONFIRM a full-number exact
  match -- it can only return a candidate whose last-4 agrees, which is NOT an exact-number match.
- The FULL, unmasked account number is available on the `account-api/*` surface (a DIFFERENT egress
  path, live-observed carrying `accountNumber: 75250097` unmasked). An exact full-number match needs
  that surface (egress-scope extension, D3) OR a BD query-by-exact-number that returns only the matching
  account (so the match is exact BY CONSTRUCTION -- you asked for that number, BD returns that account).
- Fast path where it already exists: `dim_account_xref` maps `schwab_account_id` -> `bd_account_id`
  (external `z08`+internalId), so for xref accounts internalId = int(id[3:]) with ZERO live calls and an
  EXACT number key (Chiles 0027265115 -> 22596361, confirmed). Bump/Macy are simply not in the xref yet
  -- so the resolver's job is to do the exact-number resolution for accounts the xref lacks, and (ideally)
  write the result back so the xref/registry carries it thereafter.
- **=> The resolver is an EXACT account-number lookup, fail-loud if the exact number is not found or
  returns >1 account. No fuzzy fallback, ever.**

## 3. Target architecture

```
  REGISTRY (source of truth: which accounts are in the Tax SMA ETL)
     |  active entries: {schwab_acct, bd_internal_id, bd_external_id, client_name,
     |                   trade_start_date, strategy, enrolled_at/by, status}
     v
  BRONZE ETL producer (WS-1 + WS-5 schedule) -- reads the registry each run ->
     pulls performancePeriod/costBasis/allocation per enrolled account -> raw bronze
     v
  SILVER (WS-2) -> GOLD dim_taxsma_report (WS-3) -- process ALL enrolled accounts
     v
  Alyssa reads gold via the MCP gateway (WS-4 scoped IAM)

  ONBOARDING (the new piece):  /tax-newacc {schwab_acct}  [Alyssa, via MCP gateway, scoped IAM]
     (1) RESOLVE schwab_acct -> bd_internal_id (certain; see sec 4)
     (2) ENROLL: append to the REGISTRY (idempotent) -> daily ETL includes it in perpetuity
     (3) AD-HOC RUN: run tax-pt2 for that account NOW (immediate bronze->silver->gold, don't wait
         for tomorrow's ETL) so the report is available on the spot
```

## 4. The load-bearing design decisions (for CTO to rule)

- **D1 -- Registry substrate:** S3 JSON at `blackdiamond/49f/_ops/taxsma_roster.json` (monolith-native,
  versioned = enrollment audit trail; read-modify-write, low concurrency = Alyssa enrolls one at a
  time) vs a small DynamoDB table (better concurrent append/status/query). Rec: S3 JSON unless CTO wants
  DDB semantics. Either way it is the ONE source of truth the ETL reads.
- **D2 -- EXACT account-number resolution (Andrew-mandated, sec 2):** `/tax-newacc` resolves the EXACT
  Schwab account number from Alyssa's docs to the BD internalId -- exact, never fuzzy. The mechanism must
  produce an exact-number match. Ranked options: (a) FULL-number match via `account-api/*` (unmasked
  number = a true exact match; needs the egress-scope extension, D3); (b) BD query-BY-exact-number on the
  sanctioned surface that returns ONLY the account carrying that number (exact by construction -- confirm
  the endpoint supports an exact accountNumber filter, WS-R2's job); (c) xref/registry fast-path where
  the number is already resolved (int(bd_account_id[3:])). The resolver FAILS LOUD if the exact number
  is absent or resolves to !=1 account -- no fuzzy fallback. Rec: (a) or (b), whichever gives a
  confirmed exact-number match; resolve once, persist to the registry.
- **D3 -- Egress scope:** the enumeration is `portfolioreporting/api/accounts/Query/...` (WITHIN the
  standing 49F-reporting word). If D2 needs the FULL number (option a), `account-api/*` is a NEW egress
  surface -- flag to Andrew for the word extension (same producer/purpose, different path).
- **D4 -- Gateway IAM coupling (extends WS-4):** `/tax-newacc` needs Alyssa's scoped role to (i) trigger
  the ad-hoc pull (lambda invoke) and (ii) WRITE the registry (S3 put / DDB write) -- beyond WS-4's
  read-only gold grant. This is a net-new grant -> CTO plan-gate + Rule-22a, same discipline as WS-4;
  keep it single-purpose (invoke ONLY the tax producer, write ONLY the registry key).
- **D5 -- Ad-hoc vs standing coherence:** the ad-hoc `/tax-newacc` run and the daily ETL use the SAME
  producer + SAME bronze partitioning (pull-date) so an ad-hoc pull and the next daily pull are distinct
  snapshots, never a silent overwrite (the BD-revision contract property already in WS-1).
- **D6 -- Initial seed:** seed the registry NOW with the known live accounts (Chiles 0027265115 -->
  22596361 confirmed; Bump 0035940058; Macy 0091939812; + any 4th) -- each resolved via D2's certain
  path, human-confirmed, not guessed.

## 5. Proposed WS decomposition (my specifications -- for CTO to turn into TOs, direct)

- **WS-R1 REGISTRY:** define the registry (D1 substrate + schema + read-modify-write/append protocol +
  status lifecycle) + seed the known accounts (D6, resolved+confirmed). Owner: 0.2.0_DT.
- **WS-R2 RESOLVER:** the EXACT account-number -> internalId resolver (D2/D3) -- a shared module the
  skill + seed use; input is Alyssa's exact account number; EXACT match only, FAIL-LOUD on absent-or->1;
  no fuzzy fallback. Establishes which endpoint gives the confirmed exact-number match (account-api
  full-number vs a sanctioned exact-number query). Owner: 0.2.0_DT.
- **WS-R3 ETL-READS-REGISTRY:** replace the producer `discover_accounts()` stub with a registry read
  (active entries); WS-5 schedule pulls all enrolled daily. Owner: 0.2.0_DT (small; the producer is mine).
- **WS-R4 /tax-newacc SKILL:** the skill = resolve+confirm -> enroll -> ad-hoc tax-pt2 run; MCP-gateway
  operable; idempotent. Owner: 0.2.0_DT (+ DE if any FE).
- **WS-R5 GATEWAY IAM EXTENSION:** Alyssa's role gains registry-write + tax-producer-invoke (D4);
  CTO plan-gate + Rule-22a. Couples with OPAL_TAXSMA_PT2 WS-4. Owner: 0.2.0_DT design / AE apply / CTO gate.

## 6. Relationship to existing work

Extends OPAL_TAXSMA_PT2: WS-1 producer (built, live) gains the registry read (WS-R3); WS-4 gateway IAM
(plan PASS) gains the onboarding grants (WS-R5); WS-5 schedule pulls the registry set. The registry is
the missing source-of-truth that makes the whole chain scale seamlessly as Alyssa onboards clients.
Request: register as a new PRD under the OPAL_TAXSMA macro, coupling OPAL_TAXSMA_PT2; write the TOs from
sec 5.
