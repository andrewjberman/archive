# S11-AC3 -- JUDGMENT OUTPUT, RECORDED AND NOT SELF-GRADED

TO `IRPT_BCKEND.TO-IB-s-11` | cell `IB-s-11` | worker `0.9.0_WK_IRPT_BCKEND~4`
Oracle: `3.0.0_SA_CVO` at L9. This file carries the OUTPUT and NO verdict.

## 1. WHAT THE EVIDENCE DOES NOT ESTABLISH -- 9 of 9, BY SUBTRACTION FROM THE EVIDENCE'S OWN LIST

The denominator is not a list this worker recalled. It is the `unverified` array of
`docs/briefs/sources/INVESTOR_REPORTING_PERFORMANCE_EVIDENCE_20260910.json` @410f28f7db, read
whole: 9 entries. Every one is dispositioned below, and the disposition names WHERE it lands --
an absence row in the report, a refusal in the adapter, or outside this cell.

| # | evidence's own words | what the normalizer does | why UNSUPPORTED and not PARTIAL |
|---|---|---|---|
| 1 | `49F separate live tenant` | not an absence row -- `tenants.py` RESOLVES the route and the adapter never claims a tenant it did not read; the report's `scope` carries the firm it was ASKED for, never a firm it inferred | the capture is ONE BD account on `bd3.bdreporting.com` under the CRO operator session (`meta.coverage`: "One BD account; one Orion household with two accounts"). Nothing in the bytes identifies a tenant, so there is no partial 49F reading to carry -- there is no reading at all |
| 2 | `BD exact multi-account aggregate` | `REFUSE_SUMMED_AGGREGATE` in `normalize.py`; arm (d) shows the refusal firing on the Orion household, which is the only multi-account set in evidence | a BD relationship number was never returned. A "partial" aggregate would be a number this build computed; the whole point of the refusal is that no such number exists to be partial about |
| 3 | `Orion excluded-account scope` | the report `scope` records the EXACT selected set and the adapter refuses to serve a subset it was not asked for; no absence row -- a scope not requested is not a missing fact | never exercised: the capture requested the full household. A subset response has an unknown shape, so any handling would be inferred, and an inferred shape is not a partial observation |
| 4 | `long-period annualization` | absence row F-INF `annualization` UNSUPPORTED -- "the response carries no annualization flag; the period is 92 days and an annualized figure would be this build invention"; the report `annualization` field reads UNKNOWN | the provider emitted no flag at all. A 92-day window annualized is arithmetic on top of silence |
| 5 | `currency/accrual equivalence` | absence rows F-INF `accrual_basis` UNSUPPORTED ("startAccruedInt / accruedIntChange are present per day but the response declares no accrual basis") and F-INF `fee_basis` UNSUPPORTED; the report `fee_basis` / `accrual_basis` read UNKNOWN | the per-day accrual FIELDS are present, which is exactly the trap: fields present, BASIS undeclared. Carrying it as PARTIAL would advertise a gross/net reading the vendor never made |
| 6 | `benchmark variants` | absence row F-INF `benchmark` UNSUPPORTED -- "no benchmark node was requested in the captured Scope graph and none was returned" | nothing was requested and nothing came back; there is no fragment of a benchmark series to be partial with |
| 7 | `external contribution and gain bridge` | `REFUSE_VALUE_SHORTCUT`: `startValue + valueChange` is refused as a dollar history. Arm (e) prints the measured reason -- 6 of 9 cells match, 3 do not, max difference $210.68 | the shortcut AGREES 6 times out of 9. A PARTIAL disposition here is the dangerous one: it would ship a bridge that is right two thirds of the time |
| 8 | `production auth lifecycle and rate limits` | not modelled; the two 401 receipts become ABSENT-with-reason rows carrying the HTTP status, never a value. `LiveTransport` refuses to construct without the Andrew per-use word in two independent halves | a 401 and a rate-limited 429 are indistinguishable in a capture that contains neither refresh semantics nor a retry. Outside the reach of this cell |
| 9 | `silver directory population and policy joins` | OUTSIDE THIS CELL -- IB-s-2 owns scope resolution; this cell consumes a `ResolvedScope` FIXTURE by the L5 note of the order itself | not a fact about performance at all; recorded so the subtraction stays complete rather than trimmed to what is convenient |

