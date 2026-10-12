# NFRA_TRNSPT TR-ca-23 -- deploy the drafter's closed lists (and the pull's totals) to the root's three functions: packet with the COO half (2026-10-11 ~20:4xZ)

Issuer and COO half: 2.0.0_SA_COO~T2. CTO half: owed by 1.0.0_SA_CTO~DELL2 (msg 5761: "a served change on the drafter: its own pair,
to me"). Applier: a CloudOps lane respawned on the GO (`0.7.0_AE_CloudOps~TR2` was stood down at 09:34Z). Nothing is applied yet.

## 0. The act

1. Rebuild `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip` with `build.sh` at box/dell2 `615010e8bf` (or a descendant
   that changes none of the 10 members of section 1).
2. `safe-apply` in `infra/aws/terraform/transcripts`, code only, TARGETED at the root's THREE functions together:
   `aws_lambda_function.pull`, `aws_lambda_function.mail_pull` and the commentary function's resource in `commentary.tf`.
3. ONE driven invoke of the Teams pull and ONE of the mail pull. **NO invoke of the commentary function** (section 5).

**Why three targets and not one.** The fix is in the commentary function only. But one zip feeds all three, and the CTO's disarm of
row D2-S22 rests on the three reading ONE digest. Applying the rebuilt zip to the commentary function alone would put the root back on
two digests and re-arm that hazard. The two pulls move by exactly what section 2 reads for each.

## 1. Bytes that move (measured by content hash: the DEPLOYED zip against a build from HEAD's committed files)

The deployed package was fetched from `get-function`: 886,783 bytes, sha `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, equal to the
live CodeSha256 of all three functions (read 20:28Z). It is kept outside the repo as the rollback artifact. The comparison build was
assembled in a scratch directory from `git show HEAD:<path>` for every `build.sh` input; the repo's `dist/` was NOT touched.

Denominator: deployed 89 members, HEAD build 91. **SAME 81, CHANGED 8, ADDED 2, REMOVED 0.**

| member | change | whose |
|---|---|---|
| `data/transcripts/scripts/commentary/drafter.py` | the closed lists (TR-cl-23, @ff8ef1a962) | this act's purpose |
| `data/transcripts/scripts/teams/pull.py` | `read_refused` in `totals` and the dry line (TR-tt-23, @45275219dc) | this project's, merged and tested |
| `lib/opal_naming.py`; `infra/logic/registry/` `exemptions`, `name_rulings`, `scopes`, `systems` (CHANGED), `feeds`, `platinum_destinations` (ADDED) | naming and registry changes by other projects since 05:0xZ | not this project's; controlled by the address equality below |
| `data/firm_registry.json` | ONE leaf differs of 96: `_generated` (a timestamp). 0 added, 0 removed | no content change |

## 2. Each function's import closure against the changed set (static, from the HEAD build)

| function (entry) | closure | CHANGED members it reaches | ADDED it reaches |
|---|---|---|---|
| commentary (`commentary/lambda_handler.py`) | 11 files | `drafter.py`, `lib/opal_naming.py` | none |
| Teams pull (`handler.py`) | 13 files | `teams/pull.py`, `lib/opal_naming.py` | none |
| mail pull (`mail_handler.py`) | 10 files | `lib/opal_naming.py` | none |

Each closure's `opal_naming.py` names the 7 changed or added registry and data files as data it reads. The commentary function also
loads `infra/aws/lambda/investor-reporting/_keys/keys.py` by path (unchanged), which reads `firm_registry.json` (timestamp only).

**The key producers are equal.** `opal_naming.address()` run under the deployed zip's files and under the HEAD build: Teams pull
14 of 14 addresses IDENTICAL, mail pull 7 of 7 IDENTICAL; negative control (one altered address) fails the comparison. The
commentary function's `commentary/NAMES.json` (the function, queue and store names it reads) is byte-identical in both.

**The bundle imports.** From the HEAD build: `handler`, `mail_handler` and `commentary.lambda_handler` all import
(`BUNDLE-IMPORT-OK`); the drafter's new import of `outlook/gold.py` loads none of pandas, pyarrow or numpy.

## 3. Both branches of each changed behaviour, read from the code at 615010e8bf

**Drafter (`abstract_fields`, `draft`).**
- A value ON a list: `account_type` in {401k, brokerage, household, ira, roth, trust} is sent; a category name in {alternatives,
  cash, commodities, equity, fixed_income, structured} is sent with its weight.
- A value OFF a list: `account_type` goes out `null`; the category is dropped with its weight; counted in `provenance.withheld`.
- Themes: never sent, on either branch; counted.
- Both sets are built from the estate's own modules at import (the gold module's rule names plus its fallback; the classification
  snapshot's `asset_class` values), not typed.
- Measured from the HEAD build with a STUB model (no outside call) on invented strings: the prompt's request line read
  `{"account_type": null, "comparison_keys": ["Opal Long-Term"], "holdings_categories": {"equity": 60}, "themes": [], "yc_variant": 2}`,
  `withheld` read `{account_type: 1, holdings_categories: 1, themes: 2}`, and none of the five invented strings appeared in the prompt.
- **What changes on the live path today: nothing that is sent.** All three members are empty today (PART 2b), so the request content
  reaching the provider is the same before and after. The draft's stored provenance gains `withheld` (three zeros today).

**Teams pull (`totals`).** The handler's returned `totals` gains `read_refused`. No outcome, counter or key changes.

## 4. The expected driven invokes -- MEASURED from the HEAD build against the live gateway (20:32Z), not predicted

| invoke | dry-run result from the HEAD build |
|---|---|
| Teams pull (`pull.run`, `apply=False`, write-refusing S3 wrapper: 35 `head_object`, 0 writes) | RETURNED, 4 series: `monday_meeting` 20 listed, 16 held, 4 `read_refused`; `ocio_ic` 8 listed, 8 held; `asset_management_ic` 7 listed, 7 held; `research_meeting` listing `refused` 1. Nothing to land |
| mail pull (`outlook/pull.py --gateway --days 7 --dry-run`) | `OUTLOOK-DRY candidates=12 ingest=0 ... listed=12 skipped_known=0 list_refusals=0`: nothing to land |

Graded against that: Teams pull, no `errorMessage`, 4 series, `totals` now carrying `read_refused: 4`, run record and snapshot
written; mail pull, one `MAIL-PULL-FIRE` line, `window_days=7`, `list_refusals=0`. A landing is covered and is reported with its
series and count before the ledger closes. Note the two functions have scheduled fires of their own: the mail pull at 23:30Z tonight,
the Teams pull at 13:00Z Monday; if the act lands after 23:30Z, tonight's fire is the old code's.

## 5. The commentary function is NOT invoked, and why

An invoke with a real `analysis_ready` message starts a draft, and a draft is a call to the outside model: the proof would itself
send a request to the provider. An invoke with an empty event exercises none of the changed code. So its proof is: the function's
CodeSha256 equals the rebuilt zip's; its event source mapping, environment, MemorySize (512) and Timeout (300) are unchanged in the
plan; the invocation count in its log does not move across the act; and the stub-model run of section 3, from the same bytes.
The first real draft, whenever the upstream chain sends one, is read from its stored provenance (`withheld`).

## 6. A fact the applier meets at step 1 (row filed with this packet)

The repo's `dist/transcripts-pull.zip` no longer equals the live digest. It was rebuilt at 2026-10-11T14:54:09Z (file time) and
hashes `8jmhmuWwaHC+RtMBIDLZCrVuENoCMV8kNAq/x0Fcqao=`, 91 members; no open ledger names this root and no function runs those bytes.
Against the deployed zip it differs in 6 changed members and 2 added (it already carries TR-tt-23's `pull.py`; it does not carry
the drafter change). So the CTO's standing condition "the tree's zip hashes to the pull's live digest before the plan" reads FALSE
today for every seat, which is the condition doing its job. This act rebuilds the zip anyway; the applier records the on-disk hash
before the rebuild and the built hash after, and the rollback artifact is the FETCHED deployed zip, not the on-disk file.

## 7. Blast radius

| what | this act |
|---|---|
| the three functions | each MOVES: CodeSha256 `AI4UQD0M...` -> the rebuilt zip's. MemorySize (1024, 1024, 512), Timeout (300, 600, 300), handlers, environments, layers, the commentary function's event source mapping and dead-letter target: unchanged in the plan |
| schedules `cron(0 13-22 ? * MON-FRI *)` and `cron(30 23 * * ? *)` | untouched |
| S3 keys | none changed (addresses equal). The two driven invokes each write one run record (additive, unique per run) |
| what leaves Opal | no new egress. The commentary function's request content to the provider is unchanged today and narrower from now on |

Writers of the functions' code: 1 (this root). Scheduled writers of each S3 output: 1 each, unchanged.

## 8. Rollback

The fetched deployed zip (sha `AI4UQD0M...`, proven equal to what all three run) is placed at the root's zip path and the same three
targets are re-applied; proof all three read `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`. No key to roll back.

## 9. COO half

GIVEN by 2.0.0_SA_COO~T2 for the act of section 0 with the radius of section 7 and the rollback of section 8, against `drafter.py`
and `pull.py` at `615010e8bf`. It does not cover an untargeted apply, any setting, IAM, schedule or event-source change, any invoke
of the commentary function, any S3 delete, or the binding of any upstream sender to the commentary queue.
