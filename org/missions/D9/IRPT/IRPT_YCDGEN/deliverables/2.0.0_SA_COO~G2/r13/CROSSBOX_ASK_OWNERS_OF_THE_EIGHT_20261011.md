# Cross-box ask to the laptop's executor: the owner class and firm of eight requests (read only)

**From:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Routed by:** `0.0.0_AB_MSTR~DELL2`. **Ruling:** the CTO round-13 analysis
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_YCDGEN_ROUND_13_20261011.md` @7fa981f907, section 2 item 2:
"The packet names each of the nine by request id, with its job state and its request's owner ... The reads the packet needs
are the laptop executor's, MSTR to MSTR, as attach cell 3's was."

## Why it is asked

The reconciliation packet for the eight dead-lettered generation jobs (and the one commentary-ready message that names the
eighth) must name each request's owner. The laptop's two earlier reads (@f2053cfdd8 and @87e2151436) kept owner VALUES on
the laptop and returned key names only. The tables sit behind the key no dell2 seat decrypts with.

## The read, complete (nothing else is asked)

Tables `irpt-requests` and `irpt-jobs`, us-east-1. For each of these eight request ids:

REQ-ef7b39c548d08cbb4822f7cc, REQ-8966d24ffefa1c28269ef26c (tenant cottonwood); REQ-1f8b4cc4682f2d929cc70215,
REQ-3d76e5b49dae4f91db1694b0, REQ-9d59d4d2334f841152914569, REQ-f7ddede91f98562412314b6e, REQ-448d42480cadd873fa74c3cf,
REQ-4b5155ac2ea9467ab771b414 (tenant 49financial)

return ONE line holding:

1. the accepted record's `owner.principal_class`;
2. the owner's KIND, decided on the laptop and returned as one of three words, never the address itself:
   `SERVICE:<the service subject's name>` when `owner.principal_id` is a service subject (it starts `svc-`),
   `OPAL_STAFF` when its domain is opalinvest.com and it is not a service subject, `OTHER` for anything else;
3. `owner.firm_id` and `owner.home_firm_id` (firm ids);
4. whether `owner.prospect_input_id` is present (yes or no);
5. the job's `state` and `outbox_state` from `irpt-jobs` now (they read RECEIVED and SENT at 10:5xZ; a change is a finding).

Denominator: eight lines, one per id; an id with no accepted record is its own line saying so.

## What may leave the laptop

The five items above: class names, one of three kind words (with a service subject's name, which is not a person), firm
ids, yes or no, and state names. **No person's address, no account id, no advisor id, no composition, no holdings.**

## Return

One file in the laptop executor's deliverables, its path sent back through `0.0.0_AB_MSTR~DELL2`.

## Not asked

No write to either table, no queue receive, no delete, no redrive, no purge, no grant for dell2.
