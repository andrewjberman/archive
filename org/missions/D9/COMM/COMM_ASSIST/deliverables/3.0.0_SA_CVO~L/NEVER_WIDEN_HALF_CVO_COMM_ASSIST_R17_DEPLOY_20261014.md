# Never-widen half (CVO) -- COMM_ASSIST round 17, cell CA-i-4: the targeted apply of `module.ldo_001` (code plus `MUSE_ANSWER_PUBKEY`)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~00:0xZ (laptop), on `2.0.0_SA_COO~CA` msg 109001 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17_DEPLOY_20261014.md` @e93a7913ee, pinned at
`b19849b51c`. Authority: `ledger/ROUND_ANALYSIS.round16.md` @6e9e2fc1ff (receiver-side check meets FWD-7; the key is a change-managed
deploy), PRD v0.7.

## What I measured (not taken from the COO half)

- **Live pre-state** (`get-function-configuration`, ~00:0xZ): both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda`
  carry `CodeSha256` `nIQW+3XvvaFNJQfwX5lrI99XSexESb68Pd1uLldlTgI=`, 269206 B, python3.12, no layers, LastModified
  2026-10-11T02:16:55Z / 02:17:01Z. Environment, key names only, 13 on each: `GATEWAY_BASE`, `IGNORE_NAMES`, the nine `LDO_*`,
  `MAIL_BEARER_SECRET`, `SMS_ORIGINATION`. No `MUSE_ANSWER_PUBKEY`.
- **The live build IS `2fd32e12c2`, by content.** I downloaded the ingress zip; its sha256 (base64) equals `nIQW...`. All 32 files equal
  `git show 2fd32e12c2:<path>` (LF-normalised, handlers.py and ldo.py mapped to their source paths): 32 equal, 0 differ, 0 missing.
- **What the pin adds, by content against that same zip:** 9 files differ (`assist.py`, `mail_requests.py`, `tenant.py`,
  `lib/opal_naming.py`, `exemptions.json`, `name_rulings.json`, `root_map.json`, `scopes.json`, `systems.json`) and 4 are added
  (`muse_verify.py`, `feeds.json`, `firm_pages.json`, `platinum_destinations.json`). 13 files, the COO half's set exactly.
- **Terraform, `2fd32e12c2..b19849b51c`:** `module.ldo_001`'s inputs at the pin are `local.ca_env`, `local.ca_zip`, two existing
  secrets and two variables. The only change reaching them is the new variable `chat_assist_muse_answer_pubkey` and its one map line
  `MUSE_ANSWER_PUBKEY`. The other root changes (`commentary.tf`, `pull.tf` memory 1024, `readers.tf` comments, `readers.auto.tfvars`)
  are outside the target.
- **The key is muse's:** the pinned default's blob hashes to `SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ`, the fingerprint the
  laptop's enable receipt records as `ssh-ed25519 muse` and CA-h-2 read in dell2's key file.
- **The rollback value refuses everything:** `_pinned_key("")` and an unset variable both parse as no key (`muse_verify.py:131-140`), so
  `verify` fails and `on_muse_reply` records a refusal and sends nothing.
- **New sends in the four round-17 files:** one, `a.send_sms(_mail_text(pending), tag)` in `mail_requests.py`, a text TO ANDREW
  carrying the final draft he pastes himself. No mail send, no Teams post, no new recipient.
- **Other writers of these two functions:** two projects apply this module (COMM_ASSIST and NFRA_CTLPLN). Open-deploy sentinels,
  unioned across all 3 worktrees: none on `module.ldo_001`. The two that share the root or a setting name do not move it:
  `nfra-trnspt-a18-...` targets the reader IAM and KMS resources (applied 2026-10-09, held on probe results), and
  `d12-sms-origination-...` concerns the auth handler.
- **The checks are read-only:** `check_i4_live.py` signs with throwaway keys it makes itself and imports the served code locally; it
  invokes nothing and sends nothing (it stubs `send_message`).

## SIGNED: blast radius, both branches

**What the act may touch:** the code of the two functions above and ONE environment key on each, `MUSE_ANSWER_PUBKEY`. Nothing else:
no policy, no secret, no other key, no reader, no other address.

**What changes for any caller, today:**
- A received mail that names Andrew gets a finishable draft; his `1` texts him the final text to paste. Nothing is mailed.
- A new event kind `muse.reply` exists. It acts only on an answer signed by muse's key. No forwarder exists (CA-i-5), and no signed
  answer exists, so today it acts on nothing. An unsigned or wrongly signed one is refused and recorded in `state["muse_refusals"]`.
- A versioned edit answer now meets the stale-version check (W8-S6's repair, on the text path too).
- Agent-bus messages from the assistant carry `from_tailnet=ldo-001`.

- **Branch A** (targeted 0/2/0; changed keys within {`source_code_hash`, `last_modified`, `environment`}; the environment diff is exactly
  `+ MUSE_ANSWER_PUBKEY` with fingerprint `oq0WqfmN...`; after-hash equals the clean build of the pin): applied. Exactly the 13-file
  change and the one key go live on both functions.
- **Branch B:** nothing is applied. Any pre-state hash other than `nIQW...` voids this half too, because the base I proved by content
  would no longer be the live one.

**Rollback per key:** code goes back to the saved `nIQW...` zip; `MUSE_ANSWER_PUBKEY` goes back to `""` (present and empty, which refuses
every muse answer) by the same targeted apply, the one permitted `-var`. No state is migrated; `muse_refusals` is new and unwritten.

## Carried (not grounds for this act; ONE hazard for the next one)

**A signed answer can be REPLAYED, and this must be closed before CA-i-5 installs the forwarder.** Row `COMM_ASSIST-C-S5`, ARMED,
disarm owner `2.0.0_SA_COO~CA`.
- A chat's tag is stable (`chat_tag`, tenant.py:56-66). After a draft is sent, the next draft starts again at version 1 (:238).
- `_muse_fields` accepts an answer with no version. Without a version, the tagged-reply path falls back to a time window that uses the
  envelope's `sent_at`, which the sender writes.
- So a signed `{"tag": "C123", "action": "send", "version": 1}` also verifies against a LATER chat draft under C123 at version 1.
  Signed answers will sit in dell2's `answers/` folder, which the dell2 agents' account can read. That account can send `muse.reply`
  directly. Together this sends a draft Andrew never saw, in his name. This is exactly what FWD-7 refuses.
- **Repair:** the receiver requires `version` and binds the answer to the draft's `seq`, which never repeats within a chat (`assign_seq`,
  tenant.py:119-122), or it refuses a signature it has already acted on. `drafts.json` must then carry `seq` (refresh.py does not today).
- Not reachable at this act: no forwarder exists and muse has signed nothing.

-- 3.0.0_SA_CVO~L
