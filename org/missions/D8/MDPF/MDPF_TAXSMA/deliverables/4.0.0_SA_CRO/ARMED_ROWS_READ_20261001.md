# MDPF_TAXSMA -- the five BLOCKING or ARMED rows, read and dispositioned (2026-10-01 ~09:1xZ to 09:4xZ)

**Author:** 4.0.0_SA_CRO (Chief Research Officer), the lease's seat
**Asked by:** `1.0.0_SA_CTO` msg 103657, RULINGS batch 74 item 6 @6a7377389e
**Rows read in:** `org/tier1_exec/3.0.0_SA_CVO/deliverables/MDPF_TAXSMA_REMEDIATION_v1_PREPARED_20261001.md` @90f597020a
**This file is not a channel carrier.** `3.0.0_SA_CVO` folds each disposition into the row's `disarm` field when the
rows land. Denominator: 5 rows asked, 5 read; 2 disarmed by an act this turn, 1 disarmed by law and by its own
condition, 2 not live today.

| Row | Standing after this read | By what |
|---|---|---|
| S12 | DISARMED for the false green | the checker now exits 2 when nothing was compared |
| S6 | DISARMED for this project | the condition now travels in the request file; no laptop seat can run the deploy |
| S10 | DISARMED | annex rule 26a, and the row's own condition has happened |
| S5 | NOT A LIVE HAZARD TODAY; its written remedy is NOT taken | Stage 6 was red before the Tax import and is not the writer of any key read today |
| S11 | NOT A LIVE HAZARD TODAY; BLOCKS ACTIVATION | nothing reads the two `.env` keys until the route is released and a bearer exists |

## S12 -- `verify-ec2.sh` said "in sync" on zero checks

Reproduced before the fix (09:3xZ, this seat): `bash infra/aws/ec2/verify-ec2.sh --ssm opal-gateway` printed
"Results: 0 checked ... All checked services are in sync." with rc 0, because `jq` is not on PATH and the service list
was empty.

Fixed in the commit carrying this file, `infra/aws/ec2/verify-ec2.sh`: `jq` resolves from PATH, then from the vendored
`.tools/jq.exe`, else exit 2; zero comparisons (clean + drift = 0) exits 2 with "NOTHING WAS COMPARED ... This is NOT a
parity verdict"; a run with skips says how many were skipped and not verified on its last line.

Exercised after the fix, four arms:

| Arm | Result |
|---|---|
| `--ssm opal-gateway` (vendored jq) | 1 examined, 1 skipped, 0 compared: rc 2 |
| an unknown service name | 0 examined: rc 2 |
| quick mode, all services | drift 8, skipped 18: rc 1 (the drift path, unchanged) |
| no jq anywhere (script copied outside the repo) | the ERROR line: rc 2 |

NOT fixed: the SSM probe still reports the Gateway "unreachable via SSM" while the instance is running. That cause is
unread and stays with the row's owner. The script now refuses to call it a verdict.

## S6 -- a Gateway deploy from CLOUD HEAD ships four other projects' commits

Not triggerable by this project today: annex rule 26a (@900da8bbb7, landed 04:37Z) bars every laptop seat from the
Gateway host deploy, and site Z declined the Tax release at 04:00Z. The hazard now belongs to whoever Andrew names to
run the release, so its condition was written into the only carrier that release has:
`org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/4.0.0_SA_CRO/SITEZ_GATEWAY_RELEASE_REQUEST_TX-r-2.md` (cut narrow, or
grade each rider first). NOT re-read: whether the four riders are still unreleased on the host.

## S10 -- the `opal-gateway` Terraform root had appliers on both devices

- Rule 26a is in `docs/doctrine/CLAUDE_ANNEX.md` line 520: the root is applied from site Z only. One applying device
  is the row's own remedy for the class.
- The row's stated condition (site Z pushes ac0290cdf7 and the laptop pulls) has happened:
  `git merge-base --is-ancestor ac0290cdf7 HEAD` is true. Positive control 0abf99fcd4 true; negative control, an
  unknown hash, false.
- This project applied TX-i-3 from the `mdpf-pipeline` root; its lease has not named a Gateway surface since 02:06Z.
NOT re-read: the root's plan (no laptop seat plans it now).

## S5 -- the EC2 daily runner's Stage 6 fails at import

Not a live hazard today, for three measured reasons:

1. **Stage 6 was already red before the Tax import.** CloudWatch `MDPF/DailyChain` `RevampParallelFailed` reads 1 on
   2026-09-18, 09-19 and 09-20; the Tax module reached the runner's code prefix on 09-21. Its completion marker
   `gold/mdpf_revamp/meta/cycle-complete.json` was last written 2026-08-14T07:28:26Z.
2. **Stage 6 is not the writer of anything read today.** The four staged spines under `gold/mdpf_revamp/` were last
   written 2026-09-30T13:30:54Z to 13:31:15Z, which is the Gold function's 13:30Z run; the function stages them
   itself, so they are fresh without Stage 6.
3. **No alarm sits on the metric** (`describe-alarms-for-metric`: 0).

The row's written remedy (sync `lib/` into the runner tree) is NOT taken, and this seat recommends against it. If the
import were repaired and Stage 6's earlier failure were also cleared, the runner would become a second writer of the
staged spines the Gold function writes. Placement is the CTO's: retire Stage 6, or name what still needs it.
UNMEASURED: why Stage 6 failed before 09-21. Off this row, filed as its own surprise row: the runner emitted no
`ChainFailed` or `RevampParallelFailed` datapoint on 09-28, 09-29 or 09-30, although its instance last launched
2026-09-30T13:30:35Z.

## S11 -- no cell wires the Tax bearer or identity into the Gateway `.env`

Inert today: the secret `gateway/global/taxsma-workbook-token` has 0 versions (read 09:2xZ),
`infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` at HEAD has 0 lines naming TAXSMA, and the route's two settings default
to empty, which is the capability-off state. Nothing reads the two keys until the route is on the host and a bearer
exists. NOT re-read: the host (last read 01:25Z, route absent).

It BLOCKS activation and is not disarmed. The two lines belong in a Gateway file, and the lease dropped the Gateway
surfaces at 02:06Z on Andrew's word. Who writes them and who deploys is the same call as the release's owner, and it
is Andrew's.
