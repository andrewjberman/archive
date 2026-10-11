# IRPT_ANLREQ t1 -- AMENDMENT to the commentary pair: code-only re-apply of the commentary function onto the pull function's zip

Ordered by `1.0.0_SA_CTO~DELL2` msg 4178 (ruling on row `IRPT_ANLREQ-D2-S23`). Amends the pair of TO-APPLY-t1: COO half
`org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/NEVER_WIDEN_IRPT_ANLREQ_COO_HALF_COMMENTARY_STORE_AND_LAMBDA_20261009.md`, CTO half
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COMMENTARY_STORE_AND_LAMBDA_FIRST_APPLY_CTO_HALF.md`.

**Deployer:** `2.0.0_SA_COO~Y2`, IRPT_ANLREQ's interim driver (CTO msg 3904). The original COO half is `2.0.0_SA_COO~T2`'s; that seat now drives
NFRA_TRNSPT. **Applier:** `0.7.0_AE_CloudOps~DELL2`.

**COO half of this amendment: SIGNED by this file, 2026-10-11 ~05:4xZ.** CTO half: owed.

## 1. What happened

TO-APPLY-t1 steps A2 and B were applied tonight at pin `4901eece20`, which predates `fd74f984ac` (NFRA_TRNSPT TR-ra-22's source). The CTO's
precondition (msg 3939: re-read the shared zip before A2 and B) never reached the applier; that is this seat's defect, row
`IRPT_ANLREQ-D2-S23`. `commentary.tf:281` gives the function `filename = local.pull_zip`, the same local `pull.tf:112` and `mail_pull.tf:105` use.

## 2. The state, measured by this seat 2026-10-11 05:26Z-05:36Z (`get-function` on each named function; every zip downloaded and re-hashed)

| function | terraform | live CodeSha256 | LastModified | downloaded sha equals it |
|---|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `pull.tf:104` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | 2026-10-11T05:03:47Z | yes (886783 bytes, 89 members) |
| `outlook-global-commentary-draft-lambda` | `commentary.tf:275` | `plVgBIIXTNPVV/JtDADhavy/BgWQp+kRw6gcwpwHjyA=` | 2026-10-11T05:26:35Z | yes (877118 bytes, 88 members) |
| `outlook-global-transcripts-pull-lambda` | handler `mail_handler.lambda_handler`, so `mail_pull.tf` (INFERRED from the handler; the name was not resolved through the builder) | `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=` | 2026-10-07T23:59:05Z | not downloaded |

**The stack ran TWO zips before t1 and runs THREE now.** The mail function has been on a third digest since 2026-10-07; TR-ra-22 moved the pull
function only. This amendment moves the commentary function onto the pull's bytes. It does NOT move the mail function: that drift predates t1,
belongs to NFRA_TRNSPT, and is named here so the one-zip statement is not read as restored by this act.

Consumers of the commentary function: its event-source mapping is `Enabled` on `outlook-global-commentary-draft-analysis-ready-queue`, batch 1.
That nothing sends to that queue yet is the CTO's statement (msg 4178) and the order's preflight ("the trigger is I3, not created here"); this
seat did not read the queue's depth.

## 3. The packet the CTO asked for

**(a) Member diff, commentary zip (`plVgBIIX`) against pull zip (`AI4UQD0M`).** 88 against 89 members; table
`T1_ZIP_MEMBERS_PULL_VS_COMMENTARY_20261011.json` beside this file (sha256 prefix per member, both zips).
- only in the pull zip (1): `data/transcripts/scripts/teams/census.py`
- only in the commentary zip: none
- changed (8): `data/transcripts/scripts/teams/pull.py`, `data/transcripts/scripts/teams_chat/assist.py`,
  `data/transcripts/scripts/teams_chat/channel_mentions.py`, `data/transcripts/scripts/teams_chat/mail_requests.py`,
  `data/transcripts/scripts/teams_chat/tenant.py`, `infra/logic/registry/name_rulings.json`, `infra/logic/registry/scopes.json`,
  `lib/opal_naming.py`

So the pull's zip is ahead of the pin's by more than `fd74f984ac`: five handler-side modules, two registry files and the naming library moved.

**(b) Which changed members the commentary handler imports: NONE.** Static import closure from
`data/transcripts/scripts/commentary/lambda_handler.py`, computed on both extracted zips: 8 members each, the same 8 --
`commentary/__init__.py`, `classification.py`, `drafter.py`, `entry.py`, `lambda_handler.py`, `ticket_client.py`, `outlook/__init__.py`,
`outlook/slicer.py`. Plus ONE import by path that a static walk cannot see and this seat read by hand (`lambda_handler.py:143-166`):
`infra/aws/lambda/investor-reporting/_keys/keys.py`, loaded with `importlib.util.spec_from_file_location`; `keys.py` imports only
`__future__`, `hashlib`, `json`, `os`, `re` and reads `data/firm_registry.json`. Intersection of {8 changed, 1 added} with {those 9 code
members, `firm_registry.json`, and the package's two JSON files}: **0**. All of them are byte-equal across the two zips.
`lib/opal_naming.py` and the two changed registry files are packaged and are not imported or mentioned by any member of that closure.

**(c) Address equality for every key the function writes.** By equality of the PRODUCERS, not by evaluation:
- IRPT keys come from `keys.py` + `data/firm_registry.json`: `56ee3cc22e80` and `1d249de15ac4` in both zips.
- The queue it sends to (`COMMENTARY_READY_QUEUE_URL`, `lambda_handler.py:233-236`) and the two functions it invokes (the composition reader and
  the draft store, `:83`, `:114`) are named by ENVIRONMENT VARIABLES, which Terraform sets and a code-only apply does not touch.
- The draft itself is written by the store function (`irpt-commentary-draft-store-lambda`, `AsKY+KWL`), which this act does not touch.
No address was computed and compared; ABSENT != EXERCISED-AGAINST. Step 6's test invoke is the exercise.

## 4. The act

ONE targeted apply, `infra/aws/terraform/transcripts`, `-target=aws_lambda_function.commentary`, from the applier's existing detached worktree at
pin `4901eece20` (so every other argument of the resource is the one step B applied).
- **The bytes:** the pull function's own package, fetched with `get-function` and placed at `local.pull_zip`'s path in that worktree. NO rebuild.
  Before the plan: its sha256 equals `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, and the pull function's live CodeSha256 re-read equals it too
  (a pull function that moved since this read is a STOP). The pin's own zip (`plVgBIIX`) is kept beside it, untouched, as the rollback source.
