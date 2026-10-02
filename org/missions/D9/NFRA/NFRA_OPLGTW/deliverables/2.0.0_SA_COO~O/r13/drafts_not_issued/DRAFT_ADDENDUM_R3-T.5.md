

## ADDENDUM R3-T.5 (2.0.0_SA_COO~O, 2026-10-02 ~03:xxZ) -- round 13, the enrichment list of ROUND_ANALYSIS.round12.md

**Source.** `ledger/ROUND_ANALYSIS.round12.md` @1bbd4e166f section 5 (PRD v1.5 RATIFIED, wording only), issued in the D9
tree on `1.0.0_SA_CTO~O` msg 28145 (the D9 -> D6 move deferred; section 6 superseded). Item 1 re-cut on CTO rulings
28152 and 28154: G-C's controlled-identity requirement is RETIRED (Andrew-direct 2026-09-30 ~07:2xZ, "we shouldnt need a
'test user'"; OG-g-1's evidence: 0 of 38 internal users qualify); the walkthrough principal is Alyssa with Menachem's
G-E grant, AFTER Andrew's own speed and efficacy tests (Andrew-direct 2026-09-28 ~21:2xZ Call 1); Menachem is deferred,
not dropped; opalbloomberg@ stays out. Label `<round>13</round>`, ONE issuance, nine cells, eight independent chains
(`OG-au-1` -> `OG-rl-3`; the other seven alone); fanout: 8 of 8 chains, cap 8.

| cell | item | what | risk | slot | class |
|---|---|---|---|---|---|
| `OG-g-2` | 1 | MEASURE whether a WRITE_CAPABLE principal's Schwab request is evaluated against its data grant or bypasses the entitlement guard (code at live `3a7d6a7dc8` + one ungranted-master probe at that tier); verify the pilot principal's `tid`/`oid` from an authoritative tenant read against the host-side write-capable roster, by hash only. No grant write. | SERVED | ~23 | worker |
| `OG-au-1` | 2 | BUILD on CLOUD: `app/audit.py` + `app/tools.py` give `read_meeting_transcript`'s audit record an integer `bytes` (returned bytes) and a `principal` (`<tid>/<oid>`), email `user` kept; every other caller unchanged (row Z-W15-S23). | LOCAL | ~19 | worker-light |
| `OG-rl-3` | 2 | The NEXT GATEWAY RELEASE on live `3a7d6a7dc8`, after `OG-au-1` drains: the audit lines; `.env` values quoted so systemd and bash read them identically (Z-S32); the roster log count (Z-S34); `TAXSMA_WORKBOOK_IDENTITY` read host-side from a `taxsma_workbook_identity` key of `gateway/principals/rosters` (the role already reads it; no IAM change); the shipped contract copy pinned to `org/standards` with the grant-writer staging source pinned too (Z-W19-S13); MDPF_TAXSMA's Z-S41 module bytes ONLY if they have landed by the cut, sha-verified. CTO + COO halves (no capability change); NEVER-2 ledger `nfra-oplgtw-gateway-release-r13`. | WORLD | ~15 | worker |
| `OG-tf-1` | 3 | TF ROOT HYGIENE: the committed `infra/aws/terraform/opal-gateway` root plans with zero errors from a FRESH linked worktree with no `TF_VAR_*` and no copied build output (rows NFRA_MCPINDEX-Z-W21-S19, ETFS_RIVALS-Z-W5-S3); the fix moves nothing live (targeted grant-writer plan: No changes); saved plans and stray telemetry untracked. No apply. | SERVED | ~17 | worker |
| `OG-wp-1` | 4 | WALKTHROUGH PREP, read-only: the ACTIVE `email_deny` record's origin (writer, approver, time, authorization from its operator_audit items), a revoke-or-keep proposal, the three `probe-og-i1` partitions recorded as fixtures (row Z-W12-S8). S63 is dispositioned by the issuer's row in this issuance. | SERVED | ~20 | worker-light |
| `OG-r-4` | 5 | FWD-7 RE-MEASURE, read-only on the host: one `onhost_bench.py --scale full` run against the SERVED `3a7d6a7dc8` (engine md5 first), off-hours, synthetic principals; graded by `xf.AC1`/`xf.AC2` on the new record. | SERVED | ~16 | worker |
| `OG-tb-1` | 6 | The 9 OPLGTW red tests of NFRA_MCPINDEX's round-6 packet section 4: each repaired on CLOUD or named with its reason (pre-cut on CLOUD: 3 pass, 6 red). | LOCAL | ~18 | worker |
| `OG-o-4` | 6 | Runbook section 7.2 names the live release again (rb.AC2); W5-S6 closed in code: the stale `envelope.py` docstring fixed and one test pins a 500-row page of narrow rows. `OGO2-J1` re-graded at L9 by `3.0.0_SA_CVO~O` against the current runbook. | LOCAL | ~21 | worker-light |
| `OG-gr-1` | 7 | GRAIN MEASUREMENT (row Z-W10-S1): declared and candidate grain over EVERY qualified `dim_position` / `dim_asset` snapshot (closure-marker dates; printed denominator), why 5 of 10 colliding keys carry a blank, and the ruling's ADOPT/REFUSE verdict. | LOCAL | ~22 | worker |

**Stated dependencies, not cells.** The G-E grant write to the pilot principal and the `schwab` switch follow Andrew's
own speed and efficacy tests (his act; card `org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~AI/ANDREW_SPEED_EFFICACY_TEST_CARD_20260928.md`)
and `OG-g-2`'s measurement; FWD-3's denial arms are graded on her only if `OG-g-2` reads EVALUATES, else carried
UNEXERCISED until Menachem's deferred pilot (CTO 28154 (2)). OG-v-7 folds into OG-v-8 (CTO 28152). Z-S43's re-run waits
on the Research series invitation. Z-W13-S5 waits on the LGIC gate owner (parked with `0.0.0_AB_MSTR~Z`). Z-S41 waits
on MDPF_TAXSMA (laptop `4.0.0_SA_CRO`). Z-W12-S7 (the operator upload client, idle-expiry ~2026-10-18) is Andrew's
authorization-code re-consent, due before 2026-10-15.

**Pre-cut controls (issuer, this issuance):** `tf.AC1` FAIL (fresh worktree: 2 errors, 2 missing required variables);
`tf.AC3` FAIL (4 saved plans, 3 stray telemetry files); `rl3.AC1` 3 of 4 (`.env` 48 keys, 4 whitespace values, 4 parse
disagreements; host contract equals `org/standards` a86f7e667cfc); `rl3.AC2` FAIL (6 post-deploy transcript reads, none
with `bytes` or `principal`); `rl3.AC3` FAIL (no ledger, live = 3a7d6a7dc8); `tb.AC1` FAIL (3 of 9 pass on CLOUD);
`rb.AC2` FAIL (7.2 does not name live); every record-shaped check FAIL on absence, and each PASSes a synthetic good
record and FAILs a planted defect (wp, gr, g2.AC1, g2.AC2).

**Blindness stated:** `OG-g-2`'s probe runs at the WRITE_CAPABLE tier in a harness on the live tree, not as her live
session; a live session as her is the walkthrough itself. `OG-r-4` measures one synthetic load shape, not real usage.
