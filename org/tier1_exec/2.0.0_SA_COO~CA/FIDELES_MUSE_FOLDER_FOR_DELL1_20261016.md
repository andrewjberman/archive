# The muse folder: what it is on dell2 and how dell1 keeps its own copy (for 0.0.0_AB_MSTR~DELL1)

Written by 2.0.0_SA_COO~CA, 2026-10-16 ~04:1xZ, on 1.0.0_SA_CTO msg 109587 (from 0.0.0_AB_MSTR msg 109586). The order this
serves: Andrew-direct `ANDREW_DIRECT_20261016_034xZ_FIDELES_SKILL_DELL1_MSTR_OWNS_MUSE_MAIL_WATCHER.md` (this folder), item 4:
"Both dells should maintain the muse folder on their box." Sources: the dell2 install reports
`org/missions/D9/COMM/COMM_ASSIST/deliverables/0.7.0_AE_CloudOps~CA2/REPORT_TO-CA-h-2.md` and `.../REPORT_TO-CA-i-5.md`, and
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r17/MUSE_READ_CARD.md`.

## On dell2 today (measured by its installer, 2026-10-13/14)

- Folder: `C:\Users\Test\muse-reader` (user `Test`; muse reads it over ssh `Test@dell2`, tailnet `100.104.84.87`).
- It holds `INDEX.json`, `drafts.json`, `open_calls.json`, `eod_today.json`, `sprint_today.json`, `README.txt` (layout in
  `MUSE_READ_CARD.md`), plus `answers\`, `answers\done\`, `answers\rejected\` for muse's signed answers.
- Two scheduled tasks, both user `Test`, S4U logon, working directory the checkout `C:\dev\ajb_workspace`:
  - `MuseReaderRefresh`, every 15 minutes: `python data\transcripts\scripts\muse_reader\refresh.py --root <folder>`. It rewrites
    the read files. The folder is a regenerable copy.
  - `MuseAnswerForward`, every 2 minutes: `python data\transcripts\scripts\muse_reader\forwarder.py --root <folder>`, with User
    variables `MUSE_MAILBOX_URL` and `MUSE_LDO_ID` copied from the live handler's `LDO_MAILBOX_URL` and `LDO_ID`
    (`aws lambda get-function-configuration`, read-only; never typed).

## How dell1 keeps its copy (the same install, on dell1)

1. Pull the checkout so it holds `data/transcripts/scripts/muse_reader/` at the dell2 pin or later.
2. Run `refresh.py --root %USERPROFILE%\muse-reader` once by hand; expect `MUSE-REFRESH ok=<n> absent=0 unreadable=0`.
3. Register `MuseReaderRefresh` with the exact PowerShell in `REPORT_TO-CA-h-2.md` (paths derived from dell1's own
   `$env:USERPROFILE`, its own Python and its own checkout; never the dell2 strings).
4. Create `answers\` by hand, set the two User variables from the live function, register `MuseAnswerForward` with the
   PowerShell in `REPORT_TO-CA-i-5.md`.
5. For muse to read dell1, sshd on dell1 must accept muse's key. Which key is muse's is not decided in the record (dell2's
   report lists fingerprints and adds no key); that is Andrew's to name.

Rollback is in both reports (`Unregister-ScheduledTask`, remove the folder).

## Two answers folders: safe, but muse writes to one

The receiver accepts one signed answer per draft and refuses a replay (`replayed`), so an answer forwarded from both boxes
acts once. Muse should still write each answer to ONE box: dell1, the primary, and dell2 only when dell1 is down.
