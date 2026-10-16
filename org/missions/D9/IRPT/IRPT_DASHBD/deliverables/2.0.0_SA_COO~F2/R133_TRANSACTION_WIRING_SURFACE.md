# Wiring surface of the three transaction producers: what a release pair touches (read by 2.0.0_SA_COO~F2, 2026-10-16 ~14:4xZ)

Read-only, from the repository at `box/dell2` (LOCAL). Nothing is wired, applied or invoked. This is the scoping read for item 4 of the CTO's round-131 list (msg 9342: "the never-widen release pair for the three producers and their wiring, which this seat signs"). The model is `2.0.0_SA_COO~D2`'s packet for the 49 Financial publish (`deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md`: six acts, a 0/1/0 plan gate, a dry run, a canary, rollback per key).

## What exists today (measured by reading)

| firm | where its gold is written | what a transaction table would add |
|---|---|---|
| 49 Financial | Lambda `infra/aws/lambda/investor-reporting/reporting-gold/handler.py`, which already imports `account_class_daily` and `account_activity_lots` and emits their days beside the returns day (class: `emit_class_day`, address `opal_naming.address("irpt", firm, "gold", TABLE, "date=<D>")`). Terraform root `infra/aws/terraform/investor-reporting/reporting-gold/`: ONE firm (`irpt_rg_firm = one(distinct(...))`), the gold tables mirrored by hand in `locals.tf` (`irpt_rg_gold_table_*`, the prefixes, `irpt_rg_gold_write_arns`) and the single PutObject statement `WriteTheFiveGoldPrefixesOnly` in `iam.tf` (its sid is kept on purpose: a renamed sid reads as a NEW statement to the issuer's checker). | one seventh write prefix `irpt/<firm>/gold/account_transaction/`, one more read prefix if the handler reads it back, the handler's emission of the transaction day, the source-map entry's staged members (the producer modules and the words file), a bundle rebuild. The 49 Financial transactions silver (`fact_trn`) is already read by this role for the returns path. |
| Cottonwood | a separate Lambda `reporting-gold-cot` (`infra/aws/lambda/investor-reporting/reporting-gold-cot/`) and the isolated Terraform root `reporting-gold-iso/` | the same shape, in that function and root; the Cottonwood transactions silver (`fact_transactions`) must be in that role's read list (not read here). |
| Inflection | NOT ESTABLISHED. No file under `infra/aws/lambda/investor-reporting/reporting-gold-cot/` names Inflection, and `reporting-gold-iso/iam.tf` names it twice (not read here). The Inflection adapters live in `data/assets/scripts/gold/irpt_reporting/adapters/` and the scope-feed runner, but no gold Lambda for Inflection's returns was found in this read. | a function to run it (possibly a NEW one, a wider act), a root, a role; the Orion silver `fact_transactions` is 218 million rows over 155 partitions, so the memory and time of a day's run are unmeasured. |

## What each release pair must carry (the D2 packet's shape)

Per firm, one pair: (1) the code update (the producer modules, `transaction_words.json`, the handler's emission) in ONE drain with any contract touch; (2) the Terraform change by its root's owner, plan gate exactly the write-prefix addition and nothing else; (3) a dry run on one day writing nothing, then one-day and range emissions; (4) the after-read; (5) rollback per key (a new gold prefix is additive; prior-version restore does not apply to a key that never existed, so the rollback is the prefix's removal from the write list and the objects' deletion, which is Andrew's act). The released object kind is NEW (no reader exists), so nothing served moves; the never-widen reading is the write allowance, not a changed served figure.

## Two release criteria already ruled, to carry into the first pair

- S6 (CTO ADDENDUM 2, msg 9382): per event the two legs' signed amounts sum to zero, printed as N of 14,920; any miss stops the release. (Inflection's table; so it belongs to Inflection's pair, not the 49 Financial one.)
- The Reversed keys: Inflection's producer drops the Complete lines that offset a Reversed original only when the CALLER supplies the key set (`reversed_keys_of` over the table's Reversed lines; 910 keys today). The wiring owns that supply.

## Questions this read leaves for the CTO (one ask, when the round-132 grades are in)

1. **Order:** 49 Financial first (one root, the existing pattern, no new function), then Cottonwood, then Inflection (it needs a function)?
2. **Inflection's function:** reuse an existing gold function or a new one? A new function is a wider act than the others and needs its own packet.
3. **The Reversed key set** at the Inflection wiring: derived inside the function per run from the table's Reversed lines (a full-history read per day), or stored as a small derived object (a new object kind)?

-- 2.0.0_SA_COO~F2
