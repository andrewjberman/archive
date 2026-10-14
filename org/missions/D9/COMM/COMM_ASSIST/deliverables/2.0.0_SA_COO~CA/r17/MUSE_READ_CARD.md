# The muse read -- FWD-6's exercise, one question asked in muse (COMM_ASSIST round 17, issuer 2.0.0_SA_COO~CA, 2026-10-13 ~23:5xZ)

**The act (Andrew's, in muse, a few seconds):** ask muse once: **"what is waiting on me?"** Muse answers by reading the folder on dell2 over the tailnet, with its own key.

**What muse reads** (all of it is on dell2, in the folder `muse-reader` under the `Test` account's home; ssh `Test@dell2`, address `100.104.84.87` or the tailnet name `dell2`):

| file | what it holds |
|---|---|
| `INDEX.json` | the run time and, per source, `status` (`ok`, `absent` or `unreadable`), `read_at`, `last_good_at` |
| `drafts.json` | the drafts waiting on Andrew: tag, kind, version, the draft text, the chat title, `texted_at`, `age_minutes`, `age_from`, `object_id` |
| `open_calls.json` | every box's open calls: id, box, title, `opened_at`, `age_minutes` |
| `eod_today.json` | today's End of Day draft, if any |
| `sprint_today.json` | today's sprint page objects, if any |
| `README.txt` | the layout in plain English |

The task `MuseReaderRefresh` rewrites them every 15 minutes. Read-only for muse: nothing in this round lets muse answer yet (the signed-answer path, FWD-7, is built and not deployed).

**What a good answer looks like (the grade):** every item muse shows carries its age (`age_minutes`, whole minutes since its own time, `null` when it has none); an `absent` or `unreadable`
source is SAID, never shown as an empty list; items are grouped (drafts waiting, open calls, today's End of Day) and the stalest first. If muse cannot read the folder, that is the finding:
tell the issuer which step failed (the SSH login, the folder, a file).

**Why it matters:** this is the first of FWD-6's two reads and the input to FWD-12 (muse's efficacy against the text path), which decides whether the Kimi/Quo text fallback can retire.
