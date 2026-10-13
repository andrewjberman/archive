# MUSE_ANSWER_PATH_DESIGN -- FWD-7, cell CA-h-3 (design only)

Scope: a design. Nothing was built, signed, sent, installed or called. No script, key, AWS call, SSH session or
tenant.py change was made. Sources are read at the worktree base 38ac43222d; citations are path:line.
Measured here: one local command (section 1). Everything about dell2 is "not measured".

## 1. How muse's answer is shown to come from muse

Two candidates.

(a) SIGNATURE. muse signs the answer bytes with a private key that exists only on muse. dell2 holds the public
half and runs `ssh-keygen -Y verify -f <allowed_signers> -I <principal> -n muse-answer@opal -s <sig>` over the
file. The brief says muse's public key is already in administrators_authorized_keys; the box side of that file
is ssh-tailnet-enable.ps1:40 (KeysPath) and :254 (AuthorizedKeysFile for Match Group administrators). No muse
key, muse principal or muse device row exists in org/devices/ or .tools/ (see COMM_ASSIST-W8-S7). Principal name
and fingerprint: not measured.

(b) PATH. muse writes into a location only muse's SSH principal can write. dell2 would enforce it with an ACL
(agents' account denied) or a separate account for muse. By the cell's own premise muse arrives as the SAME
account the dell2 agents run as, so no ACL separates them, and the agents' account can write the path. Not
measured on dell2.

CHOICE: (a). It depends on who holds the private key, not on who can write a folder.
Measured (laptop, not dell2): `ssh-keygen -Y verify` printed "Too few arguments for verify: missing namespace",
rc=1. The verb exists in this OpenSSH build. No sign-and-verify round trip was run (it needs a key).

WEAKER CASE, stated plainly: the signature is only as strong as its trust anchor. allowed_signers and the
forwarder's code sit on dell2 under the same account. If that account can rewrite allowed_signers (for example
through local Administrators, which ssh-tailnet-enable.ps1:496 gives the keys file's ACL; membership not
measured), it can add its own key and sign a forgery. The private key must never be on dell2; if it is, the
signature proves nothing. Both conditions are unmeasured.

Signed payload: one JSON object {"tag", "action" (send|drop|edit), "notes", "version", "signed_at"}. The
signature covers the exact bytes, so tag and version sit inside the signed text.

## 2. How the forwarder verifies it

The forwarder is a dell2 scheduled job (built in CA-h-2 or later; not built here). It reads
<reader root>/answers/ (a folder CA-h-1 does not create, see COMM_ASSIST-W8-S9) and the reader's drafts.json
(refresh.py:230-234 _draft_row, which carries tag and version).

Order of checks; the first failure ends the file as a refusal (section 3):
1. SIGNATURE: ssh-keygen -Y verify over the bytes, against the pinned allowed_signers. Unsigned, bad, or signed
   by a principal other than muse -> refuse SIGNATURE.
2. SHAPE: JSON parses; action in {send, drop, edit}; tag is a non-empty string -> else refuse SHAPE.
3. TAG: a drafts.json row with that tag exists -> else refuse TAG-NOT-WAITING.
4. VERSION: payload version equals that row's version -> else refuse VERSION-STALE (the forwarder's copy).
5. OBJECT: resolve the draft's object id from index row pk "#index#sms-tag", sk <tag> (ldo.py:152-155; the text
   path does the same at tenant.py:1157) -> else refuse OBJECT-NOT-FOUND. drafts.json carries no object id
   (refresh.py:230-234), so this lookup is a read the forwarder must make (COMM_ASSIST-W8-S8).

On success: ONE SQS FIFO send (section 5) with event_id "muse-" + sha256 hex of the answer bytes, then a done
marker answers/done/<sha256>.json (time, file name, tag, version, event_id).

IDEMPOTENT: a second copy has the same sha256, finds its done marker, and sends nothing. Two further guards
hold independently: the queue drops a repeated MessageDeduplicationId within 5 minutes (ldo.py:131-136), and the
handler skips a repeated event_id at any time (ldo.py:131-132 docstring). The assistant's own check (section 4)
is the authority; the forwarder's version check reads a copy as fresh as the last refresh.

## 3. What is recorded on a refusal

Written to <reader root>/answers/REFUSALS.jsonl: one appended line per refused file, never rewritten.
Fields: "at" (UTC, ends in Z), "file" (file name only), "reason" (SIGNATURE | SHAPE | TAG-NOT-WAITING |
VERSION-STALE | OBJECT-NOT-FOUND), "tag" (as read from the payload, or null), "sha256" of the bytes.

A refusal never reaches the assistant. The refusal path makes no SQS send, no ldo.send and no DynamoDB write;
its only write is the local line above.

