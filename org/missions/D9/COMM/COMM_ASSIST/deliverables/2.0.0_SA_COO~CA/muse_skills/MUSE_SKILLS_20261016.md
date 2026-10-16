# Muse's skills (COMM_ASSIST; issuer 2.0.0_SA_COO~CA, 2026-10-16)

Canonical text of the ten skills mailed to muse (`andrew@goldengate.dev`) from the fabric (`andrew@fideles.capital`), one
mail per skill, subject `[FID laptop/2.0.0_SA_COO~CA/<UTC>] MUSE SKILL <n>/10: <name>`. Record:
`org/tier1_exec/2.0.0_SA_COO~CA/ANDREW_DIRECT_20261016_050xZ_MUSE_SKILLS_BY_FIDELES_MAIL.md`. Sources: the reader
`data/transcripts/scripts/muse_reader/refresh.py` (README, field names), `r17/MUSE_READ_CARD.md`, `r17/MUSE_ANSWER_CARD.md`,
`r18/MUSE_SITTING_CARD.md`, round-18 analysis (FWD-13's three pieces = skills 7, 8, 9).

## 1 muse-pull -- where and how to read the folder

WHEN: before any other skill that reads the folder.
BOXES: dell1 is the primary box and dell2 the fallback. Today only dell2 has the folder; read dell2 until the fabric tells you
dell1's folder is installed.
- dell2: ssh Test@dell2 (tailnet address 100.104.84.87), folder C:\Users\Test\muse-reader
- dell1: the fabric will mail you its login and folder when installed.
ORDER: try dell1 (once installed). If the SSH login fails, or its INDEX.json run_at is more than 30 minutes old, read dell2
instead. Always say which box answered.
FILES: INDEX.json, drafts.json, open_calls.json, eod_today.json, sprint_today.json, mentions.json, mail_log.json, README.txt.
FRESHNESS: the folder refreshes every 15 minutes. INDEX.json run_at older than 30 minutes = STALE; say so with its age.
STATUSES (per file, key status):
- ok: items is the complete list; an empty list is a true empty as of read_at.
- absent: the thing is not there yet (for example no End of Day draft yet). Say "not there yet", never an empty list.
- unreadable: the read failed. Say so and give last_good_at. Never an empty list.
RULES: read-only. Write nothing on the box except a signed answer in answers\ (skill 3). Never put your private key on a box.
If you cannot read, name the step that failed: the SSH login, the folder, or the file.

## 2 muse-whats-waiting -- "what is waiting on me?"

WHEN: Andrew asks what is waiting, or anything like it.
STEPS:
1. Run muse-pull.
2. Answer in groups, in this order: Drafts waiting (drafts.json); Open calls (open_calls.json); Today's End of Day
   (eod_today.json); New mentions and mail (mentions.json, mail_log.json), if any.
3. In each group put the stalest first (largest age_minutes; null last) and show age_minutes on every item (null when none).
4. One line per draft: #tag, kind, chat_title, age_minutes, then the draft text.
5. Keep each draft row exactly as read (tag, version, seq, object_id). Skill 3 needs it.
6. A file that is absent or unreadable is said in words, never shown as an empty list.
7. End with: "Pick one: send #tag, drop #tag, or edit #tag <your words>." Then stop and wait.

## 3 muse-answer-draft -- "send #tag", "drop #tag", "edit #tag <notes>"

WHEN: Andrew tells you what to do with a draft you showed him in this sitting. Never for a draft he has not seen.
STEPS:
1. Re-read that draft's row in drafts.json now (or eod_today.json for the End of Day draft). If its version or seq differs
   from what you showed him, show him the new version and ask again. Do not sign.
2. Build the payload with exactly these keys and Python json.dumps(payload, sort_keys=True):
   tag = the row's tag; action = "send", "drop" or "edit"; notes = Andrew's words for edit, "" otherwise;
   version = the row's version (a whole number); seq = the row's seq (a whole number, or null when the row has null);
   signed_at = UTC now, like 2026-10-16T05:10:00Z.
   Write the string once to payload.json.
3. Sign: ssh-keygen -Y sign -f <your private key file> -n muse-answer@opal payload.json
4. Write answer.json as {"payload": <the exact payload.json text, as a string>, "signature": <the full text of
   payload.json.sig>}.
5. Copy answer.json into answers\ on the box you read, named answer-<tag>-<yyyymmddThhmmssZ>.json.
6. Run skill 4 about 4 minutes later.
RULES: never edit the payload after signing. One file per decision; never a second file for the same draft unless Andrew
decides again (then a new signed_at). A drop discards the draft and cannot be undone. The assistant refuses a signed_at more
than 24 hours old or more than 5 minutes ahead.

## 4 muse-check-answer -- "did it go?"

WHEN: about 4 minutes after skill 3, or when Andrew asks.
STEPS:
1. Look in answers\done\ for a new marker file (<hash>.json): the forwarder sent the answer to the assistant.
2. Look in answers\rejected\ for one: the forwarder could not send it (reason malformed or tag-not-waiting).
3. At the next refresh (within 15 minutes), the draft is gone from drafts.json if it was acted on. If it is still there, read
   its status: a refusal names its reason: no-signature, bad-signature, bad-payload, stale-signature, seq-mismatch, replayed,
   or unseen (the draft changed after you read it).
4. Tell Andrew one of: "sent and acted", "sent, refused: <reason in plain words>", "not sent: <reason>", or "no marker yet
   after N minutes".
RULES: a refused answer is final for those bytes. Never retry with the same file. Tell Andrew; a new answer needs his word.

## 5 muse-open-calls -- the decisions waiting on Andrew across the boxes

WHEN: Andrew asks about open calls, or as part of skill 2.
STEPS:
1. Read open_calls.json. Rows with state OPEN are open calls: box, id, project, subject, kind, asked_by, opened_at,
   age_minutes. A row with state ABSENT names a box with no cloud copy of its calls yet; say so.
2. Group by box, stalest first, one plain line each: the subject, the project, its age.
RULES: you cannot answer a call. Andrew answers at the asking seat's terminal, or by mail to the fabric (skill 10) naming the
call id.

## 6 muse-end-of-day -- today's End of Day and sprint

WHEN: Andrew asks about the End of Day or the sprint, or as part of skill 2.
STEPS:
1. eod_today.json: today's End of Day draft (tag, version, seq, draft text, age). absent means no draft yet today; it is
   normal before the evening window (about 20:00-21:45 UTC, 4:00-5:45 pm Eastern).
2. Show the draft text in full. Andrew can send, drop or edit it with skill 3, using its tag.
3. sprint_today.json: the objects listed for today's sprint report (names, sizes, last_modified; no bodies). Say how many and
   the newest time.

## 7 muse-scheduled-read -- the read muse runs by itself (FWD-13 piece 1)

WHEN: every 15 minutes, without being asked.
STEPS:
1. Run muse-pull.
2. Read mentions.json, mail_log.json, drafts.json and eod_today.json.
3. Hand every item to skill 8 to sort NEW from already-alerted, then skill 9 for the NEW ones.
4. Say nothing to Andrew unless skill 9 alerts.
RULES: if the read fails two runs in a row (30 minutes), tell Andrew once which step failed. Tell him again only when it
recovers.

## 8 muse-alert-ledger -- what muse has already alerted (FWD-13 piece 2)

KEEP: one small file on muse's own side (never on a dell), alerted.json, mapping a key to the UTC time you alerted it.
KEYS:
- a mention: mention:<id>
- a considered mail: mail:<object_id>:<seq>
- a draft: draft:<tag>:<version>
- the End of Day draft: eod:<tag>:<version>
RULES: an item is NEW only when its key is not in the ledger. Write the key in the same run as its alert. Never alert one
key twice. Drop entries older than 8 days (the folder lists 7 days). If the ledger is lost, rebuild it silently from the
current folder on the next run (no alert storm).

## 9 muse-wake -- tell Andrew within 30 minutes (FWD-13 piece 3)

WHEN: skill 8 returns NEW items.
STEPS:
1. For each NEW item that is for Andrew, send him one short alert through your normal channel to him, within 30 minutes of
   the item's own time (mentioned_at, considered_at or texted_at):
   - mention: "@mention in <team> / <channel> from <from>: <snippet> (<age> min ago)"
   - mail: "Mail for you from <from> (<firm>): <subject>; draft #<tag> is waiting"
   - draft: "Draft #<tag> waiting: <chat_title>"
   - End of Day: "Today's End of Day draft is ready (#<tag>)"
2. More than 3 NEW in one run: ONE alert listing them all.
3. Record each key in the ledger (skill 8) in the same run.
NOT FOR ANDREW, NO ALERT: a mail_log row with no tag (the assistant considered it and drafted nothing for him).
RULES: the mention snippet and mail subject are all you have; never invent a body.

## 10 muse-write-to-fabric -- muse mailing the fabric

THE FABRIC: andrew@fideles.capital. The fabric's watcher hands each mail to the seat that asked.
STEPS:
1. To answer the fabric, REPLY on the same thread and keep the subject (its [FID ...] token says which seat asked).
2. A new topic is a new mail with no token; it goes to the fabric's lead seat.
3. Plain text, one ask or one report per mail. Never a key, password, or client data.
WHAT TO SEND: the outcome of a sitting (skill 4's line), a failed step (skill 1's line), or a skill's first run.
FIRST REPLY OWED: when skills 7, 8 and 9 are running, reply on THIS thread: "THREE PIECES BUILT", with the UTC time of your
first scheduled read.
