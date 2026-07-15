# EC2 Telemetry + Right-Sizing + Autoshutdown Standard (OPAL_STNDRD axis D)

> **CANONICAL TARGET:** `docs/deployment/EC2_TELEMETRY_RIGHTSIZING_STANDARD.md` -- BASE_EXEC lane;
> CTO lands the canonical copy (same route as trigger-map-drift.yml @ 4fc940caa). This deliverable
> copy is the authored source of record until then.

**Status:** RATIFIED (CTO, all six axes, OPAL_STNDRD.json; Andrew mandate verbatim in brief
20b52be25 sec-0: "when we use ec2s, we install them with our telemetry analysis so we can keep an
eye on them with a protocol for right sizing").
**Binding:** NEW provisions immediately; existing boxes on natural touches (no big-bang sweep --
retroactive findings are lists, never auto-edits). Complements, never replaces, EC2 law
(CLAUDE.md Rules 7-12: manifest, safe-ec2-deploy, S3-artifact-store, TF-owns-infra).
**Owner:** 0.7.0_AE_CloudOps (Z1 phase 5). Pilot: canonical-schwab-si2.

## 1. The three requirements

**(a) TELEMETRY AT PROVISION.** Every EC2 provision installs the CloudWatch agent in its
user-data / setup script, emitting `CWAgent` namespace metrics (mem_used_percent,
disk_used_percent; CPU comes free from AWS/EC2). A box with no CWAgent metrics is UNMEASURED --
memory pressure is invisible to every right-sizing decision (CPU alone cannot justify a
downsize; the 2026-07-13 orion OOM class was a MEMORY event no AWS/EC2 metric showed).
*Instrument check:* `aws cloudwatch list-metrics --namespace CWAgent --dimensions
Name=InstanceId,Value=<id>` -- count 0 = unmeasured, a finding.

**(b) RIGHT-SIZING REVIEW, quarterly or on-incident.** The Lambda `sizing_basis` discipline
(delta-6 three-dimension form: RSS / wall / tmp on the heaviest real unit) ported to EC2:
a review records CPU avg+max, mem_used_percent max (needs (a)), disk, and the DUTY CYCLE
(scheduled windows vs 24/7) over >=7 days, and renders a verdict: KEEP / RESIZE(type) /
RESCHEDULE(autoshutdown). Recorded in the manifest row (schema sec-3), never in prose only.

**(c) AUTOSHUTDOWN BY DEFAULT.** A box whose duty cycle is scheduled windows (not 24/7) runs
schedule-scoped uptime: EventBridge Scheduler start (grammar `{unit}-run-{cadence}` per axis B)
+ self-stop at work-end (`instance_initiated_shutdown_behavior = stop`, the
consolidation-gold-runner / canonical-schwab-ec2 pattern). 24/7 is the DECLARED EXCEPTION,
never the silent default: `"autoshutdown": {"mode": "24x7-exception", "reason": "<why>"}` in
the manifest row. An undeclared 24/7 box is a finding.

## 2. Pilot: canonical-schwab-si2 (measured 2026-07-15 ~21:1xZ, live)

| Evidence | Value | Verdict |
|---|---|---|
| Instance | i-0f3d57a97f14727af, t3.large, 24/7 | duty cycle is 4 fixed cron windows/day (09:45/10:15/21:45/22:15Z pulls) |
| CWAgent metrics | **0** (list-metrics count) | UNMEASURED -- (a) violated; mem/disk invisible |
| CPU 7d (07-08..07-15) | avg ~1.0-1.1% most days; two conversion days avg ~9-10%; max 47-89% in windows | idle >90% of wall-clock |

**Pilot verdict:** exhibit A for the standard. Remediation (each at its natural touch, owner
0.6.2/AE coordination -- si2 is the 49F Schwab ingest box; NOTHING moves tonight):
1. CW agent install via SSM (S3-pulled script per Rule 12) -- first natural touch.
2. 30 days post-agent: full (b) review -- expected shape: RESCHEDULE (start/stop around the 4
   windows) and possibly RESIZE (t3.large CPU credits suit the profile; memory verdict needs (a)).
3. Manifest row gains the sec-3 fields at the same touch.

## 3. EC2_MANIFEST.json row schema additions (fill at provision / natural touch)

```json
"telemetry":     { "agent": "cloudwatch-agent", "installed_at": "YYYY-MM-DD", "namespace": "CWAgent" },
"duty_cycle":    "scheduled: 09:45,10:15,21:45,22:15Z" | "24x7",
"autoshutdown":  { "mode": "self-stop" | "scheduler-stop" | "24x7-exception", "reason": "<required for exception>" },
"sizing_review": { "last": "YYYY-MM-DD", "basis": "cpu avg/max %, mem max %, disk %, duty cycle, window", "verdict": "KEEP|RESIZE(<type>)|RESCHEDULE" }
```

Absent fields on an existing row = not yet touched (legal). Absent on a NEW row = the provision
violated this standard (gate candidate: manifest lint at safe-ec2-deploy time -- announce-then-
enforce; routes through CTO with the other Z1 gates).

## 4. Prior art + why

- consolidation-gold-runner (authored 2026-07-15, base 0.7.0): self-stop + scheduled start +
  absence alarm -- the reference implementation of (c) for new boxes.
- ADHC_TRIGMRK (phantom-consumer marker family): what the EC2<->trigger contract does without a
  standard -- the incident record behind axis D.
- The si2 numbers above: what "we have no idea what this box needs" looks like in data --
  right-sizing without telemetry is guessing with a purchase order.
