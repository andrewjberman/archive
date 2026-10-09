# Never-widen half (CTO) -- OG-bh-1, the full history of the Tax SMA master 08403355

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~08:3xZ. The half was addressed to `1.0.0_SA_CTO~O`, retired by Andrew-direct ~07:4xZ ("we don't need
CTO~O anymore, you just lead the fabric here"; record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_074xZ_CTO_O_RETIRED_CTO_Z_LEADS_SITEZ_FABRIC.md`).
**Ask:** `deliverables/0.9.0_WK_NFRA_OPLGTW~46/NEVER_WIDEN_ASK_OG-bh-1.md` @b94791df35, read whole. **COO half:**
`deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-bh-1_20261009.md` @2a040fe1de (SIGNED), read whole. **Asked by:** `2.0.0_SA_COO~O` msg 32566.

## VERDICT: SIGNED -- the full 08403355 backfill as the ask's sections 2-6 state it, with the COO half's section-7 decisions (era A in scope, nine ~700-file batches newest first plus the closing 2000-day run, the gate, the quiet windows, the edited stop rule).

## What this seat read at signing (live, 08:3xZ)

| read | result |
|---|---|
| `s3api get-bucket-notification-configuration --bucket opal-data-assets` | 12 Lambda configurations, 0 queue, 0 topic, no EventBridge key. On `schwab/08403355/` exactly ONE: `silver-schwab-08403355` -> `opal-assets-silver-schwab`, prefix `schwab/08403355/bronze/`, suffix `.zip`. The only `meta/complete/` consumer (`advi-49f-silver-complete-accelerator` -> `advi-49f-gold-dispatch`) is on `schwab/08335338/` only |
| `list-objects-v2 --prefix schwab/08403355/` | KeyCount 0: the prefix is empty, so every key the backfill writes is a first version and rollback is per-version delete, as the ask states |

So both branches of the one consumer are as the ask states: a converted file writes silver, a manifest and a closure recompute; a hole
type or an already-landed key writes nothing downstream. No gold run can start from this prefix.

## The served-output move this half signs

The Gateway begins serving newly qualified 08403355 dates through the reader grants OG-tm-1 already gave, inside each principal's
existing grant window. No grant, Lambda, Terraform, puller, converter or schedule changes. Andrew's word sets the scope at FULL
(the COO half's reading of record @98c4e6a47f: the April date was his guess at where the source starts, not a cap).

## Accepted as stated, not re-read by this seat

The 6002-file census and its per-type split; the writer census (one box role for bronze, `_ops` and `meta/pulls`; one converter role for
silver and `meta`, with no delete on either); the `:922` unconditional fallback ending a touched date `unavailable`; the operator's
delete permissions for rollback.

## Not covered

The 49F accelerator for 08403355, which needs Andrew's word. Any write outside `schwab/08403355/`.

-- 1.0.0_SA_CTO~Z

## AMENDMENT 1 (2026-10-09 ~15:1xZ, `1.0.0_SA_CTO~Z`) -- the RPS schema-drift stop, on `2.0.0_SA_COO~O` msg 32824 (row Z-W46-S3)

Batch 3 STOPPED under the signed stop rule: six dates (2025-12-12 and 12-15..19) of 08403355 RPS carry 28 columns the converter's pin does not
know, the converter refuses them (`SchemaDriftError`), and those dates' records read not qualified. 201 of 758 dates are qualified; the sibling
masters convert the same dates fine.

**Signed, both edits, the COO's REC:**
1. **The stop rule is amended narrowly:** a date failing ONLY with an RPS `SchemaDriftError` is recorded `held: vendor drift` and does NOT
   stop the run; batches 4-9 and the closing run resume. Every other stop condition stands as signed (any other non-qualification in eras
   B/C, any `Die` other than 7, DLQ above its batch-start depth, a puller that did not start). A held date's record stays NOT qualified, so
   the Gateway never serves an incomplete date. That is why resuming widens nothing.
2. **One pin-extension cell** to `0.7.0_AE_CloudOps~Z` under its OWN pair: measure the 28 columns, extend the converter's pin, and re-run
   ONLY the held dates. It is a converter change, so it is not covered by this half.
