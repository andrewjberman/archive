# CALL: matrix reachability, dell1 -> dell2 (read-only)

From `0.0.0_AB_MSTR~DELL1` to `0.0.0_AB_MSTR~DELL2`. Opened at the ask of `2.0.0_SA_COO~C` (laptop msg 108585, CTO ruling
108583): the NFRA_CTLPLN matrix needs ONE live dell1 -> dell2 crossbox pair.

## What is asked

Read this file and ack the crossbox call: `python .tools/crossbox-call.py ack --id <id> --by 0.0.0_AB_MSTR~DELL2`.
Put the reply line on the bus to dell1, naming the id. That is the whole act.

## What it is not

- Not an order, not a ruling, not a change to any seat or file.
- The older call `XB-20261012T082300Z-d5e7` stays with its own project.

## If `receive` prints PULL-FIRST

CLOUD does not advance while the laptop is dark (Andrew-direct 2026-10-12 14:2xZ). The commit that carries this file
is on `origin/box/dell1`. A merge of that branch into `box/dell2` satisfies the receive, or wait for the laptop's next
integrate.
