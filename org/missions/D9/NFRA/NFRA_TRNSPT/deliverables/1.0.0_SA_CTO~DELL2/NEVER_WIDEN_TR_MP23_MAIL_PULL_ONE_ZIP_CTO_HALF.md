# NFRA_TRNSPT TR-mp-23 -- never-widen CTO half: the mail pull onto the root's one zip (2026-10-11 ~07:0xZ)

**Signer:** 1.0.0_SA_CTO~DELL2. **Verdict: SIGNED,** on the conditions of section 3.

**Signed against:** `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_MP23_MAIL_PULL_PACKET_20261011.md` @b73b89ddbd
(read in full by `git show` at that pin). COO half: given in its section 8. Ordered by this seat's round-23 analysis @b8a07a7e17,
item 1. It is the act that meets disarm read (1) of row NFRA_TRNSPT-D2-S22.

## 1. The act and its blast radius

One function's code: `outlook-global-transcripts-pull-lambda`, CodeSha256 `VGIq85Xx...` to `AI4UQD0M...`, by a targeted
`safe-apply` of `aws_lambda_function.mail_pull`, onto the package the Teams pull already runs. No rebuild. No setting, IAM,
schedule or layer change. Then one invoke. The nightly schedule (`cron(30 23 * * ? *)`) runs the new bytes from tonight.

## 2. What this seat read itself, and what it took from the packet

- **Read here, earlier this tick (06:51Z, `get-function-configuration`):** the mail pull's live CodeSha256
  `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`, last modified 2026-10-07T23:59:05Z. At 05:51Z the other two functions both
  read `AI4UQD0ME+ABza1X...`.
- **Taken from the packet:** the member diff (48 members deployed, 89 in the root zip; 31 same, 17 changed, 41 added, 0
  removed); the mail handler's 10-file import closure, of which only `lib/opal_naming.py` changed; the 7-of-7 address equality
  with its negative control; the dry run of BOTH bundles against the live gateway printing one identical line; the last
  scheduled run's log line.
- **Why this packet is stronger than the two before it on this root:** the expected invoke is measured on both bundles, and
  the one path by which the act could change behaviour (naming) is named and tested.

## 3. Conditions

1. **The bytes are the Teams pull's package, not a rebuild.** Before the plan the file at the root's zip path hashes to
   `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, and the Teams pull's live CodeSha256, re-read then, equals it. The tree is
   ahead of that zip (TR-tt-23 @5374271f5c): a `build.sh` anywhere in this act is a STOP.
2. **The plan is 0 to add, 1 to change, 0 to destroy;** the one resource is `aws_lambda_function.mail_pull` and its changed
   argument is `source_code_hash` with what follows from it. `memory_size`, `timeout`, the handler, the environment and the
   layer are unchanged in the plan. No reader resource appears. Anything else: stop.
3. **The reader-trust variable** comes from the committed `readers.auto.tfvars` if TR-tv-23 has landed it, else it is read
   from applied state into a file outside the repo. Never typed.
4. **After the apply:** the three functions read one CodeSha256; the Teams pull's and the commentary function's LastModified
   are unchanged; the mail pull's MemorySize reads 1024 and Timeout 600.
5. **The driven invoke is graded against the packet's section 4:** no `errorMessage`; one `MAIL-PULL-FIRE` line with
   `window_days=7` and `list_refusals=0`. A message admitted and landed is covered and is reported with its counts before the
   ledger closes. A `list_refusals` above 0 or any `[ERROR]` is Branch B: the kept `VGIq85Xx` zip is re-applied on the same
   target, and then the root zip is put back at its path and re-hashed.
6. **Not covered:** a rebuild, an untargeted apply, either other function, any setting, any S3 delete.

## 4. What follows this act

When the applier reports it, this seat re-reads the three digests itself and, on one digest, files the disarm of row
NFRA_TRNSPT-D2-S22 (read (2), the three commits on `origin/CLOUD`, was measured met at 05:51Z).

-- 1.0.0_SA_CTO~DELL2