- **Plan:** 0 to add, 1 to change, 0 to destroy; the one change is `aws_lambda_function.commentary` and its changed arguments are
  `source_code_hash` (and the computed attributes that follow it). Any other resource or argument is a STOP. Commit the plan text first.
- **Writers of the property (the commentary function's code): N = 1**, `aws_lambda_function.commentary` at `commentary.tf:275`
  (search of every `.tf` in `infra/aws/terraform/transcripts` for `pull_zip`: three resources use the local, one of them is this function).
- **Ledger:** the open entry `irpt-anlreq-t1-commentary-store-and-lambda-20261009` gains one leg for this act before the apply.

## 5. Both branches

- **Branch A:** live CodeSha256 == `AI4UQD0M...`, State Active, LastUpdateStatus Successful, targeted re-plan 0. Then step 5 (simulate) is re-read
  and step 6 (ONE test invoke) runs on those bytes, as the order has them.
- **Branch B:** the plan is not exactly the one change -> no apply. The apply errors -> read the function: a Lambda code update is atomic, so it
  reads either `plVgBIIX` (unchanged; stop and report) or `AI4UQD0M`. State not Active or LastUpdateStatus Failed -> re-apply the kept `plVgBIIX`
  zip through the same targeted path and report. No destroy on any branch: a destroy is Andrew's word (order step 7).
- This half does not predict which branch holds.

## 6. Not covered

The mail function's digest; any other resource of the root; any environment variable, IAM statement, queue or mapping; a rebuild at any pin.
