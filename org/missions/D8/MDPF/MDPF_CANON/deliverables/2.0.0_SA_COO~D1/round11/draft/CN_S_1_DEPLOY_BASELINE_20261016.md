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

## Measured preconditions for the pair (read-only boto3 reads, 2026-10-16 ~15:0xZ; flags and counts only, no account id and no client name printed)

- **Identity flag (the Happyland precondition, ruling 5 of the v11 section): MATCH = TRUE.** In the newest `fact_model_assignment` partition (2026-10-16, 998 rows) exactly ONE account has `strategy_name == Opal_Muni_Income`, and that account is one of the 3 accounts whose `account_name` contains "happyland" (the Happyland-named rows carry exactly one `Opal_Muni_Income` strategy among their Opal strategies). No other account carries the strategy; none carries it as `program_name` or `account_name`.
- **The account's first date: 2026-10-08 (assignment partition), value date 2026-10-07.** `gold/dim_model_portfolio` holds a `model_name == Opal_Muni_Income` row on 9 of 69 partitions (2026-10-08 .. 2026-10-16), `account_count` 1 and `accounts_with_value` 1 on every one, a non-null `dollar_value` on all 9 (about $64.12M on value date 2026-10-07, about $63.47M on 2026-10-15). `fact_model_assignment` agrees: 9 of 77 partitions carry the strategy, the first 2026-10-08.
- **What that does to the blast radius (a correction to the v11 section and the order's record face, which said "from the account's first date" without a date):** the producer recomposes each date from the gold dim partitions, and only 9 value dates (2026-10-07 .. 2026-10-15) hold the account, so the dates whose Cottonwood and Global values can move on the first fire after the deploy are those 9 (plus the new date); every earlier date reads as today.
- **Not yet read:** the writers of each moved leaf (N), the served VersionIds after the 2026-10-16 fire, and `custom_residual_detail` on the dates before 2026-10-07 (expected empty of this account).
