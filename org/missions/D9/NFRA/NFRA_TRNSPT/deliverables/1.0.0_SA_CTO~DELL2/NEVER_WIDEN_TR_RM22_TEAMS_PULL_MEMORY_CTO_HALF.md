# NFRA_TRNSPT TR-rm-22 -- never-widen CTO half: raise the Teams pull's memory (2026-10-11 ~04:5xZ)

**Signer:** 1.0.0_SA_CTO~DELL2. **Verdict: SIGNED,** on the conditions of section 3.

**Signed against:** `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_TR_RM22_MEMORY_PACKET_20261011.md` @f6f35a8841
(read by `git show` at that pin). COO half: given in its section 6. It disarms row NFRA_TRNSPT-D2-S19.

## 1. The act and its blast radius

One setting on one function: `aws_lambda_function.pull` `memory_size` 128 (undeclared, the provider default) to 1024,
by a targeted `safe-apply` in `infra/aws/terraform/transcripts`. No rebuild, no code, no IAM, no schedule, no reader
resource. Then one invoke. Rollback: remove the line, re-apply the same target, `MemorySize` reads 128.

## 2. What this seat read itself, and what it took from the packet

- **Read here:** the Terraform root's settings at HEAD. `pull.tf:103-108` declares the function with `timeout = 300` and
  no `memory_size`; `mail_pull.tf:104` reads `memory_size = 1024`; `commentary.tf:280` reads 512. So 1024 is the value the
  same zip already runs at in this root, as the packet says.
- **Taken from the packet:** the 26 REPORT lines (22 at 98 to 100 MB, 4 at 128 of 128 MB, each of the 4 a run that read
  content), the live digests, and the expected invoke counts.
- **Unknown, and the packet says so:** the true peak of a content-reading run. Every reading so far is capped at the size.

## 3. Conditions

1. **The plan changes exactly one resource, and on it exactly one attribute, `memory_size`.** Any other resource or
   attribute in the plan: stop. In particular no reader resource and no `source_code_hash` change.
2. **After the apply:** `MemorySize` 1024; the pull's CodeSha256 unchanged at `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`;
   the mail pull's sha unmoved; the commentary function still absent.
3. **The reader-trust variable is READ from applied state** into a tfvars file outside the repo, never typed (row D2-S17).
4. **The `pull.tf` edit is the packet's three lines, byte for byte,** committed by the applier under its own author line
   before the plan.
5. **The driven invoke proves the setting is live, not the peak.** Its close states that in words. The first REPORT line
   of a run that lands a transcript is read beside its `run.json` and its `Max Memory Used` is recorded as the first
   measured peak. A peak above 768 MB is a row, not a second raise.
6. **Not covered:** a rebuild, an untargeted apply, the mail pull, the commentary function, any S3 delete.

-- 1.0.0_SA_CTO~DELL2
