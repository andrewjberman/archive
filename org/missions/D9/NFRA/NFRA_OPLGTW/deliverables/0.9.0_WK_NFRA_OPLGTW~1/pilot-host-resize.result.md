# NFRA_OPLGTW.TO-OG-i-4 -- pilot host resize (t4g.nano -> t4g.small) -- RESULT

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~1 | **Worktree:** C:/tmp/wk-oplgtw-1i4 (branch wk-oplgtw-1-i4) | **PRD:**
org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md v0.2 @f0aa50dbc0 | **Decomp:**
org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md v1 @8768f46770, cell OG-i-4.

## G-A

Verified in this worktree at HEAD before acting: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260918_140xZ_FOUR_CARDS_ANSWERED_GA_YES_SPRINT_EMPLOYEES.md`
is present at commit `80558e1508` (`git cat-file -e 80558e1508:<path>` rc=0), an ancestor of this worktree's
HEAD, and its Call 1 text reads verbatim "Call 1: Yes go ahead," answering the card "May the Gateway EC2
instance be STOPPED and STARTED for the resize (gate G-A, order OG-i-4)?" -- scoped explicitly to this
stop/start and not to the walkthrough gates (G-C/G-D, G-E/G-F).

## What was done

1. `terraform init` (cached providers, no external egress) then a pre-edit `plan` confirmed 0 drift against
   the live account before touching anything.
2. Edited `infra/aws/terraform/opal-gateway/main.tf`: `aws_instance.gw.instance_type` `t4g.nano` -> `t4g.small`.
3. `plan -out=resize.tfplan`: 84 `resource_changes`, exactly 1 non-no-op (`aws_instance.gw`, `actions=[update]`,
   `replace_paths=null`); `Plan: 0 to add, 1 to change, 0 to destroy`. The only concretely-declared changed
   attribute is `instance_type`; `public_dns`/`public_ip` show `(known after apply)` as the mechanical,
   unavoidable side effect of any stop/start on this non-EIP instance -- filed as `NFRA_OPLGTW-W1-S14`
   (OBSERVATION/INERT), not blocking.
4. Opened the change-management ledger (`nfra-oplgtw-og-i-4-pilot-host`, 2 legs) and committed it
   (`ee3bb28a51`) BEFORE the apply.
5. Applied the saved planfile through `.tools/safe-apply.sh` (`HALT_ACK=1` -- the halt-gate surfaced 25
   routine, non-STOP messages on the issuer's inbox; this worker carries no inbox of its own). rc=0:
   `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` (43 s modify).
6. Closed leg L1 (apply proof), then read live post-apply state for leg L2 (instance state, systemd,
   unauthenticated `/mcp`, existing-user latency re-take), closed leg L2, then closed the ledger. Committed
   the applied `main.tf`, the closed ledger and the surprise row together (`d83974bce5`).
7. Wrote the grading probe `probes/og_i4.py` (AC1..AC6) and ran every criterion's exact invocation from the
   task order.

## Criteria

| id | verdict | denominator |
|---|---|---|
| OGI4-AC1 | PASS | 1 ledger entry, 1 citation found; `git cat-file -e` rc=0 |
| OGI4-AC2 | PASS | 84 resource_changes, 1 non-no-op |
| OGI4-AC3 | PASS | 4 checks (safe-apply markers, apply-complete line, ledger CLOSED, sentinel absent) |
| OGI4-AC4 | PASS | 1 instance read: t4g.small / arm64 / running |
| OGI4-AC5 | PASS | 2 reads: systemd active/running; HTTP 401 with Bearer resource_metadata challenge |
| OGI4-AC6 | PASS | 2 CloudWatch reads (overall + 1 target group), 14-day window |

Full per-criterion output is in each acceptance row's `output_evidence` in the proof-of-spec instance.

## Instance, before / after (each read from AWS, not from the plan)

| | InstanceType | Architecture | State | LaunchTime | PublicIp |
|---|---|---|---|---|---|
| BEFORE | t4g.nano | arm64 | running | 2026-08-21T07:58:44.000Z | 13.221.151.249 |
| AFTER | t4g.small | arm64 | running | 2026-09-18T14:53:48.000Z | 54.197.78.28 |

## Existing-user baseline re-take (OGI4-AC6, OG-p-1's OGP1-AC11 instrument/window)

| | window | overall sample_count | overall p95 (s) |
|---|---|---|---|
| OG-p-1 (pre-change) | 2026-09-02T19:15:00Z .. 2026-09-16T19:15:00Z | 43745 | 0.5535024102704742 |
| OG-i-4 (re-take, recorded via `--record`) | 2026-09-04T15:20:10Z .. 2026-09-18T15:20:10Z | 39917.0 | 0.5506763705485934 |

Same instrument (cloudwatch `GetMetricStatistics` `AWS/ApplicationELB` `TargetResponseTime`, `SampleCount` +
`p95`), same 14-day window rule. Recorded in `OGI4_BASELINE.json`.

## Controls

- **Mutant:** `resize.plan.json`'s `changed_attribute_names`/`after_unknown_true` mutated to add a bogus
  `tags` change; `og_i4.py AC2` FAILed exactly as expected
  (`declared changed attributes ['instance_type', 'tags'] != ['instance_type']`); evidence restored
  byte-identical (`diff` empty) and AC2 PASSed again.
- **Determinism:** AC1..AC4 run twice, AC5/AC6 run twice (AC6 is a live CloudWatch re-take so its printed
  numbers legitimately drift run to run -- 39899/39917 samples, 0.5506999/0.5506763 p95 -- but the VERDICT
  is stable PASS across every run). No AC FAILed on the unmutated evidence.

## Surprises filed

- `NFRA_OPLGTW-W1-S14` (OBSERVATION/INERT): the resize plan shows `public_dns`/`public_ip` recomputed to
  `(known after apply)` alongside `instance_type` -- the unavoidable side effect of the same stop/start,
  not an independently configured second change. Not blocking; AC2's grading logic accounts for it
  explicitly (see `og_i4.py`'s `declared_changed` computation).

## Ledger

`org/critical_paths/change_management/20260918T1439Z_nfra-oplgtw-og-i-4-pilot-host_deploy_completion.md` --
opened + committed `ee3bb28a51` before the apply; closed (both legs proven) + committed `d83974bce5` before
any grading read. Sentinel `.open_deploys/nfra-oplgtw-og-i-4-pilot-host.json` removed on close. Never
half-landed.
