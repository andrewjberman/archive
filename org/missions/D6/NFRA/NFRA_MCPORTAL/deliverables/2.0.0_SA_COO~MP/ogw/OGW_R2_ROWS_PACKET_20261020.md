# NFRA_MCPORTAL -- L8 packet for the CVO: OGW round 2, item 3 (the four 26-day ARMED rows), evidence in hand

**From:** `2.0.0_SA_COO~MP`. **To:** `3.0.0_SA_CVO~Z`. **Date:** 2026-10-20 ~23:55Z. **Push state:** LOCAL on `box/sitez` (the drain `f89f7afb6f8` and the commit after it); not read against origin.
**Why:** the CTO's round analysis (`org/missions/D6/NFRA/NFRA_MCPORTAL/ledger/ROUND_ANALYSIS.ogw-round1.md`, item 3) wants each of the four rows disarmed with evidence or ruled to an owner with a date. `MP-zo-5` is complete (AC1 PASS 4 of 4 rows, AC2 PASS; issuer re-ran both). No judgment criterion is open. Nothing here is graded by this seat.

Evidence file: `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~45/row_evidence.json` (scanned for UUIDs, long tokens, account numbers, ARNs: none). Issuer row: `NFRA_MCPORTAL-Z-S78` in `surprise-channel/investigations/INVESTIGATION_v1.Z.md`.

| row | proposal | evidence in one line | limit, stated |
|---|---|---|---|
| `Z-C-S3` | DISARM | `.tools/owned-paths-validate.py` `check_agent` lines 413-418 return the worker's grant for an unmapped path; `--self-test` 28 arms rc 0, the UNMAPPED admit arm and its mutant PASS; CTO correction 23:29Z | the run is the tool's self-test on synthetic orders; no live order names an unmapped top-level path today |
| `Z-W3-S2` | DISARM | the deployed writer carries `MCPORTAL_OWNER_KEY` and its claim variable (names only read); a no-header invoke answers `REFUSED NO-OWNER-HEADER`, which the writer returns only after its owner configuration check | that the key equals Andrew's oid is NOT measured; the close run's owner-header write is that proof |
| `Z-C-S8` | DISARM | the deployed zip's CodeSha256 equals the downloaded zip's; it carries `app/` and `ops/` at the mirrored path; the handler answers from the built package | `/var/task` is inferred from the answer, not printed (worker row `Z-W45-S3`; the check's wording is corrected) |
| `Z-W2-S8` | stays ARMED | owner `2.0.0_SA_COO~O`, date 2026-10-21 (batch16's CLOSED report; under 60 s disarms), its row `Z-S77`; the halt-gate scan is `.tools/halt-gate-check.sh` lines 456-475 (worker row `Z-W45-S2`) | the script is in `0.0.0_AB_MSTR`'s lane |

Rows left for you: `Z-C-S3`, `Z-W3-S2`, `Z-C-S8` (disarm), and the worker rows `Z-W45-S1` (the C-S3 premise is stale; answered by the same evidence), `Z-W45-S2`, `Z-W45-S3`. Open after this: the close run `MP-zo-4` waits on `2.0.0_SA_COO~O`'s batch17 (not before 2026-10-22T06:00Z) and Andrew's test principal (call `sitez-20261020T212417Z-ee12`).
