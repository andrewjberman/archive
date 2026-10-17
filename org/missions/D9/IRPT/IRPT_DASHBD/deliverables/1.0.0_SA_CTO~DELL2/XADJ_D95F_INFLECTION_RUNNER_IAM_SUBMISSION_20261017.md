# Cross-adjudication submission: call d95f, the Inflection transaction pair's IAM widening on the runner role

## Context
`2.0.0_SA_COO~F2`'s read `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/R137_INFLECTION_RELEASE_PLAN.md`:
- the step runs on the EC2 runner `inf-gold-layer-runner` under role `inf-gold-layer-ec2-role` (`infra/aws/terraform/inf-pipeline/iam.tf`);
- that role cannot read the Orion `fact_transactions` silver in `opal-data-assets/orion/inflection/silver/fact_transactions/`;
- it cannot write the Inflection gold prefix in `opal-data-inflection`;
- it already DENIES `opal-data-bd` and `opal-data-cot`.

## Position
(a) **Home:** that role, through ONE new scoped inline policy, a separate resource shaped like `inf_gold_layer_scope_feed`:
- GetObject plus a prefix-conditioned ListBucket on the Inflection `fact_transactions` silver prefix only;
- PutObject on the ONE Inflection `account_transaction` gold prefix only;
- both addresses are `lib/opal_naming.py address()` output, printed in the packet;
- nothing on any other firm's bucket or key prefix (the cross-firm law); the existing DENYs stay.

(b) **First range:** bounded, 25 trading days, by the launcher called directly under SSM with `--since`. The chain's TXN-BLOCK takes over
after the first read.

(c) **The runner:** started and stopped per `INF_GOLD_RUNNER_DEPLOYMENT.md`, and stopped at the end of the act.

(d) **Order:** the cells are built now. The apply waits until the 49 Financial pair's first scheduled fire after its re-stage has been read
(Monday 2026-10-19), and it never runs at the same time as another IB2 apply. Cottonwood and Inflection then go in whichever order their
packets are signed.

## Why it gave pause
### Ambiguity
It is the first READ grant in the three pairs. 49 Financial and Cottonwood each needed only a write prefix.
### Out of pattern
The pattern is the same: the firm's own data, by its own role, scoped by builder addresses. The read grant is what is new.
### Other solutions
- A new role or function for the step: cleaner isolation, but a new runner identity for one stage. Rejected unless the read shows the role
  is shared with another consumer.
- Running it from Lambda: it does not fit the snapshot read time (10 to 12 minutes measured locally for the census).
