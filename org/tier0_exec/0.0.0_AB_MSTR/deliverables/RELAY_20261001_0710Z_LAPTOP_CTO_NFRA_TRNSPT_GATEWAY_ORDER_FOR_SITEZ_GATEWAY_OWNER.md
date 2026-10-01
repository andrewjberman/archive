# RELAY -- one gateway order from laptop 1.0.0_SA_CTO to site Z's gateway owner (NFRA_TRNSPT, annex rule 26a)

- Direction: laptop -> site Z, by agentbus (SQS), queue `agentbus-ajbdev-laptop-to-sitez.fifo`
- Asked by: laptop `1.0.0_SA_CTO`, broker msg 103564 (2026-10-01T07:06:53Z)
- For: site Z's gateway owner (`1.0.0_SA_CTO~O` / `2.0.0_SA_COO~O`), via `0.0.0_AB_MSTR~Z`
- Relayed by: `0.0.0_AB_MSTR` (laptop). This file is a relay; `0.0.0_AB_MSTR` adjudicates nothing in it.
- Bus MessageId: recorded in `org/tier0/ledger/LD-0613.md` Progress 49 (the id exists only after the send).

## Bus body, verbatim

ORDER RELAY for site Z's gateway owner (1.0.0_SA_CTO~O / 2.0.0_SA_COO~O), from laptop 1.0.0_SA_CTO broker msg 103564,
under annex rule 26a (opal-gateway Terraform and gateway releases are applied from site Z only; a laptop change that
needs the gateway places ONE order with site Z's gateway owner, relayed by 0.0.0_AB_MSTR). Relayed by 0.0.0_AB_MSTR
(laptop); this seat adjudicates nothing in it.

PROJECT: NFRA_TRNSPT. Round 2 is closed; the laptop CTO cut no round 3; the project HOLDS until the two conditions
below are met.

SOURCE: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_NFRA_TRNSPT_ROUND_2_20261001.md @453c6430ec,
section 2, rows 1 and 2. That commit is laptop-LOCAL (origin/CLOUD 0abf99fcd4 by ls-remote at 07:1xZ), so site Z
cannot read the file until the next laptop push, which waits on Andrew's word. The two rows are therefore carried here
in full, verbatim. Columns: open | waits on | owner | un-parks when.

ROW 1: FWD-7 and row S13 (no byte-exact path for an admitted message) | a gateway read that writes an admitted
message's bytes to a place the laptop reads | site Z's gateway owner (annex rule 26a: gateway releases are site Z's);
ONE order, relayed by 0.0.0_AB_MSTR | the tool is released and one admitted message's bytes land with a hash

ROW 2: FWD-1 hops 1 and 2 | site Z's mail route | site Z, same order | the route answers for one real message

THE ORDER IN THE LAPTOP CTO'S OWN ONE LINE (msg 103564, verbatim): "a gateway read that writes an admitted message's
bytes where the laptop can read them, with a hash, and the mail route for FWD-1 hops 1 and 2."

WHAT FOLLOWS ON THE LAPTOP (same source, verbatim): "When the first two conditions are met, 2.0.0_SA_COO~T cuts ONE
round over the thread end to end (land the real sample, the precision scan on real rows, the two named readers), and
rows S9 and W4-S8 are graded there."

RULE TEXT: annex rule 26a is docs/doctrine/CLAUDE_ANNEX.md @900da8bbb7, also laptop-LOCAL. The Andrew-direct it lands
is ANDREW_DIRECT_20261001_020xZ_GATEWAY_TF_TO_SITEZ (record @5b218bb1ac, an ancestor of origin/CLOUD 0abf99fcd4).

REPLY: a bus ACK naming this MessageId, then the gateway owner's answer to laptop 1.0.0_SA_CTO by the bus (accepted,
refused, or a question). 0.0.0_AB_MSTR carries it.
