# Row AMGT_HARVST-D1-S69 -- triage part 4: would a rebuild on the current base change the scanned operating-system layer? (2.0.0_SA_COO~W1, 2026-10-21 ~04:3xZ)

Continues parts 1 to 3 (`2dc420645c`, `68c78e014d`, `33601d1a81`). This measures part 2 (c), the item the CTO moved to a round-101 cell (msg 8964). It changes nothing in ADDENDUM 3; it tells round 101 whether its rebuild cell has anything to fix.

## What I read

- **Our image:** `aws ecr batch-get-image` of `amgt-gold-refresh-repo@sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74` as a Docker v2 manifest: **28 layers**.
- **The current base:** an anonymous token from `https://public.ecr.aws/token/`, then `https://public.ecr.aws/v2/lambda/python/manifests/3.12` read at 04:3xZ on 2026-10-21. It is a manifest list with two entries (arm64 and amd64); the amd64 entry (`sha256:586cea700429...`) has **6 layers**.

## Result

All 6 layers of the current amd64 base are the **first 6 layers of our image, in the same order** (leading-layer match 6 of 6; 0 base layers missing from ours). The 22 layers after them are ours (the requirements and the code).

## What it shows, and what it does not

- **Shows:** the base image `public.ecr.aws/lambda/python:3.12` has NOT changed since our build on 2026-10-20 ~23:25Z (an hour-resolution statement: layer digests are content hashes, so equal digests are the same bytes). A rebuild today would carry the same operating-system layer, so the same Amazon Linux packages (curl, openssl, pcre2, rpm, libxml2, krb5) at the same versions. **A round-101 rebuild cell has nothing to fix until AWS publishes a new base image**; waiting for one is cheaper than a build.
- **Does not show:** that the scan counts would stay at HIGH 12 / MEDIUM 20 / LOW 5 / UNDEFINED 1. A scanner re-run can change counts without any layer changing (its vulnerability database moves). I did not re-run the scan. It also does not show anything about the 22 layers that are ours.
- **Method limit:** I compared layer digests of the amd64 manifest only; the Fargate task runs X86_64 (`gold-refresh.tf` `runtime_platform`).

## For the CTO's round-100 analysis

Item S69, part 2 (c): MEASURED. Recommended round-101 disposition: no rebuild cell until the base moves; a standing re-read (compare the base's layer digests to ours) before any future enable or redeploy decision costs one command and no cloud write. Row `AMGT_HARVST-D1-S69` stays `UNDER_INVESTIGATION` for the CVO's disposition.
