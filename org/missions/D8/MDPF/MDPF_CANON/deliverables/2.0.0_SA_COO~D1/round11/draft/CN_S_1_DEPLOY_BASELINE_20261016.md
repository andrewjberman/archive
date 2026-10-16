# CN-s-1 deploy baseline -- two lambdas, MEASURED read-only 2026-10-16 14:34Z (2.0.0_SA_COO~D1)

**archetype:** EXPLORE

Pre-draft for the CN-s-1 never-widen pair and the CloudOps ADHOC order (owed after the cell builds). Nothing here is deployed. Every value below was read live with `aws lambda get-function-configuration` (us-east-1) and is MEASURED at the stated time; the pair re-reads it at signing.

| surface | CodeSha256 | LastModified | other |
|---|---|---|---|
| `mdpf-gold-lambda` | `vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=` | 2026-10-15T16:18:35Z | python3.11; `MDPF_GOLD_COMMIT` `b6352de8f843f3726ad5c51c650d9035ca8336db` (the round-10 pin, CN-r-1); 1,958,957 B |
| `opal-assets-daily-emitter` | `GLQf6kv4nzRLGd53ONG4S5F4ikOso/2lkbq03U/+G9A=` | 2026-10-09T02:43:17Z | python3.11; no `MDPF_GOLD_COMMIT`; 59,165 B |

What this says for the order:
- The gold lambda carries CN-r-1 (round 10) and has fired once with it (2026-10-16 13:30Z, readback 11 of 11). CN-s-1 is the NEXT gold change, so it can deploy no earlier than the window before the 2026-10-17 13:30Z fire, and only after the CN-s-1 pair is signed by both halves.
- The daily emitter has not been touched since 2026-10-09; the crosswalk copy it carries (`mdpf_revamp_model_crosswalk.py`, byte-identical to the gold-side file at the base, MEASURED by the check's arm S1) is a SECOND deploy surface for CN-s-1. That the emitter's package is built from that file is INFERRED from its path; the order's first leg confirms it (`comp-pipescript io` / `comp-estate`) before anything is applied.
- The rollback per surface is the prior CodeSha256 above plus the prior package VersionId, to be read at the order's start.

Not yet read (owed to the pair): the account's first served date and whether it holds a value before 2026-10-07; the Happyland identity flag (a match flag, no name); the writers of each moved leaf (N); the prior VersionIds of the served Cottonwood and Global objects after the 2026-10-16 fire.
