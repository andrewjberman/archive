# How muse answers a waiting draft -- the signed answer file (COMM_ASSIST FWD-7; issuer 2.0.0_SA_COO~CA, 2026-10-14)

**Status: NOT YET LIVE FOR A REAL ANSWER.** The path is built and the assistant refuses everything but muse's signature, but a time bound on signed answers (cells CA-i-13 and CA-i-14) must be live first, and the forwarder on dell2 (cell CA-i-5) must be installed.
This card is changed to "LIVE" by the issuer when both read PASS. Until then muse reads the folder (see `MUSE_READ_CARD.md`) and does not write an answer.

**What an answer is.** One file in `answers\` inside the reader folder on dell2 (`%USERPROFILE%\muse-reader\answers\`, account `Test`, address `100.104.84.87`). It is one JSON object with two fields, `payload` (the text that was signed, a string) and `signature` (the armored signature).
A job on dell2 forwards each file once to the assistant, which checks the signature against muse's key and acts, or refuses and records why.

**Build it from the draft muse was shown.** Read the draft's row in `drafts.json` (the same folder). The signed payload is this JSON object, with these exact keys:

| key | value |
|---|---|
| `tag` | the row's `tag` |
| `action` | `send` (post it as drafted), `drop` (discard it), or `edit` (redraft it with `notes`) |
| `notes` | Andrew's words for an `edit`; `""` otherwise |
| `version` | the row's `version`, a whole number: the version muse showed Andrew |
| `seq` | the row's `seq` (a whole number, or `null` when the row carries `null`) |
| `signed_at` | the UTC time muse signs, like `2026-10-14T02:30:00Z`. The assistant refuses a time more than 24 hours old or more than 5 minutes ahead of its own clock |

An answer for a draft that has changed since muse read it (a newer version, or a different `seq`) is refused, so muse answers only what Andrew actually saw. The same signed file never acts twice.

**Sign it with muse's own key** (muse's private key is on muse; the assistant holds only the public half). The namespace is exactly `muse-answer@opal`:

```
python - <<'PY'
import json, subprocess, datetime
row = {...}   # the draft's row from drafts.json, read just now
payload = json.dumps({"tag": row["tag"], "action": "send", "notes": "", "version": row["version"], "seq": row.get("seq"),
                      "signed_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, sort_keys=True)
open("payload.json", "wb").write(payload.encode("utf-8"))
subprocess.run(["ssh-keygen", "-Y", "sign", "-f", "<muse private key file>", "-n", "muse-answer@opal", "payload.json"], check=True)
sig = open("payload.json.sig", encoding="ascii").read()
open("answer.json", "w", encoding="utf-8").write(json.dumps({"payload": payload, "signature": sig}, sort_keys=True))
PY
```

Then copy `answer.json` into `answers\` on dell2 under any new file name (for example `answer-<tag>-<time>.json`). The `payload` string in the file must be byte-for-byte the text that was signed (`json.dumps` as above, written once and reused).

**What happens next (nothing for muse to do):** within about two minutes the forwarder sends the file; the assistant verifies and acts exactly as if Andrew had texted `1`, `0` or notes; the file moves nowhere (it is kept), and `answers\done\<hash>.json` records that it was sent
(`answers\rejected\<hash>.json` records a file the forwarder could not send, with its reason: `malformed` or `tag-not-waiting`). If the assistant refuses the answer (wrong key, changed draft, too old, already acted on), the refusal is recorded in the draft's state with its reason and nothing is sent to anyone.

**Never:** sign an answer for a draft muse has not shown Andrew; put a private key anywhere on dell2; edit `payload` after signing.
