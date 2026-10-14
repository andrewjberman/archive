# MP-pd-6 pre-act record -- 0.9.0_WK_NFRA_MCPORTAL~29

Recorded before any live write (task order NFRA_MCPORTAL.TO-MP-pd-6, section 1 step 1).

## Settings file

- Path: `C:/Users/Opal Bloomberg/.claude/settings.json` (this Windows user's Claude Code user settings).
- Size: 518 bytes.
- sha256 (before any write): `3907626e58fdb40f61b85a9d62bccbd429e4ff08e3c56e299a67591579c5a348`
- Top-level key names (names only, no values): `agentPushNotifEnabled`, `autoUpdatesChannel`, `effortLevel`, `model`, `modelSettings`, `skipDangerousModePermissionPrompt`, `switchModelsOnFlag`, `theme`, `tui`, `voice`, `voiceEnabled`.
- `statusLine` already present: NO. The file has no `statusLine` key, so the step-1 STOP condition does not hold and the order proceeds.

## Command to add

- Script (main tree, derived from `git rev-parse --git-common-dir`): `C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.tools/claude-usage-statusline.py`
- Entry: `{"type": "command", "command": "python \"C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.tools/claude-usage-statusline.py\""}`
- Smoke run (stdin `{}`, `CLAUDE_CONFIG_DIR` at a scratch directory under the worktree `.scratch/`): exit 0, wrote one `usage_snapshot.json` in that directory.

## Blast radius (my words)

Once the `statusLine` key is in the settings file, every Claude Code session on this box that reads that file runs the
command at each status-line refresh and shows its one printed line at the bottom of the terminal. That is every site Z
seat. The command reads its stdin and two local files and writes one local file, `<config dir>/usage_snapshot.json`.
It makes no network call.

## Rollback (my words)

Remove the one `statusLine` key from the settings file, or copy the backup back over it. Nothing else in the file changes.
A seat's next status-line refresh then shows its previous (empty) status line.

## Backup

- Backup path (outside the repository, never committed): `C:/Users/Opal Bloomberg/.claude/settings.json.pd6-backup`.

## Planned steps

1. Rollback proven on a copy (add key, remove key, parsed equality; backup-to-copy sha256 equality).
2. Backup, then atomic write of the live file (only the `statusLine` key added), re-read as JSON, key-by-key equality against the backup.
3. Poll for `<config dir>/usage_snapshot.json` for up to 15 minutes.
