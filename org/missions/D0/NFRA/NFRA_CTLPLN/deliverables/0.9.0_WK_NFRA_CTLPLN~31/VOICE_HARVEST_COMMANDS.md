# VOICE_HARVEST_COMMANDS -- filling Andrew's voice examples (NFRA_CTLPLN.TO-CT-i-4)

The messages Andrew wrote are client mail and are NOT committed. They live as one JSON object in the Teams agent's state
store: bucket `assist.BUCKET`, key `assist.state_key("andrew_voice_examples.json")` (both are naming-builder output through
`assist._addr`; type neither). The tracked file `data/transcripts/scripts/teams_chat/andrew_voice.md` carries only the
section list and, in each section, the line naming that object and its key.

## 1. The recorded-message shape (one message per file, `*.json`, in one folder per harvest)

```json
{"author_is_andrew": true, "sent_at": "2026-10-01T14:03:00Z", "channel": "mail", "text": "<the message, plain text>"}
```

- `author_is_andrew` (bool) -- true only for a message he wrote. Anything else is dropped by the harvest.
- `sent_at` -- ISO time; newest first is decided by it.
- `channel` -- `"mail"` or `"teams"`.
- `text` -- the message as plain text. Kept only when its length is inside `--min-chars` (40) and `--max-chars` (1500).

## 2. The harvest, one command per kind

`--out` must be a local file OUTSIDE every git working tree; the command refuses (one `ERROR:` line, exit 2, nothing written)
when it is not. It prints counts only and uploads nothing. Run it once per kind into the same `--out` file; each run merges
its kind and leaves the others.

```
python data/transcripts/scripts/teams_chat/voice.py harvest --kind mail_reply     --from <recorded dir> --out <local file>
python data/transcripts/scripts/teams_chat/voice.py harvest --kind teams_reply    --from <recorded dir> --out <local file>
python data/transcripts/scripts/teams_chat/voice.py harvest --kind teams_post     --from <recorded dir> --out <local file>
python data/transcripts/scripts/teams_chat/voice.py harvest --kind job_completion --from <recorded dir> --out <local file>
python data/transcripts/scripts/teams_chat/voice.py harvest --kind end_of_day     --from <recorded dir> --out <local file>
```

Optional on each: `--max 12` (messages kept), `--min-chars 40`, `--max-chars 1500`. The LAST line of each run reads
`VOICE-HARVEST kind=<id> read=<r> by_andrew=<a> kept=<k> written=<True|False>` (`written` is for the local file).

## 3. The upload (the issuer's act, not the harvest's)

Put the local file at the state store object named above (an `s3 cp` of that one file to the key
`assist.state_key("andrew_voice_examples.json")` in `assist.BUCKET`; build the address with `assist._addr`, do not type it).
The Teams function's role already reads the objects under that state prefix (it reads `me.json` and `switch.json` there), so no
policy change is expected; confirm with one read after the upload. A draft then carries the newest messages that fit 6000
characters, each fenced as reference for voice only.

`voice.examples()` reads the object only inside the deployed function (the Lambda runtime sets `AWS_LAMBDA_FUNCTION_NAME`) or
when `ANDREW_VOICE_EXAMPLES` is set; elsewhere it returns an empty list without a network call (row NFRA_CTLPLN-W31-S8).

## 4. The package line the deploy needs

None is new. `infra/aws/lambda/teams-chat-assist/build.sh` line 18 copies the whole `teams_chat` folder
(`cp -r "$REPO/data/transcripts/scripts/teams_chat" ...`) and the zip step packs every file except `*.pyc`, so `andrew_voice.md`
and `voice.py` ride in the zip. Line 19 already ships `daily_reports/eod/VOICE.md`, which `voice.py check` compares against. If
an explicit line is wanted, it is the same copy and changes nothing:

```
cp "$REPO/data/transcripts/scripts/teams_chat/andrew_voice.md" "$PKG/data/transcripts/scripts/teams_chat/"
```

## 5. Later items (not done this round)

- `CHAT_SYSTEM` and `COMPLETION_SYSTEM` still carry the voice lines the file repeats; removing them from the constants is a
  later item.
- The File is read by `draft_chat_reply` (`teams_reply`) and `_completion_draft` (`job_completion`). No drafter reads `mail_reply`
  or `teams_post` yet: a mail request is texted to him with no draft (CT-i-3), and nothing drafts a Teams post.
- The End of Day draft does not read this file; it still reads `daily_reports/eod/VOICE.md`.
