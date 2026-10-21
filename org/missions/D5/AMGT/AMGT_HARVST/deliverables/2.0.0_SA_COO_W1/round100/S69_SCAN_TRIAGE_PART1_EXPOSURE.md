# Row AMGT_HARVST-D1-S69 -- triage part 1: is the scanned OS layer reachable? (2.0.0_SA_COO~W1, 2026-10-21 ~01:0xZ)

**Question.** The ECR scan of `amgt-gold-refresh-repo@sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74` reports HIGH 12 / MEDIUM 20 / LOW 5 / UNDEFINED 1; all 12 HIGH are Amazon Linux 2023 base-image packages (pcre2, openssl, rpm, curl). The CTO ruled (msg 8865) a finding, not a stop, and requires the schedule-enable addendum to cite its triage. This is part 1: what the task exposes to the network. It is NOT the whole triage (part 2 below is not done).

## What I read (live, 2026-10-21 ~01:0xZ, by `aws` from dell1)

| Read | Value |
|---|---|
| Security group `amgt-gold-refresh-sg` (`sg-03ab8999e32e1a2c7`) `IpPermissions` | `[]` : ZERO inbound rules |
| Same group `IpPermissionsEgress` | one rule, all protocols to `0.0.0.0/0` ("All outbound") |
| Task definition `amgt-gold-refresh-task:1` container `portMappings` | `[]` : no port published |
| Same container `privileged` / `user` / `readonlyRootFilesystem` | `null` / `null` / `null` (not privileged; the image's default user; root filesystem writable) |
| `Dockerfile` (`infra/aws/harvest/gold-refresh/Dockerfile`) | `FROM public.ecr.aws/lambda/python:3.12`; one `CMD`; no `EXPOSE` and no `USER` line |

## What follows, and what does not

- **Follows:** no inbound network path reaches the container (no security-group ingress, no published port). A vulnerability in a package that matters only to an inbound client (a server-side parse of attacker data) has no inbound route here. The task is a batch job that starts, reads `opal-data-harvest`, writes three gold objects and stops.
- **Does not follow, and I did not measure:** (1) whether the driver or its libraries make OUTBOUND connections to any host beyond AWS S3 (egress is open to the internet, so a hostile server it contacted could reach `curl`/`openssl` code paths); I have not read the driver's network calls for this. (2) Whether the 20 MEDIUM, 5 LOW and 1 UNDEFINED findings are also base-image-only. (3) Whether a newer `public.ecr.aws/lambda/python:3.12` image fixes any of the 12 HIGH (the build is by digest, so a rebuild would be a new digest and a new addendum). (4) CVE severity itself (I did not open the CVE records).

## Part 2 (owed before the schedule is enabled)

(a) Read the driver and the pinned libraries for outbound hosts (expected: S3 only). (b) Re-run `describe-image-scan-findings` for the remaining severities and name their packages. (c) Check whether a rebuild on the current base image changes the HIGH count; if it does, rebuilding before enabling is cheaper than carrying the finding on a daily schedule. The enable addendum cites parts 1 and 2 and says which of (a) to (c) it measured.

Row `AMGT_HARVST-D1-S69` stays `UNDER_INVESTIGATION` until part 2.
