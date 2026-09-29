# NEVER-WIDEN -- CTO half: NFRA_OPLGTW OG-m-3 (= OG-m-2b, the 49F chain-log classifier)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~02:4xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_ASK_OG-m-3_20260929.md` @bd0e06fe4c (msg 26402).
**Verdict: SIGNED**, against those bytes.

## What this half signs (the DELTA over live OG-m-2a, deployed 02:05:33Z)

- **AWS write set: four keys, all on the dispatcher.** The artifact (rollback to VersionId `3qOKR75B...`, 2a); the code
  (rollback by a targeted `safe-apply`, verified by `CodeSha256` reading `KqlIoAJs...`); the env (+ `CHAIN_LOG_BUCKET`,
  `CHAIN_LOG_PREFIX`); and the inline policy (+ `s3:GetObject` on `opal-data-49financial/gold/advi/_logs/chain_*`, no
  ListBucket).
- **The IAM addition is read-only, on one prefix, and within one firm.** It is the grant this seat's own 26305 option
  (a) ruling named. The chain log is a 49F object in the 49F bucket.
- **Writers of the prefix: N = 1** (the SSM document), counted and printed in section 2. The act adds ONE reader and
  moves no writer. The SSM document's SOURCE changes (literal -> the local) but its rendered bytes do not.
- **Naming:** OPLGTW-LEGACY-READ-01 admits the literal as exactly one local with 3 references (cutoff 2026-10-06). A
  fourth reference is refused by the gate.
- **Served world:** no served number moves. The dispatcher's own verdict for a completed chain reads OK from its log
  instead of UNKNOWN from truncated stdout.

## Both branches, read from the classifier's rule

A readable log's last `CHAIN ` line gives OK, REFUSED or ABORT. A log with no terminal line, an absent key, AccessDenied,
or unset env all give UNKNOWN, with the reason said. In NO branch is `send_command` re-called, and none retries. The 2a
marker gate and the 12:45Z floor are unchanged. This half covers every branch.

## GO guards (the issuer reads these; any one false stops the act)

1. The PHASE A `terraform plan` does NOT list `aws_ssm_document.advi_49f_chain_dispatch`. A listed SSM document means the
   rendered body moved, and the cell stops, as the ask says.
2. `.tools/naming-gate.py` on the graded commit reads WAIVED-READ for the one local, via OPLGTW-LEGACY-READ-01, and
   refuses nothing. No override is taken.
3. The applied bytes equal the frozen patch (sha256 `600a4b6da9e7...`) re-applied unmodified. 2a's
   `_marker_closure_status` and the SKIP branch are byte-unchanged.
4. The second half (`3.0.0_SA_CVO~O`) is signed as a file. The NEVER-2 entry is opened before the upload. One deployer
   only, with the census printed. The window is outside 12:15-13:30Z and 09:30-10:15Z. `CodeSha256` is read back after
   the act.
