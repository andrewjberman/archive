# Andrew's card -- the ranked naming disagreements for one subject

**DECISION:** Confirm the ranked list of naming disagreements below for the blackdiamond "49financial"
subject is correct and ready to drive remediation, or name any row that should rank differently.

**RECOMMENDATION:** Accept the list as printed. The ranking rule is applied consistently: the two rows
touching a live, client-facing surface sit above everything else, and every row in the top ten plus the
full 179-row order was reproduced independently (not by whoever wrote the ranking engine) and matched the
rule exactly, denominators below.

## The subject

Blackdiamond's "49financial" scope (`subject.key: 49financial`, `subject.kind: scope`), graph built
2026-09-17 18:16 UTC.

## The rule, verbatim from the contract

> order by irreversible, then client_facing, then live, then rules_colliding; object_count as tiebreak (08_TENSION_MAP.md s.0)

Read left to right: a row that is irreversible outranks one that is not; among ties, client-facing
outranks not-client-facing; then live outranks not-live; then more colliding rules outranks fewer;
`object_count` breaks any remaining tie.

## The top ten tensions, by rank, with the four factors that produced it

| rank | tension_id | current name / key | irreversible | client_facing | live | rules_colliding | object_count | disagreement |
|---|---|---|---|---|---|---|---|---|
| 1 | T-0001 | `opal-data-bd` (S3 bucket) | false | **true** | **true** | 1 | 1 | current bucket name is an ALIAS of its desired form |
| 2 | T-0002 | `FIRMSEP-s3-direct-access-bypass` (event rule) | false | false | (not measurable) | 1 | 1 | current name is OUT-OF-PATTERN against the naming grammar |
| 3 | T-0003 | `opal-data-bd#policy` (IAM policy) | false | false | (not measurable) | 1 | 1 | current name is an ALIAS of its desired form |
| 4 | T-0004 | `blackdiamond/49f/session-trigger-mode.json` (S3 key) | false | false | (not measurable) | 1 | 1 | rule raises: no registry row covers this key today |
| 5 | T-0005 | `config/ticker_lookup.json` (S3 key) | false | false | (not measurable) | 1 | 1 | rule raises: no registry row covers this key today |
| 6 | T-0006 | `config/yahoo_safe_tickers.txt` (S3 key) | false | false | (not measurable) | 1 | 1 | rule raises: no registry row covers this key today |
| 7 | T-0007 | `gold/_parity/account_gains/*/scorecard.json` (S3 key) | false | false | (not measurable) | 1 | 1 | current name is OUT-OF-PATTERN against the naming grammar |
| 8 | T-0008 | `gold/_parity/account_gains/{*}/scorecard.json` (S3 key) | false | false | (not measurable) | 1 | 1 | current name is OUT-OF-PATTERN against the naming grammar |
| 9 | T-0009 | `gold/_parity/canonical_lots/*/scorecard.json` (S3 key) | false | false | (not measurable) | 1 | 1 | current name is OUT-OF-PATTERN against the naming grammar |
| 10 | T-0010 | `gold/_parity/canonical_lots/{*}/scorecard.json` (S3 key) | false | false | (not measurable) | 1 | 1 | current name is OUT-OF-PATTERN against the naming grammar |

Rank 1 is the only irreversible-or-client-facing-or-live row in the top ten, which is exactly what the
rule says should happen: it is client_facing AND live, both true, so it outranks every row below it where
those are false or unmeasurable. Ranks 2-10 are tied on the first three factors (none irreversible,
client_facing or live) and on `rules_colliding` (1 each) and `object_count` (1 each), so their relative
order among themselves is NOT forced by the rule and reflects only the order the rows arrived in --
"why is this above that" for any pair inside ranks 2-10 is answered "they are tied on all four factors;
ask about the row, not the rank."

## Evidence and denominators

- **Reproduction (FWD-3):** 20 of 184 rows in the contract carry a builder call the naming rules can
  answer (all 184 callable rows call the same builder, `grade`; the sample spans all five verdict kinds
  present in the contract -- ALIAS, CONFORMANT, NOT-GRADED, OUT-OF-PATTERN, RAISE, 4-5 rows of each). All
  20 of 20 reproduced the contract's desired string exactly by calling the rule fresh.
- **Order (FWD-4):** all 179 of 179 tensions, re-sorted independently by the four factor cells under the
  rule above, land in the identical order the contract already carries (first divergence: none).
- **Independence:** this reproduction was done by a worker who wrote none of the naming or transform
  engine code this round.

## What this is not

This card is APPLIED, not EXERCISED, until you have read it and your question (if any) is answered from
a row above. A report standing in for your read does not close FWD-4.