**The one PARTIAL the report does carry, stated so the contrast is legible:** F-INF
`history_before_2026-06-10`, status PARTIAL -- "the group declares inceptionDate 2023-03-03 but
the captured calculation starts 2026-06-10". That is what PARTIAL means in this build: the
provider TOLD US the fact exists and we hold a proper subset of it. Census across both providers:
7 absence rows, 6 UNSUPPORTED and 1 PARTIAL.

**The rule this worker applied, stated for grading rather than assumed:** PARTIAL requires the
provider to have ATTESTED the whole and delivered a subset. Everything else -- a fact the provider
never declared, a shape never exercised, a number this build would have to invent -- is
UNSUPPORTED. Six of the nine unverified cases are undeclared-or-unexercised, so six are
UNSUPPORTED or refusals; one is a subset with an attested whole and is PARTIAL; two (8 and 9) are
outside the report fact vocabulary entirely.

## 2. WHAT THE FIRST LIVE CALL WOULD HAVE TO SHOW BEFORE THE REPORT IS ADVERTISED FOR A TENANT

Six things, each stated as a read a person can take, and each currently UNREADABLE offline. None
of them is authorized by this order (BOUNDS 1: no live vendor call without the explicit per-use
word from Andrew); this section is what the qualified live arm must PRODUCE, not a request to run
it.

1. **TENANT IDENTITY IN THE BYTES.** A 49F-credentialed call and a COT-credentialed call to the
   same `bd3.bdreporting.com` host return DISJOINT account sets. `tenants.py` separates the two
   routes by credential and data plane today; only a live pair proves the SERVER separates them.
   Until that read exists, "49F" in a served report is a label this build applied to a request,
   not a property it observed in a response.
2. **A BD RELATIONSHIP NUMBER THAT EXISTS.** A multi-account BD request that returns the vendor
   own aggregate, so the refusal in item 2 above has something to carry instead of a refusal. If
   BD returns no such node, the correct served answer is the refusal -- and that is itself the
   finding the live call would establish.
3. **THE UNIT TIE AT THE TENANT OWN SCALE.** The three ties measured here (max
   |percent/100 - (factor-1)| = 0.0 over 92 points x 3 groups; linked-minus-summary 1.2e-13 /
   1.1e-13 / 3.2e-13) must reproduce on the tenant own data. A unit convention that holds on one
   household and flips on another is the exact failure `units.py` exists to make impossible, and a
   single live household is enough to test it.
4. **A DECLARED FEE AND ACCRUAL BASIS, OR THE ABSENCE CONFIRMED.** Either the tenant
   configuration returns gross/net and accrual basis, in which case three UNKNOWN fields become
   values, or it does not -- and then the report is advertised WITH those three absences visible
   to the reader, which is a product decision and not the decision of this cell.
5. **THE DEPLOYED PATH ACTUALLY EXERCISED.** Row `IRPT_BCKEND-W4-S3` records that the deployed
   zip carries neither `jsonschema` nor the bounded BD helpers, so the deployed function today
   returns `contract_validated=false` with a named missing instrument and degrades the BD period
   cells to UNCERTIFIED. No criterion in this order invokes the deployed function. Before any
   tenant is served, a live call must run THROUGH the Lambda and show contract validation ON --
   i.e. the layer and the helper-packaging decision that row hands to `2.0.0_SA_COO~B` must land
   first.
6. **AUTH LIFECYCLE UNDER A REAL SESSION.** The two 401s in the capture are the only auth
   evidence that exists. A live call must show a token refresh succeeding, and a rate limit
   distinguishable from an auth failure, before an absence row can honestly say WHY a fact is
   missing rather than only THAT it is.

## 3. WHAT THIS OUTPUT DOES NOT CLAIM

It does not claim the adapters are correct for any tenant. It claims they are correct for the
bytes captured on 2026-09-10 and that every place they could have guessed instead, they refuse and
say so. The nine unverified cases are the distance between those two sentences.
