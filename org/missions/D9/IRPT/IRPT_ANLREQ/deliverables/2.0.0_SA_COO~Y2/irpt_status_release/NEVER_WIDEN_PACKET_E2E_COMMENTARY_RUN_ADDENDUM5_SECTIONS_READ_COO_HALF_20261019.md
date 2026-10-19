# ADDENDUM 5 to the never-widen packet for the synthetic commentary end-to-end run -- run 4 reads the report document's sections once, read-only, as the live proof of the resident release r34l (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-19. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` and its ADDENDUMS 1 to 4 (ADDENDUM 4 CTO half signed @8aa5a765a1). **Ledger:** `irpt-commentary-e2e-4-20261019`. **Authority:** the r34l packet (`NEVER_WIDEN_PACKET_RESIDENT_R34L_REPORT_SECTIONS_AND_PRICING_ASOF_20261019.md`, blob `8ac60694bf`, CTO half signed `891cb3f4ff`), section 3 step 8: "Live proof is a separate act: run 4 reads, for one fresh synthetic Multi-Comp request, `sections[]` with 0 BUILDER_ONLY and 0 NOT_IN_THIS_VERSION entries, the NOT_SHOWN disclosure last, and the VALUE sections present."

## 1. Why

r34l changes what a NEW report's `sections[]` lists (AR-y-404, AR-y-408). Its V1 and V2 prove the package and the service environment, not a report. Run 4 already produces one fresh synthetic report through the resident, so one more read-only GET of that report's sections is the cheapest live proof. The pair as signed has no such read.

## 2. The change to the pair (everything else in the packet and ADDENDUMS 1 to 4 stands)

| step | change |
|---|---|
| R0 | adds: the running resident root reads `0485393f3a-r34l` (r34l closed by IB2's order `IRPT_ANLREQ.TO-APPLY-R34L...`); any other root is a STOP before any write, and the receipt names the root read |
| S | the variant is `multicomp` (the backend derives it from the count of comparison keys: none overview, one comparison, two or more multicomp, `ycharts/generate/submission.py:72`), with exactly TWO comparison keys in the shape the portal's `analysisBody` sends (`portal/src/pages/TicketCenter/analysisRequest.ts`, read at HEAD when the step is reached); IB2 picks the two keys from the served comparison catalogue at R0, prints them (names only) and records them. A Multi-Comp because the 425-cards defect was measured on one. The holdings and the token rules of ADDENDUM 3 are unchanged |
| R2 (new, after R, or after a stop at R, same user) | `GET /api/scoped/investor-reporting/analysis/{REQ id}/sections` with the same headers as step R. No body, one try. The receipt prints ONLY closed counts and names, no value: the HTTP status; the closed list of top-level keys of the response; `n_sections`; the counts by `status` (VALUE, NOT_AVAILABLE, other); `n_builder_only_without_value` (sections with `method` BUILDER_ONLY and `status` not VALUE); `n_not_in_this_version` (sections with `status` NOT_AVAILABLE and `reason` NOT_IN_THIS_VERSION); `n_value`; and, when the response carries a disclosure list, the ordered list of `disclosure_id`s and whether the LAST is `NOT_SHOWN` (when the response has no disclosure list, the line says `disclosures NOT-IN-RESPONSE`). A closed refusal (for example the owner placement of an advisor-owned request, ADDENDUM 1 section 4) is recorded with its code and is NOT a failure of the release: the receipt says `R2 REFUSED <code>` and the live proof is then taken from the run's own `run.json` by a separate read-only order, not here |
| D | unchanged (ADDENDUM 4: nothing is deleted before the last read, and R2 is a read) |

PASS for the release proof: `n_builder_only_without_value` 0, `n_not_in_this_version` 0, `n_value` at least 1, and the last disclosure `NOT_SHOWN` where the response carries disclosures. The receipt gains ONE line, `R2 sections ...`, between `R route` and `DLQ`.

## 3. Blast radius delta

One more read-only GET by the same synthetic user on a synthetic request; no write, no object created, no new principal.

## 4. Not claimed

- That the PDF printer or any other reader sees fewer sections (not read here).
- That a refused R2 means the release failed.
- That the counts hold for an Overview or a Comparison variant (the run is one Multi-Comp).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-19, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 4. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
