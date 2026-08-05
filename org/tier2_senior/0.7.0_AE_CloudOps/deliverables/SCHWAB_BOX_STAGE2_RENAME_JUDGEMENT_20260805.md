# Stage 2 judgement: should we rename the Schwab Box's IAM role / instance profile / SG / key pair?

**Author:** `0.7.0_AE_CloudOps~C` · **2026-08-05** · **Requested by:** `1.0.0_SA_CTO~B` (edict 20260805T210232Z)
**Subject:** EC2 `i-0f3d57a97f14727af` -- the Schwab Box. Sole live ingest for ADVI (08335338) + MDPF (08242234).
**Asked of me:** deliver a JUDGEMENT, not a migration. Do not begin Stage 2.

> **RECOMMENDATION: DO NOT DO STAGE 2.** The residual risk is real but it is **not** what a rename
> fixes, and I found the specific mechanism that carries it. There is a targeted control that costs
> minutes and addresses the actual exposure directly. **Rename: NO. Targeted control: YES, and it
> should happen regardless of what Andrew rules on the Name tag.**

---

## 1. What real risk remains after Stage 1 -- stated concretely, per the bar CTO~B set

CTO~B's bar, verbatim: *"'The role is still called spike' is only a finding if you can name who is
misled by it and what they would do -- an IAM role name is not read by a cleanup sweep the way a Name
tag is."*

That bar is correct, and on the IAM role name specifically **the finding FAILS it.** I could not find
any sweep, automation, script, or policy that resolves this box by its role name. The role name is
inert: it is referenced literally, in places that would break loudly and immediately if it changed.

**But the bar is MET by a different resource, and I can name the file.**

`infra/aws/nfra_terraform_p1/consolidated_gaps.json` -- the Terraform-adoption gap census -- carries
three entries:

```json
{"group":"ec2_network","name":"quartz-si2-spike [running]","type":"aws_instance",
 "firm":"shared","class":"UNMANAGED","module":null,"exempt_reason":""}
{"group":"ec2_network","name":"quartz-si2-spike-sg [quartz-si2-spike-sg]","type":"aws_security_group",
 "firm":"shared","class":"UNMANAGED","module":null,"exempt_reason":""}
{"group":"ec2_network","name":"quartz-si2-spike-key","type":"aws_key_pair",
 "firm":"shared","class":"UNMANAGED","module":null,"exempt_reason":""}
```

**WHO IS MISLED:** an agent working the NFRA Terraform-adoption backlog.
**WHAT THEY WOULD DO:** exactly what the census asks -- bring three `UNMANAGED` resources under
Terraform. `exempt_reason` is **EMPTY**, so nothing on that record says "do not touch this."
**WHAT THAT COSTS:** importing or (worse) replacing the SG / key pair / instance of a box holding a
**human-established standing SDD session and a refresh token in Administrator's Windows Credential
Manager vault.** A replacement does not merely restart a service -- it destroys a credential that
requires a human at a console to re-establish, and takes both 49F Portal products down until they do.

**This is a strictly worse exposure than the Name tag**, because the Name tag at least *looks* like a
label to a human, whereas this record is a **worklist with an empty exemption field**, and working it
is the correct behaviour for the agent who picks it up.

**And -- critically -- STAGE 2 DOES NOT FIX IT.** Renaming the resources to `canonical-schwab-si2-*`
leaves three entries still classed `UNMANAGED` with a still-empty `exempt_reason`. The census keys on
management status, not on the name. **Stage 2 would spend a live-production migration and change
nothing about the one mechanism that can actually take the box down.**

---

## 2. What Stage 2 would actually cost

| Resource | Rename mechanism | Cost |
|---|---|---|
| `quartz-si2-spike-role` (IAM role) | **Cannot be renamed.** Create new + migrate. | New role, replicate 11 statements incl. the resource-scoped monolith-write + backfill grants + the bd/cot/inf Deny planes, re-attach `AmazonSSMManagedInstanceCore`, swap the instance profile on a **running** instance. |
| `quartz-si2-spike-profile` (instance profile) | **Immutable name.** Create new + associate. | Profile swap on a live instance; SSM connectivity depends on it. A botched swap silently breaks the SSM path the daily pulls ride. |
| `quartz-si2-spike-sg` (security group) | **Immutable name.** Create new + attach. | New SG must exactly reproduce the RDP-scoped-to-Andrew-IP rule; a gap here is a security regression, not an outage. |
| `quartz-si2-spike-key` (key pair) | **Immutable name.** New key. | The key pair is **baked into the instance at launch.** A "new key pair" does not re-key a running instance -- practically this means losing the documented break-glass path or replacing the box. |
| `quartz-si2-backfill-08335338` (policy) | Renameable, low value | Cosmetic. |

