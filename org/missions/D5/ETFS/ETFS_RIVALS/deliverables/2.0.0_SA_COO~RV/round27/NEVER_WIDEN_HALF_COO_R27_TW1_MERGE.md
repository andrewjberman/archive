# NEVER-WIDEN -- COO HALF: ETFS_RIVALS RIV-tw-1 -- the MERGE of branch `wk-ETFS_RIVALS-19` (@de25db03ea) into site-Z CLOUD, which is a deploy of `enrichment_bloomberg.py` to the scheduled 11:00Z vehicle

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-08 ~05:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked). The four things
ruling msg 31584 names, and nothing else. The act is a merge; no Lambda, no S3 write, no vendor call.

## VERDICT: SIGNED

Conditions: the merge lands only AFTER the 2026-10-08 11:00Z vehicle run, on the unchanged file, has been read by this
seat; the branch is @de25db03ea; every read below holds.

## 1. The switch-OFF run is identical to the run before -- what was compared

`round15/checks/tw-1.AC1.py`, re-run by this seat on the branch: PASS 6 of 6 arms. It runs the `daily` mode of
`enrichment_bloomberg.handler_entry` over one fixture twice in one process -- the module on the branch, and the module as
it is at commit 361b735308 read from git -- with the vendor client stubbed, the budget ledger in a temp directory and the
sink wrapped to record every call, for the switch unset, empty and `"0"`. Compared and equal in each of the three: the
ordered sequence of sink `list` / `get` / `exists` / `put` calls; the client requests; the printed lines; the returned
result dict. `rivalfunds.history_owed` is not imported on that path (a sentinel module that raises on use is planted).
The diff of the file, read by this seat: +113, -0; one `import os`; one block of new constants and functions after
`_market_range`; and three lines before the daily path's final `return`:
`owed_mode = _history_owed_switch()` / `if owed_mode and mkt["status"] == "OK":` / the call.
Not compared: a real vehicle run (none is made by a check; the first scheduled run after the merge is the read, item 4).

## 2. The switch

- Name: environment variable `RIVALFUNDS_HISTORY_OWED`, read once per run by `_history_owed_switch()`.
- Default: OFF. It is a value only for exactly `print` or `ask`; unset, empty, `"0"`, `"1"`, `"ASK"`, `"Print"` and any
  other string are OFF.
- Where it is set on this box, measured 2026-10-08 ~05:4xZ: NOWHERE. The process, User and Machine environments read
  empty for it (control: the User PATH reads 1,195 characters through the same call). In the repository (one ripgrep over the working tree; gitignored
  files are not searched by it) the name appears in 4 files: the decomposition, this cell's order and its two check files; in no `.cmd`, no file under
  `integrations/`, no Terraform and no product module other than the one this merge adds it to (which is on the branch).
  The scheduled task's own definition was NOT opened; it launches `scheduled_daily_pull.cmd`, which does not name the
  variable.
- `ask` is the state Andrew's recorded answer gates. Nothing sets it before 1.0.0_SA_CTO~Z relays that answer; this
  seat sets neither value without that relay, and turning `print` on is asked of the CTO first as well.

## 3. `print`

Read from the code and graded by `tw-1.AC2.py` arm (a) (PASS on the branch): after a daily pull whose status is OK it
calls `history_owed.owed(s, date)` and prints ONE line, `HISTORY OWED: owed <units> units, <securities> securities, <dates>
dates; asked 0 (request off); carried <units>`. 0 vendor requests beyond the daily pull's own; 0 `bbg_budget.check_points`
calls; 0 `bbg_budget.record` calls, so 0 ledger lines; 0 puts. It does READ: the newest `security_universe` object and
the `security_market` objects of the window (on the live tables one such read took 1.8 s and returned 742 securities,
184,600 units). A failure inside the step prints `HISTORY OWED: failed ...` and leaves the daily result as it is.

## 4. The rollback, and the pair's read

- Rollback: ONE revert of the merge commit on site-Z CLOUD (`git revert -m 1 <merge>`, through `safe-commit`); the file
  returns to its bytes at 361b735308's content for that path. No object, ledger line or marker exists to undo while the
  switch is OFF.
- The pair's read: the first scheduled run after the merge (2026-10-09 11:00Z if the merge lands today after 11:00Z).
  This seat reads that day's vehicle log and states the enrichment leg's exit code and lines against 2026-10-08's: the
  same exit code, no `HISTORY OWED` line, and the `security_names` step as before. A difference is a revert the same hour.

## Known and stated, not part of the four

- Top-up rows are written with a NULL currency (the leg makes no currency lookup), so a security never pulled by the
  daily leg would have closes and no stored currency, and the chart draws no curve without one. Round 28, before `ask`.
- The leg passes the REPORT date as `owed`'s `day`; the owed window then ends one trading day earlier than the page
  day's. A unit is picked up a day late, never lost.
- `HISTORY_OWED_CAP` is 5,000 units a run, this seat's number: 184,600 units is 37 runs. The CTO has not ruled it.
- `history_owed.py` (RIV-ho-1) is merged @aca932cd3f, so the lazy import resolves if the switch is ever turned on.