GAP: no alert and no notification (standing moratorium, CLAUDE.md section 5). The record is read by whoever
opens the file. Whether Andrew reads it: not measured.

## 4. The stale-version refusal

Shape: pending = {tag, kind, draft, version, incoming, chat_title, texted_at, status, send_at} (tenant.py:19),
held in the state row's data JSON, not a table attribute (refresh.py:296-300; COMM_ASSIST-W8-S2).

The check: unseen() (tenant.py:131-147) compares want = ctx.payload.get("version") with pending["version"]
(tenant.py:137-139) and returns True on mismatch. on_sms_reply refuses send and drop with "#<tag> changed just
before your reply, so nothing was done. Reply to the latest #<tag> text." (tenant.py:497-500).

So an answer MUST carry the tag and the version it was shown: {"tag": "<tag>", "version": <int>}, the version
being drafts.json's version at the time muse displayed the draft. The assistant's compare is authoritative.

GAP, measured: the edit branch never calls unseen(). on_sms_reply calls it only for action in ("send", "drop")
(tenant.py:497). The redraft branch begins at tenant.py:527 and applies the notes to the CURRENT pending draft,
so a stale edit answer is applied to the newer version. It texts a new draft for Andrew's approval and posts
nothing, so no Teams post follows. Recorded as COMM_ASSIST-W8-S6. The fix sits in tenant.py, outside this cell.
Until it lands, the forwarder's VERSION check is the only guard for edit, and it is only as fresh as the refresh.

## 5. The write entry and the grant it needs

ENTRY: ROUTES "sms.reply" (tenant.py:931), the kind the text path sends at tenant.py:1163. It is delivered to
the chat-assist LDO's mailbox, an SQS FIFO queue (infra/aws/terraform/modules/ldo/main.tf:108); the forwarder
takes its URL and ARN from the module outputs (outputs.tf:45-50), never typed. The envelope carries object_id
(from section 2 step 5), kind "sms.reply", event_id "muse-<sha256>", sent_at, and payload:
{"tag": "<tag>", "action": "send|drop|edit", "notes": "<notes or empty>", "version": <int>}.
MessageGroupId is the object id (ldo.py:134-136). The text path's payload is the same without "version"
(tenant.py:1163); version is the only added field.

WRITE STATEMENT (named, not applied):
  {"Effect": "Allow", "Action": "sqs:SendMessage", "Resource": "<mailbox_arn output of module.ldo_001>"}
Separate read the forwarder also needs: dynamodb:GetItem on the state table's #index#sms-tag rows (ldo.py:152-155).

GRANT STATUS on the declared state: the write IS covered, so it is not a new request. dell2's user
(cloudops-dell2-agent-user, iam.tf:24-26) is a member of AdministratorAccessOpalCapital (iam.tf:40-47), which
the ruling @53acd6fe5f keeps with three denies: dell_deploy_policy.json:46-67 (DenyCloudTrailWrites,
DenyS3DeletesOnProductionData, DenyTableAndDatabaseDeletes) and DenyAuditTrailBucketWrites in
dell_create_policy.json:104-105. None names sqs:SendMessage. The group is NOT Terraform-managed (iam.tf:36-38),
so its policy document is not in the repo and was not read through a policy simulation. The dell2 user's own
Allow lists the agentbus queues only (dell_deploy_policy.json:25-30), not the LDO mailbox. The applied state of
the membership is CA-h-2's precondition (decomposition round 16, CA-h-2 row): not measured here. If that
read-back shows the membership absent, the statement above is requested by name under C-ROLE-REQUEST and is
not inherited.

## 6. The forged-answer test that must refuse

Build-cell test, two inputs, two expected outcomes.

Input A (muse-signed): an answer file for a pending tag at its current version, signed by muse over its bytes,
written into answers/. EXPECTED: exactly one sms.reply message on the mailbox for the draft's object, event_id
muse-<sha256>, and the assistant acts on it (send, drop or redraft).

Input B (forged): the same JSON content, written by the dell2 agents' account, with no signature or with a
signature by a key outside the pinned allowed_signers. EXPECTED: the forwarder refuses with reason SIGNATURE;
one REFUSALS.jsonl line carries that reason and the tag; ZERO SQS sends; the state row's version is unchanged.

CONTROL (the refused arm must refuse for the stated reason): (i) the same forged JSON with a valid muse signature
is ACCEPTED, so its shape, tag and version are valid; (ii) Input B is refused with reason SIGNATURE while shape,
tag and version pass. Without (i) a refusal could be a shape, tag or version failure. Also: the same signed file
delivered twice acts once (section 2).

LIMIT: the test proves the verifier refuses an unsigned or wrongly signed file. It does not prove the trust
anchor is out of the agents' reach (section 1, weaker case); that is an access fact and stays unmeasured.
