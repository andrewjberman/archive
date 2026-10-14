# Never-widen half (CVO) -- COMM_ASSIST round 17, cell CA-i-12: the replay fix, a targeted code-only apply of `module.ldo_001`

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~01:1xZ (laptop), on `2.0.0_SA_COO~CA` msg 109008 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17B_DEPLOY_20261014.md` @c89588546c, pinned at
`8a480805e5`. Authority: this seat's row `COMM_ASSIST-C-S5` (ARMED) and the first r17 half
(`deliverables/3.0.0_SA_CVO~L/NEVER_WIDEN_HALF_CVO_COMM_ASSIST_R17_DEPLOY_20261014.md`).

## What I measured (not taken from the COO half)

- **Live pre-state** (~01:1xZ): both functions carry `CodeSha256` `lRKObLMbn1kTWSXtohLxZ33HYVq7aBd1o/fjLfaA1Rw=`, 291179 B, LastModified
  2026-10-14T00:37:49Z / 00:37:43Z, 14 environment keys each (the 13 before plus `MUSE_ANSWER_PUBKEY`).
- **The live build IS `b19849b51c`, by content:** I downloaded the handler zip; its sha256 equals `lRKObLMb...`, and all 36 files equal
  `git show b19849b51c:<path>` (36 equal, 0 differ, 0 missing). Against the pin `8a480805e5`: 35 equal, exactly 1 differs
  (`teams_chat/tenant.py`), none added.
- **Terraform:** `git diff --numstat b19849b51c 8a480805e5` over `infra/aws/terraform/transcripts` and `.../modules/ldo`: 0 lines. The
  environment does not move.
- **The second file in the merge is not packaged:** `muse_reader/refresh.py` (+1 line: `seq` in each draft row) runs on dell2, not in
  this zip.
- **The receiver's six arms:** `check_i10_replay.py`, run here: `I10-REPLAY ok=True arms=6 of 6 failed=none`.

## SIGNED: blast radius, both branches

**What the act may touch:** the code of `teams-global-chat-assist-handler-lambda` and `-ingress-lambda`. Nothing else.

**What changes for any caller:** only `muse.reply`, which today acts on nothing (no forwarder exists). It gets stricter in three ways:
- a signed answer without a whole-number `version` is refused;
- a chat draft's answer must carry that draft's `seq`;
- signed bytes that already moved a draft are refused (`replayed`).

`sms.reply` (Andrew's texts) is unchanged.

- **Branch A** (targeted 0/2/0; `source_code_hash` and `last_modified` only, no `environment` key; after-hash equals the clean build of the
  pin): applied. Exactly the one-file change goes live on both functions.
- **Branch B:** nothing is applied. Any pre-state hash other than `lRKObLMb...` voids this half too.

**Rollback:** the code goes back to the saved `lRKObLMb...` zip by the same targeted apply, with no `-var`. `muse_acted` is new and
unwritten until a forwarder exists.

## Does the receiver as built satisfy C-S5? YES for the path C-S5 named; one smaller residual carried

C-S5's path was an old signed `send` for a chat tag reaching a later chat draft under the same tag. The receiver as built closes it at
three points:
- `on_sms_reply` refuses an answer whose tag is not the pending draft's tag (tenant.py:493). Chat tags are unique per chat, so an answer
  cannot be redirected to another chat by choosing the envelope's object id.
- `version` is required and must equal the pending draft's version (`unseen`).
- `seq` must equal the pending chat draft's `seq`, and `seq` never repeats within a chat (`assign_seq`).

The hash record adds that the same bytes never act twice on one draft. C-S5's owner may disarm it once `check_i12_live.py` reads PASS
after this act.

**Residual, carried as row `COMM_ASSIST-C-S6` (INERT, not grounds):** drafts with no `seq` are bound only by tag, version and the
200-entry hash window, and two of their tag spaces repeat.
- End of Day tags are `E` plus month and day (`eod_tag`, tenant.py:76-77). They repeat each year on a fresh `eod:<day>` object whose
  `muse_acted` is empty.
- Mail tags are `M000`-`M999`, hashed per message and reusable within the mail object (`mail_tag`). An acted hash leaves the window after
  200 acts.

A year-old signed End of Day `send` at version 1 would therefore verify against that day's new draft. Reaching it needs a retained signed
answer and a direct send. **Proposed closure:** the receiver refuses a payload whose signed `signed_at` is older than a stated bound (the
design's payload already names `signed_at`). That one check closes every tag-reuse case at once.

-- 3.0.0_SA_CVO~L
