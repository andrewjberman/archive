# MDPF_TAXSMA.TO-TX-g-2 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~1` · **cell** `TX-g-2` (PRD surface S18, FWD-7) · **branch**
`wk-mdpf_taxsma-1-1g2` in `C:/tmp/wk-taxsma-1g2` · **cut base** `2aa1e26cbf` (this cell adds no commit
before this record; the probe and this record are the whole write). **Spec:** the PRD @671925aecc, the
decomposition @7f65001ab3 s.3 (`TX-g-2` acceptance) and `infra/aws/ec2/EC2_MANIFEST.json`'s
`services.opal-gateway` row.

The cell as issued: "the Gateway package carries the module. No deploy. A change to the deploy script is
made only if it does not already bundle the new module." Every value below names its instrument, the UTC
time it was measured and its denominator.

## 1. What was found and what was (not) written

| Question | Answer | Instrument |
|---|---|---|
| Registered deploy path for `opal-gateway` | `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` | `EC2_MANIFEST.json` `services.opal-gateway.deploy_script`, read 2026-09-21T03:0xZ |
| Does the builder already bundle `app/` whole? | Yes -- `tar -czf ... -C "$SRC" --exclude=... app deploy requirements.txt identity_tool_allowlist.txt`; `app` is one bare directory member, no `--exclude` names `app`, `app/*` or `taxsma_workbook.py` | static read of `deploy-to-ec2.sh`'s tar invocation, TXG2-AC2 |
| Does the built package therefore already contain `app/taxsma_workbook.py`? | Yes, byte-identical to the source (SHA-256 `8d63bc5685a156922225b08d45df3aae67a22df4a5054be3aa02a34ea08740b5`, 3-way agreement: inside the built tarball, `sha256sum` in the same bash arm, and `hashlib.sha256` read independently in Python) | TXG2-AC1, run against the registered script's own bytes |
| Was `deploy-to-ec2.sh` edited? | No | `git status --porcelain` and `git diff --stat HEAD` on the file, both empty, TXG2-AC2 |
| Was `EC2_MANIFEST.json` (or its `deployed_commit`) edited? | No | `git diff HEAD -- infra/aws/ec2/EC2_MANIFEST.json`, empty, TXG2-AC3 |
| Did any AWS SSM send-command or S3 put occur? | No -- 0 of 8 logged commands across the whole cell (2 `git status`, 1 `git diff --stat`, 1 `git status`, 1 `git diff`, 1 bash build-fragment run, plus AC4's own pre-population when run standalone) name `ssm send-command`, `s3 cp` or `s3api put-object` | `command_log.jsonl`, TXG2-AC4 |

**Disposition: TXG2-AC2 (the `<paths>` grant, `GW/deploy-to-ec2.sh`) is VERIFY-REUSE.** The cell writes no file
under `infra/aws/ec2/opal-gateway/` and makes no Gateway deploy, no SSM send-command and no S3 put, per the
order's bounds.

## 2. Criteria -- 4 of 4 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-1g2 && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~1/probes/tx_g_2.py AC<n>`,
each a fresh process, run in AC1/AC2/AC3/AC4 order at HEAD `2aa1e26cbf` with `deploy-to-ec2.sh` and
`EC2_MANIFEST.json` 0 of 2 dirty vs HEAD throughout, 2026-09-21T03:0xZ. Each run prints its measurement, its
denominator and exactly one `VERDICT:` line; rc 0 on all four.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | package built from the registered script's own instance-id..built-artifact bytes contains `app/taxsma_workbook.py`; SHA-256 equal on all 3 independent reads (built, bash `sha256sum` of source, Python `hashlib`) | member list 84 of 84 printed; 0 SHA-256 mismatches |
| AC2 | `app` bundled whole (no per-file enumeration), 0 of 8 excludes target the app dir or the module; `deploy-to-ec2.sh` diff-empty vs HEAD | 8 excludes checked, 4 members checked |
| AC3 | `services.opal-gateway.deploy_script` = `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (stated, not edited); `deployed_commit` diff-empty vs HEAD | 1 row read, 1 file diffed |
| AC4 | 0 of N logged commands (N = 5 on a run that inherits AC1-AC3's log, N = 8 when AC4 self-populates) name an SSM send-command or an S3 put | every `command_log.jsonl` entry scanned, denominator printed each run |

**Controls.** INDEPENDENT INSTRUMENT (AC1): the built package's SHA-256 is checked three ways in the same run
(inside the tarball via a second `sha256sum` on the extracted member, and again in Python via `hashlib.sha256`
reading the source file directly) -- all three agree. NEGATIVE CONTROL (AC2): the static check is written to
FAIL if any exclude equalled `app`, `app/*`, `app/**` or the module's basename or contained `taxsma_workbook`;
none of the script's 8 real excludes (`.env`, `audit.jsonl`, `*.log`, `__pycache__`, `.token_cache`, `infra`,
`dev_smoke.py`, `make_diagram.py`) do, and the check was exercised against a first draft that DID flag two
unrelated top-level `.py` excludes as false positives (fixed before this run; see probe docstring/comments).
BELT-AND-SUSPENDERS (AC1/AC4): the extracted build fragment is scanned for the three forbidden verbs BEFORE it
is executed (it would refuse to run rather than execute an SSM/S3 call), and again AFTER via the command log.

## 3. What this cell did not do

No AWS call of any kind was made (the registered script's own `aws ec2 describe-instances` fallback never
executes here because `EC2_MANIFEST.json` already carries a live `instance_id` for `opal-gateway`, so the
build-only fragment never reaches that branch). No Gateway deploy, no `safe-ec2-deploy.sh` invocation, no
change-management ledger entry was opened (none was needed: no world-changing act occurred). No file changed
under `infra/aws/ec2/opal-gateway/` or `infra/aws/ec2/EC2_MANIFEST.json`.

## 4. Surprises filed

`MDPF_TAXSMA-W1-S4` -- the registered build already bundles a tracked runtime telemetry file
(`app/org/mcp/agent_telemetry/0.7.0_AE_CloudOps.jsonl`) into every Gateway deploy artifact via the same `app`
whole-directory tar member that carries `taxsma_workbook.py`; pre-existing, orthogonal to this cell, filed as
an OBSERVATION for NFRA_OPLGTW / the box owner.