**Windows to avoid:** four live pull windows daily -- `cron(45 9,21)` for 08335338 and
`cron(15 10,22)` for 08242234 -- all verified ENABLED today.

**The load-bearing cost is not any single step; it is that every one of them operates on the sole
live producer for two Portal products, to change strings, with no functional gain.** The estate's own
archetype doc already rules on the risk posture here: *"Essential infrastructure. Never
retired/stopped/repointed-away"* (`data/assets/docs/SCHWAB_BOX_ARCHETYPE.md:33`), and it explicitly
warns that a code deploy on this box *"must not disturb the box's standing session -- a code deploy
is a file replace, never a re-image/reboot of a box holding a fragile human-established session."*
A role/profile/SG/key migration is a far heavier act than the code deploy that warning is about.

---

## 3. Recommendation

**DON'T.** Three reasons, in order of weight:

1. **It does not fix the real exposure.** The genuine "someone acts on a misleading record" path is
   the gap census's empty `exempt_reason`, and renaming leaves that untouched. Doing Stage 2 and
   believing the risk closed would be *worse than doing nothing*, because it converts a live hazard
   into one everybody thinks is handled.
2. **The IAM role name fails CTO~B's own test.** Nothing reads it. It is cited literally in places
   that break loudly. "Untidy" is not a finding.
3. **The cost is paid on the sole live ingest for ADVI + MDPF, and the key pair leg cannot be done
   properly at all** without replacing the box -- which is the one thing the archetype forbids.

### Do this instead (cheap, targeted, addresses the actual mechanism)

**(a) Populate `exempt_reason` on the three gap-census entries** -- e.g. *"Schwab Box: essential
persistent infrastructure holding a human-established SDD session; deliberately NOT under TF
lifecycle management (IAM only). See data/assets/docs/SCHWAB_BOX_ARCHETYPE.md. Do not import,
replace, or re-key."* This is the whole fix for the mechanism I found, and it is a data edit.
**Not mine to make** -- that census belongs to the NFRA Terraform-adoption workstream; routed to CTO.

**(b) Andrew's Name-tag ruling** (pending, held) -- addresses the human-reading-a-tag path.

**(c) Drop `reversible=true`** -- authorized, pending only the mechanism question (the box is not
TF-managed, so there is no Terraform path to its tags without importing it -- which is precisely
the act (a) is meant to prevent). **Note the shape here: the ban on ad-hoc CLI mutation and the ban
on importing this box point in opposite directions for this one edit.** That tension is real and is
CTO~B's to resolve; it is not something I should quietly pick a side of.

**(d) Leave the legacy resource ids alone and say so in writing** -- the archetype doc already
established the pattern of citing legacy ids literally while calling the *device* by its true name
(`SCHWAB_BOX_ARCHETYPE.md:33`). That is the right resolution: **the identifiers are historical
artifacts; the DEVICE has a true name. Making the record say so costs nothing and breaks nothing.**

---

## 4. What I did not do

I did not stage, plan, import, or create any resource for Stage 2. No Terraform was run against the
si2 box. This document is analysis only, per the edict: *"a held item that quietly becomes work is
how a scoped authorization widens itself."*

**Grounding:** live `describe-instances` / `describe-rule` / `list-targets-by-rule` (2026-08-05),
`consolidated_gaps.json` gaps[67]/[69]/[86], `SCHWAB_BOX_ARCHETYPE.md`, `EC2_MANIFEST.json:501-517`,
`monolith-daily-schedule.tf:56,175`, `canonical-schwab-si2-schedule/main.tf:55`. The claim "nothing
resolves the box by its ROLE name" is a **negative over the repo + the applied EventBridge/SSM target
payloads**; it is bounded by what I searched (216 matches / 84 files / 22,354 files scanned for
`quartz-si2`, plus applied target inspection) and is not a proof of universal absence.
